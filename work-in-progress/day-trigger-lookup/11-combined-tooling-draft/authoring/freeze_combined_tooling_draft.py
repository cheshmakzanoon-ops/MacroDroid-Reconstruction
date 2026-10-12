from pathlib import Path
from datetime import datetime,timezone
import ast,difflib,gzip,hashlib,io,json,os,re,shutil,stat,tarfile
ROOT=Path('/dev/shm/macrodroid-day-lookup-integration')
SOURCE=ROOT/'combined-host-01/repository'
TOOLS=SOURCE/'tools/day_trigger_acceptance'
PARENT=Path('/dev/shm/day-numeric-hosted-02/checkpoints/02-hosted-filesystem-tooling-successor/source')
OUT=ROOT/'checkpoints/07-combined-tooling-draft'
assert not OUT.exists()

def identity(p):
 raw=p.read_bytes();return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'mode':stat.S_IMODE(p.stat().st_mode)}
def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def nodes(p):
 source=p.read_text();return {n.name:ast.get_source_segment(source,n) for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
rows=[{'path':p.name,**{k:v for k,v in identity(p).items() if k!='mode'}} for p in sorted(TOOLS.iterdir()) if p.is_file() and p.name!='runtime-files.json']
assert len(rows)==7
write(TOOLS/'runtime-files.json',{'schema':1,'scope':'Exact isolated combined DayTrigger job tooling; excluded self is pinned by the workflow','files':rows})
workflow=SOURCE/'.github/workflows/day-trigger-wip-acceptance.yml'
text=workflow.read_text();text,n=re.subn(r"DAY_TRIGGER_RUNTIME_MANIFEST_SHA256: '[0-9a-f]{64}'","DAY_TRIGGER_RUNTIME_MANIFEST_SHA256: '"+identity(TOOLS/'runtime-files.json')['sha256']+"'",text);assert n==1;workflow.write_text(text)
allfiles=sorted(p for p in SOURCE.rglob('*') if p.is_file());assert len(allfiles)==9
pyrows=[]
for p in allfiles:
 if p.suffix=='.py':
  tree=ast.parse(p.read_text());pyrows.append({'path':str(p.relative_to(SOURCE)),'parsed':True,'test_methods':sum(isinstance(n,ast.FunctionDef) and n.name.startswith('test_') for n in ast.walk(tree))})
protected={'inputs.py':['require','pairs','document','read_json','encoded','write_json','byte_identity','identity','relative','regular','checked_identity','metadata','snapshot','validate_snapshot','input_name','derive','scan_inputs','compare_inputs','atomic_bytes','apply_changes','load_pins','verify_git_commit','verify_runtime_manifest'],
'run_acceptance.py':['command_clock','command_file_stat','CommandStreamEvidence','stop_owned_group','run_child'],
'verify.py':['count','flags','epoch_ns','Artifacts','checked_clock','row_clock','clocks_ordered','checked_stat','verify_file_creation','verify_command_stream_evidence','verify_execution','verify_wrapper_streams','verify_python','verify_apks','verify_suite_scope','retain_class','expected_numeric_commands','verify_numeric_commands','verify_java_policy','expected_provenance_config','verify_provenance_config','verify_numeric']}
unchanged=[]
for f,names in protected.items():
 before=nodes(PARENT/'tools/day_numeric_acceptance'/f);after=nodes(TOOLS/f)
 for name in names:
  assert before[name]==after[name],(f,name)
  unchanged.append({'path':f,'definition':name,'source_sha256':hashlib.sha256(before[name].encode()).hexdigest(),'exact_source_unchanged':True})
assert nodes(PARENT/'tools/day_numeric_acceptance/verify.py')['verify_gates'].replace('len(hashes) == 23', 'len(hashes) == 24') == nodes(TOOLS/'verify.py')['verify_gates']
before=ast.parse((PARENT/'tools/day_numeric_acceptance/test_day_numeric_acceptance.py').read_text());after=ast.parse((TOOLS/'test_day_trigger_acceptance.py').read_text())
def tests(tree):return sorted(c.name+'.'+n.name for c in tree.body if isinstance(c,ast.ClassDef) for n in c.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_'))
old=tests(before);new=tests(after);assert len(old)==92 and len(new)==142 and set(old)<=set(new)
OUT.mkdir(parents=True)
for p in allfiles:
 t=OUT/'source'/p.relative_to(SOURCE);t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,t)
patch=[]
for p in allfiles:
 rel=p.relative_to(SOURCE).as_posix();oldrel=rel.replace('day_trigger_acceptance','day_numeric_acceptance').replace('day-trigger-wip-acceptance.yml','day-numeric-wip-acceptance.yml').replace('test_day_trigger_acceptance.py','test_day_numeric_acceptance.py')
 q=PARENT/oldrel;assert q.is_file(),oldrel
 patch.extend(difflib.unified_diff(q.read_text().splitlines(keepends=True),p.read_text().splitlines(keepends=True),fromfile='parent/'+oldrel,tofile='candidate/'+rel))
(OUT/'tooling-derivation.patch').write_text(''.join(patch))
report={'schema':1,'status':'SOURCE_PARSES_SHARED_RECORDER_AND_NUMERIC_PROOF_EXACT_TESTS_NOT_RUN','created_utc':datetime.now(timezone.utc).isoformat(),'python_sources':pyrows,'protected_definitions':unchanged,'inherited_test_inventory':old,'new_test_inventory':sorted(set(new)-set(old)),'defined_tests':len(new),'tests_executed':0,'application_executions':0,'full_project_materializations':0,'lookup_commit':'39250fac022aee5551f36782bafd72cabbc33718','runtime_manifest':identity(TOOLS/'runtime-files.json'),'workflow':identity(workflow),'authoring_failure_preserved':{'operation':'apply_patch attempted delete and add for same README path','result':'invalid patch: multiple operations target README.md','files_modified_by_rejected_patch':0,'subsequent_action':'Complete README written as one file; no validation result invented'}}
write(OUT/'evidence/source-prevalidation.json',report)
shutil.copytree(ROOT/'combined-host-01/failures',OUT/'evidence/failed-draft-freezer')
write(OUT/'nine-path-bindings.json',{'files':[{'path':p.relative_to(SOURCE).as_posix(),'new_active_path_required_absent':True,**identity(p)} for p in allfiles]})
for name in ['derive_combined_tooling.py','combined_input_contract.py.txt','combined_lookup_verifier.py.txt','combined_tooling_tests.py.txt','freeze_combined_tooling_draft.py']:
 p=ROOT/name;t=OUT/'authoring'/name;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,t)
(OUT/'CHECKPOINT_SCOPE.md').write_text('''# Inactive combined acceptance tooling implementation draft

This checkpoint preserves substantial authored work before its test run. Exactly nine proposed new active tooling paths are under source/. No active path, application source, registry, APK or existing workflow has changed. It implements the reviewed three fixed checkouts, Numeric19 then Lookup21 physical boundaries, union25/new13 and separate schema-2 lookup19 verifier.

Python syntax parsing succeeded; 51 protected source definitions are byte-identical to the reviewed numeric tooling parent (see actual report count), including process recording/cleanup, stream verification and numeric proof. All inherited 92 test identities remain; 50 new tests are defined. **No tooling tests have been executed for this implementation yet.** Application builds, signing, the complete 16-gate run and Android execution are all pending and receive no credit.

The derivation patch and authoring inputs are retained. Templates record original authoring stages; source/ is the authoritative final draft (later extracted verifier helper functions are reflected in the patch/source). A rejected README patch made no changes and is explicitly recorded. Future validation attempts and corrections will be separate retained successors. All parents remain unchanged.

Intended inactive repository prefix: work-in-progress/day-trigger-lookup/11-combined-tooling-draft. The publisher owns activation after independent review; this capsule itself is not activation.
''')
# Fix the textual count from actual independently compared definitions.
s=(OUT/'CHECKPOINT_SCOPE.md').read_text().replace('51 protected source definitions',str(len(unchanged))+' protected source definitions');(OUT/'CHECKPOINT_SCOPE.md').write_text(s)
archive=OUT/'evidence.tar.gz'
with archive.open('wb') as raw:
 with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as gz:
  with tarfile.open(fileobj=gz,mode='w') as tf:
   for p in sorted((OUT/'evidence').rglob('*')):
    if not p.is_file():continue
    info=tf.gettarinfo(str(p),arcname=str(p.relative_to(OUT/'evidence')));info.uid=info.gid=0;info.uname=info.gname='';info.mtime=0
    with p.open('rb') as stream:tf.addfile(info,stream)
write(OUT/'evidence-inventory.json',{'files':[{'path':str(p.relative_to(OUT/'evidence')),**identity(p)} for p in sorted((OUT/'evidence').rglob('*')) if p.is_file()],'archive':identity(archive)})
files=[{'path':p.relative_to(OUT).as_posix(),**identity(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
checkpoint={'schema':1,'status':'INACTIVE_NINE_PATH_COMBINED_TOOLING_DRAFT_TESTS_PENDING','created_utc':datetime.now(timezone.utc).isoformat(),'repo_target':'work-in-progress/day-trigger-lookup/11-combined-tooling-draft','active_source_changed':False,'active_workflow_changed':False,'full_host_acceptance_executed':False,'application_executions':0,'full_project_materializations':0,'tests_executed':0,'defined_tooling_tests':142,'inherited_tooling_tests':92,'proposed_tooling_paths':9,'lookup_commit':report['lookup_commit'],'design_checkpoint_sha256':'3da7b4fa3707c301256c8dd7236c18f7680d2fb5bd72595d353e8a01b223830f','parent_tooling_checkpoint_sha256':'815612f827f1b0d2bcec90bbb1ae8a35a8c76ced8f6b5f44cf413bc40b81f493','runtime_manifest':report['runtime_manifest'],'evidence_archive':identity(archive),'evidence_file_count':3,'files':files}
write(OUT/'checkpoint.json',checkpoint)
print(json.dumps({'checkpoint':str(OUT/'checkpoint.json'),**identity(OUT/'checkpoint.json'),'source_paths':9,'files':len(files),'protected_definitions':len(unchanged),'defined_tests':142,'tests_executed':0,'runtime':report['runtime_manifest']},indent=2))
