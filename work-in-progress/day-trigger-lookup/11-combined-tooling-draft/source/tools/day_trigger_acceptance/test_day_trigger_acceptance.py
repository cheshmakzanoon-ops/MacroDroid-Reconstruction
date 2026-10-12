#!/usr/bin/env python3
"""Small adversarial controls for job provenance and fresh-result acceptance.

Synthetic gate reports below exercise rejection policy only. They are never
application execution, signed-build, method-parity, or Android evidence.
"""
import copy
import shutil
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import inputs
import prepare
import run_acceptance
import verify


class OwnedTemporary(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='day-numeric-host-control-')
        self.root = Path(self.temp.name)

    def tearDown(self):
        # Hosted failures retain actual receipts and original metadata even though
        # an artifact copy cannot preserve the host's inode or ctime.
        retained = os.environ.get('DAY_TRIGGER_CONTROL_EVIDENCE_ROOT')
        if retained:
            output = Path(retained) / self.id()
            output.mkdir(parents=True, exist_ok=False)
            rows = []
            for path in sorted(self.root.rglob('*')):
                relative = path.relative_to(self.root).as_posix()
                status = path.lstat()
                if path.is_symlink():
                    rows.append({'path': relative, 'type': 'inert-symlink-description',
                                 'target': os.readlink(path)})
                elif path.is_file():
                    destination = output / 'files' / relative
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(path, destination)
                    rows.append({'path': relative, 'type': 'regular', **inputs.identity(path),
                                 'observed_stat': run_acceptance.command_file_stat(status)})
            values = {}
            for key, value in vars(self).items():
                if key.startswith('_') and key != '_control_observations':
                    continue
                try:
                    json.dumps(value, allow_nan=False)
                except (TypeError, ValueError):
                    continue
                values[key] = value
            inputs.write_json(output / 'observations.json', {
                'schema': 1, 'test': self.id(), 'original_temporary_root': str(self.root),
                'scope': 'Tool policy fixtures and declared small Python subprocesses only; no application build or Java parity claim',
                'metadata_scope': 'Recorded original live stat; copied inode/ctime are not substituted',
                'values': values, 'files': rows})
        self.temp.cleanup()

    def observed_command(self, prefix, label, **row):
        """Use real exclusive files; the contents explicitly remain synthetic."""
        folder = self.root / prefix
        folder.mkdir(parents=True, exist_ok=True)
        observed = run_acceptance.CommandStreamEvidence(
            self.root, folder / (label + '.stdout.log'), folder / (label + '.stderr.log'))
        with observed as stream:
            for name in ('stdout', 'stderr'):
                stream.handles[name].write(('SYNTHETIC COMMAND POLICY ONLY ' + prefix + '/' + label + ':' + name).encode())
        observed.add_to(row)
        self.__dict__.setdefault('_control_observations', []).append(copy.deepcopy(row))
        return row

    @staticmethod
    def set_flat_clock(row, prefix, value):
        row[prefix + '_unix_ns'] = value['unix_ns']
        row[prefix + '_monotonic_ns'] = value['monotonic_ns']
        row[prefix + '_utc'] = value['utc']

    @staticmethod
    def changed_clock(value, unix_delta=0, mono_delta=0):
        changed = copy.deepcopy(value)
        changed['unix_ns'] += unix_delta
        changed['monotonic_ns'] += mono_delta
        seconds, fraction = divmod(changed['unix_ns'], 1_000_000_000)
        changed['utc'] = datetime.fromtimestamp(seconds, timezone.utc).replace(
            microsecond=fraction // 1000).isoformat(timespec='microseconds')
        return changed

    def put(self, name, raw=b'original'):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        return path


class InventoryControls(OwnedTemporary):
    def tree(self):
        for name in inputs.INPUT_DIRECTORIES:
            (self.root / name).mkdir()
        self.put('source/kept.txt', b'unchanged')
        self.put('source/change.txt', b'old')
        self.put('acceptance.py', b'old runner')
        return inputs.scan_inputs(self.root)

    def change(self, name, old, new):
        return {'path': name, 'baseline': None if old is None else inputs.byte_identity(old),
                'candidate': inputs.byte_identity(new), 'must_be_absent_if_new': old is None, 'source': 'project/' + name}

    def test_complete_derivation_retains_unchanged_rows_and_adds_only_selected_input(self):
        base = self.tree()
        changes = [self.change('source/change.txt', b'old', b'new'), self.change('source/new.txt', None, b'added')]
        result = inputs.derive(base, changes)
        self.assertEqual(4, result['files'])
        self.assertEqual(base['entries']['source/kept.txt'], result['entries']['source/kept.txt'])
        self.assertEqual(inputs.byte_identity(b'new')['sha256'], result['entries']['source/change.txt']['sha256'])

    def test_truncated_inventory_with_recomputed_counters_still_differs_from_fixed_full_expected(self):
        base = self.tree()
        altered = dict(base['entries'])
        del altered['source/kept.txt']
        with self.assertRaisesRegex(ValueError, 'Full input inventory differs'):
            inputs.compare_inputs(inputs.snapshot(altered), base)

    def test_omitted_overlay_row_changes_expected_future_identity(self):
        base = self.tree()
        changes = [self.change('source/change.txt', b'old', b'new'), self.change('source/new.txt', None, b'added')]
        with self.assertRaisesRegex(ValueError, 'Full input inventory differs'):
            inputs.compare_inputs(inputs.derive(base, changes[:1]), inputs.derive(base, changes))

    def test_extra_overlay_row_changes_expected_future_identity(self):
        base = self.tree()
        changes = [self.change('source/change.txt', b'old', b'new')]
        with self.assertRaisesRegex(ValueError, 'Full input inventory differs'):
            inputs.compare_inputs(inputs.derive(base, changes + [self.change('source/extra.txt', None, b'extra')]), inputs.derive(base, changes))

    def test_duplicate_overlay_role_is_rejected(self):
        base = self.tree()
        change = self.change('source/change.txt', b'old', b'new')
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            inputs.derive(base, [change, change])

    def test_wrong_copy_role_is_rejected(self):
        base = self.tree()
        change = self.change('source/change.txt', b'old', b'new')
        change['source'] = 'project/source/kept.txt'
        with self.assertRaisesRegex(ValueError, 'copy role'):
            inputs.derive(base, [change])

    def test_new_role_cannot_replace_existing_baseline(self):
        with self.assertRaisesRegex(ValueError, 'already exists'):
            inputs.derive(self.tree(), [self.change('source/change.txt', None, b'new')])

    def test_changed_baseline_bytes_reject_before_any_write(self):
        base = self.tree()
        with self.assertRaisesRegex(ValueError, 'baseline differs'):
            inputs.derive(base, [self.change('source/change.txt', b'wrong', b'new')])
        self.assertEqual(b'old', (self.root / 'source/change.txt').read_bytes())

    def test_missing_last_candidate_rejects_before_first_source_replacement(self):
        self.tree()
        capsule = self.root / 'capsule'
        self.put('capsule/project/source/change.txt', b'new')
        changes = [self.change('source/change.txt', b'old', b'new'), self.change('source/new.txt', None, b'absent')]
        with self.assertRaisesRegex(ValueError, 'Missing regular file'):
            inputs.apply_changes(self.root, capsule, changes)
        self.assertEqual(b'old', (self.root / 'source/change.txt').read_bytes())
        self.assertFalse((self.root / 'source/new.txt').exists())

    def test_existing_new_destination_rejects_before_first_source_replacement(self):
        self.tree()
        capsule = self.root / 'capsule'
        self.put('capsule/project/source/change.txt', b'new')
        self.put('capsule/project/source/new.txt', b'added')
        self.put('source/new.txt', b'concurrent file')
        changes = [self.change('source/change.txt', b'old', b'new'), self.change('source/new.txt', None, b'added')]
        with self.assertRaisesRegex(ValueError, 'destination is present'):
            inputs.apply_changes(self.root, capsule, changes)
        self.assertEqual(b'old', (self.root / 'source/change.txt').read_bytes())
        self.assertEqual(b'concurrent file', (self.root / 'source/new.txt').read_bytes())

    def test_apply_selected_bytes_preserves_unrelated_source(self):
        base = self.tree()
        capsule = self.root / 'capsule'
        self.put('capsule/project/source/change.txt', b'new')
        self.put('capsule/project/source/new.txt', b'added')
        changes = [self.change('source/change.txt', b'old', b'new'), self.change('source/new.txt', None, b'added')]
        inputs.apply_changes(self.root, capsule, changes)
        inputs.compare_inputs(inputs.scan_inputs(self.root), inputs.derive(base, changes))
        self.assertEqual(b'unchanged', (self.root / 'source/kept.txt').read_bytes())

    def test_actual_unlisted_input_cannot_be_hidden_by_manifest(self):
        base = self.tree()
        self.put('tests/unlisted.java', b'not in fixed inventory')
        with self.assertRaisesRegex(ValueError, 'Full input inventory differs'):
            inputs.compare_inputs(inputs.scan_inputs(self.root), base)

    def test_input_directory_symlink_is_rejected(self):
        self.tree()
        (self.root / 'source/link').symlink_to(self.root / 'tests', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Symlink input directory'):
            inputs.scan_inputs(self.root)

    def test_leaf_symlink_is_rejected_even_if_bytes_are_identical(self):
        self.tree()
        (self.root / 'source/alias.txt').symlink_to(self.root / 'source/kept.txt')
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            inputs.scan_inputs(self.root)

    def test_physical_input_alias_is_rejected_even_when_hashes_match(self):
        self.tree()
        os.link(self.root / 'source/kept.txt', self.root / 'source/alias.txt')
        with self.assertRaisesRegex(ValueError, 'Physical input alias'):
            inputs.scan_inputs(self.root)

    def test_only_documented_generated_paths_are_outside_input_scope(self):
        base = self.tree()
        for path in ['tools/classes/Generated.class', 'tests/__pycache__/cached.pyc', 'source/cached.pyo', 'build/anything.bin']:
            self.put(path, b'generated')
        inputs.compare_inputs(inputs.scan_inputs(self.root), base)

    def test_dot_alias_and_traversal_paths_are_rejected(self):
        for path in ('./source/file', 'source/../tests/file', '/tmp/file', 'source//file', 'source\\file', 'source/file\n'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                inputs.relative(path)

    def test_boolean_counts_and_duplicate_json_keys_are_rejected(self):
        base = self.tree()
        base['files'] = True
        with self.assertRaises(ValueError):
            inputs.validate_snapshot(base)
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON object key'):
            inputs.document('{"files": 3, "files": 0}')

    def test_historical_reports_and_apks_are_retained_outside_fresh_scope(self):
        project = self.root / 'project'
        output = self.root / 'proof'
        output.mkdir()
        self.put('project/reports/acceptance-latest.json', b'old success')
        self.put('project/dist/old.apk', b'old artifact')
        before = [inputs.identity(project / 'reports/acceptance-latest.json'), inputs.identity(project / 'dist/old.apk')]
        records = prepare.retain_prior_outputs(project, output)
        self.assertEqual([], prepare.inventory(project / 'reports'))
        self.assertEqual([], prepare.inventory(project / 'dist'))
        self.assertEqual(2, len(records))
        self.assertEqual(before, [inputs.identity(output / 'prior-outputs/reports/acceptance-latest.json'),
                                  inputs.identity(output / 'prior-outputs/dist/old.apk')])


class GateEvidenceControls(OwnedTemporary):
    def setUp(self):
        super().setUp()
        self.pins = inputs.load_pins()
        self.start = time.time_ns() - 30_000_000_000
        self.end = time.time_ns() + 30_000_000_000
        self.folder = 'reports/acceptance-20261012T000000000001Z'
        self.execution = {'python_executable': '/synthetic/python'}
        self.latest = {'host_acceptance_passed': True, 'source_edit_probe_skipped': False,
                       'build_inputs_unchanged': True, 'android_runtime_executed': False,
                       'full_runtime_1_to_1_established': False, 'complete_high_level_java_kotlin_source': False,
                       'input_files': self.pins['future_snapshot']['files'],
                       'input_snapshot_before': self.pins['future_snapshot']['snapshot_sha256'],
                       'input_snapshot_after': self.pins['future_snapshot']['snapshot_sha256'],
                       'started_utc': datetime.now(timezone.utc).isoformat(), 'finished_utc': datetime.now(timezone.utc).isoformat(),
                       'commands': [], 'fresh_evidence_sha256': {}}
        for index, (label, arguments) in enumerate(self.pins['gate_commands'], 1):
            name = f'{self.folder}/{index:02d}-{label}.log'
            path = self.put(name, ('SYNTHETIC POLICY CONTROL ' + label).encode())
            self.latest['commands'].append({'label': label, 'command': ['/synthetic/python', *arguments], 'log': name,
                                           'exit_code': 0, 'passed': True, 'seconds': 0.01,
                                           'timeout_seconds': 5400 if label == 'ui-negative-controls' else 1200,
                                           'log_sha256': inputs.identity(path)['sha256']})
        for name in self.pins['fresh_reports']:
            path = self.put('reports/' + name, json.dumps({'SYNTHETIC_POLICY_CONTROL_ONLY': name}).encode())
            self.latest['fresh_evidence_sha256'][name] = inputs.identity(path)['sha256']

    def seal(self):
        raw = inputs.encoded(self.latest)
        self.put('reports/acceptance-latest.json', raw)
        self.put(self.folder + '/result.json', raw)

    def check(self):
        self.seal()
        return verify.verify_gates(self.latest, self.execution, self.pins, verify.Artifacts(self.root, self.start, self.end))

    def test_synthetic_complete_fresh_gate_envelope_is_accepted_only_as_policy_fixture(self):
        self.assertEqual(23, len(self.check()))

    def test_omitted_gate_rejects(self):
        self.latest['commands'].pop()
        with self.assertRaisesRegex(ValueError, 'gate inventory'):
            self.check()

    def test_wrong_gate_order_rejects(self):
        self.latest['commands'][1], self.latest['commands'][2] = self.latest['commands'][2], self.latest['commands'][1]
        with self.assertRaisesRegex(ValueError, 'Gate order'):
            self.check()

    def test_omitted_fresh_report_rejects_even_when_other_hashes_match(self):
        del self.latest['fresh_evidence_sha256']['day-numeric-dex-controls.json']
        with self.assertRaisesRegex(ValueError, 'fresh acceptance report'):
            self.check()

    def test_old_gate_bytes_under_correct_name_are_rejected_by_actual_freshness(self):
        path = self.root / self.latest['commands'][0]['log']
        os.utime(path, ns=(self.start - 1, self.start - 1))
        with self.assertRaisesRegex(ValueError, 'outside the actual execution interval'):
            self.check()

    def test_gate_log_reuse_is_rejected_before_hash_comparison(self):
        self.latest['commands'][1]['log'] = self.latest['commands'][0]['log']
        self.latest['commands'][1]['log_sha256'] = self.latest['commands'][0]['log_sha256']
        with self.assertRaisesRegex(ValueError, 'reused or renamed'):
            self.check()

    def test_physical_gate_log_alias_rejects_with_matching_recorded_hashes(self):
        first, second = [self.root / row['log'] for row in self.latest['commands'][:2]]
        second.unlink()
        os.link(first, second)
        self.latest['commands'][1]['log_sha256'] = self.latest['commands'][0]['log_sha256']
        with self.assertRaisesRegex(ValueError, 'physical result file'):
            self.check()

    def test_skipped_edit_probe_rejects(self):
        self.latest['source_edit_probe_skipped'] = True
        with self.assertRaisesRegex(ValueError, 'Incomplete or out-of-scope'):
            self.check()

    def test_nonzero_exit_cannot_be_replaced_with_pass_flag(self):
        self.latest['commands'][8]['exit_code'] = 2
        with self.assertRaisesRegex(ValueError, 'did not exit zero'):
            self.check()

    def test_boolean_zero_exit_rejects(self):
        self.latest['commands'][8]['exit_code'] = False
        with self.assertRaisesRegex(ValueError, 'did not exit zero'):
            self.check()

    def test_larger_ui_timeout_cannot_silently_replace_reviewed_bound(self):
        self.latest['commands'][10]['timeout_seconds'] = 99999
        with self.assertRaisesRegex(ValueError, 'Per-gate bound'):
            self.check()

    def test_old_acceptance_directory_rejects_even_with_fresh_latest(self):
        self.put('reports/acceptance-20200101T000000000000Z/old.log')
        with self.assertRaisesRegex(ValueError, 'historical acceptance directory'):
            self.check()

    def test_python_skips_cannot_count_as_successes(self):
        valid = b'test_one (suite.Test.test_one) ... ok\n\nRan 1 tests in 0.001s\n\nOK\n'
        self.assertEqual(1, verify.verify_python(valid, 1)['tests'])
        for raw in (valid.replace(b'... ok', b"... skipped 'missing'"), valid.replace(b'Ran 1', b'Ran 2'), valid.replace(b'OK\n', b'FAILED (failures=1)\n')):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                verify.verify_python(raw, 1)


class ActualProcessControls(OwnedTemporary):
    def execute(self, code, timeout=5):
        env = os.environ.copy()
        env.update(PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(self.root))
        return run_acceptance.run_child([sys.executable, '-B', '-c', code], self.root, env,
                                        self.root / 'actual.stdout.log', self.root / 'actual.stderr.log', timeout)

    def test_actual_nonzero_exit_and_both_streams_are_retained(self):
        result = self.execute("import sys; print('stdout evidence'); print('stderr evidence', file=sys.stderr); sys.exit(7)")
        self.assertEqual(7, result['returncode'])
        self.assertFalse(result['timed_out'])
        self.assertEqual(b'stdout evidence\n', (self.root / 'actual.stdout.log').read_bytes())
        self.assertEqual(b'stderr evidence\n', (self.root / 'actual.stderr.log').read_bytes())

    def test_actual_zero_exit_is_recorded_without_a_parity_claim(self):
        result = self.execute("print('controlled subprocess')")
        self.assertEqual(0, result['returncode'])
        self.assertFalse(result['timed_out'])
        self.assertNotIn('host_acceptance_passed', result)

    def test_timeout_stops_owned_descendant_and_preserves_literal_outcome(self):
        child = "import pathlib,time; pathlib.Path('descendant-ready').write_text('ready'); time.sleep(1.4); pathlib.Path('survived').write_text('bad')"
        parent = "import subprocess,sys,time,pathlib; subprocess.Popen([sys.executable,'-B','-c',%r]);\nwhile not pathlib.Path('descendant-ready').exists(): time.sleep(0.005)\ntime.sleep(5)" % child
        result = self.execute(parent, timeout=1.0)
        self.assertTrue(result['timed_out'])
        self.assertNotEqual(0, result['returncode'])
        self.assertTrue((self.root / 'descendant-ready').exists())
        time.sleep(0.6)
        self.assertFalse((self.root / 'survived').exists())

    def test_false_process_exit_never_satisfies_execution_verification(self):
        pins = inputs.load_pins()
        prepared = {'project': '/synthetic/project'}
        value = {'passed': True, 'build_inputs_unchanged': True, 'active_promoted': False,
                 'android_runtime_executed': False, 'full_runtime_1_to_1_established': False,
                 'status': 'HOST_ACCEPTANCE_PROCESS_EXITED_ZERO', 'project': prepared['project'],
                 'input_snapshot_before': pins['future_snapshot'], 'input_snapshot_after': pins['future_snapshot'],
                 'python_executable': '/synthetic/python', 'execution': {'returncode': False}}
        with self.assertRaisesRegex(ValueError, 'did not exit zero'):
            verify.verify_execution(value, prepared, pins)


class NumericCommandControls(OwnedTemporary):
    """Independent synthetic producer-shaped rows; no Java command is executed."""
    def setUp(self):
        super().setUp()
        self.folder = 'reports/day-numeric-dex-synthetic'
        self.java = '/synthetic/jdk/bin/java'
        self.make_report()

    def make_report(self):
        self.report = {'schema': 2, 'commands': []}
        self.set_flat_clock(self.report, 'started', run_acceptance.command_clock())
        output = self.root / self.folder
        jar = str(self.root / 'tools/lib/jadx-r2721.4574686-all.jar')
        cp = ':'.join([jar, str(self.root / 'build/java/hostclasses'), str(self.root / 'tools/classes')])
        rows = []
        def pipeline(name):
            path = output / name
            rows.extend([
                (name, 'd8-helper', 0, [self.java, '-Xmx512m', '-cp', jar, 'com.android.tools.r8.D8', '--release',
                    '--no-desugaring', '--min-api', '23', '--output', str(path / 'd8'), str(path / 'inputs.jar')]),
                (name, 'disassemble-helper', 0, [self.java, '-Xmx512m', '-cp', jar, 'com.android.tools.smali.baksmali.Main',
                    'd', '--api', '23', '--use-locals', '-o', str(path / 'helper-smali'), str(path / 'd8/classes.dex')]),
                (name, 'assemble-target', 0, [self.java, '-Xmx512m', '-cp', jar, 'com.android.tools.smali.smali.Main',
                    'a', '--api', '23', '-j', '2', '-o', str(path / 'numeric-target.dex'), str(path / 'target-smali')])])
        def harness(name, code):
            rows.append((name, 'execute', code, [self.java, '-XX:-OmitStackTraceInFastThrow',
                '-XX:+ShowCodeDetailsInExceptionMessages', '-Xmx512m', '-cp', cp, 'DayNumericControlHarness',
                str(output / name / 'config.json'), str(output / name / 'result.json')]))
        pipeline('positive-pipeline')
        method = 'Lcom/arlosoft/macrodroid/triggers/DayTrigger;->r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I'
        rows.extend([
            ('', 'signed-apk-instructions', 0, [self.java, '-Xmx512m', '-cp', cp, 'InspectMethod',
                str(self.root / 'build/hybrid/classes3.dex'), method, str(output / 'signed-apk-instructions.json')]),
            ('', 'positive-transplant-instructions', 0, [self.java, '-Xmx512m', '-cp', cp, 'InspectMethod',
                str(output / 'positive-pipeline/numeric-target.dex'), method, str(output / 'positive-transplant-instructions.json')])])
        harness('positive', 0)
        for name in ('integer-zero', 'decimal-zero'):
            pipeline(name + '-pipeline')
            harness(name + '-dex-fault', 3)
        harness('original-as-rebuilt-rejected', 1)
        harness('wrong-helper-class-rejected', 1)
        harness('positive-restoration', 0)
        for subdir, label, code, argv in rows:
            prefix = self.folder + ('/' + subdir if subdir else '')
            self.report['commands'].append(self.observed_command(
                prefix, label, name=label, argv=argv, returncode=code, timeout_seconds=120))
        self.set_flat_clock(self.report, 'finished', run_acceptance.command_clock())
        # This is the command guard alone, not a synthetic full acceptance claim.
        # Its encompassing fixture bounds include the actual filesystem witnesses.
        first = self.report['commands'][0]['stream_evidence']['before_witness']['final_stat']['ctime_ns']
        final = self.report['commands'][-1]['stream_evidence']['after_witnesses'][-1]['final_stat']['ctime_ns']
        self.start = min(first, self.report['started_unix_ns'])
        self.end = max(final, self.report['finished_unix_ns'])

    def check(self):
        ledger = verify.Artifacts(self.root, self.start, self.end)
        verify.verify_numeric_commands(self.report, self.folder, ledger, self.java)
        return ledger

    def test_exact_seventeen_synthetic_command_rows_preserve_streams_and_all_witnesses(self):
        rows = self.check().rows
        self.assertEqual(34, len([name for name in rows if name.endswith(('.stdout.log', '.stderr.log'))]))
        expected = sum(3 + len(row['stream_evidence']['after_witnesses']) for row in self.report['commands'])
        self.assertEqual(expected, len(rows))

    def test_retained_streams_cannot_make_bin_true_a_d8_command(self):
        self.report['commands'][0]['argv'] = ['/bin/true']
        with self.assertRaisesRegex(ValueError, 'Numeric exact command'):
            self.check()

    def test_missing_runtime_flag_rejects_with_unchanged_positive_streams(self):
        self.report['commands'][5]['argv'].remove('-XX:-OmitStackTraceInFastThrow')
        with self.assertRaisesRegex(ValueError, 'JVM policy'):
            self.check()

    def test_different_config_and_result_roles_reject(self):
        self.report['commands'][5]['argv'][-2:] = ['/different/config.json', '/different/result.json']
        with self.assertRaisesRegex(ValueError, 'input role'):
            self.check()

    def test_boolean_argv_element_rejects(self):
        self.report['commands'][0]['argv'] = [True]
        with self.assertRaisesRegex(ValueError, 'Numeric exact command'):
            self.check()

    def test_wrong_api_target_rejects_even_when_d8_streams_are_unchanged(self):
        self.report['commands'][0]['argv'][self.report['commands'][0]['argv'].index('--min-api') + 1] = '24'
        with self.assertRaisesRegex(ValueError, 'Numeric exact command'):
            self.check()

    def test_extra_classpath_source_rejects(self):
        self.report['commands'][5]['argv'][5] += ':/extra/classes'
        with self.assertRaisesRegex(ValueError, 'Numeric exact command'):
            self.check()

    def test_another_method_inspection_rejects(self):
        self.report['commands'][3]['argv'][-2] = 'Lexample/Other;->value()I'
        with self.assertRaisesRegex(ValueError, 'Numeric exact command'):
            self.check()

    def test_boolean_subprocess_exit_rejects(self):
        self.report['commands'][0]['returncode'] = False
        with self.assertRaisesRegex(ValueError, 'subprocess outcome'):
            self.check()

    def test_reused_numeric_stream_name_rejects(self):
        self.report['commands'][1]['stdout'] = copy.deepcopy(self.report['commands'][0]['stdout'])
        with self.assertRaisesRegex(ValueError, 'reused, renamed or substituted'):
            self.check()

    def test_physical_numeric_stream_alias_rejects_even_with_matching_hashes(self):
        row = self.report['commands'][0]
        first, second = (self.root / row[stream]['path'] for stream in ('stdout', 'stderr'))
        second.unlink()
        os.link(first, second)
        for stream in ('stdout', 'stderr'):
            receipt = row['stream_evidence']['streams'][stream]
            receipt['final_stat'] = run_acceptance.command_file_stat((self.root / receipt['path']).stat())
            receipt.update(inputs.identity(self.root / receipt['path']))
            row[stream] = {key: receipt[key] for key in ('path', 'bytes', 'sha256')}
        with self.assertRaisesRegex(ValueError, 'one owned regular inode'):
            self.check()

    def test_stream_from_before_its_own_numeric_child_rejects(self):
        row = self.report['commands'][0]
        value = row['stream_evidence']
        value['started'] = copy.deepcopy(value['invocation_finished'])
        self.set_flat_clock(row, 'started', value['started'])
        row['duration_seconds'] = (value['finished']['monotonic_ns'] - value['started']['monotonic_ns']) / 1_000_000_000
        with self.assertRaisesRegex(ValueError, 'reverse or escape'):
            self.check()

    def test_omitted_last_numeric_child_rejects(self):
        self.report['commands'].pop()
        with self.assertRaisesRegex(ValueError, 'command inventory'):
            self.check()


class WrapperStreamControls(OwnedTemporary):
    def setUp(self):
        super().setUp()
        self.prepared = {'project': '/synthetic/project'}
        self.execution = {'schema': 2, 'java_versions': []}
        self.set_flat_clock(self.execution, 'started', run_acceptance.command_clock())
        for label, argv, timeout in [('java-version', ['java', '-version'], 15),
                                      ('javac-version', ['javac', '-version'], 15),
                                      ('acceptance', [sys.executable, '-B', 'acceptance.py'], 6600)]:
            row = self.observed_command('', label, argv=argv, cwd=self.prepared['project'],
                                        timeout_seconds=timeout, returncode=0, timed_out=False)
            if label == 'acceptance':
                self.execution['execution'] = row
            else:
                self.execution['java_versions'].append(row)
        self.set_flat_clock(self.execution, 'finished', run_acceptance.command_clock())

    def check(self):
        return verify.verify_wrapper_streams(self.execution, self.prepared, self.root)

    def test_exact_synthetic_child_stream_roles_and_intervals_are_accepted(self):
        rows = self.check()
        self.assertEqual(6, len([row for row in rows if row['path'].endswith(('.stdout.log', '.stderr.log'))]))
        expected = sum(3 + len(row['stream_evidence']['after_witnesses'])
                       for row in self.execution['java_versions'] + [self.execution['execution']])
        self.assertEqual(expected, len(rows))

    def test_java_version_streams_cannot_replace_acceptance_streams(self):
        for stream in ('stdout', 'stderr'):
            (self.root / self.execution['execution'][stream]['path']).unlink()
            self.execution['execution'][stream] = copy.deepcopy(self.execution['java_versions'][0][stream])
        with self.assertRaises((ValueError, FileNotFoundError)):
            self.check()

    def test_dot_alias_does_not_create_a_new_acceptance_stream_role(self):
        self.execution['execution']['stdout']['path'] = './acceptance.stdout.log'
        with self.assertRaisesRegex(ValueError, 'reused, renamed or substituted'):
            self.check()

    def test_version_command_cannot_be_replaced_by_true(self):
        self.execution['java_versions'][0]['argv'] = ['/bin/true']
        with self.assertRaisesRegex(ValueError, 'Outer child invocation'):
            self.check()

    def test_old_acceptance_stream_fails_its_recorded_creation_order(self):
        row = self.execution['execution']
        evidence = row['stream_evidence']
        evidence['started'] = copy.deepcopy(evidence['invocation_finished'])
        self.set_flat_clock(row, 'started', evidence['started'])
        row['duration_seconds'] = (evidence['finished']['monotonic_ns'] - evidence['started']['monotonic_ns']) / 1_000_000_000
        with self.assertRaisesRegex(ValueError, 'reverse or escape'):
            self.check()

    def test_acceptance_interval_cannot_precede_the_java_observations(self):
        row = self.execution['execution']
        first = self.execution['java_versions'][0]
        delta = first['started_unix_ns'] - row['started_unix_ns'] - 1_000_000_000
        def shift(value):
            if isinstance(value, dict):
                if set(value) == {'unix_ns', 'monotonic_ns', 'utc'}:
                    return self.changed_clock(value, delta, delta)
                return {key: shift(item) for key, item in value.items()}
            if isinstance(value, list):
                return [shift(item) for item in value]
            return value
        row['stream_evidence'] = shift(row['stream_evidence'])
        self.set_flat_clock(row, 'started', row['stream_evidence']['started'])
        self.set_flat_clock(row, 'ended', row['stream_evidence']['finished'])
        with self.assertRaisesRegex(ValueError, 'outer child:acceptance'):
            self.check()


class ExclusiveStreamControls(OwnedTemporary):
    """Direct command-receipt boundary; the full outer envelope is tested above."""
    def setUp(self):
        super().setUp()
        self.row = self.observed_command('', 'guard', argv=['SYNTHETIC'],
                                         returncode=0, timeout_seconds=120)

    def check(self):
        # This direct boundary deliberately makes no overall acceptance claim.
        ledger = verify.Artifacts(self.root, 1, 2 ** 63 - 1)
        verify.verify_command_stream_evidence(self.row, '', 'guard', ledger)
        return ledger

    def test_complete_live_creation_receipts_match_all_actual_files(self):
        ledger = self.check()
        self.assertEqual(3 + len(self.row['stream_evidence']['after_witnesses']), len(ledger.rows))

    def test_missing_before_witness_rejects(self):
        self.row['stream_evidence'].pop('before_witness')
        with self.assertRaisesRegex(ValueError, 'Missing, partial or additional'):
            self.check()

    def test_missing_after_witness_rejects(self):
        self.row['stream_evidence']['after_witnesses'] = []
        with self.assertRaisesRegex(ValueError, 'After-witness inventory'):
            self.check()

    def test_borrowed_before_witness_rejects(self):
        other = self.observed_command('', 'other', argv=['SYNTHETIC'], returncode=0)
        self.row['stream_evidence']['before_witness'] = other['stream_evidence']['before_witness']
        with self.assertRaisesRegex(ValueError, 'Exclusive file role'):
            self.check()

    def test_borrowed_after_witness_rejects(self):
        other = self.observed_command('', 'other', argv=['SYNTHETIC'], returncode=0)
        self.row['stream_evidence']['after_witnesses'][-1] = other['stream_evidence']['after_witnesses'][-1]
        with self.assertRaisesRegex(ValueError, 'Exclusive file role'):
            self.check()

    def test_renamed_empty_borrowed_witness_cannot_reuse_original_fstat(self):
        other = self.observed_command('', 'other', argv=['SYNTHETIC'], returncode=0)
        receipt = self.row['stream_evidence']['after_witnesses'][-1]
        path = self.root / receipt['path']
        replacement = self.root / other['stream_evidence']['after_witnesses'][-1]['path']
        path.unlink()
        replacement.rename(path)
        with self.assertRaisesRegex(ValueError, 'Live file differs'):
            self.check()

    def test_nonexclusive_open_declaration_rejects(self):
        self.row['stream_evidence']['streams']['stdout']['exclusive_mode'] = 'wb'
        with self.assertRaisesRegex(ValueError, 'Exclusive file role'):
            self.check()

    def test_preexisting_nonempty_initial_file_rejects(self):
        self.row['stream_evidence']['streams']['stdout']['initial_stat']['bytes'] = 1
        with self.assertRaisesRegex(ValueError, 'not initially empty'):
            self.check()

    def test_recorded_final_fstat_must_match_live_metadata(self):
        self.row['stream_evidence']['streams']['stdout']['final_stat']['ctime_ns'] += 1
        with self.assertRaisesRegex(ValueError, 'Live file differs'):
            self.check()

    def test_recorded_initial_inode_cannot_belong_to_another_file(self):
        value = self.row['stream_evidence']['streams']
        value['stdout']['initial_stat']['inode'] = value['stderr']['initial_stat']['inode']
        with self.assertRaisesRegex(ValueError, 'inode ownership changed'):
            self.check()

    def test_actual_inode_replacement_with_identical_bytes_rejects(self):
        receipt = self.row['stream_evidence']['streams']['stdout']
        path = self.root / receipt['path']
        replacement = self.put('replacement', path.read_bytes())
        replacement.replace(path)
        with self.assertRaisesRegex(ValueError, 'Live file differs'):
            self.check()

    def test_actual_old_mtime_cannot_precede_exclusive_initial_stat(self):
        receipt = self.row['stream_evidence']['streams']['stdout']
        path = self.root / receipt['path']
        os.utime(path, ns=(1, 1))
        receipt['final_stat'] = run_acceptance.command_file_stat(path.stat())
        with self.assertRaisesRegex(ValueError, 'predates its recorded exclusive creation'):
            self.check()

    def test_boolean_stat_value_is_not_an_inode(self):
        self.row['stream_evidence']['streams']['stdout']['final_stat']['inode'] = True
        with self.assertRaisesRegex(ValueError, 'Exact filesystem stat fields'):
            self.check()

    def test_fine_unix_clock_reversal_rejects_even_inside_same_iso_microsecond(self):
        receipt = self.row['stream_evidence']['streams']['stdout']
        receipt['opened'] = self.changed_clock(receipt['open_started'], unix_delta=-1, mono_delta=1)
        with self.assertRaisesRegex(ValueError, 'reverse or escape'):
            self.check()

    def test_fine_monotonic_clock_reversal_rejects(self):
        receipt = self.row['stream_evidence']['streams']['stdout']
        receipt['opened'] = self.changed_clock(receipt['open_started'], unix_delta=1, mono_delta=-1)
        with self.assertRaisesRegex(ValueError, 'reverse or escape'):
            self.check()

    def test_iso_cannot_contradict_recorded_integer_time(self):
        self.row['stream_evidence']['streams']['stdout']['opened']['utc'] = '2020-01-01T00:00:00.000000+00:00'
        with self.assertRaisesRegex(ValueError, 'integer-clock truncation'):
            self.check()

    def test_literal_witness_attempt_limit_cannot_be_expanded(self):
        self.row['stream_evidence']['after_witness_attempt_limit'] = 17
        with self.assertRaisesRegex(ValueError, 'attempt bound'):
            self.check()

    def test_literal_poll_interval_cannot_be_reduced(self):
        self.row['stream_evidence']['after_witness_poll_ns'] = 4_999_999
        with self.assertRaisesRegex(ValueError, 'polling bound'):
            self.check()

    def append_actual_extra_witness(self):
        value = self.row['stream_evidence']
        index = len(value['after_witnesses'])
        time.sleep(0.005)
        observer = run_acceptance.CommandStreamEvidence(self.root,
            self.root / 'guard.stdout.log', self.root / 'guard.stderr.log')
        extra = observer.witness('filesystem-after-%02d' % index)
        value['after_witnesses'].append(extra)
        value['finished'] = run_acceptance.command_clock()
        self.set_flat_clock(self.row, 'ended', value['finished'])
        self.row['duration_seconds'] = (value['finished']['monotonic_ns'] - value['started']['monotonic_ns']) / 1_000_000_000
        return value

    def test_successful_first_bracket_cannot_be_followed_by_another_selected_witness(self):
        self.append_actual_extra_witness()
        with self.assertRaisesRegex(ValueError, 'first actual filesystem bracket'):
            self.check()

    def test_reordered_witnesses_reject_with_every_file_retained(self):
        value = self.append_actual_extra_witness()
        value['after_witnesses'][0], value['after_witnesses'][-1] = value['after_witnesses'][-1], value['after_witnesses'][0]
        with self.assertRaisesRegex(ValueError, 'Exclusive file role'):
            self.check()

    def test_partial_cleanup_evidence_cannot_be_a_zero_exit_success(self):
        self.row['stream_evidence']['cleanup_errors'] = ['synthetic recorded cleanup failure']
        with self.assertRaisesRegex(ValueError, 'Missing, partial or additional'):
            self.check()


class ClockPrecisionControls(unittest.TestCase):
    def test_all_one_thousand_integer_microseconds_convert_without_float_rounding(self):
        seconds = 1791798408
        for microsecond in range(1000):
            stamp = datetime.fromtimestamp(seconds, timezone.utc).replace(microsecond=microsecond).isoformat(timespec='microseconds')
            self.assertEqual(seconds * 1_000_000_000 + microsecond * 1000, verify.epoch_ns(stamp))

    def test_correctly_ordered_integer_nanoseconds_can_share_one_iso_microsecond(self):
        floor = 1791798408 * 1_000_000_000 + 123456000
        utc = '2026-10-12T09:46:48.123456+00:00'
        first = {'unix_ns': floor + 900, 'monotonic_ns': 2000000900, 'utc': utc}
        second = {'unix_ns': floor + 950, 'monotonic_ns': 2000000950, 'utc': utc}
        verify.checked_clock(first, 'synthetic earlier child')
        verify.checked_clock(second, 'synthetic later wrapper')
        verify.clocks_ordered(first, second, 'same display microsecond', strict=True)


class LiveEmptyStreamControls(OwnedTemporary):
    def test_actual_empty_python_child_retains_unchanged_empty_stat_and_valid_bracket(self):
        env = os.environ.copy()
        env.update(PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(self.root))
        self.row = run_acceptance.run_child([sys.executable, '-B', '-c', 'pass'], self.root, env,
            self.root / 'empty.stdout.log', self.root / 'empty.stderr.log', 5)
        self.assertEqual(0, self.row['returncode'])
        self.assertNotIn('error', self.row)
        receipts = self.row['stream_evidence']['streams']
        for name in ('stdout', 'stderr'):
            self.assertEqual(receipts[name]['initial_stat'], receipts[name]['final_stat'])
            self.assertEqual(0, receipts[name]['bytes'])
        self.equal_initial_filesystem_ticks_observed = (receipts['stdout']['initial_stat']['ctime_ns']
                                                       == receipts['stderr']['initial_stat']['ctime_ns'])
        ledger = verify.Artifacts(self.root, 1, 2 ** 63 - 1)
        verify.verify_command_stream_evidence(self.row, '', 'empty', ledger)


class JavaObservationFailureControls(OwnedTemporary):
    def test_zero_exit_with_evidence_error_stops_before_long_acceptance_child(self):
        pins = inputs.load_pins()
        expected = dict(pins['future_snapshot'])
        project = self.root / 'project'
        output = self.root / 'output'
        output.mkdir()
        manifest = 'a' * 64
        preparation = {'passed': True, 'status': 'EXACT_NUMERIC19_THEN_LOOKUP21_WIP_PREPARED', 'output': str(output),
                       'project': str(project), 'runtime_source': {'manifest': {'sha256': manifest}}}
        inputs.write_json(output / 'preparation.json', preparation)
        argv = ['run_acceptance.py', '--baseline-repository', str(self.root / 'baseline'),
                '--overlay-repository', str(self.root / 'overlay'), '--lookup-repository', str(self.root / 'lookup'), '--output', str(output),
                '--runtime-manifest-sha256', manifest]
        failure = {'returncode': 0, 'timed_out': False, 'error': 'SYNTHETIC unbracketed witness'}
        inventory = lambda path: ([{'path': 'release-input-snapshot.json', **pins['future_manifest']}]
                                  if path.name == 'reports' else [])
        with patch.object(sys, 'argv', argv), patch.object(inputs, 'verify_runtime_manifest'), \
             patch.object(inputs, 'contract', return_value=(pins, {}, expected, None)), \
             patch.object(inputs, 'verify_prepared_boundaries'), \
             patch.object(inputs, 'scan_inputs', return_value=expected), \
             patch.object(inputs, 'compare_inputs'), patch.object(run_acceptance, 'inventory', side_effect=inventory), \
             patch.object(run_acceptance, 'run_child', return_value=failure) as child:
            self.assertEqual(2, run_acceptance.main())
        self.assertEqual(1, child.call_count)
        self.assertEqual(['java', '-version'], child.call_args.args[0])
        self.execution = inputs.read_json(output / 'execution.json')
        self.assertFalse(self.execution['passed'])
        self.assertNotIn('execution', self.execution)
        self.assertIn('Java toolchain observation failed', self.execution['error'])


class NumericProvenanceControls(unittest.TestCase):
    def setUp(self):
        self.positive = {'schema': 1, 'originalFixture': {'path': '/synthetic/original.dex', 'sha256': '1' * 64},
                         'targetDex': {'path': '/synthetic/rebuilt.dex', 'sha256': '2' * 64},
                         'rebuiltApk': {'path': '/synthetic/signed.apk', 'sha256': '3' * 64},
                         'classPins': {'recovered.ui.DayTriggerValueMethods': {'path': '/synthetic/helper.class', 'sha256': '4' * 64}}}

    def test_exact_two_declared_provenance_faults_are_accepted_without_mutating_positive(self):
        saved = copy.deepcopy(self.positive)
        original = copy.deepcopy(self.positive)
        original['targetDex'] = copy.deepcopy(original['originalFixture'])
        wrong = copy.deepcopy(self.positive)
        wrong['classPins']['recovered.ui.DayTriggerValueMethods']['sha256'] = '0' * 64
        verify.verify_provenance_config(original, self.positive, 'original-as-rebuilt-rejected')
        verify.verify_provenance_config(wrong, self.positive, 'wrong-helper-class-rejected')
        self.assertEqual(saved, self.positive)

    def test_unchanged_positive_cannot_stand_in_for_either_provenance_fault(self):
        for name in ('original-as-rebuilt-rejected', 'wrong-helper-class-rejected'):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'declared fault'):
                verify.verify_provenance_config(self.positive, self.positive, name)

    def test_additional_apk_change_rejects_despite_the_expected_fault(self):
        wrong = copy.deepcopy(self.positive)
        wrong['classPins']['recovered.ui.DayTriggerValueMethods']['sha256'] = '0' * 64
        wrong['rebuiltApk']['sha256'] = 'f' * 64
        with self.assertRaisesRegex(ValueError, 'changed another input'):
            verify.verify_provenance_config(wrong, self.positive, 'wrong-helper-class-rejected')

    def test_same_hash_with_another_original_path_rejects(self):
        original = copy.deepcopy(self.positive)
        original['targetDex'] = copy.deepcopy(original['originalFixture'])
        original['targetDex']['path'] = '/synthetic/alias-original.dex'
        with self.assertRaisesRegex(ValueError, 'declared fault'):
            verify.verify_provenance_config(original, self.positive, 'original-as-rebuilt-rejected')


class JavaPolicyControls(OwnedTemporary):
    def setUp(self):
        super().setUp()
        self.start = time.time_ns() - 10_000_000
        self.java = self.put('jdk/bin/java', b'SYNTHETIC EXECUTABLE IDENTITY ONLY')
        self.vm = self.put('jdk/lib/server/libjvm.so', b'SYNTHETIC VM IDENTITY ONLY')
        argv = [str(self.java), '-XX:-OmitStackTraceInFastThrow', '-XX:+ShowCodeDetailsInExceptionMessages', '-XX:+PrintFlagsFinal', '-version']
        self.text = ('COMMAND: ' + json.dumps(argv) + '\n bool OmitStackTraceInFastThrow = false {product}\n'
                     ' bool ShowCodeDetailsInExceptionMessages = true {product}\n')
        self.policy = {'passed': True, 'androidRuntime': False,
                       'scope': 'Host UI exception runtime only; unchanged APK and exact injected messages',
                       'java_executable': str(self.java), 'java_sha256': inputs.identity(self.java)['sha256'],
                       'vm_library': str(self.vm), 'vm_library_sha256': inputs.identity(self.vm)['sha256'],
                       'argv': argv, 'log': 'ui-runtime-policy.log',
                       'effective_flags': {'OmitStackTraceInFastThrow': False, 'ShowCodeDetailsInExceptionMessages': True}}

    def check(self):
        log = self.put('reports/ui-runtime-policy.log', self.text.encode())
        self.policy['log_sha256'] = inputs.identity(log)['sha256']
        self.put('reports/ui-runtime-policy.json', inputs.encoded(self.policy))
        ledger = verify.Artifacts(self.root, self.start, time.time_ns() + 10_000_000)
        with patch.object(verify.shutil, 'which', return_value=str(self.java)):
            return verify.verify_java_policy(ledger)

    def test_synthetic_actual_file_and_raw_effective_flag_binding_is_accepted(self):
        self.assertEqual(str(self.java), self.check())

    def test_changed_actual_java_bytes_reject_the_retained_policy_hash(self):
        self.java.write_bytes(b'DIFFERENT SYNTHETIC EXECUTABLE')
        with self.assertRaisesRegex(ValueError, 'executable identity'):
            self.check()

    def test_effective_raw_flag_cannot_be_overridden_by_a_true_summary(self):
        self.text = self.text.replace('OmitStackTraceInFastThrow = false', 'OmitStackTraceInFastThrow = true')
        with self.assertRaisesRegex(ValueError, 'effective flag'):
            self.check()

    def test_ambiguous_raw_effective_flag_is_rejected(self):
        self.text += ' bool OmitStackTraceInFastThrow = false {product}\n'
        with self.assertRaisesRegex(ValueError, 'effective flag'):
            self.check()


class PreservedReportSchemaControls(unittest.TestCase):
    def engine(self):
        return {'selection': 'all', 'scope': 'Original selected DEX / recovered Java / rebuilt DEX, with controlled Android/action/store/clock/thread boundaries; not Android runtime'}

    def test_exact_preserved_engine_scope_accepts_its_observed_flag_omission(self):
        verify.verify_suite_scope('engine', self.engine())

    def test_engine_explicit_android_claim_rejects_despite_host_scope_text(self):
        report = self.engine()
        report['androidRuntime'] = True
        with self.assertRaisesRegex(ValueError, 'exact host scope'):
            verify.verify_suite_scope('engine', report)

    def test_engine_partial_selection_or_changed_scope_rejects(self):
        for key, value in [('selection', 'partial'), ('scope', 'another runtime')]:
            report = self.engine()
            report[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                verify.verify_suite_scope('engine', report)

    def test_other_suites_still_require_their_explicit_runtime_flag(self):
        for name in ('legacy', 'core', 'environment', 'ui'):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'omitted its explicit'):
                verify.verify_suite_scope(name, {})


# Exact nineteen vectors retained from the frozen combined design.
LOOKUP_COMMAND_SPEC = [{'directory': 'positive-pipeline',
  'name': 'd8-helper',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar',
           'com.android.tools.r8.D8',
           '--release',
           '--no-desugaring',
           '--min-api',
           '23',
           '--output',
           '<project>/reports/<lookup-evidence>/positive-pipeline/d8',
           '<project>/reports/<lookup-evidence>/positive-pipeline/inputs.jar']},
 {'directory': 'positive-pipeline',
  'name': 'disassemble-helper',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar',
           'com.android.tools.smali.baksmali.Main',
           'd',
           '--api',
           '23',
           '--use-locals',
           '-o',
           '<project>/reports/<lookup-evidence>/positive-pipeline/helper-smali',
           '<project>/reports/<lookup-evidence>/positive-pipeline/d8/classes.dex']},
 {'directory': 'positive-pipeline',
  'name': 'assemble-target',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar',
           'com.android.tools.smali.smali.Main',
           'a',
           '--api',
           '23',
           '-j',
           '2',
           '-o',
           '<project>/reports/<lookup-evidence>/positive-pipeline/lookup-target.dex',
           '<project>/reports/<lookup-evidence>/positive-pipeline/target-smali']},
 {'directory': '',
  'name': 'numeric-before-instructions',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar:<project>/build/java/hostclasses:<project>/tools/classes',
           'InspectMethod',
           '<project>/build/hybrid/classes3.dex',
           'Lcom/arlosoft/macrodroid/triggers/DayTrigger;->r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I',
           '<project>/reports/<lookup-evidence>/numeric-before-instructions.json']},
 {'directory': '',
  'name': 'signed-apk-instructions',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar:<project>/build/java/hostclasses:<project>/tools/classes',
           'InspectMethod',
           '<project>/build/hybrid/classes3.dex',
           'Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;',
           '<project>/reports/<lookup-evidence>/signed-apk-instructions.json']},
 {'directory': '',
  'name': 'positive-transplant-instructions',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar:<project>/build/java/hostclasses:<project>/tools/classes',
           'InspectMethod',
           '<project>/reports/<lookup-evidence>/positive-pipeline/lookup-target.dex',
           'Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;',
           '<project>/reports/<lookup-evidence>/positive-transplant-instructions.json']},
 {'directory': 'positive',
  'name': 'execute',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-XX:-OmitStackTraceInFastThrow',
           '-XX:+ShowCodeDetailsInExceptionMessages',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar:<project>/build/java/hostclasses:<project>/tools/classes',
           'DayLookupControlHarness',
           '<project>/reports/<lookup-evidence>/positive/config.json',
           '<project>/reports/<lookup-evidence>/positive/result.json']},
 {'directory': 'case-sensitive-pipeline',
  'name': 'd8-helper',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar',
           'com.android.tools.r8.D8',
           '--release',
           '--no-desugaring',
           '--min-api',
           '23',
           '--output',
           '<project>/reports/<lookup-evidence>/case-sensitive-pipeline/d8',
           '<project>/reports/<lookup-evidence>/case-sensitive-pipeline/inputs.jar']},
 {'directory': 'case-sensitive-pipeline',
  'name': 'disassemble-helper',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar',
           'com.android.tools.smali.baksmali.Main',
           'd',
           '--api',
           '23',
           '--use-locals',
           '-o',
           '<project>/reports/<lookup-evidence>/case-sensitive-pipeline/helper-smali',
           '<project>/reports/<lookup-evidence>/case-sensitive-pipeline/d8/classes.dex']},
 {'directory': 'case-sensitive-pipeline',
  'name': 'assemble-target',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar',
           'com.android.tools.smali.smali.Main',
           'a',
           '--api',
           '23',
           '-j',
           '2',
           '-o',
           '<project>/reports/<lookup-evidence>/case-sensitive-pipeline/lookup-target.dex',
           '<project>/reports/<lookup-evidence>/case-sensitive-pipeline/target-smali']},
 {'directory': 'case-sensitive-dex-fault',
  'name': 'execute',
  'expected_returncode': 3,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-XX:-OmitStackTraceInFastThrow',
           '-XX:+ShowCodeDetailsInExceptionMessages',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar:<project>/build/java/hostclasses:<project>/tools/classes',
           'DayLookupControlHarness',
           '<project>/reports/<lookup-evidence>/case-sensitive-dex-fault/config.json',
           '<project>/reports/<lookup-evidence>/case-sensitive-dex-fault/result.json']},
 {'directory': 'last-match-pipeline',
  'name': 'd8-helper',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar',
           'com.android.tools.r8.D8',
           '--release',
           '--no-desugaring',
           '--min-api',
           '23',
           '--output',
           '<project>/reports/<lookup-evidence>/last-match-pipeline/d8',
           '<project>/reports/<lookup-evidence>/last-match-pipeline/inputs.jar']},
 {'directory': 'last-match-pipeline',
  'name': 'disassemble-helper',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar',
           'com.android.tools.smali.baksmali.Main',
           'd',
           '--api',
           '23',
           '--use-locals',
           '-o',
           '<project>/reports/<lookup-evidence>/last-match-pipeline/helper-smali',
           '<project>/reports/<lookup-evidence>/last-match-pipeline/d8/classes.dex']},
 {'directory': 'last-match-pipeline',
  'name': 'assemble-target',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar',
           'com.android.tools.smali.smali.Main',
           'a',
           '--api',
           '23',
           '-j',
           '2',
           '-o',
           '<project>/reports/<lookup-evidence>/last-match-pipeline/lookup-target.dex',
           '<project>/reports/<lookup-evidence>/last-match-pipeline/target-smali']},
 {'directory': 'last-match-dex-fault',
  'name': 'execute',
  'expected_returncode': 3,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-XX:-OmitStackTraceInFastThrow',
           '-XX:+ShowCodeDetailsInExceptionMessages',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar:<project>/build/java/hostclasses:<project>/tools/classes',
           'DayLookupControlHarness',
           '<project>/reports/<lookup-evidence>/last-match-dex-fault/config.json',
           '<project>/reports/<lookup-evidence>/last-match-dex-fault/result.json']},
 {'directory': 'original-as-rebuilt-rejected',
  'name': 'execute',
  'expected_returncode': 1,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-XX:-OmitStackTraceInFastThrow',
           '-XX:+ShowCodeDetailsInExceptionMessages',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar:<project>/build/java/hostclasses:<project>/tools/classes',
           'DayLookupControlHarness',
           '<project>/reports/<lookup-evidence>/original-as-rebuilt-rejected/config.json',
           '<project>/reports/<lookup-evidence>/original-as-rebuilt-rejected/result.json']},
 {'directory': 'wrong-helper-class-rejected',
  'name': 'execute',
  'expected_returncode': 1,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-XX:-OmitStackTraceInFastThrow',
           '-XX:+ShowCodeDetailsInExceptionMessages',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar:<project>/build/java/hostclasses:<project>/tools/classes',
           'DayLookupControlHarness',
           '<project>/reports/<lookup-evidence>/wrong-helper-class-rejected/config.json',
           '<project>/reports/<lookup-evidence>/wrong-helper-class-rejected/result.json']},
 {'directory': 'positive-restoration',
  'name': 'execute',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-XX:-OmitStackTraceInFastThrow',
           '-XX:+ShowCodeDetailsInExceptionMessages',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar:<project>/build/java/hostclasses:<project>/tools/classes',
           'DayLookupControlHarness',
           '<project>/reports/<lookup-evidence>/positive-restoration/config.json',
           '<project>/reports/<lookup-evidence>/positive-restoration/result.json']},
 {'directory': '',
  'name': 'numeric-after-instructions',
  'expected_returncode': 0,
  'timeout_seconds': 120,
  'argv': ['<java>',
           '-Xmx512m',
           '-cp',
           '<project>/tools/lib/jadx-r2721.4574686-all.jar:<project>/build/java/hostclasses:<project>/tools/classes',
           'InspectMethod',
           '<project>/build/hybrid/classes3.dex',
           'Lcom/arlosoft/macrodroid/triggers/DayTrigger;->r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I',
           '<project>/reports/<lookup-evidence>/numeric-after-instructions.json']}]


class CombinedStagesControls(OwnedTemporary):
    """Small policy tree with the real 19/21 path topology; never an app tree."""
    def setUp(self):
        super().setUp()
        self.pins = copy.deepcopy(inputs.load_pins())
        self.project = self.root / 'project'; self.project.mkdir()
        self.output = self.root / 'proof'; (self.output / 'inputs').mkdir(parents=True)
        for name in inputs.INPUT_DIRECTORIES: (self.project / name).mkdir()
        self.numeric_root = self.root / 'numeric-capsule'
        for row in self.pins['source_changes']:
            if row['baseline'] is not None: self.put('project/' + row['path'], ('SYNTHETIC BASE ' + row['path']).encode())
        self.put('project/source/unrelated-policy-input.txt', b'SYNTHETIC UNCHANGED')
        self.base = inputs.scan_inputs(self.project)
        numeric = []
        for old in self.pins['source_changes']:
            raw = ('SYNTHETIC NUMERIC ' + old['path']).encode()
            source = self.put('numeric-capsule/' + old['source'], raw)
            before = self.base['entries'].get(old['path'])
            numeric.append({'path':old['path'], 'source':old['source'], 'baseline':None if before is None else {'bytes':before['size'],'sha256':before['sha256']},
                            'candidate':inputs.identity(source),'must_be_absent_if_new':before is None})
        self.middle = inputs.derive(self.base, numeric)
        lookup = []
        for old in self.pins['lookup_source_changes']:
            raw = ('SYNTHETIC LOOKUP ' + old['path']).encode()
            source = self.put('proof/inputs/lookup-overlay/' + old['source'], raw)
            before = self.middle['entries'].get(old['path'])
            lookup.append({'path':old['path'],'source':old['source'],'baseline':None if before is None else {'bytes':before['size'],'sha256':before['sha256']},
                           'candidate':inputs.identity(source),'must_be_absent_if_new':before is None})
        self.future = inputs.derive(self.middle, lookup)
        self.pins.update(source_changes=numeric,lookup_source_changes=lookup,baseline_files=self.base['files'],
            numeric_future_snapshot={k:self.middle[k] for k in ('files','snapshot_sha256')},numeric_future_manifest=inputs.byte_identity(inputs.encoded(self.middle)),
            future_snapshot={k:self.future[k] for k in ('files','snapshot_sha256')},future_manifest=inputs.byte_identity(inputs.encoded(self.future)))
        only = sorted({r['path'] for r in numeric}-{r['path'] for r in lookup})
        self.pins['numeric_only_files']=[{'path':name,**self.future['entries'][name]} for name in only]
        self.context={'numeric_root':self.numeric_root,'baseline_snapshot':self.base,'numeric_snapshot':self.middle,'future_snapshot':self.future}
        self.numeric_manifest={'active_files':[],'source_changes':numeric}
        self.lookup_manifest={'changes':[{'path':r['path'],'baseline':r['baseline'],'after':r['candidate'],'must_be_absent_if_new':r['must_be_absent_if_new']} for r in lookup]}

    def derive(self):
        return inputs.combined_inventory_contract(self.pins,self.base,self.numeric_manifest,self.lookup_manifest)

    def apply(self):
        self.records=prepare.apply_source_stages(self.project,self.output,self.pins,self.base,self.future,self.context)
        return self.records

    def test_real_small_tree_visits_both_complete_physical_boundaries(self):
        self.assertEqual((self.middle,self.future),self.derive())
        records=self.apply()
        self.assertEqual(['numeric','lookup'],[row['stage'] for row in records])
        self.assertEqual([19,21],[row['source_paths'] for row in records])
        self.assertEqual([7,6],[row['new_files'] for row in records])
        inputs.compare_inputs(inputs.scan_inputs(self.project),self.future)
        self.assertEqual(b'SYNTHETIC UNCHANGED',(self.project/'source/unrelated-policy-input.txt').read_bytes())
        for name,expected in [('baseline',self.base),('numeric',self.middle),('combined',self.future)]:
            self.assertEqual(expected,inputs.read_json(self.output/'inputs'/(name+'-complete-inputs.json')))

    def test_lookup_cannot_be_applied_directly_to_the_baseline(self):
        with self.assertRaisesRegex(ValueError,'baseline differs|already exists'):
            inputs.derive(self.base,self.pins['lookup_source_changes'])

    def test_wrong_intermediate_manifest_rejects_before_any_source_write(self):
        self.pins['numeric_future_snapshot']['snapshot_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'numeric intermediate'):self.derive()
        inputs.compare_inputs(inputs.scan_inputs(self.project),self.base)

    def test_omitted_or_duplicate_lookup_stage_role_is_rejected(self):
        good=copy.deepcopy(self.pins['lookup_source_changes'])
        for changed in (good[:-1],good[:-1]+[good[0]]):
            with self.subTest(size=len(changed)):
                self.pins['lookup_source_changes']=changed
                with self.assertRaisesRegex(ValueError,'path counts|source roles'):self.derive()
        self.pins['lookup_source_changes']=good

    def test_four_numeric_only_file_pins_are_required(self):
        self.pins['numeric_only_files'][0]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'numeric-only'):self.derive()

    def test_union_cannot_drop_or_add_a_role(self):
        self.pins['source_union_paths']=self.pins['source_union_paths'][:-1]
        with self.assertRaisesRegex(ValueError,'union'):self.derive()

    def test_mutated_physical_baseline_rejects_before_numeric_replacement(self):
        original=(self.project/'acceptance.py').read_bytes()
        (self.project/'source/unrelated-policy-input.txt').write_bytes(b'CHANGED')
        with self.assertRaisesRegex(ValueError,'Full input inventory differs'):self.apply()
        self.assertEqual(original,(self.project/'acceptance.py').read_bytes())
        self.assertFalse((self.output/'inputs/numeric-complete-inputs.json').exists())

    def test_missing_lookup_payload_preserves_the_completed_numeric_stage_only(self):
        last=self.pins['lookup_source_changes'][-1]
        (self.output/'inputs/lookup-overlay'/last['source']).unlink()
        with self.assertRaisesRegex(ValueError,'Missing regular file'):self.apply()
        inputs.compare_inputs(inputs.scan_inputs(self.project),self.middle)
        self.assertTrue((self.output/'inputs/numeric-complete-inputs.json').is_file())
        self.assertFalse((self.output/'inputs/combined-complete-inputs.json').exists())

    def test_altered_lookup_candidate_cannot_replace_any_numeric_stage_file(self):
        last=self.pins['lookup_source_changes'][-1]
        (self.output/'inputs/lookup-overlay'/last['source']).write_bytes(b'OLD RECORDER OR OTHER PAYLOAD')
        with self.assertRaisesRegex(ValueError,'Exact file identity differs'):self.apply()
        inputs.compare_inputs(inputs.scan_inputs(self.project),self.middle)

    def test_recorded_stage_order_and_counts_are_independently_required(self):
        records=self.apply()
        prepared={'passed':True,'status':'EXACT_NUMERIC19_THEN_LOOKUP21_WIP_PREPARED','source_stages':list(reversed(records))}
        with self.assertRaisesRegex(ValueError,'Physical source-stage receipt differs'):
            inputs.verify_prepared_boundaries(self.pins,prepared,self.output,self.context)
        prepared['source_stages']=records;prepared['complete_baseline_files_checked']=True
        with self.assertRaisesRegex(ValueError,'Preparation count differs'):
            inputs.verify_prepared_boundaries(self.pins,prepared,self.output,self.context)


class LookupCapsuleControls(OwnedTemporary):
    def setUp(self):
        super().setUp();self.capsule=self.root/'capsule';self.capsule.mkdir()
        self.put('capsule/project/example.py',b'SYNTHETIC SOURCE');self.put('capsule/README.md',b'SYNTHETIC CAPSULE')
        rows=[{'path':p.relative_to(self.capsule).as_posix(),**inputs.identity(p),'mode':0o644} for p in sorted(self.capsule.rglob('*')) if p.is_file()]
        inputs.write_json(self.capsule/'checkpoint.json',{'files':rows})
        self.spec={'path':'capsule','checkpoint':inputs.identity(self.capsule/'checkpoint.json'),'file_count':2}

    def check(self):return inputs.checked_capsule(self.root,self.spec)
    def test_complete_small_capsule_is_accepted_only_as_a_transport_fixture(self):self.assertEqual(self.capsule,self.check()[0])
    def test_unlisted_file_rejects_even_if_checkpoint_is_intact(self):
        self.put('capsule/unlisted',b'EXTRA')
        with self.assertRaisesRegex(ValueError,'omitted or extra'):self.check()
    def test_changed_payload_rejects_before_preparation(self):
        self.put('capsule/project/example.py',b'OLD RECORDER')
        with self.assertRaisesRegex(ValueError,'Exact file identity differs'):self.check()
    def test_rehashed_checkpoint_is_not_the_frozen_checkpoint(self):
        value=inputs.read_json(self.capsule/'checkpoint.json');value['unreviewed']=True
        (self.capsule/'checkpoint.json').write_bytes(inputs.encoded(value))
        with self.assertRaisesRegex(ValueError,'Exact file identity differs'):self.check()
    def test_mode_change_rejects_with_unchanged_bytes(self):
        (self.capsule/'project/example.py').chmod(0o600)
        with self.assertRaisesRegex(ValueError,'mode differs'):self.check()


class LookupCommandControls(OwnedTemporary):
    """The frozen design vectors are independent of the new reconstruction function."""
    def setUp(self):
        super().setUp();self.java='/synthetic/jdk/bin/java';self.folder='reports/day-lookup-dex-synthetic'
        self.report={'schema':2,'command_stream_evidence_schema':2,
                     'command_stream_evidence_provider':'day_numeric_dex_controls.CommandStreamEvidence','commands':[]}
        self.set_flat_clock(self.report,'started',run_acceptance.command_clock())
        for spec in LOOKUP_COMMAND_SPEC:
            directory=spec['directory'];label=spec['name']
            argv=[part.replace('<project>',str(self.root)).replace('reports/<lookup-evidence>',self.folder).replace('<java>',self.java) for part in spec['argv']]
            row=self.observed_command(self.folder+('/'+directory if directory else ''),label,name=label,argv=argv,
                timeout_seconds=120,returncode=spec['expected_returncode'],expected_returncode=spec['expected_returncode'],
                stream_context_entered=True,timed_out=False,error=None,error_type=None)
            row['recording_finalized']=run_acceptance.command_clock();self.report['commands'].append(row)
        self.set_flat_clock(self.report,'finished',run_acceptance.command_clock())
        self.start=min(self.report['started_unix_ns'],self.report['commands'][0]['stream_evidence']['before_witness']['final_stat']['ctime_ns'])
        self.end=max(self.report['finished_unix_ns'],self.report['commands'][-1]['stream_evidence']['after_witnesses'][-1]['final_stat']['ctime_ns'])

    def check(self):
        artifacts=verify.Artifacts(self.root,self.start,self.end)
        verify.verify_lookup_commands(self.report,self.folder,artifacts,self.java)
        return artifacts

    def test_exact_nineteen_vectors_and_all_live_stream_receipts_are_accepted_as_policy(self):
        ledger=self.check();self.assertEqual(19,len(self.report['commands']))
        self.assertEqual(38,len([n for n in ledger.rows if n.endswith(('.stdout.log','.stderr.log'))]))
        self.assertTrue(all('cwd' not in row for row in self.report['commands']))

    def test_numeric_seventeen_rows_cannot_stand_in_for_lookup(self):
        self.report['commands']=self.report['commands'][:-2]
        with self.assertRaisesRegex(ValueError,'command inventory'):self.check()

    def test_reordered_or_extra_lookup_rows_reject(self):
        self.report['commands'][0],self.report['commands'][1]=self.report['commands'][1],self.report['commands'][0]
        with self.assertRaisesRegex(ValueError,'order or exact argv'):self.check()
        self.report['commands'].append(copy.deepcopy(self.report['commands'][0]))
        with self.assertRaisesRegex(ValueError,'command inventory'):self.check()

    def test_wrong_method_api_classpath_and_harness_reject(self):
        original=copy.deepcopy(self.report['commands'])
        for index,value in [(0,'/bin/true'),(3,'ANOTHER_METHOD'),(6,'ANOTHER_HARNESS')]:
            with self.subTest(index=index):
                self.report['commands']=copy.deepcopy(original);self.report['commands'][index]['argv'][-2]=value
                with self.assertRaisesRegex(ValueError,'order or exact argv'):self.check()
        self.report['commands']=original

    def test_schema_provider_and_literal_boolean_flags_cannot_be_omitted(self):
        original=copy.deepcopy(self.report)
        for key,value in [('schema',1),('command_stream_evidence_schema',True),('command_stream_evidence_provider','another.Provider')]:
            with self.subTest(key=key):
                self.report=copy.deepcopy(original);self.report[key]=value
                with self.assertRaisesRegex(ValueError,'schema differs|provider differs'):self.check()
        self.report=original

    def test_partial_failed_rows_are_rejected_before_complete_success_validation(self):
        original=copy.deepcopy(self.report['commands'][0])
        for key,value in [('stream_context_entered',False),('timed_out',True),('error','ACTUAL FAILED ROW'),('error_type','builtins.OSError')]:
            with self.subTest(key=key):
                self.report['commands'][0]=copy.deepcopy(original);self.report['commands'][0][key]=value
                with self.assertRaisesRegex(ValueError,'stream context|Partial or failed'):self.check()
        self.report['commands'][0]=original

    def test_missing_null_error_fields_cannot_imply_success(self):
        del self.report['commands'][0]['error']
        with self.assertRaisesRegex(ValueError,'Partial or failed'):self.check()

    def test_expected_exit_actual_exit_and_timeout_are_literal_integers(self):
        original=copy.deepcopy(self.report['commands'][0])
        for key,value in [('expected_returncode',False),('returncode',False),('timeout_seconds',120.0),('timeout_seconds',121)]:
            with self.subTest(key=key,value=value):
                self.report['commands'][0]=copy.deepcopy(original);self.report['commands'][0][key]=value
                with self.assertRaisesRegex(ValueError,'outcome differs|timeout differs'):self.check()
        self.report['commands'][0]=original

    def test_finalization_cannot_precede_stream_cleanup(self):
        row=self.report['commands'][0];row['recording_finalized']=self.changed_clock(row['stream_evidence']['finished'],-1,-1)
        with self.assertRaisesRegex(ValueError,'row finalization'):self.check()

    def test_finalization_cannot_overlap_the_next_command(self):
        row=self.report['commands'][0];following=self.report['commands'][1]['stream_evidence']['started']
        row['recording_finalized']=self.changed_clock(following,1,1)
        with self.assertRaisesRegex(ValueError,'lookup child'):self.check()

    def test_finalization_cannot_escape_report_completion(self):
        row=self.report['commands'][-1];completion=verify.row_clock(self.report,'finished','fixture')
        row['recording_finalized']=self.changed_clock(completion,1,1)
        with self.assertRaisesRegex(ValueError,'report completion'):self.check()

    def test_finalization_requires_complete_integer_clock_and_exact_utc(self):
        original=copy.deepcopy(self.report['commands'][0]['recording_finalized'])
        for key,value in [('unix_ns',True),('monotonic_ns',1.0),('utc','2020-01-01T00:00:00Z')]:
            with self.subTest(key=key):
                self.report['commands'][0]['recording_finalized']=copy.deepcopy(original)
                self.report['commands'][0]['recording_finalized'][key]=value
                with self.assertRaisesRegex(ValueError,'integer clocks|ISO text'):self.check()
        self.report['commands'][0]['recording_finalized']=original

    def test_hardlinked_lookup_stream_rejects_unchanged_bytes(self):
        source=self.root/self.folder/'positive-pipeline/d8-helper.stdout.log'
        os.link(source,self.root/'alias.stdout')
        with self.assertRaisesRegex(ValueError,'Live file differs'):self.check()

    def test_replaced_lookup_inode_rejects_same_bytes(self):
        source=self.root/self.folder/'positive-pipeline/d8-helper.stdout.log';raw=source.read_bytes()
        replacement=self.put('replacement.log',raw);os.replace(replacement,source)
        with self.assertRaisesRegex(ValueError,'Live file differs'):self.check()

    def test_lookup_witness_bracket_and_cleanup_fields_are_still_required(self):
        del self.report['commands'][0]['stream_evidence']['before_witness']
        with self.assertRaisesRegex(ValueError,'Missing, partial or additional'):self.check()


class CombinedSummaryControls(OwnedTemporary):
    def setUp(self):
        super().setUp();self.pins=inputs.load_pins();self.apk='a'*64
        self.report={'schema':2,'passed':True,'androidRuntime':False,'positive_signed_apk_instruction_match':True,
            'positive_restoration_byte_exact':True,'source_class_fixture_and_apk_unchanged':True,'signed_numeric_method_unchanged':True,
            'status':'TWO_ACTUAL_LOOKUP_DEX_FAULTS_DETECTED_SIGNED_POSITIVE_RESTORED','signed_apk_sha256':self.apk,
            'original_fixture_sha256':self.pins['fixture']['sha256'],'input_inventory_sha256':self.pins['lookup_input_inventory_sha256'],
            'primary_recovered_methods':1,'original_dependency_methods':2,'expected_java_faults':10,'expected_actual_dex_faults':2,
            'provenance_controls_rejected':2,'cases':371,'execution_paths':3,'original_instruction_count':26,
            'rebuilt_instruction_count':23,'conditional_edges_per_path':4,
            'signed_class_registered_methods':sorted(r['method'] for r in self.pins['day_trigger_class_mappings']),
            'micro_dex_preservation_scope':'Only p0 changed in each micro-DEX. Other original methods stay original there; signed class has its complete three registered mappings.'}
    def check(self):verify.verify_lookup_summary(self.report,self.pins,self.apk)
    def test_exact_summary_is_only_a_summary_policy_fixture(self):self.check()
    def test_numeric_summary_wrong_apk_or_fixture_cannot_be_lookup(self):
        for key in ['status','signed_apk_sha256','original_fixture_sha256','input_inventory_sha256']:
            old=self.report[key];self.report[key]='wrong'
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'identity differs'):self.check()
            self.report[key]=old
    def test_missing_primary_packaging_restoration_or_numeric_preservation_rejects(self):
        for key in ['positive_signed_apk_instruction_match','positive_restoration_byte_exact','signed_numeric_method_unchanged']:
            self.report[key]=False
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'incomplete'):self.check()
            self.report[key]=True
    def test_wrong_counts_boolean_counts_or_getter_credit_reject(self):
        for key,value in [('cases',370),('expected_java_faults',9),('expected_actual_dex_faults',1),('provenance_controls_rejected',1),('primary_recovered_methods',3),('original_instruction_count',True),('rebuilt_instruction_count',23.0)]:
            old=self.report[key];self.report[key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'count differs'):self.check()
            self.report[key]=old
    def test_existing_constant_mapping_cannot_be_dropped_from_signed_class_scope(self):
        self.report['signed_class_registered_methods'].remove('requiresScheduleExactAlarm()Z')
        with self.assertRaisesRegex(ValueError,'preservation scope'):self.check()
    def test_exact_101_catalog_keeps_all_91_prefix_rows(self):
        rows=[{'mutation':r['name']} for r in self.pins['ui_mutation_inventory']]
        self.assertEqual(self.pins['ui_mutation_inventory'],verify.verify_combined_ui_inventory(self.pins,rows))
        with self.assertRaisesRegex(ValueError,'inventory or order'):verify.verify_combined_ui_inventory(self.pins,rows[:91])
    def test_reordering_duplication_and_relabeling_cannot_pass_the_combined_catalog(self):
        original=[{'mutation':r['name']} for r in self.pins['ui_mutation_inventory']]
        for changed in [original[1:]+original[:1],original[:-1]+original[:1]]:
            with self.subTest(first=changed[0]),self.assertRaisesRegex(ValueError,'inventory or order'):
                verify.verify_combined_ui_inventory(self.pins,changed)
        bad=copy.deepcopy(self.pins);bad['ui_mutation_inventory'][0]['mutant_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'91-control prefix'):verify.verify_combined_ui_inventory(bad,original)


class LookupByteAndProvenanceControls(OwnedTemporary):
    def setUp(self):
        super().setUp();self.folder='reports/day-lookup-dex-policy'
        for name,raw in [('signed-apk-instructions.json',b'["SYNTHETIC LOOKUP"]'),('positive-transplant-instructions.json',b'["SYNTHETIC LOOKUP"]'),
            ('numeric-before-instructions.json',b'["SYNTHETIC NUMERIC"]'),('numeric-after-instructions.json',b'["SYNTHETIC NUMERIC"]'),
            ('positive/result.json',b'{"SYNTHETIC_POLICY_ONLY":true}'),('positive-restoration/result.json',b'{"SYNTHETIC_POLICY_ONLY":true}')]:
            self.put(self.folder+'/'+name,raw)
        self.cfg={'originalFixture':{'path':'original.dex','sha256':'o'},'rebuiltApk':{'path':'signed.apk','sha256':'a'},
                  'targetDex':{'path':'rebuilt.dex','sha256':'d'},'classPins':{verify.LOOKUP_HELPER:{'path':'lookup.class','sha256':'h'}}}
    def check(self):return verify.verify_lookup_byte_equalities(verify.Artifacts(self.root,1,2**63-1),self.folder)
    def test_exact_byte_equalities_are_accepted_only_as_policy(self):self.check()
    def test_signed_lookup_body_cannot_differ_from_transplant(self):
        self.put(self.folder+'/signed-apk-instructions.json',b'["CHANGED"]')
        with self.assertRaisesRegex(ValueError,'signed lookup instructions'):self.check()
    def test_lookup_cannot_change_signed_numeric_body(self):
        self.put(self.folder+'/numeric-after-instructions.json',b'["CHANGED NUMERIC"]')
        with self.assertRaisesRegex(ValueError,'numeric instructions changed'):self.check()
    def test_equal_decoded_restoration_with_changed_bytes_is_rejected(self):
        self.put(self.folder+'/positive-restoration/result.json',b'{ "SYNTHETIC_POLICY_ONLY": true }')
        with self.assertRaisesRegex(ValueError,'not byte-exact'):self.check()
    def test_both_exact_lookup_provenance_faults_preserve_all_other_roles(self):
        before=copy.deepcopy(self.cfg)
        for name in ['original-as-rebuilt-rejected','wrong-helper-class-rejected']:
            altered=verify.expected_lookup_provenance_config(self.cfg,name)
            verify.verify_lookup_provenance_config(altered,self.cfg,name)
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,'another input|inject its fault'):
                verify.verify_lookup_provenance_config(self.cfg,self.cfg,name)
            altered['rebuiltApk']['sha256']='changed'
            with self.assertRaisesRegex(ValueError,'another input'):
                verify.verify_lookup_provenance_config(altered,self.cfg,name)
        self.assertEqual(before,self.cfg)


class CombinedRegistryControls(OwnedTemporary):
    def setUp(self):
        super().setUp();self.pins=inputs.load_pins()
        self.registry=copy.deepcopy(self.pins['day_trigger_class_mappings'])
        self.registry += [{'target':'Lsynthetic/Policy'+str(i)+';','method':'fixture()V'} for i in range(self.pins['registered_methods']-3)]
        self.put('source/java-method-map.json',inputs.encoded(self.registry))
        declaration={'schema':1,'purpose':'Test-only original getter instructions; no recovered-method credit and not an application build input.','dependencies':self.pins['combined_dependencies']}
        self.put('tests/fixtures/original-dependencies.json',inputs.encoded(declaration)+b'\n')
        dependencies=sorted(r['target']+'->'+r['method'] for r in declaration['dependencies'])
        self.put('tests/fixtures/provenance.json',inputs.encoded({'dependency_keys':dependencies,'dependency_declaration_sha256':self.pins['dependency_declaration']['sha256']}))
    def check(self):return verify.verify_combined_registry(self.root,self.pins)
    def test_exact_three_class_mappings_and_five_uncredited_getters_are_required(self):self.check()
    def test_changed_constant_or_other_helper_binding_is_rejected(self):
        self.registry[0]['expected']['value']=0;self.put('source/java-method-map.json',inputs.encoded(self.registry))
        with self.assertRaisesRegex(ValueError,'constant and two ordinary'):self.check()
    def test_getter_cannot_replace_a_registered_synthetic_policy_key(self):
        getter=self.pins['combined_dependencies'][0]
        self.registry[-1]={'target':getter['target'],'method':getter['method']}
        self.put('source/java-method-map.json',inputs.encoded(self.registry))
        with self.assertRaisesRegex(ValueError,'credited as recovered'):self.check()
    def test_omitted_duplicate_or_wrong_consumer_dependency_is_rejected(self):
        original=inputs.read_json(self.root/'tests/fixtures/original-dependencies.json')
        for kind in ['omitted','duplicate','consumer']:
            value=copy.deepcopy(original)
            if kind=='omitted':value['dependencies'].pop()
            elif kind=='duplicate':value['dependencies'][-1]=copy.deepcopy(value['dependencies'][0])
            else:value['dependencies'][-1]['consumer']=verify.NUMERIC_METHOD
            file=self.put('tests/fixtures/original-dependencies.json',inputs.encoded(value))
            pins=copy.deepcopy(self.pins);pins['dependency_declaration']=inputs.identity(file)
            with self.subTest(kind=kind),self.assertRaisesRegex(ValueError,'consumer/getter rows differ'):
                verify.verify_combined_registry(self.root,pins)


class ProducerCwdControls(OwnedTemporary):
    def setUp(self):
        super().setUp();self.pins={'method_producer_sources':{}}
        body='def run_controls(root):\n    root = root.resolve()\n    def run(argv):\n        return subprocess.run(argv, cwd=root)\n'
        sources={'day_numeric_dex_controls.py':body,'day_lookup_dex_controls.py':body,
                 'ui_negative_control.py':'def main():\n    day_numeric_dex_controls.run_controls(build.ROOT, [])\n    day_lookup_dex_controls.run_controls(build.ROOT, [])\n',
                 'build.py':'ROOT = Path(__file__).resolve().parent\n'}
        for name,raw in sources.items():self.pins['method_producer_sources'][name]=inputs.identity(self.put(name,raw.encode()))
        self.execution={'execution':{'cwd':str(self.root)}}
    def check(self):return verify.verify_method_producer_cwd(self.root,self.pins,self.execution)
    def test_exact_source_and_outer_cwd_do_not_invent_a_child_receipt_field(self):
        result=self.check();self.assertFalse(result['sources']['day_lookup_dex_controls.py']['individual_child_cwd_recorded'])
    def test_wrong_outer_project_cwd_is_rejected(self):
        self.execution['execution']['cwd']=str(self.root/'another')
        with self.assertRaisesRegex(ValueError,'Outer resolved project cwd'):self.check()
    def test_changed_producer_source_rejects_even_with_same_declared_outer_root(self):
        self.put('day_lookup_dex_controls.py',b'def run_controls(root): pass\n')
        with self.assertRaisesRegex(ValueError,'Exact file identity differs'):self.check()
    def test_rehashed_other_cwd_expression_is_rejected_by_ast_contract(self):
        path=self.root/'day_lookup_dex_controls.py';path.write_text(path.read_text().replace('cwd=root','cwd=another'))
        self.pins['method_producer_sources']['day_lookup_dex_controls.py']=inputs.identity(path)
        with self.assertRaisesRegex(ValueError,'cwd expression differs'):self.check()


if __name__ == '__main__':
    unittest.main()
