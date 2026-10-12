"""Retire one explicitly authorized, stopped, generated local AVD directory.

This one-use receipt script never changes SDK/JDK, installers, source, APKs,
reports, or another AVD. It records physical /proc PIDs, exact target contents,
preserves small configuration files, and checks retained-file content hashes.
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
OUTPUT = Path(__file__).resolve().parent


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(name, value):
    path = OUTPUT / name
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def proc_guard():
    """Read host /proc; inspect actual executable identities, not ps text matches."""
    result = {'recorded_utc': now(), 'reader_physical_pid': os.getpid(),
              'processes': [], 'vanished_during_read': [], 'blocking_processes': []}
    for directory in sorted(Path('/proc').iterdir(), key=lambda x: int(x.name) if x.name.isdecimal() else -1):
        if not directory.name.isdecimal():
            continue
        try:
            comm = (directory / 'comm').read_text().strip()
            cmdline = (directory / 'cmdline').read_bytes().split(b'\0')
            argv = [item.decode('utf-8', 'replace') for item in cmdline if item]
            status = (directory / 'status').read_text().splitlines()
            namespace_pids = next((line.split()[1:] for line in status if line.startswith('NSpid:')), [])
            try:
                executable = os.readlink(directory / 'exe')
            except FileNotFoundError:
                executable = None
        except FileNotFoundError:
            result['vanished_during_read'].append(int(directory.name))
            continue
        names = [comm, Path(executable).name if executable else '', Path(argv[0]).name if argv else '']
        emulator = any(name == 'emulator' or name.startswith(('qemu-system', 'qemu-kvm', 'emulator64')) for name in names)
        # Preserve only runtime-related argv; unrelated processes may carry user data.
        runtime = emulator or any(name in ('adb', 'netsimd') for name in names)
        row = {'physical_pid': int(directory.name), 'comm': comm, 'namespace_pids': namespace_pids,
               'executable': executable, 'runtime_process': runtime}
        if runtime:
            row['argv'] = argv
        result['processes'].append(row)
        if emulator:
            result['blocking_processes'].append(row)
    if result['blocking_processes']:
        raise RuntimeError('A live emulator/QEMU process exists; preserve the AVD and stop.')
    return result


def inventory():
    rows = []
    for path in sorted(TARGET.rglob('*')):
        info = path.lstat()
        row = {'path': str(path.relative_to(TARGET)), 'mode': stat.S_IMODE(info.st_mode),
               'bytes': info.st_size, 'allocated_bytes': info.st_blocks * 512,
               'device': info.st_dev, 'inode': info.st_ino, 'mtime_ns': info.st_mtime_ns}
        if stat.S_ISREG(info.st_mode):
            row.update(kind='file', sha256=digest(path))
        elif stat.S_ISDIR(info.st_mode):
            row.update(kind='directory')
        else:
            raise RuntimeError('Unexpected link or special file in the target: ' + str(path))
        rows.append(row)
    return rows


def retained_controls():
    paths = list((BASE / 'tooling/android-downloads').glob('*'))
    paths += list((BASE / 'tooling').glob('OpenJDK*.tar.gz'))
    paths += [BASE / value for value in (
        'tooling/jdk21/bin/java', 'tooling/jdk21/bin/javac', 'tooling/jdk21/release',
        'tooling/android/platform-tools/adb', 'tooling/android/emulator/emulator',
        'tooling/android/system-images/android-35/google_apis/x86_64/source.properties',
        'tooling/android-install-manifest.json', 'tooling/jdk21-install.json',
        'tooling/android-user/avd/MacroDroid_API35_Disposable.ini',
        'tooling-validation/android-toolchain-pins.json',
        'tooling-validation/local-framework-watchdog-result.json',
        'tooling-validation/local-framework-watchdog.log',
        'tooling-validation/local-runtime-stop.json',
        'current/MacroDroid_v9/android_acceptance.py',
        'current/MacroDroid_v9/android_compare.py',
    )]
    paths += list((BASE / 'current/MacroDroid_v9/dist').glob('*.apk'))
    result = []
    for path in sorted(set(paths)):
        if not path.is_file():
            raise RuntimeError('Retained control file is absent: ' + str(path))
        result.append({'path': str(path.relative_to(BASE)), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return result


def main():
    if TARGET.is_symlink() or TARGET.resolve() != TARGET or not TARGET.is_dir():
        raise RuntimeError('Exact authorized target is absent, redirected, or not a directory')
    if (OUTPUT / 'receipt.json').exists():
        raise RuntimeError('This retirement has already been recorded')
    started = now()
    before_disk = shutil.disk_usage(BASE)._asdict()
    first_guard = proc_guard()
    write('process-guard-before-inventory.json', first_guard)
    before = inventory()
    write('target-inventory-before.json', before)
    controls_before = retained_controls()
    write('retained-controls-before.json', controls_before)
    keep = []
    for row in before:
        path = TARGET / row['path']
        if row['kind'] == 'file' and path.suffix in ('.ini', '.txt', '.json', '.xml', '.cache') and row['bytes'] <= 256 * 1024:
            dest = OUTPUT / 'preserved-metadata' / row['path']
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dest)
            if digest(dest) != row['sha256']:
                raise RuntimeError('Configuration copy did not reproduce its original hash')
            keep.append({'original': row['path'], 'copy': str(dest.relative_to(OUTPUT)),
                         'bytes': row['bytes'], 'sha256': row['sha256']})
    # Re-read complete content inventory and physical process list immediately
    # before deletion. Any observed regeneration or live emulator aborts deletion.
    if inventory() != before:
        raise RuntimeError('Generated AVD changed during the retirement guard')
    final_guard = proc_guard()
    write('process-guard-before-removal.json', final_guard)
    print(json.dumps({'event': 'authorized_target_guarded', 'files': sum(row['kind'] == 'file' for row in before),
                      'target_allocated_bytes': sum(row['allocated_bytes'] for row in before), 'metadata_files_copied': len(keep)}), flush=True)
    shutil.rmtree(TARGET)
    if TARGET.exists() or TARGET.is_symlink():
        raise RuntimeError('Authorized target unexpectedly remains')
    controls_after = retained_controls()
    write('retained-controls-after.json', controls_after)
    if controls_before != controls_after:
        raise RuntimeError('A retained control file changed during cleanup; preserve evidence')
    for row in keep:
        if digest(OUTPUT / row['copy']) != row['sha256']:
            raise RuntimeError('Preserved metadata changed')
    receipt = {'schema': 1, 'status': 'RETIRED_CLOSED_GENERATED_AVD', 'started_utc': started,
               'finished_utc': now(), 'target': str(TARGET), 'target_absent_after': True,
               'authorization': 'Parent /root explicitly authorized retirement of only this stopped disposable generated AVD directory.',
               'prior_stop_evidence': 'docs/verification/android-environment/local-runtime-stop.json',
               'prior_failure_evidence': 'docs/verification/android-environment/local-framework-watchdog-result.json',
               'physical_proc_guards': 2, 'observed_live_emulator_processes': 0,
               'target_entries': len(before), 'target_files': sum(row['kind'] == 'file' for row in before),
               'target_allocated_bytes_before': sum(row['allocated_bytes'] for row in before),
               'target_logical_file_bytes_before': sum(row['bytes'] for row in before if row['kind'] == 'file'),
               'preserved_metadata': keep, 'retained_control_files': len(controls_before),
               'retained_controls_before_after_exact': True,
               'disk_before': before_disk, 'disk_after': shutil.disk_usage(BASE)._asdict(),
               'scope': 'Only the exact generated AVD directory was removed. SDK/JDK, pinned installers, other AVDs, source, APKs, reports and all /tmp build caches were outside the deletion scope. Retained controls are the explicitly listed content samples, not a claim that every workspace file was hashed.'}
    write('receipt.json', receipt)
    print(json.dumps(receipt, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
