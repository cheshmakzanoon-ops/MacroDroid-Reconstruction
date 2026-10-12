from pathlib import Path
import hashlib,json,subprocess
root=Path('/workspace/scratch/4130730d15aa'); repo=root/'MacroDroid-Reconstruction'; exp=root/'daytime-activation-transfer'
parent='cd35fd31ac0a1606b2dc497fa66ab0b4acca873d'
def git(*a): return subprocess.check_output(['git',*a],cwd=repo)
assert git('rev-parse','HEAD').decode().strip()==parent
prep=json.loads((exp/'preparation.json').read_text()); rows=json.loads((exp/'manifest.json').read_text())
tracked=set(git('ls-tree','-r','--name-only',parent).decode().splitlines())
checks=[]
for row in rows:
 p=repo/row['path']; b=p.read_bytes()
 assert not p.is_symlink()
 assert len(b)==row['size_bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
 assert ('100755' if p.stat().st_mode&0o111 else '100644')==row['mode'],row['path']
 if row['path'] in prep['baselines']:
  old=git('show',parent+':'+row['path'])
  assert hashlib.sha256(old).hexdigest()==prep['baselines'][row['path']],row['path']
 elif row['path'] in tracked:
  assert git('show',parent+':'+row['path'])==b,('unexpected existing content',row['path'])
 checks.append(row['path'])
result={'parent':parent,'selected_files':len(rows),'local_bytes_modes_verified':True,'existing_baselines_verified':prep['baselines'],'no_unreviewed_existing_path_overwrites':True}
(exp/'publication-guard.json').write_text(json.dumps(result,indent=2)+'\n')
(exp/'external-preservation.json').write_text(json.dumps({'old':parent,'head':parent,'files':[],'baseline_guards_passed':True},indent=2)+'\n')
print(json.dumps(result))
