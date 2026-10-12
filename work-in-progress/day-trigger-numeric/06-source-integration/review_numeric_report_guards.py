#!/usr/bin/env python3
"""Bounded report-metadata rejection controls against the unchanged targeted proof."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
EVIDENCE = BASE / 'reports/04-targeted-numeric-attempt-02'
OUT = BASE / 'reports/05-numeric-report-guard-review'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    source = EVIDENCE / 'inputs/project/day_numeric_dex_controls.py'
    positive_path = EVIDENCE / 'positive/result.json'
    sys.path[:0] = [str(EVIDENCE / 'inputs/project'), str(EVIDENCE / 'inputs/production')]
    spec = importlib.util.spec_from_file_location('reviewed_numeric', source)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    positive = json.loads(positive_path.read_text()); module.validate_positive(positive)
    controls = [
        ('wrong-primary-method', 'primaryMethod', 'Lanother/Type;->other()I'),
        ('boolean-primary-credit', 'primaryRecoveredMethods', True),
        ('duplicate-getter-credit-inventory', 'dependencyKeys', positive['dependencyKeys'] + positive['dependencyKeys'][:1]),
        ('boolean-zero-mismatch-count', 'mismatchCount', False),
        ('missing-original-method-coverage', 'originalCoverage.methods', []),
        ('missing-rebuilt-method-coverage', 'rebuiltCoverage.methods', []),
    ]
    rows = []
    for name, key, replacement in controls:
        value = copy.deepcopy(positive); parts = key.split('.'); target = value
        for part in parts[:-1]: target = target[part]
        target[parts[-1]] = replacement
        accepted, error = True, None
        try: module.validate_positive(value)
        except Exception as caught: accepted, error = False, repr(caught)
        rows.append({'name': name, 'changed_field': key, 'replacement': replacement,
                     'original_validator_accepted': accepted, 'error': error,
                     'raw_case_observations_unchanged': value['observations'] == positive['observations']})
    os.link(source, OUT / 'reviewed-day_numeric_dex_controls.py')
    os.link(positive_path, OUT / 'actual-positive-result.json')
    (OUT / 'executed-review.py').write_bytes(Path(__file__).read_bytes())
    result = {'schema': 1, 'scope': 'Metadata and coverage rejection controls; the actual numeric execution remains passed.',
              'reviewed_source_sha256': sha(source), 'actual_positive_report_sha256': sha(positive_path),
              'unmodified_positive_accepted': True, 'controls': rows,
              'concrete_false_acceptances': sum(row['original_validator_accepted'] for row in rows)}
    (OUT / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
