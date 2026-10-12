"""Exact file/archive verification of the inactive combined-host design capsule."""
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import hashlib
import json
import stat
import tarfile

root = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/06-combined-host-workflow-design')
raw = (root / 'checkpoint.json').read_bytes()
assert hashlib.sha256(raw).hexdigest() == '3da7b4fa3707c301256c8dd7236c18f7680d2fb5bd72595d353e8a01b223830f'
cp = json.loads(raw)
assert cp['active_source_changed'] is False and cp['workflow_authored_or_activated'] is False
assert cp['full_host_acceptance_executed'] is False
assert len(cp['files']) == len({r['path'] for r in cp['files']}) == 35
for row in cp['files']:
    name = PurePosixPath(row['path'])
    assert not name.is_absolute() and '..' not in name.parts and name.as_posix() == row['path']
    path = root / row['path']
    assert stat.S_ISREG(path.lstat().st_mode) and not path.is_symlink()
    assert stat.S_IMODE(path.lstat().st_mode) == row['mode']
    data = path.read_bytes()
    assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
inventory = json.loads((root / 'evidence-files.json').read_bytes())
expected = {r['path']: r for r in inventory}
assert len(expected) == len(inventory) == 19
actual = set()
with tarfile.open(root / 'evidence.tar.gz', 'r:gz') as archive:
    for member in archive:
        name = PurePosixPath(member.name)
        assert not name.is_absolute() and '..' not in name.parts and name.as_posix() == member.name
        assert member.isfile() and not member.islnk() and not member.issym() and member.name not in actual
        row = expected[member.name]
        data = archive.extractfile(member).read()
        assert member.mode == row['mode'] and len(data) == row['bytes']
        assert hashlib.sha256(data).hexdigest() == row['sha256']
        assert (root / 'evidence' / member.name).read_bytes() == data
        actual.add(member.name)
assert actual == set(expected)
assert (root / 'checkpoint.json').read_bytes() == raw
result = {'status': 'INACTIVE_LOOKUP_HOST_DESIGN_EXACT_BYTES_VERIFIED',
          'completed_utc': datetime.now(timezone.utc).isoformat(),
          'checkpoint_sha256': hashlib.sha256(raw).hexdigest(), 'payload_files': 35,
          'archive_members': 19, 'all_archived_and_direct_copies_exact': True,
          'source_or_workflow_changed': False, 'application_or_android_execution': False,
          'scope': 'Transport identity verification only; all counts in the design retain their stated unexecuted projection scope.',
          'executed_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
out = Path('/dev/shm/macrodroid-transfer-space-20261012/lookup-host-design-verification.json')
with out.open('x') as stream:
    stream.write(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
