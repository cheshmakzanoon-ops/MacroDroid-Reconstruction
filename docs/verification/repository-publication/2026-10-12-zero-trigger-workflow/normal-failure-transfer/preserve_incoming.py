from pathlib import Path
import hashlib, io, json, subprocess, zipfile

ROOT=Path('/workspace/scratch/4130730d15aa')
REPO=ROOT/'MacroDroid-Reconstruction'
EXPORT=ROOT/'normal-failure-transfer'
OLD='dbcad968c5c3e8f084205393a6c0d2d06a203c71'
HEAD='f3564f510dc897d658a7db6a98c9d7a3e74d7174'
def git(*a):return subprocess.check_output(['git',*a],cwd=REPO)
assert subprocess.run(['git','merge-base','--is-ancestor',OLD,HEAD],cwd=REPO).returncode==0
selected={r['path'] for r in json.loads((EXPORT/'manifest.json').read_text())}
changes=git('diff','--name-status',OLD,HEAD).decode().splitlines()
assert len(changes)==10
rows=[];data_by_path={}
for line in changes:
    status,name=line.split('\t');assert status=='A' and name not in selected,name
    item=git('ls-tree',HEAD,'--',name).decode().strip();info,path=item.split('\t');mode,kind,blob=info.split()
    assert path==name and kind=='blob' and mode in ('100644','100755')
    data=git('cat-file','blob',blob)
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
    row=dict(path=name,size_bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),git_blob_sha1=blob,mode=mode)
    rows.append(row);data_by_path[name]=data
archive_checks=[]
for run in (38214498409,38214498414):
    prefix=f'docs/verification/editor-journey/run-{run}-attempt-1/'
    manifest=json.loads(data_by_path[prefix+'manifest.json']);data=data_by_path[prefix+'evidence.zip']
    assert manifest['run_id']==run and manifest['head_sha']==OLD
    assert manifest['artifact_bytes']==len(data) and manifest['artifact_digest']=='sha256:'+hashlib.sha256(data).hexdigest()
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        members=[m for m in archive.infolist() if not m.is_dir()]
        expected={r['path']:r for r in manifest['members']}
        assert len(members)==len(expected)==len(manifest['members'])
        seen=set()
        for member in members:
            name=member.filename;assert name in expected and name not in seen;seen.add(name)
            d=archive.read(member);row=expected[name]
            assert len(d)==row['bytes'] and hashlib.sha256(d).hexdigest()==row['sha256'],name
    archive_checks.append(dict(run_id=run,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),verified_members=len(expected),conclusion=manifest['conclusion']))
for row in rows:
    p=REPO/row['path'];data=data_by_path[row['path']]
    assert not p.is_symlink() and (not p.exists() or p.read_bytes()==data),p
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);p.chmod(int(row['mode'],8)&0o777)
baselines=json.loads((EXPORT/'preparation.json').read_text())['baselines']
for name,h in baselines.items():assert hashlib.sha256(git('show',HEAD+':'+name)).hexdigest()==h,name
result=dict(old=OLD,head=HEAD,tree=git('rev-parse',HEAD+'^{tree}').decode().strip(),files=rows,
    archive_checks=archive_checks,baseline_guards_passed=True,unapproved_active_changes=False)
(EXPORT/'external-preservation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='files'}))
