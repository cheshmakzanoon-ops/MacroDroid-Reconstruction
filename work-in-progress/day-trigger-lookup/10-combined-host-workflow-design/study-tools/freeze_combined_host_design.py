#!/usr/bin/env python3
"""Freeze the source-only combined workflow proposal and every collector attempt."""
from pathlib import Path
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
import shutil
import stat
import tarfile

ROOT=Path(__file__).resolve().parent
DEST=ROOT/'checkpoints/06-combined-host-workflow-design'
TOOLS=Path('/dev/shm/day-numeric-hosted-02/checkpoints/02-hosted-filesystem-tooling-successor')

def identity(path):
    with path.open('rb') as stream: digest=hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'mode':stat.S_IMODE(path.stat().st_mode),'sha256':digest}

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as stream:json.dump(value,stream,indent=2);stream.write('\n')

def copy(source,name):
    target=DEST/name;target.parent.mkdir(parents=True,exist_ok=True)
    assert not target.exists();shutil.copy2(source,target);assert identity(source)==identity(target)

def main():
    DEST.mkdir(parents=True,exist_ok=False)
    result=json.loads((ROOT/'reports/22-combined-host-design-source/result.json').read_text())
    assert result['passed'] is True and result['tests_executed']==0
    reads=json.loads((ROOT/'reports/22-combined-host-design-source/read-input-identities.json').read_text())
    for name,wanted in reads.items():
        actual=identity(Path(name));assert {k:actual[k] for k in wanted}==wanted
    copy(ROOT/'COMBINED_HOST_ACCEPTANCE_DESIGN.md','DESIGN.md')
    copy(ROOT/'collect_combined_host_design.py','study-tools/collect_combined_host_design.py')
    copy(Path(__file__),'study-tools/freeze_combined_host_design.py')
    numeric_cp=json.loads((TOOLS/'checkpoint.json').read_text())
    source=[row for row in numeric_cp['files'] if row['path'].startswith('source/')]
    assert len(source)==9
    proposed=[]
    for row in source:
        name=row['path'].removeprefix('source/')
        candidate=name.replace('tools/day_numeric_acceptance/','tools/day_trigger_acceptance/').replace('test_day_numeric_acceptance.py','test_day_trigger_acceptance.py').replace('day-numeric-wip-acceptance.yml','day-trigger-wip-acceptance.yml')
        actual=identity(TOOLS/row['path']);assert actual['bytes']==row['bytes'] and actual['sha256']==row['sha256']
        copy(TOOLS/row['path'],'parent-tooling-source/'+name)
        proposed.append({'path':candidate,'must_be_absent_before_future_activation':True,
                         'implementation_authored':False,'parent_path':name,'parent_identity':actual})
    save(DEST/'proposed-tooling-paths.json',{'schema':1,'proposed_new_files':proposed,'path_count':9,
         'actual_remote_absence_check_pending':True,'lookup_checkout_commit':None,
         'lookup_commit_note':'Publisher is transporting immutable Lookup08 and Lookup09; bind its verified fixed commit during later implementation. No executable workflow is present in this design.'})
    evidence=[]
    for folder in ['reports/21-combined-host-design-source','reports/22-combined-host-design-source','design-extra']:
        for path in sorted((ROOT/folder).rglob('*')):
            if path.is_file():evidence.append({'path':path.relative_to(ROOT).as_posix(),**identity(path)})
    save(DEST/'evidence-files.json',evidence)
    archive=DEST/'evidence.tar.gz'
    with archive.open('xb') as raw:
        with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0,filename='') as zipped:
            with tarfile.open(fileobj=zipped,mode='w') as tar:
                for row in evidence:
                    data=(ROOT/row['path']).read_bytes();info=tarfile.TarInfo(row['path'])
                    info.size=len(data);info.mode=row['mode'];info.mtime=0;info.uid=0;info.gid=0
                    tar.addfile(info,io.BytesIO(data))
    with tarfile.open(archive,'r:gz') as tar:
        assert tar.getnames()==[row['path'] for row in evidence]
        for member,row in zip(tar.getmembers(),evidence):
            data=tar.extractfile(member).read()
            assert member.mode==row['mode'] and len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
    for row in evidence:
        # Keep every compact source-only result directly reviewable as well.
        copy(ROOT/row['path'],'evidence/'+row['path'])
    scope='''# Frozen combined-workflow design scope

This is a design capsule, not a new application or executable workflow. Its actual source-only collector closed successfully after one preserved failed test-name assumption. The initial interactive manifest-schema inspection error is also retained.

Actual checks: exact source/checkpoint hashes, complete 81,291 → 81,298 → 81,304 manifest derivation, exact 25-path union/13 new inputs, actual 1,249-body/607-class DEX definition inventory, 1,244 registered keys plus five uncredited getters, exact old 91 prepared Java fault prefix and all 101 prepared mutation hashes, and actual source/AST working-directory binding. No full physical application tree was materialized or scanned. No Python test suite, Java, D8, signed APK build, Android command, or acceptance gate was executed in this design study.

The proposed separate nine-file tooling surface starts from frozen numeric tooling 815612f8 and retains two complete physical preparation scans after baseline materialization. Its future expected full-run totals are 195,151 unique cases per positive run, 357 project Python tests, 101 actual Java UI faults, four actual method DEX faults, four provenance rejections and 24 fresh named reports. Those are requirements awaiting actual future execution.

The individual frozen method command rows do not record cwd. The proposal binds cwd through exact producer/caller AST and the outer acceptance receipt; it does not fabricate a field or independent observation. Failed partial recorder rows remain failed. Both Lookup08 and Lookup09 stay unchanged; the publisher must supply their fixed verified commit before future workflow implementation is activated.

Complete design: DESIGN.md. Exact source stages, count derivation, method commands, unchanged prefix, prior method-proof bindings and all actual collector output: evidence/. The exact parent nine tooling sources are copied under parent-tooling-source/ for review, not proposed as already-authored successors. The complete evidence archive is evidence.tar.gz and every member is bound by evidence-files.json.
'''
    (DEST/'CHECKPOINT_SCOPE.md').write_text(scope)
    files=[{'path':p.relative_to(DEST).as_posix(),**identity(p)} for p in sorted(DEST.rglob('*')) if p.is_file()]
    checkpoint={'schema':1,'status':'INACTIVE_COMBINED_HOST_WORKFLOW_DESIGN_REVIEW_READY',
        'created_utc':datetime.now(timezone.utc).isoformat(),'repo_target':'work-in-progress/day-trigger-lookup/10-combined-host-workflow-design',
        'active_source_changed':False,'workflow_authored_or_activated':False,'full_host_acceptance_executed':False,
        'tests_executed':0,'application_executions':0,'full_project_materializations':0,
        'parent_tooling_checkpoint_sha256':'815612f827f1b0d2bcec90bbb1ae8a35a8c76ced8f6b5f44cf413bc40b81f493',
        'numeric_source_checkpoint_sha256':'d9ddd3e0f692c66e2cd47870ff3cf95bfa0a2b1cd50fc2fd55a3c09e66df9bcf',
        'lookup_merge_checkpoint_sha256':'56aa7bfc05286d9fc474d24e6afc33fbd3a664e9dc731f70912df1a9e375b350',
        'lookup_recorder_checkpoint_sha256':'87c2a01a627590b62017eae8145db92d1a7593d5cf127114a9812ec13cd756f5',
        'source_boundary_input_counts':[81291,81298,81304],'final_source_union_paths':25,'new_inputs':13,
        'proposed_tooling_paths':9,'expected_registered_methods':1244,'expected_cases_per_positive_run':195151,
        'expected_project_python_tests':357,'required_java_ui_faults':101,'required_method_dex_faults':4,'required_provenance_rejections':4,
        'required_method_subprocesses':36,'required_method_streams':72,'required_fresh_reports':24,
        'source_only_result':identity(ROOT/'reports/22-combined-host-design-source/result.json'),
        'evidence_archive':identity(archive),'evidence_file_count':len(evidence),'files':files}
    save(DEST/'checkpoint.json',checkpoint)
    assert sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())<=256*1024*1024
    print(json.dumps({'checkpoint':str(DEST/'checkpoint.json'),**identity(DEST/'checkpoint.json'),
        'direct_payload_files':len(files),'evidence_files':len(evidence),'archive':identity(archive),
        'owned_bytes':sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())},indent=2))

if __name__=='__main__':main()
