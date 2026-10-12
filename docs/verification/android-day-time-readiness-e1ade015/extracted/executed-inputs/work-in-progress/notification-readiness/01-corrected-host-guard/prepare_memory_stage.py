#!/usr/bin/env python3
"""Preserve an exact small guard stage on separate temporary capacity."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/workspace/scratch/4130730d15aa/notification-readiness-forward/stage-01')
TARGET = ROOT / 'stage-02'


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def inventory(folder):
    return {path.relative_to(folder).as_posix(): identity(path) for path in sorted(folder.rglob('*'))
            if path.is_file() and '__pycache__' not in path.parts and path.suffix not in ('.pyc', '.pyo')}


def main():
    if TARGET.exists():
        raise RuntimeError('Memory stage already exists')
    if shutil.disk_usage(ROOT).free < 64 * 1024 * 1024:
        raise RuntimeError('Insufficient separate temporary capacity')
    before = inventory(SOURCE / 'repository')
    if before['tools/parity_journeys/notification_readiness.py']['sha256'] != 'c61e2d2e3981939d024b70a7442e8b6b0e1e59f80418fa5fc5bffa18b0202f86':
        raise RuntimeError('Reviewed initial readiness source changed')
    if sum(row['bytes'] for row in before.values()) > 16 * 1024 * 1024:
        raise RuntimeError('Guard stage exceeds its declared small copy budget')
    for name, pin in before.items():
        source, target = SOURCE / 'repository' / name, TARGET / 'repository' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if identity(target) != pin:
            raise RuntimeError('Copied guard input differs: ' + name)
    for name in ('parent-checkpoint.json', 'parent-source-identities.json', 'preparation.json'):
        shutil.copy2(SOURCE / name, TARGET / name)
    for name in ('run_controls.py', 'replay_historical.py', 'DESIGN.md'):
        shutil.copy2(SOURCE.parent / name, ROOT / name)
    after = inventory(SOURCE / 'repository')
    if before != after:
        raise RuntimeError('Source stage changed during exact copy')
    (TARGET / 'pre-correction-source-identities.json').write_text(json.dumps(before, indent=2) + '\n')
    result = {'status': 'EXACT_PRIVATE_MEMORY_STAGE_PREPARED', 'created_utc': datetime.now(timezone.utc).isoformat(),
              'files': len(before), 'bytes': sum(row['bytes'] for row in before.values()),
              'source_bytes_unchanged': True, 'destination_bytes_equal': inventory(TARGET / 'repository') == before,
              'overlay_written': False, 'active_changes': False, 'android_executed': False}
    (TARGET / 'memory-preparation.json').write_text(json.dumps(result, indent=2) + '\n')
    (ROOT / 'tmp').mkdir()
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
