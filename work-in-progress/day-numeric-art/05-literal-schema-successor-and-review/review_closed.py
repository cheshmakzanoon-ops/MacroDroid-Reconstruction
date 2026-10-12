#!/usr/bin/env python3
"""Independently bind closed wrapper evidence without rerunning suites or Android."""
from __future__ import annotations

import ast
from collections import Counter
from datetime import datetime, timezone
import difflib
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import shlex
import stat
import tarfile
import traceback

OWN = Path('/dev/shm/macrodroid-day-numeric-art-schema-02')
DRAFT = Path('/dev/shm/macrodroid-day-numeric-art/wrapper-draft-01')
PROOF = Path('/dev/shm/macrodroid-day-numeric-art/checkpoints/04-wrapper-host-controls')
RAW = Path('/dev/shm/macrodroid-day-numeric-art/wrapper-controls-01')
SOURCE = OWN / 'source'
OUT = OWN / 'reports/closed-review-01'
CAPS = [(DRAFT, '6ca4711b330c64f72c0df716e4a8c407360297a9bbc09e634bd88feb295a6dd6'),
        (PROOF, '14bd536aa8af2e8458d8c3b1d45de6c770e55ce4e7f0f5e152a70bc6ed79e0bb')]
BEFORE = {}


def identity(path):
    start = path.lstat()
    assert stat.S_ISREG(start.st_mode), str(path)
    with path.open('rb') as stream:
        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    end = path.lstat()
    assert (start.st_dev, start.st_ino, start.st_size, start.st_mtime_ns, start.st_ctime_ns) == (
        end.st_dev, end.st_ino, end.st_size, end.st_mtime_ns, end.st_ctime_ns), str(path)
    return {'bytes': end.st_size, 'sha256': sha, 'mode': stat.S_IMODE(end.st_mode)}


def bind(path, wanted=None):
    value = identity(path)
    if wanted is not None:
        assert value == wanted, (str(path), value, wanted)
    BEFORE[str(path)] = value
    return value


def save(name, value):
    with (OUT / name).open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def methods(path):
    tree = ast.parse(path.read_bytes())
    return {n.name: ast.dump(n, include_attributes=False) for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')}


def expected(row):
    u = int(row['rawBitsHex'], 16)
    if row['kind'] == 'null-entry':
        return 'exception:java.lang.NullPointerException'
    if row['kind'] == 'integer':
        value = (u + 2**31) % 2**32 - 2**31
    elif row['kind'] == 'decimal':
        sign = -1 if u >= 2**63 else 1
        exponent, mantissa = (u // 2**52) % 2**11, u % 2**52
        if exponent == 2047:
            value = 0 if mantissa else (-2**31 if sign < 0 else 2**31 - 1)
        else:
            power = (exponent or 1) - 1023 - 52
            significand = mantissa + (2**52 if exponent else 0)
            rational = Fraction(sign * significand) * (Fraction(2**power) if power >= 0 else Fraction(1, 2**(-power)))
            value = (abs(rational.numerator) // rational.denominator) * (-1 if rational < 0 else 1)
            value = min(2**31 - 1, max(-2**31, value))
    else:
        value = 0
    return 'value:' + str(value)


def wire(raw, corpus, compact):
    assert raw.endswith(b'\n')
    lines = raw.decode('ascii').split('\n')
    assert lines[-1] == '' and len(lines) == len(corpus) + 3
    assert lines[0] == 'DAY_NUMERIC_ART_BEGIN\tcases=1291\tsha256=' + compact
    assert lines[-2] == 'DAY_NUMERIC_ART_END\tcases=1291\tpassed=true'
    exceptions = []
    for index, (row, line) in enumerate(zip(corpus, lines[1:-2])):
        columns = line.split('\t')
        assert columns[:5] == ['DAY_NUMERIC_ART_CASE', str(index), row['case'], row['kind'], row['rawBitsHex']]
        outcome = expected(row)
        if row['kind'] == 'null-entry':
            assert len(columns) == 8 and columns[5:7] == ['exception', 'java.lang.NullPointerException']
            assert re.fullmatch(r'(?:null|utf16:(?:[0-9a-f]{4})*)', columns[7])
            exceptions.append({'index': index, 'case': row['case'], 'class': columns[6],
                'raw_message_encoding': columns[7], 'raw_line_hex': line.encode('ascii').hex()})
        else:
            assert columns[5:] == outcome.split(':', 1)
    return {'case_count': len(corpus), 'raw_exception_records': exceptions}


def command_review(folder, corpus, compact, properties):
    report = json.loads((folder / 'probe-result.json').read_bytes())
    bind(folder / 'probe-result.json')
    assert report['execution_backend'] == 'simulated-host-control'
    assert type(report['schema_version']) is int and report['schema_version'] == 2
    assert report['status'] == 'SIMULATED_NUMERIC_CASES_PASSED'
    for name in ['android_runtime_executed', 'numeric_cases_on_art_verified',
                 'full_runtime_1_to_1_established', 'macro_configuration_verified',
                 'alarm_scheduling_verified', 'macro_execution_verified', 'ui_behavior_verified',
                 'app_apk_modified', 'app_installed', 'app_ui_interaction', 'compile_only_stubs_on_classpath']:
        assert report[name] is False
    assert report['inputs_before'] == report['inputs_after'] and report['cleanup_complete'] is True
    remote, adb, serial = report['owned_device_directory'], report['adb_path'], report['serial']
    assert re.fullmatch(r'/data/local/tmp/md-day-numeric-[0-9a-f]{32}', remote)
    expected_rows = []
    def add(label, argv, timeout=15, shell=False):
        tail = ['shell', shlex.join(argv)] if shell else argv
        expected_rows.append((label, [adb, '-s', serial, *tail], timeout))
    def env(phase):
        assert report[phase] == properties
        for key in properties:
            add(phase + '-' + key.replace('.', '-'), ['getprop', key], shell=True)
    binaries = [('app-process', '/system/bin/app_process64'), ('guest-timeout', '/system/bin/timeout')]
    inputs = [('probe', 'day-numeric-method-probe.dex'), ('original', 'original.apk'), ('candidate', 'candidate.apk')]
    add('device-state', ['get-state']); env('environment-before'); add('avd-name', ['emu', 'avd', 'name'])
    for name, path in binaries:
        add(name + '-executable', ['test', '-x', path], shell=True)
        add(name + '-sha256-before', ['sha256sum', path], shell=True)
    add('create-owned-directory', ['mkdir', '-m', '700', remote], shell=True)
    for key, name in inputs:
        destination = remote + '/' + name
        add('push-' + key, ['push', report['inputs_before'][key]['path'], destination], 120)
        add('readonly-' + key, ['chmod', '444', destination], shell=True)
        add('mode-' + key, ['stat', '-c', '%a', destination], shell=True)
        add('sha256-before-' + key, ['sha256sum', destination], shell=True)
    for variant in ('original', 'candidate'):
        env('environment-before-' + variant)
        argv = ['/system/bin/timeout', '-s', 'KILL', '120', '/system/bin/app_process64', '-Xverify:all', '-cp',
                remote + '/day-numeric-method-probe.dex:' + remote + '/' + variant + '.apk',
                remote, 'recovered.probe.DayNumericMethodProbe']
        assert report['executions'][variant]['guest_argv'] == argv
        add('execute-' + variant, argv, 150, shell=True)
    for key, name in inputs:
        add('sha256-after-' + key, ['sha256sum', remote + '/' + name], shell=True)
    for name, path in binaries:
        add(name + '-sha256-after', ['sha256sum', path], shell=True)
    env('environment-after')
    add('remove-owned-directory', ['rm', '-rf', '--', remote], shell=True)
    add('confirm-owned-directory-absent', ['test', '!', '-e', remote], shell=True)
    assert len(expected_rows) == len(report['commands']) == 60
    observations = {}
    for number, (row, wanted) in enumerate(zip(report['commands'], expected_rows), 1):
        assert (row['label'], row['argv'], row['timeout_seconds']) == wanted
        assert type(row['timeout_seconds']) is int and type(row['returncode']) is int and row['returncode'] == 0
        assert row['timed_out'] is False and 'execution_error' not in row
        raw = {}
        for stream in ('stdout', 'stderr'):
            item = row[stream]
            assert item['path'] == f'{number:03d}-{row["label"]}.{stream}.txt'
            value = bind(folder / item['path'])
            assert value['bytes'] == item['bytes'] and value['sha256'] == item['sha256']
            raw[stream] = (folder / item['path']).read_bytes()
        if not row['label'].startswith('push-'):
            assert raw['stderr'] == b''
        if row['label'].startswith('execute-'):
            variant = row['label'].removeprefix('execute-')
            parsed = wire(raw['stdout'], corpus, compact)
            assert parsed['raw_exception_records'] == report['executions'][variant]['raw_exception_records']
            assert report['executions'][variant]['command'] == row
            observations[variant] = parsed
    return {'folder': str(folder), 'commands': 60, 'raw_streams': 120, 'observations': observations,
            'android_executed': False}


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    result = {'schema': 1, 'started_utc': datetime.now(timezone.utc).isoformat(), 'passed': False,
              'android_executed': False, 'application_build_executed': False,
              'old_41_suite_rerun': False, 'reviewed_full_suite_scope': 'Previously closed 41 controls on exact old wrapper'}
    try:
        caps = []
        for folder, sha in CAPS:
            assert bind(folder / 'checkpoint.json')['sha256'] == sha
            cap = json.loads((folder / 'checkpoint.json').read_bytes())
            assert len({row['path'] for row in cap['files']}) == len(cap['files'])
            for row in cap['files']:
                bind(folder / row['path'], {k: row[k] for k in ('bytes', 'sha256', 'mode')})
            caps.append({'root': str(folder), 'checkpoint_sha256': sha, 'payloads': len(cap['files'])})
        result['capsules'] = caps
        inventory = json.loads((PROOF / 'evidence-inventory.json').read_bytes())
        wanted = {row['path']: row for row in inventory}
        seen = set()
        total = 0
        with tarfile.open(PROOF / 'evidence.tar.gz', 'r:gz') as archive:
            for member in archive:
                assert member.isfile() and member.name not in seen and member.name in wanted
                row = wanted[member.name]
                digest = hashlib.file_digest(archive.extractfile(member), 'sha256').hexdigest()
                assert (member.size, member.mode, digest) == (row['bytes'], row['mode'], row['sha256'])
                bind(RAW / member.name, {k: row[k] for k in ('bytes', 'sha256', 'mode')})
                seen.add(member.name); total += member.size
        assert seen == set(wanted) and len(seen) == 7629
        result['complete_old_archive'] = {'members': len(seen), 'bytes': total, 'all_archived_and_raw_bytes_match': True}
        old_tests = methods(DRAFT / 'source/test_android_day_numeric_method_probe.py')
        parent_tests = methods(DRAFT / 'parents/test_android_widget_method_probe.py')
        final_tests = methods(SOURCE / 'test_android_day_numeric_method_probe.py')
        assert len(parent_tests) == 31 and set(parent_tests) <= set(old_tests) and len(old_tests) == 41
        assert len(final_tests) == 42 and all(final_tests[name] == node for name, node in old_tests.items())
        log = (RAW / 'commands/all-41-host-controls/stderr.txt').read_text()
        matches = re.findall(r'^(test_\w+) \(test_android_day_numeric_method_probe\.NumericProbeControls\.(test_\w+)\) \.\.\. ok$', log, re.M)
        assert len(matches) == 41 and all(a == b for a, b in matches) and {a for a, _ in matches} == set(old_tests)
        assert log.rstrip().endswith('Ran 41 tests in 25.433s\n\nOK')
        result['named_controls'] = {'old_parent': 31, 'old_added': 10, 'old_log_actual': len(matches),
            'final_names': 42, 'old_41_bodies_unchanged': True, 'old_named_passes': [a for a, _ in matches]}
        for patch, a, b, old_name, new_name in [
            ('wrapper-derivation.patch', DRAFT / 'parents/android_widget_method_probe.py', DRAFT / 'source/android_day_numeric_method_probe.py', 'parent/android_widget_method_probe.py', 'source/android_day_numeric_method_probe.py'),
            ('controls-derivation.patch', DRAFT / 'parents/test_android_widget_method_probe.py', DRAFT / 'source/test_android_day_numeric_method_probe.py', 'parent/test_android_widget_method_probe.py', 'source/test_android_day_numeric_method_probe.py')]:
            actual = ''.join(difflib.unified_diff(a.read_text().splitlines(True), b.read_text().splitlines(True), fromfile=old_name, tofile=new_name))
            assert actual.encode() == (DRAFT / patch).read_bytes()
        result['both_parent_patches_reproduced_exactly'] = True
        for name in ['android_day_numeric_method_probe.py', 'test_android_day_numeric_method_probe.py']:
            bind(SOURCE / name)
        corpus = json.loads((SOURCE / 'probes/day-numeric-inputs.json').read_bytes())
        compact = hashlib.sha256(json.dumps(corpus, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
        assert compact == 'e083bc1996c5c7191bffe837fc0f30e254848a4754676ba0a8a119d23e8f6e79'
        values = [{'case': row['case'], 'expected': expected(row)} for row in corpus]
        assert values == json.loads((SOURCE / 'fixtures/independent-python-expectations.json').read_bytes())
        constants = {}
        for node in ast.parse((SOURCE / 'android_day_numeric_method_probe.py').read_bytes()).body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                try:
                    constants[node.targets[0].id] = ast.literal_eval(node.value)
                except (ValueError, TypeError):
                    pass
        positive = RAW / 'host-evidence/test_complete_simulated_success_cannot_be_claimed_as_android/result'
        differing = RAW / 'host-evidence/test_null_entry_exception_messages_are_lossless_and_not_required_identical/result'
        successor = OWN / 'reports/focused-01/host-evidence/test_literal_integer_schema_is_required_for_provenance_and_result_replay/result'
        result['literal_closed_positive_reviews'] = [command_review(folder, corpus, compact, constants['EXPECTED_DEVICE'])
                                                    for folder in (positive, differing, successor)]
        result['independent_fraction_expected_values'] = {'cases': len(corpus), 'kinds': dict(Counter(row['kind'] for row in corpus)),
                                                        'all_match_frozen_expectations': True}
        parent_result = json.loads((RAW / 'result.json').read_bytes())
        assert parent_result['passed'] is True and parent_result['android_executed'] is False
        for command in parent_result['commands']:
            folder = RAW / 'commands' / command['label']
            assert json.loads((folder / 'command.json').read_bytes()) == command
            assert type(command['returncode']) is int and command['returncode'] == 0 and command['timed_out'] is False
            for stream in ('stdout', 'stderr'):
                bind(folder / (stream + '.txt'), command[stream])
        inputs = json.loads((RAW / 'inputs-before.json').read_bytes())
        assert inputs == json.loads((RAW / 'inputs-after.json').read_bytes())
        for name, value in inputs.items():
            bind(Path(name), value)
        for path in sorted(SOURCE.rglob('*')):
            if path.is_file():
                bind(path)
        result['actual_input_and_41_control_commands'] = parent_result['commands']
        new_command = json.loads((OWN / 'reports/focused-01/command.json').read_bytes())
        assert new_command['returncode'] == 0 and new_command['timed_out'] is False
        new_log = (OWN / 'reports/focused-01/stderr.txt').read_text()
        assert 'Ran 1 test in 0.898s\n\nOK' in new_log
        assert json.loads((OWN / 'reports/focused-01/inputs-before.json').read_bytes()) == json.loads((OWN / 'reports/focused-01/inputs-after.json').read_bytes())
        result['focused_new_control'] = {'named_tests': 1, 'unittest_seconds': 0.898, 'outer_command_seconds': new_command['seconds'],
                                         'passed': True, 'full_42_suite_executed': False}
        result['passed'] = True
        result['status'] = 'CLOSED_SOURCE_ARCHIVE_AND_LITERAL_SIMULATED_RECORD_REVIEW'
    except Exception as exc:
        result.update(status='REVIEW_ATTEMPT_FAILED', error=repr(exc), traceback=traceback.format_exc())
    finally:
        after = {name: identity(Path(name)) for name in BEFORE}
        result['all_reviewed_inputs_unchanged'] = before_after_equal = BEFORE == after
        if not before_after_equal:
            result['passed'] = False
        save('inputs-before.json', BEFORE); save('inputs-after.json', after)
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save('result.json', result)
        print(json.dumps({k: v for k, v in result.items() if k in ('status', 'passed', 'error', 'all_reviewed_inputs_unchanged', 'complete_old_archive')}, indent=2))
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
