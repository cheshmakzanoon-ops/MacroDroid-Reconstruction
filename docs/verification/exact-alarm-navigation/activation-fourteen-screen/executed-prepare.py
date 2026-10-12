"""Prepare only the authorized new alarm14 workflow after fetched review verification."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import stat
import subprocess

ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012')
GIT = ROOT / 'verification.git'
PARENT = '39250fac022aee5551f36782bafd72cabbc33718'
CAP = 'work-in-progress/exact-alarm-navigation-workflow/01-fourteen-screen'
WORKFLOW = '.github/workflows/editor-exact-alarm-navigation.yml'
WORKFLOW_SHA = '575a8ccb4909ba526e4c29ba7695cc8486538885b017f29093c00344214bed1f'
REVIEW = 'docs/verification/exact-alarm-navigation/03-workflow-independent-review'
LOCAL = Path('/dev/shm/macrodroid-exact-alarm-navigation/checkpoints/04-fourteen-screen-workflow')
TARGET = 'docs/verification/exact-alarm-navigation/activation-fourteen-screen'
EXPORT = ROOT / 'alarm14-activation-export'
TREE = ROOT / 'alarm14-activation-tree'
os.environ['GIT_OPTIONAL_LOCKS'] = '0'

def git(*args):
    return subprocess.check_output(['git', '--git-dir=' + str(GIT), *args])

def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def blobid(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

assert git('rev-parse', 'refs/heads/main').decode().strip() == PARENT
tree = {}
for raw in git('ls-tree', '-rz', '--full-tree', PARENT).split(b'\0'):
    if raw:
        info, path = raw.split(b'\t', 1)
        mode, kind, oid = info.decode().split()
        tree[path.decode()] = (mode, kind, oid)
assert WORKFLOW not in tree

def fetched(path):
    mode, kind, oid = tree[path]
    assert mode == '100644' and kind == 'blob', path
    data = git('cat-file', 'blob', oid)
    assert blobid(data) == oid
    return data

bindings = []
for path, expected in [
    (CAP + '/checkpoint.json', '805c4574f6047edd3d553715d83c48448d49fddd3f4d22807ebb3e0d5663b066'),
    (REVIEW + '/checkpoint.json', '4b90c46c1be4fb92f029277a86c9862b90488ed94f7de221655de859764fb790'),
    ('work-in-progress/exact-alarm-navigation/03-corrected-source-and-host-controls/checkpoint.json',
     '8deeece1c51d4320a72b065679f22a56242ea6769ed526e0c6436df405430857'),
]:
    data = fetched(path)
    assert identity(data)['sha256'] == expected
    bindings.append({'path': path, **identity(data), 'git_blob_sha1': tree[path][2]})
cp = json.loads(fetched(CAP + '/checkpoint.json'))
assert cp['active_changes'] is False and cp['android_executed'] is False
assert cp['workflow_sha256'] == WORKFLOW_SHA
review = json.loads(fetched(REVIEW + '/result.json'))
assert review['status'] == 'BOUNDED_FROZEN_ALARM14_WORKFLOW_REVIEW_PASSED'
assert review['checkpoint_sha256'] == bindings[0]['sha256']
assert review['workflow_sha256'] == WORKFLOW_SHA
workflow_raw = fetched(CAP + '/' + WORKFLOW)
assert identity(workflow_raw) == {'bytes': 11547, 'sha256': WORKFLOW_SHA}
local = LOCAL / WORKFLOW
assert local.read_bytes() == workflow_raw and stat.S_IMODE(local.lstat().st_mode) == 0o644
assert next(r for r in cp['files'] if r['path'] == WORKFLOW) == {'path': WORKFLOW, **identity(workflow_raw)}
receipt_path = ROOT / 'alarm-workflow-lookup-successors-export-v2/remote-verification.json'
receipt_raw = receipt_path.read_bytes()
receipt = json.loads(receipt_raw)
assert receipt['commit'] == PARENT and receipt['verified_paths'] == 203
assert receipt['git_mode_size_sha1_sha256_verified'] is True
assert receipt['staged_bytes_and_modes_equal_fetched_git'] is True
protected = {name: git('rev-parse', PARENT + ':' + name).decode().strip()
             for name in ('project', 'artifacts/current', 'vendor')}
previous_workflows = {p: {'mode': v[0], 'git_blob_sha1': v[2]} for p, v in tree.items()
                      if p.startswith('.github/workflows/')}
guard = {
    'status': 'EXACT_SINGLE_ALARM14_WORKFLOW_ACTIVATION_PREPARED',
    'completed_utc': datetime.now(timezone.utc).isoformat(),
    'parent_commit': PARENT, 'active_path': WORKFLOW, 'active_path_must_be_absent': True,
    'candidate': identity(workflow_raw), 'mode': '100644',
    'candidate_git_blob_sha1': tree[CAP + '/' + WORKFLOW][2],
    'fetched_capsule_and_review_bindings': bindings,
    'complete_inactive_batch_fetch_receipt': identity(receipt_raw),
    'protected_application_trees': protected, 'previous_workflows': previous_workflows,
    'source_or_apk_promotion': False, 'new_device_execution': False,
    'runtime_result': 'PENDING_NEW_AUTOMATIC_WORKFLOW_RUN',
    'authorized_input_scope': 'One observed exact-alarm explanation OK tap after the retained thirteen-screen journey, followed by Settings observation; zero Settings inputs and no permission grant.',
    'publication_scope': 'Only the new root workflow is active. Existing workflows and application inputs remain unchanged.',
}
EXPORT.mkdir()
doc = TREE / TARGET
doc.mkdir(parents=True)
contents = {
    'activation-guard.json': (json.dumps(guard, indent=2) + '\n').encode(),
    'executed-prepare.py': Path(__file__).read_bytes(),
    'reviewed-package-fetch-verification.json': receipt_raw,
    'README.md': (
        '# Fourteen-screen alarm navigation activation\n\n'
        'This checkpoint activates the exact single workflow `' + WORKFLOW + '` after '
        'the frozen package and independent review were fetched and verified at commit `' + PARENT + '`. '
        'The [guard receipt](activation-guard.json) records the previously absent path, exact candidate '
        'identity and mode, fixed source/review dependencies and protected existing trees.\n\n'
        'The authorized experiment adds the observed explanation dialog OK input to the retained '
        'thirteen-screen sequence, then captures Settings. It permits no Settings input or permission '
        'grant and keeps complete-frame differences as failures. It uses the same pinned original and '
        'current candidate APK bytes. No application source or APK is promoted here.\n\n'
        'The complete package contains the measured 209 journey, six downloader and ten animation '
        'host successes. The independent review verifies the full frozen evidence and twelve new '
        'virtual inventory controls. The actual Android outcome is pending and will be retained '
        'separately from these host checks and all prior failed device runs.\n'
    ).encode(),
}
elements = [{'path': WORKFLOW, 'mode': '100644', 'type': 'blob', 'sha': blobid(workflow_raw)}]
manifest = [{'path': WORKFLOW, 'local_path': str(local), 'size_bytes': len(workflow_raw),
             'sha256': WORKFLOW_SHA, 'git_blob_sha1': blobid(workflow_raw), 'mode': '100644'}]
for name, raw in contents.items():
    path = TARGET + '/' + name
    assert path not in tree
    file = doc / name
    file.write_bytes(raw)
    file.chmod(0o644)
    elements.append({'path': path, 'mode': '100644', 'type': 'blob', 'content': raw.decode()})
    manifest.append({'path': path, 'local_path': str(file), 'size_bytes': len(raw),
                     'sha256': identity(raw)['sha256'], 'git_blob_sha1': blobid(raw), 'mode': '100644'})
(EXPORT / 'tree-elements.json').write_text(json.dumps(elements) + '\n')
(EXPORT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
(EXPORT / 'preparation.json').write_text(json.dumps(guard, indent=2) + '\n')
print(json.dumps({'parent': PARENT, 'paths': len(manifest), 'new_active_workflows': 1,
                  'bytes': sum(r['size_bytes'] for r in manifest),
                  'fetched_package_review_and_candidate_verified': True,
                  'application_source_or_apk_changed': False}))
