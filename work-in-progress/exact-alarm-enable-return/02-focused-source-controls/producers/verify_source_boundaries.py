from __future__ import annotations

import argparse
import ast
import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

from run_host_attempt import ROOT, WORKING, inventory

PARENT = Path('/dev/shm/macrodroid-exact-alarm-navigation/source-01/repository')
PREFIX = 'tools/parity_journeys/'
CHANGED = {PREFIX + name for name in ('editor_journey.py', 'observed_journey.py')}
NEW = {PREFIX + name for name in ('exact_alarm_enable_return.py', 'exact_alarm_enable_return_readiness.py',
                                  'test_exact_alarm_enable_return.py', 'test_exact_alarm_enable_return_readiness.py')}


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def definitions(data):
    tree = ast.parse(data)
    return {node.name: ast.dump(node, include_attributes=False) for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef))}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('name'); args = parser.parse_args()
    out = ROOT / 'source-01/reports' / args.name; out.mkdir(parents=True, exist_ok=False)
    value = {'schema': 1, 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'status': 'INCOMPLETE', 'passed': False, 'android_executed': False}
    write(out / 'result.json', value)
    before, current = inventory(PARENT), inventory(WORKING)
    write(out / 'parent-before.json', before); write(out / 'current-before.json', current)
    try:
        receipt = json.loads((ROOT / 'source-01/preparation.json').read_bytes())
        expected = {row['path']: {key: row[key] for key in ('bytes', 'sha256', 'mode')} for row in receipt['files']}
        assert len(before) == 98 and before == expected
        assert set(current) - set(before) == NEW and not set(before) - set(current)
        actual_changes = {path for path in before if before[path] != current[path]}
        assert actual_changes == CHANGED
        assert len(current) == 102
        value.update(parent_source_files=98, replay_source_files=102, unchanged_parent_sources=96,
                     added_sources=sorted(NEW), changed_sources=sorted(CHANGED))
        delta = [{'path': path, 'before': before.get(path), 'after': current[path]} for path in sorted(CHANGED | NEW)]
        write(out / 'six-path-delta.json', delta)
        patch = ''.join(''.join(difflib.unified_diff((PARENT / relative).read_text().splitlines(True),
                        (WORKING / relative).read_text().splitlines(True), fromfile='parent/' + relative,
                        tofile='candidate/' + relative)) for relative in sorted(CHANGED))
        (out / 'dispatch.patch').write_text(patch)
        preserved = []; changed_definitions = {}
        for relative, allowed in ((PREFIX + 'editor_journey.py', {'validate_snapshot', 'compare', 'main'}),
                                 (PREFIX + 'observed_journey.py', {'readiness_adapter', 'information_adapter', 'require_plan',
                                        'required_surface', 'report_policy', 'input_identity'})):
            old, new = definitions((PARENT / relative).read_bytes()), definitions((WORKING / relative).read_bytes())
            actual = {name for name in old if old[name] != new.get(name)}
            assert actual == allowed
            added = set(new) - set(old)
            assert added == ({'exact_alarm_enable_return_plan'} if relative.endswith('observed_journey.py') else set())
            changed_definitions[relative] = sorted(actual)
            preserved.extend(relative + ':' + name for name in old if name not in actual)
        old_ready = (PARENT / (PREFIX + 'exact_alarm_readiness.py')).read_text()
        expected_ready = (old_ready.replace('REPORT_SCHEMA = 6', 'REPORT_SCHEMA = 7')
            .replace('4133e9410db84ac5636ece780b67331bf139afaa2de6b5c110c5ef5679fda85c',
                     'ca597b23d9c2d11ebce1ed3953d609189476d7179635f2a4c4068df0795f2211')
            .replace('exact_alarm_journey', 'exact_alarm_enable_return').replace('fourteen-screen', 'sixteen-screen'))
        assert (WORKING / (PREFIX + 'exact_alarm_enable_return_readiness.py')).read_text() == expected_ready
        old_alarm = definitions((PARENT / (PREFIX + 'exact_alarm_journey.py')).read_bytes())
        new_alarm = definitions((WORKING / (PREFIX + 'exact_alarm_enable_return.py')).read_bytes())
        assert old_alarm['_command_kind'] == new_alarm['_command_kind']
        preserved.append(PREFIX + 'exact_alarm_enable_return.py:_command_kind')
        write(out / 'definition-preservation.json', {'unchanged_parent_definitions': preserved,
              'changed_dispatch_definitions': changed_definitions,
              'readiness_only_changes': ['report schema', 'complete plan hash', 'plan/policy adapter module name', 'docstring screen count'],
              'exact_readiness_text_derivation': True, 'exact_global_command_classifier_ast': True})
        source = (WORKING / (PREFIX + 'exact_alarm_enable_return.py')).read_bytes()
        assignments = {node.targets[0].id: node.value for node in ast.parse(source).body if isinstance(node, ast.Assign)
                       and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)}
        embedded = ast.literal_eval(assignments['CONTRACT_BYTES'])
        contract = (ROOT / 'design-01/settings-contract.json').read_bytes()
        assert embedded == contract and len(contract) == 140449
        assert hashlib.sha256(contract).hexdigest() == '379544de4e9e5d84138959f1e1552fcc9b2e52d7264d30e324c63f2a82814c07'
        test_assignments = {node.targets[0].id: node.value for node in ast.parse((WORKING / (PREFIX + 'test_exact_alarm_enable_return.py')).read_bytes()).body
                            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)}
        fixture = ast.literal_eval(test_assignments['OFF_XML'])
        for label in ('original', 'candidate'):
            path = ROOT / 'design-01/observed-fixtures' / (label + '-after-exact-alarm-ok-acquisition-1-frame-2.xml')
            assert path.read_bytes() == fixture
        assert hashlib.sha256(fixture).hexdigest() == '44247f77da12d0c1eaddbebcd0fa5424399138a9bd995ee87a545294e678425e'
        value['embedded_contract_and_both_observed_xml_copies_exact'] = True
        collector = """from pathlib import Path
import json, sys, unittest
root=Path(sys.argv[1]); sys.path[:0]=[str(root/'tools/parity_journeys'),str(root/'project')]
suite=unittest.defaultTestLoader.discover(str(root/'tools/parity_journeys'),pattern='test_*.py')
def flat(s):
 if isinstance(s,unittest.TestSuite):
  for v in s: yield from flat(v)
 else: yield s.id()
ids=list(flat(suite));assert len(ids)==len(set(ids));print(json.dumps(ids,indent=2))
"""
        (out / 'discover.py').write_text(collector)
        commands = []; inventories = []
        for label, root in (('parent', PARENT), ('candidate', WORKING)):
            argv = [sys.executable, '-B', str(out / 'discover.py'), str(root)]
            env = os.environ.copy(); env['PYTHONDONTWRITEBYTECODE'] = '1'; env['TMPDIR'] = str(out)
            result = subprocess.run(argv, cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
            (out / (label + '-test-discovery.stdout')).write_bytes(result.stdout)
            (out / (label + '-test-discovery.stderr')).write_bytes(result.stderr)
            assert result.returncode == 0 and result.stderr == b''
            ids = json.loads(result.stdout); inventories.append(ids)
            commands.append({'argv': argv, 'cwd': str(root), 'timeout_seconds': 120, 'returncode': result.returncode,
                             'discovery_only': True, 'tests_executed': False})
        old_ids, new_ids = inventories
        assert len(old_ids) == 209 and len(new_ids) == 259 and set(old_ids) < set(new_ids)
        assert all(name.startswith(('test_exact_alarm_enable_return.', 'test_exact_alarm_enable_return_readiness.'))
                   for name in set(new_ids) - set(old_ids))
        write(out / 'test-discovery-commands.json', commands)
        value.update(parent_tests_preserved=209, new_tests_discovered=50, total_tests_discovered=259,
                     parent_test_source_files_unchanged=True)
        fixtures = json.loads(Path('/dev/shm/macrodroid-exact-alarm-navigation/checkpoints/03-corrected-source-and-host-controls/reports/inputs-before.json').read_bytes())
        fixtures = {path: row for path, row in fixtures.items() if path.endswith('/evidence.zip')}
        assert set(fixtures) == {'docs/verification/editor-journey/run-38198783416-attempt-1/evidence.zip',
                                 'docs/verification/editor-journey/run-38202401351-attempt-1/evidence.zip'}
        for relative, row in fixtures.items():
            data = (Path('/dev/shm/macrodroid-exact-alarm-navigation/workflow-01-validation/private-inputs') / relative).read_bytes()
            assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
        portable_inputs = {path: {key: row[key] for key in ('bytes', 'sha256')} for path, row in current.items()}
        portable_inputs.update(fixtures)
        write(out / 'inputs-before.json', portable_inputs)
        value['unchanged_portable_historical_zip_roles'] = fixtures
        assert inventory(PARENT) == before and inventory(WORKING) == current
        value.update(passed=True, status='SIX_PATH_SOURCE_AND_HISTORICAL_INPUT_BOUNDARIES_VERIFIED',
                     parent_sources_unchanged=True, current_sources_unchanged=True)
    except BaseException as error:
        value.update(error_type=type(error).__name__, error=str(error))
        (out / 'traceback.txt').write_text(traceback.format_exc())
    value['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    write(out / 'result.json', value)
    print(json.dumps(value))
    return 0 if value['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
