#!/usr/bin/env python3
"""Retain each exact inactive source snapshot and its literal host-test attempt."""
from __future__ import annotations
import argparse
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

def inventory(root):
    result = []
    for path in sorted(root.rglob('*')):
        if path.is_dir(): continue
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or path.is_symlink():
            raise RuntimeError('Nonregular input: ' + str(path))
        data = path.read_bytes()
        result.append({'path': path.relative_to(root).as_posix(), 'bytes': len(data),
                       'sha256': hashlib.sha256(data).hexdigest(),
                       'mode': '100755' if info.st_mode & 0o111 else '100644'})
    return result

def write(path, value):
    with path.open('x') as out: out.write(json.dumps(value, indent=2) + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('attempt')
    parser.add_argument('modules', nargs='+')
    args = parser.parse_args()
    if '/' in args.attempt or not args.attempt.startswith('0'):
        raise RuntimeError('Attempt name must be a new simple numbered label')
    target = ROOT / 'source-01/attempts' / args.attempt
    target.mkdir(parents=True, exist_ok=False)
    before = inventory(SOURCE)
    shutil.copytree(SOURCE, target / 'source')
    write(target / 'source-before.json', before)
    for row in before:
        if row['path'].endswith('.py'):
            ast.parse((SOURCE / row['path']).read_text(), filename=row['path'])
    write(target / 'syntax.json', {'status': 'ALL_PYTHON_INPUTS_PARSE',
                                  'files': [row['path'] for row in before if row['path'].endswith('.py')]})
    scratch = target / 'synthetic-temporary'; scratch.mkdir()
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch))
    argv = [sys.executable, '-B', '-m', 'unittest', '-v', *args.modules]
    start_utc = datetime.now(timezone.utc).isoformat(); start = time.monotonic()
    timed_out = False
    with (target / 'stdout.log').open('xb') as out, (target / 'stderr.log').open('xb') as err:
        try:
            result = subprocess.run(argv, cwd=SOURCE / 'tools/parity_journeys', env=env,
                                    stdout=out, stderr=err, timeout=600)
            code = result.returncode
        except subprocess.TimeoutExpired:
            code = None; timed_out = True
    finish = time.monotonic(); finish_utc = datetime.now(timezone.utc).isoformat()
    after = inventory(SOURCE)
    write(target / 'source-after.json', after)
    result = {'status': 'PASS' if code == 0 and after == before else 'FAILED',
              'argv': argv, 'cwd': str(SOURCE / 'tools/parity_journeys'), 'timeout_seconds': 600,
              'started_utc': start_utc, 'finished_utc': finish_utc,
              'started_monotonic': start, 'finished_monotonic': finish, 'seconds': finish - start,
              'returncode': code, 'timed_out': timed_out, 'source_unchanged': after == before,
              'source_files': len(before), 'android_executed': False,
              'synthetic_fixtures_only': True, 'full_runtime_1_to_1_established': False,
              'streams': [row for row in inventory(target) if row['path'] in ('stdout.log', 'stderr.log')]}
    write(target / 'result.json', result)
    shutil.copy2(Path(__file__), target / 'executed-run-host-attempt.py')
    print(json.dumps(result, indent=2))
    print((target / 'stderr.log').read_text()[-18000:])
    return 0 if result['status'] == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
