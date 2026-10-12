"""Prepare the exact, reviewed nine-path numeric tooling activation from fetched Git."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat
import subprocess

ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012')
GIT = ROOT / 'verification.git'
PARENT = '9d36c89d5d5dde46570d42238dc34b2c60909b04'
PACKAGE = 'work-in-progress/day-trigger-numeric/09-hosted-filesystem-acceptance'
LOCAL = Path('/dev/shm/day-numeric-hosted-02/checkpoints/02-hosted-filesystem-tooling-successor')
TARGET = 'docs/verification/day-numeric-filesystem-successor/activation'
EXPORT = ROOT / 'numeric-filesystem-activation-export'
TREE = ROOT / 'numeric-filesystem-activation-tree'
EXPECTED = {
    '.github/workflows/day-numeric-wip-acceptance.yml',
    'tools/day_numeric_acceptance/README.md',
    'tools/day_numeric_acceptance/inputs.py',
    'tools/day_numeric_acceptance/pins.json',
    'tools/day_numeric_acceptance/prepare.py',
    'tools/day_numeric_acceptance/run_acceptance.py',
    'tools/day_numeric_acceptance/runtime-files.json',
    'tools/day_numeric_acceptance/test_day_numeric_acceptance.py',
    'tools/day_numeric_acceptance/verify.py',
}
CHECKPOINTS = {
    PACKAGE + '/checkpoint.json': '815612f827f1b0d2bcec90bbb1ae8a35a8c76ced8f6b5f44cf413bc40b81f493',
    'docs/verification/day-numeric-filesystem-successor/root-review/checkpoint.json': '0915b1523e156970aa804ec5489bc73913ed036ab0a4f2addb9fd71e4d9de862',
    'docs/verification/day-numeric-filesystem-successor/tooling-pin-review/checkpoint.json': '4d3e3621f68230a230e09374194ebfc001e420e264fec68a6aa53de3176b76f4',
}
os.environ['GIT_OPTIONAL_LOCKS'] = '0'

def git(*args):
    return subprocess.check_output(['git', '--git-dir=' + str(GIT), *args])

def digest(data):
    return hashlib.sha256(data).hexdigest()

def identity(data):
    return {'bytes': len(data), 'sha256': digest(data)}

def blobid(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

assert git('rev-parse', 'refs/heads/main').decode().strip() == PARENT
tree = {}
for entry in git('ls-tree', '-rz', '--full-tree', PARENT).split(b'\0'):
    if entry:
        info, path = entry.split(b'\t', 1)
        mode, kind, oid = info.decode().split()
        tree[path.decode()] = (mode, kind, oid)

def fetched(path):
    mode, kind, oid = tree[path]
    assert mode == '100644' and kind == 'blob', path
    data = git('cat-file', 'blob', oid)
    assert blobid(data) == oid, path
    return data

checkpoint_bindings = []
for path, sha in CHECKPOINTS.items():
    data = fetched(path)
    assert digest(data) == sha, path
    checkpoint_bindings.append({'path': path, **identity(data), 'git_blob_sha1': tree[path][2]})

cp_bytes = fetched(PACKAGE + '/checkpoint.json')
assert cp_bytes == (LOCAL / 'checkpoint.json').read_bytes()
cp = json.loads(cp_bytes)
assert cp['active_application_modified'] is False
assert cp['android_executed'] is False
assert len(cp['active_files']) == 9
assert {r['path'] for r in cp['active_files']} == EXPECTED
assert len({r['path'] for r in cp['active_files']}) == 9
assert {p for p in tree if p.startswith('tools/day_numeric_acceptance/')} == {
    p for p in EXPECTED if p.startswith('tools/')
}
declared = {r['path']: r for r in cp['files']}
assert len(declared) == 2964
receipt_path = ROOT / 'numeric-tooling-reviewed-export/remote-verification.json'
receipt_bytes = receipt_path.read_bytes()
receipt = json.loads(receipt_bytes)
assert receipt['commit'] == PARENT and receipt['verified_paths'] == 3205
assert receipt['git_mode_size_sha1_sha256_verified'] is True
assert receipt['staged_bytes_and_modes_equal_fetched_git'] is True

manifest = []
elements = []
bindings = []
for row in cp['active_files']:
    path = row['path']
    assert row['source'] == 'source/' + path
    assert row['mode'] == '100644' and row['must_be_absent'] is False
    before = fetched(path)
    assert identity(before) == row['baseline'], path
    source_path = PACKAGE + '/' + row['source']
    candidate = fetched(source_path)
    assert identity(candidate) == row['candidate'], path
    assert {k: declared[row['source']][k] for k in ('bytes', 'sha256')} == row['candidate']
    local_path = LOCAL / row['source']
    st = local_path.lstat()
    assert stat.S_ISREG(st.st_mode) and not st.st_mode & 0o111
    assert local_path.read_bytes() == candidate
    oid = tree[source_path][2]
    elements.append({'path': path, 'mode': '100644', 'type': 'blob', 'sha': oid})
    manifest.append({'path': path, 'local_path': str(local_path), 'size_bytes': len(candidate),
                     'sha256': digest(candidate), 'git_blob_sha1': oid, 'mode': '100644'})
    bindings.append({'path': path, 'mode': '100644', 'baseline': row['baseline'],
                     'baseline_git_blob_sha1': tree[path][2], 'candidate': row['candidate'],
                     'candidate_git_blob_sha1': oid, 'fetched_source_path': source_path})

protected = {}
for path in ('project', 'artifacts/current', 'vendor'):
    protected[path] = git('rev-parse', PARENT + ':' + path).decode().strip()
guard = {
    'status': 'EXACT_NINE_PATH_TOOLING_ACTIVATION_PREPARED',
    'completed_utc': datetime.now(timezone.utc).isoformat(),
    'parent_commit': PARENT,
    'checkpoint_and_reviews': checkpoint_bindings,
    'fetched_full_batch_receipt': identity(receipt_bytes),
    'active_path_bindings': bindings,
    'active_tools_directory_exact_eight_files': True,
    'protected_tree_oids': protected,
    'all_nine_baselines_and_modes_match_fetched_git': True,
    'all_nine_candidates_match_fetched_reviewed_package': True,
    'new_application_source_or_apk_promotion': False,
    'hosted_execution_result': 'PENDING_NEW_WORKFLOW_RUN',
    'workspace_or_index_mutated': False,
    'scope': 'Activate the reviewed command filesystem evidence tooling and isolated numeric acceptance workflow only.',
}
EXPORT.mkdir()
doc_root = TREE / TARGET
doc_root.mkdir(parents=True)
docs = {
    'activation-guard.json': (json.dumps(guard, indent=2) + '\n').encode(),
    'executed-prepare.py': Path(__file__).read_bytes(),
    'reviewed-package-fetch-verification.json': receipt_bytes,
    'README.md': (
        '# Numeric filesystem evidence tooling activation\n\n'
        'This checkpoint applies the exact nine tooling/workflow paths from the reviewed '
        '`815612f8` package after the entire package and both independent reviews were fetched '
        'and verified at commit `' + PARENT + '`. The application source and current APK are unchanged.\n\n'
        'The frozen package passed 92 focused host controls. The earlier hosted run failed '
        'before application materialization or build; that failure remains preserved. The new '
        'workflow will execute isolated numeric acceptance against the fixed application baseline '
        'and the reviewed source overlay. Its actual full sixteen-gate result is pending at this commit.\n\n'
        'The [guard receipt](activation-guard.json) binds each old and new byte sequence and mode, '
        'the fetched package and review manifests, and the protected application trees. '
        'The [executed preparer](executed-prepare.py) performs only local read verification and '
        'writes this bounded publication evidence. Remote ref and fetched-commit verification '
        'occur separately with an expected-parent guard.\n'
    ).encode(),
}
for name, data in docs.items():
    path = TARGET + '/' + name
    assert path not in tree, path
    local = doc_root / name
    local.write_bytes(data)
    local.chmod(0o644)
    oid = blobid(data)
    elements.append({'path': path, 'mode': '100644', 'type': 'blob', 'content': data.decode('utf-8')})
    manifest.append({'path': path, 'local_path': str(local), 'size_bytes': len(data),
                     'sha256': digest(data), 'git_blob_sha1': oid, 'mode': '100644'})
assert len(manifest) == 13 and len({r['path'] for r in manifest}) == 13
(EXPORT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
(EXPORT / 'tree-elements.json').write_text(json.dumps(elements) + '\n')
(EXPORT / 'preparation.json').write_text(json.dumps(guard, indent=2) + '\n')
print(json.dumps({'parent': PARENT, 'paths': len(manifest), 'active_tooling_paths': 9,
                  'new_evidence_paths': 4, 'bytes': sum(r['size_bytes'] for r in manifest),
                  'baseline_and_candidate_bytes_modes_verified': True,
                  'application_source_or_apk_promoted': False}))
