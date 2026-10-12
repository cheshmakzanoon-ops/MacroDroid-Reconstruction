#!/usr/bin/env python3
"""Replay exact retained failures using the inactive readiness-capable guard."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parent
INPUTS = [
    ('zero12', '38216299675', 42199893, '1ea3ad6302d53c2fcc8341c03deec7ccd04d729facaf5658acb87e4aebc6f4b3'),
    ('daytime13', '38221713675', 38451864, 'ad31af7b9fb237dbca1285a671a3e12fdcd9c3cd3754f55064055066043dffa4'),
]


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def inventory(path):
    return {item.relative_to(path).as_posix(): identity(item)
            for item in sorted(path.rglob('*')) if item.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repository, output = args.repository.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    sys.path[:0] = [str(repository / 'tools/parity_journeys'), str(repository / 'project')]
    import android_compare as proof
    import editor_journey as runner
    import day_time_journey as day
    import trigger_category_journey as category
    import notification_readiness
    source_before = inventory(repository)
    (output / 'source-before.json').write_text(json.dumps(source_before, indent=2) + '\n')
    result = {'status': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(),
              'android_executed_by_this_replay': False, 'historical_results_modified': False,
              'active_changes': False, 'operation': identity(Path(__file__)), 'runs': []}
    for label, run_id, size, digest in INPUTS:
        started = time.monotonic()
        raw = ROOT.parent / f'ci-run-analysis/{label}-run-{run_id}-extracted'
        archive = ROOT.parent / f'ci-run-analysis/{label}-run-{run_id}.zip'
        expected_zip = {'bytes': size, 'sha256': digest}
        if identity(archive) != expected_zip:
            raise RuntimeError('Historical ZIP identity changed: ' + run_id)
        before = inventory(raw)
        (output / (label + '-raw-before.json')).write_text(json.dumps(before, indent=2) + '\n')
        folder = raw / 'journey'
        report = json.loads((folder / 'journey.json').read_text())
        expected = json.loads((folder / 'comparison.json').read_text())
        context = category.configured_plan if label == 'zero12' else day.configured_plan
        with context():
            actual = runner.compare(folder, report, proof)
        (output / (label + '-replayed-comparison.json')).write_text(json.dumps(actual, indent=2) + '\n')
        if actual != expected:
            raise RuntimeError('Historical full verdict changed: ' + run_id)
        if label == 'zero12':
            if (actual['journey_equal'] is not False or actual['status'] != 'JOURNEY_DIFFERENCE'
                    or [row['changed_pixels'] for row in actual['screens']] != [0, 5] + [0] * 10):
                raise RuntimeError('Historical complete five-pixel rejection differs')
        elif (actual['status'] != 'REJECTED' or actual['screens'] != []
              or actual.get('reason') != 'Incomplete run or changed environment'):
            raise RuntimeError('Historical incomplete process rejection differs')
        after = inventory(raw)
        (output / (label + '-raw-after.json')).write_text(json.dumps(after, indent=2) + '\n')
        if before != after or identity(archive) != expected_zip:
            raise RuntimeError('Historical evidence changed during read-only replay')
        result['runs'].append({'label': label, 'run_id': int(run_id), 'archive': expected_zip,
                               'raw_files': len(before), 'raw_bytes': sum(row['bytes'] for row in before.values()),
                               'raw_inputs_unchanged': True, 'full_comparison_object_unchanged': True,
                               'seconds': time.monotonic() - started, 'verdict': actual})
        (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    after = inventory(repository)
    (output / 'source-after.json').write_text(json.dumps(after, indent=2) + '\n')
    if source_before != after:
        raise RuntimeError('Inactive source changed during historical replay')
    result.update(status='BOTH_LITERAL_HISTORICAL_FAILURES_PRESERVED', source_unchanged=True,
                  finished_utc=datetime.now(timezone.utc).isoformat())
    (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'runs': [
        {key: row[key] for key in ('label', 'run_id', 'raw_files', 'full_comparison_object_unchanged', 'seconds')}
        for row in result['runs']]}, indent=2))


if __name__ == '__main__':
    main()
