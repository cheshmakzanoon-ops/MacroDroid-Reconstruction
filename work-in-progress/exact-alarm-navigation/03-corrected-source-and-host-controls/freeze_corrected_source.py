#!/usr/bin/env python3
"""Freeze the corrected source, all closed host attempts, and real-report replay."""
from __future__ import annotations

from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import re
import shutil
import stat

ROOT = Path('/dev/shm/macrodroid-exact-alarm-navigation')
STAGE = ROOT / 'source-01'
SOURCE = STAGE / 'repository'
OUTPUT = ROOT / 'checkpoints/03-corrected-source-and-host-controls'
PARENT = Path('/dev/shm/macrodroid-notification-readiness/checkpoints/01-corrected-host-guard')


def identity(path, root):
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or path.is_symlink():
        raise RuntimeError('Nonregular checkpoint input: ' + str(path))
    data = path.read_bytes()
    return {'path': path.relative_to(root).as_posix(), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(),
            'mode': '100755' if info.st_mode & 0o111 else '100644'}


def inventory(root):
    return [identity(path, root) for path in sorted(root.rglob('*')) if not path.is_dir()]


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def copy_tree(source, target):
    for row in inventory(source):
        destination = target / row['path']
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / row['path'], destination)
        if identity(destination, target) != row:
            raise RuntimeError('Checkpoint transport changed: ' + row['path'])


def main():
    source_before = inventory(SOURCE)
    if len(source_before) != 98:
        raise RuntimeError('Expected the exact 98-file source inventory')
    attempts = [('02-global-command-correction', 5, 'PASS'), ('03-corrected-full-new', 43, 'PASS'),
                ('04-corrected-full-legacy', 166, 'FAILED'), ('05-prepared-historical-fixtures', 2, 'PASS')]
    results = []
    passed_test_ids = set()
    for name, count, status in attempts:
        attempt = STAGE / 'attempts' / name
        result = json.loads((attempt / 'result.json').read_text())
        executed_source = [row for row in inventory(attempt / 'source') if not row['path'].endswith('/evidence.zip')]
        output = (attempt / 'stderr.log').read_text()
        if (result['status'] != status or result['source_unchanged'] is not True
                or result['returncode'] != (0 if status == 'PASS' else 1) or result['timed_out'] is not False
                or json.loads((attempt / 'source-before.json').read_text()) != source_before
                or json.loads((attempt / 'source-after.json').read_text()) != source_before
                or executed_source != source_before
                or ('Ran ' + str(count) + ' tests') not in output):
            raise RuntimeError('Exact closed host attempt is required: ' + name)
        passed = re.findall(r'^test[^\n]* \(([^)]+)\) \.\.\. ok$', output, flags=re.MULTILINE)
        if len(passed) != (164 if status == 'FAILED' else count):
            raise RuntimeError('Unexpected successful test inventory: ' + name)
        passed_test_ids.update(passed)
        if status == 'FAILED' and (output.count('FileNotFoundError:') != 2
                or 'FAILED (errors=2)' not in output or 'failure' in output.lower()[-100:]):
            raise RuntimeError('The retained legacy attempt has an unexpected failure')
        results.append({'attempt': name, 'tests': count, **result})
    if len(passed_test_ids) != 209:
        raise RuntimeError('Expected exactly 209 distinct passing controls across the retained attempts')
    replay = json.loads((STAGE / 'completed-schema5-replay-corrected/result.json').read_text())
    grammar = json.loads((STAGE / 'actual-command-grammar-corrected/result.json').read_text())
    if (replay['status'] != 'EXACT_HISTORICAL_RESULT_UNCHANGED'
            or replay['complete_comparison_object_equal'] is not True
            or replay['raw_files_unchanged'] is not True or replay['source_files_unchanged'] is not True
            or grammar['status'] != 'ALL_CLOSED_REAL_COMMANDS_CLASSIFIED'
            or grammar['source_unchanged'] is not True or grammar['read_inputs_unchanged'] is not True):
        raise RuntimeError('Closed actual-report replay and command classification are required')
    review = Path('/dev/shm/macrodroid-transfer-space-20261012/alarm14-global-command-review/checkpoint.json')
    if hashlib.sha256(review.read_bytes()).hexdigest() != '9eaed0702f2ff52ed02068c5565b05f5e7dfb26a385cf018f99448fca974fe6c':
        raise RuntimeError('The closed independent correction review changed')
    OUTPUT.mkdir(exist_ok=False)
    copy_tree(SOURCE, OUTPUT / 'replay-source')
    aliases = []
    historical_aliases = []
    historical = {key: value for key, value in json.loads((PARENT / 'reports/inputs-before.json').read_text()).items()
                  if key.endswith('/evidence.zip')}
    for name, _, _ in attempts:
        attempt = STAGE / 'attempts' / name
        for row in inventory(attempt):
            if row['path'].startswith('source/'):
                relative = row['path'][len('source/'):]
                if relative in historical:
                    if {key: row[key] for key in ('bytes', 'sha256')} != historical[relative]:
                        raise RuntimeError('The prepared historical ZIP differs from its durable identity')
                    historical_aliases.append({'executed_attempt_path': 'attempts/' + name + '/' + row['path'],
                                               'repository_path': relative, 'bytes': row['bytes'],
                                               'sha256': row['sha256'], 'mode': row['mode'],
                                               'already_published_input': True})
                    continue
                aliases.append({'executed_attempt_path': 'attempts/' + name + '/' + row['path'],
                                'checkpoint_source_path': 'replay-source/' + relative,
                                'bytes': row['bytes'], 'sha256': row['sha256'], 'mode': row['mode']})
            else:
                destination = OUTPUT / 'attempts' / name / row['path']
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(attempt / row['path'], destination)
    save(OUTPUT / 'attempt-source-aliases.json', {
        'schema': 1, 'scope': 'Exact byte and mode aliases for the four retained executed source snapshots; source bytes occur once in replay-source.',
        'all_392_aliases_verified_before_copy': True, 'files': aliases})
    save(OUTPUT / 'historical-archive-aliases.json', {'schema': 1, 'files': historical_aliases,
        'scope': 'The prepared historical test directory also contains these two exact already-published ZIP inputs; restore only from their pinned repository bytes.'})
    if len(aliases) != 392 or len(historical_aliases) != 2:
        raise RuntimeError('Incomplete executed source alias inventory')
    for name in ('completed-schema5-replay-corrected', 'actual-command-grammar-corrected'):
        copy_tree(STAGE / name, OUTPUT / name)
    copy_tree(STAGE / 'derivation', OUTPUT / 'derivation')
    shutil.copy2(STAGE / 'source-before.json', OUTPUT / 'source-before.json')
    (OUTPUT / 'reports').mkdir()
    shutil.copy2(PARENT / 'reports/inputs-before.json', OUTPUT / 'reports/inputs-before.json')
    scripts = ['create_source_stage.py', 'derive_shared_source.py', 'run_host_attempt.py',
               'run_prepared_fixture_attempt.py',
               'replay_completed_readiness.py', 'replay_completed_readiness_corrected.py',
               'classify_actual_global_commands.py', 'freeze_corrected_source.py']
    for name in scripts:
        shutil.copy2(ROOT / name, OUTPUT / name)
    first = STAGE / 'attempts/01-focused-first/source'
    changes = []
    for row in source_before:
        earlier = identity(first / row['path'], first)
        if row == earlier:
            continue
        old = (first / row['path']).read_text()
        new = (SOURCE / row['path']).read_text()
        patch = ''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                       fromfile='first-attempt/' + row['path'], tofile='corrected/' + row['path']))
        destination = OUTPUT / 'derivation' / (Path(row['path']).name + '.global-command-correction.patch')
        with destination.open('x') as stream:
            stream.write(patch)
        changes.append({'before': earlier, 'after': row})
    if [row['after']['path'] for row in changes] != [
            'tools/parity_journeys/editor_journey.py', 'tools/parity_journeys/exact_alarm_journey.py',
            'tools/parity_journeys/test_exact_alarm_journey.py']:
        raise RuntimeError('The bounded global-command correction changed unexpected paths')
    save(OUTPUT / 'derivation/global-command-correction.json', {
        'source_files': 98, 'changed_files': changes, 'other_95_files_unchanged': True,
        'earlier_first_attempt_checkpoint_sha256': '8552ab5bd7499cd4428e6ffc018bfdd3322c3bcf8a544d26e937ef023103c56e',
        'independent_corrected_review_checkpoint_sha256': '9eaed0702f2ff52ed02068c5565b05f5e7dfb26a385cf018f99448fca974fe6c'})
    save(OUTPUT / 'host-and-replay-summary.json', {'attempts': results, 'actual_schema5_replay': replay,
        'actual_command_grammar': grammar, 'distinct_current_host_tests': 209,
        'passing_test_ids': sorted(passed_test_ids), 'legacy_full_suite_passed_in_one_attempt': False,
        'legacy_preparation_failure_retained': True, 'both_blocked_tests_passed_with_exact_published_fixtures': True,
        'corrected_source_unchanged_during_all_four_attempts': True,
        'android_executed': False, 'full_runtime_1_to_1_established': False})
    with (OUTPUT / 'README.md').open('x') as stream:
        stream.write('''# Corrected exact-alarm navigation source and host controls

This inactive checkpoint closes the command-ownership gap found in the first draft. It contains the exact 98-file successor source, literal results from all four closed host attempts, source aliases for every executed snapshot, the complete replay of the historical Android report, and the finite-grammar classification of its 1,021 commands. A separately reviewed workflow is still required before the new fourteenth Android observation can run.

The correction changes three files relative to the preserved first attempt: the new exact-alarm adapter, its tests, and the shared recorder/comparison entry point. The other 95 files remain byte-identical. The shared recorder retains the uninstall result only for the exact new fourteen-screen plan, and the shared comparison invokes the new command gate only for schema 6. Existing schemas and the original notification-readiness implementation retain their earlier behavior.

## Confirmed flaw and correction

The exact independent counterexample was an appended `['shell', 'input tap 20 20']` command after both terminal captures. The prior checkpoint's prose accidentally omitted the space between `tap` and `20`; its stored counterexample and source were unaffected. The first draft accepted that extra input and reproduced its entire positive comparison object. That first result and all independent counterexample evidence remain preserved.

The corrected gate classifies the entire chronological command log using the literal recorder grammar. The complete ordered sequence must contain exactly 13 planned taps and the declared uninstall, install and launch commands for each APK. Setup observations have their own ordered global roles. Every command stream has a unique path and inode, and all raw streams remain hash-checked. Additional commands can only be exact recognized evidence commands, including the recorder's owned temporary XML creation and removal. Shell wrappers, permission changes, unknown launches, unowned file removal and extra input are rejected.

Independent review re-ran a complete authored fourteen-screen positive, reproduced rejection of the exact appended-tap counterexample, checked a separate chronology failure, and recovered the whole original comparison after restoration. It preserved all 98 source inputs and 1,418 synthetic artifact files. That review is separately published under `docs/verification/exact-alarm-navigation/02-global-command-correction-review` with checkpoint identity `9eaed0702f2ff52ed02068c5565b05f5e7dfb26a385cf018f99448fca974fe6c`.

## Closed validation and scope

The bounded five-test correction attempt and all 43 new tests passed. The complete 166-test legacy attempt passed 164 tests and failed two with `FileNotFoundError`: its private directory lacked the two published historical ZIP fixtures. That preparation failure and literal output remain intact. The two blocked tests were then rerun unchanged in a fresh private directory containing the exact 98 source files plus both hash-verified published ZIPs; both passed. All 209 distinct controls therefore have passing results against the same source bytes, with the failed preparation attempt explicitly retained. The five focused tests are included in the new suite. A single packaged 209-test discovery run remains a required workflow validation gate. Literal elapsed times, outputs, command arguments, syntax checks and before/after inventories are retained. Authored Settings fixtures are explicitly synthetic and do not establish an actual Settings class, permission control or application behavior.

The unchanged real schema-5 report from Android run 38230072388 was replayed under the corrected shared source. Its entire comparison object remained unchanged: both runs reached 13 screens, all paired hierarchies matched, and the changed-pixel vector remained `[0, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`. All 3,258 raw files and all 98 source files remained unchanged. The recorded known process-boundary outcome and failed exact visual comparison remain part of that result.

The finite grammar separately classified all 1,021 actual commands in that report: 991 evidence commands, 24 taps, two uninstalls, two installs and two launches. This is a classification of existing evidence. It does not retrofit the new uninstall role into that older report or invent a fourteenth capture.

The only proposed new Android input remains the exact observed OK button at `(560, 809)` in the complete exact-alarm explanation dialog. The terminal role observes Settings with the original app's required PID continuity and no assumed Settings class or control. No Settings input, permission grant, confirmed trigger configuration, saved macro, executed macro or whole-application parity is established here.
''')
    if inventory(SOURCE) != source_before:
        raise RuntimeError('Source changed while the successor was frozen')
    files = inventory(OUTPUT)
    if any(row['mode'] != '100644' for row in files):
        raise RuntimeError('The frozen source package must contain only the reviewed non-executable file mode')
    files = [{key: row[key] for key in ('path', 'bytes', 'sha256')} for row in files]
    checkpoint = {'schema': 1, 'status': 'CORRECTED_EXACT_ALARM_HOST_CONTROLS_PASSED_INACTIVE',
                  'created_utc': datetime.now(timezone.utc).isoformat(),
                  'repo_target': 'work-in-progress/exact-alarm-navigation/03-corrected-source-and-host-controls',
                  'source_files': 98, 'distinct_host_tests_passed': 209, 'focused_host_tests_passed': 5,
                  'independent_global_input_counterexample_rejected': True,
                  'complete_historical_schema5_verdict_unchanged': True,
                  'active_changes': False, 'android_executed': False,
                  'full_runtime_1_to_1_established': False, 'files': files}
    save(OUTPUT / 'checkpoint.json', checkpoint)
    manifest = identity(OUTPUT / 'checkpoint.json', OUTPUT)
    print(json.dumps({'checkpoint': str(OUTPUT / 'checkpoint.json'), **manifest,
                      'files': len(files), 'payload_bytes': sum(row['bytes'] for row in files)}, indent=2))


if __name__ == '__main__':
    main()
