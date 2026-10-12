"""Bind frozen logical archive references to exact fetched multipart storage."""
from pathlib import Path
import datetime, hashlib, json, shutil, stat, subprocess
ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012')
GIT = ROOT / 'verification.git'
COMMIT = 'd51f1b8d2b7972619bd69d6d8d1456a73e753e3e'
PREFIX = 'docs/verification/android-exact-alarm-navigation-3f0ebc9'
OUT = ROOT / 'alarm14-archive-layout-addendum'
OUT.mkdir(exist_ok=False)
def digest(raw): return hashlib.sha256(raw).hexdigest()
def git_bytes(name):
    return subprocess.check_output(['git', '--git-dir=' + str(GIT), 'show', COMMIT + ':' + name])
def put(name, raw):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as stream: stream.write(raw)
    p.chmod(0o644)
cp = git_bytes(PREFIX + '/analysis/checkpoint.json')
assert digest(cp) == '57a5a23f61ae4c115db2a629c8bad8359d6f20d76612f3bd63265e8e8a2af149'
external_raw = git_bytes(PREFIX + '/analysis/external-evidence.json')
external = json.loads(external_raw)
manifest_raw = git_bytes(PREFIX + '/manifest.json')
manifest = json.loads(manifest_raw)
receipt_raw = (ROOT / 'alarm14-and-source-reviews-export/fetched-archive-reassembly-verification.json').read_bytes()
receipt = json.loads(receipt_raw)
assert receipt['commit'] == COMMIT and receipt['status'] == 'FETCHED_MULTIPART_CONTAINER_IDENTITIES_VERIFIED'
container = receipt['containers'][0]
assert container['manifest_sha256'] == digest(manifest_raw)
assert container['bytes'] == external['zip']['bytes'] == manifest['size_bytes'] == 46626337
assert container['sha256'] == external['zip']['sha256'] == manifest['sha256'] == 'c34d417c0b5d996e62d403023e9f9c9d122633c2ea65fb1cf45599643abdcf04'
assert len(container['parts']) == len(manifest['parts']) == 6
whole = hashlib.sha256(); size = 0
for row, checked in zip(manifest['parts'], container['parts']):
    raw = git_bytes(row['path'])
    oid = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    assert len(raw) == row['size_bytes'] == checked['bytes']
    assert digest(raw) == row['sha256'] == checked['sha256']
    assert oid == row['git_blob_sha1'] == checked['git_blob_sha1']
    whole.update(raw); size += len(raw)
assert size == manifest['size_bytes'] and whole.hexdigest() == manifest['sha256']
actual_receipt_path = PREFIX + '/extraction-receipt.json'
actual_receipt_raw = git_bytes(actual_receipt_path)
assert len(actual_receipt_raw) == external['extraction_receipt']['bytes']
assert digest(actual_receipt_raw) == external['extraction_receipt']['sha256']
resolution = {
    'schema': 1, 'status': 'FROZEN_LOGICAL_REFERENCES_RESOLVED_TO_EXACT_PUBLISHED_LAYOUT',
    'verified_commit': COMMIT,
    'immutable_analysis_checkpoint': {'path': PREFIX + '/analysis/checkpoint.json', 'sha256': digest(cp)},
    'immutable_external_evidence': {'path': PREFIX + '/analysis/external-evidence.json', 'sha256': digest(external_raw)},
    'archive': {'logical_path': external['zip']['repository_path'],
                'stored_manifest_path': PREFIX + '/manifest.json', 'manifest_sha256': digest(manifest_raw),
                'part_count': len(manifest['parts']), 'bytes': size, 'sha256': whole.hexdigest(),
                'logical_path_is_a_reassembly_output_not_a_committed_single_blob': True,
                'assembled_container_written_here': False},
    'extraction_receipt': {'logical_path': external['extraction_receipt']['repository_path'],
                           'stored_path': actual_receipt_path, 'bytes': len(actual_receipt_raw),
                           'sha256': digest(actual_receipt_raw), 'same_exact_bytes': True},
    'raw_member_root': external['raw']['repository_path'],
    'raw_member_or_frozen_analysis_modified': False, 'new_runtime_execution': False,
    'verified_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
}
put('reference-resolution.json', (json.dumps(resolution, indent=2) + '\n').encode())
put('fetched-archive-reassembly-verification.json', receipt_raw)
put('frozen-external-evidence.json', external_raw)
put('executed-addendum.py', Path(__file__).read_bytes())
readme = '''# Fourteen-screen archive reference addendum

The frozen analysis names `artifact.zip` as the original logical container. Its exact bytes are committed as six parts through [the artifact manifest](../manifest.json). The complete 46,626,337-byte container has SHA-256 `c34d417c0b5d996e62d403023e9f9c9d122633c2ea65fb1cf45599643abdcf04`.

The six fetched Git blobs were independently rehashed and streamed in order at commit `d51f1b8d2b7972619bd69d6d8d1456a73e753e3e`; no assembled duplicate was written. To validate the committed parts from the repository root:

```bash
python3 scripts/assemble_artifact.py docs/verification/android-exact-alarm-navigation-3f0ebc9/manifest.json --verify-only
```

To produce the precise logical ZIP path used in the frozen external-evidence record:

```bash
python3 scripts/assemble_artifact.py docs/verification/android-exact-alarm-navigation-3f0ebc9/manifest.json --output docs/verification/android-exact-alarm-navigation-3f0ebc9/artifact.zip
```

The record also calls the extraction receipt `extracted-extraction.json`. Those identical receipt bytes are committed as [extraction-receipt.json](../extraction-receipt.json), with SHA-256 `4d0c142fa40cc52c909d59e2183392425e08cea3e04800d3e04b2afe897a2f28`. The raw member root remains [extracted/](../extracted/).

[reference-resolution.json](reference-resolution.json) binds both logical names to the published layout. The frozen `57a5a23f...` analysis and all raw members remain unchanged. This addendum supplies storage references only; it does not alter the measured fourteen-screen difference or add a runtime result.
'''
put('README.md', readme.encode())
files=[]
for path in sorted(OUT.rglob('*')):
    if path.is_file():
        raw=path.read_bytes(); files.append({'path':path.relative_to(OUT).as_posix(),'bytes':len(raw),'sha256':digest(raw),'mode':stat.S_IMODE(path.stat().st_mode)})
checkpoint={'schema':1,'repo_target':PREFIX+'/archive-layout-addendum','active_files':[],
            'status':resolution['status'],'files':files}
put('checkpoint.json',(json.dumps(checkpoint,indent=2)+'\n').encode())
print(json.dumps({'source':str(OUT),'target':checkpoint['repo_target'],'checkpoint_sha256':digest((OUT/'checkpoint.json').read_bytes()),'files':len(files),'bytes':sum(r['bytes'] for r in files)}))
