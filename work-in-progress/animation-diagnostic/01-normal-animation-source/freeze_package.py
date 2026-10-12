#!/usr/bin/env python3
"""Freeze exact normal-animation preparation source and bounded host evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import tarfile


def identity(path):
    return {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reports', type=Path, required=True)
    parser.add_argument('--checkpoint', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    args.reports, args.checkpoint = args.reports.resolve(), args.checkpoint.resolve()
    args.checkpoint.mkdir(parents=True, exist_ok=False)
    measured = json.loads((args.reports / 'result.json').read_text())
    before = json.loads((args.reports / 'inputs-before.json').read_text())
    if measured['returncode'] != 0 or not measured['source_unchanged'] or measured['android_executed']:
        raise RuntimeError('A successful bounded host-only preparation is required')
    for name, expected in before.items():
        if identity(root / 'inputs' / name)['sha256'] != expected:
            raise RuntimeError('Tested preparation input changed: ' + name)
        shutil.copy2(root / 'inputs' / name, args.checkpoint / name)
    regular, links = [], []
    for path in sorted(args.reports.rglob('*')):
        relative = path.relative_to(args.reports).as_posix()
        if path.is_symlink():
            # Preserve the exact adversarial link identity as inert metadata;
            # do not install a test-created symlink through an evidence archive.
            links.append({'path': relative, 'target': str(path.readlink()), 'kind': 'symbolic_link',
                          'target_file': identity(path) if path.is_file() else None})
        elif path.is_file():
            regular.append({'path': relative, **identity(path)})
    manifest = {'regular_files': regular, 'symbolic_links_as_inert_metadata': links}
    (args.checkpoint / 'host-evidence-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    archive = args.checkpoint / 'host-evidence.tar.gz'
    with tarfile.open(archive, 'w:gz') as bundle:
        for item in regular:
            path = args.reports / item['path']
            if identity(path) != {k: item[k] for k in ('bytes', 'sha256')}:
                raise RuntimeError('Closed host evidence changed during packaging')
            bundle.add(path, arcname=item['path'], recursive=False)
    with tarfile.open(archive) as bundle:
        if bundle.getnames() != [item['path'] for item in regular]:
            raise RuntimeError('Host archive member list changed')
        for member, expected in zip(bundle, regular):
            data = bundle.extractfile(member).read()
            if len(data) != expected['bytes'] or hashlib.sha256(data).hexdigest() != expected['sha256']:
                raise RuntimeError('Host archive member bytes changed')
    policy = {
        'status': 'INACTIVE_NORMAL_ANIMATION_DIAGNOSTIC_PREPARED',
        'serial': 'emulator-5560', 'avd': 'MacroDroid_API35_Disposable',
        'reference_current_failure': 'run 38205737183 remains JOURNEY_DIFFERENCE with 26 differing TRIGGERS pixels',
        'original_apk_sha256': '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800',
        'candidate_apk_sha256': '9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2',
        'ten_screen_plan_sha256': '5a8ca21b8e96b0ae2cfe55bc944e93749534209ca81b04141ce77eef0416c453',
        'explicit_animation_scales': {'animator_duration_scale': '1', 'window_animation_scale': '1',
                                      'transition_animation_scale': '1'},
        'configuration_commands': 19, 'host_tests': 9, 'android_executed': False,
        'apks_modified': False, 'comparison_policy_modified': False, 'existing_workflow_modified': False,
        'sample_selection': 'The unchanged ten-screen policy accepts the first two consecutive whole PNG/XML-identical captures, retaining every attempt.',
        'bounds': 'Six attempts/30 seconds; original full pre-input freshness, process and installed-APK checks stay unchanged.',
        'comparison': 'Complete decoded RGBA frames, full XML and color metadata, zero changed pixels required.',
        'scope': 'A fresh independent diagnostic using normal animation settings; prior failures and default scale-zero policy remain intact.',
        'animation_motion_parity_established': False, 'rendering_cause_established': False,
        'full_runtime_1_to_1_established': False,
    }
    (args.checkpoint / 'policy.json').write_text(json.dumps(policy, indent=2) + '\n')
    (args.checkpoint / 'README.md').write_text(
        '# Independent normal-animation diagnostic\n\n'
        'The original APK has produced more than one stable intro-dot rendering across recorded runs. '
        'A separate diagnostic will set and verify all three Android animation scales to `1` before repeating '
        'the existing ten-screen journey with unchanged PNG, XML, process, input and APK checks. '
        'This package does not modify the active APK or the existing scale-zero workflow, and does not '
        'turn any prior mismatch into a pass.\n\n'
        'The setting preparer pins the disposable emulator identity before its three writes, preserves '
        'all 19 raw command results, checks every readback and rechecks emulator identity afterward. '
        'Nine host tests passed using simulated ADB, including malformed identity, diagnostics, stale '
        'or reordered commands, changed file hashes, aliases and incorrect readbacks. '
        'These host tests do not execute Android.\n\n'
        'The evidence archive retains every regular host-control file. One deliberate symlink fault '
        'is represented by its exact inert link metadata in `host-evidence-manifest.json`, so the '
        'archive itself installs no symlink. The manifest records the target bytes too.\n')
    shutil.copy2(Path(__file__), args.checkpoint / 'freeze_package.py')
    files = [{'path': p.relative_to(args.checkpoint).as_posix(), **identity(p)}
             for p in sorted(args.checkpoint.rglob('*')) if p.is_file()]
    checkpoint = {'status': policy['status'], 'android_executed': False,
                  'created_utc': datetime.now(timezone.utc).isoformat(), 'files': files}
    path = args.checkpoint / 'checkpoint.json'
    path.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(path), **identity(path), 'files': len(files),
                      'archived_regular_files': len(regular), 'symlink_fault_records': len(links)}, indent=2))


if __name__ == '__main__':
    main()
