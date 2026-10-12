#!/usr/bin/env python3
"""Prove the differential suite rejects an intentionally incorrect Java reconstruction.
The normal sources and downloadable APKs are NOT modified.
"""
from __future__ import annotations
import hashlib,json,os,shutil,subprocess
from pathlib import Path
import build

def main():
    build.bootstrap();host=build.WORK/'java/hostclasses'
    if not host.exists():build.compile_java()
    cp=os.pathsep.join([str(build.JAR),str(host),str(build.TOOLS)])
    build.run(['javac','-cp',cp,'-d',build.TOOLS,*sorted((build.ROOT/'tests/java').glob('*.java'))],'negative-control-compile-tests.log')
    source=build.ROOT/'source/java/recovered/text/LowerCaseManipulationMethods.java';data=source.read_bytes()
    text=data.decode();assert text.count('.toLowerCase()')==1
    negative=build.WORK/'negative-control';build.remove_generated_directory(negative)
    path=negative/'src/recovered/text/LowerCaseManipulationMethods.java';path.parent.mkdir(parents=True)
    path.write_text(text.replace('.toLowerCase()','.toUpperCase()'));classes=negative/'classes';classes.mkdir()
    build.run(['javac','--release','8','-g:none','-cp',host,'-d',classes,path],'negative-control-javac.log')
    command=['java','-Xmx1200m','-cp',str(classes)+os.pathsep+cp,'ParityTests',str(build.ROOT),str(build.WORK/'hybrid')]
    with (build.REPORTS/'negative-control-run.log').open('w') as f:code=subprocess.run(command,cwd=build.ROOT,stdout=f,stderr=subprocess.STDOUT).returncode
    report=json.loads((build.REPORTS/'java-three-path-parity.json').read_text())
    (build.REPORTS/'negative-control-failures.json').write_text(json.dumps(report,indent=2))
    valid=code==2 and report['failedCases']>0 and not report['passed'] and source.read_bytes()==data
    result={'pass':valid,'mutation':'LowerCaseManipulation.apply: toLowerCase -> toUpperCase','exit_code':code,'failed_vectors':report['failedCases'],'source_and_apk_mutated':False,'source_sha256_unchanged':hashlib.sha256(data).hexdigest()}
    (build.REPORTS/'negative-control.json').write_text(json.dumps(result,indent=2))
    if not valid:raise RuntimeError('Negative control did not fail as expected')
    # Restore the positive report by executing the unmodified sources, not by editing result JSON.
    build.run(['java','-Xmx1200m','-cp',cp,'ParityTests',build.ROOT,build.WORK/'hybrid'],'negative-control-positive-restoration.log')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
