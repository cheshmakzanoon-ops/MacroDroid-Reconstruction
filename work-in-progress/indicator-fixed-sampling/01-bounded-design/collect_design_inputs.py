#!/usr/bin/env python3
"""Read exact frozen sources and existing captures for a design-only capsule.

This collector runs no Android command and imports no production recorder.
It writes only beneath its own new evidence/ directory. It does not copy APKs.
"""
from __future__ import annotations

import ast
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'evidence'
BASE = Path('/workspace/scratch/4130730d15aa')
REPO = BASE / 'MacroDroid-Reconstruction'
GIT = Path('/dev/shm/macrodroid-transfer-space-20261012/verification.git')
COMMIT = '6331410cfd2391389270564803623079e8355ad8'
GUARD = 'work-in-progress/trigger-category/05-physical-identity-host-success/replay-source'
DOSSIER = BASE / 'ink-indicator-study/checkpoints/01-source-and-ordering-dossier'
DOSSIER_SHA = '00cde07343d7d7a106171070b462b4b2879705d3f926f6f22abcaae90a97fce3'
READINESS_CP = Path('/dev/shm/macrodroid-notification-readiness/checkpoints/05-thirteen-screen-device-analysis/checkpoint.json')
READINESS_CP_SHA = '716e3cd70c54659f1b0b84a68a875d61d8c3b1b41e864eb36756938660612439'
PACKAGE = 'com.arlosoft.macrodroid'
SELECTED_IDS = [PACKAGE + ':id/' + name for name in ['titleText', 'button_next', 'indicator']]
PARENTS = [
    'tools/android/android-toolchain-pins.json',
    'tools/android/bootstrap_android_runtime.py',
    'tools/android/android_runtime_service.py',
    'tools/android/runtime_job.py',
    'tools/android/wait_android_ready.py',
    'tools/android/configure_capture_device.py',
    GUARD + '/tools/parity_journeys/editor_journey.py',
    GUARD + '/tools/parity_journeys/observed_journey.py',
    GUARD + '/project/android_compare.py',
    GUARD + '/project/android_acceptance.py',
    'scripts/assemble_artifact.py',
    'vendor/original/manifest.json',
    'work-in-progress/combined-recovery/05-full-acceptance/apk/manifest.json',
    '.github/workflows/editor-trigger-category.yml',
    'work-in-progress/trigger-category-workflow/02-zero-scale-workflow/prepare_trigger_journey.py',
    'work-in-progress/trigger-category-workflow/02-zero-scale-workflow/verify_trigger_journey.py',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def ident(data):
    return {'bytes': len(data), 'sha256': sha(data)}


def save(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(json.dumps(value, indent=2).encode() + b'\n')


def main():
    OUT.mkdir(exist_ok=False)
    before = {}

    def read(path, expected=None):
        path = Path(path)
        data = path.read_bytes()
        value = ident(data)
        if expected is not None:
            assert value == expected, (str(path), value, expected)
        previous = before.setdefault(str(path), value)
        assert previous == value
        return data

    cp_raw = read(DOSSIER / 'checkpoint.json')
    assert sha(cp_raw) == DOSSIER_SHA
    cp = json.loads(cp_raw)
    for row in cp['source_files'] + cp['review_evidence_files'] + [cp['evidence_archive']]:
        read(DOSSIER / row['path'], {'bytes': row['bytes'], 'sha256': row['sha256']})
    archive = read(DOSSIER / cp['evidence_archive']['path'])
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tf:
        files = [member for member in tf.getmembers() if member.isfile()]
        assert len(files) == len(cp['evidence_members']) == 135
        assert {m.name for m in files} == {row['path'] for row in cp['evidence_members']}
        for row in cp['evidence_members']:
            member = tf.getmember(row['path'])
            assert ident(tf.extractfile(member).read()) == {'bytes': row['bytes'], 'sha256': row['sha256']}
    save('dossier-verification.json', {
        'checkpoint': str(DOSSIER / 'checkpoint.json'), **ident(cp_raw),
        'source_files': len(cp['source_files']), 'review_files': len(cp['review_evidence_files']),
        'archive_members_verified': 135, 'archive_extracted': False,
        'cause_proven': cp['cause_proven'], 'android_proposal_executed': cp['android_proposal_executed'],
    })

    parent_rows = []
    for name in PARENTS:
        command = ['git', '--git-dir=' + str(GIT), 'show', COMMIT + ':' + name]
        result = subprocess.run(command, capture_output=True, timeout=15, check=True)
        assert not result.stderr
        data = result.stdout
        mode = subprocess.run(['git', '--git-dir=' + str(GIT), 'ls-tree', COMMIT, '--', name],
                              capture_output=True, timeout=15, check=True).stdout.decode().split()[0]
        row = {'commit': COMMIT, 'path': name, 'mode': mode, **ident(data)}
        if name.endswith('.py'):
            tree = ast.parse(data)
            row['definitions'] = [
                {'name': n.name, 'start_line': n.lineno, 'end_line': n.end_lineno}
                for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
        parent_rows.append(row)
    save('parent-bindings.json', {'fetched_git_commit': COMMIT, 'files': parent_rows,
                                'materialized_or_executed': False})

    older_cp = REPO / 'docs/verification/editor-journey/run-38205737183-attempt-1/analysis/checkpoint.json'
    older = json.loads(read(older_cp))
    older_path = older_cp.parent / 'triggers-pixel-diagnosis.json'
    row = next(row for row in older['files'] if row['path'] == 'triggers-pixel-diagnosis.json')
    older_pixels = json.loads(read(older_path, {'bytes': row['bytes'], 'sha256': row['sha256']}))
    assert older_pixels['run_id'] == 38205737183 and older_pixels['changed_rgba_pixels'] == 26
    save('run-38205737183-coordinates.json', {
        'run_id': 38205737183, 'checkpoint': str(older_cp), **before[str(older_cp)],
        'report_path': str(older_path), 'report_identity': before[str(older_path)],
        'source_commit': older['source_commit'], 'archive_commit': older['archive_commit'],
        'coordinates': older_pixels['coordinates'], 'difference_bounds_exclusive': older_pixels['difference_bounds_exclusive'],
        'raw_selected_frames': older_pixels['selected_frames'],
        'all_eight_retained_frames_replayed_by_parent': older_pixels['same_26_cross_apk_differences_in_every_triggers_frame'],
        'this_collector_replayed_older_raw_pixels': False,
    })

    readiness_cp_raw = read(READINESS_CP)
    assert sha(readiness_cp_raw) == READINESS_CP_SHA
    configs = [
        (38216299675, BASE / 'ci-run-analysis/zero12-run-38216299675-extracted/journey',
         'a6253dfea14353a2d8fe552e3772e4fe5e58a693e2339bafcce9f0d008a61409', 5,
         'docs/verification/android-trigger-category-6331410/extracted/journey'),
        (38221713675, BASE / 'ci-run-analysis/daytime13-run-38221713675-extracted/journey',
         None, 0, 'docs/verification/android-day-time-trigger-e610d98/extracted/journey'),
        (38230072388, Path('/dev/shm/macrodroid-transfer-space-20261012/readiness-run-38230072388/extracted/journey'),
         '0d4565b26a98b4a21d4294ae895fc8ac7c3e32dc313767312e8c9d06f64b8d92', 26,
         'docs/verification/android-day-time-readiness-e1ade015/extracted/journey'),
    ]
    histories = []
    for run_id, folder, expected_journey_sha, expected_pixels, repo_prefix in configs:
        raw = read(folder / 'journey.json')
        if expected_journey_sha:
            assert sha(raw) == expected_journey_sha
        journey = json.loads(raw)
        assert [r['label'] for r in journey['runs']] == ['original', 'candidate']
        images, observations = {}, []
        for run in journey['runs']:
            label = run['label']
            assert run['apk_sha256'] == {
                'original': '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800',
                'candidate': '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182',
            }[label]
            shot = next(s for s in run['screens'] if s['name'] == 'intro-2')
            a = shot['artifacts']
            png = read(folder / a['screenshot']['path'], {k: a['screenshot'][k] for k in ['bytes', 'sha256']})
            xml = read(folder / a['hierarchy']['path'], {k: a['hierarchy'][k] for k in ['bytes', 'sha256']})
            pixels = np.asarray(Image.open(io.BytesIO(png)).convert('RGBA'))
            assert pixels.shape == (1280, 720, 4)
            images[label] = pixels
            nodes = [n.attrib for n in ET.fromstring(xml).iter('node') if n.get('resource-id') in SELECTED_IDS]
            assert len(nodes) == 3
            transition = next(t for t in run['transitions'] if t['to'] == 'intro-2')
            assert transition['command']['argv'] == ['shell', 'input tap 640 1152']
            before_art = transition['before']['artifacts']
            pre_xml = read(folder / before_art['hierarchy']['path'],
                           {k: before_art['hierarchy'][k] for k in ['bytes', 'sha256']})
            root = ET.fromstring(pre_xml)
            pre_nodes = [n.attrib for n in root.iter('node') if n.get('resource-id') in SELECTED_IDS]
            next_node = next(n for n in pre_nodes if n['resource-id'].endswith('/button_next'))
            assert next_node['bounds'] == '[592,1104][688,1200]'
            assert next_node['class'] == 'android.widget.ImageButton'
            assert next_node['content-desc'] == 'Next'
            assert next_node['enabled'] == next_node['clickable'] == 'true'
            foreground = read(folder / before_art['foreground']['path'],
                              {k: before_art['foreground'][k] for k in ['bytes', 'sha256']})
            resume_lines = [line.strip() for line in foreground.decode().splitlines()
                            if re.search(r'(?:mResumedActivity|topResumedActivity|ResumedActivity):', line)]
            assert resume_lines and all('com.arlosoft.macrodroid/.intro.IntroActivity' in line for line in resume_lines)
            observations.append({
                'label': label, 'status': run['status'], 'completed_screens': len(run['screens']),
                'apk_sha256': run['apk_sha256'], 'environment': run['environment'],
                'intro2_artifacts': a, 'raw_folder': str(folder), 'published_raw_folder': repo_prefix,
                'intro2_nodes': nodes, 'preinput_nodes': pre_nodes,
                'preinput_hierarchy': before_art['hierarchy'], 'preinput_foreground': before_art['foreground'],
                'literal_resumed_lines': resume_lines, 'tap': transition['command'],
            })
            if run_id == 38230072388:
                for stem, data in [('intro1-preinput', pre_xml), ('intro2', xml)]:
                    path = OUT / 'observed-xml' / (label + '-' + stem + '.xml')
                    path.parent.mkdir(exist_ok=True)
                    with path.open('xb') as stream:
                        stream.write(data)
        positions = np.argwhere(np.any(images['original'] != images['candidate'], axis=2))
        assert len(positions) == expected_pixels
        coordinates = [{'x': int(x), 'y': int(y), 'original_rgba': images['original'][y, x].tolist(),
                        'candidate_rgba': images['candidate'][y, x].tolist()} for y, x in positions]
        histories.append({
            'run_id': run_id, 'journey_identity': ident(raw), 'journey_path': str(folder / 'journey.json'),
            'journey_status': journey['status'], 'schema': journey['schema'], 'observations': observations,
            'full_frame_shape_rgba': [1280, 720, 4], 'changed_pixels': len(positions), 'coordinates': coordinates,
            'full_frame_compared': True, 'images_modified': False, 'new_android_execution': False,
        })
    save('fixed-historical-capture-bindings.json', histories)
    for name, expected in before.items():
        assert ident(Path(name).read_bytes()) == expected, 'Read input changed: ' + name
    save('read-only-input-verification.json', {
        'status': 'EXACT_DESIGN_INPUTS_READ_AND_UNCHANGED',
        'finished_utc': datetime.now(timezone.utc).isoformat(),
        'files': [{'path': name, **value} for name, value in sorted(before.items())],
        'git_parent_files': len(parent_rows), 'git_network_access_performed': False,
        'raw_zip_whole_containers_reverified_by_this_collector': False,
        'dossier_archive_members_verified': 135, 'actual_png_pairs_redecoded': 3,
        'new_android_execution': False, 'apk_source_or_active_policy_modified': False,
    })
    print(json.dumps({'status': 'EXACT_DESIGN_INPUTS_READ_AND_UNCHANGED',
                      'read_files': len(before), 'parent_files': len(parent_rows),
                      'pixel_counts_by_run': {str(h['run_id']): h['changed_pixels'] for h in histories}}))


if __name__ == '__main__':
    main()
