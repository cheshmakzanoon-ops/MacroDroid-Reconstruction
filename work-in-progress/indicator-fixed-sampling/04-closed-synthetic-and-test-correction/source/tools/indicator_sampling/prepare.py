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
    'test_indicator_sampling.py', 'pins.json', 'protocol.json', 'historical-coordinates.json', 'aapt2',
    'fixtures/original-intro1-preinput.xml', 'fixtures/candidate-intro1-preinput.xml',
    'fixtures/original-intro2.xml', 'fixtures/candidate-intro2.xml',
)
WORKFLOW = '.github/workflows/indicator-fixed-sampling.yml'


def source_manifest(source_root):
    """Reconstruct the required names before reading a report's inventory."""
    source_root = Path(source_root).resolve()
    c.require(c.HERE == source_root / 'tools/indicator_sampling', 'Executing diagnostic module has another source root')
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


def offline_command(argv, seconds, label, evidence):
    """Keep partial stdout/stderr and the literal bounded result on every exit."""
    record = {'argv': argv, 'timeout_seconds': seconds, 'started_ns': c.now_ns(),
              'timed_out': False}
    try:
        process = subprocess.run(argv, capture_output=True, timeout=seconds)
        record['returncode'], out, err = process.returncode, process.stdout, process.stderr
    except subprocess.TimeoutExpired as error:
        record.update(returncode=None, timed_out=True)
        out, err = error.stdout or b'', error.stderr or b''
    except OSError as error:
        record.update(returncode=None, error=type(error).__name__ + ': ' + str(error))
        out, err = b'', str(error).encode()
    record['finished_ns'] = c.now_ns()
    for name, raw in [('stdout', out), ('stderr', err)]:
        filename = label + '.' + name
        with (evidence / filename).open('xb') as stream:
            stream.write(raw)
        record[name] = {'path': filename, **c.identity(raw)}
    with (evidence / (label + '-command.json')).open('xb') as stream:
        stream.write(c.bytes_json(record))
    return record


def inspect_apk(path, role, evidence, metadata_function):
    wanted = c.ORIGINAL if role == 'original' else c.CANDIDATE
    c.require(c.file_identity(path) == wanted, 'Fixed ' + role + ' APK changed')
    aapt = c.HERE / 'aapt2'
    c.require(c.file_identity(aapt) == c.json_file(c.HERE / 'pins.json')['aapt2'], 'AAPT2 differs')
    archive = zip_metadata(path)
    argv = [str(aapt), 'dump', 'badging', str(path)]
    record = offline_command(argv, 60, role + '-badging', evidence)
    out = (evidence / record['stdout']['path']).read_bytes()
    err = (evidence / record['stderr']['path']).read_bytes()
    c.require(record['returncode'] == 0 and record['timed_out'] is False and 'error' not in record
              and not err.strip(), 'AAPT2 inspection failed; partial output retained')
    metadata = metadata_function(out.decode())
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
              'python_executable': sys.executable,
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
            process = offline_command(argv, 120, role + '-assembly', output)
            report['assembly'][role] = process
            c.require(process['returncode'] == 0 and process['timed_out'] is False and 'error' not in process
                      and not (output / process['stderr']['path']).read_bytes().strip(),
                      'Pinned assembly failed; partial output retained: ' + role)
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


def verify_preparation(parents, source_root, output, archive_apks=None):
    """Exact inputs in either live or explicitly relocated saved-byte replay.

    Replay reads the immutable original argv/root strings. It separately hashes
    caller-supplied local copies of the same parent parts, source and APK bytes;
    it never rewrites the original receipt or claims new execution/stat data.
    """
    parents, source_root, output = map(lambda p: Path(p).resolve(), (parents, source_root, output))
    report = c.json_file(output / 'preparation.json')
    c.require(report.get('schema') == 1 and report.get('status') == 'EXACT_DIAGNOSTIC_INPUTS_READY'
              and report.get('parent_commit') == c.PARENT_COMMIT and report.get('android_executed') is False,
              'The exact offline input preflight is incomplete')
    expected = expected_inputs(parents, source_root)
    c.require(report['inputs'] == expected, 'Preflight inventory omitted, changed or reordered a required role')
    c.clock_interval(report['started_ns'], report['finished_ns'], 'complete offline preflight')
    for key in ('parent_root', 'source_root', 'apk_root', 'python_executable'):
        value = report[key]
        c.require(type(value) is str and Path(value).is_absolute() and str(Path(value)) == value
                  and '..' not in Path(value).parts, 'Noncanonical original preflight path: ' + key)
    if archive_apks is None:
        c.require(report['parent_root'] == str(parents) and report['source_root'] == str(source_root)
                  and report['python_executable'] == sys.executable,
                  'Preflight source/interpreter roots differ from the executed roots')
        local_apk_root = Path(report['apk_root'])
    else:
        local_apk_root = Path(archive_apks).resolve()
    required_copies = set()
    for row in expected:
        if row['role'].endswith('-part'):
            continue
        name = 'inputs/' + ('diagnostic/' if row['role'] == 'diagnostic-source' else 'parents/') + row['path']
        required_copies.add(name)
        c.require(c.file_identity(c.checked_path(output, name)) == {k: row[k] for k in ('bytes', 'sha256')},
                  'Retained executed input copy differs: ' + name)
    c.require({path.relative_to(output).as_posix() for path in (output / 'inputs').rglob('*') if path.is_file()}
              == required_copies, 'Unlisted or missing retained preflight input copy')
    modules = c.load_parents(parents)
    used, physical = set(), set()
    previous = report['started_ns']
    c.require(set(report['apks']) == set(report['assembly']) == {'original', 'candidate'},
              'Both exact APK inspection and assembly roles are required')
    for role, manifest in c.MANIFESTS.items():
        item = report['apks'][role]
        wanted = c.ORIGINAL if role == 'original' else c.CANDIDATE
        recorded_path = Path(report['apk_root']) / (role + '.apk')
        path = c.checked_path(local_apk_root, role + '.apk')
        c.require(item['path'] == str(recorded_path) and c.file_identity(path) == wanted
                  and {key: item[key] for key in ('bytes', 'sha256')} == wanted,
                  'Materialized APK differs: ' + role)
        c.require(item['zip'] == zip_metadata(path), 'APK ZIP inspection changed')
        assembly = report['assembly'][role]
        expected_assembly = [report['python_executable'], '-B', str(Path(report['parent_root']) / 'scripts/assemble_artifact.py'),
                             str(Path(report['parent_root']) / manifest), '--output', str(recorded_path)]
        for label, command, argv, seconds in [(role + '-assembly', assembly, expected_assembly, 120),
                (role + '-badging', item['badging'],
                 [str(Path(report['source_root']) / 'tools/indicator_sampling/aapt2'), 'dump', 'badging', str(recorded_path)], 60)]:
            c.require(command['argv'] == argv and command['returncode'] == 0 and type(command['returncode']) is int
                      and command['timeout_seconds'] == seconds and command['timed_out'] is False
                      and 'error' not in command, 'Offline command identity differs')
            c.require(c.checked_path(output, label + '-command.json').read_bytes() == c.bytes_json(command),
                      'Immutable offline command record differs')
            c.clock_interval(command['started_ns'], command['finished_ns'], 'offline command')
            c.require(command['finished_ns'] - command['started_ns'] <= seconds * 1_000_000_000,
                      'Offline command exceeded its bound')
            c.require(previous <= command['started_ns'] <= command['finished_ns'] <= report['finished_ns'],
                      'Offline command chronology differs')
            previous = command['finished_ns']
            raw = {}
            for stream in ('stdout', 'stderr'):
                artifact = command[stream]
                c.require(artifact['path'] == label + '.' + stream and artifact['path'] not in used,
                          'Offline command reused or renamed another stream')
                used.add(artifact['path'])
                actual_path = c.checked_path(output, artifact['path'])
                actual_stat = actual_path.stat()
                inode = (actual_stat.st_dev, actual_stat.st_ino)
                c.require(actual_stat.st_nlink == 1 and inode not in physical, 'Offline streams share a physical file')
                physical.add(inode)
                data = actual_path.read_bytes()
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
