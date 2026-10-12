#!/usr/bin/env python3
"""Freeze the closed independent DayTime13/Zero12 review without large inputs."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
STUDY = ROOT / 'reports/01-frozen-daytime13-zero12-replay'
OUT = ROOT / 'checkpoints/01-daytime13-zero12-regression'


def identity(path):
    assert path.is_file() and not path.is_symlink()
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def main():
    assert shutil.disk_usage(ROOT).free >= 8 * 1024 * 1024
    result_path = STUDY / 'review/review-result.json'
    assert identity(result_path)['sha256'] == '8af00c81777fab222862b14f28421ae1b0685498922eeee85d4ad6a17f092a8a'
    result = json.loads(result_path.read_text())
    assert result['status'] == 'FROZEN_DAYTIME13_REVIEW_AND_ACTUAL_ZERO12_REGRESSION_VERIFIED'
    assert result['historical_journey_equal'] is False and result['historical_full_rgba_pixel_vector'] == [0,5,0,0,0,0,0,0,0,0,0,0]
    command = json.loads((STUDY / 'command.json').read_text())
    assert command['passed'] is True and command['exit_code'] == 0 and command['review_source_unchanged'] is True
    assert identity(ROOT / 'review_daytime13.py')['sha256'] == command['review_source_sha256']
    assert identity(ROOT / 'run_review.py')['sha256'] == command['launcher_source_sha256']
    for stream in ('stdout', 'stderr'):
        assert identity(STUDY / command[stream]['path']) == {k: command[stream][k] for k in ('bytes', 'sha256')}
    OUT.mkdir(parents=True, exist_ok=False)
    sources = {name: ROOT / name for name in ('README.md', 'review_daytime13.py', 'run_review.py', 'freeze_review.py')}
    sources.update({'reports/' + path.relative_to(STUDY).as_posix(): path
                    for path in sorted(STUDY.rglob('*')) if path.is_file()})
    rows = []
    for name, source in sorted(sources.items()):
        before = identity(source)
        target = OUT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        assert identity(source) == before == identity(target)
        rows.append({'path': name, **before, 'mode': target.stat().st_mode & 0o777})
    checkpoint = {'schema': 1,
        'status': 'INDEPENDENT_DAYTIME13_SOURCE_REVIEW_AND_CLOSED_ZERO12_REGRESSION_VERIFIED',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'reviewed_source_checkpoint_sha256': result['reviewed_checkpoint_sha256'],
        'review_result_sha256': identity(result_path)['sha256'],
        'original_zero12_archive': result['zero12_archive'],
        'historical_journey_equal': False,
        'historical_five_pixel_failure_preserved': True,
        'android_executed_by_this_review': False, 'active_source_changes': False,
        'thirteen_screen_android_result_established': False,
        'source_and_report_count': len(rows),
        'files': rows}
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    assert {p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file()} == set(sources) | {'checkpoint.json'}
    for row in rows:
        assert identity(OUT / row['path']) == {k: row[k] for k in ('bytes','sha256')}
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
                      'files': len(rows), 'payload_bytes': sum(row['bytes'] for row in rows)}, indent=2))


if __name__ == '__main__':
    main()
