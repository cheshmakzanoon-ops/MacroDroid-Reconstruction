import hashlib, json, os
from pathlib import Path
root = Path(os.environ['RUNNER_TEMP']) / 'indicator-tooling'
output = Path('ci-indicator/toolchain')
output.mkdir()
metadata = ['jdk21/release', 'android/platform-tools/source.properties',
    'android/emulator/source.properties',
    'android/system-images/android-35/google_apis/x86_64/source.properties',
    'android/system-images/android-35/google_apis/x86_64/build.prop',
    'android-user/avd/MacroDroid_API35_Disposable.ini',
    'android-user/avd/MacroDroid_API35_Disposable.avd/config.ini']
binaries = ['jdk21/bin/java', 'jdk21/bin/javac', 'android/platform-tools/adb',
    'android/emulator/emulator', 'android/emulator/qemu/linux-x86_64/qemu-system-x86_64-headless']
rows = []
for name in metadata + binaries:
    path = root / name
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    rows.append({'path': name, 'bytes': path.stat().st_size, 'sha256': digest})
    if name in metadata:
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(path.read_bytes())
(output / 'installed-inputs.json').write_text(json.dumps(rows, indent=2) + '\n')
print(json.dumps(rows, indent=2))
