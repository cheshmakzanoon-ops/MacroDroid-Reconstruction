#!/usr/bin/env python3
"""Freeze the small closed workflow review without copying its parent payloads."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'checkpoints/02-workflow03-independent-review'


def identity(path):
    assert path.is_file() and not path.is_symlink()
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':digest}


def main():
    report_root = ROOT / 'reports/02-frozen-workflow03-review'
    command_root = ROOT / 'reports/02-frozen-workflow03-command'
    result_path = report_root / 'review-result.json'
    result = json.loads(result_path.read_text())
    assert identity(result_path)['sha256'] == '12bcdf49c588c4a85bcc5046938e3aa7536cf2c2467849084bea5d0226acfb1b'
    assert result['status'] == 'CLOSED_DAYTIME13_WORKFLOW_REVIEW_SUPPORTED_FOR_SEPARATE_RUNTIME'
    command = json.loads((command_root / 'command.json').read_text())
    assert command['exit_code'] == 0 and command['passed'] is True and command['source_unchanged'] is True
    assert identity(ROOT / 'review_workflow03.py')['sha256'] == command['source_sha256']
    for stream in ('stdout','stderr'):
        assert identity(command_root / command[stream]['path']) == {k:command[stream][k] for k in ('bytes','sha256')}
    files = {'README.md': ROOT / 'WORKFLOW_REVIEW.md',
             'review_workflow03.py':ROOT / 'review_workflow03.py',
             'run_workflow_review.py':ROOT / 'run_workflow_review.py',
             'freeze_workflow_review.py':Path(__file__)}
    for prefix, folder in (('reports',report_root),('command',command_root)):
        for path in sorted(folder.rglob('*')):
            if path.is_file():
                files[prefix + '/' + path.relative_to(folder).as_posix()] = path
    OUT.mkdir(parents=True,exist_ok=False)
    rows = []
    for name, source in sorted(files.items()):
        before = identity(source); target = OUT / name
        target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(source,target)
        assert identity(source) == before == identity(target)
        rows.append({'path':name,**before,'mode':target.stat().st_mode & 0o777})
    checkpoint = {'schema':1,'status':'INDEPENDENT_DAYTIME13_WORKFLOW_REVIEW_SUPPORTED_FOR_SEPARATE_RUNTIME',
        'created_utc':datetime.now(timezone.utc).isoformat(),
        'reviewed_checkpoint_sha256':result['source_checkpoint_sha256'],
        'workflow_sha256':result['workflow_sha256'],'review_result_sha256':identity(result_path)['sha256'],
        'new_android_execution':False,'active_changes':False,'historical_five_pixel_failure_unchanged':True,
        'runtime_result_pending':True,'files':rows}
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
    assert {p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file()} == set(files) | {'checkpoint.json'}
    for row in rows:
        assert identity(OUT / row['path']) == {k:row[k] for k in ('bytes','sha256')}
    print(json.dumps({'checkpoint':str(OUT / 'checkpoint.json'),**identity(OUT / 'checkpoint.json'),
                      'files':len(rows),'payload_bytes':sum(row['bytes'] for row in rows)},indent=2))


if __name__ == '__main__':
    main()
