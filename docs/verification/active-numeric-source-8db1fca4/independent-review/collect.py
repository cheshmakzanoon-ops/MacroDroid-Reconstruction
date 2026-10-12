#!/usr/bin/env python3
"""One content pass over the owned downloaded ZIP; retain compact reports, never APKs."""
from __future__ import annotations

from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import traceback
import zipfile

BASE = Path('/dev/shm/macrodroid-transfer-space-20261012/active-numeric-source-run-38247941263')
ZIP = BASE / 'artifact.zip'
OWN = Path('/dev/shm/macrodroid-active-numeric-independent-review')
OUT = OWN / 'collection-01'
EXPECTED_SHA = '4824e07658f0e5a808a9dc0b10615b030e3d5f3d030b0fa4ff40096060a34159'
EXPECTED_BYTES = 188572653
ACTIVE_ACCEPTANCE = 'reports/acceptance-20261012T121707487120Z/'


class ContentPassReader:
    """Hash every compressed container byte once during ordered member reads.

    ZipFile first reads its small central directory. After begin(), member reads
    proceed in physical header order, with unconsumed gaps and the final central
    directory fed to the same digest. No full preliminary ZIP hash pass is used.
    """
    def __init__(self, stream):
        self.stream = stream
        self.enabled = False
        self.covered = 0
        self.digest = hashlib.sha256()
        self.metadata_bytes = 0
        self.overlap_bytes = 0

    def __getattr__(self, name):
        return getattr(self.stream, name)

    def begin(self):
        self.enabled = True

    def read(self, size=-1):
        position = self.stream.tell()
        if not self.enabled:
            data = self.stream.read(size)
            self.metadata_bytes += len(data)
            return data
        if position > self.covered:
            self.stream.seek(self.covered)
            remaining = position - self.covered
            while remaining:
                chunk = self.stream.read(min(1024 * 1024, remaining))
                assert chunk, 'Unexpected EOF while hashing a ZIP gap'
                self.digest.update(chunk)
                self.covered += len(chunk)
                remaining -= len(chunk)
            assert self.stream.tell() == position
        data = self.stream.read(size)
        overlap = max(0, min(len(data), self.covered - position))
        self.overlap_bytes += overlap
        if overlap < len(data):
            self.digest.update(data[overlap:])
            self.covered = position + len(data)
        return data

    def finish(self, length):
        self.stream.seek(length)
        assert self.read(0) == b'' and self.covered == length
        return self.digest.hexdigest()


def file_identity(path):
    value = path.lstat()
    assert stat.S_ISREG(value.st_mode), str(path)
    return {'bytes': value.st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'mode': stat.S_IMODE(value.st_mode)}


def save(name, value):
    target = OUT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def retained(name, size):
    if name == 'reports/release-input-snapshot.json':
        return True
    if name.startswith(ACTIVE_ACCEPTANCE):
        return name.endswith(('.json', '.log'))
    if name.startswith('reports/day-numeric-dex-'):
        return size <= 2 * 1024 * 1024
    if name.count('/') == 1 and name.startswith('reports/'):
        if name.endswith('.json') and 'negative-failures' not in name:
            return size <= 2 * 1024 * 1024
        if name.endswith('.log'):
            base = name.removeprefix('reports/')
            return size <= 1024 * 1024 and (base.startswith(('java-', 'python-', 'ui-', 'full-apk-', 'input-', 'static-', 'constructor-', 'widget-bitwise-'))
                                              or base.endswith('positive-restoration.log'))
    return False


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(__file__, OUT / 'executed-collector.py')
    result = {'schema': 1, 'status': 'COLLECTION_PENDING', 'passed': False,
              'started_utc': datetime.now(timezone.utc).isoformat(), 'zip_path': str(ZIP),
              'android_executed': False, 'application_build_executed': False,
              'suites_executed': False, 'apk_files_materialized': False}
    start = ZIP.lstat()
    assert stat.S_ISREG(start.st_mode) and start.st_size == EXPECTED_BYTES
    try:
        metadata = {}
        for name in ('github-jobs.json', 'github-artifacts.json', 'artifact.zip.download.json'):
            path = BASE / name
            row = file_identity(path)
            metadata[name] = row
            target = OUT / 'github' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
            assert file_identity(target) == file_identity(path) == row
        result['github_metadata'] = metadata
        with ZIP.open('rb') as raw:
            reader = ContentPassReader(raw)
            with zipfile.ZipFile(reader) as archive:
                infos = sorted(archive.infolist(), key=lambda info: info.header_offset)
                assert len(infos) == 1304 and all(not info.is_dir() for info in infos)
                assert len({info.filename for info in infos}) == len(infos)
                selected = [info for info in infos if retained(info.filename, info.file_size)]
                assert sum(info.file_size for info in selected) < 64 * 1024 * 1024
                reader.begin()
                members = []
                selected_rows = []
                apk_rows = []
                for info in infos:
                    logical = PurePosixPath(info.filename)
                    assert not logical.is_absolute() and '..' not in logical.parts
                    assert not stat.S_ISLNK(info.external_attr >> 16)
                    capture = retained(info.filename, info.file_size)
                    compressed_copy = info.filename == 'reports/release-input-snapshot.json'
                    output = None
                    if capture:
                        target = OUT / 'retained' / (info.filename + ('.gz' if compressed_copy else ''))
                        target.parent.mkdir(parents=True, exist_ok=True)
                        if compressed_copy:
                            base_stream = target.open('xb')
                            output = gzip.GzipFile(filename='', mode='wb', fileobj=base_stream, mtime=0)
                        else:
                            output = target.open('xb')
                    digest, length = hashlib.sha256(), 0
                    try:
                        with archive.open(info) as stream:
                            while True:
                                data = stream.read(1024 * 1024)
                                if not data:
                                    break
                                digest.update(data); length += len(data)
                                if output:
                                    output.write(data)
                    finally:
                        if output:
                            output.close()
                            if compressed_copy:
                                base_stream.close()
                    assert length == info.file_size
                    row = {'path': info.filename, 'bytes': length, 'sha256': digest.hexdigest(),
                           'zip_crc32': f'{info.CRC:08x}', 'zip_mode': info.external_attr >> 16,
                           'zip_compression': info.compress_type, 'zip_compressed_bytes': info.compress_size,
                           'zip_header_offset': info.header_offset, 'zip_datetime': list(info.date_time)}
                    members.append(row)
                    if capture:
                        selected_rows.append({'source': row, 'retained_path': target.relative_to(OUT).as_posix(),
                                              'retained': file_identity(target), 'gzip_copy': compressed_copy})
                    if info.filename.endswith('.apk'):
                        apk_rows.append(row)
                digest = reader.finish(start.st_size)
                assert digest == EXPECTED_SHA
                assert sum(row['bytes'] for row in members) == 456205098
                save('zip-member-inventory.json', members)
                save('retained-file-bindings.json', selected_rows)
                result.update(status='SINGLE_CONTENT_PASS_COMPLETE', passed=True, archive_sha256=digest,
                    archive_bytes=reader.covered, member_count=len(members),
                    uncompressed_member_bytes=sum(row['bytes'] for row in members),
                    preliminary_central_metadata_read_bytes=reader.metadata_bytes,
                    overlap_bytes_during_content_pass=reader.overlap_bytes,
                    retained_files=len(selected_rows), retained_original_bytes=sum(row['source']['bytes'] for row in selected_rows),
                    retained_disk_bytes=sum(row['retained']['bytes'] for row in selected_rows), apks=apk_rows)
    except Exception as exc:
        result.update(status='COLLECTION_FAILED', error=repr(exc), traceback=traceback.format_exc())
    finally:
        end = ZIP.lstat()
        unchanged = (start.st_dev, start.st_ino, start.st_size, start.st_mtime_ns, start.st_ctime_ns) == (
            end.st_dev, end.st_ino, end.st_size, end.st_mtime_ns, end.st_ctime_ns)
        result['archive_identity_unchanged'] = unchanged
        if not unchanged:
            result['passed'] = False
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save('result.json', result)
        print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
