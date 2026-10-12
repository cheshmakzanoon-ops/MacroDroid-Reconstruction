#!/usr/bin/env python3
"""Freeze this completed independent review without altering parent evidence."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

from recheck_prepared_inputs import SOURCE_ROWS, identity
from inspect_frozen_workflow import CAPSULE, CHECKPOINT_SHA256

ROOT = Path(__file__).resolve().parent


def copy_exact(source, target, expected=None):
    actual = identity(source)
    if expected is not None and actual != expected:
        raise ValueError('A reviewed source differs from its measured identity')
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as stream:
        stream.write(source.read_bytes())
    target.chmod(source.stat().st_mode & 0o777)
    if identity(target) != actual or identity(source) != actual:
        raise ValueError('A file changed while freezing the review')


def main():
    post = json.loads((ROOT / 'reports/post-suite-inputs/result.json').read_bytes())
    audit = json.loads((ROOT / 'reports/frozen-workflow-audit/result.json').read_bytes())
    if (post.get('passed') is not True or post.get('independently_rechecked_roles') != 252
            or audit.get('passed') is not True or audit.get('verified_archive_members') != 276
            or audit.get('complete_regular_evidence_roles') != 8641
            or identity(CAPSULE / 'checkpoint.json')['sha256'] != CHECKPOINT_SHA256):
        raise ValueError('The exact completed independent reviews are required')
    for row in SOURCE_ROWS:
        copy_exact(CAPSULE / row['path'], ROOT / 'reviewed-workflow-source' / row['path'],
                   {key: row[key] for key in ('bytes', 'sha256')})
    for name in ('checkpoint.json', 'offline-validation.json'):
        copy_exact(CAPSULE / name, ROOT / 'parent-capsule-bindings' / name)
    receipts = []
    for script, result, stdout, stderr in [
            ('recheck_prepared_inputs.py', 'reports/post-suite-inputs/result.json',
             'post-suite-recheck.stdout.txt', 'post-suite-recheck.stderr.txt'),
            ('inspect_frozen_workflow.py', 'reports/frozen-workflow-audit/result.json',
             'frozen-workflow-audit.stdout.txt', 'frozen-workflow-audit.stderr.txt')]:
        value = json.loads((ROOT / result).read_bytes())
        receipts.append({'argv': ['python3', '-B', str(ROOT / script)], 'exit_code': 0,
                         'script': {'path': script, **identity(ROOT / script)},
                         'result': {'path': result, **identity(ROOT / result)},
                         'stdout': {'path': stdout, **identity(ROOT / stdout)},
                         'stderr': {'path': stderr, **identity(ROOT / stderr)},
                         'started_utc': value['started_utc'], 'finished_utc': value['finished_utc'],
                         'seconds': value['seconds'], 'record_created_after_completion': True})
    (ROOT / 'execution-receipts.json').write_text(json.dumps(receipts, indent=2) + '\n')
    source_files = sorted(path for path in ROOT.rglob('*')
                          if path.is_file() and 'checkpoints' not in path.relative_to(ROOT).parts)
    if any(path.is_symlink() for path in source_files):
        raise ValueError('Unexpected symlink in the independent review')
    output = ROOT / 'checkpoints/03-independent-workflow-review'
    output.mkdir(parents=True, exist_ok=False)
    rows = []
    for path in source_files:
        name = path.relative_to(ROOT).as_posix()
        expected = identity(path)
        copy_exact(path, output / name, expected)
        rows.append({'path': name, **expected, 'mode': path.stat().st_mode & 0o777})
    for row in rows:
        if identity(ROOT / row['path']) != {key: row[key] for key in ('bytes', 'sha256')}:
            raise ValueError('Independent review changed while freezing')
    checkpoint = {
        'status': 'INDEPENDENT_READINESS_WORKFLOW_SOURCE_AND_EVIDENCE_REVIEW_PASSED',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'repo_target': 'docs/verification/notification-readiness/03-independent-workflow-review',
        'android_executed': False, 'host_suites_rerun': False,
        'full_runtime_1_to_1_established': False,
        'activation_clearance': {'workflow': '.github/workflows/editor-day-time-readiness.yml',
                                 'sha256': SOURCE_ROWS[0]['sha256'],
                                 'condition': 'Publisher verifies expected new-path absence and all frozen bytes'},
        'parent_capsule': {'repo_path': 'work-in-progress/notification-readiness-workflow/01-thirteen-screen',
                           **identity(CAPSULE / 'checkpoint.json')},
        'parent_complete_archive': audit['archive'],
        'parent_complete_archive_manifest': audit['archive_manifest'],
        'independent_executions': ['source identity and exact derivation reconstruction',
                                  'real post-suite preparation.verify_prepared_inputs: 252 roles',
                                  'complete frozen source/raw/archive audit: 8641 roles and 276 payloads'],
        'inspected_parent_execution': {'commands': 55, 'journey_tests': 166,
                                       'downloader_tests': 6, 'animation_tests': 10,
                                       'rerun_by_reviewer': False},
        'files': rows,
    }
    target = output / 'checkpoint.json'
    target.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(target), **identity(target),
                      'files': len(rows), 'payload_bytes': sum(row['bytes'] for row in rows)}, indent=2))


if __name__ == '__main__':
    main()
