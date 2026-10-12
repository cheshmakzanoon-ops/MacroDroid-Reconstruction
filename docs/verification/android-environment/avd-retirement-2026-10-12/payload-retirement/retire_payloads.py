"""Retire only five authorized hash-matched generated AVD disk payloads.

Keep every pathname present as an empty retirement placeholder. Never mutate a
linked inode in place, or change installed tools, source, reports or metadata.
"""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat

BASE = Path('/workspace/scratch/4130730d15aa')
TARGET = BASE / 'tooling/android-user/avd/MacroDroid_API35_Disposable.avd'
OUT = Path(__file__).resolve().parent
PRIOR = BASE / 'tooling-validation/avd-retirement-2026-10-12'
NAMES = ('cache.img', 'encryptionkey.img', 'encryptionkey.img.qcow2',
         'userdata-qemu.img', 'userdata-qemu.img.qcow2')


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def inventory():
    rows = []
    for path in sorted(TARGET.rglob('*')):
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) and not stat.S_ISDIR(info.st_mode):
            raise RuntimeError('Unexpected redirected/special generated file: ' + str(path))
        row = {'path': path.relative_to(TARGET).as_posix(), 'bytes': info.st_size,
               'allocated_bytes': info.st_blocks * 512, 'mode': stat.S_IMODE(info.st_mode),
               'device': info.st_dev, 'inode': info.st_ino, 'kind': 'file' if path.is_file() else 'directory'}
        if row['kind'] == 'file':
            row['sha256'] = sha(path)
        rows.append(row)
    return rows


def guard():
    physical = int(os.readlink('/proc/self'))
    rows = []
    for directory in sorted(Path('/proc').iterdir(), key=lambda p: int(p.name) if p.name.isdecimal() else -1):
        if not directory.name.isdecimal():
            continue
        try:
            comm = (directory / 'comm').read_text().strip()
            raw = (directory / 'cmdline').read_bytes()
            args = [item.decode('utf-8', 'replace') for item in raw.split(b'\0') if item]
        except FileNotFoundError:
            continue
        names = [comm, Path(args[0]).name if args else '']
        runtime = any(name == 'emulator' or name.startswith(('qemu-system', 'qemu-kvm', 'emulator64')) for name in names)
        rows.append({'physical_pid': int(directory.name), 'comm': comm,
                     'argv_executable': args[0] if args else None, 'emulator_or_qemu': runtime})
    if any(row['emulator_or_qemu'] for row in rows):
        raise RuntimeError('A local emulator or QEMU process is live')
    return {'observed_utc': now(), 'reader_namespace_pid': os.getpid(), 'reader_physical_pid': physical,
            'processes': rows, 'visibility_scope': 'All readable physical /proc comm and cmdline executable identities; other-process cwd/fd/exe may be denied. Closure also binds the preserved local runtime stop and watchdog evidence.'}


def controls():
    original = json.loads((PRIOR / 'retained-controls-before.json').read_bytes())
    result = []
    for row in original:
        path = BASE / row['path']
        actual = {'path': row['path'], 'bytes': path.stat().st_size, 'sha256': sha(path)}
        if actual != row:
            raise RuntimeError('A protected earlier control changed: ' + row['path'])
        result.append(actual)
    return result


def main():
    # Refuse before entering the receipt-writing finally block, so an accidental
    # repeat cannot replace a successful receipt with its own rejection record.
    if (OUT / 'receipt.json').exists():
        raise RuntimeError('Refusing to overwrite an existing retirement receipt')
    report = {'schema': 1, 'status': 'AVD_PAYLOAD_RETIREMENT_RUNNING', 'started_utc': now(),
              'target': str(TARGET), 'authorized_payload_names': list(NAMES), 'replaced': [],
              'authorization': 'Parent /root explicitly authorized only previously inventoried, hash-matching large generated AVD disk payloads to become zero-byte placeholders after exact reappearance.',
              'prior_retirement_checkpoint_sha256': sha(PRIOR / 'checkpoint.json'),
              'prior_reappearance_report_sha256': sha(BASE / 'tooling-validation/avd-reappearance-2026-10-12/reappearance.json'),
              'local_closure_evidence': ['docs/verification/android-environment/local-runtime-stop.json',
                                       'docs/verification/android-environment/local-framework-watchdog-result.json'],
              'disk_before': shutil.disk_usage(BASE)._asdict()}
    try:
        if TARGET.is_symlink() or TARGET.resolve() != TARGET or not TARGET.is_dir():
            raise RuntimeError('Exact generated AVD root is absent or redirected')
        save('process-guard-before.json', guard())
        expected_rows = json.loads((PRIOR / 'target-inventory-before.json').read_bytes())
        expected = {row['path']: (row['bytes'], row['sha256']) for row in expected_rows if row['kind'] == 'file'}
        before = inventory()
        actual = {row['path']: (row['bytes'], row['sha256']) for row in before if row['kind'] == 'file'}
        if actual != expected:
            raise RuntimeError('Reappeared AVD regular files do not exactly match the retired inventory')
        save('target-before.json', before)
        protected = controls()
        save('retained-controls-before.json', protected)
        selected = {row['path']: row for row in before if row['path'] in NAMES}
        if len(selected) != len(NAMES) or any(row['bytes'] < 1024 * 1024 for row in selected.values()):
            raise RuntimeError('The exact five large generated payloads are not present')
        save('process-guard-before-replacement.json', guard())
        for name in NAMES:
            path = TARGET / name
            info = path.lstat()
            if not stat.S_ISREG(info.st_mode) or (info.st_size, sha(path)) != expected[name]:
                raise RuntimeError('Payload changed before atomic replacement: ' + name)
            temporary = TARGET / (name + '.retirement-' + str(int(os.readlink('/proc/self'))) + '.tmp')
            descriptor = os.open(temporary, os.O_CREAT | os.O_EXCL | os.O_WRONLY, stat.S_IMODE(info.st_mode))
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
            os.replace(temporary, path)
            after = path.stat()
            if after.st_size != 0 or after.st_blocks != 0 or sha(path) != hashlib.sha256(b'').hexdigest():
                raise RuntimeError('Payload was not retired to an empty placeholder: ' + name)
            report['replaced'].append({'path': name, 'original': selected[name],
                                       'after': {'bytes': after.st_size, 'allocated_bytes': after.st_blocks * 512,
                                                 'sha256': sha(path), 'mode': stat.S_IMODE(after.st_mode),
                                                 'device': after.st_dev, 'inode': after.st_ino}})
        after = inventory()
        save('target-after.json', after)
        remaining = {row['path']: (row['bytes'], row['sha256']) for row in after if row['kind'] == 'file'}
        wanted = {name: ((0, hashlib.sha256(b'').hexdigest()) if name in NAMES else identity)
                  for name, identity in expected.items()}
        if remaining != wanted:
            raise RuntimeError('Unexpected AVD metadata, file or placeholder change')
        after_controls = controls()
        save('retained-controls-after.json', after_controls)
        if after_controls != protected:
            raise RuntimeError('A protected control changed during retirement')
        report.update(status='FIVE_GENERATED_AVD_PAYLOADS_RETIRED_TO_EMPTY_PLACEHOLDERS',
                      retained_avd_regular_files=len(expected) - len(NAMES), protected_control_files=len(protected),
                      retained_avd_metadata_and_controls_exact=True, all_original_pathnames_present=True,
                      disk_after=shutil.disk_usage(BASE)._asdict(),
                      scope='Five generated disk payloads only. Small config/log/pstore/modem metadata, initrd, smaller cache overlay and index remain unchanged. No SDK/JDK, installer, APK, source, report, service, permissions or namespace setting is changed. This is a point-in-time check; later synchronization must be observed separately.')
    except Exception as error:
        report.update(status='AVD_PAYLOAD_RETIREMENT_FAILED', reason=type(error).__name__ + ': ' + str(error),
                      disk_after=shutil.disk_usage(BASE)._asdict())
        raise
    finally:
        report['finished_utc'] = now()
        save('receipt.json', report)
        print(json.dumps(report, indent=2, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
