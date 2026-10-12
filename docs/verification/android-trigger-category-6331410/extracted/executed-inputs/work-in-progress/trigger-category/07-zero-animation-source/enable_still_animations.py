#!/usr/bin/env python3
"""Set and prove animation scale 0 on the exact disposable API35 emulator.

This prepares a separately declared still-frame diagnostic. It does not modify
APKs, screen captures, comparison thresholds, or historical run evidence.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import subprocess
import time

SERIAL = 'emulator-5560'
AVD = 'MacroDroid_API35_Disposable'
FINGERPRINT = 'google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.043/12960925:userdebug/dev-keys'
SCALES = ('animator_duration_scale', 'window_animation_scale', 'transition_animation_scale')


class EvidenceError(ValueError):
    pass


def digest(path):
    return {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def exact_line(value):
    raw = value.encode('ascii') + b'\n'
    return (raw, raw.replace(b'\n', b'\r\n'))


def specification():
    result = [('device-state', ['get-state'], exact_line('device'))]
    props = [('emulator', 'ro.kernel.qemu', '1'), ('boot', 'sys.boot_completed', '1'),
             ('sdk', 'ro.build.version.sdk', '35'), ('fingerprint', 'ro.build.fingerprint', FINGERPRINT)]
    result += [(label, ['shell', 'getprop', key], exact_line(value)) for label, key, value in props]
    result += [('avd-name', ['emu', 'avd', 'name'], exact_line(AVD + '\nOK'))]
    result += [('before-' + key, ['shell', 'settings', 'get', 'global', key], None) for key in SCALES]
    result += [('set-' + key, ['shell', 'settings', 'put', 'global', key, '0'], (b'',)) for key in SCALES]
    result += [('after-' + key, ['shell', 'settings', 'get', 'global', key],
                exact_line('0') + exact_line('0.0')) for key in SCALES]
    result += [('final-' + label, ['shell', 'getprop', key], exact_line(value)) for label, key, value in props]
    return result


def validate_stdout(label, value, expected):
    if expected is not None:
        if value not in expected:
            raise EvidenceError('Unexpected exact output: ' + label)
    elif not re.fullmatch(rb'(?:null|[0-9]+(?:\.[0-9]+)?)(?:\n|\r\n)', value):
        raise EvidenceError('Malformed initial animation setting: ' + label)


def artifact(folder, item, expected_path):
    if not isinstance(item, dict) or item.get('path') != expected_path or type(item.get('bytes')) is not int:
        raise EvidenceError('Unbound command artifact')
    relative = PurePosixPath(item['path'])
    if relative.is_absolute() or '..' in relative.parts or len(relative.parts) != 1:
        raise EvidenceError('Invalid command artifact path')
    path = folder / relative
    if path.is_symlink() or path.resolve().parent != folder.resolve() or not path.is_file():
        raise EvidenceError('Missing, aliased or unconstrained command artifact')
    raw = path.read_bytes()
    if len(raw) != item['bytes'] or hashlib.sha256(raw).hexdigest() != item.get('sha256'):
        raise EvidenceError('Command artifact bytes changed')
    return raw


def verify_report(folder, report):
    if (report.get('schema') != 1 or report.get('serial') != SERIAL or report.get('expected_avd') != AVD
            or report.get('requested_scales') != {key: '0' for key in SCALES}
            or type(report.get('android_executed')) is not bool
            or report.get('apks_modified') is not False or report.get('screenshots_modified') is not False
            or report.get('comparison_rules_changed') is not False
            or report.get('source_sha256') != digest(Path(__file__))['sha256']):
        raise EvidenceError('Diagnostic identity or declared scope changed')
    spec = specification()
    if len(report.get('commands', [])) != len(spec):
        raise EvidenceError('Incomplete diagnostic command sequence')
    previous = report['started_monotonic']
    if type(previous) not in (float, int) or not math.isfinite(previous):
        raise EvidenceError('Invalid diagnostic start')
    for number, (row, (label, args, expected)) in enumerate(zip(report['commands'], spec), 1):
        if (row.get('label') != label or row.get('argv') != [report['adb'], '-s', SERIAL, *args]
                or type(row.get('exit_code')) is not int or row['exit_code'] != 0
                or row.get('timed_out') is not False):
            raise EvidenceError('Diagnostic command identity or result changed: ' + label)
        start, finish = row['started_monotonic'], row['finished_monotonic']
        if (any(type(value) not in (float, int) or not math.isfinite(value) for value in (start, finish))
                or not previous <= start <= finish or finish - start > 15.5):
            raise EvidenceError('Stale, unordered or over-deadline diagnostic command: ' + label)
        previous = finish
        stdout = artifact(folder, row['stdout'], f'{number:03d}-{label}.stdout.txt')
        stderr = artifact(folder, row['stderr'], f'{number:03d}-{label}.stderr.txt')
        if stderr:
            raise EvidenceError('Unexpected diagnostic stderr: ' + label)
        validate_stdout(label, stdout, expected)
    if not previous <= report['finished_monotonic'] <= report['started_monotonic'] + 300:
        raise EvidenceError('Diagnostic exceeded its total deadline')
    return {key: '0' for key in SCALES}


def run(args, executor=None):
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=False)
    report = {'schema': 1, 'status': 'PREPARING_ANIMATION_DIAGNOSTIC',
              'scope': 'Explicit animation-scale-zero preparation for an independent still-frame comparison',
              'serial': args.serial, 'expected_avd': AVD, 'adb': str(Path(args.adb).resolve()),
              'source_sha256': digest(Path(__file__))['sha256'],
              'requested_scales': {key: '0' for key in SCALES},
              'apks_modified': False, 'screenshots_modified': False, 'comparison_rules_changed': False,
              'animation_timing_parity_established': False, 'full_runtime_1_to_1_established': False,
              'android_executed': executor is None, 'commands': [],
              'started_utc': datetime.now(timezone.utc).isoformat(), 'started_monotonic': time.monotonic()}
    call = subprocess.run if executor is None else executor
    def save():
        (args.output / 'animation-scales.json').write_text(json.dumps(report, indent=2) + '\n')
    try:
        if args.serial != SERIAL or not Path(report['adb']).is_file():
            raise EvidenceError('Exact disposable serial and existing ADB binary required')
        for number, (label, command, expected) in enumerate(specification(), 1):
            if time.monotonic() - report['started_monotonic'] >= 285:
                raise EvidenceError('No deadline remaining for another diagnostic command')
            argv = [report['adb'], '-s', SERIAL, *command]
            row = {'label': label, 'argv': argv, 'started_monotonic': time.monotonic(), 'timed_out': False}
            report['commands'].append(row)
            try:
                completed = call(argv, capture_output=True, timeout=15, check=False)
                code, stdout, stderr = completed.returncode, completed.stdout, completed.stderr
            except subprocess.TimeoutExpired as exc:
                code, stdout, stderr = 124, exc.stdout or b'', exc.stderr or b''
                row['timed_out'] = True
            row['exit_code'], row['finished_monotonic'] = code, time.monotonic()
            for stream, raw in [('stdout', stdout), ('stderr', stderr)]:
                name = f'{number:03d}-{label}.{stream}.txt'
                path = args.output / name
                path.write_bytes(raw)
                row[stream] = {'path': name, **digest(path)}
            save()
            if type(code) is not int or code != 0 or row['timed_out'] or stderr:
                raise EvidenceError('Device command failed: ' + label)
            validate_stdout(label, stdout, expected)
        report['finished_monotonic'] = time.monotonic()
        report['observed_scales'] = verify_report(args.output, report)
        report['status'] = ('ANIMATION_SCALE_ZERO_VERIFIED' if report['android_executed']
                            else 'SIMULATED_ANIMATION_SCALE_ZERO_VERIFIED')
        report['passed'] = True
    except (OSError, ValueError, KeyError, TypeError) as exc:
        report.update(status='ANIMATION_SCALE_DIAGNOSTIC_FAILED', passed=False, reason=str(exc),
                      finished_monotonic=time.monotonic())
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    save()
    return 0 if report['passed'] else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--adb', required=True)
    parser.add_argument('--serial', default=SERIAL, choices=[SERIAL])
    parser.add_argument('--output', type=Path, required=True)
    return run(parser.parse_args())


if __name__ == '__main__':
    raise SystemExit(main())
