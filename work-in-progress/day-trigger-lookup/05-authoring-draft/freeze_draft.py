#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

root = Path(__file__).resolve().parent
stage = root / 'stage-01'
target = root / 'checkpoints/01-paused-authoring-draft'
assert not target.exists()
assert not (stage / 'source-slice.json').exists()
def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'mode': path.stat().st_mode & 0o777}
prep = json.loads((stage / 'preparation.json').read_text())
inventory = {}
for row in prep['copied_baseline_paths']:
    for folder in ('project', 'baseline'):
        p = stage / folder / row['path']
        assert identity(p) == row['baseline']
        inventory[folder + '/' + row['path']] = identity(p)
assert len(inventory) == 38
target.mkdir(parents=True)
paths = ['prepare_overlay.py', 'stage_sources.py', 'lookup_adapter_tail.java.txt', 'AUTHORING_DRAFT.md',
         'freeze_draft.py', 'stage-01/preparation.json']
for name in paths:
    p = target / name; p.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(root / name, p)
(target / 'unchanged-staging-inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')
paths.append('unchanged-staging-inventory.json')
files = [{'path': name, **identity(target / name)} for name in sorted(paths)]
cp = {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(), 'status': 'FROZEN_UNEXECUTED_AUTHORING_DRAFT',
      'repo_target': 'work-in-progress/day-trigger-lookup/05-authoring-draft',
      'baseline_checkpoint_sha256': prep['numeric_checkpoint_sha256'],
      'approved_plan_checkpoint_sha256': prep['approved_plan_checkpoint_sha256'],
      'files': files, 'actual_staging_application_changes': [], 'derivation_executed': False,
      'new_app_or_host_execution': False, 'full_build_or_signing': False, 'active_source_changed': False,
      'pause_reason': 'Prioritize independent review of actual readiness Android failure 38230072388.'}
data = (json.dumps(cp, indent=2, sort_keys=True) + '\n').encode(); (target / 'checkpoint.json').write_bytes(data)
print(json.dumps({'checkpoint': str(target / 'checkpoint.json'), **identity(target / 'checkpoint.json'),
                  'files': len(files), 'payload_bytes': sum(row['bytes'] for row in files)}, indent=2))
