from pathlib import Path, PurePosixPath
import hashlib
import gzip
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'dbcad-evidence-transfer'
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

def raw_zip(source_zip, source_dir, receipt_path, prefix, member_count):
 raw=receipt_path.read_bytes();receipt=json.loads(raw)
 assert receipt['run_id']==38214498395 and receipt['head_sha']=='dbcad968c5c3e8f084205393a6c0d2d06a203c71'
 assert receipt['member_count']==len(receipt['files'])==member_count and not receipt['key_scan_findings']
 data=source_zip.read_bytes();assert len(data)==receipt['archive']['bytes'] and sha(data)==receipt['archive']['sha256']
 archive_name=prefix+'/artifact.zip';save(archive_name,data)
 save(prefix+'/extraction-receipt.json',raw)
 jsave(prefix+'/manifest.json',dict(format='macrodroid-multipart-artifact',format_version=1,
  id=prefix.replace('/','-'),filename=source_zip.name,media_type='application/zip',
  purpose='Exact unmodified hosted reconstruction evidence; preserve each recorded result and its finite scope.',
  size_bytes=len(data),sha256=sha(data),parts=[dict(path=archive_name,size_bytes=len(data),sha256=sha(data),git_blob_sha1=oid(data))],
  source_commit=receipt['head_sha'],run_id=38214498395,artifact_id=receipt['artifact_id'],whole_application_1_to_1_established=False))
 expected={r['path']:r for r in receipt['files']};seen=set();total=0
 with zipfile.ZipFile(source_zip) as archive:
  members=[m for m in archive.infolist() if not m.is_dir()]
  assert len(members)==member_count
  for member in members:
   name=safe(member.filename);assert name in expected and name not in seen
   assert (member.external_attr>>16)&0o170000!=0o120000
   data=archive.read(member);row=expected[name];assert len(data)==row['bytes'] and sha(data)==row['sha256'],name
   p=source_dir/name;assert not p.is_symlink() and p.read_bytes()==data
   save(prefix+'/extracted/'+name,data,0o755 if p.stat().st_mode&0o111 else 0o644)
   total+=len(data);seen.add(name)
 assert seen==set(expected) and total==receipt['expanded_bytes']
 jsave(prefix+'/publication-verification.json',dict(all_members_verified=member_count,expanded_bytes=total,
  archive_sha256=receipt['archive']['sha256'],all_raw_bytes_preserved=True,recompressed=False,executed_artifacts=False))
 prefixes.append(prefix);receipts[prefix]=dict(raw_members=member_count,bytes=total,archive_sha256=receipt['archive']['sha256'])

raw_prefix='docs/verification/android-ci-dbcad968'
raw_zip(ROOT/'tooling-validation/android-cold-launch-run-38214498395.zip',
 ROOT/'tooling-validation/hosted-run-38214498395',ROOT/'tooling-validation/hosted-run-38214498395-extraction.json',raw_prefix,426)
raw_zip(ROOT/'tooling-validation/android-tools-run-38214498395.zip',
 ROOT/'tooling-validation/hosted-tools-run-38214498395',ROOT/'tooling-validation/hosted-tools-run-38214498395-extraction.json',raw_prefix+'/host-tools',1)
save(raw_prefix+'/RAW_EVIDENCE.md',b'''# Unchanged promoted-candidate Android evidence

Run 38214498395 checked out the combined reconstruction at
dbcad968c5c3e8f084205393a6c0d2d06a203c71. Its Android job reported a failed
strict intro comparison while the separate constructor allocation probe passed.
The raw 426-file capture/ART artifact and separate one-file tooling-test artifact
are preserved unchanged with their original ZIPs and exact extraction receipts.
The complete source acceptance job is a different job in this workflow.

All original member paths are under `extracted/`; tooling host evidence is under
`host-tools/`. `manifest.json` and `host-tools/manifest.json` bind exact ZIP byte
streams for `scripts/assemble_artifact.py`. Derived replay and visual measurements
are separate from these original bytes. No whole-application parity is claimed.
''')

for local,target,digest in [
 ('video-monitor-recovery/checkpoints/10-compiled-controls','work-in-progress/video-monitor/10-compiled-controls','c8ba7485fb0a506e38c17cefdce190cd9c6c9765cf059a1b485f5f3719e14357'),
 ('video-monitor-recovery/checkpoints/11-method-dex-assembly-command-failure','work-in-progress/video-monitor/11-method-dex-assembly-command-failure','10a95d413d2d866f3668bff1621bf39a9c8873829e8800b135fdec6e51215dd5'),
]:
 cp=package(local,target,digest)
 assert cp['raw_original_coverage_gate_passed'] is False and cp['android_executed'] is False
 tar_bundle(cp,target)

package('combined-cache-retirement/checkpoints/02-retirement-receipt',
 'docs/verification/storage-cleanup/combined-cache-retirement/02-retirement-receipt',
 '230fcdf1ce755c35a69881abdceebaf8c97da60a6f5c62d7d1e47330e8985296')

ops='docs/verification/repository-publication/2026-10-12-dbcad-evidence'
for p in [ROOT/'prepare_dbcad_evidence_transfer.py',ROOT/'dbcad_evidence_body.py',
 *[ROOT/'zero-trigger-transfer'/n for n in ['manifest.json','blobs.json','preparation.json','activation-guards.json','publication_guard.py','external-preservation.json','verify_remote.py','remote-verification.json','initial-workflow-observation.json']]]:
 name=('scripts/' if p.parent==ROOT else 'previous-zero-workflow-publication/')+p.name
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
