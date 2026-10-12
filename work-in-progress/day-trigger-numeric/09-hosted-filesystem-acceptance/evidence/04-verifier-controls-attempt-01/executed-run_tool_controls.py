#!/usr/bin/env python3
"""Retain exact executed tooling plus every requested control's raw fixture."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('attempt')
parser.add_argument('tests', nargs='+')
args = parser.parse_args()
output = root / 'reports' / args.attempt
output.mkdir(parents=True, exist_ok=False)
source = root / 'source'
def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
before = []
for path in sorted(source.rglob('*')):
    if path.is_file():
        name = path.relative_to(source).as_posix()
        target = output / 'executed-source' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        before.append({'path': name, **identity(path)})
(output / 'tmp').mkdir()
env = os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', TMPDIR=str(output / 'tmp'),
           DAY_NUMERIC_CONTROL_EVIDENCE_ROOT=str(output / 'control-evidence'))
command = [sys.executable, '-B', '-m', 'unittest', '-v', *args.tests]
started = time.time_ns()
with (output / 'stdout.log').open('xb') as stdout, (output / 'stderr.log').open('xb') as stderr:
    completed = subprocess.run(command, cwd=source / 'tools/day_numeric_acceptance', env=env,
                               stdout=stdout, stderr=stderr, timeout=120)
ended = time.time_ns()
after = [{'path': row['path'], **identity(source / row['path'])} for row in before]
log = (output / 'stderr.log').read_text()
counts = re.findall(r'^Ran (\d+) tests? in ([\d.]+)s$', log, re.M)
summary = {'schema': 1, 'scope': 'Tooling controls and bounded Python subprocesses only; no Java, D8, application build or Android',
           'argv': command, 'cwd': str(source / 'tools/day_numeric_acceptance'),
           'started_unix_ns': started, 'ended_unix_ns': ended,
           'started_utc': datetime.fromtimestamp(started // 1000000000, timezone.utc).isoformat(),
           'returncode': completed.returncode, 'tests': int(counts[-1][0]) if counts else None,
           'unittest_seconds': float(counts[-1][1]) if counts else None,
           'passed': completed.returncode == 0 and '\nOK\n' in log,
           'source_before': before, 'source_after': after, 'source_unchanged': before == after,
           'streams': {name: identity(output / (name + '.log')) for name in ('stdout', 'stderr')},
           'retained_control_observations': len(list((output / 'control-evidence').glob('*/observations.json')))}
(output / 'result.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({key: value for key, value in summary.items() if key not in ('source_before','source_after')}, indent=2))
if not summary['source_unchanged']:
    raise RuntimeError('Executed source changed')
raise SystemExit(completed.returncode)
