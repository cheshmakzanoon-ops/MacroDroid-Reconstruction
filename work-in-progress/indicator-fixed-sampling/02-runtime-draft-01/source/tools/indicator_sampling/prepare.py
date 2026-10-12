#!/usr/bin/env python3
"""Bind every source/part role and inspect the two immutable diagnostic APKs.

This is a read-only input operation until the two APKs are assembled into a new
owned directory. It never contacts ADB. AAPT2 is the explicitly added dependency;
the sixteen source-design parent declarations remain unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

import common as c


OWN_FILES = (
    'README.md', 'common.py', 'prepare.py', 'record.py', 'verify.py',
    'test_indicator_sampling.py', 'pins.json', 'protocol.json', 'aapt2',
    'fixtures/original-intro1-preinput.xml', 'fixtures/candidate-intro1-preinput.xml',
    'fixtures/original-intro2.xml', 'fixtures/candidate-intro2.xml',
)
WORKFLOW = '.github/workflows/indicator-fixed-sampling.yml'


def source_manifest(source_root):
    """Reconstruct the required names before reading a report's inventory."""
    source_root = Path(source_root).resolve()
    entries = c.json_file(c.HERE / 'runtime-files.json')
    expected = ['tools/indicator_sampling/' + name for name in OWN_FILES] + [WORKFLOW]
    c.require(type(entries) is list and [row.get('path') for row in entries] == sorted(expected),
              'Runtime file names do not match the independently required inventory')
    for row in entries:
        c.require(set(row) == {'path', 'bytes', 'sha256'}, 'Unexpected runtime-file record')
        path = c.checked_path(source_root, row['path'])
        c.require(c.file_identity(path) == {k: row[k] for k in ('bytes', 'sha256')},
                  'Actual diagnostic source differs: ' + row['path'])
    return entries + [{'path': 'tools/indicator_sampling/runtime-files.json',
                       **c.file_identity(c.HERE / 'runtime-files.json')}]


def expected_inputs(parents, source_root):
    """The forty parent/part roles and all exact local runtime roles."""
    parents, source_root = Path(parents).resolve(), Path(source_root).resolve()
    c.protocol()
    pins = c.json_file(c.HERE / 'pins.json')
    c.require(pins['parent_commit'] == c.PARENT_COMMIT and len(pins['parents']) == 16,
              'The sixteen parent declarations are required')
    rows = []
    for item in pins['parents']:
        path = c.checked_path(parents, item['path'])
        wanted = {k: item[k] for k in ('bytes', 'sha256')}
        c.require(c.file_identity(path) == wanted, 'Changed parent: ' + item['path'])
        rows.append({'role': 'parent', 'path': item['path'], **wanted})
    for role, manifest_name in c.MANIFESTS.items():
        manifest = c.json_file(parents / manifest_name)
        wanted = c.ORIGINAL if role == 'original' else c.CANDIDATE
        c.require(manifest['format'] == 'macrodroid-multipart-artifact'
                  and manifest['format_version'] == 1
                  and {'bytes': manifest['size_bytes'], 'sha256': manifest['sha256']} == wanted,
                  'Immutable APK manifest changed: ' + role)
        parts = manifest['parts']
        c.require(len(parts) == 12 and len({p['path'] for p in parts}) == 12,
                  'The twelve fixed APK parts are required: ' + role)
        for item in parts:
            path = c.checked_path(parents, item['path'])
            wanted_part = {'bytes': item['size_bytes'], 'sha256': item['sha256']}
            c.require(c.file_identity(path) == wanted_part, 'Changed APK part: ' + item['path'])
            rows.append({'role': role + '-part', 'path': item['path'], **wanted_part})
    for item in source_manifest(source_root):
        rows.append({'role': 'diagnostic-source', **item})
    c.require(len({(row['role'], row['path']) for row in rows}) == len(rows), 'Duplicate input role')
    return rows


def zip_metadata(path):
    with zipfile.ZipFile(path) as archive:
        members = archive.infolist()
        names = [item.filename for item in members]
        c.require(len(names) == len(set(names)), 'Duplicate APK ZIP member')
        c.require('AndroidManifest.xml' in names and 'resources.arsc' in names
                  and 'classes.dex' in names, 'Required APK members are absent')
        c.require(archive.testzip() is None, 'An APK member failed its CRC check')
        return {'members': len(members), 'duplicate_names': False, 'all_member_crc_checks_passed': True}


def inspect_apk(path, role, evidence, metadata_function):
    wanted = c.ORIGINAL if role == 'original' else c.CANDIDATE
    c.require(c.file_identity(path) == wanted, 'Fixed ' + role + ' APK changed')
    aapt = c.HERE / 'aapt2'
    c.require(c.file_identity(aapt) == c.json_file(c.HERE / 'pins.json')['aapt2'], 'AAPT2 differs')
    archive = zip_metadata(path)
    argv = [str(aapt), 'dump', 'badging', str(path)]
    started = c.now_ns()
    result = subprocess.run(argv, capture_output=True, timeout=60)
    ended = c.now_ns()
    streams = {}
    for name, raw in [('stdout', result.stdout), ('stderr', result.stderr)]:
        filename = role + '-badging.' + name
        with (evidence / filename).open('xb') as stream:
            stream.write(raw)
        streams[name] = {'path': filename, **c.identity(raw)}
    record = {'argv': argv, 'returncode': result.returncode, 'timeout_seconds': 60,
              'started_ns': started, 'finished_ns': ended, **streams}
    c.require(result.returncode == 0 and not result.stderr.strip(), 'AAPT2 inspection failed')
    metadata = metadata_function(result.stdout.decode())
    c.require(c.file_identity(path) == wanted and c.file_identity(aapt) == c.json_file(c.HERE / 'pins.json')['aapt2'],
              'APK or AAPT2 changed during read-only inspection')
    return {'path': str(path), **wanted, 'zip': archive, 'badging': record, 'metadata': metadata}


def prepare(parents, source_root, output, apk_root):
    parents, source_root, output, apk_root = map(lambda p: Path(p).resolve(), (parents, source_root, output, apk_root))
    output.mkdir(parents=True, exist_ok=False)
    apk_root.mkdir(parents=True, exist_ok=False)
    report = {'schema': 1, 'status': 'INPUTS_INCOMPLETE', 'started_utc': c.utc(), 'started_ns': c.now_ns(),
              'parent_commit': c.PARENT_COMMIT, 'source_root': str(source_root), 'parent_root': str(parents),
              'apk_root': str(apk_root), 'inputs': [], 'apks': {}, 'assembly': {},
              'android_executed': False, 'aapt2_extra_dependency': True}
    try:
        report['inputs'] = expected_inputs(parents, source_root)
        for row in report['inputs']:
            if row['role'].endswith('-part'):
                continue  # Pinned complete bytes stay in the immutable repository and assembled APK.
            base = source_root if row['role'] == 'diagnostic-source' else parents
            name = 'inputs/' + ('diagnostic/' if row['role'] == 'diagnostic-source' else 'parents/') + row['path']
            target = output / name
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as stream:
                stream.write((base / row['path']).read_bytes())
            target.chmod((base / row['path']).stat().st_mode & 0o777)
        modules = c.load_parents(parents)
        for role, manifest in c.MANIFESTS.items():
            target = apk_root / (role + '.apk')
            argv = [sys.executable, '-B', str(parents / 'scripts/assemble_artifact.py'),
                    str(parents / manifest), '--output', str(target)]
            start = c.now_ns()
            process = subprocess.run(argv, capture_output=True, timeout=120)
            end = c.now_ns()
            streams = {}
            for name, raw in [('stdout', process.stdout), ('stderr', process.stderr)]:
                filename = role + '-assembly.' + name
                with (output / filename).open('xb') as stream:
                    stream.write(raw)
                streams[name] = {'path': filename, **c.identity(raw)}
            report['assembly'][role] = {'argv': argv, 'returncode': process.returncode,
                'timeout_seconds': 120, 'started_ns': start, 'finished_ns': end, **streams}
            c.require(process.returncode == 0 and not process.stderr.strip(), 'Pinned assembly failed: ' + role)
            report['apks'][role] = inspect_apk(target, role, output, modules['android_acceptance'].badging_metadata)
        report['status'] = 'EXACT_DIAGNOSTIC_INPUTS_READY'
    except Exception as error:
        report['reason'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        report['finished_ns'] = c.now_ns()
        report['finished_utc'] = c.utc()
        c.write_json(output / 'preparation.json', report)
    verify_preparation(parents, source_root, output)
    return report


def verify_preparation(parents, source_root, output):
    """Live input check: reconstructed inventory, copies, actual APKs and raw argv."""
    parents, source_root, output = map(lambda p: Path(p).resolve(), (parents, source_root, output))
    report = c.json_file(output / 'preparation.json')
    c.require(report.get('schema') == 1 and report.get('status') == 'EXACT_DIAGNOSTIC_INPUTS_READY'
              and report.get('parent_commit') == c.PARENT_COMMIT and report.get('android_executed') is False,
              'The exact offline input preflight is incomplete')
    expected = expected_inputs(parents, source_root)
    c.require(report['inputs'] == expected, 'Preflight inventory omitted, changed or reordered a required role')
    c.require(report['parent_root'] == str(parents) and report['source_root'] == str(source_root),
              'Preflight source roots differ from the executed roots')
    for row in expected:
        if row['role'].endswith('-part'):
            continue
        name = 'inputs/' + ('diagnostic/' if row['role'] == 'diagnostic-source' else 'parents/') + row['path']
        c.require(c.file_identity(c.checked_path(output, name)) == {k: row[k] for k in ('bytes', 'sha256')},
                  'Retained executed input copy differs: ' + name)
    modules = c.load_parents(parents)
    used = set()
    for role, manifest in c.MANIFESTS.items():
        item = report['apks'][role]
        wanted = c.ORIGINAL if role == 'original' else c.CANDIDATE
        path = Path(report['apk_root']) / (role + '.apk')
        c.require(item['path'] == str(path) and not path.is_symlink() and c.file_identity(path) == wanted,
                  'Materialized APK differs: ' + role)
        c.require(item['zip'] == zip_metadata(path), 'APK ZIP inspection changed')
        assembly = report['assembly'][role]
        expected_assembly = [sys.executable, '-B', str(parents / 'scripts/assemble_artifact.py'),
                             str(parents / manifest), '--output', str(path)]
        for command, argv, seconds in [(assembly, expected_assembly, 120),
                (item['badging'], [str(c.HERE / 'aapt2'), 'dump', 'badging', str(path)], 60)]:
            c.require(command['argv'] == argv and command['returncode'] == 0 and type(command['returncode']) is int
                      and command['timeout_seconds'] == seconds, 'Offline command identity differs')
            c.clock_interval(command['started_ns'], command['finished_ns'], 'offline command')
            c.require(command['finished_ns'] - command['started_ns'] <= seconds * 1_000_000_000,
                      'Offline command exceeded its bound')
            raw = {}
            for stream in ('stdout', 'stderr'):
                artifact = command[stream]
                c.require(artifact['path'] not in used, 'Offline command reused another stream')
                used.add(artifact['path'])
                data = c.checked_path(output, artifact['path']).read_bytes()
                c.require(c.identity(data) == {k: artifact[k] for k in ('bytes', 'sha256')}, 'Offline stream changed')
                raw[stream] = data
            c.require(not raw['stderr'].strip(), 'Offline command reported stderr')
        badging = c.checked_path(output, item['badging']['stdout']['path']).read_text()
        c.require(item['metadata'] == modules['android_acceptance'].badging_metadata(badging), 'Badging metadata differs')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parents', type=Path, required=True)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--apks', type=Path)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    if args.verify:
        result = verify_preparation(args.parents, args.source_root, args.output)
    else:
        c.require(args.apks is not None, 'A new owned APK directory is required')
        result = prepare(args.parents, args.source_root, args.output, args.apks)
    print(json.dumps({'status': result['status'], 'inputs': len(result['inputs']), 'android_executed': False}, indent=2))


if __name__ == '__main__':
    main()
