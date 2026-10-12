#!/usr/bin/env python3
"""Run one bounded owned Settings workflow attempt and preserve its inputs."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--source', required=True)
parser.add_argument('--attempt', required=True)
args = parser.parse_args()
source = ROOT / args.source
evidence = ROOT / 'reports' / args.attempt
evidence.mkdir(exist_ok=False)
guard = Path('/dev/shm/macrodroid-exact-alarm-enable-return/checkpoints/03-source-and-host-controls')
original = Path('/dev/shm/macrodroid-exact-alarm-navigation/workflow-01-validation/private-inputs/workspace/artifacts/MacroDroid-5.67.8-original.apk')
candidate = Path('/dev/shm/macrodroid-exact-alarm-enable-return/numeric-input-01/MacroDroid-5.67.8-day-numeric-0762aad9.apk')
aapt = Path('/dev/shm/macrodroid-exact-alarm-navigation/workflow-01-validation/private-inputs/workspace/MacroDroid_v9/tools/prebuilt/linux/aapt2')
manifest = ROOT / 'inputs/candidate-manifest.json'
own_names = ['prepare_trigger_journey.py', 'verify_trigger_journey.py', 'validate_workflow.py',
             '.github/workflows/editor-exact-alarm-enable-return.yml']


def identity(path):
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': info.st_size, 'sha256': digest, 'mode': stat.S_IMODE(info.st_mode)}


def read_inputs():
    paths = [source / name for name in own_names]
    paths += [ROOT / 'inputs/derive_workflow.py', ROOT / 'inputs/source-review-checkpoint.json',
              ROOT / 'inputs/old-workflow-authoring-checkpoint.json', manifest,
              original, candidate, aapt, guard / 'checkpoint.json']
    paths += [guard / row['path'] for row in json.loads((guard / 'checkpoint.json').read_bytes())['files']]
    paths += [p for p in (ROOT / 'inputs/checkout').rglob('*') if p.is_file()]
    return [{'path': str(path), **identity(path)} for path in sorted(set(paths))]


before = read_inputs()
(evidence / 'inputs-before.json').write_text(json.dumps(before, indent=2) + '\n')
for name in own_names:
    target = evidence / 'executed-source' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source / name, target)
shutil.copy2(__file__, evidence / 'executed-wrapper.py')
argv = [sys.executable, '-B', str(source / 'validate_workflow.py'),
    '--workspace', '/workspace/scratch/4130730d15aa', '--guard', str(guard),
    '--candidate-manifest', str(manifest), '--candidate-apk', str(candidate),
    '--original-apk', str(original), '--aapt2', str(aapt),
    '--checkout', str(ROOT / 'inputs/checkout'), '--output', str(evidence / 'validation')]
result = {'argv': argv, 'cwd': str(ROOT), 'timeout_seconds': 900,
    'started_unix_ns': time.time_ns(), 'started_monotonic_ns': time.monotonic_ns(),
    'android_executed': False, 'app_build_executed': False,
    'fresh_259_source_suite_requested': False}
with (evidence / 'stdout.txt').open('xb') as out, (evidence / 'stderr.txt').open('xb') as err:
    try:
        process = subprocess.run(argv, cwd=ROOT, stdout=out, stderr=err, timeout=900,
            env={**os.environ, 'TMPDIR': str(ROOT / 'tmp'), 'PYTHONDONTWRITEBYTECODE': '1'})
        result.update(exit_code=process.returncode, timed_out=False)
    except subprocess.TimeoutExpired:
        result.update(exit_code=124, timed_out=True)
result.update(finished_unix_ns=time.time_ns(), finished_monotonic_ns=time.monotonic_ns())
after = read_inputs()
(evidence / 'inputs-after.json').write_text(json.dumps(after, indent=2) + '\n')
result['all_immutable_input_bytes_and_modes_unchanged'] = before == after
result['input_count'] = len(before)
for name in ['stdout.txt', 'stderr.txt']:
    result[name] = identity(evidence / name)
result['status'] = 'PASSED' if result['exit_code'] == 0 and before == after else 'FAILED'
(evidence / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
