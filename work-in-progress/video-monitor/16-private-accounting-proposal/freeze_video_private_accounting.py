#!/usr/bin/env python3
"""Freeze the sealed-evidence proposal and its guard controls without activation."""
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

HERE = Path(__file__).resolve().parent
VALIDATOR_SHA = '09528652694c21f8141e3ef8fe69bb506981463c3779fcdc298a2c4caa3f1d28'
PINS_SHA = '21ecda6da3a5791cd444e76821b5361ce5e7b458b74a500b00c30da73688ecdf'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def copy(source, target):
    if source.is_symlink() or not source.is_file() or target.exists():
        raise RuntimeError('Fresh regular-file copy required')
    target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(source, target)
    if sha(source) != sha(target) or (source.stat().st_dev, source.stat().st_ino) == (target.stat().st_dev, target.stat().st_ino):
        raise RuntimeError('Independent copy failed')


def rows(root):
    result = []
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise RuntimeError('Unexpected symlink')
        if path.is_file():
            result.append({'path': path.relative_to(root).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)})
    return result


def main():
    free = shutil.disk_usage(HERE).free
    if free < 64*1024*1024:
        raise SystemExit('Freeze deferred below 64 MiB; no destination created.')
    guard_root = HERE / 'reports/private-accounting-16-guards'
    final_root = HERE / 'reports/private-accounting-16-final'
    initial_root = HERE / 'reports/private-accounting-16-initial'
    guards = json.loads((guard_root / 'result.json').read_text())
    final = json.loads((final_root / 'result.json').read_text())
    initial = json.loads((initial_root / 'result.json').read_text())
    if guards['status'] != 'PRIVATE_ACCOUNTING_GUARDS_PASSED_EXACT_POSITIVE_RESTORED' or guards['passed'] is not True:
        raise RuntimeError('Actual private guard study did not pass')
    if guards['controls_count'] != 51 or guards['subprocess_controls_count'] != 4:
        raise RuntimeError('Actual guard counts differ')
    if len(guards['controls']) != 51 or len(guards['subprocess_controls']) != 4 or not all(row['rejected'] for row in guards['controls']+guards['subprocess_controls']):
        raise RuntimeError('Some actual guard was not rejected')
    if not guards['exact_positive_restoration'] or not guards['source_and_pins_unchanged']:
        raise RuntimeError('Exact private positive was not restored')
    if guards['validator_sha256'] != VALIDATOR_SHA or final['validator_sha256'] != VALIDATOR_SHA or sha(HERE / 'video_private_accounting.py') != VALIDATOR_SHA:
        raise RuntimeError('Actual final validator source identity changed')
    if guards['pins_sha256'] != PINS_SHA or final['pins_sha256'] != PINS_SHA or sha(HERE / 'private_accounting_pins.json') != PINS_SHA:
        raise RuntimeError('Independent pin identity changed')
    if final['status'] != 'PRIVATE_EXACT_ORIGINAL_ACCOUNTING_PROPOSAL_SATISFIED' or not final['proposed_accounting_satisfied'] or final['raw_original_coverage_gate_passed'] is not False or final['active_policy_changed'] is not False:
        raise RuntimeError('Private proposal scope was broadened')
    if final['original_instructions_dynamically_visited'] != 259 or final['original_instructions_statically_infeasible'] != 3 or final['original_instruction_total'] != 262 or final['additional_app_executions'] != 0:
        raise RuntimeError('Dynamic and static accounting was relabelled')
    for key, value in guards['baseline'].items():
        if final[key] != value:
            raise RuntimeError('Final CLI and guard baseline disagree: ' + key)
    for row in guards['controls']:
        folder = guard_root / 'controls' / row['name']
        if sha(folder / 'payload.json.gz') != row['payload_archive_sha256'] or canonical_sha(json.loads(gzip.decompress((folder / 'payload.json.gz').read_bytes()))) != row['payload_sha256']:
            raise RuntimeError('Retained actual guard payload changed')
        if row['app_executions'] != 0 or row['original_coverage_credit'] != 0:
            raise RuntimeError('Synthetic guard gained app credit')
    for row in guards['subprocess_controls']:
        folder = guard_root / 'subprocess-controls' / row['name']
        if row['returncode'] != 1 or sha(folder / 'video_private_accounting.py') != VALIDATOR_SHA or sha(folder / 'stdout.txt') != row['stdout_sha256'] or sha(folder / 'stderr.txt') != row['stderr_sha256']:
            raise RuntimeError('Actual rejection subprocess evidence changed')
    if sha(initial_root / 'executed-source/video_private_accounting.py') != initial['validator_sha256'] or initial['status'] != 'PRIVATE_EXACT_ORIGINAL_ACCOUNTING_PROPOSAL_SATISFIED':
        raise RuntimeError('Initial pre-type-guard positive/source record changed')
    name = '16-private-accounting-proposal'
    destination = HERE / 'checkpoints' / name; destination.mkdir(parents=True, exist_ok=False)
    sources = ['prepare_private_accounting_pins.py', 'private_accounting_pins.json', 'video_private_accounting.py',
        'video_private_accounting_controls.py', 'freeze_video_private_accounting.py', 'PRIVATE_ACCOUNTING_REVIEW.md',
        'PRIVATE_COVERAGE_PROPOSAL.md', 'RECOVERY_STATUS.md']
    for relative in sources:
        copy(HERE / relative, destination / relative)
    files = rows(destination); evidence = destination / 'evidence'
    for root in [initial_root, guard_root, final_root]:
        for path in sorted(root.rglob('*')):
            if path.is_file():
                copy(path, evidence / root.name / path.relative_to(root))
    for prefix in ['private-accounting', 'private-accounting-guards', 'private-accounting-final']:
        for suffix in ['stdout.txt', 'stderr.txt']:
            copy(HERE / (prefix + '-' + suffix), evidence / (prefix + '-' + suffix))
    evidence_files = rows(evidence)
    archive = HERE / 'checkpoints' / (name + '-evidence.tar.gz')
    if archive.exists():
        raise FileExistsError(archive)
    with tarfile.open(archive, 'w:gz') as stream:
        for row in evidence_files:
            stream.add(evidence / row['path'], arcname=row['path'], recursive=False)
    remaining = {row['path']: row for row in evidence_files}
    with tarfile.open(archive, 'r:gz') as stream:
        for member in stream:
            row = remaining.pop(member.name); data = stream.extractfile(member).read()
            if not member.isfile() or len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
                raise RuntimeError('Evidence archive member changed')
    if remaining:
        raise RuntimeError('Evidence archive omitted files')
    value = {'status': 'SEALED_PRIVATE_ACCOUNTING_PROPOSAL_AND_ALL_55_GUARDS_VERIFIED',
        'frozen_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Review-only calculation on one exactly bound already executed study; no active/fresh-run accounting gate, source registry or APK promotion.',
        'proposed_original_accounting_satisfied': True, 'raw_original_coverage_gate_passed': False,
        'original_dynamic_instructions': 259, 'original_static_infeasible_instructions': 3, 'original_total_instructions': 262,
        'original_static_offsets': [232, 233, 235], 'original_dynamic_conditional_edges': 46,
        'rebuilt_raw_coverage': final['rebuilt_raw_coverage'], 'rebuilt_static_accounting_applied': False,
        'pure_payload_guards': 51, 'actual_rejection_subprocesses': 4, 'all_guards_rejected': True,
        'additional_app_executions': 0, 'additional_dynamic_coverage_credit': 0,
        'exact_positive_restoration': True, 'active_policy_changed': False, 'active_registry_changed': False,
        'apk_built': False, 'android_executed': False, 'initial_pre_type_guard_positive_preserved': True,
        'validator_sha256': VALIDATOR_SHA, 'independent_pin_file_sha256': PINS_SHA,
        'bound_checkpoint_hashes': final['checkpoint_hashes'], 'bound_frozen_file_count': 367,
        'guard_result_sha256': sha(guard_root / 'result.json'), 'final_result_sha256': sha(final_root / 'result.json'),
        'free_bytes_before': free, 'files': files, 'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True}
    path = destination / 'checkpoint.json'; path.write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(path), 'sha256': sha(path), 'files': len(files),
        'evidence_files': len(evidence_files), 'evidence_bundle': value['evidence_bundle']}, indent=2))


if __name__ == '__main__':
    main()
