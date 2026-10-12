#!/usr/bin/env python3
"""Reject incorrect macro/sensor reconstructions without changing source or APKs."""
from __future__ import annotations
import hashlib,json,os,shutil,subprocess
from pathlib import Path
import build

def main():
    host=build.WORK/'java/hostclasses'
    if not host.exists():raise RuntimeError('Build the hybrid APK and run tests first.')
    apk=build.ROOT/'dist/MacroDroid-5.67.8-v9-hybrid.apk'
    apk_hash=hashlib.sha256(apk.read_bytes()).hexdigest()
    cp=os.pathsep.join(map(str,[build.JAR,host,build.TOOLS]))
    variants=[('macro-all-disabled','MacroInvocationMethods','return enabled == 0 || passed;','return enabled != 0 && passed;'),
              ('light-equality','LightLevelMethods','LightLevelConstraint.s_lightLevel < threshold','LightLevelConstraint.s_lightLevel <= threshold')]
    results=[]
    for label,cls,old,new in variants:
        source=build.ROOT/('source/java/recovered/core/'+cls+'.java');raw=source.read_bytes();text=raw.decode()
        if text.count(old)!=1:raise RuntimeError('Mutation anchor is not unique: '+label)
        work=build.WORK/'negative-core'/label;shutil.rmtree(work,ignore_errors=True)
        java=work/'src/recovered/core'/(cls+'.java');java.parent.mkdir(parents=True);java.write_text(text.replace(old,new));classes=work/'classes';classes.mkdir()
        build.run(['javac','--release','8','-g:none','-cp',host,'-d',classes,java],label+'-negative-javac.log')
        command=['java','-Xmx1200m','-cp',str(classes)+os.pathsep+cp,'CoreParityTests',str(build.ROOT),str(build.WORK/'hybrid')]
        with (build.REPORTS/(label+'-negative-run.log')).open('w') as f:
            code=subprocess.run(command,cwd=build.ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=300).returncode
        report=json.loads((build.REPORTS/'java-core-three-path-parity.json').read_text())
        (build.REPORTS/(label+'-negative-failures.json')).write_text(json.dumps(report,indent=2))
        valid=(code==2 and report['failedCases']>0 and not report['passed'] and report['unsupportedExecutions']==0
               and source.read_bytes()==raw and hashlib.sha256(apk.read_bytes()).hexdigest()==apk_hash)
        results.append({'mutation':label,'pass':valid,'failedCases':report['failedCases'],'unsupportedExecutions':report['unsupportedExecutions'],
                        'exitCode':code,'sourceUnchanged':source.read_bytes()==raw,'apkUnchanged':hashlib.sha256(apk.read_bytes()).hexdigest()==apk_hash})
        if not valid:raise RuntimeError('Negative control not rejected properly: '+label)
    build.run(['java','-Xmx1200m','-cp',cp,'CoreParityTests',build.ROOT,build.WORK/'hybrid'],'core-positive-restoration.log')
    positive=json.loads((build.REPORTS/'java-core-three-path-parity.json').read_text())
    if not positive['passed']:raise RuntimeError('Restored positive test failed')
    result={'pass':all(r['pass'] for r in results),'controls':results,'positiveRestorationPassed':True,'androidRuntime':False}
    (build.REPORTS/'core-negative-controls.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
