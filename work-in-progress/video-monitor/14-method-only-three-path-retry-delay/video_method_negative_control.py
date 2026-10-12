#!/usr/bin/env python3
"""Measure compiled video faults while preserving the failed raw-coverage baseline.

Exit 2 by itself never detects a mutant: the unchanged baseline already exits 2
for its three unvisited handler instructions. A control needs actual named
original/JVM mismatches, unchanged original coverage, no unsupported executions,
and zero original expected-result failures. Exact baseline restoration is checked.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tarfile
import tempfile
import time
import traceback

HERE = Path(__file__).resolve().parent
HOST_CHECKPOINT_SHA = '38656eed5691a48b8a11dc5148dd692e813b629141cad9ece604f0588a0311ea'
HELPER_SHA = '67f5a47013ffbffa67859f9103d2034b3225521d10be9d96d65acd31599d45ee'
FIXTURE_SHA = '940aee4861d9bd52951ccc835e91a917bb56748b4eaad5deb8a0fa1c7d2c3254'
ORACLE_SHA = 'd91ddcd8ec3d67d41d69b8252835e747c2cad2c6d5ea898323794ceec30e6b56'
METHOD = 'Lcom/arlosoft/macrodroid/action/services/a;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;'
HELPER = 'recovered.ui.VideoMonitorMethods'
CLASSES = [HELPER, 'BytecodeOracle', 'UiParityTests', 'VideoParityCases', 'VideoParityStudy',
    'defpackage.VideoControl', 'defpackage.VideoFile', 'com.arlosoft.macrodroid.action.services.a',
    'com.arlosoft.macrodroid.action.services.BaseVideoRecordingService',
    'com.arlosoft.macrodroid.action.services.BaseVideoRecordingService$a',
    'android.content.Context', 'android.os.Environment', 'android.os.ParcelFileDescriptor',
    'defpackage.sz6', 'defpackage.dt9', 'defpackage.d31', 'defpackage.u2f', 'defpackage.e6d',
    'defpackage.kjf', 'defpackage.jb3', 'defpackage.v93', 'defpackage.blg', 'defpackage.qnc',
    'defpackage.rff', 'defpackage.i93', 'defpackage.jn6', 'defpackage.at9', 'defpackage.zp4', 'defpackage.m47', 'defpackage.ad4']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def copy_checked(source, target, digest=None):
    digest = digest or sha(source)
    if source.is_symlink() or sha(source) != digest:
        raise RuntimeError('Input differs: ' + str(source))
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise FileExistsError(target)
    shutil.copyfile(source, target)
    if sha(target) != digest or (source.stat().st_dev, source.stat().st_ino) == (target.stat().st_dev, target.stat().st_ino):
        raise RuntimeError('Exact independent copy failed')


def inventory(root):
    rows = []
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise RuntimeError('Unexpected classpath symlink')
        if path.is_file():
            rows.append({'path': path.relative_to(root).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)})
    return rows


def checkpoint(root, digest):
    if sha(root / 'checkpoint.json') != digest:
        raise RuntimeError('Frozen checkpoint identity changed')
    value = json.loads((root / 'checkpoint.json').read_text())
    for name, prefix in [('files', root), ('evidence_files', root / 'evidence')]:
        for item in value[name]:
            path = prefix / item['path']
            if path.is_symlink() or path.stat().st_size != item['bytes'] or sha(path) != item['sha256']:
                raise RuntimeError('Frozen checkpoint payload changed: ' + item['path'])
    return value


def unpack(archive, destination, allowed_roots):
    destination.mkdir(parents=True, exist_ok=False)
    seen = set()
    with tarfile.open(archive, 'r:gz') as stream:
        for member in stream:
            relative = PurePosixPath(member.name)
            if (relative.is_absolute() or '..' in relative.parts or not relative.parts or
                    relative.parts[0] not in allowed_roots or member.name in seen or chr(92) in member.name):
                raise RuntimeError('Unsafe or duplicate class archive path')
            seen.add(member.name)
            target = destination / member.name
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open('xb') as handle:
                    handle.write(stream.extractfile(member).read())
            else:
                raise RuntimeError('Nonregular class archive member')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-checkpoint', required=True, type=Path)
    parser.add_argument('--host-checkpoint', required=True, type=Path)
    parser.add_argument('--catalog', required=True, type=Path)
    parser.add_argument('--tool-jar', required=True, type=Path)
    parser.add_argument('--jdk', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve(); output.mkdir(parents=True, exist_ok=False)
    private = Path(tempfile.mkdtemp(prefix='macrodroid-video-mutants-'))
    report = {'status': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Compiled method-only original/JVM faults; baseline full instruction coverage remains failed.',
        'private_work': str(private), 'active_source_changed': False, 'apk_built': False,
        'android_executed': False, 'rebuilt_dex_compared': False, 'coverage_exemption_implemented': False,
        'method': METHOD, 'commands': [], 'controls': []}
    env = {**os.environ, 'JAVA_HOME': str(args.jdk.resolve()),
           'PATH': str(args.jdk.resolve() / 'bin') + os.pathsep + os.environ.get('PATH', '')}

    def write_report():
        save(output / 'result.json', report)

    def run(label, argv, folder):
        folder.mkdir(parents=True, exist_ok=True)
        command = [str(value) for value in argv]
        out, err = folder / (label + '.stdout.txt'), folder / (label + '.stderr.txt')
        started = time.monotonic()
        with out.open('wb') as stdout, err.open('wb') as stderr:
            try:
                result = subprocess.run(command, cwd=private, env=env, stdout=stdout, stderr=stderr, timeout=300)
                code, timed_out = result.returncode, False
            except subprocess.TimeoutExpired:
                code, timed_out = 124, True
        row = {'label': label, 'argv': command, 'returncode': code, 'timed_out': timed_out,
               'timeout_seconds': 300, 'seconds': round(time.monotonic() - started, 6),
               'stdout': {'path': out.relative_to(output).as_posix(), 'sha256': sha(out)},
               'stderr': {'path': err.relative_to(output).as_posix(), 'sha256': sha(err)}}
        report['commands'].append(row); write_report()
        return row

    try:
        for source, relative in [(Path(__file__), 'video_method_negative_control.py'),
                                 (args.catalog, 'video_method_mutants.json'),
                                 (HERE / 'tests/java/VideoMutationLauncher.java', 'tests/java/VideoMutationLauncher.java')]:
            copy_checked(source.resolve(), output / 'inputs' / relative)
        authored = inventory(output / 'inputs')
        report['authored_inputs'] = authored
        catalog = json.loads((output / 'inputs/video_method_mutants.json').read_text())
        if catalog['method'] != METHOD or catalog['helper_sha256'] != HELPER_SHA:
            raise RuntimeError('Catalog identifies a different method/source')
        baseline_root, host_root = args.baseline_checkpoint.resolve(), args.host_checkpoint.resolve()
        baseline = checkpoint(baseline_root, catalog['baseline_checkpoint_sha256'])
        host_checkpoint = checkpoint(host_root, HOST_CHECKPOINT_SHA)
        report['baseline_checkpoint_sha256'] = catalog['baseline_checkpoint_sha256']
        report['host_checkpoint_sha256'] = HOST_CHECKPOINT_SHA
        study_dir = baseline_root / 'evidence/reports' / catalog['baseline_study_directory']
        prior = json.loads((study_dir / 'result.json').read_text())
        positive = json.loads((study_dir / 'parity.json').read_text())
        coverage = {'instructions': 262, 'visited': 259, 'unvisitedOffsets': [232, 233, 235],
                    'conditionalEdges': 46, 'conditionalEdgesVisited': 46, 'unvisitedConditionalEdges': []}
        if not (prior['status'] == 'ORIGINAL_JVM_GATE_FAILED' and positive['passed'] is False
                and positive['cases'] == catalog['expected_cases'] and positive['failedCases'] == 0
                and positive['unsupportedExecutions'] == 0 and positive['expectedResultFailures'] == 0
                and positive['independentExpectedResultChecks'] == catalog['expected_independent_checks']
                and positive['instructionCoverage'] == coverage and positive['noConstructorOwnerAdapterUsed']):
            raise RuntimeError('Expected unchanged semantic-match/coverage-failure baseline required')
        jar = args.tool_jar.resolve()
        if sha(jar) != prior['tool_jar']['sha256']:
            raise RuntimeError('Tool jar differs from measured baseline')
        source = baseline_root / 'source/java/recovered/ui/VideoMonitorMethods.java'
        if sha(source) != HELPER_SHA:
            raise RuntimeError('Frozen helper source differs')
        original_source = source.read_text()
        copy_checked(study_dir / 'original-video-monitor.dex', output / 'original-video-monitor.dex', FIXTURE_SHA)
        fixture = output / 'original-video-monitor.dex'
        copy_checked(baseline_root / 'proposed-method-entry.json', output / 'proposed-method-entry.json')
        proposal = output / 'proposed-method-entry.json'
        host_archive = host_root / 'evidence/reports/draft-compile-02/compiled-host-classes.tar.gz'
        harness_archive = study_dir / 'compiled-harness-and-toolclasses.tar.gz'
        copy_checked(host_archive, output / 'fixed-host-classes.tar.gz')
        copy_checked(harness_archive, output / 'fixed-harness-classes.tar.gz')
        unpack(host_archive, private / 'fixed-host', {'classes'})
        unpack(harness_archive, private / 'fixed-harness', {'harnessclasses', 'toolclasses'})
        host, harness = private / 'fixed-host/classes', private / 'fixed-harness/harnessclasses'
        fixed = {'host': inventory(private / 'fixed-host'), 'harness': inventory(private / 'fixed-harness')}
        save(output / 'fixed-class-inventory.json', fixed)
        oracle_source = baseline_root / 'evidence/executed-harness-inputs/tests/java/BytecodeOracle.java'
        if sha(oracle_source) != ORACLE_SHA:
            raise RuntimeError('Oracle source differs from unchanged original interpreter')
        relative_helper = Path(HELPER.replace('.', '/') + '.class')
        original_class_sha = sha(host / relative_helper)
        report['fixed_helper_class_sha256'] = original_class_sha
        launcher = private / 'launcherclasses'; launcher.mkdir()
        compiled = run('compile-launcher', ['javac', '-cp', os.pathsep.join(map(str, (jar, harness, host))),
            '-d', launcher, output / 'inputs/tests/java/VideoMutationLauncher.java'], output)
        if compiled['returncode'] != 0:
            raise RuntimeError('Origin-checking launcher compilation failed')
        copy_checked(launcher / 'VideoMutationLauncher.class', output / 'VideoMutationLauncher.class')

        def origins(helper_dir):
            rows = []
            for name in CLASSES:
                rel = Path(name.replace('.', '/') + '.class')
                directory = helper_dir if name == HELPER else harness if (harness / rel).is_file() else host
                rows.append({'class': name, 'path': str(directory / rel), 'sha256': sha(directory / rel)})
            return rows

        def execute(label, helper_dir, folder, override=None):
            folder.mkdir(parents=True, exist_ok=True)
            save(folder / 'expected-class-origins.json', origins(helper_dir) if override is None else override)
            cp = os.pathsep.join(map(str, (jar, launcher, helper_dir, harness, host)))
            command = run(label, ['java', '-XX:-OmitStackTraceInFastThrow', '-Xmx512m', '-cp', cp,
                'VideoMutationLauncher', folder / 'expected-class-origins.json', folder / 'class-origins.json',
                proposal, fixture, folder / 'parity.json'], folder)
            path = folder / 'parity.json'
            return command, json.loads(path.read_text()) if path.exists() else None

        before_command, before = execute('original-jvm', host, output / 'baseline-before')
        report['baseline_before'] = {'returncode': before_command['returncode'], 'exact_frozen_parity_match': before == positive,
                                    'raw_coverage_gate_failed': True, 'reproduced': before_command['returncode'] == 2 and before == positive}
        write_report()
        if not report['baseline_before']['reproduced']:
            raise RuntimeError('Frozen semantic-match/coverage-failure baseline did not reproduce exactly')
        controls = catalog['controls']
        if not controls or len({item['name'] for item in controls}) != len(controls):
            raise RuntimeError('Controls must be nonempty and uniquely named')
        built = []
        for control in controls:
            name = control['name']
            if not name or any(char not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for char in name):
                raise RuntimeError('Invalid control name')
            folder = output / 'controls' / name; folder.mkdir(parents=True)
            candidate = original_source
            for edit in control['edits']:
                if candidate.count(edit['find']) != edit['count']:
                    raise RuntimeError('Mutation anchor count differs: ' + name)
                candidate = candidate.replace(edit['find'], edit['replace'])
            if candidate == original_source or not control['expected_failure_labels']:
                raise RuntimeError('Each mutation must change source and require a named semantic failure')
            java = private / 'mutants' / name / 'src/recovered/ui/VideoMonitorMethods.java'
            java.parent.mkdir(parents=True); java.write_text(candidate)
            copy_checked(java, folder / java.name)
            classes = java.parents[3] / 'classes'; classes.mkdir()
            compilation = run('compile', ['javac', '--release', '8', '-g:none', '-Xlint:-options', '-cp', host,
                                          '-d', classes, java], folder)
            result = {'name': name, 'reason': control['reason'], 'source_sha256': sha(java),
                'compile_returncode': compilation['returncode'], 'expected_failure_labels': control['expected_failure_labels'],
                'detected': False}
            if compilation['returncode'] == 0:
                if [item['path'] for item in inventory(classes)] != [relative_helper.as_posix()]:
                    raise RuntimeError('Compiler emitted more than one target helper class')
                built.append(classes)
                target_class = classes / relative_helper
                copy_checked(target_class, folder / 'VideoMonitorMethods.class')
                command, parity = execute('original-jvm', classes, folder)
                result['execution_returncode'] = command['returncode']
                result['class_sha256'] = sha(target_class)
                if parity is not None:
                    result.update({'cases': parity['cases'], 'failed_cases': parity['failedCases'],
                        'unsupported_executions': parity['unsupportedExecutions'], 'expected_result_failures': parity['expectedResultFailures'],
                        'failed_case_labels': parity['failedCaseLabels'],
                        'named_failures_observed': all(label in parity['failedCaseLabels'] for label in control['expected_failure_labels']),
                        'original_coverage_unchanged': parity['instructionCoverage'] == coverage})
                    result['detected'] = (command['returncode'] == 2 and parity['passed'] is False
                        and parity['cases'] == catalog['expected_cases'] and parity['paths'] == 2
                        and parity['methodKeys'] == [METHOD] and parity['failedCases'] > 0
                        and parity['unsupportedExecutions'] == 0 and parity['expectedResultFailures'] == 0
                        and parity['noConstructorOwnerAdapterUsed'] and result['named_failures_observed']
                        and result['original_coverage_unchanged'] and sha(target_class) != original_class_sha)
            report['controls'].append(result); save(folder / 'result.json', result); write_report()
            print(name + ': ' + ('DETECTED' if result['detected'] else 'CONTROL_NOT_PROVEN'), flush=True)

        origin_controls = []
        bad_hash = origins(host); bad_hash[0]['sha256'] = '0' * 64
        origin_specs = [('wrong-helper-hash', bad_hash, 'Wrong loaded class hash')]
        if built:
            origin_specs.append(('baseline-shadows-mutant', origins(built[0]), 'Wrong loaded class origin'))
        for name, manifest, error in origin_specs:
            folder = output / 'origin-controls' / name
            command, parity = execute('execute', host, folder, manifest)
            log = (folder / 'execute.stderr.txt').read_text()
            origin_controls.append({'name': name, 'returncode': command['returncode'],
                'rejected_before_parity': command['returncode'] == 1 and parity is None and error in log
                    and not (folder / 'class-origins.json').exists()})
        report['class_origin_controls'] = origin_controls
        restored_source = private / 'restored/src/recovered/ui/VideoMonitorMethods.java'
        copy_checked(source, restored_source, HELPER_SHA)
        restored = private / 'restored/classes'; restored.mkdir(parents=True)
        folder = output / 'baseline-restored'
        command = run('compile', ['javac', '--release', '8', '-g:none', '-Xlint:-options', '-cp', host,
                                 '-d', restored, restored_source], folder)
        if command['returncode'] != 0:
            raise RuntimeError('Exact source restoration compilation failed')
        copy_checked(restored / relative_helper, folder / 'VideoMonitorMethods.class')
        after_command, after = execute('original-jvm', restored, folder)
        report['baseline_restoration'] = {'returncode': after_command['returncode'],
            'source_sha256': sha(restored_source), 'class_sha256': sha(restored / relative_helper),
            'source_matches_frozen': sha(restored_source) == HELPER_SHA,
            'class_matches_frozen': sha(restored / relative_helper) == original_class_sha,
            'exact_frozen_parity_match': after == positive,
            'reproduced': after_command['returncode'] == 2 and after == positive
                and sha(restored / relative_helper) == original_class_sha,
            'full_original_coverage_gate_passed': False}
        report['fixed_class_inventory_unchanged'] = fixed == {'host': inventory(private / 'fixed-host'), 'harness': inventory(private / 'fixed-harness')}
        report['fixture_unchanged'] = sha(fixture) == FIXTURE_SHA
        report['frozen_checkpoint_unchanged'] = checkpoint(baseline_root, catalog['baseline_checkpoint_sha256']) == baseline
        report['host_checkpoint_unchanged'] = checkpoint(host_root, HOST_CHECKPOINT_SHA) == host_checkpoint
        report['authored_inputs_unchanged'] = authored == inventory(output / 'inputs')
        report['controls_count'] = len(controls)
        report['controls_detected'] = sum(item['detected'] for item in report['controls'])
        report['passed'] = (report['controls_detected'] == len(controls) and len(origin_controls) == 2
            and all(item['rejected_before_parity'] for item in origin_controls)
            and report['baseline_restoration']['reproduced'] and report['fixed_class_inventory_unchanged']
            and report['fixture_unchanged'] and report['frozen_checkpoint_unchanged']
            and report['host_checkpoint_unchanged'] and report['authored_inputs_unchanged'])
        report['status'] = 'ALL_COMPILED_FAULTS_DETECTED_EXACT_FAILED_COVERAGE_BASELINE_RESTORED' if report['passed'] else 'COMPILED_FAULT_CONTROL_GATE_FAILED'
        return 0 if report['passed'] else 2
    except Exception as error:
        report['status'] = 'COMPILED_FAULT_STUDY_FAILED'; report['passed'] = False
        report['error'] = type(error).__name__ + ': ' + str(error)
        (output / 'failure-traceback.txt').write_text(traceback.format_exc())
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat(); write_report()
        print(json.dumps({key: value for key, value in report.items() if key not in ('commands', 'controls')}, indent=2))


if __name__ == '__main__':
    raise SystemExit(main())
