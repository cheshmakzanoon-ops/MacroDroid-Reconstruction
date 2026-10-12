#!/usr/bin/env python3
"""Prepare the approved small lookup overlay from exact frozen numeric inputs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
NUMERIC = Path('/workspace/scratch/4130730d15aa/day-trigger-integration/checkpoints/04-source-acceptance-integration')
PLAN = Path('/dev/shm/macrodroid-day-lookup-integration-plan/checkpoints/01-integration-plan')
ACTIVE = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')

def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'mode': path.stat().st_mode & 0o777}

def main():
    stage = ROOT / 'stage-02'
    assert not stage.exists()
    assert identity(NUMERIC / 'checkpoint.json')['sha256'] == 'c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f'
    assert identity(PLAN / 'checkpoint.json')['sha256'] == '462bc9df44e1e5e99382f2dcae7c49c8c097f3c09ebc77b299bfc57378567daa'
    proposed = json.loads((PLAN / 'evidence/prospective-source-paths.json').read_text())
    baseline = json.loads((NUMERIC / 'checkpoint.json').read_text())
    assert len(proposed) == 21 and sum(row['proposal'] == 'new' for row in proposed) == 6
    for row in proposed:
        if row['baseline'] is None:
            assert not (NUMERIC / 'project' / row['path']).exists()
            assert not (ACTIVE / row['path']).exists()
        else:
            assert identity(Path(row['baseline_source'])) == row['baseline']
    rows = []
    for row in baseline['source_changes']:
        source = NUMERIC / row['source']
        before = identity(source)
        assert {key: before[key] for key in ('bytes', 'sha256')} == row['candidate']
        for folder in ('project', 'baseline'):
            target = stage / folder / row['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            assert identity(target) == before
        rows.append({'path': row['path'], 'source': str(source), 'baseline': before})
    assert len(rows) == 19
    result = {'schema': 1, 'status': 'EXACT_NINETEEN_PATH_BASELINE_COPIED', 'created_utc': datetime.now(timezone.utc).isoformat(),
              'numeric_checkpoint_sha256': identity(NUMERIC / 'checkpoint.json')['sha256'],
              'approved_plan_checkpoint_sha256': identity(PLAN / 'checkpoint.json')['sha256'],
              'allowed_modified_or_new_paths': proposed, 'copied_baseline_paths': rows,
              'new_paths_required_absent': [row['path'] for row in proposed if row['baseline'] is None],
              'maximum_initial_owned_bytes': 256 * 1024 * 1024, 'full_project_or_apk_copied': False,
              'active_source_changed': False}
    (stage / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
    assert sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file()) < 256 * 1024 * 1024
    print(json.dumps({'status': result['status'], 'stage': str(stage), 'copied_paths': 19,
                      'approved_future_source_paths': 21, 'bytes': sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())}, indent=2))

if __name__ == '__main__':
    main()
