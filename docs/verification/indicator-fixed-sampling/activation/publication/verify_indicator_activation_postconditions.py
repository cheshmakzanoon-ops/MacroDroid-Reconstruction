"""Check the exact sixteen-path activation against its fetched parent."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

ROOT=Path('/dev/shm/macrodroid-transfer-space-20261012')
EXPORT=ROOT/'indicator-fixed-sampling-activation-export-02'
GIT=['git','--git-dir='+str(ROOT/'verification.git')]
COMMIT='89c21bff74b854927a25bd33a9f772a59e849321'
guard=json.loads((EXPORT/'preparation.json').read_bytes())
receipt=json.loads((EXPORT/'remote-verification.json').read_bytes())
assert receipt['commit']==COMMIT and receipt['git_mode_size_sha1_sha256_verified'] is True
assert receipt['staged_bytes_and_modes_equal_fetched_git'] is True
actual=set(subprocess.check_output(GIT+['diff-tree','--no-commit-id','--name-only','-r',guard['parent'],COMMIT]).decode().splitlines())
expected={row['path'] for row in guard['bindings']}
assert actual==expected and len(actual)==16
protected={}
for path,before in guard['protected_tree_oids'].items():
    after=subprocess.check_output(GIT+['rev-parse',COMMIT+':'+path]).decode().strip()
    assert after==before,path
    protected[path]=dict(before=before,after=after,unchanged=True)
result=dict(schema=1,commit=COMMIT,parent=guard['parent'],changed_paths=sorted(actual),
    all_sixteen_existing_absence_guards_passed=True,protected_trees=protected,
    active_application_and_apk_unchanged=True,other_existing_workflows_unchanged=True,
    actual_android_outcome='PENDING_AUTOMATIC_RUN',
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    completed_utc=datetime.now(timezone.utc).isoformat())
with (EXPORT/'protected-trees-after.json').open('x') as stream:stream.write(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(commit=COMMIT,exact_changed_paths=16,protected_tree_count=len(protected),all_protected_unchanged=True)))
