#!/usr/bin/env python3
"""Replay and measure the exact archived editor run; no Android actions."""
from __future__ import annotations

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
ARCHIVED = BASE / 'MacroDroid-Reconstruction/docs/verification/editor-journey/run-38202401351-attempt-1'
EXTRACTED = ROOT / 'extracted'
OUTPUT = ROOT / 'analysis'
PINS = {
    'editor_journey.py': '9d402ee1db9f9fd22ee62882198ef6722f0c150450c6fd53fe5465359ffb201b',
    'supplied_reference_journey.py': '9bef574a54b4263b576524dec87596e0c748543c434a2b9fa5cfff73f251195b',
    'robust_capture.py': 'ab4fea3dfb4220bcfc790027c8eda3b7a3421ca9dc45a3b486a89fb34757ba3d',
    'editor-plan.json': 'ff578443029fff6da5056f0e8eb30e07cc7c74c8bada126939062e5bbc311df3',
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


def main():
    assert not OUTPUT.exists()
    manifest = json.loads((ARCHIVED / 'manifest.json').read_text())
    assert manifest['run_id'] == 38202401351 and manifest['head_sha'] == 'cada56c8a11ff5cbd892ec6d0beaeab60b3e644d'
    archive = (ARCHIVED / 'evidence.zip').read_bytes()
    assert meta(archive) == {'bytes': 6517530, 'sha256': 'fa2eca5f893ae181b91aa7a7bf5df8320620bbc8da21b87eacffb1de0c3bc7ee'}
    assert len(manifest['members']) == 1042
    with zipfile.ZipFile(ARCHIVED / 'evidence.zip') as zipped:
        assert set(zipped.namelist()) == {entry['path'] for entry in manifest['members']}
        for entry in manifest['members']:
            data = zipped.read(entry['path'])
            assert meta(data) == {key: entry[key] for key in ['bytes', 'sha256']}
            path = EXTRACTED / entry['path']
            assert path.resolve().is_relative_to(EXTRACTED.resolve()) and not path.is_symlink()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    source = ROOT / 'pinned-source'
    source.mkdir(exist_ok=True)
    for name, digest in PINS.items():
        path = BASE / 'runtime-forward/android_compare.py' if name == 'android_compare.py' else EXTRACTED / 'tools/parity_journeys' / name
        data = path.read_bytes()
        assert meta(data)['sha256'] == digest
        (source / name).write_bytes(data)
    sys.path.insert(0, str(source))
    proof = importlib.import_module('android_compare')
    journey = importlib.import_module('editor_journey')
    adapter = importlib.import_module('supplied_reference_journey')
    folder = EXTRACTED / 'ci-editor/journey'
    for name in ['journey.json', 'comparison.json']:
        assert (folder / name).read_bytes() == (ARCHIVED / name).read_bytes()
    report = json.loads((folder / 'journey.json').read_text())
    comparison = json.loads((folder / 'comparison.json').read_text())
    with adapter.configured_plan():
        replay = journey.compare(folder, report, proof)
        assert replay == comparison and replay['status'] == 'REJECTED'
        assert report['plan_sha256'] == journey.fingerprint(journey.PLAN)
        plan = json.loads(json.dumps(journey.PLAN))
    entries = {}
    references = 0
    for entry in artifacts(report):
        proof.artifact(folder, entry)
        references += 1
        if entry['path'] in entries:
            assert entries[entry['path']] == entry
        entries[entry['path']] = entry
    assert [run['label'] for run in report['runs']] == ['original', 'candidate']
    assert [run['apk_sha256'] for run in report['runs']] == [proof.ORIGINAL_SHA256, '9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2']
    assert report['runs'][0]['environment'] == report['runs'][1]['environment']
    runs = []
    for run in report['runs']:
        assert run['status'] == 'FAILED' and run['current_step'] == 'trigger-catalog'
        assert run['reason'] == "Missing or ambiguous selector: {'text': 'Add Trigger'}"
        assert len(run['screens']) == 9 and len(run['transitions']) == 8
        out, err = journey.evidence_command(folder, run['absence'], proof, codes=(0, 1))
        assert proof.absence_ok(run['absence']['returncode'], out.decode(), err.decode())
        out, err = journey.evidence_command(folder, run['install'], proof)
        assert proof.install_ok(0, out.decode(), err.decode())
        out, err = journey.evidence_command(folder, run['installed_path'], proof)
        path = proof.installed_path(0, out.decode(), err.decode())
        out, err = journey.evidence_command(folder, run['installed_checksum'], proof)
        assert proof.installed_digest(0, out.decode(), err.decode(), path) == run['apk_sha256']
        out, err = journey.evidence_command(folder, run['launch'], proof)
        assert proof.launch_ok(0, out.decode())
        screens = []
        for index, shot in enumerate(run['screens']):
            journey.validate_snapshot(folder, shot, proof)
            assert shot['name'] == plan[index][0] and shot['owner'] == plan[index][1]
            root = journey.tree(proof.artifact(folder, shot['artifacts']['hierarchy']), shot['owner'])
            if index < 8:
                journey.select(root, shot['owner'], plan[index][2])
            else:
                journey.select(root, shot['owner'], {'resource-id': journey.PACKAGE + ':id/alertTitle', 'text': 'Favourite Triggers'})
                assert not any(node.get('text') == 'Add Trigger' for node in root.iter('node'))
            screens.append({'name': shot['name'], 'owner': shot['owner'], 'artifacts': shot['artifacts'],
                            'pids': [proof.artifact(folder, shot['artifacts'][key]).decode().strip() for key in ['pid_first', 'pid_final']],
                            'resumed_components': proof.resumed_components(proof.artifact(folder, shot['artifacts']['foreground']).decode()),
                            'sample_interval_seconds': shot['sample_interval_seconds']})
        transitions = []
        for index, transition in enumerate(run['transitions']):
            prior = run['screens'][index]
            before = transition['before']
            old_state = journey.validate_snapshot(folder, prior, proof)
            state = journey.validate_snapshot(folder, before, proof)
            assert state[0] == old_state[0] and 0 <= transition['precondition_age_seconds'] <= 15
            live = transition['preinput_artifacts']
            proof.live_pids(proof.artifact(folder, prior['artifacts']['pid_final']).decode(), proof.artifact(folder, before['artifacts']['pid_final']).decode())
            proof.live_pids(proof.artifact(folder, before['artifacts']['pid_final']).decode(), proof.artifact(folder, live['pid']).decode())
            assert journey.resumed(proof.artifact(folder, live['foreground']).decode(), prior['owner'])
            center = journey.target(proof.artifact(folder, before['artifacts']['hierarchy']), before['owner'], transition['action'], state[1], state[2])
            assert transition['command']['argv'] == ['shell', 'input tap ' + ' '.join(map(str, center))]
            journey.evidence_command(folder, transition['command'], proof, clean=True)
            transitions.append({'to': transition['to'], 'action': transition['action'], 'center': center,
                                'age_seconds': transition['precondition_age_seconds'],
                                'recorded_tree_pid_foreground_geometry_and_input_verified': True,
                                'full_frame_before_input_equal_to_prior_capture': state == old_state})
        runs.append({'label': run['label'], 'apk_sha256': run['apk_sha256'], 'installed_identity_verified': True,
                     'status': run['status'], 'reason': run['reason'], 'screens': screens, 'transitions': transitions,
                     'environment_after_recorded': 'environment_after' in run})
    all_inputs = [item for item in report['commands'] if item['argv'][0] == 'shell' and item['argv'][1].startswith('input ')]
    assert all_inputs == [transition['command'] for run in report['runs'] for transition in run['transitions']]
    assert len(all_inputs) == 16
    pairs = []
    for first, second in zip(*[run['screens'] for run in report['runs']]):
        a, b = [journey.validate_snapshot(folder, shot, proof) for shot in [first, second]]
        images = [np.asarray(Image.open(folder / shot['artifacts']['screenshot']['path']).convert('RGBA')) for shot in [first, second]]
        assert images[0].shape == images[1].shape == (1280, 720, 4)
        mask = np.any(images[0] != images[1], axis=2)
        yy, xx = np.where(mask)
        changed = int(mask.sum())
        assert changed == sum(a[3][i:i+4] != b[3][i:i+4] for i in range(0, len(a[3]), 4))
        pairs.append({'name': first['name'], 'changed_rgba_pixels': changed,
                      'difference_bounds_exclusive': None if not len(xx) else [int(xx.min()), int(yy.min()), int(xx.max())+1, int(yy.max())+1],
                      'png_bytes_equal': first['artifacts']['screenshot']['sha256'] == second['artifacts']['screenshot']['sha256'],
                      'xml_bytes_equal': first['artifacts']['hierarchy']['sha256'] == second['artifacts']['hierarchy']['sha256'],
                      'complete_xml_tree_equal': a[0] == b[0], 'png_color_metadata_equal': a[4] == b[4],
                      'full_observed_snapshot_equal': a == b, 'original': first['artifacts'], 'candidate': second['artifacts']})
    assert [pair['changed_rgba_pixels'] for pair in pairs] == [0, 26, 0, 0, 0, 0, 0, 0, 0]
    lifecycle = (EXTRACTED / 'ci-editor/lifecycle.log').read_bytes()
    lines = lifecycle.decode().splitlines(keepends=True)
    crashes = []
    for label, old, new in [('original', '3947', '5039'), ('candidate', '5811', '6498')]:
        pattern = re.compile(r'^\d\d-\d\d \S+\s+' + old + r'\s+' + old + r'\s+E AndroidRuntime:')
        selected = [(number + 1, line) for number, line in enumerate(lines) if pattern.match(line)]
        raw = ''.join(line for _, line in selected)
        assert len(selected) == 13 and 'FATAL EXCEPTION: main' in raw
        payloads = [line.split('AndroidRuntime: ', 1)[1].rstrip('\r\n') for _, line in selected]
        assert re.fullmatch(r'java\.lang\.IllegalStateException: Fragment LB\{[0-9a-f]+\} not attached to Activity', payloads[2])
        died = [line for line in lines if re.search(r' I am_proc_died: \[0,' + old + ',' + re.escape(journey.PACKAGE) + ',', line)]
        started = [line for line in lines if re.search(r' I am_proc_start: \[0,' + new + r',\d+,' + re.escape(journey.PACKAGE) + r',top-activity,', line)]
        assert len(died) == len(started) == 1 and '.homescreen.NewHomeScreenActivity' in started[0]
        crashes.append({'label': label, 'old_pid': old, 'new_pid': new, 'raw_log_line_numbers': [number for number, _ in selected],
                        'literal_fatal_block': raw, 'literal_exception': payloads[2],
                        'exception_type': 'java.lang.IllegalStateException', 'stack': [value.strip() for value in payloads[3:]],
                        'process_died_event': died[0], 'process_started_event': started[0]})
    assert crashes[0]['stack'] == crashes[1]['stack'] and crashes[0]['literal_exception'] != crashes[1]['literal_exception']
    dialog = report['runs'][0]['screens'][-1]
    data = proof.artifact(folder, dialog['artifacts']['hierarchy'])
    tree = journey.tree(data, journey.PACKAGE)
    selectors = {key: dict(journey.select(tree, journey.PACKAGE, selector).attrib) for key, selector in [
        ('title', {'resource-id': journey.PACKAGE + ':id/alertTitle'}), ('message', {'resource-id': 'android:id/message'}),
        ('ok', {'resource-id': 'android:id/button1'})]}
    selectors['ok_center'] = journey.target(data, journey.PACKAGE, {'resource-id': 'android:id/button1', 'text': 'OK'}, 720, 1280)
    assert selectors['ok_center'] == [560, 828]
    host = (EXTRACTED / 'ci-editor/host-tests.log').read_text()
    download = (EXTRACTED / 'ci-editor/download-tests.log').read_text()
    assert re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', host, re.M) == [('31', '3.614')]
    assert re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', download, re.M) == [('6', '0.006')]
    analysis = {'status': 'PARTIAL_EDITOR_CAPTURES_WITH_SHARED_FATAL_EXCEPTION_AND_26_PIXEL_DIFFERENCE',
                'analyzed_utc': datetime.now(timezone.utc).isoformat(), 'run_id': 38202401351,
                'head_sha': manifest['head_sha'], 'archive_commit': '4c279db5619b2d22fdb12d6f084e740bfc5ce20c',
                'archive': meta(archive), 'all_archive_members_verified': 1042,
                'all_referenced_artifact_paths_verified': len(entries), 'artifact_references_checked': references,
                'pinned_verifier_hashes': PINS, 'exact_pinned_comparator_replay_matches': True,
                'preserved_comparison': comparison, 'actual_installed_identities_verified': True,
                'actual_android_actions_and_captures_observed': True,
                'host_tests': {'journey': 31, 'download': 6, 'both_passed': True},
                'runs': runs, 'full_unmasked_snapshot_pairs': pairs, 'fatal_exceptions_and_process_events': crashes,
                'exception_types_and_stacks_equal': True, 'literal_exception_messages_equal': False,
                'lifecycle_log': {'path': 'lifecycle.log', **meta(lifecycle)}, 'observed_favourite_triggers_dialog': selectors,
                'next_ok_action_executed_by_this_run': False, 'crash_free_run_established': False,
                'catalog_reached': False, 'requested_editor_journey_passed': False,
                'full_runtime_1_to_1_established': False, 'new_device_actions_performed_by_analysis': False,
                'interpretation': [
                    'All nine complete XML trees and raw XML byte pairs match. Eight PNG byte pairs match; TRIGGERS has 26 differing RGBA pixels around the first/second page dots.',
                    'Both original and candidate record the same IllegalStateException type and ten-frame stack. Their literal messages differ in runtime fragment instance IDs; full raw logs and messages remain unchanged.',
                    'Both main processes die and new main processes start at NewHomeScreenActivity after the notification-denial boundary. This is observed post-crash continuation, not a benign or crash-free restart claim.',
                    'Both close the previously observed LITEAPKS dialog, reach home and the empty editor, then display Favourite Triggers. Neither Add Trigger catalog nor an OK action was observed.',
                    'The preserved fourteen-step comparator remains REJECTED because both runs are incomplete. The earlier measured dimming/dot failures remain unchanged historical evidence.',
                    'The artifact records one successful acquisition per named screen, not consecutive identical full-frame observations; settling of the differing page dots is not established by this run.']}
    OUTPUT.mkdir()
    (OUTPUT / 'independent-analysis.json').write_text(json.dumps(analysis, indent=2) + '\n')
    for run in report['runs']:
        for shot in run['screens']:
            for entry in shot['artifacts'].values():
                path = OUTPUT / 'captures' / entry['path']
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(proof.artifact(folder, entry))
    (OUTPUT / 'lifecycle.log').write_bytes(lifecycle)
    for crash in crashes:
        (OUTPUT / (crash['label'] + '-fatal.txt')).write_bytes(crash['literal_fatal_block'].encode())
    for name in ['host-tests.log', 'download-tests.log', 'bootstrap.log']:
        shutil.copyfile(EXTRACTED / 'ci-editor' / name, OUTPUT / name)
    shutil.copytree(source, OUTPUT / 'pinned-source', ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copyfile(Path(__file__), OUTPUT / Path(__file__).name)
    print(json.dumps({'status': analysis['status'], 'artifact_paths': len(entries), 'archive_members': 1042,
                      'pixel_vector': [pair['changed_rgba_pixels'] for pair in pairs], 'output': str(OUTPUT)}, indent=2))


if __name__ == '__main__':
    main()
