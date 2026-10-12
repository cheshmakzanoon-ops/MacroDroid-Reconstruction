#!/usr/bin/env python3
"""Freeze only the small authored review; do not copy app sources or tool caches."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import stat

root = Path(__file__).resolve().parent
target = root / 'checkpoints/01-integration-plan'
assert not target.exists()
paths = sorted(p for p in root.rglob('*') if p.is_file() and 'checkpoints' not in p.relative_to(root).parts)
assert all(not p.is_symlink() for p in paths)
assert sum(p.stat().st_size for p in paths) < 1024 * 1024
target.mkdir(parents=True)
files = []
for source in paths:
    name = source.relative_to(root).as_posix()
    destination = target / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    data = source.read_bytes()
    shutil.copy2(source, destination)
    assert destination.read_bytes() == data
    assert stat.S_IMODE(destination.stat().st_mode) == stat.S_IMODE(source.stat().st_mode)
    files.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                  'mode': stat.S_IMODE(source.stat().st_mode)})
result = json.loads((target / 'evidence/result.json').read_text())
assert result['status'] == 'READ_ONLY_LOOKUP_INTEGRATION_PLAN_INPUTS_VERIFIED'
checkpoint = {
    'schema': 1,
    'status': 'FROZEN_READ_ONLY_LOOKUP_INTEGRATION_PLAN',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'repo_target': 'work-in-progress/day-trigger-lookup/03-integration-plan',
    'scope': 'Read-only prospective integration against frozen numeric 19-path overlay; no newly executed app, build, Android or active recovery claim.',
    'numeric_baseline_checkpoint_sha256': result['numeric_checkpoint_sha256'],
    'lookup_proof_checkpoint_sha256': result['lookup_checkpoint_sha256'],
    'source_changes': [],
    'prospective_source_paths': 21,
    'prospective_new_source_paths': 6,
    'active_registration_changed': False,
    'apk_changed': False,
    'files': files,
}
payload = (json.dumps(checkpoint, indent=2, sort_keys=True) + '\n').encode()
(target / 'checkpoint.json').write_bytes(payload)
print(json.dumps({'checkpoint': str(target / 'checkpoint.json'), 'bytes': len(payload),
                  'sha256': hashlib.sha256(payload).hexdigest(), 'files': len(files),
                  'payload_bytes': sum(row['bytes'] for row in files)}, indent=2))
