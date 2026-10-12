from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,re,shutil,subprocess,sys,time
ROOT=Path('/dev/shm/macrodroid-day-lookup-integration')
def identity(p):
 raw=p.read_bytes();return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def inventory(root):return [{'path':p.relative_to(root).as_posix(),**identity(p)} for p in sorted(root.rglob('*')) if p.is_file()]
def write(p,v):p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
a=argparse.ArgumentParser();a.add_argument('attempt');a.add_argument('--source',type=Path,default=ROOT/'combined-host-01/repository');args=a.parse_args()
output=ROOT/'combined-host-01/reports'/args.attempt;output.mkdir(parents=True,exist_ok=False)
source=args.source;before=inventory(source);assert len(before)==9
shutil.copytree(source,output/'executed-source');assert inventory(output/'executed-source')==before
write(output/'source-before.json',before)
(output/'tmp').mkdir();runtime=output/'executed-source/tools/day_trigger_acceptance'
env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(output/'tmp'),DAY_TRIGGER_CONTROL_EVIDENCE_ROOT=str(output/'controls'))
command=[sys.executable,'-B','-m','unittest','discover','-s',str(runtime),'-p','test_*.py','-v']
result={'schema':1,'status':'TOOLING_CONTROL_ATTEMPT_NOT_CLOSED','passed':False,'started_utc':datetime.now(timezone.utc).isoformat(),'argv':command,'cwd':str(output),'timeout_seconds':300,'application_executions':0,'full_project_materializations':0,'android_runtime_executed':False,'scope':'Inherited and new tooling policy/owned bounded Python subprocess controls only','source_before':before}
start=time.monotonic();write(output/'result.json',result)
try:
 with (output/'stdout.log').open('xb') as stdout,(output/'stderr.log').open('xb') as stderr:
  child=subprocess.run(command,cwd=output,env=env,stdout=stdout,stderr=stderr,timeout=300)
 result['returncode']=child.returncode
except BaseException as error:result['error']=repr(error)
finally:
 result['elapsed_seconds']=time.monotonic()-start;result['finished_utc']=datetime.now(timezone.utc).isoformat()
 result['source_after']=inventory(source);result['executed_source_after']=inventory(output/'executed-source')
 result['sources_unchanged']=result['source_after']==before and result['executed_source_after']==before
 log=(output/'stderr.log').read_text();match=re.search(r'Ran (\d+) tests in ([0-9.]+)s',log)
 result['observed_tests']=int(match[1]) if match else None;result['unittest_seconds']=float(match[2]) if match else None
 result['observed_final_line']=log.strip().splitlines()[-1] if log.strip() else ''
 result['passed']=result.get('returncode')==0 and result['sources_unchanged'] and result['observed_final_line']=='OK'
 result['status']='TOOLING_CONTROLS_PASSED_NO_APPLICATION_EXECUTION' if result['passed'] else 'TOOLING_CONTROL_ATTEMPT_FAILED'
 result['logs']={n:identity(output/n) for n in ('stdout.log','stderr.log')};write(output/'result.json',result)
 print(json.dumps({k:result[k] for k in ['status','returncode','elapsed_seconds','observed_tests','observed_final_line','sources_unchanged'] if k in result},indent=2))
sys.exit(0 if result['passed'] else 2)
