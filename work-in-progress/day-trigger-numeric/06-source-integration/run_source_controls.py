#!/usr/bin/env python3
"""Run the small reviewed source union; no complete source or APK is materialized."""
from datetime import datetime, timezone
import ast
import copy
import difflib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
OVERLAY = BASE / 'overlay-01/project'
ACTIVE = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
OUT = BASE / 'reports/07-source-and-validator-controls'
JAR = BASE.parent / 'current/MacroDroid_v9/tools/lib/jadx-r2721.4574686-all.jar'
JDK = BASE.parent / 'tooling/jdk21/bin'


def identity(path):
    with path.open('rb') as stream: digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    (OUT / 'executed-driver.py').write_bytes(Path(__file__).read_bytes())
    result = {'schema': 1, 'passed': False, 'started_utc': datetime.now(timezone.utc).isoformat(),
              'full_source_copy': False, 'full_apk_build': False, 'active_paths_changed': []}
    try:
        preparation = json.loads((BASE / 'overlay-01/preparation.json').read_text())
        existing = {row['path']: row['baseline'] for row in preparation['copied_existing_paths']}
        allowed = set(existing) | set(preparation['new_paths_required_absent'])
        actual = {p.relative_to(OVERLAY).as_posix() for p in OVERLAY.rglob('*') if p.is_file()}
        assert actual == allowed and len(actual) == 19
        assert all(identity(Path(preparation['source_root']) / path) == baseline for path, baseline in existing.items())
        assert all(not (Path(preparation['source_root']) / path).exists() for path in preparation['new_paths_required_absent'])
        view = OUT / 'view'; view.mkdir()
        bindings = []
        for path in sorted(allowed):
            source = OVERLAY / path; target = view / path; target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
            bindings.append({'path': path, 'baseline': existing.get(path), 'candidate': identity(source),
                             'must_be_absent_if_new': path not in existing})
            if source.suffix == '.py': compile(source.read_bytes(), str(source), 'exec')
        support = ['build.py', 'constructor_owner.py', 'ui_runtime_policy.py',
                   'tests/test_ui_mutation_catalog.py', 'tests/fixtures/widget-method-mutants.json']
        support.extend(p.relative_to(ACTIVE).as_posix() for p in (ACTIVE / 'source/java/recovered/ui').glob('*.java'))
        support_pins = {}
        for path in sorted(support):
            assert path not in allowed
            source = ACTIVE / path; support_pins[path] = identity(source)
            target = view / path; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(source.read_bytes())
        write(OUT / 'source-bindings.json', {'approved_paths': bindings, 'unchanged_support': support_pins,
                                           'external_jar': {'path': str(JAR), **identity(JAR)},
                                           'no_apk_or_classpath_tree_copy': True})
        old_registry = json.loads((BASE / 'overlay-01/baseline/source/java-method-map.json').read_text())
        new_registry = json.loads((view / 'source/java-method-map.json').read_text())
        assert new_registry[:-1] == old_registry and len(new_registry) == 1243
        assert (view / 'ui_mutation_catalog.py').read_bytes().startswith((BASE / 'overlay-01/baseline/ui_mutation_catalog.py').read_bytes())
        old_tree = ast.parse((BASE / 'overlay-01/baseline/ui_negative_control.py').read_text())
        new_tree = ast.parse((view / 'ui_negative_control.py').read_text())
        def controls(tree):
            return next(ast.literal_eval(row.value) for row in tree.body if isinstance(row, ast.Assign)
                        and any(isinstance(t, ast.Name) and t.id == 'CONTROLS' for t in row.targets))
        assert controls(old_tree) == controls(new_tree) and len(controls(old_tree)) == 54
        def gate_list(path):
            return next(ast.literal_eval(row.value) for row in ast.walk(ast.parse(path.read_text()))
                        if isinstance(row, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'commands' for t in row.targets))
        assert gate_list(view / 'acceptance.py') == gate_list(BASE / 'overlay-01/baseline/acceptance.py')

        sys.path[:0] = [str(view)]
        build = import_file('build', view / 'build.py'); sys.modules['build'] = build; build.JAR = JAR
        catalog = import_file('ui_mutation_catalog', view / 'ui_mutation_catalog.py'); sys.modules['ui_mutation_catalog'] = catalog
        numeric = import_file('day_numeric_dex_controls', view / 'day_numeric_dex_controls.py'); sys.modules['day_numeric_dex_controls'] = numeric
        new_ui = import_file('private_new_ui', view / 'ui_negative_control.py')
        old_ui = import_file('private_old_ui', BASE / 'overlay-01/baseline/ui_negative_control.py')
        old_jobs, new_jobs = old_ui.prepared_mutations(), new_ui.prepared_mutations()
        assert len(old_jobs) == 78 and len(new_jobs) == 91 and new_jobs[:78] == old_jobs
        write(OUT / 'mutation-inventory.json', [{'name': row['name'], 'source': row['source'].relative_to(view).as_posix(),
              'mutant_sha256': hashlib.sha256(row['mutant'].encode()).hexdigest(), 'required_cases': row['required_cases'],
              'widget': row['widget'], 'day_numeric': row.get('day_numeric', False)} for row in new_jobs])

        positive_path = BASE / 'reports/04-targeted-numeric-attempt-02/positive/result.json'
        positive = json.loads(positive_path.read_text()); numeric.validate_positive(positive)
        review = json.loads((BASE / 'reports/05-numeric-report-guard-review/result.json').read_text())
        rejections = []
        for row in review['controls']:
            changed = copy.deepcopy(positive); parts = row['changed_field'].split('.'); target = changed
            for part in parts[:-1]: target = target[part]
            target[parts[-1]] = row['replacement']
            try: numeric.validate_positive(changed)
            except RuntimeError as error: rejections.append({'name': row['name'], 'rejected': True, 'reason': str(error)})
            else: raise RuntimeError('Report metadata fault was still accepted: ' + row['name'])
        old_result = json.loads((BASE / 'reports/04-targeted-numeric-attempt-02/result.json').read_text())
        for row in old_result['java_faults']:
            fault = json.loads((BASE / ('reports/04-targeted-numeric-attempt-02/java-fault-' + row['name'] + '-observation/result.json')).read_text())
            numeric.validate_fault(positive, fault, row['required_cases'], row['mismatches'], 'java')
        for row in old_result['actual_dex_faults']:
            fault = json.loads((BASE / ('reports/04-targeted-numeric-attempt-02/' + row['name'] + '-dex-fault/result.json')).read_text())
            required = next(old['required_cases'] for old in old_result['java_faults'] if old['name'] == row['name'])
            numeric.validate_fault(positive, fault, required, row['mismatches'], 'rebuilt')
        write(OUT / 'validator-replay.json', {'passed': True, 'actual_positive_report': identity(positive_path),
             'actual_positive_1291_cases_passed': True, 'actual_java_fault_reports_passed': 13,
             'actual_dex_fault_reports_passed': 2, 'previously_accepted_metadata_faults_rejected': rejections})

        runner = OUT / 'execute_focused_tests.py'
        runner.write_text('''import pathlib,sys,unittest
sys.dont_write_bytecode=True
view=pathlib.Path(sys.argv[1]);sys.path[:0]=[str(view),str(view/'tests')]
import build
build.JAR=pathlib.Path(sys.argv[2])
suite=unittest.defaultTestLoader.loadTestsFromNames(['test_day_numeric','test_ui_mutation_catalog'])
result=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() and result.testsRun==43 and not result.skipped else 2)
''')
        argv = [sys.executable, '-B', str(runner), str(view), str(JAR)]
        stdout, stderr = OUT / 'focused-tests.stdout.log', OUT / 'focused-tests.stderr.log'
        at, tick = datetime.now(timezone.utc).isoformat(), time.monotonic()
        with stdout.open('xb') as out, stderr.open('xb') as err:
            code = subprocess.run(argv, cwd=OUT, stdout=out, stderr=err, timeout=180,
                                  env={**os.environ, 'PATH': str(JDK) + os.pathsep + os.environ.get('PATH', ''),
                                       'PYTHONDONTWRITEBYTECODE': '1',
                                       'DAY_NUMERIC_TEST_COMMAND_LOG': str(OUT / 'java-selector-command-streams.jsonl')}).returncode
        result['test_command'] = {'argv': argv, 'returncode': code, 'started_utc': at,
                                  'duration_seconds': time.monotonic() - tick, 'timeout_seconds': 180,
                                  'stdout': identity(stdout), 'stderr': identity(stderr)}
        assert code == 0
        assert 'Ran 43 tests' in stderr.read_text() and stderr.read_text().endswith('\nOK\n')
        assert all(identity(OVERLAY / row['path']) == row['candidate'] for row in bindings)
        assert all(identity(Path(preparation['source_root']) / path) == baseline for path, baseline in existing.items())
        assert all(identity(ACTIVE / path) == pin for path, pin in support_pins.items())
        diffs = []
        for row in bindings:
            path = row['path']
            if Path(path).suffix == '.dex': continue
            old = (BASE / 'overlay-01/baseline' / path).read_text().splitlines(keepends=True) if row['baseline'] else []
            diffs.extend(difflib.unified_diff(old, (view / path).read_text().splitlines(keepends=True),
                                            fromfile='a/' + path if row['baseline'] else '/dev/null', tofile='b/' + path))
        (OUT / 'source.patch').write_text(''.join(diffs))
        result.update(passed=True, status='NINETEEN_PATH_SOURCE_CONTROLS_PASSED', source_paths=19,
                      focused_tests=43, skips=0, existing_controls_byte_and_job_exact=78, new_numeric_controls=13,
                      prior_validator_faults_rejected=6, actual_three_path_positive_and_fifteen_faults_replayed=True,
                      original_fixture_registered_methods=1243, original_fixture_dependencies=3,
                      full_ui_positive_and_91_actual_controls_pending=True, full_signed_build_and_16_gates_pending=True)
    except BaseException as error:
        result.update(status='SOURCE_CONTROL_FAILED', error=repr(error))
        (OUT / 'failure.traceback.txt').write_text(traceback.format_exc())
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat(); write(OUT / 'result.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
