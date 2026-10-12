#!/usr/bin/env python3
"""Fetch-verify an exact source ZIP, retire its closed duplicate, and materialize Git parts."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, tempfile

ROOT=Path('/workspace/scratch/4130730d15aa')
REPO=ROOT/'MacroDroid-Reconstruction'
EXPORT=ROOT/'dbcad-source-transfer'
SOURCE=ROOT/'tooling-validation/reconstruction-run-38214498395.zip'
PREFIX='docs/verification/source-ci-dbcad968'
COMMIT=sys.argv[1]
PARENT=sys.argv[2]

def git(*args):
    return subprocess.check_output(['git',*args],cwd=REPO)

def digest_file(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()

def write_json(path,value):
    path.write_text(json.dumps(value,indent=2)+'\n')

assert git('rev-parse',COMMIT+'^').decode().strip()==PARENT
assert subprocess.run(['git','merge-base','--is-ancestor',COMMIT,'origin/main'],cwd=REPO).returncode==0
rows=json.loads((EXPORT/'manifest.json').read_text())
virtual=json.loads((EXPORT/'virtual-blobs.json').read_text())
parts_by_path={r['path']:r for r in virtual}
assert len(parts_by_path)==23
manifest=json.loads((REPO/PREFIX/'manifest.json').read_text())
assert manifest['sha256']=='da5668cb030718c72a557179b3d38e33769531d497ec5e16d0a45ea2c8f53d88'
assert manifest['size_bytes']==188134390
assert len(manifest['parts'])==23
for index,part in enumerate(manifest['parts'],1):
    assert part['path']==PREFIX+'/archive/part-'+str(index).zfill(4)+'.bin'
    expected=parts_by_path[part['path']]
    assert all(part[key]==expected[key] for key in ['size_bytes','sha256','git_blob_sha1'])
tree={}
for raw in git('ls-tree','-rz','--full-tree',COMMIT).split(b'\0'):
    if raw:
        info,name=raw.split(b'\t',1); tree[name.decode()]=tuple(info.decode().split())
objects={}
for row in rows:
    assert tree[row['path']]==(row['mode'],'blob',row['git_blob_sha1']),row['path']
    if row['path'] not in parts_by_path:
        local=REPO/row['path']
        assert not local.is_symlink() and local.is_file(),row['path']
        assert local.stat().st_size==row['size_bytes'] and digest_file(local)==row['sha256'],row['path']
        assert ('100755' if local.stat().st_mode&0o111 else '100644')==row['mode'],row['path']
    objects.setdefault(row['git_blob_sha1'],[]).append(row)
p=subprocess.Popen(['git','cat-file','--batch'],cwd=REPO,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for oid,bound in objects.items():
    p.stdin.write((oid+'\n').encode());p.stdin.flush()
    actual,kind,size=p.stdout.readline().decode().strip().split()
    assert actual==oid and kind=='blob'
    data=p.stdout.read(int(size));assert p.stdout.read(1)==b'\n'
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==oid
    h=hashlib.sha256(data).hexdigest()
    for row in bound:
        assert len(data)==row['size_bytes'] and h==row['sha256'],row['path']
p.stdin.close();assert p.wait()==0

archive_hash=hashlib.sha256();total=0
for part in manifest['parts']:
    data=git('cat-file','blob',part['git_blob_sha1'])
    archive_hash.update(data);total+=len(data)
assert total==manifest['size_bytes'] and archive_hash.hexdigest()==manifest['sha256']
remote_receipt={'commit':COMMIT,'parent':PARENT,'verified_paths':len(rows),
 'verified_unique_git_blobs':len(objects),'all_git_modes_sizes_sha1_sha256_verified':True,
 'complete_ordered_archive_bytes':total,'complete_ordered_archive_sha256':archive_hash.hexdigest(),
 'archive_reassembly_verified_without_creating_another_zip':True,
 'source_job_success_does_not_relabel_the_separate_failed_android_job':True,
 'verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
write_json(EXPORT/'remote-byte-verification.json',remote_receipt)

# Root authorized retirement only after fetched container identity and owner closure.
# build_environment explicitly closed every ZIP reader after its independent1136-member review.
assert SOURCE.resolve()==SOURCE and SOURCE.is_file() and not SOURCE.is_symlink()
source_stat=SOURCE.stat()
assert source_stat.st_nlink==1 and source_stat.st_size==manifest['size_bytes']
assert digest_file(SOURCE)==manifest['sha256']
for name in parts_by_path:
    assert not (REPO/name).exists(),('part already exists; refuse unreviewed replacement',name)
protected_names=['README.md','project/README.md','project/reports/release-input-snapshot.json',
 'artifacts/current/manifest.json','artifacts/baseline/manifest.json',
 'vendor/original/manifest.json','vendor/v9/manifest.json']
protected={name:{'bytes':(REPO/name).stat().st_size,'sha256':digest_file(REPO/name)}
           for name in protected_names}
free_before=shutil.disk_usage(ROOT).free
fd,tmp=tempfile.mkstemp(prefix='.durable-source-download-retirement-',dir=SOURCE.parent)
try:
    os.fsync(fd);os.close(fd)
    assert SOURCE.stat().st_ino==source_stat.st_ino and SOURCE.stat().st_size==source_stat.st_size
    assert digest_file(SOURCE)==manifest['sha256']
    os.replace(tmp,SOURCE)
finally:
    if os.path.exists(tmp):
        os.unlink(tmp)
assert SOURCE.stat().st_size==0 and digest_file(SOURCE)==hashlib.sha256(b'').hexdigest()
retirement={'retired_only':str(SOURCE),'prior_bytes':source_stat.st_size,
 'prior_sha256':manifest['sha256'],'durable_commit':COMMIT,'durable_manifest':PREFIX+'/manifest.json',
 'fetched_complete_container_verified_before_retirement':True,
 'publisher_and_independent_reviewer_zip_handles_closed':True,
 'other_process_cwd_fd_visibility_not_claimed':True,
 'replacement_is_an_atomic_zero_byte_placeholder':True,
 'all_older_source_zip_containers_untouched':True,
 'free_bytes_before':free_before,'free_bytes_after_placeholder':shutil.disk_usage(ROOT).free,
 'protected_files':protected,
 'retired_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
write_json(EXPORT/'source-download-retirement.json',retirement)
for part in manifest['parts']:
    path=REPO/part['path'];path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as out:
        result=subprocess.run(['git','cat-file','blob',part['git_blob_sha1']],cwd=REPO,stdout=out)
    assert result.returncode==0
    path.chmod(0o644)
    assert path.stat().st_size==part['size_bytes'] and digest_file(path)==part['sha256']
assert {name:{'bytes':(REPO/name).stat().st_size,'sha256':digest_file(REPO/name)}
        for name in protected_names}==protected
retirement['all_protected_files_rehashed_unchanged']=True
retirement['repository_parts_materialized_from_verified_git']=len(manifest['parts'])
retirement['free_bytes_after_materialization']=shutil.disk_usage(ROOT).free
retirement['source_placeholder_observed_empty_after_materialization']=SOURCE.stat().st_size==0
write_json(EXPORT/'source-download-retirement.json',retirement)

names={r['path'] for r in rows}
pending=git('status','--porcelain=v1','-z','--untracked-files=all').split(b'\0')
i=0
while i<len(pending):
    item=pending[i];i+=1
    if not item: continue
    names.add(item[3:].decode())
    if b'R' in item[:2] or b'C' in item[:2]:
        names.add(pending[i].decode());i+=1
def fingerprint(name):
    path=REPO/name
    if path.is_symlink(): return ('symlink',path.readlink().as_posix())
    if not path.exists(): return None
    assert path.is_file(),name
    return (path.stat().st_mode&0o777,path.stat().st_size,digest_file(path))
before={name:fingerprint(name) for name in names}
for row in rows:
    assert before[row['path']][1:]==(row['size_bytes'],row['sha256']),row['path']
assert subprocess.run(['git','reset','--mixed',COMMIT],cwd=REPO,capture_output=True).returncode==0
assert {name:fingerprint(name) for name in names}==before
final=remote_receipt|{'materialized_parts':len(manifest['parts']),
 'retired_download_only_after_durability_and_reader_closure':True,
 'mixed_reset_preserved_fingerprints':len(before),
 'tree':git('rev-parse',COMMIT+'^{tree}').decode().strip(),
 'status':git('status','--short','--untracked-files=normal').decode(),
 'free_bytes':shutil.disk_usage(ROOT).free}
write_json(EXPORT/'remote-verification.json',final)
print(json.dumps(final))

