#!/usr/bin/env python3
"""Read exact published Git objects into an owned, APK-free literal checkout."""
from pathlib import Path
import hashlib
import json
import runpy
import subprocess
import time

ROOT = Path(__file__).resolve().parent
BARE = Path('/dev/shm/macrodroid-transfer-space-20261012/verification.git')
COMMIT = 'fc825ede39a40249e33c8ba75b93128a98bd5e3c'
OUTPUT = ROOT / 'inputs/checkout'
PROOF = ROOT / 'reports/checkout-01'
OUTPUT.mkdir(exist_ok=False)
PROOF.mkdir(exist_ok=False)
source = ROOT / 'source-02/prepare_trigger_journey.py'
source_before = hashlib.sha256(source.read_bytes()).hexdigest()
module = runpy.run_path(str(source))
commands = []


def git(args):
    started = time.monotonic_ns()
    command = ['git', '--git-dir=' + str(BARE), *args]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
    number = len(commands)
    (PROOF / ('command-%03d.stderr' % number)).write_bytes(result.stderr)
    commands.append({'argv': command, 'exit_code': result.returncode,
        'timeout_seconds': 15, 'started_monotonic_ns': started, 'finished_monotonic_ns': time.monotonic_ns(),
        'stdout_bytes': len(result.stdout), 'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
        'stderr_file': 'command-%03d.stderr' % number})
    return result


def blob(name):
    result = git(['show', COMMIT + ':' + name])
    if result.returncode:
        raise RuntimeError('Required published blob unavailable: ' + name)
    return result.stdout


try:
    pins = module['PINS']
    required = {name: {'sha256': digest} for name, digest in pins.items()}
    early = {}
    for prefix in [module['GUARD'], module['ANIMATION']]:
        name = prefix + '/checkpoint.json'
        raw = blob(name)
        early[name] = raw
        if hashlib.sha256(raw).hexdigest() != pins[name]:
            raise ValueError('Published checkpoint differs: ' + name)
        checkpoint = json.loads(raw)
        for row in checkpoint['files']:
            relative = prefix + '/' + row['path']
            if relative != module['GUARD_ARCHIVE']:
                required[relative] = {key: row[key] for key in ('bytes', 'sha256')}
    name = module['GUARD'] + '/reports/inputs-before.json'
    early[name] = blob(name)
    if hashlib.sha256(early[name]).hexdigest() != required[name]['sha256']:
        raise ValueError('Pinned original host-fixture input inventory differs')
    for name, row in json.loads(early[name]).items():
        if name.endswith('/evidence.zip'):
            required[name] = {key: row[key] for key in ('bytes', 'sha256')}
    listing = git(['ls-tree', '-z', COMMIT, '--', *sorted(required), module['GUARD_ARCHIVE']])
    if listing.returncode:
        raise ValueError('Could not read published input modes')
    (PROOF / 'git-tree-entries.raw').write_bytes(listing.stdout)
    modes = {}
    for item in listing.stdout.split(b'\0'):
        if not item:
            continue
        meta, raw_name = item.split(b'\t', 1)
        mode, kind, digest = meta.decode().split()
        name = raw_name.decode()
        if kind != 'blob' or mode not in ('100644', '100755') or name in modes:
            raise ValueError('Unexpected published input mode: ' + name)
        modes[name] = (mode, digest)
    if set(modes) != set(required):
        raise ValueError('Literal checkout membership differs; logical archive must be absent')
    rows = []
    for name in sorted(required):
        raw = early[name] if name in early else blob(name)
        actual = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        if any(actual[key] != value for key, value in required[name].items()):
            raise ValueError('Published input identity differs: ' + name)
        mode, oid = modes[name]
        if hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() != oid:
            raise ValueError('Published Git object identity differs')
        path = OUTPUT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(raw)
        path.chmod(0o755 if mode == '100755' else 0o644)
        if hashlib.sha256(path.read_bytes()).hexdigest() != actual['sha256']:
            raise ValueError('Literal checkout write differs')
        rows.append({'path': name, **actual, 'mode': mode, 'git_blob_sha1': oid})
    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_before
    assert not (OUTPUT / module['GUARD_ARCHIVE']).exists()
    result = {'status': 'EXACT_PUBLISHED_MULTIPART_CHECKOUT_MATERIALIZED_WITHOUT_LOGICAL_ARCHIVE',
        'commit': COMMIT, 'source_preparer_sha256': source_before,
        'logical_archive_absent': True, 'apk_payloads_copied': False,
        'files': rows, 'file_count': len(rows), 'bytes': sum(row['bytes'] for row in rows),
        'android_executed': False}
except Exception as error:
    result = {'status': 'CHECKOUT_MATERIALIZATION_FAILED', 'reason': type(error).__name__ + ': ' + str(error),
              'android_executed': False}
    raise
finally:
    (PROOF / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
    (PROOF / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({key: value for key, value in result.items() if key != 'files'}, indent=2))
