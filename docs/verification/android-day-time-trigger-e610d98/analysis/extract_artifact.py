#!/usr/bin/env python3
"""Extract and rehash an exact GitHub artifact without changing any member bytes."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--bytes', type=int, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--run', type=int, required=True)
    parser.add_argument('--head', required=True)
    parser.add_argument('--artifact-id', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    original = identity(args.archive)
    assert original == {'bytes': args.bytes, 'sha256': args.sha256}
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    files, names, findings = [], set(), []
    private = re.compile(rb'^-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----\r?$|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}', re.MULTILINE)
    with zipfile.ZipFile(args.archive) as archive:
        for info in archive.infolist():
            relative = PurePosixPath(info.filename)
            assert not info.is_dir()
            assert (relative.as_posix() == info.filename and not relative.is_absolute()
                    and '..' not in relative.parts and '\\' not in info.filename)
            assert info.filename not in names
            names.add(info.filename)
            mode = info.external_attr >> 16
            assert not stat.S_ISLNK(mode)
            assert stat.S_IFMT(mode) in (0, stat.S_IFREG)
            raw = archive.read(info)
            assert len(raw) == info.file_size
            path = output / info.filename
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as stream:
                stream.write(raw)
            expected = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
            assert identity(path) == expected
            files.append({'path': info.filename, **expected})
            if private.search(raw) or path.name in ('adbkey', 'adbkey.pub') or b'adb.pubkey=' in raw:
                findings.append(info.filename)
    assert identity(args.archive) == original
    receipt = {'schema': 1, 'run_id': args.run, 'head_sha': args.head,
               'artifact_id': args.artifact_id, 'observed_utc': datetime.now(timezone.utc).isoformat(),
               'archive_filename': args.archive.name, 'archive': original, 'github_digest_matches': True,
               'member_count': len(files), 'expanded_bytes': sum(row['bytes'] for row in files),
               'all_extracted_bytes_reverified': True, 'artifact_transformations': [],
               'key_scan_findings': findings, 'files': files}
    output.with_name(output.name + '-extraction.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({key: value for key, value in receipt.items() if key != 'files'}, indent=2))


if __name__ == '__main__':
    main()
