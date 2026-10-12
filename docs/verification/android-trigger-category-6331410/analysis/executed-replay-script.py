#!/usr/bin/env python3
"""Replay the complete, unequal zero-scale twelve-screen artifact without ADB."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

import numpy as np
from PIL import Image

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
RAW = BASE / 'zero12-run-38216299675-extracted'
OUT = BASE / 'zero12-run-38216299675-analysis'
HEAD = '6331410cfd2391389270564803623079e8355ad8'
PACKAGE = 'work-in-progress/trigger-category-workflow/02-zero-scale-workflow'
PINS = {
    '.github/workflows/editor-trigger-category.yml': 'e3e53daf3c53c315605580aa49ff5d2ffda7c99b1dcb8014c5692dbfc22570fe',
    PACKAGE + '/prepare_trigger_journey.py': 'd4f33a794cbe6b03d6e456e9a7731e016b4d5d4620f90d6397fa615fd94a1a3d',
    PACKAGE + '/verify_trigger_journey.py': '83b23a8c2c5bd33f7629aec343e13630f1b3dcab7b2ca2f3d9bd28f3828cc406',
}
APKS = [
    (BASE.parent / 'recovered/automation android app', 'MacroDroid-5.67.8-original.apk', 95725918,
     '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'),
    (Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/dist/MacroDroid-5.67.8-v9-hybrid.apk'),
     'MacroDroid-5.67.8-combined-plugin-widget-hybrid.apk', 94683119,
     '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'),
]
ARCHIVE = {'bytes': 42199893, 'sha256': '1ea3ad6302d53c2fcc8341c03deec7ccd04d729facaf5658acb87e4aebc6f4b3'}


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
    assert len(expected) == len(receipt['files']) == 2944
    actual = {}
    for p in RAW.rglob('*'):
        assert not p.is_symlink()
        if p.is_file():
            actual[p.relative_to(RAW).as_posix()] = identity(p)
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
    archive = BASE / 'zero12-run-38216299675.zip'
    assert identity(archive) == ARCHIVE
    receipt = json.loads((BASE / 'zero12-run-38216299675-extracted-extraction.json').read_text())
    assert receipt['run_id'] == 38216299675 and receipt['head_sha'] == HEAD
    original_inventory = inventory(receipt)
    assert receipt['key_scan_findings'] == ['environment/emulator-boot.log']
    boot = (RAW / 'environment/emulator-boot.log').read_text()
    key_lines = [line for line in boot.splitlines() if 'adb.pubkey=' in line]
    assert len(key_lines) == 1 and 'PRIVATE KEY' not in boot
    # Keep the exact raw log/ZIP. This separately named review copy changes one
    # ephemeral public value only, never an image, hierarchy or verifier input.
    replacement = re.sub(r'(?m)(^.*?adb\.pubkey=)[^\r\n]*', r'\1[EPHEMERAL ADB PUBLIC VALUE OMITTED IN REVIEW COPY]', boot)
    assert replacement != boot
    (OUT / 'emulator-boot-public-value-omitted.review.log').write_text(replacement)
    write('review-log-transformation.json', {
        'raw_path': 'environment/emulator-boot.log', 'raw': identity(RAW / 'environment/emulator-boot.log'),
        'review_path': 'emulator-boot-public-value-omitted.review.log',
        'review': identity(OUT / 'emulator-boot-public-value-omitted.review.log'),
        'changed_lines': 1, 'transformation': 'Only the existing adb.pubkey value is omitted in this explicitly labeled review copy.',
        'raw_archive_and_raw_log_unchanged': True,
        'scan_scope': 'The extractor scanned every member for its documented private-header/token/ADB-key-filename patterns; one public-value line matched, no private-key pattern matched.',
        'public_value_printed_or_used_as_a_private_credential': False})
    for name, digest in PINS.items():
        assert identity(RAW / 'executed-inputs' / name)['sha256'] == digest
    for path, _, size, digest in APKS:
        assert identity(path) == {'bytes': size, 'sha256': digest}
    print(json.dumps({'checkpoint': '2944_RAW_FILES_AND_FIXED_APKS_VERIFIED', 'source_pins': PINS}), flush=True)

    omitted_bytecode = []
    with tempfile.TemporaryDirectory(prefix='macrodroid-zero12-replay-') as temporary:
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
                if relative == 'trigger-category-verification.json':
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
        assert len(expected) == 192 and preflight['github_sha'] == HEAD
        assert not any('__pycache__' in row['path'] or '__pycache__' in row['copy'] for row in expected)
        write('independently-reconstructed-192-inputs.json', expected)
        literal = verification.verify(root, shadow)
        recorded = json.loads((RAW / 'trigger-category-verification.json').read_text())
        omit_time = lambda value: {k: v for k, v in value.items() if k != 'verified_at_utc'}
        assert omit_time(literal) == omit_time(recorded)
        assert literal['status'] == 'TRIGGER_CATEGORY_TWELVE_SCREEN_DIFFERENCE'
        assert literal['evidence_valid'] is True and literal['journey_equal'] is False
        assert literal['changed_pixels'] == [0,5,0,0,0,0,0,0,0,0,0,0]
        write('literal-final-verifier-replay.json', literal)
        print(json.dumps({'checkpoint': 'EXACT_FINAL_VERIFIER_REPRODUCED',
                          'evidence_valid': True, 'pixel_vector': literal['changed_pixels']}), flush=True)
        import enable_still_animations as scales
        import trigger_category_journey as category
        import observed_journey as observed
        import capture_chronology as chronology
        import editor_journey as runner
        import android_compare as proof
        settings_folder = shadow / 'animation-settings'
        settings = json.loads((settings_folder / 'animation-scales.json').read_text())
        assert scales.verify_report(settings_folder, settings) == {key: '0' for key in scales.SCALES}
        assert len(settings['commands']) == 19 and settings['android_executed'] is True
        folder = shadow / 'journey'
        report = json.loads((folder / 'journey.json').read_text())
        comparison = json.loads((folder / 'comparison.json').read_text())
        assert literal['comparison'] == comparison
        assert comparison['catalog_navigation_established'] is True and comparison['trigger_selected'] is False
        assert comparison['post_crash_continuation_observed_in_both'] is True
        assert comparison['crash_free_run_established'] is False
        refs = {}
        for row in artifacts(report):
            proof.artifact(folder, row)
            assert refs.setdefault(row['path'], row) == row
        observations = []
        raw_events = []
        for event in report['capture_events']:
            ledger = json.loads(proof.artifact(folder, event))
            raw_events.append({'event': event, 'status': ledger.get('status'), 'attempts': len(ledger['attempts'])})
            for attempt in ledger['attempts']:
                for row in artifacts(attempt):
                    proof.artifact(folder, row)
                    assert refs.setdefault(row['path'], row) == row
                observations.append({'ledger': event['path'], 'observation': attempt['observation'],
                                     'artifacts': attempt['artifacts']})
        write('all-recorded-acquisition-observations.json', observations)
        write('all-capture-ledger-identities.json', raw_events)
        write('all-unique-journey-artifact-references.json', list(refs.values()))
        pairs = []
        review_captures = OUT / 'review-captures'
        review_captures.mkdir()
        for original, candidate in zip(report['runs'][0]['screens'], report['runs'][1]['screens']):
            assert original['name'] == candidate['name']
            arrays, xmls = [], []
            for shot in (original, candidate):
                for row in shot['artifacts'].values():
                    data = proof.artifact(folder, row)
                    target = review_captures / row['path']
                    assert not target.exists()
                    target.write_bytes(data)
                arrays.append(np.asarray(Image.open(folder / shot['artifacts']['screenshot']['path']).convert('RGBA')))
                xmls.append(proof.artifact(folder, shot['artifacts']['hierarchy']))
            assert arrays[0].shape == arrays[1].shape == (1280, 720, 4)
            yy, xx = np.where(np.any(arrays[0] != arrays[1], axis=2))
            pair = {'name': original['name'], 'size': [720, 1280], 'changed_rgba_pixels': len(xx),
                    'bounds_exclusive': [int(xx.min()), int(yy.min()), int(xx.max()+1), int(yy.max()+1)] if len(xx) else None,
                    'png_bytes_equal': original['artifacts']['screenshot']['sha256'] == candidate['artifacts']['screenshot']['sha256'],
                    'xml_bytes_equal': xmls[0] == xmls[1], 'original': original, 'candidate': candidate}
            if len(xx):
                pair['all_changed_rgba_pixels'] = [{'x': int(x), 'y': int(y),
                    'original_rgba': arrays[0][y,x].tolist(), 'candidate_rgba': arrays[1][y,x].tolist()} for y,x in zip(yy,xx)]
            pairs.append(pair)
        assert [p['changed_rgba_pixels'] for p in pairs] == literal['changed_pixels']
        assert all(p['xml_bytes_equal'] for p in pairs)
        write('all-twelve-full-frame-pairs.json', pairs)
        device_path = shadow / 'device/capture-device.json'
        device = json.loads(device_path.read_text())
        device_refs = {}
        for command in device['commands']:
            assert command['exit_code'] == 0
            for stream in ('stdout','stderr'):
                row = command[stream]
                proof.artifact(device_path.parent, row)
                assert row['path'] not in device_refs
                device_refs[row['path']] = row
        write('configuration-summary.json', {
            'device_status': device['status'], 'device_commands': len(device['commands']),
            'device_output_hashes_verified': len(device_refs),
            'confirmed_primary_signal': device['confirmed_primary_signal'],
            'signal_stable_seconds': device['signal_stable_seconds'],
            'demo_clock_requested': device['demo_clock_requested'],
            'device_helper_disable_animations_requested': device['disable_animations_requested'],
            'separate_explicit_scale_zero_commands_verified': 19,
            'animation_scales': settings['observed_scales'],
            'animation_settings': identity(settings_folder / 'animation-scales.json'),
            'all_run_before_and_after_environments_equal': len({json.dumps(r[k],sort_keys=True) for r in report['runs'] for k in ('environment','environment_after')}) == 1})
        host = []
        for name, count in [('journey-host-tests.log',130),('animation-host-tests.log',10),('download-tests.log',6)]:
            text = (RAW / name).read_text()
            summaries = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', text, re.M)
            headers = re.findall(r'^test_\S+ \(.*\) \.\.\. ', text, re.M)
            successes = len(re.findall(r'(?:\.\.\. |^)ok$', text, re.M))
            assert len(summaries) == 1 and int(summaries[0][0]) == len(headers) == successes == count
            assert text.rstrip().endswith('\nOK')
            host.append({'path': name, **identity(RAW / name), 'tests': count,
                         'seconds': float(summaries[0][1]), 'individual_successes': successes})
        write('verified-host-test-summaries.json',host)
        cleanup = json.loads((RAW / 'runtime-cleanup.json').read_text())
        assert cleanup['journey_step_exit_code'] == '2' and cleanup['service_cleanup_confirmed'] is True
        assert all(cleanup[key] == '0' for key in ('diagnostic_logcat_exit_code','owned_stop_marker_exit_code',
                                                  'bounded_service_wait_exit_code','owned_service_exit_code'))
        modules = {}
        for module in (preparation,verification,scales,category,observed,chronology,runner,proof):
            path = Path(module.__file__).resolve()
            relative = str(path.relative_to(root)) if path.is_relative_to(root) else 'artifact/' + str(path.relative_to(shadow))
            modules[module.__name__] = {'private_replay_path': relative, **identity(path)}
        write('imported-exact-source-modules.json', modules)
    assert inventory(receipt) == original_inventory
    assert identity(archive) == ARCHIVE
    for path, _, size, digest in APKS:
        assert identity(path) == {'bytes': size, 'sha256': digest}
    write('all-2944-member-identities.json', [{'path': p, **value} for p,value in sorted(original_inventory.items())])
    result = {'schema': 1, 'status': 'EXACT_COMPLETE_ZERO12_EVIDENCE_REPLAYED_WITH_FIVE_PIXEL_INTRO_DIFFERENCE',
              'run_id': 38216299675, 'head_sha': HEAD, 'started_utc': started,
              'finished_utc': datetime.now(timezone.utc).isoformat(), 'archive': ARCHIVE,
              'artifact_id': 11732104868, 'raw_files_verified_before_and_after': 2944,
              'independently_reconstructed_input_copy_roles': 192, 'source_pins': PINS,
              'literal_verifier_reproduced_except_replay_timestamp': True,
              'exact_captured_comparison_object_reproduced': True,
              'evidence_valid': True, 'journey_equal': False,
              'full_rgba_pixel_vector': literal['changed_pixels'],
              'capture_ledgers': len(raw_events), 'recorded_observations': len(observations),
              'unique_referenced_journey_artifacts_checked': len(refs),
              'unexecuted_raw_bytecode_files_omitted_only_from_private_replay_views': sorted(set(omitted_bytecode)),
              'zero_scale_configuration_commands_verified': 19,
              'device_configuration_streams_verified': len(device_refs),
              'host_test_summaries': host, 'owned_cleanup_result': cleanup,
              'catalog_navigation_established': True, 'trigger_selected': False,
              'post_crash_continuation_observed_in_both': True, 'crash_free_run_established': False,
              'full_runtime_1_to_1_established': False, 'animation_timing_parity_established': False,
              'masks_or_pixel_tolerance_used': False, 'new_android_actions': [],
              'original_raw_evidence_or_apks_modified': False,
              'large_input_copies_created_for_replay': False,
              'private_hardlink_replay_directory_removed': True,
              'raw_public_key_value_kept_only_in_exact_original_evidence': True}
    write('independent-zero12-analysis.json', result)
    print(json.dumps({k:result[k] for k in ('status','raw_files_verified_before_and_after',
        'independently_reconstructed_input_copy_roles','full_rgba_pixel_vector','capture_ledgers',
        'recorded_observations','unique_referenced_journey_artifacts_checked','device_configuration_streams_verified')},indent=2),flush=True)


if __name__ == '__main__':
    main()
