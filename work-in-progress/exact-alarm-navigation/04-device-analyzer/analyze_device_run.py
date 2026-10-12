#!/usr/bin/env python3
"""Independently replay one exact fourteen-screen exact-alarm CI artifact without Android actions."""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile

import numpy as np
from PIL import Image

PACKAGE = 'work-in-progress/exact-alarm-navigation-workflow/01-fourteen-screen'
PINS = {
    '.github/workflows/editor-exact-alarm-navigation.yml': '575a8ccb4909ba526e4c29ba7695cc8486538885b017f29093c00344214bed1f',
    PACKAGE + '/prepare_trigger_journey.py': 'd59a45832aa2bf40530dc0d057339cac564ce29d4c3cfe42e8cf02505c060ad7',
    PACKAGE + '/verify_trigger_journey.py': '80dd3f2db42cd154e7ee0df037fbf48bf63d87268b1128e33bd55812286fa40e',
}
APK_PINS = [
    ('MacroDroid-5.67.8-original.apk', 95725918, '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'),
    ('MacroDroid-5.67.8-combined-plugin-widget-hybrid.apk', 94683119, '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'),
]


def require(value, message):
    if not value:
        raise ValueError(message)


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def save(folder, name, value):
    path = folder / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def scan_raw(root):
    result = {}
    for path in sorted(root.rglob('*')):
        require(not path.is_symlink(), 'Symlink in the raw evidence inventory')
        if path.is_file():
            require(stat.S_ISREG(path.stat().st_mode), 'Non-regular raw evidence file')
            result[path.relative_to(root).as_posix()] = identity(path)
    return result


def verify_archive(archive_path, raw):
    expected = {}
    with zipfile.ZipFile(archive_path) as archive:
        for row in archive.infolist():
            require(not stat.S_ISLNK(row.external_attr >> 16), 'ZIP symlink is not a raw file')
            if row.is_dir():
                continue
            name = PurePosixPath(row.filename)
            require(not name.is_absolute() and '..' not in name.parts and '\\' not in row.filename
                    and name.as_posix() == row.filename and row.filename not in expected,
                    'Noncanonical or duplicated ZIP member')
            with archive.open(row) as stream:
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            expected[row.filename] = {'bytes': row.file_size, 'sha256': digest}
    require(scan_raw(raw) == expected, 'Raw inventory differs from the complete ZIP payloads')
    return expected


def references(value):
    if isinstance(value, dict):
        if set(value) == {'path', 'bytes', 'sha256'}:
            yield value
        for item in value.values():
            yield from references(item)
    elif isinstance(value, list):
        for item in value:
            yield from references(item)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw', type=Path, required=True)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--archive-sha256', required=True)
    parser.add_argument('--run-id', type=int, required=True)
    parser.add_argument('--artifact-id', type=int, required=True)
    parser.add_argument('--head', required=True)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw, archive, output = [path.resolve() for path in (args.raw, args.archive, args.output)]
    apks = [args.original.resolve(), args.candidate.resolve()]
    output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(Path(__file__), output / 'executed-replay-script.py')
    result = {'schema': 1, 'status': 'INDEPENDENT_REPLAY_NOT_COMPLETED', 'analysis_passed': False,
              'run_id': args.run_id, 'artifact_id': args.artifact_id, 'head_sha': args.head,
              'started_utc': datetime.now(timezone.utc).isoformat(), 'new_android_actions': [],
              'full_runtime_1_to_1_established': False, 'crash_free_run_established': False,
              'masks_or_pixel_tolerance_used': False}
    before = None
    archive_before = None
    omitted_bytecode = set()
    transports = []
    try:
        require(re.fullmatch('[0-9a-f]{40}', args.head) is not None, 'Exact CI commit is required')
        require(args.run_id > 0 and args.artifact_id > 0, 'Actual CI run and artifact identifiers are required')
        archive_before = identity(archive)
        require(archive_before['sha256'] == args.archive_sha256, 'Downloaded artifact ZIP changed')
        before = verify_archive(archive, raw)
        result['raw_archive'] = archive_before
        save(output, 'raw-file-identities-before.json', before)
        for name, expected in PINS.items():
            require(identity(raw / 'executed-inputs' / name)['sha256'] == expected,
                    'Executed workflow helper changed: ' + name)
        for path, (_, size, digest) in zip(apks, APK_PINS):
            require(identity(path) == {'bytes': size, 'sha256': digest}, 'Exact compared APK changed')
        boot = raw / 'environment/emulator-boot.log'
        if boot.is_file():
            text = boot.read_text()
            review, count = re.subn(r'(?m)(^.*?adb\.pubkey=)[^\r\n]*',
                r'\1[EPHEMERAL ADB PUBLIC VALUE OMITTED IN REVIEW COPY]', text)
            if count:
                target = output / 'emulator-boot-public-value-omitted.review.log'
                target.write_text(review)
                save(output, 'review-log-transformation.json', {
                    'raw': identity(boot), 'review': identity(target), 'changed_lines': count,
                    'only_existing_ephemeral_adb_public_value_omitted_in_review_copy': True,
                    'raw_bytes_unchanged': True, 'raw_value_printed': False})
        print('Complete raw ZIP inventory and fixed workflow/APKs verified', flush=True)
        with tempfile.TemporaryDirectory(prefix='exact-alarm-device-replay-') as temporary, ExitStack() as configured_scope:
            private = Path(temporary)
            root, shadow = private / 'root', private / 'artifact'
            def transfer(source, target, *, writable=False):
                target.parent.mkdir(parents=True, exist_ok=True)
                if not writable and source.stat().st_dev == private.stat().st_dev:
                    os.link(source, target)
                    mode = 'read-only-hardlink-view'
                else:
                    shutil.copy2(source, target)
                    mode = 'private-byte-copy'
                require(identity(target) == identity(source), 'Private replay input transport changed')
                return mode
            for source in (raw / 'executed-inputs').rglob('*'):
                if not source.is_file():
                    continue
                if '__pycache__' in source.parts:
                    require(source.suffix == '.pyc', 'Unexpected bytecode directory member')
                    omitted_bytecode.add(source.relative_to(raw).as_posix())
                    continue
                transfer(source, root / source.relative_to(raw / 'executed-inputs'))
            for source in raw.rglob('*'):
                if not source.is_file():
                    continue
                if '__pycache__' in source.parts:
                    require(source.suffix == '.pyc', 'Unexpected bytecode directory member')
                    omitted_bytecode.add(source.relative_to(raw).as_posix())
                    continue
                relative = source.relative_to(raw).as_posix()
                transfer(source, shadow / relative, writable=relative == 'exact-alarm-navigation-verification.json')
            for source, (filename, _, _) in zip(apks, APK_PINS):
                target = root / 'workspace/artifacts' / filename
                transports.append({'source': str(source), 'private_role': str(target.relative_to(private)),
                                   'transport': transfer(source, target), **identity(source)})
            sys.dont_write_bytecode = True
            sys.path.insert(0, str(root / PACKAGE))
            import prepare_trigger_journey as preparation
            import verify_trigger_journey as verification
            preflight = json.loads((shadow / 'input-preflight.json').read_text())
            prepared = preparation.verify_prepared_inputs(root, shadow, preflight)
            require(len(prepared) == 295 and preflight['github_sha'] == args.head,
                    'Prepared input role count or CI revision differs')
            save(output, 'independently-reconstructed-295-inputs.json', prepared)
            literal = verification.verify(root, shadow)
            recorded = json.loads((raw / 'exact-alarm-navigation-verification.json').read_text())
            without_time = lambda item: {key: value for key, value in item.items() if key != 'verified_at_utc'}
            save(output, 'literal-final-verifier-replay.json', literal)
            require(without_time(literal) == without_time(recorded), 'Final verifier replay differs beyond its new timestamp')

            import enable_still_animations as scales
            import exact_alarm_journey as alarm
            import exact_alarm_readiness as readiness
            import observed_journey as observed
            import capture_chronology as chronology
            import editor_journey as runner
            import android_compare as proof
            configured_scope.enter_context(alarm.configured_plan())
            folder = shadow / 'journey'
            report = json.loads((folder / 'journey.json').read_text())
            recorded_comparison = json.loads((folder / 'comparison.json').read_text())
            alarm.require_navigation_policy(report)
            readiness.require_policy(report)
            replayed = runner.compare(folder, report, proof)
            require(replayed == recorded_comparison, 'Captured whole comparison object did not reproduce')
            save(output, 'literal-captured-comparison-replay.json', replayed)
            runs = report.get('runs', [])
            require([run['label'] for run in runs] == ['original', 'candidate']
                    and [run['apk_sha256'] for run in runs] == [row[2] for row in APK_PINS],
                    'Actual run order or compared APKs differ')
            all_refs, json_artifacts, pending = {}, {}, list(references(report))
            while pending:
                reference = pending.pop()
                name = reference['path']
                data = proof.artifact(folder, reference)
                if name in all_refs:
                    require(all_refs[name] == reference, 'One path has conflicting artifact identities')
                    continue
                all_refs[name] = reference
                if name.endswith('.json'):
                    value = json.loads(data)
                    json_artifacts[name] = value
                    pending.extend(references(value))
            save(output, 'all-unique-journey-artifact-references.json', sorted(all_refs.values(), key=lambda row: row['path']))
            events = [{'record': row, 'event': json.loads(proof.artifact(folder, row))} for row in report['capture_events']]
            save(output, 'all-recorded-capture-events.json', events)
            accepted = []
            for run in runs:
                for shot in run['screens'] + [transition['before'] for transition in run['transitions']]:
                    observed.stable_snapshot(folder, shot, proof, run['label'])
                    accepted.append({'label': run['label'], 'name': shot.get('name'), 'settling': shot['settling']})
            save(output, 'independently-verified-accepted-snapshots.json', accepted)
            phase_inspections = []
            for run in runs:
                for index, transition in enumerate(run['transitions']):
                    if readiness.REFERENCE_KEY not in transition:
                        continue
                    reference = transition[readiness.REFERENCE_KEY]
                    phase = json.loads(proof.artifact(folder, reference))
                    row = {'label': run['label'], 'transition_index': index, 'reference': reference,
                           'raw_phase': phase, 'inspection_scope': 'Raw phase only; full run binding is determined by the complete comparison'}
                    try:
                        readiness.verify_phase(folder, phase, proof)
                        row['ready_phase_structure_passed'] = True
                    except runner.JourneyError as error:
                        row.update(ready_phase_structure_passed=False, phase_rejection=str(error))
                    phase_inspections.append(row)
            save(output, 'raw-readiness-phase-inspection.json', phase_inspections)
            try:
                observed.capture_events(folder, report, proof)
                event_gate = {'passed': True}
            except runner.JourneyError as error:
                event_gate = {'passed': False, 'reason': str(error)}
            save(output, 'capture-event-gate-observation.json', event_gate)

            review = output / 'review-captures'
            review.mkdir()
            def copy_shot(shot):
                for reference in shot['artifacts'].values():
                    target = review / reference['path']
                    data = proof.artifact(folder, reference)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if target.exists():
                        require(target.read_bytes() == data, 'Conflicting review capture role')
                    else:
                        target.write_bytes(data)
            pairs = []
            for original, candidate in zip(runs[0]['screens'], runs[1]['screens']):
                require(original['name'] == candidate['name'], 'Available paired screen order differs')
                copy_shot(original)
                copy_shot(candidate)
                a = np.asarray(Image.open(folder / original['artifacts']['screenshot']['path']).convert('RGBA'))
                b = np.asarray(Image.open(folder / candidate['artifacts']['screenshot']['path']).convert('RGBA'))
                require(a.shape == b.shape == (1280, 720, 4), 'Full-frame dimensions changed')
                yy, xx = np.where(np.any(a != b, axis=2))
                count = len(xx)
                row = {'name': original['name'], 'changed_rgba_pixels': count,
                       'xml_bytes_equal': proof.artifact(folder, original['artifacts']['hierarchy']) == proof.artifact(folder, candidate['artifacts']['hierarchy']),
                       'png_bytes_equal': proof.artifact(folder, original['artifacts']['screenshot']) == proof.artifact(folder, candidate['artifacts']['screenshot']),
                       'bounds_exclusive': [int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1] if count else None,
                       'original': original, 'candidate': candidate, 'diagnostic_only': True,
                       'all_changed_pixels_embedded': count <= 512, 'complete_source_images_retained': True}
                if count <= 512:
                    row['all_changed_rgba_pixels'] = [{'x': int(x), 'y': int(y), 'original_rgba': a[y, x].tolist(),
                                                       'candidate_rgba': b[y, x].tolist()} for y, x in zip(yy, xx)]
                pairs.append(row)
            save(output, 'all-available-full-frame-pairs-diagnostic-only.json', pairs)
            terminals = []
            for run in runs:
                if not run['screens']:
                    continue
                shot = run['screens'][-1]
                copy_shot(shot)
                nodes = [dict(node.attrib) for node in ET.fromstring(proof.artifact(folder, shot['artifacts']['hierarchy'])).iter('node')]
                terminals.append({'label': run['label'], 'run_status': run['status'], 'shot': shot, 'literal_nodes': nodes,
                                  'new_input_executed_by_analysis': False})
            save(output, 'observed-terminal-surfaces.json', terminals)
            settings_folder = shadow / 'animation-settings'
            settings = json.loads((settings_folder / 'animation-scales.json').read_text())
            require(scales.verify_report(settings_folder, settings) == {key: '0' for key in scales.SCALES}
                    and len(settings['commands']) == 19 and settings['android_executed'] is True,
                    'Nineteen actual zero-scale commands did not verify')
            device_path = shadow / 'device/capture-device.json'
            device = json.loads(device_path.read_text())
            device_refs = set()
            for command in device['commands']:
                require(command['exit_code'] == 0, 'Device preparation command failed')
                for stream in ('stdout', 'stderr'):
                    reference = command[stream]
                    proof.artifact(device_path.parent, reference)
                    require(reference['path'] not in device_refs, 'Reused device command stream')
                    device_refs.add(reference['path'])
            host = []
            for name, count in [('journey-host-tests.log', 209), ('animation-host-tests.log', 10), ('download-tests.log', 6)]:
                text = (raw / name).read_text()
                summaries = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', text, re.M)
                headers = re.findall(r'^test_\S+ \(.*\) \.\.\. ', text, re.M)
                successes = len(re.findall(r'(?:\.\.\. |^)ok$', text, re.M))
                require(len(summaries) == 1 and int(summaries[0][0]) == len(headers) == successes == count
                        and text.rstrip().endswith('\nOK'), 'Actual hosted test log is incomplete: ' + name)
                host.append({'path': name, **identity(raw / name), 'tests': count, 'individual_successes': successes,
                             'seconds': float(summaries[0][1])})
            save(output, 'verified-host-test-summaries.json', host)
            cleanup = json.loads((raw / 'runtime-cleanup.json').read_text())
            require(cleanup['service_cleanup_confirmed'] is True
                    and all(cleanup[key] == '0' for key in ('diagnostic_logcat_exit_code', 'owned_stop_marker_exit_code',
                        'bounded_service_wait_exit_code', 'owned_service_exit_code')), 'Owned runtime cleanup did not complete')
            modules = {}
            for module in (preparation, verification, scales, alarm, readiness, observed, chronology, runner, proof):
                path = Path(module.__file__).resolve()
                require(path.is_relative_to(private), 'Replay imported an unbound project module')
                modules[module.__name__] = {'private_replay_path': path.relative_to(private).as_posix(), **identity(path)}
            save(output, 'imported-exact-source-modules.json', modules)
            save(output, 'configuration-and-cleanup-summary.json', {
                'device_status': device['status'], 'device_commands': len(device['commands']),
                'verified_device_streams': len(device_refs), 'demo_clock_requested': device['demo_clock_requested'],
                'disable_animations_requested': device['disable_animations_requested'],
                'separate_scale_zero_commands': 19, 'animation_scales': settings['observed_scales'], 'cleanup': cleanup})
            result.update(status='EXACT_ALARM_DEVICE_ARTIFACT_REPLAYED', analysis_passed=True,
                literal_verifier_reproduced_except_replay_timestamp=True, exact_captured_comparison_object_reproduced=True,
                literal_evidence_valid=literal['evidence_valid'], literal_status=literal['status'],
                literal_comparison_status=replayed['status'], journey_equal=replayed.get('journey_equal', False),
                independently_reconstructed_input_copy_roles=295,
                recorded_runs=[{'label': run['label'], 'status': run['status'], 'screens': len(run['screens']),
                                'transitions': len(run['transitions']), 'current_step': run.get('current_step'),
                                'reason': run.get('reason')} for run in runs],
                available_paired_screen_count=len(pairs), diagnostic_rgba_pixel_vector=[row['changed_rgba_pixels'] for row in pairs],
                accepted_snapshot_ledgers_independently_verified=len(accepted), capture_ledgers=len(events),
                recorded_frame_observations=sum(len(item['event']['attempts']) for item in events),
                unique_referenced_journey_artifacts_checked=len(all_refs), all_raw_commands_retained=len(report['commands']),
                readiness_phase_count=len(phase_inspections), host_test_summaries=host, source_pins=PINS,
                trigger_configuration_confirmed=False, private_replay_directory_removed=True,
                literal_exact_alarm_ok_tapped=replayed.get('exact_alarm_explanation_ok_tapped'),
                literal_settings_navigation_observed=replayed.get('settings_navigation_observed'),
                literal_settings_inputs=replayed.get('settings_inputs'),
                literal_permission_granted_flag=replayed.get('permission_granted'),
                literal_global_command_observations=replayed.get('global_command_observations'))
    except Exception as error:
        result.update(status='INDEPENDENT_EXACT_ALARM_REPLAY_REJECTED', analysis_passed=False,
                      error=type(error).__name__ + ': ' + str(error))
    finally:
        if before is not None:
            after = scan_raw(raw)
            save(output, 'raw-file-identities-after.json', after)
            unchanged = before == after and identity(archive) == archive_before
            result['raw_files_verified_before_and_after'] = len(before)
            result['raw_archive_and_all_files_unchanged'] = unchanged
            if not unchanged:
                result.update(status='RAW_EVIDENCE_CHANGED_DURING_REPLAY', analysis_passed=False)
        result['fixed_apks_unchanged'] = all(identity(path) == {'bytes': size, 'sha256': digest}
                                           for path, (_, size, digest) in zip(apks, APK_PINS))
        if not result['fixed_apks_unchanged']:
            result.update(status='COMPARED_APK_CHANGED_DURING_REPLAY', analysis_passed=False)
        result['unexecuted_raw_bytecode_omitted_only_from_private_views'] = sorted(omitted_bytecode)
        result['private_apk_transport'] = transports
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(output, 'independent-exact-alarm-analysis.json', result)
        print(json.dumps({key: result[key] for key in ('status', 'analysis_passed', 'recorded_runs',
            'diagnostic_rgba_pixel_vector', 'raw_files_verified_before_and_after', 'error') if key in result}, indent=2), flush=True)
    return 0 if result['analysis_passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
