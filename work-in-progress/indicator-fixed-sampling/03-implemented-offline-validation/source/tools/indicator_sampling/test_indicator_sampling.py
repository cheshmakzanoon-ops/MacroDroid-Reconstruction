"""Bounded synthetic controls; no ADB, emulator, Java, or Android execution.

One actual Recorder-produced synthetic eight-slot baseline is retained. Fault
cases retain only their exact byte/stat differences from that complete baseline,
plus this source and the observed rejection. No failed fixture is discarded.
"""
from __future__ import annotations

from contextlib import ExitStack, redirect_stdout
import copy
import gzip
import io
import json
import math
import os
from pathlib import Path
import shlex
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import xml.etree.ElementTree as ET
import zlib

import common as c
import prepare
import record
import verify

PARENTS = Path(os.environ.get('INDICATOR_PARENTS', c.HERE.parents[1] / 'pinned-inputs')).resolve()
MODULES = c.load_parents(PARENTS)
EVIDENCE = Path(os.environ.get('INDICATOR_HOST_EVIDENCE') or tempfile.mkdtemp(prefix='indicator-host-controls-')).resolve()
EVIDENCE.mkdir(parents=True, exist_ok=True)
REAL_IDENTITY = c.file_identity
REAL_RECORDER = record.Recorder


def snapshot(root):
    rows = {}
    for path in root.rglob('*'):
        if path.is_file():
            info = path.stat()
            rows[path.relative_to(root).as_posix()] = {**REAL_IDENTITY(path),
                'mode': info.st_mode, 'links': info.st_nlink, 'device': info.st_dev, 'inode': info.st_ino}
    return rows


class Clock:
    def __init__(self):
        self.value = c.now_ns()

    def now(self):
        self.value += 1000
        return self.value

    def seconds(self):
        return self.now() / 1e9

    def sleep(self, seconds):
        self.value += math.ceil(seconds * 1e9)


def png(tag):
    width, height = 720, 1280
    rgba = bytearray(b'\x01\x02\x03\xff' * (width * height))
    start = (1190 * width + 200) * 4
    rgba[start:start + 4] = bytes((tag, 10, 20, 255))
    scanlines = b''.join(b'\0' + rgba[row * width * 4:(row + 1) * width * 4] for row in range(height))
    def chunk(name, data):
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', zlib.crc32(name + data) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>2I5B', width, height, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(scanlines, 1)) + chunk(b'IEND', b''))


class Device:
    def __init__(self, clock):
        self.clock, self.slot, self.installed, self.post, self.sample = clock, 0, False, False, -1
        self.role, self.pid, self.calls, self.fail = 'original', '12345', [], None
        self.settings = {key.split(':', 1)[1]: value for key, value in c.expected_environment('0').items() if ':' in key}
        self.signal = 'mSignalStrength=SignalStrength:{mLte=CellSignalStrengthLte: level=4 rsrp=-75,primary=CellSignalStrengthLte}\n'
        self.bad_preinput = False
        self.dumps = 0

    def run(self, argv, capture_output=True, timeout=120, text=False, check=False):
        self.clock.sleep(0.005)
        command = argv[3:]
        self.calls.append(command)
        if self.fail is not None and self.fail(command):
            raise subprocess.TimeoutExpired(argv, timeout, output=b'synthetic partial output\n', stderr=b'synthetic timeout\n')
        code, out = 0, b''
        if command == ['get-state']:
            out = b'device\n'
        elif command[:1] == ['emu']:
            tokens = command[1:]
            if tokens == ['avd', 'name']:
                out = (c.AVD + '\nOK\n').encode()
            elif tokens == ['gsm', 'status']:
                out = b'gsm voice state: home\ngsm data state: home\nOK\n'
            else:
                out = b'OK\n'
        elif command == ['uninstall', c.PACKAGE]:
            self.slot += 1
            self.installed, self.post, self.dumps = False, False, 0
            self.sample, self.pid = -1, str(12345 + self.slot)
            out = b'Success\n'
        elif command[:2] == ['install', '--no-streaming']:
            self.installed = True
            self.role = Path(command[2]).stem
            out = b'Success\n'
        elif command[:2] == ['exec-out', 'cat']:
            fixture = 'original-intro2.xml' if self.post else 'original-intro1-preinput.xml'
            out = (c.HERE / 'fixtures' / fixture).read_bytes()
            self.dumps += 1
            if self.post:
                self.sample += 1
                tree = ET.fromstring(out)
                node = next(n for n in tree.iter('node') if n.get('resource-id') == c.PACKAGE + ':id/button_skip')
                node.set('text', 'synthetic slot %d sample %d' % (self.slot, self.sample))
                out = ET.tostring(tree)
            elif self.bad_preinput and self.dumps == 2:
                out = out.replace(b'text="SKIP"', b'text="synthetic changed preinput"')
        elif command == ['exec-out', 'screencap', '-p']:
            out = png(self.slot * 16 + max(self.sample, 0))
        elif command[:1] == ['shell']:
            tokens = shlex.split(command[1]) if len(command) == 2 else command[1:]
            if tokens[:1] == ['getprop']:
                out = (('1' if tokens[1] == 'sys.boot_completed' else c.expected_environment('0')[tokens[1]]) + '\n').encode()
            elif tokens[:2] == ['settings', 'get']:
                out = (self.settings[tokens[3]] + '\n').encode()
            elif tokens[:2] == ['settings', 'put']:
                self.settings[tokens[3]] = tokens[4]
            elif tokens == ['dumpsys', 'telephony.registry']:
                out = self.signal.encode()
            elif tokens == ['dumpsys', 'battery']:
                out = b'level: 100\n'
            elif tokens[:1] == ['date']:
                out = b'2026-10-12T00:00:00Z\n'
            elif tokens[:2] == ['wm', 'size']:
                out = b'Physical size: 720x1280\n'
            elif tokens[:2] == ['wm', 'density']:
                out = b'Physical density: 320\n'
            elif tokens == ['pm', 'path', c.PACKAGE]:
                out = b'package:/data/app/synthetic/base.apk\n' if self.installed else b''
            elif tokens[:1] == ['sha256sum']:
                out = (((c.ORIGINAL if self.role == 'original' else c.CANDIDATE)['sha256']) + '  ' + tokens[1] + '\n').encode()
            elif tokens == ['pidof', c.PACKAGE]:
                code, out = (0, (self.pid + '\n').encode()) if self.installed else (1, b'')
            elif tokens == ['dumpsys', 'activity', 'activities']:
                out = ('topResumedActivity: ActivityRecord{a u0 ' + c.INTRO + ' t1}\n').encode()
            elif tokens[:3] == ['dumpsys', 'activity', 'service']:
                out = b'isInDemoMode=true\nisDemoModeAllowed=true\n'
            elif tokens[:3] == ['cmd', 'package', 'resolve-activity']:
                out = (c.INTRO + '\n').encode()
            elif tokens[:2] == ['am', 'start']:
                out = b'Status: ok\n'
            elif tokens[:2] == ['am', 'broadcast']:
                out = b'Broadcast completed: result=0\n'
            elif tokens[:2] == ['input', 'tap']:
                self.post = True
            elif tokens[:2] == ['uiautomator', 'dump']:
                out = ('UI hierarchy dumped to: ' + tokens[2] + '\n').encode()
            elif tokens[:2] == ['rm', '-f']:
                pass
            else:
                raise AssertionError('Unexpected simulated shell argv: ' + repr(tokens))
        else:
            raise AssertionError('Unexpected simulated ADB argv: ' + repr(command))
        return subprocess.CompletedProcess(argv, code, out.decode() if text else out, '' if text else b'')


def build_baseline(folder):
    folder.mkdir()
    clock, tooling = Clock(), folder / 'tooling'
    device = Device(clock)
    metadata = folder / 'toolchain'
    rows = []
    for name in [*c.TOOL_METADATA, *c.TOOL_BINARIES]:
        path = tooling / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('SYNTHETIC HOST FIXTURE ONLY: ' + name + '\n')
        rows.append({'path': name, **REAL_IDENTITY(path)})
        if name in c.TOOL_METADATA:
            target = metadata / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())
    c.write_json(metadata / 'installed-inputs.json', rows)
    adb = tooling / 'android/platform-tools/adb'
    radio = MODULES['radio']
    console = io.StringIO()
    with mock.patch.object(sys, 'argv', ['configure_capture_device.py', '--adb', str(adb),
              '--serial', c.SERIAL, '--output', str(folder / 'device'), '--demo-clock', '1200', '--disable-animations']), \
         mock.patch.object(radio.subprocess, 'run', side_effect=device.run), \
         mock.patch.object(radio.time, 'monotonic', side_effect=clock.seconds), \
         mock.patch.object(radio.time, 'sleep', side_effect=clock.sleep), redirect_stdout(console):
        assert radio.main() == 0
    (folder / 'helper-console.txt').write_text(console.getvalue())
    runtime = folder / 'runtime'
    runtime.mkdir()
    launch = {'serial': c.SERIAL, 'adb_path': str(adb), 'avd': c.AVD,
        'command': [str(tooling / 'android/emulator/emulator'), '-avd', c.AVD, '-port', '5560',
                    '-no-window', '-no-audio', '-no-boot-anim', '-no-snapshot', '-accel', 'on',
                    '-gpu', 'swiftshader', '-cores', '2', '-memory', '3072', '-camera-back', 'none', '-camera-front', 'none'],
        'ram_mb': 3072, 'virtual_cores': 2, 'acceleration': 'on', 'state': 'booting',
        'started_utc': '2026-10-12T00:00:00Z'}
    c.write_json(runtime / 'emulator-launch.json', launch)
    ready = {**launch, 'state': 'ready', 'adb_exit_code': 0,
             'properties': {key: value for key, value in c.expected_environment('0').items() if key.startswith('ro.')}}
    ready['properties']['sys.boot_completed'] = '1'
    c.write_json(runtime / 'runtime-status.json', ready)
    apks = {}
    for role, wanted in [('original', c.ORIGINAL), ('candidate', c.CANDIDATE)]:
        path = folder / (role + '.apk')
        path.write_bytes(b'NOT AN APK: synthetic local identity boundary')
        apks[role] = {'path': str(path), **wanted}
    prepared = folder / 'prepared'
    prepared.mkdir()
    c.write_json(prepared / 'preparation.json', {'synthetic_host_control': True, 'apks': apks})
    args = type('Args', (), dict(parents=PARENTS, source_root=c.HERE.parents[1], prepared=prepared,
        adb=adb, output=folder / 'experiment', runtime=runtime, device=folder / 'device',
        toolchain_inputs=metadata / 'installed-inputs.json', tooling=tooling, slot=None))()
    def local_identity(path):
        for role, item in apks.items():
            if Path(path).resolve() == Path(item['path']):
                return c.ORIGINAL if role == 'original' else c.CANDIDATE
        return REAL_IDENTITY(path)
    def factory(*values, **kwargs):
        return REAL_RECORDER(*values, **kwargs, clock=clock.now, sleeper=clock.sleep, executor=device.run)
    with mock.patch.object(c, 'now_ns', side_effect=clock.now), \
         mock.patch.object(c, 'file_identity', side_effect=local_identity), \
         mock.patch.object(prepare, 'verify_preparation', return_value={'apks': apks}), \
         mock.patch.object(record, 'Recorder', side_effect=factory):
        record.initialize(args)
        for index in range(1, 9):
            args.slot = index
            record.one_slot(args)
        value = record.finish(args)
    assert value['evidence_complete'] is True, value['errors']
    c.write_json(folder / 'simulation-scope.json', {'android_executed': False, 'adb_executed': False,
        'apk_preflight_mocked_for_capture_protocol_only': True, 'fixture_apk_files_are_not_applications': True,
        'pinned_radio_helper_executed_with_synthetic_executor': True, 'actual_recorder_and_verifier_executed': True,
        'completed_slots': 8, 'post_input_frames': 40, 'fixed_pairs': 92,
        'all_sample_pairs_differ_in_full_rgba_and_canonical_xml': all(p['difference']['changed_pixels'] == 1
            and p['xml_canonical_equal'] is False for p in value['pairs'])})
    return value, clock, device, args


class PureControls(unittest.TestCase):
    def setUp(self):
        self.folder = EVIDENCE / self.id().split('.')[-1]
        self.folder.mkdir()

    def test_fixed_slot_and_ninety_two_pair_inventory(self):
        slots = c.protocol()['slots']
        self.assertEqual([s['apk'] for s in slots], ['original', 'candidate', 'candidate', 'original'] * 2)
        self.assertEqual([s['animator_duration_scale'] for s in slots], ['0'] * 4 + ['1'] * 4)
        pairs = verify.fixed_pairs()
        self.assertEqual((len(pairs), len({p['id'] for p in pairs})), (92, 92))
        self.assertEqual([sum(p['kind'] == kind for p in pairs) for kind in ['cross-run', 'temporal']], [60, 32])
        c.write_json(self.folder / 'actual-pairs.json', pairs)

    def test_actual_xml_next_target_is_guarded(self):
        raw = (c.HERE / 'fixtures/original-intro1-preinput.xml').read_bytes()
        self.assertEqual(MODULES['editor_journey'].target(raw, c.PACKAGE,
            {'resource-id': c.PACKAGE + ':id/button_next', 'content-desc': 'Next'}, 720, 1280), [640, 1152])
        c.surface_identity(raw, 'intro1', MODULES)

    def reject_xml(self, mutation):
        tree = ET.fromstring((c.HERE / 'fixtures/original-intro1-preinput.xml').read_bytes())
        node = next(n for n in tree.iter('node') if n.get('resource-id') == c.PACKAGE + ':id/button_next')
        mutation(tree, node)
        raw = ET.tostring(tree)
        (self.folder / 'mutant.xml').write_bytes(raw)
        with self.assertRaises(c.Invalid):
            c.surface_identity(raw, 'intro1', MODULES)

    def test_disabled_observed_next_rejects(self):
        self.reject_xml(lambda tree, node: node.set('enabled', 'false'))

    def test_changed_observed_bounds_reject(self):
        self.reject_xml(lambda tree, node: node.set('bounds', '[700,1104][800,1200]'))

    def test_duplicate_next_rejects(self):
        with self.assertRaises((c.Invalid, MODULES['editor_journey'].JourneyError)):
            tree = ET.fromstring((c.HERE / 'fixtures/original-intro1-preinput.xml').read_bytes())
            node = next(n for n in tree.iter('node') if n.get('resource-id') == c.PACKAGE + ':id/button_next')
            tree.append(copy.deepcopy(node))
            raw = ET.tostring(tree)
            (self.folder / 'mutant.xml').write_bytes(raw)
            c.surface_identity(raw, 'intro1', MODULES)

    def test_unrelated_full_xml_difference_is_measured_not_filtered(self):
        raw = (c.HERE / 'fixtures/original-intro2.xml').read_bytes()
        tree = ET.fromstring(raw)
        node = next(n for n in tree.iter('node') if n.get('resource-id') == c.PACKAGE + ':id/button_skip')
        node.set('text', 'synthetic different leaf')
        changed = ET.tostring(tree)
        self.assertNotEqual(c.surface_identity(raw, 'intro2', MODULES), c.surface_identity(changed, 'intro2', MODULES))
        (self.folder / 'mutant.xml').write_bytes(changed)

    def test_lossless_mixed_rgba_roundtrip(self):
        a = b'\x00\x01\x02\xff' * 4
        b = bytearray(a); b[4:8] = b'\x03\x04\x05\x06'; b[12:16] = b'\x07\x08\x09\x0a'
        path = self.folder / 'values.bin.gz'
        value = verify.write_difference(path, a, bytes(b), 2, 2)
        self.assertEqual(value['changed_pixels'], 2)
        self.assertEqual(list(verify.DIFF.iter_unpack(gzip.decompress(path.read_bytes()))),
                         [(1, a[4:8], bytes(b[4:8])), (3, a[12:16], bytes(b[12:16]))])
        c.write_json(self.folder / 'metadata.json', value)

    def test_lossless_empty_pair_is_retained(self):
        value = verify.write_difference(self.folder / 'values.bin.gz', b'\0' * 16, b'\0' * 16, 2, 2)
        self.assertEqual((value['changed_pixels'], value['expanded_bytes']), (0, 0))
        c.write_json(self.folder / 'metadata.json', value)

    def fault_difference(self, transform):
        a, b = b'\0' * 16, b'\1' * 16
        path = self.folder / 'values.bin.gz'
        value = verify.write_difference(path, a, b, 2, 2)
        raw = transform(gzip.decompress(path.read_bytes()))
        path.write_bytes(gzip.compress(raw, mtime=0))
        value.update(c.file_identity(path), expanded_bytes=len(raw), expanded_sha256=c.identity(raw)['sha256'])
        c.write_json(self.folder / 'mutant-metadata.json', value)
        with self.assertRaises(c.Invalid):
            verify.verify_difference(path, value, a, b)

    def test_lossless_missing_coordinate_rejects(self):
        self.fault_difference(lambda raw: raw[12:])

    def test_lossless_wrong_rgba_rejects(self):
        self.fault_difference(lambda raw: raw[:4] + b'\x09' + raw[5:])

    def test_lossless_repeated_coordinate_rejects(self):
        self.fault_difference(lambda raw: raw[:12] + raw[:12] + raw[24:])

    def test_lossless_truncated_record_rejects(self):
        self.fault_difference(lambda raw: raw[:-1])

    def test_offline_timeout_retains_both_partial_streams(self):
        error = subprocess.TimeoutExpired(['synthetic'], 60, output=b'partial out\n', stderr=b'partial err\n')
        with mock.patch.object(prepare.subprocess, 'run', side_effect=error):
            value = prepare.offline_command(['synthetic'], 60, 'timeout', self.folder)
        self.assertTrue(value['timed_out'])
        self.assertIsNone(value['returncode'])
        self.assertEqual((self.folder / 'timeout.stdout').read_bytes(), b'partial out\n')
        self.assertEqual((self.folder / 'timeout.stderr').read_bytes(), b'partial err\n')

    def test_capture_timeout_keeps_partial_output_and_cleans_without_retry(self):
        clock = Clock(); device = Device(clock)
        device.installed = True
        device.fail = lambda argv: argv[:2] == ['exec-out', 'cat']
        trace = {'commands': [], 'observations': []}
        recorder = record.Recorder(self.folder, Path('/synthetic/adb'), MODULES, trace,
            clock=clock.now, sleeper=clock.sleep, executor=device.run)
        recorder.deadline_ns = clock.now() + 900_000_000_000
        with self.assertRaisesRegex(c.Invalid, 'Fixed observation failed'):
            recorder.observation('one-failed-observation', 'intro1')
        self.assertEqual(sum(row['argv'][:2] == ['exec-out', 'cat'] for row in trace['commands']), 1)
        self.assertEqual(sum(row['argv'][0] == 'shell' and row['argv'][1].startswith('rm -f ') for row in trace['commands']), 1)
        timed_out = [row for row in trace['commands'] if row['timed_out']]
        self.assertEqual(len(timed_out), 1)
        self.assertEqual((self.folder / timed_out[0]['stdout']['path']).read_bytes(), b'synthetic partial output\n')
        self.assertEqual(trace['observations'][0]['status'], 'INCOMPLETE')


class PreflightInventoryControls(unittest.TestCase):
    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix='indicator-source-case-'))
        self.source = self.temp / 'source'
        shutil.copytree(c.HERE, self.source / 'tools/indicator_sampling')
        workflow = self.source / prepare.WORKFLOW
        workflow.parent.mkdir(parents=True)
        shutil.copyfile(c.HERE.parents[1] / prepare.WORKFLOW, workflow)
        self.here = self.source / 'tools/indicator_sampling'
        self.error = None

    def tearDown(self):
        target = EVIDENCE / self.id().split('.')[-1]
        target.mkdir()
        shutil.copyfile(self.here / 'runtime-files.json', target / 'actual-runtime-files.json')
        c.write_json(target / 'result.json', {'source_hashes_checked': True, 'observed_rejection': self.error,
            'synthetic_source_copy_only': True, 'android_executed': False})
        shutil.rmtree(self.temp)

    def check(self, mutate=None):
        if mutate:
            path = self.here / 'runtime-files.json'
            rows = c.json_file(path)
            mutate(rows)
            c.write_json(path, rows)
        with mock.patch.object(c, 'HERE', self.here):
            if mutate is None:
                return prepare.source_manifest(self.source)
            try:
                prepare.source_manifest(self.source)
            except c.Invalid as error:
                self.error = str(error)
            else:
                self.fail('Incomplete or changed source inventory was accepted')

    def test_complete_runtime_file_inventory(self):
        self.assertEqual(len(self.check()), len(prepare.OWN_FILES) + 2)

    def test_runtime_inventory_cannot_omit_hidden_workflow(self):
        self.check(lambda rows: rows.__setitem__(slice(None), [row for row in rows if row['path'] != prepare.WORKFLOW]))
        self.assertRegex(self.error, 'independently required inventory')

    def test_runtime_inventory_cannot_omit_recorder(self):
        self.check(lambda rows: rows.__setitem__(slice(None), [row for row in rows if not row['path'].endswith('/record.py')]))
        self.assertRegex(self.error, 'independently required inventory')

    def test_runtime_inventory_cannot_reorder_or_duplicate(self):
        self.check(lambda rows: rows.__setitem__(1, copy.deepcopy(rows[0])))
        self.assertRegex(self.error, 'independently required inventory')

    def test_runtime_inventory_cannot_change_a_source_hash(self):
        self.check(lambda rows: rows[1].__setitem__('sha256', '0' * 64))
        self.assertRegex(self.error, 'Actual diagnostic source differs')


class SyntheticTraceControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = EVIDENCE / 'complete-synthetic-baseline'
        cls.result, cls.clock, cls.device, cls.args = build_baseline(cls.baseline)

    def setUp(self):
        self.folder = Path(tempfile.mkdtemp(prefix='indicator-case-'))
        self.root = self.folder / 'experiment'
        shutil.copytree(self.baseline / 'experiment', self.root)
        self.before = snapshot(self.root)
        self.experiment = c.json_file(self.root / 'experiment.json')
        self.rejection = None

    def tearDown(self):
        target = EVIDENCE / self.id().split('.')[-1]
        target.mkdir()
        after = snapshot(self.root)
        changes = []
        for name in sorted(set(self.before) | set(after)):
            if self.before.get(name) != after.get(name):
                row = {'path': name, 'before': self.before.get(name), 'after': after.get(name)}
                if name in after:
                    saved = target / 'changed-files' / name
                    saved.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(self.root / name, saved)
                changes.append(row)
        c.write_json(target / 'case.json', {'synthetic_control_only': True,
            'base': '../complete-synthetic-baseline/experiment', 'changes': changes,
            'observed_rejection': self.rejection, 'android_executed': False})
        shutil.rmtree(self.folder)

    def rejected(self, pattern):
        c.write_json(self.root / 'experiment.json', self.experiment)
        try:
            verify.validate_prefix(self.root, self.experiment, MODULES, live=False)
        except Exception as error:
            self.rejection = type(error).__name__ + ': ' + str(error)
            self.assertIsInstance(error, (ValueError, KeyError))
            self.assertRegex(str(error), pattern)
        else:
            self.fail('Synthetic damaged evidence was accepted')

    def get_slot(self):
        return c.json_file(self.root / 'slot-01/slot.json')

    def artifact(self, row, data):
        (self.root / 'slot-01' / row['path']).write_bytes(data)
        row.update(c.identity(data))
        row['creation']['final_stat']['bytes'] = len(data)

    def close_slot(self, value):
        raw = c.bytes_json(value)
        self.artifact(self.experiment['slots'][0]['receipt'], raw)
        (self.root / 'slot-01/journal.json').write_bytes(raw)

    def change_observation_raw(self, value, shot, role, data):
        positions = {'pid_first': 0, 'foreground': 1, 'hierarchy': 3, 'screenshot': 5,
                     'foreground_final': 6, 'pid_final': 7}
        self.artifact(value['commands'][shot['commands'][positions[role]]]['stdout'], data)
        self.artifact(shot['artifacts'][role], data)

    def close_observation(self, value, shot, index):
        raw = c.bytes_json({key: item for key, item in shot.items() if key not in ('record_artifact', 'completed_ns')})
        self.artifact(shot['record_artifact'], raw)
        value['observations'][index] = copy.deepcopy(shot)
        self.close_slot(value)

    def test_complete_40_frames_and_92_different_pairs_are_diagnostic_complete(self):
        self.assertTrue(self.result['evidence_complete'])
        self.assertEqual((self.result['completed_slots'], self.result['post_input_frames'], self.result['measured_pairs']), (8, 40, 92))
        self.assertTrue(all(row['difference']['changed_pixels'] == 1 and row['xml_canonical_equal'] is False for row in self.result['pairs']))
        self.assertFalse(self.result['full_runtime_1_to_1_established'])
        self.assertEqual(self.result['new_runtime_parity_credit'], 0)
        replay = verify.verify_experiment(self.root, self.experiment, MODULES, live=False)
        self.assertEqual(replay, self.result)

    def test_changed_protocol_manifest_rejects(self):
        self.experiment['runtime_manifest_sha256'] = '0' * 64
        self.rejected('policy/source manifest')

    def test_reordered_install_slot_rejects(self):
        self.experiment['slots'][0]['index'] = 2
        self.rejected('directory/index')

    def test_extended_global_deadline_rejects(self):
        self.experiment['deadline_ns'] += 1
        self.rejected('reset or extended')

    def test_missing_toolchain_role_rejects(self):
        path = self.root / 'prerequisites/toolchain-inputs.json'
        rows = c.json_file(path); rows.pop()
        c.write_json(path, rows)
        entry = next(row for row in self.experiment['prerequisite_inputs'] if row['path'] == 'prerequisites/toolchain-inputs.json')
        entry.update(c.file_identity(path))
        self.rejected('toolchain role inventory')

    def test_unlisted_prerequisite_file_rejects(self):
        (self.root / 'prerequisites/extra.txt').write_text('undeclared')
        self.rejected('Unlisted or missing prerequisite')

    def test_borrowed_command_index_rejects(self):
        value = self.get_slot()
        value['slot']['samples'][0]['commands'][0] = value['slot']['initial']['commands'][0]
        self.close_slot(value)
        self.rejected('missing, borrowed, out of order')

    def test_dot_alias_stream_role_rejects(self):
        value = self.get_slot()
        value['commands'][0]['stdout']['path'] = './' + value['commands'][0]['stdout']['path']
        self.close_slot(value)
        self.rejected('another logical role')

    def test_actual_hardlink_alias_rejects_in_archive_mode(self):
        first = self.root / 'slot-01/command-00000.stderr'
        second = self.root / 'slot-01/command-00001.stderr'
        second.unlink(); os.link(first, second)
        self.rejected('physical alias')

    def test_missing_immutable_attempt_rejects(self):
        (self.root / 'slot-01/attempt-receipt.json').unlink()
        self.rejected('Missing, symbolic or unconfined')

    def test_journal_changed_after_closure_rejects(self):
        (self.root / 'slot-01/journal.json').write_bytes(b'{}\n')
        self.rejected('journal differs')

    def test_omitted_fixed_sample_rejects(self):
        value = self.get_slot(); value['slot']['samples'].pop()
        self.close_slot(value)
        self.rejected('five fixed samples')

    def test_changed_one_second_gap_rejects(self):
        value = self.get_slot(); value['slot']['gaps'][0]['requested_ns'] = 0
        self.close_slot(value)
        self.rejected('Fixed wait label, origin or duration')

    def test_changed_local_apk_identity_rejects_before_any_capture_credit(self):
        value = self.get_slot(); value['slot']['local_apk_before']['sha256'] = '0' * 64
        self.close_slot(value)
        self.rejected('Local APK')

    def test_changed_final_scale_rejects(self):
        value = self.get_slot()
        scale = value['slot']['scale_final']
        index = scale['commands'][0]
        self.artifact(value['commands'][index]['stdout'], b'1\n')
        scale['values']['animator_duration_scale'] = '1'
        self.close_slot(value)
        self.rejected('scale')

    def test_stale_sample_command_before_input_rejects(self):
        value = self.get_slot()
        index = value['slot']['samples'][0]['commands'][0]
        value['commands'][index]['started_ns'] = value['slot']['preinput']['started_ns']
        self.close_slot(value)
        self.rejected('command start')

    def test_unplanned_extra_input_argv_rejects(self):
        value = self.get_slot()
        index = value['slot']['samples'][0]['commands'][2]
        value['commands'][index]['argv'] = ['shell', 'input tap 640 1152']
        self.close_slot(value)
        self.rejected('command argv/bound')

    def test_consistent_new_pid_within_slot_rejects(self):
        value = self.get_slot(); shot = value['slot']['samples'][0]
        for role in ('pid_first', 'pid_final'):
            self.change_observation_raw(value, shot, role, b'77777\n')
        shot['pid'] = '77777'
        self.close_observation(value, shot, 2)
        self.rejected('Main process changed')

    def test_consistent_other_same_package_component_rejects(self):
        value = self.get_slot(); shot = value['slot']['samples'][0]
        component = c.PACKAGE + '/' + c.PACKAGE + '.AnotherActivity'
        for role in ('foreground', 'foreground_final'):
            self.change_observation_raw(value, shot, role, ('topResumedActivity: ' + component + '\n').encode())
        shot['component'] = component
        self.close_observation(value, shot, 2)
        self.rejected('foreground component changed')

    def test_initial_to_preinput_full_xml_difference_rejects(self):
        value = self.get_slot(); shot = value['slot']['preinput']['observation']
        path = self.root / 'slot-01' / shot['artifacts']['hierarchy']['path']
        tree = ET.fromstring(path.read_bytes())
        node = next(n for n in tree.iter('node') if n.get('resource-id') == c.PACKAGE + ':id/button_skip')
        node.set('text', 'synthetic different preinput leaf')
        self.change_observation_raw(value, shot, 'hierarchy', ET.tostring(tree))
        self.close_observation(value, shot, 1)
        self.rejected('Complete initial/preinput XML changed')

    def test_repaired_slot_cannot_retry_after_reserved_preflight_failure(self):
        # Use a separate zero-slot prefix; its source/APK preflight is explicitly
        # mocked to fail before any device action. No application operation runs.
        experiment = copy.deepcopy(self.experiment)
        experiment.update(slots=[], unattempted_indices=list(range(1, 9)), status='READY_FOR_FIXED_SLOTS')
        for path in self.root.glob('slot-*'):
            shutil.rmtree(path)
        c.write_json(self.root / 'experiment.json', experiment)
        args = copy.copy(self.args); args.output = self.root; args.slot = 1
        with mock.patch.object(prepare, 'verify_preparation', side_effect=c.Invalid('synthetic fixed input failure')):
            with self.assertRaisesRegex(c.Invalid, 'synthetic fixed input failure'):
                record.one_slot(args)
        failed = c.json_file(self.root / 'experiment.json')
        self.assertEqual(failed['status'], 'FAILED_SLOT_PREFLIGHT_NO_CONTINUATION')
        self.assertEqual(failed['unattempted_indices'], list(range(2, 9)))
        with mock.patch.object(prepare, 'verify_preparation', return_value={}) as repaired:
            with self.assertRaisesRegex(c.Invalid, 'cannot receive another install'):
                record.one_slot(args)
            repaired.assert_not_called()
        self.rejection = 'PREFLIGHT_FAILED_NO_CONTINUATION; repaired retry rejected before its preflight'

    def test_deadline_includes_fixed_pair_finalization(self):
        self.experiment['finalization']['finished_ns'] = self.experiment['deadline_ns'] + 1
        self.experiment['finished_ns'] = self.experiment['finalization']['finished_ns']
        with mock.patch.object(verify, 'validate_prefix', return_value={'slots': [], 'errors': [],
                'verified_artifact_roles': 0, 'verified_original_host_inodes': 0, 'verified_remote_xml_names': 0}):
            result = verify.verify_experiment(self.root, self.experiment, MODULES, live=False)
        self.assertFalse(result['evidence_complete'])
        self.assertTrue(any(row.get('boundary') == 'global-finalization' for row in result['errors']))
        self.rejection = 'global-finalization rejected recorded completion beyond the original global deadline'


if __name__ == '__main__':
    unittest.main(verbosity=2)
