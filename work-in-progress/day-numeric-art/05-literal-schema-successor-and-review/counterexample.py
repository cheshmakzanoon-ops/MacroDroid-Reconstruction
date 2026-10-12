#!/usr/bin/env python3
"""Preserve the old schema-number acceptance using only closed simulated evidence."""
from __future__ import annotations

import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import time
import traceback

OWN = Path('/dev/shm/macrodroid-day-numeric-art-schema-02')
DRAFT = Path('/dev/shm/macrodroid-day-numeric-art/wrapper-draft-01')
CONTROLS = Path('/dev/shm/macrodroid-day-numeric-art/wrapper-controls-01')
POSITIVE = CONTROLS / 'host-evidence/test_complete_simulated_success_cannot_be_claimed_as_android/result'
DRAFT_SHA = '6ca4711b330c64f72c0df716e4a8c407360297a9bbc09e634bd88feb295a6dd6'
WRAPPER_SHA = 'cc8b400f419ae9dc47677bcc9c71257440d46c8278ab32dd5a759378a45e7c96'


def identity(path):
    start = path.lstat()
    assert stat.S_ISREG(start.st_mode), str(path)
    with path.open('rb') as stream:
        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    end = path.lstat()
    assert (start.st_dev, start.st_ino, start.st_size, start.st_mtime_ns, start.st_ctime_ns) == (
        end.st_dev, end.st_ino, end.st_size, end.st_mtime_ns, end.st_ctime_ns), str(path)
    return {'bytes': end.st_size, 'sha256': sha, 'mode': stat.S_IMODE(end.st_mode)}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def child(output):
    wrapper = DRAFT / 'source/android_day_numeric_method_probe.py'
    assert identity(wrapper)['sha256'] == WRAPPER_SHA
    spec = importlib.util.spec_from_file_location('reviewed_old_numeric_wrapper', wrapper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    provenance = json.loads((DRAFT / 'source/probes/day-numeric-method-probe.json').read_bytes())
    original = json.loads((POSITIVE / 'probe-result.json').read_bytes())
    assert original['execution_backend'] == 'simulated-host-control'
    assert original['android_runtime_executed'] is False
    observations = []
    for label, version, expected in [('integer-two', 2, True), ('float-two', 2.0, True),
                                      ('string-two', '2', False), ('boolean-true', True, False),
                                      ('boolean-false', False, False)]:
        # A JSON round trip preserves exactly the report type being reviewed.
        changed_provenance = json.loads(json.dumps({**provenance, 'schema_version': version}))
        changed_report = copy.deepcopy(original)
        changed_report['schema_version'] = json.loads(json.dumps(version))
        row = {'label': label, 'schema_value': version, 'python_type': type(version).__name__}
        for gate, action in (
            ('provenance', lambda: module.validate_provenance(changed_provenance)),
            ('report_replay', lambda: module.verify_result(POSITIVE, changed_report,
                serial='emulator-5560', allow_simulated=True)),
        ):
            try:
                result = action()
                row[gate] = {'accepted': True, 'return_value': result, 'error_type': None, 'error': None}
            except module.ProbeError as exc:
                row[gate] = {'accepted': False, 'return_value': None,
                             'error_type': type(exc).__name__, 'error': str(exc)}
            assert row[gate]['accepted'] is expected, (label, gate, row[gate])
        observations.append(row)
        if label == 'float-two':
            save(output / 'float-provenance-input.json', changed_provenance)
            save(output / 'float-report-input.json', changed_report)
    value = {'schema': 1, 'status': 'OLD_SCHEMA_FLOAT_ACCEPTANCE_REPRODUCED',
             'counterexample_reproduced': True, 'literal_integer_schema_contract_passed': False,
             'scope': 'Read-only old-policy validation/replay of closed simulated evidence; no new ADB run',
             'source_sha256': WRAPPER_SHA, 'original_positive': str(POSITIVE),
             'observations': observations, 'android_executed': False, 'adb_executed': False,
             'application_build_executed': False, 'full_suite_executed': False}
    save(output / 'observations.json', value)
    print(json.dumps({'status': value['status'], 'float_provenance_accepted': True,
                      'float_report_replay_accepted': True, 'android_executed': False}))


def main():
    output = OWN / 'reports/counterexample-01'
    output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(__file__, output / 'executed-collector.py')
    paths = [DRAFT / 'checkpoint.json', CONTROLS / 'result.json']
    assert identity(paths[0])['sha256'] == DRAFT_SHA
    cap = json.loads(paths[0].read_bytes())
    paths.extend(DRAFT / row['path'] for row in cap['files'])
    paths.extend(sorted(path for path in POSITIVE.rglob('*') if path.is_file()))
    before = {str(path): identity(path) for path in paths}
    for row in cap['files']:
        assert before[str(DRAFT / row['path'])] == {k: row[k] for k in ('bytes', 'sha256', 'mode')}
    save(output / 'inputs-before.json', before)
    argv = [sys.executable, '-B', str(output / 'executed-collector.py'), '--child', str(output)]
    record = {'argv': argv, 'cwd': str(OWN), 'timeout_seconds': 120,
              'started_utc': datetime.now(timezone.utc).isoformat(), 'timed_out': False}
    start = time.monotonic()
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(output)}
    with (output / 'stdout.txt').open('xb') as stdout, (output / 'stderr.txt').open('xb') as stderr:
        try:
            process = subprocess.run(argv, cwd=OWN, env=env, stdout=stdout, stderr=stderr,
                                     timeout=120, check=False)
            record['returncode'] = process.returncode
        except subprocess.TimeoutExpired:
            record.update(returncode=None, timed_out=True)
    record.update(seconds=time.monotonic() - start, finished_utc=datetime.now(timezone.utc).isoformat(),
                  stdout=identity(output / 'stdout.txt'), stderr=identity(output / 'stderr.txt'))
    save(output / 'command.json', record)
    after = {str(path): identity(path) for path in paths}
    save(output / 'inputs-after.json', after)
    result = {'status': 'CLOSED_OLD_SCHEMA_COUNTEREXAMPLE' if record['returncode'] == 0 else 'COUNTEREXAMPLE_ATTEMPT_FAILED',
              'counterexample_reproduced': record['returncode'] == 0 and record['timed_out'] is False,
              'literal_integer_schema_contract_passed': False, 'all_inputs_unchanged': before == after,
              'android_executed': False, 'adb_executed': False, 'application_build_executed': False,
              'full_suite_executed': False, 'command': record}
    save(output / 'result.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'command'}, indent=2))
    return 0 if result['counterexample_reproduced'] and before == after else 2


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--child':
        try:
            child(Path(sys.argv[2]))
        except Exception:
            traceback.print_exc()
            raise
    else:
        raise SystemExit(main())
