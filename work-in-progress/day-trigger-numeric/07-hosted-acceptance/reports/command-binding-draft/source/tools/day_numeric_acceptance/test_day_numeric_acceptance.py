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
