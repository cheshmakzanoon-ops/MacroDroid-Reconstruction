from pathlib import Path
from datetime import datetime,timezone
import ast,difflib,gzip,hashlib,io,json,os,shutil,stat,sys,tarfile
ROOT=Path('/dev/shm/macrodroid-day-lookup-integration')
SOURCE=ROOT/'combined-host-01/repository'
TOOLS=SOURCE/'tools/day_trigger_acceptance'
PARENT=Path('/dev/shm/day-numeric-hosted-02/checkpoints/02-hosted-filesystem-tooling-successor/source')
DRAFT=ROOT/'checkpoints/07-combined-tooling-draft'
REPORTS=ROOT/'combined-host-01/reports'
OUT=ROOT/'checkpoints/08-combined-tooling-controls'
assert not OUT.exists()
def identity(p):
 raw=p.read_bytes();return {'bytes':len(raw),'mode':stat.S_IMODE(p.stat().st_mode),'sha256':hashlib.sha256(raw).hexdigest()}
def bare(p):return {k:v for k,v in identity(p).items() if k!='mode'}
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def scan(root):return [{'path':p.relative_to(root).as_posix(),**bare(p)} for p in sorted(root.rglob('*')) if p.is_file()]
positive=json.loads((REPORTS/'03-corrected-153-controls/result.json').read_text())
sourcecheck=json.loads((REPORTS/'05-source-and-workflow-boundaries-corrected/result.json').read_text())
assert positive['passed'] is True and positive['observed_tests']==153 and positive['sources_unchanged'] is True
assert sourcecheck['passed'] is True and sourcecheck['bound_read_files']==569 and sourcecheck['all_bound_reads_unchanged'] is True
source_rows=scan(SOURCE);assert len(source_rows)==9 and source_rows==positive['source_after']==sourcecheck['source_after']
assert bare(DRAFT/'checkpoint.json')=={'bytes':5451,'sha256':'e4df83e886976b034616671094784c3766d98812f0dab448d767bdbcc11a43e5'}
OUT.mkdir(parents=True)
for p in sorted(SOURCE.rglob('*')):
 if not p.is_file():continue
 t=OUT/'source'/p.relative_to(SOURCE);t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,t)
patch=[];bindings=[]
for row in source_rows:
 rel=row['path'];oldrel=rel.replace('day_trigger_acceptance','day_numeric_acceptance').replace('day-trigger-wip-acceptance.yml','day-numeric-wip-acceptance.yml').replace('test_day_trigger_acceptance.py','test_day_numeric_acceptance.py')
 before=PARENT/oldrel;after=SOURCE/rel;assert before.is_file()
 patch.extend(difflib.unified_diff(before.read_text().splitlines(True),after.read_text().splitlines(True),fromfile='parent/'+oldrel,tofile='candidate/'+rel))
 bindings.append({'path':rel,'candidate':identity(after),'active_path_must_be_absent':True,'parent_tooling_path':oldrel,'parent_tooling':identity(before)})
(OUT/'tooling-derivation.patch').write_text(''.join(patch))
patch=[]
for row in source_rows:
 p=SOURCE/row['path'];q=DRAFT/'source'/row['path']
 patch.extend(difflib.unified_diff(q.read_text().splitlines(True),p.read_text().splitlines(True),fromfile='draft/'+row['path'],tofile='validated/'+row['path']))
(OUT/'draft-to-validated.patch').write_text(''.join(patch))
write(OUT/'nine-path-bindings.json',{'files':bindings,'existing_application_and_workflows_changed':False,'lookup_commit':'39250fac022aee5551f36782bafd72cabbc33718'})
# Review copies are deliberately small; the full raw attempts live in the archive.
for attempt in sorted(REPORTS.iterdir()):
 if not attempt.is_dir():continue
 for name in ('result.json','stdout.log','stderr.log','traceback.txt','actual-other-gates-diff.txt','source-before.json','exact-read-boundaries.json','executed-collector.py'):
  p=attempt/name
  if p.is_file():
   t=OUT/'review'/attempt.name/name;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,t)
 for p in sorted((attempt/'commands').rglob('*.log')) if (attempt/'commands').exists() else []:
  t=OUT/'review'/attempt.name/p.relative_to(attempt);t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,t)
for name in ('derive_combined_tooling.py','refresh_combined_runtime.py','run_combined_tooling_controls.py','verify_combined_source_and_workflow.py','freeze_combined_tooling_final.py'):
 t=OUT/'authoring'/name;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,t)
write(OUT/'host-environment-at-freeze.json',{'scope':'Observed at final freeze; application Java and Android were not executed in this tooling study','python':sys.version,'executable':str(Path(sys.executable).resolve()),'executable_identity':identity(Path(sys.executable).resolve()),'platform':sys.platform,'runtime_manifest':identity(TOOLS/'runtime-files.json')})
# Every regular raw attempt is retained. The one deliberate bootstrap symlink is
# archived as an inert exact-target description, never as a traversable link.
members=[];archive=OUT/'evidence.tar.gz'
with archive.open('xb') as out:
 with gzip.GzipFile(filename='',mode='wb',fileobj=out,mtime=0) as gz:
  with tarfile.open(fileobj=gz,mode='w') as tf:
   for prefix,folder in [('reports',REPORTS),('draft-freezer-failures',ROOT/'combined-host-01/failures')]:
    for p in sorted(folder.rglob('*')):
     if p.is_dir() and not p.is_symlink():continue
     role=prefix+'/'+p.relative_to(folder).as_posix()
     if p.is_symlink():
      target=os.readlink(p);value={'schema':1,'kind':'deliberate-policy-fixture-symlink','original_role':role,'target':target,'scope':'Inert preservation of the actual bootstrap symlink rejection; no link is materialized by extraction'}
      raw=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode();name=role+'.symlink-description.json'
      member={'path':name,'bytes':len(raw),'mode':0o644,'sha256':hashlib.sha256(raw).hexdigest(),'source_kind':'symlink-description','original_role':role,'exact_original_target':target}
      assert os.readlink(p)==target
     else:
      assert p.is_file();before=identity(p);raw=p.read_bytes();assert identity(p)==before
      name=role;member={'path':name,**before,'source_kind':'regular'}
     info=tarfile.TarInfo(name);info.size=len(raw);info.mode=member['mode'];info.uid=info.gid=0;info.uname=info.gname='';info.mtime=0
     tf.addfile(info,io.BytesIO(raw));members.append(member)
write(OUT/'evidence-inventory.json',{'schema':1,'files':members,'file_count':len(members),'archive':identity(archive),'original_metadata_scope':'Live command receipt inode/ctime values are retained in raw observations. Archive inode/ctime are not claimed to match.'})
# Independently stream the complete finished archive before closing the checkpoint.
with tarfile.open(archive,'r:gz') as tf:
 actual=tf.getmembers();assert len(actual)==len(members) and all(m.isfile() for m in actual)
 for info,row in zip(actual,members):
  assert info.name==row['path'] and info.size==row['bytes'] and info.mode==row['mode']
  stream=tf.extractfile(info);digest=hashlib.file_digest(stream,'sha256').hexdigest();assert digest==row['sha256']
assert scan(SOURCE)==source_rows and scan(OUT/'source')==source_rows
scope='''# Inactive combined numeric and lookup tooling: closed host controls

Exactly nine new tooling paths are under `source/`. They derive from frozen numeric tooling 815612f8 and implement the reviewed design 3da7b4fa against fixed Lookup source commit 39250fac022aee5551f36782bafd72cabbc33718. The final application union remains the previously frozen 25 paths/13 new inputs. No active application source, APK, manifest or workflow changed during this study. This capsule is inactive pending independent review and publisher activation.

## Actual completed checks

- **153/153 tooling tests passed**, comprising all 92 inherited test identities and 61 new controls; actual runner wall time 11.234645624 seconds. Source and executed copies of all nine files remained identical. The log reports the exact unittest duration separately.
- Actual read-only verification of all three frozen source capsule inventories and 569 bound files passed, followed by complete 81,291 → 81,298 → 81,304 entry-map derivation, all21 payload selections and all four numeric-only pins. This is a full manifest derivation, not local physical materialization of the application. The new physical preparation function was actually exercised on tiny explicitly synthetic trees with the real19/21 path topology.
- The new registry/dependency guard accepted the actual final1,244 registry and exact five uncredited dependencies. The cwd guard accepted a copy of the four exact production files and explicit resolved outer-root receipt; no child cwd field was invented and no method subprocess was invoked by that source-policy check.
- Six actual shell syntax commands passed. The workflow's literal seven-file bootstrap ran successfully on an exact nine-file copy and rejected five deliberate source/manifest/pin/inventory/symlink faults. All twelve command results and streams are retained.
- Fifty shared source definitions, including the process recorder/cleanup, stream verification and the complete numeric proof, are byte-identical to frozen numeric tooling. The additional exact existing-gate changes are the required fresh report count23→24 and registry count1,243→1,244. Other combined integration changes are in the complete derivation patch.

## Failed attempts preserved

1. Draft freezer: its overly broad unchanged-function assertion included the intended23→24 fresh-report change; corrected to prove exactly that narrow delta. The failed freezer source and traceback remain retained.
2. First142-test run:140 passed. The inherited gate-envelope assertion still expected23 reports; the new replaced-inode fixture reached an earlier interval rejection. Only fixture expectations/interval setup were corrected.
3. Expanded153-test run:152 passed. Its retained-policy fault used an intentionally exclusive JSON writer on an existing file, so no alteration occurred. The test-only injection was changed to direct owned-file byte replacement; the production exclusive writer was not weakened.
4. First source/workflow collector: derived all three actual maps before its assertion failed because the collector guessed an old error string ending `body`; actual parent text ends `method`. The corrected collector proves the exact count/string delta. Its raw `passed=false` result, initial status and traceback stay unchanged.

No failed run is relabeled as a pass. The final corpus/source check uses unchanged production verifier/recorder logic from the draft; subsequent edits are test-only plus the exact runtime manifest/workflow pin that binds the changed tests. `draft-to-validated.patch` makes this scope directly reviewable.

## Required future application acceptance

This study executed **zero application/Java/D8/Android cases and zero full project materializations/builds/signing runs**. The new complete16-gate hosted run must still prove both ordinary methods against the actual signed APK; all195,151 positive cases,357 project Python tests,101 Java faults,17 numeric/19 lookup schema-2 commands, four actual method D8 faults, four provenance rejections, raw restorations and all24 fresh reports remain acceptance requirements rather than results of this tooling study. Old numeric workflow/current APK remain separate.

The final workflow runtime pin is07b58ce29d4db875ef349d23aa05b8b75145ea4f7338b7dd2943db10129a0d32; workflow SHA-256 is443e184bc3185593e1a8c268d60200ada2b1cdb6df2b8e551e51ae52dae0c6eb. The source package is complete, every archive member was independently streamed and rehashed, and the one deliberate preflight symlink is retained only as an inert exact-target description. Original live metadata receipts remain distinct from copied/archive metadata.
'''
# Legibility is part of the handoff.
for a,b in [('real19/21','real 19/21'),('all21','all 21'),('final1,244','final 1,244'),('count23','count 23'),('count1,243','count 1,243'),('intended23','intended 23'),('First142','First 142'),('run:140','run: 140'),('expected23','expected 23'),('Expanded153','Expanded 153'),('run:152','run: 152'),('complete16','complete 16'),('all195,151','all 195,151'),('cases,357','cases, 357'),('tests,101','tests, 101'),('faults,17','faults, 17'),('numeric/19','numeric / 19'),('all24','all 24'),('pin is07','pin is 07'),('is443','is 443')]:scope=scope.replace(a,b)
(OUT/'CHECKPOINT_SCOPE.md').write_text(scope)
summary={'schema':1,'passed':True,'status':'INACTIVE_COMBINED_TOOLING_153_CONTROLS_SOURCE_AND_BOOTSTRAP_VERIFIED','tooling_tests':153,'inherited_tooling_tests':92,'new_tooling_tests':61,'bound_source_reads':569,'complete_entry_map_counts':[81291,81298,81304],'physical_application_tree_materializations':0,'tiny_physical_source_stage_controls':True,'actual_shell_syntax_commands':6,'literal_bootstrap_successes':1,'literal_bootstrap_expected_rejections':5,'application_executions':0,'full_host_acceptance_executed':False,'runtime_manifest':identity(TOOLS/'runtime-files.json'),'workflow':identity(SOURCE/'.github/workflows/day-trigger-wip-acceptance.yml'),'complete_archive_members_verified':len(members),'deliberate_symlinks_archived_as_inert_descriptions':sum(r['source_kind']=='symlink-description' for r in members)}
write(OUT/'validation-summary.json',summary)
files=[{'path':p.relative_to(OUT).as_posix(),**identity(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
cp={'schema':1,'status':summary['status'],'created_utc':datetime.now(timezone.utc).isoformat(),'repo_target':'work-in-progress/day-trigger-lookup/12-combined-tooling-host-controls','active_source_changed':False,'active_workflow_changed':False,'full_host_acceptance_executed':False,'application_executions':0,'full_project_materializations':0,'tooling_tests':153,'inherited_tooling_tests':92,'new_tooling_tests':61,'proposed_tooling_paths':9,'lookup_commit':'39250fac022aee5551f36782bafd72cabbc33718','parent_draft_checkpoint_sha256':'e4df83e886976b034616671094784c3766d98812f0dab448d767bdbcc11a43e5','design_checkpoint_sha256':'3da7b4fa3707c301256c8dd7236c18f7680d2fb5bd72595d353e8a01b223830f','parent_tooling_checkpoint_sha256':'815612f827f1b0d2bcec90bbb1ae8a35a8c76ced8f6b5f44cf413bc40b81f493','runtime_manifest':summary['runtime_manifest'],'workflow':summary['workflow'],'evidence_archive':identity(archive),'evidence_file_count':len(members),'files':files}
write(OUT/'checkpoint.json',cp)
print(json.dumps({'checkpoint':str(OUT/'checkpoint.json'),**identity(OUT/'checkpoint.json'),'files':len(files),'archive':identity(archive),'archive_members':len(members),'runtime':summary['runtime_manifest'],'workflow':summary['workflow']},indent=2))
