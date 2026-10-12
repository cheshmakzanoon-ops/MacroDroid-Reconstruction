#!/usr/bin/env python3
"""Independent bounded review of the frozen numeric command-evidence successor."""
from __future__ import annotations

import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import time

ROOT = Path('/dev/shm/macrodroid-numeric-final-review')
TOOLING = Path('/dev/shm/day-numeric-hosted-02/checkpoints/02-hosted-filesystem-tooling-successor')
SOURCE = Path('/dev/shm/day-numeric-hosted-02/checkpoints/01-command-filesystem-source-successor')
TOOLING_SHA = '815612f827f1b0d2bcec90bbb1ae8a35a8c76ced8f6b5f44cf413bc40b81f493'
SOURCE_SHA = 'd9ddd3e0f692c66e2cd47870ff3cf95bfa0a2b1cd50fc2fd55a3c09e66df9bcf'


def identity(path):
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or path.is_symlink():
        raise RuntimeError('Expected a regular preserved file: ' + str(path))
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'mode': '100755' if info.st_mode & 0o111 else '100644'}


def check_capsule(folder, digest):
    manifest = identity(folder / 'checkpoint.json')
    if manifest['sha256'] != digest:
        raise RuntimeError('Closed checkpoint identity differs')
    value = json.loads((folder / 'checkpoint.json').read_text())
    for row in value['files']:
        observed = identity(folder / row['path'])
        if any(observed[key] != row[key] for key in ('bytes', 'sha256')):
            raise RuntimeError('Closed payload changed: ' + row['path'])
        expected_mode = row.get('mode', '100644')
        if isinstance(expected_mode, int):
            expected_mode = '100755' if expected_mode & 0o111 else '100644'
        if observed['mode'] != expected_mode:
            raise RuntimeError('Closed payload mode changed: ' + row['path'])
    return value


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def definitions(path):
    return {node.name: ast.dump(node, include_attributes=False) for node in ast.parse(path.read_text()).body
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))}


def main():
    ROOT.mkdir(exist_ok=False)
    started = time.monotonic(); started_utc = datetime.now(timezone.utc).isoformat()
    tooling, source = check_capsule(TOOLING, TOOLING_SHA), check_capsule(SOURCE, SOURCE_SHA)
    if len(tooling['files']) != 2964 or len(source['files']) != 408:
        raise RuntimeError('Complete capsule payload inventory differs')
    runtime = TOOLING / 'source/tools/day_numeric_acceptance'
    if identity(runtime / 'verify.py')['sha256'] != '242f016afdacce4231580b92cfa8b01bc3a6420d3456d3370340a5864e971649':
        raise RuntimeError('Final verifier differs from the already inspected correction')
    left, right = definitions(runtime / 'run_acceptance.py'), definitions(SOURCE / 'project/day_numeric_dex_controls.py')
    helper_names = ('command_clock', 'command_file_stat', 'CommandStreamEvidence')
    if any(left[name] != right[name] for name in helper_names):
        raise RuntimeError('Producer helper implementations diverged')
    producer_identity = {name: hashlib.sha256(left[name].encode()).hexdigest() for name in helper_names}
    baseline = SOURCE / 'evidence/exact-failed-job-source/tools/day_numeric_acceptance/run_acceptance.py'
    old_definitions = definitions(baseline)
    if left['stop_owned_group'] != old_definitions['stop_owned_group']:
        raise RuntimeError('Existing owned process-group cleanup changed')
    inputs_delta = (TOOLING / 'tooling-derivation.patch').read_text()
    full_tests = json.loads((TOOLING / 'evidence/08-complete-tooling-discovery/result.json').read_text())
    if (full_tests['passed'] is not True or full_tests['tests'] != 92 or full_tests['returncode'] != 0
            or full_tests['source_unchanged'] is not True or full_tests['source_before'] != full_tests['source_after']):
        raise RuntimeError('Closed full tooling run is incomplete')
    for row in full_tests['source_before']:
        if any(identity(TOOLING / 'source' / row['path'])[key] != row[key] for key in ('bytes', 'sha256')):
            raise RuntimeError('Executed tooling source differs from frozen source')
    retained = json.loads((TOOLING / 'retained-fixture-index.json').read_text())
    sys.path.insert(0, str(runtime))
    import inputs
    import run_acceptance as producer
    import verify as verifier
    observed_runtime = inputs.verify_runtime_manifest('a1b6464be0603913f9fe37b0b90e7026034fd1823f3b24b949355109b9632428')
    cases = []
    case_specs = [
        ('empty', 'pass', [], 0, False),
        ('nonempty-exit-seven', 'import sys; print("retained stdout"); print("retained stderr", file=sys.stderr); sys.exit(7)', [], 7, False),
        ('child-adds-hardlink', 'import os,sys; os.link(sys.argv[1], sys.argv[2])', ['stdout', 'link'], 0, True),
        ('child-replaces-stream', 'from pathlib import Path; import sys; p=Path(sys.argv[1]); p.unlink(); p.write_text("replacement inode\\n")', ['stdout'], 0, True),
    ]
    for name, program, roles, code, rejects in case_specs:
        folder = ROOT / 'actual-controls' / name; folder.mkdir(parents=True)
        stdout, stderr = folder / 'probe.stdout.log', folder / 'probe.stderr.log'
        arguments = [str(stdout) if role == 'stdout' else str(folder / 'extra-hardlink.log') for role in roles]
        argv = [sys.executable, '-B', '-c', program, *arguments]
        row = producer.run_child(argv, folder, {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, stdout, stderr, 15)
        save(folder / 'producer-command.json', row)
        if row['returncode'] != code or row['timed_out'] is not False or ('error' in row) is not rejects:
            raise RuntimeError('Unexpected actual producer outcome: ' + name)
        evidence = row['stream_evidence']
        first = folder / 'probe.filesystem-before.log'
        witnesses = evidence['after_witnesses']
        last = folder / witnesses[-1]['path']
        artifacts = verifier.Artifacts(folder, first.stat().st_ctime_ns, last.stat().st_ctime_ns)
        reason = None
        try:
            verifier.verify_command_stream_evidence(row, '', 'probe', artifacts)
        except Exception as error:
            reason = type(error).__name__ + ': ' + str(error)
        if (reason is not None) is not rejects:
            raise RuntimeError('Unexpected actual live receipt verification: ' + name)
        before_stats = {role: evidence['streams'][role]['initial_stat'] for role in ('stdout', 'stderr')}
        result = {'case': name, 'returncode': code, 'producer_error_observed': 'error' in row,
                  'receipt_rejected': rejects, 'reason': reason,
                  'coarse_initial_mtime_before_fine_open': {role: before_stats[role]['mtime_ns'] < evidence['streams'][role]['open_started']['unix_ns']
                                                          for role in ('stdout', 'stderr')},
                  'all_owned_streams_closed': all('closed' in evidence['streams'][role] for role in ('stdout', 'stderr')),
                  'actual_python_child_executed': True, 'application_or_java_or_android_executed': False}
        if result['all_owned_streams_closed'] is not True:
            raise RuntimeError('An owned stream lacks closure evidence')
        save(folder / 'review-result.json', result)
        cases.append(result)
    for name in ('checkpoint.json', 'nine-path-bindings.json', 'tooling-derivation.patch', 'retained-fixture-index.json'):
        destination = ROOT / 'reviewed-tooling' / name; destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(TOOLING / name, destination)
    for name in ('result.json', 'stdout.log', 'stderr.log'):
        original = TOOLING / 'evidence/08-complete-tooling-discovery' / name
        if original.exists():
            target = ROOT / 'reviewed-tooling/full-92-tests' / name; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, target)
    for name in ('run_acceptance.py', 'verify.py', 'README.md'):
        target = ROOT / 'reviewed-tooling/source' / name; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(runtime / name, target)
    shutil.copy2(Path(__file__), ROOT / 'executed-review-numeric-successor.py')
    if check_capsule(TOOLING, TOOLING_SHA) != tooling or check_capsule(SOURCE, SOURCE_SHA) != source:
        raise RuntimeError('Closed inputs changed during review')
    result = {'status': 'BOUNDED_NUMERIC_FILESYSTEM_SUCCESSOR_REVIEW_PASSED',
              'started_utc': started_utc, 'finished_utc': datetime.now(timezone.utc).isoformat(),
              'seconds': time.monotonic() - started, 'tooling_checkpoint_sha256': TOOLING_SHA,
              'source_checkpoint_sha256': SOURCE_SHA, 'all_tooling_payloads_verified': 2964,
              'all_source_payloads_verified': 408, 'all_closed_inputs_unchanged': True,
              'final_verifier_equals_previously_reviewed_correction': True,
              'producer_helper_asts_identical': producer_identity, 'owned_process_group_cleanup_ast_unchanged': True,
              'closed_full_tool_tests': {'tests': 92, 'seconds': full_tests['unittest_seconds'], 'passed': True},
              'independent_actual_python_controls': cases,
              'application_build_executed': False, 'android_executed': False,
              'full_runtime_1_to_1_established': False,
              'activation_scope': 'Eligible only for the separately reviewed isolated numeric host workflow. Active application source and APK promotion remain pending actual full acceptance.',
              'metadata_scope': 'The four independent receipt checks use their original live files. Copied archived fixture metadata is retained verbatim and is not substituted into a live-stat replay.'}
    save(ROOT / 'result.json', result)
    files = [{'path': p.relative_to(ROOT).as_posix(), **identity(p)} for p in sorted(ROOT.rglob('*')) if not p.is_dir()]
    checkpoint = {'schema': 1, 'status': result['status'],
                  'repo_target': 'docs/verification/day-numeric-filesystem-successor/root-review',
                  'active_changes': False, 'application_build_executed': False, 'android_executed': False,
                  'files': files, 'result': result}
    save(ROOT / 'checkpoint.json', checkpoint)
    print(json.dumps({'checkpoint': str(ROOT / 'checkpoint.json'), **identity(ROOT / 'checkpoint.json'),
                      'files': len(files), 'payload_bytes': sum(row['bytes'] for row in files), 'result': result}, indent=2))


if __name__ == '__main__':
    main()
