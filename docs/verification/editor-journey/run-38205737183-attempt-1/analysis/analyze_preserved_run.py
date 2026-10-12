#!/usr/bin/env python3
"""Replay exact archived ten-screen policy and independently measure raw evidence."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image

BASE = Path('/workspace/scratch/4130730d15aa')
ROOT = Path(__file__).resolve().parent
RUN_ID = 38205737183
HEAD = '5a95831d897a6fc2b6e59a0ef4088badf63c92da'
ARCHIVE_COMMIT = '95c424943d26ac920ab83e15d2e011808cd34dc3'
ARCHIVE_META = {'bytes': 15156144, 'sha256': 'f6760a909477b09e91cb9315c67c4c59146bbf454aecc50a72809d101749b2ca'}
MANIFEST_META = {'bytes': 419840, 'sha256': '3bbc99e2c3f6a2268b5055c4afb449decf708fc1f806bda81d98ae2c2e936ade'}
PINS = {
    'editor_journey.py': 'cc8425fd09ea8c0d5bde354bd3ad2a94289a528b36fde8a485965207234e6f7c',
    'observed_journey.py': '47658995c576a8e07124014fedbb131eedf0095fffe0672f34ae279456630057',
    'favourite_info_journey.py': '4014e46b7a529d5b82bfffac18a606416af8d39b5597b6bf0c88cb8de2a2a313',
    'supplied_reference_journey.py': '7c03b5cf3c7aaeb4211e444a7e86d7b93ccb621c508516f07e7bf1f56b5321b0',
    'robust_capture.py': 'ab4fea3dfb4220bcfc790027c8eda3b7a3421ca9dc45a3b486a89fb34757ba3d',
    'editor-plan.json': '28ea38698dcfcf0146955be9ddd07d1df0fe01a234c13633dac85628edbbc448',
    'android_compare.py': '0b9a50cec26d0cc97a2b8c5592aaf614a40b5dc339bccf85d85f1d753500126f',
}


def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def artifacts(value):
    if isinstance(value, dict):
        if set(value) == {'path', 'bytes', 'sha256'}:
            yield value
        for child in value.values():
            yield from artifacts(child)
    elif isinstance(value, list):
        for child in value:
            yield from artifacts(child)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, default=ROOT / 'evidence.zip')
    parser.add_argument('--manifest', type=Path, default=ROOT / 'archived-manifest.json')
    parser.add_argument('--extracted', type=Path, default=ROOT / 'extracted')
    parser.add_argument('--output', type=Path, default=ROOT / 'analysis')
    parser.add_argument('--android-compare', type=Path, default=BASE / 'runtime-forward/android_compare.py')
    args = parser.parse_args()
    output = args.output.resolve()
    assert not output.exists(), 'Use a fresh analysis output directory; preserve earlier attempts'
    archive = args.archive.read_bytes()
    assert meta(archive) == ARCHIVE_META
    manifest_bytes = args.manifest.read_bytes()
    assert meta(manifest_bytes) == MANIFEST_META
    manifest = json.loads(manifest_bytes)
    assert manifest['run_id'] == RUN_ID and manifest['head_sha'] == HEAD
    members = {entry['path']: entry for entry in manifest['members']}
    assert len(members) == len(manifest['members']) == 2302
    extracted = args.extracted.resolve()
    with zipfile.ZipFile(args.archive) as zipped:
        assert len(zipped.namelist()) == len(set(zipped.namelist())) == 2302
        assert set(zipped.namelist()) == set(members)
        for name, entry in members.items():
            data = zipped.read(name)
            assert meta(data) == {key: entry[key] for key in ['bytes', 'sha256']}
            path = extracted / name
            assert path.resolve().is_relative_to(extracted) and not path.is_symlink()
            if path.exists():
                assert path.read_bytes() == data
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
    print('VERIFIED exact archive, manifest and all 2302 extracted members', flush=True)
    output.mkdir(parents=True)
    source = output / 'pinned-source'
    source.mkdir()
    for name, digest in PINS.items():
        path = args.android_compare if name == 'android_compare.py' else extracted / 'tools/parity_journeys' / name
        data = path.read_bytes()
        assert meta(data)['sha256'] == digest
        (source / name).write_bytes(data)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(source))
    proof = importlib.import_module('android_compare')
    journey = importlib.import_module('editor_journey')
    favourite = importlib.import_module('favourite_info_journey')
    observed = importlib.import_module('observed_journey')
    folder = extracted / 'ci-editor/journey'
    report = json.loads((folder / 'journey.json').read_text())
    comparison = json.loads((folder / 'comparison.json').read_text())
    assert meta((folder / 'journey.json').read_bytes()) == {
        'bytes': 709737, 'sha256': '169ca0ac100b8a6e3cb9504ba3eb1077b6b06d99add19bda2925b4795afb4bc6'}
    assert meta((folder / 'comparison.json').read_bytes()) == {
        'bytes': 6427, 'sha256': 'ffb41a33258749503bcb3baf3b2795e2cc61345cf8633f6e01d3f25a9c64e4a7'}
    print('REPLAYING exact pinned comparator, full-frame ledgers and all input/identity guards', flush=True)
    with favourite.configured_plan():
        replay = journey.compare(folder, report, proof)
        write_json(output / 'comparator-replay.json', replay)
        assert replay == comparison, 'Exact pinned comparator replay differs from actual hosted result'
        assert replay['status'] == 'JOURNEY_DIFFERENCE' and replay['android_runtime_executed'] is True
        assert report['plan_sha256'] == journey.fingerprint(journey.PLAN)
        plan = json.loads(json.dumps(journey.PLAN))
    print('REPLAY MATCHES JOURNEY_DIFFERENCE; no recorded guard rejected', flush=True)
    entries = {}
    reference_count = 0
    queue = list(artifacts(report))
    while queue:
        entry = queue.pop()
        reference_count += 1
        data = proof.artifact(folder, entry)
        archived = members['ci-editor/journey/' + entry['path']]
        assert meta(data) == {key: archived[key] for key in ['bytes', 'sha256']}
        if entry['path'] in entries:
            assert entries[entry['path']] == entry
            continue
        entries[entry['path']] = entry
        if entry['path'].endswith('.json'):
            queue.extend(artifacts(json.loads(data)))
    assert [run['label'] for run in report['runs']] == ['original', 'candidate']
    assert [run['apk_sha256'] for run in report['runs']] == [proof.ORIGINAL_SHA256, '9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2']
    assert len(plan) == 10 and len(report['capture_events']) == 38
    review = set()
    runs = []
    for run in report['runs']:
        assert run['status'] == 'COMPLETE' and run['current_step'] == 'after-favourite-info'
        assert len(run['screens']) == 10 and len(run['transitions']) == 9
        assert run['environment'] == run['environment_after'] == report['runs'][0]['environment']
        screens = []
        for index, shot in enumerate(run['screens']):
            assert shot['name'] == plan[index][0] and shot['owner'] == plan[index][1]
            review.update(item['path'] for item in artifacts(shot))
            screens.append({'name': shot['name'], 'owner': shot['owner'], 'artifacts': shot['artifacts'],
                            'pids': [proof.artifact(folder, shot['artifacts'][key]).decode().strip() for key in ['pid_first', 'pid_final']],
                            'resumed_components_first': proof.resumed_components(proof.artifact(folder, shot['artifacts']['foreground']).decode()),
                            'resumed_components_final': proof.resumed_components(proof.artifact(folder, shot['artifacts']['foreground_final']).decode()),
                            'observation': shot['observation'], 'settling': shot['settling']})
        transitions = []
        for index, transition in enumerate(run['transitions']):
            prior = run['screens'][index]
            before = transition['before']
            assert 0 <= transition['precondition_age_seconds'] <= 15
            assert all(proof.artifact(folder, prior['artifacts'][key]) == proof.artifact(folder, before['artifacts'][key])
                       for key in ['hierarchy', 'screenshot'])
            action = transition['action']
            assert action != 'BACK', 'This exact ten-screen plan contains taps only'
            center = journey.target(proof.artifact(folder, before['artifacts']['hierarchy']), before['owner'], action, 720, 1280)
            assert transition['command']['argv'] == ['shell', 'input tap ' + ' '.join(map(str, center))]
            review.update(item['path'] for item in artifacts(transition))
            transitions.append({'to': transition['to'], 'action': action, 'center': center,
                                'precondition_age_seconds': transition['precondition_age_seconds'],
                                'full_png_and_xml_before_input_equal_to_prior_capture': True,
                                'pinned_identity_component_geometry_and_freshness_guards_replayed': True,
                                'actual_input_command': transition['command']})
        handoff_ref = run['transitions'][4]['process_handoff']
        handoff = json.loads(proof.artifact(folder, handoff_ref))
        assert handoff['status'] == 'OBSERVED_NOTIFICATION_BOUNDARY'
        assert handoff['outcome'] == comparison['process_handoff_outcomes'][len(runs)]
        assert handoff['outcome']['old_pid_absent_in_both_lists'] is True
        assert handoff['outcome']['installed_apk_identity_verified'] is True
        review.update(item['path'] for item in artifacts(handoff))
        for key in ['absence', 'install', 'installed_path', 'installed_checksum', 'launch']:
            review.update(item['path'] for item in artifacts(run[key]))
        runs.append({'label': run['label'], 'apk_sha256': run['apk_sha256'], 'status': run['status'],
                     'installed_identity_and_post_denial_and_pre_ok_identity_replayed': True,
                     'environment': run['environment'], 'environment_after_equal': True,
                     'screens': screens, 'transitions': transitions, 'handoff': handoff,
                     'last_input_is_one_observed_ok': transitions[-1]['action'] == favourite.OK,
                     'no_subsequent_input': len(run['transitions']) == 9})
    inputs = [command for command in report['commands'] if command['argv'][0] == 'shell' and command['argv'][1].startswith('input ')]
    assert inputs == [transition['command'] for run in report['runs'] for transition in run['transitions']]
    assert len(inputs) == 18
    events = []
    for entry in report['capture_events']:
        event = json.loads(proof.artifact(folder, entry))
        assert event['status'] == 'CONSECUTIVE_FULL_FRAMES_IDENTICAL'
        assert len(event['attempts']) == 2 and event['accepted_pair'] == [0, 1]
        assert all(proof.artifact(folder, event['attempts'][0]['artifacts'][key]) ==
                   proof.artifact(folder, event['attempts'][1]['artifacts'][key]) for key in ['hierarchy', 'screenshot'])
        review.add(entry['path'])
        review.update(item['path'] for item in artifacts(event))
        events.append({'artifact': entry, 'label': event['label'], 'seconds': event['seconds'],
                       'attempts': event['attempts'], 'accepted_pair': [0, 1], 'rejected_intermediate_frames': 0})
    pairs = []
    for first, second, reported in zip(*[run['screens'] for run in report['runs']], comparison['screens']):
        images = [np.asarray(Image.open(folder / shot['artifacts']['screenshot']['path']).convert('RGBA')) for shot in [first, second]]
        assert images[0].shape == images[1].shape == (1280, 720, 4)
        mask = np.any(images[0] != images[1], axis=2)
        yy, xx = np.where(mask)
        changed = int(mask.sum())
        assert changed == reported['changed_pixels']
        xml = [proof.artifact(folder, shot['artifacts']['hierarchy']) for shot in [first, second]]
        assert xml[0] == xml[1]
        pairs.append({'name': first['name'], 'changed_rgba_pixels': changed,
                      'difference_bounds_exclusive': None if not len(xx) else [int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1],
                      'full_png_bytes_equal': first['artifacts']['screenshot']['sha256'] == second['artifacts']['screenshot']['sha256'],
                      'full_xml_bytes_equal': True, 'complete_xml_tree_equal': reported['hierarchy_equal'],
                      'png_color_metadata_equal': reported['color_metadata_equal'],
                      'full_observed_snapshot_equal': reported['equal'], 'original': first['artifacts'], 'candidate': second['artifacts']})
    assert [pair['changed_rgba_pixels'] for pair in pairs] == [0, 26, 0, 0, 0, 0, 0, 0, 0, 0]
    lifecycle = (extracted / 'ci-editor/lifecycle.log').read_bytes()
    lines = lifecycle.decode().splitlines(keepends=True)
    crashes = []
    for run in runs:
        label, old, new = run['label'], run['handoff']['old_pid'], run['handoff']['new_pid']
        pattern = re.compile(r'^\d\d-\d\d \S+\s+' + old + r'\s+' + old + r'\s+E AndroidRuntime:')
        selected = [(number + 1, line) for number, line in enumerate(lines) if pattern.match(line)]
        literal = ''.join(line for _, line in selected)
        assert len(selected) == 13 and 'FATAL EXCEPTION: main' in literal
        payloads = [line.split('AndroidRuntime: ', 1)[1].rstrip('\r\n') for _, line in selected]
        assert re.fullmatch(r'java\.lang\.IllegalStateException: Fragment LB\{[0-9a-f]+\} not attached to Activity', payloads[2])
        died = [line for line in lines if re.search(r' I am_proc_died: \[0,' + old + ',' + re.escape(journey.PACKAGE) + ',', line)]
        start_pattern = re.compile(r' I am_proc_start: \[0,' + new + r',\d+,' + re.escape(journey.PACKAGE) + r',([^,]+),\{([^}]+)\}\]\s*$')
        started = [line for line in lines if start_pattern.search(line)]
        assert len(died) == len(started) == 1
        hosting_type, hosting_component = start_pattern.search(started[0]).groups()
        assert (hosting_type, hosting_component) == ('top-activity', observed.HOME)
        crashes.append({'label': label, 'old_pid': old, 'new_pid': new,
                        'raw_lifecycle_log_line_numbers': [number for number, _ in selected], 'literal_fatal_block': literal,
                        'literal_exception': payloads[2], 'stack': [value.strip() for value in payloads[3:]],
                        'process_died_event': died[0], 'process_started_event': started[0],
                        'new_process_hosting_type': hosting_type, 'new_process_hosting_component': hosting_component,
                        'separately_guarded_boundary': run['handoff']['outcome']})
    assert crashes[0]['stack'] == crashes[1]['stack']
    assert crashes[0]['literal_exception'] != crashes[1]['literal_exception']
    dialog = report['runs'][0]['screens'][8]
    data = proof.artifact(folder, dialog['artifacts']['hierarchy'])
    tree = journey.tree(data, journey.PACKAGE)
    selectors = {key: dict(journey.select(tree, journey.PACKAGE, selector).attrib) for key, selector in [
        ('title', favourite.TITLE), ('message', {'resource-id': 'android:id/message'}), ('ok', {'resource-id': 'android:id/button1'})]}
    assert selectors['message']['text'] == favourite.MESSAGE
    selectors['ok_center'] = journey.target(data, journey.PACKAGE, favourite.OK, 720, 1280)
    assert selectors['ok_center'] == [560, 828]
    host = (extracted / 'ci-editor/host-tests.log').read_text()
    download = (extracted / 'ci-editor/download-tests.log').read_text()
    assert re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', host, re.M) == [('81', '24.423')]
    assert re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', download, re.M) == [('6', '0.006')]
    assert len(re.findall(r'^test_.* \.\.\. ok$', host, re.M)) == 81
    assert re.search(r'^OK$', host, re.M) and re.search(r'^OK$', download, re.M)
    config_bytes = (extracted / 'ci-editor/device/capture-device.json').read_bytes()
    config = json.loads(config_bytes)
    assert config['status'] == 'CAPTURE_DEVICE_CONFIGURED'
    assert config['demo_clock_requested'] == '1200' and config['requested_animation_scales_observed'] is True
    assert config['animation_scales_requested'] == {'animator_duration_scale': '0', 'window_animation_scale': '0', 'transition_animation_scale': '0'}
    result = {'schema': 1, 'status': 'EXACT_PINNED_POLICY_REPLAYED_WITH_PERSISTENT_UNMASKED_TRIGGERS_DIFFERENCE',
              'analyzed_utc': datetime.now(timezone.utc).isoformat(), 'run_id': RUN_ID, 'head_sha': HEAD,
              'archive_commit': ARCHIVE_COMMIT, 'archive': ARCHIVE_META, 'manifest': MANIFEST_META,
              'all_archive_members_verified': 2302, 'all_referenced_artifact_paths_verified': len(entries),
              'recursive_artifact_references_checked': reference_count,
              'pinned_verifier_hashes': PINS, 'exact_pinned_comparator_replay_matches': True,
              'actual_comparison': comparison, 'actual_installed_identities_verified': True,
              'host_tests': {'journey': 81, 'journey_seconds': 24.423, 'download': 6, 'download_seconds': 0.006, 'both_passed': True},
              'runs': runs, 'full_unmasked_snapshot_pairs': pairs, 'all_stabilization_events': events,
              'stabilization_events': 38, 'raw_frame_observations': 76,
              'rejected_intermediate_frames': 0, 'each_event_used_first_two_consecutive_identical_full_png_and_xml_frames': True,
              'all_actual_input_commands': inputs, 'actual_inputs': 18,
              'fatal_exceptions_and_process_events': crashes, 'exception_types_and_stacks_equal': True,
              'literal_exception_messages_equal': False, 'new_process_hosting_types_equal': True,
              'full_process_lifecycle_equivalence_established': False,
              'device_and_host_wall_clock_synchronization_established': False,
              'notification_denial_caused_the_fatal_exception_established': False,
              'observed_favourite_triggers_dialog': selectors, 'one_observed_ok_per_app_executed': True,
              'terminal_components': [item['component'] for item in comparison['terminal_surfaces']],
              'device_capture_config': {'path': 'device/capture-device.json', **meta(config_bytes)},
              'animation_timing_and_motion_parity_tested': False, 'crash_free_run_established': False,
              'catalog_navigation_established': False, 'requested_ten_screen_journey_passed': False,
              'full_runtime_1_to_1_established': False, 'new_device_actions_performed_by_analysis': False,
              'app_or_active_policy_edited_by_analysis': False,
              'scope_notes': [
                  'Both runs completed ten screens and nine taps under the exact opt-in policy; one visual comparison failed.',
                  'All raw frames, XML, PID/component guards and installed identities remain unmodified.',
                  'The known fatal exception is retained, and paired post-crash continuation is not a crash-free pass.',
                  'The comparator cause field classifies observed Java fatal blocks; it does not prove denial caused a crash or complete lifecycle equivalence.',
                  'Diagnostic coordinates do not crop, mask, normalize, tolerate, or change any acceptance rule.',
                  'This capture stopped after one Favourite Triggers OK and its actual EditMacroActivity surface; no catalog input followed.',
              ]}
    write_json(output / 'independent-analysis.json', result)
    write_json(output / 'artifact-graph.json', {'schema': 1, 'run_id': RUN_ID, 'members': [entries[name] for name in sorted(entries)]})
    capture_folder = output / 'captures'
    capture_folder.mkdir()
    for name in sorted(review):
        assert name in entries
        target = capture_folder / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(proof.artifact(folder, entries[name]))
    for relative in ['ci-editor/lifecycle.log', 'ci-editor/host-tests.log', 'ci-editor/download-tests.log',
                     'ci-editor/device/capture-device.json', 'ci-editor/environment/runtime-status.json',
                     'ci-editor/environment/runtime-properties.json']:
        target = output / relative.removeprefix('ci-editor/')
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(extracted / relative, target)
    print(json.dumps({'status': result['status'], 'archive_members': 2302, 'artifact_paths': len(entries),
                      'review_copy_files': len(review), 'policy_replay_equal': True,
                      'pixel_vector': [pair['changed_rgba_pixels'] for pair in pairs],
                      'all_xml_bytes_equal': True, 'raw_frame_observations': 76,
                      'rejected_intermediate_frames': 0, 'screens_each': 10, 'inputs_each': 9,
                      'host_tests_passed': [81, 6], 'crash_free_run_established': False}, indent=2), flush=True)


if __name__ == '__main__':
    main()
