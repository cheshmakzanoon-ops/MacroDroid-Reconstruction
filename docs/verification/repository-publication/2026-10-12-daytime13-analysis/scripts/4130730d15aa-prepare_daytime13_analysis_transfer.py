from pathlib import Path, PurePosixPath
import hashlib
import gzip
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'daytime13-analysis-transfer'
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
 ('ci-run-analysis/checkpoints/06-daytime13-original-process-failure',
  'docs/verification/android-day-time-trigger-e610d98/analysis',
  '7b3fd99fed8b5871446ab443c4f373e04b5d882d12ffdda09d1d229a48532787'),
 ('day-trigger-integration/checkpoints/03-targeted-numeric-integration',
  'work-in-progress/day-trigger-numeric/05-targeted-integration',
  '81f44192b6c8862938d952ec9b5b37368c9a32d7d31e0c5ca9391b3ebbe975bc'),
]:
 cp=package(local,target,digest)
 assert cp['active_files'] == []

local='ink-indicator-study/checkpoints/01-source-and-ordering-dossier'
target='docs/verification/indicator-timing/01-source-and-ordering-dossier'
digest='00cde07343d7d7a106171070b462b4b2879705d3f926f6f22abcaae90a97fce3'
cp=package(local,target,digest,'source_files')
copy_checkpoint(ROOT/local,target,digest,'review_evidence_files')
assert cp['cause_proven'] is False and cp['android_proposal_executed'] is False
assert cp['active_source_policy_registry_or_apk_modified'] is False
archive_row=cp['evidence_archive']
a=ROOT/local/safe(archive_row['path']); b=a.read_bytes()
assert len(b)==archive_row['bytes'] and sha(b)==archive_row['sha256']
assert a.stat().st_mode & 0o777 == archive_row['mode']
save(target+'/'+archive_row['path'],b,archive_row['mode'])
member_checks=[]
with tarfile.open(a,'r:gz') as archive:
 members=archive.getmembers()
 assert all(m.isfile() or m.isdir() for m in members)
 files={safe(m.name):m for m in members if m.isfile()}
 assert len(files)==len([m for m in members if m.isfile()])==cp['evidence_member_count']==len(cp['evidence_members'])
 for row in cp['evidence_members']:
  m=files[safe(row['path'])]; data=archive.extractfile(m).read()
  assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
  assert m.mode & 0o777 == row['mode'],row['path']
  member_checks.append(row)
receipts[target].update(review_files=len(cp['review_evidence_files']),complete_archive_members=len(member_checks),
 archive_sha256=sha(b),archive_modes_and_hashes_verified=True)
jsave(target+'/publication-verification.json',dict(checkpoint_sha256=digest,
 source_files=len(cp['source_files']),review_files=len(cp['review_evidence_files']),
 evidence_archive_sha256=sha(b),all_archive_members_mode_size_hash_verified=len(member_checks),
 archive_recompressed=False,active_files=[],cause_proven=False,android_proposal_executed=False))

ops='docs/verification/repository-publication/2026-10-12-daytime13-analysis'
for p in [ROOT/'prepare_daytime13_analysis_transfer.py',
 *[ROOT/'daytime13-raw-transfer'/name for name in ['manifest.json','blobs.json','preparation.json',
 'publication_guard.py','publication-guard.json','external-preservation.json','verify_remote.py','remote-verification.json']]]:
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

