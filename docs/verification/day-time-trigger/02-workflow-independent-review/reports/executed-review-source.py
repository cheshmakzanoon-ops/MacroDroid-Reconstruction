#!/usr/bin/env python3
"""Read-only review of the closed Day/Time13 workflow and its actual controls."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile
import yaml

sys.dont_write_bytecode = True
ROOT = Path('/workspace/scratch/4130730d15aa')
SOURCE = ROOT / 'day-time-trigger-forward/checkpoints/03-zero-scale-thirteen-screen-workflow'
OUT = ROOT / 'day-time-trigger-review/reports/02-frozen-workflow03-review'
EXPECTED = '2510711052d2f41bde1a7a583e4bd42f1aab2e1f2001b3bd03d5e2b9eff29229'
WORKFLOW = '74ebef4583e28e345d91c8aa01c0e0723c57c13e6e209084f48e8423751ccbf3'
GUARD = '0e010cfbace03cffa6d45e8c9157402b1b68c9a392249eb2aeae39445dc57a7d'
PLAN = '42ece5a06a280186ddf9796a4524975d478263e545260674e2b1b4cf718d46fb'


def identity(path):
    assert path.is_file() and not path.is_symlink(), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def safe(name):
    p = PurePosixPath(name)
    assert p.as_posix() == name and not p.is_absolute() and '..' not in p.parts and '\\' not in name


def capsule():
    assert identity(SOURCE / 'checkpoint.json') == {'bytes': 42332, 'sha256': EXPECTED}
    value = json.loads((SOURCE / 'checkpoint.json').read_text())
    assert value['workflow_sha256'] == WORKFLOW and len(value['files']) == 13
    assert value['android_executed'] is False and value['active_changes'] is False
    names = set()
    for row in value['files']:
        safe(row['path']); assert row['path'] not in names; names.add(row['path'])
        assert identity(SOURCE / row['path']) == {k: row[k] for k in ('bytes','sha256')}
    assert {p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob('*') if p.is_file()} == names | {'checkpoint.json'}
    return value


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    (OUT / 'executed-review-source.py').write_bytes(Path(__file__).read_bytes())
    def save(name, value):
        with (OUT / name).open('x') as stream:
            stream.write(json.dumps(value, indent=2) + '\n')
    frozen = capsule()
    report = json.loads((SOURCE / 'offline-validation.json').read_text())
    assert frozen['offline_validation'] == report and report['passed'] is True
    assert report['status'] == 'OFFLINE_DAY_TIME_TRIGGER_WORKFLOW_VALIDATED'
    assert report['prepared_input_copies'] == 224 and report['android_executed'] is False
    assert report['workflow_sha256'] == WORKFLOW and report['source_apks_and_preserved_tool_bytes_unchanged'] is True
    manifest = json.loads((SOURCE / 'offline-evidence-manifest.json').read_text())
    rows = manifest['files']; assert len(rows) == manifest['file_count'] == 5873
    index = {row['path']: row for row in rows}; assert len(index) == len(rows)
    external = manifest['exact_already_published_runtime_inputs']
    assert set(external) == {
        '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800',
        '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182',
        '6fbed5edaddcfbee99a3ae6e7208c8654c6cb2bedb4ed5cbbf4e154d7d38a745'}
    for digest, row in external.items():
        assert row['sha256'] == digest
        assert identity(Path(row['source'])) == {k: row[k] for k in ('bytes','sha256')}
    archive_rows = {}
    for row in rows:
        safe(row['path']); assert type(row['mode']) is int and 0 <= row['mode'] <= 0o777
        wanted = {k: row[k] for k in ('bytes','sha256')}
        if 'archive_member' in row:
            assert archive_rows.setdefault(row['archive_member'], wanted) == wanted
        else:
            assert set(row) == {'path','mode','bytes','sha256','external_input_sha256'}
            assert wanted == {k: external[row['external_input_sha256']][k] for k in ('bytes','sha256')}
    assert len(archive_rows) == manifest['unique_archived_payloads'] == 231
    contents = {}
    with tarfile.open(SOURCE / 'offline-evidence-blobs.tar.gz', 'r:gz') as archive:
        for member in archive:
            safe(member.name); assert member.isfile() and member.name not in contents
            raw = archive.extractfile(member).read()
            actual = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
            assert actual == archive_rows[member.name]
            assert member.name == 'blobs/sha256/' + actual['sha256'] + '.bin'
            contents[member.name] = raw
    assert set(contents) == set(archive_rows)
    assert len(manifest['inert_symlink_controls']) == 1
    inert = manifest['inert_symlink_controls'][0]
    assert inert['restored_as_symlink'] is False and inert['path'] not in index
    def raw(name):
        return contents[index[name]['archive_member']]
    commands = report['commands']; assert len(commands) == len({c['label'] for c in commands}) == 45
    for command in commands:
        folder = 'commands/' + command['label'] + '/'
        assert json.loads(raw(folder + 'command.json')) == command
        assert not command['timed_out'] and command['android_executed'] is False
        assert folder + 'stdout.txt' in index and folder + 'stderr.txt' in index
    hosts = []
    for number, count in ((0,6),(1,145),(2,10)):
        name = 'packaged-host-controls-' + str(number)
        command = next(c for c in commands if c['label'] == name); assert command['exit_code'] == 0
        text = raw('commands/' + name + '/stdout.txt').decode()
        matches = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', text, re.M)
        successes = len(re.findall(r'(?:\.\.\. |^)ok$', text, re.M))
        assert len(matches) == 1 and int(matches[0][0]) == successes == count and text.rstrip().endswith('\nOK')
        hosts.append({'label': name, 'tests': count, 'individual_successes': successes, 'seconds': float(matches[0][1])})
    faults = [r for r in report['checks'] if isinstance(r,dict) and 'inventory_fault' in r]
    assert len(faults) == 12
    for fault in faults:
        assert fault['rejected_before_copied_code_or_aapt2_execution'] is True
        assert [v['phase'] for v in fault['outcomes']] == ['materialized','final']
        assert [v['exit_code'] for v in fault['outcomes']] == [1,2]
        for outcome in fault['outcomes']:
            label = 'inventory-' + fault['inventory_fault'] + '-' + outcome['phase']
            assert next(c for c in commands if c['label'] == label)['exit_code'] == outcome['exit_code']
            filename = 'materialized-inputs.json' if outcome['phase'] == 'materialized' else 'day-time-trigger-verification.json'
            value = json.loads(raw('inventory-faults/' + fault['inventory_fault'] + '/ci-day-time-trigger/' + filename))
            assert value['reason'] == outcome['reason']
    for name in ('changed-original-manifest','changed-active-manifest','changed-chronology-guard',
                 'changed-animation-helper','symlinked-runtime-input','changed-reviewed-finalizer','existing-output'):
        assert next(c for c in commands if c['label'] == name)['exit_code'] == 1
    cleanups = []
    for name, code, clean in (('clean',0,True),('failed-journey',7,True),('failed-service',1,False)):
        command = next(c for c in commands if c['label'] == 'owned-cleanup-' + name)
        value = json.loads(raw('cleanup-controls/' + name + '/ci-day-time-trigger/runtime-cleanup.json'))
        assert command['exit_code'] == code and value['service_cleanup_confirmed'] is clean
        cleanups.append({'case':name,'actual_exit_code':code,'recorded_cleanup':value})
    workflow_path = SOURCE / '.github/workflows/editor-day-time-trigger.yml'
    assert identity(workflow_path)['sha256'] == WORKFLOW
    document = yaml.load(workflow_path.read_text(), Loader=yaml.BaseLoader)
    assert document['permissions'] == {'contents':'read'}
    assert set(document['on']) == {'push','workflow_dispatch'}
    assert document['on']['push']['paths'] == ['.github/workflows/editor-day-time-trigger.yml',
        'work-in-progress/day-time-trigger-workflow/01-zero-scale-workflow/**']
    job = document['jobs']['editor-day-time-trigger']; steps = job['steps']
    assert len(steps) == 8 and job['timeout-minutes'] == '75'
    assert steps[0]['uses'] == 'actions/checkout@11d5960a326750d5838078e36cf38b85af677262'
    assert steps[0]['with']['persist-credentials'] == 'false'
    assert steps[-1]['uses'] == 'actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02'
    assert steps[-1]['if'] == steps[-2]['if'] == 'always()'
    assert steps[-1]['with']['path'] == 'ci-day-time-trigger/' and steps[-1]['with']['include-hidden-files'] == 'true'
    assert steps[-1]['with']['if-no-files-found'] == 'error'
    assert len([s for s in steps if 'run' in s]) == 6
    runtime = next(s['run'] for s in steps if s['name'].startswith('Observe the thirteen'))
    assert runtime.count('python3 tools/android/runtime_job.py') == 3
    assert '--id day-time-trigger-thirteen-screen --timeout 2400 --' in runtime
    assert 'reviewed-source/tools/parity_journeys/day_time_journey.py"' in runtime
    assert '--accept-package-data-removal --observe-denial-handoff --settle-full-frames' in runtime
    assert '--avd MacroDroid_API35_Disposable --port 5560 --acceleration on' in runtime
    assert 'touch ci-day-time-trigger/environment/queue/STOP' in runtime
    assert 'timeout 60s tail --pid="$trigger_service_pid" -f /dev/null' in runtime
    assert '--demo-clock 1200' in runtime
    spec = importlib.util.spec_from_file_location('reviewed_daytime_preparation', SOURCE / 'prepare_trigger_journey.py')
    preparation = importlib.util.module_from_spec(spec); spec.loader.exec_module(preparation)
    assert preparation.PINS[preparation.GUARD + '/checkpoint.json'] == GUARD
    assert preparation.WORKFLOW == '.github/workflows/editor-day-time-trigger.yml'
    root = ROOT / 'day-time-trigger-forward/workflow-01/reports/validation-01/private-inputs'
    output = root / 'ci-day-time-trigger'
    preflight = json.loads((output / 'input-preflight.json').read_text())
    expected = preparation.verify_prepared_inputs(root, output, preflight)
    assert len(expected) == 224 and preflight['plan_sha256'] == PLAN and preflight['requested_scales'] == '0'
    assert expected == json.loads(raw('private-inputs/ci-day-time-trigger/input-preflight.json'))['files']
    assert preparation.APKS[1][2:] == (94683119, '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182')
    assert capsule() == frozen
    for row in external.values():
        assert identity(Path(row['source'])) == {k:row[k] for k in ('bytes','sha256')}
    save('all-231-archive-payload-identities.json', archive_rows)
    save('all-224-reconstructed-input-roles.json', expected)
    save('all-45-closed-command-records.json', commands)
    save('all-rejection-and-cleanup-results.json', {'inventory_faults':faults,'cleanups':cleanups,'host_summaries':hosts})
    result = {'schema':1,'status':'CLOSED_DAYTIME13_WORKFLOW_REVIEW_SUPPORTED_FOR_SEPARATE_RUNTIME',
        'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
        'source_checkpoint_sha256':EXPECTED,'workflow_sha256':WORKFLOW,'guard_checkpoint_sha256':GUARD,
        'plan_sha256':PLAN,'workflow_capsule_files_verified':13,'offline_evidence_regular_paths_verified':5873,
        'archived_unique_payloads_verified':231,'source_copy_roles_reconstructed':224,
        'actual_closed_commands_and_logs_verified':45,'host_summaries':hosts,
        'all_12_inventory_faults_rejected_at_both_boundaries':True,'all_6_input_faults_and_existing_output_rejected':True,
        'all_3_owned_cleanup_results_verified':True,'inert_symlink_not_restored':True,
        'new_android_execution':False,'new_application_build':False,'new_full_host_suite_execution':False,
        'active_source_or_workflow_changes':False,'raw_or_frozen_inputs_modified':False,
        'large_input_copies_created':False,'scope_requires_13_screens_and_12_inputs_per_apk':True,
        'scope_requires_type_tapped_and_configuration_unconfirmed':True,
        'full_pixels_hierarchies_chronology_and_process_scope_unchanged':True,
        'only_independent_new_workflow_path_is_proposed':True,'historical_five_pixel_failure_unchanged':True,
        'thirteen_screen_runtime_result_pending':True,'full_runtime_1_to_1_established':False,
        'concrete_review_blockers_found':[]}
    save('review-result.json',result)
    print(json.dumps(result,indent=2),flush=True)


if __name__ == '__main__':
    main()
