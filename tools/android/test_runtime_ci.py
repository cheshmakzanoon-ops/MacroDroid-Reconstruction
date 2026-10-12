"""Host orchestration controls with simulated processes and comparator reports.

These tests establish process/result handling, never Android or app parity.
The independent ART artifact verifier is tested in test_constructor_probe.py.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

import run_ci_runtime as ci


class SimulatedService:
    def __init__(self, exit_code=0):
        self.returncode = None
        self.exit_code = exit_code

    def poll(self):
        return self.returncode

    def wait(self, timeout):
        self.returncode = self.exit_code
        return self.returncode


class SimulatedPipeline:
    def __init__(self, args, *, boot=0, configuration=0, art=0, captured=0,
                 comparison_change=None, malformed_art=False, service_exit=0):
        self.args = args
        self.boot, self.configuration, self.art, self.captured = boot, configuration, art, captured
        self.comparison_change = comparison_change or {}
        self.malformed_art = malformed_art
        self.commands = []
        self.capture_called = False
        self.service = SimulatedService(service_exit)

    def start(self, argv, **kwargs):
        self.commands.append(argv)
        return self.service

    def write(self, relative, value):
        path = self.args.output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value) + '\n')

    def __call__(self, argv, **kwargs):
        self.commands.append(argv)
        names = [Path(value).name for value in argv]
        code = 0
        if 'wait_android_ready.py' in names:
            self.write('environment/runtime-status.json', {
                'state': 'ready' if self.boot == 0 else 'booting', 'serial': ci.SERIAL, 'avd': ci.DEFAULT_AVD,
                'properties': dict(ci.EXPECTED_DEVICE),
            })
            code = self.boot
        elif 'configure_capture_device.py' in names:
            self.write('capture-device/capture-device.json', {
                'status': 'CAPTURE_DEVICE_CONFIGURED' if self.configuration == 0 else 'FAILED',
                'serial': ci.SERIAL, 'expected_avd': ci.DEFAULT_AVD, 'demo_clock_requested': '1200',
                'disable_animations_requested': True, 'requested_animation_scales_observed': True,
            })
            code = self.configuration
        elif 'android_constructor_probe.py' in names:
            self.write('constructor-probe/probe-result.json', {
                'status': 'ART_CONSTRUCTOR_ALLOCATION_VERIFIED' if self.art == 0 else 'ART_CONSTRUCTOR_PROBE_FAILED',
                'cleanup_complete': True, 'simulated_verifier_accepts': self.art == 0,
            })
            if self.malformed_art:
                (self.args.output / 'constructor-probe/probe-result.json').write_text('{incomplete')
            code = self.art
        elif 'android_acceptance.py' in names:
            self.capture_called = True
            if '--intro-pages' not in argv or '--post-intro' not in argv:
                raise AssertionError('The entire requested capture scope must be enabled')
            code = self.captured
        else:
            for prefix, label, script, filename, flag, status in ci.COMPARISONS:
                if script not in names:
                    continue
                value = {
                    flag: self.capture_called, 'status': status if self.capture_called else 'REJECTED',
                    'android_runtime_executed': self.capture_called,
                    'installed_apk_identities_verified': self.capture_called,
                    'complete_intro_sequences_observed': self.capture_called,
                    'complete_post_intro_captures_observed': self.capture_called,
                    'apk_sha256': [ci.ORIGINAL_SHA256, ci.digest(self.args.candidate)],
                }
                change = self.comparison_change.get(prefix, {})
                value.update(change.get('fields', {}))
                code = change.get('exit_code', 0 if self.capture_called else 2)
                if not change.get('missing'):
                    self.write('capture/' + filename, value)
                    if change.get('malformed'):
                        (self.args.output / 'capture' / filename).write_text('[')
                if change.get('os_error'):
                    raise OSError('Simulated comparator launch failure')
                break
            else:
                raise AssertionError('Unexpected subprocess: ' + repr(argv))
        kwargs['stdout'].write(b'Simulated host control output only\n')
        return subprocess.CompletedProcess(argv, code)


class RuntimeCITests(unittest.TestCase):
    def execute(self, **changes):
        temp = tempfile.TemporaryDirectory(prefix='runtime-ci-host-control-')
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        original, candidate = root / 'original.apk', root / 'candidate.apk'
        original.write_bytes(b'original synthetic fixture')
        candidate.write_bytes(b'candidate synthetic fixture')
        args = argparse.Namespace(tooling=root / 'tooling', source=root / 'source', original=original,
            candidate=candidate, output=root / 'result', acceleration='on')
        pipeline = SimulatedPipeline(args, **changes)
        real_digest = ci.digest

        def digest(path):
            return ci.ORIGINAL_SHA256 if path == original else real_digest(path)

        def simulated_verification(folder, proof, **kwargs):
            if proof.get('simulated_verifier_accepts') is not True:
                raise ValueError('Simulated ART evidence rejected')
            return True

        with mock.patch.object(ci, 'digest', side_effect=digest), \
                mock.patch.object(ci, 'verify_result', side_effect=simulated_verification), \
                contextlib.redirect_stdout(io.StringIO()):
            code, report = ci.run_ci(args, runner=pipeline, starter=pipeline.start)
        self.assertEqual(json.loads((args.output / 'runtime-run.json').read_text()), report)
        self.assertTrue((args.output / 'environment/queue/STOP').exists())
        self.assertEqual(pipeline.service.returncode, changes.get('service_exit', 0))
        compared = [Path(command[1]).name for command in pipeline.commands if len(command) > 1 and
                    Path(command[1]).name in {entry[2] for entry in ci.COMPARISONS}]
        self.assertEqual(compared, [entry[2] for entry in ci.COMPARISONS])
        self.assertFalse(report['full_runtime_1_to_1_established'])
        self.assertFalse(report['animation_parity_established'])
        return code, report, pipeline

    def test_all_independent_reports_are_required_for_requested_gate(self):
        code, report, pipeline = self.execute()
        self.assertEqual(code, 0)
        self.assertTrue(report['requested_capture_gate_passed'])
        self.assertTrue(report['constructor_probe_gate_passed'])
        self.assertTrue(report['all_requested_runtime_checks_passed'])

    def test_art_failure_preserves_successful_capture_scope(self):
        code, report, pipeline = self.execute(art=2)
        self.assertEqual(code, 2)
        self.assertTrue(pipeline.capture_called)
        self.assertTrue(report['requested_capture_gate_passed'])
        self.assertFalse(report['constructor_probe_gate_passed'])

    def test_malformed_art_report_still_permits_capture_and_comparisons(self):
        code, report, pipeline = self.execute(malformed_art=True)
        self.assertEqual(code, 2)
        self.assertTrue(report['requested_capture_gate_passed'])
        self.assertFalse(report['constructor_probe_gate_passed'])
        self.assertIn('constructor_probe', report['report_errors'])

    def test_later_post_intro_failure_preserves_cold_and_intro_scopes(self):
        code, report, pipeline = self.execute(captured=2, comparison_change={
            'post_intro': {'exit_code': 2, 'fields': {'post_intro_surface_equal': False, 'status': 'REJECTED',
                                                   'complete_post_intro_captures_observed': False}},
        })
        self.assertEqual(code, 2)
        self.assertTrue(report['cold_launch_capture_equal'])
        self.assertTrue(report['intro_sequence_equal'])
        self.assertFalse(report['post_intro_surface_equal'])
        self.assertFalse(report['requested_capture_gate_passed'])

    def test_nonzero_recorder_cannot_be_overruled_by_comparator_booleans(self):
        code, report, pipeline = self.execute(captured=124)
        self.assertEqual(code, 2)
        self.assertTrue(report['post_intro_surface_equal'])
        self.assertFalse(report['requested_capture_gate_passed'])

    def test_malformed_or_missing_earlier_report_never_skips_later_comparators(self):
        for change in [{'malformed': True}, {'missing': True}, {'os_error': True}]:
            with self.subTest(change=change):
                code, report, pipeline = self.execute(comparison_change={'cold_launch': change})
                self.assertEqual(code, 2)
                self.assertFalse(report['cold_launch_capture_equal'])
                self.assertTrue(report['intro_sequence_equal'])
                self.assertTrue(report['post_intro_surface_equal'])

    def test_positive_boolean_with_wrong_status_exit_or_identity_is_rejected(self):
        cases = [{'exit_code': 1}, {'fields': {'status': 'REJECTED'}},
                 {'fields': {'apk_sha256': [ci.ORIGINAL_SHA256, '0' * 64]}},
                 {'fields': {'post_intro_surface_equal': 1}},
                 {'fields': {'complete_post_intro_captures_observed': False}}]
        for change in cases:
            with self.subTest(change=change):
                code, report, pipeline = self.execute(comparison_change={'post_intro': change})
                self.assertEqual(code, 2)
                self.assertFalse(report['post_intro_surface_equal'])
                self.assertTrue(report['cold_launch_capture_equal'])
                self.assertTrue(report['intro_sequence_equal'])

    def test_boot_or_configuration_failure_still_produces_three_rejections(self):
        for change in [{'boot': 2}, {'configuration': 2}]:
            with self.subTest(change=change):
                code, report, pipeline = self.execute(**change)
                self.assertEqual(code, 2)
                self.assertFalse(pipeline.capture_called)
                self.assertFalse(report['android_runtime_executed'])
                self.assertFalse(report['constructor_probe_gate_passed'])
                self.assertFalse(report['requested_capture_gate_passed'])

    def test_service_failure_is_independent_of_successful_measured_scopes(self):
        code, report, pipeline = self.execute(service_exit=1)
        self.assertEqual(code, 2)
        self.assertTrue(report['requested_capture_gate_passed'])
        self.assertTrue(report['constructor_probe_gate_passed'])
        self.assertIn('runtime-service-exit', report['failures'])


if __name__ == '__main__':
    unittest.main()
