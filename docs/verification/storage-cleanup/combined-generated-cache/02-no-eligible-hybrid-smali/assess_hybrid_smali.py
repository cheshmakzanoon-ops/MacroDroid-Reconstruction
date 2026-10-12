#!/usr/bin/env python3
"""Read-only eligibility proof for exactly the old hybrid-smali cache."""
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
CACHE = PROJECT / 'build/hybrid-smali'
REPO = Path('/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction')
MANIFEST_SHA = '11217d372fef3f4ca644ae4b10019aba69888d7944aeb5c22d7738db2a16eea3'
SOURCE_ZIP_SHA = 'c11f2d4727a6882943ffccbd81fa45dc738b6fe9c1c5a1c620564e90d8824e01'
DURABLE_COMMIT = 'c9373851d4408fb4db63c21873ac2d0bb6867270'
REGISTRY_SHA = '73a37f1ac4148c03a1dc0df9810e899ebb8ff7bcc6f1df7c1672fd525d66a20e'
FROZEN_REGISTRY = Path('/workspace/scratch/4130730d15aa/combined-recovery/checkpoints/05-full-acceptance/project/source/java-method-map.json')


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



import subprocess

OUTPUT = Path('/workspace/scratch/4130730d15aa/combined-cache-inventory/checkpoints/02-hybrid-smali-eligibility')
SURVEY = Path('/workspace/scratch/4130730d15aa/combined-cache-inventory/metadata-inventory.jsonl.gz')
SURVEY_SHA = '34074e100d8552a84af5759fcaad7104ce737686b90bb0f6b0bcfae083f65b33'


def metadata(path):
    s = path.lstat()
    kind = 'file' if stat.S_ISREG(s.st_mode) else 'symlink' if stat.S_ISLNK(s.st_mode) else 'other'
    result = dict(kind=kind, bytes=s.st_size, allocated_bytes=s.st_blocks * 512,
                  device=s.st_dev, inode=s.st_ino, links=s.st_nlink,
                  mode=stat.S_IMODE(s.st_mode), mtime_ns=s.st_mtime_ns, ctime_ns=s.st_ctime_ns)
    if kind == 'symlink':
        result['link_target'] = os.readlink(path)
    return result


def gzip_rows(path, rows):
    with path.open('xb') as stream, gzip.GzipFile(fileobj=stream, filename='', mode='wb', mtime=0) as zipped:
        for row in rows:
            zipped.write((json.dumps(row, separators=(',', ':')) + '\n').encode())


def selected_protected():
    paths = [PROJECT / 'source/class-index.json', PROJECT / 'source/java-method-map.json',
             PROJECT / 'build.py', PROJECT / 'build/hybrid/classes3.dex']
    for relative in ('dist', 'reports', 'build/java/hostclasses', 'tools/classes'):
        base = PROJECT / relative
        if base.exists():
            paths.extend(p for p in base.rglob('*') if p.is_file())
    rows = []
    for path in sorted(set(paths)):
        closed_file(path, PROJECT)
        rows.append(dict(path=str(path), **identity(path)))
    return rows


def process_observation():
    out = dict(reader_physical_pid=int(Path('/proc/self').resolve().name),
               observed_references=[], unavailable=[], processes=[])
    for entry in sorted(Path('/proc').iterdir()):
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        try:
            comm = (entry / 'comm').read_text().strip()
            argv = (entry / 'cmdline').read_bytes().split(b'\0')
            # Record role/identity only. Do not copy unrelated process arguments.
            refs = [arg.decode(errors='replace') for arg in argv if str(CACHE).encode() in arg]
            out['processes'].append(dict(physical_pid=pid, comm=comm, target_argument_count=len(refs)))
            if refs:
                out['observed_references'].append(dict(physical_pid=pid, role='argv', count=len(refs)))
        except (PermissionError, FileNotFoundError, ProcessLookupError, OSError) as error:
            out['unavailable'].append(dict(physical_pid=pid, role='comm/argv', error=type(error).__name__))
        for role in ('cwd', 'exe'):
            try:
                target = (entry / role).readlink()
                if target == CACHE or CACHE in target.parents:
                    out['observed_references'].append(dict(physical_pid=pid, role=role))
            except (PermissionError, FileNotFoundError, ProcessLookupError, OSError) as error:
                out['unavailable'].append(dict(physical_pid=pid, role=role, error=type(error).__name__))
        try:
            descriptors = list((entry / 'fd').iterdir())
        except (PermissionError, FileNotFoundError, ProcessLookupError, OSError) as error:
            out['unavailable'].append(dict(physical_pid=pid, role='fd', error=type(error).__name__))
            continue
        for descriptor in descriptors:
            try:
                target = descriptor.readlink()
                if target == CACHE or CACHE in target.parents:
                    out['observed_references'].append(dict(physical_pid=pid, role='fd', descriptor=descriptor.name))
            except (PermissionError, FileNotFoundError, ProcessLookupError, OSError) as error:
                out['unavailable'].append(dict(physical_pid=pid, role='fd/' + descriptor.name, error=type(error).__name__))
    out['unavailable_checks_are_passes'] = False
    return out


def main():
    OUTPUT.mkdir(parents=True, exist_ok=False)
    result = dict(status='READ_ONLY_ELIGIBILITY_IN_PROGRESS', started_utc=now(), cache=str(CACHE),
                  mutations_performed=False, retirement_authorized=False,
                  free_bytes_before=shutil.disk_usage(PROJECT).free)
    try:
        assert identity(SURVEY)['sha256'] == SURVEY_SHA
        with gzip.open(SURVEY, 'rt') as stream:
            surveyed = {row['path']: row for row in map(json.loads, stream)
                        if row['path'].startswith('hybrid-smali/')}
        assert len(surveyed) == 71267
        gzip_rows(OUTPUT / 'metadata-before.jsonl.gz', [surveyed[k] for k in sorted(surveyed)])
        manifest_raw = (REPO / 'vendor/v9/manifest.json').read_bytes()
        assert hashlib.sha256(manifest_raw).hexdigest() == MANIFEST_SHA
        assert subprocess.check_output(['git', 'show', DURABLE_COMMIT + ':vendor/v9/manifest.json'], cwd=REPO) == manifest_raw
        source = next(a for a in json.loads(manifest_raw)['archives'] if a['id'] == 'source')
        combined = hashlib.sha256()
        part_receipts = []
        for row in source['parts']:
            path = REPO / row['path']; closed_file(path, REPO)
            raw = path.read_bytes()
            assert len(raw) == row['size_bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
            oid = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
            assert oid == row['git_blob_sha1']
            tree = subprocess.check_output(['git', 'ls-tree', DURABLE_COMMIT, '--', row['path']], cwd=REPO).decode().strip()
            assert tree.split()[2] == oid
            combined.update(raw)
            part_receipts.append(row)
        assert combined.hexdigest() == source['sha256'] == SOURCE_ZIP_SHA
        save(OUTPUT / 'published-source-parts.json', dict(commit=DURABLE_COMMIT,
             manifest_sha256=MANIFEST_SHA, archive_sha256=SOURCE_ZIP_SHA, archive_bytes=source['size_bytes'], parts=part_receipts))
        index_raw = (PROJECT / 'source/class-index.json').read_bytes()
        index = json.loads(index_raw)
        expected = {row['path']: row for row in index.values()}
        assert len(expected) == 71267
        registry_path = PROJECT / 'source/java-method-map.json'
        assert identity(registry_path)['sha256'] == identity(FROZEN_REGISTRY)['sha256'] == REGISTRY_SHA
        registry = json.loads(registry_path.read_text())
        recovered = {r['target'] for r in registry}
        assert len(registry) == 1242 and len(recovered) == 605
        protected = selected_protected()
        save(OUTPUT / 'protected-before.json', protected)
        rows, seen, recovered_paths = [], set(), set()
        with PublishedParts(source['parts']) as stream, zipfile.ZipFile(stream) as archive:
            assert archive.read('MacroDroid_v9/source/class-index.json') == index_raw
            members = archive.infolist()
            assert len({m.filename for m in members}) == len(members)
            for member in members:
                name = member.filename.removeprefix('MacroDroid_v9/')
                if name not in expected:
                    continue
                entry = expected[name]
                assert name.startswith('source/smali/') and '..' not in Path(name).parts
                canonical = PROJECT / name
                cache = CACHE / name.removeprefix('source/smali/')
                relative = cache.relative_to(PROJECT / 'build').as_posix()
                assert relative in surveyed and relative not in seen
                cm, sm = metadata(cache), metadata(canonical)
                assert all(cm[key] == value for key, value in surveyed[relative].items() if key != 'path'), relative
                assert sm['kind'] == 'file' and not canonical.is_symlink()
                original = dict(bytes=member.file_size, sha256=hashlib.sha256(archive.read(member)).hexdigest())
                assert original['sha256'] == entry['sha256'] and identity(canonical) == original
                cached = identity(cache) if cm['kind'] == 'file' else None
                reasons = []
                if entry['descriptor'] in recovered:
                    reasons.append('registered recovered class'); recovered_paths.add(relative)
                if cm['kind'] != 'file': reasons.append('nonregular file')
                if cm['links'] != 1: reasons.append('multiple links')
                if cached != original: reasons.append('not an exact published source duplicate')
                if (cm['device'], cm['inode']) == (sm['device'], sm['inode']): reasons.append('shared canonical source inode')
                row = dict(cache=str(cache), source=str(canonical), descriptor=entry['descriptor'],
                           archive_member=member.filename, canonical_identity=original,
                           cache_identity=cached, cache_metadata=cm, source_metadata=sm,
                           eligible=not reasons, retained_reasons=reasons)
                rows.append(row); seen.add(relative)
                if len(rows) % 10000 == 0:
                    print(json.dumps({'verified_canonical_and_cache_rows': len(rows)}), flush=True)
        assert seen == set(surveyed) and len(recovered_paths) == 605
        gzip_rows(OUTPUT / 'all-class-identities-before.jsonl.gz', rows)
        eligible = [r for r in rows if r['eligible']]
        retained = [r for r in rows if not r['eligible']]
        assert all(r['cache_metadata']['links'] == 1 for r in eligible)
        gzip_rows(OUTPUT / 'exact-duplicates.jsonl.gz', eligible)
        save(OUTPUT / 'retained-classes.json', retained)
        after = []
        for row in rows:
            cache, canonical = Path(row['cache']), Path(row['source'])
            assert identity(canonical) == row['canonical_identity']
            assert metadata(canonical) == row['source_metadata']
            assert metadata(cache) == row['cache_metadata']
            if row['cache_identity'] is not None:
                assert identity(cache) == row['cache_identity']
            after.append(dict(path=cache.relative_to(PROJECT / 'build').as_posix(), **metadata(cache)))
        gzip_rows(OUTPUT / 'metadata-after.jsonl.gz', after)
        for row in protected:
            assert identity(Path(row['path'])) == {k: row[k] for k in ('bytes', 'sha256')}, row['path']
        save(OUTPUT / 'protected-after.json', protected)
        result.update(status='READ_ONLY_EXACT_DUPLICATE_ELIGIBILITY_VERIFIED',
                      metadata_inventory_sha256=SURVEY_SHA, complete_cache_paths=len(rows),
                      canonical_source_files_rehashed_unchanged=len(rows),
                      cache_files_rehashed_or_metadata_rechecked_unchanged=len(rows),
                      eligible_files=len(eligible), eligible_logical_bytes=sum(r['cache_metadata']['bytes'] for r in eligible),
                      eligible_allocated_bytes_observed=sum(r['cache_metadata']['allocated_bytes'] for r in eligible),
                      retained_files=len(retained), recovered_classes_retained=len(recovered_paths),
                      all_nonidentical_nonregular_multilink_files_retained=True,
                      protected_files_rehashed_unchanged=len(protected),
                      owner_closure=dict(root='Old hybrid-smali cache closed for reuse; read-only eligibility requested.',
                          build_environment='Parent relayed only old Java hostclasses, tools/classes and hybrid/classes3.dex are required; those are protected.',
                          recover_touch_action='Explicit no current or planned readers or queued jobs for this exact hybrid-smali cache.',
                          repository_transfer='No build or runtime reader; only this bounded read-only assessment.'),
                      process_observation=process_observation())
    except Exception as error:
        result.update(status='READ_ONLY_ELIGIBILITY_REJECTED', reason=type(error).__name__ + ': ' + str(error))
        raise
    finally:
        result.update(finished_utc=now(), free_bytes_after=shutil.disk_usage(PROJECT).free)
        save(OUTPUT / 'result.json', result)
    shutil.copyfile(Path(__file__), OUTPUT / 'assess_hybrid_smali.py')
    files = [dict(path=p.name, **identity(p)) for p in sorted(OUTPUT.iterdir()) if p.is_file()]
    save(OUTPUT / 'checkpoint.json', dict(status=result['status'], created_utc=now(),
         active_files=[], mutations_performed=False, retirement_authorized=False, files=files))
    print(json.dumps({k: result[k] for k in ('status', 'eligible_files', 'eligible_logical_bytes',
                                          'eligible_allocated_bytes_observed', 'retained_files', 'free_bytes_after')}))


if __name__ == '__main__':
    main()

