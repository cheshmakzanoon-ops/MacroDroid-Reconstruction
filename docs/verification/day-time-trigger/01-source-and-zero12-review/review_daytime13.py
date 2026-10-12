#!/usr/bin/env python3
"""Independently review the sealed Day/Time13 capsule and replay actual Zero12.

No Android command, APK build, source mutation, or large artifact copy occurs.
The different-source replay is separate from the unchanged historical verifier.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import time
import xml.etree.ElementTree as ET
import zipfile

sys.dont_write_bytecode = True
BASE = Path('/workspace/scratch/4130730d15aa')
CAPSULE = BASE / 'day-time-trigger-forward/checkpoints/02-host-success'
CAPSULE_SHA = '0e010cfbace03cffa6d45e8c9157402b1b68c9a392249eb2aeae39445dc57a7d'
RAW = BASE / 'ci-run-analysis/zero12-run-38216299675-extracted'
ARCHIVE = BASE / 'ci-run-analysis/zero12-run-38216299675.zip'
ARCHIVE_ID = {'bytes': 42199893, 'sha256': '1ea3ad6302d53c2fcc8341c03deec7ccd04d729facaf5658acb87e4aebc6f4b3'}
JOURNEY_ID = {'bytes': 839255, 'sha256': 'a6253dfea14353a2d8fe552e3772e4fe5e58a693e2339bafcce9f0d008a61409'}
COMPARISON_ID = {'bytes': 6873, 'sha256': '5e3d1683ad09d0ef5e64d6b02ef152c11c1ac9095a1e96de0c6ff787407542c5'}
PREFIX_SHA = '940be18b226ab29de46ea48a1496238b8a2221a52077466693a34a2113bc24cc'
HISTORICAL14_SHA = '69bae4f2af8e2f14c407808dbcdea91cdca009af2ae390e13b5c7fbf035a3065'
SOURCE_PINS = {
    'tools/parity_journeys/day_time_journey.py': '80659a544535cf8bab436aaf592536bf2093ac407b466c88f9f8771fed7b18c7',
    'tools/parity_journeys/editor_journey.py': '533aef012009d867f5ec5d83a56a9f30ff1199f9ace2a52d83f530bbb4a9e574',
    'tools/parity_journeys/observed_journey.py': '79bc7a58a5f40a50199e18a653b39aaecc3a7dfc8899b5c36e42e1c5616cb091',
    'tools/parity_journeys/test_day_time_journey.py': '4e3756f77a22f65820aed7f5cba1643072efaa7ee16145c98d5bfe1366f34f9a',
}
PARENT_PINS = {
    'tools/parity_journeys/editor_journey.py': 'bb62c975090c4f78b49c1ef638f4e55edbe1b0d24f8c40982e8d1769c5cdb99b',
    'tools/parity_journeys/observed_journey.py': 'dd4e2b953e697b8ac2114848d2fafc3844b2b80e9706943e353abd4990b8c083',
}


def identity(path):
    assert path.is_file() and not path.is_symlink(), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def safe(name):
    path = PurePosixPath(name)
    assert path.as_posix() == name and not path.is_absolute() and '..' not in path.parts and '\\' not in name


def inventory(root):
    result = {}
    for path in sorted(root.rglob('*')):
        assert not path.is_symlink(), str(path)
        if path.is_file():
            name = path.relative_to(root).as_posix()
            safe(name)
            result[name] = identity(path)
    return result


def checkpoint():
    assert identity(CAPSULE / 'checkpoint.json') == {'bytes': 23239, 'sha256': CAPSULE_SHA}
    value = json.loads((CAPSULE / 'checkpoint.json').read_text())
    assert value['status'] == 'HOST_CONTROLS_PASSED_INACTIVE'
    assert value['android_executed'] is False and value['active_changes'] is False
    rows = value['files']
    assert len(rows) == 114
    expected = {}
    for row in rows:
        safe(row['path'])
        assert row['path'] not in expected
        expected[row['path']] = {k: row[k] for k in ('bytes', 'sha256')}
    actual = inventory(CAPSULE)
    assert set(actual) == set(expected) | {'checkpoint.json'}
    assert all(actual[name] == record for name, record in expected.items())
    return value, expected


def main(output):
    assert shutil.disk_usage(BASE).free >= 32 * 1024 * 1024
    output.mkdir(parents=True, exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    ticks = time.monotonic()
    def write(name, value):
        with (output / name).open('x') as stream:
            stream.write(json.dumps(value, indent=2) + '\n')
    (output / 'executed-review-source.py').write_bytes(Path(__file__).read_bytes())
    write('started.json', {'started_utc': started, 'source': identity(Path(__file__)),
                          'capsule_sha256': CAPSULE_SHA, 'new_android_execution': False})
    frozen, capsule_files = checkpoint()
    write('all-114-capsule-file-identities.json', capsule_files)
    source = CAPSULE / 'replay-source'
    preparation = json.loads((CAPSULE / 'preparation.json').read_text())
    before = json.loads((CAPSULE / 'reports/inputs-before.json').read_text())
    after = json.loads((CAPSULE / 'reports/inputs-after.json').read_text())
    assert before == after and len(before) == 81
    assert identity(CAPSULE / 'parent-checkpoint.json') == preparation['parent_checkpoint']
    assert preparation['parent_checkpoint']['sha256'] == '8c985ee7da3a2f3d0dab9a9b93cac49b07246f9f78f8b0b897144c60c085f743'
    parent = json.loads((CAPSULE / 'parent-source-identities.json').read_text())
    changes = [{'path': name, 'before': parent.get(name), 'after': before.get(name)}
               for name in sorted(set(parent) | set(before)) if parent.get(name) != before.get(name)]
    assert changes == preparation['changes'] and len(changes) == 17
    assert {row['path'] for row in changes if row['before'] is not None} == set(PARENT_PINS)
    assert len([row for row in changes if row['before'] is None]) == 15
    source_inventory = inventory(source)
    external = preparation['external_historical_archives']
    assert len(external) == 2 and len(source_inventory) == 79
    assert source_inventory == {name: row for name, row in before.items() if name not in external}
    for name, row in external.items():
        safe(name)
        assert before[name] == row
        assert identity(BASE / 'MacroDroid-Reconstruction' / name) == row
    for name, digest in SOURCE_PINS.items():
        assert source_inventory[name]['sha256'] == digest
        assert identity(CAPSULE / 'repository-overlay' / name) == source_inventory[name]
    write('complete-source-change-review.json', {'verified_source_files': 79, 'unchanged_host_inputs': 81,
        'independently_derived_changes': changes, 'external_historical_archives': external})
    delta = []
    for name, digest in PARENT_PINS.items():
        original = RAW / 'reviewed-source' / name
        assert identity(original)['sha256'] == digest
        delta.extend(difflib.unified_diff(original.read_text().splitlines(True),
                     (source / name).read_text().splitlines(True),
                     fromfile='captured-zero12/' + name, tofile='frozen-daytime13/' + name))
    (output / 'independent-central-source.diff').write_text(''.join(delta))
    host = json.loads((CAPSULE / 'reports/result.json').read_text())
    host_log = (CAPSULE / 'reports/tests.log').read_text()
    assert identity(CAPSULE / 'reports/tests.log')['sha256'] == host['log_sha256']
    assert host['status'] == 'HOST_CONTROLS_PASSED_INACTIVE' and host['exit_code'] == 0
    assert host['source_bytes_unchanged'] is True and host['android_executed'] is False
    assert host['timeout_seconds'] == 300 and host['seconds'] == 197.194609
    summaries = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', host_log, re.M)
    successes = len(re.findall(r'(?:\.\.\. |^)ok$', host_log, re.M))
    names = re.findall(r'^(test_\S+) \(([^\n]+)\) \.\.\. ', host_log, re.M)
    assert len(summaries) == 1 and int(summaries[0][0]) == successes == len(names) == 145
    assert host_log.rstrip().endswith('\nOK')
    assert not re.search(r'^(FAILED|FAIL:|ERROR:)', host_log, re.M)
    write('closed-host-test-review.json', {'tests': 145, 'individual_successes': successes,
        'summary_seconds': float(summaries[0][1]), 'command': host,
        'actual_individual_test_names': names, 'rerun_redundant_host_suite': False})
    assert identity(ARCHIVE) == ARCHIVE_ID
    archived = {}
    with zipfile.ZipFile(ARCHIVE) as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            safe(member.filename)
            assert member.filename not in archived and not stat.S_ISLNK(member.external_attr >> 16)
            with archive.open(member) as stream:
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            archived[member.filename] = {'bytes': member.file_size, 'sha256': digest}
    assert len(archived) == 2944
    raw_before = inventory(RAW)
    assert raw_before == archived
    write('all-2944-unchanged-archive-member-identities.json', archived)
    folder = RAW / 'journey'
    assert identity(folder / 'journey.json') == JOURNEY_ID
    assert identity(folder / 'comparison.json') == COMPARISON_ID
    report = json.loads((folder / 'journey.json').read_text())
    captured = json.loads((folder / 'comparison.json').read_text())
    final = json.loads((RAW / 'trigger-category-verification.json').read_text())
    assert final['status'] == 'TRIGGER_CATEGORY_TWELVE_SCREEN_DIFFERENCE'
    assert final['evidence_valid'] is True and final['journey_equal'] is False
    assert final['comparison'] == captured
    forbidden_process_events = []
    def no_process(event, args):
        if event in ('subprocess.Popen', 'os.system', 'os.posix_spawn', 'pty.spawn'):
            forbidden_process_events.append(event)
            raise RuntimeError('This review is read-only and cannot execute a guest/host subprocess')
    sys.addaudithook(no_process)
    sys.path[:0] = [str(source / 'tools/parity_journeys'), str(source / 'project')]
    import android_compare as proof
    import day_time_journey as day
    import editor_journey as runner
    import observed_journey as observed
    import trigger_category_journey as category
    base_plan = runner.PLAN
    plan_rows = []
    fixture_root = source / 'tools/parity_journeys/fixtures/day-time-trigger'
    observation = json.loads((fixture_root / 'source-observation.json').read_text())
    assert observation['sourceRunId'] == 38216299675
    assert observation['sourceCommit'] == '6331410cfd2391389270564803623079e8355ad8'
    assert observation['sourceJourney'] == JOURNEY_ID and observation['sourceComparison'] == COMPARISON_ID
    assert observation['sourceArchive'] == ARCHIVE_ID
    with day.configured_plan():
        observed.require_plan()
        twelve = category.expected_plan()
        assert runner.fingerprint(twelve) == PREFIX_SHA == day.TWELVE_PLAN_SHA256
        assert len(runner.PLAN) == 13 and runner.PLAN[:11] == twelve[:11]
        assert runner.PLAN[11] == ['after-trigger-date-category', runner.PACKAGE, day.DAY_TIME, day.DATE_TIME]
        assert runner.PLAN[12] == ['after-day-time-trigger', runner.PACKAGE, None, day.DAY_TIME]
        assert sum(step[3] == day.DAY_TIME for step in runner.PLAN) == 1
        assert sum(step[3] == day.OK for step in runner.PLAN) == 1
        new_plan = json.loads(json.dumps(runner.PLAN))
        for run, row in zip(report['runs'], observation['pairedRawSurfaces']):
            assert run['label'] == row['label'] and run['apk_sha256'] == row['apkSha256']
            shot = run['screens'][-1]
            assert shot['name'] == row['shot'] == 'after-trigger-date-category'
            for role, artifact in row['artifacts'].items():
                wanted = {k: artifact[k] for k in ('bytes', 'sha256')}
                assert shot['artifacts'][role] == {'path': artifact['source'], **wanted}
                assert identity(fixture_root / artifact['fixture']) == identity(folder / artifact['source']) == wanted
            actual = day.day_time_identity(folder, shot, proof)
            assert actual == [184, 626]
            tree = ET.fromstring(proof.artifact(folder, shot['artifacts']['hierarchy']))
            nodes = [n for n in tree.iter('node') if n.get('package') == runner.PACKAGE
                     and n.get('text') == 'Day/Time' and n.get('resource-id') == runner.PACKAGE + ':id/select_item_name']
            assert len(nodes) == 1
            parents = {child: parent for parent in tree.iter() for child in parent}
            chain = [nodes[0]]
            for _ in range(3):
                chain.append(parents[chain[-1]])
            assert chain[-1].get('bounds') == '[14,574][354,678]'
            assert [n.get('clickable') for n in chain] == ['false', 'false', 'false', 'true']
            plan_rows.append({'label': run['label'], 'resolved_center': actual,
                              'raw_chain': [dict(node.attrib) for node in chain],
                              'shot_artifacts': shot['artifacts']})
    assert runner.PLAN is base_plan
    historical = json.loads((source / 'tools/parity_journeys/fixtures/reviewed-reference-plan14.json').read_text())
    # The archived fixture may wrap its exact plan in a provenance record.
    historical_plan = historical['plan'] if isinstance(historical, dict) else historical
    assert len(historical_plan) == 14 and runner.fingerprint(historical_plan) == HISTORICAL14_SHA
    with category.configured_plan():
        observed.require_plan()
        assert runner.fingerprint(runner.PLAN) == report['plan_sha256'] == PREFIX_SHA
        replayed = runner.compare(folder, report, proof)
    assert runner.PLAN is base_plan
    write('replayed-zero12-with-frozen-daytime13-source.json', replayed)
    assert replayed == captured, 'Complete historical comparison differs under the new frozen modules'
    assert replayed['status'] == 'JOURNEY_DIFFERENCE' and replayed['journey_equal'] is False
    assert [row['changed_pixels'] for row in replayed['screens']] == [0,5,0,0,0,0,0,0,0,0,0,0]
    assert all(row['hierarchy_equal'] for row in replayed['screens'])
    assert replayed['catalog_navigation_established'] is True and replayed['trigger_selected'] is False
    assert replayed['post_crash_continuation_observed_in_both'] is True
    assert replayed['crash_free_run_established'] is False and replayed['crash_literal_messages_compared_for_equality'] is False
    assert replayed['full_runtime_1_to_1_established'] is False and replayed['masks_used'] is False
    assert replayed['macros_saved'] is False and replayed['macros_executed'] is False
    imported = {}
    for name, module in tuple(sys.modules.items()):
        path = getattr(module, '__file__', None)
        if not path:
            continue
        path = Path(path).resolve()
        if path.is_relative_to(source):
            relative = path.relative_to(source).as_posix()
            assert identity(path) == source_inventory[relative]
            imported[name] = {'path': relative, **identity(path)}
    assert {'android_compare', 'day_time_journey', 'editor_journey', 'observed_journey',
            'trigger_category_journey', 'favourite_info_journey', 'supplied_reference_journey',
            'capture_chronology'} <= set(imported)
    assert imported['observed_journey']['sha256'] == SOURCE_PINS['tools/parity_journeys/observed_journey.py']
    assert imported['editor_journey']['sha256'] == SOURCE_PINS['tools/parity_journeys/editor_journey.py']
    assert not forbidden_process_events
    assert inventory(RAW) == raw_before and identity(ARCHIVE) == ARCHIVE_ID
    assert checkpoint() == (frozen, capsule_files)
    write('actual-imported-source-identities.json', imported)
    write('observed-row-and-plan-review.json', {'twelve_plan_sha256': PREFIX_SHA,
        'thirteen_plan_sha256': runner.fingerprint(new_plan), 'historical_fourteen_plan_sha256': HISTORICAL14_SHA,
        'thirteen_plan': new_plan, 'unchanged_raw_paired_rows': plan_rows,
        'current_base_plan_restored_by_identity': runner.PLAN is base_plan,
        'new_day_time_tap_executed': False})
    result = {'schema': 1, 'status': 'FROZEN_DAYTIME13_REVIEW_AND_ACTUAL_ZERO12_REGRESSION_VERIFIED',
        'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
        'seconds': round(time.monotonic()-ticks, 6), 'reviewed_checkpoint_sha256': CAPSULE_SHA,
        'capsule_files_verified_before_and_after': 114, 'replay_source_files_verified': 79,
        'closed_host_tests_verified': 145, 'new_host_suite_execution': False,
        'source_changed_existing_files': sorted(PARENT_PINS), 'source_added_files': 15,
        'exact_observed_fixture_files_verified_against_actual_raw_capture': 12,
        'source_pins': SOURCE_PINS, 'actual_imported_source_modules': imported,
        'zero12_run_id': 38216299675, 'zero12_head_sha': '6331410cfd2391389270564803623079e8355ad8',
        'zero12_archive': ARCHIVE_ID, 'raw_files_and_archive_members_verified_before_and_after': 2944,
        'original_journey': JOURNEY_ID, 'original_comparison': COMPARISON_ID,
        'different_source_replay_full_comparison_object_equal': True,
        'historical_final_verifier_status_unchanged': final['status'],
        'historical_evidence_valid': True, 'historical_journey_equal': False,
        'historical_full_rgba_pixel_vector': [row['changed_pixels'] for row in replayed['screens']],
        'historical_crash_continuation_and_no_crash_free_claim_retained': True,
        'additional_android_actions': [], 'additional_app_builds': 0, 'active_source_changes': False,
        'raw_capture_or_archive_modified': False, 'frozen_source_modified': False,
        'large_artifact_or_source_copies_created': False, 'historical_result_relabelled_as_success': False,
        'thirteen_screen_android_result_established': False, 'full_runtime_1_to_1_established': False,
        'concrete_source_or_historical_regression_blockers_found': [],
        'scope': 'Reviewed inactive observation guard; replayed the closed actual twelve-screen evidence with exact new source hashes. This is not a new Android run or a new thirteen-screen runtime result.'}
    write('review-result.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'actual_imported_source_modules'}, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    main(parser.parse_args().output.resolve())
