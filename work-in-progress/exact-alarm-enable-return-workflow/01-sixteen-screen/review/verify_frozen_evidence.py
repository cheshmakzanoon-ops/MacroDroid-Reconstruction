#!/usr/bin/env python3
"""Verify exact frozen payloads and every indexed immutable content reference."""
from pathlib import Path, PurePosixPath
import argparse
import gzip
import hashlib
import json
import re
import stat
import subprocess
from datetime import datetime, timezone


def digest(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def safe_name(name):
    if (type(name) is not str or not name or PurePosixPath(name).is_absolute()
            or '..' in PurePosixPath(name).parts or PurePosixPath(name).as_posix() != name
            or '\\' in name):
        raise ValueError('Unsafe evidence name')
    return name


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capsule', type=Path, required=True)
    parser.add_argument('--git-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.capsule.resolve()
    output = args.output.resolve()
    if output.is_relative_to(root):
        raise ValueError('The verification receipt must not mutate the frozen capsule')
    report = {'status': 'VERIFYING_COMPLETE_SETTINGS_EVIDENCE', 'passed': False,
              'android_executed': False, 'application_code_executed': False,
              'started_utc': datetime.now(timezone.utc).isoformat()}
    git_commands = []
    byte_cache = {}

    def git(commit, name):
        if re.fullmatch('[0-9a-f]{40}', commit) is None:
            raise ValueError('Invalid immutable Git revision')
        safe_name(name)
        command = ['git', '--git-dir=' + str(args.git_dir.resolve()), 'show', commit + ':' + name]
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        git_commands.append({'commit': commit, 'path': name, 'exit_code': process.returncode,
            'timeout_seconds': 30, 'stdout': digest(process.stdout), 'stderr': digest(process.stderr)})
        if process.returncode:
            raise ValueError('Immutable referenced Git object unavailable: ' + name)
        return process.stdout

    try:
        checkpoint_raw = (root / 'checkpoint.json').read_bytes()
        checkpoint = json.loads(checkpoint_raw)
        rows = checkpoint['files']
        if len({row['path'] for row in rows}) != len(rows):
            raise ValueError('Duplicate frozen payload path')
        local = {}
        for row in rows:
            path = root / safe_name(row['path'])
            info = path.lstat()
            if not stat.S_ISREG(info.st_mode) or path.resolve() != path:
                raise ValueError('Frozen payload is not a confined regular file')
            raw = path.read_bytes()
            expected = {key: row[key] for key in ('bytes', 'sha256')}
            if digest(raw) != expected or ('100755' if info.st_mode & 0o111 else '100644') != row['mode']:
                raise ValueError('Frozen payload changed: ' + row['path'])
            local[row['path']] = expected
        metadata = json.loads((root / 'complete-evidence-index.json.metadata').read_bytes())
        compressed = (root / 'complete-evidence-index.json.gz').read_bytes()
        if digest(compressed) != metadata['compressed']:
            raise ValueError('Compressed evidence index changed')
        raw = gzip.decompress(compressed)
        if digest(raw) != metadata['uncompressed']:
            raise ValueError('Complete evidence index changed')
        index = json.loads(raw)
        records = index['files']
        if len({row['path'] for row in records}) != len(records):
            raise ValueError('Duplicate original evidence path')
        regular = links = total = 0
        external_seen = set()
        multipart_seen = set()
        for row in records:
            safe_name(row['path'])
            if row['kind'] == 'inert_symlink':
                if type(row['target']) is not str:
                    raise ValueError('Invalid inert symlink record')
                links += 1
                continue
            if (row['kind'] != 'regular' or type(row['bytes']) is not int or row['bytes'] < 0
                    or type(row['mode']) is not int or not 0 <= row['mode'] <= 0o7777
                    or re.fullmatch('[0-9a-f]{64}', row['sha256']) is None):
                raise ValueError('Invalid regular evidence record')
            regular += 1
            total += row['bytes']
            expected = {key: row[key] for key in ('bytes', 'sha256')}
            reference = row['content']
            if reference['kind'] == 'capsule_file':
                if local.get(safe_name(reference['path'])) != expected:
                    raise ValueError('Indexed locally retained bytes differ: ' + row['path'])
            elif reference['kind'] == 'git_blob':
                key = (reference['commit'], reference['path'])
                if key not in byte_cache:
                    raw = git(*key)
                    byte_cache[key] = digest(raw)
                    actual_oid = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
                    if actual_oid != reference['git_blob_sha1']:
                        raise ValueError('Referenced Git blob identity changed')
                if byte_cache[key] != expected:
                    raise ValueError('Referenced immutable Git bytes differ')
                external_seen.add(key)
            elif reference['kind'] == 'multipart_manifest':
                key = (reference['commit'], reference['path'])
                if key not in byte_cache:
                    manifest_raw = git(*key)
                    if (hashlib.sha256(manifest_raw).hexdigest() != reference['manifest_sha256']
                            or 'manifest_bytes' in reference and len(manifest_raw) != reference['manifest_bytes']):
                        raise ValueError('Referenced multipart manifest changed')
                    manifest = json.loads(manifest_raw)
                    combined = hashlib.sha256()
                    count = 0
                    for part in manifest['parts']:
                        raw = git(reference['commit'], part['path'])
                        if digest(raw) != {'bytes': part['size_bytes'], 'sha256': part['sha256']}:
                            raise ValueError('Referenced immutable part changed')
                        combined.update(raw)
                        count += len(raw)
                    value = {'bytes': count, 'sha256': combined.hexdigest()}
                    if value != {'bytes': manifest['size_bytes'], 'sha256': manifest['sha256']}:
                        raise ValueError('Referenced multipart reassembly differs')
                    byte_cache[key] = value
                if byte_cache[key] != expected:
                    raise ValueError('Referenced exact logical bytes differ')
                multipart_seen.add(key)
            else:
                raise ValueError('Unknown content reference')
        if (len(records) != metadata['files'] or regular != metadata['regular_paths']
                or regular != index['regular_paths'] or links != index['symlink_paths']
                or total != metadata['logical_regular_bytes'] or total != index['logical_regular_bytes']):
            raise ValueError('Complete indexed evidence totals differ')
        if (root / 'checkpoint.json').read_bytes() != checkpoint_raw:
            raise ValueError('Frozen checkpoint changed during verification')
        report.update(status='COMPLETE_FROZEN_SETTINGS_EVIDENCE_VERIFIED', passed=True,
            checkpoint=digest(checkpoint_raw), frozen_payloads=len(rows),
            indexed_paths=len(records), indexed_regular_paths=regular, inert_symlinks=links,
            logical_regular_bytes=total, unique_git_blob_references=len(external_seen),
            reassembled_multipart_references=len(multipart_seen),
            apk_files_materialized=False,
            scope='Read-only content and publication binding; no host suite, application code, build or Android execution.')
    except Exception as error:
        report.update(status='FROZEN_SETTINGS_EVIDENCE_VERIFICATION_FAILED',
                      reason=type(error).__name__ + ': ' + str(error))
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    report['git_reads'] = git_commands
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x') as stream:
        stream.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'git_reads'}, indent=2))
    return 0 if report['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
