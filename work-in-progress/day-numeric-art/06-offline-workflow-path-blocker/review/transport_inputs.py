#!/usr/bin/env python3
"""Record the approved one-copy original-part transport; hardlink existing tmpfs inputs."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat

ROOT = Path('/dev/shm/day-numeric-art-workflow-01')
PARENT = ROOT / 'inputs/parent'
REPOSITORY = Path('/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction')
NUMERIC = Path('/dev/shm/macrodroid-transfer-space-20261012/numeric-success-candidate-capsule/parts')
APK_ORIGINS = [
    (Path('/dev/shm/macrodroid-exact-alarm-navigation/workflow-01-validation/private-inputs/workspace/artifacts/MacroDroid-5.67.8-original.apk'),
     'MacroDroid-5.67.8-original.apk', 95725918, '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'),
    (Path('/dev/shm/macrodroid-exact-alarm-enable-return/numeric-input-01/MacroDroid-5.67.8-day-numeric-0762aad9.apk'),
     'MacroDroid-5.67.8-day-numeric-0762aad9.apk', 94683136, '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd'),
]


def identity(path):
    a = path.lstat()
    if not stat.S_ISREG(a.st_mode):
        raise ValueError('Regular input required')
    with path.open('rb') as stream:
        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    b = path.lstat()
    if (a.st_dev, a.st_ino, a.st_size, a.st_mtime_ns, a.st_ctime_ns, a.st_mode) != (
            b.st_dev, b.st_ino, b.st_size, b.st_mtime_ns, b.st_ctime_ns, b.st_mode):
        raise ValueError('Input changed during transport identity read')
    return {'bytes': b.st_size, 'sha256': sha, 'mode': '100755' if b.st_mode & 0o111 else '100644'}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def main():
    out = ROOT / 'reports/input-transport-01'
    out.mkdir(parents=True, exist_ok=False)
    report = {'started_utc': datetime.now(timezone.utc).isoformat(), 'passed': False,
        'approval_scope': 'One 95,725,918-byte original-part temporary copy required for literal offline parent layout; numeric parts and existing APKs are read-only hardlinks.',
        'part_rows': [], 'apk_rows': [], 'android_executed': False,
        'application_build_executed': False, 'apk_assembled': False,
        'tmpfs_free_before': shutil.disk_usage('/dev/shm').free}
    origins = []
    try:
        if report['tmpfs_free_before'] < 256 * 1024 * 1024:
            raise ValueError('Insufficient bounded tmpfs headroom')
        rows = json.loads((ROOT / 'reports/parent-inputs-01/result.json').read_bytes())['rows']
        copied = 0
        for row in rows:
            if row['role'] != 'apk-part-not-copied':
                continue
            original = row['path'].startswith('vendor/original/')
            source = REPOSITORY / row['path'] if original else NUMERIC / Path(row['path']).name
            before = identity(source)
            if before != {key: row[key] for key in ('bytes','sha256','mode')}:
                raise ValueError('Borrowed immutable part differs: ' + str(source))
            dest = PARENT / row['path']
            dest.parent.mkdir(parents=True, exist_ok=True)
            if original:
                with source.open('rb') as stream, dest.open('xb') as target:
                    shutil.copyfileobj(stream, target, 1024 * 1024)
                dest.chmod(0o755 if before['mode'] == '100755' else 0o644)
                copied += before['bytes']
            else:
                os.link(source, dest, follow_symlinks=False)
            if identity(source) != before or identity(dest) != before:
                raise ValueError('Part transport changed exact bytes or mode')
            same_inode = (source.stat().st_dev, source.stat().st_ino) == (dest.stat().st_dev, dest.stat().st_ino)
            if same_inode is original:
                raise ValueError('Unexpected part transport ownership')
            origins.append((source, before))
            report['part_rows'].append({'source': str(source), 'destination': str(dest), **before,
                'transport': 'one-copy-across-filesystems' if original else 'read-only-hardlink',
                'source_device': source.stat().st_dev, 'destination_device': dest.stat().st_dev,
                'same_inode': same_inode})
        if copied != 95725918 or len(report['part_rows']) != 24:
            raise ValueError('Exact approved transport size/count differs')
        for source, name, size, sha in APK_ORIGINS:
            before = identity(source)
            if (before['bytes'], before['sha256']) != (size, sha):
                raise ValueError('Borrowed fixed APK differs')
            dest = PARENT / 'workspace/artifacts' / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            os.link(source, dest, follow_symlinks=False)
            if identity(source) != before or identity(dest) != before:
                raise ValueError('Borrowed APK hardlink bytes or modes differ')
            origins.append((source, before))
            report['apk_rows'].append({'source': str(source), 'destination': str(dest), **before,
                'same_inode': (source.stat().st_dev, source.stat().st_ino) == (dest.stat().st_dev, dest.stat().st_ino),
                'transport': 'read-only-hardlink; no APK data copy'})
        for path, before in origins:
            if identity(path) != before:
                raise ValueError('Borrowed immutable origin changed')
        report.update(passed=True, status='LITERAL_PARENT_LAYOUT_AND_EXISTING_APK_LINKS_VERIFIED',
                      original_part_bytes_copied=copied, numeric_part_bytes_copied=0,
                      assembled_apk_bytes_copied=0, all_origin_bytes_and_modes_unchanged=True,
                      metadata_note='Hardlink creation changes link-count/ctime metadata; the unchanged claim covers exact file bytes and modes, not those link metadata.')
    except Exception as error:
        report.update(status='INPUT_TRANSPORT_FAILED', reason=repr(error))
    finally:
        report.update(finished_utc=datetime.now(timezone.utc).isoformat(),
                      tmpfs_free_after=shutil.disk_usage('/dev/shm').free)
        save(out / 'result.json', report)
        print(json.dumps({k:v for k,v in report.items() if k not in ('part_rows','apk_rows')}, indent=2))
    if not report['passed']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
