#!/usr/bin/env python3
"""Prepare a private copy of the frozen thirteen-screen guard, without an APK copy."""
from pathlib import Path
import datetime
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'day-time-trigger-forward/checkpoints/02-host-success'
PARENT_SHA = '0e010cfbace03cffa6d45e8c9157402b1b68c9a392249eb2aeae39445dc57a7d'
STAGE = ROOT / 'stage-01'


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    if STAGE.exists():
        raise RuntimeError('Private stage already exists')
    if identity(PARENT / 'checkpoint.json')['sha256'] != PARENT_SHA:
        raise RuntimeError('Frozen parent checkpoint changed')
    checkpoint = json.loads((PARENT / 'checkpoint.json').read_text())
    STAGE.mkdir(parents=True)
    before = {}
    for row in checkpoint['files']:
        if not row['path'].startswith('replay-source/'):
            continue
        name = row['path'][len('replay-source/'):]
        source = PARENT / row['path']
        pin = {key: row[key] for key in ('bytes', 'sha256')}
        if identity(source) != pin:
            raise RuntimeError('Frozen source changed: ' + name)
        target = STAGE / 'repository' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(source.read_bytes())
        os.chmod(target, source.stat().st_mode & 0o777)
        if identity(target) != pin:
            raise RuntimeError('Private copy differs: ' + name)
        before[name] = pin
    external = {}
    for run, size, digest in [
        ('38198783416', 3892915, 'abf947195917bb8f090cee7ae2eff250963c8d0ddd5d5663d7b76103a850c46e'),
        ('38202401351', 6517530, 'fa2eca5f893ae181b91aa7a7bf5df8320620bbc8da21b87eacffb1de0c3bc7ee'),
    ]:
        name = f'docs/verification/editor-journey/run-{run}-attempt-1/evidence.zip'
        source = ROOT.parent / 'day-time-trigger-forward/stage-02/repository' / name
        pin = {'bytes': size, 'sha256': digest}
        if identity(source) != pin:
            raise RuntimeError('Historical ZIP differs: ' + name)
        target = STAGE / 'repository' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(source, target)
        before[name] = pin
        external[name] = {'source': str(source), **pin, 'read_only_hardlink': True}
    (STAGE / 'parent-checkpoint.json').write_bytes((PARENT / 'checkpoint.json').read_bytes())
    (STAGE / 'parent-source-identities.json').write_text(json.dumps(before, indent=2) + '\n')
    result = {'status': 'PRIVATE_STAGE_PREPARED', 'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'parent_checkpoint_sha256': PARENT_SHA, 'source_files': len(before),
              'external_historical_archives': external, 'active_changes': False, 'android_executed': False}
    (STAGE / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
