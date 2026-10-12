"""Prepare only the sixteen fetched, reviewed indicator diagnostic mappings."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import stat
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--parent', required=True)
parser.add_argument('--receipt', type=Path, required=True)
args = parser.parse_args()
ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012')
GIT = ['git', '--git-dir=' + str(ROOT / 'verification.git')]
PACKAGE = 'work-in-progress/indicator-fixed-sampling/04-closed-synthetic-and-test-correction'
LOCAL = Path('/dev/shm/ink-indicator-fixed-sampling-01/checkpoints/03-closed-synthetic-test-correction')
EXPORT = ROOT / 'indicator-fixed-sampling-activation-export-02'
IMPLEMENTATION_COMMIT = '78d8a01d2e02d2fbfc4d1f20da644dcfd2f8ea1c'
EXPECTED = {
 '.github/workflows/indicator-fixed-sampling.yml',
 'tools/indicator_sampling/README.md',
 'tools/indicator_sampling/aapt2',
 'tools/indicator_sampling/common.py',
 'tools/indicator_sampling/fixtures/candidate-intro1-preinput.xml',
 'tools/indicator_sampling/fixtures/candidate-intro2.xml',
 'tools/indicator_sampling/fixtures/original-intro1-preinput.xml',
 'tools/indicator_sampling/fixtures/original-intro2.xml',
 'tools/indicator_sampling/historical-coordinates.json',
 'tools/indicator_sampling/pins.json',
 'tools/indicator_sampling/prepare.py',
 'tools/indicator_sampling/protocol.json',
 'tools/indicator_sampling/record.py',
 'tools/indicator_sampling/runtime-files.json',
 'tools/indicator_sampling/test_indicator_sampling.py',
 'tools/indicator_sampling/verify.py',
}
os.environ['GIT_OPTIONAL_LOCKS'] = '0'

def git(*argv):
    return subprocess.check_output(GIT + list(argv))

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def oid(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def git_mode(value):
    mode = (int(value, 8) if isinstance(value, str) else value) & 0o777
    assert mode in (0o644, 0o755)
    return format(0o100000 | mode, 'o')

assert git('rev-parse', 'refs/heads/main').decode().strip() == args.parent
entries = {}
for item in git('ls-tree', '-rz', '--full-tree', args.parent).split(b'\0'):
    if item:
        header, name = item.split(b'\t', 1)
        entries[name.decode()] = tuple(header.decode().split())

def fetched(name, expected_mode='100644'):
    mode, kind, object_id = entries[name]
    assert kind == 'blob' and mode == expected_mode, name
    raw = git('cat-file', 'blob', object_id)
    assert oid(raw) == object_id
    return raw

raw_checkpoint = fetched(PACKAGE + '/checkpoint.json')
assert sha(raw_checkpoint) == '89064abe581191cd0690eda4e739a91a9b5bae3c56cb9156533ddd78a857f7be'
checkpoint = json.loads(raw_checkpoint)
assert len(checkpoint['files']) == 3422 and not checkpoint['active_files']
assert git('rev-parse', args.parent + ':' + PACKAGE) == git('rev-parse', IMPLEMENTATION_COMMIT + ':' + PACKAGE)
implementation_receipt_path = ROOT / 'indicator-and-numeric-art-progress-export/remote-verification.json'
implementation_receipt_raw = implementation_receipt_path.read_bytes()
implementation_receipt = json.loads(implementation_receipt_raw)
assert implementation_receipt['commit'] == IMPLEMENTATION_COMMIT
assert implementation_receipt['git_mode_size_sha1_sha256_verified'] is True
assert implementation_receipt['staged_bytes_and_modes_equal_fetched_git'] is True

proofs = []
for prefix, digest, count in [
 ('docs/verification/indicator-fixed-sampling/implementation-review',
  '3a781f2b91b06f2d7884f47030fcd30ec3601bf93ef09534571a178e7412456b', 30),
 ('docs/verification/indicator-fixed-sampling/root-final-activation-review',
  '77d8905c083276a6a6a0593d016f611f9edcb58ff5be6448b52c2a38ec6c5b37', 12),
]:
    raw = fetched(prefix + '/checkpoint.json')
    assert sha(raw) == digest
    review = json.loads(raw)
    assert len(review['files']) == len({row['path'] for row in review['files']}) == count
    for row in review['files']:
        data = fetched(prefix + '/' + row['path'], git_mode(row['mode']))
        assert len(data) == row['bytes'] and sha(data) == row['sha256']
    proofs.append(dict(path=prefix + '/checkpoint.json', sha256=digest,
                       payloads=count, all_fetched_payloads_verified=True))

rows = json.loads(fetched(PACKAGE + '/proposed-source-files.json'))
assert len(rows) == 16 and {row['target'] for row in rows} == EXPECTED
assert len({row['source'] for row in rows}) == 16
declared = {row['path']: row for row in checkpoint['files']}
manifest, elements, bindings = [], [], []
for row in rows:
    target, source_path = row['target'], row['source']
    assert target not in entries, 'Unexpected existing active path: ' + target
    declared_row = declared[source_path]
    mode = git_mode(row['mode'])
    assert (row['bytes'], row['sha256'], mode) == (
        declared_row['bytes'], declared_row['sha256'], git_mode(declared_row['mode']))
    raw = fetched(PACKAGE + '/' + source_path, mode)
    assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
    local = LOCAL / source_path
    info = local.lstat()
    assert stat.S_ISREG(info.st_mode) and git_mode(stat.S_IMODE(info.st_mode)) == mode
    assert local.read_bytes() == raw
    elements.append(dict(path=target, mode=mode, type='blob', sha=oid(raw)))
    manifest.append(dict(path=target, local_path=str(local), size_bytes=len(raw),
                         sha256=sha(raw), git_blob_sha1=oid(raw), mode=mode))
    bindings.append(dict(path=target, expected_absent=True, source=PACKAGE + '/' + source_path,
                         bytes=len(raw), sha256=sha(raw), git_blob_sha1=oid(raw), mode=mode))
assert next(row['sha256'] for row in bindings if row['path'].startswith('.github/')) == '64bcf452be163872aca494294c0e57117d7e15436c21cbc0f13c80ce539c1aeb'
assert next(row['mode'] for row in bindings if row['path'].endswith('/aapt2')) == '100755'
pins = fetched(PACKAGE + '/source/tools/indicator_sampling/pins.json')
pin_object = json.loads(pins)
assert pin_object['parent_commit'] == '6331410cfd2391389270564803623079e8355ad8'
parent_rows = {row['path']: row for row in pin_object['parents']}
assert len(parent_rows) == len(pin_object['parents']) == 16

def pinned_manifest(name, expected_digest):
    row = parent_rows[name]
    assert row['sha256'] == expected_digest and git_mode(row['mode']) == '100644'
    raw = git('show', pin_object['parent_commit'] + ':' + name)
    assert len(raw) == row['bytes'] and sha(raw) == expected_digest
    assert fetched(name) == raw
    return json.loads(raw)

diagnostic_manifest = pinned_manifest(
    'work-in-progress/combined-recovery/05-full-acceptance/apk/manifest.json',
    '459960a6afc81fc0119cd66f3a9f6be823f7947ae90cd74c902d1a8a1e010afc')
original_manifest = pinned_manifest('vendor/original/manifest.json',
    'b2f12b669ac0e937198216458410aaab03da6682659d6d922c730a175b77d684')
assert diagnostic_manifest['sha256'] == '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'
assert diagnostic_manifest['size_bytes'] == 94683119
assert original_manifest['size_bytes'] == 95725918
assert json.loads(fetched('artifacts/current/manifest.json'))['sha256'] == '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd'
receipt_raw = args.receipt.read_bytes()
receipt = json.loads(receipt_raw)
assert receipt['commit'] == args.parent and receipt['git_mode_size_sha1_sha256_verified'] is True
assert receipt['staged_bytes_and_modes_equal_fetched_git'] is True
guard = dict(schema=1, status='SIXTEEN_REVIEWED_ABSENT_INDICATOR_PATHS_READY',
    parent=args.parent, paths=16, bindings=bindings, review_proofs=proofs,
    implementation_checkpoint_sha256=sha(raw_checkpoint),
    unchanged_implementation_tree=git('rev-parse', args.parent + ':' + PACKAGE).decode().strip(),
    implementation_fetched_receipt_sha256=sha(implementation_receipt_raw),
    latest_fetched_receipt_sha256=sha(receipt_raw),
    diagnostic_candidate_sha256='5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182',
    current_application_apk_preserved=True, new_android_diagnostic='PENDING_AUTOMATIC_RUN',
    protected_tree_oids={name:git('rev-parse', args.parent + ':' + name).decode().strip()
                         for name in ('project','artifacts','vendor','docs','work-in-progress')},
    executed_source_sha256=sha(Path(__file__).read_bytes()), no_workspace_or_index_mutation=True,
    completed_utc=datetime.now(timezone.utc).isoformat())
EXPORT.mkdir(exist_ok=False)
for name, value in [('manifest.json', manifest), ('tree-elements.json', elements), ('preparation.json', guard)]:
    with (EXPORT / name).open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')
    (EXPORT / name).chmod(0o644)
print(json.dumps({key:guard[key] for key in ('status','parent','paths','diagnostic_candidate_sha256','completed_utc')}))
