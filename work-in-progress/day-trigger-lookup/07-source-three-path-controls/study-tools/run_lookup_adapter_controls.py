#!/usr/bin/env python3
"""Measure the unchanged 91-job prefix and ten actual original/JVM adapter faults."""
from __future__ import annotations
from datetime import datetime, timezone
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT/'stage-02/project'
BASELINE=ROOT/'stage-02/baseline'
ACTIVE=Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
PRIOR=ROOT/'reports/04-original-jvm-adapter'
JDK=Path('/workspace/scratch/4130730d15aa/tooling/jdk21/bin')
JAR=Path('/workspace/scratch/4130730d15aa/current/MacroDroid_v9/tools/lib/jadx-r2721.4574686-all.jar')
COUNTS={'case-sensitive':127,'reverse-receiver':3,'skip-null-entry':2,'null-query-early-return':3,
        'last-match':233,'trim-query':1,'indexed-loop':369,'extra-iteration-after-match':233,
        'swallow-iterator-fault':25,'replace-injected-npe-identity':6}

def identity(path):
    with path.open('rb') as stream: digest=hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':digest}
def save(path,value): path.write_text(json.dumps(value,indent=2)+'\n')
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module; spec.loader.exec_module(module); return module
def serial(jobs):
    return [{k:str(v) if isinstance(v,Path) else v for k,v in row.items()} for row in jobs]

def main():
    out=ROOT/'reports/06-compiled-adapter-controls';out.mkdir(parents=True,exist_ok=False)
    shutil.copy2(__file__,out/'executed-driver.py')
    result={'status':'RUNNING','passed':False,'started_utc':datetime.now(timezone.utc).isoformat(),
            'commands':[],'controls':[],'scope':'Ten actual Java lookup faults through the 371-case original/JVM UI adapter. Existing 91 jobs prepared and compared only. No full UI-suite, D8, signed-primary or Android execution.'}
    save(out/'result.json',result)
    def run(folder,name,argv,expected=0,timeout=90):
        folder.mkdir(parents=True,exist_ok=True)
        stdout,stderr=folder/(name+'.stdout.log'),folder/(name+'.stderr.log')
        started,tick=datetime.now(timezone.utc).isoformat(),time.monotonic();code=None
        env={**os.environ,'JAVA_HOME':str(JDK.parent),'PATH':str(JDK)+os.pathsep+os.environ.get('PATH',''),
             'TMPDIR':str(out),'PYTHONDONTWRITEBYTECODE':'1'}
        try:
            with stdout.open('xb') as so,stderr.open('xb') as se:
                code=subprocess.run(list(map(str,argv)),cwd=out,stdout=so,stderr=se,env=env,timeout=timeout).returncode
        finally:
            row={'name':name,'argv':list(map(str,argv)),'returncode':code,'expected_returncode':expected,
                 'started_utc':started,'duration_seconds':time.monotonic()-tick,'timeout_seconds':timeout,
                 'stdout':{'path':stdout.relative_to(out).as_posix(),**identity(stdout)},
                 'stderr':{'path':stderr.relative_to(out).as_posix(),**identity(stderr)}}
            result['commands'].append(row);save(out/'result.json',result)
        assert code==expected, name+': '+stderr.read_text(errors='replace')[-3000:]
    try:
        sys.path[:0]=[str(PROJECT),str(ACTIVE)]
        import build
        import ui_mutation_catalog as current_catalog
        current=load('lookup_current_controls',PROJECT/'ui_negative_control.py')
        old_catalog=load('lookup_baseline_catalog',BASELINE/'ui_mutation_catalog.py')
        sys.modules['ui_mutation_catalog']=old_catalog
        old=load('lookup_baseline_controls',BASELINE/'ui_negative_control.py')
        sys.modules['ui_mutation_catalog']=current_catalog
        assert current_catalog.__file__==str(PROJECT/'ui_mutation_catalog.py')
        assert current.ui_mutation_catalog is current_catalog and old.ui_mutation_catalog is old_catalog
        view=out/'preparation-inputs';view.mkdir()
        names={f'source/java/recovered/ui/{row[1]}.java' for row in current.CONTROLS}
        names.update([current_catalog.CATALOG_PATH,current_catalog.HELPER_PATH,current_catalog.DAY_CATALOG_PATH,
                      current_catalog.DAY_HELPER_PATH,current_catalog.LOOKUP_CATALOG_PATH,current_catalog.LOOKUP_HELPER_PATH])
        pins={}
        for name in sorted(names):
            source=PROJECT/name if (PROJECT/name).is_file() else ACTIVE/name
            pins[str(source)]=identity(source)
            target=view/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
            assert identity(source)==identity(target)
        for path in [PROJECT/'ui_mutation_catalog.py',PROJECT/'ui_negative_control.py',BASELINE/'ui_mutation_catalog.py',
                     BASELINE/'ui_negative_control.py',PROJECT/'tests/java/UiParityTests.java',PROJECT/'tests/java/DayLookupParityCases.java',
                     PROJECT/'tests/fixtures/original-methods.dex',PROJECT/'source/ui-methods.json',PROJECT/'tests/fixtures/original-dependencies.json',
                     PRIOR/'adapter-parity.json',PRIOR/'config.json',JAR,JDK/'java',JDK/'javac']:
            pins[str(path)]=identity(path)
        save(out/'source-inputs.json',pins)
        build.ROOT=view
        before=old.prepared_mutations();after=current.prepared_mutations()
        assert len(before)==91 and len(after)==101 and after[:91]==before
        assert current.CONTROLS==old.CONTROLS and len(current.CONTROLS)==54
        assert (PROJECT/'ui_mutation_catalog.py').read_bytes().startswith((BASELINE/'ui_mutation_catalog.py').read_bytes())
        save(out/'prior-91-prepared-jobs.json',serial(before));save(out/'current-101-prepared-jobs.json',serial(after))
        result['first_91_prepared_jobs_byte_and_order_exact']=True
        result['first_91_prepared_jobs_sha256']=identity(out/'prior-91-prepared-jobs.json')['sha256']
        base=json.loads((PRIOR/'adapter-parity.json').read_text());assert base['passed'] is True
        config=json.loads((PRIOR/'config.json').read_text())
        host,tools=PRIOR/'hostclasses',PRIOR/'harnessclasses'
        cp_base=[JAR,host,tools,ACTIVE/'build/java/hostclasses',ACTIVE/'tools/classes']
        def execute(folder,config,classpath,expected):
            save(folder/'config.json',config)
            run(folder,'execute',[JDK/'java','-Xverify:all','-XX:-OmitStackTraceInFastThrow','-cp',os.pathsep.join(map(str,classpath)),
                                  'LookupAdapterProbe',folder/'config.json',folder/'result.json'],expected)
            return json.loads((folder/'result.json').read_text())
        for job in after[91:]:
            name=job['name']; short=name.removeprefix('day-lookup-');folder=out/name;folder.mkdir()
            source=folder/'DayTriggerLookupMethods.java';source.write_text(job['mutant'])
            classes=folder/'classes';classes.mkdir()
            run(folder,'compile',[JDK/'javac','--release','8','-g:none','-cp',host,'-d',classes,source])
            compiled=classes/'recovered/ui/DayTriggerLookupMethods.class'
            assert sorted(p.relative_to(classes).as_posix() for p in classes.rglob('*') if p.is_file())==['recovered/ui/DayTriggerLookupMethods.class']
            assert identity(compiled)['sha256']!='df4383e951f3e897f58adc33f27847198f52cd455ccc5a9b22eb70712f66e082'
            cfg=copy.deepcopy(config);cfg['classPins']['recovered.ui.DayTriggerLookupMethods']={'path':str(compiled),**identity(compiled)}
            actual=execute(folder,cfg,[classes,*cp_base],2)
            assert actual['passed'] is False and actual['mismatches']==COUNTS[short] and actual['unsupported']==0
            assert set(job['required_cases']).issubset(actual['failedLabels'])
            assert actual['dayLookupOriginalCoverage']==base['dayLookupOriginalCoverage']
            assert actual['cases']==371 and actual['executionPaths']==2 and actual['methodsExecuted']==1
            expected_rows=base['dayLookupRawObservations'];actual_rows=actual['dayLookupRawObservations']
            assert len(expected_rows)==len(actual_rows)==742
            for left,right in zip(expected_rows,actual_rows):
                assert {k:v for k,v in left.items() if k!='observed'}=={k:v for k,v in right.items() if k!='observed'}
                if left['path']=='original': assert left==right
            assert all(identity(Path(path))==pin for path,pin in pins.items())
            result['controls'].append({'name':name,'passed':True,'mismatches':actual['mismatches'],'required_cases':job['required_cases'],
                                       'source':identity(source),'compiled':identity(compiled),'original_inputs_and_observations_unchanged':True})
            save(out/'result.json',result);print(name+': '+str(actual['mismatches'])+' detected',flush=True)
        restore=out/'positive-restoration';restore.mkdir()
        restored=execute(restore,config,cp_base,0)
        assert restored==base and (restore/'result.json').read_bytes()==(PRIOR/'adapter-parity.json').read_bytes()
        assert all(identity(Path(path))==pin for path,pin in pins.items())
        result.update(passed=True,status='TEN_COMPILED_LOOKUP_ADAPTER_FAULTS_DETECTED_EXACT_RESTORATION',
                      control_count=10,cases_per_execution=371,execution_paths=2,original_instructions=26,original_edges=4,
                      positive_restoration_byte_exact=True,restored_report=identity(restore/'result.json'),all_source_and_original_inputs_unchanged=True,
                      full_101_ui_controls_pending=True,signed_primary_proof_pending=True)
    except BaseException as error:
        result.update(status='FAILED_PRESERVED',error=repr(error));(out/'failure.traceback.txt').write_text(traceback.format_exc());raise
    finally:
        result['finished_utc']=datetime.now(timezone.utc).isoformat();save(out/'result.json',result)
        print(json.dumps({k:v for k,v in result.items() if k not in {'commands','controls'}},indent=2))
        assert sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())<=256*1024*1024

if __name__=='__main__':main()
