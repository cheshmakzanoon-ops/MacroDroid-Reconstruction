#!/usr/bin/env python3
"""Record one bounded read-only workflow review, without repeating its suites."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

root = Path(__file__).resolve().parent
output = root / 'reports/02-frozen-workflow03-command'
output.mkdir(parents=True, exist_ok=False)
source = root / 'review_workflow03.py'
argv = [sys.executable, '-B', str(source)]
record = {'argv': argv, 'timeout_seconds': 300, 'started_utc': datetime.now(timezone.utc).isoformat(),
          'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
(output / 'executed-launcher.py').write_bytes(Path(__file__).read_bytes())
start = time.monotonic()
with (output / 'stdout.log').open('xb') as stdout, (output / 'stderr.log').open('xb') as stderr:
    try:
        record['exit_code'] = subprocess.run(argv, cwd=root, stdout=stdout, stderr=stderr, timeout=300).returncode
    except subprocess.TimeoutExpired:
        record['exit_code'] = 124; record['timed_out'] = True
record['seconds'] = round(time.monotonic()-start, 6)
record['finished_utc'] = datetime.now(timezone.utc).isoformat()
record['source_unchanged'] = hashlib.sha256(source.read_bytes()).hexdigest() == record['source_sha256']
for stream in ('stdout','stderr'):
    path = output / (stream + '.log')
    record[stream] = {'path':path.name,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
record['passed'] = record['exit_code'] == 0 and record['source_unchanged']
(output / 'command.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2),flush=True)
raise SystemExit(0 if record['passed'] else 2)
