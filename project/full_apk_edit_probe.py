#!/usr/bin/env python3
"""Prove a Java dispatcher edit reaches a signed APK, then reject its behavior.
All edits/builds happen in an isolated project under build/. No APK is installed.
The intentionally incorrect APK is diagnostic-only and is never a release output.
"""
from __future__ import annotations
import hashlib,json,os,shutil,subprocess,sys,zipfile
from pathlib import Path
import build,release_integrity

TARGET='Lcom/arlosoft/macrodroid/macro/Macro;'
METHOD='invokeActions(Ljava/util/List;ILcom/arlosoft/macrodroid/triggers/TriggerContextInfo;ZLjava/util/Stack;Lcom/arlosoft/macrodroid/data/ResumeMacroInfo;)V'

def sha(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()

def signature_entry(name:str)->bool:
    return name=='META-INF/MANIFEST.MF' or (name.startswith('META-INF/') and '/' not in name[9:] and name.upper().endswith(('.SF','.RSA','.DSA','.EC')))

def canonical_classes(folder:Path)->dict[str,str]:
    result={}
    for p in folder.rglob('*.smali'):
        text=p.read_text();name=next(line.split()[-1] for line in text.splitlines() if line.startswith('.class '))
        if name in result:raise RuntimeError('Duplicate class in comparison: '+name)
        result[name]=text
    return result

def main()->None:
    original_apk=build.ROOT/'dist/MacroDroid-5.67.8-v9-hybrid.apk'
    verified=build.WORK/'verify-hybrid/classes3'
    if not original_apk.is_file() or not verified.is_dir():raise RuntimeError('First build, verify, and test the hybrid APK.')
    inputs_before=release_integrity.snapshot();apk_before=sha(original_apk)
    probe=build.WORK/'signed-edit-probe';shutil.rmtree(probe,ignore_errors=True);probe.mkdir()
    copier=os.link if os.name!='nt' else shutil.copy2
    for name in ['source','test-support','signing','tools']:
        shutil.copytree(build.ROOT/name,probe/name,copy_function=copier,ignore=shutil.ignore_patterns('classes','__pycache__') if name=='tools' else shutil.ignore_patterns('__pycache__'))
    for p in build.ROOT.glob('*.py'):shutil.copy2(p,probe/p.name)
    (probe/'build').mkdir()
    # These are only freshly source-derived outputs, validated again by build.py.
    shutil.copytree(build.WORK/'assembly-cache',probe/'build/assembly-cache',copy_function=copier)
    src=probe/'source/java/recovered/engine/ActionDispatchMethods.java'
    old='milliseconds,force,pause.W());return;'
    text=src.read_text()
    if text.count(old)!=1:raise RuntimeError('Expected one pause-return edit anchor')
    candidate=text.replace(old,'milliseconds,force,pause.W());self.terminateMacro();return;')
    temporary=src.with_suffix('.java.tmp');temporary.write_text(candidate);temporary.replace(src)
    command=[sys.executable,'build.py','build','--variant','hybrid']
    with (build.REPORTS/'full-apk-edit-build.log').open('w') as stream:
        result=subprocess.run(command,cwd=probe,stdout=stream,stderr=subprocess.STDOUT,timeout=900)
    if result.returncode:raise RuntimeError('Edited APK build failed; see full-apk-edit-build.log')
    mutated=probe/'dist/MacroDroid-5.67.8-v9-hybrid.apk'
    with zipfile.ZipFile(original_apk) as a,zipfile.ZipFile(mutated) as b:
        an={n for n in a.namelist() if not signature_entry(n)};bn={n for n in b.namelist() if not signature_entry(n)}
        if an!=bn:raise RuntimeError('Edited APK changed its payload entry set')
        changed=[n for n in sorted(an) if a.read(n)!=b.read(n)]
        if changed!=['classes3.dex']:raise RuntimeError('Unexpected edited APK payload changes: '+repr(changed))
        dex=probe/'build/edited-primary.dex';dex.write_bytes(b.read('classes3.dex'))
    disassembled=probe/'build/edited-smali'
    build.java('com.android.tools.smali.baksmali.Main','d','--api','23','--use-locals','-j','2','-o',disassembled,dex,log='full-apk-edit-disassembly.log')
    before=canonical_classes(verified);after=canonical_classes(disassembled)
    if before.keys()!=after.keys():raise RuntimeError('Edited DEX changed the class inventory')
    classes=[c for c in before if before[c]!=after[c]]
    if classes!=[TARGET]:raise RuntimeError('Unexpected edited classes: '+repr(classes))
    bm=build.methods(before[TARGET]);am=build.methods(after[TARGET])
    if bm.keys()!=am.keys():raise RuntimeError('Edited class changed method declarations')
    methods=[m for m in bm if bm[m]!=am[m]]
    if methods!=[METHOD] or build.METHOD.sub('<METHOD>',before[TARGET])!=build.METHOD.sub('<METHOD>',after[TARGET]):raise RuntimeError('Edit isolation check failed')
    # Test-only original fixture is introduced only AFTER the APK has been built.
    fixtures=probe/'tests/fixtures';fixtures.mkdir(parents=True)
    shutil.copy2(build.ROOT/'tests/fixtures/original-methods.dex',fixtures/'original-methods.dex')
    reportpath=build.REPORTS/'full-apk-edit-negative-comparison.json'
    cp=os.pathsep.join(map(str,[build.JAR,probe/'build/java/hostclasses',build.TOOLS]))
    argv=['java','-Xmx1200m','-javaagent:'+str(build.WORK/'test-clock-agent.jar'),'-cp',cp,'EngineParityTests',str(probe),str(reportpath),'dispatch']
    with (build.REPORTS/'full-apk-edit-negative-run.log').open('w') as stream:
        negative=subprocess.run(argv,stdout=stream,stderr=subprocess.STDOUT,timeout=300)
    evidence=json.loads(reportpath.read_text())
    rejected=(negative.returncode==1 and evidence['pass'] is False and evidence['failures']>0 and evidence['unsupportedExecutions']==0 and 'fixed-pause' in evidence['failedCaseLabels'])
    unchanged=inputs_before==release_integrity.snapshot() and apk_before==sha(original_apk)
    result={'pass':rejected and unchanged,'scope':'Actual Java-source edit -> rebuilt DEX -> signed APK, with isolated class/method change and bounded host rejection, NOT Android execution',
            'application_source_edit':'Intentionally terminate immediately after pause handoff',
            'original_release_apk_sha256':apk_before,'experimental_apk_sha256':sha(mutated),'experimental_apk_not_distributed':True,
            'payload_entries_compared':len(an),'changed_non_signature_entries':changed,'classes_compared_in_changed_partition':len(before),
            'changed_classes':classes,'changed_methods':methods,'negative_exit_code':negative.returncode,
            'negative_failed_cases':evidence['failures'],'unsupported_executions':evidence['unsupportedExecutions'],
            'required_pause_case_rejected':'fixed-pause' in evidence['failedCaseLabels'],'release_inputs_and_apk_unchanged':unchanged,
            'android_runtime_executed':False}
    (build.REPORTS/'full-apk-edit-probe.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
    if not result['pass']:raise RuntimeError('Source-edit proof did not meet its acceptance rules')

if __name__=='__main__':main()
