#!/usr/bin/env python3
"""Independently read the actual cada56c hosted capture and ART evidence."""
from __future__ import annotations
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image

BASE = Path('/workspace/scratch/4130730d15aa')
FOLDER = BASE / 'tooling-validation/hosted-run-38202401393'
OUT = BASE / 'tooling-validation/android-run-38202401393-analysis'
SOURCE = BASE / 'runtime-forward'


def meta(path):
    data = path.read_bytes()
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
    assert not OUT.exists()
    archive = BASE / 'tooling-validation/android-cold-launch-run-38202401393.zip'
    assert meta(archive) == {'bytes': 1022164, 'sha256': '552cfb1df46eb0fb324fde6468c9edee53611db2983ee7a60dc85179ccdf4891'}
    extraction = json.loads((FOLDER.parent / (FOLDER.name + '-extraction.json')).read_text())
    assert extraction['member_count'] == 428 and len(extraction['files']) == 428
    for entry in extraction['files']:
        path = FOLDER / entry['path']
        assert path.resolve().is_relative_to(FOLDER.resolve()) and not path.is_symlink()
        assert meta(path) == {'bytes': entry['size_bytes'], 'sha256': entry['sha256']}
    pins = {
        'android_compare.py': '0b9a50cec26d0cc97a2b8c5592aaf614a40b5dc339bccf85d85f1d753500126f',
        'android_intro.py': '5af591694ff06ae1518345fdc6510d58183f07d54cddff8899c03a9a8c85bd83',
        'android_post_intro.py': '941e4703467afedba33445575c4611c9afc0238ba79b46f43ff4f8683a6281c9',
        'tools/android/android_constructor_probe.py': 'f2ce05d3e5e50b76876b2761221c7dd796b97ce27a1207c8e5fda2ee7313afcd',
    }
    for name, digest in pins.items():
        assert meta(SOURCE / name)['sha256'] == digest
    sys.path[:0] = [str(SOURCE), str(SOURCE / 'tools/android')]
    import android_compare as cold
    import android_intro as intro
    import android_post_intro as post
    import android_constructor_probe as constructor
    runtime = json.loads((FOLDER / 'runtime-run.json').read_text())
    capture = json.loads((FOLDER / 'capture/result.json').read_text())
    probe = json.loads((FOLDER / 'constructor-probe/probe-result.json').read_text())
    assert constructor.verify_result(FOLDER / 'constructor-probe', probe, serial='emulator-5560') is True
    assert probe['status'] == 'ART_CONSTRUCTOR_ALLOCATION_VERIFIED' and probe['cleanup_complete'] is True
    assert probe['art_command']['returncode'] == 0 and probe['art_command']['timed_out'] is False
    assert (FOLDER / 'constructor-probe' / probe['art_command']['stdout']['path']).read_bytes() == b'CONSTRUCTOR_ALLOCATION_OK class=zhh arity=2\n'
    assert (FOLDER / 'constructor-probe' / probe['art_command']['stderr']['path']).read_bytes() == b''
    checked = {}
    for label, root, value in [('capture', FOLDER / 'capture', capture), ('constructor', FOLDER / 'constructor-probe', probe['commands'])]:
        entries = {}
        for entry in artifacts(value):
            cold.artifact(root, entry)
            if entry['path'] in entries:
                assert entries[entry['path']] == entry
            entries[entry['path']] = entry
        checked[label] = len(entries)
    comparisons = {}
    for name, function, filename in [('cold', cold.compare_capture, 'cold-launch-comparison.json'),
                                     ('intro', intro.compare_intro, 'intro-comparison.json'),
                                     ('post_intro', post.compare_post_intro, 'post-intro-comparison.json')]:
        actual = function(FOLDER / 'capture')
        preserved = json.loads((FOLDER / 'capture' / filename).read_text())
        assert actual == preserved, name
        comparisons[name] = actual
    report_bindings = {
        'capture_device_report_sha256': 'capture-device/capture-device.json',
        'constructor_probe_report_sha256': 'constructor-probe/probe-result.json',
        'cold_launch_comparison_report_sha256': 'capture/cold-launch-comparison.json',
        'intro_comparison_report_sha256': 'capture/intro-comparison.json',
        'post_intro_comparison_report_sha256': 'capture/post-intro-comparison.json',
    }
    for key, path in report_bindings.items():
        assert runtime[key] == meta(FOLDER / path)['sha256'], key
    # The live service updates runtime-status.json to stopped on clean shutdown.
    # The original ready JSON survives literally in the captured wait stdout.
    boot_stdout = (FOLDER / 'stages/boot-readiness.stdout.txt').read_bytes()
    boot_offset = boot_stdout.index(b'{\n  "started_utc"')
    boot_ready_bytes = boot_stdout[boot_offset:]
    assert hashlib.sha256(boot_ready_bytes).hexdigest() == runtime['boot_report_sha256']
    assert json.loads(boot_ready_bytes)['state'] == 'ready'
    assert json.loads((FOLDER / 'environment/runtime-status.json').read_text())['state'] == 'stopped'
    pairs = []
    for label, png_suffix, xml_suffix in [('cold', '', '-hierarchy'), ('intro-2', '-intro-2', '-intro-2-hierarchy'),
                                         ('intro-3', '-intro-3', '-intro-3-hierarchy'), ('intro-4', '-intro-4', '-intro-4-hierarchy'),
                                         ('post-intro', '-post-intro', '-post-intro-hierarchy')]:
        png_paths = [FOLDER / 'capture' / (variant + png_suffix + '.png') for variant in ['original', 'candidate']]
        xml_paths = [FOLDER / 'capture' / (variant + xml_suffix + '.xml') for variant in ['original', 'candidate']]
        frames = [np.asarray(Image.open(path).convert('RGBA')) for path in png_paths]
        assert frames[0].shape == frames[1].shape == (1280, 720, 4)
        difference = np.any(frames[0] != frames[1], axis=2)
        yy, xx = np.where(difference)
        pairs.append({'name': label, 'size': [720, 1280], 'changed_rgba_pixels': int(difference.sum()),
                      'bounds_exclusive': None if not len(xx) else [int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1],
                      'png_bytes_equal': png_paths[0].read_bytes() == png_paths[1].read_bytes(),
                      'xml_bytes_equal': xml_paths[0].read_bytes() == xml_paths[1].read_bytes(),
                      'pngs': [{'path': path.relative_to(FOLDER).as_posix(), **meta(path)} for path in png_paths],
                      'xmls': [{'path': path.relative_to(FOLDER).as_posix(), **meta(path)} for path in xml_paths]})
    assert [pair['changed_rgba_pixels'] for pair in pairs] == [0, 26, 0, 0, 0]
    assert comparisons['cold']['installed_apk_identities_verified'] is True
    assert comparisons['cold']['apk_sha256'] == ['84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800', '9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2']
    assert comparisons['intro']['intro_sequence_equal'] is False and comparisons['intro']['transitions_equal'] is True
    assert comparisons['post_intro']['changed_pixels'] == 0 and comparisons['post_intro']['surface_identity_equal'] is True
    assert comparisons['post_intro']['post_intro_surface_equal'] is False
    assert runtime['constructor_probe_gate_passed'] is True and runtime['requested_capture_gate_passed'] is False
    host = BASE / 'tooling-validation/hosted-tools-run-38202401393/android-tooling-host-tests.log'
    host_text = host.read_text()
    assert re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', host_text, re.M) == [('33', '0.729')]
    assert len(re.findall(r'^test.* \.\.\. ok$', host_text, re.M)) == 33
    evidence = {
        'status': 'ART_VERIFIED_COLD_EXACT_INTRO_DIFFERENCE',
        'analyzed_utc': datetime.now(timezone.utc).isoformat(),
        'run_id': 38202401393, 'commit': 'cada56c8a11ff5cbd892ec6d0beaeab60b3e644d',
        'archive': meta(archive), 'all_archive_files_verified': 428,
        'recorded_artifact_hashes_verified': checked, 'all_six_runtime_report_bindings_verified': True,
        'boot_ready_binding': {'source_path': 'stages/boot-readiness.stdout.txt', 'literal_byte_offset': boot_offset,
                              'literal_bytes': len(boot_ready_bytes), 'sha256': runtime['boot_report_sha256'],
                              'exact_literal_bytes_match_recorded_ready_hash': True,
                              'final_live_status_file_is_expected_stopped_state': True},
        'source_verifier_pins': pins, 'all_three_exact_comparator_replays_match': True,
        'constructor_probe_independent_verify_result': True,
        'constructor': {'status': probe['status'], 'probe_sha256': probe['probe_sha256'],
                        'original_apk_sha256': probe['original_apk_sha256'], 'environment': probe['environment'],
                        'art_binary_sha256': probe['art_binary_sha256'], 'device_inputs': probe['device_inputs'],
                        'art_command': probe['art_command'], 'art_argv': probe['art_argv'],
                        'cleanup_complete': True, 'compile_only_stubs_on_classpath': False,
                        'app_apk_modified': False, 'app_installed': False, 'widget_behavior_verified': False},
        'capture_original_sha256': runtime['original_sha256'], 'capture_candidate_sha256': runtime['candidate_sha256'],
        'capture_device_environment': capture['device'], 'capture_status': capture['status'],
        'full_unmasked_pairs': pairs, 'comparisons': comparisons,
        'runtime_status': runtime['status'], 'runtime_failures': runtime['failures'],
        'constructor_probe_gate_passed': True, 'cold_launch_capture_equal': True,
        'intro_sequence_equal': False, 'post_intro_surface_equal': False,
        'post_intro_raw_notification_pixels_and_xml_equal': True,
        'post_intro_gate_retains_unequal_intro_prerequisite': True,
        'requested_capture_gate_passed': False, 'full_runtime_1_to_1_established': False,
        'tooling_host_tests': {'count': 33, 'individual_ok_lines': 33, 'seconds': 0.729, 'path': 'android-tooling-host-tests.log', **meta(host)},
        'new_android_actions_performed_by_analysis': False,
    }
    OUT.mkdir()
    (OUT / 'independent-analysis.json').write_text(json.dumps(evidence, indent=2) + '\n')
    (OUT / 'boot-ready-snapshot.json').write_bytes(boot_ready_bytes)
    shutil.copyfile(Path(__file__), OUT / Path(__file__).name)
    shutil.copyfile(host, OUT / 'android-tooling-host-tests.log')
    print(json.dumps({'status': evidence['status'], 'art_verified': True, 'artifact_hashes_checked': checked,
                      'pixel_counts': [pair['changed_rgba_pixels'] for pair in pairs], 'output': str(OUT)}, indent=2))


if __name__ == '__main__':
    main()
