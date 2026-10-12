#!/usr/bin/env python3
"""Replay the exact dbcad session while retaining the separate failed startup."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

import numpy as np
from PIL import Image

BASE = Path('/workspace/scratch/4130730d15aa')
REPO = BASE / 'MacroDroid-Reconstruction'
SOURCE_COMMIT = 'dbcad968c5c3e8f084205393a6c0d2d06a203c71'
ROOT = BASE / 'ci-run-analysis'
RAW = ROOT / 'session-run-38214498414-extracted'
PUBLISHED = REPO / 'docs/verification/editor-journey/run-38214498414-attempt-1'
OUT = ROOT / 'session-run-38214498414-analysis-02'
ORIGINAL = '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'
CANDIDATE = '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'
ARCHIVE = {'bytes': 11628251, 'sha256': 'b671aa04ef05ed5bf064bd16dd92b7046819da69578ec362b7d3ea86bfb17ff5'}


def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def read_json(path):
    return json.loads(path.read_text())


def put_json(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def git_bytes(relative):
    result = subprocess.run(['git', 'show', SOURCE_COMMIT + ':' + relative], cwd=REPO,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    assert result.returncode == 0, (relative, result.stderr.decode())
    return result.stdout


def artifacts(value):
    if isinstance(value, dict):
        if set(value) == {'path', 'bytes', 'sha256'}:
            yield value
        for child in value.values():
            yield from artifacts(child)
    elif isinstance(value, list):
        for child in value:
            yield from artifacts(child)


def tests(path, count):
    text = path.read_text()
    rows = re.findall(r'^test_\S+ \([^\n]+\)', text, re.M)
    summary = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', text, re.M)
    assert len(rows) == len(set(rows)) == count
    assert len(summary) == 1 and int(summary[0][0]) == count
    assert re.search(r'^OK\s*$', text, re.M) and not re.search(r'^(FAILED|ERROR:|FAIL:)', text, re.M)
    return {**meta(path.read_bytes()), 'count': count, 'seconds': float(summary[0][1]),
            'distinct_headers': len(set(rows))}


def main():
    started = datetime.now(timezone.utc).isoformat()
    OUT.mkdir(parents=True, exist_ok=False)
    archive = PUBLISHED / 'evidence.zip'
    assert meta(archive.read_bytes()) == ARCHIVE
    manifest = read_json(PUBLISHED / 'manifest.json')
    assert (manifest['run_id'], manifest['run_attempt'], manifest['head_sha'], manifest['artifact_id']) == (
        38214498414, 1, SOURCE_COMMIT, 11731381967)
    assert manifest['artifact_bytes'] == ARCHIVE['bytes'] and manifest['artifact_digest'] == 'sha256:' + ARCHIVE['sha256']
    entries = {row['path']: row for row in manifest['members']}
    assert len(entries) == len(manifest['members']) == 2096
    receipt = read_json(ROOT / 'session-run-38214498414-extracted-extraction.json')
    assert receipt['archive'] == ARCHIVE and receipt['key_scan_findings'] == []
    assert {row['path']: row for row in receipt['files']} == entries
    with zipfile.ZipFile(archive) as zipped:
        assert set(zipped.namelist()) == set(entries) and len(zipped.namelist()) == len(entries)
        for name, record in entries.items():
            data = zipped.read(name)
            assert meta(data) == {key: record[key] for key in ('bytes', 'sha256')}
            path = RAW / name
            assert path.resolve().is_relative_to(RAW.resolve()) and not path.is_symlink()
            assert path.read_bytes() == data
    source_pins, retained_generated_bytecode = [], []
    source_dir = OUT / 'replay-source'
    source_dir.mkdir()
    for path in sorted((RAW / 'tools/parity_journeys').rglob('*')):
        if path.is_file():
            relative = path.relative_to(RAW).as_posix()
            if '__pycache__' in path.parts:
                assert path.suffix == '.pyc'
                retained_generated_bytecode.append({'path': relative, **meta(path.read_bytes()),
                                                    'retained_unchanged': True, 'executed': False})
                continue
            data = git_bytes(relative)
            assert path.read_bytes() == data
            source_pins.append({'path': relative, **meta(data), 'matches_exact_source_commit': True})
            destination = source_dir / path.relative_to(RAW / 'tools/parity_journeys')
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
    proof_path = 'project/android_compare.py'
    proof_bytes = git_bytes(proof_path)
    assert meta(proof_bytes)['sha256'] == '0b9a50cec26d0cc97a2b8c5592aaf614a40b5dc339bccf85d85f1d753500126f'
    (source_dir / 'android_compare.py').write_bytes(proof_bytes)
    workflow_path = '.github/workflows/editor-session.yml'
    (source_dir / 'editor-session.yml').write_bytes(git_bytes(workflow_path))
    source_pins += [{'path': p, **meta(git_bytes(p)), 'matches_exact_source_commit': True}
                    for p in (proof_path, workflow_path)]
    print(json.dumps({'checkpoint': 'ALL_2096_RAW_AND_CAPTURED_SOURCE_BYTES_VERIFIED',
                      'source_files': len(source_pins)}), flush=True)
    sys.dont_write_bytecode = True
    sys.path[:0] = [str(source_dir)]
    import android_compare as proof
    import editor_journey as runner
    import post_onboarding as session
    from supplied_reference_journey import load_plan
    assert meta(Path(session.__file__).read_bytes())['sha256'] == '6e155f43a2a7f7cdd2364911191f2b88b0085db915da2adefb8b2f918a1dbd80'
    folder = RAW / 'ci-editor/journey'
    document = (folder / 'journey.json').read_bytes()
    report = json.loads(document)
    plan = load_plan()
    assert report['plan'] == plan and runner.fingerprint(plan) == report['plan_sha256']
    assert len(plan) == 16 and [r['apk_sha256'] for r in report['runs']] == [ORIGINAL, CANDIDATE]
    reference_artifacts = {}
    for row in artifacts(report):
        proof.artifact(folder, row)
        previous = reference_artifacts.setdefault(row['path'], row)
        assert previous == row
    for name in ('journey.json', 'comparison.json', 'editor-session-comparison.json', 'editor-session-replay.json'):
        assert (folder / name).read_bytes() == (PUBLISHED / name).read_bytes()
    result = session.compare_session(folder, report, plan, proof)
    assert result == read_json(folder / 'editor-session-comparison.json')
    replay = {**result, 'journey_document_sha256': meta(document)['sha256']}
    assert replay == read_json(folder / 'editor-session-replay.json')
    assert result['schema'] == 4 and result['status'] == 'EXACT_POST_ONBOARDING_EDITOR_MATCH_ONLY'
    assert result['editor_session_equal'] is True and result['full_runtime_1_to_1_established'] is False
    put_json('literal-session-replay.json', replay)
    previous_plan = runner.PLAN
    try:
        runner.PLAN = plan
        continuous = runner.compare(folder, report, proof)
    finally:
        runner.PLAN = previous_plan
    assert continuous == read_json(folder / 'comparison.json')
    assert continuous['status'] == 'REJECTED'
    assert continuous['reason'] == 'App PID changed or lacks two live samples'
    put_json('literal-continuous-startup-replay.json', continuous)
    print(json.dumps({'checkpoint': 'EXACT_SCHEMA4_AND_FAILED_STARTUP_REPLAYED',
                      'session': result['status'], 'startup': continuous['status']}), flush=True)
    captures = OUT / 'review-captures'
    captures.mkdir()
    pairs = []
    for left, right in zip(report['runs'][0]['screens'], report['runs'][1]['screens']):
        assert left['name'] == right['name']
        images = []
        for shot in (left, right):
            for row in shot['artifacts'].values():
                data = proof.artifact(folder, row)
                path = captures / row['path']
                assert not path.exists()
                path.write_bytes(data)
            images.append(np.asarray(Image.open(folder / shot['artifacts']['screenshot']['path']).convert('RGBA')))
        assert images[0].shape == images[1].shape == (1280, 720, 4)
        yy, xx = np.where(np.any(images[0] != images[1], axis=2))
        hierarchy = [proof.artifact(folder, shot['artifacts']['hierarchy']) for shot in (left, right)]
        state = [proof.xml_state(data, owner_package=shot['owner'])[0] for data, shot in zip(hierarchy, (left, right))]
        components = [session.component(proof.artifact(folder, shot['artifacts']['foreground']), proof) for shot in (left, right)]
        pairs.append({'name': left['name'], 'size': [720, 1280], 'changed_rgba_pixels': len(xx),
                      'bounds_exclusive': [int(xx.min()), int(yy.min()), int(xx.max()+1), int(yy.max()+1)] if len(xx) else None,
                      'full_png_bytes_equal': left['artifacts']['screenshot']['sha256'] == right['artifacts']['screenshot']['sha256'],
                      'full_xml_bytes_equal': hierarchy[0] == hierarchy[1], 'full_xml_state_equal': state[0] == state[1],
                      'foreground_components': components, 'foreground_component_equal': components[0] == components[1],
                      'original': left['artifacts'], 'candidate': right['artifacts'],
                      'original_observation': left['session_observation'], 'candidate_observation': right['session_observation']})
    assert len(pairs) == 16 and all(p['changed_rgba_pixels'] == 0 and p['full_xml_state_equal']
                                  and p['foreground_component_equal'] for p in pairs[6:])
    lifecycle = (RAW / 'ci-editor/lifecycle.log').read_bytes()
    text = lifecycle.decode()
    lines = text.splitlines(keepends=True)
    crashes = []
    process_summary = []
    for run in report['runs']:
        label = run['label']
        pids = [{ 'screen': shot['name'],
                  'first': proof.artifact(folder, shot['artifacts']['pid_first']).decode().strip(),
                  'final': proof.artifact(folder, shot['artifacts']['pid_final']).decode().strip() }
                 for shot in run['screens']]
        first_pid = pids[0]['first']
        home_pid = pids[6]['first']
        assert first_pid != home_pid
        assert all(p['first'] == p['final'] for p in pids)
        assert all(p['first'] == home_pid for p in pids[6:])
        hit = [i for i, line in enumerate(lines) if re.search(r'\s' + re.escape(first_pid) + r'\s+' + re.escape(first_pid)
               + r' E AndroidRuntime: FATAL EXCEPTION: main', line)]
        assert len(hit) == 1
        start = hit[0]
        block = []
        for line in lines[start:]:
            if ' E AndroidRuntime: ' not in line:
                break
            block.append(line)
        raw_block = ''.join(block).encode()
        assert b'java.lang.IllegalStateException: Fragment LB{' in raw_block
        assert b'not attached to Activity' in raw_block
        assert b'at android.app.Fragment.getResources(Fragment.java:785)' in raw_block
        assert b'at com.zx.lbua80.onShow(Unknown Source:22)' in raw_block
        (OUT / (label + '-actual-java-crash.txt')).write_bytes(raw_block)
        events = [line for line in lines if (('am_proc_start:' in line or 'am_proc_died:' in line)
                  and 'com.arlosoft.macrodroid,' in line
                  and any(',' + pid + ',' in line for pid in (first_pid, home_pid)))]
        assert any('am_proc_died:' in line and ',' + first_pid + ',' in line for line in events)
        assert any('am_proc_start:' in line and ',' + home_pid + ',' in line for line in events)
        (OUT / (label + '-actual-process-events.txt')).write_text(''.join(events))
        crashes.append({'label': label, 'pid': first_pid, 'first_log_line': start + 1,
                        'raw_crash_excerpt': meta(raw_block), 'exception_class': 'java.lang.IllegalStateException',
                        'actual_exception_line': next(line.rstrip('\n') for line in block if 'java.lang.IllegalStateException:' in line),
                        'raw_object_identity_preserved': True, 'scope': 'Before the observed home session boundary'})
        process_summary.append({'label': label, 'intro_pid': first_pid, 'post_crash_home_pid': home_pid,
                                'all_scoped_captures_keep_home_pid': True, 'per_screen': pids})
    config_path = RAW / 'ci-editor/device/capture-device.json'
    config = read_json(config_path)
    assert config['status'] == 'CAPTURE_DEVICE_CONFIGURATION_VERIFIED'
    config_refs = {}
    for row in artifacts(config):
        assert meta((config_path.parent / row['path']).read_bytes()) == {k: row[k] for k in ('bytes','sha256')}
        config_refs[row['path']] = row
    # Re-read every extracted byte after all literal replay and diagnostic reads.
    for name, row in entries.items():
        assert meta((RAW / name).read_bytes()) == {k: row[k] for k in ('bytes', 'sha256')}
    assert meta(archive.read_bytes()) == ARCHIVE
    host = tests(RAW / 'ci-editor/host-tests.log', 148)
    download = tests(RAW / 'ci-editor/download-tests.log', 6)
    put_json('source-commit-pins.json', {'commit': SOURCE_COMMIT, 'files': source_pins})
    put_json('retained-unexecuted-generated-bytecode.json', retained_generated_bytecode)
    put_json('all-2096-member-identities.json', list(entries.values()))
    put_json('all-journey-artifact-references.json', list(reference_artifacts.values()))
    analysis = {'schema': 1, 'status': 'INDEPENDENT_SCHEMA4_POST_ONBOARDING_MATCH_STARTUP_REMAINS_REJECTED',
                'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
                'run_id': 38214498414, 'head_sha': SOURCE_COMMIT,
                'archive': ARCHIVE, 'archive_repository_path': 'docs/verification/editor-journey/run-38214498414-attempt-1/evidence.zip',
                'artifact_id': 11731381967, 'all_archive_members_checked_before_and_after': 2096,
                'source_commit_files_verified': len(source_pins), 'journey_document': meta(document),
                'raw_generated_bytecode_files_retained_and_not_executed': len(retained_generated_bytecode),
                'all_unique_referenced_journey_artifacts_verified': len(reference_artifacts),
                'session_verifier_source_sha256': meta(Path(session.__file__).read_bytes())['sha256'],
                'exact_hosted_session_comparison_and_replay_reproduced': True,
                'scoped_session_result': result, 'continuous_startup_result': continuous,
                'startup_exit_status': read_json(RAW / 'ci-editor/startup-status.json'),
                'complete_unmasked_image_pairs': pairs, 'startup_java_crashes': crashes,
                'raw_lifecycle_log': meta(lifecycle), 'recorded_process_changes': process_summary,
                'capture_device_report': meta(config_path.read_bytes()),
                'capture_device_status': config['status'], 'capture_device_artifact_hashes_verified': len(config_refs),
                'host_tests': host, 'download_tests': download,
                'archive_replay_uses_new_local_inodes': True,
                'original_hosted_ledger_result_matches_literal_replay': True,
                'raw_source_or_report_bytes_modified': False, 'new_android_actions': [],
                'screens_or_xml_masked_normalized_or_selected_for_cross_app_similarity': False,
                'startup_parity_established': False, 'crash_free_established': False,
                'animation_parity_established': False, 'macros_saved_or_executed': False,
                'full_runtime_1_to_1_established': False}
    put_json('independent-session-analysis.json', analysis)
    shutil.copy2(Path(__file__), OUT / Path(__file__).name)
    for name in ('host-tests.log', 'download-tests.log', 'startup-status.json', 'lifecycle.log'):
        shutil.copy2(RAW / 'ci-editor' / name, OUT / name)
    print(json.dumps({'status': analysis['status'], 'pixel_counts_all_16': [p['changed_rgba_pixels'] for p in pairs],
                      'unique_semantic_observations': result['evidence_identity_check'],
                      'crashes': [{k: c[k] for k in ('label','pid','exception_class')} for c in crashes],
                      'output': str(OUT)}, indent=2), flush=True)


if __name__ == '__main__':
    main()
