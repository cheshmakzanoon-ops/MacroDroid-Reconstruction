#!/usr/bin/env python3
"""Freeze the appended retry-delay cases with the unchanged raw coverage failure."""
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

HERE = Path(__file__).resolve().parent
BASELINE_SHA = '06986104338d570dd78e4abf34f2691756f772c8f6e521769a9ebf06ea97edbe'
MICRO_SHA = '1561b6af59ac41ea54da6b34df0f9c85af24d3d80c691763c8bb1de6c7c973fb'


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
    study = HERE / 'reports/original-jvm-13-retry-delay'
    result = json.loads((study / 'result.json').read_text())
    parity = json.loads((study / 'parity.json').read_text())
    wanted_coverage = {'instructions': 262, 'visited': 259, 'unvisitedOffsets': [232, 233, 235],
        'conditionalEdges': 46, 'conditionalEdgesVisited': 46, 'unvisitedConditionalEdges': []}
    if (result['status'] != 'ORIGINAL_JVM_GATE_FAILED' or parity['passed'] is not False or
            parity['cases'] != 1125 or parity['failedCases'] != 0 or parity['unsupportedExecutions'] != 0 or
            parity['independentExpectedResultChecks'] != 237 or parity['expectedResultFailures'] != 0 or
            parity['instructionCoverage'] != wanted_coverage or not parity['noConstructorOwnerAdapterUsed']):
        raise RuntimeError('Exact expanded observed result must remain unchanged')
    previous = HERE / 'checkpoints/07-cast-source-original-jvm-coverage-gap'
    if sha(previous / 'checkpoint.json') != BASELINE_SHA:
        raise RuntimeError('Earlier positive checkpoint changed')
    old = (previous / 'tests/java/VideoParityCases.java').read_text()
    new = (HERE / 'tests/java/VideoParityCases.java').read_text()
    suffix = '    static void run(){entryCases();ordinaryCases();faultCases();mutationCases();numericContracts();expandedResumes();nestedFailures();capturedOwnerContracts();}\n}\n'
    if not old.endswith(suffix) or not new.startswith(old[:-len(suffix)]):
        raise RuntimeError('Existing cases or observer changed')
    helper = 'source/java/recovered/ui/VideoMonitorMethods.java'
    if sha(HERE / helper) != '67f5a47013ffbffa67859f9103d2034b3225521d10be9d96d65acd31599d45ee':
        raise RuntimeError('Recovered body changed')
    destination = HERE / 'checkpoints/13-retry-delay-original-jvm-coverage-gap'
    destination.mkdir(parents=True, exist_ok=False)
    names = [path.relative_to(HERE).as_posix() for tree in ('source/java', 'test-support/java', 'tests/java')
             for path in (HERE / tree).rglob('*.java')]
    names += ['DRAFT_SCOPE.md', 'RETRY_DELAY_COVERAGE.md', 'video_original_jvm_study.py',
              'freeze_video_retry_study.py', 'proposed-method-entry.json', 'shared-baseline.json',
              'CCE_OBSERVATION_POLICY.md']
    for name in names:
        copy(HERE / name, destination / name)
    patch = ''.join(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True),
        fromfile='checkpoint07/tests/java/VideoParityCases.java', tofile='checkpoint13/tests/java/VideoParityCases.java'))
    (destination / 'retry-delay-cases.patch').write_text(patch)
    files = [row(path, destination) for path in sorted(destination.rglob('*')) if path.is_file()]
    evidence = destination / 'evidence'
    for path in study.rglob('*'):
        if path.is_file():
            copy(path, evidence / 'reports/original-jvm-13-retry-delay' / path.relative_to(study))
    for name in ('retry-delay-study-stdout.txt', 'retry-delay-study-stderr.txt'):
        copy(HERE / name, evidence / name)
    for item in json.loads((study / 'inputs.json').read_text())['files']:
        copy(Path(item['copy']), evidence / 'executed-harness-inputs' / item['path'], item['sha256'])
    copy(previous / 'checkpoint.json', evidence / 'previous-positive-checkpoint.json', BASELINE_SHA)
    copy(HERE / 'checkpoints/12-method-only-three-path/checkpoint.json', evidence / 'previous-micro-d8-checkpoint.json', MICRO_SHA)
    evidence_files = [row(path, evidence) for path in sorted(evidence.rglob('*')) if path.is_file()]
    archive = HERE / 'checkpoints/13-retry-delay-original-jvm-coverage-gap-evidence.tar.gz'
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
            if not member.isfile() or len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise RuntimeError('Evidence archive changed bytes')
    if remaining:
        raise RuntimeError('Evidence archive omitted files')
    value = {'status': 'ORIGINAL_JVM_ZERO_MISMATCHES_ORIGINAL_COVERAGE_GATE_FAILED',
        'frozen_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Seven appended retry-delay cases; 1,125 original/JVM cases match but strict original instruction coverage still fails. No active source, APK or coverage-policy change.',
        'cases': 1125, 'paths': 2, 'failed_cases': 0, 'unsupported_executions': 0,
        'independent_expected_checks': 237, 'expected_failures': 0,
        'new_cases': 7, 'existing_cases_and_observer_unchanged': True, 'helper_unchanged': True,
        'original_instruction_coverage': wanted_coverage, 'full_original_coverage_gate_passed': False,
        'registered': False, 'rebuilt_dex_compared': False, 'android_executed': False,
        'coverage_exemption_implemented': False, 'full_runtime_1_to_1_established': False,
        'prior_57_compiled_controls_reexecuted_here': False, 'prior_68_observer_controls_reexecuted_here': False,
        'previous_positive_checkpoint_sha256': BASELINE_SHA, 'previous_micro_d8_checkpoint_sha256': MICRO_SHA,
        'draft_host_dependency_checkpoint_sha256': '38656eed5691a48b8a11dc5148dd692e813b629141cad9ece604f0588a0311ea',
        'study_result_sha256': sha(study / 'result.json'), 'parity_result_sha256': sha(study / 'parity.json'),
        'files': files, 'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True}
    manifest = destination / 'checkpoint.json'; manifest.write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(manifest), 'sha256': sha(manifest), 'files': len(files),
        'evidence_files': len(evidence_files), 'evidence_bundle': value['evidence_bundle']}, indent=2))


if __name__ == '__main__':
    main()
