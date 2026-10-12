#!/usr/bin/env python3
"""Create only the owned small implementation inputs from the approved design."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
DESIGN = Path('/dev/shm/ink-indicator-fixed-sampling-design')
GIT = Path('/dev/shm/macrodroid-transfer-space-20261012/verification.git')
SOURCE = ROOT / 'source/tools/indicator_sampling'


def ident(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)


def main():
    cp = (DESIGN / 'checkpoint.json').read_bytes()
    assert hashlib.sha256(cp).hexdigest() == 'fccc817be37d821a781348a8870c227ff5471fcdc72d71f38a81bc062c7a3eec'
    design = json.loads(cp)
    for row in design['files']:
        assert ident((DESIGN / row['path']).read_bytes()) == {k: row[k] for k in ['bytes', 'sha256']}
    parents = json.loads((DESIGN / 'evidence/parent-bindings.json').read_bytes())
    assert len(parents['files']) == 16
    for row in parents['files']:
        command = ['git', '--git-dir=' + str(GIT), 'show', row['commit'] + ':' + row['path']]
        process = subprocess.run(command, capture_output=True, check=True, timeout=15)
        assert not process.stderr
        assert ident(process.stdout) == {k: row[k] for k in ['bytes', 'sha256']}
        write(ROOT / 'parent-inputs' / row['path'], process.stdout)
    aapt_source = Path('/workspace/scratch/4130730d15aa/current/MacroDroid_v9/tools/prebuilt/linux/aapt2')
    aapt = aapt_source.read_bytes()
    expected_aapt = {'bytes': 6135688, 'sha256': '6fbed5edaddcfbee99a3ae6e7208c8654c6cb2bedb4ed5cbbf4e154d7d38a745'}
    assert ident(aapt) == expected_aapt
    write(SOURCE / 'aapt2', aapt)
    (SOURCE / 'aapt2').chmod(0o755)
    protocol = json.loads((DESIGN / 'protocol.json').read_bytes())
    protocol['kind'] = 'FIXED_INDICATOR_DIAGNOSTIC_V1'
    del protocol['android_execution_authorized_by_this_capsule']
    del protocol['active_files']
    write(SOURCE / 'protocol.json', json.dumps(protocol, indent=2).encode() + b'\n')
    pins = {
        'schema': 1, 'parent_commit': parents['fetched_git_commit'],
        'design_checkpoint_sha256': hashlib.sha256(cp).hexdigest(),
        'parents': [{k: row[k] for k in ['path', 'bytes', 'sha256', 'mode']} for row in parents['files']],
        'aapt2': expected_aapt,
        'aapt2_extra_dependency_approved_by_root': True,
        'protocol': ident((SOURCE / 'protocol.json').read_bytes()),
    }
    write(SOURCE / 'pins.json', json.dumps(pins, indent=2).encode() + b'\n')
    for path in sorted((DESIGN / 'evidence/observed-xml').glob('*.xml')):
        write(SOURCE / 'fixtures' / path.name, path.read_bytes())
    write(ROOT / 'source-input-binding.json', json.dumps({
        'status': 'APPROVED_DESIGN_AND_PARENT_INPUTS_COPIED',
        'design_checkpoint': {'path': str(DESIGN / 'checkpoint.json'), **ident(cp)},
        'parent_files': 16, 'parent_commit': parents['fetched_git_commit'],
        'aapt2_source': {'path': str(aapt_source), **expected_aapt},
        'source_or_apk_mutated': False, 'android_executed': False,
    }, indent=2).encode() + b'\n')
    assert ident(aapt_source.read_bytes()) == expected_aapt
    print(json.dumps({'status': 'APPROVED_DESIGN_AND_PARENT_INPUTS_COPIED', 'parent_files': 16,
                      'aapt2_extra_bytes': len(aapt), 'no_apks_copied': True}))


if __name__ == '__main__':
    main()
