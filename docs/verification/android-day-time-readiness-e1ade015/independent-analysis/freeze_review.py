#!/usr/bin/env python3
"""Freeze the independent result and selected unchanged raw excerpts only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parent
raw = Path('/dev/shm/macrodroid-transfer-space-20261012/readiness-run-38230072388/extracted')
target = root / 'checkpoints/01-independent-device-analysis'
assert not target.exists()
def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'mode': path.stat().st_mode & 0o777}
result = json.loads((root / 'reports/01-actual-readiness-analysis/result.json').read_text())
assert result['status'] == 'INDEPENDENT_ACTUAL_READINESS_DIFFERENCE_CONFIRMED'
assert json.loads((root / 'execute-01.json').read_text())['returncode'] == 0
assert (root / 'execute-01.stderr.log').read_bytes() == b''
journey = json.loads((raw / 'journey/journey.json').read_text())
selected = ['journey/comparison.json', 'day-time-readiness-verification.json',
            'journey/original-notification-readiness.json', 'journey/candidate-notification-readiness.json']
for run in journey['runs']:
    for index in (1, 12):
        for kind in ('screenshot', 'hierarchy'):
            selected.append('journey/' + run['screens'][index]['artifacts'][kind]['path'])
excerpts = root / 'raw-excerpts'; excerpts.mkdir(exist_ok=False)
bindings = []
for name in selected:
    source = raw / name; destination = excerpts / Path(name).name
    assert not destination.exists(); shutil.copy2(source, destination)
    assert identity(source) == identity(destination)
    bindings.append({'original_artifact_path': name, 'copy': destination.relative_to(root).as_posix(), **identity(source)})
pixel = json.loads((root / 'reports/01-actual-readiness-analysis/paired-full-frames.json').read_text())[1]
screen = journey['runs'][0]['screens'][1]
xml_path = raw / 'journey' / screen['artifacts']['hierarchy']['path']
nodes = [node for node in ET.fromstring(xml_path.read_bytes()).iter() if node.attrib.get('resource-id') == 'com.arlosoft.macrodroid:id/indicator']
assert len(nodes) == 1 and nodes[0].attrib['bounds'] == '[128,1184][592,1200]'
assert pixel['inclusive_changed_bbox'] == [313, 1184, 351, 1199]
assert all(128 <= row['x'] < 592 and 1184 <= row['y'] < 1200 for row in pixel['changed_coordinates_and_rgba'])
localization = {'scope': 'Spatial localization only; no cause assigned.', 'changed_pixels': 26,
                'inclusive_changed_bbox': pixel['inclusive_changed_bbox'], 'actual_xml_node': dict(nodes[0].attrib),
                'all_changed_pixels_inside_node': True, 'xml_identity': identity(xml_path)}
(root / 'reports/01-actual-readiness-analysis/indicator-localization.json').write_text(json.dumps(localization, indent=2) + '\n')
(root / 'raw-excerpt-bindings.json').write_text(json.dumps(bindings, indent=2) + '\n')
paths = sorted(p for p in root.rglob('*') if p.is_file() and 'checkpoints' not in p.relative_to(root).parts)
assert sum(p.stat().st_size for p in paths) < 5 * 1024 * 1024
target.mkdir(parents=True)
files = []
for source in paths:
    name = source.relative_to(root).as_posix(); destination = target / name
    destination.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(source, destination)
    assert identity(source) == identity(destination)
    files.append({'path': name, **identity(destination)})
cp = {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
      'status': 'FROZEN_INDEPENDENT_ACTUAL_READINESS_DIFFERENCE_REVIEW',
      'repo_target': 'docs/verification/android-day-time-readiness-e1ade015/independent-analysis',
      'run_id': 38230072388, 'artifact_id': 11739145683, 'head_sha': 'e1ade015f938339479216a1a91518e556902fce8',
      'raw_zip_sha256': 'c8f0af87e5d91efe2dfc49b8ca76acc1a0943b2a2b8e17ffe279892726d2c80f',
      'raw_extraction_receipt_sha256': '61c47bb315336958869a5cf3b945c7cbdb649de65786495f04b105ce5fa33419',
      'raw_literal_comparison': 'JOURNEY_DIFFERENCE', 'full_runtime_1_to_1_established': False,
      'independent_review_checks_passed': True, 'new_android_execution': False, 'raw_changed': False,
      'files': files}
data = (json.dumps(cp, indent=2, sort_keys=True) + '\n').encode(); (target / 'checkpoint.json').write_bytes(data)
print(json.dumps({'checkpoint': str(target / 'checkpoint.json'), **identity(target / 'checkpoint.json'),
                  'files': len(files), 'payload_bytes': sum(row['bytes'] for row in files)}, indent=2))
