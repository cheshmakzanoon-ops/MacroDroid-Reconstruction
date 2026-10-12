#!/usr/bin/env python3
"""Retire only closed verification-cache files proved identical to published source."""
from __future__ import annotations

import argparse
import bisect
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import zipfile

PROJECT = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
CACHE = PROJECT / 'build/verify-baseline'
REPO = Path('/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction')
MANIFEST_SHA = '11217d372fef3f4ca644ae4b10019aba69888d7944aeb5c22d7738db2a16eea3'
SOURCE_ZIP_SHA = 'c11f2d4727a6882943ffccbd81fa45dc738b6fe9c1c5a1c620564e90d8824e01'
DURABLE_COMMIT = 'c9373851d4408fb4db63c21873ac2d0bb6867270'


def now():
    return datetime.now(timezone.utc).isoformat()


def identity(path):
    digest = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        while raw := stream.read(1024 * 1024):
            digest.update(raw)
            size += len(raw)
    return {'bytes': size, 'sha256': digest.hexdigest()}


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def closed_file(path, root):
    if (path.is_symlink() or not path.is_file() or path.resolve() != path
            or not path.is_relative_to(root)):
        raise ValueError('Unconfined or nonregular path: ' + str(path))
    return path.stat()


class PublishedParts(io.RawIOBase):
    """Seek over already present verified parts without assembling another ZIP."""
    def __init__(self, rows):
        self.rows, self.position = rows, 0
        self.starts, self.handles = [], []
        total = 0
        for row in rows:
            self.starts.append(total)
            total += row['size_bytes']
            self.handles.append((REPO / row['path']).open('rb'))
        self.size = total

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self.position

    def seek(self, value, whence=0):
        position = value if whence == 0 else self.position + value if whence == 1 else self.size + value
        if position < 0:
            raise ValueError('Negative multipart seek')
        self.position = position
        return position

    def read(self, size=-1):
        remaining = max(0, self.size - self.position)
        size = remaining if size < 0 else min(size, remaining)
        chunks = []
        while size:
            index = bisect.bisect_right(self.starts, self.position) - 1
            offset = self.position - self.starts[index]
            amount = min(size, self.rows[index]['size_bytes'] - offset)
            stream = self.handles[index]
            stream.seek(offset)
            raw = stream.read(amount)
            if len(raw) != amount:
                raise ValueError('Multipart source changed during reading')
            chunks.append(raw)
            self.position += amount
            size -= amount
        return b''.join(chunks)

    def close(self):
        for handle in self.handles:
            handle.close()
        super().close()


def observed_process_references():
    result = {'self_physical_pid': int(Path('/proc/self').resolve().name),
              'cache_references': [], 'unavailable_process_checks': [],
              'scope': 'Best-effort observable process metadata; unavailable checks are not passes.'}
    for process in sorted(Path('/proc').iterdir()):
        if not process.name.isdigit():
            continue
        for role in ('cwd', 'exe'):
            try:
                target = (process / role).readlink()
                if str(target).startswith(str(CACHE)):
                    result['cache_references'].append({'pid': process.name, 'role': role, 'target': str(target)})
            except (PermissionError, FileNotFoundError, ProcessLookupError, OSError) as error:
                result['unavailable_process_checks'].append({'pid': process.name, 'role': role, 'error': type(error).__name__})
        try:
            for descriptor in (process / 'fd').iterdir():
                try:
                    target = descriptor.readlink()
                    if str(target).startswith(str(CACHE)):
                        result['cache_references'].append({'pid': process.name, 'role': 'fd', 'target': str(target)})
                except (PermissionError, FileNotFoundError, ProcessLookupError, OSError):
                    pass
        except (PermissionError, FileNotFoundError, ProcessLookupError, OSError) as error:
            result['unavailable_process_checks'].append({'pid': process.name, 'role': 'fd', 'error': type(error).__name__})
    if result['cache_references']:
        raise ValueError('An observable process still uses the retirement cache')
    return result


def protected_files():
    paths = [PROJECT / 'source/class-index.json', PROJECT / 'build.py']
    paths += [path for folder in ('dist', 'reports') for path in (PROJECT / folder).rglob('*') if path.is_file()]
    paths += [path for path in CACHE.rglob('*') if path.is_file() and path.suffix != '.smali']
    result = []
    for path in sorted(set(paths)):
        closed_file(path, PROJECT)
        result.append({'path': str(path), **identity(path)})
    return result


def assess(output):
    output.mkdir(parents=True, exist_ok=False)
    result = {'status': 'ASSESSING', 'started_utc': now(), 'cache': str(CACHE),
              'mutations_performed': False, 'free_bytes_before': shutil.disk_usage(PROJECT).free}
    try:
        manifest = REPO / 'vendor/v9/manifest.json'
        if identity(manifest)['sha256'] != MANIFEST_SHA:
            raise ValueError('Durable vendor manifest changed')
        source = next(row for row in json.loads(manifest.read_text())['archives'] if row['id'] == 'source')
        combined = hashlib.sha256()
        for row in source['parts']:
            path = REPO / row['path']
            closed_file(path, REPO)
            raw = path.read_bytes()
            if len(raw) != row['size_bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
                raise ValueError('Published source part changed')
            blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
            if blob != row['git_blob_sha1']:
                raise ValueError('Published source Git object differs')
            combined.update(raw)
        if combined.hexdigest() != SOURCE_ZIP_SHA or source['sha256'] != SOURCE_ZIP_SHA:
            raise ValueError('Published complete source ZIP differs')
        result['durable_source'] = {'repository': 'https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction.git',
            'commit': DURABLE_COMMIT, 'manifest': 'vendor/v9/manifest.json', 'manifest_sha256': MANIFEST_SHA,
            'archive_sha256': SOURCE_ZIP_SHA, 'archive_bytes': source['size_bytes'], 'all_parts_verified': len(source['parts'])}
        index = json.loads((PROJECT / 'source/class-index.json').read_text())
        expected = {row['path']: row for row in index.values()}
        if len(expected) != 71267:
            raise ValueError('Canonical class inventory changed')
        protected = protected_files()
        save(output / 'protected-before.json', protected)
        count, total, allocated = 0, 0, 0
        consumed, cache_paths, inodes = set(), set(), set()
        with PublishedParts(source['parts']) as stream, zipfile.ZipFile(stream) as archive, gzip.open(output / 'exact-duplicates.jsonl.gz', 'wt') as records:
            members = archive.infolist()
            if len({item.filename for item in members}) != len(members):
                raise ValueError('Ambiguous source ZIP inventory')
            for member in members:
                name = member.filename.removeprefix('MacroDroid_v9/')
                if name not in expected:
                    continue
                entry = expected[name]
                cache = CACHE / entry['partition'] / (entry['descriptor'][1:-1] + '.smali')
                canonical = PROJECT / name
                cs, ss = closed_file(cache, CACHE), closed_file(canonical, PROJECT)
                raw = archive.read(member)
                original = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
                if original['sha256'] != entry['sha256'] or identity(cache) != original or identity(canonical) != original:
                    raise ValueError('Cache/source/published member are not exact duplicates: ' + name)
                if cache in cache_paths or (cs.st_dev, cs.st_ino) == (ss.st_dev, ss.st_ino):
                    raise ValueError('Ambiguous retirement path or shared source inode')
                row = {'cache': str(cache), 'source': str(canonical), 'archive_member': member.filename,
                       **original, 'cache_mode': stat.S_IMODE(cs.st_mode), 'cache_dev': cs.st_dev,
                       'cache_inode': cs.st_ino, 'cache_nlink': cs.st_nlink,
                       'source_dev': ss.st_dev, 'source_inode': ss.st_ino}
                records.write(json.dumps(row, separators=(',', ':')) + '\n')
                consumed.add(name)
                cache_paths.add(cache)
                count += 1
                total += cs.st_size
                if (cs.st_dev, cs.st_ino) not in inodes:
                    allocated += cs.st_blocks * 512
                    inodes.add((cs.st_dev, cs.st_ino))
                if count % 10000 == 0:
                    print(json.dumps({'verified_exact_duplicates': count}), flush=True)
        if consumed != set(expected) or cache_paths != {path for path in CACHE.rglob('*.smali') if path.is_file()}:
            raise ValueError('Complete canonical/cache membership differs')
        result.update(status='EXACT_PUBLISHED_SOURCE_DUPLICATES_VERIFIED', files=count,
            logical_bytes=total, allocated_bytes_observed=allocated, protected_files=len(protected),
            owner_confirmations={'root': 'Closed full acceptance and cache sample reads.',
                'build_environment': 'No active or planned reads; complete combined review closed and durable.',
                'recover_touch_action': 'No active or planned reads; future micro-D8 excludes this cache.',
                'repository_transfer': 'No current or planned reader/writer; only frozen proofs and repo objects used.'},
            process_observation=observed_process_references(),
            intended_operation='Atomic zero-byte placeholders at only this exact closed duplicate cache inventory; no source links or process changes.')
    except Exception as error:
        result.update(status='ASSESSMENT_REJECTED', reason=type(error).__name__ + ': ' + str(error))
        raise
    finally:
        result['finished_utc'] = now()
        save(output / 'result.json', result)
    shutil.copyfile(Path(__file__), output / 'retire_verified_smali_duplicates.py')
    files = [{'path': path.name, **identity(path)} for path in sorted(output.iterdir()) if path.is_file()]
    save(output / 'checkpoint.json', {'status': result['status'], 'created_utc': now(), 'mutations_performed': False, 'files': files})
    print(json.dumps({'checkpoint': str(output / 'checkpoint.json'), **identity(output / 'checkpoint.json'),
                      'files': count, 'logical_bytes': total, 'allocated_bytes_observed': allocated}, indent=2))


def retire(assessment, output, published_commit):
    if len(published_commit) != 40 or any(char not in '0123456789abcdef' for char in published_commit):
        raise ValueError('Exact published assessment commit required')
    frozen = json.loads((assessment / 'checkpoint.json').read_text())
    if frozen['status'] != 'EXACT_PUBLISHED_SOURCE_DUPLICATES_VERIFIED':
        raise ValueError('A complete exact duplicate assessment is required')
    for row in frozen['files']:
        if identity(assessment / row['path']) != {key: row[key] for key in ('bytes', 'sha256')}:
            raise ValueError('Frozen assessment input changed')
    output.mkdir(parents=True, exist_ok=False)
    result = {'status': 'RETIRING_CLOSED_EXACT_DUPLICATES', 'started_utc': now(),
              'assessment_commit': published_commit, 'assessment_sha256': identity(assessment / 'checkpoint.json')['sha256'],
              'free_bytes_before': shutil.disk_usage(PROJECT).free, 'replaced_files': 0,
              'process_observation': observed_process_references()}
    try:
        with gzip.open(assessment / 'exact-duplicates.jsonl.gz', 'rt') as records:
            rows = [json.loads(line) for line in records]
        for row in rows:
            path, source = Path(row['cache']), Path(row['source'])
            info = closed_file(path, CACHE)
            expected = {key: row[key] for key in ('bytes', 'sha256')}
            if (info.st_dev != row['cache_dev'] or info.st_ino != row['cache_inode']
                    or identity(path) != expected or identity(source) != expected):
                raise ValueError('Exact assessed source or cache identity changed before retirement')
        for row in rows:
            path = Path(row['cache'])
            temporary = path.with_name(path.name + '.retired-placeholder')
            descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, row['cache_mode'])
            os.fchmod(descriptor, row['cache_mode'])
            os.close(descriptor)
            temporary.replace(path)
            result['replaced_files'] += 1
        for row in rows:
            path, source = Path(row['cache']), Path(row['source'])
            if closed_file(path, CACHE).st_size != 0 or identity(source) != {key: row[key] for key in ('bytes', 'sha256')}:
                raise ValueError('Placeholder or protected source postcondition differs')
        protected = json.loads((assessment / 'protected-before.json').read_text())
        for row in protected:
            if identity(Path(row['path'])) != {key: row[key] for key in ('bytes', 'sha256')}:
                raise ValueError('Protected artifact changed: ' + row['path'])
        result.update(status='CLOSED_DUPLICATE_CACHE_RETIRED_WITH_PROTECTED_BYTES_UNCHANGED',
            all_placeholders_zero=True, all_canonical_sources_unchanged=True,
            protected_files_unchanged=len(protected), canonical_source_files_unchanged=len(rows),
            no_source_hardlinks_created=True, no_process_or_sync_controls_changed=True)
    except Exception as error:
        result.update(status='RETIREMENT_INCOMPLETE', reason=type(error).__name__ + ': ' + str(error))
        raise
    finally:
        result.update(finished_utc=now(), free_bytes_after=shutil.disk_usage(PROJECT).free)
        save(output / 'receipt.json', result)
    shutil.copyfile(Path(__file__), output / 'retire_verified_smali_duplicates.py')
    files = [{'path': path.name, **identity(path)} for path in sorted(output.iterdir()) if path.is_file()]
    save(output / 'checkpoint.json', {'status': result['status'], 'created_utc': now(), 'files': files})
    print(json.dumps({'checkpoint': str(output / 'checkpoint.json'), **identity(output / 'checkpoint.json'),
        **{key: result[key] for key in ('status', 'replaced_files', 'free_bytes_before', 'free_bytes_after',
                                       'protected_files_unchanged', 'canonical_source_files_unchanged')}}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    check = commands.add_parser('assess')
    check.add_argument('--output', type=Path, required=True)
    action = commands.add_parser('retire')
    action.add_argument('--assessment', type=Path, required=True)
    action.add_argument('--output', type=Path, required=True)
    action.add_argument('--published-commit', required=True)
    args = parser.parse_args()
    if args.command == 'assess':
        assess(args.output.resolve())
    else:
        retire(args.assessment.resolve(), args.output.resolve(), args.published_commit)


if __name__ == '__main__':
    main()
