"""Verify and preserve the complete actual Normal03 artifact without transformation."""
from pathlib import Path, PurePosixPath
import datetime
import hashlib
import json
import stat
import zipfile

BASE = Path(__file__).resolve().parent.parent
ZIP = BASE / 'tooling-validation/normal-animation-run-38212813248.zip'
OUT = BASE / 'tooling-validation/normal-animation-run-38212813248'
RECEIPT = BASE / 'tooling-validation/normal-animation-run-38212813248-extraction.json'
EXPECTED = {'bytes': 28080813, 'sha256': '93cfed4c5f5c17170a926bd79781807422698c22b26cf7afc60430b2a7183d92'}


def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    assert not OUT.exists() and not RECEIPT.exists()
    assert meta(ZIP.read_bytes()) == EXPECTED
    OUT.mkdir()
    rows, findings = [], []
    with zipfile.ZipFile(ZIP) as archive:
        assert len(archive.infolist()) == 952
        assert len({entry.filename for entry in archive.infolist()}) == 952
        for entry in archive.infolist():
            relative = PurePosixPath(entry.filename)
            assert not relative.is_absolute() and '..' not in relative.parts and not entry.is_dir()
            assert not stat.S_ISLNK(entry.external_attr >> 16)
            data = archive.read(entry)
            target = OUT / entry.filename
            assert target.resolve().is_relative_to(OUT.resolve())
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as stream:
                stream.write(data)
            assert meta(target.read_bytes()) == meta(data)
            rows.append({'path': entry.filename, **meta(data)})
            if any(marker in data for marker in (b'-----BEGIN PRIVATE KEY-----', b'-----BEGIN RSA PRIVATE KEY-----',
                                                 b'-----BEGIN OPENSSH PRIVATE KEY-----')):
                findings.append({'path': entry.filename, 'kind': 'private-key-header'})
            if relative.name in ('adbkey', 'adbkey.pub'):
                findings.append({'path': entry.filename, 'kind': 'adb-key-file'})
    result = {'schema': 1, 'run_id': 38212813248, 'head_sha': '3edcddd86660ea10c8aff71b651b446f86412525',
              'job_id': 114690610883, 'artifact_id': 11730023332,
              'artifact_name': 'editor-normal-animation-3edcddd86660ea10c8aff71b651b446f86412525',
              'download_observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'archive_file': ZIP.name, 'archive': EXPECTED, 'github_digest_matches': True,
              'member_count': len(rows), 'expanded_bytes': sum(row['bytes'] for row in rows),
              'all_extracted_bytes_reverified': True, 'artifact_transformations': [],
              'raw_key_scan_findings': findings, 'files': rows}
    with RECEIPT.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'receipt': str(RECEIPT), 'member_count': len(rows), 'expanded_bytes': result['expanded_bytes'],
                      'archive': EXPECTED, 'raw_key_scan_findings': findings}, indent=2))


if __name__ == '__main__':
    main()
