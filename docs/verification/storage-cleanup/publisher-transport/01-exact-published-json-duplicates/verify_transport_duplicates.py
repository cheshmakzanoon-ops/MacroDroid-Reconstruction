from pathlib import Path
import hashlib,json,subprocess,stat,shutil
R=Path('/workspace/scratch/4130730d15aa'); G=R/'MacroDroid-Reconstruction'; C='a58c9560d0658e29c63bedb97c748d41a107e421'
tree={}
for row in subprocess.check_output(['git','ls-tree','-rz',C],cwd=G).split(b'\0'):
 if not row:continue
 info,name=row.split(b'\t',1);mode,kind,oid=info.decode().split()
 if kind=='blob':tree.setdefault(oid,[]).append((mode,name.decode()))
candidates=[]
for d in sorted(R.iterdir()):
 if not d.is_dir() or d.is_symlink() or not d.name.endswith('-transfer') or d.name in ['day-source-storage-transfer']:continue
 for p in sorted(d.iterdir()):
  if not p.is_file() or p.is_symlink() or p.suffix!='.json' or p.name.startswith('text-'):continue
  s=p.stat()
  if not (10000<=s.st_size<=32*1024*1024) or s.st_nlink!=1:continue
  b=p.read_bytes();h=hashlib.sha256(b).hexdigest();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();mode='100755' if s.st_mode&0o111 else '100644'
  refs=[name for m,name in tree.get(oid,[]) if m==mode]
  if not refs:continue
  target=G/refs[0]
  if target.is_symlink() or not target.is_file() or target.samefile(p):continue
  if target.read_bytes()!=b or (target.stat().st_mode&0o777)!=(s.st_mode&0o777):continue
  candidates.append(dict(path=str(p),bytes=len(b),sha256=h,git_blob_sha1=oid,mode=s.st_mode&0o777,device=s.st_dev,inode=s.st_ino,links=s.st_nlink,allocated_bytes=s.st_blocks*512,authoritative_repository_path=refs[0]))
selected=[];total=0
for row in sorted(candidates,key=lambda r:r['allocated_bytes'],reverse=True):
 if total+row['allocated_bytes']>48*1024*1024:continue
 selected.append(row);total+=row['allocated_bytes']
 if total>=32*1024*1024:break
assert selected
p=subprocess.Popen(['git','cat-file','--batch'],cwd=G,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for row in selected:
 p.stdin.write((row['git_blob_sha1']+'\n').encode());p.stdin.flush();oid,kind,size=p.stdout.readline().decode().split();b=p.stdout.read(int(size));assert p.stdout.read(1)==b'\n';assert oid==row['git_blob_sha1'] and kind=='blob' and len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
p.stdin.close();assert p.wait()==0
print(json.dumps(dict(status='EXACT_FETCHED_TRANSPORT_DUPLICATES_VERIFIED',commit=C,free_bytes_before=shutil.disk_usage(R).free,total_allocated_bytes=total,selected=selected,authoritative_repository_files_and_git_objects_verified=True,target_scope='Closed publisher JSON transport metadata only; no text wrappers, source, checkpoint originals, APKs or evidence archives.'),indent=2))
