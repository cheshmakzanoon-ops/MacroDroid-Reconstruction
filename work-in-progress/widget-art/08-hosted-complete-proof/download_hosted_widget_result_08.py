#!/usr/bin/env python3
"""Download the exact new Widget artifact and preserve its unmodified safe members.

The first argument is an ephemeral connector download URL. It is used in memory
and is never copied to a report or repository file.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent / 'hosted-run-38209599059'
SIZE = 4780068
SHA = 'ad8b7f1e9e6ecc34c2b32199da0c7d777298a9a2cf8a89a464eff5779d2d1cc5'


def main():
    if len(sys.argv) != 2:
        raise ValueError('Expected the ephemeral download URL')
    archive = ROOT / 'artifact.zip'
    temporary = ROOT / 'artifact.zip.part'
    extracted = ROOT / 'extracted'
    if archive.exists() or temporary.exists() or extracted.exists():
        raise FileExistsError('Fresh archive and extraction paths are required')
    with urllib.request.urlopen(sys.argv[1], timeout=60) as response, temporary.open('xb') as stream:
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            stream.write(block)
    data = temporary.read_bytes()
    if len(data) != SIZE or hashlib.sha256(data).hexdigest() != SHA:
        raise RuntimeError('Downloaded bytes differ from exact GitHub artifact metadata')
    temporary.rename(archive)
    extracted.mkdir()
    files = []
    seen = set()
    with zipfile.ZipFile(archive) as source:
        for member in source.infolist():
            name = member.filename
            relative = PurePosixPath(name)
            if (relative.is_absolute() or '..' in relative.parts or chr(92) in name or
                    not relative.parts or name in seen or stat.S_ISLNK(member.external_attr >> 16)):
                raise RuntimeError('Unsafe or duplicate archive member')
            seen.add(name)
            if member.is_dir():
                continue
            target = extracted / relative
            payload = source.read(member)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as stream:
                stream.write(payload)
            files.append({'path': name, 'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()})
    manifest = {'downloaded_utc': datetime.now(timezone.utc).isoformat(),
        'run_id': 38209599059, 'job_id': 114680586735,
        'head_sha': 'dbbb89cf4ca65edd3d2c2b96151dadf41aaec514', 'artifact_id': 11728337456,
        'archive': {'path': 'artifact.zip', 'bytes': SIZE, 'sha256': SHA},
        'whole_zip_matches_github_digest': True, 'safe_fresh_extraction': True,
        'signed_download_url_persisted': False, 'files': files}
    (ROOT / 'download-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({key: value for key, value in manifest.items() if key != 'files'}, indent=2))
    print('Files:', len(files))


if __name__ == '__main__':
    main()
