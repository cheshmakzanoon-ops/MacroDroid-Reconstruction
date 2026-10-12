#!/usr/bin/env python3
"""Compare unchanged full TRIGGERS frames from six pinned historical archives."""
from __future__ import annotations

import argparse
import hashlib
import io
import itertools
import json
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

BASE = Path('/workspace/scratch/4130730d15aa')
ROOT = Path(__file__).resolve().parent
PINNED = [
    ('android-ci-95077fc', 38194498356, 803571, '0f82b5480cf7a3d38c766cfed81a9a2f47087e057d03329c7953cb8df5608739'),
    ('android-ci-3a2e6ea', 38200503458, 1016845, 'fb22f6daa60ae9806b6c1e1980e3e129c7454337100779b5ac79f278c06471db'),
    ('android-ci-cada56c', 38202401393, 1022164, '552cfb1df46eb0fb324fde6468c9edee53611db2983ee7a60dc85179ccdf4891'),
    ('editor-journey/run-38202401351-attempt-1', 38202401351, 6517530, 'fa2eca5f893ae181b91aa7a7bf5df8320620bbc8da21b87eacffb1de0c3bc7ee'),
    ('editor-journey/run-38204928419-attempt-1', 38204928419, 10973841, '1120c0bdcff9d054a08bf3e52f733000597ca18c28a5a17230276e0fd7fad785'),
    ('editor-journey/run-38205737183-attempt-1', 38205737183, 15156144, 'f6760a909477b09e91cb9315c67c4c59146bbf454aecc50a72809d101749b2ca'),
]
ORIGINAL = '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'
OLD_CANDIDATE = 'be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce'
CANDIDATE = '9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2'
ENV_ALIASES = {'font_scale': 'system:font_scale', **{key: 'global:' + key for key in [
    'airplane_mode_on', 'wifi_on', 'mobile_data', 'sysui_demo_allowed', 'sysui_tuner_demo_on',
    'animator_duration_scale', 'window_animation_scale', 'transition_animation_scale']}}


def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def delta(a, b, coordinates=False):
    mask = np.any(a != b, axis=2)
    yy, xx = np.where(mask)
    result = {'full_rgba_changed_pixels': int(mask.sum()),
              'bounds_exclusive': None if not len(xx) else [int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1],
              'maximum_absolute_channel_delta': np.abs(a.astype(int) - b.astype(int)).max(axis=(0, 1)).tolist()}
    if coordinates:
        result['all_changed_coordinates'] = [{'x': int(x), 'y': int(y), 'left_rgba': a[y, x].tolist(), 'right_rgba': b[y, x].tolist()} for y, x in zip(yy, xx)]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=BASE / 'MacroDroid-Reconstruction')
    parser.add_argument('--output', type=Path, default=ROOT / 'analysis/cross-run-triggers')
    args = parser.parse_args()
    assert not args.output.exists(), 'Use a fresh output directory'
    args.output.mkdir(parents=True)
    rows, arrays = [], {}
    archives = []
    for relative, run_id, size, digest in PINNED:
        root = args.repo / 'docs/verification' / relative
        manifest_data = (root / 'manifest.json').read_bytes()
        manifest = json.loads(manifest_data)
        android = relative.startswith('android-ci-')
        data = b''.join((args.repo / part['path']).read_bytes() for part in manifest['parts']) if android else (root / 'evidence.zip').read_bytes()
        assert meta(data) == {'bytes': size, 'sha256': digest}
        archive_record = {'run_id': run_id, 'repository_directory': 'docs/verification/' + relative,
                          'archive': meta(data), 'manifest': meta(manifest_data)}
        archives.append(archive_record)
        with zipfile.ZipFile(io.BytesIO(data)) as zipped:
            prefix = 'capture/' if android else 'ci-editor/journey/'
            report_bytes = zipped.read(prefix + ('result.json' if android else 'journey.json'))
            report = json.loads(report_bytes)
            archive_record['report'] = {'member': prefix + ('result.json' if android else 'journey.json'), **meta(report_bytes)}
            assert [run['label'] for run in report['runs']] == ['original', 'candidate']
            for run in report['runs']:
                shot = run['intro_sequence']['pages'][1] if android else run['screens'][1]
                assert (shot['title'] if android else shot['name']) == ('TRIGGERS' if android else 'intro-2')
                assert run['apk_sha256'] == (ORIGINAL if run['label'] == 'original' else OLD_CANDIDATE if run_id == 38194498356 else CANDIDATE)
                identity = str(run_id) + '-' + run['label']
                saved = args.output / identity
                saved.mkdir()
                for key, entry in shot['artifacts'].items():
                    raw = zipped.read(prefix + entry['path'])
                    assert meta(raw) == {name: entry[name] for name in ['bytes', 'sha256']}
                    if key in ['screenshot', 'hierarchy']:
                        (saved / entry['path']).write_bytes(raw)
                image = np.asarray(Image.open(io.BytesIO(zipped.read(prefix + shot['artifacts']['screenshot']['path']))).convert('RGBA'))
                assert image.shape == (1280, 720, 4)
                arrays[identity] = image
                mapped_environment = {ENV_ALIASES.get(key, key): value for key, value in run['environment'].items()}
                rows.append({'id': identity, 'run_id': run_id, 'label': run['label'], 'apk_sha256': run['apk_sha256'],
                             'recorded_run_status': run['status'], 'artifacts': shot['artifacts'],
                             'recorded_environment': run['environment'], 'diagnostic_environment_keys_mapped': mapped_environment,
                             'full_raw_frame_shape': [1280, 720, 4]})
    current = {row['label']: row for row in rows if row['run_id'] == 38205737183}
    env = current['original']['diagnostic_environment_keys_mapped']
    for row in rows:
        mapping = row['diagnostic_environment_keys_mapped']
        row['all_current_recorded_environment_keys_present_and_equal'] = all(mapping.get(key) == value for key, value in env.items())
        row['additional_recorded_environment_fields'] = {key: value for key, value in mapping.items() if key not in env}
        assert row['all_current_recorded_environment_keys_present_and_equal']
        row['comparison_to_current_same_label'] = delta(arrays[row['id']], arrays[current[row['label']]['id']], coordinates=True)
    pairs = []
    for left, right in itertools.combinations(rows, 2):
        pairs.append({'left': left['id'], 'right': right['id'],
                      'same_apk_bytes': left['apk_sha256'] == right['apk_sha256'],
                      'same_full_png_bytes': left['artifacts']['screenshot']['sha256'] == right['artifacts']['screenshot']['sha256'],
                      'same_full_xml_bytes': left['artifacts']['hierarchy']['sha256'] == right['artifacts']['hierarchy']['sha256'],
                      **delta(arrays[left['id']], arrays[right['id']])})
    groups = {}
    for row in rows:
        groups.setdefault(row['artifacts']['screenshot']['sha256'], []).append(row['id'])
    original_old = next(row for row in rows if row['id'] == '38194498356-original')
    assert original_old['artifacts']['screenshot']['sha256'] == current['candidate']['artifacts']['screenshot']['sha256']
    assert delta(arrays[original_old['id']], arrays[current['original']['id']])['full_rgba_changed_pixels'] == 26
    result = {'schema': 1, 'scope': 'Diagnostic comparison of twelve unchanged complete TRIGGERS frames from six pinned archives',
              'archives': archives, 'frames': rows, 'all_66_full_frame_pairs': pairs,
              'full_png_byte_identity_groups': groups, 'all_twelve_full_xml_bytes_equal': len({row['artifacts']['hierarchy']['sha256'] for row in rows}) == 1,
              'environment_key_aliases_for_diagnostic_reporting_only': ENV_ALIASES,
              'all_current_reported_environment_fields_match_across_runs': True,
              'unrecorded_environment_or_renderer_state_equality_established': False,
              'original_apk_has_multiple_recorded_full_frame_renderings': True,
              'older_original_full_png_equals_current_candidate_full_png': True,
              'current_failure_changed': False, 'active_policy_changed': False,
              'normalization_mask_crop_or_tolerance_used': False,
              'cause_established': False, 'universal_cross_run_determinism_established': False,
              'interpretation': [
                  'The same original APK produced the current candidate byte-identical PNG in run38194498356 and a different PNG in later runs.',
                  'The current original/candidate PNG pair recurs byte-for-byte in both cada56 reconstruction and the earlier nine-screen editor artifact.',
                  'These observations disprove a universal one-rendering-per-APK assumption; they do not identify a renderer or application cause.',
                  'The different recorder scopes and unrecorded renderer state are not treated as controlled experimental equality.',
                  'No screenshot is selected to replace another; every original run result and the current26-pixel failure remains unchanged.',
              ]}
    (args.output / 'cross-run-analysis.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'full_png_identity_groups': groups,
                      'same_label_full_pixel_difference_from_current': {row['id']: row['comparison_to_current_same_label']['full_rgba_changed_pixels'] for row in rows},
                      'all_current_recorded_environment_fields_equal': True,
                      'older_original_png_equals_current_candidate_png': True, 'cause_established': False}, indent=2))


if __name__ == '__main__':
    main()
