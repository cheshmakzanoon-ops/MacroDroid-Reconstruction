"""Host controls with simulated ADB only; all raw evidence is retained if asked."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import enable_still_animations as diagnostic


class Simulation:
    def __init__(self, edit=None):
        self.calls = []
        self.edit = edit

    def __call__(self, argv, **kwargs):
        number = len(self.calls)
        label, expected_args, outputs = diagnostic.specification()[number]
        assert argv[1:] == ['-s', diagnostic.SERIAL, *expected_args]
        self.calls.append(argv)
        value = outputs[0] if outputs is not None else b'1.0\n'
        code, error = 0, b''
        if self.edit:
            code, value, error = self.edit(label, code, value, error)
        return subprocess.CompletedProcess(argv, code, value, error)


class AnimationControls(unittest.TestCase):
    def setUp(self):
        parent = os.environ.get('ANIMATION_CONTROL_EVIDENCE')
        if parent:
            root = Path(parent).resolve()
            root.mkdir(parents=True, exist_ok=True)
            self.root = Path(tempfile.mkdtemp(prefix=self._testMethodName + '-', dir=root))
        else:
            self.temp = tempfile.TemporaryDirectory()
            self.addCleanup(self.temp.cleanup)
            self.root = Path(self.temp.name)
        self.adb = self.root / 'simulated-adb'
        self.adb.write_bytes(b'Synthetic command identity only; this file is not executed.\n')
        self.count = 0

    def execute(self, edit=None, serial=diagnostic.SERIAL):
        self.count += 1
        folder = self.root / ('case-' + str(self.count))
        args = argparse.Namespace(adb=str(self.adb), serial=serial, output=folder)
        simulator = Simulation(edit)
        code = diagnostic.run(args, simulator)
        report = json.loads((folder / 'animation-scales.json').read_text())
        return code, report, simulator, folder

    def test_complete_exact_lf_sequence_verifies_all_three_scale_readbacks(self):
        code, report, simulator, folder = self.execute()
        self.assertEqual(code, 0, report)
        self.assertEqual(report['status'], 'SIMULATED_ANIMATION_SCALE_ZERO_VERIFIED')
        self.assertFalse(report['android_executed'])
        self.assertEqual(len(simulator.calls), 19)
        self.assertEqual(diagnostic.verify_report(folder, report), {key: '0' for key in diagnostic.SCALES})
        self.assertFalse(report['apks_modified'])
        self.assertFalse(report['screenshots_modified'])
        self.assertFalse(report['comparison_rules_changed'])

    def test_independent_literal_nineteen_command_zero_scale_sequence(self):
        code, report, simulator, _ = self.execute()
        expected = [
            ['get-state'],
            ['shell', 'getprop', 'ro.kernel.qemu'],
            ['shell', 'getprop', 'sys.boot_completed'],
            ['shell', 'getprop', 'ro.build.version.sdk'],
            ['shell', 'getprop', 'ro.build.fingerprint'],
            ['emu', 'avd', 'name'],
            ['shell', 'settings', 'get', 'global', 'animator_duration_scale'],
            ['shell', 'settings', 'get', 'global', 'window_animation_scale'],
            ['shell', 'settings', 'get', 'global', 'transition_animation_scale'],
            ['shell', 'settings', 'put', 'global', 'animator_duration_scale', '0'],
            ['shell', 'settings', 'put', 'global', 'window_animation_scale', '0'],
            ['shell', 'settings', 'put', 'global', 'transition_animation_scale', '0'],
            ['shell', 'settings', 'get', 'global', 'animator_duration_scale'],
            ['shell', 'settings', 'get', 'global', 'window_animation_scale'],
            ['shell', 'settings', 'get', 'global', 'transition_animation_scale'],
            ['shell', 'getprop', 'ro.kernel.qemu'],
            ['shell', 'getprop', 'sys.boot_completed'],
            ['shell', 'getprop', 'ro.build.version.sdk'],
            ['shell', 'getprop', 'ro.build.fingerprint'],
        ]
        self.assertEqual(code, 0, report)
        self.assertEqual([row[3:] for row in simulator.calls], expected)
        self.assertEqual(report['requested_scales'], {
            'animator_duration_scale': '0', 'window_animation_scale': '0',
            'transition_animation_scale': '0'})
        self.assertEqual(report['observed_scales'], report['requested_scales'])

    def test_crlf_console_and_shell_lines_are_exactly_supported(self):
        code, report, _, folder = self.execute(lambda label, code, out, err: (code, out.replace(b'\n', b'\r\n'), err))
        self.assertEqual(code, 0, report)
        diagnostic.verify_report(folder, report)

    def test_wrong_serial_stops_before_any_adb(self):
        code, report, simulator, _ = self.execute(serial='emulator-5554')
        self.assertEqual(code, 2)
        self.assertEqual(simulator.calls, [])

    def test_each_device_identity_failure_stops_before_any_setting_write(self):
        for label in ('device-state', 'emulator', 'boot', 'sdk', 'fingerprint', 'avd-name'):
            with self.subTest(label=label):
                code, report, simulator, _ = self.execute(lambda name, code, out, err:
                    (code, b'other\n' if name == label else out, err))
                self.assertEqual(code, 2, report)
                self.assertTrue(all('put' not in argv for argv in simulator.calls))

    def test_final_device_identity_drift_rejects_completed_configuration(self):
        for label in ('final-emulator', 'final-boot', 'final-sdk', 'final-fingerprint'):
            with self.subTest(label=label):
                code, report, _, _ = self.execute(lambda name, code, out, err:
                    (code, b'changed\n' if name == label else out, err))
                self.assertEqual(code, 2, report)

    def test_every_scale_readback_must_equal_zero(self):
        for key in diagnostic.SCALES:
            with self.subTest(key=key):
                code, report, _, _ = self.execute(lambda label, code, out, err:
                    (code, b'1\n' if label == 'after-' + key else out, err))
                self.assertEqual(code, 2, report)

    def test_nonzero_boolean_diagnostic_and_malformed_avd_outputs_are_rejected(self):
        changes = [(7, b'device\n', b''), (False, b'device\n', b''),
                   (0, b'device\n', b'warning\n'), (0, b'device\nextra\n', b'')]
        for change in changes:
            with self.subTest(change=change):
                code, report, simulator, _ = self.execute(lambda label, code, out, err:
                    change if label == 'device-state' else (code, out, err))
                self.assertEqual(code, 2, report)
                self.assertEqual(len(simulator.calls), 1)
        for output in [(diagnostic.AVD + '\r\nOK\n').encode(), (diagnostic.AVD + '\nOK').encode(),
                       (diagnostic.AVD + '\nOK\n\n').encode(), b'\xff\nOK\n']:
            with self.subTest(avd=output):
                code, report, simulator, _ = self.execute(lambda label, code, out, err:
                    (code, output if label == 'avd-name' else out, err))
                self.assertEqual(code, 2, report)
                self.assertTrue(all('put' not in argv for argv in simulator.calls))

    def test_rehashed_stream_changes_and_endpoint_artifact_reuse_are_rejected(self):
        _, original, _, folder = self.execute()
        row = original['commands'][12]
        path = folder / row['stdout']['path']
        previous = path.read_bytes()
        path.write_bytes(b'1\n')
        changed = copy.deepcopy(original)
        changed['commands'][12]['stdout'].update(diagnostic.digest(path))
        with self.assertRaises(diagnostic.EvidenceError):
            diagnostic.verify_report(folder, changed)
        path.write_bytes(previous)
        for kind in ('copy-before', 'dot-alias', 'symlink'):
            changed = copy.deepcopy(original)
            record = changed['commands'][12]['stdout']
            if kind == 'copy-before':
                changed['commands'][12]['stdout'] = copy.deepcopy(changed['commands'][6]['stdout'])
            elif kind == 'dot-alias':
                record['path'] = './' + record['path']
            else:
                path.unlink()
                saved = folder / 'aliased-output.txt'
                saved.write_bytes(previous)
                path.symlink_to(saved)
            with self.subTest(kind=kind), self.assertRaises(diagnostic.EvidenceError):
                diagnostic.verify_report(folder, changed)

    def test_reordered_commands_changed_scope_and_stale_times_are_rejected(self):
        _, original, _, folder = self.execute()
        for kind in ('order', 'argv', 'boolean-code', 'source-hash', 'scope', 'time', 'count'):
            changed = copy.deepcopy(original)
            if kind == 'order':
                changed['commands'][6:8] = reversed(changed['commands'][6:8])
            elif kind == 'argv':
                changed['commands'][9]['argv'][-1] = '1'
            elif kind == 'boolean-code':
                changed['commands'][0]['exit_code'] = False
            elif kind == 'source-hash':
                changed['source_sha256'] = '0' * 64
            elif kind == 'scope':
                changed['comparison_rules_changed'] = True
            elif kind == 'time':
                changed['commands'][-1]['started_monotonic'] = changed['started_monotonic'] - 1
            else:
                changed['commands'].pop()
            with self.subTest(kind=kind), self.assertRaises(diagnostic.EvidenceError):
                diagnostic.verify_report(folder, changed)


if __name__ == '__main__':
    unittest.main()
