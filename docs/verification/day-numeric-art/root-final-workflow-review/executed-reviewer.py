#!/usr/bin/env python3
"""Final read-only review of the corrected fixed numeric ART workflow."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import gzip
import hashlib
import json
import re
import shlex
import stat
import subprocess
import traceback
import yaml

ROOT=Path('/dev/shm/macrodroid-day-numeric-workflow-root-review')
OUT=ROOT/'review-01'
BASE=Path('/dev/shm/day-numeric-art-workflow-01')
A=BASE/'checkpoints/01-offline-validated-runtime-path-blocker'
B=BASE/'checkpoints/02-corrected-queued-wrapper-path'
S=Path('/dev/shm/macrodroid-day-numeric-art-schema-02/checkpoints/01-literal-schema-successor-and-review')
PARENT=BASE/'inputs/parent'
COMMIT='fc825ede39a40249e33c8ba75b93128a98bd5e3c'
GIT='/dev/shm/macrodroid-transfer-space-20261012/verification.git'
CAPS=[('blocked-workflow',A,32019,'3945eb046eaf5019099349383c3557ca752e27866b27dc80a9272af2ab2bf6ab',141),
      ('corrected-workflow',B,7711,'a0e28dda5ae269727cbe1f9d3f5f1cd9ad019b8b2b5b9272f443eb900380f1ef',34),
      ('schema-successor',S,10758,'4d2bc4d8c9c5350b9572d5fa0b384438faf0a7b550156486da1e6701cc5eee1a',40)]

def need(value,message):
    if not value:raise ValueError(message)
def digest(raw):return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def read(p):return json.loads(p.read_bytes())
def write(name,value):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:f.write(json.dumps(value,indent=2)+'\n')
def copy(p,name):
    q=OUT/name;q.parent.mkdir(parents=True,exist_ok=True)
    with q.open('xb') as f:f.write(p.read_bytes())
def identity(p,git=False,combined=None):
    before=p.lstat();need(stat.S_ISREG(before.st_mode) and p.resolve()==p,'Confined regular input '+str(p))
    h=hashlib.sha256();g=hashlib.sha1(b'blob '+str(before.st_size).encode()+b'\0') if git else None;n=0
    with p.open('rb') as f:
        while chunk:=f.read(1024*1024):
            h.update(chunk);n+=len(chunk)
            if g is not None:g.update(chunk)
            if combined is not None:combined.update(chunk)
    after=p.lstat()
    fields=lambda x:(x.st_dev,x.st_ino,x.st_size,x.st_mode,x.st_mtime_ns,x.st_ctime_ns)
    need(fields(before)==fields(after) and n==after.st_size,'Input changed while read '+str(p))
    result=dict(bytes=n,sha256=h.hexdigest(),mode='100755' if after.st_mode&0o111 else '100644')
    if g is not None:result['git_blob_sha1']=g.hexdigest()
    return result
def capsules():
    all_rows=[]
    for label,p,size,sha,count in CAPS:
        need(digest((p/'checkpoint.json').read_bytes())==dict(bytes=size,sha256=sha),'Checkpoint '+label)
        rows=read(p/'checkpoint.json')['files'];need(len(rows)==len({r['path'] for r in rows})==count,'Unique payload count')
        need({q.relative_to(p).as_posix() for q in p.rglob('*') if q.is_file() or q.is_symlink()}==
             {r['path'] for r in rows}|{'checkpoint.json'},'Exact capsule membership '+label)
        for row in rows:
            actual=identity(p/row['path']);expected={k:row[k] for k in ('bytes','sha256','mode')}
            if type(expected['mode']) is int:expected['mode']='100755' if expected['mode']&0o111 else '100644'
            need(actual==expected,'Exact payload '+label+': '+row['path']);all_rows.append(dict(capsule=label,path=row['path'],**actual))
    return all_rows

def main():
    OUT.mkdir(parents=True,exist_ok=False);copy(Path(__file__),'executed-reviewer.py')
    result=dict(status='REVIEWING_CORRECTED_NUMERIC_ART_WORKFLOW',passed=False,started_utc=datetime.now(timezone.utc).isoformat(),
        android_executed=False,application_build_executed=False,host_suites_reexecuted=False,
        production_preflight_or_probe_executed=False,full_runtime_1_to_1_established=False)
    rc=2
    try:
        before=capsules();write('capsule-payloads-before.json',before)
        for label,p,*_ in CAPS:copy(p/'checkpoint.json','inputs/'+label+'-checkpoint.json')
        mapping=read(B/'proposed-active-files.json');need(len(mapping)==12,'Exactly twelve proposed active paths')
        changes=[]
        for row in mapping:
            observed=identity(B/row['source']);need(observed=={k:row[k] for k in ('bytes','sha256','mode')},'Mapped source identity')
            if observed!=identity(A/row['source']):changes.append(row['path'])
        workflow='.github/workflows/day-numeric-method-probe.yml'
        need(changes==[workflow],'Only queued workflow path changes')
        old=(A/'source'/workflow).read_text();new=(B/'source'/workflow).read_text()
        wrong='$GITHUB_WORKSPACE/tools/day_numeric_art/android_numeric_method_probe.py'
        right='$GITHUB_WORKSPACE/tools/day_numeric_art/android_day_numeric_method_probe.py'
        need(old.count(wrong)==1 and new==old.replace(wrong,right,1),'Exact one-token workflow correction')
        need(digest(new.encode())==dict(bytes=14360,sha256='f5f37bab137d67bb9499f6e44749139213108814ff88636c864065ce45b23368'),'Final workflow identity')
        manifest=read(B/'source/tools/day_numeric_art/runtime-files.json')
        need(manifest['parent_commit']==COMMIT and manifest['expected_host_controls']==42
             and len(manifest['source_roles'])==9 and len(manifest['parent_roles'])==34,'Fixed complete role manifest')
        for row in manifest['source_roles']:
            need(identity(B/'source'/row['path'])==identity(S/row['source_checkpoint_path']), 'Nine reviewed schema source roles unchanged')
        doc=yaml.load(new,Loader=yaml.BaseLoader);job=doc['jobs']['day-numeric-method-probe'];steps=job['steps']
        need(job['timeout-minutes']=='60' and doc['permissions']=={'contents':'read'},'Fixed job bound and permissions')
        need([s['with']['ref'] for s in steps if s.get('with',{}).get('ref')]==[COMMIT],'Single immutable parent checkout')
        runtime=[s['run'] for s in steps if s['name']=='Run the neutral probe once per exact APK with verification enabled'][0]
        marker='python3 parent-inputs/tools/android/runtime_job.py '
        command=marker+runtime.split(marker,1)[1].split('2>&1 | tee ci-day-numeric-art/runtime-job.log',1)[0]
        queued=shlex.split(command.replace('\\\n',' '));child=queued[queued.index('--')+1:]
        expected=['python3',right,'--adb','$RUNNER_TEMP/macrodroid-numeric-art-tooling/android/platform-tools/adb',
            '--serial','emulator-5560','--avd','MacroDroid_API35_Disposable','--original',
            '$GITHUB_WORKSPACE/parent-inputs/workspace/artifacts/MacroDroid-5.67.8-original.apk','--candidate',
            '$GITHUB_WORKSPACE/parent-inputs/workspace/artifacts/MacroDroid-5.67.8-day-numeric-0762aad9.apk',
            '--probe','$GITHUB_WORKSPACE/tools/day_numeric_art/probes/day-numeric-method-probe.dex','--provenance',
            '$GITHUB_WORKSPACE/tools/day_numeric_art/probes/day-numeric-method-probe.json','--output',
            '$GITHUB_WORKSPACE/ci-day-numeric-art/probe','--timeout','120']
        need(child==expected and queued[queued.index('--timeout')+1]=='720','Exact queued executable, arguments and bound')
        need('--timeout 900' in runtime and 'timeout 60s tail --pid="$numeric_service_pid"' in runtime
             and 'touch ci-day-numeric-art/environment/queue/STOP' in runtime,'Bounded owned lifecycle')
        need(steps[-2]['if']=='always()' and steps[-1]['if']=='always()'
             and steps[-1]['with']['include-hidden-files']=='true','Always preserve final verification and complete evidence')
        for name,sha in [('preflight.py','61ac7a308128661eda663d1c36ee47baba238c2aa8ded9e0545fe5939e3cffd5'),
                         ('runtime-files.json','e3e6b34e6a531c1fe1ba2d82aef1a25fbb5fbd4535028564d8e7af6c3b8b0be3')]:
            need(new.count("'tools/day_numeric_art/"+name+"': '"+sha+"'")==3,'Repeated exact preflight-entry pin')
        blocked=read(A/'closed-result.json');need(blocked['offline_checks_passed'] is True and blocked['activation_blocked'] is True,
             'Historical offline pass and later activation blocker both preserved')
        index_meta=read(A/'complete-evidence-index.metadata.json');compressed=(A/'complete-evidence-index.json.gz').read_bytes();raw=gzip.decompress(compressed)
        need(digest(compressed)=={k:index_meta['compressed'][k] for k in ('bytes','sha256')} and digest(raw)==index_meta['decompressed'],'Exact complete evidence index')
        idx=read_json_index=json.loads(raw);rows=idx['files'];indexed={r['path']:r for r in rows}
        need(len(rows)==len(indexed)==945,'Exact index membership');regular=[r for r in rows if r['type']=='regular']
        need(len(regular)==944 and sum(r['bytes'] for r in regular)==4569557369,'Complete regular evidence count and bytes')
        def local_bytes(name):
            row=indexed[name];ref=row['reference'];need(ref['kind']=='local','Expected retained small raw evidence '+name)
            return (A/ref['path']).read_bytes()
        actual=json.loads(local_bytes('reports/validation-01/result.json'))
        faults=['missing-source','changed-source','extra-source','changed-runtime-manifest','missing-runtime','changed-runtime',
                'missing-original-part','substituted-original-part','truncated-candidate-part','symlink-original-part',
                'wrong-candidate-apk','existing-output','missing-runtime-result','simulated-runtime-result']
        expected_commands=[('bash-syntax-%02d'%i,0) for i in range(1,8)]
        expected_commands += [(x,0) for x in ['preflight-help','probe-help','literal-complete-inputs','actual-original-and-candidate-preflight','verify-parts-original','verify-parts-candidate']]
        expected_commands += [(x,1 if x=='existing-output' else 2) for x in faults]
        expected_commands += [('owned-cleanup-clean',0),('owned-cleanup-failed-probe',7),('owned-cleanup-failed-service',1)]
        need([(r['label'],r['returncode']) for r in actual['commands']]==expected_commands and len(expected_commands)==30,'All thirty literal commands and outcomes')
        bindings=[]
        for row in actual['commands']:
            name='reports/validation-01/commands/'+row['label']+'/'
            need(json.loads(local_bytes(name+'command.json'))==row and row['timed_out'] is False,'Literal bounded command receipt')
            for stream in ('stdout','stderr'):
                need(digest(local_bytes(name+stream+'.txt'))=={k:row[stream][k] for k in ('bytes','sha256')},'Literal raw stream binding')
            bindings.append(row)
        write('actual-thirty-command-bindings.json',bindings)
        protected_before=local_bytes('reports/validation-01/inputs-before.json');protected_after=local_bytes('reports/validation-01/inputs-after.json')
        need(protected_before==protected_after and len(json.loads(protected_before))==48,'48 unchanged protected identities')
        need(actual['passed'] is True and actual['full_42_wrapper_suite_executed'] is False and len(actual['python_snippets_parsed'])==6,'Actual offline scope')
        positive=json.loads(local_bytes('reports/validation-01/observations/literal-complete-inputs/result.json'))
        apk_positive=json.loads(local_bytes('reports/validation-01/observations/actual-original-and-candidate-preflight/result.json'))
        need(positive['passed'] is True and apk_positive['passed'] is True and len(positive['files'])==43 and len(positive['entry_points'])==3,'Complete literal source and actual-APK positives')
        simulated=json.loads(local_bytes('reports/validation-01/observations/simulated-runtime-result/result.json'))
        need(simulated['passed'] is False and simulated['reason']=='ProbeError: A simulated host result is not Android evidence','Actual simulated-result rejection at final boundary')
        focused=B/'evidence/reports/path-control-01';command=read(focused/'command.json');observed=read(focused/'observations.json')
        need(command['returncode']==0 and command['timeout_seconds']==60 and command['timed_out'] is False,'Bounded focused command')
        for stream in ('stdout','stderr'):
            need(digest((focused/(stream+'.txt')).read_bytes())=={k:command[stream][k] for k in ('bytes','sha256')},'Focused raw stream')
        need(re.search(r'\nRan 1 test in [0-9.]+s\n\nOK\n\s*$',(focused/'stderr.txt').read_text()),'One actual focused test passed')
        obs=observed['observations'];need(len(obs)==3 and obs[0]['queued_child_argv']==expected==obs[2]['queued_child_argv'] and obs[1]['rejected'] is True,'Corrected positive, old rejection, restoration')
        need((focused/'inputs-before.json').read_bytes()==(focused/'inputs-after.json').read_bytes()
             and read(focused/'result.json')['unchanged_source_and_frozen_payloads']==166,'166 focused source identities unchanged')
        roles=manifest['parent_roles'];args=['git','--git-dir='+GIT,'ls-tree',COMMIT,'--']+[r['path'] for r in roles]
        proc=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
        write('parent-tree-command.json',dict(argv=args,timeout_seconds=30,returncode=proc.returncode,stdout=digest(proc.stdout),stderr=digest(proc.stderr)))
        with (OUT/'parent-tree.stdout.txt').open('xb') as f:f.write(proc.stdout)
        with (OUT/'parent-tree.stderr.txt').open('xb') as f:f.write(proc.stderr)
        need(proc.returncode==0 and not proc.stderr,'Read-only immutable Git tree access')
        tree={}
        for line in proc.stdout.decode().splitlines():
            metadata,name=line.split('\t',1);mode,kind,oid=metadata.split();need(kind=='blob','Parent tree blob');tree[name]=(mode,oid)
        need(set(tree)=={r['path'] for r in roles},'Exact immutable parent tree membership')
        parent_ids={}
        for row in roles:
            need(tree[row['path']]==(row['mode'],row['git_blob_sha1']),'Pinned immutable Git role identity')
            actual_id=identity(PARENT/row['path'],git=True)
            need(actual_id=={k:row[k] for k in actual_id},'Independently rehashed parent role '+row['path']);parent_ids[row['path']]=actual_id
        logical={}
        for name in ['vendor/original/manifest.json','work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json']:
            value=read(PARENT/name);combined=hashlib.sha256();size=0
            for part in value['parts']:
                actual_id=identity(PARENT/part['path'],git=True,combined=combined)
                need(actual_id==parent_ids[part['path']],'Unchanged ordered multipart role');size+=actual_id['bytes']
            observed=dict(bytes=size,sha256=combined.hexdigest());need(observed==dict(bytes=value['size_bytes'],sha256=value['sha256']),'Independent complete APK part stream')
            logical[name]=observed
        declared={r['path']:{k:r[k] for k in ('bytes','sha256','mode')} for r in read(A/'checkpoint.json')['files']}
        reference_counts={};unique_git=set();unique_multi=set()
        for row in regular:
            ref=row['reference'];kind=ref['kind'];reference_counts[kind]=reference_counts.get(kind,0)+1
            expected_id={k:row[k] for k in ('bytes','sha256','mode')}
            if kind=='local':need(declared.get(ref['path'])==expected_id,'Local frozen index reference')
            elif kind=='git_blob':
                need(ref['commit']==COMMIT and parent_ids[ref['path']]==dict(**expected_id,git_blob_sha1=ref['git_blob_sha1']),'Exact immutable index blob reference');unique_git.add(ref['path'])
            elif kind=='multipart_manifest':
                need(ref['commit']==COMMIT and logical[ref['path']]=={k:row[k] for k in ('bytes','sha256')}
                     and parent_ids[ref['path']]['sha256']==ref['manifest_sha256'] and parent_ids[ref['path']]['bytes']==ref['manifest_bytes'],'Exact indexed logical APK');unique_multi.add(ref['path'])
            else:need(False,'Unknown evidence reference')
        need(reference_counts==dict(local=635,git_blob=285,multipart_manifest=24),'Complete content-reference use counts')
        write('independent-parent-and-index-review.json',dict(parent_commit=COMMIT,parent_roles=parent_ids,logical_apks=logical,
              index=digest(raw),regular_paths=944,inert_links=1,logical_bytes=4569557369,reference_uses=reference_counts,
              unique_git_references=len(unique_git),unique_multipart_references=len(unique_multi),apk_materializations=0))
        for name in ['source/.github/workflows/day-numeric-method-probe.yml','source/tools/day_numeric_art/preflight.py',
                     'source/tools/day_numeric_art/runtime-files.json','evidence/reports/path-correction-01/derivation.patch',
                     'evidence/reports/path-control-01/observations.json','evidence/reports/path-control-01/result.json']:
            copy(B/name,'reviewed/'+name)
        copy(B/'proposed-active-files.json','proposed-active-files.json')
        after=capsules();need(after==before,'All 215 capsule payloads unchanged after review');write('capsule-payloads-after.json',after)
        needed=[c[3] for c in CAPS]+['14bd536aa8af2e8458d8c3b1d45de6c770e55ce4e7f0f5e152a70bc6ed79e0bb',
                '49b84bf68c2bac9e88bdd9a9e28f87ac13259fba705480701ddb1b616e8ff097']
        write('activation-clearance.json',dict(status='ROOT_CLEARED_AFTER_EXACT_FETCHED_PUBLICATION',required_prior_checkpoint_sha256=needed,
            exact_absent_paths_to_add=mapping,required_this_review_to_be_pushed_and_fetched=True,
            all_other_application_apk_workflow_and_history_paths_unchanged=True,one_automatic_run_only=True,
            additional_dispatch_authorized=False,application_promotion_authorized=False,final_host_control_count_required=42))
        result.update(status='CLOSED_ROOT_CORRECTED_NUMERIC_ART_WORKFLOW_REVIEW',passed=True,
            reviewed_capsule_payloads=215,reviewed_source_paths=12,unchanged_schema_roles=9,workflow_only_delta=True,
            historical_offline_commands=30,successor_focused_controls=1,independently_rehashed_parent_roles=34,
            independently_streamed_logical_apks=2,complete_index_paths=945,full_final_host_suite_still_required=42,
            actual_android_case_count_still_pending_per_apk=1291,
            manual_review='Read complete fixed workflow/preflight and queued-role control. Validated exact parent/current separation, source manifest gates, actual APK preflight, single bounded per-APK probe schedule inherited from the reviewed wrapper, real-only final evidence replay, owned service cleanup, and complete partial artifact retention. No remaining activation blocker found.')
        rc=0
    except Exception as e:
        result.update(status='ROOT_NUMERIC_WORKFLOW_REVIEW_FAILED',reason=type(e).__name__+': '+str(e),traceback=traceback.format_exc())
    result['finished_utc']=datetime.now(timezone.utc).isoformat();write('result.json',result)
    with (OUT/'README.md').open('x') as f:
        f.write('# Final root review of the corrected numeric ART workflow\n\nThe executed read-only audit and its literal result are retained here. It checks the exact twelve proposed source paths, one-token correction, nine schema-successor inputs, thirty actual historical offline command outcomes, one focused corrected-path test, and complete publication references. The first workflow remains explicitly activation-blocked in its immutable capsule.\n\nThe root audit independently rehashes all 34 parent roles against the immutable Git tree and streams both twelve-part APK sequences without materializing an APK. It binds all 945 indexed evidence paths, keeps simulated results separate from Android, and changes no source, test, capture or prior verdict. No host suite, compiler, preflight, probe or Android command is reexecuted.\n\nA passing result clears only the twelve listed new workflow/tool paths after every required checkpoint and this review are pushed, fetched and verified. CI still must run all 42 final host controls and both 1,291-case ART executions. The current original/candidate APK identities remain fixed; this review grants no application promotion or whole-runtime parity credit.\n')
    files=[]
    for p in sorted(OUT.rglob('*')):
        if p.is_file():files.append(dict(path=p.relative_to(OUT).as_posix(),**identity(p)))
    write('checkpoint.json',dict(schema=1,status=result['status'],passed=result['passed'],repo_target='docs/verification/day-numeric-art/root-final-workflow-review',
        active_files=[],android_executed=False,application_build_executed=False,full_runtime_1_to_1_established=False,
        frozen_payload_count=len(files),frozen_payload_bytes=sum(r['bytes'] for r in files),files=files))
    print(json.dumps(dict(status=result['status'],checkpoint=str(OUT/'checkpoint.json'),**digest((OUT/'checkpoint.json').read_bytes()))))
    return rc
if __name__=='__main__':raise SystemExit(main())
