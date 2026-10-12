from pathlib import Path
from datetime import datetime,timezone
import ast,copy,difflib,hashlib,json,os,shutil,subprocess,sys,time,traceback,yaml
ROOT=Path('/dev/shm/macrodroid-day-lookup-integration')
SOURCE=ROOT/'combined-host-01/repository'
TOOLS=SOURCE/'tools/day_trigger_acceptance'
PARENT=Path('/dev/shm/day-numeric-hosted-02/checkpoints/02-hosted-filesystem-tooling-successor/source')
BASE=Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
NUM=Path('/dev/shm/day-numeric-hosted-02/checkpoints/01-command-filesystem-source-successor')
MERGE=ROOT/'checkpoints/04-numeric-filesystem-merge'
SUCCESSOR=ROOT/'checkpoints/05-lookup-recorder-successor'
OVERLAY=ROOT/'stage-04/project'
OUT=ROOT/'combined-host-01/reports/04-source-and-workflow-boundaries'
OUT.mkdir(parents=True,exist_ok=False)
sys.path.insert(0,str(TOOLS));import inputs,verify
read_rows={}
def bind(p):
 p=Path(p);row=inputs.identity(p)
 if str(p) in read_rows:assert read_rows[str(p)]==row
 read_rows[str(p)]=row;return row
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def inventory(root):return [{'path':p.relative_to(root).as_posix(),**bind(p)} for p in sorted(root.rglob('*')) if p.is_file()]
def source_nodes(p):
 bind(p);s=p.read_text();return {n.name:ast.get_source_segment(s,n) for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
result={'schema':1,'passed':False,'status':'COMBINED_SOURCE_WORKFLOW_VALIDATION_PENDING','started_utc':datetime.now(timezone.utc).isoformat(),'application_executions':0,'full_project_materializations':0,'full_host_acceptance_executed':False,'git_checkout_not_locally_repeated':True,'scope':'Actual frozen source bytes/full entry-map derivation, small source-policy copies, literal hosted tooling preflight, shell syntax, and explicit preflight faults only','commands':[]}
write(OUT/'result.json',result)
def command(name,argv,cwd,env,expected):
 folder=OUT/'commands'/name;folder.mkdir(parents=True)
 start=time.time_ns()
 with (folder/'stdout.log').open('xb') as out,(folder/'stderr.log').open('xb') as err:
  child=subprocess.run(argv,cwd=cwd,env=env,stdout=out,stderr=err,timeout=15)
 row={'name':name,'argv':argv,'cwd':str(cwd),'started_unix_ns':start,'finished_unix_ns':time.time_ns(),'timeout_seconds':15,'expected_returncode':expected,'returncode':child.returncode,'stdout':inputs.identity(folder/'stdout.log'),'stderr':inputs.identity(folder/'stderr.log')}
 result['commands'].append(row);assert child.returncode==expected,(name,child.returncode,expected,(folder/'stderr.log').read_text())
 return row
try:
 before=inventory(SOURCE);assert len(before)==9;write(OUT/'source-before.json',before)
 pins=inputs.load_pins()
 workflow=SOURCE/'.github/workflows/day-trigger-wip-acceptance.yml'
 loaded=yaml.load(workflow.read_text(),Loader=yaml.BaseLoader)
 pin=loaded['env']['DAY_TRIGGER_RUNTIME_MANIFEST_SHA256'];runtime=inputs.verify_runtime_manifest(pin)
 # No copied project: use the exact complete baseline manifest and frozen capsule roots read-only.
 base_path=BASE/'reports/release-input-snapshot.json';assert bind(base_path)=={k:pins['baseline_manifest'][k] for k in ('bytes','sha256')}
 base=inputs.validate_snapshot(inputs.read_json(base_path))
 capsule_manifest={}
 for role,path,spec in [('numeric',NUM,{'checkpoint':pins['overlay_checkpoint'],'file_count':408}),('merge',MERGE,pins['lookup_capsules']['merge']),('successor',SUCCESSOR,pins['lookup_capsules']['successor'])]:
  spec=copy.deepcopy(spec);spec['path']=path.name
  actual,manifest=inputs.checked_capsule(path.parent,spec);assert actual==path
  capsule_manifest[role]=manifest
  for f in sorted(path.rglob('*')):
   if f.is_file():bind(f)
 final_overlay=inputs.read_json(inputs.checked_identity(SUCCESSOR,'complete-future-overlay-manifest.json',pins['lookup_final_overlay_manifest']))
 middle,future=inputs.combined_inventory_contract(pins,base,capsule_manifest['numeric'],final_overlay)
 assert base['files']==81291 and middle['files']==81298 and future['files']==81304
 resolutions=[]
 for row,resolution in zip(pins['lookup_source_changes'],pins['lookup_payload_resolutions']):
  assert row['path']==resolution['path'] and row['source']==resolution['source']
  role=resolution['capsule'];assert (role=='successor')==(row['path'] in ('day_lookup_dex_controls.py','tests/test_day_lookup.py'))
  p=({'merge':MERGE,'successor':SUCCESSOR})[role]/resolution['source'];assert bind(p)==row['candidate']
  assert bind(OVERLAY/row['path'])==row['candidate']
  resolutions.append({'path':row['path'],'capsule':role,'input':str(p),**row['candidate']})
 assert len(resolutions)==21
 for row in pins['numeric_only_files']:assert bind(OVERLAY/row['path'])=={'bytes':row['size'],'sha256':row['sha256']}
 result['source_boundaries']=[{k:value[k] for k in ('files','snapshot_sha256')} for value in (base,middle,future)]
 result['resolved_lookup_payloads']=resolutions;result['numeric_only_files']=pins['numeric_only_files']
 # Independently exercise the new exact registry and source-backed cwd guards with actual file bytes.
 result['combined_registry']=verify.verify_combined_registry(OVERLAY,pins)
 for name in ('source/java-method-map.json','tests/fixtures/original-dependencies.json','tests/fixtures/provenance.json'):bind(OVERLAY/name)
 policy=OUT/'actual-producer-source-copy';policy.mkdir()
 for name,expected in pins['method_producer_sources'].items():
  src=(BASE if name=='build.py' else OVERLAY)/name;assert bind(src)==expected
  shutil.copyfile(src,policy/name);assert inputs.identity(policy/name)==expected
 result['cwd_source_guard']=verify.verify_method_producer_cwd(policy,pins,{'execution':{'cwd':str(policy.resolve())}})
 result['cwd_source_guard']['scope_note']='Source-policy-only copy of four exact production files; no producer subprocess/app execution'
 # Exact inheritance: changed application-count gates are listed separately.
 protected={'inputs.py':['require','pairs','document','read_json','encoded','write_json','byte_identity','identity','relative','regular','checked_identity','metadata','snapshot','validate_snapshot','input_name','derive','scan_inputs','compare_inputs','atomic_bytes','apply_changes','load_pins','verify_git_commit','verify_runtime_manifest'],
 'run_acceptance.py':['command_clock','command_file_stat','CommandStreamEvidence','stop_owned_group','run_child'],
 'verify.py':['count','flags','epoch_ns','Artifacts','checked_clock','row_clock','clocks_ordered','checked_stat','verify_file_creation','verify_command_stream_evidence','verify_execution','verify_wrapper_streams','verify_python','verify_apks','verify_suite_scope','retain_class','expected_numeric_commands','verify_numeric_commands','verify_java_policy','expected_provenance_config','verify_provenance_config','verify_numeric']}
 same=[]
 for name,defs in protected.items():
  a,b=source_nodes(PARENT/'tools/day_numeric_acceptance'/name),source_nodes(TOOLS/name)
  for n in defs:
   assert a[n]==b[n],(name,n);same.append({'path':name,'definition':n,'sha256':hashlib.sha256(a[n].encode()).hexdigest()})
 a,b=source_nodes(PARENT/'tools/day_numeric_acceptance/verify.py'),source_nodes(TOOLS/'verify.py')
 assert a['verify_gates'].replace('len(hashes) == 23','len(hashes) == 24')==b['verify_gates']
 assert a['verify_other_gates'].replace('1243','1244').replace('Static/linkage gate omitted the numeric body','Static/linkage gate omitted a recovered DayTrigger method')==b['verify_other_gates']
 result['exact_preserved_definitions']=same;result['fresh_report_only_gate_change']='23 to 24'
 def tests(p):
  bind(p);s=p.read_text();return {c.name+'.'+n.name:ast.get_source_segment(s,n) for c in ast.parse(s).body if isinstance(c,ast.ClassDef) for n in c.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')}
 old,new=tests(PARENT/'tools/day_numeric_acceptance/test_day_numeric_acceptance.py'),tests(TOOLS/'test_day_trigger_acceptance.py')
 assert len(old)==92 and len(new)==153 and set(old)<=set(new)
 result['inherited_test_count']=len(old);result['new_test_count']=len(new)-len(old)
 result['inherited_test_changes']=[{'test':n,'diff':''.join(difflib.unified_diff(old[n].splitlines(True),new[n].splitlines(True),fromfile='numeric-parent/'+n,tofile='combined/'+n))} for n in sorted(old) if old[n]!=new[n]]
 # Actual shell syntax for every run step; action blocks remain source inspections.
 steps=loaded['jobs']['isolated-day-trigger-source']['steps'];assert len(steps)==11
 action_pins={'actions/checkout@11d5960a326750d5838078e36cf38b85af677262','actions/setup-java@cf277c60eb25467037889841efdb72551f06f6c3','actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02'}
 assert {s['uses'] for s in steps if 'uses' in s}==action_pins
 checkouts=[s['with'] for s in steps if s.get('uses','').startswith('actions/checkout@')]
 assert [s['ref'] for s in checkouts]==['${{ github.sha }}',pins['baseline_commit'],pins['overlay_commit'],pins['lookup_commit']]
 assert loaded['jobs']['isolated-day-trigger-source']['timeout-minutes']=='120'
 assert loaded['on']['push']['paths']==loaded['on']['pull_request']['paths']==['tools/day_trigger_acceptance/**','.github/workflows/day-trigger-wip-acceptance.yml']
 assert all(s['with']['persist-credentials']=='false' for s in steps if s.get('uses','').startswith('actions/checkout@'))
 assert steps[-1]['if']=='always()' and steps[-1]['with']['include-hidden-files']=='true'
 assert steps[-2]['if']=="always() && steps.tool-inputs.outcome == 'success'"
 env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',DAY_TRIGGER_RUNTIME_MANIFEST_SHA256=pin)
 for i,s in enumerate(steps):
  if 'run' not in s:continue
  script=OUT/'shell'/('%02d.sh'%i);script.parent.mkdir(exist_ok=True);script.write_text(s['run']+'\n')
  command('shell-syntax-%02d'%i,['bash','-n',str(script)],OUT,env,0)
 preflight=next(s['run'] for s in steps if s.get('id')=='tool-inputs')
 raw_inputs=[]
 for name in ('clean','changed-runtime-source','extra-runtime-file','changed-runtime-manifest','wrong-workflow-pin','symlink-runtime-source'):
  folder=OUT/'preflight'/name;folder.mkdir(parents=True);shutil.copytree(SOURCE,folder/'job-source')
  localenv=env.copy();tool=folder/'job-source/tools/day_trigger_acceptance'
  if name=='changed-runtime-source':(tool/'verify.py').write_bytes((tool/'verify.py').read_bytes()+b'\n# deliberate source fault\n')
  elif name=='extra-runtime-file':(tool/'unlisted.py').write_bytes(b'EXTRA POLICY FIXTURE')
  elif name=='changed-runtime-manifest':(tool/'runtime-files.json').write_bytes((tool/'runtime-files.json').read_bytes()+b'\n')
  elif name=='wrong-workflow-pin':localenv['DAY_TRIGGER_RUNTIME_MANIFEST_SHA256']='0'*64
  elif name=='symlink-runtime-source':
   shutil.copyfile(tool/'verify.py',folder/'outside-verify.py');(tool/'verify.py').unlink();(tool/'verify.py').symlink_to(folder/'outside-verify.py')
  outcome=command('literal-preflight-'+name,['bash','-euo','pipefail','-c',preflight],folder,localenv,0 if name=='clean' else 1)
  if name=='clean':
   value=inputs.read_json(folder/'hosted-tool-source-verification.json');assert value['passed'] is True and value['manifest_sha256']==pin and value['files']==runtime['files']
  else:assert not (folder/'hosted-tool-source-verification.json').exists()
  raw_inputs.append({'case':name,'intended_exit':outcome['expected_returncode'],'actual_exit':outcome['returncode'],'scope':'Tooling bootstrap fixture; no app commands'})
 result['actual_literal_preflight_controls']=raw_inputs
 result['runtime_manifest']=bind(TOOLS/'runtime-files.json');result['workflow']=bind(workflow)
 result['source_after']=inventory(SOURCE);assert result['source_after']==before
 for name,identity in read_rows.items():assert inputs.identity(Path(name))==identity,('changed-bound-read',name)
 write(OUT/'exact-read-boundaries.json',read_rows)
 result['bound_read_files']=len(read_rows);result['all_bound_reads_unchanged']=True
 result['passed']=True;result['status']='COMBINED_TOOLING_SOURCE_AND_LITERAL_WORKFLOW_PREFLIGHT_PASSED_NO_APP_EXECUTION'
except BaseException as error:
 result['error']=repr(error);(OUT/'traceback.txt').write_text(traceback.format_exc());print(traceback.format_exc(),file=sys.stderr)
finally:
 result['finished_utc']=datetime.now(timezone.utc).isoformat();write(OUT/'result.json',result)
 print(json.dumps({k:result[k] for k in ['status','passed','bound_read_files','source_boundaries','inherited_test_count','new_test_count','error'] if k in result},indent=2))
sys.exit(0 if result['passed'] else 2)
