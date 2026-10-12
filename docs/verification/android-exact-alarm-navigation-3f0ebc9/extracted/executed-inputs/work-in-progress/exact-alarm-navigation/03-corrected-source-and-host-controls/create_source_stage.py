#!/usr/bin/env python3
"""Copy the exact closed replay source and derive the observed dialog contract."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import stat
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = Path('/dev/shm/macrodroid-exact-alarm-navigation')
PARENT = Path('/dev/shm/macrodroid-notification-readiness/checkpoints/01-corrected-host-guard')
DESIGN = ROOT / 'checkpoints/01-observed-input-and-design'
STAGE = ROOT / 'source-01'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def record(path, relative):
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode) and not path.is_symlink(), relative
    return {'path': relative, 'bytes': info.st_size, 'sha256': digest(path),
            'mode': '100755' if info.st_mode & 0o111 else '100644'}

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as out:
        out.write(json.dumps(value, indent=2) + '\n')

def main():
    assert digest(PARENT / 'checkpoint.json') == 'b9d069a653b3ecc483f8e6579ccfb13e5a70450c00015f9a3a31c5277c9a84b3'
    assert digest(DESIGN / 'checkpoint.json') == '9c0979511fb17f09a57bf1a08b33d581797e050f6f13b2437028b1b1fae946dc'
    parent = json.loads((PARENT / 'checkpoint.json').read_bytes())
    design = json.loads((DESIGN / 'checkpoint.json').read_bytes())
    sources = [r for r in parent['files'] if r['path'].startswith('replay-source/')]
    assert len(sources) == 81 and sum(r['bytes'] for r in sources) == 1445624
    for row in sources:
        source = PARENT / row['path']
        assert source.stat().st_size == row['bytes'] and digest(source) == row['sha256'], row['path']
    for row in design['files']:
        source = DESIGN / row['path']
        assert source.stat().st_size == row['bytes'] and digest(source) == row['sha256'], row['path']
    STAGE.mkdir(exist_ok=False)
    repository = STAGE / 'repository'
    before = []
    for row in sources:
        relative = row['path'].removeprefix('replay-source/')
        source, target = PARENT / row['path'], repository / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        target.chmod(0o755 if source.stat().st_mode & 0o111 else 0o644)
        before.append(record(target, relative))
    fixture = repository / 'tools/parity_journeys/fixtures/exact-alarm'
    fixture.mkdir(exist_ok=False)
    observed = []
    for source in sorted((DESIGN / 'observed').iterdir()):
        target = fixture / source.name
        shutil.copy2(source, target)
        target.chmod(0o644)
        observed.append(record(target, target.relative_to(repository).as_posix()))
    assert len(observed) == 12
    contracts = json.loads((DESIGN / 'observed-dialog-contract.json').read_bytes())
    keys = ['positive', 'positive_ancestor_chain', 'title', 'message', 'cancel',
            'canonical_panel_sha256', 'observed_center']
    core = {key: contracts[0][key] for key in keys}
    assert core == {key: contracts[1][key] for key in keys}
    roots = [ET.fromstring((DESIGN / 'observed' / item['shot']['artifacts']['hierarchy']['path']).read_bytes())
             for item in contracts]
    assert roots[0].attrib == roots[1].attrib == {'rotation': '0'}
    core.update(schema=1, hierarchy_attributes=roots[0].attrib, image_size=[720, 1280],
                component='com.arlosoft.macrodroid/com.arlosoft.macrodroid.selectableitemlist.AddTriggerActivity',
                source_run=38230072388,
                source_design_sha256=digest(DESIGN / 'checkpoint.json'),
                observations=[{'label': item['label'], 'artifacts': item['shot']['artifacts']}
                              for item in contracts])
    write_json(fixture / 'dialog-contract.json', core)
    write_json(STAGE / 'source-before.json', {
        'status': 'EXACT_CLOSED_PARENT_COPIED', 'created_utc': datetime.now(timezone.utc).isoformat(),
        'parent_checkpoint_sha256': digest(PARENT / 'checkpoint.json'),
        'design_checkpoint_sha256': digest(DESIGN / 'checkpoint.json'),
        'files': before, 'new_observed_fixture_files': observed,
        'derived_contract': record(fixture / 'dialog-contract.json',
                                   (fixture / 'dialog-contract.json').relative_to(repository).as_posix()),
        'android_executed': False, 'active_changes': False})
    print(json.dumps({'source_files': len(before), 'raw_fixture_files': len(observed),
                      'contract_sha256': digest(fixture / 'dialog-contract.json'),
                      'stage': str(STAGE)}))

if __name__ == '__main__':
    main()
