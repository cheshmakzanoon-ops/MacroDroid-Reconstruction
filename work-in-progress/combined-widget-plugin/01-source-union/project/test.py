#!/usr/bin/env python3
"""Run registered migration suites with explicit two/three-path evidence.
The instruction oracle is a bounded host interpreter, not ART or Android.
--three-way also checks that every interpreted rebuilt DEX is in the signed APK.
"""
from __future__ import annotations
import argparse,hashlib,json,os,sys,zipfile
from pathlib import Path
import build

def aggregate_reports(reports:dict[str,dict],expected:int,paths:int)->dict:
    """Fail closed on missing suites, malformed counts, failures or wrong paths."""
    required={'legacy','core','environment','engine','ui'}
    schema=type(expected) is int and expected>0 and type(paths) is int and paths in (2,3)
    for r in reports.values():
        for key,value in [('methods',r.get('methodsCovered')),('cases',r.get('cases')),
                          ('failures',r.get('failedCases',r.get('failures'))),('unsupported',r.get('unsupportedExecutions'))]:
            if type(value) is not int or value<0 or (key in ('methods','cases') and value==0):schema=False
    if not schema:
        return {'passed':False,'cases':0,'methodsCovered':0,'methodsExpected':expected,'paths':paths,
                'failedCases':0,'unsupportedExecutions':0,'androidRuntime':False,'suiteCases':{},
                'schemaValid':False,'scope':'Invalid host-report schema; no acceptance'}
    covered=sum(r['methodsCovered'] for r in reports.values())
    cases=sum(r['cases'] for r in reports.values())
    failed=sum(r.get('failedCases',r.get('failures',0)) for r in reports.values())
    unsupported=sum(r['unsupportedExecutions'] for r in reports.values())
    valid=all(r.get('passed',r.get('pass',False)) is True and type(r.get('paths')) is int and r.get('paths')==paths for r in reports.values())
    return {'passed':valid and set(reports)==required and covered==expected and failed==0 and unsupported==0,
            'cases':cases,'methodsCovered':covered,'methodsExpected':expected,'paths':paths,'schemaValid':True,
            'failedCases':failed,'unsupportedExecutions':unsupported,'androidRuntime':False,
            'suiteCases':{k:r['cases'] for k,r in reports.items()},'scope':'Bounded host comparison only; not Android execution'}

def validate_method_partition(reports:dict[str,dict],registry:list[dict])->None:
    """Count equality alone cannot hide duplicate tests or untested replacements."""
    expected_keys={e['target']+'->'+e['method'] for e in registry}
    if len(expected_keys)!=len(registry):raise RuntimeError('Duplicate migration registry key')
    flat=[]
    for report in reports.values():
        keys=report.get('methodKeys')
        if not isinstance(keys,list) or any(not isinstance(k,str) for k in keys):raise RuntimeError('Missing or invalid executed method-key list')
        if len(keys)!=report.get('methodsCovered') or len(set(keys))!=len(keys):raise RuntimeError('A suite omitted or duplicated its executed method-key inventory')
        flat.extend(keys)
    if len(flat)!=len(set(flat)) or set(flat)!=expected_keys:raise RuntimeError('Executed suite method keys do not exactly partition the migration registry')

def main()->None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--three-way',action='store_true')
    args=ap.parse_args();build.bootstrap()
    build.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],'python-unit-tests.log')
    build.compile_java()
    build.run([sys.executable,'validate_migration.py'],'static-migration-validation.log')
    build.run([sys.executable,'linkage_verify.py'],'static-migration-linkage.log')
    cp=os.pathsep.join(map(str,[build.JAR,build.WORK/'java/hostclasses',build.TOOLS]))
    build.run(['javac','-cp',cp,'-d',build.TOOLS,*sorted((build.ROOT/'tests/java').glob('*.java'))],'compile-host-tests.log')
    for fixture,output,mainclass,logbase in [
        ('opcode-conformance.smali','oracle-conformance.dex','OracleSemanticsTests','oracle-conformance'),
        ('engine-opcodes.smali','engine-opcodes.dex','EngineOracleConformance','engine-oracle'),
        ('ui-opcodes.smali','ui-opcodes.dex','UiOracleConformance','ui-oracle')]:
        build.java('com.android.tools.smali.smali.Main','a','--api','23','-o',build.WORK/output,build.ROOT/'tests/fixtures'/fixture,log=logbase+'-assemble.log')
        build.run(['java','-Xmx500m','-cp',cp,mainclass,build.ROOT],logbase+'-run.log')
    # These fixtures take explicit DEX/report paths, not the app root used above.
    # The constructor reflection adapter remains host-only; ART proof is separate.
    for fixture, output, mainclass, stem, expected_cases in [
        ('constructor-owner-opcodes.smali','constructor-owner-opcodes.dex','ConstructorOracleConformance','constructor-oracle',16),
        ('widget-bitwise-opcodes.smali','widget-bitwise-opcodes.dex','WidgetOracleOpcodeConformance','widget-bitwise-oracle',4546)]:
        fixture_path=build.ROOT/'tests/fixtures'/fixture
        dex_path=build.WORK/output
        report_path=build.REPORTS/(stem+'-conformance.json')
        report_path.unlink(missing_ok=True)
        build.java('com.android.tools.smali.smali.Main','a','--api','23','-o',dex_path,fixture_path,log=stem+'-assemble.log')
        build.run(['java','-Xmx500m','-cp',cp,mainclass,dex_path,report_path],stem+'-run.log')
        conformance=json.loads(report_path.read_text())
        if conformance.get('passed') is not True or type(conformance.get('cases')) is not int or conformance['cases']!=expected_cases or conformance.get('androidRuntime') is not False:
            raise RuntimeError('Incomplete explicit host conformance: '+stem)
        conformance.update(fixtureSourceSha256=hashlib.sha256(fixture_path.read_bytes()).hexdigest(),fixtureDexSha256=hashlib.sha256(dex_path.read_bytes()).hexdigest())
        report_path.write_text(json.dumps(conformance,indent=2)+'\n')
    apk=None
    if args.three_way:
        apk=build.ROOT/'dist/MacroDroid-5.67.8-v9-hybrid.apk'
        if not apk.is_file():raise RuntimeError('Build the hybrid APK before a three-way test.')
        with zipfile.ZipFile(apk) as z:
            for part in json.loads((build.ROOT/'source/partitions.json').read_text()):
                p=build.WORK/'hybrid'/(part['name']+'.dex')
                if not p.is_file() or p.read_bytes()!=z.read(part['apk_path']):raise RuntimeError('APK/build DEX mismatch: '+part['name'])
    agent=build.WORK/'test-clock-agent.jar'
    with zipfile.ZipFile(agent,'w',compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('META-INF/MANIFEST.MF','Manifest-Version: 1.0\nPremain-Class: TestClockAgent\n\n')
        for p in sorted(build.TOOLS.glob('TestClockAgent*.class')):z.write(p,p.name)
    suffix='three' if args.three_way else 'two'
    fixture_hash=hashlib.sha256((build.ROOT/'tests/fixtures/original-methods.dex').read_bytes()).hexdigest()
    apk_hash=hashlib.sha256(apk.read_bytes()).hexdigest() if apk else None
    reports={}
    for key,mainclass,stem in [
        ('legacy','ParityTests','java'),('core','CoreParityTests','java-core'),
        ('environment','EnvironmentParityTests','java-environment'),('engine','EngineParityTests','java-engine'),
        ('ui','UiParityTests','java-ui')]:
        reportpath=build.REPORTS/(stem+'-'+suffix+'-path-parity.json')
        # Never accept a previously saved result if the executable fails to emit a new report.
        reportpath.unlink(missing_ok=True)
        argv=['java','-Xmx1200m']
        if key in ('environment','engine'):argv+=['-javaagent:'+str(agent)]
        argv+=['-cp',cp,mainclass,str(build.ROOT)]
        if key=='engine':
            argv += [str(reportpath),'all']
            if not args.three_way:argv+=['--two-way']
        elif args.three_way:argv+=[str(build.WORK/'hybrid')]
        build.run(argv,stem+'-differential-tests.log')
        r=json.loads(reportpath.read_text())
        r.update(fixture_sha256=fixture_hash,rebuilt_apk_sha256=apk_hash,rebuilt_dex_compared_to_apk=bool(apk))
        reportpath.write_text(json.dumps(r,indent=2)+'\n');reports[key]=r
    registry=json.loads((build.ROOT/'source/java-method-map.json').read_text())
    registered=len(registry)
    validate_method_partition(reports,registry)
    result=aggregate_reports(reports,registered,3 if args.three_way else 2)
    result.update(exactMethodKeyPartitionVerified=True,apkSha256=apk_hash,rebuiltDexComparedToApk=bool(apk),fixtureSha256=fixture_hash)
    (build.REPORTS/'java-all-path-parity.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    if not result['passed']:raise RuntimeError('Incomplete or failed aggregate coverage')

if __name__=='__main__':
    try:main()
    except Exception as exc:print('TEST FAILURE:',exc,file=sys.stderr);sys.exit(1)
