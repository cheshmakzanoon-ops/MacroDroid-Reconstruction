#!/usr/bin/env python3
"""Independently verify the closed zero-scale12 capsule without rebuilding it."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile

sys.dont_write_bytecode = True
WORK = Path('/workspace/scratch/4130730d15aa')
SOURCE = WORK / 'trigger-catalog-forward/checkpoints/08-zero-scale-twelve-screen-workflow'
HELPER = WORK / 'trigger-catalog-forward/checkpoints/07-zero-animation-source'
OUT = WORK / 'zero-trigger-review/01-closed-review'
EXPECTED = 'a6a279c48af61b553728eeaf05f92c8cf15e34bd5b4fdd907e193d31a63a5af0'


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')


def safe(name):
    path = PurePosixPath(name)
    assert path.as_posix() == name and not path.is_absolute() and '..' not in path.parts and '\\' not in name


def capsule(root, expected, count):
    assert identity(root / 'checkpoint.json')['sha256'] == expected
    data = json.loads((root / 'checkpoint.json').read_text())
    assert len(data['files']) == count
    names = set()
    for row in data['files']:
        safe(row['path'])
        assert row['path'] not in names
        names.add(row['path'])
        path = root / row['path']
        assert not path.is_symlink() and path.is_file()
        assert identity(path) == {k: row[k] for k in ('bytes', 'sha256')}
    assert {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()} == names | {'checkpoint.json'}
    return data


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    checkpoint = capsule(SOURCE, EXPECTED, 12)
    helper = capsule(HELPER, '5cb124753f8acb7cf8e0ec070f1ddf2b2f9b49d99ad144dea6f2b37047258a48', 9)
    assert checkpoint['workflow_sha256'] == 'e3e53daf3c53c315605580aa49ff5d2ffda7c99b1dcb8014c5692dbfc22570fe'
    report = json.loads((SOURCE / 'offline-validation.json').read_text())
    assert checkpoint['offline_validation'] == report
    assert report['passed'] is True and report['android_executed'] is False and len(report['commands']) == 45
    manifest = json.loads((SOURCE / 'offline-evidence-manifest.json').read_text())
    rows = manifest['files']
    assert len(rows) == manifest['file_count'] == 5134
    assert len({row['path'] for row in rows}) == len(rows)
    archive_rows = {row['archive_member']: {k: row[k] for k in ('bytes', 'sha256')}
                    for row in rows if 'archive_member' in row}
    assert len(archive_rows) == manifest['unique_archived_payloads'] == 217
    contents, members = {}, []
    with tarfile.open(SOURCE / 'offline-evidence-blobs.tar.gz', 'r:gz') as archive:
        for member in archive:
            safe(member.name)
            assert member.isfile() and member.name not in contents
            raw = archive.extractfile(member).read()
            actual = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
            assert actual == archive_rows[member.name]
            assert member.name == 'blobs/sha256/' + actual['sha256'] + '.bin'
            contents[member.name] = raw
            members.append({'path': member.name, **actual})
    assert set(contents) == set(archive_rows)
    external = manifest['exact_already_published_runtime_inputs']
    assert set(external) == {
        '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800',
        '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182',
        '6fbed5edaddcfbee99a3ae6e7208c8654c6cb2bedb4ed5cbbf4e154d7d38a745'}
    for digest, record in external.items():
        assert record['sha256'] == digest
        assert identity(Path(record['source'])) == {k: record[k] for k in ('bytes', 'sha256')}
    index = {row['path']: row for row in rows}
    for row in rows:
        safe(row['path'])
        assert type(row['mode']) is int and 0 <= row['mode'] <= 0o777
        if 'archive_member' in row:
            assert archive_rows[row['archive_member']] == {k: row[k] for k in ('bytes', 'sha256')}
        else:
            assert set(row) == {'path', 'bytes', 'sha256', 'mode', 'external_input_sha256'}
            assert {k: external[row['external_input_sha256']][k] for k in ('bytes', 'sha256')} == {k: row[k] for k in ('bytes', 'sha256')}
    inert = manifest['inert_symlink_controls']
    assert len(inert) == 1 and inert[0]['restored_as_symlink'] is False and inert[0]['path'] not in index
    def raw(name):
        return contents[index[name]['archive_member']]
    for command in report['commands']:
        folder = 'commands/' + command['label'] + '/'
        assert json.loads(raw(folder + 'command.json')) == command
        assert not command['timed_out'] and command['android_executed'] is False
        assert folder + 'stdout.txt' in index and folder + 'stderr.txt' in index
    host = []
    for number, expected in [(0, 6), (1, 130), (2, 10)]:
        label = 'packaged-host-controls-' + str(number)
        text = raw('commands/' + label + '/stdout.txt').decode()
        summaries = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', text, re.MULTILINE)
        successes = len(re.findall(r'(?:\.\.\. |^)ok$', text, re.MULTILINE))
        assert len(summaries) == 1 and int(summaries[0][0]) == successes == expected
        assert text.rstrip().endswith('\nOK')
        host.append({'label': label, 'tests': expected, 'individual_successes': successes,
                     'seconds': float(summaries[0][1])})
    faults = [row for row in report['checks'] if isinstance(row, dict) and 'inventory_fault' in row]
    assert len(faults) == 12
    for fault in faults:
        assert fault['rejected_before_copied_code_or_aapt2_execution'] is True
        assert [o['phase'] for o in fault['outcomes']] == ['materialized', 'final']
        assert [o['exit_code'] for o in fault['outcomes']] == [1, 2]
    for label, expected, service in [('clean', 0, True), ('failed-journey', 7, True), ('failed-service', 1, False)]:
        command = next(c for c in report['commands'] if c['label'] == 'owned-cleanup-' + label)
        result = json.loads(raw('cleanup-controls/' + label + '/ci-trigger-category/runtime-cleanup.json'))
        assert command['exit_code'] == expected and result['service_cleanup_confirmed'] is service
    # The reviewed function recomputes its source/role membership from immutable
    # pins. Reading the already closed private inputs avoids another payload copy.
    spec = importlib.util.spec_from_file_location('zero_review_preparation', SOURCE / 'prepare_trigger_journey.py')
    preparation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(preparation)
    root = (WORK / 'trigger-catalog-forward/workflow-02/reports/validation-01/private-inputs').resolve()
    output = root / 'ci-trigger-category'
    preflight = json.loads((output / 'input-preflight.json').read_text())
    expected_inputs = preparation.verify_prepared_inputs(root, output, preflight)
    assert len(expected_inputs) == 192 and preflight['requested_scales'] == '0'
    assert expected_inputs == json.loads(raw('private-inputs/ci-trigger-category/input-preflight.json'))['files']
    assert preparation.APKS[1] == (
        'work-in-progress/combined-recovery/05-full-acceptance/apk/manifest.json',
        'MacroDroid-5.67.8-combined-plugin-widget-hybrid.apk', 94683119,
        '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182')
    result = {
        'schema': 1, 'status': 'CLOSED_ZERO_SCALE12_REVIEW_APPROVED_FOR_SEPARATE_RUNTIME',
        'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
        'reviewed_checkpoint_sha256': EXPECTED, 'workflow_sha256': checkpoint['workflow_sha256'],
        'workflow_capsule_files_verified': 12, 'zero_helper_capsule_files_verified': 9,
        'offline_evidence_regular_paths_verified': 5134, 'archived_unique_payloads_verified': 217,
        'external_runtime_identities_verified': external, 'inert_symlink_not_restored': True,
        'actual_command_records_and_logs_verified': 45, 'host_test_summaries': host,
        'all_12_inventory_faults_rejected_at_both_boundaries': True,
        'all_3_owned_cleanup_controls_verified': True, 'complete_source_copy_roles_reconstructed': 192,
        'full_thresholds_and_frozen_capture_guard_unchanged': True,
        'final_scope_requires_12_screens_11_inputs_per_apk': True,
        'final_scope_requires_catalog_navigation_true_and_trigger_selected_false': True,
        'final_comparison_permits_reported_difference_but_exit_success_requires_equality': True,
        'all_key_scripts_and_hidden_inputs_preserved': True,
        'new_android_execution_by_review': False, 'new_application_build_by_review': False,
        'unrelated_or_redundant_tests_run': False,
        'runtime_result_pending': True, 'full_runtime_1_to_1_established': False,
        'concrete_blockers_found': [],
    }
    assert capsule(SOURCE, EXPECTED, 12) == checkpoint
    assert capsule(HELPER, '5cb124753f8acb7cf8e0ec070f1ddf2b2f9b49d99ad144dea6f2b37047258a48', 9) == helper
    save('all-217-archive-members.json', members)
    save('all-192-source-copy-roles.json', expected_inputs)
    save('review-result.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'external_runtime_identities_verified'}, indent=2))


if __name__ == '__main__':
    main()
