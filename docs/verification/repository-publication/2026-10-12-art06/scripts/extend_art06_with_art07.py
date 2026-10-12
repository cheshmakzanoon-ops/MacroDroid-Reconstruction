from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'widget-art06-transfer'
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

old_preparation=json.loads((EXPORT/'preparation.json').read_text())
paths={row['path'] for row in json.loads((EXPORT/'manifest.json').read_text())}
baselines=old_preparation['baselines'];receipts=old_preparation['receipts']
source=ROOT/'widget-art-probe/checkpoints/07-hidden-input-capture'
prefix='work-in-progress/widget-art/07-hidden-input-capture'
cp=copy_checkpoint(source,prefix,'9e048428bebd58bb8726997eabd8633e223646db77ddbb51c92dd0b5911126ae')
assert len(cp['files'])==6 and len(cp['baseline_inputs'])==19 and cp['validation_passed'] is True
assert cp['android_executed'] is False and cp['uploader_executed'] is False
for row in cp['baseline_inputs']:
 data=(REPO/safe(row['path'])).read_bytes()
 assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
 assert data==subprocess.check_output(['git','show','55db6717d2ede0f1732b258d97d3106e23a33de5:'+row['path']],cwd=REPO)
archive_path=ROOT/'widget-art-probe/checkpoints/07-hidden-input-capture-evidence.tar.gz'
data=archive_path.read_bytes()
assert len(data)==cp['evidence_bundle']['bytes']==336285
assert sha(data)==cp['evidence_bundle']['sha256']=='6758d59880db109b704aa34f05fd719738dd84783cbc26759a9196d4bf3e4694'
archive_name=prefix+'/evidence-archive/complete-evidence.tar.gz';save(archive_name,data)
jsave(prefix+'/evidence-archive/manifest.json',dict(format='macrodroid-multipart-artifact',format_version=1,id='widget-art07-hidden-input-copy-review',
 filename='widget-art07-hidden-input-copy-review.tar.gz',media_type='application/gzip',purpose='Frozen offline review of the one-line owned hidden-input upload correction; fresh complete Android artifact remains pending.',
 size_bytes=len(data),sha256=sha(data),parts=[dict(path=archive_name,size_bytes=len(data),sha256=sha(data),git_blob_sha1=oid(data))]))
with tarfile.open(archive_path,'r:gz') as archive:
 members={safe(item.name):item for item in archive.getmembers()}
 assert len(members)==len(archive.getmembers())==len(cp['evidence_files'])==52
 assert all(item.isfile() for item in members.values())
 for row in cp['evidence_files']:
  data=archive.extractfile(members[safe(row['path'])]).read()
  assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
  save(prefix+'/evidence/'+row['path'],data,0o755 if members[row['path']].mode&0o111 else 0o644)
workflow_path='.github/workflows/widget-method-probe.yml'
old=(REPO/workflow_path).read_bytes();new=(source/workflow_path).read_bytes()
assert sha(old)==cp['baseline_workflow_sha256']=='b694b68e29dcb815c4dded4aed48773999f1800d5fd489dacbca067926ac32c7'
assert sha(new)==cp['workflow_sha256']=='f0d210cc3f877f407a33df84e7e15b3e5a9179288ffb640e3aabf9eb499fffba'
assert new.replace(b'          include-hidden-files: true\n',b'')==old
(REPO/workflow_path).write_bytes(new);(REPO/workflow_path).chmod(0o644);paths.add(workflow_path);baselines[workflow_path]=sha(old)
jsave(prefix+'/publication-verification.json',dict(source_paths_verified=6,exact_baseline_dependencies_verified=19,complete_evidence_members_verified=52,
 single_line_active_workflow_change_verified=True,active_workflow_sha256=sha(new),owned_upload_root='ci-widget-method/',historical_widget_art06_unchanged=True,
 fresh_android_artifact='PENDING',application_or_apk_modified=False))
receipts['widget-art07']=dict(source_paths=6,evidence_members=52,active_workflow=workflow_path,only_change='include-hidden-files: true for ci-widget-method/',fresh_result_pending=True)

assessment_prefix='docs/verification/storage-cleanup/20261012-validation-duplicates-assessment'
assessment_source=ROOT/'transfer-validation-assessment'
summary=json.loads((assessment_source/'assessment.json').read_text())
assert summary['no_files_removed'] is True and summary['verified_repository_commit']=='55db6717d2ede0f1732b258d97d3106e23a33de5'
assert sum(row['files'] for row in summary['targets'].values())==60809
assert all(row['files']==row['matched_durable_archive_files'] and not row['retained_unmatched'] for row in summary['targets'].values())
assessment_rows=[]
for original in [assessment_source/'assessment.json',assessment_source/'inventory.json.gz',ROOT/'assess_transfer_validation_duplicates.py']:
 data=original.read_bytes();save(assessment_prefix+'/'+original.name,data)
 assessment_rows.append(dict(path=original.name,bytes=len(data),sha256=sha(data)))
jsave(assessment_prefix+'/checkpoint.json',dict(status='READ_ONLY_ASSESSMENT_PRIOR_TO_APPROVED_RETIREMENT',files=assessment_rows,
 exact_roots=['overlay-bootstrap-validation','transfer-validation'],durable_files_matched=60809,no_files_removed_at_freeze=True,
 later_guarded_retirement_requires_durable_assessment_and_process_recheck=True))
save(assessment_prefix+'/README.md',b'# Closed validation duplicate assessment\n\nEvery one of the 60,809 files in the two closed publisher validation roots matches an exact member or full ZIP of the preserved v9 source or toolchain archives. The executed audit rehashed the fetched Git parts at commit 55db6717d2ede0f1732b258d97d3106e23a33de5, the complete authoritative ZIPs, and every candidate file. No unmatched files or symbolic links were found.\n\nThe complete per-file inventory is preserved as inventory.json.gz; its uncompressed SHA-256 and byte count are in assessment.json. The matches total 913,364,812 logical bytes and 1,056,043,008 allocated file bytes. Directory allocation is additional. This checkpoint is read-only: it records no deletion.\n\nThe approved follow-up may retire only overlay-bootstrap-validation and transfer-validation after this checkpoint is fetched and verified, all candidate bytes are rechecked, and no live process uses either root. Authoritative recovered archives, repository data, evidence, checkpoints, current source and the private running acceptance checkout are outside those roots and remain retained. The actual retirement and observed disk change will have a separate receipt.\n')
receipts['validation-duplicate-assessment']=dict(files=60809,matched_logical_bytes=913364812,matched_allocated_bytes=1056043008,no_files_removed=True)

ops='docs/verification/repository-publication/2026-10-12-art06'
script=ROOT/'extend_art06_with_art07.py';data=script.read_bytes();save(ops+'/scripts/'+script.name,data)
jsave(ops+'/extension-checkpoint.json',dict(scope='Exact approved ART07 and read-only duplicate assessment publication script',files=[dict(path='scripts/'+script.name,bytes=len(data),sha256=sha(data))]))
ignored_result=subprocess.run(['git','check-ignore','--stdin','-z'],cwd=REPO,input=b'\0'.join(name.encode() for name in sorted(paths))+b'\0',capture_output=True)
assert ignored_result.returncode in (0,1)
ignored=[name.decode() for name in ignored_result.stdout.split(b'\0') if name]
if ignored:
 p=REPO/'.gitignore';p.write_bytes(p.read_bytes()+('\n# Exact approved Widget archive correction and audit inputs\n'+''.join('!'+name+'\n' for name in ignored)).encode());paths.add('.gitignore')
p=REPO/'.gitattributes';p.write_bytes(p.read_bytes()+('\n# Exact Widget archive correction and validation inventories\n'+prefix+'/** -text\n'+assessment_prefix+'/** -text\n').encode());paths.add('.gitattributes')

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
        blobs.append(row | dict(known=row['git_blob_sha1'] in known, encoding='base64'))
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
    baselines=baselines, receipts=receipts, active_workflow_modified=workflow_path, active_app_or_apk_modified=False)
(EXPORT / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
