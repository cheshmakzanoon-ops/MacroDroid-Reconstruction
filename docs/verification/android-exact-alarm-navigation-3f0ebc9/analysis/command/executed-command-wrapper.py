#!/usr/bin/env python3
"""Retain one bounded, offline replay of the immutable Alarm14 artifact."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path('/dev/shm/macrodroid-exact-alarm-navigation')
DEST = ROOT / 'device-run-38240023189'
RAW_ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012/alarm14-run-38240023189')
SOURCE = ROOT / 'device-analysis-01/analyze_device_run.py'


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def clock():
    wall = time.time_ns()
    mono = time.monotonic_ns()
    whole, remainder = divmod(wall, 1_000_000_000)
    utc = datetime.fromtimestamp(whole, timezone.utc).replace(microsecond=remainder // 1000).isoformat()
    return {'unix_ns': wall, 'monotonic_ns': mono, 'utc': utc}


def main():
    DEST.mkdir(exist_ok=False)
    command = DEST / 'command'
    command.mkdir()
    shutil.copyfile(Path(__file__), command / 'executed-command-wrapper.py')
    shutil.copyfile(SOURCE, command / 'replayed-source.py')
    scratch = DEST / 'temporary-replay-work'
    scratch.mkdir()
    argv = [sys.executable, '-B', str(SOURCE),
        '--raw', str(RAW_ROOT / 'extracted'),
        '--archive', str(RAW_ROOT / 'artifact.zip'),
        '--archive-sha256', 'c34d417c0b5d996e62d403023e9f9c9d122633c2ea65fb1cf45599643abdcf04',
        '--run-id', '38240023189', '--artifact-id', '11742624179',
        '--head', '3f0ebc910be72beeb9d7f2443928df2df2258c7d',
        '--original', '/workspace/scratch/4130730d15aa/recovered/automation android app',
        '--candidate', '/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/dist/MacroDroid-5.67.8-v9-hybrid.apk',
        '--output', str(DEST / 'analysis')]
    receipt = {'schema': 1, 'argv': argv, 'cwd': str(ROOT), 'source_before': identity(SOURCE),
        'timeout_seconds': 900, 'timed_out': False, 'new_android_actions': [],
        'started': clock(), 'tmpdir': str(scratch)}
    environment = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
    returncode = 127
    try:
        with (command / 'stdout.log').open('xb') as stdout, (command / 'stderr.log').open('xb') as stderr:
            child = subprocess.Popen(argv, cwd=ROOT, env=environment, stdout=stdout, stderr=stderr,
                                     start_new_session=True)
            receipt['owned_child_pid'] = child.pid
            try:
                returncode = child.wait(timeout=900)
            except subprocess.TimeoutExpired:
                receipt['timed_out'] = True
                os.killpg(child.pid, signal.SIGKILL)
                returncode = child.wait(timeout=30)
    except Exception as error:
        receipt['wrapper_error'] = type(error).__name__ + ': ' + str(error)
    finally:
        receipt.update(finished=clock(), exit_code=returncode, source_after=identity(SOURCE))
        receipt['source_unchanged'] = receipt['source_before'] == receipt['source_after']
        receipt['streams'] = {name: identity(command / name) for name in ('stdout.log', 'stderr.log')
                              if (command / name).is_file()}
        receipt['temporary_children_after_process_exit'] = sorted(p.name for p in scratch.iterdir())
        if not receipt['temporary_children_after_process_exit']:
            scratch.rmdir()
        receipt['temporary_directory_removed'] = not scratch.exists()
        (command / 'command.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps({'exit_code': returncode, 'timed_out': receipt['timed_out'],
                          'source_unchanged': receipt['source_unchanged'], 'output': str(DEST)}, indent=2))
    return returncode if returncode >= 0 else 2


if __name__ == '__main__':
    raise SystemExit(main())
