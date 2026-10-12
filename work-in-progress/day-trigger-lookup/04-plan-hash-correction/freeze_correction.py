#!/usr/bin/env python3
"""Correct one documentation literal without modifying the original capsule."""
from pathlib import Path
import hashlib
import json
import shutil
import difflib
from datetime import datetime, timezone

root = Path(__file__).resolve().parent
baseline = Path('/dev/shm/macrodroid-day-lookup-integration-plan/checkpoints/01-integration-plan')
expected = '462bc9df44e1e5e99382f2dcae7c49c8c097f3c09ebc77b299bfc57378567daa'
correct = 'c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f'
wrong = 'c59d9624844864de085723167ed6e0ef17e06ba0206a33649e92b2f'
sha = lambda value: hashlib.sha256(value).hexdigest()
raw_cp = (baseline / 'checkpoint.json').read_bytes()
assert sha(raw_cp) == expected
cp = json.loads(raw_cp)
before = {}
for row in cp['files']:
    data = (baseline / row['path']).read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256']
    before[row['path']] = sha(data)
old = (baseline / 'INTEGRATION_PLAN.md').read_text()
assert old.count(wrong) == 1
new = old.replace(wrong, correct, 1)
target = root / 'checkpoints/02-hash-literal-correction'
target.mkdir(parents=True, exist_ok=False)
(target / 'INTEGRATION_PLAN.md').write_text(new)
(target / 'original-INTEGRATION_PLAN.md').write_text(old)
(target / 'original-checkpoint.json').write_bytes(raw_cp)
shutil.copy2(__file__, target / 'freeze_correction.py')
(target / 'correction.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile='original/INTEGRATION_PLAN.md', tofile='corrected/INTEGRATION_PLAN.md')))
assert {name: sha((baseline / name).read_bytes()) for name in before} == before
receipt = {'status': 'EXACT_SINGLE_HASH_LITERAL_CORRECTED', 'original_checkpoint_sha256': expected,
           'correct_numeric_checkpoint_sha256': correct, 'old_plan_sha256': sha(old.encode()),
           'corrected_plan_sha256': sha(new.encode()), 'replacement_count': 1,
           'original_capsule_files_unchanged': len(before), 'source_code_changed': False,
           'note': 'Only the opening paragraph was wrong; original machine-readable checkpoint/input bindings were already exact.'}
(target / 'correction.json').write_text(json.dumps(receipt, indent=2) + '\n')
files = [{'path': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes()), 'mode': p.stat().st_mode & 0o777} for p in sorted(target.iterdir())]
result = {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(), 'status': 'FROZEN_DOCUMENTATION_CORRECTION_ONLY',
          'repo_target': 'work-in-progress/day-trigger-lookup/04-plan-hash-correction', 'parent_checkpoint_sha256': expected,
          'files': files, 'active_source_changed': False}
payload = (json.dumps(result, indent=2, sort_keys=True) + '\n').encode()
(target / 'checkpoint.json').write_bytes(payload)
print(json.dumps({'checkpoint': str(target / 'checkpoint.json'), 'bytes': len(payload), 'sha256': sha(payload),
                  'files': len(files), 'payload_bytes': sum(row['bytes'] for row in files), 'correction': receipt}, indent=2))
