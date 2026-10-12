#!/usr/bin/env python3
"""Retain bounded control attempts with immutable source identities and snapshots."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time


def identity(path):
    return {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def inventory(folder):
    return {path.relative_to(folder).as_posix(): identity(path) for path in sorted(folder.rglob('*'))
            if path.is_file() and '__pycache__' not in path.parts and path.suffix not in ('.pyc', '.pyo')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--pattern', default='test_*.py')
    args = parser.parse_args()
    repository, output = args.repository.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    before = inventory(repository)
    (output / 'inputs-before.json').write_text(json.dumps(before, indent=2) + '\n')
    for name in ('notification_readiness.py', 'test_notification_readiness.py', 'editor_journey.py', 'observed_journey.py'):
        target = output / 'executed-source' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(repository / 'tools/parity_journeys' / name, target)
    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s',
               str(repository / 'tools/parity_journeys'), '-p', args.pattern, '-v']
    result = {'started_utc': datetime.now(timezone.utc).isoformat(), 'command': command, 'timeout_seconds': 300,
              'android_executed': False, 'active_changes': False, 'operation': identity(Path(__file__))}
    start = time.monotonic()
    with (output / 'tests.log').open('wb') as log:
        try:
            result['exit_code'] = subprocess.run(command, cwd=repository, stdout=log, stderr=subprocess.STDOUT, timeout=300).returncode
        except subprocess.TimeoutExpired:
            result.update(exit_code=124, timed_out=True)
    result['seconds'] = time.monotonic() - start
    after = inventory(repository)
    (output / 'inputs-after.json').write_text(json.dumps(after, indent=2) + '\n')
    result.update(source_bytes_unchanged=before == after, log=identity(output / 'tests.log'),
                  finished_utc=datetime.now(timezone.utc).isoformat())
    result['status'] = 'HOST_CONTROLS_PASSED_INACTIVE' if result['exit_code'] == 0 and before == after else 'HOST_CONTROLS_FAILED_INACTIVE'
    (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'HOST_CONTROLS_PASSED_INACTIVE' else 2


if __name__ == '__main__':
    raise SystemExit(main())
