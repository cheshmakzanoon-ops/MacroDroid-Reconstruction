#!/usr/bin/env python3
"""Build and verify the complete configured offline reconstruction checks.
This runner records actual subprocess exit codes and fresh report hashes. It never
installs an APK and never equates host acceptance with whole-app Android parity.
"""
from __future__ import annotations
import argparse,hashlib,json,os,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
import release_integrity
ROOT=Path(__file__).resolve().parent

def digest(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-edit-probe',action='store_true',help='Skip the isolated full-APK source-edit experiment; explicitly recorded as skipped.')
    args=parser.parse_args()
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    folder=ROOT/'reports'/('acceptance-'+stamp);folder.mkdir(parents=True)
    before=release_integrity.snapshot()
    result={'started_utc':datetime.now(timezone.utc).isoformat(),'input_snapshot_before':before['snapshot_sha256'],
            'input_files':before['files'],'commands':[],'host_acceptance_passed':False,'android_runtime_executed':False,
            'full_runtime_1_to_1_established':False,'complete_high_level_java_kotlin_source':False,
            'source_edit_probe_skipped':args.skip_edit_probe}
    commands=[
        ('input-integrity',['release_integrity.py','verify']),
        ('baseline-build',['build.py','build','--variant','baseline']),
        ('hybrid-build',['build.py','build','--variant','hybrid']),
        ('baseline-code',['build.py','verify','--variant','baseline']),
        ('hybrid-code',['build.py','verify','--variant','hybrid']),
        ('baseline-resources',['resource_verify.py','--variant','baseline']),
        ('hybrid-resources',['resource_verify.py','--variant','hybrid']),
        ('positive-host-tests',['test.py','--three-way']),
        ('reference-status',['reference_status.py']),
        ('engine-negative-controls',['engine_negative_control.py']),
        ('ui-negative-controls',['ui_negative_control.py']),
        ('core-negative-controls',['core_negative_control.py']),
        ('environment-negative-controls',['environment_negative_control.py']),
        ('legacy-negative-control',['negative_control.py']),
    ]
    if not args.skip_edit_probe:commands.append(('signed-source-edit',['full_apk_edit_probe.py']))
    commands.append(('final-positive-host-tests',['test.py','--three-way']))
    env=os.environ.copy();env['PYTHONUTF8']='1'
    def save():
        (folder/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        (ROOT/'reports/acceptance-latest.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    save()
    for number,(label,arguments) in enumerate(commands,1):
        logfile=folder/(f'{number:02d}-'+label+'.log');command=[sys.executable,*arguments]
        print(f'[{number}/{len(commands)}] {label}',flush=True);started=time.monotonic()
        timeout_seconds=5400 if label=='ui-negative-controls' else 1200
        entry={'label':label,'command':command,'log':logfile.relative_to(ROOT).as_posix(),'timeout_seconds':timeout_seconds}
        try:
            with logfile.open('w',encoding='utf-8') as stream:
                process=subprocess.run(command,cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=timeout_seconds)
            entry.update(exit_code=process.returncode,passed=process.returncode==0)
        except (OSError,subprocess.TimeoutExpired) as exc:entry.update(exit_code=None,passed=False,error=str(exc))
        entry['seconds']=round(time.monotonic()-started,3);entry['log_sha256']=digest(logfile)
        result['commands'].append(entry);save()
        if not entry['passed']:
            result['failure']=label;result['remaining_not_executed']=[x[0] for x in commands[number:]];save();return 2
    after=release_integrity.snapshot();result['input_snapshot_after']=after['snapshot_sha256']
    result['build_inputs_unchanged']=before==after
    if before!=after:result['failure']='Build/test inputs changed during acceptance';save();return 2
    # This only records availability; a missing device is not a successful Android test.
    probe=subprocess.run([sys.executable,'android_acceptance.py','--probe-only'],cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
    (folder/'android-probe.log').write_text(probe.stdout+'\n'+probe.stderr,encoding='utf-8')
    result['android_probe_exit_code']=probe.returncode
    result['android_status']=json.loads((ROOT/'reports/android-runtime/result.json').read_text(encoding='utf-8'))['status']
    result['apks']={}
    for variant in ['baseline','hybrid']:
        p=ROOT/'dist'/('MacroDroid-5.67.8-v9-'+variant+'.apk')
        result['apks'][variant]={'bytes':p.stat().st_size,'sha256':digest(p),'path':p.relative_to(ROOT).as_posix()}
    names=['baseline-roundtrip.json','hybrid-roundtrip.json','baseline-resource-parity.json','hybrid-resource-parity.json',
           'java-all-path-parity.json','java-ui-three-path-parity.json','ui-oracle-semantics.json','ui-negative-controls.json','java-engine-three-path-parity.json','oracle-semantics.json','engine-oracle-semantics.json',
           'engine-negative-controls.json','core-negative-controls.json','environment-negative-controls.json','negative-control.json',
           'migration-static-proof.json','migration-linkage-check.json','reference-failures-status-v9.json',
           'constructor-oracle-conformance.json','widget-bitwise-oracle-conformance.json','ui-runtime-policy.json']
    if not args.skip_edit_probe:names.append('full-apk-edit-probe.json')
    result['fresh_evidence_sha256']={n:digest(ROOT/'reports'/n) for n in names}
    result['finished_utc']=datetime.now(timezone.utc).isoformat();result['host_acceptance_passed']=True;save()
    print(json.dumps({k:v for k,v in result.items() if k not in ['commands','fresh_evidence_sha256']},indent=2))
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as exc:print('ACCEPTANCE ERROR:',exc,file=sys.stderr);sys.exit(2)
