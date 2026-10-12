#!/usr/bin/env python3
"""Run one explicitly selected bounded authoring/host-review command with immutable logs."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import time

OWN = Path('/dev/shm/macrodroid-day-numeric-art-schema-02')


def identity(path):
    st = path.lstat()
    assert stat.S_ISREG(st.st_mode)
    return {'bytes': st.st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'mode': stat.S_IMODE(st.st_mode)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--timeout', type=int, required=True)
    parser.add_argument('--source', type=Path)
    parser.add_argument('argv', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    assert args.name in ('author-01', 'focused-01')
    assert args.timeout == 120
    assert args.argv and args.argv[0] == '--'
    argv = args.argv[1:]
    folder = OWN / 'reports' / args.name
    folder.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(__file__, folder / 'executed-recorder.py')
    temporary = folder / 'temporary'
    temporary.mkdir()
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(temporary)}
    if args.source:
        assert args.source.resolve() == (OWN / 'source').resolve()
        env['PYTHONPATH'] = str(args.source.resolve())
        env['NUMERIC_PROBE_CONTROL_EVIDENCE'] = str(folder / 'host-evidence')
    record = {'argv': argv, 'cwd': str(OWN), 'timeout_seconds': args.timeout,
              'environment_overrides': {name: env[name] for name in (
                  'PYTHONDONTWRITEBYTECODE', 'TMPDIR', 'PYTHONPATH', 'NUMERIC_PROBE_CONTROL_EVIDENCE')
                  if name in env and (name not in ('PYTHONPATH', 'NUMERIC_PROBE_CONTROL_EVIDENCE') or args.source)},
              'started_utc': datetime.now(timezone.utc).isoformat(), 'timed_out': False,
              'android_executed': False, 'application_build_executed': False}
    before = {str(path): identity(path) for path in sorted(args.source.rglob('*')) if path.is_file()} if args.source else {}
    started = time.monotonic()
    with (folder / 'stdout.txt').open('xb') as out, (folder / 'stderr.txt').open('xb') as err:
        try:
            p = subprocess.run(argv, cwd=OWN, env=env, stdout=out, stderr=err,
                               timeout=args.timeout, check=False)
            record['returncode'] = p.returncode
        except subprocess.TimeoutExpired:
            record.update(returncode=None, timed_out=True)
        except OSError as exc:
            record.update(returncode=None, error_type=type(exc).__name__, error=str(exc))
    record.update(seconds=time.monotonic() - started, finished_utc=datetime.now(timezone.utc).isoformat(),
                  stdout=identity(folder / 'stdout.txt'), stderr=identity(folder / 'stderr.txt'))
    after = {name: identity(Path(name)) for name in before}
    for name, value in [('command.json', record), ('inputs-before.json', before), ('inputs-after.json', after)]:
        with (folder / name).open('x') as stream:
            stream.write(json.dumps(value, indent=2) + '\n')
    passed = record['returncode'] == 0 and record['timed_out'] is False and before == after
    print(json.dumps({'label': args.name, 'returncode': record['returncode'], 'timed_out': record['timed_out'],
                      'seconds': record['seconds'], 'source_unchanged': before == after,
                      'android_executed': False, 'passed': passed}, indent=2))
    return 0 if passed else 2


if __name__ == '__main__':
    raise SystemExit(main())
