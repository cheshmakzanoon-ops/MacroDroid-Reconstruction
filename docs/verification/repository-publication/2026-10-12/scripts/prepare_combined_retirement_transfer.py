from pathlib import Path, PurePosixPath
import gzip
import hashlib
import io
import json
import subprocess
import tarfile

ROOT=Path('/workspace/scratch/4130730d15aa')
REPO=ROOT/'MacroDroid-Reconstruction'
EXPORT=ROOT/'combined-retirement-transfer'
EXPORT.mkdir(exist_ok=True)
paths=set();receipts={}
def sha(b):return hashlib.sha256(b).hexdigest()
def oid(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def safe(name):
    p=PurePosixPath(name);assert not p.is_absolute() and '..' not in p.parts
    return p.as_posix()
def save(name,data,mode=0o644):
    name=safe(name);p=REPO/name;assert not p.is_symlink() and (not p.exists() or p.read_bytes()==data),name
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);p.chmod(mode);paths.add(name)
def jsave(name,value):save(name,(json.dumps(value,indent=2)+'\n').encode())
def copy_checkpoint(source,prefix,expected_hash,filename='checkpoint.json'):
    raw=(source/filename).read_bytes();assert sha(raw)==expected_hash
    cp=json.loads(raw)
    for row in cp['files']:
        p=source/safe(row['path']);data=p.read_bytes();assert not p.is_symlink()
        assert len(data)==row.get('bytes',row.get('size_bytes')) and sha(data)==row['sha256'],row['path']
        save(prefix+'/'+row['path'],data,0o755 if p.stat().st_mode&0o111 else 0o644)
    save(prefix+'/'+filename,raw)
    return cp

source=ROOT/'combined-recovery/checkpoints/04-fresh-source-preparation'
prefix='work-in-progress/combined-widget-plugin/04-fresh-source-preparation'
cp=copy_checkpoint(source,prefix,'da0a1a8944e24f2d559083ac7232634be257756a5073ea1755eb5006761191e6')
assert len(cp['files'])==90 and cp['changed_input_files']==63
assert cp['compiled'] is False and cp['full_acceptance_executed'] is False and cp['active_source_changed'] is False and cp['active_apk_changed'] is False
with tarfile.open(source/'input-snapshot.tar.gz','r:gz') as t:
    members=t.getmembers();assert len(members)==1 and members[0].isfile()
    assert safe(members[0].name)=='project/reports/release-input-snapshot.json'
    data=t.extractfile(members[0]).read()
    assert len(data)==cp['input_manifest']['bytes']==14502990 and sha(data)==cp['input_manifest']['sha256']
    pin=json.loads(data);assert pin['files']==len(pin['entries'])==81291
    assert pin['snapshot_sha256']==cp['input_snapshot_sha256']=='b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553'
jsave(prefix+'/publication-verification.json',dict(frozen_checkpoint_sha256='da0a1a8944e24f2d559083ac7232634be257756a5073ea1755eb5006761191e6',
    declared_files_verified=90,compressed_input_member_verified=True,input_manifest_entries_verified=81291,
    publisher_rehashed_materialized_inputs=False,prepared_registry_methods=1242,prepared_registry_classes=605,
    source_delta_files=63,prepared_workflow_remains_inactive=True,active_source_or_apk_changed=False))
save(prefix+'/PUBLICATION_NOTE.md',b'''# Inactive fresh combined preparation

All 90 declared files and the frozen checkpoint are copied unchanged. The compressed input snapshot contains the exact verified 81,291-entry manifest. The prepared 1,242-body/605-class registry and expected suite/control counts describe planned combined inputs; this checkpoint does not claim compilation, full acceptance or Android execution.

The workflow under `preparation/repository-overlay/` remains part of this inactive capsule. It is not copied to the active repository workflow. Source and APK promotion require their own later coherent verified checkpoint.
''')
receipts['combined04']=dict(files=90,source_delta_files=63,input_manifest_entries=81291,active_source_or_apk_changed=False)

widget_prefix='docs/verification/storage-cleanup/widget-signed-study'
widget_rows=[]
mapping=[('widget-recovery/reports/closed-signed-cache-retirement.json','closed-signed-cache-retirement.json'),
         ('widget-recovery/retire_closed_cache.py','retire_closed_cache.py')]
for i in range(1,4):
    folder=ROOT/f'widget-recovery/reports/closed-cache-attempt{i:02d}'
    mapping += [(p.relative_to(ROOT).as_posix(),f'attempt-{i:02d}/'+p.relative_to(folder).as_posix()) for p in sorted(folder.rglob('*')) if p.is_file()]
assert len(mapping)==8
for original,destination in mapping:
    p=ROOT/original;data=p.read_bytes();assert not p.is_symlink()
    save(widget_prefix+'/'+destination,data,0o755 if p.stat().st_mode&0o111 else 0o644)
    widget_rows.append(dict(path=destination,source_path=original,bytes=len(data),sha256=sha(data)))
widget_result=json.loads((ROOT/mapping[0][0]).read_text())
assert widget_result['proof_commit']=='a17e119f90418fb642aea4777c0f920bbf9fb92c'
assert widget_result['source_files_verified_before_and_after']==81266 and widget_result['source_reports_apk_docs_unchanged'] is True
assert widget_result['preserved_files']==81351 and sum(x['files'] for x in widget_result['removed'])==160791
for i in range(1,4):
    attempt=json.loads((ROOT/f'widget-recovery/reports/closed-cache-attempt{i:02d}/result.json').read_text())
    assert attempt['files_deleted']==0
    script=(ROOT/f'widget-recovery/reports/closed-cache-attempt{i:02d}/retire_closed_cache.py').read_bytes()
    assert sha(script)==attempt['script_sha256']
jsave(widget_prefix+'/checkpoint.json',dict(scope='Closed Widget cache retirement and all three earlier guard/diagnostic failures',files=widget_rows,
    proof_commit=widget_result['proof_commit'],source_reports_apk_docs_unchanged=True))
save(widget_prefix+'/README.md',b'''# Closed Widget generated-cache retirement

The successful receipt records removal of only the closed private study's `build` and `tools/classes` outputs after its complete signed proof was durably published at `a17e119f90418fb642aea4777c0f920bbf9fb92c`. It records 160,791 generated files removed, all 81,266 source inputs rehashed before and after, and 81,351 retained files unchanged.

All three earlier blocked/diagnostic attempts and their exact executed scripts are preserved. They deleted zero files. The final process guard uses the actual mounted procfs self identity; the third attempt records the observed inner-versus-procfs PID distinction and the diagnostic error. The first attempt did not retain a process identity, so its receipt does not claim a proven explanation.

This publication preserves the recorded operation. It performs no cache or source removal.
''')
receipts['widget-retirement']=dict(source_files=8,preserved_files=81351,source_inputs_checked=81266,generated_files_removed_by_prior_operation=160791)

k_source=ROOT/'plugin-upload-recovery/cache-retirement-04'
k_prefix='docs/verification/storage-cleanup/plugin-upload-signed-study'
k=copy_checkpoint(k_source,k_prefix,'54f6b396cf6590d4e9a624decdecc5c8dbb52b97e1603b40b002e3d42e1f4f0a','manifest.json')
assert len(k['files'])==8
k_result=json.loads((k_source/'attempt-01/result.json').read_text())
before=gzip.decompress((k_source/'attempt-01/retained-inventory-before.json.gz').read_bytes())
after=gzip.decompress((k_source/'attempt-01/retained-inventory-after.json.gz').read_bytes())
assert before==after and sha(before)==k_result['retained_inventory_before_sha256']==k_result['retained_inventory_after_sha256']
inventory=json.loads(before);assert len(inventory)==k_result['retained_files']==81609
assert k_result['all_retained_files_unchanged'] is True and k_result['generated_cache_absent'] is True
assert k_result['proof_commit']=='075cdcb5b5e7309057acdac63a097ac48dbbd545' and k_result['files_deleted']==160946
jsave(k_prefix+'/publication-verification.json',dict(frozen_manifest_sha256='54f6b396cf6590d4e9a624decdecc5c8dbb52b97e1603b40b002e3d42e1f4f0a',
    declared_files_verified=8,before_after_inventory_bytes_identical=True,inventory_sha256=sha(before),retained_entries=81609,
    publisher_rehashed_live_private_files=False,publication_performed_no_deletion=True))
save(k_prefix+'/README.md',b'''# Closed plugin-upload generated-cache retirement

The exact executed guard, fetched final proof, command outputs and both complete compressed inventories are preserved. Independent publication review decompressed the before/after inventories and verified identical bytes and all 81,609 entries against the receipt's recorded digest.

The prior guarded operation removed only the closed K study's generated `build` directory: 160,946 files. Its source, tests, reports, APK and frozen evidence remained byte-identical after final proof commit `075cdcb5b5e7309057acdac63a097ac48dbbd545` was fetched and verified. This publication performs no deletion and does not repeat the live private-file inventory.
''')
receipts['k-retirement']=dict(files=8,retained_inventory_entries=81609,uncompressed_before_after_bytes_identical=True)

editor_source=ROOT/'tooling-validation/editor-run-38204928419/analysis'
editor_prefix='docs/verification/editor-journey/run-38204928419-attempt-1/analysis'
editor=copy_checkpoint(editor_source,editor_prefix,'7a5c6ac9b1365e9b5ec9bf77282a5035e672cb48d5d77dcf98f7ab5eb781cc4b')
assert len(editor['files'])==181 and editor['all_archive_members_verified']==1784 and editor['artifact_paths_verified']==1616
assert editor['recorded_screens_per_apk']==16 and editor['verified_inputs_total']==30
assert editor['original_comparator_result_preserved'] is True and editor['full_runtime_1_to_1_established'] is False
receipts['external16-analysis']=dict(files=181,source_run=38204928419,original_comparator_result_preserved=True)

ops_prefix='docs/verification/repository-publication/2026-10-12'
ops_rows=[]
def ops_copy(p,dest):
    data=p.read_bytes();save(ops_prefix+'/'+dest,data,0o755 if p.stat().st_mode&0o111 else 0o644)
    ops_rows.append(dict(path=dest,source_path=p.relative_to(ROOT).as_posix(),bytes=len(data),sha256=sha(data)))
for p in sorted(ROOT.glob('prepare_*transfer.py')):
    ops_copy(p,'scripts/'+p.name)
closed=[]
for folder in sorted(ROOT.glob('*-transfer')):
    if not (folder/'remote-verification.json').is_file():continue
    closed.append(folder.name)
    for name in ['manifest.json','blobs.json','preparation.json','remote-verification.json','verify_remote.py','prepublication-verification.json','assembly-verification.json']:
        p=folder/name
        if p.is_file():ops_copy(p,'closed/'+folder.name+'/'+name)
jsave(ops_prefix+'/checkpoint.json',dict(scope='Exact historical publication scripts and completed fetched-byte verification records',
    closed_export_directories=closed,files=ops_rows,transport_content_chunks_omitted_as_reproducible_duplicates=True))
save(ops_prefix+'/README.md',b'''# Historical repository publication operations

These exact preparation and verification scripts, file/object manifests and completed verification receipts preserve the authored repository-transfer work. The receipts bind the relevant commits, fetched Git modes, SHA-1 object identifiers, SHA-256 content hashes and fingerprint-preserving mixed resets. Each record retains its measured scope and original task paths.

The scripts are historical operation records with explicit task-specific paths and baseline guards; no workflow executes them automatically. Reproducible transport text chunks are omitted because their complete file contents are already represented in the published Git trees. APKs and source/evidence archives remain at the manifests referenced by the respective project checkpoints.

This folder adds operational evidence only. It changes no active application or runtime policy.
''')
receipts['publication-operations']=dict(closed_exports=len(closed),source_and_record_files=len(ops_rows))

baselines={}
ignored_result=subprocess.run(['git','check-ignore','--stdin','-z'],cwd=REPO,input=b'\0'.join(p.encode() for p in sorted(paths))+b'\0',capture_output=True)
assert ignored_result.returncode in (0,1)
ignored=[p.decode() for p in ignored_result.stdout.split(b'\0') if p]
if ignored:
    p=REPO/'.gitignore';before=p.read_bytes();baselines['.gitignore']=sha(before)
    p.write_bytes(before+('\n# Exact combined preparation and archived publication evidence\n'+''.join('!'+n+'\n' for n in ignored)).encode());paths.add('.gitignore')
p=REPO/'.gitattributes';before=p.read_bytes();baselines['.gitattributes']=sha(before)
rules='\n# Exact inactive source snapshot and retained-file inventories\n'+prefix+'/input-snapshot.tar.gz -text -diff -merge\n'+k_prefix+'/attempt-01/*.json.gz -text -diff -merge\n'
p.write_bytes(before+rules.encode());paths.add('.gitattributes')
known={line.split(b' ',1)[0].decode() for line in subprocess.check_output(['git','rev-list','--objects','--all'],cwd=REPO).splitlines()}
rows=[];blobs=[];texts=[]
for name in sorted(paths):
    p=REPO/name;data=p.read_bytes();row=dict(path=name,size_bytes=len(data),sha256=sha(data),git_blob_sha1=oid(data),mode='100755' if p.stat().st_mode&0o111 else '100644');rows.append(row)
    try:content=data.decode('utf-8');binary='\0' in content
    except UnicodeDecodeError:binary=True
    if row['git_blob_sha1'] in known or binary or len(data)>250000:blobs.append(row|dict(known=row['git_blob_sha1'] in known,encoding='base64'))
    else:texts.append(dict(path=name,mode=row['mode'],type='blob',content=content))
chunks=[];chunk=[]
for entry in texts:
    if chunk and len(json.dumps(chunk+[entry],ensure_ascii=False).encode())>650000:chunks.append(chunk);chunk=[]
    chunk.append(entry)
if chunk:chunks.append(chunk)
for i,entries in enumerate(chunks):(EXPORT/f'text-{i:02d}.json').write_text(json.dumps(entries,ensure_ascii=False))
for name,data in [('manifest.json',rows),('blobs.json',blobs)]:(EXPORT/name).write_text(json.dumps(data,indent=2)+'\n')
result=dict(files=len(rows),bytes=sum(r['size_bytes'] for r in rows),text_chunks=len(chunks),text_entries=len(texts),
    new_unique_blobs=len({r['git_blob_sha1'] for r in blobs if not r['known']}),baselines=baselines,receipts=receipts,
    active_source_apk_or_workflow_changed=False)
(EXPORT/'preparation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
