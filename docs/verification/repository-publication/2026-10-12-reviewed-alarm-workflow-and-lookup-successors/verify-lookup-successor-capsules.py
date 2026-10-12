"""Verify exact inactive lookup archives and compressed future manifests without extraction."""
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import gzip
import hashlib
import json
import stat
import tarfile

ROOT = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints')
CASES = [
    ('04-numeric-filesystem-merge', '56aa7bfc05286d9fc474d24e6afc33fbd3a664e9dc731f70912df1a9e375b350', 62, 119),
    ('05-lookup-recorder-successor', '87c2a01a627590b62017eae8145db92d1a7593d5cf127114a9812ec13cd756f5', 56, 168),
]

def safe(path):
    value = PurePosixPath(path)
    assert type(path) is str and path and not value.is_absolute()
    assert '..' not in value.parts and '\\' not in path and value.as_posix() == path

def digest(data):
    return hashlib.sha256(data).hexdigest()

results = []
for directory, checkpoint_sha, count, members in CASES:
    root = ROOT / directory
    raw = (root / 'checkpoint.json').read_bytes()
    assert digest(raw) == checkpoint_sha
    cp = json.loads(raw)
    assert cp['active_source_changed'] is False and cp['full_build_or_signing'] is False and cp['new_apk'] is False
    assert len(cp['files']) == len({r['path'] for r in cp['files']}) == count
    for row in cp['files']:
        safe(row['path'])
        path = root / row['path']
        mode = path.lstat().st_mode
        assert stat.S_ISREG(mode) and not path.is_symlink() and stat.S_IMODE(mode) == row['mode']
        data = path.read_bytes()
        assert len(data) == row['bytes'] and digest(data) == row['sha256']
    rows = json.loads((root / 'evidence-files.json').read_bytes())
    expected = {row['path']: row for row in rows}
    assert len(rows) == len(expected) == members
    actual = set()
    with tarfile.open(root / 'evidence.tar.gz', 'r:gz') as archive:
        for member in archive:
            safe(member.name)
            assert member.isfile() and not member.islnk() and not member.issym()
            assert member.name not in actual
            row = expected[member.name]
            assert member.size == row['bytes'] and member.mode == row['mode']
            with archive.extractfile(member) as stream:
                assert hashlib.file_digest(stream, 'sha256').hexdigest() == row['sha256']
            actual.add(member.name)
    assert actual == set(expected)
    future_raw = gzip.decompress((root / 'future-input-snapshot.json.gz').read_bytes())
    assert len(future_raw) == cp['future_manifest']['bytes'] and digest(future_raw) == cp['future_manifest']['sha256']
    future = json.loads(future_raw)
    assert future['files'] == len(future['entries']) == cp['future_snapshot']['files'] == 81304
    canonical = json.dumps(future['entries'], sort_keys=True, separators=(',', ':')).encode()
    assert digest(canonical) == future['snapshot_sha256'] == cp['future_snapshot']['snapshot_sha256']
    assert (root / 'checkpoint.json').read_bytes() == raw
    results.append({'checkpoint': checkpoint_sha, 'directory': directory, 'files': count,
                    'archive_members': members, 'archive': cp['evidence_archive'],
                    'future_manifest': cp['future_manifest'], 'future_snapshot': cp['future_snapshot'],
                    'all_exact_bytes_and_modes_verified': True,
                    'archive_or_manifest_extracted_to_disk': False,
                    'application_or_android_execution': False})
result = {'schema': 1, 'status': 'LOOKUP_SUCCESSOR_CAPSULE_BYTES_AND_ARCHIVES_VERIFIED',
          'completed_utc': datetime.now(timezone.utc).isoformat(), 'capsules': results,
          'executed_source_sha256': digest(Path(__file__).read_bytes()),
          'scope': 'Exact transport verification of inactive evidence; no new source, test, build, or runtime acceptance claim.'}
out = Path('/dev/shm/macrodroid-transfer-space-20261012/lookup-successor-capsule-verification.json')
with out.open('x') as stream:
    stream.write(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'capsules': len(results), 'files': sum(r['files'] for r in results), 'archive_members': sum(r['archive_members'] for r in results)}))
