from pathlib import Path, PurePosixPath
import hashlib
import gzip
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'closed-followups-transfer'
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

art_local='widget-art-probe/checkpoints/08-hosted-complete-proof'
art_prefix='work-in-progress/widget-art/08-hosted-complete-proof'
art=package(art_local,art_prefix,'23a97a9998764b24cedca03f47bcaf8569fbd9ca27a642b5481c8b9f2fa19baa','visible_files')
assert len(art['visible_files'])==189 and art['actual_probe_status']=='ART_WIDGET_CASES_VERIFIED'
assert art['actual_job_success'] is True and art['complete_artifact_input_copy_audit_passed'] is True
assert art['archived_input_copies']==19 and art['recorded_commands_verified']==60 and art['raw_streams_verified']==120
assert art['full_runtime_1_to_1_established'] is False and art['widget_rendering_verified'] is False and art['nonempty_widget_behavior_verified'] is False
archive_path=ROOT/art_local/'artifact.zip';archive_data=archive_path.read_bytes()
assert len(archive_data)==art['archive']['bytes']==4780068 and sha(archive_data)==art['archive']['sha256']=='ad8b7f1e9e6ecc34c2b32199da0c7d777298a9a2cf8a89a464eff5779d2d1cc5'
with zipfile.ZipFile(archive_path) as z:
 members={safe(item.filename):item for item in z.infolist()}
 assert len(members)==len(z.infolist())==len(art['archive_members'])==7214
 for row in art['archive_members']:
  data=z.read(members[safe(row['path'])]);assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
 for row in art['visible_files']:
  if row['path'].startswith('extracted/'):
   assert (ROOT/art_local/row['path']).read_bytes()==z.read(members[row['path'][len('extracted/'):]]),row['path']
 hidden=z.read(members['executed-inputs/.github/workflows/widget-method-probe.yml'])
 assert sha(hidden)=='f0d210cc3f877f407a33df84e7e15b3e5a9179288ffb640e3aabf9eb499fffba'
 assert hidden==subprocess.check_output(['git','show','dbbb89cf4ca65edd3d2c2b96151dadf41aaec514:.github/workflows/widget-method-probe.yml'],cwd=REPO)
for row in art['historical_evidence_unchanged']:
 p=ROOT/'widget-art-probe'/row['path'];data=p.read_bytes();assert len(data)==row['bytes'] and sha(data)==row['sha256']
jsave(art_prefix+'/manifest.json',dict(format='macrodroid-multipart-artifact',format_version=1,id='widget-art08-complete-actual-guest-proof',
 filename='widget-art-run-38209599059.zip',media_type='application/zip',purpose='Unmodified complete actual Android Widget eight-case probe archive, including all nineteen executed input copies.',
 size_bytes=len(archive_data),sha256=sha(archive_data),parts=[dict(path=art_prefix+'/artifact.zip',size_bytes=len(archive_data),sha256=sha(archive_data),git_blob_sha1=oid(archive_data))]))
jsave(art_prefix+'/publication-verification.json',dict(frozen_visible_files_verified=189,complete_unmodified_zip_members_verified=7214,
 visible_extracted_bytes_match_archive=True,archived_hidden_workflow_matches_published_dbbb_commit=True,
 all_four_historical_checkpoint_and_archive_hashes_unchanged=True,actual_eight_case_probe_verified=True,
 complete_archived_input_copy_audit_passed=True,new_android_commands_by_publisher=False,full_runtime_1_to_1_established=False))
receipts[art_prefix].update(archive_members=7214,actual_probe_and_complete_archive_passed=True,active_apk_promoted=False)

for local,target,digest in [
 ('trigger-catalog-forward/checkpoints/03-initial-chronology-test-failure','work-in-progress/trigger-category/03-initial-chronology-test-failure','b71e143aca19c3223ff5465550352b6216450dbe2779e8627e591d9e9b646bbc'),
 ('trigger-catalog-forward/checkpoints/04-chronology-host-success','work-in-progress/trigger-category/04-chronology-host-success','8aa91588f809c8dc7bfbf88aaf6d96a130fd72502f10076e94043c6e23dc23af'),
 ('trigger-category-review/corrected-guard-review','docs/verification/capture-order-review/02-hardlink-review','ea2b726a2689d4c4efc8a1200a5c3a2ca90dc613ff17c42e87901b819d951ce5'),
 ('tooling-validation/avd-retirement-2026-10-12','docs/verification/android-environment/avd-retirement-2026-10-12','9d17a0fc1ef5bd5945b4694b1f644e5a1b09f568f2d4d1e3198ce85324e57c2f'),
 ('tooling-validation/process-guard-availability-2026-10-12','docs/verification/android-environment/avd-retirement-2026-10-12/process-guard-followup','b4fb68b52d5c07aff3b408b1549eba24edd036cef57050ad88d603a6fef2d623'),
 ('session-guard-forward/checkpoints/01-against-934c654','work-in-progress/editor-session-chronology/01-against-934c654','8188ececa77e2df83b816465e7b8e94aa680150f7dc3b94b22562c578adc4f93'),
 ('session-guard-forward/checkpoints/02-against-4745809','work-in-progress/editor-session-chronology/02-against-4745809','b0b6929d2962d6c505cbfb68e73828365b111610969ea6fc5a9ab18a6c3e2bd1')]:
 cp=package(local,target,digest)
 assert not cp.get('active_files',[]) and not cp.get('active_changes',False)

for local,target,digest in [
 ('video-monitor-recovery/checkpoints/01-original-assessment','work-in-progress/video-monitor/01-original-assessment','b367416660ecca26762c0c3e0323de738cb136258817ed219ba78e7d75597029'),
 ('video-monitor-recovery/checkpoints/02-draft-compile','work-in-progress/video-monitor/02-draft-compile','38656eed5691a48b8a11dc5148dd692e813b629141cad9ece604f0588a0311ea'),
 ('video-monitor-recovery/checkpoints/03-original-jvm-coverage-gap','work-in-progress/video-monitor/03-original-jvm-coverage-gap','48932d02bd05ea3dc319be19b4cc902cd0e170b5a6bc4aeaf6051ae4e1d3bbc5')]:
 cp=package(local,target,digest);assert cp['registered'] is False and cp['android_executed'] is False
 tar_bundle(cp,target)

retirement_prefix='docs/verification/storage-cleanup/20261012-validation-placeholder-retirement'
raw=(ROOT/'transfer-validation-assessment/retirement-checkpoint.json').read_bytes()
assert sha(raw)=='61ee99c111911c9ab4bab29fdb704d6b8c2c3b6922a67c24f52a0136dfe277cd'
cp=json.loads(raw)
for row in cp['files']:
 p=ROOT/'transfer-validation-assessment'/safe(row['path']);data=p.read_bytes()
 assert len(data)==row['bytes'] and sha(data)==row['sha256'];save(retirement_prefix+'/'+row['path'],data,int(row['mode'],8)&0o777)
save(retirement_prefix+'/checkpoint.json',raw)
receipt=json.loads((REPO/retirement_prefix/'placeholder-retirement/receipt.json').read_text())
metadata=gzip.decompress((REPO/retirement_prefix/'placeholder-retirement/full-before-after.json.gz').read_bytes())
assert len(metadata)==receipt['full_before_after_metadata_bytes']==31711364
assert sha(metadata)==receipt['full_before_after_metadata_sha256']=='3107f1240a46153090b9cedafe2e20f9beffcd72f5c0a1885ed9a309dbbf5ff4'
rows=json.loads(metadata);assert len(rows)==60809 and all(row['after']['bytes']==0 and row['after']['allocated_bytes']==0 for row in rows)
assert receipt['protected_source_and_evidence_files_rehashed']==909 and receipt['protected_hashes_unchanged'] is True
save(retirement_prefix+'/README.md',b'# Closed validation payload retirement with exact provenance\n\nThe final operation retired only payloads in transfer-validation and overlay-bootstrap-validation after every original file matched the already committed source/toolchain archive inventory. Each of the 60,809 paths was atomically replaced by a zero-byte placeholder; names deliberately remain and these validation copies are no longer usable project materializations. Authoritative archives and active source are retained.\n\nThe first stricter attempt stopped before deletion because other processes cwd/fd views were denied. The next approved guarded deletion verified all payloads but stopped when paths reappeared. Both exact scripts, available process/retained-file records and reported failures are preserved. No permission or infrastructure setting was changed.\n\nThe approved final criterion used explicit closure confirmations from all four task owners and two readable physical-process comm/argv inventories while other agent writes were paused. Unavailable cwd/fd checks are recorded as unavailable, not passed. After replacement, all 60,809 files were zero-length with zero allocated file blocks, and all 909 selected original/source/evidence hashes remained unchanged.\n\nThe full before/after per-file metadata is compressed in placeholder-retirement/full-before-after.json.gz; its uncompressed size and SHA-256 are in the final receipt. It binds 913,364,812 original logical bytes and 1,056,043,008 allocated file bytes to the previously published exact archive inventory. Observed free space increased by 1,050,210,304 bytes to 1,297,334,272 bytes at the final check, with concurrent private acceptance work explicitly noted. No continuing absence or permanent free-space claim is made.\n')
prefixes.append(retirement_prefix);receipts[retirement_prefix]=dict(files=60809,protected_hashes_unchanged=909,paths_remain_as_placeholders=True,prior_failures_preserved=True)

ops='docs/verification/repository-publication/2026-10-12-closed-followups';ops_rows=[]
for p in [ROOT/'prepare_closed_followups_transfer.py',*[ROOT/'widget-art06-transfer'/name for name in ['manifest.json','blobs.json','preparation.json','external-preservation.json','preserve_incoming.py','verify_remote.py','remote-verification.json']]]:
 name='scripts/'+p.name if p.parent==ROOT else 'closed/widget-art06-transfer/'+p.name;data=p.read_bytes();save(ops+'/'+name,data)
 ops_rows.append(dict(path=name,source_path=p.relative_to(ROOT).as_posix(),bytes=len(data),sha256=sha(data)))
jsave(ops+'/checkpoint.json',dict(scope='Exact publication scripts and completed fetched verification records',files=ops_rows,previous_verified_commit='dbbb89cf4ca65edd3d2c2b96151dadf41aaec514'))

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
    baselines=baselines, receipts=receipts, active_workflow_modified=False, active_app_or_apk_modified=False)
(EXPORT / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
