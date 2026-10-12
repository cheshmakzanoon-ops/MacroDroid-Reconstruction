#!/usr/bin/env python3
"""Copy the closed twelve-role source, changing only its queued wrapper filename."""
from datetime import datetime,timezone
import difflib
import hashlib
import json
from pathlib import Path
import shutil

ROOT=Path('/dev/shm/day-numeric-art-workflow-01')
FIRST=ROOT/'checkpoints/01-offline-validated-runtime-path-blocker'
OLD=ROOT/'source-01'
NEW=ROOT/'source-02'
WORKFLOW='.github/workflows/day-numeric-method-probe.yml'
EXPECTED='3945eb046eaf5019099349383c3557ca752e27866b27dc80a9272af2ab2bf6ab'


def identity(path):
    raw=path.read_bytes()
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
            'mode':'100755' if path.stat().st_mode&0o111 else '100644'}


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as stream:stream.write(json.dumps(value,indent=2)+'\n')


def main():
    output=ROOT/'reports/path-correction-01'
    output.mkdir(parents=True,exist_ok=False)
    result={'started_utc':datetime.now(timezone.utc).isoformat(),'passed':False,
            'android_executed':False,'application_build_executed':False,
            'prior_30_checks_rerun':False,'prior_42_controls_rerun':False}
    try:
        if identity(FIRST/'checkpoint.json')['sha256']!=EXPECTED:
            raise ValueError('Closed first attempt changed')
        sources=json.loads((FIRST/'source-files.json').read_bytes())
        if len(sources)!=12:
            raise ValueError('Exact twelve-role source inventory required')
        NEW.mkdir(exist_ok=False)
        rows=[]
        for row in sources:
            path=OLD/row['path']
            before=identity(path)
            if before!={k:row[k] for k in ('bytes','sha256','mode')}:
                raise ValueError('Retained source01 changed')
            raw=path.read_bytes()
            if row['path']==WORKFLOW:
                wrong=b'$GITHUB_WORKSPACE/tools/day_numeric_art/android_numeric_method_probe.py'
                right=b'$GITHUB_WORKSPACE/tools/day_numeric_art/android_day_numeric_method_probe.py'
                if raw.count(wrong)!=1 or right in raw:
                    raise ValueError('Exact one-token path correction boundary differs')
                raw=raw.replace(wrong,right,1)
            target=NEW/row['path'];target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as stream:stream.write(raw)
            target.chmod(0o755 if row['mode']=='100755' else 0o644)
            after=identity(target)
            if row['path']!=WORKFLOW and after!=before:
                raise ValueError('An unrelated executable source changed')
            if identity(path)!=before:
                raise ValueError('Retained source changed during successor copy')
            rows.append({'path':row['path'],'before':before,'after':after,'changed':before!=after})
        if [row['path'] for row in rows if row['changed']]!=[WORKFLOW]:
            raise ValueError('Expected workflow-only successor')
        patch=''.join(difflib.unified_diff((OLD/WORKFLOW).read_text().splitlines(True),
            (NEW/WORKFLOW).read_text().splitlines(True),fromfile='source-01/'+WORKFLOW,tofile='source-02/'+WORKFLOW))
        (output/'derivation.patch').write_text(patch)
        save(output/'source-delta.json',rows)
        result.update(passed=True,status='WORKFLOW_ONLY_QUEUED_WRAPPER_PATH_CORRECTED',
                      old_checkpoint_sha256=EXPECTED,unchanged_source_roles=11,
                      changed_paths=[WORKFLOW],old_workflow=identity(OLD/WORKFLOW),new_workflow=identity(NEW/WORKFLOW))
    except Exception as error:
        result.update(status='PATH_SUCCESSOR_AUTHORING_FAILED',reason=repr(error))
    finally:
        result['finished_utc']=datetime.now(timezone.utc).isoformat()
        save(output/'result.json',result);print(json.dumps(result,indent=2))
    if not result['passed']:raise SystemExit(2)


if __name__=='__main__':main()
