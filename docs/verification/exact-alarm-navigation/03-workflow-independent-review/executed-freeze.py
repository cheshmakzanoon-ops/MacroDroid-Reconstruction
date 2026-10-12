"""Freeze the bounded review and its original reader-format failure without altering source."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import stat

base = Path('/dev/shm/macrodroid-transfer-space-20261012')
root = base / 'alarm14-workflow-review'
parent = Path('/dev/shm/macrodroid-exact-alarm-navigation/checkpoints/04-fourteen-screen-workflow')
result = json.loads((root / 'result.json').read_bytes())
assert result['status'] == 'BOUNDED_FROZEN_ALARM14_WORKFLOW_REVIEW_PASSED'
assert result['workflow_sha256'] == '575a8ccb4909ba526e4c29ba7695cc8486538885b017f29093c00344214bed1f'
for source, target in [
    (base / 'review_alarm14_workflow.py', root / 'executed-review.py'),
    (Path(__file__), root / 'executed-freeze.py'),
    (base / 'alarm14-workflow-review.stdout.log', root / 'stdout.log'),
    (base / 'alarm14-workflow-review.stderr.log', root / 'stderr.log'),
]:
    assert not target.exists()
    shutil.copyfile(source, target)
    target.chmod(0o644)
source_root = root / 'reviewed-source'
source_root.mkdir()
for name in ('prepare_trigger_journey.py', 'verify_trigger_journey.py',
             '.github/workflows/editor-exact-alarm-navigation.yml', 'checkpoint.json'):
    target = source_root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(parent / name, target)
    target.chmod(0o644)
shutil.copytree(base / 'alarm14-workflow-review-log-format-attempt01', root / 'initial-reader-log-format-attempt')
(root / 'README.md').write_text('''# Independent review of the frozen alarm14 workflow

The bounded review passed for the exact `805c4574` workflow package and workflow SHA-256 `575a8ccb4909ba526e4c29ba7695cc8486538885b017f29093c00344214bed1f`. The review found no concrete blocker for the separately authorized diagnostic. The actual Android outcome remains pending at this freeze.

The [result](result.json) binds all 13 package files, all 317 archived payloads and 11,900 regular-file roles, and 295 source-copy roles independently rebuilt from the fetched dependencies at commit `3d91187924af10457366ede7a1a8f10d3a1a6ac4`. All 98 frozen source files are represented. The three external APK/AAPT2 payload identities were rehashed locally and their durable manifest references checked. The AAPT2 tool was not freshly extracted from the published archive in this review.

The [closed command verification](closed-offline-command-verification.json) checks all 63 preserved command records and both streams, including 209 journey, six downloader and ten animation test successes. This inspects the closed host runs; it does not rerun that suite. The [new inventory controls](inventory-boundary-controls.json) call the unchanged real preparation functions over an explicit virtual read-only filesystem backed by exact fetched and archived bytes. Twelve cases cover the genuine inventory, omitted/empty/reordered/duplicate rows, changed sources/copies, schema and policy corruption, and positive restoration. No copied program, AAPT2 or Android command is executed by these controls.

The workflow remains limited to fourteen captured screens and thirteen inputs per APK. The only added input is the observed explanation dialog's OK control. The final comparison requires schema6, both exact policy identities, 26 total planned inputs, six setup mutations, zero unbound mutations and zero Settings inputs. It keeps whole-frame differences as exit2, and makes no permission-grant or whole-app parity claim. The existing workflows, application source and APKs remain untouched by this review.

The initial reviewer attempt incorrectly expected every unittest success on the same line as its test name. Five downloader tests emit their intentional attempt diagnostics before a standalone `ok`. That reader stopped after the complete inventory checks; its exact source, partial outputs and traceback are preserved in [initial-reader-log-format-attempt](initial-reader-log-format-attempt/). The corrected reader binds every test name and permits only those literal downloader diagnostic lines. No production or frozen test source changed.

The complete original offline archive remains in `work-in-progress/exact-alarm-navigation-workflow/01-fourteen-screen`; it is referenced rather than duplicated here. This capsule preserves every authored reviewer/freezer and all review output. Activation, expected-head publication and actual run evidence are separate steps.
''')
files = []
for path in sorted(root.rglob('*')):
    if not path.is_file():
        assert not path.is_symlink()
        continue
    assert path.name != 'checkpoint.json' or path.parent == source_root
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode)
    data = path.read_bytes()
    files.append({'path': path.relative_to(root).as_posix(), 'bytes': len(data),
                  'sha256': hashlib.sha256(data).hexdigest(),
                  'mode': '100755' if mode & 0o111 else '100644'})
checkpoint = {
    'schema': 1, 'status': 'BOUNDED_ALARM14_WORKFLOW_REVIEW_PASSED',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'repo_target': 'docs/verification/exact-alarm-navigation/03-workflow-independent-review',
    'active_files': [], 'android_executed': False,
    'application_source_or_apk_changed': False,
    'reviewed_checkpoint_sha256': result['checkpoint_sha256'],
    'reviewed_workflow_sha256': result['workflow_sha256'],
    'files': files, 'file_count': len(files), 'payload_bytes': sum(r['bytes'] for r in files),
}
raw = (json.dumps(checkpoint, indent=2) + '\n').encode()
with (root / 'checkpoint.json').open('xb') as stream:
    stream.write(raw)
for row in files:
    data = (root / row['path']).read_bytes()
    assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
print(json.dumps({'checkpoint': str(root / 'checkpoint.json'), 'bytes': len(raw),
                  'sha256': hashlib.sha256(raw).hexdigest(), 'files': len(files),
                  'payload_bytes': checkpoint['payload_bytes'], 'repo_target': checkpoint['repo_target']}))
