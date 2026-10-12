"""Demonstrate omitted executed-input rows against unchanged workflow-02.

Only private hard-link fixtures are created. A mutated fixture is unlinked before
replacement, so no original source, APK, tool or evidence file is modified.
"""
from __future__ import annotations
from datetime import datetime, timezone
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

BASE = Path('/workspace/scratch/4130730d15aa')
ROOT = Path(__file__).resolve().parent
WORKFLOW = BASE / 'animation-diagnostic/workflow-02'
INPUT = WORKFLOW / 'reports/validation-01/private-inputs'
INPUT_OUTPUT = INPUT / 'ci-normal-animation'
REVIEWED = 'tools/android/bootstrap_android_runtime.py'


def meta(path):
    with path.open('rb') as stream:
        return {'bytes': path.stat().st_size, 'sha256': hashlib.file_digest(stream, 'sha256').hexdigest()}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def main():
    out = ROOT / 'reports/01-materialized-preflight-omission'
    out.mkdir(parents=True, exist_ok=False)
    source_pins = {name: meta(WORKFLOW / name) for name in
                   ('prepare_normal_journey.py', 'verify_normal_journey.py', '.github/workflows/editor-normal-animation.yml')}
    assert source_pins['prepare_normal_journey.py']['sha256'] == '0f0c022f556f9798afd886e1943f6e2fc63e35dc0498abe1e6db2b53fce72129'
    assert source_pins['verify_normal_journey.py']['sha256'] == '47137b6f86a95e42ae55aa1d5362e471139436b714c88a07e047bfc17b04b03c'
    baseline = json.loads((INPUT_OUTPUT / 'input-preflight.json').read_bytes())
    assert baseline['passed'] is True
    target_rows = [r for r in baseline['files'] if r['path'] == REVIEWED]
    assert len(target_rows) == 1
    target_row = target_rows[0]
    all_sources = {}
    for row in baseline['files']:
        for source in (INPUT / row['path'], INPUT_OUTPUT / row['copy']):
            assert meta(source) == {key: row[key] for key in ('bytes', 'sha256')}
            all_sources[str(source)] = meta(source)
    binaries = ['workspace/MacroDroid_v9/tools/prebuilt/linux/aapt2',
                'workspace/artifacts/MacroDroid-5.67.8-original.apk',
                'workspace/artifacts/MacroDroid-5.67.8-current-hybrid.apk']
    for name in binaries:
        all_sources[str(INPUT / name)] = meta(INPUT / name)
    save(out / 'baseline-source-pins.json', source_pins)
    save(out / 'retained-inputs-before.json', all_sources)
    save(out / 'baseline-preflight.json', baseline)
    rows = []
    for label, mutation in (('positive', None), ('changed-source-retained-row', 'keep'),
                            ('changed-source-omitted-row', 'omit'), ('changed-source-empty-inventory', 'empty')):
        case = out / 'cases' / label
        private = ROOT / 'private-cases' / label
        root, output = private / 'root', private / 'root/ci-normal-animation'
        output.mkdir(parents=True, exist_ok=False)
        links = {}
        for row in baseline['files']:
            for source, target in ((INPUT / row['path'], root / row['path']),
                                   (INPUT_OUTPUT / row['copy'], output / row['copy'])):
                if target.exists():
                    assert meta(target) == meta(source)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                os.link(source, target)
                links[target.relative_to(root).as_posix()] = {'source': str(source), **meta(source)}
        for name in binaries:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(INPUT / name, target)
            links[name] = {'source': str(INPUT / name), **meta(INPUT / name)}
        preflight = copy.deepcopy(baseline)
        modified = []
        if mutation is not None:
            marker = b'\n# DELIBERATE PRIVATE SOURCE-HASH DEFECT; NO ANDROID EXECUTION\n'
            for path in (root / REVIEWED, output / target_row['copy']):
                raw = path.read_bytes()
                path.unlink()
                path.write_bytes(raw + marker)
                modified.append({'path': path.relative_to(root).as_posix(), **meta(path)})
            if mutation == 'omit':
                preflight['files'] = [row for row in preflight['files'] if row['path'] != REVIEWED]
            elif mutation == 'empty':
                preflight['files'] = []
        save(output / 'input-preflight.json', preflight)
        case.mkdir(parents=True)
        save(case / 'before-preflight.json', baseline)
        save(case / 'after-preflight.json', preflight)
        save(case / 'private-fixture-links.json', links)
        if modified:
            (case / 'modified-bootstrap_android_runtime.py').write_bytes((root / REVIEWED).read_bytes())
        argv = [sys.executable, '-B', str(WORKFLOW / 'prepare_normal_journey.py'),
                '--root', str(root), '--output', str(output), '--materialized']
        started = time.monotonic()
        completed = subprocess.run(argv, capture_output=True, timeout=120,
                                   env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        (case / 'stdout.log').write_bytes(completed.stdout)
        (case / 'stderr.log').write_bytes(completed.stderr)
        materialized = json.loads((output / 'materialized-inputs.json').read_bytes())
        save(case / 'materialized-inputs.json', materialized)
        expected_pass = mutation != 'keep'
        assert (completed.returncode == 0) is expected_pass, (label, completed.stderr.decode())
        assert materialized['passed'] is expected_pass
        if mutation == 'keep':
            assert 'Prepared input changed before execution: ' + REVIEWED in materialized['reason']
        row = {'case': label, 'started_utc': datetime.now(timezone.utc).isoformat(), 'argv': argv,
               'exit_code': completed.returncode, 'seconds': time.monotonic() - started,
               'input_inventory_entries': len(preflight['files']), 'baseline_inventory_entries': len(baseline['files']),
               'deliberately_modified_private_files': modified, 'materialized_status': materialized['status'],
               'materialized_passed': materialized['passed'], 'false_acceptance': mutation in ('omit', 'empty'),
               'android_executed': False}
        save(case / 'result.json', row)
        rows.append(row)
        print(json.dumps(row, sort_keys=True), flush=True)
    for source, expected in all_sources.items():
        assert meta(Path(source)) == expected, source
    for name, expected in source_pins.items():
        assert meta(WORKFLOW / name) == expected
    save(out / 'retained-inputs-after.json', all_sources)
    result = {'schema': 1, 'status': 'MUTABLE_PREFLIGHT_ROW_OMISSION_FALSE_ACCEPTANCE_REPRODUCED',
              'source_pins': source_pins, 'cases': rows, 'protected_source_tool_apk_and_evidence_hashes_unchanged': True,
              'retained_unique_input_files': len(all_sources), 'android_executed': False,
              'workflow02_sources_modified': False, 'active_repository_modified': False,
              'final_verifier_gap': 'The same unchecked iteration of preflight[files] appears in verify_normal_journey.verify; this proof executes the materialized gate only and does not claim a full final-verifier false pass.'}
    save(out / 'review-result.json', result)


if __name__ == '__main__':
    main()
