#!/usr/bin/env python3
"""Freeze the failed integration pin, exact diagnosis and measured replacement.

Only completed private reports are linked. No active source or build input changes.
"""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
REPORTS = BASE / 'reports'
FAILED = REPORTS / '02-targeted-numeric-attempt-01'
DIAGNOSIS = REPORTS / '03-helper-metadata-diagnosis'
PASSED = REPORTS / '04-targeted-numeric-attempt-02'
OUT = BASE / 'checkpoints/03-targeted-numeric-integration'


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def link_tree(source, destination):
    for path in sorted(source.rglob('*')):
        if path.is_symlink():
            raise RuntimeError('Unexpected report symlink: ' + str(path))
        if path.is_file():
            target = destination / path.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(path, target)


def load(path):
    return json.loads(path.read_text())


def main():
    failed, diagnosis, good = [load(path / 'result.json') for path in (FAILED, DIAGNOSIS, PASSED)]
    assert failed['passed'] is False and failed['error'] == 'AssertionError()'
    assert len(failed['commands']) == 1 and failed['commands'][0]['returncode'] == 0
    assert diagnosis['passed'] is True and diagnosis['complete_difference_accounted_for'] is True
    assert diagnosis['constant_pool_byte_identity'] is True
    assert diagnosis['all_fields_methods_attributes_byte_identity'] is True
    assert diagnosis['changed_byte_offsets'] == [806, 814, 822]
    assert good['passed'] is True and good['status'] == 'TARGETED_NUMERIC_INTEGRATION_THREE_PATH_CONTROLS_PASSED'
    assert good['ui_positive_and_91_controls_pending'] is True and good['full_signed_build_and_16_gates_pending'] is True
    assert good['signed_numeric_primary_packaging_verified'] is False
    assert good['active_paths_changed'] == [] and good['full_source_copy'] is False and good['app_build_started'] is False
    assert good['recovered_methods'] == good['original_fixture_registered_methods'] == 1243
    assert good['registered_classes'] == 605 and good['original_fixture_methods'] == 1246
    assert good['original_fixture_classes'] == 607 and good['original_fixture_dependencies'] == 3
    assert good['old_fixture_recreated_byte_exact'] is True and good['existing_classpath_files_unchanged'] == 912
    assert len(good['commands']) == 45
    verified_streams = 0
    for root, report in [(FAILED, failed), (PASSED, good)]:
        seen = set()
        for command in report['commands']:
            assert command['timeout_seconds'] == 120 and command['returncode'] is not None
            for name in ('stdout', 'stderr'):
                row = command[name]
                assert row['path'] not in seen
                seen.add(row['path'])
                assert identity(root / row['path']) == {k: row[k] for k in ('bytes', 'sha256')}
                verified_streams += 1
    for name, command in zip(('reviewed', 'integrated'), diagnosis['commands']):
        assert command['returncode'] == 0 and command['timeout_seconds'] == 30
        for stream in ('stdout', 'stderr'):
            assert identity(DIAGNOSIS / (name + '.' + stream + '.log'))['sha256'] == command[stream + '_sha256']
            verified_streams += 1
    assert verified_streams == 96

    # Replay the exact validator bytes used by the closed successful attempt.
    sys.path[:0] = [str(PASSED / 'inputs/project'), str(PASSED / 'inputs/production')]
    spec = importlib.util.spec_from_file_location('frozen_numeric', PASSED / 'inputs/project/day_numeric_dex_controls.py')
    numeric = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(numeric)
    positive = load(PASSED / 'positive/result.json')
    numeric.validate_positive(positive)
    java_rows = good['java_faults']
    assert len(java_rows) == 13 and {r['name'] for r in java_rows} == set(numeric.JAVA_FAILURE_COUNTS)
    for row in java_rows:
        name = row['name']
        assert row['passed'] is True and row['mismatches'] == numeric.JAVA_FAILURE_COUNTS[name]
        source = PASSED / ('java-fault-' + name) / 'source/recovered/ui/DayTriggerValueMethods.java'
        compiled = PASSED / ('java-fault-' + name) / 'classes/recovered/ui/DayTriggerValueMethods.class'
        assert identity(source) == row['source'] and identity(compiled) == row['class']
        fault = load(PASSED / ('java-fault-' + name + '-observation') / 'result.json')
        numeric.validate_fault(positive, fault, row['required_cases'], row['mismatches'], 'java')
    dex_rows = good['actual_dex_faults']
    assert [row['name'] for row in dex_rows] == ['integer-zero', 'decimal-zero']
    required = {row['name']: row['required_cases'] for row in java_rows}
    for row in dex_rows:
        name = row['name']
        assert row['passed'] is True
        assert row['pipeline'] == load(PASSED / (name + '-pipeline') / 'method-body-binding.json')
        assert identity(PASSED / (name + '-pipeline/numeric-target.dex'))['sha256'] == row['pipeline']['target_dex_sha256']
        numeric.validate_fault(positive, load(PASSED / (name + '-dex-fault/result.json')),
                               required[name], numeric.JAVA_FAILURE_COUNTS[name], 'rebuilt')
    assert (PASSED / 'positive/result.json').read_bytes() == (PASSED / 'positive-restoration/result.json').read_bytes()
    assert good['provenance_controls_rejected'] == 2
    for folder, reason in [('original-as-rebuilt-rejected', 'Original fixture cannot masquerade as rebuilt target'),
                           ('wrong-helper-class-rejected', 'Wrong input identity: class recovered.ui.DayTriggerValueMethods')]:
        assert not (PASSED / folder / 'result.json').exists()
        assert reason in (PASSED / folder / 'execute.stderr.log').read_text()

    binding = good['positive_pipeline']
    assert binding == load(PASSED / 'positive-pipeline/method-body-binding.json')
    assert binding['helper_class']['sha256'] == '2f8b2d3769749301442dae35aca9fda5314eb1f17d59ea6310bd50be62596211'
    assert binding['target_dex_sha256'] == '867e137f65908d8360f307cdd0f23b3f910e5606d6b5916f876e85186b813b47'
    assert identity(PASSED / 'positive-pipeline/numeric-target.dex')['sha256'] == binding['target_dex_sha256']
    assert identity(PASSED / 'hostclasses/recovered/ui/DayTriggerValueMethods.class') == binding['helper_class']

    OUT.mkdir(parents=True, exist_ok=False)
    for name, source in [('failed-pin-attempt', FAILED), ('class-metadata-diagnosis', DIAGNOSIS), ('targeted-pass', PASSED)]:
        link_tree(source, OUT / 'evidence' / name)
    old_class = BASE.parent / 'day-trigger-numeric-recovery/reports/original-java-01/hostclasses/recovered/ui/DayTriggerValueMethods.class'
    assert identity(old_class)['sha256'] == diagnosis['reviewed_sha256']
    os.link(old_class, OUT / 'evidence/class-metadata-diagnosis/reviewed-helper.class')
    for name in ('freeze_targeted_numeric.py', 'run_targeted_numeric.py', 'diagnose_helper_metadata.py',
                 'CompareOriginalFixture.java', 'stage_numeric_sources.py'):
        (OUT / name).write_bytes((BASE / name).read_bytes())
    receipt = {'schema': 1, 'passed': True, 'created_utc': datetime.now(timezone.utc).isoformat(),
               'verified_command_streams': verified_streams, 'failed_attempt_commands': 1,
               'diagnostic_commands': 2, 'successful_attempt_commands': 45,
               'successful_case_inventory': 1291, 'replayed_java_faults': 13, 'replayed_actual_dex_faults': 2,
               'provenance_rejections': 2, 'positive_restoration_byte_exact': True,
               'original_fixture': good['original_fixture'], 'positive_pipeline': binding,
               'no_active_application_change': True, 'signed_primary_packaging_pending': True}
    (OUT / 'freeze-verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    (OUT / 'README.md').write_text('''# DayTrigger.r0: integrated host types and targeted three-path proof

The isolated integration passes all 1,291 exact numeric inputs through the original fixture, the Java helper and a fresh production D8/transplant. This checkpoint preserves the failed first pin, its complete diagnosis, and the successful replacement. The active application is unchanged. The full UI run, 91 Java controls in that suite, signed numeric-primary packaging and all 16 acceptance gates remain pending.

The [closed successful result](evidence/targeted-pass/result.json) ran from 08:30:37.038605 to 08:33:30.785300 UTC on 2026-10-12. Its 45 bounded commands retain exact arguments, return codes and all streams. The [freeze verification](freeze-verification.json) independently rechecks 96 streams across both attempts and the two diagnostic commands, all 1,291 positive observations, thirteen actual compiled Java faults, two actual D8/transplant faults, two provenance rejections and byte-exact positive restoration.

## The failed pin and precise replacement

The [first attempt](evidence/failed-pin-attempt/result.json) stopped after successful compilation because the helper class did not match the private-study pin. Existing active host nested classes are public and non-final; the earlier study used final nested classes. Their public fields, constructors, serialization and event contracts are retained, as already measured in the [host-contract checkpoint](../04-host-contract-regression/README.md).

The [class parser diagnosis](evidence/class-metadata-diagnosis/result.json) proves that both classfiles contain 823 bytes, with identical constant pools and identical fields/methods and their attributes. Only byte offsets 806, 814 and 822 differ: the three external `InnerClasses` access flags change from `public static final` to `public static`. Substituting only those flags reconstructs the complete integrated class. Both actual classes and both `javap` outputs are preserved. No private-study class was used as the integrated artifact.

The freshly compiled integrated helper is SHA256 `2f8b2d3769749301442dae35aca9fda5314eb1f17d59ea6310bd50be62596211`. A one-class D8 input contains no host stubs. Its freshly emitted helper DEX is `63b80e2a325efeac446cb02c2d2a8f9c3a97abd5dd312a1a3c856330cf5037df`; the [production transplant binding](evidence/targeted-pass/positive-pipeline/method-body-binding.json) yields target DEX `867e137f65908d8360f307cdd0f23b3f910e5606d6b5916f876e85186b813b47`, byte-identical to the independently verified study target. All other 33 methods and non-target class text remain exact. No constructor-owner correction is applied.

## Scope and accounting

The isolated registry contains 1,243 recovered methods in 605 target classes. Fresh fixture extraction from the pinned original APK selects 1,246 methods in 607 classes: 1,243 registered methods and exactly three separately declared original getters. Those getters earn zero recovered-method credit. The original fixture SHA256 is `6a7c7f5acc1bca7b2eab584a40d8037a2256756b7244acf9b6ba2f0880b245b4`. Reconstructing the previous fixture from this selection produces byte-identical previous fixture bytes, preserving all prior selected methods and class metadata.

The exact input inventory is `e083bc1996c5c7191bffe837fc0f30e254848a4754676ba0a8a119d23e8f6e79`: 547 integer inputs, 734 binary64 inputs and ten other/null inputs. Independent expectations use integer bit arithmetic. All 32 selected original instructions, 25 rebuilt instructions and four conditional edges per path execute. Null-entry scope compares the `NullPointerException` class while preserving every raw message; other outcomes compare their complete recorded values and exception details.

The active interpreter source remains `d91ddcd8ec3d67d41d69b8252835e747c2cad2c6d5ea898323794ceec30e6b56`. The three getter bodies are read from `classes3.dex` in the exact active signed APK `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`. The rebuilt numeric primary is a separately bound standalone transplant. This run does not claim that primary is already packaged in the signed application, and it does not execute Android scheduling, parceling or ART. All 912 existing read-only classpath files and source/APK inputs rehash unchanged.
''')
    files = [{'path': p.relative_to(OUT).as_posix(), **identity(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
    checkpoint = {'schema': 1, 'status': 'FROZEN_DAY_TARGETED_INTEGRATION_WITH_FAILED_PIN_AND_DIAGNOSIS',
                  'created_utc': datetime.now(timezone.utc).isoformat(),
                  'repo_target': 'work-in-progress/day-trigger-numeric/05-targeted-integration',
                  'active_files': [], 'files': files}
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
                      'files': len(files), 'bytes_total': sum(row['bytes'] for row in files),
                      'repo_target': checkpoint['repo_target']}, indent=2))


if __name__ == '__main__':
    main()
