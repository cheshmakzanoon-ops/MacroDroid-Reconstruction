#!/usr/bin/env python3
"""Keep old actual session evidence separate from the corrected policy's gate."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
ARCHIVED = ROOT.parent / 'MacroDroid-Reconstruction/docs/verification/editor-journey/run-38206460588-attempt-1'
OUT = ROOT / 'reports/04-actual-external-session'


def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def worker(source, report, output):
    sys.dont_write_bytecode = True
    sys.path[:0] = [str(source / 'tools/parity_journeys'), str(source / 'project')]
    import android_compare as proof
    import post_onboarding as session
    from supplied_reference_journey import load_plan
    result = session.compare_session(report.parent, json.loads(report.read_text()), load_plan(), proof)
    output.write_text(json.dumps(result, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker-source', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.worker_source:
        worker(args.worker_source, args.report, args.output)
        return
    assert not OUT.exists()
    OUT.mkdir(parents=True)
    archive_data = (ARCHIVED / 'evidence.zip').read_bytes()
    assert meta(archive_data) == {'bytes': 11576977, 'sha256': 'd22377dacd276c2c8ab2d52bfa639a912d1871c90757ebefc71af16d106cdff6'}
    manifest = json.loads((ARCHIVED / 'manifest.json').read_text())
    assert manifest['run_id'] == 38206460588 and manifest['head_sha'] == '934c6543dce0897975f52457717b3a70bd27ce00'
    members = {entry['path']: entry for entry in manifest['members']}
    assert len(members) == len(manifest['members']) == 2034
    raw = ROOT / 'external-session-raw'
    with zipfile.ZipFile(ARCHIVED / 'evidence.zip') as zipped:
        assert len(zipped.namelist()) == len(set(zipped.namelist())) == 2034
        assert set(zipped.namelist()) == set(members)
        for name, entry in members.items():
            data = zipped.read(name)
            assert meta(data) == {key: entry[key] for key in ['bytes', 'sha256']}
            path = raw / name
            assert path.resolve().is_relative_to(raw.resolve()) and not path.is_symlink()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    folder = raw / 'ci-editor/journey'
    report = json.loads((folder / 'journey.json').read_text())
    assert (folder / 'journey.json').read_bytes() == (ARCHIVED / 'journey.json').read_bytes()
    pins = json.loads((ROOT / 'input-manifest.json').read_text())['reviewed_source_pins']
    for relative, expected in pins.items():
        source = ROOT / 'inputs' / relative
        assert meta(source.read_bytes())['sha256'] == expected
        if relative.startswith('tools/parity_journeys/'):
            assert source.read_bytes() == (raw / relative).read_bytes()
    executions = []
    for label, source in [('historical', ROOT / 'inputs'), ('corrected', ROOT / 'worktree')]:
        output = OUT / (label + '-replay.json')
        result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker-source', str(source),
                                 '--report', str(folder / 'journey.json'), '--output', str(output)],
                                capture_output=True, timeout=180)
        (OUT / (label + '-stdout.log')).write_bytes(result.stdout)
        (OUT / (label + '-stderr.log')).write_bytes(result.stderr)
        assert result.returncode == 0, result.stderr.decode()
        executions.append({'label': label, 'returncode': result.returncode,
                           'post_onboarding_source': meta((source / 'tools/parity_journeys/post_onboarding.py').read_bytes()),
                           'result': json.loads(output.read_text())})
    historical, corrected = [entry['result'] for entry in executions]
    assert historical == json.loads((ARCHIVED / 'editor-session-comparison.json').read_text())
    assert historical['status'] == 'EXACT_POST_ONBOARDING_EDITOR_MATCH_ONLY'
    assert corrected['status'] == 'REJECTED' and corrected['reason'] == "'session_observation'"
    assert corrected['editor_session_equal'] is False
    continuous = json.loads((ARCHIVED / 'comparison.json').read_text())
    assert continuous['status'] == 'REJECTED'
    pairs = []
    for original, candidate in zip(report['runs'][0]['screens'][6:], report['runs'][1]['screens'][6:]):
        assert original['name'] == candidate['name']
        images = []
        for shot in [original, candidate]:
            for key in ['screenshot', 'hierarchy']:
                entry = shot['artifacts'][key]
                assert meta((folder / entry['path']).read_bytes()) == {name: entry[name] for name in ['bytes', 'sha256']}
            images.append(np.asarray(Image.open(folder / shot['artifacts']['screenshot']['path']).convert('RGBA')))
        assert images[0].shape == images[1].shape == (1280, 720, 4)
        changed = int(np.any(images[0] != images[1], axis=2).sum())
        a, b = [shot['artifacts']['hierarchy']['sha256'] for shot in [original, candidate]]
        pairs.append({'name': original['name'], 'changed_full_rgba_pixels': changed,
                      'full_xml_bytes_equal': a == b, 'original': original['artifacts'], 'candidate': candidate['artifacts']})
    assert len(pairs) == 10 and all(row['changed_full_rgba_pixels'] == 0 and row['full_xml_bytes_equal'] for row in pairs)
    result = {'schema': 1, 'status': 'HISTORICAL_SESSION_REPLAYED_NEW_CHRONOLOGY_GATE_PENDING_FRESH_CAPTURE',
              'run_id': 38206460588, 'head_sha': manifest['head_sha'],
              'archive_repository_path': 'docs/verification/editor-journey/run-38206460588-attempt-1/evidence.zip',
              'archive': meta(archive_data), 'all_2034_members_verified': True,
              'pinned_historical_source': pins, 'replays': executions,
              'unchanged_continuous_startup_result': continuous,
              'independent_complete_session_image_pairs': pairs,
              'historical_runtime_command_windows_present': True,
              'historical_absolute_capture_observation_intervals_present': False,
              'new_corrected_gate_passed': False, 'new_android_execution_performed': False,
              'historical_reports_or_sources_modified': False,
              'full_runtime_1_to_1_established': False,
              'scope_note': 'The historical comparator reports ten full matching session stills, but has reproduced guard gaps. New chronology cannot be inferred from capture durations. Both source policies and results remain separate.'}
    (OUT / 'actual-session-analysis.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'historical_result': historical['status'], 'corrected_result': corrected['status'],
                      'corrected_reason': corrected['reason'], 'full_pixel_vector': [row['changed_full_rgba_pixels'] for row in pairs],
                      'continuous_startup_result': continuous['status'], 'new_android_execution_performed': False}, indent=2))


if __name__ == '__main__':
    main()
