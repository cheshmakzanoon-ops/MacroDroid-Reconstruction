#!/usr/bin/env python3
"""Prepare exact frozen capture tools for a separate normal-animation journey."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys

GUARD = 'work-in-progress/trigger-category/04-chronology-host-success'
ANIMATION = 'work-in-progress/animation-diagnostic/01-normal-animation-source'
WORKFLOW = '.github/workflows/editor-normal-animation.yml'
PACKAGE = 'work-in-progress/animation-diagnostic/02-reviewed-workflow'
PINS = {
    'scripts/materialize_v9.py': '99a2a50a1518bf7f960ba8bc07b9e4c25bbb882118494cc4b82d0cc87f94be0c',
    'scripts/import_v9.py': '11a1890a9e60d3905181189df6f28963c7c59b2046bc759a28b975d9b309ffa1',
    'scripts/assemble_artifact.py': 'f85a570f864ec2481dd75783b82006129755194c941b54e193c893b7ee17e97c',
    'vendor/v9/manifest.json': '11217d372fef3f4ca644ae4b10019aba69888d7944aeb5c22d7738db2a16eea3',
    'vendor/original/manifest.json': 'b2f12b669ac0e937198216458410aaab03da6682659d6d922c730a175b77d684',
    'artifacts/current/manifest.json': '350f15eca6daf43b129fc66f4fa9e3afc6df9d607cab7ba00919943b3a139730',
    'tools/android/bootstrap_android_runtime.py': '8ae2a365cc5ec5109c76967642d6ee7f6655df96287cf8feb3355444e14e4e36',
    'tools/android/android-toolchain-pins.json': '3ce2078cb52f540fd86ffdccf8577535662fee1c5274f13bcf01d8d15e3bd8b2',
    'tools/android/android_runtime_service.py': '3ac1047b8ff41aba79d1ef335e8eed260067d696460bf8322195631f09dfec57',
    'tools/android/runtime_job.py': '7babd7ebcc35e531b6b0fea9167b3436ff738e43bf0f869b44534573cb849bc8',
    'tools/android/wait_android_ready.py': '72cb3bcd56df72cd901ee724c48a44b0254235e1d7cdda6c991b985e572f34af',
    'tools/android/configure_capture_device.py': '50b93f00b68147323be46c8311ee32d3f201683a40b1825d17a02bc51ce25ec8',
    'tools/android/test_download_retry.py': 'bd5d871951fbf1e5f7aa3093c8c155b1c599d84ae008b90e1eda53bf3a60948a',
    GUARD + '/checkpoint.json': '8aa91588f809c8dc7bfbf88aaf6d96a130fd72502f10076e94043c6e23dc23af',
    ANIMATION + '/checkpoint.json': '42a37e351e0a5ef782f12de9b8140f84eebea4363ec39d4a833fc78122acdcad',
}
APKS = [
    ('vendor/original/manifest.json', 'MacroDroid-5.67.8-original.apk', 95725918,
     '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'),
    ('artifacts/current/manifest.json', 'MacroDroid-5.67.8-current-hybrid.apk', 94683497,
     '9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2'),
]
AAPT = {'bytes': 6135688, 'sha256': '6fbed5edaddcfbee99a3ae6e7208c8654c6cb2bedb4ed5cbbf4e154d7d38a745'}


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def checked_file(root, name):
    relative = PurePosixPath(name)
    if relative.is_absolute() or '..' in relative.parts or '\\' in name:
        raise ValueError('Unsafe input path: ' + name)
    path = root / name
    if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root):
        raise ValueError('Missing or unconfined input: ' + name)
    return path


def prepare(root, output):
    output.mkdir(parents=True, exist_ok=False)
    report = {'status': 'VERIFYING_FROZEN_INPUTS', 'passed': False, 'android_executed': False,
              'github_sha': os.environ.get('GITHUB_SHA'), 'files': [],
              'started_utc': datetime.now(timezone.utc).isoformat()}
    def copy(name, expected, expected_bytes=None, destination=None):
        path = checked_file(root, name)
        actual = identity(path)
        if actual['sha256'] != expected or expected_bytes is not None and actual['bytes'] != expected_bytes:
            raise ValueError('Pinned input changed: ' + name)
        target = output / (destination or ('executed-inputs/' + name))
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(path.read_bytes())
        if identity(target) != actual or identity(path) != actual:
            raise ValueError('Input changed while copying: ' + name)
        report['files'].append({'path': name, 'copy': target.relative_to(output).as_posix(), **actual})
    try:
        for name, expected in PINS.items():
            copy(name, expected)
        for package, count in [(GUARD, 93), (ANIMATION, 7)]:
            checkpoint = json.loads((root / package / 'checkpoint.json').read_text())
            rows = checkpoint['files']
            if len(rows) != count or len({row['path'] for row in rows}) != count:
                raise ValueError('Frozen package inventory changed: ' + package)
            for row in rows:
                copy(package + '/' + row['path'], row['sha256'], row['bytes'])
                if package == GUARD and row['path'].startswith('replay-source/'):
                    suffix = row['path'][len('replay-source/'):]
                    copy(package + '/' + row['path'], row['sha256'], row['bytes'],
                         'reviewed-source/' + suffix)
        guard_inputs = json.loads((root / GUARD / 'reports/inputs-before.json').read_text())
        archives = {name: expected for name, expected in guard_inputs.items() if name.endswith('/evidence.zip')}
        if len(archives) != 2:
            raise ValueError('Exactly two pinned historical host fixtures are required')
        for name, expected in archives.items():
            copy(name, expected['sha256'], expected['bytes'])
            copy(name, expected['sha256'], expected['bytes'], 'reviewed-source/' + name)
        for name, filename, size, digest in APKS:
            value = json.loads((root / name).read_text())
            if (value['filename'], value['size_bytes'], value['sha256']) != (filename, size, digest):
                raise ValueError('Unexpected diagnostic APK identity: ' + name)
        for name in [WORKFLOW, PACKAGE + '/prepare_normal_journey.py', PACKAGE + '/verify_normal_journey.py']:
            copy(name, identity(checked_file(root, name))['sha256'])
        report.update(status='FROZEN_NORMAL_ANIMATION_INPUTS_VERIFIED', passed=True,
                      plan_sha256='5a8ca21b8e96b0ae2cfe55bc944e93749534209ca81b04141ce77eef0416c453',
                      requested_scales='1', full_runtime_1_to_1_established=False)
    except Exception as error:
        report.update(status='FROZEN_INPUT_PREFLIGHT_FAILED', reason=type(error).__name__ + ': ' + str(error))
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (output / 'input-preflight.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def materialized(root, output):
    report = {'status': 'VERIFYING_MATERIALIZED_INPUTS', 'passed': False, 'android_executed': False}
    try:
        initial = json.loads((output / 'input-preflight.json').read_text())
        if initial.get('passed') is not True:
            raise ValueError('Successful frozen input preflight required')
        for row in initial['files']:
            expected = {key: row[key] for key in ('bytes', 'sha256')}
            if (identity(checked_file(root, row['path'])) != expected
                    or identity(checked_file(output, row['copy'])) != expected):
                raise ValueError('Prepared input changed before execution: ' + row['path'])
        source = checked_file(root, 'workspace/MacroDroid_v9/tools/prebuilt/linux/aapt2')
        if identity(source) != AAPT:
            raise ValueError('Preserved AAPT2 identity changed')
        target = output / 'reviewed-source/project/tools/prebuilt/linux/aapt2'
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(source.read_bytes())
        if identity(target) != AAPT:
            raise ValueError('AAPT2 copy changed')
        target.chmod(0o755)
        apk_paths = []
        for _, filename, size, digest in APKS:
            path = checked_file(root, 'workspace/artifacts/' + filename)
            if identity(path) != {'bytes': size, 'sha256': digest}:
                raise ValueError('Materialized APK identity changed: ' + filename)
            apk_paths.append(path)
        sys.dont_write_bytecode = True
        sys.path.insert(0, str(output / 'reviewed-source/project'))
        from android_acceptance import prevalidate_pair
        report['apk_prevalidation'] = prevalidate_pair(*apk_paths)
        report.update(status='EXACT_APKS_AND_AAPT2_VERIFIED_OFFLINE', passed=True,
                      aapt2={'source': str(source.relative_to(root)), 'executed_copy': str(target.relative_to(output)), **AAPT})
    except Exception as error:
        report.update(status='MATERIALIZED_INPUT_PREFLIGHT_FAILED', reason=type(error).__name__ + ': ' + str(error))
        raise
    finally:
        (output / 'materialized-inputs.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--materialized', action='store_true')
    args = parser.parse_args()
    function = materialized if args.materialized else prepare
    print(json.dumps(function(args.root.resolve(), args.output.resolve()), indent=2))


if __name__ == '__main__':
    main()
