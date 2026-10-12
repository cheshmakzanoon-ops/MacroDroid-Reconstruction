#!/usr/bin/env python3
"""Retain a source-bound host attempt without any Android or APK execution."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def identities(root):
    return [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size,
             'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
             'mode': oct(p.stat().st_mode & 0o777)}
            for p in sorted(root.rglob('*')) if p.is_file()]


def save(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


parser = argparse.ArgumentParser()
parser.add_argument('attempt')
args = parser.parse_args()
output = ROOT / 'reports' / args.attempt
output.mkdir(parents=True, exist_ok=False)
shutil.copytree(ROOT / 'source', output / 'source')
for name in ['generate_workflow.py', 'run_host_attempt.py']:
    shutil.copy2(ROOT / name, output / name)
before = identities(ROOT / 'source')
parents_before = identities(ROOT / 'parent-inputs')
save(output / 'source-before.json', before)
save(output / 'parents-before.json', parents_before)
temporary = ROOT / 'tmp'
temporary.mkdir(exist_ok=True)
selected = {'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(temporary),
            'INDICATOR_PARENTS': str(ROOT / 'parent-inputs'),
            'INDICATOR_HOST_EVIDENCE': str(output / 'host-evidence')}
argv = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s',
        str(ROOT / 'source/tools/indicator_sampling'), '-p', 'test_*.py', '-v']
record = {'schema': 1, 'scope': 'Synthetic host controls only; no ADB, emulator, Java, or Android.',
          'argv': argv, 'cwd': str(ROOT), 'selected_environment': selected,
          'timeout_seconds': 900, 'started_unix_ns': time.time_ns(),
          'started_monotonic_ns': time.monotonic_ns(), 'android_executed': False}
save(output / 'execution-start.json', record)
with (output / 'stdout.log').open('xb') as stdout, (output / 'stderr.log').open('xb') as stderr:
    try:
        process = subprocess.run(argv, cwd=ROOT, env={**os.environ, **selected},
                                 stdout=stdout, stderr=stderr, timeout=900)
        record.update(returncode=process.returncode, timed_out=False)
    except subprocess.TimeoutExpired:
        record.update(returncode=None, timed_out=True)
record.update(finished_unix_ns=time.time_ns(), finished_monotonic_ns=time.monotonic_ns())
after = identities(ROOT / 'source')
parents_after = identities(ROOT / 'parent-inputs')
save(output / 'source-after.json', after)
save(output / 'parents-after.json', parents_after)
record['source_unchanged'] = before == after
record['parent_inputs_unchanged'] = parents_before == parents_after
record['status'] = ('PASS' if record.get('returncode') == 0 and record['source_unchanged']
                    and record['parent_inputs_unchanged'] else 'FAILED')
record['duration_seconds'] = (record['finished_monotonic_ns'] - record['started_monotonic_ns']) / 1e9
save(output / 'result.json', record)
print(json.dumps(record, indent=2))
