from pathlib import Path, PurePosixPath
import hashlib
import gzip
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'day-source-storage-transfer'
EXPORT.mkdir(exist_ok=True)
paths = set()
receipts = {}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def oid(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def safe(name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts
    return p.as_posix()

def save(name, data, mode=0o644):
    name = safe(name)
    p = REPO / name
    assert not p.is_symlink() and (not p.exists() or p.read_bytes() == data), name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    p.chmod(mode)
    paths.add(name)

def jsave(name, value):
    save(name, (json.dumps(value, indent=2) + '\n').encode())

def copy_checkpoint(source, prefix, expected_sha, list_key='files'):
    raw = (source / 'checkpoint.json').read_bytes()
    assert sha(raw) == expected_sha
    cp = json.loads(raw)
    for row in cp[list_key]:
        p = source / safe(row['path'])
        data = p.read_bytes()
        assert not p.is_symlink()
        assert len(data) == row.get('bytes', row.get('size_bytes')) and sha(data) == row['sha256'], row['path']
        mode = '100755' if p.stat().st_mode & 0o111 else '100644'
        if 'mode' in row:
            recorded = row['mode']
            if type(recorded) is int:
                assert recorded == p.stat().st_mode & 0o777, row['path']
            elif isinstance(recorded, str) and recorded.startswith('0o'):
                assert int(recorded, 8) == p.stat().st_mode & 0o777, row['path']
            else:
                assert recorded == mode, row['path']
        target_name = prefix + '/' + row['path']
        target = REPO / safe(target_name)
        assert not target.is_symlink()
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert target.samefile(p) and target.read_bytes() == data, target_name
        else:
            os.link(p, target)
        # These are closed immutable checkpoint files, never active inputs.
        # Do not chmod or write through either link; distinct source files
        # are not coalesced based on their contents.
        paths.add(target_name)
    save(prefix + '/checkpoint.json', raw)
    return cp

prefixes=[]

def package(local, target, digest, key='files'):
 cp=copy_checkpoint(ROOT/local,target,digest,key)
 prefixes.append(target)
 receipts[target]=dict(files=len(cp[key]),checkpoint_sha256=digest)
 return cp

def tar_bundle(cp,target):
 source=Path(cp['evidence_bundle']['path']);data=source.read_bytes()
 assert len(data)==cp['evidence_bundle']['bytes'] and sha(data)==cp['evidence_bundle']['sha256']
 path=target+'/evidence-archive/complete-evidence.tar.gz';save(path,data)
 jsave(target+'/evidence-archive/manifest.json',dict(format='macrodroid-multipart-artifact',format_version=1,id=target.replace('/','-'),
 filename='complete-evidence.tar.gz',media_type='application/gzip',purpose='Exact closed inactive study evidence with the original checkpoint scope preserved.',
 size_bytes=len(data),sha256=sha(data),parts=[dict(path=path,size_bytes=len(data),sha256=sha(data),git_blob_sha1=oid(data))]))
 with tarfile.open(source,'r:gz') as archive:
  members={safe(item.name):item for item in archive.getmembers() if item.isfile()}
  assert len(members)==len(cp['evidence_files'])
  assert all(item.isfile() or item.isdir() for item in archive.getmembers())
  for row in cp['evidence_files']:
   data=archive.extractfile(members[safe(row['path'])]).read()
   assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
   save(target+'/evidence/'+row['path'],data,0o755 if members[row['path']].mode & 0o111 else 0o644)
 receipts[target]['complete_archive_members']=len(cp['evidence_files'])

import os

for local,target,digest in [
 ('combined-cache-inventory/checkpoints/01-generated-metadata',
  'docs/verification/storage-cleanup/combined-generated-cache/01-metadata-survey',
  '076a59cb3924674a9fefa740afebbea36e86549b67b521d33ea42562a1476f93'),
 ('day-trigger-integration/checkpoints/04-source-acceptance-integration',
  'work-in-progress/day-trigger-numeric/06-source-integration',
  'c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f'),
]:
 cp=package(local,target,digest)
 assert cp['active_files'] == []

local='day-trigger-lookup-review/checkpoints/01-independent-three-path-review'
target='docs/verification/day-trigger-lookup/01-independent-three-path-review'
digest='7614752b03e2c34c64cedcef8bf82c73dfaafe6a859fe4e7e85fd76cfdde2a78'
cp=package(local,target,digest,'sourceFiles')
copy_checkpoint(ROOT/local,target,digest,'readableEvidenceFiles')
assert all(cp[name] is False for name in ['activeSourceChanged','activeRegistryChanged','apkChanged','androidExecuted'])
a=cp['evidenceArchive'];p=ROOT/local/safe(a['path']);data=p.read_bytes()
assert len(data)==a['bytes'] and sha(data)==a['sha256'] and int(a['mode'],8)==p.stat().st_mode & 0o777
save(target+'/'+a['path'],data,int(a['mode'],8))
with tarfile.open(p,'r:gz') as archive:
 allmembers=archive.getmembers()
 assert all(m.isfile() or m.isdir() for m in allmembers)
 members={safe(m.name):m for m in allmembers if m.isfile()}
 assert len(members)==len([m for m in allmembers if m.isfile()])==len(cp['evidenceFiles'])==100
 for row in cp['evidenceFiles']:
  m=members[safe(row['path'])];b=archive.extractfile(m).read()
  assert len(b)==row['bytes'] and sha(b)==row['sha256'] and m.mode & 0o777 == int(row['mode'],8),row['path']
receipts[target].update(readable_files=len(cp['readableEvidenceFiles']),complete_archive_members=100,archive_sha256=a['sha256'],all_modes_and_hashes_verified=True)
jsave(target+'/publication-verification.json',dict(checkpoint_sha256=digest,source_files=len(cp['sourceFiles']),readable_files=len(cp['readableEvidenceFiles']),exact_archive_members=100,
 archive_sha256=a['sha256'],original_archive_unchanged=True,all_member_modes_and_hashes_verified=True,active_files=[],android_executed=False))

ops='docs/verification/repository-publication/2026-10-12-day-source-and-storage'
for p in [ROOT/'prepare_day_source_storage_transfer.py',
 *[ROOT/'daytime13-analysis-transfer'/name for name in ['manifest.json','blobs.json','preparation.json','publication_guard.py','publication-guard.json','external-preservation.json','verify_remote.py','remote-verification.json']]]:
 name=('scripts/' if p.suffix=='.py' else 'receipts/')+p.parent.name+'-'+p.name
 save(ops+'/'+name,p.read_bytes())
prefixes.append(ops)

baselines = {}
ignored_result = subprocess.run(['git', 'check-ignore', '--stdin', '-z'], cwd=REPO,
    input=b'\0'.join(name.encode() for name in sorted(paths)) + b'\0', capture_output=True)
assert ignored_result.returncode in (0, 1)
ignored = [name.decode() for name in ignored_result.stdout.split(b'\0') if name]
if ignored:
    path = REPO / '.gitignore'
    old = path.read_bytes(); baselines['.gitignore'] = sha(old)
    path.write_bytes(old + ('\n# Exact closed runtime and guard-review evidence\n' + ''.join('!' + name + '\n' for name in ignored)).encode())
    paths.add('.gitignore')
path = REPO / '.gitattributes'
old = path.read_bytes(); baselines['.gitattributes'] = sha(old)
rules = '\n# Preserve exact raw device, protocol and synthetic evidence bytes\n'
rules += ''.join(prefix + '/** -text\n' for prefix in prefixes)
path.write_bytes(old + rules.encode()); paths.add('.gitattributes')

known = {line.split(b' ', 1)[0].decode() for line in subprocess.check_output(['git', 'rev-list', '--objects', '--all'], cwd=REPO).splitlines()}
manifest = []; blobs = []; texts = []
for name in sorted(paths):
    p = REPO / name; data = p.read_bytes()
    row = dict(path=name, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data), mode='100755' if p.stat().st_mode & 0o111 else '100644')
    manifest.append(row)
    try:
        content = data.decode('utf-8'); binary = '\0' in content
    except UnicodeDecodeError:
        binary = True
    if row['git_blob_sha1'] in known or binary or len(data) > 250000:
        blobs.append(row | dict(known=row['git_blob_sha1'] in known, encoding='utf-8' if len(data) > 12500000 and data.isascii() else 'base64'))
    else:
        texts.append(dict(path=name, mode=row['mode'], type='blob', content=content))
chunks = []; chunk = []
for entry in texts:
    if chunk and len(json.dumps(chunk + [entry], ensure_ascii=False).encode()) > 650000:
        chunks.append(chunk); chunk = []
    chunk.append(entry)
if chunk:
    chunks.append(chunk)
for index, chunk in enumerate(chunks):
    (EXPORT / f'text-{index:02d}.json').write_text(json.dumps(chunk, ensure_ascii=False))
for name, data in [('manifest.json', manifest), ('blobs.json', blobs)]:
    (EXPORT / name).write_text(json.dumps(data, indent=2) + '\n')
result = dict(files=len(manifest), bytes=sum(row['size_bytes'] for row in manifest), text_chunks=len(chunks),
    text_entries=len(texts), new_unique_blobs=len({row['git_blob_sha1'] for row in blobs if not row['known']}),
    baselines=baselines, receipts=receipts, active_workflow_modified=False, active_app_or_apk_modified=False)
(EXPORT / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))

