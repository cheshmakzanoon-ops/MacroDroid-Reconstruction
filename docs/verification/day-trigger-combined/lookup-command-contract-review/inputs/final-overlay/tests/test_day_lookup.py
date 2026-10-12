"""Focused controls for lookup provenance, identity-sensitive observations and coverage.

Small synthetic records test rejection boundaries only; they receive no application
case or instruction credit. Actual Java/DEX fault execution is separate evidence.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import build
import day_numeric_dex_controls as numeric
import day_lookup_dex_controls as lookup
import ui_mutation_catalog as catalog
import ui_negative_control

ROOT = Path(__file__).resolve().parents[1]


def read(path): return json.loads(path.read_text())


def copy_inputs(root):
    for name in ('source/java-method-map.json', lookup.DEPENDENCY_PATH,
                 catalog.LOOKUP_HELPER_PATH, catalog.LOOKUP_CATALOG_PATH):
        path = root / name; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((ROOT / name).read_bytes())


class DayLookupCatalogTests(unittest.TestCase):
    def test_all_ten_measured_source_faults_have_required_labels(self):
        source = (ROOT / catalog.LOOKUP_HELPER_PATH).read_bytes()
        jobs = catalog.load_lookup_mutations(ROOT)
        self.assertEqual(len(jobs), 10)
        self.assertEqual({job['name'].removeprefix('day-lookup-') for job in jobs}, set(lookup.JAVA_FAILURE_COUNTS))
        self.assertTrue(all(job['day_lookup'] is True and job['widget'] is False and job['required_cases']
                            and job['mutant'].encode() != source for job in jobs))
        self.assertEqual((ROOT / catalog.LOOKUP_HELPER_PATH).read_bytes(), source)

    def test_exact_complete_91_job_prefix_is_preserved(self):
        jobs = ui_negative_control.prepared_mutations()
        self.assertEqual(len(jobs), 101)
        prefix = [{key: value.relative_to(build.ROOT).as_posix() if isinstance(value, Path) else value
                   for key, value in row.items()} for row in jobs[:91]]
        digest = hashlib.sha256(json.dumps(prefix, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
        self.assertEqual(digest, 'fcaf78249b265ec4b96b125a6a73b8167d9e76a9b33db81615040ceb1a3438a8')
        self.assertTrue(all(row.get('day_lookup') is True for row in jobs[91:]))

    def test_existing_catalog_loader_source_prefix_is_byte_exact(self):
        prefix = (ROOT / 'ui_mutation_catalog.py').read_bytes()[:6588]
        self.assertEqual(hashlib.sha256(prefix).hexdigest(), '10d8f5b6b7c8c0ff31fac3da7b4c0c269383736ebc185b56a72440a030f4a062')

    def test_changed_lookup_catalog_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); copy_inputs(root); path = root / catalog.LOOKUP_CATALOG_PATH
            path.write_bytes(path.read_bytes() + b'\n')
            with self.assertRaisesRegex(RuntimeError, 'catalog differs'): catalog.load_lookup_mutations(root)

    def test_changed_lookup_positive_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); copy_inputs(root); path = root / catalog.LOOKUP_HELPER_PATH
            path.write_bytes(path.read_bytes() + b'\n')
            with self.assertRaisesRegex(RuntimeError, 'positive source'): catalog.load_lookup_mutations(root)

    def test_exact_combined_and_per_consumer_dependency_sets(self):
        registry = read(ROOT / 'source/java-method-map.json')
        parts = numeric.validate_dependency_declaration(ROOT, registry)
        self.assertEqual(len(registry), 1244)
        self.assertEqual(len({row['target'] for row in registry}), 605)
        self.assertEqual(parts, {numeric.METHOD: set(numeric.GETTERS), lookup.METHOD: set(lookup.GETTERS)})
        self.assertEqual(lookup.validate_dependencies(ROOT, registry), set(lookup.GETTERS))
        self.assertFalse(set(numeric.GETTERS) & set(lookup.GETTERS))
        keys = {row['target'] + '->' + row['method'] for row in registry}
        self.assertEqual(len(keys | set(numeric.GETTERS)), 1247)
        self.assertEqual(len(keys | set(numeric.GETTERS) | set(lookup.GETTERS)), 1249)
        self.assertFalse(keys & (set(numeric.GETTERS) | set(lookup.GETTERS)))

    def test_existing_constant_mapping_is_retained(self):
        entries = [row for row in read(ROOT / 'source/java-method-map.json') if row['target'] == lookup.TARGET]
        self.assertEqual({row['method'] for row in entries}, {lookup.SIGNATURE, numeric.METHOD.split('->', 1)[1], 'requiresScheduleExactAlarm()Z'})
        constant = next(row for row in entries if row['method'] == 'requiresScheduleExactAlarm()Z')
        self.assertEqual(constant['java_source'], 'source/java/recovered/constants/DayTrigger_74d1108d.java')

    def test_missing_or_duplicate_lookup_consumer_is_rejected(self):
        registry = read(ROOT / 'source/java-method-map.json')
        entry = next(row for row in registry if row['target'] + '->' + row['method'] == lookup.METHOD)
        for values in ([row for row in registry if row is not entry], registry + [copy.deepcopy(entry)]):
            with self.subTest(count=len(values)), self.assertRaisesRegex(RuntimeError, 'absent or duplicated'):
                lookup.validate_dependencies(ROOT, values)

    def test_lookup_getter_cannot_receive_recovery_credit(self):
        registry = read(ROOT / 'source/java-method-map.json')
        key = sorted(lookup.GETTERS)[0]; target, method = key.split('->', 1)
        registry.append({'target': target, 'method': method})
        with self.assertRaisesRegex(RuntimeError, 'credited'): lookup.validate_dependencies(ROOT, registry)

    def test_lookup_registry_cannot_select_another_helper_method(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); copy_inputs(root); path = root / 'source/java-method-map.json'; data = read(path)
            next(row for row in data if row['target'] + '->' + row['method'] == lookup.METHOD)['helper_method'] = 'wrong'
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(RuntimeError, 'registry binding'): lookup.target_entry(root)


def report_identity():
    return {'schema': 1, 'cases': 371, 'executionPaths': 3, 'primaryMethod': lookup.METHOD,
            'primaryRecoveredMethods': 1, 'originalDependencyMethods': 2, 'androidRuntime': False,
            'dependencyKeys': sorted(lookup.GETTERS), 'generatedNullMessageCases': sorted(lookup.VM_NULL_CASES),
            'inputInventorySha256': catalog.LOOKUP_INPUT_INVENTORY_SHA256}


def coverage_fixture(count=26):
    methods = []
    for key in sorted({lookup.METHOD, *lookup.GETTERS}):
        primary = key == lookup.METHOD
        size = count - 5 if primary else 3 if 'DictionaryEntry;' in key else 2
        offsets = list(range(size)); edges = ['0:1', '0:2', '1:2', '1:3'] if primary else []
        methods.append({'key': key, 'primaryRecovery': primary, 'requiredOffsets': offsets,
                        'executedOffsets': list(offsets), 'missingOffsets': [], 'requiredEdges': edges,
                        'executedEdges': list(edges), 'missingEdges': [], 'instructionCount': size, 'exceptionRegions': 0})
    return {'methods': methods, 'instructionCount': count, 'executedInstructionCount': count,
            'requiredBranchEdges': 4, 'executedBranchEdges': 4, 'allInstructionsAndEdgesExecuted': True}


class DayLookupCoverageGuardTests(unittest.TestCase):
    def test_exact_report_identity_is_accepted(self): lookup.validate_report_identity(report_identity())

    def test_boolean_and_float_counts_are_rejected(self):
        for key, value in [('schema', True), ('primaryRecoveredMethods', True), ('cases', 371.0), ('originalDependencyMethods', 2.0)]:
            row = report_identity(); row[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(RuntimeError, 'count or schema'): lookup.validate_report_identity(row)

    def test_wrong_method_dependency_inventory_and_case_hash_are_rejected(self):
        for key, value in [('primaryMethod', numeric.METHOD), ('dependencyKeys', sorted(numeric.GETTERS)),
                           ('inputInventorySha256', '0' * 64), ('androidRuntime', True), ('generatedNullMessageCases', [])]:
            row = report_identity(); row[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(RuntimeError, 'identity'): lookup.validate_report_identity(row)

    def test_complete_original_and_rebuilt_rows_are_accepted(self):
        for count in (26, 23): lookup.validate_positive_coverage(coverage_fixture(count), count)

    def test_unknown_coverage_total_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, 'Unknown'): lookup.validate_positive_coverage(coverage_fixture(), 29)

    def test_omitted_or_duplicate_method_rows_are_rejected(self):
        for change in ('omit', 'duplicate'):
            row = coverage_fixture()
            if change == 'omit': row['methods'].pop()
            else: row['methods'][1] = copy.deepcopy(row['methods'][0])
            with self.subTest(change=change), self.assertRaisesRegex(RuntimeError, 'inventory'): lookup.validate_positive_coverage(row, 26)

    def test_uncredited_getter_cannot_become_a_recovery(self):
        row = coverage_fixture(); row['methods'][1]['primaryRecovery'] = True
        with self.assertRaisesRegex(RuntimeError, 'recovery credit'): lookup.validate_positive_coverage(row, 26)

    def test_missing_instruction_and_conditional_edge_are_rejected(self):
        for key in ('executedOffsets', 'executedEdges'):
            row = coverage_fixture(); row['methods'][0][key].pop()
            with self.subTest(key=key), self.assertRaisesRegex(RuntimeError, 'Incomplete'): lookup.validate_positive_coverage(row, 26)

    def test_duplicate_or_boolean_instruction_offsets_are_rejected(self):
        for value in (0, True):
            row = coverage_fixture(); row['methods'][0]['requiredOffsets'][1] = value
            with self.subTest(value=value), self.assertRaisesRegex(RuntimeError, 'Malformed'): lookup.validate_positive_coverage(row, 26)

    def test_edge_target_outside_method_is_rejected(self):
        row = coverage_fixture(); row['methods'][0]['requiredEdges'][1] = '0:99'
        with self.assertRaisesRegex(RuntimeError, 'another instruction'): lookup.validate_positive_coverage(row, 26)

    def test_inconsistent_summary_cannot_hide_missing_coverage(self):
        row = coverage_fixture(); row['executedInstructionCount'] = 25
        with self.assertRaisesRegex(RuntimeError, 'summary'): lookup.validate_positive_coverage(row, 26)


class DayLookupExecutionBindingTests(unittest.TestCase):
    def fixture(self):
        path = str((ROOT / 'test.class').resolve())
        config = {'classPins': {'Example': {'path': path, 'sha256': 'a' * 64}}, 'originalFixture': {'sha256': 'b' * 64}}
        report = {'inputIdentities': copy.deepcopy(config), 'loadedClassOrigins': copy.deepcopy(config['classPins'])}
        return config, report

    def test_exact_command_config_and_loaded_origins_are_accepted(self):
        config, report = self.fixture(); lookup.validate_execution_binding(report, config)

    def test_other_original_fixture_identity_is_rejected(self):
        config, report = self.fixture(); report['inputIdentities']['originalFixture']['sha256'] = 'c' * 64
        with self.assertRaisesRegex(RuntimeError, 'another command'): lookup.validate_execution_binding(report, config)

    def test_changed_omitted_and_extra_loaded_class_are_rejected(self):
        for change in ('changed', 'omitted', 'extra'):
            config, report = self.fixture()
            if change == 'changed': report['loadedClassOrigins']['Example']['sha256'] = 'd' * 64
            elif change == 'omitted': report['loadedClassOrigins'] = {}
            else: report['loadedClassOrigins']['Unbound'] = copy.deepcopy(report['loadedClassOrigins']['Example'])
            with self.subTest(change=change), self.assertRaisesRegex(RuntimeError, 'loaded class origins'):
                lookup.validate_execution_binding(report, config)


def injected_input():
    return {'case': 'injected-iterator-npe', 'expectedExceptionClass': 'java.lang.NullPointerException',
            'expectedReturnIndex': None, 'expectedEvents': ['iterator'], 'injectedFaultAt': 'iterator'}


def injected_observation():
    return {'returnIndex': None, 'exceptionClass': 'java.lang.NullPointerException',
            'rawMessage': 'EXACT_INJECTED_LOOKUP_FAULT:injected-iterator-npe', 'injectedExceptionIdentity': True,
            'events': ['iterator'], 'unsupported': False}


def observer_controls():
    positive = injected_observation(); faults = []
    for key, value in [('rawMessage', 'CHANGED_INJECTED_MESSAGE'), ('injectedExceptionIdentity', False),
                       ('events', []), ('returnIndex', 0), ('unsupported', True)]:
        row = copy.deepcopy(positive); row[key] = value; faults.append(row)
    return {'case': 'injected-iterator-npe', 'positiveAccepted': True, 'changedRecordsRejected': 5,
            'applicationExecutions': 0, 'applicationCoverageCredit': 0, 'positive': positive, 'rejectedRecords': faults}


class DayLookupObservationGuardTests(unittest.TestCase):
    def test_exact_injected_exception_is_accepted(self):
        output = injected_observation(); lookup.validate_raw_observation(output)
        self.assertTrue(lookup.matches_expected(injected_input(), output))

    def test_injected_message_identity_order_type_and_return_faults_are_rejected(self):
        for key, value in [('rawMessage', 'changed'), ('injectedExceptionIdentity', False), ('events', []),
                           ('exceptionClass', 'java.lang.ClassCastException'), ('returnIndex', 0), ('unsupported', True)]:
            output = injected_observation(); output[key] = value
            with self.subTest(key=key): self.assertFalse(lookup.matches_expected(injected_input(), output))

    def test_boolean_return_index_and_missing_raw_field_are_rejected(self):
        for change in ('boolean-index', 'missing-message'):
            output = injected_observation()
            if change == 'boolean-index': output['returnIndex'] = False
            else: del output['rawMessage']
            with self.subTest(change=change), self.assertRaisesRegex(RuntimeError, 'Malformed'): lookup.validate_raw_observation(output)

    def test_generated_message_exclusion_is_limited_to_seven_named_inputs(self):
        output = injected_observation(); output.update(rawMessage='retained VM diagnostic', injectedExceptionIdentity=False)
        for name in sorted(lookup.VM_NULL_CASES):
            row = injected_input(); row.update(case=name, injectedFaultAt=None)
            self.assertTrue(lookup.matches_expected(row, output))
        row = injected_input(); row.update(case='unlisted-null-receiver', injectedFaultAt=None)
        self.assertFalse(lookup.matches_expected(row, output))

    def test_vm_null_name_does_not_exempt_injected_message_or_identity(self):
        row = injected_input(); row['case'] = 'dictionary-null'
        output = injected_observation(); output.update(rawMessage='VM-like diagnostic', injectedExceptionIdentity=False)
        self.assertFalse(lookup.is_vm_null_case(row)); self.assertFalse(lookup.matches_expected(row, output))

    def test_returned_entry_index_compares_by_identity_contract(self):
        row = {'case': 'first-match', 'expectedExceptionClass': None, 'expectedReturnIndex': 0,
               'expectedEvents': ['iterator', 'hasNext@0', 'next@0'], 'injectedFaultAt': None}
        output = {'returnIndex': 0, 'exceptionClass': None, 'rawMessage': None, 'injectedExceptionIdentity': False,
                  'events': list(row['expectedEvents']), 'unsupported': False}
        self.assertTrue(lookup.matches_expected(row, output))
        for value in (1, -1, -2):
            output['returnIndex'] = value; self.assertFalse(lookup.matches_expected(row, output))

    def test_all_five_record_faults_are_separate_and_uncredited(self):
        lookup.validate_observer_controls({'observerRecordControls': observer_controls()}, [injected_input()])

    def test_record_controls_cannot_gain_application_credit(self):
        for key, value in [('applicationExecutions', 1), ('applicationCoverageCredit', 1), ('applicationExecutions', False)]:
            control = observer_controls(); control[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(RuntimeError, 'credit or wrong count'):
                lookup.validate_observer_controls({'observerRecordControls': control}, [injected_input()])

    def test_replacing_fault_record_with_positive_is_rejected(self):
        control = observer_controls(); control['rejectedRecords'][1] = copy.deepcopy(control['positive'])
        with self.assertRaisesRegex(RuntimeError, 'fault records differ'):
            lookup.validate_observer_controls({'observerRecordControls': control}, [injected_input()])


# These controls enter the real production run_controls function and its actual
# nested recorder. A test-only first-boundary hook stops before all application
# input validation. Every generated acceptance report must remain explicitly
# failed. Optional retained output is used by the independent source study.
import os
import subprocess
import sys
import time
import traceback


class _LookupRecorderBoundaryStop(RuntimeError):
    pass


class _LookupRecorderFaultHandle:
    def __init__(self, underlying, flush_error=None, close_error=None):
        self.underlying = underlying
        self.flush_error = flush_error
        self.close_error = close_error

    @property
    def closed(self):
        return self.underlying.closed

    def fileno(self):
        return self.underlying.fileno()

    def flush(self):
        if self.flush_error is not None:
            raise self.flush_error
        self.underlying.flush()

    def close(self):
        self.underlying.close()
        if self.close_error is not None:
            raise self.close_error


class DayLookupRecorderTests(unittest.TestCase):
    """Actual bounded children and explicit I/O faults; zero app-proof credit."""

    def setUp(self):
        retained = os.environ.get('LOOKUP_RECORDER_TEST_REPORT_ROOT')
        if retained:
            self.folder = Path(retained) / self._testMethodName
            self.folder.mkdir(parents=True, exist_ok=False)
        else:
            self.temporary = tempfile.TemporaryDirectory(prefix='lookup-recorder-control-')
            self.folder = Path(self.temporary.name)
            self.addCleanup(self.temporary.cleanup)
        self.commands = self.folder / 'commands'; self.commands.mkdir()
        self.stdout = self.commands / 'actual.stdout.log'
        self.stderr = self.commands / 'actual.stderr.log'
        self.contexts = []
        self.original_context = numeric.CommandStreamEvidence

    def invoke(self, code='pass', expected=0, timeout=5, fault=None, executable=None):
        source = self.folder / 'child.py'; source.write_text(code + '\n')
        argv = [str(executable or sys.executable), '-B', str(source), str(self.stdout)]
        evidence = {'scope': 'Real production recorder only; no application proof.',
                    'application_executions': 0, 'application_coverage_credit': 0,
                    'argv': argv, 'timeout_seconds': timeout, 'expected_returncode': expected,
                    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'boundary_calls': 0}
        original_entry = lookup.target_entry
        nested = [value for value in lookup.run_controls.__code__.co_consts
                  if hasattr(value, 'co_name') and value.co_name == 'run']
        self.assertEqual(1, len(nested))

        def boundary(root):
            evidence['boundary_calls'] += 1
            self.assertEqual(self.folder.resolve(), root)
            caller = sys._getframe(1)
            self.assertIs(caller.f_code, lookup.run_controls.__code__)
            run = caller.f_locals['run']
            self.assertIs(run.__code__, nested[0])
            self.assertIs(run.__globals__, lookup.__dict__)
            run(self.commands, 'actual', argv, expected=expected, timeout=timeout)
            raise _LookupRecorderBoundaryStop('Stopped before every application input and signed-proof gate')

        def context_factory(*arguments, **keywords):
            context = self.original_context(*arguments, **keywords)
            self.assertIs(type(context), self.original_context)
            self.contexts.append(context)
            if fault is not None:
                fault(context)
            return context

        caught = None
        lookup.target_entry = boundary
        if fault is not None:
            numeric.CommandStreamEvidence = context_factory
        try:
            lookup.run_controls(self.folder, [])
        except BaseException as error:
            caught = error
            evidence.update(caught_type=type(error).__module__ + '.' + type(error).__qualname__, caught_error=repr(error))
            (self.folder / 'actual.traceback.txt').write_text(traceback.format_exc())
        finally:
            lookup.target_entry = original_entry
            numeric.CommandStreamEvidence = self.original_context
            path = self.folder / 'reports/day-lookup-dex-controls.json'
            if path.exists():
                evidence['acceptance_report'] = read(path)
            evidence['context_handles_closed'] = [all(handle.closed for handle in context.handles.values()) for context in self.contexts]
            files = {}
            for role, path in [('stdout', self.stdout), ('stderr', self.stderr),
                               ('extra_hardlink', self.commands / 'extra-hardlink.txt')]:
                if path.exists():
                    st = path.stat()
                    files[role] = {'bytes': st.st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                                   'device': st.st_dev, 'inode': st.st_ino, 'links': st.st_nlink,
                                   'mtime_ns': st.st_mtime_ns, 'ctime_ns': st.st_ctime_ns}
            evidence['observed_files'] = files
            (self.folder / 'observation.json').write_text(json.dumps(evidence, indent=2) + '\n')
        self.assertIsNotNone(caught)
        self.assertEqual(1, evidence['boundary_calls'])
        report = evidence['acceptance_report']
        self.assertIs(report['passed'], False)
        self.assertEqual('LOOKUP_DEX_CONTROL_FAILED', report['status'])
        self.assertEqual(2, report['schema'])
        self.assertEqual(2, report['command_stream_evidence_schema'])
        self.assertEqual('day_numeric_dex_controls.CommandStreamEvidence', report['command_stream_evidence_provider'])
        self.assertNotIn('positive_signed_apk_instruction_match', report)
        self.assertEqual(1, len(report['commands']), 'Every entered recorder attempt needs a finalized row, including failures')
        row = report['commands'][0]
        self.assertEqual(argv, row['argv']); self.assertEqual(timeout, row['timeout_seconds'])
        self.assertEqual(expected, row['expected_returncode'])
        self.assertEqual(2, row['stream_evidence']['schema'])
        self.assertIs(type(row['recording_finalized']['monotonic_ns']), int)
        self.assertLessEqual(row['started_monotonic_ns'], row['recording_finalized']['monotonic_ns'])
        self.assertLessEqual(row['recording_finalized']['monotonic_ns'], report['finished_monotonic_ns'])
        self.assertTrue(all(evidence['context_handles_closed']))
        if isinstance(caught, _LookupRecorderBoundaryStop):
            self.assertIsNone(row['error']); self.assertIsNone(row['error_type']); self.assertIs(row['timed_out'], False)
            self.assertIs(row['stream_context_entered'], True)
            self.assertTrue(row['stream_evidence']['filesystem_bracket_complete'])
            self.assertNotIn('cleanup_errors', row['stream_evidence'])
            for role, path in [('stdout', self.stdout), ('stderr', self.stderr)]:
                self.assertEqual(path.stat().st_size, row[role]['bytes'])
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row[role]['sha256'])
        else:
            self.assertEqual(type(caught).__module__ + '.' + type(caught).__qualname__, row['error_type'])
            self.assertEqual(repr(caught), row['error'])
            self.assertIs(row['timed_out'], isinstance(caught, subprocess.TimeoutExpired))
        return caught, report, row

    def io_fault(self, flush=None, close=None, second_open=None):
        def install(context):
            original = context.open_file
            def open_file(path):
                if path == self.stderr and second_open is not None:
                    raise second_open
                handle, row = original(path)
                if path == self.stderr and (flush is not None or close is not None):
                    return _LookupRecorderFaultHandle(handle, flush, close), row
                return handle, row
            context.open_file = open_file
        return install

    def assert_owned_timeout_reaped(self):
        pid = int((self.folder / 'child.pid').read_text())
        with self.assertRaises(ProcessLookupError):
            os.kill(pid, 0)
        (self.folder / 'child-reaped.json').write_text(json.dumps({'owned_child_pid': pid, 'reaped': True}) + '\n')

    def test_real_empty_streams_keep_actual_filesystem_witnesses(self):
        error, _, row = self.invoke()
        self.assertIsInstance(error, _LookupRecorderBoundaryStop)
        self.assertEqual(b'', self.stdout.read_bytes()); self.assertEqual(b'', self.stderr.read_bytes())
        self.assertEqual(0, row['returncode'])

    def test_real_nonempty_streams_keep_exact_bytes(self):
        error, _, _ = self.invoke('import sys; print("exact stdout"); print("exact stderr", file=sys.stderr)')
        self.assertIsInstance(error, _LookupRecorderBoundaryStop)
        self.assertEqual(b'exact stdout\n', self.stdout.read_bytes()); self.assertEqual(b'exact stderr\n', self.stderr.read_bytes())

    def test_expected_nonzero_exit_is_recorded_without_child_error(self):
        error, _, row = self.invoke('raise SystemExit(7)', expected=7)
        self.assertIsInstance(error, _LookupRecorderBoundaryStop); self.assertEqual(7, row['returncode'])

    def test_unexpected_nonzero_exit_retains_failed_command_row(self):
        error, _, row = self.invoke('raise SystemExit(7)')
        self.assertIs(type(error), RuntimeError); self.assertEqual('Lookup command failed: actual', str(error))
        self.assertEqual(7, row['returncode'])

    def test_timeout_is_actual_and_owned_child_is_reaped(self):
        error, _, row = self.invoke('from pathlib import Path; import os,time; Path("child.pid").write_text(str(os.getpid())); print("before timeout", flush=True); time.sleep(10)', timeout=0.4)
        self.assertIsInstance(error, subprocess.TimeoutExpired); self.assertIsNone(row['returncode'])
        self.assert_owned_timeout_reaped()

    def test_preexisting_stdout_rejects_before_child_and_still_records_failure(self):
        self.stdout.write_bytes(b'owned previous stdout')
        error, _, row = self.invoke('from pathlib import Path; Path("child-ran").write_text("bad")')
        self.assertEqual('Lookup command output already exists', str(error)); self.assertIs(row['stream_context_entered'], False)
        self.assertEqual(b'owned previous stdout', self.stdout.read_bytes())
        self.assertFalse(self.stderr.exists()); self.assertFalse((self.folder / 'child-ran').exists())

    def test_preexisting_stderr_rejects_before_child_and_still_records_failure(self):
        self.stderr.write_bytes(b'owned previous stderr')
        error, _, row = self.invoke('from pathlib import Path; Path("child-ran").write_text("bad")')
        self.assertEqual('Lookup command output already exists', str(error)); self.assertIs(row['stream_context_entered'], False)
        self.assertEqual(b'owned previous stderr', self.stderr.read_bytes())
        self.assertFalse(self.stdout.exists()); self.assertFalse((self.folder / 'child-ran').exists())

    def test_actual_launch_failure_retains_original_exception_and_row(self):
        error, _, row = self.invoke(executable=self.folder / 'intentionally-absent-executable')
        self.assertIsInstance(error, FileNotFoundError); self.assertIsNone(row['returncode'])
        self.assertIs(row['stream_context_entered'], True)

    def test_second_stream_open_failure_closes_first_and_preserves_identity(self):
        injected = OSError('controlled second stream open failure')
        error, _, row = self.invoke(fault=self.io_fault(second_open=injected))
        self.assertIs(error, injected); self.assertIs(row['stream_context_entered'], False)
        self.assertIsNone(row['returncode']); self.assertTrue(self.stdout.exists()); self.assertFalse(self.stderr.exists())
        self.assertIn('finished', row['stream_evidence'])

    def test_existing_filesystem_witness_is_not_overwritten(self):
        witness = self.commands / 'actual.filesystem-before.log'; witness.write_bytes(b'existing witness')
        error, _, row = self.invoke()
        self.assertIsInstance(error, FileExistsError); self.assertIsNone(row['returncode'])
        self.assertEqual(b'existing witness', witness.read_bytes())
        self.assertTrue(row['stream_evidence']['failed_file_operations'])

    def test_actual_stdout_inode_replacement_keeps_the_failed_command_row(self):
        error, _, row = self.invoke('from pathlib import Path; import os,sys; p=Path(sys.argv[1]); q=p.with_name("replacement.txt"); q.write_bytes(b"replacement"); os.replace(q,p)')
        self.assertIs(type(error), RuntimeError); self.assertIn('changed inode or metadata', str(error))
        self.assertEqual(0, row['returncode']); self.assertTrue(row['stream_evidence']['cleanup_errors'])

    def test_actual_additional_hardlink_is_rejected_and_retained(self):
        error, _, row = self.invoke('from pathlib import Path; import os,sys; p=Path(sys.argv[1]); os.link(p,p.with_name("extra-hardlink.txt")); print("two links", flush=True)')
        self.assertIs(type(error), RuntimeError); self.assertIn('ownership changed', str(error))
        self.assertEqual(2, self.stdout.stat().st_nlink); self.assertEqual(0, row['returncode'])
        self.assertTrue(row['stream_evidence']['cleanup_errors'])

    def test_flush_failure_retains_identity_closes_handles_and_finalizes_row(self):
        injected = OSError('controlled flush failure')
        error, _, row = self.invoke(fault=self.io_fault(flush=injected))
        self.assertIs(error, injected); self.assertEqual(0, row['returncode'])
        self.assertTrue(row['stream_evidence']['cleanup_errors'])

    def test_close_failure_retains_identity_closes_handles_and_finalizes_row(self):
        injected = OSError('controlled close failure after actual closure')
        error, _, row = self.invoke(fault=self.io_fault(close=injected))
        self.assertIs(error, injected); self.assertEqual(0, row['returncode'])
        self.assertTrue(row['stream_evidence']['cleanup_errors'])

    def test_both_flush_and_close_failures_keep_first_error_and_other_cleanup(self):
        flush, close = OSError('controlled first flush failure'), OSError('controlled second close failure')
        error, _, row = self.invoke(fault=self.io_fault(flush=flush, close=close))
        self.assertIs(error, flush); self.assertEqual(0, row['returncode'])
        self.assertTrue(any(repr(close) == value for value in row['stream_evidence']['cleanup_errors']))

    def test_timeout_is_not_masked_by_flush_and_close_errors(self):
        flush, close = OSError('controlled timeout cleanup flush'), OSError('controlled timeout cleanup close')
        error, _, row = self.invoke('from pathlib import Path; import os,time; Path("child.pid").write_text(str(os.getpid())); time.sleep(10)',
                                  timeout=0.4, fault=self.io_fault(flush=flush, close=close))
        self.assertIsInstance(error, subprocess.TimeoutExpired); self.assertIsNone(row['returncode'])
        self.assertTrue(any(repr(flush) == value for value in row['stream_evidence']['cleanup_errors']))
        self.assertTrue(any(repr(close) == value for value in row['stream_evidence']['cleanup_errors']))
        self.assert_owned_timeout_reaped()


if __name__ == '__main__': unittest.main()
