#!/usr/bin/env python3
"""Read only exact small parent blobs; inventory APK parts without copying them."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path('/dev/shm/day-numeric-art-workflow-01')
GIT = Path('/dev/shm/macrodroid-transfer-space-20261012/verification.git')
COMMIT = 'fc825ede39a40249e33c8ba75b93128a98bd5e3c'
SMALL = [
    '.github/workflows/widget-method-probe.yml',
    'scripts/assemble_artifact.py',
    'tools/android/bootstrap_android_runtime.py',
    'tools/android/android-toolchain-pins.json',
    'tools/android/android_runtime_service.py',
    'tools/android/runtime_job.py',
    'tools/android/wait_android_ready.py',
    'tools/android/test_download_retry.py',
    'vendor/original/manifest.json',
    'work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json',
]


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def main():
    folder = ROOT / 'reports/parent-inputs-01'
    folder.mkdir(parents=True, exist_ok=False)
    output = ROOT / 'inputs/parent'
    output.mkdir(parents=True, exist_ok=False)
    rows, commands = [], []
    result = {'started_utc': datetime.now(timezone.utc).isoformat(), 'passed': False,
              'commit': COMMIT, 'apk_payloads_copied': False,
              'android_executed': False, 'application_build_executed': False}
    def git(args):
        argv = ['git', '--git-dir=' + str(GIT), *args]
        value = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        commands.append({'argv': argv, 'returncode': value.returncode,
            'stdout_bytes': len(value.stdout), 'stdout_sha256': hashlib.sha256(value.stdout).hexdigest(),
            'stderr': value.stderr.decode('utf-8', errors='strict'), 'timeout_seconds': 30})
        if value.returncode:
            raise ValueError('Fetched Git read failed')
        return value.stdout
    def meta(name):
        line = git(['ls-tree', COMMIT, '--', name]).decode().rstrip('\n')
        header, actual_name = line.split('\t')
        mode, kind, oid = header.split()
        if actual_name != name or kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Unexpected pinned parent mode/path')
        return mode, oid
    try:
        for name in SMALL:
            mode, oid = meta(name)
            raw = git(['cat-file', 'blob', oid])
            if hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() != oid:
                raise ValueError('Fetched blob does not match object identity')
            path = output / name
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as stream:
                stream.write(raw)
            path.chmod(0o755 if mode == '100755' else 0o644)
            rows.append({'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                         'mode': mode, 'git_blob_sha1': oid, 'role': 'retained-parent-source'})
        for name in SMALL[-2:]:
            manifest = json.loads((output / name).read_bytes())
            if len(manifest['parts']) != 12:
                raise ValueError('Exactly twelve frozen APK parts required')
            for part in manifest['parts']:
                mode, oid = meta(part['path'])
                if oid != part['git_blob_sha1']:
                    raise ValueError('Manifest part Git identity differs from pinned commit')
                rows.append({'path': part['path'], 'bytes': part['size_bytes'],
                    'sha256': part['sha256'], 'mode': mode, 'git_blob_sha1': oid,
                    'role': 'apk-part-not-copied', 'manifest': name})
        if len(rows) != 34 or len({r['path'] for r in rows}) != 34:
            raise ValueError('Complete parent role count differs')
        result.update(passed=True, status='PINNED_PARENT_SOURCE_AND_PART_METADATA_COLLECTED',
                      small_blobs_verified=10, part_metadata_checked=24, rows=rows)
    except Exception as error:
        result.update(status='PARENT_INPUT_COLLECTION_FAILED', reason=repr(error))
    finally:
        result.update(finished_utc=datetime.now(timezone.utc).isoformat(), commands=commands)
        save(folder / 'result.json', result)
        print(json.dumps({k:v for k,v in result.items() if k not in ('commands','rows')}, indent=2))
    if not result['passed']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
