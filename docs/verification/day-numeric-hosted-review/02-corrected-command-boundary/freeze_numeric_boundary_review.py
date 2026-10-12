"""Freeze the closed selected-test review without mutating its source capsule."""
from pathlib import Path
import datetime, hashlib, json, shutil, stat

root = Path('/dev/shm/macrodroid-transfer-space-20261012/day-numeric-final-boundary-review')
shutil.copyfile(Path(__file__), root / Path(__file__).name)
rows = []
for path in sorted(root.rglob('*')):
    if path.is_dir():
        continue
    relative = path.relative_to(root).as_posix()
    assert relative != 'checkpoint.json'
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode)
    data = path.read_bytes()
    rows.append({'path': relative, 'bytes': len(data),
                 'sha256': hashlib.sha256(data).hexdigest(), 'mode': stat.S_IMODE(mode)})
assert json.loads((root / 'result.json').read_text())['passed'] is True
value = {'schema': 1, 'status': 'FROZEN_NARROW_CORRECTED_BOUNDARY_REVIEW',
         'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'repo_target': 'docs/verification/day-numeric-hosted-review/02-corrected-command-boundary',
         'reviewed_package_checkpoint_sha256': '994a29b51e3758cf9f3b32e5bd22a489009cfd45febb31f3d403572ffc1e9473',
         'active_files': [], 'android_executed_here': False,
         'scope': 'Nine selected synthetic controls and unchanged frozen-source verification only',
         'files': rows}
raw = (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
(root / 'checkpoint.json').write_bytes(raw)
print(json.dumps({'path': str(root / 'checkpoint.json'), 'bytes': len(raw),
                  'sha256': hashlib.sha256(raw).hexdigest(), 'files': len(rows),
                  'payload_bytes': sum(row['bytes'] for row in rows)}))
