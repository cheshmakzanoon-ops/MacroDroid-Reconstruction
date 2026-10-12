#!/usr/bin/env python3
"""Replay the incomplete DayTime13 run and retain its actual process failure."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
RAW = BASE / 'daytime13-run-38221713675-extracted'
OUT = BASE / 'daytime13-run-38221713675-analysis'
HEAD = 'e610d98812f3d26da732035e039a1250b8afe9f3'
PACKAGE = 'work-in-progress/day-time-trigger-workflow/01-zero-scale-workflow'
PINS = {
    '.github/workflows/editor-day-time-trigger.yml': '74ebef4583e28e345d91c8aa01c0e0723c57c13e6e209084f48e8423751ccbf3',
    PACKAGE + '/prepare_trigger_journey.py': '35ac5130001c07517e35e1bd877537f567449b27c5a7def22a05150b9465cdfb',
    PACKAGE + '/verify_trigger_journey.py': '7d4fb02599741d7f8eb521b492e77d2371d2c133b8b9e5afb11fcfe45734f9d0',
}
APKS = [
    (BASE.parent / 'recovered/automation android app', 'MacroDroid-5.67.8-original.apk', 95725918,
     '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'),
    (Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/dist/MacroDroid-5.67.8-v9-hybrid.apk'),
     'MacroDroid-5.67.8-combined-plugin-widget-hybrid.apk', 94683119,
     '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'),
]
ARCHIVE = {'bytes': 38451864, 'sha256': 'ad31af7b9fb237dbca1285a671a3e12fdcd9c3cd3754f55064055066043dffa4'}


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def write(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def inventory(receipt):
    expected = {r['path']: {k: r[k] for k in ('bytes', 'sha256')} for r in receipt['files']}
    assert len(expected) == len(receipt['files']) == 2395
    actual = {}
    for path in RAW.rglob('*'):
        assert not path.is_symlink()
        if path.is_file():
            actual[path.relative_to(RAW).as_posix()] = identity(path)
    assert actual == expected
    return actual


def artifacts(value):
    if isinstance(value, dict):
        if set(value) == {'path', 'bytes', 'sha256'}:
            yield value
        for child in value.values():
            yield from artifacts(child)
    elif isinstance(value, list):
        for child in value:
            yield from artifacts(child)


def main():
    started = datetime.now(timezone.utc).isoformat()
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(__file__, OUT / 'executed-replay-script.py')
    archive = BASE / 'daytime13-run-38221713675.zip'
    assert identity(archive) == ARCHIVE
    receipt = json.loads((BASE / 'daytime13-run-38221713675-extracted-extraction.json').read_text())
    assert receipt['run_id'] == 38221713675 and receipt['head_sha'] == HEAD and receipt['artifact_id'] == 11735470323
    original_inventory = inventory(receipt)
    assert receipt['key_scan_findings'] == ['environment/emulator-boot.log']
    boot = (RAW / 'environment/emulator-boot.log').read_text()
    assert len([line for line in boot.splitlines() if 'adb.pubkey=' in line]) == 1 and 'PRIVATE KEY' not in boot
    review_boot = re.sub(r'(?m)(^.*?adb\.pubkey=)[^\r\n]*', r'\1[EPHEMERAL ADB PUBLIC VALUE OMITTED IN REVIEW COPY]', boot)
    assert review_boot != boot
    (OUT / 'emulator-boot-public-value-omitted.review.log').write_text(review_boot)
    write('review-log-transformation.json', {
        'raw_path': 'environment/emulator-boot.log', 'raw': identity(RAW / 'environment/emulator-boot.log'),
        'review_path': 'emulator-boot-public-value-omitted.review.log',
        'review': identity(OUT / 'emulator-boot-public-value-omitted.review.log'), 'changed_lines': 1,
        'transformation': 'Only the existing ephemeral adb.pubkey value is omitted in this separately labeled review copy.',
        'raw_bytes_unchanged': True, 'raw_value_printed': False})
    for name, digest in PINS.items():
        assert identity(RAW / 'executed-inputs' / name)['sha256'] == digest
    for path, _, size, digest in APKS:
        assert identity(path) == {'bytes': size, 'sha256': digest}
    print(json.dumps({'checkpoint': '2395_RAW_FILES_AND_FIXED_APKS_VERIFIED'}), flush=True)

    omitted_bytecode = []
    with tempfile.TemporaryDirectory(prefix='macrodroid-daytime13-replay-') as temporary:
        root = Path(temporary) / 'root'
        shadow = Path(temporary) / 'artifact'
        for source in (RAW / 'executed-inputs').rglob('*'):
            if source.is_file():
                if '__pycache__' in source.parts:
                    assert source.suffix == '.pyc'
                    omitted_bytecode.append(source.relative_to(RAW).as_posix())
                    continue
                target = root / source.relative_to(RAW / 'executed-inputs')
                target.parent.mkdir(parents=True, exist_ok=True)
                os.link(source, target)
        for source in RAW.rglob('*'):
            if source.is_file():
                if '__pycache__' in source.parts:
                    assert source.suffix == '.pyc'
                    omitted_bytecode.append(source.relative_to(RAW).as_posix())
                    continue
                relative = source.relative_to(RAW).as_posix()
                target = shadow / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                if relative == 'day-time-trigger-verification.json':
                    shutil.copyfile(source, target)
                else:
                    os.link(source, target)
        for source, filename, _, _ in APKS:
            target = root / 'workspace/artifacts' / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(source, target)
        sys.path[:0] = [str(root / PACKAGE)]
        import prepare_trigger_journey as preparation
        import verify_trigger_journey as verification
        preflight = json.loads((shadow / 'input-preflight.json').read_text())
        expected = preparation.verify_prepared_inputs(root, shadow, preflight)
        assert len(expected) == 224 and preflight['github_sha'] == HEAD
        assert not any('__pycache__' in row['path'] or '__pycache__' in row['copy'] for row in expected)
        write('independently-reconstructed-224-inputs.json', expected)
        literal = verification.verify(root, shadow)
        recorded = json.loads((RAW / 'day-time-trigger-verification.json').read_text())
        omit_time = lambda value: {k: v for k, v in value.items() if k != 'verified_at_utc'}
        assert omit_time(literal) == omit_time(recorded)
        assert literal['status'] == 'DAY_TIME_TRIGGER_EVIDENCE_INCOMPLETE' and literal['evidence_valid'] is False
        assert literal['reason'] == 'ValueError: Configuration and complete journey are not in order'
        write('literal-final-verifier-replay.json', literal)

        import enable_still_animations as scales
        import day_time_journey as daytime
        import observed_journey as observed
        import capture_chronology as chronology
        import editor_journey as runner
        import android_compare as proof
        folder = shadow / 'journey'
        report = json.loads((folder / 'journey.json').read_text())
        comparison = json.loads((folder / 'comparison.json').read_text())
        with daytime.configured_plan():
            replayed = runner.compare(folder, report, proof)
        assert replayed == comparison and comparison['status'] == 'REJECTED'
        assert comparison['reason'] == 'Incomplete run or changed environment' and comparison['screens'] == []
        write('literal-captured-comparison-replay.json', replayed)
        original, candidate = report['runs']
        assert [(run['label'], run['status'], len(run['screens']), len(run['transitions'])) for run in report['runs']] == [
            ('original', 'FAILED', 5, 5), ('candidate', 'COMPLETE', 13, 12)]
        assert original['current_step'] == 'reference-promotion' and original['reason'] == "Device command failed: ['pidof', 'com.arlosoft.macrodroid']"
        assert candidate['current_step'] == 'after-day-time-trigger'
        assert [run['apk_sha256'] for run in report['runs']] == [row[3] for row in APKS]
        refs = {}
        for row in artifacts(report):
            proof.artifact(folder, row)
            assert refs.setdefault(row['path'], row) == row
        events = []
        for record in report['capture_events']:
            event = json.loads(proof.artifact(folder, record))
            for row in artifacts(event):
                proof.artifact(folder, row)
                assert refs.setdefault(row['path'], row) == row
            events.append({'record': record, 'event': event})
        write('all-recorded-capture-events.json', events)
        write('all-unique-journey-artifact-references.json', list(refs.values()))
        accepted = []
        for run in report['runs']:
            for shot in run['screens'] + [t['before'] for t in run['transitions']]:
                observed.stable_snapshot(folder, shot, proof, run['label'])
                accepted.append({'label': run['label'], 'name': shot.get('name'), 'settling': shot['settling']})
        write('independently-verified-accepted-snapshots.json', accepted)
        try:
            observed.capture_events(folder, report, proof)
        except runner.JourneyError as error:
            assert str(error) == 'Completed journey contains a rejected semantic/process acquisition'
            event_rejection = str(error)
        else:
            raise AssertionError('The original process failure was incorrectly accepted')

        failed_commands = [command for command in report['commands'] if command['argv'] == ['shell', 'pidof com.arlosoft.macrodroid'] and command['returncode'] != 0]
        assert len(failed_commands) == 1
        missing_pid = failed_commands[0]
        assert missing_pid['returncode'] == 1 and missing_pid['timed_out'] is False
        assert all(proof.artifact(folder, missing_pid[key]) == b'' for key in ('stdout', 'stderr'))
        failed_events = [item for item in events if item['event']['label'] == 'original-reference-promotion-acquisition-1']
        assert len(failed_events) == 1
        failed_event = failed_events[0]['event']
        assert failed_event['status'] == 'FAILED' and failed_event['attempts'] == [] and failed_event['error_type'] == 'JourneyError'
        assert failed_event['started_monotonic'] <= missing_pid['started_monotonic'] <= missing_pid['finished_monotonic'] <= failed_event['finished_monotonic']
        original_transition = original['transitions'][-1]
        candidate_transition = next(t for t in candidate['transitions'] if t['to'] == 'reference-promotion')
        old_pid = observed.one_pid(proof.artifact(folder, original_transition['preinput_artifacts']['pid']), proof)
        original_crash = observed.crash_observation(folder, original_transition['pre_denial_diagnostics'], candidate_transition['pre_denial_diagnostics'], old_pid, proof)
        assert old_pid == '3891' and original_crash['classification']['status'] == 'NEW_OBSERVED_FRAGMENT_FATAL_EXCEPTION'
        assert original_crash['classification']['count'] == 1
        later_crash_command = candidate_transition['pre_denial_diagnostics']['crash']
        assert original_transition['command']['finished_monotonic'] < missing_pid['started_monotonic'] < later_crash_command['started_monotonic']
        with daytime.configured_plan():
            candidate_handoff = observed.verified_handoff(folder, candidate, candidate_transition, candidate['screens'][4], candidate['screens'][5], proof)
        assert candidate_handoff['pid_replaced'] and candidate_handoff['cause'] == 'RECORDED_JAVA_FATAL_EXCEPTION'
        write('original-process-failure-and-candidate-handoff.json', {
            'original_old_pid': old_pid, 'original_input_transition': original_transition,
            'missing_pid_command': missing_pid, 'failed_capture': failed_events[0],
            'later_retained_crash_buffer_command': later_crash_command,
            'original_fatal_classified_from_exact_later_raw_buffer': original_crash,
            'original_restart_or_post_crash_continuation_observed': False,
            'candidate_verified_post_crash_handoff': candidate_handoff,
            'completed_capture_event_gate_rejection': event_rejection,
            'notification_denial_as_root_cause_established': False})

        review_captures = OUT / 'review-captures'
        review_captures.mkdir()
        def copy_shot(shot):
            for row in shot['artifacts'].values():
                target = review_captures / row['path']
                data = proof.artifact(folder, row)
                if target.exists():
                    assert target.read_bytes() == data
                else:
                    target.write_bytes(data)
        pairs = []
        for old, new in zip(original['screens'], candidate['screens']):
            assert old['name'] == new['name']
            copy_shot(old); copy_shot(new)
            a = np.asarray(Image.open(folder / old['artifacts']['screenshot']['path']).convert('RGBA'))
            b = np.asarray(Image.open(folder / new['artifacts']['screenshot']['path']).convert('RGBA'))
            assert a.shape == b.shape == (1280, 720, 4)
            yy, xx = np.where(np.any(a != b, axis=2))
            pairs.append({'name': old['name'], 'changed_rgba_pixels': len(xx),
                'xml_bytes_equal': proof.artifact(folder, old['artifacts']['hierarchy']) == proof.artifact(folder, new['artifacts']['hierarchy']),
                'png_bytes_equal': proof.artifact(folder, old['artifacts']['screenshot']) == proof.artifact(folder, new['artifacts']['screenshot']),
                'bounds_exclusive': [int(xx.min()), int(yy.min()), int(xx.max()+1), int(yy.max()+1)] if len(xx) else None,
                'all_changed_rgba_pixels': [{'x':int(x), 'y':int(y), 'original_rgba':a[y,x].tolist(), 'candidate_rgba':b[y,x].tolist()} for y,x in zip(yy,xx)],
                'original': old, 'candidate': new, 'diagnostic_only': True})
        assert len(pairs) == 5 and [pair['changed_rgba_pixels'] for pair in pairs] == [0,0,0,0,0]
        assert all(pair['xml_bytes_equal'] for pair in pairs)
        write('five-available-full-frame-pairs-diagnostic-only.json', pairs)
        terminal = candidate['screens'][-1]
        copy_shot(terminal)
        with daytime.configured_plan():
            terminal_scope = daytime.terminal_surface(folder, terminal, proof)
            daytime.input_identity(folder, candidate['screens'][-2], candidate['transitions'][-1]['before'], candidate['transitions'][-1]['action'], 'after-day-time-trigger', proof)
        observed.verify_preinput(folder, candidate['transitions'][-1], proof)
        nodes = list(ET.fromstring(proof.artifact(folder, terminal['artifacts']['hierarchy'])).iter('node'))
        selects = {}
        for name, selector in [('title', {'resource-id':runner.PACKAGE + ':id/alertTitle', 'text':'Permission Required'}),
                               ('message', {'resource-id':'android:id/message'}),
                               ('cancel', {'resource-id':'android:id/button2', 'text':'CANCEL'}),
                               ('ok', {'resource-id':'android:id/button1', 'text':'OK'})]:
            matching = [node for node in nodes if node.get('package') == runner.PACKAGE and all(node.get(k) == v for k,v in selector.items())]
            assert len(matching) == 1
            selects[name] = dict(matching[0].attrib)
        assert selects['message']['text'] == 'To use this feature MacroDroid requires permission to set exact alarms.\n\nOn the next screen please grant access to MacroDroid.'
        assert all(selects[key]['class'] == 'android.widget.Button' and selects[key]['enabled'] == selects[key]['clickable'] == 'true' for key in ('cancel','ok'))
        write('candidate-only-observed-exact-alarm-dialog.json', {
            'shot': terminal, 'verified_terminal_scope': terminal_scope, 'literal_nodes': selects,
            'observed_ok_center': [560,809], 'original_corresponding_screen_available': False,
            'permission_granted': False, 'new_android_inputs_executed_by_analysis': [],
            'trigger_configuration_confirmed': False})

        settings_folder = shadow / 'animation-settings'
        settings = json.loads((settings_folder / 'animation-scales.json').read_text())
        assert scales.verify_report(settings_folder, settings) == {key:'0' for key in scales.SCALES}
        assert len(settings['commands']) == 19 and settings['android_executed'] is True
        device_path = shadow / 'device/capture-device.json'
        device = json.loads(device_path.read_text())
        device_refs = {}
        for command in device['commands']:
            assert command['exit_code'] == 0
            for key in ('stdout','stderr'):
                row = command[key]
                proof.artifact(device_path.parent, row)
                assert row['path'] not in device_refs
                device_refs[row['path']] = row
        host = []
        for name, count in [('journey-host-tests.log',145),('animation-host-tests.log',10),('download-tests.log',6)]:
            log = (RAW / name).read_text()
            summaries = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', log, re.M)
            headers = re.findall(r'^test_\S+ \(.*\) \.\.\. ', log, re.M)
            successes = len(re.findall(r'(?:\.\.\. |^)ok$', log, re.M))
            assert len(summaries) == 1 and int(summaries[0][0]) == len(headers) == successes == count
            assert log.rstrip().endswith('\nOK')
            host.append({'path':name, **identity(RAW / name), 'tests':count, 'seconds':float(summaries[0][1]), 'individual_successes':successes})
        write('verified-host-test-summaries.json', host)
        cleanup = json.loads((RAW / 'runtime-cleanup.json').read_text())
        assert cleanup['journey_step_exit_code'] == '2' and cleanup['service_cleanup_confirmed'] is True
        assert all(cleanup[key] == '0' for key in ('diagnostic_logcat_exit_code','owned_stop_marker_exit_code','bounded_service_wait_exit_code','owned_service_exit_code'))
        modules = {}
        for module in (preparation,verification,scales,daytime,observed,chronology,runner,proof):
            path = Path(module.__file__).resolve()
            relative = str(path.relative_to(root)) if path.is_relative_to(root) else 'artifact/' + str(path.relative_to(shadow))
            modules[module.__name__] = {'private_replay_path':relative, **identity(path)}
        write('imported-exact-source-modules.json', modules)
        write('configuration-and-cleanup-summary.json', {
            'device_status':device['status'], 'device_commands':len(device['commands']),
            'confirmed_primary_signal':device['confirmed_primary_signal'], 'device_output_hashes_verified':len(device_refs),
            'demo_clock_requested':device['demo_clock_requested'], 'disable_animations_requested':device['disable_animations_requested'],
            'separate_scale_zero_commands':19, 'animation_scales':settings['observed_scales'], 'cleanup':cleanup})
    assert inventory(receipt) == original_inventory and identity(archive) == ARCHIVE
    for path, _, size, digest in APKS:
        assert identity(path) == {'bytes':size,'sha256':digest}
    write('all-2395-member-identities.json', [{'path':path, **value} for path,value in sorted(original_inventory.items())])
    result = {
        'schema':1, 'status':'INCOMPLETE_DAYTIME13_REPLAYED_WITH_ORIGINAL_PROCESS_FAILURE',
        'run_id':38221713675, 'head_sha':HEAD, 'artifact_id':11735470323, 'archive':ARCHIVE,
        'started_utc':started, 'finished_utc':datetime.now(timezone.utc).isoformat(),
        'raw_files_verified_before_and_after':2395, 'independently_reconstructed_input_copy_roles':224,
        'literal_verifier_reproduced_except_replay_timestamp':True, 'exact_captured_comparison_object_reproduced':True,
        'literal_evidence_valid':False, 'literal_comparison_status':'REJECTED', 'journey_equal':False,
        'original_recorded_screens':5, 'candidate_recorded_screens':13, 'diagnostic_paired_screen_count':5,
        'five_available_rgba_pixel_vector':[0,0,0,0,0], 'thirteen_screen_comparison_established':False,
        'accepted_snapshot_ledgers_independently_verified':len(accepted), 'capture_ledgers':len(events),
        'recorded_observations':sum(len(item['event']['attempts']) for item in events),
        'unique_referenced_journey_artifacts_checked':len(refs), 'all_raw_commands_retained':len(report['commands']),
        'original_absent_pid_returncode':1, 'original_failed_pid_capture_seconds':failed_event['seconds'],
        'original_main_fatal_confirmed_in_later_retained_buffer':True, 'original_restart_observed':False,
        'candidate_post_crash_continuation_observed':True, 'post_crash_continuation_observed_in_both':False,
        'candidate_terminal_is_exact_alarm_permission_dialog':True, 'trigger_configuration_confirmed':False,
        'host_test_summaries':host, 'source_pins':PINS,
        'unexecuted_raw_bytecode_omitted_only_from_private_replay_views':sorted(set(omitted_bytecode)),
        'new_android_actions':[], 'masks_or_pixel_tolerance_used':False, 'raw_evidence_or_apks_modified':False,
        'large_input_copies_created_for_replay':False, 'private_hardlink_replay_directory_removed':True,
        'full_runtime_1_to_1_established':False, 'crash_free_run_established':False,
    }
    write('independent-daytime13-analysis.json', result)
    print(json.dumps({key:result[key] for key in ('status','raw_files_verified_before_and_after',
        'independently_reconstructed_input_copy_roles','five_available_rgba_pixel_vector',
        'original_recorded_screens','candidate_recorded_screens','accepted_snapshot_ledgers_independently_verified',
        'unique_referenced_journey_artifacts_checked')},indent=2),flush=True)


if __name__ == '__main__':
    main()
