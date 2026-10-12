#!/usr/bin/env python3
"""Host regressions using the preserved failed-run signal observations.

ADB and time are simulated here. These tests do not establish device configuration
or app equivalence; a subsequent hosted emulator run provides that evidence.
"""
from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import configure_capture_device as helper


EVIDENCE = (Path(__file__).resolve().parents[2] / 'docs' / 'verification' /
            'android-ci-bebf448' / 'capture-device')
RECORDED = json.loads((EVIDENCE / 'capture-device.json').read_text())
SIGNALS = [x['signals'][0] for x in RECORDED['signal_observations']]


class CaptureSignalStabilityTests(unittest.TestCase):
    def run_helper(self, lines: list[str], *, disable_animations: bool = False,
                   ignored_animation_write: str | None = None) -> tuple[int, dict]:
        """Exercise the actual main loop with recorded responses and a fake clock."""
        elapsed = 0.0
        telephony_calls = 0
        animation_scales = {key: '1.0' for key in helper.ANIMATION_SCALE_KEYS}
        responses = {tuple(x['argv'][3:]): (EVIDENCE / x['stdout']['path']).read_text()
                     for x in RECORDED['commands']}

        def sleep(seconds: float) -> None:
            nonlocal elapsed
            elapsed += seconds

        clock = SimpleNamespace(monotonic=lambda: elapsed, sleep=sleep,
                                strftime=time.strftime, gmtime=lambda: time.gmtime(elapsed))

        def adb(argv: list[str], **kwargs) -> subprocess.CompletedProcess:
            nonlocal telephony_calls
            command = tuple(argv[3:])
            if command == ('shell', 'dumpsys', 'telephony.registry'):
                # The first registry call precedes the stability sampling window.
                stdout = (SIGNALS[0]['registry_line'] if telephony_calls == 0 else
                          lines[min(telephony_calls - 1, len(lines) - 1)]) + '\n'
                telephony_calls += 1
            elif command[:4] == ('shell', 'settings', 'get', 'global') and command[4] in animation_scales:
                stdout = animation_scales[command[4]] + '\n'
            elif command[:4] == ('shell', 'settings', 'put', 'global') and command[4] in animation_scales:
                if command[4] != ignored_animation_write:
                    animation_scales[command[4]] = command[5]
                stdout = ''
            else:
                stdout = responses[command]
            return subprocess.CompletedProcess(argv, 0, stdout, '')

        with tempfile.TemporaryDirectory(prefix='macrodroid-signal-regression-') as directory:
            output = Path(directory) / 'capture-device'
            argv = ['configure_capture_device.py', '--output', str(output)]
            if disable_animations:
                argv.append('--disable-animations')
            with (patch.object(sys, 'argv', argv), patch.object(helper, 'time', clock),
                  patch.object(helper.subprocess, 'run', adb), redirect_stdout(io.StringIO())):
                result = helper.main()
            report = json.loads((output / 'capture-device.json').read_text())
        return result, report

    def test_recorded_raw_variation_keeps_primary_level_stable(self) -> None:
        result, report = self.run_helper([x['registry_line'] for x in SIGNALS])
        self.assertEqual(result, 0)
        self.assertEqual(report['status'], 'CAPTURE_DEVICE_CONFIGURED')
        self.assertEqual(report['signal_stability_fields'], ['primary', 'level'])
        self.assertEqual(report['signal_stable_seconds'], 15)
        observed = report['signal_observations']
        self.assertEqual(len(observed), 5)
        self.assertEqual([x['signals'][0] for x in observed], SIGNALS[:5])
        wcdma_measurements = {x['signals'][0]['primary_measurements'] for x in observed[1:]}
        self.assertGreater(len(wcdma_measurements), 1)
        self.assertFalse(report['disable_animations_requested'])
        self.assertEqual(report['before']['animation_scales'], report['after']['animation_scales'])
        self.assertFalse(any(x['label'].startswith('disable-') for x in report['commands']))

    def test_level_drop_restarts_the_fifteen_second_window(self) -> None:
        strong = SIGNALS[1]['registry_line']
        weak = strong.replace(SIGNALS[1]['primary_measurements'],
                              SIGNALS[1]['primary_measurements'].replace('level=4', 'level=3'))
        result, report = self.run_helper([strong, strong, weak, strong, strong, strong, strong])
        self.assertEqual(result, 0)
        self.assertEqual(len(report['signal_observations']), 7)
        self.assertEqual(report['signal_stable_seconds'], 15)

    def test_primary_radio_change_restarts_the_fifteen_second_window(self) -> None:
        wcdma, lte = SIGNALS[1]['registry_line'], SIGNALS[0]['registry_line']
        result, report = self.run_helper([wcdma, wcdma, lte, lte, lte, lte])
        self.assertEqual(result, 0)
        self.assertEqual(len(report['signal_observations']), 6)
        self.assertEqual(report['confirmed_primary_signal']['primary'], 'CellSignalStrengthLte')
        self.assertEqual(report['signal_stable_seconds'], 15)

    def test_missing_or_multiple_modems_fail_at_the_deadline(self) -> None:
        duplicate = SIGNALS[1]['registry_line'] + '\n' + SIGNALS[1]['registry_line']
        for line in ('', duplicate):
            with self.subTest(registry=line[:50]):
                result, report = self.run_helper([line])
                self.assertEqual(result, 2)
                self.assertEqual(report['status'], 'CAPTURE_DEVICE_CONFIGURATION_FAILED')
                self.assertEqual(len(report['signal_observations']), 18)
                self.assertIn('within the deadline', report['failure'])

    def test_completion_rejects_a_primary_radio_handoff(self) -> None:
        wcdma, lte = SIGNALS[1]['registry_line'], SIGNALS[0]['registry_line']
        result, report = self.run_helper([wcdma, wcdma, wcdma, wcdma, lte])
        self.assertEqual(result, 2)
        self.assertEqual(len(report['signal_observations']), 4)
        self.assertIn('changed at configuration completion', report['failure'])

    def test_requested_animation_scales_are_recorded_and_verified(self) -> None:
        result, report = self.run_helper([x['registry_line'] for x in SIGNALS], disable_animations=True)
        self.assertEqual(result, 0)
        self.assertTrue(report['disable_animations_requested'])
        self.assertTrue(report['requested_animation_scales_observed'])
        self.assertEqual(report['before']['animation_scales'], {key: '1.0' for key in helper.ANIMATION_SCALE_KEYS})
        self.assertEqual(report['after']['animation_scales'], {key: '0' for key in helper.ANIMATION_SCALE_KEYS})
        writes = [x['argv'][3:] for x in report['commands'] if x['label'].startswith('disable-')]
        self.assertEqual(writes, [['shell', 'settings', 'put', 'global', key, '0'] for key in helper.ANIMATION_SCALE_KEYS])
        self.assertFalse(report['animation_timing_and_motion_parity_tested'])

    def test_unobserved_animation_scale_change_fails(self) -> None:
        for key in helper.ANIMATION_SCALE_KEYS:
            with self.subTest(setting=key):
                result, report = self.run_helper([x['registry_line'] for x in SIGNALS],
                                                 disable_animations=True, ignored_animation_write=key)
                self.assertEqual(result, 2)
                self.assertFalse(report['requested_animation_scales_observed'])
                self.assertEqual(report['after']['animation_scales'][key], '1.0')
                self.assertIn('zero animation scales were not observed', report['failure'])


if __name__ == '__main__':
    unittest.main()
