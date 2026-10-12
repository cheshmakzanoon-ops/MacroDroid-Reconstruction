"""Prepare the single Settings workflow after its exact reviewed package is durable."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess

ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012')
GIT = ROOT / 'verification.git'
PARENT = 'a12369837cdd5d6c795726c0de646be5cc52c0d2'
CAP = 'work-in-progress/exact-alarm-enable-return-workflow/01-sixteen-screen'
LOCAL = Path('/dev/shm/settings-enable-return-workflow-01/checkpoints/01-multipart-workflow-and-offline-validation')
WORKFLOW = '.github/workflows/editor-exact-alarm-enable-return.yml'
EXPECTED_WORKFLOW = 'f0b063179dd0f01330787b65908ca861926f16576add80392d5922d2cfd5bbd3'
EXPORT = ROOT / 'settings-enable-return-activation-export'
os.environ['GIT_OPTIONAL_LOCKS'] = '0'

def git(*args):
    return subprocess.check_output(['git', '--git-dir=' + str(GIT), *args])

def identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def oid(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

assert git('rev-parse', 'refs/heads/main').decode().strip() == PARENT
tree = {}
for line in git('ls-tree', '-rz', '--full-tree', PARENT).split(b'\0'):
    if line:
        info, name = line.split(b'\t', 1)
        mode, kind, obj = info.decode().split()
        tree[name.decode()] = (mode, kind, obj)
assert WORKFLOW not in tree

def fetched(name, mode='100644'):
    actual_mode, kind, obj = tree[name]
    assert actual_mode == mode and kind == 'blob', name
    raw = git('cat-file', 'blob', obj)
    assert oid(raw) == obj, name
    return raw

checkpoint_pins = [
    (CAP, '5f64e5e87270fd1f2e5203bdc54559c50c4920102451f9761c58c2f269b72cfa', 602),
    ('docs/verification/exact-alarm-enable-return/workflow-evidence-reader/01-content-reference-verification',
     '819ce0d2b72ea9e1179ac87cc30613c72e10efb8f6eac45621ed0fe02cead92b', 12),
    ('docs/verification/exact-alarm-enable-return/root-final-workflow-review',
     '5914d40016a131b554c4c72936d38d5da6549d2a9f3ae05ff78fdab3887e3053', 37),
]
capsules, bindings = [], []
for name, digest, count in checkpoint_pins:
    raw = fetched(name + '/checkpoint.json')
    assert identity(raw)['sha256'] == digest
    value = json.loads(raw)
    assert len(value['files']) == count and value['active_files'] == []
    capsules.append(value)
    bindings.append({'path': name + '/checkpoint.json', **identity(raw),
                     'git_blob_sha1': tree[name + '/checkpoint.json'][2], 'payload_count': count})
assert capsules[0]['workflow_offline_validated'] is True
assert capsules[0]['offline_commands'] == 74 and capsules[0]['complete_input_copy_roles'] == 317
assert capsules[0]['android_executed'] is False
assert capsules[1]['corrected_reader_passed'] is True
assert capsules[2]['passed'] is True

receipt_path = ROOT / 'settings-workflow-ready-export/remote-verification.json'
receipt_raw = receipt_path.read_bytes()
receipt = json.loads(receipt_raw)
assert receipt['commit'] == PARENT and receipt['verified_paths'] == 686
assert receipt['git_mode_size_sha1_sha256_verified'] is True
assert receipt['staged_bytes_and_modes_equal_fetched_git'] is True

mapping_raw = fetched(CAP + '/proposed-source-files.json')
assert mapping_raw == (LOCAL / 'proposed-source-files.json').read_bytes()
mappings = json.loads(mapping_raw)
assert len(mappings) == 4 and len({r['target'] for r in mappings}) == 4
expected_helpers = {CAP + '/' + n for n in
                    ('prepare_trigger_journey.py', 'verify_trigger_journey.py', 'validate_workflow.py')}
assert {r['target'] for r in mappings} == expected_helpers | {WORKFLOW}
rowmap = {r['path']: r for r in capsules[0]['files']}
helper_bindings, workflow_raw, workflow_local = [], None, None
for row in mappings:
    assert row['mode'] == '100644'
    source = CAP + '/' + row['source']
    raw = fetched(source)
    local = LOCAL / row['source']
    assert local.read_bytes() == raw and stat.S_IMODE(local.lstat().st_mode) == 0o644
    assert identity(raw) == {'bytes': row['bytes'], 'sha256': row['sha256']}
    assert rowmap[row['source']] == {'path': row['source'], **identity(raw), 'mode': '100644'}
    if row['target'] == WORKFLOW:
        assert row['source'] == WORKFLOW
        assert identity(raw) == {'bytes': 11735, 'sha256': EXPECTED_WORKFLOW}
        workflow_raw, workflow_local = raw, local
    else:
        assert row['target'] in expected_helpers and source == row['target']
        assert fetched(row['target']) == raw
        helper_bindings.append({'path': row['target'], **identity(raw),
                                'mode': '100644', 'git_blob_sha1': tree[row['target']][2]})
assert len(helper_bindings) == 3 and workflow_raw is not None
current_raw = fetched('artifacts/current/manifest.json')
assert identity(current_raw)['sha256'] == 'f342782af8251342a02061c31ceb601f9585f9b701f4147e7817231250c58e62'
protected = {name: git('rev-parse', PARENT + ':' + name).decode().strip()
             for name in ('project', 'artifacts', 'vendor', 'docs', 'work-in-progress', 'tools')}
previous_workflows = {name: {'mode': value[0], 'git_blob_sha1': value[2]}
                      for name, value in tree.items() if name.startswith('.github/workflows/')}
guard = {
    'schema': 1, 'status': 'EXACT_SINGLE_SETTINGS_ENABLE_RETURN_WORKFLOW_ACTIVATION_PREPARED',
    'completed_utc': datetime.now(timezone.utc).isoformat(), 'parent': PARENT,
    'active_path': WORKFLOW, 'active_path_must_be_absent': True,
    'candidate': identity(workflow_raw), 'mode': '100644', 'candidate_git_blob_sha1': oid(workflow_raw),
    'fetched_capsule_and_review_bindings': bindings,
    'reviewed_existing_helpers': helper_bindings,
    'complete_inactive_batch_fetch_receipt': identity(receipt_raw),
    'protected_tree_oids': protected, 'previous_workflows': previous_workflows,
    'current_apk_manifest': identity(current_raw),
    'application_source_or_apk_promotion': False, 'android_executed_here': False,
    'runtime_result': 'PENDING_NEW_AUTOMATIC_WORKFLOW_RUN',
    'input_scope': 'The exact sixteen-screen plan uses the observed off toggle, requires the new checked surface before the observed Navigate up input, and retains full-frame and continuity failures.',
    'activation_scope': 'Only the absent top-level workflow is added; three already-published helper files are checked and left unchanged.',
}
EXPORT.mkdir(exist_ok=False)
manifest = [{'path': WORKFLOW, 'local_path': str(workflow_local), 'size_bytes': len(workflow_raw),
             'sha256': EXPECTED_WORKFLOW, 'git_blob_sha1': oid(workflow_raw), 'mode': '100644'}]
elements = [{'path': WORKFLOW, 'mode': '100644', 'type': 'blob', 'sha': oid(workflow_raw)}]
for name, value in [('preparation.json', guard), ('manifest.json', manifest), ('tree-elements.json', elements)]:
    (EXPORT / name).write_text(json.dumps(value, indent=2) + '\n')
print(json.dumps({'parent': PARENT, 'active_paths': 1, 'verified_existing_helpers': 3,
                  'bytes': len(workflow_raw), 'fetched_package_and_reviews_verified': True,
                  'application_source_or_apk_changed': False}))

