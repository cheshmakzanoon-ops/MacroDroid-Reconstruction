"""Verify all exact frozen lookup adapter files and archived evidence in memory."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import tarfile

root = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/02-original-jvm-adapter-controls')
checkpoint_raw = (root / 'checkpoint.json').read_bytes()
assert hashlib.sha256(checkpoint_raw).hexdigest() == 'c0d1a691aeb857607b1b44ca0eb66a2a5799b8c02726b39e6acec5a0c49646f7'
cp = json.loads(checkpoint_raw)
assert cp['active_source_changed'] is False and cp['androidRuntime'] is False
assert len(cp['files']) == 41
for row in cp['files']:
    path = root / row['path']
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode) and stat.S_IMODE(mode) == row['mode']
    raw = path.read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
inventory = json.loads((root / 'evidence-files.json').read_bytes())
expected = {row['path']: row for row in inventory}
assert len(expected) == len(inventory) == 297
actual = set()
with tarfile.open(root / 'evidence.tar.gz', 'r:gz') as archive:
    for item in archive:
        name = PurePosixPath(item.name)
        assert not name.is_absolute() and '..' not in name.parts and name.as_posix() == item.name
        assert item.isfile() and item.name not in actual and item.name in expected
        row = expected[item.name]
        assert item.size == row['bytes'] and item.mode == row['mode']
        with archive.extractfile(item) as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        assert digest == row['sha256']
        actual.add(item.name)
assert actual == set(expected)
assert (root / 'checkpoint.json').read_bytes() == checkpoint_raw
result = dict(schema=1, status='ALL_FROZEN_LOOKUP_ADAPTER_FILES_AND_ARCHIVE_MEMBERS_VERIFIED',
              checkpoint_sha256=hashlib.sha256(checkpoint_raw).hexdigest(), files=41,
              archive_members=297, archive_sha256=cp['evidence_archive']['sha256'],
              archive_bytes=cp['evidence_archive']['bytes'], bytes_and_modes_verified=True,
              archive_extracted=False, active_source_changed=False,
              application_or_android_execution=False,
              executed_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              completed_utc=datetime.now(timezone.utc).isoformat())
out = Path('/dev/shm/macrodroid-transfer-space-20261012/lookup-adapter-archive-verification.json')
with out.open('x') as stream:
    stream.write(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
