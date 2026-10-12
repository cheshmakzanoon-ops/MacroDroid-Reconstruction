from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
PARENT = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/08-combined-tooling-controls/source')


def inventory(root, single_link=True):
    rows = {}
    for path in sorted(root.rglob('*')):
        if path.is_dir(): continue
        info = path.lstat()
        assert stat.S_ISREG(info.st_mode) and (not single_link or info.st_nlink == 1), str(path)
        data = path.read_bytes()
        rows[str(path.relative_to(root))] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                                           'mode': stat.S_IMODE(info.st_mode)}
    return rows


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('name')
    parser.add_argument('--scope', choices=('old-reproduction', 'focused', 'all'), required=True)
    args = parser.parse_args()
    out = ROOT / 'reports' / args.name; out.mkdir(parents=True, exist_ok=False)
    source = PARENT if args.scope == 'old-reproduction' else ROOT / 'stage-01/repository'
    before = inventory(source, single_link=False); assert len(before) == 9
    checkout = out / 'checkout'; shutil.copytree(source, checkout)
    assert inventory(checkout) == before
    metadata = {'README.md': b'Unrelated checkout root content; fixture only\n',
                'docs/unrelated.txt': b'Unrelated project documentation; fixture only\n'}
    for index in range(45):
        metadata['.git/inert-layout-files/' + f'{index:02d}.txt'] = ('Synthetic inert Git-style metadata ' + str(index) + '\n').encode()
    for relative, data in metadata.items():
        path = checkout / relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
    executed_before = inventory(checkout); assert len(executed_before) == 56
    write(out / 'source-before.json', before); write(out / 'executed-checkout-before.json', executed_before)
    shutil.copyfile(__file__, out / 'executed-wrapper.py')
    tests = ['test_day_trigger_acceptance.CombinedWorkflowControls']
    if args.scope == 'focused': tests.append('test_day_trigger_acceptance.CombinedCheckoutLayoutControls')
    argv = ([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', str(checkout / 'tools/day_trigger_acceptance'),
             '-p', 'test_*.py', '-v'] if args.scope == 'all' else [sys.executable, '-B', '-m', 'unittest', '-v', *tests])
    temporary = out / 'tmp'; temporary.mkdir()
    env = os.environ.copy()
    env.update(PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(temporary),
               PYTHONPATH=str(checkout / 'tools/day_trigger_acceptance'),
               DAY_TRIGGER_CONTROL_EVIDENCE_ROOT=str(out / 'controls'))
    result = {'schema': 1, 'scope': args.scope, 'status': 'INCOMPLETE', 'passed': False,
              'argv': argv, 'cwd': str(checkout), 'timeout_seconds': 300,
              'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'application_executions': 0, 'full_project_materializations': 0, 'android_runtime_executed': False,
              'source_file_count': 9, 'synthetic_unrelated_metadata_files': 47,
              'actual_executed_checkout_files': 56, 'metadata_is_actual_original_checkout_bytes': False}
    write(out / 'result.json', result); start = time.monotonic()
    try:
        with (out / 'stdout.log').open('xb') as stdout, (out / 'stderr.log').open('xb') as stderr:
            child = subprocess.run(argv, cwd=checkout, env=env, stdout=stdout, stderr=stderr, timeout=300)
        result['returncode'] = child.returncode
    except BaseException as error:
        result['error'] = repr(error)
    result['elapsed_seconds'] = time.monotonic() - start
    result['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    after = inventory(source, single_link=False); executed_after = inventory(checkout)
    write(out / 'source-after.json', after); write(out / 'executed-checkout-after.json', executed_after)
    result['source_unchanged'] = before == after
    result['entire_checkout_including_unrelated_metadata_unchanged'] = executed_before == executed_after
    raw = (out / 'stderr.log').read_text(); summaries = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', raw, re.M)
    assert len(summaries) == 1
    result['observed_tests'] = int(summaries[0][0]); result['unittest_seconds'] = float(summaries[0][1])
    result['failed_tests'] = re.findall(r'^FAIL: ([^\n]+)$', raw, re.M)
    result['errors'] = re.findall(r'^ERROR: ([^\n]+)$', raw, re.M)
    result['test_names'] = re.findall(r'^test_\S+ \(([^)]+)\) \.\.\. ', raw, re.M)
    assert len(result['test_names']) == len(set(result['test_names'])) == result['observed_tests']
    result['last_log_line'] = raw.strip().splitlines()[-1]
    if args.scope == 'old-reproduction':
        result['expected_failure_reproduced'] = (result.get('returncode') == 1 and result['observed_tests'] == 4
            and len(result['failed_tests']) == 1 and not result['errors'] and 'AssertionError: 9 != 56' in raw
            and result['failed_tests'][0].startswith('test_workflow_runtime_pin_binds_all_seven_actual_runtime_siblings '))
        result['passed'] = result['expected_failure_reproduced'] and before == after and executed_before == executed_after
        result['status'] = 'ORIGINAL_TEST_CHECKOUT_LAYOUT_FAILURE_REPRODUCED' if result['passed'] else 'REPRODUCTION_DID_NOT_MATCH'
        result['tooling_gate_passed'] = False
    else:
        result['passed'] = (result.get('returncode') == 0 and result['last_log_line'] == 'OK'
            and result['observed_tests'] == (6 if args.scope == 'focused' else 155)
            and before == after and executed_before == executed_after)
        result['status'] = 'CHECKOUT_LAYOUT_TOOLING_CONTROLS_PASSED_NO_APP_EXECUTION' if result['passed'] else 'CHECKOUT_LAYOUT_TOOLING_CONTROLS_FAILED'
        result['tooling_gate_passed'] = result['passed'] and args.scope == 'all'
    write(out / 'result.json', result)
    print(json.dumps({key: result[key] for key in ('status','returncode','passed','observed_tests','failed_tests',
          'elapsed_seconds','source_unchanged','entire_checkout_including_unrelated_metadata_unchanged')}))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
