#!/usr/bin/env python3
"""Submit one explicit argv command to android_runtime_service.py's file queue."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time
import uuid


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--queue', type=Path, required=True)
    parser.add_argument('--timeout', type=float, default=120)
    parser.add_argument('--cwd')
    parser.add_argument('--env', action='append', default=[], metavar='NAME=VALUE')
    parser.add_argument('--stdout-file', type=Path)
    parser.add_argument('--id')
    parser.add_argument('argv', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = args.argv[1:] if args.argv[:1] == ['--'] else args.argv
    if not argv:
        parser.error('Provide a command after --')
    job_id = args.id or uuid.uuid4().hex
    if not job_id or len(job_id) > 100 or any(not (x.isascii() and (x.isalnum() or x in '_-')) for x in job_id):
        parser.error('Job ID must contain only ASCII letters, digits, underscore, or hyphen')
    request = {'argv': argv, 'timeout_s': args.timeout, 'cwd': args.cwd, 'env': {}}
    for item in args.env:
        if '=' not in item:
            parser.error('--env requires NAME=VALUE')
        name, value = item.split('=', 1)
        request['env'][name] = value
    queue = args.queue.resolve()
    pending = queue / 'requests' / (job_id + '.json')
    response = queue / 'responses' / (job_id + '.json')
    if any(p.exists() for p in [pending, pending.with_suffix('.running'), pending.with_suffix('.done'), response]):
        parser.error('Job ID has already been used')
    temp = pending.with_suffix('.tmp')
    temp.write_text(json.dumps(request, indent=2) + '\n')
    temp.replace(pending)
    deadline = time.monotonic() + args.timeout + 30
    while not response.exists():
        if time.monotonic() >= deadline:
            print(f'No response before client deadline; request remains queued: {job_id}', file=sys.stderr)
            return 124
        time.sleep(0.2)
    result = json.loads(response.read_text())
    stdout = Path(result['stdout_path'])
    stderr = Path(result['stderr_path'])
    if stdout.exists():
        if args.stdout_file:
            args.stdout_file.write_bytes(stdout.read_bytes())
        else:
            sys.stdout.buffer.write(stdout.read_bytes())
    if stderr.exists():
        sys.stderr.buffer.write(stderr.read_bytes())
    if result.get('error'):
        print(result['error'], file=sys.stderr)
    return int(result['exit_code'])


if __name__ == '__main__':
    raise SystemExit(main())
