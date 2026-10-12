"""Freeze a guarded 22-path numeric source/APK promotion proposal; apply nothing."""
from pathlib import Path
from datetime import datetime, timezone
import copy, difflib, gzip, hashlib, json, stat, subprocess
from numeric_promotion_readme import update_readme
ROOT=Path('/dev/shm/macrodroid-transfer-space-20261012')
GIT=ROOT/'verification.git'
PARENT='59df96186fefb2bf883031c09562af08b48bde16'
BASELINE='dbcad968c5c3e8f084205393a6c0d2d06a203c71'
OVERLAY='811f979eda1b937917c18defef38455c49a59062'
PROOF='48ddc442c61e383c4368606cb31984f15d03bb1f'
SOURCE='work-in-progress/day-trigger-numeric/08-command-filesystem-source-successor'
EVIDENCE='docs/verification/day-numeric-hosted-run-3d91187'
ARTIFACT='work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact'
OUT=ROOT/'numeric-source-promotion-proposal'
TARGET='work-in-progress/day-trigger-numeric/11-source-promotion-proposal'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def identity(raw):return {'bytes':len(raw),'sha256':sha(raw)}
def oid(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def git(*args):return subprocess.check_output(['git','--git-dir='+str(GIT),*args])
def row_at(commit,path):
    rows=git('ls-tree','-z',commit,'--',path).split(b'\0')
    rows=[r for r in rows if r]
    if not rows:return None
    assert len(rows)==1
    metadata,name=rows[0].split(b'\t',1);mode,kind,blob=metadata.decode().split()
    assert name.decode()==path and kind=='blob'
    return {'mode':mode,'git_blob_sha1':blob}
def fetched(commit,path):
    row=row_at(commit,path);assert row and row['mode']=='100644',path
    raw=git('cat-file','blob',row['git_blob_sha1']);assert oid(raw)==row['git_blob_sha1']
    return raw
assert git('rev-parse','refs/heads/main').decode().strip()==PARENT
current_project=git('rev-parse',PARENT+':project').decode().strip()
assert current_project==git('rev-parse',BASELINE+':project').decode().strip()
source_raw=fetched(OVERLAY,SOURCE+'/checkpoint.json')
assert sha(source_raw)=='d9ddd3e0f692c66e2cd47870ff3cf95bfa0a2b1cd50fc2fd55a3c09e66df9bcf'
cp=json.loads(source_raw);assert len(cp['source_changes'])==19 and cp['active_files']==[]
old_pin=fetched(PARENT,'project/reports/release-input-snapshot.json')
assert sha(old_pin)=='ca3bed290f18a378c7a3d6cc70d924c8d6ec85481e236b4e7561c31fedafdfbe'
assert old_pin==fetched(BASELINE,'project/reports/release-input-snapshot.json')
base=json.loads(old_pin);assert base['files']==81291 and base['snapshot_sha256']=='b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553'
def canonical(entries):return hashlib.sha256(json.dumps(entries,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert canonical(base['entries'])==base['snapshot_sha256']
future_gzip=fetched(OVERLAY,SOURCE+'/evidence/future-input-snapshot.json.gz')
assert sha(future_gzip)=='821996d28b23b42e55731c6f92a845057d2b4962ff98782dcfce2e69eeb6b11f'
new_pin=gzip.decompress(future_gzip)
assert identity(new_pin)=={'bytes':14504095,'sha256':'896f3eb29dc832eb245fee8dcb70b0e8c8935c9635bf1ccc54c09987b26c91c6'}
future=json.loads(new_pin)
assert future['files']==81298 and future['snapshot_sha256']=='f8fc1cadac8213468e42ac99a2cd5d807827dcdeee25166b8025620ff39a6545'
assert canonical(future['entries'])==future['snapshot_sha256']
proposed={};before={};bindings=[];changed_entries=copy.deepcopy(base['entries'])
for row in cp['source_changes']:
    path='project/'+row['path'];assert row['source']==path
    raw=fetched(OVERLAY,SOURCE+'/'+row['source'])
    assert identity(raw)==row['candidate']
    current=row_at(PARENT,path)
    if row['baseline'] is None:
        assert row['must_be_absent_if_new'] is True and current is None and row['path'] not in changed_entries
        old=None
    else:
        assert row['must_be_absent_if_new'] is False and current is not None
        old=fetched(PARENT,path);assert identity(old)==row['baseline']
        assert changed_entries[row['path']]=={'size':len(old),'sha256':sha(old)}
    proposed[path]=raw;before[path]=old
    changed_entries[row['path']]={'size':len(raw),'sha256':sha(raw)}
    bindings.append({'path':path,'mode':'100644','baseline':None if old is None else identity(old),
                     'baseline_git_blob_sha1':None if old is None else oid(old),'must_be_absent':old is None,
                     'candidate':identity(raw),'candidate_git_blob_sha1':oid(raw),
                     'source_commit':OVERLAY,'source_path':SOURCE+'/'+row['source']})
assert changed_entries==future['entries']
derived={'format':1,'files':len(changed_entries),'snapshot_sha256':canonical(changed_entries),'entries':dict(sorted(changed_entries.items()))}
assert derived==future and json.dumps(derived,indent=2,ensure_ascii=True).encode()==new_pin
verification_path=EVIDENCE+'/selected/hosted-proof/verification.json'
verification_raw=fetched(PROOF,verification_path);v=json.loads(verification_raw)
review_path=EVIDENCE+'/analysis/attempt-02/result.json'
review_raw=fetched(PROOF,review_path);review=json.loads(review_raw)
assert v['passed'] is True and v['status']=='ISOLATED_DAY_NUMERIC_ALL_16_HOST_GATES_VERIFIED'
assert v['gates_verified']==16 and v['fresh_reports_verified']==23
assert v['actual_cases']==194780 and v['registered_methods']==1243 and v['target_classes']==605
assert v['suite_cases']['ui']==24465 and v['python']['tests']==v['python']['individual_successes']==308
assert v['actual_ui_java_controls']==91 and len(v['all_ui_mutant_checks'])==91
assert v['numeric']['actual_dex_faults']==2 and v['numeric']['exact_positive_restoration'] is True
assert v['source_edit_signed_apk_probe_verified'] is True
assert v['android_runtime_executed'] is False and v['android_probe_status']=='BLOCKED'
assert v['source_snapshot']=={'files':81298,'snapshot_sha256':future['snapshot_sha256']}
assert v['future_manifest']==identity(new_pin) and v['source_overlay_commit']==OVERLAY
assert review['passed'] is True and review['tooling_python']['tests']==review['tooling_python']['individual_successes']==92
assert review['gates']==16 and review['actual_cases']==194780 and review['registered_methods']==1243
assert len(review['actual_numeric_dex_faults'])==2 and review['signed_transplant_instructions_equal'] is True
apk_raw=fetched(PROOF,ARTIFACT+'/manifest.json');apk=json.loads(apk_raw)
assert identity(apk_raw)=={'bytes':5189,'sha256':'e1e9c5713c83981cc85ec84e0ce25bfe3fe3a4918d8ff35744ff86194cad0152'}
assert {'bytes':apk['size_bytes'],'sha256':apk['sha256']}==v['apks']['hybrid']==review['apks']['hybrid']
assert apk['size_bytes']==94683136 and apk['sha256']=='0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd'
combined=hashlib.sha256();total=0
for part in apk['parts']:
    raw=fetched(PROOF,part['path'])
    assert len(raw)==part['size_bytes'] and sha(raw)==part['sha256'] and oid(raw)==part['git_blob_sha1']
    combined.update(raw);total+=len(raw)
assert len(apk['parts'])==12 and total==apk['size_bytes'] and combined.hexdigest()==apk['sha256']
old_manifest_raw=fetched(PARENT,'artifacts/current/manifest.json');old_manifest=json.loads(old_manifest_raw)
assert old_manifest['sha256']=='5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'
new_manifest={k:old_manifest[k] for k in ('format','format_version','id','filename','media_type','source_build_filename')}
new_manifest.update({
 'purpose':'Current development candidate with 1,243 recovered bodies and complete hosted numeric source acceptance; Android and whole-application parity remain separately measured.',
 'recovered_method_bodies':1243,'recovered_classes':605,'full_functional_parity_established':False,
 'source_checkpoint_manifest':{'path':SOURCE+'/checkpoint.json','sha256':sha(source_raw),'commit':OVERLAY},
 'source_input_snapshot':{'path':'project/reports/release-input-snapshot.json','files':81298,'canonical_sha256':future['snapshot_sha256'],
                          'manifest_file_bytes':len(new_pin),'manifest_file_sha256':sha(new_pin)},
 'origin':{'kind':'hosted-sixteen-gate-numeric-source-acceptance','proof_commit':PROOF,'run_id':38238858564,'job_id':114776169911,
           'tooling_commit':'3d91187924af10457366ede7a1a8f10d3a1a6ac4','immutable_apk_manifest':ARTIFACT+'/manifest.json',
           'immutable_apk_manifest_sha256':sha(apk_raw),'independent_review_manifest':EVIDENCE+'/analysis/checkpoint.json',
           'independent_review_manifest_sha256':'dc154a04c2a734446cf57d8d32628f1b0cc7110d66100f098e247e5cdb2e3301',
           'complete_ci_artifact_manifest':EVIDENCE+'/manifest.json','literal_verification_path':verification_path},
 'validation_at_publication':{'configured_acceptance_gates_passed':16,'fresh_reports_verified':23,
      'original_jvm_rebuilt_cases':194780,'registered_methods':1243,'python_tests_passed':308,'tooling_host_tests_passed':92,
      'ui_cases':24465,'actual_ui_java_fault_controls_passed':91,'actual_numeric_dex_fault_controls_passed':2,
      'numeric_cases':1291,'numeric_original_instructions':32,'numeric_rebuilt_instructions':25,'numeric_conditional_edges_per_path':4,
      'exact_positive_restoration_passed':True,'signed_source_edit_probe_passed':True,
      'full_configured_acceptance_executed_for_this_pin':True,'android_executed_for_this_candidate':False,
      'android_status':'Not yet observed for the 0762aad9 candidate'},
 'previous_candidate':{'commit':PARENT,'manifest_path':'artifacts/current/manifest.json','manifest_sha256':sha(old_manifest_raw),
                       'immutable_manifest_path':'work-in-progress/combined-recovery/05-full-acceptance/apk/manifest.json',
                       'sha256':old_manifest['sha256'],'size_bytes':old_manifest['size_bytes']},
 'size_bytes':apk['size_bytes'],'sha256':apk['sha256'],'parts':apk['parts']})
assert new_manifest['filename']==old_manifest['filename']=='MacroDroid-5.67.8-current-hybrid.apk'
new_manifest_raw=(json.dumps(new_manifest,indent=2)+'\n').encode()
old_readme=fetched(PARENT,'README.md')
assert identity(old_readme)=={'bytes':18272,'sha256':'5cb418202d6cf6898e29e61ebb29d3c0971022d62b4c1d9e1209213324074c63'}
new_readme,readme_checks=update_readme(old_readme)
for path,old,raw in [('project/reports/release-input-snapshot.json',old_pin,new_pin),
                     ('artifacts/current/manifest.json',old_manifest_raw,new_manifest_raw),('README.md',old_readme,new_readme)]:
    proposed[path]=raw;before[path]=old
    bindings.append({'path':path,'mode':'100644','baseline':identity(old),'baseline_git_blob_sha1':oid(old),'must_be_absent':False,
                     'candidate':identity(raw),'candidate_git_blob_sha1':oid(raw),'source_path':'proposed/'+path})
assert len(bindings)==22 and len(proposed)==22
OUT.mkdir(exist_ok=False)
def put(path,raw):
    p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as stream:stream.write(raw)
    p.chmod(0o644)
for path,raw in proposed.items():put('proposed/'+path,raw)
put('before/README.md',old_readme);put('before/artifacts-current-manifest.json',old_manifest_raw)
put('source-checkpoint.json',source_raw)
put('literal-numeric-verification.json',verification_raw)
put('independent-numeric-result.json',review_raw)
put('executed-preparer.py',Path(__file__).read_bytes())
put('numeric_promotion_readme.py',(ROOT/'numeric_promotion_readme.py').read_bytes())
for name,paths in [('README.patch',['README.md']),('current-manifest.patch',['artifacts/current/manifest.json']),
                    ('nineteen-source.patch',[r['path'] for r in bindings[:19]])]:
    pieces=[]
    for path in paths:
        a=before[path] or b'';b=proposed[path]
        try: at=a.decode();bt=b.decode()
        except UnicodeDecodeError:
            pieces.append('Binary identity change for '+path+'; exact bytes are bound in promotion-manifest.json.\n');continue
        pieces.extend(difflib.unified_diff(at.splitlines(True),bt.splitlines(True),fromfile='before/'+path,tofile='proposed/'+path))
    put(name,''.join(pieces).encode())
manifest={'schema':1,'status':'PREPARED_FOR_ROOT_REVIEW_NOT_APPLIED','reviewed_parent':PARENT,'baseline_commit':BASELINE,
          'baseline_project_tree':current_project,'source_overlay_commit':OVERLAY,'evidence_commit':PROOF,
          'source_checkpoint_sha256':sha(source_raw),'source_files':19,'companion_files':3,'proposed_active_files':bindings,
          'input_derivation':{'before':{'files':base['files'],'snapshot_sha256':base['snapshot_sha256'],'manifest':identity(old_pin)},
                              'after':{'files':future['files'],'snapshot_sha256':future['snapshot_sha256'],'manifest':identity(new_pin)},
                              'exact_19_delta_reconstructs_every_81298_entry':True},
          'readme_checks':readme_checks,'all_existing_workflows_preserved':True,'historical_apk_parts_and_manifests_preserved':True,
          'application_source_or_apk_activated_here':False,'new_build_or_android_execution':False,
          'prepared_utc':datetime.now(timezone.utc).isoformat()}
put('promotion-manifest.json',(json.dumps(manifest,indent=2)+'\n').encode())
put('README.md',b'''# Numeric source promotion proposal

This inactive capsule contains exactly 22 proposed repository payloads: the nineteen source rows actually used by the successful numeric CI run, the byte-exact complete release-input snapshot, the matching current candidate manifest, and a narrow root README update. Nothing is applied by creating or publishing this capsule.

[promotion-manifest.json](promotion-manifest.json) binds every before/after size, SHA-256, Git blob identity and file mode. All seven new source paths must remain absent; each of the twelve existing source paths and three companions must match its recorded baseline. The full current project tree equals the immutable `dbcad968` baseline at preparation. Applying exactly the nineteen rows reconstructs every entry of the 81,298-input `f8fc1cad` snapshot; its exact 14,504,095 bytes have SHA-256 `896f3eb29dc832eb245fee8dcb70b0e8c8935c9635bf1ccc54c09987b26c91c6`.

The proposed current manifest retains `MacroDroid-5.67.8-current-hybrid.apk` and references the twelve already-fetched immutable numeric parts. They stream to 94,683,136 bytes / `0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd`. No APK copy or historical part mutation is needed.

All new current metrics are taken from the closed numeric job and its independent review: 16 gates, 23 fresh reports, 1,243 bodies, 605 classes, 194,780 cases, 24,465 UI cases, 308 project Python tests, 92 tooling tests, 91 actual Java UI faults and two actual numeric DEX faults. Old independent-UI counts are retained only in clearly historical README text. Android behavior for this new candidate remains unobserved.

The complete existing Latest trigger-navigation observations section is byte-identical. The README labels previous 5f source/device evidence as historical and retains it. Existing workflows and historical APK manifests remain unchanged. Root review must precede active application promotion; a coherent later promotion is expected to trigger the existing source and Android workflows, whose actual results must be preserved separately.
''')
files=[]
for path in sorted(OUT.rglob('*')):
    if path.is_file():
        raw=path.read_bytes();files.append({'path':path.relative_to(OUT).as_posix(),'bytes':len(raw),'sha256':sha(raw),'mode':stat.S_IMODE(path.stat().st_mode)})
checkpoint={'schema':1,'status':'EXACT_NUMERIC_22_PATH_PROMOTION_PROPOSAL_PENDING_ROOT_REVIEW','repo_target':TARGET,
            'active_files':[],'proposed_file_count':22,'files':files}
put('checkpoint.json',(json.dumps(checkpoint,indent=2)+'\n').encode())
print(json.dumps({'source':str(OUT),'target':TARGET,'checkpoint_sha256':sha((OUT/'checkpoint.json').read_bytes()),'files':len(files),
                  'payload_bytes':sum(r['bytes'] for r in files),'proposed_paths':22,'new_readme':identity(new_readme),
                  'new_current_manifest':identity(new_manifest_raw),'new_input_snapshot':identity(new_pin)}))
