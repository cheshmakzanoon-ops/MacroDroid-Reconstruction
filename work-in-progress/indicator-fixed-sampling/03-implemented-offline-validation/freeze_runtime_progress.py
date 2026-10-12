#!/usr/bin/env python3
"""Preserve the implemented inactive source and already closed offline work."""
from pathlib import Path
import difflib
import hashlib
import json
import shutil
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'checkpoints/02-implemented-offline-validated'
DEST.mkdir(parents=True, exist_ok=False)
shutil.copytree(ROOT / 'source', DEST / 'source')
for name in ('attempt-01', 'workflow-01'):
    shutil.copytree(ROOT / 'reports' / name, DEST / 'reports' / name)
for name in ('generate_workflow.py', 'run_host_attempt.py', 'validate_workflow.py', 'freeze_runtime_progress.py'):
    shutil.copy2(ROOT / name, DEST / name)


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


old = ROOT / 'checkpoints/01-incomplete-runtime-draft/source'
changes = []
patches = []
for path in sorted((DEST / 'source').rglob('*')):
    if not path.is_file():
        continue
    name = path.relative_to(DEST / 'source').as_posix()
    prior = old / name
    item = {'path': name, 'before': identity(prior) if prior.is_file() else None, 'after': identity(path)}
    if item['before'] != item['after']:
        changes.append(item)
        if path.suffix in ('.py', '.json', '.md', '.yml'):
            patches.extend(difflib.unified_diff(prior.read_text().splitlines(True) if prior.is_file() else [],
                path.read_text().splitlines(True), fromfile='draft-01/' + name, tofile='offline-02/' + name))
(DEST / 'source-delta.patch').write_text(''.join(patches))
(DEST / 'source-delta.json').write_text(json.dumps(changes, indent=2) + '\n')
correction = {'scope': 'Synthetic host fixture only; no parent or device policy change.',
    'failed_attempt': 'reports/attempt-01/result.json', 'actual_tests_completed': 19,
    'actual_test_failures': 0, 'actual_test_errors': 1,
    'failure': "Synthetic setUpClass tried radio.sys; the unchanged pinned helper has no sys attribute.",
    'correction': "Patch the imported process sys.argv directly for the pinned helper's argparse call.",
    'frozen_failed_test_source': identity(DEST / 'reports/attempt-01/source/tools/indicator_sampling/test_indicator_sampling.py'),
    'corrected_test_source': identity(DEST / 'source/tools/indicator_sampling/test_indicator_sampling.py'),
    'successor_full_host_attempt_status_at_freeze': 'RUNNING; excluded because its output is not closed',
    'android_executed': False}
(DEST / 'first-host-attempt-correction.json').write_text(json.dumps(correction, indent=2) + '\n')
(DEST / 'README.md').write_text('''# Implemented indicator diagnostic: offline validation checkpoint

This is an inactive implementation checkpoint. It preserves the complete fixed eight-slot source and workflow after the approved design deltas, the first closed failed host attempt, its one-line fixture correction, and the closed offline input/workflow checks. It is not an Android result and does not authorize activation.

The original and candidate remain the fixed 84333011… / 5f635e16… APKs. All sixteen design parent declarations remain unchanged. The explicit AAPT2 dependency, eight separately bounded slot invocations, exact full-XML target guard, and streamed lossless 12-byte difference format are documented in the source README.

`reports/workflow-01/result.json` passes twelve retained shell/CLI/owned-cleanup command records, embedded Python parsing, all forty fetched parent/part identities, the complete sixteen-file own-source inventory, and actual read-only full-ZIP/CRC/AAPT2 inspection of both exact applications. The two AAPT2 records and forty fetched-Git byte/mode bindings are retained separately. Both applications were read in place; neither was copied or installed.

`reports/attempt-01/` remains the exact failed first host attempt: nineteen tests passed before synthetic setUpClass errored because the fixture incorrectly addressed `radio.sys`. The corrected fixture patches process `sys.argv`; the frozen helper is unchanged. The successor full host attempt was still running at this checkpoint and its mutable outputs are deliberately excluded. No closed full-host pass is claimed here.

The complete source delta is reviewable in `source-delta.patch` and its exact byte identities in `source-delta.json`. This capsule is a successor of the already published incomplete draft `effbce44…` and leaves that draft and the original `fccc817b…` design untouched. No active repository path, application source, APK, or Android runtime was changed by this freeze.
''')
files = []
for path in sorted(DEST.rglob('*')):
    if path.is_file():
        files.append({'path': path.relative_to(DEST).as_posix(), **identity(path),
                      'mode': '100755' if path.stat().st_mode & 0o111 else '100644'})
checkpoint = {'schema': 1, 'kind': 'INACTIVE_INDICATOR_IMPLEMENTED_OFFLINE_SUCCESS_HOST_PENDING',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'target': 'work-in-progress/indicator-fixed-sampling/03-implemented-offline-validation',
    'parent_design_sha256': 'fccc817be37d821a781348a8870c227ff5471fcdc72d71f38a81bc062c7a3eec',
    'parent_draft_sha256': 'effbce444cd4630f0d877163ef0477c273d4d796822f0ec2357c379212585675',
    'android_executed': False, 'active_files': [], 'full_runtime_1_to_1_established': False,
    'source_path_count': 16, 'frozen_payload_count': len(files),
    'frozen_payload_bytes': sum(row['bytes'] for row in files), 'files': files}
(DEST / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
print(json.dumps({'path': str(DEST / 'checkpoint.json'), **identity(DEST / 'checkpoint.json'),
                  'payloads': len(files), 'payload_bytes': checkpoint['frozen_payload_bytes']}, indent=2))
