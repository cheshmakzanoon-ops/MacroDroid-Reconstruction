"""Host fault controls only: all ADB responses are simulated, never executed."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

import android_widget_method_probe as probe


class SimulatedADB:
    def __init__(self, *, properties=None, avd=None, state='device', mode='444',
                 avd_stdout=None, avd_code=0, avd_stderr=b'',
                 wrong_hash=None, changed_hash=None, changed_binary=None, extra_opts_phase=None,
                 original_code=0, candidate_code=0, original_stdout=None, candidate_stdout=None,
                 original_stderr=b'', candidate_stderr=b'', timeout_variant=None,
                 cleanup_failure=False, mkdir_failure=False, push_failure=None, silent_output=None):
        self.properties = dict(probe.EXPECTED_DEVICE)
        self.properties.update(properties or {})
        self.avd, self.state, self.mode = avd or probe.DEFAULT_AVD, state, mode
        self.avd_stdout, self.avd_code, self.avd_stderr = avd_stdout, avd_code, avd_stderr
        self.wrong_hash, self.changed_hash, self.changed_binary = wrong_hash, changed_hash, changed_binary
        self.extra_opts_phase = extra_opts_phase
        self.codes = {'original': original_code, 'candidate': candidate_code}
        self.stdout = {'original': original_stdout, 'candidate': candidate_stdout}
        self.stderr = {'original': original_stderr, 'candidate': candidate_stderr}
        self.timeout_variant = timeout_variant
        self.cleanup_failure, self.mkdir_failure, self.push_failure = cleanup_failure, mkdir_failure, push_failure
        self.silent_output = silent_output
        self.commands, self.executions, self.owned = [], [], None
        self.hash_reads, self.extra_opts_reads = {}, 0

    def __call__(self, argv, **kwargs):
        self.commands.append(list(argv))
        if kwargs.get('check') is not False or kwargs.get('stdout') != subprocess.PIPE or kwargs.get('stderr') != subprocess.PIPE:
            raise AssertionError('The runner must preserve separate raw command streams')
        code, out, err = 0, b'', b''
        if argv[3:] == ['get-state']:
            out = (self.state + '\n').encode()
        elif argv[3:] == ['emu', 'avd', 'name']:
            code, err = self.avd_code, self.avd_stderr
            out = self.avd_stdout if self.avd_stdout is not None else (self.avd + '\nOK\n').encode()
        elif argv[3] == 'push':
            key = 'probe' if argv[-1].endswith('.dex') else Path(argv[-1]).stem
            if self.push_failure == key:
                code, err = 1, b'failed to push\n'
            else:
                out, err = b'1 file pushed\n', b'progress on stderr\n'
        elif argv[3] == 'shell':
            command = shlex.split(argv[4])
            if command[0] == 'getprop':
                key = command[1]
                value = self.properties[key]
                if key == 'dalvik.vm.extra-opts':
                    self.extra_opts_reads += 1
                    if self.extra_opts_reads == self.extra_opts_phase:
                        value = '-Xverify:none -cp /data/local/tmp/unbound.jar'
                out = (value + '\n').encode()
            elif command[0] == 'mkdir':
                if self.mkdir_failure:
                    code, err = 1, b'File exists\n'
                else:
                    self.owned = command[-1]
            elif command[0] == 'chmod':
                if command[1] != '444' or not command[-1].startswith(self.owned + '/'):
                    raise AssertionError('Only owned classpath files may be chmodded')
            elif command[0] == 'stat':
                out = (self.mode + '\n').encode()
            elif command[0] == 'sha256sum':
                target = command[1]
                self.hash_reads[target] = self.hash_reads.get(target, 0) + 1
                if target in (probe.APP_PROCESS, probe.GUEST_TIMEOUT):
                    value = 'a' * 64 if target == probe.APP_PROCESS else 'b' * 64
                    if target == self.changed_binary and self.hash_reads[target] > 1:
                        value = '0' * 64
                else:
                    key = 'probe' if target.endswith('.dex') else Path(target).stem
                    value = {'probe': probe.PROBE_SHA256, 'original': probe.ORIGINAL_SHA256,
                             'candidate': probe.CANDIDATE_SHA256}[key]
                    if key == self.wrong_hash or key == self.changed_hash and self.hash_reads[target] > 1:
                        value = '0' * 64
                out = (value + '  ' + target + '\n').encode()
            elif command[0] == probe.GUEST_TIMEOUT:
                if command[4] != probe.APP_PROCESS or command[-1] != probe.MAIN_CLASS:
                    raise AssertionError('Only the proposed AndroidRuntime probe may run')
                variant = Path(command[7].split(':')[-1]).stem
                self.executions.append(variant)
                if self.timeout_variant == variant:
                    raise subprocess.TimeoutExpired(argv, kwargs['timeout'],
                        output=('\n'.join(probe.EXPECTED_LINES[:2]) + '\n').encode(), stderr=b'partial guest diagnostics\n')
                code = self.codes[variant]
                out = self.stdout[variant] if self.stdout[variant] is not None else probe.EXPECTED_STDOUT.encode()
                err = self.stderr[variant]
            elif command[0] == 'rm':
                if command != ['rm', '-rf', '--', self.owned]:
                    raise AssertionError('Cleanup escaped the fresh owned directory')
                if self.cleanup_failure:
                    code, err = 1, b'Permission denied\n'
            elif command[0] == 'test':
                if command[1] == '-x':
                    if command[2] not in (probe.APP_PROCESS, probe.GUEST_TIMEOUT):
                        raise AssertionError('Unexpected executable probe')
                elif command != ['test', '!', '-e', self.owned]:
                    raise AssertionError('Unexpected existence check')
            else:
                raise AssertionError('Unexpected simulated shell command: ' + repr(command))
            if command[0] == self.silent_output:
                out = b'unexpected output\n'
        else:
            raise AssertionError('Unexpected simulated ADB command: ' + repr(argv))
        return subprocess.CompletedProcess(argv, code, out, err)


class WidgetProbeControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='widget-art-host-control-')
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.addCleanup(self.preserve_evidence)
        self.adb = self.root / 'adb'
        self.adb.write_text('Simulated runner. This file is never executed.\n')
        self.original, self.candidate = self.root / 'original.apk', self.root / 'candidate.apk'
        self.original.write_bytes(b'Host control fixture, not an Android APK.\n')
        self.candidate.write_bytes(b'Host control candidate fixture, not an Android APK.\n')
        self.args = argparse.Namespace(adb=str(self.adb), serial='emulator-5560', avd=probe.DEFAULT_AVD,
            original=self.original, candidate=self.candidate,
            probe=probe.ROOT / 'probes/widget-method-probe.dex',
            provenance=probe.ROOT / 'probes/widget-method-probe.json', output=self.root / 'result', timeout=120)
        self.inputs = {
            'probe': {'path': str(self.args.probe.resolve()), **probe.validate_probe(self.args.probe.read_bytes())},
            'original': {'path': str(self.original), 'bytes': probe.ORIGINAL_BYTES, 'sha256': probe.ORIGINAL_SHA256},
            'candidate': {'path': str(self.candidate), 'bytes': probe.CANDIDATE_BYTES, 'sha256': probe.CANDIDATE_SHA256},
            'provenance': {'path': str(self.args.provenance.resolve()),
                'bytes': self.args.provenance.stat().st_size, 'sha256': probe.digest(self.args.provenance),
                'content': json.loads(self.args.provenance.read_text())},
        }

    def preserve_evidence(self):
        destination = os.environ.get('WIDGET_PROBE_CONTROL_EVIDENCE')
        if destination:
            folder = Path(destination) / self.id().rsplit('.', 1)[-1]
            for result in self.root.rglob('probe-result.json'):
                shutil.copytree(result.parent, folder / result.parent.relative_to(self.root))

    def execute(self, simulator=None, *, input_side_effect=None):
        simulator = simulator or SimulatedADB()
        with mock.patch.object(probe, 'validate_inputs', side_effect=input_side_effect,
                               return_value=copy.deepcopy(self.inputs)), \
                mock.patch.object(probe.shutil, 'which', return_value=str(self.adb)):
            code, report = probe.run_probe(self.args, runner=simulator)
        return code, report, simulator

    def test_real_compiled_dex_and_exact_provenance(self):
        value = probe.validate_probe(self.args.probe.read_bytes())
        self.assertEqual(value['runtime_class_count'], 1)
        self.assertEqual(value['runtime_class'], probe.PROBE_CLASS)
        self.assertEqual(value['android_or_application_host_stub_definitions'], 0)
        self.assertEqual(value['direct_android_or_application_type_references'], 0)
        probe.validate_provenance(self.inputs['provenance']['content'])
        self.assertEqual(probe.digest(self.args.provenance), probe.PROVENANCE_SHA256)

    def test_changed_dex_rejected_before_any_android_command(self):
        data = bytearray(self.args.probe.read_bytes())
        data[192] ^= 1
        altered = self.root / 'changed.dex'
        altered.write_bytes(data)
        self.args.probe = altered
        simulator = SimulatedADB()
        code, report = probe.run_probe(self.args, runner=simulator)
        self.assertEqual(code, 2)
        self.assertEqual(simulator.commands, [])
        self.assertFalse(report['art_execution_attempted'])

    def test_wrong_original_stops_before_adb(self):
        simulator = SimulatedADB()
        code, report = probe.run_probe(self.args, runner=simulator)
        self.assertEqual(code, 2)
        self.assertEqual(simulator.commands, [])
        self.assertIn('original', report['reason'])

    def test_wrong_candidate_and_provenance_are_rejected(self):
        with mock.patch.object(probe, 'stable_identity') as identity, \
                mock.patch.object(probe.zipfile, 'ZipFile') as archive:
            archive.return_value.__enter__.return_value.namelist.return_value = ['classes.dex']
            identity.side_effect = [self.inputs['probe'], self.inputs['original'],
                                   {**self.inputs['candidate'], 'sha256': '0' * 64}]
            with self.assertRaisesRegex(probe.ProbeError, 'candidate'):
                probe.validate_inputs(self.original, self.candidate, self.args.probe, self.args.provenance)
        altered = copy.deepcopy(self.inputs['provenance']['content'])
        for path, value in [('target_method', 'unbound'), ('runtime_cases', []), ('android_runtime_executed_during_preparation', True)]:
            with self.subTest(path=path):
                changed = {**altered, path: value}
                with self.assertRaises(probe.ProbeError):
                    probe.validate_provenance(changed)

    def test_complete_simulated_success_cannot_be_claimed_as_android(self):
        code, report, simulator = self.execute()
        self.assertEqual(code, 0, report.get('evidence_error'))
        self.assertEqual(simulator.executions, ['original', 'candidate'])
        self.assertEqual(report['status'], 'SIMULATED_WIDGET_CASES_PASSED')
        self.assertTrue(report['both_semantic_case_sets_passed'])
        self.assertFalse(report['android_runtime_executed'])
        self.assertFalse(report['widget_cases_on_art_verified'])
        self.assertTrue(probe.verify_result(self.args.output, report, serial=self.args.serial, allow_simulated=True))
        with self.assertRaisesRegex(probe.ProbeError, 'simulated'):
            probe.verify_result(self.args.output, report, serial=self.args.serial)
        for variant in ('original', 'candidate'):
            argv = report['executions'][variant]['guest_argv']
            self.assertEqual(argv[:7], ['/system/bin/timeout', '-s', 'KILL', '120',
                '/system/bin/app_process64', '-Xverify:all', '-cp'])
            self.assertEqual(argv[7].split(':'), [simulator.owned + '/widget-method-probe.dex', simulator.owned + '/' + variant + '.apk'])
            self.assertNotIn('--application', argv)
            self.assertEqual(report['executions'][variant]['completed_case_prefix'], probe.CASES)
        self.assertTrue(report['cleanup_complete'])
        self.assertEqual(len(report['commands']), 60)

    def test_captured_crlf_avd_passes_both_stages_without_rewriting_bytes(self):
        captured = (probe.ROOT / 'fixtures/observed-avd-name-crlf.stdout.txt').read_bytes()
        self.assertEqual(len(captured), 33)
        self.assertEqual(hashlib.sha256(captured).hexdigest(),
                         '8522ad4bd14867dd505fdecb0e0657c506a22c36d86c8a8634fdfda384bae977')
        self.assertEqual(captured, b'MacroDroid_API35_Disposable\r\nOK\r\n')
        code, report, simulator = self.execute(SimulatedADB(avd_stdout=captured))
        self.assertEqual(code, 0, report.get('evidence_error'))
        self.assertEqual(simulator.executions, ['original', 'candidate'])
        self.assertEqual(report['status'], 'SIMULATED_WIDGET_CASES_PASSED')
        self.assertFalse(report['android_runtime_executed'])
        row = next(row for row in report['commands'] if row['label'] == 'avd-name')
        self.assertEqual((self.args.output / row['stdout']['path']).read_bytes(), captured)
        self.assertEqual(row['stdout']['sha256'], hashlib.sha256(captured).hexdigest())
        self.assertTrue(probe.verify_result(self.args.output, report, serial=self.args.serial,
                                          allow_simulated=True))
        with self.assertRaisesRegex(probe.ProbeError, 'simulated'):
            probe.verify_result(self.args.output, report, serial=self.args.serial)

    @staticmethod
    def invalid_avd_outputs():
        name = b'MacroDroid_API35_Disposable'
        return {
            'wrong-name-lf': b'Personal_AVD\nOK\n',
            'wrong-name-crlf': b'Personal_AVD\r\nOK\r\n',
            'name-prefix': b'other-' + name + b'\nOK\n',
            'name-suffix': name + b'-other\nOK\n',
            'lowercase-ok': name + b'\nOk\n',
            'missing-ok': name + b'\n',
            'duplicate-ok': name + b'\nOK\nOK\n',
            'extra-before': b'EXTRA\n' + name + b'\nOK\n',
            'extra-after': name + b'\nOK\nEXTRA\n',
            'leading-blank': b'\n' + name + b'\nOK\n',
            'trailing-blank': name + b'\nOK\n\n',
            'name-leading-space': b' ' + name + b'\nOK\n',
            'name-trailing-space': name + b' \nOK\n',
            'ok-trailing-space': name + b'\nOK \n',
            'cr-only': name + b'\rOK\r',
            'mixed-line-endings': name + b'\r\nOK\n',
            'double-cr': name + b'\r\r\nOK\r\n',
            'missing-final-newline': name + b'\nOK',
            'vertical-tab': name + b'\vOK\n',
            'form-feed': name + b'\fOK\n',
            'unicode-line-separator': name + '\u2028OK\n'.encode(),
            'null-byte': name + b'\x00\nOK\n',
            'invalid-utf8': name + b'\xff\nOK\n',
            'byte-order-mark': b'\xef\xbb\xbf' + name + b'\nOK\n',
            'empty': b'',
        }

    def test_avd_identity_and_protocol_faults_stop_before_guest_mutation(self):
        for label, output in self.invalid_avd_outputs().items():
            with self.subTest(label=label):
                self.args.output = self.root / label
                code, report, simulator = self.execute(SimulatedADB(avd_stdout=output))
                self.assertEqual(code, 2)
                self.assertIsNone(simulator.owned)
                self.assertEqual(simulator.executions, [])
                self.assertFalse(report['art_execution_attempted'])
                self.assertFalse(report['both_semantic_case_sets_passed'])
                row = report['commands'][-1]
                self.assertEqual(row['label'], 'avd-name')
                self.assertEqual((self.args.output / row['stdout']['path']).read_bytes(), output)

    def test_avd_nonzero_exit_and_diagnostics_stop_before_guest_mutation(self):
        for label, changes in [('nonzero', {'avd_code': 7}),
                               ('boolean-exit', {'avd_code': False}),
                               ('diagnostics', {'avd_stderr': b'unexpected ADB warning\n'})]:
            with self.subTest(label=label):
                self.args.output = self.root / label
                code, report, simulator = self.execute(SimulatedADB(**changes))
                self.assertEqual(code, 2)
                self.assertIsNone(simulator.owned)
                self.assertEqual(simulator.executions, [])
                self.assertIn('Device command failed: avd-name', report['reason'])

    def test_rehashed_avd_identity_and_protocol_faults_fail_evidence_recheck(self):
        code, report, simulator = self.execute()
        self.assertEqual(code, 0)
        positive_folder = self.args.output
        for label, output in self.invalid_avd_outputs().items():
            with self.subTest(label=label):
                folder = self.root / ('rehashed-' + label)
                shutil.copytree(positive_folder, folder)
                changed = copy.deepcopy(report)
                row = next(row for row in changed['commands'] if row['label'] == 'avd-name')
                (folder / row['stdout']['path']).write_bytes(output)
                row['stdout']['bytes'] = len(output)
                row['stdout']['sha256'] = hashlib.sha256(output).hexdigest()
                (folder / 'probe-result.json').write_text(json.dumps(changed, indent=2) + '\n')
                with self.assertRaises(probe.ProbeError) as rejected:
                    probe.verify_result(folder, changed, serial=self.args.serial, allow_simulated=True)
                (folder / 'deliberate-fault-result.json').write_text(json.dumps({
                    'scope': 'Deliberately rewritten simulated evidence; no Android execution',
                    'control': label, 'accepted': False, 'error': str(rejected.exception),
                    'changed_stdout': row['stdout'],
                }, indent=2) + '\n')
        self.assertTrue(probe.verify_result(positive_folder, report, serial=self.args.serial,
                                          allow_simulated=True))

    def test_physical_serial_and_other_avd_rejected_before_adb(self):
        for field, value in [('serial', 'ABC123'), ('avd', 'Personal_AVD')]:
            with self.subTest(field=field):
                prior = getattr(self.args, field)
                setattr(self.args, field, value)
                self.args.output = self.root / ('result-' + field)
                code, report, simulator = self.execute()
                self.assertEqual(code, 2)
                self.assertEqual(simulator.commands, [])
                setattr(self.args, field, prior)

    def test_invalid_timeouts_rejected_before_adb(self):
        for value in [False, 0, 29, 181, 600, 30.0]:
            with self.subTest(value=value):
                self.args.timeout = value
                self.args.output = self.root / ('result-' + repr(value))
                code, report, simulator = self.execute()
                self.assertEqual(code, 2)
                self.assertEqual(simulator.commands, [])

    def test_device_not_booted_or_pinned_stops_before_mutation(self):
        for key, value in [('ro.build.fingerprint', 'other-image'), ('sys.boot_completed', '0'),
                           ('ro.kernel.qemu', '0'), ('ro.build.version.sdk', '34')]:
            with self.subTest(key=key):
                self.args.output = self.root / key
                code, report, simulator = self.execute(SimulatedADB(properties={key: value}))
                self.assertEqual(code, 2)
                self.assertIsNone(simulator.owned)
                self.assertEqual(simulator.executions, [])

    def test_unavailable_device_and_wrong_observed_avd_stop_before_mutation(self):
        for key, value in [('state', 'offline'), ('avd', 'Personal_AVD')]:
            with self.subTest(key=key):
                self.args.output = self.root / key
                code, report, simulator = self.execute(SimulatedADB(**{key: value}))
                self.assertEqual(code, 2)
                self.assertIsNone(simulator.owned)

    def test_late_verifier_or_classpath_override_is_rejected(self):
        for phase in [1, 2, 3, 4]:
            with self.subTest(phase=phase):
                self.args.output = self.root / ('phase-' + str(phase))
                code, report, simulator = self.execute(SimulatedADB(extra_opts_phase=phase))
                self.assertEqual(code, 2)
                self.assertEqual(len(simulator.executions), max(0, phase - 2))
                if phase > 1:
                    self.assertTrue(report['cleanup_complete'])

    def test_wrong_device_input_hashes_stop_before_execution_and_cleanup(self):
        for key in ['probe', 'original', 'candidate']:
            with self.subTest(key=key):
                self.args.output = self.root / key
                code, report, simulator = self.execute(SimulatedADB(wrong_hash=key))
                self.assertEqual(code, 2)
                self.assertEqual(simulator.executions, [])
                self.assertTrue(report['cleanup_complete'])

    def test_readonly_mode_is_required(self):
        code, report, simulator = self.execute(SimulatedADB(mode='644'))
        self.assertEqual(code, 2)
        self.assertEqual(simulator.executions, [])
        self.assertTrue(report['cleanup_complete'])

    def test_failed_mkdir_never_removes_unowned_directory(self):
        code, report, simulator = self.execute(SimulatedADB(mkdir_failure=True))
        self.assertEqual(code, 2)
        self.assertIsNone(simulator.owned)
        self.assertFalse(report['cleanup_complete'])
        self.assertFalse(any(row[3] == 'shell' and shlex.split(row[4])[0] == 'rm' for row in simulator.commands))

    def test_failed_candidate_push_never_executes(self):
        code, report, simulator = self.execute(SimulatedADB(push_failure='candidate'))
        self.assertEqual(code, 2)
        self.assertEqual(simulator.executions, [])
        self.assertTrue(report['cleanup_complete'])

    def test_original_failure_stops_candidate_even_with_success_stdout(self):
        code, report, simulator = self.execute(SimulatedADB(original_code=1))
        self.assertEqual(code, 2)
        self.assertEqual(simulator.executions, ['original'])
        self.assertEqual(report['executions']['original']['completed_cases'], 8)
        self.assertFalse(report['executions']['original']['semantic_cases_passed'])
        self.assertEqual(set(report['device_inputs_after']), {'probe', 'original', 'candidate'})
        self.assertTrue(report['cleanup_complete'])

    def test_missing_or_extra_candidate_case_output_is_rejected(self):
        for name, output in [('missing', ('\n'.join(probe.EXPECTED_LINES[:-2]) + '\n').encode()),
                             ('extra', probe.EXPECTED_STDOUT.encode() + b'UNEXPECTED\n'),
                             ('different-line-ending', probe.EXPECTED_STDOUT.replace('\n', '\r\n').encode())]:
            with self.subTest(name=name):
                self.args.output = self.root / name
                code, report, simulator = self.execute(SimulatedADB(candidate_stdout=output))
                self.assertEqual(code, 2)
                self.assertFalse(report['executions']['candidate']['semantic_cases_passed'])
                self.assertTrue(report['cleanup_complete'])

    def test_diagnostics_stay_separate_from_observed_semantic_success(self):
        code, report, simulator = self.execute(SimulatedADB(candidate_stderr=b'W/art: unreviewed diagnostic\n'))
        self.assertEqual(code, 2)
        self.assertTrue(report['both_semantic_case_sets_passed'])
        self.assertFalse(report['strict_diagnostics_passed'])
        self.assertTrue(report['executions']['candidate']['semantic_cases_passed'])
        self.assertFalse(report['executions']['candidate']['strict_command_passed'])
        self.assertFalse(report['widget_cases_on_art_verified'])
        self.assertTrue(report['cleanup_complete'])

    def test_timeout_preserves_prefix_stderr_and_after_identities(self):
        code, report, simulator = self.execute(SimulatedADB(timeout_variant='candidate'))
        self.assertEqual(code, 2)
        value = report['executions']['candidate']
        self.assertTrue(value['command']['timed_out'])
        self.assertEqual(value['completed_case_prefix'], probe.CASES[:2])
        self.assertFalse(value['semantic_cases_passed'])
        self.assertEqual((self.args.output / value['command']['stderr']['path']).read_bytes(), b'partial guest diagnostics\n')
        self.assertEqual(set(report['device_inputs_after']), {'probe', 'original', 'candidate'})
        self.assertEqual(report['inputs_before'], report['inputs_after'])
        self.assertTrue(report['cleanup_complete'])

    def test_device_file_or_binary_change_preserves_cases_but_fails_binding(self):
        options = [{'changed_hash': 'original'}, {'changed_hash': 'candidate'}, {'changed_hash': 'probe'},
                   {'changed_binary': probe.APP_PROCESS}, {'changed_binary': probe.GUEST_TIMEOUT}]
        for index, option in enumerate(options):
            with self.subTest(option=option):
                self.args.output = self.root / str(index)
                code, report, simulator = self.execute(SimulatedADB(**option))
                self.assertEqual(code, 2)
                self.assertTrue(report['both_semantic_case_sets_passed'])
                self.assertTrue(report['postcheck_errors'])
                self.assertTrue(report['cleanup_complete'])

    def test_local_input_change_is_a_failed_postcheck(self):
        code, report, simulator = self.execute(input_side_effect=[self.inputs, probe.ProbeError('Local candidate changed')])
        self.assertEqual(code, 2)
        self.assertTrue(report['both_semantic_case_sets_passed'])
        self.assertFalse(report['inputs_unchanged'])
        self.assertIn('Local candidate changed', report['postcheck_errors'])
        self.assertTrue(report['cleanup_complete'])

    def test_cleanup_failure_preserves_cases_and_fails_overall(self):
        code, report, simulator = self.execute(SimulatedADB(cleanup_failure=True))
        self.assertEqual(code, 2)
        self.assertEqual(report['status'], 'SIMULATED_WIDGET_CLEANUP_FAILED')
        self.assertTrue(report['both_semantic_case_sets_passed'])
        self.assertFalse(report['cleanup_complete'])
        with self.assertRaises(probe.ProbeError):
            probe.verify_result(self.args.output, report, serial=self.args.serial, allow_simulated=True)

    def test_unexpected_silent_command_output_is_preserved_and_fails(self):
        code, report, simulator = self.execute(SimulatedADB(silent_output='chmod'))
        self.assertEqual(code, 2)
        self.assertTrue(report['both_semantic_case_sets_passed'])
        self.assertIn('Silent command', report['evidence_error'])

    def test_result_rejects_modified_flags_classpath_origin_and_scope(self):
        code, report, simulator = self.execute()
        self.assertEqual(code, 0)
        mutations = ['verifier', 'extra-classpath', 'different-apk', 'wrong-device', 'wrong-provenance',
                     'runtime-claim', 'missing-command', 'unexpected-command', 'nonzero', 'timeout', 'cleanup-path']
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                changed = copy.deepcopy(report)
                command = next(row for row in changed['commands'] if row['label'] == 'execute-candidate')
                if mutation == 'verifier':
                    command['argv'][4] = command['argv'][4].replace('-Xverify:all', '-Xverify:none')
                elif mutation == 'extra-classpath':
                    command['argv'][4] = command['argv'][4].replace('-cp ', '-cp /tmp/stubs.jar:')
                elif mutation == 'different-apk':
                    changed['device_inputs_after']['candidate']['sha256'] = '0' * 64
                elif mutation == 'wrong-device':
                    changed['environment-before-candidate']['dalvik.vm.extra-opts'] = '-Xverify:none'
                elif mutation == 'wrong-provenance':
                    changed['inputs_before']['provenance']['content']['runtime_cases'] = []
                elif mutation == 'runtime-claim':
                    changed['full_runtime_1_to_1_established'] = True
                elif mutation == 'missing-command':
                    changed['commands'].pop(1)
                elif mutation == 'unexpected-command':
                    changed['commands'].append(copy.deepcopy(command))
                elif mutation == 'nonzero':
                    command['returncode'] = 1
                elif mutation == 'timeout':
                    command['timed_out'] = True
                else:
                    changed['commands'][-2]['argv'][4] = 'rm -rf -- /data/local/tmp'
                with self.assertRaises(probe.ProbeError):
                    probe.verify_result(self.args.output, changed, serial=self.args.serial, allow_simulated=True)

    def test_every_command_output_is_hashed_and_semantically_rechecked(self):
        code, report, simulator = self.execute()
        self.assertEqual(code, 0)
        for index in [0, 2, 9, 12, 18, len(report['commands']) - 1]:
            with self.subTest(index=index):
                changed = copy.deepcopy(report)
                changed['commands'][index]['stdout']['sha256'] = '0' * 64
                with self.assertRaises(probe.ProbeError):
                    probe.verify_result(self.args.output, changed, serial=self.args.serial, allow_simulated=True)
        target = next(row for row in report['commands'] if row['label'] == 'environment-before-dalvik-vm-extra-opts')
        path = self.args.output / target['stdout']['path']
        original = path.read_bytes()
        data = b'-Xverify:none\n'
        path.write_bytes(data)
        changed = copy.deepcopy(report)
        row = next(row for row in changed['commands'] if row['label'] == target['label'])
        row['stdout']['bytes'], row['stdout']['sha256'] = len(data), hashlib.sha256(data).hexdigest()
        with self.assertRaisesRegex(probe.ProbeError, 'Observed environment'):
            probe.verify_result(self.args.output, changed, serial=self.args.serial, allow_simulated=True)
        path.write_bytes(original)

    def test_reusing_nonempty_output_is_rejected_without_overwriting(self):
        self.args.output.mkdir()
        guard = self.args.output / 'prior-evidence.txt'
        guard.write_text('preserve this exact evidence')
        simulator = SimulatedADB()
        with self.assertRaises(probe.ProbeError):
            probe.run_probe(self.args, runner=simulator)
        self.assertEqual(guard.read_text(), 'preserve this exact evidence')
        self.assertEqual(simulator.commands, [])

    def test_local_hash_race_is_detected(self):
        path = self.root / 'racy-input'
        path.write_bytes(b'before')
        def changed(_):
            path.write_bytes(b'after with different length')
            return 'a' * 64
        with mock.patch.object(probe, 'digest', side_effect=changed):
            with self.assertRaisesRegex(probe.ProbeError, 'changed while being hashed'):
                probe.stable_identity(path)

    def test_exact_case_predicate_rejects_bool_returncode_and_retains_partial(self):
        value = probe.observation(False, probe.EXPECTED_STDOUT.encode(), b'')
        self.assertFalse(value['semantic_cases_passed'])
        self.assertEqual(value['completed_cases'], 8)
        value = probe.observation(0, ('\n'.join(probe.EXPECTED_LINES[:3]) + '\n').encode(), b'failure detail\n')
        self.assertFalse(value['semantic_cases_passed'])
        self.assertEqual(value['completed_case_prefix'], probe.CASES[:3])


if __name__ == '__main__':
    unittest.main()
