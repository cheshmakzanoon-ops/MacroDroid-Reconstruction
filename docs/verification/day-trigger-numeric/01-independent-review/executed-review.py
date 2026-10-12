#!/usr/bin/env python3
"""Independently review the frozen DayTrigger numeric proof; do not build an app."""
from collections import Counter
from datetime import datetime, timezone
import difflib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tarfile
import time
import traceback
import zipfile
import zlib

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'day-trigger-review/reports/01-closed-capsules'
CAPSULES = [
    ('01-original-java-proof', '6c78e9a5498e516f4a2b6f939055151fa2ab1d5585e12b77a4c991534593da0e'),
    ('02-three-path-and-compiled-controls', 'd93f08507afce1b6eebe1e3ae64338f86eb04ca01e26118bdd97f98f5d6af631'),
]
METHOD = 'r0(Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;)I'
TARGET = 'Lcom/arlosoft/macrodroid/triggers/DayTrigger;'
HELPER = 'recovered.ui.DayTriggerValueMethods'


def now():
    return datetime.now(timezone.utc).isoformat()


def bytes_id(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def identity(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return {'bytes': path.stat().st_size, 'sha256': digest.hexdigest()}


def write_json(relative, value):
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def declared_identity(row):
    return {k: row[k] for k in ('bytes', 'sha256')}


def read_capsule(name, digest):
    base = ROOT / 'day-trigger-numeric-recovery/checkpoints' / name
    assert identity(base / 'checkpoint.json')['sha256'] == digest
    cp = json.loads((base / 'checkpoint.json').read_text())
    source = []
    for row in cp['sourceFiles']:
        path = base / row['path']
        assert path.is_file() and not path.is_symlink()
        assert identity(path) == declared_identity(row), path
        source.append(row)
    assert len({r['path'] for r in source}) == len(source)
    archive = base / cp['evidenceArchive']['path']
    assert identity(archive) == declared_identity(cp['evidenceArchive'])
    with tarfile.open(archive) as stream:
        members = stream.getmembers()
        assert all(m.isfile() for m in members)
        assert len({m.name for m in members}) == len(members)
        assert set(m.name for m in members) == {r['path'] for r in cp['evidenceFiles']}
        payload = {m.name: stream.extractfile(m).read() for m in members}
    for row in cp['evidenceFiles']:
        assert bytes_id(payload[row['path']]) == declared_identity(row), row['path']
    assert bytes_id(payload['result.json']) == cp['result']
    result = json.loads(payload['result.json'])
    commands = json.loads(payload['command-ledger.json'])
    assert result['commands'] == commands
    observed_paths = set()
    previous = result['startedUtc']
    for command in commands:
        assert command['timeoutSeconds'] == 120 and not command.get('timedOut', False)
        assert command['startedUtc'] >= previous and command['finishedUtc'] >= command['startedUtc']
        previous = command['finishedUtc']
        assert command['returncode'] in (0, 1, 3)
        for stream in ('stdout', 'stderr'):
            row = command[stream]
            assert row['path'] not in observed_paths
            observed_paths.add(row['path'])
            assert bytes_id(payload[row['path']]) == declared_identity(row)
    assert previous <= result['finishedUtc']
    write_json(name + '/all-source-identities.json', source)
    write_json(name + '/all-evidence-identities.json', cp['evidenceFiles'])
    write_json(name + '/command-ledger.json', commands)
    write_json(name + '/actual-result.json', result)
    return base, cp, payload


def expected(row):
    """Use only integer bit operations, including for IEEE-754 binary64 inputs."""
    kind = row['kind']
    bits = int(row['rawBitsHex'], 16)
    if kind == 'null-entry':
        return None
    if kind == 'integer':
        low = bits & 0xffffffff
        return low - (1 << 32) if low & (1 << 31) else low
    if kind != 'decimal':
        return 0
    negative = bool(bits >> 63)
    exponent = (bits >> 52) & 0x7ff
    fraction = bits & ((1 << 52) - 1)
    if exponent == 0x7ff:
        if fraction:
            return 0
        return -(1 << 31) if negative else (1 << 31) - 1
    significand = fraction if exponent == 0 else fraction | (1 << 52)
    power = -1074 if exponent == 0 else exponent - 1023 - 52
    magnitude = significand << power if power >= 0 else significand >> -power
    value = -magnitude if negative else magnitude
    return max(-(1 << 31), min((1 << 31) - 1, value))


def matches(row, outcome):
    if outcome['unsupported']:
        return False
    if row['kind'] == 'null-entry':
        return outcome['value'] is None and outcome['exceptionClass'] == 'java.lang.NullPointerException'
    return outcome['value'] == expected(row) and outcome['exceptionClass'] is None and outcome['rawMessage'] is None


def evaluate_report(raw, paths):
    report = json.loads(raw)
    rows = report['observations']
    assert len(rows) == 1291 and len({row['case'] for row in rows}) == 1291
    assert report['cases'] == 1291 and report['executionPaths'] == len(paths)
    failures = []
    expected_failures = 0
    unsupported = 0
    for row in rows:
        exp = expected(row)
        if row['kind'] == 'null-entry':
            assert row['expectedExceptionClass'] == 'java.lang.NullPointerException'
        else:
            assert row['expected'] == exp
        correct = all(matches(row, row[p]) for p in paths)
        if row['kind'] == 'null-entry':
            same = correct
        else:
            same = all(row[p] == row[paths[0]] for p in paths)
        assert row['allPathsMatchIndependentExpected'] == correct
        assert row['sameScopedOutcome'] == same
        if not same or not correct:
            failures.append(row['case'])
        if not correct:
            expected_failures += 1
        unsupported += sum(bool(row[p]['unsupported']) for p in paths)
    assert report['mismatches'] == failures and report['mismatchCount'] == len(failures)
    assert report['independentExpectedFailures'] == expected_failures
    assert report['unsupportedCount'] == unsupported == 0
    return report


def case_identity(row):
    return {k: row[k] for k in ('case', 'kind', 'rawBitsHex', 'text') if k in row}


def verify_coverage(report):
    for key, total, primary in [('originalCoverage', 32, 25), ('rebuiltCoverage', 25, 18)]:
        if key not in report:
            continue
        coverage = report[key]
        assert coverage['instructionCount'] == coverage['executedInstructionCount'] == total
        assert coverage['requiredBranchEdges'] == coverage['executedBranchEdges'] == 4
        assert coverage['allInstructionsAndEdgesExecuted']
        assert len(coverage['methods']) == 4
        for row in coverage['methods']:
            assert row['requiredOffsets'] == row['executedOffsets']
            assert row['requiredEdges'] == row['executedEdges']
            assert not row['missingOffsets'] and not row['missingEdges']
            assert row['exceptionRegions'] == 0
            if row['primaryRecovery']:
                assert row['key'] == TARGET + '->' + METHOD and row['instructionCount'] == primary


def dex_checks(raw):
    assert raw[:4] == b'dex\n' and raw[7] == 0
    assert struct.unpack_from('<I', raw, 32)[0] == len(raw)
    assert hashlib.sha1(raw[32:]).digest() == raw[12:32]
    assert zlib.adler32(raw[12:]) & 0xffffffff == struct.unpack_from('<I', raw, 8)[0]
    return bytes_id(raw)


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    (OUT / 'executed-review.py').write_bytes(Path(__file__).read_bytes())
    result = {'schema': 1, 'started_utc': now(), 'status': 'REVIEW_PENDING', 'passed': False}
    own_commands = []
    try:
        first, cp1, a = read_capsule(*CAPSULES[0])
        second, cp2, b = read_capsule(*CAPSULES[1])
        assert len(cp1['sourceFiles']) == 19 and len(cp1['evidenceFiles']) == 47
        assert len(cp2['sourceFiles']) == 20 and len(cp2['evidenceFiles']) == 174
        assert b['baseline-checkpoint.json'] == (first / 'checkpoint.json').read_bytes()
        positives = [evaluate_report(a['positive-report.json'], ['original', 'java']),
                     evaluate_report(b['positive/parity.json'], ['original', 'java', 'rebuilt'])]
        for report in positives:
            assert report['passed'] and report['mismatchCount'] == 0 and report['independentExpectedFailures'] == 0
            verify_coverage(report)
        assert a['positive-report.json'] == a['restored-report.json']
        assert b['positive/parity.json'] == b['positive-restored/parity.json']
        rows = positives[1]['observations']
        for left, right in zip(positives[0]['observations'], rows):
            assert case_identity(left) == case_identity(right)
            assert left['original'] == right['original'] and left['java'] == right['java']
        arithmetic = [{'case': r['case'], 'kind': r['kind'], 'rawBitsHex': r['rawBitsHex'],
                       'recomputed_expected': expected(r), 'all_three_actual_paths_match': all(matches(r, r[p]) for p in ['original', 'java', 'rebuilt'])}
                      for r in rows]
        write_json('all-1291-integer-only-expectation-checks.json', arithmetic)
        controls = []
        r2 = json.loads(b['result.json'])
        catalog = json.loads(b['fault-catalog.json'])
        source = (second / 'inputs/source/java/recovered/ui/DayTriggerValueMethods.java').read_text()
        assert len(catalog) == len(r2['compiledJavaFaults']) == 13
        for fault, declared in zip(catalog, r2['compiledJavaFaults']):
            name = fault['name']
            assert name == declared['name']
            prefix = 'controls/' + name + '/'
            mutant_source = b[prefix + 'source/recovered/ui/DayTriggerValueMethods.java']
            mutant_class = b[prefix + 'hostclasses/recovered/ui/DayTriggerValueMethods.class']
            assert source.count(fault['old']) == 1
            assert source.replace(fault['old'], fault['new'], 1).encode() == mutant_source
            assert bytes_id(mutant_source) == declared['source']
            assert bytes_id(mutant_class) == declared['compiledClass']
            assert mutant_class != a['hostclasses/recovered/ui/DayTriggerValueMethods.class']
            observed = evaluate_report(b[prefix + 'execution/parity.json'], ['original', 'java', 'rebuilt'])
            assert not observed['passed'] and fault['requiredFailingCase'] in observed['mismatches']
            assert observed['mismatchCount'] == declared['mismatchCount']
            for old, changed in zip(rows, observed['observations']):
                assert case_identity(old) == case_identity(changed)
                assert old['original'] == changed['original'] and old['rebuilt'] == changed['rebuilt']
            controls.append({'name': name, 'kind': 'actual_compiled_java', 'mismatch_count': observed['mismatchCount'],
                             'required_case': fault['requiredFailingCase'], 'source_and_class_hashes_verified': True,
                             'complete_original_and_rebuilt_outcomes_unchanged': True})
        for declared in r2['compiledRebuiltFaults']:
            name = declared['name']
            observed = evaluate_report(b['controls/' + name + '-rebuilt-execution/parity.json'], ['original', 'java', 'rebuilt'])
            assert not observed['passed'] and observed['mismatchCount'] == declared['mismatchCount']
            assert declared['requiredFailingCase'] in observed['mismatches']
            for old, changed in zip(rows, observed['observations']):
                assert case_identity(old) == case_identity(changed)
                assert old['original'] == changed['original'] and old['java'] == changed['java']
            controls.append({'name': name, 'kind': 'actual_compiled_rebuilt_dex', 'mismatch_count': observed['mismatchCount'],
                             'required_case': declared['requiredFailingCase'], 'complete_original_and_java_outcomes_unchanged': True})
        for name, reason in [('original-as-rebuilt', 'Original fixture cannot masquerade as rebuilt'),
                             ('wrong-loaded-helper', 'Wrong loaded class hash: ' + HELPER)]:
            prefix = 'controls/' + name + '/'
            assert reason in b[prefix + 'execute-study.stderr.txt'].decode()
            assert prefix + 'parity.json' not in b
            controls.append({'name': name, 'kind': 'provenance_rejection_before_report', 'actual_reason': reason})
        write_json('all-17-compiled-and-provenance-controls.json', controls)
        inputs = second / 'inputs'
        pins = json.loads((inputs / 'preserved-input-pins.json').read_text())
        active = ROOT / 'MacroDroid-Reconstruction/project'
        binding_rows = []
        for name in ('build.py', 'constructor_owner.py'):
            frozen = inputs / 'production-pipeline' / name
            assert frozen.read_bytes() == (active / name).read_bytes()
            binding_rows.append({'role': name, 'frozen': identity(frozen), 'active_same_bytes': True})
        registry = json.loads((active / 'source/java-method-map.json').read_text())
        assert not any(r['target'] == TARGET and r['method'] == METHOD for r in registry)
        oracle = inputs / 'BytecodeOracle.java'
        current_oracle = active / 'tests/java/BytecodeOracle.java'
        delta = ''.join(difflib.unified_diff(oracle.read_text().splitlines(True), current_oracle.read_text().splitlines(True),
                                           fromfile='frozen-study/BytecodeOracle.java', tofile='active-project/BytecodeOracle.java'))
        (OUT / 'frozen-to-active-oracle.patch').write_text(delta)
        binding_rows.append({'role': 'BytecodeOracle.java', 'frozen': identity(oracle), 'active': identity(current_oracle),
                             'same_bytes': oracle.read_bytes() == current_oracle.read_bytes(),
                             'reviewed_delta': 'Active adds constructor-owner adapter/validation and AND_INT; neither path is executed by the four selected methods.'})
        sys.path.insert(0, str(inputs / 'production-pipeline'))
        spec = importlib.util.spec_from_file_location('independent_day_production_build', inputs / 'production-pipeline/build.py')
        build = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build)
        index = json.loads((inputs / 'production-pipeline/source/class-index-selected.json').read_text())
        target_pin = next(r for r in pins['selectedOriginalMethods'] if r['descriptor'] == TARGET)
        original_path = inputs / 'production-pipeline' / target_pin['sourcePath']
        original_text = original_path.read_text()
        old = build.methods(original_text)
        assert len(old) == 34 and bytes_id(old[METHOD].encode())['sha256'] == target_pin['methodTextSha256']
        for pin in pins['selectedOriginalMethods']:
            path = inputs / 'production-pipeline' / pin['sourcePath']
            assert identity(path) == pin['sourceIdentity']
            assert bytes_id(build.methods(path.read_text())[pin['method']].encode())['sha256'] == pin['methodTextSha256']
            assert path.read_bytes() == (ROOT / 'current/MacroDroid_v9' / pin['sourcePath']).read_bytes()
        proposed = json.loads(b['proposed-method-entry.json'])
        pipeline_checks = []
        for prefix, helper_bytes in [
            ('positive-pipeline/', a['hostclasses/recovered/ui/DayTriggerValueMethods.class']),
            ('controls/integer-zero-rebuilt-pipeline/', b['controls/integer-zero/hostclasses/recovered/ui/DayTriggerValueMethods.class']),
            ('controls/decimal-zero-rebuilt-pipeline/', b['controls/decimal-zero/hostclasses/recovered/ui/DayTriggerValueMethods.class'])]:
            binding = json.loads(b[prefix + 'method-body-binding.json'])
            relocated = b[prefix + 'relocated/recovered/ui/DayTriggerValueMethods.class']
            assert build.relocate_class(helper_bytes) == relocated
            with zipfile.ZipFile(io.BytesIO(b[prefix + 'inputs.jar'])) as z:
                assert z.namelist() == ['recovered/ui/DayTriggerValueMethods.class']
                assert z.read(z.namelist()[0]) == relocated
            helper_text = b[prefix + 'helper-smali/recovered/ui/DayTriggerValueMethods.smali'].decode()
            compiled = build.methods(helper_text)['numericValue' + METHOD[METHOD.index('('):]]
            restored, corrections = build.restore_from_preserved_source(proposed, compiled, old[METHOD], index, inputs / 'production-pipeline')
            assert restored == compiled and corrections == []
            body = build.ANNOT.sub('', compiled.split('\n', 1)[1].rsplit('.end method', 1)[0])
            assert 'Lrecovered/' not in body and 'Ldefpackage/' not in body
            replacement = old[METHOD].splitlines()[0] + '\n' + ''.join(build.ANNOT.findall(old[METHOD])) + body + '.end method'
            target_text = b[prefix + 'target-smali/DayTrigger.smali'].decode()
            assert original_text.replace(old[METHOD], replacement, 1) == target_text
            new = build.methods(target_text)
            assert set(old) == set(new)
            assert all(new[key] == value for key, value in old.items() if key != METHOD)
            assert target_text.replace(replacement, '<PRIMARY>', 1) == original_text.replace(old[METHOD], '<PRIMARY>', 1)
            assert binding['loadedHelperClass'] == bytes_id(helper_bytes)
            assert binding['relocatedHelperClass'] == bytes_id(relocated)
            assert binding['compilerInput'] == bytes_id(b[prefix + 'inputs.jar'])
            assert binding['compiledMethodSha256'] == bytes_id(compiled.encode())['sha256']
            assert binding['transplantedMethodSha256'] == bytes_id(replacement.encode())['sha256']
            assert binding['transplantedClass'] == bytes_id(target_text.encode())
            assert binding['helperDexSha256'] == dex_checks(b[prefix + 'd8/classes.dex'])['sha256']
            assert binding['rebuiltDexSha256'] == dex_checks(b[prefix + 'rebuilt-day-trigger.dex'])['sha256']
            commands = [q for q in r2['commands'] if q['stdout']['path'].startswith(prefix)]
            assert len(commands) == 3 and all(q['returncode'] == 0 for q in commands)
            args = commands[0]['argv']
            assert args[args.index('com.android.tools.r8.D8') + 1:args.index('--output')] == ['--release', '--no-desugaring', '--min-api', '23']
            pipeline_checks.append({'prefix': prefix, 'binding': binding, 'recomputed_production_transplant_matches': True,
                                    'all_33_other_methods_and_other_class_text_unchanged': True,
                                    'both_dex_header_signature_checksum_and_sha_verified': True})
        write_json('all-three-production-transplant-checks.json', pipeline_checks)
        write_json('active-input-and-integration-bindings.json', binding_rows)
        external = json.loads(b['external-input-identities.json'])
        for role, pin in external.items():
            assert identity(Path(pin['path'])) == declared_identity(pin), role
        extractor = inputs / 'ExtractDayFixture.java'
        jar = Path(pins['externalToolchainJar']['path'])
        jdk = ROOT / 'tooling/jdk21'
        direct = OUT / 'direct-original-apk-check'
        direct.mkdir()
        classes = direct / 'classes'
        classes.mkdir()
        def run(name, args):
            began = now()
            started = time.monotonic()
            stdout = direct / (name + '.stdout.txt')
            stderr = direct / (name + '.stderr.txt')
            with stdout.open('xb') as out, stderr.open('xb') as err:
                proc = subprocess.run(list(map(str, args)), stdout=out, stderr=err, timeout=120,
                                      cwd=direct, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
            row = {'name': name, 'argv': list(map(str, args)), 'started_utc': began, 'finished_utc': now(),
                   'seconds': time.monotonic() - started, 'timeout_seconds': 120, 'exit_code': proc.returncode,
                   'stdout': {'path': stdout.relative_to(OUT).as_posix(), **identity(stdout)},
                   'stderr': {'path': stderr.relative_to(OUT).as_posix(), **identity(stderr)}}
            own_commands.append(row)
            write_json('independent-command-ledger.json', own_commands)
            assert proc.returncode == 0, name
        run('compile-exact-extractor', [jdk / 'bin/javac', '-cp', jar, '-d', classes, extractor])
        assert (classes / 'ExtractDayFixture.class').read_bytes() == a['harnessclasses/ExtractDayFixture.class']
        fixture = direct / 'original-selected.dex'
        inventory = direct / 'original-method-inventory.json'
        run('extract-from-pinned-original-apk', [jdk / 'bin/java', '-Xmx512m', '-Xverify:all', '-cp', os.pathsep.join(map(str, [classes, jar])),
                                                'ExtractDayFixture', pins['originalApk']['path'], fixture, inventory])
        assert fixture.read_bytes() == a['original-selected.dex']
        assert inventory.read_bytes() == a['original-method-inventory.json']
        actual_inventory = json.loads(inventory.read_text())
        coverage = {r['key']: r for r in positives[1]['originalCoverage']['methods']}
        assert set(coverage) == {r['key'] for r in actual_inventory}
        for method in actual_inventory:
            assert method['partition'] == 'classes3.dex' and method['exceptionRegions'] == 0
            assert [i['offset'] for i in method['instructions']] == coverage[method['key']]['requiredOffsets']
            assert not any(i['opcode'] in ['NEW_INSTANCE', 'INVOKE_DIRECT', 'AND_INT'] for i in method['instructions'])
        for role, pin in external.items():
            assert identity(Path(pin['path'])) == declared_identity(pin), role
        for name, digest in CAPSULES:
            base = ROOT / 'day-trigger-numeric-recovery/checkpoints' / name
            assert identity(base / 'checkpoint.json')['sha256'] == digest
            cp = json.loads((base / 'checkpoint.json').read_text())
            for row in cp['sourceFiles']:
                assert identity(base / row['path']) == declared_identity(row)
            assert identity(base / cp['evidenceArchive']['path']) == declared_identity(cp['evidenceArchive'])
        write_json('primary-language-reference.json', {
            'url': 'https://docs.oracle.com/javase/specs/jls/se21/html/jls-5.html#jls-5.1.3',
            'section': '5.1.3 Narrowing Primitive Conversion',
            'consulted_utc_date': '2026-10-12',
            'paraphrase': 'Integral narrowing retains the low destination-width bits. Floating narrowing truncates toward zero; NaN becomes zero and out-of-range values saturate at the destination integer limits.',
            'independent_reviewer_implementation': 'Integer bit extraction and shifting only; no floating-point-to-integer cast or BigDecimal computation is used by this reviewer.'})
        result.update({'status': 'INDEPENDENT_DAY_NUMERIC_CAPSULE_REVIEW_PASSED', 'passed': True,
                       'capsules': [{'name': n, 'checkpoint_sha256': h} for n, h in CAPSULES],
                       'all_source_files_verified': [19, 20], 'all_archive_members_verified': [47, 174],
                       'cases': 1291, 'case_kinds': dict(Counter(r['kind'] for r in rows)), 'execution_paths': 3,
                       'independent_integer_only_expected_mismatches': 0,
                       'original_instructions': 32, 'original_primary_instructions': 25,
                       'rebuilt_instructions': 25, 'rebuilt_primary_instructions': 18,
                       'branch_edges_per_path': 4, 'compiled_java_faults_detected': 13,
                       'actual_rebuilt_dex_faults_detected': 2, 'provenance_controls_detected': 2,
                       'original_commands_verified': [len(json.loads(a['command-ledger.json'])), len(r2['commands'])],
                       'positive_reports_restored_byte_for_byte': True,
                       'fresh_extractor_class_matches_frozen': True, 'fresh_direct_original_fixture_matches_frozen': True,
                       'original_fixture': identity(fixture), 'all_three_production_transplants_recomputed': True,
                       'all_33_non_target_methods_preserved_each_time': True,
                       'production_helpers_match_active': True, 'frozen_oracle_diff_reviewed_as_outside_selected_opcodes': True,
                       'selected_method_registered_in_active_project': False,
                       'app_apk_built_or_modified': False, 'android_or_art_executed': False,
                       'calendar_or_scheduling_behavior_established': False,
                       'original_source_archive_toolchain_and_apk_hashes_unchanged': True})
    except BaseException as error:
        result.update({'status': 'INDEPENDENT_DAY_REVIEW_FAILURE_RETAINED', 'error': str(error), 'passed': False})
        (OUT / 'failure-traceback.txt').write_text(traceback.format_exc())
    finally:
        result['finished_utc'] = now()
        write_json('result.json', result)
        print(json.dumps(result, indent=2))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
