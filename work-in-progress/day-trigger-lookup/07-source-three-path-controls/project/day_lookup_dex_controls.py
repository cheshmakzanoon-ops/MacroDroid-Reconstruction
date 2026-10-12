#!/usr/bin/env python3
"""Bind ten lookup Java faults and two actual production-D8 lookup faults.

The acceptance entry requires the complete current UI fault evidence, a positive
instruction match to the signed APK, that APK's two original getters and exact
positive restoration. The one-method compiler is also usable for explicitly
scoped private studies; it alone makes no signed packaging or ART claim.
"""
from __future__ import annotations

from datetime import datetime, timezone
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import zipfile

import build
import day_numeric_dex_controls as numeric
import ui_mutation_catalog as catalog
import ui_runtime_policy

METHOD = catalog.LOOKUP_METHOD
TARGET, SIGNATURE = METHOD.split('->', 1)
HELPER_NAME = 'recovered.ui.DayTriggerLookupMethods'
HELPER_CLASS = 'recovered/ui/DayTriggerLookupMethods.class'
# Preserve existing shared nested-class flags; do not substitute minimal study stubs.
HELPER_CLASS_SHA256 = 'df4383e951f3e897f58adc33f27847198f52cd455ccc5a9b22eb70712f66e082'
DEPENDENCY_PATH = numeric.DEPENDENCY_PATH
DEPENDENCY_SHA256 = '159061ce552e3364c113f28e72e5a4c1bc091a21153d0d5e0a793d2f773b0229'
ORIGINAL_METHOD_SHA256 = 'afdaa9b0977db46a2f333cccb0de57a401b77e2e3b66b535b2bff50991e4614e'
GETTERS = {
    'Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;->getEntries()Ljava/util/List;': 'f3959381d2067a3611069ac45c01a34078ef9e718f9c4906f74bb545da48be0e',
    'Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getKey()Ljava/lang/String;': '41c4ec0e7f0ec7f3b6638765a92670cdbae7c839b794b8f3de9ba1c2b431b1a3',
}
JAVA_FAILURE_COUNTS = {
    'case-sensitive': 127, 'reverse-receiver': 3, 'skip-null-entry': 2, 'null-query-early-return': 3,
    'last-match': 233, 'trim-query': 1, 'indexed-loop': 369, 'extra-iteration-after-match': 233,
    'swallow-iterator-fault': 25, 'replace-injected-npe-identity': 6,
}



def require(value, message):
    if not value:
        raise RuntimeError(message)



def sha(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()



def identity(path: Path) -> dict:
    return {'bytes': path.stat().st_size, 'sha256': sha(path)}



def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + '\n')



def require_counts(report: dict, expected: dict[str, int], message: str) -> None:
    require(all(type(report.get(key)) is int and report[key] == count for key, count in expected.items()), message)



def validate_dependencies(root: Path, registry: list[dict]) -> set[str]:
    require(numeric.DEPENDENCY_PATH == DEPENDENCY_PATH and numeric.DEPENDENCY_SHA256 == DEPENDENCY_SHA256,
            'Numeric and lookup dependency declarations disagree')
    selected = numeric.validate_dependency_declaration(root, registry)
    require(selected[METHOD] == set(GETTERS) and selected[numeric.METHOD] == set(numeric.GETTERS),
            'Combined numeric/lookup dependency partitions differ')
    return selected[METHOD]



def target_entry(root: Path) -> dict:
    registry = json.loads((root / 'source/java-method-map.json').read_text())
    validate_dependencies(root, registry)
    rows = [row for row in registry if row['target'] + '->' + row['method'] == METHOD]
    require(len(rows) == 1, 'Lookup target must be registered exactly once')
    entry = rows[0]
    require(entry['java_source'] == catalog.LOOKUP_HELPER_PATH and entry['helper'] == 'Lrecovered/ui/DayTriggerLookupMethods;'
            and entry['helper_method'] == 'findEntry' and entry['instance'] is False
            and entry['proof_family'] == 'v9-ui' and entry['original_method_sha256'] == ORIGINAL_METHOD_SHA256,
            'Lookup registry binding changed')
    require(sha(root / catalog.LOOKUP_HELPER_PATH) == catalog.LOOKUP_HELPER_SHA256, 'Lookup positive source changed')
    return entry



def compile_target(production, source_root: Path, index: dict, entry: dict, helper_class: Path,
                   folder: Path, run, java: str | Path, jar: Path) -> tuple[Path, dict]:
    """Apply the production relocation and sole-method transplant to one real class."""
    folder.mkdir(parents=True, exist_ok=False)
    matches = [row for row in index.values() if row['descriptor'] == TARGET]
    require(len(matches) == 1, 'Original lookup class is not unique')
    original = source_root / matches[0]['path']
    require(sha(original) == matches[0]['sha256'], 'Original lookup class differs from its source index')
    old_text = original.read_text(); old_methods = production.methods(old_text); old = old_methods[SIGNATURE]
    require(hashlib.sha256(old.encode()).hexdigest() == ORIGINAL_METHOD_SHA256, 'Original lookup method body changed')
    relocated = folder / 'relocated' / HELPER_CLASS; relocated.parent.mkdir(parents=True)
    relocated.write_bytes(production.relocate_class(helper_class.read_bytes()))
    compiler_input = folder / 'inputs.jar'
    with zipfile.ZipFile(compiler_input, 'x') as archive:
        member = zipfile.ZipInfo(HELPER_CLASS, (1980, 1, 1, 0, 0, 0)); member.external_attr = 0o100644 << 16
        archive.writestr(member, relocated.read_bytes())
    with zipfile.ZipFile(compiler_input) as archive:
        require(archive.namelist() == [HELPER_CLASS] and archive.read(HELPER_CLASS) == relocated.read_bytes(), 'Unexpected D8 compiler input')
    dex_dir = folder / 'd8'; dex_dir.mkdir()
    run(folder, 'd8-helper', [java, '-Xmx512m', '-cp', jar, 'com.android.tools.r8.D8',
                            '--release', '--no-desugaring', '--min-api', '23', '--output', dex_dir, compiler_input])
    require(sorted(p.name for p in dex_dir.iterdir()) == ['classes.dex'], 'Unexpected lookup D8 output inventory')
    helper_dex_sha = production.dex_integrity(dex_dir / 'classes.dex')
    smali = folder / 'helper-smali'
    run(folder, 'disassemble-helper', [java, '-Xmx512m', '-cp', jar, 'com.android.tools.smali.baksmali.Main',
                                      'd', '--api', '23', '--use-locals', '-o', smali, dex_dir / 'classes.dex'])
    require(sorted(p.relative_to(smali).as_posix() for p in smali.rglob('*.smali')) == ['recovered/ui/DayTriggerLookupMethods.smali'], 'Unexpected helper disassembly class')
    emitted = production.methods((smali / 'recovered/ui/DayTriggerLookupMethods.smali').read_text())
    compiled = emitted['findEntry' + SIGNATURE[SIGNATURE.index('('):]]
    restored, corrections = production.restore_from_preserved_source(entry, compiled, old, index, source_root)
    require(restored == compiled and corrections == [], 'Lookup method unexpectedly needs constructor-owner correction')
    body = production.ANNOT.sub('', compiled.split('\n', 1)[1].rsplit('.end method', 1)[0])
    require('Lrecovered/' not in body and 'Ldefpackage/' not in body, 'Host/helper type escaped lookup transplant')
    replacement = old.splitlines()[0] + '\n' + ''.join(production.ANNOT.findall(old)) + body + '.end method'
    require(old_text.count(old) == 1, 'Lookup replacement anchor is not unique')
    new_text = old_text.replace(old, replacement, 1); new_methods = production.methods(new_text)
    require(set(new_methods) == set(old_methods) and all(new_methods[k] == v for k, v in old_methods.items() if k != SIGNATURE), 'Other original methods changed')
    require(new_text.replace(replacement, '<LOOKUP>', 1) == old_text.replace(old, '<LOOKUP>', 1), 'Non-target class text changed')
    target = folder / 'target-smali/DayTrigger.smali'; target.parent.mkdir(); target.write_text(new_text)
    dex = folder / 'lookup-target.dex'
    run(folder, 'assemble-target', [java, '-Xmx512m', '-cp', jar, 'com.android.tools.smali.smali.Main',
                                  'a', '--api', '23', '-j', '2', '-o', dex, target.parent])
    digest = production.dex_integrity(dex)
    binding = {'method': METHOD, 'original_class': identity(original), 'original_method_sha256': ORIGINAL_METHOD_SHA256,
               'helper_class': identity(helper_class), 'relocated_class': identity(relocated), 'compiler_input': identity(compiler_input),
               'compiler_input_classes': [HELPER_CLASS], 'host_stubs_sent_to_d8': 0, 'helper_dex_sha256': helper_dex_sha,
               'compiled_method_sha256': hashlib.sha256(compiled.encode()).hexdigest(),
               'transplanted_method_sha256': hashlib.sha256(replacement.encode()).hexdigest(),
               'transplanted_class': identity(target), 'target_dex_sha256': digest,
               'other_original_methods_unchanged': len(old_methods) - 1, 'non_target_class_text_unchanged': True,
               'preservation_scope': 'One-method micro-DEX only; signed class also contains the pre-existing constant mapping and recovered r0. Signed p0 instructions are independently bound.',
               'constructor_owner_corrections': []}
    write_json(folder / 'method-body-binding.json', binding)
    return dex, binding



def class_pins(host: Path, tools: Path, helper_override: Path | None = None) -> dict:
    """Pin every declared class of the harness, active oracle and scoped host types."""
    pins = {}
    specs = [(tools, 'DayLookupControlHarness'), (tools, 'DayLookupParityCases'), (tools, 'BytecodeOracle'),
             (host, 'com/arlosoft/macrodroid/variables/VariableValue'), (host, 'defpackage/EngineRuntime'),
             (host, 'defpackage/TestClock'), (helper_override or host, 'recovered/ui/DayTriggerLookupMethods')]
    for root, prefix in specs:
        stem = root / prefix
        paths = sorted(p for p in stem.parent.glob(stem.name + '*.class') if p.name == stem.name + '.class' or p.name.startswith(stem.name + '$'))
        require(any(p.name == stem.name + '.class' for p in paths), 'Missing lookup harness class: ' + prefix)
        for path in paths:
            name = path.relative_to(root).as_posix()[:-6].replace('/', '.')
            require(name not in pins, 'Duplicate class pin')
            pins[name] = {'path': str(path.resolve()), 'sha256': sha(path)}
    return pins



INPUT_FIELDS = ('case', 'keysUtf16Hex', 'queryUtf16Hex', 'mode', 'nullEntryIndex', 'injectedFaultAt',
                'injectedFaultType', 'expectedReturnIndex', 'expectedExceptionClass', 'expectedEvents',
                'exceptionComparisonScope')
VM_NULL_CASES = frozenset({'dictionary-null', 'entries-null', 'iterator-null', 'null-first-entry',
                         'null-query-and-null-key', 'null-query-nonempty', 'null-second-entry'})


def same_inputs(a: dict, b: dict) -> bool:
    return {key: a[key] for key in INPUT_FIELDS} == {key: b[key] for key in INPUT_FIELDS}


def validate_report_identity(report: dict) -> None:
    require_counts(report, {'schema': 1, 'cases': 371, 'executionPaths': 3,
                           'primaryRecoveredMethods': 1, 'originalDependencyMethods': 2},
                   'Lookup report count or schema differs')
    require(report.get('primaryMethod') == METHOD and report.get('androidRuntime') is False
            and report.get('dependencyKeys') == sorted(GETTERS)
            and report.get('generatedNullMessageCases') == sorted(VM_NULL_CASES)
            and report.get('inputInventorySha256') == catalog.LOOKUP_INPUT_INVENTORY_SHA256,
            'Lookup report method, dependency or exception scope identity differs')


def validate_execution_binding(report: dict, config: dict) -> None:
    """Require the returned proof to name exactly the inputs used by this command."""
    require(report.get('inputIdentities') == config, 'Lookup report identifies another command configuration')
    pins = config.get('classPins')
    require(isinstance(pins, dict) and pins and all(isinstance(row, dict)
            and set(row) == {'path', 'sha256'} for row in pins.values()), 'Malformed lookup execution class pins')
    expected = {name: {'path': str(Path(row['path']).resolve()), 'sha256': row['sha256']} for name, row in pins.items()}
    require(report.get('loadedClassOrigins') == expected, 'Lookup reported loaded class origins differ from the actual command pins')


def validate_positive_coverage(coverage: dict, count: int) -> None:
    require(type(count) is int and count in {26, 23}, 'Unknown lookup coverage count')
    methods = coverage.get('methods')
    require(isinstance(methods, list) and len(methods) == 3
            and all(isinstance(row, dict) for row in methods)
            and [row.get('key') for row in methods] == sorted({METHOD, *GETTERS}),
            'Lookup coverage method/dependency inventory differs')
    instructions = edges = 0
    for row in methods:
        primary = row['key'] == METHOD
        require(row.get('primaryRecovery') is primary, 'Lookup getter was given recovery credit')
        offsets, branches = row.get('requiredOffsets'), row.get('requiredEdges')
        require(isinstance(offsets, list) and offsets
                and all(type(offset) is int and offset >= 0 for offset in offsets)
                and offsets == sorted(set(offsets)), 'Malformed lookup instruction offsets')
        require(isinstance(branches, list) and all(isinstance(edge, str) for edge in branches)
                and branches == sorted(set(branches)), 'Malformed lookup conditional edges')
        for edge in branches:
            parts = edge.split(':')
            require(len(parts) == 2 and all(part.isdecimal() for part in parts)
                    and all(int(part) in offsets for part in parts), 'Lookup branch edge names another instruction')
        wanted = count - 5 if primary else 3 if 'DictionaryEntry;' in row['key'] else 2
        require_counts(row, {'instructionCount': wanted, 'exceptionRegions': 0}, 'Lookup method coverage count differs')
        require(len(offsets) == wanted and len(branches) == (4 if primary else 0)
                and row.get('executedOffsets') == offsets and row.get('executedEdges') == branches
                and row.get('missingOffsets') == [] and row.get('missingEdges') == [],
                'Incomplete lookup method instruction/edge coverage')
        instructions += len(offsets); edges += len(branches)
    require(instructions == count and edges == 4, 'Lookup coverage totals differ from method rows')
    require_counts(coverage, {'instructionCount': instructions, 'executedInstructionCount': instructions,
                              'requiredBranchEdges': edges, 'executedBranchEdges': edges},
                   'Lookup coverage summary differs from method rows')
    require(coverage.get('allInstructionsAndEdgesExecuted') is True, 'Incomplete lookup coverage flag')


def validate_raw_observation(observed: dict) -> None:
    require(isinstance(observed, dict)
            and set(observed) == {'returnIndex', 'exceptionClass', 'rawMessage', 'injectedExceptionIdentity', 'events', 'unsupported'}
            and (observed['returnIndex'] is None or type(observed['returnIndex']) is int)
            and (observed['exceptionClass'] is None or isinstance(observed['exceptionClass'], str))
            and (observed['rawMessage'] is None or isinstance(observed['rawMessage'], str))
            and type(observed['injectedExceptionIdentity']) is bool and type(observed['unsupported']) is bool
            and isinstance(observed['events'], list) and all(isinstance(event, str) for event in observed['events']),
            'Malformed raw lookup outcome')


def is_vm_null_case(row: dict) -> bool:
    return row['case'] in VM_NULL_CASES and row['injectedFaultAt'] is None and row['expectedExceptionClass'] == 'java.lang.NullPointerException'


def matches_expected(row: dict, observed: dict) -> bool:
    if observed['unsupported'] or observed['events'] != row['expectedEvents']:
        return False
    exception = row['expectedExceptionClass']
    if exception is None:
        return (observed['exceptionClass'] is None and observed['returnIndex'] == row['expectedReturnIndex']
                and not observed['injectedExceptionIdentity'] and observed['rawMessage'] is None)
    if observed['returnIndex'] is not None or observed['exceptionClass'] != exception:
        return False
    if row['injectedFaultAt'] is not None:
        return observed['injectedExceptionIdentity'] and observed['rawMessage'] == 'EXACT_INJECTED_LOOKUP_FAULT:' + row['case']
    return is_vm_null_case(row) and not observed['injectedExceptionIdentity']


def validate_observer_controls(report: dict, inputs: list[dict]) -> None:
    """These five altered records earn no application execution or coverage credit."""
    selected = [row for row in inputs if row['case'] == 'injected-iterator-npe']
    require(len(selected) == 1, 'Lookup observer control input is absent or duplicated')
    control = report.get('observerRecordControls')
    require(isinstance(control, dict) and set(control) == {'case', 'positiveAccepted', 'changedRecordsRejected',
            'applicationExecutions', 'applicationCoverageCredit', 'positive', 'rejectedRecords'}
            and control.get('case') == selected[0]['case'] and control.get('positiveAccepted') is True,
            'Lookup observer control identity differs')
    require_counts(control, {'changedRecordsRejected': 5, 'applicationExecutions': 0, 'applicationCoverageCredit': 0},
                   'Lookup observer controls received application credit or wrong count')
    positive = control['positive']; validate_raw_observation(positive)
    require(matches_expected(selected[0], positive), 'Lookup observer positive rejected')
    faults = control.get('rejectedRecords')
    require(isinstance(faults, list) and len(faults) == 5, 'Lookup observer fault inventory differs')
    expected = []
    for key, value in [('rawMessage', 'CHANGED_INJECTED_MESSAGE'), ('injectedExceptionIdentity', False),
                       ('events', []), ('returnIndex', 0), ('unsupported', True)]:
        altered = copy.deepcopy(positive); altered[key] = value; expected.append(altered)
    require(faults == expected, 'Lookup observer fault records differ from their exact controls')
    for fault in faults:
        validate_raw_observation(fault)
        require(not matches_expected(selected[0], fault) and fault != positive, 'Lookup observer accepted a changed injected fault')


def validate_observations(report: dict) -> list[str]:
    """Bind all UTF-16 inputs/expectations, then recompute outcomes from raw records."""
    rows = report.get('observations')
    require(isinstance(rows, list) and len(rows) == 371
            and all(isinstance(row, dict) and set(row) == set(INPUT_FIELDS) | {'original', 'java', 'rebuilt',
                'sameScopedOutcome', 'allPathsMatchIndependentExpected'} for row in rows),
            'Missing or malformed lookup observation inventory')
    inputs = [{key: row[key] for key in INPUT_FIELDS} for row in rows]
    digest = hashlib.sha256(json.dumps(inputs, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
    require(digest == catalog.LOOKUP_INPUT_INVENTORY_SHA256, 'Lookup input identities or pinned independent expectations changed')
    require({row['case'] for row in rows if row['injectedFaultAt'] is None
             and row['expectedExceptionClass'] == 'java.lang.NullPointerException'} == VM_NULL_CASES,
            'Lookup generated-null exception scope changed')
    validate_observer_controls(report, inputs)
    failures, unsupported, wrong_expected = [], 0, 0
    for row in rows:
        observations = [row[path] for path in ('original', 'java', 'rebuilt')]
        for observed in observations: validate_raw_observation(observed)
        correct = [matches_expected(row, observed) for observed in observations]
        same = all(correct) if is_vm_null_case(row) else observations[0] == observations[1] == observations[2]
        right = all(correct)
        require(row.get('sameScopedOutcome') is same and row.get('allPathsMatchIndependentExpected') is right,
                'Lookup outcome flags disagree with raw observations')
        if not same or not right: failures.append('day-lookup:' + row['case'])
        unsupported += sum(observed['unsupported'] for observed in observations)
        wrong_expected += not right
    require(report.get('mismatches') == failures, 'Lookup summary labels differ from all recorded cases')
    require_counts(report, {'mismatchCount': len(failures), 'unsupportedCount': unsupported,
                           'independentExpectedChecks': 371, 'independentExpectedFailures': wrong_expected},
                   'Lookup summary differs from all recorded cases')
    return failures


def validate_positive(report: dict) -> None:
    validate_report_identity(report)
    require(validate_observations(report) == [], 'Positive lookup raw outcomes contain a failure')
    require(report.get('passed') is True, 'Incomplete positive lookup three-path report')
    for key, count in [('originalCoverage', 26), ('rebuiltCoverage', 23)]:
        validate_positive_coverage(report.get(key, {}), count)


def validate_fault(positive: dict, fault: dict, required: list[str], expected_count: int, changed_path: str) -> None:
    validate_report_identity(fault)
    require(type(expected_count) is int and expected_count > 0 and len(validate_observations(fault)) == expected_count,
            'Lookup fault raw outcome count differs')
    require(changed_path in {'java', 'rebuilt'}, 'Invalid lookup changed path')
    require(fault.get('passed') is False and fault.get('unsupportedCount') == 0
            and set(required).issubset(fault.get('mismatches', [])), 'Lookup fault lacks its required measured failures')
    old, changed = positive['observations'], fault.get('observations', [])
    require(len(old) == len(changed) == 371, 'Lookup fault changed case count')
    stable_paths = {'original', 'java', 'rebuilt'} - {changed_path}
    for a, b in zip(old, changed):
        require(same_inputs(a, b) and all(a[path] == b[path] for path in stable_paths), 'Lookup fault changed an independent input/path')
    require(fault.get('originalCoverage') == positive['originalCoverage'], 'Lookup fault changed original instruction coverage')
    require(fault.get('observerRecordControls') == positive['observerRecordControls'], 'Lookup fault changed observer controls')



def validate_java_controls(root: Path, records: list[dict]) -> tuple[dict[str, Path], list[dict]]:
    jobs = catalog.load_lookup_mutations(root)
    wanted = {job['name']: job for job in jobs}
    selected = [row for row in records if row.get('mutation', '').startswith('day-lookup-')]
    require(len(selected) == 10 and {row.get('mutation') for row in selected} == set(wanted), 'All ten actual UI Java faults are required')
    classes, bindings = {}, []
    for row in selected:
        name = row['mutation']; job = wanted[name]; short = name.removeprefix('day-lookup-')
        source = root / row['retainedSource']; compiled = root / row['retainedClass']
        expected_root = (root / 'reports/ui-mutants' / name).resolve()
        require(source.resolve() == expected_root / 'DayTriggerLookupMethods.java'
                and compiled.resolve() == expected_root / 'DayTriggerLookupMethods.class', 'Java control reused another artifact path')
        require(row.get('pass') is True and row.get('exitCode') == 2
                and row.get('failedCases') == JAVA_FAILURE_COUNTS[short] and row.get('unsupportedExecutions') == 0
                and row.get('requiredCases') == job['required_cases'] and row.get('requiredCaseRejected') is True
                and row.get('sourceFixtureAndApkUnchanged') is True and row.get('originalCoverageAndInventoryUnchanged') is True
                and row.get('positiveClassSha256') == HELPER_CLASS_SHA256, 'Current UI Java fault proof is incomplete')
        require(source.read_text() == job['mutant'] and sha(source) == row['mutantSourceSha256']
                and sha(compiled) == row['mutantClassSha256'] != HELPER_CLASS_SHA256, 'Java fault source/class differs from actual UI control')
        classes[short] = compiled
        bindings.append({'name': name, 'source': row['retainedSource'], 'source_identity': identity(source),
                         'class': row['retainedClass'], 'class_identity': identity(compiled),
                         'failed_cases': row['failedCases'], 'required_cases': job['required_cases']})
    return classes, bindings



def run_controls(root: Path, java_control_records: list[dict]) -> dict:
    """Acceptance entry: all positive/fault/packaging/provenance/restoration gates required."""
    root = root.resolve(); reports = root / 'reports'; reports.mkdir(exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix='day-lookup-dex-', dir=reports))
    destination = reports / 'day-lookup-dex-controls.json'
    report = {'schema': 1, 'passed': False, 'status': 'RUNNING', 'androidRuntime': False,
              'started_utc': datetime.now(timezone.utc).isoformat(), 'commands': [],
              'evidence_directory': output.relative_to(root).as_posix(), 'primary_recovered_methods': 1,
              'original_dependency_methods': 2, 'expected_java_faults': 10, 'expected_actual_dex_faults': 2}
    write_json(destination, report)

    def run(folder, name, argv, expected=0, timeout=120):
        folder.mkdir(parents=True, exist_ok=True)
        stdout, stderr = folder / (name + '.stdout.log'), folder / (name + '.stderr.log')
        require(not stdout.exists() and not stderr.exists(), 'Lookup command output already exists')
        started = datetime.now(timezone.utc).isoformat(); tick = time.monotonic_ns(); code = None
        witnesses = {}
        try:
            with stdout.open('xb') as out, stderr.open('xb') as err:
                for role, stream in [('stdout', out), ('stderr', err)]:
                    stat = os.fstat(stream.fileno())
                    witnesses[role] = {'device': stat.st_dev, 'inode': stat.st_ino}
                code = subprocess.run(list(map(str, argv)), cwd=root, stdout=out, stderr=err, timeout=timeout).returncode
        finally:
            finished_tick = time.monotonic_ns()
            outputs = {}
            for role, path in [('stdout', stdout), ('stderr', stderr)]:
                stat = path.stat()
                require(witnesses.get(role) == {'device': stat.st_dev, 'inode': stat.st_ino},
                        'Lookup command output path no longer names its exclusively created stream')
                outputs[role] = {'path': path.relative_to(root).as_posix(), **identity(path),
                                 'exclusive_stream_witness': witnesses[role]}
            row = {'name': name, 'argv': list(map(str, argv)), 'started_utc': started,
                   'ended_utc': datetime.now(timezone.utc).isoformat(),
                   'started_monotonic_ns': tick, 'finished_monotonic_ns': finished_tick,
                   'duration_nanoseconds': finished_tick - tick, 'timeout_seconds': timeout,
                   'returncode': code, **outputs}
            report['commands'].append(row); write_json(destination, report)
        require(code == expected, 'Lookup command failed: ' + name)
        return row

    try:
        entry = target_entry(root)
        numeric_entry = numeric.target_entry(root)
        registry = json.loads((root / 'source/java-method-map.json').read_text())
        class_mappings = [row for row in registry if row['target'] == TARGET]
        require({row['method'] for row in class_mappings} == {SIGNATURE, numeric_entry['method'], 'requiresScheduleExactAlarm()Z'},
                'DayTrigger class registry differs from the existing constant and two ordinary-method mappings')
        report['signed_class_registered_methods'] = sorted(row['method'] for row in class_mappings)
        host, tools, jar = root / 'build/java/hostclasses', root / 'tools/classes', root / 'tools/lib/jadx-r2721.4574686-all.jar'
        apk = root / 'dist/MacroDroid-5.67.8-v9-hybrid.apk'; fixture = root / 'tests/fixtures/original-methods.dex'
        getter = root / 'build/hybrid/classes3.dex'
        require(sha(host / HELPER_CLASS) == HELPER_CLASS_SHA256, 'Current positive lookup class differs from measured compilation')
        classes, java_bindings = validate_java_controls(root, java_control_records)
        report['java_fault_bindings'] = java_bindings
        policy = ui_runtime_policy.verify(reports); java = policy['java_executable']
        index = json.loads((root / 'source/class-index.json').read_text())
        selected_original = [root / row['path'] for row in index.values() if row['descriptor'] in {TARGET, *(k.split('->', 1)[0] for k in GETTERS)}]
        pinned = [apk, fixture, getter, jar, root / 'build.py', root / 'constructor_owner.py',
                  root / 'tests/java/BytecodeOracle.java', root / catalog.LOOKUP_HELPER_PATH, root / DEPENDENCY_PATH,
                  root / catalog.LOOKUP_CATALOG_PATH, root / 'source/java-method-map.json',
                  root / 'test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java',
                  root / catalog.DAY_HELPER_PATH, host / numeric.HELPER_CLASS, *selected_original,
                  *[Path(row['class']) if Path(row['class']).is_absolute() else root / row['class'] for row in java_bindings]]
        pins = {str(p): identity(p) for p in pinned}
        write_json(output / 'input-identities.json', pins)
        require(sha(root / 'tests/java/BytecodeOracle.java') == 'd91ddcd8ec3d67d41d69b8252835e747c2cad2c6d5ea898323794ceec30e6b56', 'Active lookup oracle changed')
        positive_dex, positive_binding = compile_target(build, root, index, entry, host / HELPER_CLASS, output / 'positive-pipeline', run, java, jar)
        require(sha(host / numeric.HELPER_CLASS) == numeric.HELPER_CLASS_SHA256, 'Positive numeric class changed')
        cp = os.pathsep.join(map(str, [jar, host, tools]))
        run(output, 'numeric-before-instructions', [java, '-Xmx512m', '-cp', cp, 'InspectMethod', getter, numeric.METHOD, output / 'numeric-before-instructions.json'])
        for name, dex in [('signed-apk', getter), ('positive-transplant', positive_dex)]:
            run(output, name + '-instructions', [java, '-Xmx512m', '-cp', cp, 'InspectMethod', dex, METHOD, output / (name + '-instructions.json')])
        packaged = (output / 'signed-apk-instructions.json').read_bytes() == (output / 'positive-transplant-instructions.json').read_bytes()
        require(packaged, 'Positive lookup transplant does not match the signed APK instructions')
        cfg = {'schema': 1, 'originalFixture': {'path': str(fixture), 'sha256': sha(fixture)},
               'rebuiltApk': {'path': str(apk), 'sha256': sha(apk)},
               'rebuiltGetterDex': {'path': str(getter), 'sha256': sha(getter), 'apk_member': 'classes3.dex'},
               'targetDex': {'path': str(positive_dex), 'sha256': sha(positive_dex)}, 'classPins': class_pins(host, tools)}

        def execute(name, config, expected=0):
            folder = output / name; folder.mkdir()
            path = folder / 'config.json'; target = folder / 'result.json'; write_json(path, config)
            run(folder, 'execute', [java, *ui_runtime_policy.JVM_FLAGS, '-Xmx512m', '-cp', cp,
                                    'DayLookupControlHarness', path, target], expected)
            if not target.exists():
                return None
            observed = json.loads(target.read_text())
            validate_execution_binding(observed, config)
            return observed

        positive = execute('positive', cfg); validate_positive(positive)
        report['positive_signed_apk_instruction_match'] = True
        report['positive_pipeline'] = positive_binding
        faults = []
        jobs = {job['name'].removeprefix('day-lookup-'): job for job in catalog.load_lookup_mutations(root)}
        for name in ('case-sensitive', 'last-match'):
            dex, binding = compile_target(build, root, index, entry, classes[name], output / (name + '-pipeline'), run, java, jar)
            altered = copy.deepcopy(cfg); altered['targetDex'] = {'path': str(dex), 'sha256': sha(dex)}
            bad = execute(name + '-dex-fault', altered, 3)
            validate_fault(positive, bad, jobs[name]['required_cases'], JAVA_FAILURE_COUNTS[name], 'rebuilt')
            faults.append({'name': name, 'passed': True, 'mismatches': bad['mismatchCount'],
                           'required_cases': jobs[name]['required_cases'], 'pipeline': binding})
        original_substitution = copy.deepcopy(cfg); original_substitution['targetDex'] = copy.deepcopy(cfg['originalFixture'])
        require(execute('original-as-rebuilt-rejected', original_substitution, 1) is None, 'Provenance fault emitted an accepted report')
        require('Original fixture cannot masquerade as rebuilt target' in (output / 'original-as-rebuilt-rejected/execute.stderr.log').read_text(), 'Original substitution failed for another reason')
        wrong_class = copy.deepcopy(cfg); wrong_class['classPins'][HELPER_NAME]['sha256'] = '0' * 64
        require(execute('wrong-helper-class-rejected', wrong_class, 1) is None, 'Wrong helper identity emitted an accepted report')
        require('Wrong input identity: class ' + HELPER_NAME in (output / 'wrong-helper-class-rejected/execute.stderr.log').read_text(), 'Wrong helper identity failed for another reason')
        restored = execute('positive-restoration', cfg); validate_positive(restored)
        require(restored == positive and (output / 'positive/result.json').read_bytes() == (output / 'positive-restoration/result.json').read_bytes(), 'Lookup positive restoration differs')
        require(all(identity(Path(p)) == value for p, value in pins.items()), 'Lookup source, class, fixture, APK or original inputs changed')
        validate_java_controls(root, java_control_records)
        run(output, 'numeric-after-instructions', [java, '-Xmx512m', '-cp', cp, 'InspectMethod', getter, numeric.METHOD, output / 'numeric-after-instructions.json'])
        require((output / 'numeric-before-instructions.json').read_bytes() == (output / 'numeric-after-instructions.json').read_bytes(),
                'Signed positive numeric method changed during lookup controls')
        report['signed_numeric_method_unchanged'] = True
        report['micro_dex_preservation_scope'] = 'Only p0 changed in each micro-DEX. Other original methods stay original there; signed class has its complete three registered mappings.'
        report.update(passed=True, status='TWO_ACTUAL_LOOKUP_DEX_FAULTS_DETECTED_SIGNED_POSITIVE_RESTORED',
                      actual_dex_faults=faults, provenance_controls_rejected=2,
                      positive_restoration_byte_exact=True, source_class_fixture_and_apk_unchanged=True,
                      cases=371, execution_paths=3, input_inventory_sha256=catalog.LOOKUP_INPUT_INVENTORY_SHA256,
                      original_instruction_count=26, rebuilt_instruction_count=23, conditional_edges_per_path=4,
                      signed_apk_sha256=sha(apk), original_fixture_sha256=sha(fixture))
    except BaseException as error:
        report.update(status='LOOKUP_DEX_CONTROL_FAILED', error=repr(error))
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat(); write_json(destination, report)
    return report

