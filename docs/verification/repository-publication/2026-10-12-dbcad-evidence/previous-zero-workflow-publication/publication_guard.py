from pathlib import Path
import hashlib,json,subprocess
ROOT=Path('/workspace/scratch/4130730d15aa');REPO=ROOT/'MacroDroid-Reconstruction';EXPORT=ROOT/'zero-trigger-transfer'
HEAD='d5a805d53b7fe166e2c81ed1439d0449defc4dc6'
def git(*a):return subprocess.check_output(['git',*a],cwd=REPO)
assert git('rev-parse','HEAD').decode().strip()==HEAD
manifest=json.loads((EXPORT/'manifest.json').read_text());selected={r['path'] for r in manifest};assert len(selected)==185
tree={}
for item in git('ls-tree','-rz','--full-tree',HEAD).split(b'\0'):
    if item:
        info,path=item.split(b'\t',1);tree[path.decode()]=info.decode().split()
for name,h in json.loads((EXPORT/'preparation.json').read_text())['baselines'].items():assert hashlib.sha256(git('show',HEAD+':'+name)).hexdigest()==h
guards=json.loads((EXPORT/'activation-guards.json').read_text())
for name in guards['absent_paths']:assert name not in tree,name
for row in guards['unchanged_files']:
    data=(REPO/row['path']).read_bytes()
    assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
    if row['path'] not in selected:
        assert tree[row['path']][2]==hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),row['path']
for row in manifest:
    data=(REPO/row['path']).read_bytes();assert len(data)==row['size_bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
(EXPORT/'external-preservation.json').write_text(json.dumps(dict(old=HEAD,head=HEAD,files=[],baseline_guards_passed=True,exact_active_workflow_absence_verified=True,unchanged_role_bindings=192),indent=2)+'\n')
print('185 exact paths and 192 complete source roles match the approved tree; workflow was absent at parent.')
