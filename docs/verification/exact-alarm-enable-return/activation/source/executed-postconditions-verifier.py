"""Verify only the approved Settings workflow changed in the fetched commit."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess
ROOT=Path('/dev/shm/macrodroid-transfer-space-20261012')
EXPORT=ROOT/'settings-enable-return-activation-export'
GIT=['git','--git-dir='+str(ROOT/'verification.git')]
COMMIT='88f35e5f1ff52236e8cd51fe0188eabcb4d7bec4'
guard=json.loads((EXPORT/'preparation.json').read_bytes())
receipt=json.loads((EXPORT/'remote-verification.json').read_bytes())
assert receipt['commit']==COMMIT and receipt['git_mode_size_sha1_sha256_verified'] is True
assert receipt['staged_bytes_and_modes_equal_fetched_git'] is True
actual=set(subprocess.check_output(GIT+['diff-tree','--no-commit-id','--name-only','-r',guard['parent'],COMMIT]).decode().splitlines())
assert actual=={guard['active_path']}
protected={}
for path,before in guard['protected_tree_oids'].items():
    after=subprocess.check_output(GIT+['rev-parse',COMMIT+':'+path]).decode().strip()
    assert after==before,path
    protected[path]={'before':before,'after':after,'unchanged':True}
helpers=[]
for row in guard['reviewed_existing_helpers']:
    entry=subprocess.check_output(GIT+['ls-tree',COMMIT,'--',row['path']]).decode().strip()
    info,path=entry.split('\t',1)
    mode,kind,oid=info.split()
    raw=subprocess.check_output(GIT+['cat-file','blob',oid])
    assert path==row['path'] and mode==row['mode'] and kind=='blob' and oid==row['git_blob_sha1']
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    helpers.append(row|{'unchanged':True})
for path,row in guard['previous_workflows'].items():
    info,name=subprocess.check_output(GIT+['ls-tree',COMMIT,'--',path]).decode().strip().split('\t',1)
    mode,kind,oid=info.split()
    assert name==path and mode==row['mode'] and kind=='blob' and oid==row['git_blob_sha1'],path
result={'schema':1,'commit':COMMIT,'parent':guard['parent'],'changed_paths':sorted(actual),
 'previous_absence_guard_verified':True,'existing_helpers':helpers,'protected_trees':protected,
 'existing_workflows_checked':len(guard['previous_workflows']),
 'active_application_and_apk_unchanged':True,'other_existing_workflows_unchanged':True,
 'actual_android_outcome':'PENDING_AUTOMATIC_RUN',
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'completed_utc':datetime.now(timezone.utc).isoformat()}
with (EXPORT/'protected-trees-after.json').open('x') as stream:stream.write(json.dumps(result,indent=2)+'\n')
print(json.dumps({'commit':COMMIT,'exact_changed_paths':1,'existing_helpers_unchanged':len(helpers),'all_protected_unchanged':True}))

