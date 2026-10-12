#!/usr/bin/env python3
"""Record the bounded, read-only DayTime13 independent review subprocess."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'reports/01-frozen-daytime13-zero12-replay'


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    source = ROOT / 'review_daytime13.py'
    argv = [sys.executable, '-B', str(source), '--output', str(OUT / 'review')]
    record = {'argv': argv, 'timeout_seconds': 300,
              'started_utc': datetime.now(timezone.utc).isoformat(),
              'review_source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'launcher_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT / 'executed-launcher.py').write_bytes(Path(__file__).read_bytes())
    tick = time.monotonic()
    with (OUT / 'stdout.log').open('xb') as stdout, (OUT / 'stderr.log').open('xb') as stderr:
        try:
            record['exit_code'] = subprocess.run(argv, stdout=stdout, stderr=stderr,
                cwd=ROOT, timeout=300).returncode
        except subprocess.TimeoutExpired:
            record['exit_code'] = 124
            record['timed_out'] = True
    record['seconds'] = round(time.monotonic()-tick, 6)
    record['finished_utc'] = datetime.now(timezone.utc).isoformat()
    for stream in ('stdout', 'stderr'):
        path = OUT / (stream + '.log')
        record[stream] = {'path': path.name, 'bytes': path.stat().st_size,
                          'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    record['review_source_unchanged'] = hashlib.sha256(source.read_bytes()).hexdigest() == record['review_source_sha256']
    record['passed'] = record['exit_code'] == 0 and record['review_source_unchanged']
    (OUT / 'command.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2), flush=True)
    return 0 if record['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
