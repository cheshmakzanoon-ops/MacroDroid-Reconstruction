#!/usr/bin/env python3
"""Preserve the closed, read-only Settings evidence-reader correction."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
from datetime import datetime, timezone


ROOT = Path('/dev/shm/settings-enable-return-workflow-01')
SOURCE = ROOT / 'checkpoints/01-multipart-workflow-and-offline-validation'
DEST = ROOT / 'checkpoints/02-content-reference-verification'
EXPECTED = '5f64e5e87270fd1f2e5203bdc54559c50c4920102451f9761c58c2f269b72cfa'
TARGET = 'docs/verification/exact-alarm-enable-return/workflow-evidence-reader/01-content-reference-verification'


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def identity(path: Path) -> dict:
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise ValueError('Expected regular file: ' + str(path))
    digest = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    after = path.lstat()
    if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
            before.st_ctime_ns) != (after.st_dev, after.st_ino, after.st_size,
                                    after.st_mtime_ns, after.st_ctime_ns):
        raise ValueError('File changed while read: ' + str(path))
    return {'bytes': size, 'sha256': digest.hexdigest(),
            'mode': '100755' if after.st_mode & 0o111 else '100644'}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True) + '\n')
    path.chmod(0o644)


def main() -> None:
    start = utc()
    source_cp = identity(SOURCE / 'checkpoint.json')
    if source_cp['sha256'] != EXPECTED:
        raise ValueError('Frozen source checkpoint changed')
    checkpoint = json.loads((SOURCE / 'checkpoint.json').read_text())
    rows = checkpoint['files']
    if len(rows) != 602:
        raise ValueError('Unexpected frozen source inventory')
    verified = []
    for row in rows:
        relative = Path(row['path'])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe frozen path')
        actual = identity(SOURCE / relative)
        if actual != {key: row[key] for key in ('bytes', 'sha256', 'mode')}:
            raise ValueError('Frozen payload changed: ' + row['path'])
        verified.append({'path': row['path'], **actual})
    expected_paths = {row['path'] for row in rows} | {'checkpoint.json'}
    actual_paths = {str(p.relative_to(SOURCE)) for p in SOURCE.rglob('*') if p.is_file() or p.is_symlink()}
    if expected_paths != actual_paths:
        raise ValueError('Frozen source membership changed')
    if identity(SOURCE / 'checkpoint.json') != source_cp:
        raise ValueError('Frozen source checkpoint changed after payload verification')

    first = json.loads((ROOT / 'frozen-evidence-verification-01.json').read_text())
    final = json.loads((ROOT / 'frozen-evidence-verification-02.json').read_text())
    if first['passed'] is not False or first['status'] != 'FROZEN_SETTINGS_EVIDENCE_VERIFICATION_FAILED':
        raise ValueError('Original reader failure was not retained')
    if final['passed'] is not True or final['status'] != 'COMPLETE_FROZEN_SETTINGS_EVIDENCE_VERIFIED':
        raise ValueError('Corrected reader did not pass')
    for key, expected in {
        'frozen_payloads': 602, 'indexed_paths': 16454,
        'indexed_regular_paths': 16452, 'inert_symlinks': 2,
        'logical_regular_bytes': 7114730719,
        'unique_git_blob_references': 173,
        'reassembled_multipart_references': 3,
        'android_executed': False, 'application_code_executed': False,
        'apk_files_materialized': False,
    }.items():
        if final[key] != expected or type(final[key]) is not type(expected):
            raise ValueError('Final reader scope differs: ' + key)
    if final['checkpoint'] != {key: source_cp[key] for key in ('bytes', 'sha256')}:
        raise ValueError('Final reader checkpoint binding differs')
    if (ROOT / 'frozen-verification-attempt-01/result.json').read_bytes() != (ROOT / 'frozen-evidence-verification-01.json').read_bytes():
        raise ValueError('Retained failure result differs')
    if (ROOT / 'frozen-verification-attempt-01/executed-verifier.py').read_bytes() != (ROOT / 'verify_frozen_evidence.py').read_bytes():
        raise ValueError('Retained original reader differs')
    DEST.mkdir(parents=True, exist_ok=False)
    copies = [
        ('frozen-verification-attempt-01/result.json', 'retained-failure/result.json'),
        ('frozen-verification-attempt-01/executed-verifier.py', 'retained-failure/executed-verifier.py'),
        ('frozen-verification-attempt-01/cache-role-diagnosis.json', 'retained-failure/cache-role-diagnosis.json'),
        ('verify_frozen_evidence_v2.py', 'corrected-reader/verify_frozen_evidence.py'),
        ('frozen-verifier-correction.patch', 'corrected-reader/derivation.patch'),
        ('frozen-evidence-verification-02.json', 'corrected-reader/result.json'),
        ('checkpoints/01-multipart-workflow-and-offline-validation/checkpoint.json', 'bindings/source-workflow-checkpoint.json'),
        ('freeze_reader_followup.py', 'freeze_reader_followup.py'),
    ]
    copied = []
    for origin, relative in copies:
        src, dest = ROOT / origin, DEST / relative
        before = identity(src)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with src.open('rb') as reader, dest.open('xb') as writer:
            shutil.copyfileobj(reader, writer)
        dest.chmod(0o755 if before['mode'] == '100755' else 0o644)
        if identity(src) != before or identity(dest) != before:
            raise ValueError('Copy changed: ' + origin)
        copied.append({'source': str(src), 'path': relative, **before})
    rehash = {
        'status': 'ALL_602_FROZEN_WORKFLOW_PAYLOADS_REHASHED_UNCHANGED',
        'started_utc': start, 'finished_utc': utc(),
        'source_checkpoint': source_cp, 'frozen_payload_count': len(verified),
        'frozen_membership_exact': True, 'files': verified,
        'scope': 'Read-only post-reader bytes and Git-mode check; no source modification or test rerun.',
        'application_build_executed': False, 'android_executed': False,
    }
    write_json(DEST / 'bindings/final-frozen-payload-rehash.json', rehash)
    write_json(DEST / 'bindings/copied-inputs.json', copied)
    summary = {
        'source_workflow_checkpoint_sha256': EXPECTED,
        'source_workflow_repo_target': checkpoint['repo_target'],
        'workflow_offline_commands_passed': 74,
        'workflow_input_copy_roles': 317,
        'workflow_protected_input_files_unchanged': 402,
        'source_tests_reused_without_rerun': 259,
        'reader_attempt_01': {k: first[k] for k in ('status', 'passed', 'reason', 'started_utc', 'finished_utc')},
        'reader_attempt_02': {k: final[k] for k in final if k != 'git_reads'},
        'production_workflow_payloads_changed': False,
        'new_host_suite_executed': False, 'application_build_executed': False,
        'android_executed': False, 'workflow_activated': False,
        'full_runtime_1_to_1_established': False,
    }
    write_json(DEST / 'result.json', summary)
    readme = '''# Settings workflow evidence-reference verification

The corrected read-only reader verified the complete frozen Settings workflow evidence. The original workflow and its four executable payloads remain unchanged at checkpoint `5f64e5e87270fd1f2e5203bdc54559c50c4920102451f9761c58c2f269b72cfa`. This follow-up records a separate reader defect and its correction; it adds no application, workflow, image-comparison, or Android change.

## Retained first attempt

At 12:35:13–12:35:22 UTC on 2026-10-12, the first reader returned `FROZEN_SETTINGS_EVIDENCE_VERIFICATION_FAILED` with `ValueError: Referenced exact logical bytes differ`. Its source, full result and diagnosis are retained under `retained-failure/`.

The reader cached two different content roles under the same `(commit, path)` key. The source03 archive-layout manifest was first read as a 1,549-byte Git blob. The same immutable manifest path later identified the 13,014,001-byte logical archive assembled from its two parts. Reusing the manifest's digest for that second role incorrectly rejected the reference. The preserved diagnosis identifies the exact commit, paths, sizes and SHA-256 values.

## Narrow correction and actual result

`corrected-reader/derivation.patch` makes the content-reference kind part of each cache key and removes that tag only when forming the Git read. The exact size, SHA-256, Git-object, mode, inventory and archive checks are unchanged. No retained bytes or source workflow were adjusted to satisfy the reader.

The corrected invocation completed at 12:37:37 UTC with `COMPLETE_FROZEN_SETTINGS_EVIDENCE_VERIFIED`. Its full receipt preserves every fetched Git read. It checked:

- All 602 frozen workflow/evidence payloads.
- All 16,454 indexed paths: 16,452 regular paths and two symlinks retained as inert evidence.
- 7,114,730,719 logical regular bytes, including repeated case-tree references without duplicate APK copies.
- 173 distinct immutable Git-blob references.
- Three complete multipart logical containers, streamed from fetched Git objects and rehashed: the original APK, the fixed numeric candidate APK, and the source03 evidence archive.

No APK file was materialized by this reader. `bindings/final-frozen-payload-rehash.json` separately rechecks all 602 original payloads, their modes and complete membership after the reader attempts. All remain exact.

## Scope of the workflow result

The source capsule's earlier offline validation remains the actual 74-command pass, with 317 complete input-copy roles and 402 protected inputs unchanged. The closed 259 source controls were reused rather than rerun locally; the future hosted workflow retains the full suite. Archive, inventory, policy, APK and cleanup faults remain in that original capsule.

This follow-up is evidence-reference validation only. It does not run the host suite, application build, emulator or Settings journey, and does not establish runtime parity or activate a workflow. Recorded closure filesystem metadata remains closure metadata; the reader does not reinterpret it as the original command's filesystem timestamps.

## Files

- `bindings/source-workflow-checkpoint.json` binds the immutable 602-file source capsule.
- `bindings/final-frozen-payload-rehash.json` records the final exact-source check.
- `retained-failure/` preserves the first actual failure and its source.
- `corrected-reader/` preserves the four-line correction, final source and actual successful receipt.
- `result.json` keeps offline workflow and reader scopes separate.
'''
    (DEST / 'README.md').write_text(readme)
    (DEST / 'README.md').chmod(0o644)
    files = []
    for path in sorted(DEST.rglob('*')):
        if path.is_file():
            files.append({'path': str(path.relative_to(DEST)), **identity(path)})
    final_cp = {
        'schema': 1,
        'status': 'CLOSED_READ_ONLY_SETTINGS_CONTENT_REFERENCE_VERIFICATION',
        'created_utc': utc(), 'repo_target': TARGET,
        'active_files': [], 'source_checkpoint_sha256': EXPECTED,
        'source_payloads_unchanged': 602,
        'original_reader_failure_preserved': True,
        'corrected_reader_passed': True,
        'new_host_suite_executed': False,
        'application_build_executed': False, 'android_executed': False,
        'workflow_activated': False, 'full_runtime_1_to_1_established': False,
        'files': files, 'frozen_payload_count': len(files),
        'frozen_payload_bytes': sum(row['bytes'] for row in files),
    }
    write_json(DEST / 'checkpoint.json', final_cp)
    print(json.dumps({'checkpoint': str(DEST / 'checkpoint.json'),
                      **identity(DEST / 'checkpoint.json'),
                      'payload_count': len(files),
                      'payload_bytes': final_cp['frozen_payload_bytes']}, indent=2))


if __name__ == '__main__':
    main()
