#!/usr/bin/env python3
"""Eight pinned Widget method cases on real APK classes in AndroidRuntime.

The two app_process64 commands are bounded and use separate guest processes.
The helper installs no application, supplies no Context or nonempty widget list,
and requires verification to remain enabled. Host controls inject a simulated
runner explicitly; their reports cannot be accepted as Android execution.
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
CANDIDATE_SHA256 = 'b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f'
CANDIDATE_BYTES = 94_683_439
PROBE_SHA256 = '79bd3b46e71253b17ec75099cce3611df1735b8f74e8bdcb61c61e5a37ae1a07'
PROBE_BYTES = 7_580
PROVENANCE_SHA256 = '31e7ebb8bebaa12210d1486b87b864e9ed7cf9771dde4488ffe435dd4e434901'
PROBE_CLASS = 'Lrecovered/probe/WidgetMethodProbe;'
MAIN_CLASS = 'recovered.probe.WidgetMethodProbe'
TARGET = ('Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->'
          'm(Landroid/content/Context;Ljava/util/List;Lo73;)Ljava/lang/Object;')
ORIGINAL_METHOD_SHA256 = 'a1dd490bbfd6837fa72e6bf8ae4c75736612989fcba050fe2f0582aa03640e34'
HELPER_SHA256 = 'dbcb1a98d25ae4637531644da37d24f6e1bc494f941d4212da03c360fe315d79'
CASES = [
    'fresh-empty-unit-identity', 'reused-label-zero-empty', 'resumed-label-two-empty',
    'invalid-label-exact-exception', 'label-two-dead-cast-L7',
    'label-two-dead-cast-L4', 'label-two-dead-cast-L1', 'null-list-exception-type',
]
EXPECTED_LINES = ['WIDGET_ART_CASE_OK ' + case for case in CASES] + ['WIDGET_METHOD_ART_OK cases=8']
EXPECTED_STDOUT = '\n'.join(EXPECTED_LINES) + '\n'
APP_PROCESS = '/system/bin/app_process64'
GUEST_TIMEOUT = '/system/bin/timeout'
DEFAULT_AVD = 'MacroDroid_API35_Disposable'
EXPECTED_DEVICE = {
    'ro.kernel.qemu': '1',
    'sys.boot_completed': '1',
    'ro.build.version.sdk': '35',
    'ro.build.fingerprint': 'google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.043/12960925:userdebug/dev-keys',
    'ro.product.cpu.abi': 'x86_64',
    'ro.product.cpu.abilist': 'x86_64,arm64-v8a',
    'ro.dalvik.vm.native.bridge': 'libndk_translation.so',
    # AndroidRuntime parses this property after the explicit command-line options.
    'dalvik.vm.extra-opts': '',
}
REMOTE_PATTERN = r'/data/local/tmp/md-widget-method-[0-9a-f]{32}'
UNCLAIMED_FLAGS = [
    'full_runtime_1_to_1_established', 'nonempty_widget_behavior_verified',
    'widget_rendering_verified', 'app_apk_modified', 'app_installed',
    'app_ui_interaction', 'compile_only_stubs_on_classpath',
]
INPUT_SPECS = (
    ('probe', 'widget-method-probe.dex', PROBE_BYTES, PROBE_SHA256),
    ('original', 'original.apk', ORIGINAL_BYTES, ORIGINAL_SHA256),
    ('candidate', 'candidate.apk', CANDIDATE_BYTES, CANDIDATE_SHA256),
)


class ProbeError(ValueError):
    pass


def digest(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def stable_identity(path: Path) -> dict:
    before = path.stat()
    sha = digest(path)
    after = path.stat()
    if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
            after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns):
        raise ProbeError('Local input changed while being hashed: ' + str(path))
    return {'path': str(path.resolve()), 'bytes': after.st_size, 'sha256': sha}


def validate_probe(data: bytes) -> dict:
    if len(data) != PROBE_BYTES or hashlib.sha256(data).hexdigest() != PROBE_SHA256:
        raise ProbeError('Widget probe DEX differs from the exact compiled preparation')
    if data[:8] != b'dex\n035\x00' or struct.unpack_from('<II', data, 32) != (len(data), 112):
        raise ProbeError('Probe DEX header is invalid')
    if (struct.unpack_from('<I', data, 8)[0] != (zlib.adler32(data[12:]) & 0xffffffff) or
            data[12:32] != hashlib.sha1(data[32:]).digest()):
        raise ProbeError('Probe DEX internal checksums differ')
    strings, string_offset = struct.unpack_from('<II', data, 56)
    types, type_offset = struct.unpack_from('<II', data, 64)
    classes, class_offset = struct.unpack_from('<II', data, 96)
    if classes != 1 or class_offset + 32 > len(data):
        raise ProbeError('Probe must define exactly one runtime class')
    if string_offset + strings * 4 > len(data) or type_offset + types * 4 > len(data):
        raise ProbeError('Probe descriptor tables exceed the DEX')

    def descriptor(index):
        if index >= types:
            raise ProbeError('Probe type index is invalid')
        string_index = struct.unpack_from('<I', data, type_offset + index * 4)[0]
        if string_index >= strings:
            raise ProbeError('Probe string index is invalid')
        cursor = struct.unpack_from('<I', data, string_offset + string_index * 4)[0]
        for _ in range(5):
            if cursor >= len(data):
                raise ProbeError('Probe descriptor length exceeds the DEX')
            byte = data[cursor]
            cursor += 1
            if byte < 128:
                break
        else:
            raise ProbeError('Probe descriptor length is invalid')
        return data[cursor:data.index(b'\x00', cursor)].decode('ascii')

    owner = descriptor(struct.unpack_from('<I', data, class_offset)[0])
    if owner != PROBE_CLASS:
        raise ProbeError('Probe defines an unexpected class')
    references = sorted(descriptor(index) for index in range(types))
    for reference in references:
        base = reference.lstrip('[')
        if (base not in set('VZBSCIJFD') and base != PROBE_CLASS and not base.startswith('Ljava/') and
                base not in ('Ldalvik/annotation/Signature;', 'Ldalvik/annotation/Throws;')):
            raise ProbeError('Probe directly references an Android or application type: ' + reference)
    return {'bytes': PROBE_BYTES, 'sha256': PROBE_SHA256, 'runtime_class_count': 1,
            'runtime_class': owner, 'android_or_application_host_stub_definitions': 0,
            'direct_android_or_application_type_references': 0, 'type_references': references}


def validate_provenance(info: dict) -> None:
    if (not isinstance(info, dict) or info.get('main_class') != MAIN_CLASS or
            info.get('target_method') != TARGET or info.get('original_method_sha256') != ORIGINAL_METHOD_SHA256 or
            info.get('candidate_helper_sha256') != HELPER_SHA256 or
            info.get('runtime_cases') != CASES or info.get('expected_stdout_lines') != EXPECTED_LINES or
            info.get('android_runtime_executed_during_preparation') is not False):
        raise ProbeError('Probe provenance does not describe the frozen eight-case preparation')
    for key, _, size, expected in INPUT_SPECS:
        row = info['probe'] if key == 'probe' else info['apks'][key]
        if type(row.get('bytes')) is not int or row['bytes'] != size or row.get('sha256') != expected:
            raise ProbeError('Probe provenance contains another input identity: ' + key)
    row = info['probe']
    if (row.get('runtime_class') != PROBE_CLASS or row.get('runtime_class_count') != 1 or
            row.get('android_or_application_host_stub_definitions') != 0 or
            row.get('direct_android_or_application_type_references') != 0):
        raise ProbeError('Probe provenance contains additional runtime definitions or references')


def validate_inputs(original: Path, candidate: Path, probe: Path, provenance: Path) -> dict:
    paths = {'original': original, 'candidate': candidate, 'probe': probe}
    result = {}
    for key, _, size, expected in INPUT_SPECS:
        row = stable_identity(paths[key])
        if row['bytes'] != size or row['sha256'] != expected:
            raise ProbeError('Local input differs from the pinned comparison: ' + key)
        if key != 'probe':
            with zipfile.ZipFile(paths[key]) as apk:
                names = apk.namelist()
                if 'classes.dex' not in names or len(names) != len(set(names)):
                    raise ProbeError('APK classpath structure is invalid: ' + key)
        result[key] = row
    result['probe'].update(validate_probe(probe.read_bytes()))
    provenance_row = stable_identity(provenance)
    if provenance_row['sha256'] != PROVENANCE_SHA256:
        raise ProbeError('Probe provenance bytes differ from the frozen preparation')
    provenance_row['content'] = json.loads(provenance.read_text())
    validate_provenance(provenance_row['content'])
    result['provenance'] = provenance_row
    return result


def observed_hash(code, stdout: str, stderr: str, path: str, expected=None) -> str:
    match = re.fullmatch(r'([0-9a-f]{64})\s+' + re.escape(path) + r'\s*', stdout)
    if (type(code) is not int or code != 0 or stderr or not match or
            (expected is not None and match[1] != expected)):
        raise ProbeError('Device-side file identity differs or was not observed: ' + path)
    return match[1]


def observed_avd_name(stdout: bytes) -> None:
    """Require the exact pinned name and OK line with complete LF or CRLF lines."""
    expected = (DEFAULT_AVD + '\nOK\n').encode('ascii')
    if stdout not in (expected, expected.replace(b'\n', b'\r\n')):
        raise ProbeError('Selected emulator AVD output differs from the exact two-line protocol')


def observation(code, stdout: bytes, stderr: bytes, *, timed_out=False) -> dict:
    expected = EXPECTED_STDOUT.encode()
    lines = stdout.decode('utf-8', errors='replace').splitlines()
    prefix = []
    for index, case in enumerate(CASES):
        if index < len(lines) and lines[index] == EXPECTED_LINES[index]:
            prefix.append(case)
        else:
            break
    semantics = type(code) is int and code == 0 and not timed_out and stdout == expected
    return {'completed_case_prefix': prefix, 'completed_cases': len(prefix),
            'exact_stdout': stdout == expected, 'semantic_cases_passed': semantics,
            'stderr_empty': stderr == b'', 'diagnostic_bytes': len(stderr),
            'strict_command_passed': semantics and stderr == b''}


def guest_argv(remote: str, variant: str, timeout: int) -> list[str]:
    if not re.fullmatch(REMOTE_PATTERN, remote) or variant not in ('original', 'candidate'):
        raise ProbeError('Unexpected classpath selection')
    if type(timeout) is not int or not 30 <= timeout <= 180:
        raise ProbeError('Guest timeout must be an integer between 30 and 180 seconds')
    return [GUEST_TIMEOUT, '-s', 'KILL', str(timeout), APP_PROCESS, '-Xverify:all', '-cp',
            remote + '/widget-method-probe.dex:' + remote + '/' + variant + '.apk', remote, MAIN_CLASS]


def run_probe(args, *, runner=None) -> tuple[int, dict]:
    simulated = runner is not None
    runner = runner or subprocess.run
    output = args.output
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ProbeError('A new or empty output directory is required')
    output.mkdir(parents=True, exist_ok=True)
    report = {
        'schema_version': 1,
        'scope': 'Eight bounded Widget method entry/restoration/type-check cases in real original and candidate APK classes',
        'started_utc': datetime.now(timezone.utc).isoformat(), 'status': 'BLOCKED',
        'commands': [], 'serial': args.serial, 'expected_avd': args.avd,
        'guest_timeout_seconds': args.timeout, 'verification_mode': '-Xverify:all',
        'execution_backend': 'simulated-host-control' if simulated else 'adb-android-runtime',
        'android_runtime_executed': False, 'art_execution_attempted': False,
        'widget_cases_on_art_verified': False, 'both_semantic_case_sets_passed': False,
        'strict_diagnostics_passed': False, 'inputs_unchanged': False,
        'cleanup_complete': False, 'runtime_cases': CASES, 'expected_stdout': EXPECTED_STDOUT,
        'target_method': TARGET, 'executions': {},
        **{key: False for key in UNCLAIMED_FLAGS},
    }
    created = False
    remote = '/data/local/tmp/md-widget-method-' + uuid.uuid4().hex
    adb = None

    def checkpoint():
        temporary = output / 'probe-result.json.tmp'
        temporary.write_text(json.dumps(report, indent=2) + '\n')
        temporary.replace(output / 'probe-result.json')

    def artifact(name, value):
        data = value.encode() if isinstance(value, str) else value or b''
        (output / name).write_bytes(data)
        return {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

    def call(label, argv, timeout=15):
        number = len(report['commands']) + 1
        record = {'label': label, 'argv': argv, 'timeout_seconds': timeout,
                  'returncode': None, 'timed_out': False, 'started_utc': datetime.now(timezone.utc).isoformat()}
        report['commands'].append(record)
        started = time.monotonic()
        out = err = b''
        try:
            completed = runner(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=False)
            record['returncode'], out, err = completed.returncode, completed.stdout, completed.stderr
        except subprocess.TimeoutExpired as exc:
            record['timed_out'] = True
            out, err = exc.stdout or b'', exc.stderr or b''
        except OSError as exc:
            record['execution_error'] = str(exc)
        record['seconds'] = round(time.monotonic() - started, 3)
        record['stdout'] = artifact(f'{number:03d}-{label}.stdout.txt', out)
        record['stderr'] = artifact(f'{number:03d}-{label}.stderr.txt', err)
        checkpoint()
        return record, out, err

    def shell(label, argv, timeout=15):
        return call(label, [adb, '-s', args.serial, 'shell', shlex.join(argv)], timeout)

    def checked(value, label, *, allow_stderr=False):
        record, stdout, stderr = value
        if (type(record['returncode']) is not int or record['returncode'] != 0 or record['timed_out'] or
                (stderr and not allow_stderr)):
            raise ProbeError('Device command failed: ' + label)
        return stdout.decode('utf-8', errors='strict').strip()

    def file_hash(label, path, expected=None):
        record, out, err = shell(label, ['sha256sum', path])
        return observed_hash(record['returncode'], out.decode('utf-8', errors='strict'),
                             err.decode('utf-8', errors='strict'), path, expected)

    def environment(label):
        values = {key: checked(shell(label + '-' + key.replace('.', '-'), ['getprop', key]), key)
                  for key in EXPECTED_DEVICE}
        report[label] = values
        if values != EXPECTED_DEVICE:
            raise ProbeError('Device identity or late runtime options differ: ' + label)

    checkpoint()
    try:
        if not re.fullmatch(r'emulator-[0-9]+', args.serial) or args.avd != DEFAULT_AVD:
            raise ProbeError('An explicit pinned disposable emulator serial and AVD are required')
        guest_argv(remote, 'original', args.timeout)
        report['inputs_before'] = validate_inputs(args.original, args.candidate, args.probe, args.provenance)
        report['provenance_artifact'] = artifact('input-provenance.json', args.provenance.read_bytes())
        report['probe_artifact'] = artifact('input-probe.dex', args.probe.read_bytes())
        report['wrapper_artifact'] = artifact('executed-wrapper.py', Path(__file__).read_bytes())
        adb = shutil.which(args.adb)
        if not adb:
            raise ProbeError('ADB executable is unavailable')
        report['adb_path'], report['adb_sha256'] = adb, digest(Path(adb))
        if checked(call('device-state', [adb, '-s', args.serial, 'get-state']), 'device-state') != 'device':
            raise ProbeError('Selected emulator is unavailable or unauthorized')
        environment('environment-before')
        avd = call('avd-name', [adb, '-s', args.serial, 'emu', 'avd', 'name'])
        checked(avd, 'avd-name')
        observed_avd_name(avd[1])
        report['binaries_before'] = {}
        for name, path in (('app-process', APP_PROCESS), ('guest-timeout', GUEST_TIMEOUT)):
            checked(shell(name + '-executable', ['test', '-x', path]), name + '-executable')
            report['binaries_before'][name] = {'path': path, 'sha256': file_hash(name + '-sha256-before', path)}
        checked(shell('create-owned-directory', ['mkdir', '-m', '700', remote]), 'create-owned-directory')
        created = True
        report['owned_device_directory'] = remote
        report['device_inputs_before'] = {}
        for key, name, size, expected in INPUT_SPECS:
            local, destination = getattr(args, key), remote + '/' + name
            checked(call('push-' + key, [adb, '-s', args.serial, 'push', str(local.resolve()), destination], 120),
                    'push-' + key, allow_stderr=True)
            checked(shell('readonly-' + key, ['chmod', '444', destination]), 'readonly-' + key)
            if checked(shell('mode-' + key, ['stat', '-c', '%a', destination]), 'mode-' + key) != '444':
                raise ProbeError('Classpath file is not read-only: ' + key)
            report['device_inputs_before'][key] = {
                'path': destination, 'sha256': file_hash('sha256-before-' + key, destination, expected), 'mode': '444'}
        for variant in ('original', 'candidate'):
            environment('environment-before-' + variant)
            argv = guest_argv(remote, variant, args.timeout)
            report['art_execution_attempted'] = True
            checkpoint()
            record, out, err = shell('execute-' + variant, argv, args.timeout + 30)
            observed = observation(record['returncode'], out, err, timed_out=record['timed_out'])
            report['executions'][variant] = {'guest_argv': argv, 'command': record, **observed}
            if observed['completed_cases'] and not simulated:
                report['android_runtime_executed'] = True
            report['both_semantic_case_sets_passed'] = all(
                report['executions'].get(key, {}).get('semantic_cases_passed') is True
                for key in ('original', 'candidate'))
            report['widget_cases_on_art_verified'] = report['both_semantic_case_sets_passed'] and not simulated
            report['strict_diagnostics_passed'] = all(
                report['executions'].get(key, {}).get('stderr_empty') is True for key in ('original', 'candidate'))
            checkpoint()
            if not observed['strict_command_passed']:
                raise ProbeError('Exact Widget cases or clean diagnostics failed: ' + variant)
        report['status'] = 'SIMULATED_WIDGET_CASES_PASSED' if simulated else 'ART_WIDGET_CASES_VERIFIED'
    except (OSError, ValueError, KeyError, IndexError, struct.error, zipfile.BadZipFile) as exc:
        report['status'] = 'SIMULATED_WIDGET_PROBE_FAILED' if simulated else 'ART_WIDGET_PROBE_FAILED'
        report['reason'] = str(exc)
    finally:
        if created:
            # Preserve after-identities even when the guest fails or times out.
            # Postcheck failures do not erase the original command or its case prefix.
            report['postcheck_errors'] = []
            report['device_inputs_after'] = {}
            for key, name, _, expected in INPUT_SPECS:
                if key not in report.get('device_inputs_before', {}):
                    continue
                path = remote + '/' + name
                try:
                    report['device_inputs_after'][key] = {
                        'path': path, 'sha256': file_hash('sha256-after-' + key, path, expected)}
                except (OSError, ValueError) as exc:
                    report['postcheck_errors'].append(str(exc))
            report['binaries_after'] = {}
            for name, path in (('app-process', APP_PROCESS), ('guest-timeout', GUEST_TIMEOUT)):
                try:
                    report['binaries_after'][name] = {'path': path, 'sha256': file_hash(
                        name + '-sha256-after', path, report['binaries_before'][name]['sha256'])}
                except (OSError, ValueError) as exc:
                    report['postcheck_errors'].append(str(exc))
            try:
                environment('environment-after')
                report['inputs_after'] = validate_inputs(args.original, args.candidate, args.probe, args.provenance)
                report['inputs_unchanged'] = report['inputs_after'] == report['inputs_before']
                if (not report['inputs_unchanged'] or digest(Path(adb)) != report['adb_sha256'] or
                        digest(Path(__file__)) != report['wrapper_artifact']['sha256']):
                    raise ProbeError('Local input, wrapper or ADB identity changed during the probe')
            except (OSError, ValueError, KeyError, IndexError, struct.error, zipfile.BadZipFile) as exc:
                report['postcheck_errors'].append(str(exc))
            if report['postcheck_errors']:
                report['status'] = 'SIMULATED_WIDGET_POSTCHECK_FAILED' if simulated else 'ART_WIDGET_POSTCHECK_FAILED'
            try:
                checked(shell('remove-owned-directory', ['rm', '-rf', '--', remote]), 'remove-owned-directory')
                checked(shell('confirm-owned-directory-absent', ['test', '!', '-e', remote]),
                        'confirm-owned-directory-absent')
                report['cleanup_complete'] = True
            except (OSError, ValueError) as exc:
                report['cleanup_error'] = str(exc)
                if report['both_semantic_case_sets_passed']:
                    report['status'] = 'SIMULATED_WIDGET_CLEANUP_FAILED' if simulated else 'ART_WIDGET_CLEANUP_FAILED'
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        checkpoint()
    success = report['status'] in ('ART_WIDGET_CASES_VERIFIED', 'SIMULATED_WIDGET_CASES_PASSED')
    if success and report['cleanup_complete']:
        try:
            verify_result(output, report, serial=args.serial, allow_simulated=simulated)
        except ProbeError as exc:
            report['status'] = 'SIMULATED_WIDGET_EVIDENCE_INVALID' if simulated else 'ART_WIDGET_EVIDENCE_INVALID'
            report['evidence_error'] = str(exc)
            success = False
            checkpoint()
    return (0 if success and report['cleanup_complete'] else 2), report


def verify_result(folder: Path, report: dict, *, serial: str, allow_simulated=False) -> bool:
    """Independently bind every command and output of a successful completed run."""
    try:
        simulated = report.get('execution_backend') == 'simulated-host-control'
        if simulated and not allow_simulated:
            raise ProbeError('A simulated host result is not Android evidence')
        if report.get('execution_backend') != ('simulated-host-control' if simulated else 'adb-android-runtime'):
            raise ProbeError('Unknown execution backend')
        expected_status = 'SIMULATED_WIDGET_CASES_PASSED' if simulated else 'ART_WIDGET_CASES_VERIFIED'
        if (report.get('status') != expected_status or report.get('serial') != serial or
                not re.fullmatch(r'emulator-[0-9]+', serial) or report.get('expected_avd') != DEFAULT_AVD or
                report.get('verification_mode') != '-Xverify:all' or report.get('target_method') != TARGET or
                report.get('runtime_cases') != CASES or report.get('expected_stdout') != EXPECTED_STDOUT or
                any(report.get(key) is not False for key in UNCLAIMED_FLAGS) or
                any(report.get(key) is not True for key in ('art_execution_attempted', 'both_semantic_case_sets_passed',
                    'strict_diagnostics_passed', 'inputs_unchanged', 'cleanup_complete')) or
                report.get('postcheck_errors') != [] or
                report.get('widget_cases_on_art_verified') is not (not simulated) or
                report.get('android_runtime_executed') is not (not simulated)):
            raise ProbeError('A complete bounded result with its exact scope is required')
        remote, adb, timeout = report['owned_device_directory'], report['adb_path'], report['guest_timeout_seconds']
        guest_argv(remote, 'original', timeout)
        if not re.fullmatch(r'[0-9a-f]{64}', report['adb_sha256']):
            raise ProbeError('ADB binary hash is absent')
        if report['inputs_before'] != report['inputs_after']:
            raise ProbeError('Local inputs differ before and after execution')
        for key, name, size, expected in INPUT_SPECS:
            local = report['inputs_before'][key]
            if local.get('sha256') != expected or type(local.get('bytes')) is not int or local['bytes'] != size:
                raise ProbeError('Local input identity differs: ' + key)
            for phase in ('before', 'after'):
                value = report['device_inputs_' + phase][key]
                if value.get('path') != remote + '/' + name or value.get('sha256') != expected:
                    raise ProbeError('Device input identity differs: ' + key)
            if report['device_inputs_before'][key].get('mode') != '444':
                raise ProbeError('Device classpath file was writable')
        provenance = report['inputs_before']['provenance']
        if provenance.get('sha256') != PROVENANCE_SHA256:
            raise ProbeError('Provenance hash differs')
        validate_provenance(provenance['content'])
        for key, name, sha in (
                ('provenance_artifact', 'input-provenance.json', PROVENANCE_SHA256),
                ('probe_artifact', 'input-probe.dex', PROBE_SHA256),
                ('wrapper_artifact', 'executed-wrapper.py', digest(Path(__file__)))):
            row = report[key]
            if row.get('path') != name or (folder / name).is_symlink():
                raise ProbeError('Copied input evidence path differs')
            data = (folder / name).read_bytes()
            if (row.get('sha256') != sha or hashlib.sha256(data).hexdigest() != sha or
                    type(row.get('bytes')) is not int or row['bytes'] != len(data)):
                raise ProbeError('Copied input evidence bytes differ')
            if key == 'provenance_artifact' and json.loads(data) != provenance['content']:
                raise ProbeError('Reported provenance differs from its exact copied bytes')
            if key == 'probe_artifact':
                actual = validate_probe(data)
                if any(report['inputs_before']['probe'].get(k) != v for k, v in actual.items()):
                    raise ProbeError('Reported probe structure differs from actual DEX bytes')
        for name, path in (('app-process', APP_PROCESS), ('guest-timeout', GUEST_TIMEOUT)):
            before, after = report['binaries_before'][name], report['binaries_after'][name]
            if before != after or before.get('path') != path or not re.fullmatch(r'[0-9a-f]{64}', before['sha256']):
                raise ProbeError('Guest binary identity changed or is missing')

        expected = []

        def add(label, args, timeout=15, kind='empty', value=''):
            expected.append((label, [adb, '-s', serial, *args], timeout, kind, value))

        def shell(label, args, timeout=15, kind='empty', value=''):
            add(label, ['shell', shlex.join(args)], timeout, kind, value)

        def env(label):
            if report.get(label) != EXPECTED_DEVICE:
                raise ProbeError('Pinned Android environment differs: ' + label)
            for key, value in EXPECTED_DEVICE.items():
                shell(label + '-' + key.replace('.', '-'), ['getprop', key], kind='text', value=value)

        add('device-state', ['get-state'], kind='text', value='device')
        env('environment-before')
        add('avd-name', ['emu', 'avd', 'name'], kind='avd')
        for name, path in (('app-process', APP_PROCESS), ('guest-timeout', GUEST_TIMEOUT)):
            shell(name + '-executable', ['test', '-x', path])
            shell(name + '-sha256-before', ['sha256sum', path], kind='sha',
                  value=(path, report['binaries_before'][name]['sha256']))
        shell('create-owned-directory', ['mkdir', '-m', '700', remote])
        for key, name, _, sha in INPUT_SPECS:
            destination = remote + '/' + name
            add('push-' + key, ['push', report['inputs_before'][key]['path'], destination], 120, kind='push')
            shell('readonly-' + key, ['chmod', '444', destination])
            shell('mode-' + key, ['stat', '-c', '%a', destination], kind='text', value='444')
            shell('sha256-before-' + key, ['sha256sum', destination], kind='sha', value=(destination, sha))
        for variant in ('original', 'candidate'):
            env('environment-before-' + variant)
            argv = guest_argv(remote, variant, timeout)
            value = report['executions'][variant]
            if value.get('guest_argv') != argv:
                raise ProbeError('Widget command changed its verifier or classpath')
            shell('execute-' + variant, argv, timeout + 30, kind='execution', value=variant)
        for key, name, _, sha in INPUT_SPECS:
            shell('sha256-after-' + key, ['sha256sum', remote + '/' + name], kind='sha', value=(remote + '/' + name, sha))
        for name, path in (('app-process', APP_PROCESS), ('guest-timeout', GUEST_TIMEOUT)):
            shell(name + '-sha256-after', ['sha256sum', path], kind='sha', value=(path, report['binaries_before'][name]['sha256']))
        env('environment-after')
        shell('remove-owned-directory', ['rm', '-rf', '--', remote])
        shell('confirm-owned-directory-absent', ['test', '!', '-e', remote])
        if len(expected) != len(report['commands']):
            raise ProbeError('Command sequence contains missing or additional operations')
        paths = set()
        for number, (record, wanted) in enumerate(zip(report['commands'], expected), 1):
            label, argv, seconds, kind, value = wanted
            if (record.get('label') != label or record.get('argv') != argv or
                    type(record.get('timeout_seconds')) is not int or record['timeout_seconds'] != seconds or
                    type(record.get('returncode')) is not int or record['returncode'] != 0 or
                    record.get('timed_out') is not False or 'execution_error' in record):
                raise ProbeError('Command identity or result differs: ' + label)
            raw = {}
            for stream in ('stdout', 'stderr'):
                row = record[stream]
                path = f'{number:03d}-{label}.{stream}.txt'
                if row.get('path') != path or path in paths or (folder / path).is_symlink():
                    raise ProbeError('Command output path differs or is duplicated')
                paths.add(path)
                data = (folder / path).read_bytes()
                if type(row.get('bytes')) is not int or len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
                    raise ProbeError('Command output bytes differ: ' + path)
                raw[stream] = data
            if kind != 'push' and raw['stderr']:
                raise ProbeError('Command diagnostics are not empty: ' + label)
            stdout = raw['stdout'].decode('utf-8', errors='strict')
            if kind == 'empty' and stdout:
                raise ProbeError('Silent command produced unexpected output: ' + label)
            if kind == 'text' and stdout.strip() != value:
                raise ProbeError('Observed environment or state differs: ' + label)
            if kind == 'avd':
                observed_avd_name(raw['stdout'])
            if kind == 'sha':
                observed_hash(0, stdout, '', value[0], value[1])
            if kind == 'execution':
                observed = observation(0, raw['stdout'], raw['stderr'])
                if (report['executions'][value].get('command') != record or
                        any(report['executions'][value].get(key) != item for key, item in observed.items()) or
                        observed['strict_command_passed'] is not True):
                    raise ProbeError('Widget case observation differs from its raw command output')
        return True
    except ProbeError:
        raise
    except (OSError, ValueError, TypeError, KeyError, IndexError) as exc:
        raise ProbeError('Incomplete or malformed runtime evidence: ' + str(exc)) from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--adb', default='adb')
    parser.add_argument('--serial', required=True)
    parser.add_argument('--avd', default=DEFAULT_AVD, choices=[DEFAULT_AVD])
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--probe', type=Path, default=ROOT / 'probes/widget-method-probe.dex')
    parser.add_argument('--provenance', type=Path, default=ROOT / 'probes/widget-method-probe.json')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--timeout', type=int, default=120)
    args = parser.parse_args()
    code, report = run_probe(args)
    if code == 0:
        verify_result(args.output, report, serial=args.serial)
    print(json.dumps({'status': report['status'], 'output': str(args.output.resolve()),
                      'both_semantic_case_sets_passed': report['both_semantic_case_sets_passed'],
                      'strict_diagnostics_passed': report['strict_diagnostics_passed'],
                      'cleanup_complete': report['cleanup_complete']}, indent=2))
    return code


if __name__ == '__main__':
    sys.exit(main())
