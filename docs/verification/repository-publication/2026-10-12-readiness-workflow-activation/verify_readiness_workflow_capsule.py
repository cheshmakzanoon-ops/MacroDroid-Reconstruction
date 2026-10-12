"""Verify the exact closed workflow capsule and lossless evidence-role mapping."""
from pathlib import Path, PurePosixPath
import hashlib, json, stat, tarfile

SOURCE = Path('/dev/shm/macrodroid-notification-readiness/checkpoints/02-thirteen-screen-readiness-workflow')
OUT = Path('/dev/shm/macrodroid-transfer-space-20261012/readiness-workflow-verification.json')
EXPECTED = '3ca1103f0e247cb827be1d654ce082989658a54cfb8b6b7c4f2c655fd553c50b'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def safe(value):
    p = PurePosixPath(value)
    assert not p.is_absolute() and '..' not in p.parts and p.as_posix() == value
    return value

raw = (SOURCE / 'checkpoint.json').read_bytes()
assert sha(raw) == EXPECTED
cp = json.loads(raw)
assert len(cp['files']) == len({r['path'] for r in cp['files']}) == 13
assert cp['android_executed'] is False and cp['active_changes'] is False
for row in cp['files']:
    p = SOURCE / safe(row['path'])
    assert stat.S_ISREG(p.lstat().st_mode) and not p.is_symlink()
    b = p.read_bytes()
    assert len(b) == row['bytes'] and sha(b) == row['sha256']
manifest = json.loads((SOURCE / 'offline-evidence-manifest.json').read_text())
rows = manifest['files']
assert len(rows) == len({safe(r['path']) for r in rows}) == manifest['file_count'] == 8641
expected_members = {}
external_counts = {}
for row in rows:
    assert type(row['mode']) is int and row['mode'] in (0o644, 0o755)
    if 'archive_member' in row:
        member = safe(row['archive_member'])
        assert member == 'blobs/sha256/' + row['sha256'] + '.bin'
        identity = (row['bytes'], row['sha256'])
        assert member not in expected_members or expected_members[member] == identity
        expected_members[member] = identity
    else:
        digest = row['external_input_sha256']
        expected = manifest['exact_already_published_runtime_inputs'][digest]
        assert (row['bytes'], row['sha256']) == (expected['bytes'], expected['sha256'])
        external_counts[digest] = external_counts.get(digest, 0) + 1
assert len(expected_members) == manifest['unique_archived_payloads'] == 276
with tarfile.open(SOURCE / 'offline-evidence-blobs.tar.gz', 'r:gz') as archive:
    members = archive.getmembers()
    assert all(m.isfile() and not m.issym() and not m.islnk() for m in members)
    assert len(members) == len({safe(m.name) for m in members}) == 276
    assert {m.name for m in members} == set(expected_members)
    for member in members:
        b = archive.extractfile(member).read()
        assert (len(b), sha(b)) == expected_members[member.name]
        assert member.mode == 0o644
expected_sources = {
    '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800': '/workspace/scratch/4130730d15aa/recovered/automation android app',
    '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182': '/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/dist/MacroDroid-5.67.8-v9-hybrid.apk',
    '6fbed5edaddcfbee99a3ae6e7208c8654c6cb2bedb4ed5cbbf4e154d7d38a745': '/workspace/scratch/4130730d15aa/current/MacroDroid_v9/tools/prebuilt/linux/aapt2',
}
assert set(manifest['exact_already_published_runtime_inputs']) == set(expected_sources)
for digest, row in manifest['exact_already_published_runtime_inputs'].items():
    assert row['source'] == expected_sources[digest]
    p = Path(row['source'])
    assert p.is_file() and not p.is_symlink() and p.stat().st_size == row['bytes']
    with p.open('rb') as stream:
        assert hashlib.file_digest(stream, 'sha256').hexdigest() == digest
assert len(manifest['inert_symlink_controls']) == 1
assert all(r['restored_as_symlink'] is False for r in manifest['inert_symlink_controls'])
for row in cp['files']:
    b = (SOURCE / row['path']).read_bytes()
    assert len(b) == row['bytes'] and sha(b) == row['sha256']
result = dict(checkpoint_sha256=EXPECTED, capsule_files=13,
              exact_regular_evidence_roles=8641, verified_unique_archive_payloads=276,
              verified_external_runtime_inputs=3, external_role_counts=external_counts,
              inert_symlink_controls=1, all_frozen_bytes_unchanged=True,
              android_executed=False, active_paths_changed=False,
              scope='Transfer-integrity checks of exact frozen bytes and external input bindings; no new host or Android execution')
OUT.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
