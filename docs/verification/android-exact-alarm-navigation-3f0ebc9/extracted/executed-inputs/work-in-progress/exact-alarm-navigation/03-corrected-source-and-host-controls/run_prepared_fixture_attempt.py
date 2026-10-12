#!/usr/bin/env python3
"""Run the two unchanged historical controls with their exact published ZIP inputs."""
from __future__ import annotations

import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import time

ROOT = Path('/dev/shm/macrodroid-exact-alarm-navigation')
SOURCE = ROOT / 'source-01/repository'
PUBLISHED = Path('/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction')
OUTPUT = ROOT / 'source-01/attempts/05-prepared-historical-fixtures'
FIXTURES = [
    ('docs/verification/editor-journey/run-38198783416-attempt-1/evidence.zip', 3892915,
     'abf947195917bb8f090cee7ae2eff250963c8d0ddd5d5663d7b76103a850c46e'),
    ('docs/verification/editor-journey/run-38202401351-attempt-1/evidence.zip', 6517530,
     'fa2eca5f893ae181b91aa7a7bf5df8320620bbc8da21b87eacffb1de0c3bc7ee'),
]


def inventory(root):
    result = []
    for path in sorted(root.rglob('*')):
        if path.is_dir():
            continue
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or path.is_symlink():
            raise RuntimeError('Nonregular input: ' + str(path))
        data = path.read_bytes()
        result.append({'path': path.relative_to(root).as_posix(), 'bytes': len(data),
                       'sha256': hashlib.sha256(data).hexdigest(),
                       'mode': '100755' if info.st_mode & 0o111 else '100644'})
    return result


def write(name, value):
    with (OUTPUT / name).open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def main():
    OUTPUT.mkdir(exist_ok=False)
    before = inventory(SOURCE)
    reviewed = json.loads((ROOT / 'source-01/attempts/02-global-command-correction/source-before.json').read_text())
    if before != reviewed or len(before) != 98:
        raise RuntimeError('The exact reviewed source must remain unchanged')
    execution = OUTPUT / 'source'
    shutil.copytree(SOURCE, execution)
    write('source-before.json', before)
    fixture_rows = []
    for name, size, digest in FIXTURES:
        original, target = PUBLISHED / name, execution / name
        if original.is_symlink() or not original.is_file():
            raise RuntimeError('Missing published historical fixture')
        raw = original.read_bytes()
        if len(raw) != size or hashlib.sha256(raw).hexdigest() != digest:
            raise RuntimeError('Published historical fixture changed')
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(raw)
        fixture_rows.append({'path': name, 'bytes': size, 'sha256': digest, 'mode': '100644',
                             'source': str(original), 'role': 'exact previously published historical host fixture'})
    write('historical-fixture-inputs.json', fixture_rows)
    executed_before = inventory(execution)
    if len(executed_before) != 100:
        raise RuntimeError('Expected exactly 98 source files and two historical ZIP fixtures')
    write('executed-inputs-before.json', executed_before)
    for row in before:
        if row['path'].endswith('.py'):
            ast.parse((execution / row['path']).read_text(), filename=row['path'])
    scratch = OUTPUT / 'temporary'; scratch.mkdir()
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(scratch)}
    argv = [sys.executable, '-B', '-m', 'unittest', '-v',
            'test_supplied_reference_journey.ReferencePlanTests.test_observed_first_use_tip_is_acknowledged_then_trigger_is_tapped_again',
            'test_supplied_reference_journey.ReferencePlanTests.test_observed_original_and_candidate_dialog_targets']
    started_utc = datetime.now(timezone.utc).isoformat(); started = time.monotonic()
    timed_out = False
    with (OUTPUT / 'stdout.log').open('xb') as stdout, (OUTPUT / 'stderr.log').open('xb') as stderr:
        try:
            child = subprocess.run(argv, cwd=execution / 'tools/parity_journeys', env=env,
                                   stdout=stdout, stderr=stderr, timeout=60)
            code = child.returncode
        except subprocess.TimeoutExpired:
            code = None; timed_out = True
    finished = time.monotonic(); finished_utc = datetime.now(timezone.utc).isoformat()
    after, executed_after = inventory(SOURCE), inventory(execution)
    write('source-after.json', after); write('executed-inputs-after.json', executed_after)
    for row in fixture_rows:
        raw = Path(row['source']).read_bytes()
        if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
            raise RuntimeError('Original historical fixture changed during the test')
    result = {'status': 'PASS' if code == 0 and before == after and executed_before == executed_after else 'FAILED',
              'argv': argv, 'cwd': str(execution / 'tools/parity_journeys'), 'timeout_seconds': 60,
              'started_utc': started_utc, 'finished_utc': finished_utc,
              'started_monotonic': started, 'finished_monotonic': finished, 'seconds': finished - started,
              'returncode': code, 'timed_out': timed_out, 'source_unchanged': before == after,
              'source_files': 98, 'executed_files': 100, 'executed_inputs_unchanged': executed_before == executed_after,
              'published_fixtures_unchanged': True, 'android_executed': False,
              'synthetic_fixtures_only': False, 'full_runtime_1_to_1_established': False,
              'scope': 'Reruns only the two unchanged historical tests previously blocked by absent ZIP inputs; no source or application change.',
              'streams': [row for row in inventory(OUTPUT) if row['path'] in ('stdout.log', 'stderr.log')]}
    write('result.json', result)
    shutil.copy2(Path(__file__), OUTPUT / 'executed-run-prepared-fixture-attempt.py')
    print(json.dumps(result, indent=2))
    print((OUTPUT / 'stderr.log').read_text())
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
