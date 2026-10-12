#!/usr/bin/env python3
"""Review the exact two-guard successor against its preserved source and results."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import re
import stat
import tarfile
import traceback

ROOT=Path('/dev/shm/macrodroid-day-numeric-art-schema-root-review')
OUT=ROOT/'review-01'
NEW=Path('/dev/shm/macrodroid-day-numeric-art-schema-02/checkpoints/01-literal-schema-successor-and-review')
OLD=Path('/dev/shm/macrodroid-day-numeric-art/wrapper-draft-01')
CAPS=[('successor',NEW,10758,'4d2bc4d8c9c5350b9572d5fa0b384438faf0a7b550156486da1e6701cc5eee1a',40),
      ('old-wrapper',OLD,4276,'6ca4711b330c64f72c0df716e4a8c407360297a9bbc09e634bd88feb295a6dd6',20)]

def need(x,message):
    if not x: raise ValueError(message)

def digest(raw): return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def read(p): return json.loads(p.read_bytes())
def write(name,obj):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:f.write(json.dumps(obj,indent=2)+'\n')
def copy(p,name):
    q=OUT/name;q.parent.mkdir(parents=True,exist_ok=True)
    with q.open('xb') as f:f.write(p.read_bytes())
def identity(p):
    info=p.lstat();need(stat.S_ISREG(info.st_mode) and p.resolve()==p,'Confined regular payload: '+str(p))
    return dict(**digest(p.read_bytes()),mode=stat.S_IMODE(info.st_mode))
def capsules():
    checks=[]
    for label,base,n,sha,count in CAPS:
        need(digest((base/'checkpoint.json').read_bytes())==dict(bytes=n,sha256=sha),'Checkpoint '+label)
        rows=read(base/'checkpoint.json')['files']
        need(len(rows)==len({r['path'] for r in rows})==count,'Membership count '+label)
        need({p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file() or p.is_symlink()}==
             {r['path'] for r in rows}|{'checkpoint.json'},'Exact capsule membership '+label)
        for r in rows:
            actual=identity(base/r['path']); mode=int(r['mode'],8)&0o7777 if isinstance(r['mode'],str) else r['mode']
            need(actual==dict(bytes=r['bytes'],sha256=r['sha256'],mode=mode),'Exact payload '+label+': '+r['path'])
            checks.append(dict(capsule=label,path=r['path'],**actual))
    return checks

def main():
    OUT.mkdir(parents=True,exist_ok=False);copy(Path(__file__),'executed-reviewer.py')
    result=dict(status='REVIEWING_LITERAL_NUMERIC_SCHEMA_DELTA',passed=False,
                started_utc=datetime.now(timezone.utc).isoformat(),android_executed=False,
                application_build_executed=False,host_suite_reexecuted=False,production_wrapper_imported=False,
                full_runtime_1_to_1_established=False,workflow_activated=False)
    rc=2
    try:
        before=capsules();write('reviewed-payloads-before.json',before)
        for label,base,*_ in CAPS:copy(base/'checkpoint.json','inputs/'+label+'-checkpoint.json')
        cp=read(NEW/'checkpoint.json')
        old=(OLD/'source/android_day_numeric_method_probe.py').read_text()
        new=(NEW/'source/android_day_numeric_method_probe.py').read_text()
        replacements=[("if (not isinstance(info, dict) or info.get('schema_version') != 2 or",
                       "if (not isinstance(info, dict) or type(info.get('schema_version')) is not int or\n            info.get('schema_version') != 2 or"),
                      ("if (report.get('schema_version') != 2 or report.get('scope') != PROBE_SCOPE or",
                       "if (type(report.get('schema_version')) is not int or\n                report.get('schema_version') != 2 or report.get('scope') != PROBE_SCOPE or")]
        expected=old
        for a,b in replacements:
            need(expected.count(a)==1,'Unique old schema expression');expected=expected.replace(a,b,1)
        need(new==expected,'Successor differs by exactly the two schema type guards')
        old_test=ast.parse((OLD/'source/test_android_day_numeric_method_probe.py').read_bytes())
        new_test=ast.parse((NEW/'source/test_android_day_numeric_method_probe.py').read_bytes())
        name='test_literal_integer_schema_is_required_for_provenance_and_result_replay'
        old_tests={n.name:ast.dump(n,include_attributes=False) for n in ast.walk(old_test) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')}
        new_tests={n.name:ast.dump(n,include_attributes=False) for n in ast.walk(new_test) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')}
        need(len(old_tests)==41 and len(new_tests)==42 and set(new_tests)-set(old_tests)=={name},'Exact 41+1 named control union')
        need(all(new_tests[k]==v for k,v in old_tests.items()),'All prior 41 control bodies unchanged')
        removed=0
        for node in ast.walk(new_test):
            if isinstance(node,ast.ClassDef):
                before_count=len(node.body);node.body=[n for n in node.body if not isinstance(n,ast.FunctionDef) or n.name!=name]
                removed+=before_count-len(node.body)
        need(removed==1 and ast.dump(old_test,include_attributes=False)==ast.dump(new_test,include_attributes=False),
             'Entire test module otherwise unchanged')
        changes=[]
        for row in cp['source_files']:
            relative=row['path']; a=identity(OLD/relative); b=identity(NEW/relative)
            need(b=={k:row[k] for k in ('bytes','sha256','mode')},'Complete successor source binding')
            if a!=b:changes.append(relative)
        need(changes==['source/android_day_numeric_method_probe.py','source/test_android_day_numeric_method_probe.py'], 'Only wrapper and test source roles changed')
        archive=NEW/'evidence.tar.gz';need(identity(archive)==cp['evidence_archive'],'Exact complete evidence archive')
        inventory=read(NEW/'evidence-inventory.json');need(len(inventory)==151,'Archive inventory count')
        names=[];total=0
        with tarfile.open(archive,'r|gz') as tf:
            for member in tf:
                need(member.isfile(),'Only regular archived evidence')
                row=inventory[len(names)];need(member.name==row['path'] and member.mode==row['mode'],'Exact archive order and mode')
                raw=tf.extractfile(member).read();need(digest(raw)=={k:row[k] for k in ('bytes','sha256')},'Exact archived evidence '+member.name)
                names.append(member.name);total+=len(raw)
        need(len(names)==151 and total==7268932,'Complete archive membership and bytes')
        old_obs=read(NEW/'reports/counterexample-01/observations.json')
        need(old_obs['counterexample_reproduced'] is True and old_obs['literal_integer_schema_contract_passed'] is False,'Old literal schema failure preserved')
        for row in old_obs['observations']:
            expected_pass=row['label'] in ('integer-two','float-two')
            need(row['provenance']['accepted'] is expected_pass and row['report_replay']['accepted'] is expected_pass,'Old actual boundary observations')
        observed=read(NEW/('reports/focused-01/host-evidence/'+name+'/result/schema-observations.json'))
        need(observed['android_executed'] is False and len(observed['observations'])==5,'Five explicit simulated schema subcases')
        for row in observed['observations']:
            expected_pass=row['label']=='integer-two'
            need(row['provenance_accepted'] is expected_pass and row['report_replay_accepted'] is expected_pass,'Successor exact schema observations')
        command=read(NEW/'reports/focused-01/command.json')
        need(command['returncode']==0 and command['timed_out'] is False and command['timeout_seconds']==120,'Bounded focused actual command')
        for stream in ('stdout','stderr'):
            raw=(NEW/'reports/focused-01'/(stream+'.txt')).read_bytes()
            need(digest(raw)=={k:command[stream][k] for k in ('bytes','sha256')},'Exact focused raw stream')
        raw=(NEW/'reports/focused-01/stderr.txt').read_text()
        need(name in raw and re.search(r'\nRan 1 test in [0-9.]+s\n\nOK\n\s*$',raw),'One literal focused control passed')
        need((NEW/'reports/focused-01/inputs-before.json').read_bytes()==(NEW/'reports/focused-01/inputs-after.json').read_bytes(),'Successor source unchanged during focused control')
        review=read(NEW/'reports/closed-review-01/result.json')
        need(review['passed'] is True and review['all_reviewed_inputs_unchanged'] is True and review['old_41_suite_rerun'] is False,'Closed independent source/archive review')
        need(len(review['literal_closed_positive_reviews'])==3,'Three separately bound already closed simulated positives')
        for source in ['source-successor.patch','ast-derivation.json','source-bindings.json',
                       'reports/focused-01/command.json','reports/focused-01/stdout.txt','reports/focused-01/stderr.txt',
                       'reports/counterexample-01/observations.json','reports/closed-review-01/result.json']:
            copy(NEW/source,'retained/'+source)
        write('source-delta-review.json',dict(wrapper_guard_changes=2,unchanged_other_source_roles=7,
              unchanged_prior_test_bodies=41,new_test_name=name,final_test_count=42,
              old_float_acceptance_preserved=True,successor_focus_count=1,complete_final_suite_locally_run=False,
              actual_closed_archive_files=151,actual_closed_archive_bytes=total,source_files=cp['source_files']))
        after=capsules();need(before==after,'Reviewed capsules unchanged after root review');write('reviewed-payloads-after.json',after)
        result.update(status='CLOSED_ROOT_LITERAL_NUMERIC_SCHEMA_DELTA_REVIEW',passed=True,reviewed_payloads=60,
                      archive_files=151,source_delta_approved=True,
                      approval_scope='Exact final nine-role successor is cleared for inclusion in the separately reviewed numeric ART workflow. No activation is cleared until its workflow/input/cleanup review and fetched publication close.',
                      full_host_suite_required_in_ci=42,actual_android_numeric_cases_still_pending=1291)
        rc=0
    except Exception as e:
        result.update(status='ROOT_NUMERIC_SCHEMA_DELTA_REVIEW_FAILED',reason=type(e).__name__+': '+str(e),traceback=traceback.format_exc())
    result['finished_utc']=datetime.now(timezone.utc).isoformat();write('result.json',result)
    with (OUT/'README.md').open('x') as f:
        f.write('# Root review: numeric ART wrapper schema correction\n\nThe executed root audit and literal result are retained here. It independently checks the complete old and successor payloads, the exact two schema guards, the unchanged 41 prior test bodies and seven other source roles, all 151 archived evidence files, and the actual old counterexample and new focused success. It performs no compilation, test rerun, wrapper import, Android execution or application modification.\n\nA passing result clears only the exact nine-role successor for the pending workflow review. The complete final 42-test suite and both 1,291-case Android executions remain required in CI. The original float-accepting schema failure stays preserved and is not reclassified as parity evidence.\n')
    rows=[]
    for p in sorted(OUT.rglob('*')):
        if p.is_file():
            d=identity(p);rows.append(dict(path=p.relative_to(OUT).as_posix(),bytes=d['bytes'],sha256=d['sha256'],mode='100755' if d['mode']&0o111 else '100644'))
    write('checkpoint.json',dict(schema=1,status=result['status'],passed=result['passed'],
          repo_target='docs/verification/day-numeric-art/root-schema-successor-review',active_files=[],
          android_executed=False,application_build_executed=False,full_runtime_1_to_1_established=False,
          files=rows,frozen_payload_count=len(rows),frozen_payload_bytes=sum(r['bytes'] for r in rows)))
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),status=result['status'],**digest((OUT/'checkpoint.json').read_bytes()))))
    return rc
if __name__=='__main__':raise SystemExit(main())
