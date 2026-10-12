#!/usr/bin/env python3
"""Independently check fresh full-host results before labeling the WIP build accepted."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import math
from pathlib import Path
import re
import shutil
import sys
import zipfile

import inputs


def count(value, expected, message):
    inputs.require(type(value) is int and value == expected, message)


def flags(value, expected, message):
    inputs.require(all(value.get(key) is wanted for key, wanted in expected.items()), message)


def epoch_ns(value):
    inputs.require(isinstance(value, str), 'Missing timestamp')
    parsed = datetime.fromisoformat(value)
    inputs.require(parsed.tzinfo is not None, 'Timestamp lacks timezone')
    return int(parsed.timestamp() * 1_000_000_000)


class Artifacts:
    """Every result path is canonical, fresh, and physically distinct from other paths."""
    def __init__(self, root, started_ns, ended_ns):
        self.root = Path(root)
        self.started_ns, self.ended_ns = started_ns, ended_ns
        self.rows, self.physical = {}, {}

    def path(self, name):
        path = inputs.regular(self.root, name)
        status = path.stat()
        inputs.require(self.started_ns <= status.st_mtime_ns <= self.ended_ns
                       and self.started_ns <= status.st_ctime_ns <= self.ended_ns,
                       'Result is outside the actual execution interval: ' + name)
        key = (status.st_dev, status.st_ino)
        inputs.require(key not in self.physical or self.physical[key] == name,
                       'One physical result file represents multiple artifacts: ' + name)
        row = {'path': name, **inputs.identity(path), 'device': status.st_dev, 'inode': status.st_ino,
               'mtime_ns': status.st_mtime_ns, 'ctime_ns': status.st_ctime_ns}
        inputs.require(name not in self.rows or self.rows[name] == row, 'Result changed during verification: ' + name)
        self.rows[name] = row
        self.physical[key] = name
        return path

    def raw(self, name):
        raw = self.path(name).read_bytes()
        inputs.require(inputs.byte_identity(raw) == {k: self.rows[name][k] for k in ('bytes', 'sha256')},
                       'Result changed while reading: ' + name)
        return raw

    def json(self, name):
        return inputs.document(self.raw(name))

    def hash(self, name, expected):
        self.path(name)
        inputs.require(self.rows[name]['sha256'] == expected, 'Recorded result hash differs: ' + name)


def verify_execution(execution, prepared, pins):
    flags(execution, {'passed': True, 'build_inputs_unchanged': True, 'active_promoted': False,
                      'android_runtime_executed': False, 'full_runtime_1_to_1_established': False},
          'Execution wrapper did not complete exactly')
    inputs.require(execution.get('status') == 'HOST_ACCEPTANCE_PROCESS_EXITED_ZERO'
                   and 'error' not in execution and execution.get('project') == prepared['project'],
                   'Wrong wrapper result or project')
    inputs.require(execution.get('input_snapshot_before') == execution.get('input_snapshot_after') == pins['future_snapshot'],
                   'Wrapper input identity differs')
    child = execution.get('execution', {})
    count(child.get('returncode'), 0, 'Acceptance process did not exit zero')
    count(child.get('timeout_seconds'), pins['acceptance_timeout_seconds'], 'Overall acceptance bound differs')
    inputs.require(child.get('timed_out') is False and 'error' not in child
                   and child.get('argv') == [execution['python_executable'], '-B', 'acceptance.py']
                   and child.get('cwd') == prepared['project'], 'Acceptance invocation differs')
    start, end = child.get('started_unix_ns'), child.get('ended_unix_ns')
    inputs.require(type(start) is int and type(end) is int and 0 < start < end,
                   'Missing actual execution interval')
    return start, end


def verify_gates(latest, execution, pins, artifacts):
    flags(latest, {'host_acceptance_passed': True, 'source_edit_probe_skipped': False,
                   'build_inputs_unchanged': True, 'android_runtime_executed': False,
                   'full_runtime_1_to_1_established': False, 'complete_high_level_java_kotlin_source': False},
          'Incomplete or out-of-scope acceptance result')
    count(latest.get('input_files'), pins['future_snapshot']['files'], 'Acceptance input count differs')
    inputs.require(latest.get('input_snapshot_before') == latest.get('input_snapshot_after') == pins['future_snapshot']['snapshot_sha256']
                   and 'failure' not in latest and 'remaining_not_executed' not in latest, 'Acceptance source or completion differs')
    inputs.require(artifacts.started_ns <= epoch_ns(latest.get('started_utc')) <= epoch_ns(latest.get('finished_utc')) <= artifacts.ended_ns,
                   'Acceptance report is outside the invocation interval')
    commands = latest.get('commands')
    inputs.require(isinstance(commands, list) and len(commands) == 16, 'Missing full gate inventory')
    folder = str(inputs.relative(commands[0]['log']).parent)
    inputs.require(re.fullmatch(r'reports/acceptance-[0-9]{8}T[0-9]{12}Z', folder), 'Unexpected acceptance result directory')
    actual_folders = sorted(path.relative_to(artifacts.root).as_posix() for path in (artifacts.root / 'reports').glob('acceptance-*') if path.is_dir())
    inputs.require(actual_folders == [folder], 'Missing, additional, or historical acceptance directory')
    inputs.require(artifacts.raw(folder + '/result.json') == artifacts.raw('reports/acceptance-latest.json'),
                   'Latest and session result bytes differ')
    for index, (row, expected) in enumerate(zip(commands, pins['gate_commands']), 1):
        label, arguments = expected
        inputs.require(row.get('label') == label and row.get('command') == [execution['python_executable'], *arguments],
                       'Gate order or exact command differs')
        inputs.require(row.get('log') == f'{folder}/{index:02d}-{label}.log', 'Gate reused or renamed another log')
        count(row.get('exit_code'), 0, 'A required gate did not exit zero')
        count(row.get('timeout_seconds'), 5400 if label == 'ui-negative-controls' else 1200, 'Per-gate bound differs')
        inputs.require(row.get('passed') is True and 'error' not in row
                       and type(row.get('seconds')) in (int, float) and math.isfinite(row['seconds']) and row['seconds'] >= 0,
                       'Malformed or failed gate outcome')
        artifacts.hash(row['log'], row['log_sha256'])
    hashes = latest.get('fresh_evidence_sha256')
    inputs.require(isinstance(hashes, dict) and set(hashes) == set(pins['fresh_reports']) and len(hashes) == 23,
                   'Missing or additional fresh acceptance report')
    reports = {}
    for name in pins['fresh_reports']:
        artifacts.hash('reports/' + name, hashes[name])
        reports[name] = artifacts.json('reports/' + name)
    return reports


def verify_python(raw, expected):
    text = raw.decode('utf-8')
    summaries = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', text, re.M)
    headers = re.findall(r'^test_\S+ \(.*\) \.\.\. ', text, re.M)
    successes = re.findall(r'(?:\.\.\. |^)ok$', text, re.M)
    inputs.require(len(summaries) == 1 and int(summaries[0][0]) == expected
                   and len(headers) == len(successes) == expected and text.rstrip().endswith('\nOK'),
                   'Python success count is incomplete or includes skips/failures')
    return {'tests': expected, 'individual_successes': len(successes), 'seconds': float(summaries[0][1])}


def verify_apks(latest, pins, artifacts, reports):
    rows = latest.get('apks')
    inputs.require(isinstance(rows, dict) and set(rows) == {'baseline', 'hybrid'}, 'Missing actual APK inventory')
    actual = {}
    for variant in ('baseline', 'hybrid'):
        row = rows[variant]
        name = f'dist/MacroDroid-5.67.8-v9-{variant}.apk'
        inputs.require(row.get('path') == name, 'Unexpected APK path')
        value = inputs.identity(artifacts.path(name))
        inputs.require(value == {k: row[k] for k in ('bytes', 'sha256')}, 'Actual APK identity differs from acceptance')
        if variant == 'baseline':
            inputs.require(value == pins['baseline_apk'], 'Unchanged baseline APK did not reproduce')
        else:
            inputs.require(value != pins['previous_active_apk'], 'Numeric method did not change the old hybrid artifact')
        built = artifacts.json('reports/' + variant + '-build.json')
        inputs.require(built.get('variant') == variant and built.get('apk') == name
                       and built.get('bytes') == value['bytes'] and built.get('sha256') == value['sha256'], 'Build/APK result differs')
        flags(built, {'original_apk_build_input': False, 'original_dex_build_input': False}, 'Original APK/DEX became an application build input')
        count(built.get('source_dex_partitions'), 9, 'Application DEX partition count differs')
        for suffix in ('-roundtrip.json', '-resource-parity.json'):
            report = reports[variant + suffix]
            inputs.require(report.get('pass') is True and report.get('variant') == variant
                           and report.get('apk_sha256') == value['sha256'], 'APK code/resource report is misbound')
        actual[variant] = value
    return actual


def verify_suite_scope(name, report):
    if name == 'engine':
        # The unchanged EngineParityTests report uses these exact scope/selection
        # fields rather than emitting an androidRuntime field. Do not generalize
        # that omission to other suites, or accept a contradictory explicit flag.
        inputs.require(report.get('scope') == 'Original selected DEX / recovered Java / rebuilt DEX, with controlled Android/action/store/clock/thread boundaries; not Android runtime'
                       and report.get('selection') == 'all'
                       and ('androidRuntime' not in report or report['androidRuntime'] is False),
                       'Engine report changed its exact host scope or selection')
    else:
        inputs.require(report.get('androidRuntime') is False, 'Suite omitted its explicit host-only runtime flag: ' + name)


def verify_registry_and_partition(project, pins, apk, reports, artifacts):
    registry = inputs.read_json(inputs.regular(project, 'source/java-method-map.json'))
    keys = [row['target'] + '->' + row['method'] for row in registry]
    inputs.require(len(keys) == len(set(keys)) == pins['registered_methods']
                   and len({row['target'] for row in registry}) == pins['target_classes'], 'Registry count, class count, or uniqueness differs')
    fixture = inputs.identity(inputs.regular(project, 'tests/fixtures/original-methods.dex'))
    inputs.require(fixture == pins['fixture'], 'Test-only original fixture differs')
    provenance = inputs.read_json(inputs.regular(project, 'tests/fixtures/provenance.json'))
    for key, expected in [('methods', pins['fixture_methods']), ('classes', pins['fixture_classes']),
                          ('registered_methods', pins['registered_methods']), ('dependency_methods', 3)]:
        count(provenance.get(key), expected, 'Fixture registration/dependency credit differs')
    inputs.require(provenance.get('original_apk_sha256') == pins['original_apk_sha256']
                   and provenance.get('fixture_sha256') == fixture['sha256'], 'Fixture provenance differs')
    all_path = reports['java-all-path-parity.json']
    flags(all_path, {'passed': True, 'schemaValid': True, 'androidRuntime': False,
                     'exactMethodKeyPartitionVerified': True, 'rebuiltDexComparedToApk': True}, 'All-path host report is incomplete')
    for key, expected in [('cases', pins['all_cases']), ('methodsCovered', 1243), ('methodsExpected', 1243),
                          ('paths', 3), ('failedCases', 0), ('unsupportedExecutions', 0)]:
        count(all_path.get(key), expected, 'All-path count differs: ' + key)
    inputs.require(all_path.get('suiteCases') == pins['suite_cases'] and all_path.get('apkSha256') == apk
                   and all_path.get('fixtureSha256') == fixture['sha256'], 'All-path source/APK or case partition differs')
    suites, flat = {}, []
    for name, stem in [('legacy', 'java'), ('core', 'java-core'), ('environment', 'java-environment'), ('engine', 'java-engine'), ('ui', 'java-ui')]:
        report = artifacts.json(f'reports/{stem}-three-path-parity.json')
        count(report.get('cases'), pins['suite_cases'][name], 'Suite case count differs: ' + name)
        count(report.get('paths'), 3, 'Suite did not execute all three paths')
        count(report.get('failedCases', report.get('failures')), 0, 'Suite has failures')
        count(report.get('unsupportedExecutions'), 0, 'Suite has unsupported execution')
        verify_suite_scope(name, report)
        inputs.require(report.get('passed', report.get('pass')) is True
                       and report.get('fixture_sha256') == fixture['sha256'] and report.get('rebuilt_apk_sha256') == apk
                       and report.get('rebuilt_dex_compared_to_apk') is True, 'Suite identity or scoped result differs')
        selected = report.get('methodKeys')
        inputs.require(isinstance(selected, list) and all(isinstance(key, str) for key in selected)
                       and len(selected) == len(set(selected)), 'Suite method inventory is invalid')
        count(report.get('methodsCovered'), len(selected), 'Suite method count differs from its inventory')
        flat += selected
        suites[name] = report
    inputs.require(len(flat) == len(set(flat)) == 1243 and set(flat) == set(keys), 'Executed method keys do not exactly partition the registry')
    hybrid = reports['hybrid-roundtrip.json']
    changed = [row[0] + '->' + row[1] for row in hybrid.get('changed_methods', [])]
    inputs.require(len(changed) == len(set(changed)) == 1243 and set(changed) == set(keys)
                   and len(hybrid.get('changed_classes', [])) == 605
                   and set(hybrid.get('changed_classes', [])) == {row['target'] for row in registry}, 'Signed APK change inventory differs from the registered source delta')
    for report in (hybrid, reports['baseline-roundtrip.json']):
        for field in ('baseline_source_hash_mismatches', 'missing', 'extra', 'unexpected_changed_methods',
                      'omitted_registered_changes', 'altered_opaque_payload', 'misaligned'):
            inputs.require(report.get(field) == [], 'Code roundtrip has an unexplained difference: ' + field)
        count(report.get('classes_compared'), 71267, 'Code roundtrip omitted classes')
        count(report.get('methods_total'), 349972, 'Code roundtrip omitted methods')
    inputs.require(reports['baseline-roundtrip.json'].get('changed_methods') == []
                   and reports['baseline-roundtrip.json'].get('changed_classes') == [], 'Baseline code changed')
    return suites


def retain_class(project, relative_path, output, retained):
    path = inputs.regular(project, relative_path)
    value = inputs.identity(path)
    if relative_path in retained:
        inputs.require(retained[relative_path]['identity'] == value, 'A retained runtime class changed')
        return
    target = output / 'runtime-classes' / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as stream:
        stream.write(path.read_bytes())
    inputs.require(inputs.identity(target) == value, 'Retained runtime class bytes differ')
    retained[relative_path] = {'source_path': relative_path,
                               'retained_path': target.relative_to(output).as_posix(), 'identity': value}


def verify_ui_controls(project, pins, report, ui, artifacts, output, retained):
    flags(report, {'pass': True, 'positiveRestorationPassed': True, 'positiveRestorationExactBaseline': True,
                   'sourceFixtureAndApkUnchanged': True, 'dayNumericDexControlsPassed': True, 'androidRuntime': False},
          'UI fault controls or exact restoration did not pass')
    inputs.require(report.get('status') == 'ALL_91_JAVA_AND_TWO_NUMERIC_DEX_FAULTS_DETECTED_EXACT_POSITIVE_RESTORED', 'UI control completion status differs')
    for name in ('expectedControlCount', 'controlsCount'):
        count(report.get(name), 91, 'UI fault control count differs')
    count(report.get('restorationCases'), 24465, 'UI restoration omitted cases')
    rows, wanted = report.get('controls'), pins['ui_mutation_inventory']
    inputs.require(isinstance(rows, list) and len(rows) == 91
                   and [row.get('mutation') for row in rows] == [row['name'] for row in wanted], 'UI fault inventory or order differs')
    fixed = ('cases', 'paths', 'methodsCovered', 'methodKeys', 'methods', 'instructionCoverage',
             'independentExpectedResultChecks', 'expectedResultFailures', 'unsupportedExecutions',
             'dayNumericRecoveredMethods', 'dayNumericOriginalDependencyMethods', 'dayNumericOriginalDependencyKeys',
             'dayNumericInputInventorySha256', 'dayNumericOriginalCoverage')
    baseline = artifacts.json('reports/ui-negative-baseline.json')
    restored = artifacts.json('reports/ui-positive-restoration.json')
    stripped = {key: value for key, value in ui.items() if key not in ('fixture_sha256', 'rebuilt_apk_sha256', 'rebuilt_dex_compared_to_apk')}
    inputs.require(baseline == restored == stripped and baseline.get('passed') is True, 'Full positive UI restoration differs from the final actual suite')
    artifacts.hash('reports/java-ui-three-path-parity.json', report['positiveBaselineSha256'])
    checks = []
    for row, expected in zip(rows, wanted):
        name = expected['name']
        stem = Path(expected['source']).stem
        source_name = f'reports/ui-mutants/{name}/{stem}.java'
        class_name = f'reports/ui-mutants/{name}/{stem}.class'
        inputs.require(row.get('retainedSource') == source_name and row.get('retainedClass') == class_name
                       and row.get('requiredCases') == expected['required_cases'] and row.get('requiredCase') == expected['required_cases'][0],
                       'UI mutation changed retained artifact or required case identities')
        flags(row, {'pass': True, 'requiredCaseRejected': True, 'sourceFixtureAndApkUnchanged': True,
                    'originalCoverageAndInventoryUnchanged': True}, 'UI fault is incomplete')
        count(row.get('exitCode'), 2, 'UI fault did not produce the expected rejection exit')
        count(row.get('unsupportedExecutions'), 0, 'UI fault used unsupported execution')
        inputs.require(type(row.get('failedCases')) is int and row['failedCases'] > 0, 'UI fault has no actual failures')
        artifacts.hash(source_name, expected['mutant_sha256'])
        inputs.require(row.get('mutantSourceSha256') == expected['mutant_sha256'], 'UI mutant source differs from the frozen compiled-control selection')
        artifacts.hash(class_name, row['mutantClassSha256'])
        positive_name = f'build/java/hostclasses/recovered/ui/{stem}.class'
        positive = inputs.identity(inputs.regular(project, positive_name))
        inputs.require(row.get('positiveClassSha256') == positive['sha256'] != row['mutantClassSha256'], 'UI fault did not use a distinct class from the final positive compilation')
        retain_class(project, positive_name, output, retained)
        negative = artifacts.json('reports/' + name + '-negative-failures.json')
        flags(negative, {'passed': False, 'androidRuntime': False}, 'UI negative result reports success')
        count(negative.get('failedCases'), row['failedCases'], 'UI negative failure count differs')
        inputs.require(all(negative.get(key) == baseline[key] for key in fixed)
                       and set(expected['required_cases']).issubset(negative.get('failedCaseLabels', [])), 'UI negative evidence changed the original coverage, input inventory, or required failures')
        checks.append({'mutation': name, 'failed_cases': row['failedCases'], 'source': source_name,
                       'class': class_name, 'source_sha256': expected['mutant_sha256'], 'class_sha256': row['mutantClassSha256']})
    return checks


def verify_numeric_commands(report, folder, artifacts):
    expected = []
    def pipeline(name):
        expected.extend((name, label, 0) for label in ('d8-helper', 'disassemble-helper', 'assemble-target'))
    pipeline('positive-pipeline')
    expected.extend([('', 'signed-apk-instructions', 0), ('', 'positive-transplant-instructions', 0), ('positive', 'execute', 0)])
    for name in ('integer-zero', 'decimal-zero'):
        pipeline(name + '-pipeline')
        expected.append((name + '-dex-fault', 'execute', 3))
    expected += [('original-as-rebuilt-rejected', 'execute', 1), ('wrong-helper-class-rejected', 'execute', 1), ('positive-restoration', 'execute', 0)]
    commands = report.get('commands')
    inputs.require(isinstance(commands, list) and len(commands) == len(expected) == 17, 'Numeric actual command inventory differs')
    previous_end = epoch_ns(report['started_utc'])
    inputs.require(artifacts.started_ns <= previous_end, 'Numeric commands predate acceptance')
    for row, (subdir, label, code) in zip(commands, expected):
        inputs.require(row.get('name') == label, 'Numeric command order differs')
        count(row.get('returncode'), code, 'Numeric actual subprocess outcome differs')
        count(row.get('timeout_seconds'), 120, 'Numeric child timeout differs')
        start, end = epoch_ns(row.get('started_utc')), epoch_ns(row.get('ended_utc'))
        inputs.require(previous_end <= start <= end <= artifacts.ended_ns, 'Numeric subprocess chronology differs')
        previous_end = end
        inputs.require(type(row.get('duration_seconds')) in (int, float) and math.isfinite(row['duration_seconds'])
                       and row['duration_seconds'] >= 0 and isinstance(row.get('argv'), list) and row['argv'],
                       'Numeric subprocess lacks an actual bounded invocation')
        prefix = folder + ('/' + subdir if subdir else '')
        for stream in ('stdout', 'stderr'):
            name = prefix + '/' + label + '.' + stream + '.log'
            value = row.get(stream, {})
            inputs.require(value.get('path') == name, 'Numeric subprocess reused another stream')
            artifacts.hash(name, value['sha256'])
            count(artifacts.rows[name]['bytes'], value['bytes'], 'Numeric stream length differs')
    inputs.require(previous_end <= epoch_ns(report.get('finished_utc')) <= artifacts.ended_ns, 'Numeric completion time differs')


def verify_numeric(project, pins, apk, ui, controls, report, artifacts, output, retained):
    # Import only after the independent full input scan, which binds these exact
    # validators to the published nineteen-file delta and immutable baseline.
    sys.path.insert(0, str(project))
    import day_numeric_dex_controls as numeric
    import ui_mutation_catalog as catalog
    flags(report, {'passed': True, 'androidRuntime': False, 'positive_signed_apk_instruction_match': True,
                   'positive_restoration_byte_exact': True, 'source_class_fixture_and_apk_unchanged': True},
          'Numeric signed-D8 acceptance is incomplete')
    inputs.require(report.get('status') == 'TWO_ACTUAL_NUMERIC_DEX_FAULTS_DETECTED_SIGNED_POSITIVE_RESTORED'
                   and report.get('signed_apk_sha256') == apk and report.get('original_fixture_sha256') == pins['fixture']['sha256']
                   and report.get('input_inventory_sha256') == catalog.DAY_INPUT_INVENTORY_SHA256, 'Numeric acceptance identity differs')
    for key, expected in [('schema', 1), ('primary_recovered_methods', 1), ('original_dependency_methods', 3),
                          ('expected_java_faults', 13), ('expected_actual_dex_faults', 2), ('provenance_controls_rejected', 2),
                          ('cases', 1291), ('execution_paths', 3), ('original_instruction_count', 32),
                          ('rebuilt_instruction_count', 25), ('conditional_edges_per_path', 4)]:
        count(report.get(key), expected, 'Numeric acceptance count differs: ' + key)
    artifacts.hash('reports/day-numeric-dex-controls.json', controls['dayNumericDexControlsSha256'])
    folder = report.get('evidence_directory')
    inputs.require(isinstance(folder, str) and re.fullmatch(r'reports/day-numeric-dex-[A-Za-z0-9_]+', folder), 'Numeric evidence directory differs')
    verify_numeric_commands(report, folder, artifacts)
    inputs.require(report.get('positive_pipeline') == pins['numeric_positive_pipeline'], 'Fresh numeric production transplant differs from the reviewed pipeline')
    inputs.require(artifacts.json(folder + '/positive-pipeline/method-body-binding.json') == pins['numeric_positive_pipeline'],
                   'Positive method-body binding differs')
    artifacts.hash(folder + '/positive-pipeline/numeric-target.dex', pins['numeric_positive_pipeline']['target_dex_sha256'])
    inputs.require(artifacts.raw(folder + '/signed-apk-instructions.json') == artifacts.raw(folder + '/positive-transplant-instructions.json'),
                   'Actual signed-method instructions differ from the positive transplant')
    positive = artifacts.json(folder + '/positive/result.json')
    restoration = artifacts.json(folder + '/positive-restoration/result.json')
    numeric.validate_positive(positive)
    numeric.validate_positive(restoration)
    inputs.require(positive == restoration and artifacts.raw(folder + '/positive/result.json') == artifacts.raw(folder + '/positive-restoration/result.json'),
                   'Numeric raw positive restoration is not byte-exact')
    cfg = artifacts.json(folder + '/positive/config.json')
    inputs.require(positive.get('inputIdentities') == cfg and positive.get('loadedClassOrigins') == cfg.get('classPins'),
                   'Numeric positive raw input/class origins differ from its actual invocation')
    inputs.require(artifacts.json(folder + '/positive-restoration/config.json') == cfg, 'Restoration used different positive inputs')
    for field, name, digest in [
        ('originalFixture', 'tests/fixtures/original-methods.dex', pins['fixture']['sha256']),
        ('rebuiltApk', 'dist/MacroDroid-5.67.8-v9-hybrid.apk', apk),
        ('targetDex', folder + '/positive-pipeline/numeric-target.dex', pins['numeric_positive_pipeline']['target_dex_sha256'])]:
        inputs.require(cfg.get(field) == {'path': str(project / name), 'sha256': digest}, 'Numeric positive input role differs: ' + field)
    getter = inputs.regular(project, 'build/hybrid/classes3.dex')
    getter_hash = inputs.identity(getter)['sha256']
    inputs.require(cfg.get('rebuiltGetterDex') == {'path': str(getter), 'sha256': getter_hash, 'apk_member': 'classes3.dex'}, 'Getter DEX role differs')
    with zipfile.ZipFile(inputs.regular(project, 'dist/MacroDroid-5.67.8-v9-hybrid.apk')) as archive:
        inputs.require(archive.namelist().count('classes3.dex') == 1, 'Signed APK getter partition is not unique')
        with archive.open('classes3.dex') as stream:
            signed_getter_hash = hashlib.file_digest(stream, 'sha256').hexdigest()
    inputs.require(getter_hash == signed_getter_hash, 'The three getter bodies were not read from the actual signed APK partition')
    current_pins = numeric.class_pins(project / 'build/java/hostclasses', project / 'tools/classes')
    inputs.require(cfg.get('classPins') == current_pins and len(current_pins) == 23, 'Actual 23-class numeric runtime inventory differs')
    for value in current_pins.values():
        name = Path(value['path']).relative_to(project).as_posix()
        inputs.require(inputs.identity(inputs.regular(project, name))['sha256'] == value['sha256'], 'Loaded numeric class bytes differ')
        retain_class(project, name, output, retained)
    faults = report.get('actual_dex_faults')
    inputs.require(isinstance(faults, list) and [row.get('name') for row in faults] == ['integer-zero', 'decimal-zero'], 'Actual numeric DEX fault inventory differs')
    jobs = {row['name'].removeprefix('day-numeric-'): row for row in catalog.load_day_mutations(project)}
    for row in faults:
        name = row['name']
        flags(row, {'passed': True}, 'An actual numeric DEX fault was not rejected')
        count(row.get('mismatches'), numeric.JAVA_FAILURE_COUNTS[name], 'Numeric DEX fault failure count differs')
        inputs.require(row.get('required_cases') == jobs[name]['required_cases'], 'Numeric DEX fault required cases differ')
        bad = artifacts.json(folder + '/' + name + '-dex-fault/result.json')
        numeric.validate_fault(positive, bad, jobs[name]['required_cases'], numeric.JAVA_FAILURE_COUNTS[name], 'rebuilt')
        bad_cfg = artifacts.json(folder + '/' + name + '-dex-fault/config.json')
        inputs.require(bad.get('inputIdentities') == bad_cfg and bad.get('loadedClassOrigins') == cfg['classPins'], 'Numeric DEX fault origins differ')
        wanted = dict(cfg)
        wanted['targetDex'] = {'path': str(project / folder / (name + '-pipeline/numeric-target.dex')), 'sha256': row['pipeline']['target_dex_sha256']}
        inputs.require(bad_cfg == wanted and row['pipeline'] == artifacts.json(folder + '/' + name + '-pipeline/method-body-binding.json'), 'Numeric fault changed another input or its production binding')
        artifacts.hash(folder + '/' + name + '-pipeline/numeric-target.dex', row['pipeline']['target_dex_sha256'])
    for name, expected_error in [('original-as-rebuilt-rejected', 'Original fixture cannot masquerade as rebuilt target'),
                                  ('wrong-helper-class-rejected', 'Wrong input identity: class recovered.ui.DayTriggerValueMethods')]:
        inputs.require(not (project / folder / name / 'result.json').exists()
                       and expected_error in artifacts.raw(folder + '/' + name + '/execute.stderr.log').decode(),
                       'Numeric provenance control did not reject for the required reason')
    _, bindings = numeric.validate_java_controls(project, controls['controls'])
    inputs.require(report.get('java_fault_bindings') == bindings and len(bindings) == 13, 'Numeric Java-control source/class binding differs')
    for key, wanted in [('dayNumericRecoveredMethods', 1), ('dayNumericOriginalDependencyMethods', 3)]:
        count(ui.get(key), wanted, 'UI numeric method/dependency credit differs')
    inputs.require(ui.get('dayNumericOriginalDependencyKeys') == sorted(numeric.GETTERS)
                   and ui.get('dayNumericInputInventorySha256') == catalog.DAY_INPUT_INVENTORY_SHA256
                   and ui.get('dayNumericInstructionAndConditionalCoverage') is True, 'UI numeric original coverage is incomplete')
    numeric.validate_positive_coverage(ui['dayNumericOriginalCoverage'], 32)
    numeric.validate_positive_coverage(ui['dayNumericRebuiltCoverage'], 25)
    return {'cases': 1291, 'paths': 3, 'original_instructions': 32, 'rebuilt_instructions': 25,
            'conditional_edges_per_path': 4, 'java_faults': 13, 'actual_dex_faults': 2,
            'uncredited_original_getters': 3, 'actual_command_streams_checked': 34,
            'signed_positive_instruction_bytes_equal': True, 'exact_positive_restoration': True,
            'loaded_runtime_classes': 23}


def verify_other_gates(reports, apk):
    for name in ('baseline-resource-parity.json', 'hybrid-resource-parity.json'):
        row = reports[name]
        for field in ('changed_files', 'missing_files', 'extra_files', 'changed_resource_ids', 'missing_resource_names',
                      'extra_resource_names', 'missing_apk_entries', 'extra_apk_entries', 'changed_zip_compression_methods',
                      'public_resource_visibility_changes'):
            inputs.require(row.get(field) == [], 'Resource parity has unexplained differences: ' + field)
        for field, expected in [('files_expected', 7212), ('files_actual', 7212), ('byte_identical', 7211),
                                 ('resource_ids_expected', 23854), ('resource_ids_actual', 23854)]:
            count(row.get(field), expected, 'Resource inventory count differs')
        inputs.require(row.get('equivalent_enum_order_only') == ['res/values/attrs.xml']
                       and len(row.get('native_libraries', [])) == 22
                       and all(value.get('pass') is True and value.get('original_bytes_preserved') is True for value in row['native_libraries']),
                       'Declared resource/native equivalence scope differs')
    for name, field in [('migration-static-proof.json', 'methods_registered'), ('migration-linkage-check.json', 'registered_methods')]:
        row = reports[name]
        flags(row, {'pass': True}, 'Migration static/linkage gate did not pass')
        count(row.get(field), 1243, 'Static/linkage gate omitted the numeric method')
        inputs.require(row.get('errors') == [], 'Static/linkage gate contains errors')
    for name, key, cases in [('oracle-semantics.json', 'pass', 2458), ('engine-oracle-semantics.json', 'pass', 4145),
                             ('ui-oracle-semantics.json', 'passed', 6270), ('constructor-oracle-conformance.json', 'passed', 16),
                             ('widget-bitwise-oracle-conformance.json', 'passed', 4546)]:
        row = reports[name]
        flags(row, {key: True, 'androidRuntime': False}, 'An independent host oracle conformance failed')
        count(row.get('cases'), cases, 'Host oracle conformance inventory differs')
    for name, count_wanted in [('engine-negative-controls.json', 4), ('core-negative-controls.json', 2), ('environment-negative-controls.json', 3)]:
        row = reports[name]
        flags(row, {'pass': True, 'positiveRestorationPassed': True, 'androidRuntime': False}, 'An existing fault/restoration gate failed')
        inputs.require(isinstance(row.get('controls'), list) and len(row['controls']) == count_wanted
                       and all(value.get('pass') is True and type(value.get('failedCases')) is int and value['failedCases'] > 0
                               and value.get('unsupportedExecutions') == 0 for value in row['controls']), 'Existing fault inventory is incomplete')
    legacy = reports['negative-control.json']
    flags(legacy, {'pass': True, 'source_and_apk_mutated': False}, 'Legacy negative control failed')
    count(legacy.get('exit_code'), 2, 'Legacy negative control had another outcome')
    count(legacy.get('failed_vectors'), 1110, 'Legacy negative case inventory differs')
    edited = reports['full-apk-edit-probe.json']
    flags(edited, {'pass': True, 'experimental_apk_not_distributed': True, 'release_inputs_and_apk_unchanged': True,
                   'required_pause_case_rejected': True, 'android_runtime_executed': False}, 'Actual signed source-edit probe did not pass')
    inputs.require(edited.get('original_release_apk_sha256') == apk
                   and edited.get('changed_non_signature_entries') == ['classes3.dex']
                   and edited.get('changed_classes') == ['Lcom/arlosoft/macrodroid/macro/Macro;']
                   and edited.get('changed_methods') == ['invokeActions(Ljava/util/List;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;)V'], 'Signed source-edit probe changed another scope')
    count(edited.get('negative_exit_code'), 1, 'Signed source-edit negative process outcome differs')
    count(edited.get('negative_failed_cases'), 113, 'Signed source-edit negative cases differ')
    count(edited.get('unsupported_executions'), 0, 'Signed source-edit used unsupported execution')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-repository', type=Path, required=True)
    parser.add_argument('--overlay-repository', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--runtime-manifest-sha256', required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    inputs.require(not output.is_symlink() and not any(output.is_relative_to(path.resolve()) for path in
                   (args.baseline_repository, args.overlay_repository, Path(__file__).resolve().parents[2])), 'Invalid proof output directory')
    output.mkdir(parents=True, exist_ok=True)
    result = {'schema': 1, 'status': 'WIP_FULL_HOST_ACCEPTANCE_NOT_ESTABLISHED', 'passed': False,
              'started_utc': datetime.now(timezone.utc).isoformat(), 'active_promoted': False,
              'android_runtime_executed': False, 'full_runtime_1_to_1_established': False,
              'complete_high_level_java_kotlin_source': False}
    artifacts = None
    retained = {}
    try:
        runtime = inputs.verify_runtime_manifest(args.runtime_manifest_sha256)
        pins, _, future, _ = inputs.contract(args.baseline_repository, args.overlay_repository)
        inputs.verify_git_commit(args.baseline_repository, pins['baseline_commit'])
        inputs.verify_git_commit(args.overlay_repository, pins['overlay_commit'])
        prepared_path = inputs.regular(output, 'preparation.json')
        prepared = inputs.read_json(prepared_path)
        inputs.require(prepared.get('passed') is True and prepared.get('status') == 'EXACT_19_FILE_WIP_PREPARED'
                       and prepared.get('output') == str(output) and prepared.get('runtime_source') == runtime,
                       'The exact preparation proof is absent')
        project = Path(prepared['project'])
        execution_path = inputs.regular(output, 'execution.json')
        execution = inputs.read_json(execution_path)
        inputs.require(execution.get('preparation_sha256') == inputs.identity(prepared_path)['sha256'], 'Preparation changed after execution began')
        start, end = verify_execution(execution, prepared, pins)
        result['actual_acceptance_execution'] = execution['execution']
        for stream in ('stdout', 'stderr'):
            row = execution['execution'][stream]
            inputs.checked_identity(output, row['path'], {k: row[k] for k in ('bytes', 'sha256')})
        inputs.compare_inputs(inputs.scan_inputs(project), future)
        inputs.checked_identity(project, 'reports/release-input-snapshot.json', pins['future_manifest'])
        inputs.require(inputs.read_json(project / 'reports/release-input-snapshot.json') == future, 'Acceptance manifest differs from independent complete derivation')
        artifacts = Artifacts(project, start, end)
        latest = artifacts.json('reports/acceptance-latest.json')
        reports = verify_gates(latest, execution, pins, artifacts)
        apks = verify_apks(latest, pins, artifacts, reports)
        suites = verify_registry_and_partition(project, pins, apks['hybrid']['sha256'], reports, artifacts)
        python = verify_python(artifacts.raw('reports/python-unit-tests.log'), pins['python_tests'])
        ui_checks = verify_ui_controls(project, pins, reports['ui-negative-controls.json'], suites['ui'], artifacts, output, retained)
        numeric = verify_numeric(project, pins, apks['hybrid']['sha256'], suites['ui'], reports['ui-negative-controls.json'],
                                 reports['day-numeric-dex-controls.json'], artifacts, output, retained)
        verify_other_gates(reports, apks['hybrid']['sha256'])
        staging = artifacts.json('reports/java-staging.json')
        flags(staging, {'published_after_all_compiler_commands': True}, 'Fresh Java/D8 generation was not published atomically')
        inputs.require(staging.get('published_directory') == 'build/java', 'Unexpected Java generation destination')
        # The complete actual reports/dist inventory is retained, even beyond the
        # required gate subset. No stale file, symlink or alias is accepted here.
        for directory in ('reports', 'dist'):
            for path in sorted((project / directory).rglob('*')):
                inputs.require(not path.is_symlink(), 'Symlink in produced evidence')
                if path.is_file() and path != project / 'reports/release-input-snapshot.json':
                    artifacts.path(path.relative_to(project).as_posix())
        inputs.compare_inputs(inputs.scan_inputs(project), future)
        result.update(status='ISOLATED_DAY_NUMERIC_ALL_16_HOST_GATES_VERIFIED', passed=True,
                      source_snapshot=pins['future_snapshot'], future_manifest=pins['future_manifest'],
                      baseline_commit=pins['baseline_commit'], source_overlay_commit=pins['overlay_commit'],
                      overlay_checkpoint=pins['overlay_checkpoint'], gates_verified=16, fresh_reports_verified=23,
                      actual_cases=194780, registered_methods=1243, target_classes=605,
                      fixture_methods=1246, fixture_classes=607, uncredited_original_dependencies=3,
                      suite_cases=pins['suite_cases'], python=python, actual_ui_java_controls=91,
                      all_ui_mutant_checks=ui_checks, numeric=numeric, apks=apks,
                      source_edit_signed_apk_probe_verified=True,
                      candidate_is_wip_only=True, android_probe_status=latest.get('android_status'))
        return 0
    except Exception as error:
        result['error'] = repr(error)
        print('WIP VERIFICATION FAILED:', error, file=sys.stderr)
        return 2
    finally:
        result['retained_runtime_classes'] = sorted(retained.values(), key=lambda row: row['source_path'])
        result['verified_output_artifacts'] = sorted(artifacts.rows.values(), key=lambda row: row['path']) if artifacts else []
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        inputs.write_json(output / 'verification.json', result)
        print(result['status'], flush=True)


if __name__ == '__main__':
    sys.exit(main())
