#!/usr/bin/env python3
"""Record bounded host controls for an inactive UI observation proposal."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


def identities(root):
    return {path.relative_to(root).as_posix(): {'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in sorted(root.rglob('*'))
            if path.is_file() and '__pycache__' not in path.parts and path.suffix not in ('.pyc', '.pyo')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.repository = args.repository.resolve()
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=False)
    before = identities(args.repository)
    (args.output / 'inputs-before.json').write_text(json.dumps(before, indent=2) + '\n')
    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s',
               str(args.repository / 'tools/parity_journeys'), '-p', 'test_*.py', '-v']
    result = {'started_utc': datetime.now(timezone.utc).isoformat(), 'command': command,
              'timeout_seconds': 300, 'android_executed': False, 'active_changes': False}
    start = time.monotonic()
    with (args.output / 'tests.log').open('wb') as log:
        try:
            result['exit_code'] = subprocess.run(command, cwd=args.repository, stdout=log,
                                                  stderr=subprocess.STDOUT, timeout=300).returncode
        except subprocess.TimeoutExpired:
            result['exit_code'] = 124
            result['timed_out'] = True
    result['seconds'] = round(time.monotonic() - start, 6)
    after = identities(args.repository)
    (args.output / 'inputs-after.json').write_text(json.dumps(after, indent=2) + '\n')
    result['source_bytes_unchanged'] = before == after
    result['log_sha256'] = hashlib.sha256((args.output / 'tests.log').read_bytes()).hexdigest()
    result['status'] = 'HOST_CONTROLS_PASSED_INACTIVE' if result['exit_code'] == 0 and before == after else 'HOST_CONTROLS_FAILED_INACTIVE'
    result['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (args.output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'HOST_CONTROLS_PASSED_INACTIVE' else 2


if __name__ == '__main__':
    raise SystemExit(main())
