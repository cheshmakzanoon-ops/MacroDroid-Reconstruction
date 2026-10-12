#!/usr/bin/env python3
"""Freeze stronger proof-input guards without changing any app coverage policy."""
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
    if source.is_symlink() or target.exists():
        raise RuntimeError('Fresh regular-file copy required')
    shutil.copyfile(source, target)
    if sha(source) != sha(target) or (source.stat().st_dev, source.stat().st_ino) == (target.stat().st_dev, target.stat().st_ino):
        raise RuntimeError('Copy differs or uses a hardlink')


def rows(root):
    return [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)}
            for p in sorted(root.rglob('*')) if p.is_file()]


def main():
    facts_root = HERE / 'reports/handler-facts-04b-pinned'
    guard_root = HERE / 'reports/handler-guard-followup-04b'
    facts = json.loads((facts_root / 'result.json').read_text())
    guards = json.loads((guard_root / 'result.json').read_text())
    if (facts['status'] != 'STRUCTURAL_FACTS_VERIFIED_SYNCHRONOUS_HOST_ARGUMENT_FOR_REVIEW' or
            len(facts['synthetic_fact_guard_controls']) != 11 or
            guards['status'] != 'PINNED_PROOF_GUARDS_PASSED_NO_COVERAGE_POLICY_CHANGE' or
            guards['structural_guards_rejected'] != 11 or guards['rehashed_evidence_controls_rejected'] != 2 or
            not guards['added_throw_comparison']['old_substring_guard_accepted'] or
            not guards['added_throw_comparison']['new_complete_disassembly_guard_rejected'] or
            any(row['returncode'] != 1 or not row['rejected'] for row in guards['commands'])):
        raise RuntimeError('Pinned proof-guard outcome differs')
    original = HERE / 'checkpoints/04-handler-dataflow-review'
    if sha(original / 'checkpoint.json') != '053ee22c427813258cc64f7363c150353ce1f5bbc8118aa12dbb9af049b8e754':
        raise RuntimeError('Reviewed predecessor changed')
    destination = HERE / 'checkpoints/04b-pinned-handler-proof-guards'
    destination.mkdir(parents=True, exist_ok=False)
    for name in ('verify_handler_dataflow.py', 'handler_guard_followup.py', 'PINNED_PROOF_GUARDS.md', 'freeze_pinned_handler_guards.py'):
        copy(HERE / name, destination / name)
    files = rows(destination)
    evidence = destination / 'evidence'
    for folder in (facts_root, guard_root):
        for path in folder.rglob('*'):
            if path.is_file():
                copy(path, evidence / 'reports' / folder.name / path.relative_to(folder))
    for name in ('handler-facts-pinned-stdout.txt', 'handler-facts-pinned-stderr.txt',
                 'handler-guard-followup-stdout.txt', 'handler-guard-followup-stderr.txt'):
        copy(HERE / name, evidence / name)
    for name in ('checkpoint.json', 'HANDLER_DATAFLOW_REVIEW.md', 'verify_handler_dataflow.py'):
        copy(original / name, evidence / 'reviewed-predecessor' / name)
    evidence_files = rows(evidence)
    archive = HERE / 'checkpoints/04b-pinned-handler-proof-guards-evidence.tar.gz'
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
                raise RuntimeError('Archive bytes differ')
    if remaining:
        raise RuntimeError('Archive omitted evidence')
    value = {'status': 'EXACT_REVIEWED_PROOF_IDENTITIES_AND_GUARDS_VERIFIED_NO_COVERAGE_EXEMPTION',
        'frozen_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Follow-up proof-input safeguards. All prior app coverage failures remain unchanged; actual future execution runtime still needs its own gate binding.',
        'reviewed_predecessor_sha256': sha(original / 'checkpoint.json'),
        'original_coverage_credit_added': 0, 'app_method_executions_added': 0,
        'coverage_exemption_implemented': False, 'oracle_changed': False, 'active_source_changed': False,
        'structural_guards': 11, 'structural_guards_rejected': 11,
        'rehashed_evidence_controls': 2, 'rehashed_evidence_controls_rejected': 2,
        'old_added_throw_substring_acceptance_preserved': True, 'new_added_throw_rejected': True,
        'facts_result_sha256': sha(facts_root / 'result.json'), 'guard_result_sha256': sha(guard_root / 'result.json'),
        'independent_digest_bindings': facts['independent_digest_bindings'],
        'files': files, 'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True}
    manifest = destination / 'checkpoint.json'; manifest.write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(manifest), 'sha256': sha(manifest), 'files': len(files),
                      'evidence_files': len(evidence_files), 'evidence_bundle': value['evidence_bundle']}, indent=2))


if __name__ == '__main__':
    main()
