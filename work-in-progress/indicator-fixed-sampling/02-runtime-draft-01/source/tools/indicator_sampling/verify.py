#!/usr/bin/env python3
"""Independently verify fixed capture provenance and all predetermined pairs.

Evidence completeness has no equality requirement. Every full-frame difference
is retained losslessly. ZIP replay checks saved bytes and the host's serialized
identity records; it does not claim extracted inode/ctime values are host values.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import re
import shlex
import struct

import common as c

SCALES = ('animator_duration_scale', 'window_animation_scale', 'transition_animation_scale')
PROPERTIES = ('ro.build.fingerprint', 'ro.build.version.sdk', 'ro.product.cpu.abilist',
              'ro.kernel.qemu', 'ro.dalvik.vm.native.bridge', 'persist.sys.locale', 'persist.sys.timezone')
SETTINGS = [('system', 'font_scale')] + [('global', key) for key in SCALES + (
    'airplane_mode_on', 'wifi_on', 'mobile_data', 'sysui_demo_allowed', 'sysui_tuner_demo_on')]
DIFF = struct.Struct('>I4s4s')


def verify_prerequisites(root, experiment, parents):
    """Literal runtime identity and every raw parent setup command are retained."""
    root = Path(root).resolve()
    inventory = experiment['prerequisite_inputs']
    c.require(type(inventory) is list and len({row['path'] for row in inventory}) == len(inventory),
              'Prerequisite inventory has repeated roles')
    actual_names = set()
    for row in inventory:
        path = c.checked_path(root, row['path'])
        c.require(c.file_identity(path) == {key: row[key] for key in ('bytes', 'sha256')},
                  'Prerequisite bytes changed: ' + row['path'])
        actual_names.add(row['path'])
    launch = c.json_file(root / 'prerequisites/emulator-launch.json')
    ready = c.json_file(root / 'prerequisites/runtime-ready.json')
    tooling = Path(experiment['tooling_root'])
    adb = str(tooling / 'android/platform-tools/adb')
    command = [str(tooling / 'android/emulator/emulator'), '-avd', c.AVD, '-port', '5560',
               '-no-window', '-no-audio', '-no-boot-anim', '-no-snapshot', '-accel', 'on',
               '-gpu', 'swiftshader', '-cores', '2', '-memory', '3072',
               '-camera-back', 'none', '-camera-front', 'none']
    for value in (launch, ready):
        c.require(value['serial'] == c.SERIAL and value['adb_path'] == adb and value['avd'] == c.AVD
                  and value['command'] == command and value['ram_mb'] == 3072
                  and value['virtual_cores'] == 2 and value['acceleration'] == 'on',
                  'The owned disposable emulator launch changed')
    c.require(launch['state'] == 'booting' and ready['state'] == 'ready'
              and ready['started_utc'] == launch['started_utc'] and ready['adb_exit_code'] == 0,
              'Actual same-launch readiness is absent')
    props = ready['properties']
    for key, expected in {'sys.boot_completed': '1', 'ro.build.version.sdk': '35',
                          'ro.build.fingerprint': c.FINGERPRINT, 'ro.product.cpu.abilist': 'x86_64,arm64-v8a',
                          'ro.dalvik.vm.native.bridge': 'libndk_translation.so'}.items():
        c.require(props.get(key) == expected, 'Required ready property differs: ' + key)
    binaries = c.json_file(root / 'prerequisites/toolchain-inputs.json')
    rows = [row for row in binaries if row['path'] == 'android/platform-tools/adb']
    c.require(len(rows) == 1 and experiment['adb'] == {'path': adb, **{key: rows[0][key] for key in ('bytes', 'sha256')}},
              'Executed ADB differs from the pinned bootstrap output observation')
    device = c.json_file(root / 'prerequisites/device/capture-device.json')
    c.require(device.get('status') == 'CAPTURE_DEVICE_CONFIGURED' and device.get('serial') == c.SERIAL
              and device.get('expected_avd') == c.AVD and device.get('requested_signal_profile') == 4
              and device.get('required_stable_seconds') == 15
              and device.get('signal_stability_fields') == ['primary', 'level']
              and device.get('demo_clock_requested') == '1200'
              and device.get('disable_animations_requested') is True
              and device.get('requested_animation_scales_observed') is True
              and device.get('systemui_demo_mode_observed') is True
              and device.get('animation_scales_requested') == dict.fromkeys(SCALES, '0'),
              'Actual radio/demo/initial-scale configuration is incomplete')
    fixed = {
        'emulator-check': ['shell', 'getprop', 'ro.kernel.qemu'],
        'boot-check': ['shell', 'getprop', 'sys.boot_completed'],
        'avd-name': ['emu', 'avd', 'name'],
        'signal-profile-help': ['emu', 'help', 'gsm', 'signal-profile'],
        'voice-home': ['emu', 'gsm', 'voice', 'home'], 'data-home': ['emu', 'gsm', 'data', 'home'],
        'signal-profile-four': ['emu', 'gsm', 'signal-profile', '4'],
        'telephony': ['shell', 'dumpsys', 'telephony.registry'],
        'confirmed-gsm': ['emu', 'gsm', 'status'],
        'allow-demo': ['shell', 'settings', 'put', 'global', 'sysui_demo_allowed', '1'],
        'start-demo': ['shell', 'settings', 'put', 'global', 'sysui_tuner_demo_on', '1'],
        'demo-controller': ['shell', 'dumpsys', 'activity', 'service',
                            'com.android.systemui/.SystemUIService', 'DemoModeController'],
        'demo-clock': ['shell', 'am', 'broadcast', '-a', 'com.android.systemui.demo',
                       '-e', 'command', 'clock', '-e', 'hhmm', '1200'],
    }
    observation_order = []
    for moment in ('before', 'after'):
        entries = [('gsm', ['emu', 'gsm', 'status']), ('power', ['emu', 'power', 'display']),
            ('battery', ['shell', 'dumpsys', 'battery']), ('clock', ['shell', 'date', '-u', '+%Y-%m-%dT%H:%M:%SZ']),
            ('demo-allowed', ['shell', 'settings', 'get', 'global', 'sysui_demo_allowed']),
            ('demo-on', ['shell', 'settings', 'get', 'global', 'sysui_tuner_demo_on'])]
        entries += [(key, ['shell', 'settings', 'get', 'global', key]) for key in SCALES]
        entries += [('telephony', ['shell', 'dumpsys', 'telephony.registry'])]
        for label, argv in entries:
            fixed[moment + '-' + label] = argv
        if moment == 'before':
            observation_order = ['before-' + label for label, _ in entries]
    for key in SCALES:
        fixed['disable-' + key] = ['shell', 'settings', 'put', 'global', key, '0']
    labels = [row['label'] for row in device['commands']]
    prefix = ['emulator-check', 'boot-check', 'avd-name', *observation_order,
              'signal-profile-help', 'voice-home', 'data-home', 'signal-profile-four']
    c.require(labels[:len(prefix)] == prefix, 'Setup command prefix differs')
    index = len(prefix)
    radio_labels = []
    while index < len(labels) and labels[index] == 'telephony':
        radio_labels.append(index)
        index += 1
    middle = ['confirmed-gsm', *['disable-' + key for key in SCALES], 'allow-demo', 'start-demo']
    c.require(len(radio_labels) >= 4 and labels[index:index + len(middle)] == middle,
              'Actual signal observations or clock/scale setup order differs')
    index += len(middle)
    controllers = []
    while index < len(labels) and labels[index] == 'demo-controller':
        controllers.append(index)
        index += 1
    suffix = ['demo-clock'] + [name.replace('before-', 'after-', 1) for name in observation_order]
    c.require(controllers and labels[index:] == suffix, 'Demo completion or final setup observations differ')
    streams, raw = set(), {}
    expected_names = {'prerequisites/emulator-launch.json', 'prerequisites/runtime-ready.json',
                      'prerequisites/toolchain-inputs.json', 'prerequisites/device/capture-device.json'}
    previous_start = None
    for index, row in enumerate(device['commands']):
        label = row['label']
        c.require(row['argv'] == [adb, '-s', c.SERIAL, *fixed[label]]
                  and type(row['exit_code']) is int and row['exit_code'] == 0 and 'error' not in row
                  and type(row['seconds']) in (int, float) and 0 <= row['seconds'] <= 15,
                  'Parent setup command argv/result differs')
        started = datetime.fromisoformat(row['started_utc'].replace('Z', '+00:00'))
        c.require(previous_start is None or started >= previous_start, 'Setup command timestamps reverse')
        previous_start = started
        values = {}
        for stream in ('stdout', 'stderr'):
            item = row[stream]
            filename = f'{index + 1:03d}-{label}.{stream}.txt'
            c.require(item['path'] == filename and filename not in streams, 'Setup stream is reused or renamed')
            streams.add(filename)
            name = 'prerequisites/device/' + filename
            expected_names.add(name)
            data = c.checked_path(root, name).read_bytes()
            c.require(c.identity(data) == {key: item[key] for key in ('bytes', 'sha256')}, 'Setup stream hash differs')
            values[stream] = data.decode()
        c.require(not values['stderr'].strip(), 'Parent setup command reported stderr')
        if fixed[label][0] == 'emu':
            lines = values['stdout'].strip().splitlines()
            c.require(lines and lines[-1].strip() == 'OK' and not re.search(r'(?m)^\s*KO:', values['stdout']),
                      'Emulator console setup command did not complete')
        raw[index] = values['stdout']
    c.require(actual_names == expected_names, 'Complete prerequisite input inventory differs')
    single = {label: raw[index] for index, label in enumerate(labels) if labels.count(label) == 1}
    c.require(single['emulator-check'].strip() == single['boot-check'].strip() == '1'
              and single['avd-name'].strip().splitlines() == [c.AVD, 'OK'], 'Initial emulator identity differs')
    actual_observations = [parents['radio'].primary_signals(raw[index]) for index in radio_labels]
    c.require([row['signals'] for row in device['signal_observations']] == actual_observations,
              'Signal observations differ from their actual raw commands')
    primary = device['confirmed_primary_signal']['primary']
    c.require(actual_observations[-1] == [device['confirmed_primary_signal']]
              and all(len(rows) == 1 and (rows[0]['primary'], rows[0]['level']) == (primary, 4)
                      for rows in actual_observations[-4:])
              and 15 <= device['signal_stable_seconds'] <= device['signal_timeout_seconds'] <= 180,
              'One primary level-four radio was not retained for the declared stable interval')
    c.require(all(re.search(r'gsm ' + name + r' state:\s*home\b', single['confirmed-gsm'])
                  for name in ('voice', 'data')), 'Home registration was not observed')
    c.require(re.search(r'\bisInDemoMode=true\b', raw[controllers[-1]])
              and re.search(r'\bisDemoModeAllowed=true\b', raw[controllers[-1]]), 'Actual demo controller was not ready')
    final_signals = parents['radio'].primary_signals(single['after-telephony'])
    c.require(final_signals == device['after']['primary_signals'] and len(final_signals) == 1
              and (final_signals[0]['primary'], final_signals[0]['level']) == (primary, 4),
              'Configured radio changed before the fixed experiment')
    for label in ('demo-allowed', 'demo-on'):
        c.require(single['after-' + label].strip() == '1', 'Requested demo settings were not observed')
    c.require(all(single['after-' + key].strip() in ('0', '0.0') for key in SCALES),
              'Initial zero animation configuration differs')
    c.require(experiment['primary_radio'] == primary, 'Experiment radio identity differs from actual setup')
    return primary


class Ledger:
    def __init__(self, root, live):
        self.root = Path(root).resolve()
        self.live = live
        self.names, self.host_inodes, self.actual_inodes = set(), set(), set()

    def artifact(self, prefix, row, name):
        c.require(type(row) is dict and set(row) == {'path', 'bytes', 'sha256', 'creation'}
                  and row['path'] == name, 'Artifact has another logical role: ' + name)
        full = prefix + '/' + name
        c.canonical_name(full)
        c.require(full not in self.names, 'Artifact role reused: ' + full)
        path = c.checked_path(self.root, full)
        data = path.read_bytes()
        c.require(c.identity(data) == {k: row[k] for k in ('bytes', 'sha256')}, 'Artifact bytes changed: ' + full)
        creation = row['creation']
        c.require(set(creation) == {'started_ns', 'opened_ns', 'closed_ns', 'initial_stat', 'final_stat'},
                  'Missing exclusive-creation evidence')
        c.clock_interval(creation['started_ns'], creation['opened_ns'], full)
        c.clock_interval(creation['opened_ns'], creation['closed_ns'], full)
        first, last = creation['initial_stat'], creation['final_stat']
        c.require(c.regular_one_link(first) and c.regular_one_link(last) and first['bytes'] == 0
                  and last['bytes'] == len(data), 'Invalid exclusive regular-file metadata: ' + full)
        host = (last['device'], last['inode'])
        c.require(host == (first['device'], first['inode']) and host not in self.host_inodes,
                  'Original host inode was replaced or borrowed: ' + full)
        actual = c.stats(path.stat())
        physical = (actual['device'], actual['inode'])
        c.require(c.regular_one_link(actual) and physical not in self.actual_inodes,
                  'Local evidence has a physical alias: ' + full)
        if self.live:
            c.require(actual == last, 'Live stat record no longer matches its file: ' + full)
        self.names.add(full)
        self.host_inodes.add(host)
        self.actual_inodes.add(physical)
        return data


class Commands:
    def __init__(self, ledger, prefix, values, begin, end, deadline):
        c.require(type(values) is list, 'Commands are not an ordered list')
        self.ledger, self.prefix, self.values = ledger, prefix, values
        self.cursor, self.raw = 0, []
        previous = begin
        for index, command in enumerate(values):
            c.require(command.get('index') == index and type(command['index']) is int,
                      'Command index changed or repeats')
            argv = command.get('argv')
            c.require(type(argv) is list and argv and all(type(x) is str for x in argv), 'Invalid command argv')
            start, returned, closed = (command[k] for k in ('started_ns', 'subprocess_finished_ns', 'record_finished_ns'))
            c.clock_interval(previous, start, 'command start')
            c.clock_interval(start, returned, 'command execution')
            c.clock_interval(returned, closed, 'command evidence closure')
            c.require(closed <= end <= deadline, 'Command or enclosing recorder exceeded its bound')
            limit = command.get('enclosing_deadline_ns')
            maximum, actual = command.get('requested_timeout_seconds'), command.get('timeout_seconds')
            c.require(type(limit) is int and start < limit <= deadline
                      and type(maximum) is int and maximum in (120, 180, 600)
                      and type(actual) in (int, float) and actual == min(maximum, (limit - start) / 1e9),
                      'Recorded command timeout is not its actual clipped fixed bound')
            c.require(returned <= limit and command.get('timed_out') is False and 'error' not in command
                      and type(command.get('returncode')) is int, 'A device command did not finish within its bound')
            raw = {}
            for stream in ('stdout', 'stderr'):
                row = command[stream]
                raw[stream] = ledger.artifact(prefix, row, f'command-{index:05d}.' + stream)
            stdout, stderr = command['stdout']['creation'], command['stderr']['creation']
            c.require(returned <= stdout['started_ns'] <= stdout['closed_ns'] <= stderr['started_ns']
                      <= stderr['closed_ns'] <= closed, 'Raw streams are not owned by this completed command')
            self.raw.append(raw)
            previous = closed

    def take(self, index, argv, maximum=120, code=0, clean_stderr=True):
        c.require(type(index) is int and index == self.cursor and index < len(self.values),
                  'Command is missing, borrowed, out of order or extra')
        value = self.values[index]
        c.require(value['argv'] == argv and value['requested_timeout_seconds'] == maximum,
                  'Actual command argv/bound differs at role ' + str(index))
        if code is not None:
            c.require(value['returncode'] == code, 'Command result differs at role ' + str(index))
        raw = self.raw[index]
        if clean_stderr:
            c.require(not raw['stderr'].strip(), 'Command reported unexpected stderr')
        self.cursor += 1
        return raw['stdout'], raw['stderr'], value

    def shell(self, index, argv, maximum=120, code=0, clean_stderr=True):
        return self.take(index, ['shell', shlex.join(argv)], maximum, code, clean_stderr)

    def done(self):
        c.require(self.cursor == len(self.values), 'Undeclared extra device command remains')


def environment(commands, value, scale):
    expected = c.expected_environment(scale)
    rows = value['commands']
    c.require(len(rows) == len(PROPERTIES) + len(SETTINGS) + 2, 'Environment command inventory changed')
    actual, index = {'serial': c.SERIAL}, 0
    for key in PROPERTIES:
        raw, _, _ = commands.shell(rows[index], ['getprop', key])
        actual[key], index = raw.decode().strip(), index + 1
    for namespace, key in SETTINGS:
        raw, _, _ = commands.shell(rows[index], ['settings', 'get', namespace, key])
        actual[namespace + ':' + key], index = raw.decode().strip(), index + 1
    for key in ('size', 'density'):
        raw, _, _ = commands.shell(rows[index], ['wm', key])
        actual['display_' + key], index = raw.decode().strip(), index + 1
    c.require(value['values'] == actual == expected, 'Full device environment differs')


def scales(commands, value, desired=None):
    c.require(len(value['commands']) == 3, 'All three scale reads are required')
    actual = {}
    for key, index in zip(SCALES, value['commands']):
        raw, _, _ = commands.shell(index, ['settings', 'get', 'global', key])
        actual[key] = raw.decode().strip()
    c.require(actual == value['values'], 'Scale report differs from its raw reads')
    if desired is not None:
        c.require(actual == desired, 'Requested animation scale was not observed')


def guard(commands, value, scale, primary, parents):
    indices = value['commands']
    c.require(set(indices) == {'state', 'avd', 'gsm', 'boot', 'telephony'}, 'Device guard inventory differs')
    out, _, _ = commands.take(indices['state'], ['get-state'])
    c.require(out.decode().strip() == 'device', 'The selected device is not ready')
    out, _, _ = commands.take(indices['avd'], ['emu', 'avd', 'name'])
    c.require(out.decode().strip().splitlines() == [c.AVD, 'OK'], 'The actual AVD changed')
    out, _, _ = commands.take(indices['gsm'], ['emu', 'gsm', 'status'])
    text = out.decode().strip()
    c.require(text.splitlines()[-1] == 'OK' and all(re.search(r'gsm ' + key + r' state:\s*home\b', text)
              for key in ('voice', 'data')), 'Home cellular registration changed')
    out, _, _ = commands.shell(indices['boot'], ['getprop', 'sys.boot_completed'])
    c.require(out.decode().strip() == '1', 'Framework boot is incomplete')
    out, _, _ = commands.shell(indices['telephony'], ['dumpsys', 'telephony.registry'])
    signals = parents['radio'].primary_signals(out.decode())
    c.require(len(signals) == 1 and signals[0] == value['primary_signal']
              and (signals[0]['primary'], signals[0]['level']) == (primary, 4),
              'Actual primary radio or strength changed')
    environment(commands, value['environment'], scale)
    first = commands.values[indices['state']]['started_ns']
    last = commands.values[value['environment']['commands'][-1]]['record_finished_ns']
    c.require(value['started_ns'] <= first <= last <= value['finished_ns'], 'Device guard chronology differs')


def installed(commands, value, digest, proof):
    raw, err, item = commands.shell(value['path_command'], ['pm', 'path', c.PACKAGE], code=None, clean_stderr=False)
    path = proof.installed_path(item['returncode'], raw.decode(), err.decode())
    raw, err, item = commands.shell(value['checksum_command'], ['sha256sum', path], code=None, clean_stderr=False)
    actual = proof.installed_digest(item['returncode'], raw.decode(), err.decode(), path)
    c.require(value['path'] == path and value['sha256'] == actual == digest,
              'Fresh installed identity differs from its exact APK')


def wait(value, label, duration, origin, previous, following):
    c.require(value['label'] == label and value['requested_ns'] == duration and type(value['requested_ns']) is int
              and value['origin_ns'] == origin and value['target_ns'] == origin + duration,
              'Fixed wait label, origin or duration changed')
    start, end = value['started_ns'], value['finished_ns']
    c.require(origin <= previous <= start <= end <= following and end >= origin + duration,
              'Fixed wait is incomplete or out of actual operation order')


def observation(commands, value, label, surface, pid, parents):
    c.require(value['label'] == label and value['surface'] == surface and value['status'] == 'RECORDED'
              and 'reason' not in value and 'cleanup_error' not in value, 'Fixed observation is incomplete')
    start, end, completed = (value[k] for k in ('started_ns', 'finished_ns', 'completed_ns'))
    c.clock_interval(start, end, label)
    c.clock_interval(end, completed, label + ' closure')
    c.require(1_000_000_000 <= end - start <= 30_000_000_000 and completed - start <= 30_000_000_000,
              'Observation interval lies outside the fixed live bounds')
    indices = value['commands']
    c.require(len(indices) == 8, 'Observation must have exactly eight acquisition commands')
    remote = value['remote_xml']
    c.require(re.fullmatch(r'/data/local/tmp/md-indicator-[0-9a-f]{32}\.xml', remote), 'Unexpected remote XML name')
    expected = [(['shell', shlex.join(['pidof', c.PACKAGE])], 'pid_first', label + '-pid_first.txt'),
        (['shell', 'dumpsys activity activities'], 'foreground', label + '-foreground.txt'),
        (['shell', 'uiautomator dump ' + remote], None, None),
        (['exec-out', 'cat', remote], 'hierarchy', label + '.xml'),
        (['shell', 'rm -f ' + remote], None, None),
        (['exec-out', 'screencap', '-p'], 'screenshot', label + '.png'),
        (['shell', 'dumpsys activity activities'], 'foreground_final', label + '-foreground_final.txt'),
        (['shell', shlex.join(['pidof', c.PACKAGE])], 'pid_final', label + '-pid_final.txt')]
    raw = {}
    for index, (argv, role, filename) in zip(indices, expected):
        data, _, command = commands.take(index, argv)
        c.require(start <= command['started_ns'] <= command['record_finished_ns'] <= end,
                  'Observation borrowed a command outside its own interval')
        if role:
            artifact = value['artifacts'][role]
            raw[role] = commands.ledger.artifact(commands.prefix, artifact, filename)
            c.require(raw[role] == data, 'Observation bytes do not come from their own command: ' + role)
            c.require(command['record_finished_ns'] <= artifact['creation']['started_ns']
                      <= artifact['creation']['closed_ns'] <= end, 'Observation copy chronology differs')
    c.require(set(value['artifacts']) == set(raw), 'Observation artifact inventory differs')
    live_wait = value['minimum_live_interval_wait']
    prior = value['artifacts']['screenshot']['creation']['closed_ns']
    next_start = commands.values[indices[6]]['started_ns']
    c.require(prior <= live_wait['started_ns'] <= live_wait['finished_ns'] <= next_start
              and live_wait['target_ns'] == start + 1_050_000_000
              and live_wait['requested_ns'] == max(0, live_wait['target_ns'] - live_wait['started_ns'])
              and live_wait['finished_ns'] >= live_wait['target_ns'], 'Minimum live-interval timing differs')
    proof, runner = parents['android_compare'], parents['editor_journey']
    actual_pid = c.single_pid(raw['pid_first'].decode(), proof)
    c.require(c.single_pid(raw['pid_final'].decode(), proof) == actual_pid
              and (pid is None or actual_pid == pid) and value['pid'] == actual_pid,
              'Main process changed within its fresh install')
    c.require(all(c.canonical_component(raw[key].decode(), proof) == c.INTRO for key in ('foreground', 'foreground_final'))
              and value['component'] == c.INTRO, 'Observed foreground component changed')
    fixture_name = 'original-intro1-preinput.xml' if surface == 'intro1' else 'original-intro2.xml'
    canonical = runner.canonical(runner.tree(raw['hierarchy'], c.PACKAGE))
    expected_tree = runner.canonical(runner.tree((c.HERE / 'fixtures' / fixture_name).read_bytes(), c.PACKAGE))
    c.require(canonical == expected_tree, 'Full XML semantics/ancestors/bounds differ from the observed surface')
    width, height, rgba = parents['observed_journey'].png_pixels(raw['screenshot'], proof)
    c.require((width, height, len(rgba)) == (720, 1280, 720 * 1280 * 4), 'Full PNG dimensions differ')
    serialized = commands.ledger.artifact(commands.prefix, value['record_artifact'], label + '-observation.json')
    expected_value = {k: v for k, v in value.items() if k not in ('record_artifact', 'completed_ns')}
    c.require(serialized == c.bytes_json(expected_value)
              and end <= value['record_artifact']['creation']['started_ns']
              <= value['record_artifact']['creation']['closed_ns'] <= completed,
              'Immutable observation record differs from its own complete acquisition')
    return {'pid': actual_pid, 'hierarchy': raw['hierarchy'], 'screenshot': raw['screenshot'],
            'xml_sha256': c.identity(raw['hierarchy'])['sha256'], 'png_sha256': c.identity(raw['screenshot'])['sha256'],
            'source': commands.prefix + '/' + value['artifacts']['screenshot']['path'],
            'xml_source': commands.prefix + '/' + value['artifacts']['hierarchy']['path'],
            'started_ns': start, 'finished_ns': end, 'completed_ns': completed}


def verify_slot(ledger, entry, spec, experiment, parents, previous_end, primary):
    prefix = f'slot-{spec["index"]:02d}'
    c.require(entry['index'] == spec['index'] and entry['directory'] == prefix, 'Slot directory/index changed')
    serialized = ledger.artifact(prefix, entry['receipt'], 'slot.json')
    report = json.loads(serialized)
    c.require(serialized == c.bytes_json(report), 'Slot serialization changed')
    c.require(report.get('schema') == 1 and report.get('status') == 'COMPLETE'
              and report.get('experiment_id') == experiment['id']
              and report.get('experiment_start_ns') == experiment['started_ns']
              and report.get('global_deadline_ns') == experiment['deadline_ns']
              and report.get('runtime_manifest_sha256') == experiment['runtime_manifest_sha256'],
              'Slot is incomplete or belongs to another experiment/source')
    begin, end = report['started_ns'], report['finished_ns']
    c.clock_interval(previous_end, begin, 'successive slot invocations')
    c.clock_interval(begin, end, 'slot invocation')
    c.require(end - begin <= 900_000_000_000 and end <= experiment['deadline_ns'], 'Fixed slot/global deadline exceeded')
    receipt = entry['receipt']['creation']
    c.require(end <= receipt['started_ns'] <= receipt['closed_ns'] <= experiment['deadline_ns'],
              'Slot completion receipt is out of order')
    value = report['slot']
    c.require({key: value[key] for key in spec} == spec and value.get('status') == 'COMPLETE'
              and begin <= value['started_ns'] <= value['finished_ns'] <= end, 'Fixed slot body is incomplete or reordered')
    commands = Commands(ledger, prefix, report['commands'], begin, end,
                        min(begin + 900_000_000_000, experiment['deadline_ns']))
    expected_apk = c.ORIGINAL if spec['apk'] == 'original' else c.CANDIDATE
    path = experiment['apks'][spec['apk']]['path']
    for name in ('local_apk_before', 'local_apk_after'):
        row = value[name]
        c.require(row['path'] == path and {key: row[key] for key in ('bytes', 'sha256')} == expected_apk,
                  'Slot local APK read differs from its fixed input')
        c.clock_interval(row['started_ns'], row['finished_ns'], name)
        c.require(value['started_ns'] <= row['started_ns'] <= row['finished_ns'] <= value['finished_ns'],
                  'Local APK read is outside the slot')
    previous_scale = '0' if spec['index'] <= 5 else '1'
    guard(commands, value['device_guard'], previous_scale, primary, parents)
    c.require(value['local_apk_before']['finished_ns'] <= value['device_guard']['started_ns'],
              'Device mutation preceded the fresh local APK read')
    _, _, removal = commands.take(value['uninstall'], ['uninstall', c.PACKAGE], code=None, clean_stderr=False)
    c.require(value['device_guard']['finished_ns'] <= removal['started_ns'], 'Package removal preceded its device guard')
    proof = parents['android_compare']
    raw, err, item = commands.shell(value['absence'], ['pm', 'path', c.PACKAGE], code=None, clean_stderr=False)
    c.require(proof.absence_ok(item['returncode'], raw.decode(), err.decode()), 'Full package absence is unproved')
    raw, err, _ = commands.shell(value['pid_absence'], ['pidof', c.PACKAGE], code=1)
    c.require(not raw.strip() and not err.strip(), 'Previous process remained after uninstall')
    desired = {'animator_duration_scale': spec['animator_duration_scale'],
               'window_animation_scale': '0', 'transition_animation_scale': '0'}
    scales(commands, value['scale_before'], {**desired, 'animator_duration_scale': previous_scale})
    c.require(len(value['scale_write']) == 3, 'All three explicit scale writes are required')
    for key, index in zip(SCALES, value['scale_write']):
        raw, _, _ = commands.shell(index, ['settings', 'put', 'global', key, desired[key]])
        c.require(not raw.strip(), 'Scale write produced unexpected output')
    scales(commands, value['scale_after_write'], desired)
    environment(commands, value['environment_before'], spec['animator_duration_scale'])
    raw, err, item = commands.take(value['install'], ['install', '--no-streaming', path], 600,
                                    code=None, clean_stderr=False)
    c.require(proof.install_ok(item['returncode'], raw.decode(), err.decode()), 'Fixed APK install did not succeed')
    installed(commands, value['installed_initial'], expected_apk['sha256'], proof)
    raw, _, _ = commands.shell(value['resolve'], ['cmd', 'package', 'resolve-activity', '--brief', '-a',
                'android.intent.action.MAIN', '-c', 'android.intent.category.LAUNCHER', '-p', c.PACKAGE])
    launchers = re.findall(re.escape(c.PACKAGE) + r'/[A-Za-z0-9_.$]+', raw.decode())
    c.require(launchers == [value['launcher']], 'Actual launcher identity is ambiguous')
    raw, _, launch = commands.shell(value['launch'], ['am', 'start', '-W', '-n', launchers[0]], 180)
    c.require(proof.launch_ok(launch['returncode'], raw.decode()), 'Launch did not succeed')
    wait(value['launch_wait'], 'post-launch', 4_000_000_000, launch['subprocess_finished_ns'],
         launch['record_finished_ns'], value['initial']['started_ns'])
    label = prefix
    first = observation(commands, value['initial'], label + '-initial', 'intro1', None, parents)
    boundary = value['preinput']
    c.require(first['completed_ns'] <= boundary['started_ns'] <= boundary['finished_ns']
              and boundary['finished_ns'] - boundary['started_ns'] <= 15_000_000_000,
              'Fresh input boundary is out of order or expired')
    first_guard_command = commands.cursor
    installed(commands, boundary['installed'], expected_apk['sha256'], proof)
    scales(commands, boundary['scales'], desired)
    fresh = observation(commands, boundary['observation'], label + '-preinput', 'intro1', first['pid'], parents)
    raw, _, _ = commands.shell(boundary['immediate_pid'], ['pidof', c.PACKAGE])
    c.require(c.single_pid(raw.decode(), proof) == first['pid'], 'Immediate preinput PID differs')
    raw, _, _ = commands.shell(boundary['immediate_foreground'], ['dumpsys', 'activity', 'activities'])
    c.require(c.canonical_component(raw.decode(), proof) == c.INTRO, 'Immediate preinput component differs')
    runner = parents['editor_journey']
    target = runner.target(fresh['hierarchy'], c.PACKAGE,
                           {'resource-id': c.PACKAGE + ':id/button_next', 'content-desc': 'Next'}, 720, 1280)
    c.require(target == [640, 1152], 'Observed NEXT bounds/ancestor guard differs')
    raw, _, tap = commands.shell(boundary['tap'], ['input', 'tap', '640', '1152'])
    c.require(not raw.strip() and boundary['started_ns'] <= commands.values[first_guard_command]['started_ns']
              and tap['record_finished_ns'] <= boundary['finished_ns'], 'Tap did not follow its own complete guard')
    c.require(len(value['samples']) == 5 and len(value['gaps']) == 4, 'The five fixed samples/four gaps are required')
    wait(value['input_wait'], 'post-input', 2_000_000_000, tap['subprocess_finished_ns'],
         boundary['finished_ns'], value['samples'][0]['started_ns'])
    samples = []
    for index, sample in enumerate(value['samples']):
        if index:
            prior = value['samples'][index - 1]['completed_ns']
            wait(value['gaps'][index - 1], 'sample-gap-' + str(index), 1_000_000_000,
                 prior, prior, sample['started_ns'])
        samples.append(observation(commands, sample, label + '-sample-' + str(index), 'intro2', first['pid'], parents))
    installed(commands, value['installed_final'], expected_apk['sha256'], proof)
    scales(commands, value['scale_final'], desired)
    environment(commands, value['environment_after'], spec['animator_duration_scale'])
    c.require(commands.values[-1]['record_finished_ns'] <= value['local_apk_after']['started_ns'],
              'Final local APK read predates the completed observations')
    commands.done()
    c.require(report['observations'] == [value['initial'], boundary['observation'], *value['samples']],
              'Observation ledger is missing, duplicated or reordered')
    journal = c.checked_path(ledger.root, prefix + '/journal.json').read_bytes()
    c.require(journal == serialized, 'Closed slot journal differs from its immutable receipt')
    return {'index': spec['index'], 'condition': spec['condition'], 'apk': spec['apk'],
            'started_ns': begin, 'finished_ns': end, 'receipt_closed_ns': receipt['closed_ns'], 'samples': samples,
            'main_pid': first['pid'], 'observations': 7, 'inputs': 1}


def difference_records(first, second):
    for offset in range(0, len(first), 4):
        a, b = first[offset:offset + 4], second[offset:offset + 4]
        if a != b:
            yield offset // 4, a, b


def write_difference(path, first, second, width, height):
    """Lossless row-major index + two RGBA tuples, streamed in fixed records."""
    c.require(len(first) == len(second) == width * height * 4, 'Difference dimensions differ')
    count, digest, buffered = 0, hashlib.sha256(), bytearray()
    with Path(path).open('xb') as destination:
        with gzip.GzipFile(filename='', mode='wb', fileobj=destination, mtime=0, compresslevel=6) as compressed:
            for index, a, b in difference_records(first, second):
                buffered.extend(DIFF.pack(index, a, b))
                count += 1
                if len(buffered) >= 65_520:
                    digest.update(buffered)
                    compressed.write(buffered)
                    buffered.clear()
            if buffered:
                digest.update(buffered)
                compressed.write(buffered)
    result = {'format': 'row-major-u32be-rgba8-rgba8-gzip-v1', 'record_bytes': 12,
              'width': width, 'height': height, 'changed_pixels': count,
              'expanded_bytes': count * 12, 'expanded_sha256': digest.hexdigest(), **c.file_identity(path)}
    verify_difference(path, result, first, second)
    return result


def verify_difference(path, metadata, first, second):
    c.require(metadata['format'] == 'row-major-u32be-rgba8-rgba8-gzip-v1' and metadata['record_bytes'] == 12
              and metadata['expanded_bytes'] == metadata['changed_pixels'] * 12
              and c.file_identity(path) == {key: metadata[key] for key in ('bytes', 'sha256')},
              'Lossless difference stream identity/format differs')
    width, height = metadata['width'], metadata['height']
    c.require(len(first) == len(second) == width * height * 4, 'Recount dimensions differ')
    previous, count, digest = -1, 0, hashlib.sha256()
    with gzip.open(path, 'rb') as source:
        while True:
            data = source.read(65_520)
            if not data:
                break
            c.require(len(data) % 12 == 0, 'Truncated fixed pixel-difference record')
            digest.update(data)
            for index, a, b in DIFF.iter_unpack(data):
                c.require(previous < index < width * height and a != b
                          and first[index * 4:index * 4 + 4] == a
                          and second[index * 4:index * 4 + 4] == b,
                          'Difference record omits order or changes actual RGBA values')
                previous, count = index, count + 1
                c.require(count <= width * height, 'Difference stream exceeds the complete frame')
    actual_count = sum(first[i:i + 4] != second[i:i + 4] for i in range(0, len(first), 4))
    c.require(count == actual_count == metadata['changed_pixels']
              and digest.hexdigest() == metadata['expanded_sha256'], 'Full-frame decode/recount differs')
    return count
