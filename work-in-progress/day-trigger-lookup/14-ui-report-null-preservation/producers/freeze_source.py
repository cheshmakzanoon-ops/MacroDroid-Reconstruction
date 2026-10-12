from __future__ import annotations

import datetime
import gzip
import hashlib
import json
from pathlib import Path

from prepare_source import ROOT, MERGE, SUCCESSOR, identity, write, copy, checkpoint_inputs, OLD_LINE, NEW_LINE


def byte_identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    stage = ROOT / 'stage-01'
    controls = ROOT / 'controls-01'
    result = json.loads((controls / 'result.json').read_bytes())
    assert result['passed'] is True and result['source_input_files_unchanged'] == 53
    assert len(result['commands']) == 6
    assert [row['returncode'] for row in result['commands']] == [0, 0, 0, 0, 2, 0]
    derivation = json.loads((stage / 'derivation.json').read_bytes())
    assert checkpoint_inputs(MERGE, '56aa7bfc05286d9fc474d24e6afc33fbd3a664e9dc731f70912df1a9e375b350') == derivation['parent_inputs']['merge']
    assert checkpoint_inputs(SUCCESSOR, '87c2a01a627590b62017eae8145db92d1a7593d5cf127114a9812ec13cd756f5') == derivation['parent_inputs']['successor']
    out = ROOT / 'checkpoints/01-source-and-serializer-boundary'
    out.mkdir(parents=True, exist_ok=False)
    for folder, destination in [(stage, out / 'boundary-inputs'), (controls, out / 'boundary-controls')]:
        for path in sorted(folder.rglob('*')):
            if path.is_file(): copy(path, destination / path.relative_to(folder))
    for name in ('prepare_source.py', 'run_source_controls.py', 'freeze_source.py'):
        copy(ROOT / name, out / 'producers' / name)
    source_names = ('day_lookup_dex_controls.py', 'tests/test_day_lookup.py', 'tests/java/UiParityTests.java')
    for name in source_names:
        origin = stage if name.endswith('UiParityTests.java') else SUCCESSOR
        copy(origin / 'project' / name, out / 'project' / name)
    old_ui = (stage / 'inputs/source/UiParityTests.java').read_text()
    new_ui = (out / 'project/tests/java/UiParityTests.java').read_text()
    assert old_ui.count(OLD_LINE) == 1 and new_ui.replace(NEW_LINE, OLD_LINE) == old_ui
    copy(SUCCESSOR / 'complete-future-overlay-manifest.json', out / 'parent-complete-future-overlay-manifest.json')
    previous = json.loads((SUCCESSOR / 'complete-future-overlay-manifest.json').read_bytes())
    manifest = json.loads(json.dumps(previous))
    changed_rows = []
    for row in manifest['changes']:
        if row['path'] == 'tests/java/UiParityTests.java':
            row['report_serializer_parent'] = row['after']
            row['after'] = identity(out / 'project' / row['path'])
            row['payload_source'] = 'this-capsule/project/' + row['path']
            row['reason'] += ' Preserve explicit JSON nulls at the final report write; the shared comparison Gson and every application case remain unchanged.'
            changed_rows.append(row['path'])
    assert changed_rows == ['tests/java/UiParityTests.java']
    assert len(manifest['changes']) == 21
    manifest['serializer_successor'] = {
        'parent_checkpoint': identity(SUCCESSOR / 'checkpoint.json'),
        'parent_source_paths_preserved': ['day_lookup_dex_controls.py', 'tests/test_day_lookup.py'],
        'replaced_source_path': 'tests/java/UiParityTests.java',
        'selected_source_paths_in_this_capsule': list(source_names),
        'only_application_input_change_from_failed_combined_snapshot': 'tests/java/UiParityTests.java',
        'application_executions': 0, 'active_source_changed': False,
        'actual_regression_old_returncode': 2, 'actual_regression_corrected_returncode': 0,
    }
    write(out / 'complete-future-overlay-manifest.json', manifest)
    prior_raw = gzip.decompress((SUCCESSOR / 'future-input-snapshot.json.gz').read_bytes())
    assert byte_identity(prior_raw) == {'bytes': 14505034, 'sha256': 'cd89966dae610579966c7d0ebfd62861ce3468c43c25427c738b369d98727b1a'}
    prior = json.loads(prior_raw)
    assert prior['files'] == 81304 and prior['snapshot_sha256'] == 'b981dd67fd84ddf8dc026b2aed0ede7f1770c48ef64acc9009f5eaa076f34a0c'
    assert hashlib.sha256(json.dumps(prior['entries'], sort_keys=True, separators=(',', ':')).encode()).hexdigest() == prior['snapshot_sha256']
    fresh = json.loads(prior_raw)
    row = identity(out / 'project/tests/java/UiParityTests.java')
    fresh['entries']['tests/java/UiParityTests.java'] = {'size': row['bytes'], 'sha256': row['sha256']}
    fresh['snapshot_sha256'] = hashlib.sha256(json.dumps(fresh['entries'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert fresh['files'] == len(fresh['entries']) == 81304
    assert [name for name in prior['entries'] if prior['entries'][name] != fresh['entries'][name]] == ['tests/java/UiParityTests.java']
    fresh_raw = json.dumps(fresh, indent=2, ensure_ascii=True).encode()
    with (out / 'future-input-snapshot.json.gz').open('xb') as stream:
        with gzip.GzipFile(filename='', fileobj=stream, mode='wb', mtime=0) as zipped:
            zipped.write(fresh_raw)
    assert gzip.decompress((out / 'future-input-snapshot.json.gz').read_bytes()) == fresh_raw
    future = {'schema': 1, 'derivation_only_no_physical_source_materialization': True,
        'previous_snapshot': {k: prior[k] for k in ('files', 'snapshot_sha256')},
        'previous_manifest': byte_identity(prior_raw),
        'future_snapshot': {k: fresh[k] for k in ('files', 'snapshot_sha256')},
        'future_manifest': byte_identity(fresh_raw),
        'changed_entries': ['tests/java/UiParityTests.java'],
        'all_other_81303_entries_unchanged': True, 'application_execution': False}
    write(out / 'future-manifest-derivation.json', future)
    source_files = [{'path': 'project/' + name, **identity(out / 'project' / name)} for name in source_names]
    write(out / 'source-files.json', source_files)
    readme = '''# Explicit nulls in the combined UI report

Run 38248170022 at 97322c18273818b0241fa1fa962da9d4a445afd1 built both APKs
and returned zero for all sixteen application acceptance gates. The independent
finalizer then rejected the UI observer controls. The original job remains a
failure and its original reports are unchanged.

The UI report and the standalone control call the same observer producer. The
UI writer's Gson configuration omitted null-valued object members, even though
the shared observer had already built a JSON tree containing those members.
The standalone writer explicitly serialized nulls. The sole differing fields
are the null returnIndex on the positive record and rejected records 0, 1, 2,
and 4. Rejected record 3 has the non-null integer 0 and agrees. The other four
parts of the finalizer's conjunction match exactly, as do all remaining fields
of the observer controls. The five-value diagnosis is retained in this capsule.

This successor changes one line in tests/java/UiParityTests.java. Its final
Files.writeString call now uses G.newBuilder().serializeNulls().create() to
serialize the report. The shared G instance used during comparisons, all case
and observer implementations, and the strict finalizer equality stay unchanged.
The two previously reviewed recorder successor source files are copied exactly.
The complete overlay remains twenty-one paths. The complete logical future
inventory retains 81,304 entries and changes only this test harness source row.
This derivation is not a substitute for the next physical source verification.

## Executed boundary regression

Six bounded commands are retained with exact argv, environment, start/finish
clocks, exit codes and raw streams: source preparation; Java and javac version
observations; compilation; original writer; corrected writer. Both Java runs use
-Xverify:all. The boundary harness mechanically includes the actual unchanged
G initializer and the exact old and corrected final write statements. It calls
the already compiled, archived DayLookupParityCases.observerControls on the
exact 371-entry pinned input inventory. Its generated controls are first compared
strictly with the closed standalone record from the failed run.

The original writer exits 2, reproduces exactly the five missing fields, and
matches the original closed UI observer object. The corrected writer exits 0
and retains strict equality for the whole JSON tree, including nested nulls,
null array entries, empty containers, empty strings, zero, false, escaped text,
and all six observer records. The five generated mutations are rejected by the
unchanged compiled observer. All 53 copied source/control inputs and the Java,
javac, Python and pinned Gson-containing JAR remain unchanged. The original
writer's failed result is preserved as a failure.

These are host report serialization controls. They execute no recovered app
method, complete UI parity harness, APK build, Android process, alarm or macro.
They add no application case or recovered-body credit. A fresh full hosted run
with unchanged strict finalization is still required before source promotion.
The 40 exact runtime classes and all boundary outputs are retained here; the
large existing dependency JAR is identified by hash and is not duplicated.
'''
    (out / 'README.md').write_text(readme)
    files = [{'path': p.relative_to(out).as_posix(), **identity(p)} for p in sorted(out.rglob('*')) if p.is_file()]
    cp = {'schema': 1, 'status': 'ONE_LINE_UI_REPORT_SERIALIZER_BOUNDARY_PASSED_SOURCE_INACTIVE',
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'repo_target': 'work-in-progress/day-trigger-lookup/14-ui-report-null-preservation',
        'active_source_changed': False, 'active_workflow_changed': False,
        'application_executions': 0, 'full_host_acceptance_executed': False, 'android_runtime_executed': False,
        'parent_successor_checkpoint': identity(SUCCESSOR / 'checkpoint.json'),
        'merge_checkpoint': identity(MERGE / 'checkpoint.json'),
        'actual_failed_run': 38248170022, 'actual_artifact': derivation['actual_artifact'],
        'source_path_count': 3, 'changed_from_previous_combined_source_paths': ['tests/java/UiParityTests.java'],
        'complete_future_overlay_path_count': 21, 'future_snapshot': future['future_snapshot'],
        'future_manifest': future['future_manifest'], 'boundary_commands': 6,
        'old_serializer_failure_reproduced': True, 'corrected_serializer_exact_tree_roundtrip': True,
        'strict_finalizer_unchanged': True, 'files': files}
    write(out / 'checkpoint.json', cp)
    print(json.dumps({'checkpoint': str(out / 'checkpoint.json'), **identity(out / 'checkpoint.json'),
                      'files': len(files), 'payload_bytes': sum(row['bytes'] for row in files),
                      'future_snapshot': future['future_snapshot'], 'future_manifest': future['future_manifest']}))


if __name__ == '__main__':
    main()
