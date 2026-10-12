"""Bind the final Editor requirement to untouched foreground/XML artifact bytes."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
REPO_PATH = 'docs/verification/editor-journey/run-38206460588-attempt-1/evidence.zip'
ARCHIVE = BASE / 'MacroDroid-Reconstruction' / REPO_PATH
OUT = ROOT / 'component-pair-reports/03-observed-final-component'


def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    archive_meta = meta(ARCHIVE.read_bytes())
    assert archive_meta == {'bytes': 11576977, 'sha256': 'd22377dacd276c2c8ab2d52bfa639a912d1871c90757ebefc71af16d106cdff6'}
    OUT.mkdir(parents=True, exist_ok=False)
    rows = []
    with zipfile.ZipFile(ARCHIVE) as archive:
        member = 'ci-editor/journey/journey.json'
        raw = archive.read(member)
        assert meta(raw) == {'bytes': 647860, 'sha256': '023461ca583b6586f317ab64cec34f8e25ad04af3a30a3fb05b429b20957c9e0'}
        journey_meta = meta(raw)
        report = json.loads(raw)
        for run in report['runs']:
            shot = run['screens'][-1]
            assert shot['name'] == 'editor-after-constraint-back'
            records = [('captured_foreground', shot['artifacts']['foreground']),
                       ('endpoint_foreground', shot['session_identity']['foreground']['stdout']),
                       ('captured_hierarchy', shot['artifacts']['hierarchy'])]
            observations = []
            for role, record in records:
                member = 'ci-editor/journey/' + record['path']
                data = archive.read(member)
                assert meta(data) == {key: record[key] for key in ('bytes', 'sha256')}
                output = run['label'] + '-' + role + ('.xml' if role.endswith('hierarchy') else '.txt')
                (OUT / output).write_bytes(data)
                observed = {'role': role, 'archive_member': member, 'copy': output, **meta(data)}
                if role.endswith('foreground'):
                    lines = [line for line in data.decode().splitlines() if 'topResumedActivity=' in line]
                    assert len(lines) == 1 and 'com.arlosoft.macrodroid/.editscreen.EditMacroActivity' in lines[0]
                    observed['exact_resumed_line'] = lines[0]
                    observed['normalized_component'] = 'com.arlosoft.macrodroid/com.arlosoft.macrodroid.editscreen.EditMacroActivity'
                else:
                    nodes = [node.attrib for node in ET.fromstring(data).iter('node')
                             if node.get('resource-id') == 'com.arlosoft.macrodroid:id/edit_macro_addTriggerButton']
                    assert len(nodes) == 1 and nodes[0]['enabled'] == 'true' and nodes[0]['clickable'] == 'true'
                    observed['observed_plan_selector'] = nodes[0]
                observations.append(observed)
            rows.append({'label': run['label'], 'apk_sha256': run['apk_sha256'], 'capture': shot['name'],
                         'owner': shot['owner'], 'observations': observations})
    result = {'schema': 1, 'status': 'EXACT_HISTORICAL_FINAL_EDITOR_COMPONENT_BOUND',
              'run_id': 38206460588, 'head_commit': '934c6543dce0897975f52457717b3a70bd27ce00',
              'archive_repository_path': REPO_PATH, 'archive': archive_meta,
              'journey_member': 'ci-editor/journey/journey.json', 'journey': journey_meta,
              'observed_final_class': 'com.arlosoft.macrodroid.editscreen.EditMacroActivity',
              'variants': rows, 'new_android_execution_performed': False,
              'historical_results_modified': False, 'whole_activity_lifecycle_parity_established': False}
    (OUT / 'provenance.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'raw_copies': 6, 'variants': [row['label'] for row in rows]}))


if __name__ == '__main__':
    main()
