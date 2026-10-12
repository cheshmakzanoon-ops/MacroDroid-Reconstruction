#!/usr/bin/env python3
"""Preserve the actual compiled cast-order fault that the old harness missed."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() or source.is_symlink():
        raise RuntimeError('Fresh exact regular-file copy required')
    shutil.copyfile(source, target)
    if sha(source) != sha(target) or (source.stat().st_dev, source.stat().st_ino) == (target.stat().st_dev, target.stat().st_ino):
        raise RuntimeError('Copy identity differs')


def rows(root):
    return [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)}
            for p in sorted(root.rglob('*')) if p.is_file()]


def main():
    report_root = HERE / 'reports/compiled-fault-06-cast-order-gap'
    result = json.loads((report_root / 'result.json').read_text())
    control = result['controls'][0]
    if (result['status'] != 'COMPILED_FAULT_CONTROL_GATE_FAILED' or result['passed'] is not False or
            result['controls_count'] != 1 or result['controls_detected'] != 0 or
            control['compile_returncode'] != 0 or control['failed_cases'] != 0 or
            control['unsupported_executions'] != 0 or not result['baseline_restoration']['reproduced'] or
            not all(item['rejected_before_parity'] for item in result['class_origin_controls'])):
        raise RuntimeError('The actual missed-fault outcome changed')
    destination = HERE / 'checkpoints/06-compiled-cast-order-gap'
    destination.mkdir(parents=True, exist_ok=False)
    for name in ('CAST_ORDER_CONTROL_GAP.md', 'video_method_negative_control.py', 'video_method_mutants_initial.json',
                 'tests/java/VideoMutationLauncher.java', 'freeze_video_fault_gap.py'):
        copy(HERE / name, destination / name)
    files = rows(destination)
    evidence = destination / 'evidence'
    for path in report_root.rglob('*'):
        if path.is_file():
            copy(path, evidence / 'run' / path.relative_to(report_root))
    for name in ('cast-order-fault-stdout.txt', 'cast-order-fault-stderr.txt'):
        copy(HERE / name, evidence / name)
    prior = HERE / 'checkpoints/05-expanded-original-jvm-coverage-gap/checkpoint.json'
    if sha(prior) != '1e94ebcdb8644fbada96e702e4000d0268a5b1d22d5247e6a56e55c90b8ad0fe':
        raise RuntimeError('Frozen dependency changed')
    copy(prior, evidence / 'baseline-checkpoint.json')
    evidence_files = rows(evidence)
    archive = HERE / 'checkpoints/06-compiled-cast-order-gap-evidence.tar.gz'
    if archive.exists():
        raise FileExistsError(archive)
    with tarfile.open(archive, 'w:gz') as stream:
        for item in evidence_files:
            stream.add(evidence / item['path'], arcname=item['path'], recursive=False)
    remaining = {item['path']: item for item in evidence_files}
    with tarfile.open(archive, 'r:gz') as stream:
        for member in stream:
            item = remaining.pop(member.name); data = stream.extractfile(member).read()
            if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise RuntimeError('Archive differs')
    if remaining:
        raise RuntimeError('Archive omitted evidence')
    value = {'status': 'ACTUAL_COMPILED_CAST_ORDER_FAULT_NOT_DETECTED',
        'frozen_utc': datetime.now(timezone.utc).isoformat(), 'controls': 1, 'detected': 0,
        'cases': 1111, 'mismatches': 0, 'control_gate_passed': False,
        'raw_original_coverage_gate_passed': False, 'raw_original_instructions_visited': 259,
        'raw_original_instructions': 262, 'original_unvisited_offsets': [232, 233, 235],
        'positive_source_class_and_full_report_restored': True, 'origin_controls_rejected': 2,
        'scope': 'Observed harness false negative; no active source, APK, oracle or coverage-policy changes. Follow-up correction remains separate.',
        'baseline_checkpoint_sha256': sha(prior), 'study_result_sha256': sha(report_root / 'result.json'),
        'files': files, 'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True}
    manifest = destination / 'checkpoint.json'; manifest.write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(manifest), 'sha256': sha(manifest), 'files': len(files),
                      'evidence_files': len(evidence_files), 'evidence_bundle': value['evidence_bundle']}, indent=2))


if __name__ == '__main__':
    main()
