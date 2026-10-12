#!/usr/bin/env python3
"""Bind the thirteen UI Java faults and separately measure two actual numeric DEX faults.

The acceptance entry point requires a signed-APK instruction match for the positive
target, the three getter bodies from that APK, current Java-control artifacts, and
exact positive restoration. The lower-level one-class compiler is also useful for
explicitly scoped private studies; it alone makes no packaging or acceptance claim.
"""
from __future__ import annotations

from datetime import datetime, timezone
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import time
import zipfile

import build
import ui_mutation_catalog as catalog
import ui_runtime_policy

METHOD = catalog.DAY_METHOD
TARGET, SIGNATURE = METHOD.split('->', 1)
HELPER_NAME = 'recovered.ui.DayTriggerValueMethods'
HELPER_CLASS = 'recovered/ui/DayTriggerValueMethods.class'
# The active host's three referenced nested types are non-final. Only their
# InnerClasses metadata differs from the standalone study; method bytes are exact.
HELPER_CLASS_SHA256 = '2f8b2d3769749301442dae35aca9fda5314eb1f17d59ea6310bd50be62596211'
DEPENDENCY_PATH = 'tests/fixtures/original-dependencies.json'
DEPENDENCY_SHA256 = 'e30552cc8ba0520bbee3a993298cb0bcaa973a9d4633649e80362d35b3eda631'
ORIGINAL_METHOD_SHA256 = '8383c90ebe3d35afa63d52cf92cd4c92b54ed4525ca0d8a31a29fe603f9eef21'
GETTERS = {
    'Lcom/arlosoft/macrodroid/variables/VariableValue$DecimalValue;->getDecimalValue()D': '89c5a3751f7de7f7bdfaddba05f28651eb8b0b78413e4263e05c9dc795acf7ae',
    'Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;->getVariable()Lcom/arlosoft/macrodroid/variables/VariableValue;': 'b3674d51703eb3811fc4918e739777c37de3c580bee961343b80c21e014ca5c0',
    'Lcom/arlosoft/macrodroid/variables/VariableValue$IntegerValue;->getIntValue()J': '1760568e68babc8e32459eed0352a8a20cfdbe35e02b87f2fc6dacc914399993',
}
JAVA_FAILURE_COUNTS = {
    'integer-zero': 509, 'decimal-zero': 406, 'integer-saturation': 468,
    'integer-via-double': 468, 'integer-via-byte': 449, 'decimal-round': 351,
    'decimal-floor': 210, 'decimal-nan-one': 8, 'decimal-infinity-zero': 2,
    'other-minus-one': 9, 'parse-string': 4, 'null-contained-throws': 1, 'null-entry-zero': 1,
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


def command_clock():
    """Record exact clocks; the ISO text is a display of this same Unix value."""
    unix_ns = time.time_ns()
    monotonic_ns = time.monotonic_ns()
    seconds, nanos = divmod(unix_ns, 1_000_000_000)
    utc = datetime.fromtimestamp(seconds, timezone.utc).replace(microsecond=nanos // 1000)
    return {'unix_ns': unix_ns, 'monotonic_ns': monotonic_ns,
            'utc': utc.isoformat(timespec='microseconds')}


def command_file_stat(value):
    return {'device': value.st_dev, 'inode': value.st_ino, 'mode': value.st_mode,
            'links': value.st_nlink, 'bytes': value.st_size,
            'mtime_ns': value.st_mtime_ns, 'ctime_ns': value.st_ctime_ns}


class CommandStreamEvidence:
    """Observe exclusive files using both clocks and actual filesystem witnesses.

    Witnesses contain no invented timestamps. Every attempted after-witness is
    retained; the first whose actual filesystem clock brackets the closed streams
    is used. The bounded wait changes no timestamp and adds no acceptance slack.
    """
    WITNESS_ATTEMPTS = 16
    WITNESS_POLL_NS = 5_000_000

    def __init__(self, root, stdout, stderr):
        self.root = Path(root).resolve()
        self.paths = {'stdout': Path(stdout), 'stderr': Path(stderr)}
        if self.paths['stdout'].parent != self.paths['stderr'].parent:
            raise RuntimeError('Command streams must share a filesystem witness directory')
        if not self.paths['stdout'].name.endswith('.stdout.log'):
            raise RuntimeError('Command stdout role differs')
        self.label = self.paths['stdout'].name[:-len('.stdout.log')]
        if self.paths['stderr'].name != self.label + '.stderr.log':
            raise RuntimeError('Command stderr role differs')
        self.folder = self.paths['stdout'].parent
        self.handles = {}
        self.value = {'schema': 2, 'started': command_clock(), 'streams': {},
                      'after_witnesses': [], 'after_witness_attempt_limit': self.WITNESS_ATTEMPTS,
                      'after_witness_poll_ns': self.WITNESS_POLL_NS,
                      'filesystem_bracket_complete': False}

    def open_file(self, path):
        name = path.relative_to(self.root).as_posix()
        row = {'path': name, 'exclusive_mode': 'xb', 'open_started': command_clock()}
        try:
            handle = path.open('xb')
        except BaseException as error:
            self.value.setdefault('failed_file_operations', []).append({**row, 'error': repr(error)})
            raise
        try:
            row['initial_stat'] = command_file_stat(os.fstat(handle.fileno()))
            row['initial_sha256'] = hashlib.sha256(b'').hexdigest()
            row['opened'] = command_clock()
            value = row['initial_stat']
            if not stat.S_ISREG(value['mode']) or value['links'] != 1 or value['bytes'] != 0:
                raise RuntimeError('Exclusive command file is not a new empty regular inode')
            return handle, row
        except BaseException as error:
            self.value.setdefault('failed_file_operations', []).append({**row, 'error': repr(error)})
            self.close_after_error(handle)
            raise

    def close_after_error(self, handle):
        """A second close error must not prevent cleanup of another owned handle."""
        try:
            if not handle.closed:
                handle.close()
        except BaseException as error:
            self.value.setdefault('cleanup_errors', []).append(repr(error))
            return error
        return None

    def close_file(self, handle, row):
        handle.flush()
        row['closing'] = command_clock()
        row['final_stat'] = command_file_stat(os.fstat(handle.fileno()))
        handle.close()
        row['closed'] = command_clock()
        path = self.root / row['path']
        before = command_file_stat(path.stat())
        if before != row['final_stat'] or path.is_symlink():
            raise RuntimeError('Command file changed inode or metadata during closure')
        with path.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        after = command_file_stat(path.stat())
        if after != before:
            raise RuntimeError('Command file changed while hashing')
        first = row['initial_stat']
        if any(first[key] != before[key] for key in ('device', 'inode', 'mode', 'links')):
            raise RuntimeError('Exclusive command file ownership changed')
        row.update(bytes=before['bytes'], sha256=digest, hashed=command_clock())

    def witness(self, suffix):
        handle, row = self.open_file(self.folder / (self.label + '.' + suffix + '.log'))
        try:
            self.close_file(handle, row)
        except BaseException as error:
            self.value.setdefault('failed_witnesses', []).append({**row, 'error': repr(error)})
            raise
        finally:
            self.close_after_error(handle)
        return row

    def __enter__(self):
        try:
            self.value['before_witness'] = self.witness('filesystem-before')
            for name in ('stdout', 'stderr'):
                handle, row = self.open_file(self.paths[name])
                self.handles[name] = handle
                self.value['streams'][name] = row
            self.value['invocation_started'] = command_clock()
            return self
        except BaseException as error:
            self.value['error'] = repr(error)
            for name, handle in self.handles.items():
                if not handle.closed:
                    try:
                        self.close_file(handle, self.value['streams'][name])
                    except BaseException as cleanup_error:
                        self.value.setdefault('cleanup_errors', []).append(repr(cleanup_error))
                        self.close_after_error(handle)
            self.value['finished'] = command_clock()
            raise

    def __exit__(self, kind, error, traceback):
        self.value['invocation_finished'] = command_clock()
        if error is not None:
            self.value['error'] = repr(error)
        cleanup_error = None
        for name in ('stderr', 'stdout'):
            handle = self.handles[name]
            try:
                self.close_file(handle, self.value['streams'][name])
            except BaseException as failure:
                self.value.setdefault('cleanup_errors', []).append(repr(failure))
                if cleanup_error is None:
                    cleanup_error = failure
            finally:
                failure = self.close_after_error(handle)
                if cleanup_error is None and failure is not None:
                    cleanup_error = failure
        try:
            before = self.value['before_witness']['final_stat']
            streams = [self.value['streams'][name][phase]
                       for name in ('stdout', 'stderr') for phase in ('initial_stat', 'final_stat')]
            for index in range(self.WITNESS_ATTEMPTS):
                witness = self.witness(f'filesystem-after-{index:02d}')
                self.value['after_witnesses'].append(witness)
                after = witness['final_stat']
                complete = all(before['device'] == value['device'] == after['device']
                    and before['ctime_ns'] <= value['mtime_ns'] <= after['ctime_ns']
                    and before['ctime_ns'] <= value['ctime_ns'] <= after['ctime_ns'] for value in streams)
                if complete:
                    self.value['filesystem_bracket_complete'] = True
                    break
                if index + 1 < self.WITNESS_ATTEMPTS:
                    time.sleep(self.WITNESS_POLL_NS / 1_000_000_000)
            if not self.value['filesystem_bracket_complete']:
                raise RuntimeError('Actual filesystem witnesses did not bracket command stream timestamps')
        except BaseException as failure:
            self.value.setdefault('cleanup_errors', []).append(repr(failure))
            if cleanup_error is None:
                cleanup_error = failure
        self.value['finished'] = command_clock()
        if error is None and cleanup_error is not None:
            raise cleanup_error
        return False

    def add_to(self, row):
        for prefix, name in (('started', 'started'), ('ended', 'finished')):
            value = self.value.get(name)
            if value is not None:
                row[prefix + '_unix_ns'] = value['unix_ns']
                row[prefix + '_monotonic_ns'] = value['monotonic_ns']
                row[prefix + '_utc'] = value['utc']
        if 'finished' in self.value:
            row['duration_seconds'] = (self.value['finished']['monotonic_ns'] - self.value['started']['monotonic_ns']) / 1_000_000_000
        for name in ('stdout', 'stderr'):
            value = self.value['streams'].get(name)
            if value is not None and all(key in value for key in ('path', 'bytes', 'sha256')):
                row[name] = {key: value[key] for key in ('path', 'bytes', 'sha256')}
            else:
                row[name] = None
        row['stream_evidence'] = self.value




def validate_dependencies(root: Path, registry: list[dict]) -> set[str]:
    """Require the exact uncredited getters and a unique registered numeric consumer."""
    require(sha(root / DEPENDENCY_PATH) == DEPENDENCY_SHA256, 'Original numeric dependency bytes changed')
    keys = [row['target'] + '->' + row['method'] for row in registry]
    require(len(set(keys)) == len(keys) and keys.count(METHOD) == 1, 'Numeric consumer is absent or duplicated')
    data = json.loads((root / DEPENDENCY_PATH).read_text())
    observed = {}
    for row in data['dependencies']:
        key = row['target'] + '->' + row['method']
        require(row['consumer'] == METHOD and key not in keys and key not in observed, 'Original dependency credited, duplicated or misbound')
        observed[key] = row['original_method_sha256']
    require(observed == GETTERS, 'Original numeric getter selection changed')
    return set(observed)


def target_entry(root: Path) -> dict:
    registry = json.loads((root / 'source/java-method-map.json').read_text())
    validate_dependencies(root, registry)
    rows = [row for row in registry if row['target'] + '->' + row['method'] == METHOD]
    require(len(rows) == 1, 'Numeric target must be registered exactly once')
    entry = rows[0]
    require(entry['java_source'] == catalog.DAY_HELPER_PATH and entry['helper'] == 'Lrecovered/ui/DayTriggerValueMethods;'
            and entry['helper_method'] == 'numericValue' and entry['instance'] is False
            and entry['proof_family'] == 'v9-ui' and entry['original_method_sha256'] == ORIGINAL_METHOD_SHA256,
            'Numeric registry binding changed')
    require(sha(root / catalog.DAY_HELPER_PATH) == catalog.DAY_HELPER_SHA256, 'Numeric positive source changed')
    return entry


def compile_target(production, source_root: Path, index: dict, entry: dict, helper_class: Path,
                   folder: Path, run, java: str | Path, jar: Path) -> tuple[Path, dict]:
    """Apply the production relocation and sole-method transplant to one real class."""
    folder.mkdir(parents=True, exist_ok=False)
    matches = [row for row in index.values() if row['descriptor'] == TARGET]
    require(len(matches) == 1, 'Original numeric class is not unique')
    original = source_root / matches[0]['path']
    require(sha(original) == matches[0]['sha256'], 'Original numeric class differs from its source index')
    old_text = original.read_text(); old_methods = production.methods(old_text); old = old_methods[SIGNATURE]
    require(hashlib.sha256(old.encode()).hexdigest() == ORIGINAL_METHOD_SHA256, 'Original numeric method body changed')
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
    require(sorted(p.name for p in dex_dir.iterdir()) == ['classes.dex'], 'Unexpected numeric D8 output inventory')
    helper_dex_sha = production.dex_integrity(dex_dir / 'classes.dex')
    smali = folder / 'helper-smali'
    run(folder, 'disassemble-helper', [java, '-Xmx512m', '-cp', jar, 'com.android.tools.smali.baksmali.Main',
                                      'd', '--api', '23', '--use-locals', '-o', smali, dex_dir / 'classes.dex'])
    require(sorted(p.relative_to(smali).as_posix() for p in smali.rglob('*.smali')) == ['recovered/ui/DayTriggerValueMethods.smali'], 'Unexpected helper disassembly class')
    emitted = production.methods((smali / 'recovered/ui/DayTriggerValueMethods.smali').read_text())
    compiled = emitted['numericValue' + SIGNATURE[SIGNATURE.index('('):]]
    restored, corrections = production.restore_from_preserved_source(entry, compiled, old, index, source_root)
    require(restored == compiled and corrections == [], 'Numeric method unexpectedly needs constructor-owner correction')
    body = production.ANNOT.sub('', compiled.split('\n', 1)[1].rsplit('.end method', 1)[0])
    require('Lrecovered/' not in body and 'Ldefpackage/' not in body, 'Host/helper type escaped numeric transplant')
    replacement = old.splitlines()[0] + '\n' + ''.join(production.ANNOT.findall(old)) + body + '.end method'
    require(old_text.count(old) == 1, 'Numeric replacement anchor is not unique')
    new_text = old_text.replace(old, replacement, 1); new_methods = production.methods(new_text)
    require(set(new_methods) == set(old_methods) and all(new_methods[k] == v for k, v in old_methods.items() if k != SIGNATURE), 'Other original methods changed')
    require(new_text.replace(replacement, '<NUMERIC>', 1) == old_text.replace(old, '<NUMERIC>', 1), 'Non-target class text changed')
    target = folder / 'target-smali/DayTrigger.smali'; target.parent.mkdir(); target.write_text(new_text)
    dex = folder / 'numeric-target.dex'
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
               'constructor_owner_corrections': []}
    write_json(folder / 'method-body-binding.json', binding)
    return dex, binding


def class_pins(host: Path, tools: Path, helper_override: Path | None = None) -> dict:
    """Pin every declared class of the harness, active oracle and scoped host types."""
    pins = {}
    specs = [(tools, 'DayNumericControlHarness'), (tools, 'DayTriggerParityCases'), (tools, 'BytecodeOracle'),
             (host, 'com/arlosoft/macrodroid/variables/VariableValue'), (host, 'defpackage/EngineRuntime'),
             (host, 'defpackage/TestClock'), (helper_override or host, 'recovered/ui/DayTriggerValueMethods')]
    for root, prefix in specs:
        stem = root / prefix
        paths = sorted(p for p in stem.parent.glob(stem.name + '*.class') if p.name == stem.name + '.class' or p.name.startswith(stem.name + '$'))
        require(any(p.name == stem.name + '.class' for p in paths), 'Missing numeric harness class: ' + prefix)
        for path in paths:
            name = path.relative_to(root).as_posix()[:-6].replace('/', '.')
            require(name not in pins, 'Duplicate class pin')
            pins[name] = {'path': str(path.resolve()), 'sha256': sha(path)}
    return pins


def same_inputs(a: dict, b: dict) -> bool:
    fields = ('case', 'kind', 'rawBitsHex', 'text', 'expected', 'expectedExceptionClass')
    return {k: a[k] for k in fields if k in a} == {k: b[k] for k in fields if k in b}


def require_counts(report: dict, expected: dict[str, int], message: str) -> None:
    require(all(type(report.get(key)) is int and report[key] == count for key, count in expected.items()), message)


def validate_report_identity(report: dict) -> None:
    require_counts(report, {'schema': 1, 'cases': 1291, 'executionPaths': 3,
                           'primaryRecoveredMethods': 1, 'originalDependencyMethods': 3},
                   'Numeric report count or schema differs')
    require(report.get('primaryMethod') == METHOD and report.get('androidRuntime') is False
            and report.get('dependencyKeys') == sorted(GETTERS)
            and report.get('inputInventorySha256') == catalog.DAY_INPUT_INVENTORY_SHA256,
            'Numeric report method or uncredited dependency identity differs')


def validate_positive_coverage(coverage: dict, count: int) -> None:
    methods = coverage.get('methods')
    require(isinstance(methods, list) and len(methods) == 4
            and [row.get('key') for row in methods] == sorted({METHOD, *GETTERS}),
            'Numeric coverage method/dependency inventory differs')
    instructions = edges = 0
    for row in methods:
        primary = row['key'] == METHOD
        require(row.get('primaryRecovery') is primary, 'Numeric getter was given recovery credit')
        offsets, branches = row.get('requiredOffsets'), row.get('requiredEdges')
        require(isinstance(offsets, list) and offsets
                and all(type(offset) is int and offset >= 0 for offset in offsets)
                and offsets == sorted(set(offsets)), 'Malformed numeric instruction offsets')
        require(isinstance(branches, list) and all(isinstance(edge, str) for edge in branches)
                and branches == sorted(set(branches)), 'Malformed numeric conditional edges')
        for edge in branches:
            parts = edge.split(':')
            require(len(parts) == 2 and all(part.isdecimal() for part in parts)
                    and all(int(part) in offsets for part in parts), 'Numeric branch edge names another instruction')
        wanted = count - 7 if primary else 3 if 'DictionaryEntry;' in row['key'] else 2
        require_counts(row, {'instructionCount': wanted, 'exceptionRegions': 0}, 'Numeric method coverage count differs')
        require(len(offsets) == wanted and len(branches) == (4 if primary else 0)
                and row.get('executedOffsets') == offsets and row.get('executedEdges') == branches
                and row.get('missingOffsets') == [] and row.get('missingEdges') == [],
                'Incomplete numeric method instruction/edge coverage')
        instructions += len(offsets); edges += len(branches)
    require(instructions == count and edges == 4, 'Numeric coverage totals differ from method rows')
    require_counts(coverage, {'instructionCount': instructions, 'executedInstructionCount': instructions,
                              'requiredBranchEdges': edges, 'executedBranchEdges': edges},
                   'Numeric coverage summary differs from method rows')
    require(coverage.get('allInstructionsAndEdgesExecuted') is True, 'Incomplete numeric coverage flag')


def validate_observations(report: dict) -> list[str]:
    """Recompute the fixed case inventory, integer-bit expectations and raw flags."""
    rows = report.get('observations')
    require(isinstance(rows, list) and len(rows) == 1291, 'Missing numeric observation inventory')
    inputs = [{k: row[k] for k in ('case', 'kind', 'rawBitsHex', 'text') if k in row} for row in rows]
    digest = hashlib.sha256(json.dumps(inputs, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
    require(digest == catalog.DAY_INPUT_INVENTORY_SHA256, 'Numeric input identities changed')
    failures, unsupported, wrong_expected = [], 0, 0
    for row in rows:
        bits = int(row['rawBitsHex'], 16); kind = row['kind']
        if kind == 'integer':
            expected = bits & 0xffffffff
            if expected & 0x80000000:
                expected -= 1 << 32
        elif kind == 'decimal':
            exponent, fraction = (bits >> 52) & 0x7ff, bits & ((1 << 52) - 1)
            negative = bool(bits >> 63)
            if exponent == 0x7ff:
                expected = 0 if fraction else -(1 << 31) if negative else (1 << 31) - 1
            else:
                significand = fraction | ((1 << 52) if exponent else 0)
                shift = (exponent or 1) - 1023 - 52
                magnitude = significand << shift if shift >= 0 else significand >> -shift
                expected = max(-(1 << 31), min((1 << 31) - 1, -magnitude if negative else magnitude))
        else:
            expected = 0
        null_entry = kind == 'null-entry'
        require((row.get('expectedExceptionClass') == 'java.lang.NullPointerException' and 'expected' not in row)
                if null_entry else type(row.get('expected')) is int and row['expected'] == expected and 'expectedExceptionClass' not in row,
                'Numeric recorded expectation differs from raw-bit arithmetic')
        observations = [row.get(path) for path in ('original', 'java', 'rebuilt')]
        for observed in observations:
            require(isinstance(observed, dict) and set(observed) == {'value', 'exceptionClass', 'rawMessage', 'unsupported'}
                    and type(observed['unsupported']) is bool and (observed['value'] is None or type(observed['value']) is int)
                    and (observed['exceptionClass'] is None or isinstance(observed['exceptionClass'], str))
                    and (observed['rawMessage'] is None or isinstance(observed['rawMessage'], str)), 'Malformed raw numeric outcome')
        def correct(observed):
            return not observed['unsupported'] and (observed['value'] is None and observed['exceptionClass'] == 'java.lang.NullPointerException'
                    if null_entry else observed['exceptionClass'] is None and observed['value'] == expected)
        same = all(correct(o) for o in observations) if null_entry else observations[0] == observations[1] == observations[2]
        right = all(correct(o) for o in observations)
        require(row.get('sameScopedOutcome') is same and row.get('allPathsMatchIndependentExpected') is right, 'Numeric outcome flags disagree with raw observations')
        if not same or not right:
            failures.append('day-numeric:' + row['case'])
        unsupported += sum(o['unsupported'] for o in observations)
        wrong_expected += not right
    require(report.get('mismatches') == failures, 'Numeric summary labels differ from all recorded cases')
    require_counts(report, {'mismatchCount': len(failures), 'unsupportedCount': unsupported,
                           'independentExpectedChecks': 1291, 'independentExpectedFailures': wrong_expected},
                   'Numeric summary differs from all recorded cases')
    return failures


def validate_positive(report: dict) -> None:
    validate_report_identity(report)
    require(validate_observations(report) == [], 'Positive numeric raw outcomes contain a failure')
    require(report.get('passed') is True
            and report.get('mismatchCount') == 0 and report.get('unsupportedCount') == 0
            and report.get('independentExpectedChecks') == 1291 and report.get('independentExpectedFailures') == 0,
            'Incomplete positive numeric three-path report')
    require(len(report.get('observations', [])) == 1291 and all(row.get('sameScopedOutcome') is True
            and row.get('allPathsMatchIndependentExpected') is True for row in report['observations']), 'Missing positive numeric observations')
    for key, count in [('originalCoverage', 32), ('rebuiltCoverage', 25)]:
        validate_positive_coverage(report.get(key, {}), count)


def validate_fault(positive: dict, fault: dict, required: list[str], expected_count: int, changed_path: str) -> None:
    validate_report_identity(fault)
    require(len(validate_observations(fault)) == expected_count, 'Numeric fault raw outcome count differs')
    require(changed_path in {'java', 'rebuilt'}, 'Invalid numeric changed path')
    require(fault.get('passed') is False and fault.get('cases') == 1291 and fault.get('executionPaths') == 3
            and fault.get('inputInventorySha256') == catalog.DAY_INPUT_INVENTORY_SHA256
            and fault.get('mismatchCount') == expected_count and fault.get('unsupportedCount') == 0
            and set(required).issubset(fault.get('mismatches', [])), 'Numeric fault lacks its required measured failures')
    old, changed = positive['observations'], fault.get('observations', [])
    require(len(old) == len(changed) == 1291, 'Numeric fault changed case count')
    stable_paths = {'original', 'java', 'rebuilt'} - {changed_path}
    for a, b in zip(old, changed):
        require(same_inputs(a, b) and all(a[path] == b[path] for path in stable_paths), 'Numeric fault changed an independent input/path')
    require(fault.get('originalCoverage') == positive['originalCoverage'], 'Numeric fault changed original instruction coverage')


def validate_java_controls(root: Path, records: list[dict]) -> tuple[dict[str, Path], list[dict]]:
    jobs = catalog.load_day_mutations(root)
    wanted = {job['name']: job for job in jobs}
    selected = [row for row in records if row.get('mutation', '').startswith('day-numeric-')]
    require(len(selected) == 13 and {row.get('mutation') for row in selected} == set(wanted), 'All thirteen actual UI Java faults are required')
    classes, bindings = {}, []
    for row in selected:
        name = row['mutation']; job = wanted[name]; short = name.removeprefix('day-numeric-')
        source = root / row['retainedSource']; compiled = root / row['retainedClass']
        expected_root = (root / 'reports/ui-mutants' / name).resolve()
        require(source.resolve() == expected_root / 'DayTriggerValueMethods.java'
                and compiled.resolve() == expected_root / 'DayTriggerValueMethods.class', 'Java control reused another artifact path')
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
    output = Path(tempfile.mkdtemp(prefix='day-numeric-dex-', dir=reports))
    destination = reports / 'day-numeric-dex-controls.json'
    started = command_clock()
    report = {'schema': 2, 'passed': False, 'status': 'RUNNING', 'androidRuntime': False,
              'started_utc': started['utc'], 'started_unix_ns': started['unix_ns'],
              'started_monotonic_ns': started['monotonic_ns'], 'commands': [],
              'evidence_directory': output.relative_to(root).as_posix(), 'primary_recovered_methods': 1,
              'original_dependency_methods': 3, 'expected_java_faults': 13, 'expected_actual_dex_faults': 2}
    write_json(destination, report)

    def run(folder, name, argv, expected=0, timeout=120):
        folder.mkdir(parents=True, exist_ok=True)
        stdout, stderr = folder / (name + '.stdout.log'), folder / (name + '.stderr.log')
        require(not stdout.exists() and not stderr.exists(), 'Numeric command output already exists')
        observation = CommandStreamEvidence(root, stdout, stderr); code = None
        try:
            with observation as streams:
                code = subprocess.run(list(map(str, argv)), cwd=root, stdout=streams.handles['stdout'],
                                      stderr=streams.handles['stderr'], timeout=timeout).returncode
        finally:
            row = {'name': name, 'argv': list(map(str, argv)), 'timeout_seconds': timeout, 'returncode': code}
            observation.add_to(row)
            report['commands'].append(row); write_json(destination, report)
        require(code == expected, 'Numeric command failed: ' + name)
        return row

    try:
        entry = target_entry(root)
        host, tools, jar = root / 'build/java/hostclasses', root / 'tools/classes', root / 'tools/lib/jadx-r2721.4574686-all.jar'
        apk = root / 'dist/MacroDroid-5.67.8-v9-hybrid.apk'; fixture = root / 'tests/fixtures/original-methods.dex'
        getter = root / 'build/hybrid/classes3.dex'
        require(sha(host / HELPER_CLASS) == HELPER_CLASS_SHA256, 'Current positive numeric class differs from measured compilation')
        classes, java_bindings = validate_java_controls(root, java_control_records)
        report['java_fault_bindings'] = java_bindings
        policy = ui_runtime_policy.verify(reports); java = policy['java_executable']
        index = json.loads((root / 'source/class-index.json').read_text())
        selected_original = [root / row['path'] for row in index.values() if row['descriptor'] in {TARGET, *(k.split('->', 1)[0] for k in GETTERS)}]
        pinned = [apk, fixture, getter, jar, root / 'build.py', root / 'constructor_owner.py',
                  root / 'tests/java/BytecodeOracle.java', root / catalog.DAY_HELPER_PATH, root / DEPENDENCY_PATH,
                  root / catalog.DAY_CATALOG_PATH, root / 'source/java-method-map.json',
                  root / 'test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java', *selected_original,
                  *[Path(row['class']) if Path(row['class']).is_absolute() else root / row['class'] for row in java_bindings]]
        pins = {str(p): identity(p) for p in pinned}
        write_json(output / 'input-identities.json', pins)
        require(sha(root / 'tests/java/BytecodeOracle.java') == 'd91ddcd8ec3d67d41d69b8252835e747c2cad2c6d5ea898323794ceec30e6b56', 'Active numeric oracle changed')
        positive_dex, positive_binding = compile_target(build, root, index, entry, host / HELPER_CLASS, output / 'positive-pipeline', run, java, jar)
        cp = os.pathsep.join(map(str, [jar, host, tools]))
        for name, dex in [('signed-apk', getter), ('positive-transplant', positive_dex)]:
            run(output, name + '-instructions', [java, '-Xmx512m', '-cp', cp, 'InspectMethod', dex, METHOD, output / (name + '-instructions.json')])
        packaged = (output / 'signed-apk-instructions.json').read_bytes() == (output / 'positive-transplant-instructions.json').read_bytes()
        require(packaged, 'Positive numeric transplant does not match the signed APK instructions')
        cfg = {'schema': 1, 'originalFixture': {'path': str(fixture), 'sha256': sha(fixture)},
               'rebuiltApk': {'path': str(apk), 'sha256': sha(apk)},
               'rebuiltGetterDex': {'path': str(getter), 'sha256': sha(getter), 'apk_member': 'classes3.dex'},
               'targetDex': {'path': str(positive_dex), 'sha256': sha(positive_dex)}, 'classPins': class_pins(host, tools)}

        def execute(name, config, expected=0):
            folder = output / name; folder.mkdir()
            path = folder / 'config.json'; target = folder / 'result.json'; write_json(path, config)
            run(folder, 'execute', [java, *ui_runtime_policy.JVM_FLAGS, '-Xmx512m', '-cp', cp,
                                    'DayNumericControlHarness', path, target], expected)
            return json.loads(target.read_text()) if target.exists() else None

        positive = execute('positive', cfg); validate_positive(positive)
        report['positive_signed_apk_instruction_match'] = True
        report['positive_pipeline'] = positive_binding
        faults = []
        jobs = {job['name'].removeprefix('day-numeric-'): job for job in catalog.load_day_mutations(root)}
        for name in ('integer-zero', 'decimal-zero'):
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
        require(restored == positive and (output / 'positive/result.json').read_bytes() == (output / 'positive-restoration/result.json').read_bytes(), 'Numeric positive restoration differs')
        require(all(identity(Path(p)) == value for p, value in pins.items()), 'Numeric source, class, fixture, APK or original inputs changed')
        validate_java_controls(root, java_control_records)
        report.update(passed=True, status='TWO_ACTUAL_NUMERIC_DEX_FAULTS_DETECTED_SIGNED_POSITIVE_RESTORED',
                      actual_dex_faults=faults, provenance_controls_rejected=2,
                      positive_restoration_byte_exact=True, source_class_fixture_and_apk_unchanged=True,
                      cases=1291, execution_paths=3, input_inventory_sha256=catalog.DAY_INPUT_INVENTORY_SHA256,
                      original_instruction_count=32, rebuilt_instruction_count=25, conditional_edges_per_path=4,
                      signed_apk_sha256=sha(apk), original_fixture_sha256=sha(fixture))
    except BaseException as error:
        report.update(status='NUMERIC_DEX_CONTROL_FAILED', error=repr(error))
        raise
    finally:
        finished = command_clock()
        report.update(finished_utc=finished['utc'], finished_unix_ns=finished['unix_ns'],
                      finished_monotonic_ns=finished['monotonic_ns']); write_json(destination, report)
    return report
