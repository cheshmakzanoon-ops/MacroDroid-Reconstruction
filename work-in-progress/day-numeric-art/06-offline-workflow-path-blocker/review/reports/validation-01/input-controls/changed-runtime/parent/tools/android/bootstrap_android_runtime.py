#!/usr/bin/env python3
"""Install the pinned Linux x86_64 JDK and Android runtime from official archives.

Requires Python 3.12+, curl, and enough disk for the archives and extracted SDK.
Existing matching installations are reused. Downloads are integrity checked
against the adjacent published package metadata before extraction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import stat
import subprocess
import tarfile
import time
import zipfile


def properties(path: Path) -> dict[str, str]:
    return dict(line.split('=', 1) for line in path.read_text().splitlines()
                if line and not line.startswith('#') and '=' in line)


def installed(package: dict, root: Path) -> bool:
    expected = root / package['installed_marker']
    if not expected.exists():
        return False
    if package['id'] == 'jdk21':
        return package['version'] in properties(expected).get('JAVA_VERSION', '')
    return properties(expected).get('Pkg.Revision') == package['version']


def safe_zip_extract(archive: Path, destination: Path) -> None:
    destination = destination.resolve()
    with zipfile.ZipFile(archive) as source:
        for item in source.infolist():
            target = (destination / item.filename).resolve()
            if not target.is_relative_to(destination):
                raise ValueError('Archive member escapes its installation directory')
            mode = item.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise ValueError('Unexpected symbolic link in pinned Android ZIP')
            source.extract(item, destination)
            if mode & 0o777:
                target.chmod(mode & 0o777)


def download_verified(package: dict, archive: Path) -> None:
    """Retry interrupted GETs, never accept partial or unverified archive bytes.

    Explicit HTTP/1.1 avoids the observed HTTP/2 stream-92 failure. Each retry
    starts a new file; certificate/HTTP failures and integrity errors fail closed.
    """
    if not package['url'].startswith('https://'):
        raise ValueError('Pinned downloads must use HTTPS')
    partial = archive.with_suffix(archive.suffix + '.partial')
    transient = {5, 6, 7, 18, 28, 35, 52, 55, 56, 92}
    try:
        for attempt in range(1, 4):
            partial.unlink(missing_ok=True)
            command = ['curl', '-fL', '--http1.1', '--proto', '=https',
                       '--proto-redir', '=https', '--connect-timeout', '10',
                       '--max-time', '600', '--speed-limit', '1024', '--speed-time', '30',
                       '-sS', package['url'], '-o', str(partial)]
            print('Download attempt', attempt, 'of 3:', package['id'], flush=True)
            try:
                subprocess.run(command, check=True, timeout=625)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
                retryable = isinstance(error, subprocess.TimeoutExpired) or error.returncode in transient
                if not retryable or attempt == 3:
                    raise
                time.sleep(attempt * 2)
                continue
            with partial.open('rb') as stream:
                digest = hashlib.file_digest(stream, package['checksum_algorithm']).hexdigest()
            if partial.stat().st_size != package['download_bytes'] or digest != package['checksum']:
                raise ValueError('Downloaded bytes do not match the package pin: ' + package['id'])
            partial.replace(archive)
            return
    finally:
        partial.unlink(missing_ok=True)


def install(package: dict, root: Path, downloads: Path) -> None:
    if installed(package, root):
        print('Reuse', package['id'], package['version'], flush=True)
        return
    archive = downloads / package['filename']
    downloads.mkdir(parents=True, exist_ok=True)
    if not archive.exists():
        download_verified(package, archive)
    with archive.open('rb') as stream:
        digest = hashlib.file_digest(stream, package['checksum_algorithm']).hexdigest()
    if archive.stat().st_size != package['download_bytes'] or digest != package['checksum']:
        raise ValueError(f"Checksum or size mismatch for {archive}; refusing extraction")
    print('Verified', package['id'], package['checksum_algorithm'], digest, flush=True)
    destination = root / package['extract_destination']
    if package['format'] == 'tar.gz':
        if destination.exists():
            raise FileExistsError(f'Refusing to overwrite an unmatched installation: {destination}')
        staging = root / ('.extract-' + package['id'])
        staging.mkdir()
        with tarfile.open(archive, 'r:gz') as source:
            source.extractall(staging, filter='data')
        children = list(staging.iterdir())
        if len(children) != 1 or not (children[0] / 'bin/javac').is_file():
            raise ValueError('Unexpected JDK archive structure')
        children[0].rename(destination)
        staging.rmdir()
    else:
        existing_tree = root / package['installed_tree']
        if existing_tree.exists():
            raise FileExistsError(f'Refusing to overwrite an unmatched installation: {existing_tree}')
        destination.mkdir(parents=True, exist_ok=True)
        safe_zip_extract(archive, destination)
    if not installed(package, root):
        raise RuntimeError('Installed version metadata does not match pin: ' + package['id'])
    print('Installed', package['id'], flush=True)


def create_avd(root: Path) -> None:
    name = 'MacroDroid_API35_Disposable'
    avds = root / 'android-user/avd'
    avds.mkdir(parents=True, exist_ok=True)
    avd = avds / (name + '.avd')
    if avd.exists():
        print('Reuse existing disposable AVD without changing its data:', avd)
        return
    avd.mkdir()
    values = {
        'avd.ini.encoding': 'UTF-8', 'AvdId': name,
        'avd.ini.displayname': 'MacroDroid API35 Disposable',
        'abi.type': 'x86_64', 'hw.cpu.arch': 'x86_64', 'hw.cpu.ncore': '2',
        'hw.ramSize': '3072', 'hw.lcd.width': '720', 'hw.lcd.height': '1280',
        'hw.lcd.density': '320', 'hw.keyboard': 'yes', 'hw.mainKeys': 'no',
        'hw.gpu.enabled': 'yes', 'hw.gpu.mode': 'swiftshader',
        'hw.camera.back': 'none', 'hw.camera.front': 'none',
        'hw.audioInput': 'no', 'hw.audioOutput': 'no', 'hw.gps': 'yes',
        'hw.sdCard': 'no', 'showDeviceFrame': 'no',
        'disk.dataPartition.size': '3G',
        'image.sysdir.1': 'system-images/android-35/google_apis/x86_64/',
        'tag.id': 'google_apis', 'tag.display': 'Google APIs',
        'PlayStore.enabled': 'false', 'fastboot.forceColdBoot': 'yes',
        'fastboot.forceFastBoot': 'no', 'skin.name': '720x1280',
        'skin.path': '_no_skin', 'runtime.network.latency': 'none',
        'runtime.network.speed': 'full', 'vm.heapSize': '256',
    }
    (avd / 'config.ini').write_text(''.join(k + '=' + v + '\n' for k, v in values.items()))
    (avds / (name + '.ini')).write_text('avd.ini.encoding=UTF-8\npath=' + str(avd)
                                      + '\npath.rel=avd/' + name + '.avd\ntarget=android-35\n')
    print('Created disposable AVD:', avd)


def verify(root: Path, packages: list[dict]) -> None:
    for package in packages:
        if not installed(package, root):
            raise RuntimeError('Missing or different pinned installation: ' + package['id'])
    commands = [
        [str(root / 'jdk21/bin/java'), '-version'],
        [str(root / 'jdk21/bin/javac'), '-version'],
        [str(root / 'android/platform-tools/adb'), 'version'],
        [str(root / 'android/emulator/emulator'), '-no-window', '-version'],
    ]
    for command in commands:
        result = subprocess.run(command, capture_output=True, text=True, timeout=15, check=True)
        print((result.stdout + result.stderr).strip())
    props = properties(root / 'android/system-images/android-35/google_apis/x86_64/build.prop')
    for key in ['ro.system.product.cpu.abilist', 'ro.dalvik.vm.native.bridge',
                'ro.enable.native.bridge.exec', 'ro.ndk_translation.version']:
        print(key + '=' + props.get(key, ''))
    if 'arm64-v8a' not in props.get('ro.system.product.cpu.abilist', ''):
        raise RuntimeError('Pinned image does not advertise ARM64 ABI')
    if props.get('ro.dalvik.vm.native.bridge') != 'libndk_translation.so':
        raise RuntimeError('Pinned image does not advertise the expected native bridge')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--create-avd', action='store_true')
    parser.add_argument('--keep-archives', action='store_true')
    args = parser.parse_args()
    if platform.system() != 'Linux' or platform.machine() not in ('x86_64', 'amd64'):
        parser.error('These exact package pins target Linux x86_64')
    pins = json.loads(Path(__file__).with_name('android-toolchain-pins.json').read_text())
    root = args.root.resolve()
    if not args.verify_only:
        if not shutil.which('curl'):
            parser.error('curl is required to download the official packages')
        root.mkdir(parents=True, exist_ok=True)
        downloads = root / 'downloads'
        for package in pins['packages']:
            install(package, root, downloads)
        if not args.keep_archives and downloads.exists():
            for package in pins['packages']:
                archive = downloads / package['filename']
                if archive.exists():
                    archive.unlink()
    verify(root, pins['packages'])
    if args.create_avd:
        create_avd(root)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

# bounded offline identity fault
