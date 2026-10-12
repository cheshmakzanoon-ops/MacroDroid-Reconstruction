#!/usr/bin/env python3
"""Deliberately reject three environment-logic defects in temporary host classes.

Never edits original source, DEX or APK files. The test clock affects only the
host-loaded recovered classes. Real Android execution is not part of this check.
"""
from __future__ import annotations
import hashlib,json,os,shutil,subprocess
from pathlib import Path
import build

def sha(path:Path)->str:
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main()->None:
    host=build.WORK/'java/hostclasses';agent=build.WORK/'test-clock-agent.jar'
    apk=build.ROOT/'dist/MacroDroid-5.67.8-v9-hybrid.apk';apk_hash=sha(apk)
    if not agent.is_file():raise RuntimeError('Run test.py --three-way before the negative controls.')
    cp=os.pathsep.join(map(str,[build.JAR,host,build.TOOLS]));results=[]
    variants=[
        ('invalid-integer-default','SystemSettingMethods','long threshold = parsed == null ? 0L : parsed.longValue();','long threshold = parsed == null ? 1L : parsed.longValue();'),
        ('hotspot-api-29-boundary','WifiMethods','Build.VERSION.SDK_INT >= 29','Build.VERSION.SDK_INT > 29'),
        ('sunrise-widened-catch','SolarConstraintMethods','g94 coordinates = new g94(latitude, longitude);','g94 coordinates; try { coordinates = new g94(latitude, longitude); } catch (NumberFormatException invalid) { return false; }')
    ]
    report_file=build.REPORTS/'java-environment-three-path-parity.json'
    for label,cls,old,new in variants:
        source=build.ROOT/'source/java/recovered/environment'/(cls+'.java');raw=source.read_bytes();text=raw.decode()
        if text.count(old)!=1:raise RuntimeError('Mutation anchor must be unique: '+label)
        work=build.WORK/'negative-environment'/label;build.remove_generated_directory(work)
        temporary_source=work/'src/recovered/environment'/(cls+'.java');temporary_source.parent.mkdir(parents=True);temporary_source.write_text(text.replace(old,new))
        classes=work/'classes';classes.mkdir()
        build.run(['javac','--release','8','-g:none','-cp',host,'-d',classes,temporary_source],label+'-negative-javac.log')
        command=['java','-Xmx1200m','-javaagent:'+str(agent),'-cp',str(classes)+os.pathsep+cp,'EnvironmentParityTests',str(build.ROOT),str(build.WORK/'hybrid')]
        report_file.unlink(missing_ok=True)
        with (build.REPORTS/(label+'-negative-run.log')).open('w') as log:
            code=subprocess.run(command,cwd=build.ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=300).returncode
        if not report_file.is_file():raise RuntimeError('Negative control did not produce its own report: '+label)
        result=json.loads(report_file.read_text());(build.REPORTS/(label+'-negative-failures.json')).write_text(json.dumps(result,indent=2))
        passed=(code!=0 and result['failedCases']>0 and not result['passed'] and result['unsupportedExecutions']==0 and result['methodsCovered']==15 and source.read_bytes()==raw and sha(apk)==apk_hash)
        item={'mutation':label,'pass':passed,'failedCases':result['failedCases'],'unsupportedExecutions':result['unsupportedExecutions'],'exitCode':code,'sourceUnchanged':source.read_bytes()==raw,'apkUnchanged':sha(apk)==apk_hash}
        results.append(item);print(json.dumps(item),flush=True)
        if not passed:raise RuntimeError('Mutation was not rejected through valid comparisons: '+label)
    build.run(['java','-Xmx1200m','-javaagent:'+str(agent),'-cp',cp,'EnvironmentParityTests',build.ROOT,build.WORK/'hybrid'],'environment-positive-restoration.log')
    positive=json.loads(report_file.read_text())
    if not positive['passed'] or sha(apk)!=apk_hash:raise RuntimeError('Restored positive suite/APK preservation failed')
    result={'pass':all(x['pass'] for x in results),'controls':results,'positiveRestorationPassed':True,'positiveCases':positive['cases'],'apkSha256':apk_hash,'androidRuntime':False}
    (build.REPORTS/'environment-negative-controls.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
