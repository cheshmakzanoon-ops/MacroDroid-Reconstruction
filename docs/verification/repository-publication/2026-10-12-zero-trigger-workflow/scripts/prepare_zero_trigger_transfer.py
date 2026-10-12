from pathlib import Path, PurePosixPath
import hashlib
import gzip
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'zero-trigger-transfer'
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

proposal_local=ROOT/'trigger-catalog-forward/checkpoints/08-zero-scale-twelve-screen-workflow'
proposal_prefix='work-in-progress/trigger-category-workflow/02-zero-scale-workflow'
proposal=package('trigger-catalog-forward/checkpoints/08-zero-scale-twelve-screen-workflow',proposal_prefix,
 'a6a279c48af61b553728eeaf05f92c8cf15e34bd5b4fdd907e193d31a63a5af0')
assert proposal['workflow_sha256']=='e3e53daf3c53c315605580aa49ff5d2ffda7c99b1dcb8014c5692dbfc22570fe'
assert not proposal['android_executed'] and not proposal['active_changes']
inventory=json.loads((proposal_local/'offline-evidence-manifest.json').read_text())
assert len(inventory['files'])==inventory['file_count']==5134 and inventory['unique_archived_payloads']==217
payloads={}
with tarfile.open(proposal_local/'offline-evidence-blobs.tar.gz','r:gz') as archive:
 for item in archive:
  if item.isdir():continue
  assert item.isfile() and safe(item.name)==item.name and item.name not in payloads
  data=archive.extractfile(item).read();assert item.name=='blobs/sha256/'+sha(data)+'.bin'
  payloads[item.name]=data
assert len(payloads)==217
external={}
for digest,row in inventory['exact_already_published_runtime_inputs'].items():
 path=Path(row['source']);data=path.read_bytes()
 assert not path.is_symlink() and sha(data)==row['sha256']==digest and len(data)==row['bytes']
 if row['durable_manifest']!='vendor/v9/manifest.json':
  value=json.loads(subprocess.check_output(['git','show',row['durable_commit']+':'+row['durable_manifest']],cwd=REPO))
  assert value['sha256']==digest and value['size_bytes']==len(data)
 else:
  found=False
  for z in (ROOT/'recovered/MacroDroid_v9_Source.zip',ROOT/'recovered/MacroDroid_v9_Toolchain.zip'):
   with zipfile.ZipFile(z) as archive:
    for n in archive.namelist():
     if n.endswith('/tools/prebuilt/linux/aapt2') or n=='tools/prebuilt/linux/aapt2':
      if archive.read(n)==data:found=True
  assert found
 external[digest]=dict(bytes=len(data),sha256=digest,durable_commit=row['durable_commit'],durable_manifest=row['durable_manifest'])
seen=set();used=set();readable=[]
for row in inventory['files']:
 name=safe(row['path']);assert name not in seen;seen.add(name)
 assert type(row['mode']) is int and row['mode']&~0o777==0
 if 'archive_member' in row:
  data=payloads[row['archive_member']];used.add(row['archive_member'])
  assert len(data)==row['bytes'] and sha(data)==row['sha256'],name
 else:
  ext=external[row['external_input_sha256']]
  assert row['bytes']==ext['bytes'] and row['sha256']==ext['sha256'];data=None
 if '/' not in name or name.startswith('commands/') or (name.startswith('private-inputs/ci-normal-animation/') and name.count('/')==2 and name.endswith('.log')):
  assert data is not None
  save(proposal_prefix+'/review-evidence/'+name,data,row['mode']);readable.append(row)
assert used==set(payloads)
jsave(proposal_prefix+'/publication-verification.json',dict(exact_checkpoint_preserved=True,complete_logical_evidence_files=5134,
 unique_archived_payloads=217,external_inputs=external,reviewable_members=readable,
 active_workflow_changed=False,android_executed=False,
 status='FROZEN_ZERO_SCALE_CAPSULE_PRESERVED_BEFORE_SEPARATE_AUTHORIZED_ACTIVATION'))

review_prefix='docs/verification/trigger-category-workflow/02-zero-scale-independent-review'
review=package('zero-trigger-review/checkpoints/01-independent-zero12-review',review_prefix,
 'a7d962e2f6080a35c16588b8a4aa8e1ce9c871ab4d09dda7d128495ae93691b0')
assert review['active_files']==[] and review['reviewed_checkpoint_sha256']=='a6a279c48af61b553728eeaf05f92c8cf15e34bd5b4fdd907e193d31a63a5af0'
workflow_path='.github/workflows/editor-trigger-category.yml'
assert not (REPO/workflow_path).exists() and not (REPO/workflow_path).is_symlink()
workflow=(proposal_local/workflow_path).read_bytes()
assert sha(workflow)=='e3e53daf3c53c315605580aa49ff5d2ffda7c99b1dcb8014c5692dbfc22570fe'
save(workflow_path,workflow)
roles=json.loads((REPO/review_prefix/'all-192-source-copy-roles.json').read_text())
assert len(roles)==192 and len({r['copy'] for r in roles})==192
for row in roles:
 path=REPO/safe(row['path']);data=path.read_bytes()
 assert not path.is_symlink() and len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
jsave(proposal_prefix+'/activation-verification.json',dict(
 active_files=[dict(path=workflow_path,expected_before='absent',bytes=len(workflow),sha256=sha(workflow))],
 independent_review_checkpoint_sha256='a7d962e2f6080a35c16588b8a4aa8e1ce9c871ab4d09dda7d128495ae93691b0',
 all192_source_copy_roles_rechecked=True,required_unchanged_repository_files=roles,
 original_apk_sha256='84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800',
 candidate_apk_sha256='5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182',
 immutable_candidate_commit='c9373851d4408fb4db63c21873ac2d0bb6867270',
 actual_zero_scale_runtime_result='pending',declared_full_frame_stills_per_apk=12,declared_inputs_per_apk=11,
 active_application_source_changed=False,active_apk_changed=False,full_runtime_1_to_1_established=False))
(EXPORT/'activation-guards.json').write_text(json.dumps(dict(absent_paths=[workflow_path],unchanged_files=roles),indent=2)+'\n')
receipts[proposal_prefix].update(complete_logical_evidence_files=5134,unique_archived_payloads=217,active_workflow_only=True)
ops='docs/verification/repository-publication/2026-10-12-zero-trigger-workflow'
for path in [Path(__file__),*[ROOT/'normal-failure-transfer'/name for name in ['manifest.json','preparation.json','external-preservation.json','preserve_incoming.py','verify_remote.py','remote-verification.json']],*[ROOT/'cache-assessment-transfer'/name for name in ['manifest.json','preparation.json','external-preservation.json','verify_remote.py','remote-verification.json']]]:
 name=('scripts/' if path.parent==ROOT else path.parent.name+'/')+path.name
 save(ops+'/'+name,path.read_bytes())
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
    baselines=baselines, receipts=receipts, active_workflow_modified=True, active_app_or_apk_modified=False)
(EXPORT / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
