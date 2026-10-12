#!/usr/bin/env python3
"""Replay the closed real thirteen-screen report under the new shared source."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time

ROOT = Path('/dev/shm/macrodroid-exact-alarm-navigation')
SOURCE = ROOT / 'source-01/repository'
RAW = Path('/dev/shm/macrodroid-transfer-space-20261012/readiness-run-38230072388/extracted')
PARENT = Path('/dev/shm/macrodroid-notification-readiness/checkpoints/01-corrected-host-guard/replay-source')
OUTPUT = ROOT / 'source-01/completed-schema5-replay-corrected'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inventory(folder):
    rows = []
    for path in sorted(folder.rglob('*')):
        if path.is_dir(): continue
        if path.is_symlink() or not path.is_file(): raise RuntimeError('Nonregular evidence')
        data = path.read_bytes()
        rows.append({'path': path.relative_to(folder).as_posix(), 'bytes': len(data), 'sha256': sha(data)})
    return rows

def write(name, value):
    with (OUTPUT / name).open('x') as out: out.write(json.dumps(value, indent=2) + '\n')

def main():
    OUTPUT.mkdir(exist_ok=False)
    before = inventory(RAW)
    assert len(before) == 3258 and sum(row['bytes'] for row in before) == 70899613
    write('raw-before.json', before)
    inputs = inventory(SOURCE); write('source-before.json', inputs)
    parent_module = PARENT / 'tools/parity_journeys/notification_readiness.py'
    old = parent_module.read_bytes()
    assert sha(old) == '08a838681c6b3ece018240d54013996bafd4204133bdd3eaa6a6c2dddeea6f85'
    assert old == (SOURCE / 'tools/parity_journeys/notification_readiness.py').read_bytes()
    new = (SOURCE / 'tools/parity_journeys/exact_alarm_readiness.py').read_bytes()
    def functions(data):
        return {node.name: ast.dump(node, include_attributes=False) for node in ast.parse(data).body
                if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    left, right = functions(old), functions(new)
    assert set(left) == set(right)
    changed = [name for name in left if left[name] != right[name]]
    assert changed == ['require_plan', 'require_policy']
    write('readiness-algorithm-identity.json', {'parent_source_sha256': sha(old), 'successor_source_sha256': sha(new),
        'top_level_functions': len(left), 'changed_binding_functions': changed,
        'unchanged_algorithm_functions': [{'name': name, 'ast_sha256': sha(value.encode())}
                                        for name, value in left.items() if name not in changed]})
    sys.path[:0] = [str(SOURCE / 'tools/parity_journeys'), str(SOURCE / 'project')]
    import android_compare as proof
    import day_time_journey as day
    import editor_journey as runner
    journey = RAW / 'journey'
    report_data = (journey / 'journey.json').read_bytes()
    prior_data = (journey / 'comparison.json').read_bytes()
    report, prior = json.loads(report_data), json.loads(prior_data)
    start_utc = datetime.now(timezone.utc).isoformat(); start = time.monotonic()
    with day.configured_plan():
        current = runner.compare(journey, report, proof)
    finish = time.monotonic(); finish_utc = datetime.now(timezone.utc).isoformat()
    write('replayed-comparison.json', current)
    after = inventory(RAW); write('raw-after.json', after)
    final_inputs = inventory(SOURCE); write('source-after.json', final_inputs)
    expected = [0, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    result = {'status': 'EXACT_HISTORICAL_RESULT_UNCHANGED' if current == prior and after == before and final_inputs == inputs else 'FAILED',
              'run_id': 38230072388, 'head_sha': 'e1ade015f938339479216a1a91518e556902fce8',
              'report_sha256': sha(report_data), 'prior_comparison_sha256': sha(prior_data),
              'complete_comparison_object_equal': current == prior,
              'raw_files_unchanged': after == before, 'source_files_unchanged': final_inputs == inputs,
              'raw_files': len(before), 'source_files': len(inputs),
              'started_utc': start_utc, 'finished_utc': finish_utc,
              'started_monotonic': start, 'finished_monotonic': finish, 'seconds': finish - start,
              'pixel_differences': [row['changed_pixels'] for row in current.get('screens', [])],
              'all_hierarchies_equal': all(row['hierarchy_equal'] for row in current.get('screens', [])),
              'recorded_journey_equal': current['journey_equal'], 'new_android_execution': False,
              'full_runtime_1_to_1_established': False}
    assert result['pixel_differences'] == expected and result['recorded_journey_equal'] is False
    write('result.json', result)
    shutil.copy2(Path(__file__), OUTPUT / 'executed-replay-completed-readiness.py')
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'EXACT_HISTORICAL_RESULT_UNCHANGED' else 1

if __name__ == '__main__':
    raise SystemExit(main())
