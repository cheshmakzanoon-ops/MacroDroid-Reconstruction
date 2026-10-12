"""Verify the inactive producer successor against fetched prior source identities."""
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import stat
import subprocess

root = Path('/dev/shm/day-numeric-hosted-02/checkpoints/01-command-filesystem-source-successor')
git = ['git', '--git-dir=/dev/shm/macrodroid-transfer-space-20261012/verification.git']
raw = (root / 'checkpoint.json').read_bytes()
assert hashlib.sha256(raw).hexdigest() == 'd9ddd3e0f692c66e2cd47870ff3cf95bfa0a2b1cd50fc2fd55a3c09e66df9bcf'
cp = json.loads(raw)
assert cp['active_files'] == [] and len(cp['files']) == 408
assert len(cp['files']) == len({row['path'] for row in cp['files']})
for row in cp['files']:
    path = root / row['path']
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode) and stat.S_IMODE(mode) in (0o644, 0o755)
    data = path.read_bytes()
    assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
future_raw = gzip.decompress((root / 'evidence/future-input-snapshot.json.gz').read_bytes())
assert len(future_raw) == cp['future_manifest']['bytes']
assert hashlib.sha256(future_raw).hexdigest() == cp['future_manifest']['sha256']
future = json.loads(future_raw)
assert future['files'] == len(future['entries']) == cp['future_snapshot']['files'] == 81298
canonical = json.dumps(future['entries'], sort_keys=True, separators=(',', ':')).encode()
assert hashlib.sha256(canonical).hexdigest() == future['snapshot_sha256'] == cp['future_snapshot']['snapshot_sha256']
baseline_raw = subprocess.check_output(git + ['show', 'dbcad968c5c3e8f084205393a6c0d2d06a203c71:project/reports/release-input-snapshot.json'])
assert hashlib.sha256(baseline_raw).hexdigest() == 'ca3bed290f18a378c7a3d6cc70d924c8d6ec85481e236b4e7561c31fedafdfbe'
baseline = json.loads(baseline_raw)
expected = dict(baseline['entries'])
changed_from_prior = []
bindings = []
assert len(cp['source_changes']) == 19
for row in cp['source_changes']:
    path = row['path']
    candidate = (root / row['source']).read_bytes()
    assert len(candidate) == row['candidate']['bytes']
    assert hashlib.sha256(candidate).hexdigest() == row['candidate']['sha256']
    original = baseline['entries'].get(path)
    if row['baseline'] is None:
        assert original is None and row['must_be_absent_if_new'] is True
    else:
        assert original == {'size': row['baseline']['bytes'], 'sha256': row['baseline']['sha256']}
    expected[path] = {'size': len(candidate), 'sha256': hashlib.sha256(candidate).hexdigest()}
    previous = subprocess.check_output(git + ['show',
        '394234b0e74c9f1d660836c8f2a89901fe05ff9d:work-in-progress/day-trigger-numeric/06-source-integration/project/' + path])
    same = previous == candidate
    if not same:
        changed_from_prior.append(path)
    bindings.append(dict(path=path, prior_sha256=hashlib.sha256(previous).hexdigest(),
                         candidate_sha256=hashlib.sha256(candidate).hexdigest(), unchanged_from_prior=same))
assert expected == future['entries']
assert changed_from_prior == ['day_numeric_dex_controls.py']
assert (root / 'checkpoint.json').read_bytes() == raw
result = dict(schema=1, status='EXACT_ONE_FILE_SUCCESSOR_AND_COMPLETE_FUTURE_INPUT_MANIFEST_VERIFIED',
              checkpoint_sha256=hashlib.sha256(raw).hexdigest(), capsule_files=408,
              complete_future_manifest=cp['future_manifest'], future_snapshot=cp['future_snapshot'],
              reconstructed_from_fetched_active_manifest_and_exact_19_paths=True,
              changed_from_prior_source_capsule=changed_from_prior, source_bindings=bindings,
              decompressed_manifest_written=False, active_source_or_workflow_changed=False,
              application_build_or_android_execution=False,
              executed_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              completed_utc=datetime.now(timezone.utc).isoformat())
out = Path('/dev/shm/macrodroid-transfer-space-20261012/numeric-filesystem-successor-verification.json')
with out.open('x') as stream:
    stream.write(json.dumps(result, indent=2) + '\n')
print(json.dumps({key: value for key, value in result.items() if key != 'source_bindings'}))
