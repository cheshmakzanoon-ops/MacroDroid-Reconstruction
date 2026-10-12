#!/usr/bin/env python3
"""Rebuild one frozen method with the bound production pipeline; retain the strict raw coverage failure."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import traceback
import zipfile

HERE = Path(__file__).resolve().parent
BASELINE_SHA = '06986104338d570dd78e4abf34f2691756f772c8f6e521769a9ebf06ea97edbe'
HOST_SHA = '38656eed5691a48b8a11dc5148dd692e813b629141cad9ece604f0588a0311ea'
UTILITY_SHA = '8d90c144d624f3f4cdf4aaff1ef30b858e45b486bee56801070a4b79a7254089'
BUILD_SHA = 'dd599090fc075fed0835875937a2c2b76d91381936c26f4275f876edf47345f0'
CONSTRUCTOR_SHA = 'b77672c0fb1cca53a2cb88280c2688c93fd6a95f95ee0325cabdddad00f58014'
CLASS_SHA = '05149221b78ddab67933f4aa8aba10330787889c9a3749d6d7296eaeb6cd6d4d'
METHOD_SHA = '4c1233b2c46c08ba5713e1194d626e29a4bd07c6891190d08ff86afd6380c376'
HELPER_SHA = '67f5a47013ffbffa67859f9103d2034b3225521d10be9d96d65acd31599d45ee'
HELPER_CLASS_SHA = '80e94baecb1ed256bced1fe81d154688ceb124bda8e535483156779118006704'
FIXTURE_SHA = '940aee4861d9bd52951ccc835e91a917bb56748b4eaad5deb8a0fa1c7d2c3254'
JAR_SHA = '354b10af74c09f5d2ab139def4231f0906dc6cc75738b1057e5a8263a412848e'
ORACLE_SHA = 'd91ddcd8ec3d67d41d69b8252835e747c2cad2c6d5ea898323794ceec30e6b56'
CLASS_PATH = 'source/smali/classes/0d/a_0dfe0f87312c8ea9.smali'
TARGET = 'Lcom/arlosoft/macrodroid/action/services/a;'
METHOD = 'invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;'
KEY = TARGET + '->' + METHOD
COVERAGE = {'instructions': 262, 'visited': 259, 'unvisitedOffsets': [232, 233, 235],
            'conditionalEdges': 46, 'conditionalEdgesVisited': 46, 'unvisitedConditionalEdges': []}


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def text_sha(value):
    return hashlib.sha256(value.encode()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--baseline-checkpoint', required=True, type=Path)
    parser.add_argument('--host-checkpoint', required=True, type=Path)
    parser.add_argument('--jdk', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve(); output.mkdir(parents=True, exist_ok=False)
    private = Path(tempfile.mkdtemp(prefix='macrodroid-video-dex-study-'))
    report = {'status': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Method-only production D8/transplant study; the strict original instruction coverage gate is unchanged.',
        'private_work': str(private), 'active_source_changed': False, 'apk_built': False,
        'android_executed': False, 'coverage_exemption_implemented': False, 'method': KEY, 'commands': []}
    jdk = args.jdk.resolve()
    env = dict(os.environ)
    removed = [key for key in ('JAVA_TOOL_OPTIONS', 'JDK_JAVA_OPTIONS', '_JAVA_OPTIONS', 'CLASSPATH') if key in env]
    for key in removed:
        env.pop(key)
    env.update(JAVA_HOME=str(jdk), PATH=str(jdk / 'bin') + os.pathsep + env.get('PATH', ''))
    report['removed_option_environment_keys'] = removed
    java, javac = jdk / 'bin/java', jdk / 'bin/javac'

    def write_report():
        save(output / 'result.json', report)

    def run(label, argv, folder=output, allowed=(0,)):
        folder.mkdir(parents=True, exist_ok=True)
        command = [str(value) for value in argv]
        stdout, stderr = folder / (label + '.stdout.txt'), folder / (label + '.stderr.txt')
        started = time.monotonic()
        with stdout.open('xb') as out, stderr.open('xb') as err:
            try:
                result = subprocess.run(command, cwd=private, env=env, stdout=out, stderr=err, timeout=300)
                code, timed_out = result.returncode, False
            except subprocess.TimeoutExpired:
                code, timed_out = 124, True
        row = {'label': label, 'argv': command, 'returncode': code, 'timed_out': timed_out,
            'timeout_seconds': 300, 'seconds': round(time.monotonic() - started, 6),
            'stdout': {'path': stdout.relative_to(output).as_posix(), 'sha256': sha(stdout)},
            'stderr': {'path': stderr.relative_to(output).as_posix(), 'sha256': sha(stderr)}}
        report['commands'].append(row); write_report()
        if code not in allowed:
            raise RuntimeError(label + ' returned ' + str(code))
        return row

    try:
        utility = HERE / 'video_method_negative_control.py'
        if sha(utility) != UTILITY_SHA:
            raise RuntimeError('Reviewed checkpoint/archive utilities changed')
        util = load_module(utility, 'video_bound_control_utilities')
        inputs = output / 'inputs'
        for relative in ('video_method_dex_study.py', 'video_method_negative_control.py', 'tests/java/VideoDexStudy.java', 'tests/java/VideoDexLauncher.java'):
            util.copy_checked(HERE / relative, inputs / relative)
        util = load_module(inputs / 'video_method_negative_control.py', 'video_frozen_control_utilities')
        baseline_root, host_root, project = args.baseline_checkpoint.resolve(), args.host_checkpoint.resolve(), args.project.resolve()
        baseline = util.checkpoint(baseline_root, BASELINE_SHA)
        host_checkpoint = util.checkpoint(host_root, HOST_SHA)
        study = baseline_root / 'evidence/reports/original-jvm-07-cast-source'
        positive = json.loads((study / 'parity.json').read_text())
        if not (positive['cases'] == 1118 and positive['failedCases'] == 0 and positive['unsupportedExecutions'] == 0 and
                positive['independentExpectedResultChecks'] == 230 and positive['expectedResultFailures'] == 0 and
                positive['instructionCoverage'] == COVERAGE and positive['passed'] is False and positive['noConstructorOwnerAdapterUsed']):
            raise RuntimeError('Frozen semantic-match/raw-coverage-failure baseline changed')
        util.copy_checked(baseline_root / 'checkpoint.json', inputs / 'baseline-checkpoint.json', BASELINE_SHA)
        util.copy_checked(host_root / 'checkpoint.json', inputs / 'host-checkpoint.json', HOST_SHA)
        util.copy_checked(baseline_root / 'source/java/recovered/ui/VideoMonitorMethods.java', inputs / 'source/java/recovered/ui/VideoMonitorMethods.java', HELPER_SHA)
        util.copy_checked(baseline_root / 'evidence/executed-harness-inputs/tests/java/BytecodeOracle.java', inputs / 'tests/java/BytecodeOracle.java', ORACLE_SHA)
        util.copy_checked(baseline_root / 'proposed-method-entry.json', inputs / 'proposed-method-entry.json')
        util.copy_checked(study / 'original-video-monitor.dex', inputs / 'original-video-monitor.dex', FIXTURE_SHA)
        util.copy_checked(study / 'compiled-harness-and-toolclasses.tar.gz', inputs / 'fixed-harness-classes.tar.gz')
        util.copy_checked(host_root / 'evidence/reports/draft-compile-02/compiled-host-classes.tar.gz', inputs / 'fixed-host-classes.tar.gz')
        for relative, digest in [('build.py', BUILD_SHA), ('constructor_owner.py', CONSTRUCTOR_SHA), (CLASS_PATH, CLASS_SHA)]:
            util.copy_checked(project / relative, inputs / 'production-pipeline' / relative, digest)
        jar = project / 'tools/lib/jadx-r2721.4574686-all.jar'
        if sha(jar) != JAR_SHA:
            raise RuntimeError('Compiler/disassembler tool identity differs')
        report['tool_jar'] = {'path': str(jar), 'bytes': jar.stat().st_size, 'sha256': JAR_SHA}
        report['jdk_inputs'] = [{'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path)}
            for path in (java, javac, jdk / 'release', jdk / 'lib/server/libjvm.so', jdk / 'lib/modules')]
        entry = json.loads((inputs / 'proposed-method-entry.json').read_text())
        if entry['target'] != TARGET or entry['method'] != METHOD or entry.get('constructor_owner_mappings') is not None:
            raise RuntimeError('Unexpected proposed method or constructor mapping')
        index = json.loads((project / 'source/class-index.json').read_text())
        selected = {key: value for key, value in index.items() if value['descriptor'] == TARGET}
        if len(selected) != 1 or next(iter(selected.values())) != {'descriptor': TARGET, 'partition': 'classes', 'path': CLASS_PATH, 'sha256': CLASS_SHA, 'methods': 4}:
            raise RuntimeError('Pinned original target index record differs')
        save(inputs / 'production-pipeline/class-index-selected.json', selected)
        report['class_index'] = {'path': str(project / 'source/class-index.json'), 'sha256': sha(project / 'source/class-index.json'), 'selected_records': 1}
        util.unpack(inputs / 'fixed-host-classes.tar.gz', private / 'fixed-host', {'classes'})
        util.unpack(inputs / 'fixed-harness-classes.tar.gz', private / 'fixed-harness', {'harnessclasses', 'toolclasses'})
        host, harness = private / 'fixed-host/classes', private / 'fixed-harness/harnessclasses'
        fixed = {'host': util.inventory(private / 'fixed-host'), 'harness': util.inventory(private / 'fixed-harness')}
        save(output / 'fixed-class-inventory.json', fixed)
        sys.path.insert(0, str(inputs / 'production-pipeline'))
        build = load_module(inputs / 'production-pipeline/build.py', 'video_bound_production_build')
        original_class = (inputs / 'production-pipeline' / CLASS_PATH).read_text()
        original_methods = build.methods(original_class)
        old = original_methods[METHOD]
        if len(original_methods) != 4 or text_sha(old) != METHOD_SHA or original_class.count(old) != 1:
            raise RuntimeError('Original selected body identity differs')
        original_helper_class = host / 'recovered/ui/VideoMonitorMethods.class'
        if sha(original_helper_class) != HELPER_CLASS_SHA:
            raise RuntimeError('Frozen javac output identity differs')
        util.copy_checked(original_helper_class, output / 'pipeline-output/host/VideoMonitorMethods.class', HELPER_CLASS_SHA)
        relocated = output / 'pipeline-output/relocated/recovered/ui/VideoMonitorMethods.class'
        relocated.parent.mkdir(parents=True)
        relocated.write_bytes(build.relocate_class(original_helper_class.read_bytes()))
        compiler_input = output / 'pipeline-output/inputs.jar'
        with zipfile.ZipFile(compiler_input, 'x') as stream:
            item = zipfile.ZipInfo('recovered/ui/VideoMonitorMethods.class', (1980, 1, 1, 0, 0, 0))
            item.external_attr = 0o100644 << 16
            stream.writestr(item, relocated.read_bytes())
        with zipfile.ZipFile(compiler_input) as stream:
            if stream.namelist() != ['recovered/ui/VideoMonitorMethods.class'] or stream.read(stream.namelist()[0]) != relocated.read_bytes():
                raise RuntimeError('Only the relocated recovered helper may be sent to D8')
        dexdir = output / 'pipeline-output/d8'; dexdir.mkdir()
        run('d8-one-helper', [java, '-Xmx512m', '-cp', jar, 'com.android.tools.r8.D8', '--release', '--no-desugaring', '--min-api', '23', '--output', dexdir, compiler_input])
        helper_dex = dexdir / 'classes.dex'
        if [item.name for item in dexdir.iterdir()] != ['classes.dex']:
            raise RuntimeError('D8 must emit exactly one DEX')
        helper_digest = build.dex_integrity(helper_dex)
        disassembly = output / 'pipeline-output/helper-smali'
        run('disassemble-one-helper', [java, '-Xmx512m', '-cp', jar, 'com.android.tools.smali.baksmali.Main', 'd', '--api', '23', '--use-locals', '-o', disassembly, helper_dex])
        helper_path = disassembly / 'recovered/ui/VideoMonitorMethods.smali'
        if [item.relative_to(disassembly).as_posix() for item in sorted(disassembly.rglob('*.smali'))] != ['recovered/ui/VideoMonitorMethods.smali']:
            raise RuntimeError('Unexpected emitted runtime/helper class')
        helpers = build.methods(helper_path.read_text())
        suffix = METHOD[METHOD.index('('):]
        expected = entry.get('helper_descriptor', entry['helper_method'] + '(' + (TARGET if entry['instance'] else '') + suffix[1:])
        if expected not in helpers:
            raise RuntimeError('Exact compiler output method descriptor is missing')
        compiled, corrections = build.restore_from_preserved_source(entry, helpers[expected], old, selected, inputs / 'production-pipeline')
        if corrections or compiled != helpers[expected]:
            raise RuntimeError('This method must require zero constructor-owner corrections')
        body = compiled.split('\n', 1)[1].rsplit('.end method', 1)[0]
        body = build.ANNOT.sub('', body)
        if 'Lrecovered/' in body or 'Ldefpackage/' in body:
            raise RuntimeError('Unexpected helper/stub reference in runtime body')
        replacement = old.splitlines()[0] + '\n' + ''.join(build.ANNOT.findall(old)) + body + '.end method'
        transplanted = original_class.replace(old, replacement, 1)
        new_methods = build.methods(transplanted)
        if set(new_methods) != set(original_methods) or any(new_methods[name] != value for name, value in original_methods.items() if name != METHOD):
            raise RuntimeError('Non-target original method changed')
        if transplanted.replace(replacement, '<SELECTED-METHOD>', 1) != original_class.replace(old, '<SELECTED-METHOD>', 1):
            raise RuntimeError('Original class content outside the selected body changed')
        smali = output / 'pipeline-output/target-smali/a.smali'; smali.parent.mkdir(); smali.write_text(transplanted)
        rebuilt = output / 'pipeline-output/rebuilt-video-monitor.dex'
        run('assemble-one-target', [java, '-Xmx512m', '-cp', jar, 'com.android.tools.smali.smali.Main', 'a', '--api', '23', '-j', '2', '-o', rebuilt, smali.parent])
        rebuilt_digest = build.dex_integrity(rebuilt)
        binding = {'method': KEY, 'original_class_sha256': CLASS_SHA, 'original_method_sha256': METHOD_SHA,
            'helper_source_sha256': HELPER_SHA, 'helper_class_sha256': HELPER_CLASS_SHA,
            'relocated_helper_class_sha256': sha(relocated), 'compiler_input_sha256': sha(compiler_input),
            'compiler_input_class_count': 1, 'host_stubs_sent_to_d8': 0, 'helper_dex_sha256': helper_digest,
            'compiled_helper_method_sha256': text_sha(helpers[expected]), 'transplanted_method_sha256': text_sha(replacement),
            'transplanted_class_sha256': text_sha(transplanted), 'rebuilt_dex_sha256': rebuilt_digest,
            'other_original_methods_unchanged': 3, 'all_non_target_class_text_unchanged': True,
            'constructor_owner_corrections': [], 'production_build_sha256': BUILD_SHA,
            'production_constructor_guard_sha256': CONSTRUCTOR_SHA, 'signed_apk_built': False}
        save(output / 'method-body-binding.json', binding)
        launcher = private / 'launcherclasses'; launcher.mkdir()
        run('compile-three-path-launcher', [javac, '-cp', os.pathsep.join(map(str, (jar, harness, host))), '-d', launcher,
            inputs / 'tests/java/VideoDexStudy.java', inputs / 'tests/java/VideoDexLauncher.java'])
        for path in launcher.rglob('*.class'):
            util.copy_checked(path, output / 'launcherclasses' / path.relative_to(launcher))
        expected_classes = util.CLASSES + ['VideoDexStudy', 'VideoDexLauncher']
        origins = []
        for name in expected_classes:
            relative = Path(name.replace('.', '/') + '.class')
            directory = launcher if (launcher / relative).is_file() else harness if (harness / relative).is_file() else host
            origins.append({'class': name, 'path': str(directory / relative), 'sha256': sha(directory / relative)})
        save(output / 'expected-class-origins.json', origins)
        input_inventory = util.inventory(inputs)
        save(output / 'input-inventory.json', input_inventory)
        classpath = os.pathsep.join(map(str, (jar, launcher, harness, host)))

        def execute(folder, selected_dex=rebuilt, expected_digest=rebuilt_digest, manifest=None, allowed=(2,)):
            folder.mkdir(parents=True)
            save(folder / 'expected-class-origins.json', origins if manifest is None else manifest)
            command = run('execute-three-path', [java, '-XX:-OmitStackTraceInFastThrow', '-Xmx512m', '-cp', classpath,
                'VideoDexLauncher', folder / 'expected-class-origins.json', folder / 'class-origins.json',
                inputs / 'proposed-method-entry.json', inputs / 'original-video-monitor.dex', selected_dex, expected_digest,
                folder / 'parity.json', folder / 'live-runtime'], folder, allowed)
            path = folder / 'parity.json'
            return command, json.loads(path.read_text()) if path.exists() else None

        command, parity = execute(output / 'positive')
        positive_ok = (command['returncode'] == 2 and parity['passed'] is False and parity['semanticMatch'] is True and
            parity['cases'] == 1118 and parity['paths'] == 3 and parity['methodKeys'] == [KEY] and
            parity['failedCases'] == 0 and parity['unsupportedExecutions'] == 0 and parity['expectedResultFailures'] == 0 and
            parity['independentExpectedResultChecks'] == 230 and parity['instructionCoverage'] == COVERAGE and
            parity['noConstructorOwnerAdapterUsed'] and parity['liveRuntimeUnchanged'] and not parity['coverageExemptionImplemented'])
        report['positive_semantic_match'] = positive_ok
        report['positive_parity_sha256'] = sha(output / 'positive/parity.json')
        report['original_coverage'] = parity['instructionCoverage']
        report['rebuilt_coverage'] = parity['rebuiltInstructionCoverage']
        if not positive_ok:
            raise RuntimeError('Three-path semantic/expected-result/runtime criteria were not satisfied')
        controls = []
        folder = output / 'controls/original-substituted-for-rebuilt'
        code, observed = execute(folder, selected_dex=inputs / 'original-video-monitor.dex', allowed=(1,))
        controls.append({'name': 'original-substituted-for-rebuilt', 'returncode': code['returncode'],
            'rejected_before_parity': observed is None and not (folder / 'live-runtime').exists() and
                'Rebuilt fixture identity differs' in (folder / 'execute-three-path.stderr.txt').read_text()})
        bad_origins = json.loads(json.dumps(origins)); bad_origins[0]['sha256'] = '0' * 64
        folder = output / 'controls/wrong-loaded-helper-hash'
        code, observed = execute(folder, manifest=bad_origins, allowed=(1,))
        controls.append({'name': 'wrong-loaded-helper-hash', 'returncode': code['returncode'],
            'rejected_before_parity': observed is None and not (folder / 'class-origins.json').exists() and
                'Wrong loaded class hash' in (folder / 'execute-three-path.stderr.txt').read_text()})
        delay_pattern = r'(?m)^([ \t]*const-wide/16[ \t]+v\d+,[ \t]*)0x1388[ \t]*$'
        if len(re.findall(delay_pattern, replacement)) != 1:
            raise RuntimeError('The exact one-body initial-delay mutant anchor is not unique')
        wrong_method = re.sub(delay_pattern, lambda match: match.group(1) + '0xfa0', replacement)
        wrong_class = transplanted.replace(replacement, wrong_method, 1)
        fault_folder = output / 'controls/rebuilt-delay-duration'
        fault_source = fault_folder / 'smali/a.smali'; fault_source.parent.mkdir(parents=True); fault_source.write_text(wrong_class)
        wrong_dex = fault_folder / 'rebuilt-delay-mutant.dex'
        run('assemble-delay-fault', [java, '-Xmx512m', '-cp', jar, 'com.android.tools.smali.smali.Main', 'a', '--api', '23', '-j', '2', '-o', wrong_dex, fault_source.parent], fault_folder)
        wrong_digest = build.dex_integrity(wrong_dex)
        code, wrong = execute(fault_folder / 'execution', selected_dex=wrong_dex, expected_digest=wrong_digest)
        fault_detected = (code['returncode'] == 2 and wrong['cases'] == 1118 and wrong['paths'] == 3 and
            wrong['failedCases'] > 0 and 'video-entry:0:false:0' in wrong['failedCaseLabels'] and
            wrong['unsupportedExecutions'] == 0 and wrong['expectedResultFailures'] == 0 and
            wrong['instructionCoverage'] == COVERAGE and wrong['noConstructorOwnerAdapterUsed'] and wrong['liveRuntimeUnchanged'])
        controls.append({'name': 'rebuilt-delay-duration', 'actual_smali_assembly_returncode': 0,
            'mutant_dex_sha256': wrong_digest, 'returncode': code['returncode'],
            'cases': wrong['cases'], 'failed_cases': wrong['failedCases'], 'unsupported_executions': wrong['unsupportedExecutions'],
            'expected_result_failures': wrong['expectedResultFailures'], 'named_failure_observed': 'video-entry:0:false:0' in wrong['failedCaseLabels'],
            'detected': fault_detected})
        restored_command, restored = execute(output / 'positive-restored')
        report['positive_restoration'] = {'returncode': restored_command['returncode'], 'entire_report_matches_before': restored == parity,
            'source_unchanged': sha(smali) == text_sha(transplanted), 'rebuilt_dex_unchanged': sha(rebuilt) == rebuilt_digest,
            'helper_class_unchanged': sha(original_helper_class) == HELPER_CLASS_SHA}
        report['controls'] = controls
        report['all_controls_passed'] = all(item.get('rejected_before_parity', item.get('detected', False)) for item in controls)
        report['fixed_class_inventory_unchanged'] = fixed == {'host': util.inventory(private / 'fixed-host'), 'harness': util.inventory(private / 'fixed-harness')}
        report['input_inventory_unchanged'] = input_inventory == util.inventory(inputs)
        report['frozen_baseline_unchanged'] = util.checkpoint(baseline_root, BASELINE_SHA) == baseline
        report['frozen_host_checkpoint_unchanged'] = util.checkpoint(host_root, HOST_SHA) == host_checkpoint
        report['jdk_inputs_unchanged'] = all(sha(Path(row['path'])) == row['sha256'] for row in report['jdk_inputs'])
        report['tool_jar_unchanged'] = sha(jar) == JAR_SHA
        restored_ok = restored_command['returncode'] == 2 and all(value is True for key, value in report['positive_restoration'].items() if key != 'returncode')
        complete = positive_ok and restored_ok and report['all_controls_passed'] and all(report[key] for key in
            ('fixed_class_inventory_unchanged', 'input_inventory_unchanged', 'frozen_baseline_unchanged', 'frozen_host_checkpoint_unchanged', 'jdk_inputs_unchanged', 'tool_jar_unchanged'))
        report['rebuilt_dex_compared'] = True
        report['method_only_semantic_and_control_study_complete'] = complete
        report['raw_original_coverage_gate_passed'] = False
        report['passed'] = False
        report['status'] = 'THREE_PATH_SEMANTIC_MATCH_CONTROLS_PASSED_RAW_COVERAGE_GATE_FAILED' if complete else 'METHOD_ONLY_THREE_PATH_STUDY_FAILED'
        return 2 if complete else 1
    except Exception as error:
        report['status'] = 'METHOD_ONLY_THREE_PATH_STUDY_FAILED'; report['passed'] = False
        report['error'] = type(error).__name__ + ': ' + str(error)
        (output / 'failure-traceback.txt').write_text(traceback.format_exc())
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat(); write_report()
        print(json.dumps({key: value for key, value in report.items() if key != 'commands'}, indent=2))


if __name__ == '__main__':
    raise SystemExit(main())
