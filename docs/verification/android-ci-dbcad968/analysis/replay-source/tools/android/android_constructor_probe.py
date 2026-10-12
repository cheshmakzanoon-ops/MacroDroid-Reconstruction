#!/usr/bin/env python3
"""Run one pinned constructor-allocation DEX on a disposable Android 15 ART VM.

The unchanged original APK supplies the application classes on the classpath.
This helper installs no app, changes no app state, and makes no UI interaction.
Its result concerns only this constructor allocation, not application parity.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shlex
import shutil
import struct
import subprocess
import sys
import time
import uuid
import zipfile
import zlib

ROOT = Path(__file__).resolve().parent
ORIGINAL_SHA256 = '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'
ORIGINAL_BYTES = 95_725_918
PROBE_SHA256 = '85f53ad51a1a85fd2161bd485db9f12556f737b0745f6e26ffdff31a927d5281'
PROBE_BYTES = 1_436
PROBE_CLASS = 'Lrecovered/probe/ConstructorProbe;'
MAIN_CLASS = 'recovered.probe.ConstructorProbe'
EXPECTED_STDOUT = 'CONSTRUCTOR_ALLOCATION_OK class=zhh arity=2'
VM = '/apex/com.android.art/bin/dalvikvm64'
GUEST_TIMEOUT = '/system/bin/timeout'
DEFAULT_AVD = 'MacroDroid_API35_Disposable'
CHECKPOINT_PATH = 'work-in-progress/constructor-owner/02-pipeline-proof/checkpoint.json'
CHECKPOINT_SHA256 = '98d73cb9f3c73731e2a376bfdb446704674b2019e996a59483263f0d37b31e9a'
CHECKPOINT_COMMIT = 'c7abf086ebffbc70cb3143f909a7f48648de22bc'
EXPECTED_DEVICE = {
    'ro.kernel.qemu': '1',
    'sys.boot_completed': '1',
    'ro.build.version.sdk': '35',
    'ro.build.fingerprint': 'google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.043/12960925:userdebug/dev-keys',
    'ro.product.cpu.abi': 'x86_64',
    'ro.product.cpu.abilist': 'x86_64,arm64-v8a',
    'ro.dalvik.vm.native.bridge': 'libndk_translation.so',
}


class ProbeError(ValueError):
    pass


def digest(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def validate_probe(data: bytes) -> dict:
    if len(data) != PROBE_BYTES or hashlib.sha256(data).hexdigest() != PROBE_SHA256:
        raise ProbeError('Probe DEX does not match the pinned constructor proof')
    if data[:8] != b'dex\n035\x00' or struct.unpack_from('<II', data, 32) != (len(data), 112):
        raise ProbeError('Probe DEX header is invalid')
    if (struct.unpack_from('<I', data, 8)[0] != (zlib.adler32(data[12:]) & 0xffffffff) or
            data[12:32] != hashlib.sha1(data[32:]).digest()):
        raise ProbeError('Probe DEX internal checksums differ')
    classes, offset = struct.unpack_from('<II', data, 96)
    if classes != 1 or offset + 32 > len(data):
        raise ProbeError('Probe must contain exactly one runtime class')
    class_index = struct.unpack_from('<I', data, offset)[0]
    type_count, type_offset = struct.unpack_from('<II', data, 64)
    string_count, string_offset = struct.unpack_from('<II', data, 56)
    if class_index >= type_count:
        raise ProbeError('Probe class type index is invalid')
    descriptor_index = struct.unpack_from('<I', data, type_offset + 4 * class_index)[0]
    if descriptor_index >= string_count:
        raise ProbeError('Probe descriptor index is invalid')
    cursor = struct.unpack_from('<I', data, string_offset + 4 * descriptor_index)[0]
    for _ in range(5):
        byte = data[cursor]
        cursor += 1
        if byte < 128:
            break
    else:
        raise ProbeError('Probe descriptor length is invalid')
    descriptor = data[cursor:data.index(b'\x00', cursor)].decode('ascii')
    if descriptor != PROBE_CLASS:
        raise ProbeError('Probe contains an unexpected runtime class')
    return {'bytes': len(data), 'sha256': PROBE_SHA256, 'runtime_class_count': classes,
            'runtime_class': descriptor, 'compile_only_stub_classes_in_probe': 0}


def validate_inputs(original: Path, probe: Path, provenance: Path) -> dict:
    if not original.is_file() or original.stat().st_size != ORIGINAL_BYTES or digest(original) != ORIGINAL_SHA256:
        raise ProbeError('Original APK does not match the supplied comparison target')
    with zipfile.ZipFile(original) as apk:
        names = apk.namelist()
        if 'classes.dex' not in names or len(names) != len(set(names)):
            raise ProbeError('Original APK classpath structure is invalid')
    checked_probe = validate_probe(probe.read_bytes())
    info = json.loads(provenance.read_text())
    if not isinstance(info, dict) or not isinstance(info.get('constructor_checkpoint'), dict):
        raise ProbeError('Probe provenance must identify its frozen constructor checkpoint')
    if (info.get('probe_sha256') != PROBE_SHA256 or
            type(info.get('probe_bytes')) is not int or info.get('probe_bytes') != PROBE_BYTES or
            info.get('original_apk_sha256') != ORIGINAL_SHA256 or info.get('main_class') != MAIN_CLASS or
            info.get('constructor_checkpoint', {}).get('repository_path') != CHECKPOINT_PATH or
            info.get('constructor_checkpoint', {}).get('manifest_sha256') != CHECKPOINT_SHA256 or
            info.get('constructor_checkpoint', {}).get('commit') != CHECKPOINT_COMMIT):
        raise ProbeError('Probe provenance differs from the pinned runtime inputs')
    return {'original': {'path': str(original.resolve()), 'bytes': ORIGINAL_BYTES, 'sha256': ORIGINAL_SHA256},
            'probe': {'path': str(probe.resolve()), **checked_probe},
            'provenance': {'path': str(provenance.resolve()), 'sha256': digest(provenance), 'content': info}}


def observed_hash(code: int, stdout: str, stderr: str, path: str, expected: str) -> str:
    match = re.fullmatch(r'([0-9a-f]{64})\s+' + re.escape(path) + r'\s*', stdout)
    if type(code) is not int or code != 0 or stderr.strip() or not match or match[1] != expected:
        raise ProbeError('Device-side file identity does not match the pinned input')
    return match[1]


def successful_output(code: int, stdout: str, stderr: str) -> bool:
    if type(code) is not int or code != 0 or stdout.splitlines() != [EXPECTED_STDOUT]:
        return False
    return not re.search(r'\b(?:[\w.$]*(?:Error|Exception)|FATAL)\b|verification failed', stderr, re.I)


def run_probe(args, *, runner=None) -> tuple[int, dict]:
    runner = runner or subprocess.run
    output = args.output
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ProbeError('A new or empty probe output directory is required')
    output.mkdir(parents=True, exist_ok=True)
    report = {'schema_version': 1, 'scope': 'Pinned Lzhh allocation through Lrff constructor on Android 15 ART only',
              'started_utc': datetime.now(timezone.utc).isoformat(), 'status': 'BLOCKED', 'commands': [],
              'art_execution_attempted': False, 'android_runtime_executed': False,
              'constructor_allocation_on_art_verified': False, 'full_runtime_1_to_1_established': False,
              'widget_behavior_verified': False, 'app_apk_modified': False, 'app_installed': False,
              'app_ui_interaction': False, 'compile_only_stubs_on_classpath': False,
              'probe_sha256': PROBE_SHA256, 'original_apk_sha256': ORIGINAL_SHA256,
              'serial': args.serial, 'expected_avd': args.avd, 'expected_stdout': EXPECTED_STDOUT,
              'guest_timeout_seconds': args.timeout, 'verification_mode': '-Xverify:all',
              'cleanup_complete': False}
    created = False
    remote = '/data/local/tmp/md-constructor-' + uuid.uuid4().hex
    adb = None

    def checkpoint():
        temporary = output / 'probe-result.json.tmp'
        temporary.write_text(json.dumps(report, indent=2) + '\n')
        temporary.replace(output / 'probe-result.json')

    def artifact(name, data):
        data = data.encode() if isinstance(data, str) else (data or b'')
        (output / name).write_bytes(data)
        return {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

    def call(label, argv, timeout=15):
        started = time.monotonic()
        number = len(report['commands']) + 1
        record = {'label': label, 'argv': argv, 'started_utc': datetime.now(timezone.utc).isoformat(),
                  'timeout_seconds': timeout, 'returncode': None, 'timed_out': False}
        report['commands'].append(record)
        stdout = stderr = b''
        error = None
        try:
            completed = runner(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=False)
            stdout, stderr = completed.stdout, completed.stderr
            record['returncode'] = completed.returncode
        except subprocess.TimeoutExpired as exc:
            stdout, stderr = exc.stdout, exc.stderr
            record['timed_out'] = True
            error = ProbeError('Timed out: ' + label)
        except OSError as exc:
            error = ProbeError('Could not execute ' + label + ': ' + str(exc))
        record['seconds'] = round(time.monotonic() - started, 3)
        record['stdout'] = artifact(f'{number:03d}-{label}.stdout.txt', stdout)
        record['stderr'] = artifact(f'{number:03d}-{label}.stderr.txt', stderr)
        checkpoint()
        if error:
            raise error
        out = stdout.decode('utf-8', errors='replace') if isinstance(stdout, bytes) else stdout
        err = stderr.decode('utf-8', errors='replace') if isinstance(stderr, bytes) else stderr
        return completed.returncode, out or '', err or '', record

    def shell(label, argv, timeout=15):
        return call(label, [adb, '-s', args.serial, 'shell', shlex.join(argv)], timeout)

    def checked(value, label, *, allow_stderr=False):
        code, stdout, stderr, _ = value
        if type(code) is not int or code != 0 or (stderr.strip() and not allow_stderr):
            raise ProbeError('Device command failed: ' + label)
        return stdout.strip()

    checkpoint()
    try:
        if not re.fullmatch(r'emulator-[0-9]+', args.serial):
            raise ProbeError('Only an explicitly selected disposable emulator is supported')
        report['inputs'] = validate_inputs(args.original, args.probe, args.provenance)
        adb = shutil.which(args.adb)
        if not adb:
            raise ProbeError('ADB executable is unavailable')
        report['adb_path'] = adb
        report['adb_sha256'] = digest(Path(adb))
        state = call('device-state', [adb, '-s', args.serial, 'get-state'])
        if checked(state, 'device-state') != 'device':
            raise ProbeError('Selected emulator is unavailable or unauthorized')
        environment = {}
        for key in EXPECTED_DEVICE:
            environment[key] = checked(shell('property-' + key.replace('.', '-'), ['getprop', key]), key)
        report['environment'] = environment
        if environment != EXPECTED_DEVICE:
            raise ProbeError('Device properties differ from the booted, pinned Android 15 emulator')
        avd = checked(call('avd-name', [adb, '-s', args.serial, 'emu', 'avd', 'name']), 'avd-name')
        if avd.splitlines() != [args.avd, 'OK']:
            raise ProbeError('Selected emulator AVD name differs from the disposable runtime')
        checked(shell('art-executable', ['test', '-x', VM]), 'art-executable')
        checked(shell('guest-timeout-executable', ['test', '-x', GUEST_TIMEOUT]), 'guest-timeout-executable')
        binary_output = checked(shell('art-binary-sha256', ['sha256sum', VM]), 'art-binary-sha256')
        binary_match = re.fullmatch(r'([0-9a-f]{64})\s+' + re.escape(VM), binary_output)
        if not binary_match:
            raise ProbeError('ART binary identity was not observed')
        report['art_binary_sha256'] = binary_match[1]
        if not re.fullmatch(r'/data/local/tmp/md-constructor-[0-9a-f]{32}', remote):
            raise ProbeError('Generated temporary path is invalid')
        checked(shell('create-owned-directory', ['mkdir', '-m', '700', remote]), 'create-owned-directory')
        created = True
        report['owned_device_directory'] = remote
        identities = {}
        for key, local, name, expected in [('probe', args.probe, 'constructor-probe.dex', PROBE_SHA256),
                                          ('original', args.original, 'original.apk', ORIGINAL_SHA256)]:
            destination = remote + '/' + name
            checked(call('push-' + key, [adb, '-s', args.serial, 'push', str(local.resolve()), destination], 120),
                    'push-' + key, allow_stderr=True)
            checked(shell('readonly-' + key, ['chmod', '444', destination]), 'readonly-' + key)
            mode = checked(shell('mode-' + key, ['stat', '-c', '%a', destination]), 'mode-' + key)
            if mode != '444':
                raise ProbeError('Pushed classpath file is not read-only')
            measured = shell('sha256-' + key, ['sha256sum', destination])
            identities[key] = {'path': destination, 'sha256': observed_hash(*measured[:3], destination, expected), 'mode': mode}
        report['device_inputs'] = identities
        argv = [GUEST_TIMEOUT, '-s', 'KILL', str(args.timeout), VM, '-Xverify:all', '-cp',
                identities['probe']['path'] + ':' + identities['original']['path'], MAIN_CLASS]
        report['art_argv'] = argv
        report['art_execution_attempted'] = True
        checkpoint()
        record_index = len(report['commands'])
        try:
            code, stdout, stderr, record = shell('execute-constructor-probe', argv, args.timeout + 30)
        finally:
            if len(report['commands']) > record_index:
                report['art_command'] = report['commands'][record_index]
        report['android_runtime_executed'] = (EXPECTED_STDOUT in stdout.splitlines() or
            bool(re.search(r'\b(?:VerifyError|NoClassDefFoundError|ClassNotFoundException|NoSuchMethodError)\b', stderr)))
        if not successful_output(code, stdout, stderr):
            raise ProbeError('ART did not report the exact successful constructor allocation')
        report['constructor_allocation_on_art_verified'] = True
        report['status'] = 'ART_CONSTRUCTOR_ALLOCATION_VERIFIED'
    except (OSError, ValueError, KeyError, IndexError, struct.error, zipfile.BadZipFile) as exc:
        report['status'] = 'ART_CONSTRUCTOR_PROBE_FAILED'
        report['reason'] = str(exc)
    finally:
        if created:
            try:
                checked(shell('remove-owned-directory', ['rm', '-rf', '--', remote]), 'remove-owned-directory')
                checked(shell('confirm-owned-directory-absent', ['test', '!', '-e', remote]), 'confirm-owned-directory-absent')
                report['cleanup_complete'] = True
            except (OSError, ValueError) as exc:
                report['cleanup_error'] = str(exc)
                if report['constructor_allocation_on_art_verified']:
                    report['status'] = 'ART_CONSTRUCTOR_VERIFIED_CLEANUP_FAILED'
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        checkpoint()
    return (0 if report['status'] == 'ART_CONSTRUCTOR_ALLOCATION_VERIFIED' else 2), report


def _verify_result(folder: Path, report: dict, *, serial: str) -> bool:
    """Recheck a completed allocation result and its exact command artifacts.

    Cleanup is a separate gate: an observed allocation remains observed if the
    helper later reports a cleanup failure. A CI success must require both.
    """
    if (report.get('status') not in ('ART_CONSTRUCTOR_ALLOCATION_VERIFIED', 'ART_CONSTRUCTOR_VERIFIED_CLEANUP_FAILED') or
            any(report.get(k) is not True for k in ['art_execution_attempted', 'android_runtime_executed',
                                                   'constructor_allocation_on_art_verified']) or
            report.get('serial') != serial or report.get('expected_avd') != DEFAULT_AVD or
            report.get('environment') != EXPECTED_DEVICE or report.get('verification_mode') != '-Xverify:all' or
            report.get('probe_sha256') != PROBE_SHA256 or report.get('original_apk_sha256') != ORIGINAL_SHA256):
        raise ProbeError('A complete allocation result on the selected pinned emulator is required')
    if any(not re.fullmatch(r'[0-9a-f]{64}', report.get(k, '')) for k in ['art_binary_sha256', 'adb_sha256']):
        raise ProbeError('ART or ADB binary hash is missing')
    remote = report['owned_device_directory']
    if not re.fullmatch(r'/data/local/tmp/md-constructor-[0-9a-f]{32}', remote):
        raise ProbeError('Unexpected device probe directory')
    for key, name, size, expected in [('probe', 'constructor-probe.dex', PROBE_BYTES, PROBE_SHA256),
                                      ('original', 'original.apk', ORIGINAL_BYTES, ORIGINAL_SHA256)]:
        local, device = report['inputs'][key], report['device_inputs'][key]
        if (local.get('sha256') != expected or type(local.get('bytes')) is not int or local['bytes'] != size or
                device != {'path': remote + '/' + name, 'sha256': expected, 'mode': '444'}):
            raise ProbeError('Probe result input identities are inconsistent')
    provenance = report['inputs']['provenance']['content']
    if (provenance.get('probe_sha256') != PROBE_SHA256 or provenance.get('original_apk_sha256') != ORIGINAL_SHA256 or
            provenance.get('constructor_checkpoint', {}).get('repository_path') != CHECKPOINT_PATH or
            provenance.get('constructor_checkpoint', {}).get('manifest_sha256') != CHECKPOINT_SHA256 or
            provenance.get('constructor_checkpoint', {}).get('commit') != CHECKPOINT_COMMIT):
        raise ProbeError('Probe result does not refer to the frozen constructor proof')
    seconds = report['guest_timeout_seconds']
    if type(seconds) is not int or not 1 <= seconds <= 300:
        raise ProbeError('Probe result guest timeout is invalid')
    expected_argv = [GUEST_TIMEOUT, '-s', 'KILL', str(seconds), VM, '-Xverify:all', '-cp',
                     remote + '/constructor-probe.dex:' + remote + '/original.apk', MAIN_CLASS]
    command = report['art_command']
    if (report.get('art_argv') != expected_argv or not Path(report['adb_path']).is_absolute() or
            command.get('argv') != [report['adb_path'], '-s', serial, 'shell', shlex.join(expected_argv)] or
            command.get('label') != 'execute-constructor-probe' or command.get('timed_out') is not False or
            type(command.get('returncode')) is not int or command['returncode'] != 0):
        raise ProbeError('Probe result does not record the required verified ART invocation')
    outputs = []
    for key in ['stdout', 'stderr']:
        reference = command[key]
        relative = Path(reference['path'])
        path = folder / relative
        if (relative.is_absolute() or len(relative.parts) != 1 or path.is_symlink() or
                path.resolve().parent != folder.resolve()):
            raise ProbeError('Probe command artifact path escapes its result directory')
        data = path.read_bytes()
        if (type(reference.get('bytes')) is not int or len(data) != reference['bytes'] or
                hashlib.sha256(data).hexdigest() != reference.get('sha256')):
            raise ProbeError('Probe command artifact differs from its recorded identity')
        outputs.append(data.decode('utf-8', errors='replace'))
    if not successful_output(command['returncode'], *outputs):
        raise ProbeError('Probe command artifacts do not establish the exact allocation result')
    return True


def verify_result(folder: Path, report: dict, *, serial: str) -> bool:
    try:
        return _verify_result(folder, report, serial=serial)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError) as exc:
        raise ProbeError(str(exc)) from exc


def bounded_timeout(value: str) -> int:
    try:
        seconds = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError('Timeout must be an integer') from exc
    if not 1 <= seconds <= 300:
        raise argparse.ArgumentTypeError('Timeout must be between 1 and 300 seconds')
    return seconds


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--adb', default='adb')
    parser.add_argument('--serial', required=True)
    parser.add_argument('--avd', default=DEFAULT_AVD)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--probe', type=Path, default=ROOT / 'probes/constructor-probe.dex')
    parser.add_argument('--provenance', type=Path, default=ROOT / 'probes/constructor-probe.json')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--timeout', type=bounded_timeout, default=120)
    args = parser.parse_args()
    try:
        code, result = run_probe(args)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return code


if __name__ == '__main__':
    sys.exit(main())
