#!/usr/bin/env python3
"""Replay the immutable failed job's bytes; all replay commands stay simulated."""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import time
from unittest import mock
import uuid

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / 'checkpoints/01-wrapper-review/android_widget_method_probe.py'
ACTUAL = ROOT.parent / 'hosted-run-38206308421'
OLD_SHA256 = 'c16dcf9376b1ea4de42ca51c63caeeb2ab157a5f4b89fcd0eea505182302d983'
ZIP_SHA256 = 'a860b5ca2b438db9c77e0ed362d4dcc8f2268ea29a767e931e370c29fb79afbe'
ORIGINAL = ROOT.parent.parent / 'recovered/automation android app'
CANDIDATE = Path('/tmp/macrodroid-widget-art-inputs-t0vfcjt_/candidate.apk')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path):
    return {'path': str(path.resolve()), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def module(name, source):
    spec = importlib.util.spec_from_file_location(name, source)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def validate_actual_bytes():
    manifest = json.loads((ACTUAL / 'download-manifest.json').read_text())
    if (manifest['run_id'] != 38206308421 or manifest['job_id'] != 114670448046 or
            manifest['head_sha'] != 'f050cfcfd70af4699f9145311b8628260c1ed17c' or
            manifest['archive']['bytes'] != 1_995_749 or
            manifest['archive']['sha256'] != ZIP_SHA256 or sha(ACTUAL / 'artifact.zip') != ZIP_SHA256):
        raise RuntimeError('Historical artifact identity changed')
    for row in manifest['files']:
        path = ACTUAL / 'extracted' / row['path']
        if path.is_symlink() or path.stat().st_size != row['bytes'] or sha(path) != row['sha256']:
            raise RuntimeError('Historical extracted evidence changed: ' + row['path'])
    report = json.loads((ACTUAL / 'extracted/probe/probe-result.json').read_text())
    if (report['status'] != 'ART_WIDGET_EVIDENCE_INVALID' or
            report['evidence_error'] != 'Observed environment or state differs: avd-name' or
            len(report['commands']) != 60 or
            report['wrapper_artifact']['sha256'] != OLD_SHA256 or sha(OLD) != OLD_SHA256):
        raise RuntimeError('Historical failure or original wrapper changed')
    if sha(ACTUAL / 'extracted/probe/executed-wrapper.py') != OLD_SHA256:
        raise RuntimeError('Actual job did not run the frozen original wrapper')
    raw = ACTUAL / 'extracted/probe/010-avd-name.stdout.txt'
    if (raw.read_bytes() != b'MacroDroid_API35_Disposable\r\nOK\r\n' or
            sha(raw) != '8522ad4bd14867dd505fdecb0e0657c506a22c36d86c8a8634fdfda384bae977'):
        raise RuntimeError('The observed failure is not the exact CRLF response')
    return manifest, report


class RecordedADB:
    """Reject unrecorded commands, then return unchanged observed stdout/stderr."""
    def __init__(self, actual, args):
        self.actual, self.args, self.index = actual, args, 0

    def __call__(self, argv, **kwargs):
        if self.index >= len(self.actual['commands']):
            raise AssertionError('Replay attempted an extra command')
        record = self.actual['commands'][self.index]
        expected = list(record['argv'])
        expected[0] = self.args.adb
        if record['label'].startswith('push-'):
            key = record['label'].removeprefix('push-')
            expected[4] = str(getattr(self.args, key).resolve())
        if (argv != expected or kwargs != {'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
                'timeout': record['timeout_seconds'], 'check': False} or
                record['returncode'] != 0 or record['timed_out'] is not False):
            raise AssertionError('Replay command diverged from the actual bound sequence: ' + record['label'])
        self.index += 1
        streams = {}
        for name in ('stdout', 'stderr'):
            row = record[name]
            path = ACTUAL / 'extracted/probe' / row['path']
            data = path.read_bytes()
            if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
                raise AssertionError('Recorded command bytes changed')
            streams[name] = data
        return subprocess.CompletedProcess(argv, record['returncode'], streams['stdout'], streams['stderr'])


def replay(source, output, actual):
    implementation = module('widget_replay_' + output.name.replace('-', '_'), source)
    with tempfile.TemporaryDirectory(prefix='widget-avd-readonly-replay-') as temporary:
        adb = Path(temporary) / 'simulated-adb'
        adb.write_text('Never executed. Recorded ADB responses are injected explicitly.\n')
        args = argparse.Namespace(adb=str(adb), serial='emulator-5560', avd=implementation.DEFAULT_AVD,
            original=ORIGINAL, candidate=CANDIDATE, probe=ROOT / 'probes/widget-method-probe.dex',
            provenance=ROOT / 'probes/widget-method-probe.json', output=output, timeout=120)
        runner = RecordedADB(actual, args)
        # Preserve the exact recorded remote path solely to compare the commands.
        # The runner returns captured bytes and never invokes ADB or this path.
        recorded_uuid = uuid.UUID(hex=actual['owned_device_directory'].rsplit('-', 1)[-1])
        with mock.patch.object(implementation.shutil, 'which', return_value=str(adb)), \
                mock.patch.object(implementation.uuid, 'uuid4', return_value=recorded_uuid):
            code, report = implementation.run_probe(args, runner=runner)
        if runner.index != 60 or report['android_runtime_executed'] is not False:
            raise RuntimeError('Replay omitted commands or claimed new Android execution')
        return {'source': identity(source), 'returncode': code, 'status': report['status'],
            'command_count': runner.index, 'evidence_error': report.get('evidence_error'),
            'android_executed_during_replay': False,
            'scope': 'Recorded command/stream replay only; local APK hashes are checked, no guest command is executed.',
            'path_rebindings': 'Only the local ADB pathname and three local push source paths differ; all guest commands remain exact.',
            'report': identity(output / 'probe-result.json')}


def main():
    output = ROOT / 'reports/validation-01'
    output.mkdir(parents=True, exist_ok=False)
    result = {'status': 'RUNNING', 'passed': False, 'android_executed_during_validation': False,
        'historical_android_job_stays_failed': True, 'fresh_android_rerun_required': True,
        'started_utc': datetime.now(timezone.utc).isoformat(), 'commands': [], 'replays': []}
    before = identity(ACTUAL / 'extracted/probe/probe-result.json')
    try:
        manifest, actual = validate_actual_bytes()
        result['actual_artifact'] = manifest['archive']
        result['historical_files_hash_verified'] = len(manifest['files'])
        result['historical_probe_result_before'] = before
        for label, source, expected_code in [('old-wrapper-recorded-failure', OLD, 2),
                ('new-policy-recorded-replay', ROOT / 'android_widget_method_probe.py', 0)]:
            value = replay(source, output / label, actual)
            result['replays'].append(value)
            if value['returncode'] != expected_code:
                raise RuntimeError('Recorded replay returned an unexpected outcome: ' + label)
        if result['replays'][0]['evidence_error'] != actual['evidence_error']:
            raise RuntimeError('Old wrapper did not reproduce its exact recorded evidence failure')
        result['replays'][1]['scope'] += ' Success concerns the new host evidence policy; it does not relabel the historical job.'
        command = [sys.executable, '-m', 'unittest', 'discover', '-s', str(ROOT),
                   '-p', 'test_android_widget_method_probe.py', '-v']
        env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1',
            'WIDGET_PROBE_CONTROL_EVIDENCE': str(output / 'host-control-evidence')}
        started = time.monotonic()
        with (output / 'tests.stdout.txt').open('wb') as out, (output / 'tests.stderr.txt').open('wb') as err:
            completed = subprocess.run(command, cwd=ROOT, env=env, stdout=out, stderr=err, timeout=120)
        result['commands'].append({'argv': command, 'cwd': str(ROOT), 'timeout_seconds': 120,
            'elapsed_seconds': round(time.monotonic() - started, 6), 'returncode': completed.returncode,
            'stdout': identity(output / 'tests.stdout.txt'), 'stderr': identity(output / 'tests.stderr.txt')})
        text = (output / 'tests.stderr.txt').read_text()
        if completed.returncode != 0 or 'Ran 31 tests in ' not in text or not text.rstrip().endswith('OK'):
            raise RuntimeError('All 31 existing and new wrapper tests must pass')
        validate_actual_bytes()
        result['historical_probe_result_after'] = identity(ACTUAL / 'extracted/probe/probe-result.json')
        if result['historical_probe_result_after'] != before:
            raise RuntimeError('Historical report changed during validation')
        result['wrapper_sha256'] = sha(ROOT / 'android_widget_method_probe.py')
        result['tests_sha256'] = sha(ROOT / 'test_android_widget_method_probe.py')
        result['passed'] = True
        result['status'] = 'OLD_FAILURE_REPRODUCED_NEW_POLICY_HOST_CONTROLS_PASSED'
    except Exception as error:
        result['status'] = 'VALIDATION_FAILED'
        result['error'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(output / 'result.json', result)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
