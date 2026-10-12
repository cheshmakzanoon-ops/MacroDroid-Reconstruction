#!/usr/bin/env python3
"""Verify the preserved pre-app radio drift without inferring app parity."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

BASE = Path(__file__).resolve().parent
REPO = BASE.parent / 'MacroDroid-Reconstruction'
HEAD = 'dbcad968c5c3e8f084205393a6c0d2d06a203c71'
PUBLISHED = REPO / 'docs/verification/editor-journey/run-38214498409-attempt-1'
RAW = BASE / 'editor-run-38214498409-extracted'
OUT = BASE / 'editor-run-38214498409-analysis'
ARCHIVE = {'bytes': 659380, 'sha256': '888eec110a622313bfc1a0fa4eb183b14d6b7302f38d4b0bf5c063a8844d37a9'}


def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def put_json(name, data):
    target = OUT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x') as stream:
        stream.write(json.dumps(data, indent=2) + '\n')


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((PUBLISHED / 'manifest.json').read_text())
    assert (manifest['run_id'], manifest['head_sha'], manifest['artifact_id']) == (38214498409, HEAD, 11731511399)
    assert manifest['conclusion'] == 'failure'
    assert manifest['artifact_bytes'] == ARCHIVE['bytes'] and manifest['artifact_digest'] == 'sha256:' + ARCHIVE['sha256']
    archive = PUBLISHED / 'evidence.zip'
    assert meta(archive.read_bytes()) == ARCHIVE
    rows = {row['path']: row for row in manifest['members']}
    assert len(rows) == len(manifest['members']) == 149
    receipt = json.loads((BASE / 'editor-run-38214498409-extracted-extraction.json').read_text())
    assert {row['path']: row for row in receipt['files']} == rows and receipt['key_scan_findings'] == []
    with zipfile.ZipFile(archive) as zipped:
        assert len(zipped.namelist()) == len(rows) and set(zipped.namelist()) == set(rows)
        for name, row in rows.items():
            actual = zipped.read(name)
            path = RAW / name
            assert path.resolve().is_relative_to(RAW.resolve()) and not path.is_symlink()
            assert path.read_bytes() == actual and meta(actual) == {k: row[k] for k in ('bytes', 'sha256')}
    assert not any(name.startswith('ci-editor/journey/') for name in rows)
    pins = []
    for relative in ('tools/android/configure_capture_device.py', '.github/workflows/editor-journey.yml'):
        git = subprocess.run(['git', 'show', HEAD + ':' + relative], cwd=REPO,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        assert git.returncode == 0, git.stderr.decode()
        target = OUT / 'reviewed-source' / Path(relative).name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(git.stdout)
        pins.append({'commit': HEAD, 'path': relative, **meta(git.stdout)})
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('radio_source_for_read_only_parse', OUT / 'reviewed-source/configure_capture_device.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    config_folder = RAW / 'ci-editor/device'
    config = json.loads((config_folder / 'capture-device.json').read_text())
    assert config['status'] == 'CAPTURE_DEVICE_CONFIGURATION_FAILED'
    assert config['failure'] == 'Primary radio type or computed level changed at configuration completion'
    assert len(config['commands']) == 41
    commands = {}
    output_refs = {}
    for command in config['commands']:
        label = command['label']
        commands.setdefault(label, []).append(command)
        assert command['exit_code'] == 0 and 0 <= command['seconds'] <= 15
        for stream in ('stdout', 'stderr'):
            row = command[stream]
            assert row['path'] not in output_refs
            assert meta((config_folder / row['path']).read_bytes()) == {k: row[k] for k in ('bytes', 'sha256')}
            output_refs[row['path']] = row
    def read(label):
        assert len(commands[label]) == 1
        return (config_folder / commands[label][0]['stdout']['path']).read_text()
    last_telephony = commands['telephony'][-1]
    confirmed = helper.primary_signals((config_folder / last_telephony['stdout']['path']).read_text())
    after = helper.primary_signals(read('after-telephony'))
    assert len(confirmed) == len(after) == 1
    assert confirmed[0] == config['confirmed_primary_signal']
    assert after == config['after']['primary_signals']
    assert (confirmed[0]['primary'], confirmed[0]['level']) == ('CellSignalStrengthLte', 4)
    assert (after[0]['primary'], after[0]['level']) == ('CellSignalStrengthWcdma', 4)
    assert config['signal_stable_seconds'] == 15.178
    assert config['signal_stability_fields'] == ['primary', 'level']
    assert config['after']['animation_scales'] == {key: '0' for key in helper.ANIMATION_SCALE_KEYS}
    assert config['requested_animation_scales_observed'] is False
    service = (RAW / 'ci-editor/service.log').read_text()
    queue_results = [json.loads(line) for line in service.splitlines() if line.startswith('{') and '"job"' in line]
    assert queue_results == [{'job': 'eaa1a981d8bc44a18fdf5661c1c3fd40', 'exit_code': 2}]
    host_results = {}
    for name, expected in [('host-tests.log', 148), ('download-tests.log', 6)]:
        path = RAW / 'ci-editor' / name
        text = path.read_text()
        headers = re.findall(r'^test_\S+ \([^\n]+\)', text, re.M)
        summaries = re.findall(r'^Ran (\d+) tests in ([0-9.]+)s$', text, re.M)
        assert len(headers) == len(set(headers)) == expected
        assert len(summaries) == 1 and int(summaries[0][0]) == expected
        assert re.search(r'^OK\s*$', text, re.M) and not re.search(r'^(FAILED|FAIL:|ERROR:)', text, re.M)
        host_results[name] = {**meta(path.read_bytes()), 'count': expected, 'seconds': float(summaries[0][1])}
    for name, row in rows.items():
        assert meta((RAW / name).read_bytes()) == {k: row[k] for k in ('bytes', 'sha256')}
    # Review copies preserve complete recorded device logs and command output bytes.
    for path in sorted((RAW / 'ci-editor').rglob('*')):
        if path.is_file():
            target = OUT / 'raw' / path.relative_to(RAW / 'ci-editor')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
            assert target.read_bytes() == path.read_bytes()
    analysis = {'schema': 1, 'status': 'PRE_APP_DEVICE_CONFIGURATION_REJECTED_RADIO_TYPE_DRIFT',
                'analyzed_utc': datetime.now(timezone.utc).isoformat(), 'run_id': 38214498409,
                'head_sha': HEAD, 'artifact_id': 11731511399, 'archive': ARCHIVE,
                'archive_repository_path': 'docs/verification/editor-journey/run-38214498409-attempt-1/evidence.zip',
                'all_149_archive_members_verified_before_and_after': True,
                'all_41_commands_succeeded': True, 'command_output_hashes_verified': len(output_refs),
                'configuration_report': meta((config_folder / 'capture-device.json').read_bytes()),
                'failure': config['failure'], 'actual_status': config['status'],
                'stable_observation_seconds': config['signal_stable_seconds'],
                'confirmed_primary_signal': confirmed[0], 'completion_primary_signal': after[0],
                'raw_registry_reparsed_with_exact_git_source': True,
                'raw_before_and_after': {key: config[key] for key in ('before', 'after')},
                'requested_animation_scales_observed_flag_retained': False,
                'queue_results': queue_results, 'journey_artifacts_present': False,
                'host_results': host_results, 'source_pins': pins,
                'app_pixel_or_behavior_conclusion': None, 'new_android_actions': [],
                'helper_main_invoked': False, 'raw_bytes_or_active_source_modified': False,
                'full_runtime_1_to_1_established': False}
    put_json('independent-editor-analysis.json', analysis)
    put_json('all-149-member-identities.json', list(rows.values()))
    put_json('source-pins.json', pins)
    shutil.copyfile(Path(__file__), OUT / Path(__file__).name)
    assert meta(archive.read_bytes()) == ARCHIVE
    print(json.dumps({'status': analysis['status'], 'before_primary': confirmed[0]['primary'],
                      'after_primary': after[0]['primary'], 'level': 4,
                      'verified_command_outputs': len(output_refs), 'journey_recorded': False,
                      'output': str(OUT)}, indent=2))


if __name__ == '__main__':
    main()
