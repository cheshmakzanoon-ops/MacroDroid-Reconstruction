from pathlib import Path, PurePosixPath
import hashlib
import gzip
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'daytime-activation-transfer'
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
            assert row['mode'] == ((p.stat().st_mode & 0o777) if type(row['mode']) is int else mode), row['path']
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

bulk = ROOT / 'zero12-evidence-transfer'
old = json.loads((bulk / 'preparation.json').read_text())
selected_prefixes = [
 'work-in-progress/day-time-trigger/01-host-plan-rejection-controls/',
 'work-in-progress/day-time-trigger/02-host-success/',
 'work-in-progress/day-time-trigger-workflow/01-zero-scale-workflow/',
 'docs/verification/day-time-trigger/01-source-and-zero12-review/',
 'docs/verification/day-time-trigger/02-workflow-independent-review/',
]
selected_exact = {'.gitattributes', '.gitignore', '.github/workflows/editor-day-time-trigger.yml'}
rows = json.loads((bulk / 'manifest.json').read_text())
paths = {row['path'] for row in rows if row['path'] in selected_exact or any(row['path'].startswith(p) for p in selected_prefixes)}
for row in rows:
 if row['path'] in paths:
  p = REPO / row['path']; data = p.read_bytes()
  assert len(data) == row['size_bytes'] and sha(data) == row['sha256']
  assert ('100755' if p.stat().st_mode & 0o111 else '100644') == row['mode']
baselines = old['baselines']
receipts = {k:v for k,v in old['receipts'].items() if any((k+'/').startswith(p) for p in selected_prefixes)}
ops = 'docs/verification/repository-publication/2026-10-12-daytime-activation'
save(ops + '/prepare_daytime_activation.py', (ROOT / 'prepare_daytime_activation.py').read_bytes())
jsave(ops + '/activation-scope.json', dict(
 workflow_path='.github/workflows/editor-day-time-trigger.yml',
 workflow_sha256='74ebef4583e28e345d91c8aa01c0e0723c57c13e6e209084f48e8423751ccbf3',
 guard_checkpoint_sha256='0e010cfbace03cffa6d45e8c9157402b1b68c9a392249eb2aeae39445dc57a7d',
 workflow_checkpoint_sha256='2510711052d2f41bde1a7a583e4bd42f1aab2e1f2001b3bd03d5e2b9eff29229',
 independent_workflow_review_sha256='5ef1a07e41645a3417e1451a95362ac479be4fc9a13bc2c32929012496ce8206',
 root_final_clearance_received=True, independent_review_passed=True,
 complete_guard_and_workflow_dependencies_published_together=True,
 prior_twelve_screen_workflow_modified=False, application_or_apk_modified=False,
 new_thirteen_screen_android_result_pending=True,
 bulk_zero12_and_video_evidence_preserved_locally_for_next_commit=True))
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
    baselines=baselines, receipts=receipts, active_workflow_modified=True, active_app_or_apk_modified=False)
(EXPORT / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))

