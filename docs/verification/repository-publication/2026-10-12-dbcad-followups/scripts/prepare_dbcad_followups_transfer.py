from pathlib import Path, PurePosixPath
import hashlib
import gzip
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'dbcad-followups-transfer'
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
            assert row['mode'] == mode, row['path']
        save(prefix + '/' + row['path'], data, int(mode, 8) & 0o777)
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


for local,target,digest in [
 ('ci-run-analysis/checkpoints/02-dbcad-session-actual','docs/verification/editor-journey/run-38214498414-attempt-1/analysis','1a75ee9e4988f72a0fab0fdde1851ccfc6ebef2e1ceafcf2c134e46dcd12e263'),
 ('ci-run-analysis/checkpoints/03-dbcad-editor-device-failure','docs/verification/editor-journey/run-38214498409-attempt-1/analysis','46b232aff98727dd6b7ea5d2527ed1901cb4b732459ae63a30bd9663e89d0927'),
]:
 cp=package(local,target,digest)
 assert cp['active_files']==[] and cp['key_scan_findings']==[]

for local,target,digest in [
 ('video-monitor-recovery/checkpoints/12-method-only-three-path','work-in-progress/video-monitor/12-method-only-three-path','1561b6af59ac41ea54da6b34df0f9c85af24d3d80c691763c8bb1de6c7c973fb'),
 ('video-monitor-recovery/checkpoints/13-retry-delay-original-jvm-coverage-gap','work-in-progress/video-monitor/13-retry-delay-original-jvm-coverage-gap','02f80d76ee2fcf9d9cacf38f4b8d0fdd9c8697934daa190aa9c3450ab7cfc6ac'),
 ('video-monitor-recovery/checkpoints/14-method-only-three-path-retry-delay','work-in-progress/video-monitor/14-method-only-three-path-retry-delay','5174cc11e51cc333f7b75042259aee15cf4cf5ff666eb733730351ef31d7e278'),
]:
 cp=package(local,target,digest)
 assert cp.get('raw_original_coverage_gate_passed',cp.get('full_original_coverage_gate_passed')) is False and cp['android_executed'] is False
 tar_bundle(cp,target)

for local,target,digest in [
 ('day-trigger-numeric-recovery/checkpoints/01-original-java-proof','work-in-progress/day-trigger-numeric/01-original-java-proof','6c78e9a5498e516f4a2b6f939055151fa2ab1d5585e12b77a4c991534593da0e'),
 ('day-trigger-numeric-recovery/checkpoints/02-three-path-and-compiled-controls','work-in-progress/day-trigger-numeric/02-three-path-and-compiled-controls','d93f08507afce1b6eebe1e3ae64338f86eb04ca01e26118bdd97f98f5d6af631'),
]:
 cp=package(local,target,digest,'sourceFiles')
 assert cp['activeRegistryChanged'] is False and cp['apkChanged'] is False
 a=cp['evidenceArchive']; original=ROOT/local/safe(a['path']); data=original.read_bytes()
 assert len(data)==a['bytes'] and sha(data)==a['sha256']
 save(target+'/'+a['path'],data)
 with tarfile.open(original,'r:gz') as archive:
  members={safe(m.name):m for m in archive.getmembers() if m.isfile()}
  assert all(m.isfile() or m.isdir() for m in archive.getmembers())
  assert len(members)==len(cp['evidenceFiles'])
  for row in cp['evidenceFiles']:
   member=members[safe(row['path'])]; data=archive.extractfile(member).read()
   assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
   save(target+'/evidence/'+row['path'],data,0o755 if member.mode&0o111 else 0o644)
 receipts[target]['complete_archive_members']=len(cp['evidenceFiles'])

ops='docs/verification/repository-publication/2026-10-12-dbcad-followups'
for p in [ROOT/'prepare_dbcad_followups_transfer.py',
 *[ROOT/'dbcad-evidence-transfer'/n for n in ['manifest.json','blobs.json','preparation.json','publication_guard.py','publication-guard.json','external-preservation.json','verify_remote.py','remote-verification.json']]]:
 name=('scripts/' if p.parent==ROOT else 'previous-evidence-publication/')+p.name
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

