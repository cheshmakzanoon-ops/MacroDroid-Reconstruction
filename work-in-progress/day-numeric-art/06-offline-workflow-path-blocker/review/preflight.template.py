#!/usr/bin/env python3
"""Pin complete numeric ART inputs; validate APKs and real result without starting Android."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

MANIFEST_SHA256 = '__MANIFEST_SHA256__'
PARENT_COMMIT = 'fc825ede39a40249e33c8ba75b93128a98bd5e3c'
PACKAGE = 'tools/day_numeric_art'
WORKFLOW = '.github/workflows/day-numeric-method-probe.yml'
ORIGINAL = ('MacroDroid-5.67.8-original.apk', 95725918,
            '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800')
CANDIDATE = ('MacroDroid-5.67.8-day-numeric-0762aad9.apk', 94683136,
             '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd')


def canonical(name):
    if not isinstance(name, str) or not name or '\\' in name:
        raise ValueError('Invalid pinned relative path')
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in ('', '.', '..') for part in name.split('/')) or str(path) != name:
        raise ValueError('Noncanonical pinned relative path')
    return path


def safe_file(root, name):
    relative = canonical(name)
    path = root
    for part in relative.parts:
        path = path / part
        if path.is_symlink():
            raise ValueError('Symlinked input is not allowed: ' + name)
    if not stat.S_ISREG(path.lstat().st_mode) or not path.resolve().is_relative_to(root):
        raise ValueError('Missing or unsafe regular input: ' + name)
    return path


def identity(path, *, git_blob=False):
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise ValueError('Regular input required')
    sha = hashlib.sha256()
    git = hashlib.sha1(b'blob ' + str(before.st_size).encode() + b'\0') if git_blob else None
    size = 0
    with path.open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            sha.update(chunk)
            if git is not None:
                git.update(chunk)
            size += len(chunk)
    after = path.lstat()
    fields = lambda value: (value.st_dev, value.st_ino, value.st_size,
                             value.st_mtime_ns, value.st_ctime_ns, value.st_mode)
    if fields(before) != fields(after) or size != after.st_size:
        raise ValueError('Input changed during read: ' + str(path))
    value = {'bytes': size, 'sha256': sha.hexdigest(),
             'mode': '100755' if after.st_mode & 0o111 else '100644'}
    if git is not None:
        value['git_blob_sha1'] = git.hexdigest()
    return value


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def copy_exact(path, destination, expected):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with path.open('rb') as source, destination.open('xb') as target:
        while chunk := source.read(1024 * 1024):
            target.write(chunk)
    destination.chmod(0o755 if expected['mode'] == '100755' else 0o644)
    if identity(destination) != {key: expected[key] for key in ('bytes', 'sha256', 'mode')}:
        raise ValueError('Retained executed source differs')


def module_from(path):
    spec = importlib.util.spec_from_file_location('fixed_numeric_art_probe', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_inputs(current, parent, output, report):
    manifest_path = safe_file(current, PACKAGE + '/runtime-files.json')
    manifest_raw = manifest_path.read_bytes()
    if hashlib.sha256(manifest_raw).hexdigest() != MANIFEST_SHA256:
        raise ValueError('Exact runtime input manifest changed')
    manifest = json.loads(manifest_raw)
    if (type(manifest.get('schema')) is not int or manifest['schema'] != 1 or
            manifest.get('parent_commit') != PARENT_COMMIT or
            len(manifest.get('source_roles', [])) != 9 or len(manifest.get('parent_roles', [])) != 34):
        raise ValueError('Complete fixed source and parent role inventory required')
    wanted_sources = {row['path'] for row in manifest['source_roles']}
    if len(wanted_sources) != 9 or any(not name.startswith(PACKAGE + '/') for name in wanted_sources):
        raise ValueError('Exact nine source roles required')
    expected_package = wanted_sources | {PACKAGE + '/runtime-files.json', PACKAGE + '/preflight.py'}
    actual_package = {str(path.relative_to(current)) for path in (current / PACKAGE).rglob('*')
                      if path.is_file() or path.is_symlink()}
    if actual_package != expected_package:
        raise ValueError('Executable package has missing or extra input paths')
    if Path(__file__).resolve() != (current / PACKAGE / 'preflight.py').resolve():
        raise ValueError('The checked current preflight must be the executed entry point')
    input_rows = []
    seen = set()
    for surface, rows, root in (('current', manifest['source_roles'], current),
                                ('parent', manifest['parent_roles'], parent)):
        for row in rows:
            name = str(canonical(row['path']))
            key = (surface, name)
            if key in seen or type(row.get('bytes')) is not int or row['bytes'] < 0:
                raise ValueError('Repeated or malformed input identity')
            seen.add(key)
            path = safe_file(root, name)
            actual = identity(path, git_blob=surface == 'parent')
            expected = {key: row[key] for key in actual}
            observation = {'surface': surface, 'path': name, **actual,
                           'expected': expected, 'retained_copy': row['retain_copy']}
            report['files'].append(observation)
            if actual != expected:
                raise ValueError('Pinned source or part changed: ' + surface + '/' + name)
            if type(row['retain_copy']) is not bool:
                raise ValueError('Explicit source retention policy required')
            if row['retain_copy']:
                if actual['bytes'] > 2 * 1024 * 1024:
                    raise ValueError('Unexpected large executed-source payload')
                copy_exact(path, output / 'executed-inputs' / surface / name, actual)
            input_rows.append((path, actual))
    if len(seen) != 43:
        raise ValueError('Complete 43-role inventory required')
    for name in (PACKAGE + '/preflight.py', PACKAGE + '/runtime-files.json', WORKFLOW):
        path = safe_file(current, name)
        actual = identity(path)
        copy_exact(path, output / 'executed-inputs/current' / name, actual)
        report['entry_points'].append({'path': name, **actual})
        input_rows.append((path, actual))
    for label, name, expected_apk in (
            ('original', 'vendor/original/manifest.json', ORIGINAL),
            ('candidate', 'work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json', CANDIDATE)):
        value = json.loads(safe_file(parent, name).read_bytes())
        if (value['filename'], value['size_bytes'], value['sha256']) != expected_apk:
            raise ValueError('Wrong fixed ' + label + ' APK manifest')
        parts = value['parts']
        if len(parts) != 12 or len({part['path'] for part in parts}) != 12:
            raise ValueError('Exactly twelve independent APK parts required')
        for part in parts:
            matching = [row for row in manifest['parent_roles'] if row['path'] == part['path']]
            if len(matching) != 1 or any(matching[0][field] != part[other]
                    for field, other in [('bytes','size_bytes'),('sha256','sha256'),('git_blob_sha1','git_blob_sha1')]):
                raise ValueError('Manifest-to-part role binding differs')
        report['apk_manifests'][label] = {'path': name, 'filename': value['filename'],
                'bytes': value['size_bytes'], 'sha256': value['sha256'], 'parts': len(parts)}
    return input_rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current', type=Path, required=True)
    parser.add_argument('--parent', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--phase', choices=('inputs', 'apks', 'final'), required=True)
    parser.add_argument('--probe-result', type=Path)
    args = parser.parse_args()
    current, parent = args.current.resolve(), args.parent.resolve()
    output = args.output.resolve()
    if args.output.is_symlink() or output.exists():
        raise ValueError('A new owned preflight output directory is required')
    output.mkdir(parents=True, exist_ok=False)
    report = {'schema': 1, 'passed': False, 'phase': args.phase,
        'started_utc': datetime.now(timezone.utc).isoformat(), 'files': [], 'entry_points': [],
        'apk_manifests': {}, 'expected_parent_commit': PARENT_COMMIT,
        'github_sha': os.environ.get('GITHUB_SHA'), 'github_actions': os.environ.get('GITHUB_ACTIONS') == 'true',
        'scope': 'Exact input and output validation; this program never starts a device or application process.',
        'android_started_by_preflight': False, 'app_installed': False, 'app_ui_interaction': False,
        'application_build_executed': False, 'full_runtime_1_to_1_established': False}
    input_rows = []
    try:
        input_rows = verify_inputs(current, parent, output, report)
        if args.phase in ('apks', 'final'):
            if args.phase == 'apks' and args.probe_result is not None:
                raise ValueError('Unexpected runtime report in APK preflight')
            original = safe_file(parent, 'workspace/artifacts/' + ORIGINAL[0])
            candidate = safe_file(parent, 'workspace/artifacts/' + CANDIDATE[0])
            apks_before = [(path, identity(path)) for path in (original, candidate)]
            for (path, observed), expected in zip(apks_before, (ORIGINAL, CANDIDATE)):
                if (observed['bytes'], observed['sha256']) != expected[1:]:
                    raise ValueError('Fixed actual APK identity differs: ' + path.name)
            module = module_from(current / PACKAGE / 'android_day_numeric_method_probe.py')
            report['actual_input_validation'] = module.validate_inputs(original, candidate,
                current / PACKAGE / 'probes/day-numeric-method-probe.dex',
                current / PACKAGE / 'probes/day-numeric-method-probe.json')
            input_rows.extend(apks_before)
            if args.phase == 'final':
                if args.probe_result is None or args.probe_result.is_symlink():
                    raise ValueError('The actual bounded probe result is required')
                folder = args.probe_result.resolve()
                raw = safe_file(folder, 'probe-result.json').read_bytes()
                value = json.loads(raw)
                if module.verify_result(folder, value, serial='emulator-5560') is not True:
                    raise ValueError('The full real numeric result did not verify')
                if safe_file(folder, 'probe-result.json').read_bytes() != raw:
                    raise ValueError('Actual runtime result changed during verification')
                report['runtime_result'] = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                    'status': value['status'], 'verified_without_simulation': True,
                    'both_semantic_case_sets_passed': value['both_semantic_case_sets_passed'],
                    'strict_diagnostics_passed': value['strict_diagnostics_passed'],
                    'cleanup_complete': value['cleanup_complete']}
        elif args.probe_result is not None:
            raise ValueError('Initial input phase cannot consume a runtime result')
        for path, before in input_rows:
            if identity(path, git_blob='git_blob_sha1' in before) != before:
                raise ValueError('Input changed after verification: ' + str(path))
        report.update(passed=True, status='EXACT_NUMERIC_ART_' + args.phase.upper() + '_VERIFIED',
                      inputs_unchanged=True, roles_verified=43, entry_points_retained=3)
    except Exception as error:
        report.update(status='NUMERIC_ART_' + args.phase.upper() + '_VERIFICATION_FAILED',
                      reason=type(error).__name__ + ': ' + str(error))
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(output / 'result.json', report)
        print(json.dumps({key:value for key,value in report.items()
                          if key not in ('files','entry_points','actual_input_validation')}, indent=2))
    return 0 if report['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
