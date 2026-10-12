#!/usr/bin/env python3
"""Make one owned read-only validation input from the already frozen APK parts."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat

BASE = Path('/dev/shm/macrodroid-exact-alarm-enable-return')
INPUT = Path('/dev/shm/macrodroid-transfer-space-20261012/numeric-success-candidate-capsule')
OUTPUT = BASE / 'numeric-input-01'
PREFIX = 'work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/'


def identity(path):
    assert stat.S_ISREG(path.lstat().st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def main():
    OUTPUT.mkdir(exist_ok=False)
    shutil.copyfile(__file__, OUTPUT / 'executed-materialize_numeric_input.py')
    result = {'schema': 1, 'passed': False, 'started_utc': datetime.now(timezone.utc).isoformat(),
              'android_executed': False, 'apk_build_executed': False, 'parts': []}
    before = {}
    try:
        manifest = INPUT / 'manifest.json'
        before[str(manifest)] = identity(manifest)
        assert before[str(manifest)] == {'bytes': 5189, 'sha256': 'e1e9c5713c83981cc85ec84e0ce25bfe3fe3a4918d8ff35744ff86194cad0152'}
        data = json.loads(manifest.read_bytes())
        assert data['filename'] == 'MacroDroid-5.67.8-day-numeric-0762aad9.apk'
        assert data['size_bytes'] == 94683136
        assert data['sha256'] == '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd'
        assert len(data['parts']) == 12
        shutil.copyfile(manifest, OUTPUT / 'manifest.json')
        target = OUTPUT / data['filename']
        total, complete = 0, hashlib.sha256()
        with target.open('xb') as sink:
            for number, row in enumerate(data['parts'], 1):
                relative = PurePosixPath(row['path'])
                assert row['path'] == PREFIX + 'parts/part-' + str(number).zfill(4) + '.bin'
                path = INPUT / relative.relative_to(PurePosixPath(PREFIX))
                expected = {'bytes': row['size_bytes'], 'sha256': row['sha256']}
                before[str(path)] = identity(path)
                assert before[str(path)] == expected
                part, size = hashlib.sha256(), 0
                with path.open('rb') as stream:
                    while block := stream.read(1024 * 1024):
                        part.update(block); complete.update(block)
                        size += len(block); total += len(block)
                        sink.write(block)
                assert {'bytes': size, 'sha256': part.hexdigest()} == expected
                result['parts'].append({'path': row['path'], **expected})
        expected = {'bytes': data['size_bytes'], 'sha256': data['sha256']}
        assert {'bytes': total, 'sha256': complete.hexdigest()} == expected == identity(target)
        target.chmod(0o444)
        result.update(passed=True, status='OWNED_NUMERIC_APK_REASSEMBLED_FROM_FROZEN_PARTS',
                      artifact={'path': str(target), **expected}, candidate_manifest=before[str(manifest)],
                      durable_repo_manifest=PREFIX + 'manifest.json')
    except Exception as error:
        result.update(status='OWNED_NUMERIC_INPUT_PREPARATION_FAILED', reason=repr(error))
    finally:
        after = {name: identity(Path(name)) for name in before}
        result['all_frozen_inputs_unchanged'] = before == after
        if before != after:
            result.update(passed=False, status='FROZEN_INPUT_CHANGED')
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (OUTPUT / 'read-input-identities.json').write_text(json.dumps({'before': before, 'after': after}, indent=2) + '\n')
        (OUTPUT / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({key: value for key, value in result.items() if key != 'parts'}, indent=2))
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
