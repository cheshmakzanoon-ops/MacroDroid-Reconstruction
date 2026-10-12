#!/usr/bin/env python3
"""Measured isolated integration with the active oracle and only one compiled target.

No full source tree or APK is copied or built. Original getters come from the exact
active signed APK; the tested primary comes from a fresh production transplant.
The eventual signed-APK packaging check remains a separate, pending full-build gate.
"""
from datetime import datetime, timezone
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback
import zipfile

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
OVERLAY = BASE / 'overlay-01/project'
ACTIVE = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
JDK = BASE.parent / 'tooling/jdk21/bin'
JAR = BASE.parent / 'current/MacroDroid_v9/tools/lib/jadx-r2721.4574686-all.jar'
ORIGINAL_APK = BASE.parent / 'recovered/automation android app'
SIGNED_APK = ACTIVE / 'dist/MacroDroid-5.67.8-v9-hybrid.apk'
GETTER_DEX = ACTIVE / 'build/hybrid/classes3.dex'
USED = ['source/java/recovered/ui/DayTriggerValueMethods.java', 'source/java-method-map.json', 'source/ui-methods.json',
        'test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java',
        'tests/java/DayTriggerParityCases.java', 'tests/java/DayNumericControlHarness.java', 'tests/java/UiParityTests.java',
        'tools/src/ExtractOracle.java', 'tests/fixtures/original-dependencies.json', 'tests/fixtures/day-numeric-mutants.json',
        'ui_mutation_catalog.py', 'day_numeric_dex_controls.py']


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def inventory(root):
    return {p.relative_to(root).as_posix(): identity(p) for p in sorted(root.rglob('*')) if p.is_file()}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True)
    args = parser.parse_args(); output = Path(args.output).resolve()
    assert not output.exists()
    assert shutil.disk_usage(BASE).free >= 128 * 1024 * 1024
    output.mkdir(parents=True)
    (output / 'executed-driver.py').write_bytes(Path(__file__).read_bytes())
    result = {'schema': 1, 'passed': False, 'status': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(),
              'commands': [], 'active_paths_changed': [], 'full_source_copy': False, 'app_build_started': False,
              'signed_numeric_primary_packaging_verified': False, 'androidRuntime': False}

    def save():
        (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')

    def run(folder, name, argv, expected=0, timeout=120):
        folder.mkdir(parents=True, exist_ok=True)
        stdout, stderr = folder / (name + '.stdout.log'), folder / (name + '.stderr.log')
        assert not stdout.exists() and not stderr.exists()
        at, tick = datetime.now(timezone.utc).isoformat(), time.monotonic(); code = None
        try:
            with stdout.open('xb') as out, stderr.open('xb') as err:
                code = subprocess.run(list(map(str, argv)), cwd=output, stdout=out, stderr=err, timeout=timeout,
                                      env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}).returncode
        finally:
            result['commands'].append({'name': name, 'argv': list(map(str, argv)), 'started_utc': at,
                'finished_utc': datetime.now(timezone.utc).isoformat(), 'duration_seconds': time.monotonic() - tick,
                'timeout_seconds': timeout, 'returncode': code,
                'stdout': {'path': stdout.relative_to(output).as_posix(), **identity(stdout)},
                'stderr': {'path': stderr.relative_to(output).as_posix(), **identity(stderr)}})
            save()
        assert code == expected, name + ': ' + stderr.read_text(errors='replace')[-2000:]
        return code

    try:
        inputs = output / 'inputs'; project = inputs / 'project'; production = inputs / 'production'
        source_pins = {}
        for relative in USED:
            source, target = OVERLAY / relative, project / relative
            target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(source, target)
            source_pins[str(source)] = identity(source)
        for relative in ['build.py', 'constructor_owner.py', 'ui_runtime_policy.py', 'tests/java/BytecodeOracle.java', 'tools/src/InspectMethod.java']:
            source, target = ACTIVE / relative, production / relative
            target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(source, target)
            source_pins[str(source)] = identity(source)
        assert identity(production / 'tests/java/BytecodeOracle.java')['sha256'] == 'd91ddcd8ec3d67d41d69b8252835e747c2cad2c6d5ea898323794ceec30e6b56'
        shutil.copyfile(BASE / 'CompareOriginalFixture.java', inputs / 'CompareOriginalFixture.java')
        baseline_fixture = inputs / 'prior-original-fixture.dex'
        shutil.copyfile(BASE / 'overlay-01/baseline/tests/fixtures/original-methods.dex', baseline_fixture)
        sys.path[:0] = [str(project), str(production)]
        import build
        import day_numeric_dex_controls as numeric
        import ui_mutation_catalog as catalog
        import ui_runtime_policy
        entry = numeric.target_entry(project)
        assert identity(production / 'build.py')['sha256'] == 'dd599090fc075fed0835875937a2c2b76d91381936c26f4275f876edf47345f0'
        assert identity(production / 'constructor_owner.py')['sha256'] == 'b77672c0fb1cca53a2cb88280c2688c93fd6a95f95ee0325cabdddad00f58014'
        index = json.loads((ACTIVE / 'source/class-index.json').read_text())
        wanted_types = {numeric.TARGET, *(key.split('->', 1)[0] for key in numeric.GETTERS)}
        selected = {key: row for key, row in index.items() if row['descriptor'] in wanted_types}
        assert len(selected) == 4
        for row in selected.values():
            source, target = ACTIVE / row['path'], production / row['path']
            assert identity(source)['sha256'] == row['sha256']
            target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(source, target)
            source_pins[str(source)] = identity(source)
        numeric.write_json(production / 'source/class-index-selected.json', selected)
        numeric.write_json(inputs / 'source-pins.json', source_pins)
        external = {str(p): identity(p) for p in [ORIGINAL_APK, SIGNED_APK, GETTER_DEX, JAR, JDK / 'java', JDK / 'javac', JDK.parent / 'release']}
        assert external[str(ORIGINAL_APK)]['sha256'] == '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'
        assert external[str(SIGNED_APK)]['sha256'] == '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'
        assert external[str(JAR)]['sha256'] == '354b10af74c09f5d2ab139def4231f0906dc6cc75738b1057e5a8263a412848e'
        with zipfile.ZipFile(SIGNED_APK) as archive:
            assert hashlib.sha256(archive.read('classes3.dex')).hexdigest() == external[str(GETTER_DEX)]['sha256']
        numeric.write_json(inputs / 'external-identities.json', external)
        base_host, base_tools = ACTIVE / 'build/java/hostclasses', ACTIVE / 'tools/classes'
        classpath_before = {'host': inventory(base_host), 'tools': inventory(base_tools)}
        numeric.write_json(inputs / 'classpath-identities.json', classpath_before)
        host, tools = output / 'hostclasses', output / 'harnessclasses'; host.mkdir(); tools.mkdir()
        run(output, 'compile-production-level-helper-and-host', [JDK / 'javac', '--release', '8', '-g:none', '-cp', base_host, '-d', host,
                project / 'test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java', project / catalog.DAY_HELPER_PATH])
        assert identity(host / numeric.HELPER_CLASS)['sha256'] == numeric.HELPER_CLASS_SHA256
        for relative in ['defpackage/EngineRuntime.class', 'defpackage/EngineRuntime$Dispatch.class', 'defpackage/TestClock.class']:
            target = host / relative; target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(base_host / relative, target)
            assert identity(target) == identity(base_host / relative)
        cp = os.pathsep.join(map(str, [JAR, host, base_host, base_tools]))
        run(output, 'compile-active-oracle-and-integrated-harness', [JDK / 'javac', '-cp', cp, '-d', tools,
                production / 'tests/java/BytecodeOracle.java', production / 'tools/src/InspectMethod.java',
                project / 'tools/src/ExtractOracle.java', inputs / 'CompareOriginalFixture.java',
                *[project / 'tests/java' / (name + '.java') for name in ('UiParityTests', 'DayTriggerParityCases', 'DayNumericControlHarness')]])
        cp = os.pathsep.join(map(str, [JAR, host, tools, base_host, base_tools]))
        run(output, 'extract-exact-original-fixture', [JDK / 'java', '-Xverify:all', '-Xmx768m', '-cp', cp, 'ExtractOracle', project, ORIGINAL_APK])
        fixture = project / 'tests/fixtures/original-methods.dex'
        run(output, 'recreate-prior-fixture-from-new-selection', [JDK / 'java', '-Xverify:all', '-Xmx512m', '-cp', cp, 'CompareOriginalFixture',
                baseline_fixture, fixture, output / 'recreated-prior-fixture.dex', output / 'fixture-invariance.json'])
        extraction = json.loads((project / 'reports/original-fixture-extraction.json').read_text())
        assert extraction['registered_methods'] == 1243 and extraction['dependency_methods'] == 3
        assert extraction['methods'] == 1246 and extraction['classes'] == 607
        assert set(extraction['dependency_keys']) == set(numeric.GETTERS)
        registry = json.loads((project / 'source/java-method-map.json').read_text())
        assert len(registry) == 1243 and len({r['target'] for r in registry}) == 605
        positive_dex, binding = numeric.compile_target(build, production, selected, entry, host / numeric.HELPER_CLASS,
                output / 'positive-pipeline', run, JDK / 'java', JAR)
        assert identity(positive_dex)['sha256'] == '867e137f65908d8360f307cdd0f23b3f910e5606d6b5916f876e85186b813b47'
        cfg = {'schema': 1, 'originalFixture': {'path': str(fixture), 'sha256': numeric.sha(fixture)},
               'rebuiltApk': {'path': str(SIGNED_APK), 'sha256': numeric.sha(SIGNED_APK)},
               'rebuiltGetterDex': {'path': str(GETTER_DEX), 'sha256': numeric.sha(GETTER_DEX), 'apk_member': 'classes3.dex'},
               'targetDex': {'path': str(positive_dex), 'sha256': numeric.sha(positive_dex)},
               'classPins': numeric.class_pins(host, tools)}

        def execute(name, config, expected=0, override=None):
            folder = output / name; folder.mkdir()
            config_path, report_path = folder / 'config.json', folder / 'result.json'; numeric.write_json(config_path, config)
            runtime_cp = (str(override) + os.pathsep if override else '') + cp
            run(folder, 'execute', [JDK / 'java', *ui_runtime_policy.JVM_FLAGS, '-Xmx512m', '-cp', runtime_cp,
                    'DayNumericControlHarness', config_path, report_path], expected)
            return json.loads(report_path.read_text()) if report_path.exists() else None

        positive = execute('positive', cfg); numeric.validate_positive(positive)
        java_controls = []
        jobs = catalog.load_day_mutations(project)
        for job in jobs:
            name = job['name'].removeprefix('day-numeric-'); folder = output / ('java-fault-' + name)
            source = folder / 'source/recovered/ui/DayTriggerValueMethods.java'; source.parent.mkdir(parents=True); source.write_text(job['mutant'])
            classes = folder / 'classes'; classes.mkdir()
            run(folder, 'compile-fault', [JDK / 'javac', '--release', '8', '-g:none', '-cp', host, '-d', classes, source])
            compiled = classes / numeric.HELPER_CLASS
            assert numeric.sha(compiled) != numeric.HELPER_CLASS_SHA256
            altered = copy.deepcopy(cfg); altered['classPins'] = numeric.class_pins(host, tools, classes)
            observed = execute('java-fault-' + name + '-observation', altered, 3, classes)
            numeric.validate_fault(positive, observed, job['required_cases'], numeric.JAVA_FAILURE_COUNTS[name], 'java')
            java_controls.append({'name': name, 'passed': True, 'mismatches': observed['mismatchCount'],
                                  'required_cases': job['required_cases'], 'source': identity(source), 'class': identity(compiled)})
        dex_controls = []
        for name in ('integer-zero', 'decimal-zero'):
            compiled = output / ('java-fault-' + name) / 'classes' / numeric.HELPER_CLASS
            dex, fault_binding = numeric.compile_target(build, production, selected, entry, compiled,
                    output / (name + '-pipeline'), run, JDK / 'java', JAR)
            altered = copy.deepcopy(cfg); altered['targetDex'] = {'path': str(dex), 'sha256': numeric.sha(dex)}
            observed = execute(name + '-dex-fault', altered, 3)
            required = next(j['required_cases'] for j in jobs if j['name'] == 'day-numeric-' + name)
            numeric.validate_fault(positive, observed, required, numeric.JAVA_FAILURE_COUNTS[name], 'rebuilt')
            dex_controls.append({'name': name, 'passed': True, 'mismatches': observed['mismatchCount'], 'pipeline': fault_binding})
        substituted = copy.deepcopy(cfg); substituted['targetDex'] = copy.deepcopy(cfg['originalFixture'])
        assert execute('original-as-rebuilt-rejected', substituted, 1) is None
        assert 'Original fixture cannot masquerade as rebuilt target' in (output / 'original-as-rebuilt-rejected/execute.stderr.log').read_text()
        wrong = copy.deepcopy(cfg); wrong['classPins'][numeric.HELPER_NAME]['sha256'] = '0' * 64
        assert execute('wrong-helper-class-rejected', wrong, 1) is None
        assert 'Wrong input identity: class ' + numeric.HELPER_NAME in (output / 'wrong-helper-class-rejected/execute.stderr.log').read_text()
        restored = execute('positive-restoration', cfg); numeric.validate_positive(restored)
        assert (output / 'positive/result.json').read_bytes() == (output / 'positive-restoration/result.json').read_bytes()
        assert all(identity(Path(path)) == pin for path, pin in source_pins.items())
        assert all(identity(Path(path)) == pin for path, pin in external.items())
        assert {'host': inventory(base_host), 'tools': inventory(base_tools)} == classpath_before
        result.update(passed=True, status='TARGETED_NUMERIC_INTEGRATION_THREE_PATH_CONTROLS_PASSED',
                      recovered_methods=1243, registered_classes=605, original_fixture_methods=1246, original_fixture_classes=607,
                      original_fixture_registered_methods=1243, original_fixture_dependencies=3,
                      original_fixture=extraction, old_fixture_recreated_byte_exact=True,
                      numeric_cases=1291, numeric_input_inventory_sha256=catalog.DAY_INPUT_INVENTORY_SHA256,
                      execution_paths=3, original_instruction_count=32, rebuilt_instruction_count=25, conditional_edges_per_path=4,
                      java_faults=java_controls, actual_dex_faults=dex_controls, provenance_controls_rejected=2,
                      positive_restoration_byte_exact=True, positive_pipeline=binding,
                      original_fixture_and_external_inputs_unchanged=True, existing_classpath_files_unchanged=912,
                      ui_positive_and_91_controls_pending=True, full_signed_build_and_16_gates_pending=True)
        # Publish only the freshly measured fixture into the private overlay.
        shutil.copyfile(fixture, OVERLAY / 'tests/fixtures/original-methods.dex')
        provenance = {'origin': 'User-uploaded APK', 'original_apk_sha256': extraction['original_apk_sha256'],
                      'fixture_sha256': extraction['fixture_sha256'], 'fixture_bytes': extraction['fixture_bytes'],
                      'methods': extraction['methods'], 'classes': extraction['classes'],
                      'registered_methods': 1243, 'dependency_methods': 3,
                      'dependency_declaration_sha256': numeric.DEPENDENCY_SHA256, 'dependency_keys': sorted(numeric.GETTERS),
                      'purpose': 'Test-only original instructions; dependencies earn no recovered-method credit. Not an application build input.',
                      'extraction': 'Fresh hash-checked ExtractOracle run directly from the exact original APK; all prior 1242-method fixture bytes independently recreated from the new selection.'}
        numeric.write_json(OVERLAY / 'tests/fixtures/provenance.json', provenance)
        numeric.write_json(output / 'new-fixture-provenance.json', provenance)
    except BaseException as error:
        result.update(status='TARGETED_NUMERIC_INTEGRATION_FAILED', error=repr(error))
        (output / 'failure.traceback.txt').write_text(traceback.format_exc())
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat(); save()
        print(json.dumps({k: v for k, v in result.items() if k not in ('commands', 'java_faults', 'actual_dex_faults')}, indent=2))


if __name__ == '__main__':
    main()
