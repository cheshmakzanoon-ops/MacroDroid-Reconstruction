#!/usr/bin/env python3
"""Freeze the small authored hosted package without touching application inputs."""
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import stat
import sys

ROOT = Path('/dev/shm/day-numeric-hosted-01')
REPO = Path('/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction')


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def encoded(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def main():
    output = ROOT / 'checkpoints/01-hosted-wip-acceptance'
    if output.exists():
        raise ValueError('Closed capsule may not be overwritten')
    before = ROOT / 'reports/command-binding-draft/source'
    diffs = []
    for path in sorted((ROOT / 'source').rglob('*')):
        if path.is_file():
            name = path.relative_to(ROOT / 'source').as_posix()
            old = before / name
            if old.exists() and old.read_bytes() != path.read_bytes():
                diffs.extend(difflib.unified_diff(old.read_text().splitlines(keepends=True), path.read_text().splitlines(keepends=True),
                                                  fromfile='retained-draft/' + name, tofile='corrected/' + name))
    (ROOT / 'reports/command-binding-correction.patch').write_text(''.join(diffs))
    tests = json.loads((ROOT / 'reports/validation-02/result.json').read_text())
    offline = json.loads((ROOT / 'reports/workflow-validation-01/result.json').read_text())
    real = json.loads((ROOT / 'reports/real-command-compatibility-01/result.json').read_text())
    if not (tests['passed'] is True and tests['individual_successes'] == 67
            and offline['passed'] is True and offline['completed_commands'] == 12 and real['passed'] is True):
        raise ValueError('Closed local tooling gates did not pass')
    proposed = offline['active_proposals']
    if len(proposed) != 9:
        raise ValueError('Unexpected active proposal inventory')
    for row in proposed:
        if (REPO / row['path']).exists() or (REPO / row['path']).is_symlink():
            raise ValueError('Concurrent authored path is present')
        if identity(ROOT / 'source' / row['path']) != row['candidate']:
            raise ValueError('Final source differs from the closed workflow check')
    selected = [ROOT / 'README.md', ROOT / 'freeze_capsule.py']
    for name in ('source', 'reports'):
        selected.extend(path for path in (ROOT / name).rglob('*') if path.is_file())
    for path in selected:
        if path.is_symlink() or not stat.S_ISREG(path.stat().st_mode):
            raise ValueError('Unexpected alias or special authored file')
    current_bytes = sum(path.stat().st_size for path in ROOT.rglob('*') if path.is_file())
    selected_bytes = sum(path.stat().st_size for path in selected)
    if current_bytes + selected_bytes + 2 * 1024 * 1024 > 64 * 1024 * 1024:
        raise ValueError('Owned local output budget would be exceeded')
    output.mkdir(parents=True)
    files = []
    for path in sorted(selected):
        name = path.relative_to(ROOT).as_posix()
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        target.chmod(0o644)
        value = identity(path)
        if identity(target) != value:
            raise ValueError('Frozen copy differs')
        files.append({'path': name, **value, 'mode': '100644'})
    checkpoint = {'schema': 1, 'status': 'FROZEN_HOSTED_WIP_PACKAGE_LOCAL_TOOLING_VERIFIED',
                  'created_utc': datetime.now(timezone.utc).isoformat(),
                  'publication_path': 'work-in-progress/day-trigger-numeric/07-hosted-acceptance',
                  'scope': 'Nine additive tooling/workflow paths; immutable nineteen-source overlay is evaluated only in a future hosted workspace',
                  'active_application_modified': False, 'full_host_acceptance_executed': False,
                  'signed_numeric_primary_packaging_verified': False, 'android_executed': False,
                  'full_runtime_1_to_1_established': False,
                  'baseline_commit': 'dbcad968c5c3e8f084205393a6c0d2d06a203c71',
                  'source_overlay_commit': '394234b0e74c9f1d660836c8f2a89901fe05ff9d',
                  'source_overlay_checkpoint_sha256': 'c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f',
                  'future_snapshot': offline['exact_real_input_contract']['future'],
                  'future_manifest': offline['exact_real_input_contract']['future_manifest'],
                  'independent_failed_draft_review': {
                      'commit': '01a36663c9455a1192fedd3d1cade2c090561e59',
                      'path': 'docs/verification/day-numeric-hosted-review/01-command-argv-counterexamples/checkpoint.json',
                      'bytes': 13029, 'sha256': '17528d34bb9475e7bd0e666500ff5111847aaf2e547c8c31677cd2d514f2f0d3'},
                  'local_verification': {'host_controls': 67, 'offline_commands': 12,
                                         'read_only_prior_d8_templates': 9, 'read_only_prior_harness_templates': 6,
                                         'read_only_prior_streams': 30,
                                         'host_test_result': identity(ROOT / 'reports/validation-02/result.json'),
                                         'offline_result': identity(ROOT / 'reports/workflow-validation-01/result.json'),
                                         'prior_command_result': identity(ROOT / 'reports/real-command-compatibility-01/result.json')},
                  'active_files': [{'path': row['path'], 'source': 'source/' + row['path'], 'baseline': None,
                                    'must_be_absent': True, 'candidate': row['candidate'], 'mode': '100644'} for row in proposed],
                  'runtime_manifest': identity(ROOT / 'source/tools/day_numeric_acceptance/runtime-files.json'),
                  'workflow': identity(ROOT / 'source/.github/workflows/day-numeric-wip-acceptance.yml'),
                  'files': files, 'file_count': len(files), 'payload_bytes': selected_bytes,
                  'owned_tmpfs_budget_bytes': 64 * 1024 * 1024}
    with (output / 'checkpoint.json').open('xb') as stream:
        stream.write(encoded(checkpoint))
    if any(identity(output / row['path']) != {key: row[key] for key in ('bytes', 'sha256')} for row in files):
        raise ValueError('Closed capsule inventory verification failed')
    receipt = {'checkpoint_path': str(output / 'checkpoint.json'), **identity(output / 'checkpoint.json'),
               'file_count': len(files), 'payload_bytes': selected_bytes, 'active_paths': proposed,
               'workflow': checkpoint['workflow'], 'runtime_manifest': checkpoint['runtime_manifest']}
    with (ROOT / 'freeze-receipt.json').open('xb') as stream:
        stream.write(encoded(receipt))
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
