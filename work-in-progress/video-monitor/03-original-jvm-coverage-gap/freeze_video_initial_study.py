#!/usr/bin/env python3
"""Preserve the zero-mismatch study and its still-failing original coverage gate."""
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
    study = HERE / 'reports/original-jvm-03-initial'
    result = json.loads((study / 'result.json').read_text())
    parity = json.loads((study / 'parity.json').read_text())
    if (result['status'] != 'ORIGINAL_JVM_GATE_FAILED' or parity['passed'] is not False or
            parity['cases'] != 1014 or parity['failedCases'] != 0 or parity['unsupportedExecutions'] != 0 or
            parity['independentExpectedResultChecks'] != 126 or parity['expectedResultFailures'] != 0 or
            parity['instructionCoverage']['unvisitedOffsets'] != [232, 233, 235] or
            parity['instructionCoverage']['unvisitedConditionalEdges'] != []):
        raise RuntimeError('Exact first observed result must remain unchanged')
    destination = HERE / 'checkpoints/03-original-jvm-coverage-gap'
    destination.mkdir(parents=True, exist_ok=False)
    names = [path.relative_to(HERE).as_posix() for tree in ('source/java', 'test-support/java', 'tests/java')
             for path in (HERE / tree).rglob('*.java')]
    names += ['DRAFT_SCOPE.md', 'RECOVERY_STATUS.md', 'compile_video_draft.py', 'freeze_video_draft.py',
              'video_original_jvm_study.py', 'freeze_video_initial_study.py', 'proposed-method-entry.json', 'shared-baseline.json']
    for name in names:
        copy(HERE / name, destination / name)
    files = [row(path, destination) for path in sorted(destination.rglob('*')) if path.is_file()]
    evidence = destination / 'evidence'
    for path in study.rglob('*'):
        if path.is_file():
            copy(path, evidence / 'reports/original-jvm-03-initial' / path.relative_to(study))
    for name in ('initial-study-stdout.txt', 'initial-study-stderr.txt'):
        copy(HERE / name, evidence / name)
    inputs = json.loads((study / 'inputs.json').read_text())['files']
    for item in inputs:
        copy(Path(item['copy']), evidence / 'executed-harness-inputs' / item['path'], item['sha256'])
    evidence_files = [row(path, evidence) for path in sorted(evidence.rglob('*')) if path.is_file()]
    archive = HERE / 'checkpoints/03-original-jvm-coverage-gap-evidence.tar.gz'
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
        'scope': '1,014 original/JVM cases pass; full original instruction coverage explicitly fails. No active source or APK changes.',
        'cases': 1014, 'failed_cases': 0, 'unsupported_executions': 0,
        'independent_expected_checks': 126, 'expected_failures': 0,
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
