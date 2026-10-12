#!/usr/bin/env python3
"""Small adversarial controls for job provenance and fresh-result acceptance.

Synthetic gate reports below exercise rejection policy only. They are never
application execution, signed-build, method-parity, or Android evidence.
"""
import copy
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
        self.temp.cleanup()

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
                                        self.root / 'stdout.log', self.root / 'stderr.log', timeout)

    def test_actual_nonzero_exit_and_both_streams_are_retained(self):
        result = self.execute("import sys; print('stdout evidence'); print('stderr evidence', file=sys.stderr); sys.exit(7)")
        self.assertEqual(7, result['returncode'])
        self.assertFalse(result['timed_out'])
        self.assertEqual(b'stdout evidence\n', (self.root / 'stdout.log').read_bytes())
        self.assertEqual(b'stderr evidence\n', (self.root / 'stderr.log').read_bytes())

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

    def make_report(self, alias_first_streams=False):
        self.start = time.time_ns() - 10_000_000
        self.report = {'started_utc': datetime.now(timezone.utc).isoformat(), 'commands': []}
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
        for index, (subdir, label, code, argv) in enumerate(rows):
            started = datetime.now(timezone.utc).isoformat()
            value = {'name': label, 'argv': argv, 'started_utc': started, 'returncode': code,
                     'timeout_seconds': 120, 'duration_seconds': 0.01}
            prefix = self.folder + ('/' + subdir if subdir else '')
            for stream in ('stdout', 'stderr'):
                name = prefix + '/' + label + '.' + stream + '.log'
                path = self.put(name, ('SYNTHETIC NUMERIC POLICY ONLY ' + name).encode())
                if alias_first_streams and index == 0 and stream == 'stderr':
                    path.unlink()
                    os.link(self.root / value['stdout']['path'], path)
                value[stream] = {'path': name, **inputs.identity(path)}
            value['ended_utc'] = datetime.now(timezone.utc).isoformat()
            self.report['commands'].append(value)
        self.report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        self.end = time.time_ns() + 10_000_000

    def check(self):
        ledger = verify.Artifacts(self.root, self.start, self.end)
        verify.verify_numeric_commands(self.report, self.folder, ledger, self.java)
        return ledger

    def test_exact_seventeen_synthetic_command_rows_preserve_thirty_four_distinct_streams(self):
        self.assertEqual(34, len(self.check().rows))

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
        with self.assertRaisesRegex(ValueError, 'reused another stream'):
            self.check()

    def test_physical_numeric_stream_alias_rejects_even_with_matching_hashes(self):
        self.make_report(alias_first_streams=True)
        with self.assertRaisesRegex(ValueError, 'physical result file'):
            self.check()

    def test_stream_from_before_its_own_numeric_child_rejects(self):
        row = self.report['commands'][0]
        row['started_utc'] = row['ended_utc']
        with self.assertRaisesRegex(ValueError, 'own subprocess interval'):
            self.check()

    def test_omitted_last_numeric_child_rejects(self):
        self.report['commands'].pop()
        with self.assertRaisesRegex(ValueError, 'command inventory'):
            self.check()


class WrapperStreamControls(OwnedTemporary):
    def setUp(self):
        super().setUp()
        self.prepared = {'project': '/synthetic/project'}
        self.execution = {'started_utc': datetime.now(timezone.utc).isoformat(), 'java_versions': []}
        for label, argv, timeout in [('java-version', ['java', '-version'], 15),
                                      ('javac-version', ['javac', '-version'], 15),
                                      ('acceptance', [sys.executable, '-B', 'acceptance.py'], 6600)]:
            row = {'argv': argv, 'cwd': self.prepared['project'], 'timeout_seconds': timeout,
                   'returncode': 0, 'timed_out': False, 'started_unix_ns': time.time_ns()}
            for stream in ('stdout', 'stderr'):
                name = label + '.' + stream + '.log'
                path = self.put(name, ('SYNTHETIC OUTER CHILD POLICY ONLY ' + name).encode())
                row[stream] = {'path': name, **inputs.identity(path)}
            row['ended_unix_ns'] = time.time_ns()
            if label == 'acceptance':
                self.execution['execution'] = row
            else:
                self.execution['java_versions'].append(row)
        self.execution['finished_utc'] = datetime.now(timezone.utc).isoformat()

    def check(self):
        return verify.verify_wrapper_streams(self.execution, self.prepared, self.root)

    def test_exact_synthetic_child_stream_roles_and_intervals_are_accepted(self):
        self.assertEqual(6, len(self.check()))

    def test_java_version_streams_cannot_replace_acceptance_streams(self):
        for stream in ('stdout', 'stderr'):
            (self.root / self.execution['execution'][stream]['path']).unlink()
            self.execution['execution'][stream] = copy.deepcopy(self.execution['java_versions'][0][stream])
        with self.assertRaisesRegex(ValueError, 'reused or renamed'):
            self.check()

    def test_dot_alias_does_not_create_a_new_acceptance_stream_role(self):
        self.execution['execution']['stdout']['path'] = './acceptance.stdout.log'
        with self.assertRaisesRegex(ValueError, 'reused or renamed'):
            self.check()

    def test_version_command_cannot_be_replaced_by_true(self):
        self.execution['java_versions'][0]['argv'] = ['/bin/true']
        with self.assertRaisesRegex(ValueError, 'Outer child invocation'):
            self.check()

    def test_old_acceptance_stream_fails_its_specific_child_window(self):
        row = self.execution['execution']
        row['started_unix_ns'] = row['ended_unix_ns'] - 1
        with self.assertRaisesRegex(ValueError, 'own child interval'):
            self.check()

    def test_acceptance_interval_cannot_precede_the_java_observations(self):
        self.execution['execution']['started_unix_ns'] = self.execution['java_versions'][0]['started_unix_ns']
        with self.assertRaisesRegex(ValueError, 'Outer child chronology'):
            self.check()


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


if __name__ == '__main__':
    unittest.main()
