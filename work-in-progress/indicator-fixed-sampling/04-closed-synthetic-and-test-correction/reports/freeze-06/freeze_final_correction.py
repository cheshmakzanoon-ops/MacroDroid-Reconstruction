#!/usr/bin/env python3
"""Freeze the closed full synthetic attempt and its test-only correction."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import stat

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'checkpoints/03-closed-synthetic-test-correction'
PARENT = ROOT / 'checkpoints/02-implemented-offline-validated'
PARENT_SHA = 'd555736471dafe7cf9c93a2d32580d76ca9cd2a1f41a4ae60fc8c68deb5cdf62'


def identity(path):
    path = Path(path)
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), str(path)
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def inventory(folder):
    rows = []
    for path in sorted(folder.rglob('*')):
        assert not path.is_symlink(), str(path)
        if path.is_file():
            rows.append({'path': path.relative_to(folder).as_posix(), **identity(path),
                         'mode': '100755' if path.stat().st_mode & 0o111 else '100644'})
    return rows


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


assert identity(PARENT / 'checkpoint.json')['sha256'] == PARENT_SHA
parent = json.loads((PARENT / 'checkpoint.json').read_text())
for row in parent['files']:
    assert identity(PARENT / row['path']) == {k: row[k] for k in ('bytes', 'sha256')}
    assert ('100755' if (PARENT / row['path']).stat().st_mode & 0o111 else '100644') == row['mode']
expected = json.loads((ROOT / 'reports/final-binding-05/required-final-source.json').read_text())
before_source = inventory(ROOT / 'source')
assert [{k: row[k] for k in ('path', 'bytes', 'sha256')} for row in before_source] == expected
assert len(before_source) == 16
full_result = json.loads((ROOT / 'reports/attempt-02/result.json').read_text())
focused_result = json.loads((ROOT / 'reports/focused-03/result.json').read_text())
binding_result = json.loads((ROOT / 'reports/final-binding-05/result.json').read_text())
assert full_result['status'] == 'FAILED' and full_result['returncode'] == 1 and full_result['timed_out'] is False
assert focused_result['status'] == 'FOCUSED_ASSERTION_CORRECTION_PASSED'
assert (focused_result['tests_run'], focused_result['failures'], focused_result['errors']) == (1, 0, 0)
assert binding_result['full_host_attempt'] == {
    'tests_run': 41, 'passed': 40, 'failed_assertions': 1,
    'timed_out': False, 'literal_status_preserved': 'FAILED'}
assert binding_result['all_production_source_and_fixed_inputs_unchanged'] is True

DEST.mkdir(parents=True, exist_ok=False)
shutil.copytree(ROOT / 'source', DEST / 'source')
for name in ('attempt-02', 'focused-03', 'final-binding-04', 'final-binding-05'):
    shutil.copytree(ROOT / 'reports' / name, DEST / 'reports' / name)
for name in ('final-binding-05.stdout', 'final-binding-05.stderr', 'final-binding-05-execution.json'):
    shutil.copy2(ROOT / 'reports' / name, DEST / 'reports' / name)
for name in ('generate_workflow.py', 'run_host_attempt.py', 'run_focused_correction.py',
             'verify_final_source_binding.py', 'freeze_final_correction.py'):
    shutil.copy2(ROOT / name, DEST / name)
shutil.copy2(ROOT / 'reports/final-binding-05/source-delta.patch', DEST / 'source-delta.patch')
shutil.copy2(ROOT / 'reports/final-binding-05/source-delta.json', DEST / 'source-delta.json')
write_json(DEST / 'proposed-source-files.json', [
    {'source': 'source/' + row['path'], 'target': row['path'],
     **{k: row[k] for k in ('bytes', 'sha256', 'mode')}} for row in before_source])
write_json(DEST / 'parent-binding.json', {
    'path': 'work-in-progress/indicator-fixed-sampling/03-implemented-offline-validation/checkpoint.json',
    **identity(PARENT / 'checkpoint.json'),
    'verified_payloads': len(parent['files']),
    'retained_first_failed_host_attempt': 'reports/attempt-01/',
    'retained_closed_offline_validation': 'reports/workflow-01/',
    'offline_result': identity(PARENT / 'reports/workflow-01/result.json'),
    'parent_unchanged': True,
    'source_delta_from_this_parent': 'source-delta.patch'})
write_json(DEST / 'evidence-reference-map.json', {
    'scope': 'Reference resolution only; original evidence bytes are unchanged.',
    'full_synthetic_baseline': 'reports/attempt-02/host-evidence/complete-synthetic-baseline/',
    'focused_case_baseline': 'reports/attempt-02/host-evidence/complete-synthetic-baseline/experiment/',
    'focused_original_annotation': '../complete-synthetic-baseline/experiment',
    'focused_annotation_note': 'The ordinary test teardown emitted this relative annotation. The focused wrapper records the exact original absolute baseline and its before/after inventories; use the frozen full_synthetic_baseline here.',
    'original_owned_root': str(ROOT),
    'recorded_metadata_note': 'Original command timestamps, inode and path records are retained literally. Copies are evidence; their new local filesystem metadata is not the metadata of the original synthetic execution.'})
write_json(DEST / 'closed-results.json', {
    'status': 'CLOSED_SYNTHETIC_ATTEMPT_WITH_FOCUSED_TEST_ASSERTION_CORRECTION',
    'full_attempt': {'result': 'reports/attempt-02/result.json',
        'literal_status': 'FAILED', 'tests_run': 41, 'successes': 40,
        'assertion_failures': 1, 'errors': 0, 'unittest_seconds': 851.940,
        'outer_seconds': full_result['duration_seconds'], 'timeout_seconds': 900,
        'timed_out': False,
        'sole_failure': 'test_changed_local_apk_identity_rejects_before_any_capture_credit',
        'actual_guard_rejection': 'Slot local APK read differs from its fixed input',
        'incorrect_test_regex': 'Local APK'},
    'focused_final_test': {'result': 'reports/focused-03/result.json',
        'tests_run': 1, 'failures': 0, 'errors': 0,
        'fresh_full_suite': False, 'reused_exact_closed_synthetic_baseline': True},
    'complete_recorder_dataset': binding_result['complete_recorder_produced_synthetic_dataset'],
    'final_binding_result': 'reports/final-binding-05/result.json',
    'preserved_binding_checker_failure': 'reports/final-binding-04/result.json',
    'only_changed_source_paths': binding_result['changed_paths'],
    'production_inputs_unchanged': True, 'timeouts_unchanged': True,
    'final_fresh_full_suite_locally_reexecuted': False,
    'hosted_full_suite_remains_required': True,
    'android_executed': False, 'new_runtime_parity_credit': 0})
(DEST / 'README.md').write_text('''# Fixed indicator sampling: closed synthetic evidence and test correction

This inactive checkpoint contains the final sixteen proposed diagnostic files, the complete closed synthetic eight-slot execution, all forty post-input frames and all ninety-two predetermined comparisons, the literal failed full-host result, and a focused correction of its sole test assertion. No application source, APK, active workflow, or Android device was changed. No new runtime parity is claimed.

## Actual host outcome

`reports/attempt-02/` retains every file from the full unittest discovery invocation. It ran **41 tests in 851.940 seconds** (852.341924428 seconds including the wrapper) within its unchanged 900-second limit. Forty tests passed. One test failed because its regular expression expected `Local APK`, while the production guard correctly rejected the altered input with `Slot local APK read differs from its fixed input`. The literal result remains **FAILED**, with no timeout and no other test error. The source and all sixteen parent inputs were unchanged across that invocation.

The actual synthetic Recorder path completed all eight fixed-order slots, forty post-input PNG/XML frames, forty full indicator arrays and all ninety-two comparisons. Its independent literal replay test passed. Each predetermined synthetic pair deliberately has one differing RGBA pixel and unequal canonical XML; none is relabeled as equal. The changed pixel is outside the retained historical indicator coordinate union, so the full-frame records demonstrate that the diagnostic retains differences outside that diagnostic region too. This is a simulated executor/clock with marker APK inputs and real parent-policy code. It is not an Android capture or an application behavior result.

The final edit changes exactly one assertion string in `test_indicator_sampling.py`. `reports/focused-03/` executes that corrected test body against the exact closed Recorder-produced baseline and unchanged verifier: one test passed. Its wrapper inventories the baseline and final source before and after. It does not repeat all forty-one tests, create a new device trace, or claim a fresh source-preparation result. The future hosted workflow still runs full unittest discovery. The focused test teardown's inherited relative baseline annotation is preserved literally; `evidence-reference-map.json` maps it to the complete baseline included here.

## Source and workflow binding

Only the test file and its two generated bindings differ from the previous implemented checkpoint: `runtime-files.json` and the workflow's test metadata entry. `source-delta.patch` and `source-delta.json` show the complete difference; all recorder, verifier, preparation, protocol, radio helper, XML fixtures, AAPT2 and application pins are unchanged. The workflow's timeouts, order, inputs, capture count and comparison rules are unchanged.

The first read-only final-binding checker wrongly assumed that only the test SHA changed in the workflow metadata, forgetting its byte count. Its failed assumption and exact checker source are retained under `reports/final-binding-04/`; the original tool stderr was not separately captured. The corrected checker verifies replacement of the complete exact test metadata entry and otherwise identical workflow bytes. Its passed result, source, raw streams and execution receipt are retained under `reports/final-binding-05/` and the adjacent files.

The earlier `d5557364…` checkpoint remains unchanged. It preserves the first fixture-import error and correction plus the closed offline workflow validation: twelve retained shell/help/owned-cleanup commands, complete sixteen-file own inventory, all forty fetched parent/part identities, and read-only full ZIP/CRC/AAPT2 checks of the exact original and 5f635e16… candidate. `parent-binding.json` gives that capsule and offline-result identities. The final source changes do not alter those application or parent inputs. The separately frozen `fccc817b…` design and `effbce44…` incomplete draft remain historical inputs.

## Review and publication

`proposed-source-files.json` lists all sixteen proposed paths with exact bytes, SHA256 and Git mode. They are reviewable proposed files, and `active_files` remains empty in this checkpoint. Activation and actual Android execution require the separate closed source/workflow review. All copied evidence preserves its original serialized timestamps, file identities and raw bytes; extracted copies do not claim to retain the original host's inode or ctime values.
''')

assert inventory(ROOT / 'source') == before_source
assert inventory(DEST / 'source') == before_source
for row in parent['files']:
    assert identity(PARENT / row['path']) == {k: row[k] for k in ('bytes', 'sha256')}
files = inventory(DEST)
checkpoint = {
    'schema': 1, 'kind': 'INACTIVE_INDICATOR_CLOSED_SYNTHETIC_AND_FOCUSED_TEST_CORRECTION',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'target': 'work-in-progress/indicator-fixed-sampling/04-closed-synthetic-and-test-correction',
    'parent_checkpoint_sha256': PARENT_SHA,
    'parent_design_sha256': 'fccc817be37d821a781348a8870c227ff5471fcdc72d71f38a81bc062c7a3eec',
    'active_files': [], 'proposed_source_path_count': 16,
    'full_host_literal_status': 'FAILED', 'full_host_test_count': 41,
    'full_host_success_count': 40, 'full_host_assertion_failures': 1,
    'focused_corrected_test_count': 1, 'focused_corrected_test_passed': True,
    'final_fresh_full_suite_locally_reexecuted': False,
    'android_executed': False, 'new_runtime_parity_credit': 0,
    'frozen_payload_count': len(files),
    'frozen_payload_bytes': sum(row['bytes'] for row in files), 'files': files}
write_json(DEST / 'checkpoint.json', checkpoint)
for row in files:
    assert identity(DEST / row['path']) == {k: row[k] for k in ('bytes', 'sha256')}
print(json.dumps({'path': str(DEST / 'checkpoint.json'), **identity(DEST / 'checkpoint.json'),
    'payloads': len(files), 'payload_bytes': checkpoint['frozen_payload_bytes'],
    'final_source': before_source}, indent=2))
