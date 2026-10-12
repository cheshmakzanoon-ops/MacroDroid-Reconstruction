from pathlib import Path, PurePosixPath
import hashlib, json, os, stat, subprocess, tarfile
from datetime import datetime, timezone

BASE=Path('/dev/shm/macrodroid-transfer-space-20261012')
REPO=Path('/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction')
PARENT='394234b0e74c9f1d660836c8f2a89901fe05ff9d'
TREE=BASE/'publication-tree';TREE.mkdir(exist_ok=False)
EXPORT=BASE/'export';EXPORT.mkdir(exist_ok=False)
paths=set();prefixes=[];checks={}
def sha(b):return hashlib.sha256(b).hexdigest()
def safe(s):
 p=PurePosixPath(s);assert not p.is_absolute() and '..' not in p.parts;return p.as_posix()
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def save(name,b,mode=0o644):
 name=safe(name);p=TREE/name;p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists();p.write_bytes(b);p.chmod(mode);paths.add(name)
def jsave(name,j):save(name,(json.dumps(j,indent=2)+'\n').encode())
def link(source,name):
 name=safe(name);target=TREE/name;assert source.is_file() and not source.is_symlink();target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists();os.link(source,target);paths.add(name)
def mode_of(row,p):
 actual=stat.S_IMODE(p.stat().st_mode);m=row.get('mode')
 if m is not None:
  expected=int(m,8) if isinstance(m,str) and m.startswith('0o') else (int(m,8)&0o777) if isinstance(m,str) and m.startswith('100') else m
  assert type(expected)is int and expected==actual,(p,m,actual)
 return actual

target='docs/verification/storage-cleanup/combined-generated-cache/02-no-eligible-hybrid-smali'
cpraw=(BASE/'eligibility/checkpoint.json').read_bytes();assert sha(cpraw)=='6b82b42cb236f1c85024d9f90c1fa73f5b7c3e253af8bc9838a09e280d9f5d5b'
layout=json.loads((BASE/'eligibility/publication-layout.json').read_text())
assert layout['original_checkpoint_unchanged'] and layout['original_assessment_payload_unchanged']
for p in sorted((BASE/'eligibility').iterdir()):
 if p.is_file():link(p,target+'/'+p.name)
result=json.loads((BASE/'eligibility/result.json').read_text())
assert result['eligible_files']==0 and result['retained_files']==71267 and result['recovered_classes_retained']==605 and result['mutations_performed'] is False
save(target+'/README.md',b'''# No eligible hybrid-smali cache files

The exhaustive read-only assessment retained all 71,267 cache entries. Of these,
70,662 share their physical inode with canonical source and have multiple links;
the other 605 are registered recovered classes. Zero files are eligible for
retirement under the conservative exact-duplicate policy. No cache or source
payload was changed. All canonical/cache identities and 1,608 protected file
identities were checked before and after; result.json carries the actual count.
Unavailable process checks remain unavailable, never passing checks.

The original checkpoint.json is preserved byte-for-byte. Its 97,324,105-byte
retained-classes.json is represented without data loss by retained-classes.json.gz.
publication-layout.json binds the original length, SHA-256 and mode to the exact
compressed container. Decompression was independently streamed and verified.
Use materialize_retained_classes.py with an explicit output file to reconstruct
that original checkpoint member; all other declared members are stored normally.

The unusually large expanded retained list contributed to a full workspace.
This fact does not authorize retirement of any cache or authoritative evidence.
The accompanying publisher transport receipt is a separate operation on exact,
already-published JSON duplicates and reported no observed free-space increase.
''')
# Set the documented protected count from the actual sealed result, avoiding a
# guessed summary count while leaving the result and original checkpoint intact.
p=TREE/target/'README.md';p.write_bytes(p.read_bytes().replace(b'1,608 protected',format(result['protected_files_rehashed_unchanged'],',').encode()+b' protected'))
materializer='''from pathlib import Path
import argparse,gzip,hashlib,json,os
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
r=Path(__file__).resolve().parent;j=json.loads((r/'publication-layout.json').read_text())['payload_mapping'][0]
z=r/j['stored_path'];assert z.stat().st_size==j['stored_bytes'] and hashlib.sha256(z.read_bytes()).hexdigest()==j['stored_sha256']
assert not a.output.exists() and not a.output.is_symlink()
a.output.parent.mkdir(parents=True,exist_ok=True);tmp=a.output.with_name(a.output.name+'.partial');h=hashlib.sha256();size=0
owned=False
try:
 with gzip.open(z,'rb') as src,tmp.open('xb') as dst:
  owned=True
  while b:=src.read(1024*1024):dst.write(b);h.update(b);size+=len(b)
 assert size==j['original_bytes'] and h.hexdigest()==j['original_sha256']
 os.chmod(tmp,j['original_mode']);os.link(tmp,a.output);tmp.unlink();owned=False
except BaseException:
 if owned and tmp.exists():tmp.unlink()
 raise
print(json.dumps({'path':str(a.output),'bytes':size,'sha256':h.hexdigest()}))
'''
save(target+'/materialize_retained_classes.py',materializer.encode())
checks[target]=dict(original_checkpoint_sha256=sha(cpraw),original_declared_files=10,eligible_files=0,all_retained=True,compressed_member_mapping=layout['payload_mapping'])
prefixes.append(target)

target='docs/verification/storage-cleanup/publisher-transport/01-exact-published-json-duplicates'
for p in sorted((BASE/'transport-retirement').iterdir()):
 if p.is_file():link(p,target+'/'+p.name)
r=json.loads((BASE/'transport-retirement/receipt.json').read_text())
assert r['zero_placeholders']==58 and r['all_authoritative_repository_bytes_and_modes_unchanged']
assert r['free_bytes_before']==r['free_bytes_after']==0
save(target+'/README.md',b'''# Exact published JSON transport duplicates

This closed bounded operation verified 58 publisher-owned JSON staging files
against exact Git objects in fetched commit a58c9560d0658e29c63bedb97c748d41a107e421
and unchanged authoritative repository files, including modes. Each selected
staging file had one link and a distinct inode from its authoritative copy.
Only these verified transport duplicates were truncated to zero-byte placeholders.

All repository files, source/checkpoint originals, APKs, archives and Git history
were preserved. The full before inventory and executed verifier/operation code
are included. The observed allocated total was 10,743,808 bytes, but free space
was zero both before and after. No reclaimed-capacity or persistent-absence claim
is made. JSON text transport wrappers were excluded because their wrapper bytes
were not themselves proven to be a fetched Git object.
''')
checks[target]=dict(files=58,observed_allocated_bytes=10743808,free_bytes_before=0,free_bytes_after=0,authoritative_copies_unchanged=True)
prefixes.append(target)

source=Path('/dev/shm/macrodroid-readiness-counterexample-g7iqur_y')
target='docs/verification/notification-readiness/01-independent-counterexamples'
raw=(source/'checkpoint.json').read_bytes();assert sha(raw)=='dcbb18a66a636718edc2bb680298e82db8464fb0d4905e6d2e73563ab039658a';cp=json.loads(raw)
assert not cp['activeSourceChanged'] and not cp['activeRegistryChanged'] and not cp['androidExecuted']
for row in cp['sourceFiles']+cp['readableEvidenceFiles']:
 p=source/safe(row['path']);b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'];mode_of(row,p);link(p,target+'/'+row['path'])
a=cp['evidenceArchive'];p=source/safe(a['path']);b=p.read_bytes();assert len(b)==a['bytes'] and sha(b)==a['sha256'];mode_of(a,p);link(p,target+'/'+a['path'])
with tarfile.open(p,'r:gz') as z:
 allmembers=z.getmembers();assert all(m.isfile() or m.isdir() for m in allmembers)
 members={safe(m.name):m for m in allmembers if m.isfile()};assert len(members)==len([m for m in allmembers if m.isfile()])==len(cp['evidenceFiles'])==16
 for row in cp['evidenceFiles']:
  m=members[safe(row['path'])];data=z.extractfile(m).read();assert len(data)==row['bytes'] and sha(data)==row['sha256'] and (m.mode&0o777)==int(row['mode'],8)
link(source/'checkpoint.json',target+'/checkpoint.json')
checks[target]=dict(checkpoint_sha256=sha(raw),source_files=6,readable_reports=9,archive_members=16,archive_sha256=a['sha256'],all_member_modes_and_hashes_verified=True,android_executed=False)
prefixes.append(target)

ops='docs/verification/repository-publication/2026-10-12-tmpfs-space-evidence'
for p in [Path(__file__),BASE/'verification-repository-setup.json',*[p for p in (BASE/'current-commit-verification').iterdir() if p.is_file()]]:
 link(p,ops+'/'+p.name)
jsave(ops+'/publication-scope.json',dict(parent=PARENT,prepared_utc=datetime.now(timezone.utc).isoformat(),existing_source_repository_read_only=True,temporary_storage_for_publication=True,active_application_apk_or_workflow_changes=False,checks=checks))
prefixes.append(ops)

baselines={}
ignored=subprocess.run(['git','check-ignore','--stdin','-z'],cwd=REPO,input=b'\0'.join(p.encode() for p in sorted(paths))+b'\0',capture_output=True)
assert ignored.returncode in (0,1)
names=[v.decode() for v in ignored.stdout.split(b'\0') if v]
if names:
 old=git('show',PARENT+':.gitignore');baselines['.gitignore']=sha(old)
 save('.gitignore',old+('\n# Exact closed memory-staged evidence\n'+''.join('!'+p+'\n' for p in names)).encode())
old=git('show',PARENT+':.gitattributes');baselines['.gitattributes']=sha(old)
save('.gitattributes',old+('\n# Preserve exact closed memory-staged evidence bytes\n'+''.join(p+'/** -text\n' for p in prefixes)).encode())
known={row.split(b' ',1)[0].decode() for row in git('rev-list','--objects','--all').splitlines()}
manifest=[];blobs=[];texts=[]
for name in sorted(paths):
 p=TREE/name;b=p.read_bytes();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();row=dict(path=name,local_path=str(p),size_bytes=len(b),sha256=sha(b),git_blob_sha1=oid,mode='100755' if p.stat().st_mode&0o111 else '100644');manifest.append(row)
 try:content=b.decode('utf-8');binary='\0' in content
 except UnicodeDecodeError:binary=True
 if oid in known or binary or len(b)>250000:blobs.append(row|dict(known=oid in known,encoding='base64'))
 else:texts.append(dict(path=name,mode=row['mode'],type='blob',content=content))
chunks=[];chunk=[]
for entry in texts:
 if chunk and len(json.dumps(chunk+[entry],ensure_ascii=False).encode())>650000:chunks.append(chunk);chunk=[]
 chunk.append(entry)
if chunk:chunks.append(chunk)
for i,c in enumerate(chunks):(EXPORT/('text-'+str(i).zfill(2)+'.json')).write_text(json.dumps(c,ensure_ascii=False))
for name,j in [('manifest.json',manifest),('blobs.json',blobs)]: (EXPORT/name).write_text(json.dumps(j,indent=2)+'\n')
prep=dict(parent=PARENT,files=len(manifest),bytes=sum(r['size_bytes'] for r in manifest),text_chunks=len(chunks),baselines=baselines,new_unique_blobs=len({r['git_blob_sha1'] for r in blobs if not r['known']}),checks=checks,active_source_apk_or_workflows_changed=False)
(EXPORT/'preparation.json').write_text(json.dumps(prep,indent=2)+'\n');print(json.dumps(prep))
