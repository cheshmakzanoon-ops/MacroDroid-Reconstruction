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


if __name__ == '__main__': unittest.main()
