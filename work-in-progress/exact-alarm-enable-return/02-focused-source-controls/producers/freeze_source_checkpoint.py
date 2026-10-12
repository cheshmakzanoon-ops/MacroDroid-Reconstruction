from __future__ import annotations

import argparse
import datetime
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import tarfile

from run_host_attempt import ROOT, WORKING, inventory


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'mode': stat.S_IMODE(path.stat().st_mode)}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def copy_file(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    target.chmod(stat.S_IMODE(source.stat().st_mode))
    assert identity(source) == identity(target)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('name')
    parser.add_argument('--final', action='store_true'); args = parser.parse_args()
    out = ROOT / 'checkpoints' / args.name; out.mkdir(parents=True, exist_ok=False)
    reports = ROOT / 'source-01/reports'
    selected = ['01-first-focused-controls', '02-source-boundary-review']
    if args.final: selected += ['03-parent-compatibility-controls', '04-real-fourteen-screen-replay']
    results = {name: json.loads((reports / name / 'result.json').read_bytes()) for name in selected}
    assert all(row['passed'] for row in results.values())
    sources = inventory(WORKING)
    assert len(sources) == 102
    focused_ids = json.loads((reports / selected[0] / 'discovered-tests.json').read_bytes())
    focused_result = json.loads((reports / selected[0] / 'tests-result.json').read_bytes())
    assert focused_result['passed'] and focused_result['tests_run'] == len(focused_ids) == 50
    tests_passed = list(focused_ids)
    if args.final:
        parent_ids = json.loads((reports / '03-parent-compatibility-controls/discovered-tests.json').read_bytes())
        parent_result = json.loads((reports / '03-parent-compatibility-controls/tests-result.json').read_bytes())
        assert parent_result['passed'] and parent_result['tests_run'] == len(parent_ids) == 209
        assert not set(parent_ids) & set(focused_ids)
        tests_passed += parent_ids
        declared = json.loads((reports / '02-source-boundary-review/candidate-test-discovery.stdout').read_bytes())
        assert set(declared) == set(tests_passed) and len(tests_passed) == 259
    for relative, row in sources.items(): copy_file(WORKING / relative, out / 'source' / relative)
    for name in ('design.json', 'settings-contract.json', 'sixteen-screen-plan.json'):
        copy_file(ROOT / 'design-01' / name, out / 'design' / name)
    copy_file(ROOT / 'design-01/checkpoint.json', out / 'design/original-design-checkpoint.json')
    for name in ('prepare_source.py', 'author_adapters.py', 'author_dispatch.py', 'author_tests.py',
                 'adapter-template.py.txt', 'new-tests-template.py.txt', 'run_host_attempt.py',
                 'verify_source_boundaries.py', 'replay_closed_fourteen.py', 'freeze_source_checkpoint.py'):
        copy_file(ROOT / name, out / 'producers' / name)
    copy_file(ROOT / 'source-01/preparation.json', out / 'reports/preparation.json')
    for name in ('inputs-before.json', 'six-path-delta.json', 'definition-preservation.json', 'dispatch.patch',
                 'parent-before.json', 'current-before.json', 'parent-test-discovery.stdout', 'candidate-test-discovery.stdout'):
        copy_file(reports / '02-source-boundary-review' / name, out / 'reports' / name)
    write(out / 'reports/distinct-passed-tests.json', sorted(tests_passed))
    write(out / 'reports/closed-results.json', results)
    write(out / 'reports/current-source.json', sources)
    evidence = []
    for name in selected:
        for path in sorted((reports / name).rglob('*')):
            if path.is_dir(): continue
            info = path.lstat()
            assert stat.S_ISREG(info.st_mode) and info.st_nlink == 1, str(path)
            relative = name + '/' + str(path.relative_to(reports / name))
            evidence.append((relative, path, identity(path)))
            if path.parent == reports / name and path.suffix in ('.json', '.txt', '.stdout', '.stderr', '.patch'):
                copy_file(path, out / 'reports/attempts' / relative)
    write(out / 'evidence-inventory.json', [{**row, 'path': relative} for relative, path, row in evidence])
    with (out / 'evidence.tar.gz').open('xb') as raw:
        with gzip.GzipFile(fileobj=raw, mode='wb', filename='', mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode='w|') as archive:
                for relative, path, row in evidence:
                    data = path.read_bytes(); assert identity(path) == row
                    info = tarfile.TarInfo(relative); info.size = len(data); info.mode = row['mode']; info.mtime = 0
                    archive.addfile(info, io.BytesIO(data))
    with tarfile.open(out / 'evidence.tar.gz', 'r:gz') as archive:
        members = archive.getmembers()
        assert [member.name for member in members] == [relative for relative, path, row in evidence]
        for member, (relative, path, row) in zip(members, evidence):
            data = archive.extractfile(member).read()
            assert member.isfile() and len(data) == row['bytes'] and member.mode == row['mode']
            assert hashlib.sha256(data).hexdigest() == row['sha256']
    status = ('EXACT_ALARM_ENABLE_RETURN_HOST_AND_HISTORICAL_CONTROLS_PASSED_INACTIVE' if args.final
              else 'EXACT_ALARM_ENABLE_RETURN_FOCUSED_HOST_CONTROLS_PASSED_PARENT_AND_DEVICE_REPLAY_PENDING')
    readme = f'''# Exact-alarm Settings enable and return: source checkpoint

Status: **{status}**. This checkpoint adds the two visible Settings actions to an
isolated source proposal. No workflow, active application source, APK or device was
changed by this source study. Android execution is false for this authoring task.

## Exact source and observed control binding

The complete replay tree contains 102 files: 96 byte-identical parent files, two
narrow dispatch edits, and four new adapter/test modules. All 98 parent file pins
remain checked against design d3a8623c00ec814fb92f2cf07d148110efc058c19d40d73450251adeafdd373c.
The full 140,449-byte Settings contract is embedded unchanged in the new adapter
and independently copied under design; its SHA-256 is
379544de4e9e5d84138959f1e1552fcc9b2e52d7264d30e324c63f2a82814c07.
Both observed Alarm14 XML fixture bytes equal the separately embedded 6,919-byte
test fixture, SHA-25644247f77da12d0c1eaddbebcd0fa5424399138a9bd995ee87a545294e678425e.
The new on hierarchy is a prediction: only the actual clickable toggle parent's
checked attribute changes from false to true. It has not been observed on Android.

The exact sixteen-screen plan is
ca597b23d9c2d11ebce1ed3953d609189476d7179635f2a4c4068df0795f2211.
It preserves the fourteen-screen prefix's thirteen inputs, requires the complete
observed off hierarchy before a single tap at (360, 771), requires the complete
predicted checked-on hierarchy before a single Navigate up tap at (56, 104), then
records a stable MacroDroid-owned surface without assuming its activity class or
any control. All six Settings raw artifact roles must share one exact run, step,
acquisition and frame stem; four Settings capture-role names are permitted.

## Policy and future outcome fields

The policy function is exact_alarm_enable_return.require_navigation_policy;
the key is exact_alarm_enable_return_policy and the evidence schema is 7. Its
completed narrow comparison status is EXACT_ALARM_ENABLED_RETURN_OBSERVATION_ONLY,
subject to the unchanged post-crash continuation status override. A complete
comparison binds 30 total planned inputs, six setup mutations, and exactly four
Settings taps. It separately records displayed checked-on state and navigation
back to an app-owned surface. permission_api_result_observed,
trigger_configuration_confirmed, macros_saved, macros_executed and
full_runtime_1_to_1_established remain false. No AlarmManager API result is claimed.

## Measured host evidence

There are {len(tests_passed)} distinct named host successes in this checkpoint.
The 50 new controls passed in {focused_result['seconds']:.6f} seconds against an
unchanged 102-file executed copy. They exercise actual recorder command construction
through virtual ADB, full off/on geometry, exact coordinates, stale preconditions,
PID/component changes, unsupported Settings roles, all command mutations, stream
aliases, raw hierarchy/RGBA differences, and the inherited notification-readiness
contract under schema 7. The screenshots, on/return state and process clocks of
those finite host cases are authored; they are not device parity evidence.

{'The separate 209 unchanged parent tests also passed. Their exact test identities are disjoint from the new 50; the verified union is 259. No duplicate full local run was used to inflate that count. The two original historical ZIP fixtures retain their existing paths and exact identities in reports/inputs-before.json.' if args.final else 'The separate 209 unchanged parent-test execution and actual fourteen-screen replay are still pending at this freeze. The source boundary check only discovered and preserved their identities; it did not count them as executed successes.'}

{'A separate read-only replay of actual run38240023189/artifact11742624179 preserves the complete old schema6 comparison object exactly: JOURNEY_DIFFERENCE, 35 changed intro2 pixels, all other thirteen full screens equal, 1091 commands, 26 planned inputs and zero Settings inputs. The actual recorded crash/restart evidence and full-runtime false result remain unchanged. The replay executes no Android action, and its complete raw input inventory is checked before and after.' if args.final else 'No old device result has been relabeled in this focused checkpoint.'}

All closed attempts and complete executed source trees are retained in the exact
evidence archive. Test temporary directories follow their existing cleanup rules;
the executed tests, complete logs, discovered names and before/after source/fixture
identities are preserved. The two historical ZIP bytes are preserved in the final
parent-test archive only, separate from the 102 source files. The real Alarm14 raw
artifact is reused read-only and is not duplicated here.

The future workflow must pin the actually published 0762aad9 candidate manifest.
It must run the full 259-case package in CI, preserve all literal failures, and
stop on any unpredicted Settings or returned app state. This source checkpoint
does not authorize an Android action or imply a successful future capture.
'''
    (out / 'README.md').write_text(readme)
    assert inventory(WORKING) == sources
    direct = []
    for path in sorted(out.rglob('*')):
        if path.is_file(): direct.append({'path': str(path.relative_to(out)), **identity(path)})
    checkpoint = {'schema': 1, 'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'status': status, 'repo_target': 'work-in-progress/exact-alarm-enable-return/' + args.name,
                  'source_files': 102, 'parent_source_files': 98, 'unchanged_parent_sources': 96,
                  'changed_existing_source_files': 2, 'new_source_files': 4,
                  'distinct_host_tests_passed': len(tests_passed), 'focused_host_tests_passed': 50,
                  'parent_host_tests_passed': 209 if args.final else 0,
                  'complete_historical_schema6_verdict_unchanged': bool(args.final),
                  'predicted_on_state_observed_on_android': False, 'active_changes': False,
                  'android_executed': False, 'full_runtime_1_to_1_established': False,
                  'evidence_files': len(evidence), 'evidence_archive': identity(out / 'evidence.tar.gz'),
                  'files': direct}
    write(out / 'checkpoint.json', checkpoint)
    print(json.dumps({'path': str(out / 'checkpoint.json'), **identity(out / 'checkpoint.json'),
                      'files': len(direct), 'evidence_files': len(evidence), 'evidence_archive': checkpoint['evidence_archive']}))


if __name__ == '__main__':
    main()
