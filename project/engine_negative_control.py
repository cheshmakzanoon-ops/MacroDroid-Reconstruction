#!/usr/bin/env python3
"""Reject deliberate dispatcher/guard defects in disposable host classes.
No application source, fixture, original smali, or signed APK is modified.
Positive engine comparisons are rerun afterward; this is not Android execution.
"""
from __future__ import annotations
import hashlib,json,os,shutil,subprocess
from pathlib import Path
import build

# Each mutation has an independent, named expected case that must reject it.
CONTROLS = [
    ('pause-must-not-terminate','ActionDispatchMethods','dispatch',
     'milliseconds,force,pause.W());return;',
     'milliseconds,force,pause.W());self.terminateMacro();return;','fixed-pause'),
    ('group-marker-must-dispatch','ActionDispatchMethods','dispatch',
     '!(action instanceof ActionGroupEndAction)&&action instanceof EndParentAction',
     'action instanceof EndParentAction','group-end-boundary-preserves-conditional-stack'),
    ('goto-must-respect-scopes','ActionDispatchMethods','dispatch',
     'if(j$.util.Objects.equals(currentScope,destinationScope))',
     'if(true)','goto-cannot-enter-if'),
    ('strict-sixty-second-boundary','LoopGuardMethods','guards',
     'elapsed>60000000000L','elapsed>=60000000000L','sixty-seconds-not-aborted'),
]

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()

def main()->None:
    host=build.WORK/'java/hostclasses';agent=build.WORK/'test-clock-agent.jar'
    apk=build.ROOT/'dist/MacroDroid-5.67.8-v9-hybrid.apk'
    if not host.is_dir() or not agent.is_file() or not apk.is_file():
        raise RuntimeError('Build the hybrid APK and run test.py --three-way first.')
    pinned={p:sha(p) for p in [apk,build.ROOT/'tests/fixtures/original-methods.dex',*(build.ROOT/'source/java/recovered/engine').glob('*.java')]}
    cp=os.pathsep.join(map(str,[build.JAR,host,build.TOOLS]));results=[]
    for name,cls,selection,old,new,required_case in CONTROLS:
        src=build.ROOT/'source/java/recovered/engine'/(cls+'.java');text=src.read_text()
        if text.count(old)!=1:raise RuntimeError('Mutation anchor is not unique: '+name)
        out=build.WORK/'negative-engine'/name;shutil.rmtree(out,ignore_errors=True)
        java=out/'src/recovered/engine'/(cls+'.java');java.parent.mkdir(parents=True);java.write_text(text.replace(old,new))
        classes=out/'classes';classes.mkdir()
        build.run(['javac','--release','8','-g:none','-cp',host,'-d',classes,java],name+'-negative-javac.log')
        reportpath=out/'result.json'
        command=['java','-Xmx1200m','-javaagent:'+str(agent),'-cp',str(classes)+os.pathsep+cp,
                 'EngineParityTests',str(build.ROOT),str(reportpath),selection]
        with (build.REPORTS/(name+'-negative-run.log')).open('w') as stream:
            code=subprocess.run(command,cwd=build.ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=300).returncode
        report=json.loads(reportpath.read_text())
        observed={x['case'] for x in report['examples']}
        unchanged=all(sha(p)==digest for p,digest in pinned.items())
        accepted=(code==1 and report['pass'] is False and report['failures']>0 and report['unsupportedExecutions']==0 and unchanged)
        # Examples are capped; a separate isolated expectation is not necessarily in the
        # first 20 mismatches. The full case labels are recorded by EngineParityTests.
        labels=set(report.get('failedCaseLabels',observed))
        accepted=accepted and required_case in labels
        record={'mutation':name,'pass':accepted,'failedCases':report['failures'],
                'requiredCase':required_case,'requiredCaseRejected':required_case in labels,
                'unsupportedExecutions':report['unsupportedExecutions'],'exitCode':code,
                'sourceFixtureAndApkUnchanged':unchanged}
        results.append(record)
        (build.REPORTS/(name+'-negative-failures.json')).write_text(json.dumps(report,indent=2)+'\n')
        if not accepted:raise RuntimeError('Negative control not reliably rejected: '+name+' '+json.dumps(record))
    positive=build.REPORTS/'engine-positive-restoration.json'
    build.run(['java','-Xmx1200m','-javaagent:'+str(agent),'-cp',cp,'EngineParityTests',build.ROOT,positive,'all'],'engine-positive-restoration.log')
    good=json.loads(positive.read_text())
    if not good['pass'] or not all(sha(p)==d for p,d in pinned.items()):raise RuntimeError('Correct engine state was not preserved')
    result={'pass':all(r['pass'] for r in results),'controls':results,'positiveRestorationPassed':True,
            'restorationCases':good['cases'],'androidRuntime':False,'sourceFixtureAndApkUnchanged':True}
    (build.REPORTS/'engine-negative-controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
