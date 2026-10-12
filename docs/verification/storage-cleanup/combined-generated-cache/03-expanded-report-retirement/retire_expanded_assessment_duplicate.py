from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, io, json, os, shutil, stat, subprocess

BASE=Path('/dev/shm/macrodroid-transfer-space-20261012')
SOURCE=Path('/workspace/scratch/4130730d15aa/combined-cache-inventory/checkpoints/02-hybrid-smali-eligibility')
TARGET=SOURCE/'retained-classes.json'
COMMIT='573370e92ca9736c2ae47862989e72ff8c7b8700'
PREFIX='docs/verification/storage-cleanup/combined-generated-cache/02-no-eligible-hybrid-smali/'
EXPECTED=dict(bytes=97324105,sha256='c7915bd24ff18447c85e32d662eefcd8042b3d5dfeb4ac4d8d454cecf9384a6c',mode=0o644,device=27,inode=765746,nlink=1)
OUT=BASE/'expanded-report-retirement';OUT.mkdir(exist_ok=False)

def now():return datetime.now(timezone.utc).isoformat()
def digest(path):
 h=hashlib.sha256();n=0
 with path.open('rb') as f:
  while b:=f.read(1024*1024):h.update(b);n+=len(b)
 return dict(bytes=n,sha256=h.hexdigest())
def git(*a):return subprocess.check_output(['git','--git-dir='+str(BASE/'verification.git'),*a])
def save(name,j):(OUT/name).write_text(json.dumps(j,indent=2)+'\n')
def md(s):return dict(bytes=s.st_size,mode=stat.S_IMODE(s.st_mode),device=s.st_dev,inode=s.st_ino,nlink=s.st_nlink,allocated_bytes=s.st_blocks*512)

result=dict(status='VERIFYING_ONE_PUBLISHED_EXPANDED_REPORT_DUPLICATE',started_utc=now(),commit=COMMIT,target=str(TARGET),free_bytes_before=shutil.disk_usage(SOURCE).free,target_mutated=False)
fd=None
try:
 cpraw=(SOURCE/'checkpoint.json').read_bytes();assert hashlib.sha256(cpraw).hexdigest()=='6b82b42cb236f1c85024d9f90c1fa73f5b7c3e253af8bc9838a09e280d9f5d5b'
 assert git('show',COMMIT+':'+PREFIX+'checkpoint.json')==cpraw
 layout_raw=git('show',COMMIT+':'+PREFIX+'publication-layout.json');mapping=json.loads(layout_raw)['payload_mapping'][0]
 assert {k:mapping['original_'+k] for k in ('bytes','sha256','mode')}=={k:EXPECTED[k] for k in ('bytes','sha256','mode')}
 compressed=git('show',COMMIT+':'+PREFIX+mapping['stored_path'])
 assert len(compressed)==mapping['stored_bytes'] and hashlib.sha256(compressed).hexdigest()==mapping['stored_sha256']
 cp=json.loads(cpraw);controls=[]
 for row in cp['files']:
  if row['path']=='retained-classes.json':continue
  p=SOURCE/row['path'];actual=digest(p);assert actual=={k:row[k] for k in ('bytes','sha256')}
  controls.append(dict(path=str(p),mode=stat.S_IMODE(p.stat().st_mode),**actual))
 controls.append(dict(path=str(SOURCE/'checkpoint.json'),mode=stat.S_IMODE((SOURCE/'checkpoint.json').stat().st_mode),**digest(SOURCE/'checkpoint.json')))
 prior_protected=json.loads((SOURCE/'protected-after.json').read_text())
 for row in prior_protected:
  p=Path(row['path']);assert digest(p)=={k:row[k] for k in ('bytes','sha256')}
  controls.append(dict(path=str(p),mode=stat.S_IMODE(p.stat().st_mode),bytes=row['bytes'],sha256=row['sha256']))
 save('protected-before.json',controls)
 fd=os.open(TARGET,os.O_RDWR|os.O_NOFOLLOW)
 s=os.fstat(fd);assert stat.S_ISREG(s.st_mode)
 assert {k:md(s)[k] for k in EXPECTED if k!='sha256'}=={k:v for k,v in EXPECTED.items() if k!='sha256'}
 before=md(s);h=hashlib.sha256();n=0
 with gzip.GzipFile(fileobj=io.BytesIO(compressed),mode='rb') as uncompressed,os.fdopen(os.dup(fd),'rb') as original:
  while b:=uncompressed.read(1024*1024):
   other=original.read(len(b));assert other==b;h.update(b);n+=len(b)
  assert original.read(1)==b''
 assert n==EXPECTED['bytes'] and h.hexdigest()==EXPECTED['sha256']
 current=TARGET.lstat();assert stat.S_ISREG(current.st_mode) and md(current)==before
 os.ftruncate(fd,0);os.close(fd);fd=None;result['target_mutated']=True
 after=md(TARGET.lstat());assert after['bytes']==0 and after['mode']==EXPECTED['mode'] and after['device']==EXPECTED['device'] and after['inode']==EXPECTED['inode'] and after['nlink']==1
 for row in controls:
  p=Path(row['path']);assert digest(p)=={k:row[k] for k in ('bytes','sha256')} and stat.S_IMODE(p.stat().st_mode)==row['mode']
 save('protected-after.json',controls)
 result.update(status='EXACT_PUBLISHED_EXPANDED_REPORT_DUPLICATE_RETIRED',before=before,after=after,
  original_payload_sha256=EXPECTED['sha256'],fetched_compressed_sha256=mapping['stored_sha256'],
  fetched_decompression_compared_byte_for_byte=True,protected_control_files_unchanged=len(controls),
  original_checkpoint_and_mapping_unchanged=True,source_apk_or_generated_cache_modified=False,
  retained_representation=dict(commit=COMMIT,compressed_repository_path=PREFIX+mapping['stored_path'],mapping_repository_path=PREFIX+'publication-layout.json'))
except BaseException as error:
 result.update(status='EXPANDED_REPORT_RETIREMENT_STOPPED',error=type(error).__name__+': '+str(error))
 raise
finally:
 if fd is not None:os.close(fd)
 result.update(finished_utc=now(),free_bytes_after=shutil.disk_usage(SOURCE).free)
 save('receipt.json',result)
shutil.copy2(Path(__file__),OUT/'retire_expanded_assessment_duplicate.py')
files=[dict(path=p.name,**digest(p)) for p in sorted(OUT.iterdir()) if p.is_file()]
save('checkpoint.json',dict(status=result['status'],created_utc=now(),active_files=[],files=files))
print(json.dumps(result))
