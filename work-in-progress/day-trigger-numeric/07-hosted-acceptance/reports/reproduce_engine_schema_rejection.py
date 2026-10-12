#!/usr/bin/env python3
"""Exercise the draft verifier against a synthetic future-count rebinding of real reports."""
from datetime import datetime, timezone
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path('/dev/shm/day-numeric-hosted-01')
BASE = Path('/workspace/scratch/4130730d15aa')
TOOLS = ROOT / 'source/tools/day_numeric_acceptance'
SOURCE = BASE / 'day-trigger-integration/checkpoints/04-source-acceptance-integration/project'
ACTUAL = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/reports')
sys.path.insert(0, str(TOOLS))
import inputs
import verify


def main():
    output = ROOT / 'reports/report-compatibility-01'
    output.mkdir(exist_ok=False)
    project = output / 'candidate-inputs'
    for name in ('source/java-method-map.json', 'tests/fixtures/original-methods.dex', 'tests/fixtures/provenance.json'):
        path = project / name
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE / name, path)
    shutil.copyfile(TOOLS / 'verify.py', output / 'executed-verifier.py')
    pins = inputs.load_pins()
    names = ['java-all-path-parity.json', 'hybrid-roundtrip.json', 'baseline-roundtrip.json',
             'java-three-path-parity.json', 'java-core-three-path-parity.json', 'java-environment-three-path-parity.json',
             'java-engine-three-path-parity.json', 'java-ui-three-path-parity.json']
    actual = {name: inputs.read_json(ACTUAL / name) for name in names}
    values = copy.deepcopy(actual)
    all_path = values['java-all-path-parity.json']
    all_path.update(cases=194780, methodsCovered=1243, methodsExpected=1243,
                    suiteCases=pins['suite_cases'], fixtureSha256=pins['fixture']['sha256'])
    method = next(row for row in inputs.read_json(project / 'source/java-method-map.json') if row.get('helper_method') == 'numericValue')
    key = method['target'] + '->' + method['method']
    values['hybrid-roundtrip.json']['changed_methods'].append([method['target'], method['method']])
    values['java-ui-three-path-parity.json']['methodKeys'].append(key)
    values['java-ui-three-path-parity.json'].update(cases=24465, methodsCovered=11)
    for name in names:
        if name.endswith('three-path-parity.json'):
            values[name]['fixture_sha256'] = pins['fixture']['sha256']
        inputs.write_json(output / 'synthetic-rebound-reports' / name, values[name])
    class MemoryReports:
        def json(self, name):
            return values[name.removeprefix('reports/')]
    result = {'schema': 1, 'status': 'DRAFT_SCHEMA_CHECK_PENDING',
              'scope': 'Synthetic future-count/input-hash rebinding of preserved actual report formats; no new application execution',
              'actual_report_inputs': [{'path': str(ACTUAL / name), **inputs.identity(ACTUAL / name)} for name in names],
              'executed_verifier': inputs.identity(output / 'executed-verifier.py'),
              'actual_engine_scope': actual['java-engine-three-path-parity.json']['scope'],
              'actual_engine_selection': actual['java-engine-three-path-parity.json']['selection'],
              'actual_engine_androidRuntime_field_present': 'androidRuntime' in actual['java-engine-three-path-parity.json'],
              'synthetic_transform': 'Only future counts/method selection/fixture hash are rebound; engine format and all execution claims stay unchanged'}
    try:
        verify.verify_registry_and_partition(project, pins, all_path['apkSha256'], values, MemoryReports())
    except ValueError as error:
        result.update(status='DRAFT_REJECTED_VALID_PRESERVED_ENGINE_SCHEMA', exception=repr(error))
    else:
        result.update(status='DRAFT_ACCEPTED_SCHEMA')
    inputs.write_json(output / 'result.json', result)
    print(json.dumps({key: value for key, value in result.items() if key not in ('actual_report_inputs',)}, indent=2))


if __name__ == '__main__':
    main()
