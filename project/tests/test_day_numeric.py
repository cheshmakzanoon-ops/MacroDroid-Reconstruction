"""Reject drift in numeric method credit, original getter selection and proof rows.

The selector tests execute the real ExtractOracle Java implementation. The small
coverage fixtures isolate report validation; actual 1,291-case observations and
compiled fault detection are separate acceptance evidence.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import unittest

import build
import day_numeric_dex_controls as numeric
import ui_mutation_catalog as catalog

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def copy_inputs(folder):
    for name in ('source/java-method-map.json', numeric.DEPENDENCY_PATH,
                 catalog.DAY_CATALOG_PATH, catalog.DAY_HELPER_PATH):
        target = folder / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / name).read_bytes())


class DayNumericCatalogTests(unittest.TestCase):
    def test_all_thirteen_real_source_mutations(self):
        source = (ROOT / catalog.DAY_HELPER_PATH).read_bytes()
        jobs = catalog.load_day_mutations(ROOT)
        self.assertEqual(len(jobs), 13)
        self.assertEqual({job['name'].removeprefix('day-numeric-') for job in jobs}, set(numeric.JAVA_FAILURE_COUNTS))
        self.assertTrue(all(job['mutant'].encode() != source and job['day_numeric'] is True
                            and job['widget'] is False and job['required_cases'] for job in jobs))
        self.assertEqual((ROOT / catalog.DAY_HELPER_PATH).read_bytes(), source)

    def test_changed_catalog_bytes_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); copy_inputs(root)
            path = root / catalog.DAY_CATALOG_PATH
            path.write_bytes(path.read_bytes() + b'\n')
            with self.assertRaisesRegex(RuntimeError, 'catalog differs'):
                catalog.load_day_mutations(root)

    def test_changed_positive_helper_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); copy_inputs(root)
            path = root / catalog.DAY_HELPER_PATH
            path.write_bytes(path.read_bytes() + b'\n')
            with self.assertRaisesRegex(RuntimeError, 'positive source'):
                catalog.load_day_mutations(root)

    def test_exact_recovered_and_uncredited_dependency_inventory(self):
        registry = read(ROOT / 'source/java-method-map.json')
        dependencies = numeric.validate_dependencies(ROOT, registry)
        self.assertEqual(len(registry), 1244)
        self.assertEqual(len({row['target'] for row in registry}), 605)
        self.assertEqual(dependencies, set(numeric.GETTERS))
        keys = {row['target'] + '->' + row['method'] for row in registry}
        self.assertEqual(len(keys | dependencies), 1247)
        self.assertFalse(keys & dependencies)
        self.assertEqual(len({key.split('->', 1)[0] for key in keys | dependencies}), 607)

    def test_duplicate_numeric_consumer_is_rejected(self):
        registry = read(ROOT / 'source/java-method-map.json')
        registry.append(copy.deepcopy(next(row for row in registry if row['target'] + '->' + row['method'] == numeric.METHOD)))
        with self.assertRaisesRegex(RuntimeError, 'absent or duplicated'):
            numeric.validate_dependencies(ROOT, registry)

    def test_original_getter_cannot_be_credited_as_recovered(self):
        registry = read(ROOT / 'source/java-method-map.json')
        row = read(ROOT / numeric.DEPENDENCY_PATH)['dependencies'][0]
        registry.append({'target': row['target'], 'method': row['method']})
        with self.assertRaisesRegex(RuntimeError, 'credited'):
            numeric.validate_dependencies(ROOT, registry)

    def test_dependency_declaration_bytes_are_required(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); copy_inputs(root)
            path = root / numeric.DEPENDENCY_PATH
            data = read(path); data['dependencies'] = []
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(RuntimeError, 'dependency bytes'):
                numeric.validate_dependencies(root, read(root / 'source/java-method-map.json'))

    def test_numeric_registry_cannot_bind_another_helper_method(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); copy_inputs(root)
            path = root / 'source/java-method-map.json'; registry = read(path)
            next(row for row in registry if row['target'] + '->' + row['method'] == numeric.METHOD)['helper_method'] = 'other'
            path.write_text(json.dumps(registry))
            with self.assertRaisesRegex(RuntimeError, 'registry binding'):
                numeric.target_entry(root)


def report_identity():
    return {'schema': 1, 'cases': 1291, 'executionPaths': 3, 'primaryMethod': numeric.METHOD,
            'primaryRecoveredMethods': 1, 'originalDependencyMethods': 3, 'androidRuntime': False,
            'dependencyKeys': sorted(numeric.GETTERS), 'inputInventorySha256': catalog.DAY_INPUT_INVENTORY_SHA256}


def coverage_fixture(count=32):
    methods = []
    for key in sorted({numeric.METHOD, *numeric.GETTERS}):
        primary = key == numeric.METHOD
        size = count - 7 if primary else 3 if 'DictionaryEntry;' in key else 2
        offsets = list(range(size)); edges = ['0:1', '0:2', '1:2', '1:3'] if primary else []
        methods.append({'key': key, 'primaryRecovery': primary, 'requiredOffsets': offsets,
                        'executedOffsets': list(offsets), 'missingOffsets': [], 'requiredEdges': edges,
                        'executedEdges': list(edges), 'missingEdges': [], 'instructionCount': size, 'exceptionRegions': 0})
    return {'methods': methods, 'instructionCount': count, 'executedInstructionCount': count,
            'requiredBranchEdges': 4, 'executedBranchEdges': 4, 'allInstructionsAndEdgesExecuted': True}


class DayNumericReportGuardTests(unittest.TestCase):
    def test_exact_numeric_identity_is_accepted(self):
        numeric.validate_report_identity(report_identity())

    def test_wrong_primary_method_is_rejected(self):
        value = report_identity(); value['primaryMethod'] = 'Lanother/Type;->other()I'
        with self.assertRaisesRegex(RuntimeError, 'identity'):
            numeric.validate_report_identity(value)

    def test_boolean_recovered_credit_is_rejected(self):
        value = report_identity(); value['primaryRecoveredMethods'] = True
        with self.assertRaisesRegex(RuntimeError, 'count'):
            numeric.validate_report_identity(value)

    def test_duplicate_uncredited_getter_is_rejected(self):
        value = report_identity(); value['dependencyKeys'].append(value['dependencyKeys'][0])
        with self.assertRaisesRegex(RuntimeError, 'identity'):
            numeric.validate_report_identity(value)

    def test_omitted_uncredited_getter_is_rejected(self):
        value = report_identity(); value['dependencyKeys'].pop()
        with self.assertRaisesRegex(RuntimeError, 'identity'):
            numeric.validate_report_identity(value)

    def test_unexecuted_android_claim_is_rejected(self):
        value = report_identity(); value['androidRuntime'] = True
        with self.assertRaisesRegex(RuntimeError, 'identity'):
            numeric.validate_report_identity(value)

    def test_different_case_inventory_is_rejected(self):
        value = report_identity(); value['inputInventorySha256'] = '0' * 64
        with self.assertRaisesRegex(RuntimeError, 'identity'):
            numeric.validate_report_identity(value)

    def test_boolean_zero_and_float_summary_counts_are_rejected(self):
        for value in (False, 0.0, '0', None):
            with self.subTest(value=value), self.assertRaisesRegex(RuntimeError, 'summary'):
                numeric.require_counts({'failed': value}, {'failed': 0}, 'summary count')

    def test_complete_original_and_rebuilt_coverage_rows_are_accepted(self):
        for count in (32, 25): numeric.validate_positive_coverage(coverage_fixture(count), count)

    def test_deleted_method_rows_cannot_reuse_total_counters(self):
        value = coverage_fixture(); value['methods'] = []
        with self.assertRaisesRegex(RuntimeError, 'inventory'):
            numeric.validate_positive_coverage(value, 32)

    def test_duplicate_method_row_is_rejected(self):
        value = coverage_fixture(); value['methods'][-1] = copy.deepcopy(value['methods'][0])
        with self.assertRaisesRegex(RuntimeError, 'inventory'):
            numeric.validate_positive_coverage(value, 32)

    def test_getter_recovery_credit_is_rejected(self):
        value = coverage_fixture(); value['methods'][1]['primaryRecovery'] = True
        with self.assertRaisesRegex(RuntimeError, 'recovery credit'):
            numeric.validate_positive_coverage(value, 32)

    def test_missing_executed_offset_is_rejected(self):
        value = coverage_fixture(); value['methods'][0]['executedOffsets'].pop()
        with self.assertRaisesRegex(RuntimeError, 'Incomplete'):
            numeric.validate_positive_coverage(value, 32)

    def test_duplicate_required_offset_is_rejected(self):
        value = coverage_fixture(); value['methods'][0]['requiredOffsets'][1] = 0
        with self.assertRaisesRegex(RuntimeError, 'offsets'):
            numeric.validate_positive_coverage(value, 32)

    def test_branch_to_an_unlisted_instruction_is_rejected(self):
        value = coverage_fixture(); value['methods'][0]['requiredEdges'][0] = '0:999'
        value['methods'][0]['requiredEdges'].sort()
        with self.assertRaisesRegex(RuntimeError, 'another instruction'):
            numeric.validate_positive_coverage(value, 32)

    def test_missing_conditional_edge_is_rejected(self):
        value = coverage_fixture(); value['methods'][0]['executedEdges'].pop()
        with self.assertRaisesRegex(RuntimeError, 'Incomplete'):
            numeric.validate_positive_coverage(value, 32)

    def test_inconsistent_summary_is_rejected(self):
        value = coverage_fixture(); value['executedInstructionCount'] = 31
        with self.assertRaisesRegex(RuntimeError, 'summary'):
            numeric.validate_positive_coverage(value, 32)


SELECTOR_PROBE = r'''
import com.google.gson.*;
import java.nio.file.*;
public final class NumericSelectionTestProbe {
  public static void main(String[] args) throws Exception {
    var registry = JsonParser.parseString(Files.readString(Path.of(args[0]))).getAsJsonArray();
    var declaration = JsonParser.parseString(Files.readString(Path.of(args[1]))).getAsJsonObject();
    var selection = ExtractOracle.selection(registry, declaration);
    JsonObject report = new JsonObject();
    report.addProperty("registered", selection.registered().size());
    report.addProperty("dependencies", selection.dependencies().size());
    report.addProperty("selected", selection.registered().size() + selection.dependencies().size());
    report.addProperty("classes", selection.methods().size());
    System.out.println(report);
  }
}
'''


class DayOriginalSelectorExecutionTests(unittest.TestCase):
    @staticmethod
    def execute(argv, timeout):
        started = time.monotonic()
        result = subprocess.run(list(map(str, argv)), capture_output=True, text=True, timeout=timeout)
        # A targeted integration run may retain every child stream and command.
        log = os.environ.get('DAY_NUMERIC_TEST_COMMAND_LOG')
        if log:
            with Path(log).open('a') as stream:
                stream.write(json.dumps({'argv': list(map(str, argv)), 'returncode': result.returncode,
                                         'timeout_seconds': timeout, 'duration_seconds': time.monotonic() - started,
                                         'stdout': result.stdout, 'stderr': result.stderr}) + '\n')
        return result

    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='day-numeric-selector-tests-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.folder = Path(cls.temp.name)
        cls.java, cls.javac = shutil.which('java'), shutil.which('javac')
        if cls.java is None or cls.javac is None or not build.JAR.is_file():
            raise RuntimeError('Actual Day original-selector controls require the configured JDK and build JAR')
        source = cls.folder / 'NumericSelectionTestProbe.java'; source.write_text(SELECTOR_PROBE)
        result = cls.execute([cls.javac, '-cp', build.JAR, '-d', cls.folder,
                              ROOT / 'tools/src/ExtractOracle.java', source], 60)
        if result.returncode != 0: raise RuntimeError('Actual original-selector compile failed: ' + result.stderr)
        cls.classpath = os.pathsep.join(map(str, [build.JAR, cls.folder]))

    def selector(self, registry=None, declaration=None, error=None):
        registry = read(ROOT / 'source/java-method-map.json') if registry is None else registry
        declaration = read(ROOT / numeric.DEPENDENCY_PATH) if declaration is None else declaration
        with tempfile.TemporaryDirectory(dir=self.folder) as temp:
            folder = Path(temp); a = folder / 'registry.json'; b = folder / 'dependencies.json'
            a.write_text(json.dumps(registry)); b.write_text(json.dumps(declaration))
            result = self.execute([self.java, '-Xverify:all', '-cp', self.classpath,
                                   'NumericSelectionTestProbe', a, b], 30)
        if error is None:
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), {'registered': 1244, 'dependencies': 5, 'selected': 1249, 'classes': 607})
        else:
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(error, result.stderr)

    def test_actual_java_selection_keeps_dependencies_separate(self):
        self.selector()

    def test_actual_java_rejects_duplicate_registry(self):
        data = read(ROOT / 'source/java-method-map.json'); data.append(copy.deepcopy(data[0]))
        self.selector(registry=data, error='Duplicate registered original method')

    def test_actual_java_rejects_unregistered_dependency_consumer(self):
        data = read(ROOT / numeric.DEPENDENCY_PATH); data['dependencies'][0]['consumer'] = 'Lmissing;->absent()I'
        self.selector(declaration=data, error='no registered consumer')

    def test_actual_java_rejects_registered_dependency(self):
        data = read(ROOT / numeric.DEPENDENCY_PATH)
        first = read(ROOT / 'source/java-method-map.json')[0]
        data['dependencies'][0].update(target=first['target'], method=first['method'])
        self.selector(declaration=data, error='overlaps recovered registry')

    def test_actual_java_rejects_duplicate_dependency(self):
        data = read(ROOT / numeric.DEPENDENCY_PATH); data['dependencies'].append(copy.deepcopy(data['dependencies'][0]))
        self.selector(declaration=data, error='Duplicate original dependency')

    def test_actual_java_rejects_extra_dependency_field(self):
        data = read(ROOT / numeric.DEPENDENCY_PATH); data['dependencies'][0]['recovered'] = True
        self.selector(declaration=data, error='Invalid original dependency fields')

    def test_actual_java_rejects_boolean_schema(self):
        data = read(ROOT / numeric.DEPENDENCY_PATH); data['schema'] = True
        self.selector(declaration=data, error='Invalid original dependency declaration')

    def test_actual_java_rejects_non_hash_dependency_provenance(self):
        data = read(ROOT / numeric.DEPENDENCY_PATH); data['dependencies'][0]['original_method_sha256'] = 'changed'
        self.selector(declaration=data, error='Invalid original dependency method hash')

    def test_actual_java_rejects_malformed_method_selection(self):
        data = read(ROOT / numeric.DEPENDENCY_PATH); data['dependencies'][0]['method'] = 'no-descriptor'
        self.selector(declaration=data, error='Malformed original method selection')

    def test_wrong_original_apk_rejected_before_fixture_write(self):
        with tempfile.TemporaryDirectory(dir=self.folder) as temp:
            root = Path(temp); copy_inputs(root)
            fixture = root / 'tests/fixtures/original-methods.dex'; fixture.write_bytes(b'prior fixture must remain')
            prior = hashlib.sha256(fixture.read_bytes()).hexdigest()
            apk = root / 'wrong-original.apk'; apk.write_bytes(b'not the pinned original')
            result = self.execute([self.java, '-Xverify:all', '-cp', self.classpath,
                                   'ExtractOracle', root, apk], 30)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Unexpected original APK identity', result.stderr)
            self.assertEqual(hashlib.sha256(fixture.read_bytes()).hexdigest(), prior)
            self.assertFalse(fixture.with_name('original-methods.dex.new').exists())


if __name__ == '__main__': unittest.main()
