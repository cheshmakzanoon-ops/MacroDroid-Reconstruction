#!/usr/bin/env python3
"""Measure and freeze the separate zero-scale device preparer and host evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import time


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reports', type=Path, required=True)
    parser.add_argument('--checkpoint', type=Path, required=True)
    args = parser.parse_args()
    home = Path(__file__).resolve().parent
    source = home / 'inputs'
    reports, checkpoint = args.reports.resolve(), args.checkpoint.resolve()
    reports.mkdir(parents=True, exist_ok=False)
    before = {path.name: identity(path) for path in sorted(source.iterdir()) if path.is_file()}
    save(reports / 'inputs-before.json', before)
    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', str(source),
               '-p', 'test_enable_still_animations.py', '-v']
    started = time.monotonic()
    result = {'status': 'ZERO_SCALE_HOST_CONTROLS_RUNNING', 'android_executed': False,
              'argv': command, 'started_utc': datetime.now(timezone.utc).isoformat()}
    with (reports / 'stdout.txt').open('wb') as out, (reports / 'stderr.txt').open('wb') as err:
        try:
            child = subprocess.run(command, cwd=home,
                env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1',
                     'ANIMATION_CONTROL_EVIDENCE': str(reports / 'simulated-adb-cases')},
                stdout=out, stderr=err, timeout=60)
            code, timed_out = child.returncode, False
        except subprocess.TimeoutExpired:
            code, timed_out = 124, True
    after = {path.name: identity(path) for path in sorted(source.iterdir()) if path.is_file()}
    save(reports / 'inputs-after.json', after)
    log = (reports / 'stderr.txt').read_text()
    passed = code == 0 and not timed_out and before == after and '\nRan 10 tests in ' in log and log.endswith('\nOK\n')
    result.update(status='ZERO_SCALE_HOST_CONTROLS_PASSED' if passed else 'ZERO_SCALE_HOST_CONTROLS_FAILED',
                  passed=passed, returncode=code, timed_out=timed_out, source_unchanged=before == after,
                  seconds=round(time.monotonic() - started, 6),
                  finished_utc=datetime.now(timezone.utc).isoformat(),
                  stdout=identity(reports / 'stdout.txt'), stderr=identity(reports / 'stderr.txt'))
    save(reports / 'result.json', result)
    if not passed:
        print(json.dumps(result, indent=2))
        return 2

    checkpoint.mkdir(parents=True, exist_ok=False)
    for name, expected in before.items():
        if identity(source / name) != expected:
            raise ValueError('Measured input changed before freezing: ' + name)
        shutil.copyfile(source / name, checkpoint / name)
        if identity(checkpoint / name) != expected:
            raise ValueError('Frozen input differs: ' + name)
    regular, links = [], []
    for path in sorted(reports.rglob('*')):
        name = path.relative_to(reports).as_posix()
        if path.is_symlink():
            links.append({'path': name, 'target': str(path.readlink()), 'restored_as_symlink': False,
                          'target_file': identity(path) if path.is_file() else None})
        elif path.is_file():
            regular.append({'path': name, **identity(path)})
    archive = checkpoint / 'host-evidence.tar.gz'
    with tarfile.open(archive, 'w:gz') as bundle:
        for row in regular:
            path = reports / row['path']
            if identity(path) != {key: row[key] for key in ('bytes', 'sha256')}:
                raise ValueError('Host evidence changed before archiving')
            bundle.add(path, arcname=row['path'], recursive=False)
    with tarfile.open(archive, 'r:gz') as bundle:
        members = bundle.getmembers()
        if [member.name for member in members] != [row['path'] for row in regular]:
            raise ValueError('Archive member inventory changed')
        for member, row in zip(members, regular):
            raw = bundle.extractfile(member).read()
            if not member.isfile() or len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
                raise ValueError('Archive member changed: ' + row['path'])
    for row in regular:
        if identity(reports / row['path']) != {key: row[key] for key in ('bytes', 'sha256')}:
            raise ValueError('Host evidence changed during archiving')
    for name, expected in before.items():
        if identity(source / name) != expected:
            raise ValueError('Measured input changed during freezing: ' + name)
    save(checkpoint / 'host-evidence-manifest.json', {
        'android_executed': False, 'regular_files': regular,
        'symbolic_links_as_inert_metadata': links, 'all_archived_members_verified': True})
    save(checkpoint / 'policy.json', {
        'status': 'INACTIVE_ZERO_SCALE_PREPARATION_HOST_CONTROLS_PASSED',
        'android_executed': False, 'host_tests': 10, 'configuration_commands': 19,
        'requested_scales': {'animator_duration_scale': '0', 'window_animation_scale': '0',
                             'transition_animation_scale': '0'},
        'parent_checkpoint_sha256': '42a37e351e0a5ef782f12de9b8140f84eebea4363ec39d4a833fc78122acdcad',
        'normal_animation_run': 38212813248,
        'normal_animation_outcome': 'Both APKs stopped at intro-2 without accepted stable frames; this failure remains recorded separately.',
        'candidate_apk_sha256': '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182',
        'intended_plan_sha256': '940be18b226ab29de46ea48a1496238b8a2221a52077466693a34a2113bc24cc',
        'comparison_rules_changed': False, 'apk_modified': False,
        'animation_timing_parity_established': False, 'full_runtime_1_to_1_established': False})
    (checkpoint / 'README.md').write_text('''# Explicit zero-scale preparation for the twelve-screen journey

This separate preparer sets all three Android animation scales to zero on the
exact disposable API35 emulator. It preserves the reviewed normal preparer's
nineteen-command identity, ordering, raw-output and deadline checks. The source
and test patches against the immutable normal preparer are included.

Ten host tests pass using simulated ADB. They cover wrong device identity,
incorrect readbacks, changed and aliased raw outputs, stale or reordered
commands, malformed console output and an independent literal specification
of all nineteen commands. The archive preserves every regular host-evidence
file; deliberate symlinks are stored as inert metadata only.

Normal-animation run 38212813248 stopped at intro-2 for both APKs without
accepting stable frames. Its failure and prior scale-zero pixel differences
remain separate records. This package supports a new declared scale-zero
observation of the combined 5f635e APK through the Date/Time category.
Full PNG/XML equality, capture chronology, process checks and APK identity
remain unchanged. Animation timing and motion are outside this still-frame
measurement. No Android execution or whole-application parity is claimed here.
''')
    shutil.copyfile(Path(__file__), checkpoint / 'measure_and_freeze.py')
    files = [{'path': path.relative_to(checkpoint).as_posix(), **identity(path)}
             for path in sorted(checkpoint.rglob('*')) if path.is_file()]
    save(checkpoint / 'checkpoint.json', {
        'status': 'INACTIVE_ZERO_SCALE_PREPARATION_HOST_CONTROLS_PASSED',
        'created_utc': datetime.now(timezone.utc).isoformat(), 'android_executed': False,
        'active_changes': False, 'files': files})
    print(json.dumps({'checkpoint': str(checkpoint / 'checkpoint.json'),
                      **identity(checkpoint / 'checkpoint.json'), 'files': len(files),
                      'host_tests': 10, 'archived_regular_files': len(regular),
                      'inert_symlink_controls': len(links)}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
