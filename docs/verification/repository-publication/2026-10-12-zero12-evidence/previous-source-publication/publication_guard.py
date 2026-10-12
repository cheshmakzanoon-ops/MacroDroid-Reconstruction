from pathlib import Path
import hashlib,json,subprocess
ROOT=Path('/workspace/scratch/4130730d15aa');REPO=ROOT/'MacroDroid-Reconstruction';EXP=ROOT/'dbcad-source-transfer'
PARENT='5f2e8b598a9c871e5374c7f1e1645780699c844d'
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
assert git('rev-parse','HEAD').decode().strip()==PARENT
prep=json.loads((EXP/'preparation.json').read_text());rows=json.loads((EXP/'manifest.json').read_text())
virtual={r['path']:r for r in json.loads((EXP/'virtual-blobs.json').read_text())}
tracked=set(git('ls-tree','-r','--name-only',PARENT).decode().splitlines())
for row in rows:
 p=REPO/row['path']
 if row['path'] in virtual:
  v=virtual[row['path']];source=Path(v['source_path'])
  assert not p.exists() and not p.is_symlink(),row['path']
  with source.open('rb') as f:f.seek(v['source_offset']);data=f.read(row['size_bytes'])
  assert row['mode']=='100644'
 else:
  assert p.is_file() and not p.is_symlink(),row['path']
  data=p.read_bytes();assert ('100755' if p.stat().st_mode&0o111 else '100644')==row['mode']
 assert len(data)==row['size_bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['git_blob_sha1']
 if row['path'] in prep['baselines']:
  assert hashlib.sha256(git('show',PARENT+':'+row['path'])).hexdigest()==prep['baselines'][row['path']],row['path']
 elif row['path'] in tracked:
  assert git('show',PARENT+':'+row['path'])==data,('unreviewed overwrite',row['path'])
result={'parent':PARENT,'selected_files':len(rows),'virtual_ranges':len(virtual),'all_metadata_and_virtual_range_bytes_modes_verified':True,'existing_baselines_verified':prep['baselines'],'source_archive_or_repo_parts_retired_or_materialized':False}
(EXP/'publication-guard.json').write_text(json.dumps(result,indent=2)+'\n')
(EXP/'external-preservation.json').write_text(json.dumps({'old':PARENT,'head':PARENT,'files':[],'baseline_guards_passed':True},indent=2)+'\n')
print(json.dumps(result))
