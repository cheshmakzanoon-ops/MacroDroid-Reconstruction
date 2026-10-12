from pathlib import Path
from datetime import datetime, timezone
import difflib
import hashlib
import json
import shutil
import stat

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'checkpoints/01-promotion-review'
PROPOSAL = Path('/dev/shm/macrodroid-transfer-space-20261012/numeric-source-promotion-proposal')
def identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
def put(name, raw):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as stream:
        stream.write(raw)
    p.chmod(0o644)
def dump(value):
    return (json.dumps(value, indent=2) + '\n').encode()
OUT.mkdir(parents=True, exist_ok=False)
first = json.loads((ROOT / 'attempt-01/result.json').read_bytes())
last = json.loads((ROOT / 'attempt-02/result.json').read_bytes())
assert first['passed'] is False and last['passed'] is True
before = json.loads((ROOT / 'attempt-02/proposal-before.json').read_bytes())
now = []
for p in sorted(PROPOSAL.rglob('*')):
    s = p.lstat()
    assert not stat.S_ISLNK(s.st_mode)
    if stat.S_ISDIR(s.st_mode):
        continue
    assert stat.S_ISREG(s.st_mode)
    now.append({'path': p.relative_to(PROPOSAL).as_posix(), **identity(p.read_bytes()), 'mode': stat.S_IMODE(s.st_mode)})
assert before == now
for part in ('README.md', 'review_numeric_promotion.py', 'freeze_review.py'):
    put(part, (ROOT / part).read_bytes())
for dirname in ('attempt-01', 'attempt-02'):
    for p in sorted((ROOT / dirname).rglob('*')):
        if p.is_file():
            assert stat.S_ISREG(p.lstat().st_mode)
            put(p.relative_to(ROOT).as_posix(), p.read_bytes())
old = (ROOT / 'attempt-01/executed-review.py').read_text()
new = (ROOT / 'attempt-02/executed-review.py').read_text()
put('reviewer-correction.patch', ''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile='attempt-01/executed-review.py', tofile='attempt-02/executed-review.py')).encode())
put('final-proposal-preservation.json', dump({'proposal_files': len(now), 'unchanged': True, 'inventory_sha256': identity((ROOT / 'attempt-02/proposal-before.json').read_bytes())['sha256']}))
files = []
for p in sorted(OUT.rglob('*')):
    if p.is_file():
        files.append({'path': p.relative_to(OUT).as_posix(), **identity(p.read_bytes()), 'mode': stat.S_IMODE(p.stat().st_mode)})
checkpoint = {'schema': 1, 'status': 'INDEPENDENT_NUMERIC_22_PROMOTION_IDENTITY_REVIEW_PASS',
              'created_utc': datetime.now(timezone.utc).isoformat(),
              'repo_target': 'docs/verification/day-trigger-numeric/11-source-promotion-independent-review',
              'proposal_checkpoint': last['proposal_checkpoint'], 'source_paths': 19, 'promotion_paths': 22,
              'future_entries': 81298, 'streamed_apk_parts': 12, 'application_gates_executed': 0,
              'android_executed': False, 'git_writes': False, 'active_promoted': False,
              'initial_reviewer_failure_preserved': True, 'files': files}
put('checkpoint.json', dump(checkpoint))
print(json.dumps({'path': str(OUT / 'checkpoint.json'), **identity((OUT / 'checkpoint.json').read_bytes()),
                  'files': len(files), 'payload_bytes': sum(r['bytes'] for r in files)}))
