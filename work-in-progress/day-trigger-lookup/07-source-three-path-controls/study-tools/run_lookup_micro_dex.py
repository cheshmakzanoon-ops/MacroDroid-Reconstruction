#!/usr/bin/env python3
"""Small production-D8 study, borrowing only exact existing APK getter bytes.

This does not invoke the acceptance entry, claim the new primary is packaged, or
copy/build/sign an APK. The old APK primary is independently compared and kept
separate from the newly compiled one-method target.
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import traceback

ROOT=Path(__file__).resolve().parent;PROJECT=ROOT/'stage-02/project'
ACTIVE=Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
PRIOR=ROOT/'reports/04-original-jvm-adapter'
JDK=Path('/workspace/scratch/4130730d15aa/tooling/jdk21/bin')
JAR=Path('/workspace/scratch/4130730d15aa/current/MacroDroid_v9/tools/lib/jadx-r2721.4574686-all.jar')

def identity(path):
    with path.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':digest}
def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')

def main():
    out=ROOT/'reports/12-micro-dex-three-path-corrected';out.mkdir(parents=True,exist_ok=False)
    shutil.copy2(__file__,out/'executed-driver.py')
    result={'status':'RUNNING','passed':False,'started_utc':datetime.now(timezone.utc).isoformat(),
            'commands':[],'androidRuntime':False,'new_signed_apk':False,'new_primary_packaged':False,
            'scope':'One-method micro-DEX over the 371-case lookup inventory. The two getters are bound to unchanged active APK bytes; its old p0 body is not a new signed-primary proof. No full acceptance invocation.'}
    save(out/'result.json',result)
    def run(folder,name,argv,expected=0,timeout=120):
        folder.mkdir(parents=True,exist_ok=True)
        so,se=folder/(name+'.stdout.log'),folder/(name+'.stderr.log');started=datetime.now(timezone.utc).isoformat();tick=time.monotonic_ns();code=None
        try:
            with so.open('xb') as stdout,se.open('xb') as stderr:
                code=subprocess.run(list(map(str,argv)),cwd=out,stdout=stdout,stderr=stderr,timeout=timeout,
                    env={**os.environ,'JAVA_HOME':str(JDK.parent),'PATH':str(JDK)+os.pathsep+os.environ.get('PATH',''),
                         'TMPDIR':str(out),'PYTHONDONTWRITEBYTECODE':'1'}).returncode
        finally:
            result['commands'].append({'name':name,'argv':list(map(str,argv)),'started_utc':started,
                'duration_nanoseconds':time.monotonic_ns()-tick,'returncode':code,'expected_returncode':expected,'timeout_seconds':timeout,
                'stdout':{'path':so.relative_to(out).as_posix(),**identity(so)},'stderr':{'path':se.relative_to(out).as_posix(),**identity(se)}})
            save(out/'result.json',result)
        assert code==expected,name+': '+se.read_text(errors='replace')[-3000:]
    try:
        sys.path[:0]=[str(PROJECT),str(ACTIVE)]
        import build
        import day_lookup_dex_controls as lookup
        import ui_mutation_catalog as catalog
        entry=lookup.target_entry(PROJECT)
        index=json.loads((ACTIVE/'source/class-index.json').read_text())
        old=next(ACTIVE/row['path'] for row in index.values() if row['descriptor']==lookup.TARGET)
        apk=ACTIVE/'dist/MacroDroid-5.67.8-v9-hybrid.apk';getter=ACTIVE/'build/hybrid/classes3.dex'
        fixture=PROJECT/'tests/fixtures/original-methods.dex'
        paths=[PROJECT/name for name in ['day_lookup_dex_controls.py','day_numeric_dex_controls.py','ui_mutation_catalog.py',
            'source/java/recovered/ui/DayTriggerLookupMethods.java','source/java/recovered/ui/DayTriggerValueMethods.java',
            'test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java','tests/java/DayLookupControlHarness.java',
            'tests/java/DayLookupParityCases.java','source/java-method-map.json','tests/fixtures/original-dependencies.json',
            'tests/fixtures/day-lookup-mutants.json']]
        paths += [fixture,old,apk,getter,JAR,JDK/'java',JDK/'javac',JDK.parent/'release',ACTIVE/'source/class-index.json',
                  ACTIVE/'build.py',ACTIVE/'constructor_owner.py',ACTIVE/'tests/java/BytecodeOracle.java',
                  ACTIVE/'tools/classes/InspectMethod.class',ACTIVE/'tools/src/InspectMethod.java']
        pins={str(path):identity(path) for path in paths};save(out/'source-and-external-inputs.json',pins)
        assert pins[str(apk)]['sha256']=='5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'
        assert pins[str(ACTIVE/'build.py')]['sha256']=='dd599090fc075fed0835875937a2c2b76d91381936c26f4275f876edf47345f0'
        assert pins[str(ACTIVE/'tests/java/BytecodeOracle.java')]['sha256']=='d91ddcd8ec3d67d41d69b8252835e747c2cad2c6d5ea898323794ceec30e6b56'
        for path in paths:
            if path.is_relative_to(PROJECT):
                saved=out/'executed-sources'/path.relative_to(PROJECT);saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,saved)
        host,tools=out/'hostclasses',out/'harnessclasses';host.mkdir();tools.mkdir()
        families=[(PRIOR/'hostclasses','com/arlosoft/macrodroid/variables/VariableValue',host),
                  (PRIOR/'hostclasses','recovered/ui/DayTriggerLookupMethods',host),
                  (ACTIVE/'build/java/hostclasses','defpackage/EngineRuntime',host),
                  (ACTIVE/'build/java/hostclasses','defpackage/TestClock',host),
                  (PRIOR/'harnessclasses','DayLookupParityCases',tools),
                  (PRIOR/'harnessclasses','BytecodeOracle',tools),
                  (ROOT/'reports/07-control-harness-compile/classes','DayLookupControlHarness',tools)]
        for source_root,prefix,destination in families:
            stem=source_root/prefix
            for path in sorted(stem.parent.glob(stem.name+'*.class')):
                if path.name!=stem.name+'.class' and not path.name.startswith(stem.name+'$'):continue
                copied=destination/path.relative_to(source_root);copied.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,copied)
                pins[str(path)]=identity(path);assert identity(path)==identity(copied)
        class_pins=lookup.class_pins(host,tools)
        for row in class_pins.values():pins[row['path']]=identity(Path(row['path']))
        save(out/'source-and-external-inputs.json',pins)
        cp=os.pathsep.join(map(str,[JAR,host,tools,PRIOR/'harnessclasses',ACTIVE/'build/java/hostclasses',ACTIVE/'tools/classes']))
        positive_dex,binding=lookup.compile_target(build,ACTIVE,index,entry,host/lookup.HELPER_CLASS,out/'positive-pipeline',run,JDK/'java',JAR)
        for name,dex in [('old-signed-apk',getter),('new-positive-micro-dex',positive_dex)]:
            run(out,name+'-instructions',[JDK/'java','-Xmx512m','-cp',cp,'InspectMethod',dex,lookup.METHOD,out/(name+'-instructions.json')])
        old_signed_matches=(out/'old-signed-apk-instructions.json').read_bytes()==(out/'new-positive-micro-dex-instructions.json').read_bytes()
        assert old_signed_matches is False, 'Existing APK unexpectedly has new target instructions; inspect without relabeling'
        cfg={'schema':1,'originalFixture':{'path':str(fixture),'sha256':lookup.sha(fixture)},
             'rebuiltApk':{'path':str(apk),'sha256':lookup.sha(apk)},
             'rebuiltGetterDex':{'path':str(getter),'sha256':lookup.sha(getter),'apk_member':'classes3.dex'},
             'targetDex':{'path':str(positive_dex),'sha256':lookup.sha(positive_dex)},'classPins':class_pins}
        def execute(name,config,expected=0):
            folder=out/name;folder.mkdir();save(folder/'config.json',config)
            run(folder,'execute',[JDK/'java','-Xverify:all','-XX:-OmitStackTraceInFastThrow','-Xmx512m','-cp',cp,
                                  'DayLookupControlHarness',folder/'config.json',folder/'result.json'],expected)
            return json.loads((folder/'result.json').read_text()) if (folder/'result.json').exists() else None
        positive=execute('positive',cfg);lookup.validate_positive(positive)
        jobs={row['name'].removeprefix('day-lookup-'):row for row in catalog.load_lookup_mutations(PROJECT)}
        faults=[]
        for name in ('case-sensitive','last-match'):
            compiled=ROOT/'reports/06-compiled-adapter-controls'/('day-lookup-'+name)/'classes'/lookup.HELPER_CLASS
            source=compiled.parents[3]/'DayTriggerLookupMethods.java'
            assert source.read_text()==jobs[name]['mutant']
            pins[str(source)]=identity(source);pins[str(compiled)]=identity(compiled)
            dex,bad_binding=lookup.compile_target(build,ACTIVE,index,entry,compiled,out/(name+'-pipeline'),run,JDK/'java',JAR)
            altered=copy.deepcopy(cfg);altered['targetDex']={'path':str(dex),'sha256':lookup.sha(dex)}
            report=execute(name+'-dex-fault',altered,3)
            lookup.validate_fault(positive,report,jobs[name]['required_cases'],lookup.JAVA_FAILURE_COUNTS[name],'rebuilt')
            faults.append({'name':name,'passed':True,'mismatches':report['mismatchCount'],'binding':bad_binding})
        altered=copy.deepcopy(cfg);altered['targetDex']=copy.deepcopy(cfg['originalFixture'])
        assert execute('original-as-rebuilt-rejected',altered,1) is None
        assert 'Original fixture cannot masquerade as rebuilt target' in (out/'original-as-rebuilt-rejected/execute.stderr.log').read_text()
        altered=copy.deepcopy(cfg);altered['classPins'][lookup.HELPER_NAME]['sha256']='0'*64
        assert execute('wrong-helper-class-rejected',altered,1) is None
        assert 'Wrong input identity: class '+lookup.HELPER_NAME in (out/'wrong-helper-class-rejected/execute.stderr.log').read_text()
        restored=execute('positive-restoration',cfg);lookup.validate_positive(restored)
        assert restored==positive and (out/'positive/result.json').read_bytes()==(out/'positive-restoration/result.json').read_bytes()
        assert all(identity(Path(path))==pin for path,pin in pins.items())
        save(out/'source-and-external-inputs.json',pins)
        result.update(passed=True,status='LOOKUP_MICRO_DEX_THREE_PATH_AND_TWO_FAULTS_PASSED_SIGNED_PRIMARY_PENDING',
                      cases=371,execution_paths=3,original_instructions=26,rebuilt_instructions=23,conditional_edges_per_path=4,
                      actual_dex_faults=faults,provenance_faults_rejected=2,positive_pipeline=binding,
                      positive_restoration_byte_exact=True,old_signed_apk_primary_matches_new_body=False,
                      original_source_and_compiled_inputs_unchanged=True,full_101_ui_controls_pending=True)
    except BaseException as error:
        result.update(status='FAILED_PRESERVED',error=repr(error));(out/'failure.traceback.txt').write_text(traceback.format_exc());raise
    finally:
        result['finished_utc']=datetime.now(timezone.utc).isoformat();save(out/'result.json',result)
        print(json.dumps({k:v for k,v in result.items() if k not in {'commands','actual_dex_faults','positive_pipeline'}},indent=2))
        assert sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())<=256*1024*1024

if __name__=='__main__':main()
