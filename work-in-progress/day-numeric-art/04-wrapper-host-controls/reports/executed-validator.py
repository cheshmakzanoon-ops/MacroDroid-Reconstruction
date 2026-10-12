#!/usr/bin/env python3
"""Execute only read-only real-input validation and explicit simulated host controls."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import time
import traceback

BASE = Path('/dev/shm/macrodroid-day-numeric-art')
CAP = BASE / 'wrapper-draft-01'
OUT = BASE / 'wrapper-controls-01'
ORIGINAL = Path('/workspace/scratch/4130730d15aa/recovered/automation android app')
CANDIDATE = Path('/dev/shm/macrodroid-exact-alarm-enable-return/numeric-input-01/MacroDroid-5.67.8-day-numeric-0762aad9.apk')


def identity(path):
    a = path.lstat(); assert stat.S_ISREG(a.st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    b = path.lstat()
    assert (a.st_dev, a.st_ino, a.st_size, a.st_mtime_ns, a.st_ctime_ns) == (b.st_dev, b.st_ino, b.st_size, b.st_mtime_ns, b.st_ctime_ns)
    return {'bytes': b.st_size, 'sha256': digest, 'mode': stat.S_IMODE(b.st_mode)}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def preflight(source, output):
    module_path = source / 'android_day_numeric_method_probe.py'
    spec = importlib.util.spec_from_file_location('numeric_probe', module_path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    value = module.validate_inputs(ORIGINAL, CANDIDATE,
        source / 'probes/day-numeric-method-probe.dex', source / 'probes/day-numeric-method-probe.json')
    save(output, {'status': 'ACTUAL_PINNED_INPUTS_VALIDATED_READ_ONLY', 'inputs': value,
                 'android_executed': False, 'app_build_executed': False,
                 'application_class_loaded': False, 'adb_executed': False})
    print('Actual original, candidate, neutral DEX, provenance and all 1291 input rows verified read-only.')


def main():
    OUT.mkdir(exist_ok=False)
    shutil.copyfile(__file__, OUT / 'executed-validator.py')
    before = {str(CAP / 'checkpoint.json'): identity(CAP / 'checkpoint.json')}
    assert before[str(CAP / 'checkpoint.json')]['sha256'] == '6ca4711b330c64f72c0df716e4a8c407360297a9bbc09e634bd88feb295a6dd6'
    cap = json.loads((CAP / 'checkpoint.json').read_bytes())
    source = OUT / 'executed-source'; source.mkdir()
    for row in cap['files']:
        path = CAP / row['path']; before[str(path)] = identity(path)
        assert before[str(path)] == {k: row[k] for k in ('bytes', 'sha256', 'mode')}
        if row['path'].startswith('source/'):
            target = source / row['path'][len('source/'):]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target); target.chmod(row['mode'])
            before[str(target)] = identity(target)
            assert before[str(target)] == before[str(path)]
    for path in (ORIGINAL, CANDIDATE):
        before[str(path)] = identity(path)
    tmp = OUT / 'temporary'; tmp.mkdir()
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(tmp),
           'NUMERIC_PROBE_CONTROL_EVIDENCE': str(OUT / 'host-evidence')}
    result = {'schema': 1, 'started_utc': datetime.now(timezone.utc).isoformat(), 'passed': False,
              'commands': [], 'android_executed': False, 'app_build_executed': False,
              'test_backend': 'explicit-simulated-ADB-host-controls'}
    def execute(label, argv, bound):
        folder = OUT / 'commands' / label; folder.mkdir(parents=True, exist_ok=False)
        record = {'label': label, 'argv': argv, 'cwd': str(OUT), 'timeout_seconds': bound,
                  'started_utc': datetime.now(timezone.utc).isoformat(), 'timed_out': False}
        started = time.monotonic()
        with (folder / 'stdout.txt').open('wb') as out, (folder / 'stderr.txt').open('wb') as err:
            try:
                process = subprocess.run(argv, cwd=OUT, env=env, stdout=out, stderr=err, timeout=bound)
                record['returncode'] = process.returncode
            except subprocess.TimeoutExpired:
                record.update(returncode=None, timed_out=True)
        record.update(seconds=time.monotonic() - started, finished_utc=datetime.now(timezone.utc).isoformat(),
                      stdout=identity(folder / 'stdout.txt'), stderr=identity(folder / 'stderr.txt'))
        save(folder / 'command.json', record); result['commands'].append(record)
        print(json.dumps({'label': label, 'returncode': record['returncode'], 'timed_out': record['timed_out'],
                          'seconds': record['seconds']}), flush=True)
        return record
    try:
        first = execute('actual-input-preflight', [sys.executable, '-B', str(OUT / 'executed-validator.py'),
            '--preflight', str(source), str(OUT / 'actual-input-preflight.json')], 120)
        assert first['returncode'] == 0 and first['timed_out'] is False
        second = execute('all-41-host-controls', [sys.executable, '-B', '-m', 'unittest', 'discover',
            '-s', str(source), '-p', 'test_android_day_numeric_method_probe.py', '-v'], 240)
        text = (OUT / 'commands/all-41-host-controls/stderr.txt').read_text()
        summary = re.search(r'^Ran (\d+) tests in ([0-9.]+)s$', text, re.M)
        result['actual_named_test_count'] = int(summary[1]) if summary else None
        result['unittest_summary'] = summary[0] if summary else None
        assert second['returncode'] == 0 and second['timed_out'] is False
        assert summary and int(summary[1]) == 41 and text.rstrip().endswith('OK')
        result.update(passed=True, status='ACTUAL_INPUT_PREFLIGHT_AND_41_SIMULATED_HOST_CONTROLS_PASSED')
    except Exception as error:
        result.update(status='NUMERIC_ART_WRAPPER_HOST_VALIDATION_FAILED', reason=repr(error))
        save(OUT / 'exception.json', {'error': repr(error), 'traceback': traceback.format_exc()})
    finally:
        after = {name: identity(Path(name)) for name in before}
        result['all_read_inputs_unchanged'] = before == after
        if before != after:
            result['passed'] = False
        save(OUT / 'inputs-before.json', before); save(OUT / 'inputs-after.json', after)
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(OUT / 'result.json', result)
        print(json.dumps({k:v for k,v in result.items() if k != 'commands'}, indent=2), flush=True)
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == '--preflight':
        preflight(Path(sys.argv[2]), Path(sys.argv[3]))
    else:
        raise SystemExit(main())
