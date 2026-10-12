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
    c.require(type(binaries) is list and [row.get('path') for row in binaries]
              == [*c.TOOL_METADATA, *c.TOOL_BINARIES], 'Complete installed toolchain role inventory differs')
    for row in binaries:
        c.require(set(row) == {'path', 'bytes', 'sha256'} and type(row['bytes']) is int and row['bytes'] > 0
                  and re.fullmatch(r'[0-9a-f]{64}', row['sha256']), 'Invalid installed toolchain record')
        if row['path'] in c.TOOL_METADATA:
            c.require(c.file_identity(c.checked_path(root, 'prerequisites/toolchain/' + row['path']))
                      == {key: row[key] for key in ('bytes', 'sha256')}, 'Actual toolchain metadata copy differs')
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
    expected_names.update('prerequisites/toolchain/' + name for name in c.TOOL_METADATA)
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
    c.require({path.relative_to(root).as_posix() for path in (root / 'prerequisites').rglob('*') if path.is_file()}
              == expected_names, 'Unlisted or missing prerequisite file')
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
        self.remote_xml_names = set()

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
    c.clock_interval(start, end, 'fixed wait')
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
    c.require(remote not in commands.ledger.remote_xml_names, 'Another observation reused this remote XML role')
    commands.ledger.remote_xml_names.add(remote)
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
    c.surface_identity(raw['hierarchy'], surface, parents)
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
    c.require(type(entry['index']) is int, 'Slot index must be an actual integer')
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
    attempt_bytes = ledger.artifact(prefix, report['attempt'], 'attempt-receipt.json')
    attempt = json.loads(attempt_bytes)
    c.require(attempt_bytes == c.bytes_json(attempt)
              and c.checked_path(ledger.root, prefix + '/attempt.json').read_bytes() == attempt_bytes
              and attempt['schema'] == 1 and attempt['experiment_id'] == experiment['id']
              and attempt['slot'] == spec['index'] and attempt['status'] == 'PREFLIGHT_VERIFIED'
              and attempt['started_ns'] == begin
              and begin <= attempt['preflight_finished_ns'] <= report['attempt']['creation']['started_ns']
              <= report['attempt']['creation']['closed_ns'] <= value['started_ns'],
              'Slot did not follow its own reserved and verified preflight')
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
    c.require(parents['editor_journey'].canonical(parents['editor_journey'].tree(first['hierarchy'], c.PACKAGE))
              == parents['editor_journey'].canonical(parents['editor_journey'].tree(fresh['hierarchy'], c.PACKAGE)),
              'Complete initial/preinput XML changed within the fresh input boundary')
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


def validate_prefix(root, experiment, parents, live, allow_incomplete=False):
    c.require(experiment.get('schema') == 1 and type(experiment.get('schema')) is int
              and experiment.get('kind') == 'FIXED_INDICATOR_DIAGNOSTIC_V1'
              and re.fullmatch(r'[0-9a-f]{32}', experiment.get('id', ''))
              and experiment.get('parent_commit') == c.PARENT_COMMIT,
              'Wrong diagnostic report or fixed parent identity')
    policy = c.protocol()
    c.require(experiment['protocol_sha256'] == c.file_identity(c.HERE / 'protocol.json')['sha256']
              and experiment['runtime_manifest_sha256'] == c.file_identity(c.HERE / 'runtime-files.json')['sha256'],
              'Executed fixed policy/source manifest changed')
    c.clock_interval(experiment['started_ns'], experiment['deadline_ns'], 'whole experiment')
    c.require(experiment['deadline_ns'] == experiment['started_ns'] + 7_200_000_000_000,
              'Global experiment deadline was reset or extended')
    c.require(experiment.get('new_runtime_parity_credit') == 0 and type(experiment.get('new_runtime_parity_credit')) is int
              and all(experiment.get(key) is False for key in ('full_runtime_1_to_1_established', 'cause_established',
                  'crash_free_run_established', 'app_apk_modified', 'cross_app_frame_selection', 'masks_used')),
              'Diagnostic report claims undeclared parity or normalization')
    c.require(set(experiment['apks']) == {'original', 'candidate'}, 'Both fixed APK roles are required')
    for role, wanted in (('original', c.ORIGINAL), ('candidate', c.CANDIDATE)):
        row = experiment['apks'][role]
        c.require({key: row[key] for key in ('bytes', 'sha256')} == wanted
                  and type(row['path']) is str and Path(row['path']).is_absolute(), 'Fixed APK identity/path changed')
    primary = verify_prerequisites(root, experiment, parents)
    ledger = Ledger(root, live)
    entry = experiment['initialization']
    c.require(entry['directory'] == 'initialization', 'Initialization evidence directory changed')
    serialized = ledger.artifact('initialization', entry['receipt'], 'initialization.json')
    initial = json.loads(serialized)
    c.require(initial.get('schema') == 1 and initial.get('status') == 'READY'
              and initial.get('experiment_id') == experiment['id']
              and initial['started_ns'] == experiment['started_ns']
              and serialized == c.bytes_json(initial), 'Initial disposable-device observation is incomplete')
    commands = Commands(ledger, 'initialization', initial['commands'], initial['started_ns'], initial['finished_ns'],
                        min(experiment['deadline_ns'], initial['started_ns'] + 240_000_000_000))
    guard(commands, initial['device_guard'], '0', primary, parents)
    commands.done()
    c.require(initial['finished_ns'] <= entry['receipt']['creation']['started_ns'], 'Initialization receipt predates its commands')
    c.require(c.checked_path(root, 'initialization/journal.json').read_bytes() == serialized,
              'Initialization journal differs from its immutable receipt')
    previous = entry['receipt']['creation']['closed_ns']
    entries = experiment['slots']
    reserved = experiment.get('reserved_slot')
    c.require(reserved is None or (type(reserved) is int and reserved == len(entries) + 1 and reserved <= 8),
              'Reserved invocation is not the next fixed slot')
    c.require(type(entries) is list and len(entries) <= 8
              and experiment['unattempted_indices'] == list(range(len(entries) + 1 + (reserved is not None), 9)),
              'Attempted/unattempted slot inventory differs from the fixed prefix')
    completed, errors = [], []
    for entry, spec in zip(entries, policy['slots']):
        try:
            value = verify_slot(ledger, entry, spec, experiment, parents, previous, primary)
            completed.append(value)
            previous = value['receipt_closed_ns']
        except Exception as error:
            if not allow_incomplete:
                raise
            errors.append({'slot': spec['index'], 'reason': type(error).__name__ + ': ' + str(error)})
            break
    if len(completed) != len(entries):
        c.require(allow_incomplete, 'An incomplete slot cannot be followed')
    return {'slots': completed, 'errors': errors, 'last_receipt_closed_ns': previous,
            'verified_artifact_roles': len(ledger.names), 'verified_original_host_inodes': len(ledger.host_inodes),
            'verified_remote_xml_names': len(ledger.remote_xml_names)}


def fixed_pairs():
    values = []
    for condition, indices in [('A', (1, 2, 3, 4)), ('B', (5, 6, 7, 8))]:
        for sample in range(5):
            for first, second in itertools.combinations(indices, 2):
                values.append({'id': f'{condition}-sample-{sample}-slot-{first}-{second}', 'kind': 'cross-run',
                               'first': [first, sample], 'second': [second, sample]})
    for slot in range(1, 9):
        for sample in range(4):
            values.append({'id': f'slot-{slot}-temporal-{sample}-{sample + 1}', 'kind': 'temporal',
                           'first': [slot, sample], 'second': [slot, sample + 1]})
    c.require(len(values) == 92, 'Internal fixed-pair inventory differs')
    return values


def pair_result(root, pair, first, second, parents, write):
    proof, observer, runner = parents['android_compare'], parents['observed_journey'], parents['editor_journey']
    width, height, a = observer.png_pixels(first['screenshot'], proof)
    second_width, second_height, b = observer.png_pixels(second['screenshot'], proof)
    c.require((width, height) == (second_width, second_height) == (720, 1280), 'Pair viewport differs')
    filename = 'pairs/' + pair['id'] + '.rgba-diff.bin.gz'
    metadata_path = Path(root) / 'pairs' / (pair['id'] + '.json')
    if write:
        metadata = write_difference(Path(root) / filename, a, b, width, height)
    else:
        metadata = c.json_file(metadata_path)['difference']
        verify_difference(c.checked_path(root, filename), metadata, a, b)
    color_a = [{'chunk': kind.decode('ascii'), 'payload_hex': payload.hex()}
               for kind, payload in proof.color_metadata(first['screenshot'])]
    color_b = [{'chunk': kind.decode('ascii'), 'payload_hex': payload.hex()}
               for kind, payload in proof.color_metadata(second['screenshot'])]
    value = {**pair, 'status': 'MEASURED', 'first_png': first['source'], 'second_png': second['source'],
             'first_xml': first['xml_source'], 'second_xml': second['xml_source'],
             'first_png_sha256': first['png_sha256'], 'second_png_sha256': second['png_sha256'],
             'first_xml_sha256': first['xml_sha256'], 'second_xml_sha256': second['xml_sha256'],
             'png_bytes_equal': first['screenshot'] == second['screenshot'],
             'xml_bytes_equal': first['hierarchy'] == second['hierarchy'],
             'xml_canonical_equal': runner.canonical(runner.tree(first['hierarchy'], c.PACKAGE))
                                    == runner.canonical(runner.tree(second['hierarchy'], c.PACKAGE)),
             'width': width, 'height': height, 'first_color_metadata': color_a, 'second_color_metadata': color_b,
             'color_metadata_equal': color_a == color_b, 'difference_file': filename, 'difference': metadata}
    if write:
        with metadata_path.open('xb') as stream:
            stream.write(c.bytes_json(value))
    else:
        c.require(c.json_file(metadata_path) == value, 'Saved predetermined-pair report differs from independent replay')
    return value


def indicator_values(root, sample, parents, write):
    """Additional numerical diagnostics only; never a comparison mask."""
    width, height, rgba = parents['observed_journey'].png_pixels(sample['screenshot'], parents['android_compare'])
    c.require((width, height) == (720, 1280), 'Indicator-array viewport differs')
    # Bounds are the actual unique XML node, enforced by surface_identity.
    left, top, right, bottom = 128, 1184, 592, 1200
    data = b''.join(rgba[(y * width + left) * 4:(y * width + right) * 4] for y in range(top, bottom))
    stem = Path(sample['source']).stem
    filename = 'indicator-arrays/' + stem + '.rgba'
    path = Path(root) / filename
    if write:
        with path.open('xb') as stream:
            stream.write(data)
    else:
        c.require(c.checked_path(root, filename).read_bytes() == data, 'Saved indicator values differ from complete PNG')
    # Coordinates are taken from the fixed historical read-only design evidence.
    coordinates = c.json_file(c.HERE / 'historical-coordinates.json')
    values = [{'x': x, 'y': y, 'rgba': list(rgba[(y * width + x) * 4:(y * width + x) * 4 + 4])}
              for x, y in coordinates['union_coordinates']]
    return {'source_png': sample['source'], 'source_png_sha256': sample['png_sha256'],
            'bounds': [left, top, right, bottom], 'format': 'row-major-rgba8',
            'artifact': {'path': filename, **c.identity(data)}, 'historical_coordinate_values': values,
            'parity_weight': 0, 'used_as_mask': False}


def verify_experiment(root, experiment, parents, live, write_pairs=False):
    if write_pairs:
        measurement_start = c.now_ns()
    result = {'status': 'INDICATOR_FIXED_SAMPLE_EVIDENCE_INCOMPLETE', 'evidence_complete': False,
              'schema': 1, 'experiment_id': experiment.get('id'), 'completed_slots': 0,
              'post_input_frames': 0, 'planned_pairs': 92, 'measured_pairs': 0,
              'slots': [], 'pairs': [], 'indicator_arrays': [], 'errors': [],
              'new_runtime_parity_credit': 0, 'full_runtime_1_to_1_established': False,
              'animation_parity_established': False, 'cause_established': False,
              'crash_free_run_established': False, 'masks_used': False,
              'cross_app_frame_selection': False, 'historical_results_rewritten': False}
    samples = {}
    try:
        verified = validate_prefix(root, experiment, parents, live, allow_incomplete=True)
        result['errors'].extend(verified['errors'])
        for item in verified['slots']:
            result['slots'].append({key: value for key, value in item.items() if key != 'samples'})
            for index, sample in enumerate(item['samples']):
                samples[(item['index'], index)] = sample
        result.update(completed_slots=len(verified['slots']), post_input_frames=len(samples),
                      verified_artifact_roles=verified['verified_artifact_roles'],
                      verified_original_host_inodes=verified['verified_original_host_inodes'],
                      verified_remote_xml_names=verified['verified_remote_xml_names'])
    except Exception as error:
        result['errors'].append({'boundary': 'fixed-capture-provenance', 'reason': type(error).__name__ + ': ' + str(error)})
    if write_pairs:
        (Path(root) / 'pairs').mkdir(exist_ok=False)
        (Path(root) / 'indicator-arrays').mkdir(exist_ok=False)
    for pair in fixed_pairs():
        first, second = tuple(pair['first']), tuple(pair['second'])
        if first not in samples or second not in samples:
            result['pairs'].append({**pair, 'status': 'UNAVAILABLE_FIXED_INPUT'})
            continue
        try:
            if write_pairs:
                c.require(c.now_ns() <= experiment['deadline_ns'], 'Global deadline expired before a fixed comparison')
            measured = pair_result(root, pair, samples[first], samples[second], parents, write_pairs)
            result['pairs'].append(measured)
            result['measured_pairs'] += 1
        except Exception as error:
            result['pairs'].append({**pair, 'status': 'MEASUREMENT_FAILED', 'reason': type(error).__name__ + ': ' + str(error)})
    for key in sorted(samples):
        try:
            if write_pairs:
                c.require(c.now_ns() <= experiment['deadline_ns'], 'Global deadline expired before a fixed indicator array')
            result['indicator_arrays'].append(indicator_values(root, samples[key], parents, write_pairs))
        except Exception as error:
            result['errors'].append({'sample': list(key), 'reason': type(error).__name__ + ': ' + str(error)})
    c.require(len(result['pairs']) == 92, 'Fixed pair report inventory was reduced')
    if write_pairs:
        experiment['finalization'] = {'started_ns': measurement_start, 'finished_ns': c.now_ns(),
                                      'fixed_comparisons': 92}
        experiment['finished_ns'] = experiment['finalization']['finished_ns']
        experiment['finished_utc'] = c.utc()
    finalization = experiment.get('finalization', {})
    try:
        c.require(set(finalization) == {'started_ns', 'finished_ns', 'fixed_comparisons'}
                  and finalization['fixed_comparisons'] == 92
                  and experiment['started_ns'] <= experiment['capture_finished_ns'] <= finalization['started_ns']
                  and finalization['finished_ns'] == experiment['finished_ns'] <= experiment['deadline_ns'],
                  'Global deadline or finalization record is incomplete')
        c.clock_interval(finalization['started_ns'], finalization['finished_ns'], 'fixed comparison finalization')
        if result['slots']:
            c.require(result['slots'][-1]['receipt_closed_ns'] <= experiment['capture_finished_ns'],
                      'Finalization predates the last completed slot')
    except Exception as error:
        result['errors'].append({'boundary': 'global-finalization', 'reason': type(error).__name__ + ': ' + str(error)})
    complete = (result['completed_slots'] == 8 and result['post_input_frames'] == 40
                and result['measured_pairs'] == 92 and len(result['indicator_arrays']) == 40 and not result['errors']
                and experiment.get('status') == 'FIXED_CAPTURE_SCHEDULE_COMPLETE'
                and experiment.get('reserved_slot') is None
                and experiment.get('live_inputs_verified_after_capture') is True
                and type(experiment.get('finished_ns')) is int
                and experiment['started_ns'] <= experiment['finished_ns'] <= experiment['deadline_ns'])
    result['evidence_complete'] = complete
    if complete:
        result['status'] = 'INDICATOR_FIXED_SAMPLE_EVIDENCE_COMPLETE'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parents', type=Path, required=True)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--prepared', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--archive-replay', action='store_true',
                        help='Compare saved bytes/serialized host metadata; never equate extracted ctime with host ctime')
    parser.add_argument('--archive-apks', type=Path,
                        help='Relocated directory containing the two exact original.apk/candidate.apk bytes, for archive replay only')
    args = parser.parse_args()
    root = args.output.resolve()
    result = {'status': 'INDICATOR_FIXED_SAMPLE_EVIDENCE_INCOMPLETE', 'evidence_complete': False}
    envelope = {'verification_mode': 'saved-byte-and-recorded-host-metadata-replay' if args.archive_replay else 'live-host-stat-and-byte-verification',
                'extracted_ctime_or_inode_claimed_as_original_host': False, 'started_utc': c.utc()}
    try:
        import prepare
        c.require((args.archive_apks is not None) == args.archive_replay,
                  'Archive replay requires an explicit relocated exact-APK directory')
        prepare.verify_preparation(args.parents, args.source_root, args.prepared,
                                   archive_apks=args.archive_apks)
        parents = c.load_parents(args.parents)
        experiment = c.json_file(root / 'experiment.json')
        c.require(experiment['preparation_identity'] == c.file_identity(args.prepared / 'preparation.json'),
                  'Preparation receipt differs from the one used before installation')
        result = verify_experiment(root, experiment, parents, live=not args.archive_replay)
        captured = c.json_file(root / 'comparison.json')
        c.require(result == captured, 'Independent full fixed-schedule replay differs from its saved result')
        envelope['literal_replay_equal'] = True
    except Exception as error:
        result = {'status': 'INDICATOR_FIXED_SAMPLE_EVIDENCE_INCOMPLETE', 'evidence_complete': False,
                  'reason': type(error).__name__ + ': ' + str(error)}
        envelope['literal_replay_equal'] = False
    envelope.update(result=result, finished_utc=c.utc())
    c.write_json(root.parent / 'independent-verification.json', envelope)
    print(json.dumps({'status': result['status'], 'evidence_complete': result['evidence_complete'],
                      'literal_replay_equal': envelope['literal_replay_equal'],
                      'verification_mode': envelope['verification_mode']}, indent=2))
    return 0 if result['evidence_complete'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
