#!/usr/bin/env python3
"""Freeze expanded cases separately; preserve the unchanged original coverage failure."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(path, base):
    return {'path': path.relative_to(base).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def copy(source, target, expected=None):
    digest = expected or sha(source)
    if source.is_symlink() or sha(source) != digest:
        raise RuntimeError('Input identity changed')
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise FileExistsError(target)
    shutil.copyfile(source, target)
    if sha(target) != digest or (source.stat().st_dev, source.stat().st_ino) == (target.stat().st_dev, target.stat().st_ino):
        raise RuntimeError('Exact non-hardlinked copy failed')


def main():
    study = HERE / 'reports/original-jvm-07-cast-source'
    result = json.loads((study / 'result.json').read_text())
    parity = json.loads((study / 'parity.json').read_text())
    if (result['status'] != 'ORIGINAL_JVM_GATE_FAILED' or parity['passed'] is not False or
            parity['cases'] != 1118 or parity['failedCases'] != 0 or parity['unsupportedExecutions'] != 0 or
            parity['independentExpectedResultChecks'] != 230 or parity['expectedResultFailures'] != 0 or
            parity['instructionCoverage']['unvisitedOffsets'] != [232, 233, 235] or
            parity['instructionCoverage']['unvisitedConditionalEdges'] != []):
        raise RuntimeError('Exact expanded observed result must remain unchanged')
    destination = HERE / 'checkpoints/07-cast-source-original-jvm-coverage-gap'
    destination.mkdir(parents=True, exist_ok=False)
    names = [path.relative_to(HERE).as_posix() for tree in ('source/java', 'test-support/java', 'tests/java')
             for path in (HERE / tree).rglob('*.java')]
    names += ['DRAFT_SCOPE.md', 'RECOVERY_STATUS.md', 'compile_video_draft.py', 'freeze_video_draft.py',
              'video_original_jvm_study.py', 'freeze_video_cce_study.py', 'proposed-method-entry.json', 'shared-baseline.json', 'video_exception_conformance.py', 'CCE_OBSERVATION_POLICY.md']
    for name in names:
        copy(HERE / name, destination / name)
    files = [row(path, destination) for path in sorted(destination.rglob('*')) if path.is_file()]
    evidence = destination / 'evidence'
    for path in study.rglob('*'):
        if path.is_file():
            copy(path, evidence / 'reports/original-jvm-07-cast-source' / path.relative_to(study))
    for name in ('cast-source-study-stdout.txt', 'cast-source-study-stderr.txt'):
        copy(HERE / name, evidence / name)
    inputs = json.loads((study / 'inputs.json').read_text())['files']
    for item in inputs:
        copy(Path(item['copy']), evidence / 'executed-harness-inputs' / item['path'], item['sha256'])
    controls = HERE / 'reports/exception-conformance-07'
    conformance = json.loads((controls / 'result.json').read_text())
    if conformance['status'] != 'ALL_68_EXACT_EXCEPTION_OBSERVATION_CONTROLS_PASSED' or conformance['controls'] != 68:
        raise RuntimeError('Exact observation controls required')
    for path in controls.rglob('*'):
        if path.is_file():
            copy(path, evidence / 'reports/exception-conformance-07' / path.relative_to(controls))
    for name in ('exception-controls-stdout.txt', 'exception-controls-stderr.txt'):
        copy(HERE / name, evidence / name)
    copy(HERE / 'checkpoints/06-compiled-cast-order-gap/checkpoint.json', evidence / 'previous-compiled-fault-gap-checkpoint.json',
         'a55dcbd316ce139b64f43acc05444b21bcd18230ff1ddf21405462992c3d7192')
    evidence_files = [row(path, evidence) for path in sorted(evidence.rglob('*')) if path.is_file()]
    archive = HERE / 'checkpoints/07-cast-source-original-jvm-coverage-gap-evidence.tar.gz'
    if archive.exists():
        raise FileExistsError(archive)
    with tarfile.open(archive, 'w:gz') as stream:
        for item in evidence_files:
            stream.add(evidence / item['path'], arcname=item['path'], recursive=False)
    remaining = {item['path']: item for item in evidence_files}
    with tarfile.open(archive, 'r:gz') as stream:
        for member in stream:
            item = remaining.pop(member.name)
            data = stream.extractfile(member).read()
            if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise RuntimeError('Evidence archive changed bytes')
    if remaining:
        raise RuntimeError('Evidence archive omitted files')
    checkpoint = {'status': 'ORIGINAL_JVM_ZERO_MISMATCHES_ORIGINAL_COVERAGE_GATE_FAILED',
        'frozen_utc': datetime.now(timezone.utc).isoformat(),
        'scope': '1,118 original/JVM cases pass; full original instruction coverage explicitly fails. No active source or APK changes.',
        'cases': 1118, 'failed_cases': 0, 'unsupported_executions': 0,
        'independent_expected_checks': 230, 'expected_failures': 0,
        'separate_exception_observation_controls': 68, 'observation_control_app_executions': 0,
        'original_instruction_coverage': parity['instructionCoverage'],
        'full_original_coverage_gate_passed': False, 'registered': False,
        'rebuilt_dex_compared': False, 'android_executed': False, 'full_runtime_1_to_1_established': False,
        'draft_host_dependency_checkpoint_sha256': '38656eed5691a48b8a11dc5148dd692e813b629141cad9ece604f0588a0311ea',
        'study_result_sha256': sha(study / 'result.json'), 'parity_result_sha256': sha(study / 'parity.json'),
        'files': files, 'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True}
    manifest = destination / 'checkpoint.json'
    manifest.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(manifest), 'sha256': sha(manifest), 'files': len(files),
        'evidence_files': len(evidence_files), 'evidence_bundle': checkpoint['evidence_bundle']}, indent=2))


if __name__ == '__main__':
    main()
