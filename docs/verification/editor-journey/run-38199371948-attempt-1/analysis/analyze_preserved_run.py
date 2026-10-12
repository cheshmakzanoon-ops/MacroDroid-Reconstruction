#!/usr/bin/env python3
"""Read and measure the preserved 38199371948 artifact without device actions."""
from __future__ import annotations

import hashlib
import importlib
import json
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
REPO_EVIDENCE = Path('/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction/docs/verification/editor-journey/run-38199371948-attempt-1')
EXTRACTED = ROOT / 'extracted'
FOLDER = EXTRACTED / 'ci-editor/journey'
OUTPUT = ROOT / 'analysis'
PINNED = ROOT / 'pinned-source'
EXPECTED = {
    'android_compare.py': '24da5bedb4a6e4650f83e58cff735323596522468096891efd4cb8e6c6c58b85',
    'editor_journey.py': '9d402ee1db9f9fd22ee62882198ef6722f0c150450c6fd53fe5465359ffb201b',
}


def meta(path):
    value = path.read_bytes()
    return {'bytes': len(value), 'sha256': hashlib.sha256(value).hexdigest()}


def bound_artifacts(value):
    if isinstance(value, dict):
        if set(value) == {'path', 'bytes', 'sha256'}:
            yield value
        for child in value.values():
            yield from bound_artifacts(child)
    elif isinstance(value, list):
        for child in value:
            yield from bound_artifacts(child)


def main():
    assert not OUTPUT.exists(), 'Analysis output already exists'
    manifest = json.loads((REPO_EVIDENCE / 'manifest.json').read_text())
    assert manifest['run_id'] == 38199371948
    assert manifest['head_sha'] == '3f584e6c958958a5d823e33f8facd0dcdae906f8'
    assert meta(REPO_EVIDENCE / 'evidence.zip') == {'bytes': 4058327, 'sha256': '5edc5aa2a46b2281432c082046400474f53a466ed8c77f6747c5e11a2f0adc70'}
    assert len(manifest['members']) == 740
    for entry in manifest['members']:
        path = EXTRACTED / entry['path']
        assert path.resolve().is_relative_to(EXTRACTED.resolve()) and not path.is_symlink()
        assert meta(path) == {key: entry[key] for key in ['bytes', 'sha256']}, entry['path']
    assert (FOLDER / 'journey.json').read_bytes() == (REPO_EVIDENCE / 'journey.json').read_bytes()
    assert (FOLDER / 'comparison.json').read_bytes() == (REPO_EVIDENCE / 'comparison.json').read_bytes()
    for name, digest in EXPECTED.items():
        assert meta(PINNED / name)['sha256'] == digest
    assert (PINNED / 'editor_journey.py').read_bytes() == (EXTRACTED / 'tools/parity_journeys/editor_journey.py').read_bytes()
    # These are exact reviewed source files fetched from the tested commit. Only
    # pure evidence-reading functions are called; Recorder and main are not used.
    sys.path.insert(0, str(PINNED))
    proof = importlib.import_module('android_compare')
    journey = importlib.import_module('editor_journey')
    report = json.loads((FOLDER / 'journey.json').read_text())
    comparison = json.loads((FOLDER / 'comparison.json').read_text())
    replay = journey.compare(FOLDER, report, proof)
    assert replay == comparison and replay['status'] == 'REJECTED'
    assert report['schema'] == 2 and report['plan_sha256'] == journey.fingerprint(journey.PLAN)
    records = {}
    reference_count = 0
    for entry in bound_artifacts(report):
        reference_count += 1
        proof.artifact(FOLDER, entry)
        if entry['path'] in records:
            assert records[entry['path']] == entry
        records[entry['path']] = entry
    assert [run['label'] for run in report['runs']] == ['original', 'candidate']
    assert [run['apk_sha256'] for run in report['runs']] == [proof.ORIGINAL_SHA256, 'be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce']
    assert report['runs'][0]['environment'] == report['runs'][1]['environment']
    run_analysis = []
    for run in report['runs']:
        assert run['status'] == 'FAILED' and run['current_step'] == 'home'
        assert len(run['screens']) == 6 and len(run['transitions']) == 5
        out, err = journey.evidence_command(FOLDER, run['absence'], proof, codes=(0, 1))
        assert proof.absence_ok(run['absence']['returncode'], out.decode(), err.decode())
        out, err = journey.evidence_command(FOLDER, run['install'], proof)
        assert proof.install_ok(0, out.decode(), err.decode())
        out, err = journey.evidence_command(FOLDER, run['installed_path'], proof)
        installed = proof.installed_path(0, out.decode(), err.decode())
        out, err = journey.evidence_command(FOLDER, run['installed_checksum'], proof)
        installed_digest = proof.installed_digest(0, out.decode(), err.decode(), installed)
        assert installed_digest == run['apk_sha256']
        out, err = journey.evidence_command(FOLDER, run['launch'], proof)
        assert proof.launch_ok(0, out.decode())
        states = []
        for screen_index, screen in enumerate(run['screens']):
            journey.validate_snapshot(FOLDER, screen, proof)
            artifacts = screen['artifacts']
            if screen_index < 5:
                name, owner, required, _ = journey.PLAN[screen_index]
                assert screen['name'] == name and screen['owner'] == owner
                journey.select(journey.tree(proof.artifact(FOLDER, artifacts['hierarchy']), owner), owner, required)
            pids = [proof.artifact(FOLDER, artifacts[key]).decode().strip() for key in ['pid_first', 'pid_final']]
            components = proof.resumed_components(proof.artifact(FOLDER, artifacts['foreground']).decode())
            states.append({'name': screen['name'], 'owner': screen['owner'], 'pids': pids,
                           'resumed_components': components, 'artifacts': artifacts})
        transitions = []
        for index, transition in enumerate(run['transitions']):
            previous = run['screens'][index]
            before = transition['before']
            prior = journey.validate_snapshot(FOLDER, previous, proof)
            state = journey.validate_snapshot(FOLDER, before, proof)
            assert prior[0] == state[0]
            assert transition['precondition_age_seconds'] <= 15
            live = transition['preinput_artifacts']
            proof.live_pids(proof.artifact(FOLDER, previous['artifacts']['pid_final']).decode(),
                            proof.artifact(FOLDER, before['artifacts']['pid_final']).decode())
            proof.live_pids(proof.artifact(FOLDER, before['artifacts']['pid_final']).decode(),
                            proof.artifact(FOLDER, live['pid']).decode())
            assert journey.resumed(proof.artifact(FOLDER, live['foreground']).decode(), previous['owner'])
            center = journey.target(proof.artifact(FOLDER, before['artifacts']['hierarchy']),
                                    before['owner'], transition['action'], state[1], state[2])
            assert transition['command']['argv'] == ['shell', 'input tap ' + ' '.join(map(str, center))]
            journey.evidence_command(FOLDER, transition['command'], proof, clean=True)
            transitions.append({'to': transition['to'], 'action': transition['action'], 'center': center,
                                'age_seconds': transition['precondition_age_seconds'], 'fresh_tree_pid_foreground_and_command_verified': True})
        assert [item['center'] for item in transitions] == [[640, 1152]] * 4 + [[360, 820]]
        run_analysis.append({'label': run['label'], 'installed_apk_sha256': installed_digest,
                             'fresh_install_and_launch_verified': True, 'status': run['status'],
                             'current_step': run['current_step'], 'reason': run['reason'],
                             'environment_after_recorded': 'environment_after' in run,
                             'screens': states, 'transitions': transitions,
                             'pid_changed_after_denial': states[4]['pids'][1] != states[5]['pids'][0]})
    recorded_inputs = [command for command in report['commands']
                       if command['argv'][0] == 'shell' and command['argv'][1].startswith('input ')]
    planned_inputs = [transition['command'] for run in report['runs'] for transition in run['transitions']]
    assert recorded_inputs == planned_inputs and len(recorded_inputs) == 10
    pairs = []
    for first, second in zip(*[run['screens'] for run in report['runs']]):
        assert first['name'] == second['name']
        state_a = journey.validate_snapshot(FOLDER, first, proof)
        state_b = journey.validate_snapshot(FOLDER, second, proof)
        png_a = FOLDER / first['artifacts']['screenshot']['path']
        png_b = FOLDER / second['artifacts']['screenshot']['path']
        rgba_a = np.asarray(Image.open(png_a).convert('RGBA'))
        rgba_b = np.asarray(Image.open(png_b).convert('RGBA'))
        assert rgba_a.shape == rgba_b.shape == (1280, 720, 4)
        mask = np.any(rgba_a != rgba_b, axis=2)
        yy, xx = np.where(mask)
        changed = int(mask.sum())
        independent_changed = sum(state_a[3][i:i+4] != state_b[3][i:i+4] for i in range(0, len(state_a[3]), 4))
        assert changed == independent_changed
        pairs.append({'name': first['name'], 'size': [720, 1280], 'changed_rgba_pixels': changed,
                      'difference_bounds_exclusive': None if not len(xx) else [int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1],
                      'png_bytes_equal': png_a.read_bytes() == png_b.read_bytes(),
                      'xml_bytes_equal': proof.artifact(FOLDER, first['artifacts']['hierarchy']) == proof.artifact(FOLDER, second['artifacts']['hierarchy']),
                      'complete_xml_tree_equal': state_a[0] == state_b[0], 'png_color_metadata_equal': state_a[4] == state_b[4],
                      'exact_observed_snapshot_equal': state_a == state_b,
                      'original': first['artifacts'], 'candidate': second['artifacts']})
    assert [pair['changed_rgba_pixels'] for pair in pairs] == [0, 35, 0, 0, 570819, 0]
    dialog = journey.tree((FOLDER / 'original-home.xml').read_bytes(), journey.PACKAGE)
    details = {}
    for label, selector in [('title', {'text': 'LITEAPKS'}), ('close', {'text': 'CLOSE'}), ('download', {'text': 'DOWNLOAD✅'})]:
        node = journey.select(dialog, journey.PACKAGE, selector)
        details[label] = dict(node.attrib)
    details['close_center'] = journey.target((FOLDER / 'original-home.xml').read_bytes(), journey.PACKAGE, {'text': 'CLOSE'}, 720, 1280)
    details['home_selector_matches'] = len([node for node in dialog.iter('node') if node.get('resource-id') == journey.PACKAGE + ':id/navigation_home'])
    host_text = (EXTRACTED / 'ci-editor/host-tests.log').read_text()
    assert re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', host_text, re.M) == [('23', '2.167')]
    analysis = {'status': 'MEASURED_PARTIAL_CAPTURES_WITH_DIFFERENCES', 'analyzed_utc': datetime.now(timezone.utc).isoformat(),
                'run_id': 38199371948, 'head_sha': manifest['head_sha'], 'archive_commit': '4f7e19d4d63c2f6ac4b3eba2cfa2de8604099ebb',
                'archive': meta(REPO_EVIDENCE / 'evidence.zip'), 'all_archive_members_verified': 740,
                'all_referenced_artifact_paths_verified': len(records), 'artifact_references_checked': reference_count,
                'host_tests': {'actual_count': 23, 'seconds': 2.167, 'passed': True},
                'preserved_comparison': comparison, 'exact_pinned_comparator_replay_matches': True,
                'actual_android_install_and_capture_observed': True,
                'requested_editor_journey_passed': False, 'full_runtime_1_to_1_established': False,
                'environment_before_runs_equal': True, 'environment': report['runs'][0]['environment'],
                'runs': run_analysis, 'full_unmasked_snapshot_pairs': pairs, 'observed_app_dialog': details,
                'interpretation': ['Both failed at the planned home selector after four Next actions and notification denial.',
                                   'The observed app-owned LITEAPKS dialog overlays NewHomeScreenActivity; its full PNG and full XML bytes match.',
                                   'Intro-2 has a 35-pixel difference around the pager indicators, and the permission-request full images differ by 570,819 pixels.',
                                   'Visual inspection shows different background dimming behind the permission dialog; the cause has not been established.',
                                   'Both app PIDs changed after denial; snapshots at the resulting dialog have stable live PIDs. The existing full-journey comparator retains one initial PID anchor.',
                                   'No editor screen was reached. No CLOSE, DOWNLOAD, macro save, macro execution, or permission grant command was issued.',
                                   'The original comparator android_runtime_executed=false is a completeness-gate field; actual installation and captures are preserved in both failed runs.'],
                'new_device_actions_performed_by_analysis': False}
    OUTPUT.mkdir()
    (OUTPUT / 'independent-analysis.json').write_text(json.dumps(analysis, indent=2) + '\n')
    for run in report['runs']:
        for screen in run['screens']:
            for entry in screen['artifacts'].values():
                destination = OUTPUT / 'captures' / entry['path']
                destination.parent.mkdir(exist_ok=True)
                shutil.copyfile(FOLDER / entry['path'], destination)
                assert meta(destination) == {key: entry[key] for key in ['bytes', 'sha256']}
    shutil.copyfile(Path(__file__), OUTPUT / Path(__file__).name)
    shutil.copytree(PINNED, OUTPUT / 'pinned-source', ignore=shutil.ignore_patterns('__pycache__'))
    print(json.dumps({'status': analysis['status'], 'archive_members': 740, 'artifact_paths': len(records),
                      'pairs': [{key: item[key] for key in ['name', 'changed_rgba_pixels', 'xml_bytes_equal']} for item in pairs],
                      'observed_close_center': details['close_center'], 'output': str(OUTPUT)}, indent=2))


if __name__ == '__main__':
    main()
