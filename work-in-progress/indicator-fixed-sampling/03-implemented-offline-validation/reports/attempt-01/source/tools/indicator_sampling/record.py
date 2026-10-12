#!/usr/bin/env python3
"""Record eight fixed fresh installs and five unconditional frames after one NEXT.

The command/acquisition sequence derives from the pinned editor recorder. This
independent report never invokes its settling policy or changes a parent plan.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import time
import uuid

import common as c

SCALES = ['animator_duration_scale', 'window_animation_scale', 'transition_animation_scale']
PROPERTIES = ['ro.build.fingerprint', 'ro.build.version.sdk', 'ro.product.cpu.abilist',
              'ro.kernel.qemu', 'ro.dalvik.vm.native.bridge', 'persist.sys.locale', 'persist.sys.timezone']
SETTINGS = [('system', 'font_scale')] + [('global', key) for key in SCALES + [
    'airplane_mode_on', 'wifi_on', 'mobile_data', 'sysui_demo_allowed', 'sysui_tuner_demo_on']]


class Recorder:
    def __init__(self, folder, adb, parents, report, clock=c.now_ns, sleeper=time.sleep, executor=subprocess.run):
        self.folder = Path(folder).resolve()
        self.adb = str(Path(adb).resolve())
        self.parents = parents
        self.proof = parents['android_compare']
        self.runner = parents['editor_journey']
        self.report = report
        self.clock = clock
        self.sleeper = sleeper
        self.executor = executor
        self.deadline_ns = None

    def checkpoint(self):
        c.write_json(self.folder / 'journal.json', self.report)

    def save(self, name, data):
        c.canonical_name(name)
        started = self.clock()
        path = self.folder / name
        c.require(path.parent == self.folder, 'Raw capture files must be direct owned children')
        with path.open('xb') as stream:
            initial = c.stats(os.fstat(stream.fileno()))
            opened = self.clock()
            c.require(c.regular_one_link(initial) and initial['bytes'] == 0,
                      'New evidence file is not an exclusive empty regular file')
            stream.write(data)
            stream.flush()
            final = c.stats(os.fstat(stream.fileno()))
        closed = self.clock()
        c.require(c.stats(path.stat()) == final and c.regular_one_link(final),
                  'Evidence file changed during exclusive write')
        c.require((initial['device'], initial['inode']) == (final['device'], final['inode']),
                  'Evidence inode changed while writing')
        return {'path': name, **c.identity(data), 'creation': {
            'started_ns': started, 'opened_ns': opened, 'closed_ns': closed,
            'initial_stat': initial, 'final_stat': final,
        }}

    def command(self, argv, timeout=120):
        c.require(type(argv) is list and argv and all(type(x) is str for x in argv), 'Invalid ADB argv')
        started = self.clock()
        requested_timeout = timeout
        if self.deadline_ns is not None:
            timeout = min(timeout, (self.deadline_ns - started) / 1e9)
        c.require(timeout > 0, 'Enclosing command deadline expired')
        number = len(self.report['commands'])
        item = {'index': number, 'argv': argv, 'started_ns': started,
                'started_utc': c.utc(), 'timeout_seconds': timeout, 'timed_out': False,
                'requested_timeout_seconds': requested_timeout, 'enclosing_deadline_ns': self.deadline_ns}
        self.report['commands'].append(item)
        try:
            process = self.executor([self.adb, '-s', c.SERIAL, *argv], capture_output=True, timeout=timeout)
            code, out, err = process.returncode, process.stdout, process.stderr
        except subprocess.TimeoutExpired as error:
            code, out, err = None, error.stdout or b'', error.stderr or b''
            item['timed_out'] = True
        except OSError as error:
            code, out, err = None, b'', str(error).encode()
            item['error'] = str(error)
        item['subprocess_finished_ns'] = self.clock()
        item['returncode'] = code
        try:
            item['stdout'] = self.save(f'command-{number:05d}.stdout', out)
            item['stderr'] = self.save(f'command-{number:05d}.stderr', err)
        finally:
            item['record_finished_ns'] = self.clock()
            self.checkpoint()
        if item['timed_out'] or 'error' in item:
            raise c.Invalid('Device command failed; partial output retained')
        return number, out, err

    def shell(self, argv, timeout=120):
        return self.command(['shell', shlex.join(argv)], timeout)

    def checked(self, argv, timeout=120):
        index, out, err = self.shell(argv, timeout)
        c.require(self.report['commands'][index]['returncode'] == 0 and not err.strip(),
                  'Device command did not complete cleanly: ' + repr(argv))
        return index, out

    def wait(self, label, requested_ns, origin_ns):
        started = self.clock()
        target = origin_ns + requested_ns
        c.require(type(requested_ns) is int and requested_ns >= 0 and origin_ns <= started,
                  'Invalid fixed wait')
        c.require(self.deadline_ns is None or max(started, target) <= self.deadline_ns, 'Fixed wait exceeds the enclosing deadline')
        while True:
            remaining = target - self.clock()
            if remaining <= 0:
                break
            self.sleeper(remaining / 1e9)
        return {'label': label, 'origin_ns': origin_ns, 'started_ns': started, 'target_ns': target,
                'requested_ns': requested_ns, 'finished_ns': self.clock()}

    def environment(self):
        value, commands = {'serial': c.SERIAL}, []
        for key in PROPERTIES:
            index, out = self.checked(['getprop', key])
            commands.append(index)
            value[key] = out.decode().strip()
        for namespace, key in SETTINGS:
            index, out = self.checked(['settings', 'get', namespace, key])
            commands.append(index)
            value[namespace + ':' + key] = out.decode().strip()
        for key in ['size', 'density']:
            index, out = self.checked(['wm', key])
            commands.append(index)
            value['display_' + key] = out.decode().strip()
        return {'values': value, 'commands': commands}

    def scales(self):
        values, commands = {}, []
        for key in SCALES:
            index, out = self.checked(['settings', 'get', 'global', key])
            values[key] = out.decode().strip()
            commands.append(index)
        return {'values': values, 'commands': commands}

    def device_guard(self, scale, primary):
        """A fresh same-AVD, boot, modem and full environment read before removal."""
        value = {'started_ns': self.clock(), 'commands': {}}
        for name, argv in [('state', ['get-state']), ('avd', ['emu', 'avd', 'name']),
                           ('gsm', ['emu', 'gsm', 'status'])]:
            index, out, err = self.command(argv)
            value['commands'][name] = index
            c.require(self.report['commands'][index]['returncode'] == 0 and not err.strip(),
                      'Fresh emulator identity command failed')
            text = out.decode().strip()
            if name == 'state':
                c.require(text == 'device', 'The selected emulator is not ready')
            elif name == 'avd':
                c.require(text.splitlines() == [c.AVD, 'OK'], 'The disposable AVD identity changed')
            else:
                c.require(text.splitlines()[-1] == 'OK' and all(re.search(r'gsm ' + kind + r' state:\s*home\b', text)
                          for kind in ('voice', 'data')), 'Modem home registration changed')
        index, out = self.checked(['getprop', 'sys.boot_completed'])
        value['commands']['boot'] = index
        c.require(out.decode().strip() == '1', 'Framework boot is not complete')
        index, out = self.checked(['dumpsys', 'telephony.registry'])
        value['commands']['telephony'] = index
        signals = self.parents['radio'].primary_signals(out.decode())
        c.require(len(signals) == 1 and (signals[0]['primary'], signals[0]['level']) == (primary, 4),
                  'Configured primary radio or computed level changed')
        value['primary_signal'] = signals[0]
        value['environment'] = self.environment()
        c.require(value['environment']['values'] == c.expected_environment(scale),
                  'Fixed device environment changed before package removal')
        value['finished_ns'] = self.clock()
        return value

    def installed(self, digest):
        index, out, err = self.shell(['pm', 'path', c.PACKAGE])
        path = self.proof.installed_path(self.report['commands'][index]['returncode'], out.decode(), err.decode())
        hash_index, out, err = self.shell(['sha256sum', path])
        actual = self.proof.installed_digest(self.report['commands'][hash_index]['returncode'],
                                           out.decode(), err.decode(), path)
        c.require(actual == digest, 'Fresh installed APK checksum differs from its slot')
        return {'path_command': index, 'checksum_command': hash_index, 'path': path, 'sha256': actual}

    def observation(self, label, surface, expected_pid=None):
        started = self.clock()
        prior_deadline = self.deadline_ns
        self.deadline_ns = min(prior_deadline or started + 30_000_000_000, started + 30_000_000_000)
        value = {'label': label, 'surface': surface, 'status': 'INCOMPLETE', 'started_ns': started,
                 'commands': [], 'artifacts': {}}
        self.report.setdefault('observations', []).append(value)
        remote = '/data/local/tmp/md-indicator-' + uuid.uuid4().hex + '.xml'
        value['remote_xml'] = remote
        try:
            def capture(key, argv):
                index, data = self.checked(argv)
                value['commands'].append(index)
                value['artifacts'][key] = self.save(label + '-' + key + '.txt', data)
                return data
            first = capture('pid_first', ['pidof', c.PACKAGE])
            capture('foreground', ['dumpsys', 'activity', 'activities'])
            acquisition_error = None
            try:
                index, _ = self.checked(['uiautomator', 'dump', remote])
                value['commands'].append(index)
                index, xml, err = self.command(['exec-out', 'cat', remote])
                value['commands'].append(index)
                c.require(self.report['commands'][index]['returncode'] == 0 and not err.strip(), 'UI retrieval failed')
                value['artifacts']['hierarchy'] = self.save(label + '.xml', xml)
            except (ValueError, OSError, subprocess.SubprocessError) as error:
                acquisition_error = error
            finally:
                try:
                    index, _ = self.checked(['rm', '-f', remote])
                    value['commands'].append(index)
                except (ValueError, OSError, subprocess.SubprocessError) as error:
                    value['cleanup_error'] = str(error)
                    if acquisition_error is None:
                        acquisition_error = error
            if acquisition_error is not None:
                raise acquisition_error
            index, png, err = self.command(['exec-out', 'screencap', '-p'])
            value['commands'].append(index)
            c.require(self.report['commands'][index]['returncode'] == 0 and not err.strip(), 'PNG retrieval failed')
            value['artifacts']['screenshot'] = self.save(label + '.png', png)
            target = started + 1_050_000_000
            wait_start = self.clock()
            requested = max(0, target - wait_start)
            if requested:
                self.sleeper(requested / 1e9)
            value['minimum_live_interval_wait'] = {'started_ns': wait_start, 'target_ns': target,
                                                 'requested_ns': requested, 'finished_ns': self.clock()}
            capture('foreground_final', ['dumpsys', 'activity', 'activities'])
            capture('pid_final', ['pidof', c.PACKAGE])
            value['finished_ns'] = self.clock()
            validate_live_observation(self, value, expected_pid)
            value['status'] = 'RECORDED'
        except (ValueError, OSError, subprocess.SubprocessError) as error:
            value['reason'] = str(error)
            value['finished_ns'] = self.clock()
        finally:
            self.deadline_ns = prior_deadline
            value['record_artifact'] = self.save(label + '-observation.json', c.bytes_json(value))
            self.checkpoint()
            value['completed_ns'] = self.clock()
        c.require(value['status'] == 'RECORDED', 'Fixed observation failed: ' + value.get('reason', 'unknown'))
        return value


def validate_live_observation(recorder, value, expected_pid=None):
    artifacts = value['artifacts']
    raw = {name: (recorder.folder / row['path']).read_bytes() for name, row in artifacts.items()}
    pid = c.single_pid(raw['pid_first'].decode(), recorder.proof)
    c.require(c.single_pid(raw['pid_final'].decode(), recorder.proof) == pid
              and (expected_pid is None or pid == expected_pid), 'Main PID changed during this install slot')
    for key in ['foreground', 'foreground_final']:
        c.require(c.canonical_component(raw[key].decode(), recorder.proof) == c.INTRO,
                  'Expected IntroActivity left the foreground')
    c.surface_identity(raw['hierarchy'], value['surface'], recorder.parents)
    width, height, _ = recorder.parents['observed_journey'].png_pixels(raw['screenshot'], recorder.proof)
    c.require((width, height) == (720, 1280), 'Unexpected full-frame size')
    c.require(recorder.proof.valid_live_interval((value['finished_ns'] - value['started_ns']) / 1e9),
              'Invalid complete observation interval')
    value['pid'] = pid
    value['component'] = c.INTRO


def slot(recorder, spec, apk, entire_deadline, previous_scale, primary):
    begin = recorder.clock()
    record = {**spec, 'status': 'INCOMPLETE', 'started_ns': begin, 'samples': [], 'gaps': []}
    recorder.report['slot'] = record
    recorder.deadline_ns = min(entire_deadline, begin + 900_000_000_000)
    digest = (c.ORIGINAL if spec['apk'] == 'original' else c.CANDIDATE)['sha256']
    try:
        before = {'path': str(apk), 'started_ns': recorder.clock()}
        before.update(c.file_identity(apk), finished_ns=recorder.clock())
        record['local_apk_before'] = before
        c.require({key: before[key] for key in ('bytes', 'sha256')} == (c.ORIGINAL if spec['apk'] == 'original' else c.CANDIDATE),
                  'Local exact APK changed before removal')
        record['device_guard'] = recorder.device_guard(previous_scale, primary)
        record['uninstall'] = recorder.command(['uninstall', c.PACKAGE])[0]
        index, out, err = recorder.shell(['pm', 'path', c.PACKAGE])
        record['absence'] = index
        c.require(recorder.proof.absence_ok(recorder.report['commands'][index]['returncode'], out.decode(), err.decode()),
                  'Package absence after uninstall was not established')
        index, out, err = recorder.shell(['pidof', c.PACKAGE])
        record['pid_absence'] = index
        c.require(recorder.report['commands'][index]['returncode'] == 1 and not out.strip() and not err.strip(),
                  'Previous main process did not disappear')
        record['scale_before'] = recorder.scales()
        desired = {'animator_duration_scale': spec['animator_duration_scale'],
                   'window_animation_scale': '0', 'transition_animation_scale': '0'}
        record['scale_write'] = []
        for key in SCALES:
            index, out = recorder.checked(['settings', 'put', 'global', key, desired[key]])
            c.require(not out.strip(), 'Scale write returned unexpected output')
            record['scale_write'].append(index)
        record['scale_after_write'] = recorder.scales()
        c.require(record['scale_after_write']['values'] == desired, 'Requested scales were not observed')
        record['environment_before'] = recorder.environment()
        c.require(record['environment_before']['values'] == c.expected_environment(spec['animator_duration_scale']),
                  'Unexpected fixed device environment before install')
        index, out, err = recorder.command(['install', '--no-streaming', str(apk)], 600)
        record['install'] = index
        c.require(recorder.proof.install_ok(recorder.report['commands'][index]['returncode'], out.decode(), err.decode()),
                  'Fresh APK install failed')
        record['installed_initial'] = recorder.installed(digest)
        index, out = recorder.checked(['cmd', 'package', 'resolve-activity', '--brief', '-a',
                                      'android.intent.action.MAIN', '-c', 'android.intent.category.LAUNCHER', '-p', c.PACKAGE])
        record['resolve'] = index
        components = re.findall(re.escape(c.PACKAGE) + r'/[A-Za-z0-9_.$]+', out.decode())
        c.require(len(components) == 1, 'Ambiguous actual launcher')
        record['launcher'] = components[0]
        index, out, err = recorder.shell(['am', 'start', '-W', '-n', components[0]], 180)
        record['launch'] = index
        c.require(not err.strip() and recorder.proof.launch_ok(recorder.report['commands'][index]['returncode'], out.decode()),
                  'Activity launch failed')
        record['launch_wait'] = recorder.wait('post-launch', 4_000_000_000, recorder.report['commands'][index]['subprocess_finished_ns'])
        label = f'slot-{spec["index"]:02d}'
        record['initial'] = recorder.observation(label + '-initial', 'intro1')
        initial_pid = record['initial']['pid']
        guard_start = recorder.clock()
        slot_deadline = recorder.deadline_ns
        recorder.deadline_ns = min(slot_deadline, guard_start + 15_000_000_000)
        try:
            guard = {'started_ns': guard_start, 'installed': recorder.installed(digest), 'scales': recorder.scales()}
            record['preinput'] = guard
            c.require(guard['scales']['values'] == desired, 'Scale changed before input')
            guard['observation'] = recorder.observation(label + '-preinput', 'intro1', initial_pid)
            initial_xml = (recorder.folder / record['initial']['artifacts']['hierarchy']['path']).read_bytes()
            fresh_xml = (recorder.folder / guard['observation']['artifacts']['hierarchy']['path']).read_bytes()
            c.require(recorder.runner.canonical(recorder.runner.tree(initial_xml, c.PACKAGE))
                      == recorder.runner.canonical(recorder.runner.tree(fresh_xml, c.PACKAGE)),
                      'Complete initial/preinput hierarchies changed before the only input')
            index, out = recorder.checked(['pidof', c.PACKAGE])
            guard['immediate_pid'] = index
            c.require(c.single_pid(out.decode(), recorder.proof) == initial_pid, 'Main PID changed immediately before input')
            index, out = recorder.checked(['dumpsys', 'activity', 'activities'])
            guard['immediate_foreground'] = index
            c.require(c.canonical_component(out.decode(), recorder.proof) == c.INTRO,
                      'Component changed immediately before input')
            xml = (recorder.folder / guard['observation']['artifacts']['hierarchy']['path']).read_bytes()
            selector = {'resource-id': c.PACKAGE + ':id/button_next', 'content-desc': 'Next'}
            target = recorder.runner.target(xml, c.PACKAGE, selector, 720, 1280)
            c.require(target == [640, 1152], 'Observed NEXT target bounds changed')
            c.require(recorder.clock() - guard_start <= 15_000_000_000, 'Input precondition expired')
            index, out = recorder.checked(['input', 'tap', *map(str, target)])
            guard['tap'] = index
            c.require(not out.strip(), 'NEXT input returned unexpected output')
            guard['finished_ns'] = recorder.clock()
        finally:
            recorder.deadline_ns = slot_deadline
        record['input_wait'] = recorder.wait('post-input', 2_000_000_000,
                                             recorder.report['commands'][guard['tap']]['subprocess_finished_ns'])
        for sample in range(5):
            if sample:
                record['gaps'].append(recorder.wait('sample-gap-' + str(sample), 1_000_000_000,
                                                    record['samples'][-1]['completed_ns']))
            record['samples'].append(recorder.observation(label + '-sample-' + str(sample), 'intro2', initial_pid))
            recorder.checkpoint()
        record['installed_final'] = recorder.installed(digest)
        record['scale_final'] = recorder.scales()
        record['environment_after'] = recorder.environment()
        c.require(record['scale_final']['values'] == desired
                  and record['environment_after']['values'] == record['environment_before']['values'],
                  'Environment or scale changed during the fixed samples')
        after = {'path': str(apk), 'started_ns': recorder.clock()}
        after.update(c.file_identity(apk), finished_ns=recorder.clock())
        record['local_apk_after'] = after
        c.require({key: after[key] for key in ('bytes', 'sha256')} == (c.ORIGINAL if spec['apk'] == 'original' else c.CANDIDATE),
                  'Local exact APK changed during capture')
        record['status'] = 'COMPLETE'
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        record['reason'] = str(error)
        record['status'] = 'FAILED'
    finally:
        record['finished_ns'] = recorder.clock()
        recorder.deadline_ns = entire_deadline
        recorder.checkpoint()
    return record


def prerequisite_copy(output, runtime, device, toolchain):
    rows = []
    mapping = [(runtime / 'emulator-launch.json', 'prerequisites/emulator-launch.json'),
               (runtime / 'runtime-status.json', 'prerequisites/runtime-ready.json'),
               (toolchain, 'prerequisites/toolchain-inputs.json')]
    mapping += [(toolchain.parent / name, 'prerequisites/toolchain/' + name) for name in c.TOOL_METADATA]
    report = c.json_file(device / 'capture-device.json')
    mapping.append((device / 'capture-device.json', 'prerequisites/device/capture-device.json'))
    for entry in report['commands']:
        for stream in ('stdout', 'stderr'):
            name = entry[stream]['path']
            c.canonical_name(name)
            mapping.append((device / name, 'prerequisites/device/' + name))
    c.require(len({target for _, target in mapping}) == len(mapping), 'Repeated setup copy role')
    for source, name in mapping:
        c.require(source.is_file() and not source.is_symlink(), 'Missing actual setup evidence: ' + str(source))
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = source.read_bytes()
        with target.open('xb') as stream:
            stream.write(raw)
        rows.append({'path': name, **c.identity(raw)})
    return rows, report['confirmed_primary_signal']['primary']


def initialize(args):
    start = c.now_ns()
    import prepare
    from verify import verify_prerequisites
    prepared = prepare.verify_preparation(args.parents, args.source_root, args.prepared)
    parents = c.load_parents(args.parents)
    c.protocol()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    report = {'schema': 1, 'kind': 'FIXED_INDICATOR_DIAGNOSTIC_V1', 'id': uuid.uuid4().hex,
              'status': 'INITIALIZING', 'started_utc': c.utc(), 'started_ns': start,
              'deadline_ns': start + 7_200_000_000_000,
              'parent_commit': c.PARENT_COMMIT,
              'protocol_sha256': c.file_identity(c.HERE / 'protocol.json')['sha256'],
              'runtime_manifest_sha256': c.file_identity(c.HERE / 'runtime-files.json')['sha256'],
              'source_root': str(args.source_root.resolve()), 'parents': str(args.parents.resolve()),
              'prepared': str(args.prepared.resolve()), 'preparation_identity': c.file_identity(args.prepared / 'preparation.json'),
              'apks': prepared['apks'], 'tooling_root': str(args.tooling.resolve()),
              'adb': {'path': str(args.adb.resolve()), **c.file_identity(args.adb)},
              'slots': [], 'unattempted_indices': list(range(1, 9)), 'new_runtime_parity_credit': 0,
              'full_runtime_1_to_1_established': False, 'cause_established': False,
              'crash_free_run_established': False, 'app_apk_modified': False,
              'cross_app_frame_selection': False, 'masks_used': False}
    c.write_json(output / 'experiment.json', report)
    try:
        rows, primary = prerequisite_copy(output, args.runtime.resolve(), args.device.resolve(), args.toolchain_inputs.resolve())
        report.update(prerequisite_inputs=rows, primary_radio=primary)
        verify_prerequisites(output, report, parents)
        initial = {'schema': 1, 'status': 'INCOMPLETE', 'started_ns': start,
                   'experiment_id': report['id'], 'commands': []}
        folder = output / 'initialization'
        folder.mkdir()
        recorder = Recorder(folder, args.adb, parents, initial)
        recorder.deadline_ns = min(report['deadline_ns'], start + 240_000_000_000)
        try:
            initial['device_guard'] = recorder.device_guard('0', primary)
            initial['status'] = 'READY'
        finally:
            initial['finished_ns'] = c.now_ns()
            recorder.checkpoint()
            report['initialization'] = {'directory': 'initialization',
                                        'receipt': recorder.save('initialization.json', c.bytes_json(initial))}
        report['status'] = 'READY_FOR_FIXED_SLOTS'
    except Exception as error:
        report['status'] = 'FAILED_BEFORE_ANY_INSTALL'
        report['reason'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        report['updated_ns'] = c.now_ns()
        c.write_json(output / 'experiment.json', report)
    return report


def one_slot(args):
    invocation_start = c.now_ns()
    import prepare
    from verify import validate_prefix
    output = args.output.resolve()
    experiment = c.json_file(output / 'experiment.json')
    c.require(experiment.get('status') in ('READY_FOR_FIXED_SLOTS', 'FIXED_SLOTS_IN_PROGRESS'),
              'A failed, finished or uninitialized experiment cannot receive another install')
    policy = c.protocol()
    c.require(type(args.slot) is int and 1 <= args.slot <= 8 and args.slot == len(experiment['slots']) + 1,
              'Only the next fixed unattempted slot may be invoked; retries/reordering are forbidden')
    spec = policy['slots'][args.slot - 1]
    folder = output / f'slot-{args.slot:02d}'
    folder.mkdir(exist_ok=False)
    # Reserve this exact invocation before any further read/guard. A failed
    # preflight retains its owned slot folder and cannot be retried after repair.
    attempt = {'schema': 1, 'experiment_id': experiment['id'], 'slot': args.slot,
               'started_ns': invocation_start, 'status': 'PREFLIGHT_RUNNING'}
    c.write_json(folder / 'attempt.json', attempt)
    experiment['status'] = 'SLOT_INVOCATION_RESERVED'
    experiment['reserved_slot'] = args.slot
    experiment['unattempted_indices'] = list(range(args.slot + 1, 9))
    c.write_json(output / 'experiment.json', experiment)
    try:
        parents = c.load_parents(args.parents)
        prepare.verify_preparation(args.parents, args.source_root, args.prepared)
        c.require(experiment['preparation_identity'] == c.file_identity(args.prepared / 'preparation.json')
                  and experiment['source_root'] == str(args.source_root.resolve())
                  and experiment['parents'] == str(args.parents.resolve())
                  and experiment['prepared'] == str(args.prepared.resolve())
                  and experiment['adb'] == {'path': str(args.adb.resolve()), **c.file_identity(args.adb)},
                  'Executed source/preflight/ADB changed between slot invocations')
        validate_prefix(output, experiment, parents, live=True)
        c.require(invocation_start < c.now_ns() < experiment['deadline_ns'], 'Global experiment deadline expired')
        attempt['status'] = 'PREFLIGHT_VERIFIED'
        attempt['preflight_finished_ns'] = c.now_ns()
        c.write_json(folder / 'attempt.json', attempt)
    except Exception as error:
        attempt.update(status='PREFLIGHT_FAILED_NO_CONTINUATION', finished_ns=c.now_ns(),
                       reason=type(error).__name__ + ': ' + str(error))
        c.write_json(folder / 'attempt.json', attempt)
        experiment.update(status='FAILED_SLOT_PREFLIGHT_NO_CONTINUATION', failed_reserved_slot=args.slot,
                          reason=attempt['reason'], updated_ns=c.now_ns())
        c.write_json(output / 'experiment.json', experiment)
        raise
    report = {'schema': 1, 'status': 'INCOMPLETE', 'experiment_id': experiment['id'],
              'experiment_start_ns': experiment['started_ns'], 'global_deadline_ns': experiment['deadline_ns'],
              'runtime_manifest_sha256': experiment['runtime_manifest_sha256'],
              'started_ns': invocation_start, 'commands': [], 'observations': []}
    recorder = Recorder(folder, args.adb, parents, report)
    recorder.deadline_ns = min(experiment['deadline_ns'], invocation_start + 900_000_000_000)
    try:
        report['attempt'] = recorder.save('attempt-receipt.json', c.bytes_json(attempt))
        body = slot(recorder, spec, Path(experiment['apks'][spec['apk']]['path']),
                    recorder.deadline_ns, '0' if args.slot <= 5 else '1', experiment['primary_radio'])
        report['status'] = body['status']
    finally:
        report['finished_ns'] = c.now_ns()
        recorder.checkpoint()
        receipt = recorder.save('slot.json', c.bytes_json(report))
        experiment['slots'].append({'index': args.slot, 'directory': folder.name, 'receipt': receipt})
        experiment.pop('reserved_slot')
        experiment['unattempted_indices'] = list(range(args.slot + 1, 9))
        experiment['status'] = ('FIXED_SLOTS_IN_PROGRESS' if report['status'] == 'COMPLETE' else 'FAILED_SLOT_NO_CONTINUATION')
        experiment['updated_ns'] = c.now_ns()
        c.write_json(output / 'experiment.json', experiment)
    c.require(report['status'] == 'COMPLETE', 'Fixed slot failed; all remaining slots are unattempted')
    return report


def finish(args):
    from verify import verify_experiment
    import prepare
    output = args.output.resolve()
    experiment = c.json_file(output / 'experiment.json')
    parents = c.load_parents(args.parents)
    try:
        prepare.verify_preparation(args.parents, args.source_root, args.prepared)
        c.require(experiment['preparation_identity'] == c.file_identity(args.prepared / 'preparation.json'),
                  'Final preparation identity changed')
        experiment['live_inputs_verified_after_capture'] = True
    except Exception as error:
        experiment['live_inputs_verified_after_capture'] = False
        experiment['final_input_error'] = type(error).__name__ + ': ' + str(error)
    experiment['capture_finished_ns'] = c.now_ns()
    experiment['status'] = ('FIXED_CAPTURE_SCHEDULE_COMPLETE' if len(experiment['slots']) == 8
                            and experiment['status'] == 'FIXED_SLOTS_IN_PROGRESS' else 'FIXED_CAPTURE_SCHEDULE_INCOMPLETE')
    c.write_json(output / 'experiment.json', experiment)
    result = verify_experiment(output, experiment, parents, live=True, write_pairs=True)
    c.write_json(output / 'experiment.json', experiment)
    c.write_json(output / 'comparison.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parents', type=Path, required=True)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--prepared', type=Path, required=True)
    parser.add_argument('--adb', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--initialize', action='store_true')
    mode.add_argument('--slot', type=int)
    mode.add_argument('--finish', action='store_true')
    parser.add_argument('--runtime', type=Path)
    parser.add_argument('--device', type=Path)
    parser.add_argument('--toolchain-inputs', type=Path)
    parser.add_argument('--tooling', type=Path)
    parser.add_argument('--accept-package-data-removal', action='store_true')
    args = parser.parse_args()
    c.require(args.accept_package_data_removal, 'Explicit disposable-package data removal acceptance is required')
    if args.initialize:
        c.require(all(value is not None for value in (args.runtime, args.device, args.toolchain_inputs, args.tooling)),
                  'Owned runtime, actual device setup and toolchain evidence are required')
        result = initialize(args)
    elif args.slot is not None:
        result = one_slot(args)
    else:
        result = finish(args)
    print(json.dumps({key: result[key] for key in ('status', 'evidence_complete') if key in result}, indent=2))
    return 0 if result.get('evidence_complete', result.get('status') in ('READY_FOR_FIXED_SLOTS', 'COMPLETE')) else 2


if __name__ == '__main__':
    raise SystemExit(main())

