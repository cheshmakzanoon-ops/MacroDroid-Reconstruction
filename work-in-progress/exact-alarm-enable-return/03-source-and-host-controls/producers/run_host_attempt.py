from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
WORKING = ROOT / 'source-01/repository'


def inventory(folder):
    rows = {}
    for path in sorted(folder.rglob('*')):
        if '__pycache__' in path.parts or path.is_dir():
            continue
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError('Source must be an owned regular single-link file: ' + str(path))
        data = path.read_bytes()
        rows[str(path.relative_to(folder))] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                                            'mode': stat.S_IMODE(info.st_mode)}
    return rows


CHILD = '''from pathlib import Path
import datetime, json, sys, time, unittest
root = Path(sys.argv[1])
sys.path[:0] = [str(root / 'repository/tools/parity_journeys'), str(root / 'repository/project')]
scope = sys.argv[2]
suite = (unittest.defaultTestLoader.loadTestsFromNames([
    'test_exact_alarm_enable_return', 'test_exact_alarm_enable_return_readiness']) if scope == 'focused' else
    unittest.defaultTestLoader.discover(str(root / 'repository/tools/parity_journeys'), pattern='test_*.py'))
def cases(test):
    if isinstance(test, unittest.TestSuite):
        for value in test: yield from cases(value)
    else: yield test
if scope == 'parent':
    suite = unittest.TestSuite(test for test in cases(suite)
        if not test.id().startswith(('test_exact_alarm_enable_return.', 'test_exact_alarm_enable_return_readiness.')))
def flatten(test):
    if isinstance(test, unittest.TestSuite):
        for value in test: yield from flatten(value)
    else: yield test.id()
ids = list(flatten(suite))
assert len(ids) == len(set(ids)), 'Duplicate discovered test identity'
assert len(ids) == (50 if scope == 'focused' else 209), 'Unexpected focused or parent test inventory'
(root / 'discovered-tests.json').write_text(json.dumps(ids, indent=2) + '\\n')
start = time.monotonic()
result = unittest.TextTestRunner(verbosity=2).run(suite)
value = {'schema': 1, 'scope': scope, 'tests_discovered': len(ids), 'tests_run': result.testsRun,
         'failures': [{'test': item.id(), 'traceback': trace} for item, trace in result.failures],
         'errors': [{'test': item.id(), 'traceback': trace} for item, trace in result.errors],
         'skipped': result.skipped, 'unexpected_successes': [item.id() for item in result.unexpectedSuccesses],
         'seconds': time.monotonic() - start, 'passed': result.wasSuccessful(),
         'android_executed': False, 'application_build_executed': False,
         'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
(root / 'tests-result.json').write_text(json.dumps(value, indent=2) + '\\n')
raise SystemExit(0 if value['passed'] else 1)
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('--scope', choices=('focused', 'parent'), default='focused')
    args = parser.parse_args()
    attempt = ROOT / 'source-01/reports' / args.name
    attempt.mkdir(parents=True, exist_ok=False)
    before = inventory(WORKING)
    (attempt / 'source-before.json').write_text(json.dumps(before, indent=2) + '\n')
    for relative, row in before.items():
        target = attempt / 'repository' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(WORKING / relative, target)
        target.chmod(row['mode'])
    assert inventory(attempt / 'repository') == before
    executed_inputs = dict(before)
    fixtures = {}
    if args.scope == 'parent':
        declarations = json.loads((ROOT / 'source-01/reports/02-source-boundary-review/inputs-before.json').read_bytes())
        fixtures = {path: row for path, row in declarations.items() if path.endswith('/evidence.zip')}
        assert len(fixtures) == 2
        parent_inputs = Path('/dev/shm/macrodroid-exact-alarm-navigation/workflow-01-validation/private-inputs')
        for relative, row in fixtures.items():
            data = (parent_inputs / relative).read_bytes()
            assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
            target = attempt / 'repository' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data); target.chmod(0o644)
            executed_inputs[relative] = dict(row, mode=0o644)
        assert inventory(attempt / 'repository') == executed_inputs
    (attempt / 'executed-inputs-before.json').write_text(json.dumps(executed_inputs, indent=2) + '\n')
    (attempt / 'run-tests.py').write_text(CHILD)
    shutil.copyfile(__file__, attempt / 'executed-wrapper.py')
    temporary = attempt / 'test-temporaries'; temporary.mkdir()
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(temporary))
    command = [sys.executable, '-B', str(attempt / 'run-tests.py'), str(attempt), args.scope]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat(); start = time.monotonic()
    with (attempt / 'stdout.txt').open('xb') as out, (attempt / 'stderr.txt').open('xb') as err:
        result = subprocess.run(command, cwd=attempt / 'repository', env=env, stdout=out, stderr=err, timeout=900)
    after = inventory(WORKING)
    executed_after = inventory(attempt / 'repository')
    value = {'schema': 1, 'argv': command, 'cwd': str(attempt / 'repository'), 'timeout_seconds': 900,
             'started_utc': started, 'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'seconds': time.monotonic() - start, 'returncode': result.returncode,
             'source_file_count': len(before), 'working_source_unchanged': before == after,
             'executed_source_unchanged': all(executed_after.get(path) == row for path, row in before.items()),
             'executed_inputs_unchanged': executed_inputs == executed_after,
             'historical_zip_inputs': fixtures,
             'android_executed': False, 'application_build_executed': False}
    (attempt / 'source-after.json').write_text(json.dumps(after, indent=2) + '\n')
    (attempt / 'executed-source-after.json').write_text(json.dumps(executed_after, indent=2) + '\n')
    value['passed'] = result.returncode == 0 and before == after and executed_inputs == executed_after
    (attempt / 'result.json').write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps(value))
    return 0 if value['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
