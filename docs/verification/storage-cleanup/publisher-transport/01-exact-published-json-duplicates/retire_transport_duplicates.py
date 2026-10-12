from pathlib import Path
import os,sys,json,hashlib,shutil,stat
from datetime import datetime,timezone
R=Path('/workspace/scratch/4130730d15aa');G=R/'MacroDroid-Reconstruction';plan=json.loads(sys.argv[1]);rows=plan['selected']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for row in rows:
 p=Path(row['path']);a=G/row['authoritative_repository_path'];s=p.lstat()
 assert p.parent.parent==R and p.parent.name.endswith('-transfer') and p.name.endswith('.json') and not p.name.startswith('text-')
 assert stat.S_ISREG(s.st_mode) and not p.is_symlink() and s.st_nlink==1 and (s.st_dev,s.st_ino,s.st_size,stat.S_IMODE(s.st_mode))==(row['device'],row['inode'],row['bytes'],row['mode'])
 assert digest(p)==digest(a)==row['sha256'] and not p.samefile(a)
result=dict(status='EXACT_PUBLISHED_TRANSPORT_RETIREMENT_IN_PROGRESS',started_utc=datetime.now(timezone.utc).isoformat(),immutable_commit=plan['commit'],free_bytes_before=shutil.disk_usage(R).free,selected=rows,scope=plan['target_scope'],zeroed=[])
for row in rows:
 p=Path(row['path']);fd=os.open(p,os.O_WRONLY|os.O_NOFOLLOW)
 try:
  s=os.fstat(fd);assert s.st_dev==row['device'] and s.st_ino==row['inode'] and s.st_nlink==1 and s.st_size==row['bytes']
  os.ftruncate(fd,0)
 finally:os.close(fd)
 result['zeroed'].append(str(p))
for row in rows:
 p=Path(row['path']);a=G/row['authoritative_repository_path'];assert p.stat().st_size==0 and digest(a)==row['sha256'] and (a.stat().st_mode&0o777)==row['mode']
result.update(status='EXACT_PUBLISHED_TRANSPORT_DUPLICATES_RETIRED',finished_utc=datetime.now(timezone.utc).isoformat(),free_bytes_after=shutil.disk_usage(R).free,all_authoritative_repository_bytes_and_modes_unchanged=True,zero_placeholders=len(rows),github_history_untouched=True)
print(json.dumps(result,indent=2))
