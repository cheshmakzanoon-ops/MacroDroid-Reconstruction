#!/usr/bin/env python3
"""Copy only the approved integration paths after exact baseline verification."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

BASE = Path(__file__).resolve().parent
SOURCE = BASE.parent / 'MacroDroid-Reconstruction/project'
OUT = BASE / 'overlay-01'


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    proposal_path = BASE / 'checkpoints/01-integration-design/proposal.json'
    assert identity(proposal_path)['sha256'] == 'ae98ca78248cc9236ac7c6f60268da56b9905eca41009f50fe2258b6176c4de2'
    proposal = json.loads(proposal_path.read_text())
    for row in proposal['proposed_paths']:
        p = SOURCE / row['path']
        if row['baseline'] is None:
            assert not p.exists(), row['path']
        else:
            assert identity(p) == row['baseline'], row['path']
    for row in proposal['required_unchanged_inputs']:
        assert identity(SOURCE / row['path']) == {k: row[k] for k in ('bytes', 'sha256')}, row['path']
    OUT.mkdir(parents=True, exist_ok=False)
    for row in proposal['proposed_paths']:
        for stem in ('project', 'baseline'):
            p = OUT / stem / row['path']
            p.parent.mkdir(parents=True, exist_ok=True)
            if row['baseline'] is not None:
                shutil.copyfile(SOURCE / row['path'], p)
                assert identity(p) == row['baseline']
    (OUT / 'prepare_overlay.py').write_bytes(Path(__file__).read_bytes())
    receipt = {'schema': 1, 'status': 'EXACT_APPROVED_PATHS_COPIED',
               'created_utc': datetime.now(timezone.utc).isoformat(),
               'source_root': str(SOURCE), 'source_snapshot_sha256': proposal['active_snapshot_sha256'],
               'proposal_sha256': identity(proposal_path)['sha256'],
               'copied_existing_paths': [r for r in proposal['proposed_paths'] if r['baseline'] is not None],
               'new_paths_required_absent': [r['path'] for r in proposal['proposed_paths'] if r['baseline'] is None],
               'required_unchanged_inputs': proposal['required_unchanged_inputs'],
               'active_paths_changed': [], 'full_source_copy': False}
    (OUT / 'preparation.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'receipt': str(OUT / 'preparation.json'), **identity(OUT / 'preparation.json'),
                      'existing_copies': len(receipt['copied_existing_paths']),
                      'new_paths': len(receipt['new_paths_required_absent'])}, indent=2))


if __name__ == '__main__':
    main()
