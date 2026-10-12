#!/usr/bin/env python3
"""Measure every retained normal-animation frame without changing or selecting it."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from itertools import combinations, product
import json
from pathlib import Path, PurePosixPath
import re
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image

RUN = 38212813248
HEAD = '3edcddd86660ea10c8aff71b651b446f86412525'
ZIP_SHA = '93cfed4c5f5c17170a926bd79781807422698c22b26cf7afc60430b2a7183d92'
APKS = {
    'original': '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800',
    'candidate': '9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2',
}
REGIONS = {
    'lottie_view_from_actual_xml': [0, 531, 720, 1011],
    'indicator_view_from_actual_xml': [128, 1184, 592, 1200],
    'historical_26_pixel_difference_bounds': [313, 1184, 352, 1200],
}


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def checked(folder, row):
    name = row['path']
    rel = PurePosixPath(name)
    assert rel.as_posix() == name and not rel.is_absolute() and '..' not in rel.parts
    path = folder / name
    assert path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(folder)
    assert identity(path) == {key: row[key] for key in ('bytes', 'sha256')}, name
    return path


def bounds(mask):
    ys, xs = np.nonzero(mask)
    return None if not len(xs) else [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def differences(left, right):
    assert left.shape == right.shape == (1280, 720, 4)
    delta = np.abs(left.astype(np.int16) - right.astype(np.int16))
    mask = np.any(delta != 0, axis=2)
    region_counts = {}
    for name, (x0, y0, x1, y1) in REGIONS.items():
        region_counts[name] = int(mask[y0:y1, x0:x1].sum())
    return {
        'changed_pixels': int(mask.sum()), 'difference_bounds_exclusive': bounds(mask),
        'maximum_absolute_rgba_difference': delta.max(axis=(0, 1)).tolist(),
        'diagnostic_region_changed_pixels': region_counts,
        'changed_pixels_outside_xml_lottie_view': int(mask.sum()) - region_counts['lottie_view_from_actual_xml'],
        'changed_rows': [{'y': int(y), 'pixels': int(mask[y].sum())} for y in np.flatnonzero(mask.any(axis=1))],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifact', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    folder = args.artifact.resolve()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    receipt = json.loads(args.receipt.read_text())
    assert receipt['run_id'] == RUN and receipt['head_sha'] == HEAD
    assert receipt['archive'] == {'bytes': 28080813, 'sha256': ZIP_SHA}
    assert len(receipt['files']) == receipt['member_count'] == 952
    inventory = {r['path']: {k: r[k] for k in ('bytes', 'sha256')} for r in receipt['files']}
    assert len(inventory) == 952
    actual_names = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
    assert actual_names == set(inventory)
    for row in receipt['files']:
        checked(folder, row)

    journey_dir = folder / 'journey'
    journey = json.loads((journey_dir / 'journey.json').read_text())
    all_referenced = set()

    def verify_references(value):
        if isinstance(value, dict):
            if set(('path', 'bytes', 'sha256')).issubset(value):
                all_referenced.add(checked(journey_dir, value).relative_to(journey_dir).as_posix())
            for item in value.values():
                verify_references(item)
        elif isinstance(value, list):
            for item in value:
                verify_references(item)

    verify_references(journey)
    assert len(journey['runs']) == 2 and len(journey['commands']) == 226
    ledgers, arrays, frame_rows, run_rows = {}, {}, {}, []
    for run in journey['runs']:
        label = run['label']
        assert run['apk_sha256'] == APKS[label]
        assert run['status'] == 'FAILED' and run['current_step'] == 'intro-2'
        assert len(run['screens']) == len(run['transitions']) == 1
        assert run['screens'][0]['name'] == 'intro-1'
        installed = checked(journey_dir, run['installed_path']['stdout']).read_text().strip()
        assert installed.startswith('package:/data/app/') and '\n' not in installed
        installed = installed.removeprefix('package:')
        checksum = checked(journey_dir, run['installed_checksum']['stdout']).read_text().strip().split()
        assert checksum == [APKS[label], installed]
        for key in ('animator_duration_scale', 'window_animation_scale', 'transition_animation_scale'):
            assert run['environment']['global:' + key] in ('1', '1.0')
        transition = run['transitions'][0]
        tap = transition['command']
        assert tap['argv'] == ['shell', 'input tap 640 1152'] and tap['returncode'] == 0 and not tap['timed_out']
        ledger_path = journey_dir / f'{label}-intro-2-acquisition-1-settling.json'
        ledger = json.loads(ledger_path.read_text())
        verify_references(ledger)
        assert ledger['status'] == 'FAILED' and ledger['max_attempts'] == 6 and ledger['max_seconds'] == 30
        assert len(ledger['attempts']) == (5 if label == 'original' else 6)
        ledgers[label] = ledger
        frame_rows[label], arrays[label] = [], []
        for index, attempt in enumerate(ledger['attempts'], 1):
            png = checked(journey_dir, attempt['artifacts']['screenshot'])
            xml = checked(journey_dir, attempt['artifacts']['hierarchy'])
            tree = ET.fromstring(xml.read_bytes())
            title = [n for n in tree.iter('node') if n.get('resource-id') == 'com.arlosoft.macrodroid:id/titleText']
            assert len(title) == 1 and title[0].get('text') == 'TRIGGERS'
            for resource, expected in [('lottieAnimationView', REGIONS['lottie_view_from_actual_xml']),
                                       ('indicator', REGIONS['indicator_view_from_actual_xml'])]:
                nodes = [n for n in tree.iter('node') if n.get('resource-id') == 'com.arlosoft.macrodroid:id/' + resource]
                assert len(nodes) == 1 and [int(x) for x in re.findall(r'\d+', nodes[0].get('bounds'))] == expected
            array = np.asarray(Image.open(png).convert('RGBA'))
            assert array.shape == (1280, 720, 4)
            arrays[label].append(array)
            obs = attempt['observation']
            assert obs['started_monotonic'] > tap['finished_monotonic']
            if index > 1:
                assert obs['started_monotonic'] > ledger['attempts'][index - 2]['observation']['finished_monotonic']
            region_hashes = {}
            for name, (x0, y0, x1, y1) in REGIONS.items():
                region_hashes[name] = hashlib.sha256(array[y0:y1, x0:x1].tobytes()).hexdigest()
            frame_rows[label].append({
                'frame_number': index, 'png': attempt['artifacts']['screenshot'],
                'xml': attempt['artifacts']['hierarchy'], 'observation': obs,
                'observation_seconds': obs['finished_monotonic'] - obs['started_monotonic'],
                'started_seconds_after_tap_completed': obs['started_monotonic'] - tap['finished_monotonic'],
                'finished_seconds_after_tap_completed': obs['finished_monotonic'] - tap['finished_monotonic'],
                'diagnostic_region_rgba_sha256': region_hashes,
            })
        commands = [c for c in journey['commands'] if ledger['started_monotonic'] <= c['started_monotonic'] <= ledger['finished_monotonic']]
        run_rows.append({
            'label': label, 'apk_sha256': APKS[label], 'installed_path': installed,
            'environment': run['environment'], 'environment_after_present': 'environment_after' in run,
            'status': run['status'], 'reason': run['reason'], 'accepted_screen_count': 1,
            'input_count': 1, 'tap': tap, 'failed_ledger': {'path': ledger_path.name, **identity(ledger_path)},
            'settling_started_monotonic': ledger['started_monotonic'],
            'settling_finished_monotonic': ledger['finished_monotonic'],
            'settling_seconds': ledger['seconds'], 'retained_frames': len(ledger['attempts']),
            'commands_during_failed_settling': commands,
        })

    pairs = []
    for label in ('original', 'candidate'):
        for a, b in combinations(range(len(arrays[label])), 2):
            pairs.append({'kind': 'within_apk', 'left': [label, a + 1], 'right': [label, b + 1],
                          'consecutive': b == a + 1, **differences(arrays[label][a], arrays[label][b])})
    for a, b in product(range(len(arrays['original'])), range(len(arrays['candidate']))):
        pairs.append({'kind': 'cross_apk_diagnostic_only', 'left': ['original', a + 1], 'right': ['candidate', b + 1],
                      'consecutive': False, **differences(arrays['original'][a], arrays['candidate'][b])})
    assert len(pairs) == 55
    intro = [checked(journey_dir, r['screens'][0]['artifacts']['screenshot']) for r in journey['runs']]
    intro_measurement = differences(*[np.asarray(Image.open(p).convert('RGBA')) for p in intro])
    xml_hashes = {f['xml']['sha256'] for rows in frame_rows.values() for f in rows}
    indicator_hashes = {f['diagnostic_region_rgba_sha256']['indicator_view_from_actual_xml'] for rows in frame_rows.values() for f in rows}
    result = {
        'schema': 1, 'status': 'FAILED_NORMAL_ANIMATION_CAPTURE_MEASURED',
        'run_id': RUN, 'head_sha': HEAD, 'archive_sha256': ZIP_SHA,
        'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
        'verified_raw_files': len(inventory), 'verified_journey_referenced_files': len(all_referenced),
        'verified_journey_commands': len(journey['commands']), 'diagnostic_regions': REGIONS,
        'coordinate_convention': 'Full-frame integer pixels; bounds include left/top and exclude right/bottom.',
        'regions_change_acceptance': False, 'images_written_or_modified': False,
        'frame_selection_for_cross_apk_equality': False, 'all_retained_intro2_frames': frame_rows,
        'all_55_frame_pair_measurements': pairs, 'runs': run_rows,
        'intro1_accepted_pair_diagnostic': intro_measurement,
        'intro2_xml_distinct_sha256': sorted(xml_hashes),
        'intro2_indicator_region_distinct_rgba_sha256': sorted(indicator_hashes),
        'all_consecutive_pairs_have_changed_full_frames': all(p['changed_pixels'] > 0 for p in pairs if p['consecutive']),
        'all_55_pair_differences_confined_to_actual_lottie_view': all(p['changed_pixels_outside_xml_lottie_view'] == 0 for p in pairs),
        'historical_scale_zero_failure_rewritten': False, 'complete_ten_screen_comparison': False,
        'animation_timing_parity_established': False, 'full_runtime_1_to_1_established': False,
    }
    for row in receipt['files']:
        checked(folder, row)
    result['raw_artifact_files_unchanged_after_measurement'] = True
    (out / 'frame-measurements.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({
        'status': result['status'], 'raw_files': 952, 'pair_count': 55,
        'adjacent_differences': {label: [p['changed_pixels'] for p in pairs if p['left'][0] == label and p['consecutive']] for label in APKS},
        'all_differences_confined_to_lottie_view': result['all_55_pair_differences_confined_to_actual_lottie_view'],
        'xml_variants': len(xml_hashes), 'indicator_variants': len(indicator_hashes),
        'intro1_changed_pixels': intro_measurement['changed_pixels'],
        'output': str(out / 'frame-measurements.json'),
    }, indent=2))


if __name__ == '__main__':
    main()
