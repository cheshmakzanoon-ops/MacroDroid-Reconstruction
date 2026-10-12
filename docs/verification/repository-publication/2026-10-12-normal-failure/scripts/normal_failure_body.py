normal_root = ROOT / 'tooling-validation'
normal_zip = normal_root / 'normal-animation-run-38212813248.zip'
normal_receipt = normal_root / 'normal-animation-run-38212813248-extraction.json'
normal_extracted = normal_root / 'normal-animation-run-38212813248'
normal_prefix = 'docs/verification/android-normal-animation-3edcddd'
receipt_raw = normal_receipt.read_bytes(); receipt = json.loads(receipt_raw)
assert receipt['run_id'] == 38212813248 and receipt['head_sha'] == '3edcddd86660ea10c8aff71b651b446f86412525'
assert receipt['archive'] == dict(bytes=28080813, sha256='93cfed4c5f5c17170a926bd79781807422698c22b26cf7afc60430b2a7183d92')
assert len(receipt['files']) == receipt['member_count'] == 952 and not receipt['raw_key_scan_findings']
save(normal_prefix+'/extraction-receipt.json',receipt_raw)
parts=[];total=0;digest=hashlib.sha256()
with normal_zip.open('rb') as stream:
 while True:
  data=stream.read(8*1024*1024)
  if not data:break
  name=normal_prefix+'/archive/part-'+str(len(parts)+1).zfill(4)+'.bin'
  save(name,data);total+=len(data);digest.update(data)
  parts.append(dict(path=name,size_bytes=len(data),sha256=sha(data),git_blob_sha1=oid(data)))
assert total==receipt['archive']['bytes'] and digest.hexdigest()==receipt['archive']['sha256'] and len(parts)==4
jsave(normal_prefix+'/manifest.json',dict(format='macrodroid-multipart-artifact',format_version=1,
 id='normal-animation-run-38212813248',filename=normal_zip.name,media_type='application/zip',
 purpose='Unchanged failed actual normal-animation CI artifact; both APKs failed TRIGGERS consecutive-frame stabilization.',
 size_bytes=total,sha256=digest.hexdigest(),parts=parts,github_run_id=38212813248,
 github_job_id=114690610883,github_artifact_id=11730023332,source_commit=receipt['head_sha'],
 all_members_preserved=True,complete_ten_screen_comparison_passed=False))
expected={r['path']:r for r in receipt['files']};seen=set();expanded=0
with zipfile.ZipFile(normal_zip) as archive:
 members=[item for item in archive.infolist() if not item.is_dir()]
 assert len(members)==len(expected)==952
 for item in members:
  name=safe(item.filename);assert name in expected and name not in seen
  assert (item.external_attr>>16)&0o170000 != 0o120000
  data=archive.read(item);row=expected[name]
  assert len(data)==row['bytes'] and sha(data)==row['sha256'],name
  p=normal_extracted/name;assert not p.is_symlink() and p.read_bytes()==data,name
  save(normal_prefix+'/extracted/'+name,data,0o755 if p.stat().st_mode&0o111 else 0o644)
  expanded+=len(data);seen.add(name)
assert seen==set(expected) and expanded==receipt['expanded_bytes']==37695272
result=subprocess.run(['python3','scripts/assemble_artifact.py',normal_prefix+'/manifest.json','--verify-only'],cwd=REPO,capture_output=True,text=True)
assert result.returncode==0,result.stderr
jsave(normal_prefix+'/publication-verification.json',dict(archive_bytes=total,archive_sha256=digest.hexdigest(),
 raw_member_count=952,raw_member_bytes=expanded,all_raw_files_reverified_against_zip_and_download_inventory=True,
 artifact_recompressed=False,duplicate_archive_assembly_created=False,complete_ten_screen_comparison_passed=False,
 assembler=dict(exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr)))
save(normal_prefix+'/RAW_EVIDENCE.md',b'''# Exact normal-animation failure evidence

Run 38212813248 checked out commit 3edcddd86660ea10c8aff71b651b446f86412525 and
used the original and prior 9108 candidate. The recorder accepted intro-1 for both
APKs, then failed to acquire matching consecutive TRIGGERS frames at animation
scale 1. No complete ten-screen comparison passed. This run predates promotion of
the combined 5f635e candidate; it is not a result for that new candidate.

The unchanged downloaded ZIP is preserved in four parts. `manifest.json` pins the
28,080,813-byte archive and its GitHub run/job/artifact identity. Reconstruct it
with `scripts/assemble_artifact.py` from the repository root. Every one of its
952 original regular members is also preserved under `extracted/` and bound by
the exact `extraction-receipt.json`. No raw artifact was rewritten or relabeled.
Derived visual analysis is separate from these complete original bytes.
''')
prefixes.append(normal_prefix)
receipts[normal_prefix]=dict(run_id=38212813248,archive_parts=4,original_members=952,raw_bytes=expanded,actual_capture_complete=False)

for local,target,expected_sha in [
 ('video-monitor-recovery/checkpoints/06-compiled-cast-order-gap','work-in-progress/video-monitor/06-compiled-cast-order-gap','a55dcbd316ce139b64f43acc05444b21bcd18230ff1ddf21405462992c3d7192'),
 ('video-monitor-recovery/checkpoints/07-cast-source-original-jvm-coverage-gap','work-in-progress/video-monitor/07-cast-source-original-jvm-coverage-gap','06986104338d570dd78e4abf34f2691756f772c8f6e521769a9ebf06ea97edbe'),
 ('video-monitor-recovery/checkpoints/04b-pinned-handler-proof-guards','work-in-progress/video-monitor/04b-pinned-handler-proof-guards','aade36da986f9fd683577caed650ce2a2a8b24008a92e4194931ed1ac7af0255'),
 ('video-monitor-recovery/checkpoints/08-compiled-controls-type-error','work-in-progress/video-monitor/08-compiled-controls-type-error','827312b71e98ff455fd7a9359d4bbc073c25a8967d50e9604e69b5784ce5b30c'),
]:
 cp=package(local,target,expected_sha)
 tar_bundle(cp,target)

zero_local=ROOT/'trigger-catalog-forward/checkpoints/07-zero-animation-source'
zero_prefix='work-in-progress/trigger-category/07-zero-animation-source'
zero=package('trigger-catalog-forward/checkpoints/07-zero-animation-source',zero_prefix,
 '5cb124753f8acb7cf8e0ec070f1ddf2b2f9b49d99ad144dea6f2b37047258a48')
assert not zero['android_executed'] and not zero['active_changes']
inv=json.loads((zero_local/'host-evidence-manifest.json').read_text())
expected={r['path']:r for r in inv['regular_files']};seen=set()
assert len(expected)==554 and len(inv['symbolic_links_as_inert_metadata'])==1
with tarfile.open(zero_local/'host-evidence.tar.gz','r:gz') as archive:
 for item in archive:
  assert item.isfile();name=safe(item.name);assert name in expected and name not in seen
  data=archive.extractfile(item).read();row=expected[name]
  assert len(data)==row['bytes'] and sha(data)==row['sha256']
  if '/' not in name:
   save(zero_prefix+'/review-evidence/'+name,data,0o755 if item.mode&0o111 else 0o644)
  seen.add(name)
assert seen==set(expected) and inv['symbolic_links_as_inert_metadata'][0]['restored_as_symlink'] is False
jsave(zero_prefix+'/publication-verification.json',dict(exact_original_checkpoint_preserved=True,complete_host_archive_members=554,
 inert_symlink_metadata_entries=1,created_symbolic_links=0,android_executed=False,active_source_or_workflow_modified=False))

proposal_local=ROOT/'trigger-catalog-forward/checkpoints/06-twelve-screen-workflow'
proposal_prefix='work-in-progress/trigger-category-workflow/01-reviewed-workflow'
proposal=package('trigger-catalog-forward/checkpoints/06-twelve-screen-workflow',proposal_prefix,
 '3bde1da21b4c3243ac4c87f582db42ac334c3831556aa36be41aa2a9d4e1479c')
assert proposal['workflow_sha256']=='0447611f6479db154208cebc88deeea568dbdaf4802f4b67e3404cdf051bee8d'
assert not proposal['android_executed'] and not proposal['active_changes']
inventory=json.loads((proposal_local/'offline-evidence-manifest.json').read_text())
assert len(inventory['files'])==inventory['file_count']==5070 and inventory['unique_archived_payloads']==215
payloads={}
with tarfile.open(proposal_local/'offline-evidence-blobs.tar.gz','r:gz') as archive:
 for item in archive:
  if item.isdir():continue
  assert item.isfile() and safe(item.name)==item.name and item.name not in payloads
  data=archive.extractfile(item).read();assert item.name=='blobs/sha256/'+sha(data)+'.bin'
  payloads[item.name]=data
assert len(payloads)==215
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
jsave(proposal_prefix+'/publication-verification.json',dict(exact_checkpoint_preserved=True,complete_logical_evidence_files=5070,
 unique_archived_payloads=215,external_inputs=external,reviewable_members=readable,
 active_workflow_changed=False,android_executed=False,
 status='INACTIVE_NORMAL_SCALE_PROPOSAL_RETAINED_AFTER_ACTUAL_NORMAL03_STABILIZATION_FAILURE'))
save(proposal_prefix+'/PUBLICATION_SCOPE.md',b'''# Inactive twelve-screen normal-scale proposal

The exact offline-validated workflow and all 5,070 evidence paths are preserved
with 215 deduplicated payloads and exact durable APK/tool references. This is an
inactive proposal. The separate actual Normal03 ten-screen run failed TRIGGERS
frame stabilization for both APKs at animation scale 1. No twelve-screen Android
run is claimed here, and this workflow has not been installed under active
`.github/workflows/`. The separate zero-scale preparation remains a later study.
''')
receipts[proposal_prefix].update(complete_logical_evidence_files=5070,unique_archived_payloads=215,active=False)

ops='docs/verification/repository-publication/2026-10-12-normal-failure'
ops_rows=[]
for p in [ROOT/'prepare_normal_failure_transfer.py',ROOT/'normal_failure_body.py',
 *[ROOT/'combined-promotion-transfer'/n for n in ['manifest.json','blobs.json','preparation.json','external-preservation.json','verify_remote.py','remote-verification.json','initial-workflow-observation.json']]]:
 name=('scripts/' if p.parent==ROOT else 'previous-promotion/')+p.name
 data=p.read_bytes();save(ops+'/'+name,data);ops_rows.append(dict(path=name,bytes=len(data),sha256=sha(data)))
jsave(ops+'/checkpoint.json',dict(scope='Closed exact publication and fetched verification; new evidence retains its original pass/fail scope',
 previous_verified_commit='dbcad968c5c3e8f084205393a6c0d2d06a203c71',files=ops_rows))
prefixes.append(ops)
