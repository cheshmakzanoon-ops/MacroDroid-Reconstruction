#!/usr/bin/env python3
"""Apply new strict report guards to closed real rows and deliberate data faults.

These are report/observer controls only, with zero new application executions or
instruction credit. Original command outcomes and report bytes remain unchanged.
"""
from pathlib import Path
from datetime import datetime, timezone
import copy
import hashlib
import json
import shutil
import sys
import time

ROOT=Path(__file__).resolve().parent;PROJECT=ROOT/'stage-02/project'
ACTUAL=ROOT/'reports/12-micro-dex-three-path-corrected'
ACTIVE=Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')

def identity(path):
    with path.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':digest}
def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')

def main():
    out=ROOT/'reports/15-raw-report-guard-controls';out.mkdir(parents=True,exist_ok=False)
    shutil.copy2(__file__,out/'executed-driver.py');tick=time.monotonic_ns()
    result={'status':'RUNNING','passed':False,'started_utc':datetime.now(timezone.utc).isoformat(),
            'applicationExecutions':0,'applicationInstructionCredit':0,'controls':[]}
    save(out/'result.json',result)
    sys.path[:0]=[str(PROJECT),str(ACTIVE)]
    import day_lookup_dex_controls as lookup
    paths=[PROJECT/'day_lookup_dex_controls.py',PROJECT/'day_numeric_dex_controls.py',PROJECT/'ui_mutation_catalog.py',
           ACTUAL/'positive/result.json',ACTUAL/'positive/config.json',ACTUAL/'case-sensitive-dex-fault/result.json',
           ACTUAL/'case-sensitive-dex-fault/config.json',ACTUAL/'last-match-dex-fault/result.json',ACTUAL/'last-match-dex-fault/config.json']
    pins={str(path):identity(path) for path in paths};save(out/'input-identities.json',pins)
    for path in paths[:3]:shutil.copy2(path,out/path.name)
    positive=json.loads(paths[3].read_text());config=json.loads(paths[4].read_text())
    lookup.validate_execution_binding(positive,config);lookup.validate_positive(positive)
    for name,count,required in [('case-sensitive',127,'day-lookup:first-duplicate-entry-identity'),('last-match',233,'day-lookup:empty-string-match')]:
        report=json.loads((ACTUAL/(name+'-dex-fault')/'result.json').read_text())
        cfg=json.loads((ACTUAL/(name+'-dex-fault')/'config.json').read_text())
        lookup.validate_execution_binding(report,cfg);lookup.validate_fault(positive,report,[required],count,'rebuilt')
    def select(report,name):return next(row for row in report['observations'] if row['case']==name)
    def change_all(report,name,key,value):
        row=select(report,name)
        for path in ('original','java','rebuilt'):row[path][key]=copy.deepcopy(value)
    def reject(name,mutate,reason):
        row=copy.deepcopy(positive);mutate(row);save(out/(name+'.json'),row)
        try:
            lookup.validate_execution_binding(row,config);lookup.validate_positive(row)
        except RuntimeError as error:
            assert reason in str(error),(name,str(error))
            result['controls'].append({'name':name,'rejected':True,'error':str(error),'report':identity(out/(name+'.json'))})
        else:raise AssertionError('False positive: '+name)
        save(out/'result.json',result)
    reject('changed-query-input',lambda r:select(r,'empty')['keysUtf16Hex'].append('0064'),'input identities')
    reject('reordered-inputs',lambda r:r['observations'].reverse(),'input identities')
    reject('changed-independent-first-identity',lambda r:select(r,'first-duplicate-entry-identity').update(expectedReturnIndex=1),'input identities')
    reject('omitted-original-path',lambda r:select(r,'empty').pop('original'),'observation inventory')
    reject('all-path-wrong-first-identity',lambda r:change_all(r,'first-duplicate-entry-identity','returnIndex',1),'outcome flags')
    reject('all-path-extra-iterator-read',lambda r:change_all(r,'first-duplicate-entry-identity','events',['iterator','hasNext@0','next@0','hasNext@1']),'outcome flags')
    reject('all-path-changed-injected-message',lambda r:change_all(r,'injected-iterator-npe','rawMessage','CHANGED'),'outcome flags')
    reject('all-path-replaced-injected-object',lambda r:change_all(r,'injected-iterator-npe','injectedExceptionIdentity',False),'outcome flags')
    reject('vm-null-case-wrong-exception-type',lambda r:change_all(r,'dictionary-null','exceptionClass','java.lang.ClassCastException'),'outcome flags')
    reject('expanded-message-exclusion-scope',lambda r:r['generatedNullMessageCases'].append('injected-iterator-npe'),'scope identity')
    reject('boolean-recovered-method-credit',lambda r:r.update(primaryRecoveredMethods=True),'count or schema')
    reject('observer-control-application-credit',lambda r:r['observerRecordControls'].update(applicationExecutions=1),'application credit')
    reject('missing-original-instruction',lambda r:r['originalCoverage']['methods'][0]['executedOffsets'].pop(),'Incomplete')
    reject('uncredited-getter-counted-as-recovered',lambda r:r['originalCoverage']['methods'][1].update(primaryRecovery=True),'recovery credit')
    reject('wrong-recorded-original-fixture',lambda r:r['inputIdentities']['originalFixture'].update(sha256='0'*64),'another command')
    reject('wrong-loaded-helper-origin',lambda r:r['loadedClassOrigins'][lookup.HELPER_NAME].update(sha256='0'*64),'loaded class origins')
    allowed=copy.deepcopy(positive)
    for path in ('original','java','rebuilt'):
        select(allowed,'dictionary-null')[path]['rawMessage']='RETAINED_DIAGNOSTIC_VARIANT_'+path
    save(out/'allowed-exact-vm-null-message-variant.json',allowed)
    lookup.validate_execution_binding(allowed,config);lookup.validate_positive(allowed)
    # This record-only acceptance is intentional and restricted to the exact pinned
    # VM-null case. It does not alter the original report or the actual JVM outputs.
    result['allowed_control']={'case':'dictionary-null','field':'rawMessage','accepted':True,
                              'applicationExecutions':0,'applicationInstructionCredit':0}
    assert all(identity(Path(path))==pin for path,pin in pins.items())
    result.update(passed=True,status='SIXTEEN_RAW_PROOF_FAULTS_REJECTED_EXACT_VM_MESSAGE_SCOPE_CONFIRMED',
                  controls_rejected=len(result['controls']),closed_real_positive_and_two_fault_reports_revalidated=True,
                  original_reports_and_source_unchanged=True,finished_utc=datetime.now(timezone.utc).isoformat(),
                  duration_nanoseconds=time.monotonic_ns()-tick)
    save(out/'result.json',result);print(json.dumps({k:v for k,v in result.items() if k!='controls'},indent=2))

if __name__=='__main__':main()
