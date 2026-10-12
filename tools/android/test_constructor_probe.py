"""Host controls for the pinned ART helper; every ADB response is simulated."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest
from unittest import mock

import android_constructor_probe as probe


class SimulatedADB:
    def __init__(self, *, property_change=None, avd=None, device_hash=None,
                 art_code=0, art_stderr='', timeout=False, cleanup_failure=False):
        self.properties = dict(probe.EXPECTED_DEVICE)
        self.properties.update(property_change or {})
        self.avd = avd or probe.DEFAULT_AVD
        self.device_hash = device_hash
        self.art_code, self.art_stderr = art_code, art_stderr
        self.timeout, self.cleanup_failure = timeout, cleanup_failure
        self.commands, self.owned, self.executions = [], None, 0

    def __call__(self, argv, **kwargs):
        self.commands.append(argv)
        code, out, err = 0, '', ''
        if argv[3:] == ['get-state']:
            out = 'device\n'
        elif argv[3:6] == ['emu', 'avd', 'name']:
            out = self.avd + '\nOK\n'
        elif argv[3] == 'push':
            out = '1 file pushed\n'
        elif argv[3] == 'shell':
            command = shlex.split(argv[4])
            if command[0] == 'getprop':
                out = self.properties[command[1]] + '\n'
            elif command[0] == 'mkdir':
                self.owned = command[-1]
            elif command[0] == 'sha256sum':
                target = command[-1]
                value = ('a' * 64 if target == probe.VM else
                         probe.PROBE_SHA256 if target.endswith('.dex') else probe.ORIGINAL_SHA256)
                out = (self.device_hash if target.endswith('.dex') and self.device_hash else value) + '  ' + target + '\n'
            elif command[0] == 'stat':
                out = '444\n'
            elif command[0] == probe.GUEST_TIMEOUT:
                self.executions += 1
                if self.timeout:
                    raise subprocess.TimeoutExpired(argv, kwargs['timeout'], output=b'partial output\n')
                code, out, err = self.art_code, probe.EXPECTED_STDOUT + '\n', self.art_stderr
            elif command[0] == 'rm':
                if command != ['rm', '-rf', '--', self.owned]:
                    raise AssertionError('Cleanup escaped the freshly owned directory')
                if self.cleanup_failure:
                    code, err = 1, 'Permission denied\n'
        return subprocess.CompletedProcess(argv, code, out.encode(), err.encode())


class ConstructorProbeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='constructor-host-control-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.adb = self.root / 'adb'
        self.adb.write_text('simulated executable only\n')
        self.original = self.root / 'original.apk'
        self.original.write_bytes(b'host fixture; not an APK')
        self.args = argparse.Namespace(adb=str(self.adb), serial='emulator-5560', avd=probe.DEFAULT_AVD,
            original=self.original, probe=probe.ROOT / 'probes/constructor-probe.dex',
            provenance=probe.ROOT / 'probes/constructor-probe.json', output=self.root / 'result', timeout=120)
        self.inputs = {
            'original': {'path': str(self.original), 'bytes': probe.ORIGINAL_BYTES, 'sha256': probe.ORIGINAL_SHA256},
            'probe': {'path': str(self.args.probe), **probe.validate_probe(self.args.probe.read_bytes())},
            'provenance': {'path': str(self.args.provenance), 'sha256': probe.digest(self.args.provenance),
                           'content': json.loads(self.args.provenance.read_text())},
        }

    def execute(self, adb=None):
        adb = adb or SimulatedADB()
        with mock.patch.object(probe, 'validate_inputs', return_value=copy.deepcopy(self.inputs)), \
                mock.patch.object(probe.shutil, 'which', return_value=str(self.adb)):
            result = probe.run_probe(self.args, runner=adb)
        return (*result, adb)

    def test_exact_committed_dex_has_one_runtime_class_and_no_stubs(self):
        info = probe.validate_probe(self.args.probe.read_bytes())
        self.assertEqual((info['runtime_class_count'], info['runtime_class']), (1, probe.PROBE_CLASS))
        self.assertEqual(info['compile_only_stub_classes_in_probe'], 0)
        with self.assertRaises(probe.ProbeError):
            probe.validate_probe(self.args.probe.read_bytes()[:-1] + b'!')

    def test_wrong_original_stops_before_any_adb_command(self):
        adb = SimulatedADB()
        code, report = probe.run_probe(self.args, runner=adb)
        self.assertEqual(code, 2)
        self.assertFalse(report['art_execution_attempted'])
        self.assertEqual(adb.commands, [])

    def test_success_requires_pinned_device_inputs_and_verified_vm(self):
        code, report, adb = self.execute()
        self.assertEqual(code, 0)
        self.assertTrue(probe.verify_result(self.args.output, report, serial=self.args.serial))
        self.assertTrue(report['cleanup_complete'])
        self.assertEqual(adb.executions, 1)
        self.assertIn('-Xverify:all', report['art_argv'])
        self.assertEqual(report['art_argv'][:4], [probe.GUEST_TIMEOUT, '-s', 'KILL', '120'])
        self.assertFalse(report['app_installed'])
        self.assertFalse(report['full_runtime_1_to_1_established'])

    def test_wrong_device_fingerprint_stops_before_push(self):
        code, report, adb = self.execute(SimulatedADB(property_change={'ro.build.fingerprint': 'wrong-image'}))
        self.assertEqual(code, 2)
        self.assertFalse(report['art_execution_attempted'])
        self.assertFalse(any(command[3] == 'push' for command in adb.commands))

    def test_other_avd_stops_before_device_mutation(self):
        code, report, adb = self.execute(SimulatedADB(avd='Personal_AVD'))
        self.assertEqual(code, 2)
        self.assertIsNone(adb.owned)
        self.assertFalse(report['constructor_allocation_on_art_verified'])

    def test_device_checksum_mismatch_stops_vm_and_cleans_owned_files(self):
        code, report, adb = self.execute(SimulatedADB(device_hash='0' * 64))
        self.assertEqual(code, 2)
        self.assertEqual(adb.executions, 0)
        self.assertTrue(report['cleanup_complete'])

    def test_zero_exit_and_success_marker_cannot_hide_art_error(self):
        code, report, adb = self.execute(SimulatedADB(art_stderr='java.lang.VerifyError: rejected constructor\n'))
        self.assertEqual(code, 2)
        self.assertTrue(report['android_runtime_executed'])
        self.assertFalse(report['constructor_allocation_on_art_verified'])
        self.assertTrue(report['cleanup_complete'])

    def test_timeout_preserves_partial_art_output_and_cleans_owned_files(self):
        code, report, adb = self.execute(SimulatedADB(timeout=True))
        self.assertEqual(code, 2)
        self.assertTrue(report['art_command']['timed_out'])
        self.assertEqual((self.args.output / report['art_command']['stdout']['path']).read_bytes(), b'partial output\n')
        self.assertTrue(report['cleanup_complete'])
        self.assertFalse(report['constructor_allocation_on_art_verified'])

    def test_cleanup_failure_keeps_observed_allocation_but_fails_helper(self):
        code, report, adb = self.execute(SimulatedADB(cleanup_failure=True))
        self.assertEqual(code, 2)
        self.assertEqual(report['status'], 'ART_CONSTRUCTOR_VERIFIED_CLEANUP_FAILED')
        self.assertTrue(probe.verify_result(self.args.output, report, serial=self.args.serial))
        self.assertFalse(report['cleanup_complete'])

    def test_modified_command_output_and_missing_nested_proof_are_rejected(self):
        code, report, adb = self.execute()
        for mutation in ['output', 'provenance', 'wrong_original', 'disabled_verifier']:
            with self.subTest(mutation=mutation):
                changed = copy.deepcopy(report)
                if mutation == 'output':
                    changed['art_command']['stdout']['sha256'] = '0' * 64
                elif mutation == 'provenance':
                    changed['inputs']['provenance']['content'] = None
                elif mutation == 'wrong_original':
                    changed['device_inputs']['original']['sha256'] = '0' * 64
                else:
                    changed['art_argv'][5] = '-Xverify:none'
                with self.assertRaises(probe.ProbeError):
                    probe.verify_result(self.args.output, changed, serial=self.args.serial)

    def test_output_predicate_rejects_nonzero_extra_text_and_runtime_exception(self):
        self.assertTrue(probe.successful_output(0, probe.EXPECTED_STDOUT + '\n', 'W/art: benign diagnostic\n'))
        for code, stdout, stderr in [(1, probe.EXPECTED_STDOUT, ''), (False, probe.EXPECTED_STDOUT, ''),
                (0, probe.EXPECTED_STDOUT + '\nextra\n', ''), (0, probe.EXPECTED_STDOUT, 'java.lang.RuntimeException: failed')]:
            with self.subTest(code=code, stdout=stdout, stderr=stderr):
                self.assertFalse(probe.successful_output(code, stdout, stderr))


if __name__ == '__main__':
    unittest.main()
