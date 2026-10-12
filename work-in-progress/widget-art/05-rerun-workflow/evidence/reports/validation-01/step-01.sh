set -euo pipefail
mkdir ci-widget-method
python3 - <<'PY' 2>&1 | tee ci-widget-method/input-preflight.log
import hashlib, json, os
from pathlib import Path, PurePosixPath
root = Path(os.environ['GITHUB_WORKSPACE']).resolve()
output = Path('ci-widget-method')
probe = 'work-in-progress/widget-art/04-avd-parser-fix'
pins = {
    'scripts/assemble_artifact.py': 'f85a570f864ec2481dd75783b82006129755194c941b54e193c893b7ee17e97c',
    'tools/android/bootstrap_android_runtime.py': '8ae2a365cc5ec5109c76967642d6ee7f6655df96287cf8feb3355444e14e4e36',
    'tools/android/android-toolchain-pins.json': '3ce2078cb52f540fd86ffdccf8577535662fee1c5274f13bcf01d8d15e3bd8b2',
    'tools/android/android_runtime_service.py': '3ac1047b8ff41aba79d1ef335e8eed260067d696460bf8322195631f09dfec57',
    'tools/android/runtime_job.py': '7babd7ebcc35e531b6b0fea9167b3436ff738e43bf0f869b44534573cb849bc8',
    'tools/android/wait_android_ready.py': '72cb3bcd56df72cd901ee724c48a44b0254235e1d7cdda6c991b985e572f34af',
    'tools/android/test_download_retry.py': 'bd5d871951fbf1e5f7aa3093c8c155b1c599d84ae008b90e1eda53bf3a60948a',
    'vendor/original/manifest.json': 'b2f12b669ac0e937198216458410aaab03da6682659d6d922c730a175b77d684',
    'work-in-progress/widget-update/06-initial-signed-failure/apk/manifest.json': 'e0735120e642c1f0ca849a52c3f0f5127c93313457e39d854fad480bc8ef112c',
    probe + '/checkpoint.json': '3f1126ec9ee00af1f8b2ca3bcbdb36cbfee1545b229a5cb29705d7bfee3e35dc',
}
report = {'scope': 'Exact prepared inputs only; no Android execution in preflight',
          'github_sha': os.environ.get('GITHUB_SHA'), 'passed': False, 'files': []}
def verify(name, expected, expected_bytes=None):
    rel = PurePosixPath(name)
    if rel.is_absolute() or '..' in rel.parts or '\\' in name:
        raise RuntimeError('Unsafe pinned input path')
    path = root / name
    if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root):
        raise RuntimeError('Missing or unsafe pinned file: ' + name)
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    item = {'path': name, 'bytes': len(data), 'sha256': actual, 'expected_sha256': expected}
    report['files'].append(item)
    if actual != expected or expected_bytes is not None and len(data) != expected_bytes:
        raise RuntimeError('Pinned input identity changed: ' + name)
    target = output / 'executed-inputs' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
try:
    for name, expected in pins.items():
        verify(name, expected)
    checkpoint = json.loads((root / probe / 'checkpoint.json').read_text())
    if len(checkpoint['files']) != 8 or len({x['path'] for x in checkpoint['files']}) != 8:
        raise RuntimeError('Reviewed 8-file corrected probe package required')
    for item in checkpoint['files']:
        verify(probe + '/' + item['path'], item['sha256'], item['bytes'])
    expected_apks = {
        'vendor/original/manifest.json': ('MacroDroid-5.67.8-original.apk', 95725918, '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'),
        'work-in-progress/widget-update/06-initial-signed-failure/apk/manifest.json': ('MacroDroid-5.67.8-widget-update-06.apk', 94683439, 'b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f'),
    }
    for name, expected in expected_apks.items():
        value = json.loads((root / name).read_text())
        if (value['filename'], value['size_bytes'], value['sha256']) != expected:
            raise RuntimeError('Wrong original or inactive Widget artifact')
    workflow = root / '.github/workflows/widget-method-probe.yml'
    verify('.github/workflows/widget-method-probe.yml', hashlib.sha256(workflow.read_bytes()).hexdigest())
    report['passed'] = True
except Exception as error:
    report['error'] = type(error).__name__ + ': ' + str(error)
    raise
finally:
    (output / 'input-preflight.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
PY
