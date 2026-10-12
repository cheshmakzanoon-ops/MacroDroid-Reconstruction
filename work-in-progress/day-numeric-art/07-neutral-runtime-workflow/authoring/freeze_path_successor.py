#!/usr/bin/env python3
"""Freeze only the workflow path successor and its one measured regression control."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import shutil

ROOT=Path('/dev/shm/day-numeric-art-workflow-01')
DEST=ROOT/'checkpoints/02-corrected-queued-wrapper-path'
FIRST=ROOT/'checkpoints/01-offline-validated-runtime-path-blocker'
PARENT_SHA='3945eb046eaf5019099349383c3557ca752e27866b27dc80a9272af2ab2bf6ab'
TARGET='work-in-progress/day-numeric-art/07-neutral-runtime-workflow'


def identity(path):
    raw=path.read_bytes()
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
            'mode':'100755' if path.stat().st_mode&0o111 else '100644'}


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as stream:stream.write(json.dumps(value,indent=2)+'\n')
    path.chmod(0o644)


def copy(path,target):
    before=identity(path)
    target.parent.mkdir(parents=True,exist_ok=True)
    with path.open('rb') as source,target.open('xb') as output:shutil.copyfileobj(source,output)
    target.chmod(0o755 if before['mode']=='100755' else 0o644)
    if identity(path)!=before or identity(target)!=before:raise ValueError('Exact successor copy changed')
    return before


def main():
    if identity(FIRST/'checkpoint.json')['sha256']!=PARENT_SHA:raise ValueError('Closed first attempt changed')
    parent=json.loads((FIRST/'checkpoint.json').read_bytes())
    for row in parent['files']:
        if identity(FIRST/row['path'])!={key:row[key] for key in ('bytes','sha256','mode')}:
            raise ValueError('Preserved first-attempt payload changed')
    delta=json.loads((ROOT/'reports/path-correction-01/source-delta.json').read_bytes())
    if len(delta)!=12 or [row['path'] for row in delta if row['changed']]!=['.github/workflows/day-numeric-method-probe.yml']:
        raise ValueError('Expected one-path workflow successor')
    controls=json.loads((ROOT/'reports/path-control-01/result.json').read_bytes())
    if controls['passed'] is not True or controls['actual_tests_run']!=1 or controls['unchanged_source_and_frozen_payloads']!=166:
        raise ValueError('Focused closed one-test result differs')
    observations=json.loads((ROOT/'reports/path-control-01/observations.json').read_bytes())
    if [row['label'] for row in observations['observations']]!=['corrected-workflow-positive','retained-old-spelling','corrected-workflow-restored']:
        raise ValueError('All positive/negative/restoration observations required')
    DEST.mkdir(parents=True,exist_ok=False)
    proposed=[]
    for row in delta:
        src=ROOT/'source-02'/row['path']
        if identity(src)!=row['after'] or identity(ROOT/'source-01'/row['path'])!=row['before']:
            raise ValueError('Workflow/source delta binding changed')
        actual=copy(src,DEST/'source'/row['path'])
        proposed.append({'path':row['path'],'source':'source/'+row['path'],**actual,
                         'required_active_baseline':'absent; verify against fetched main before activation'})
    for folder in ['reports/path-correction-01','reports/path-control-01']:
        for path in sorted((ROOT/folder).rglob('*')):
            if path.is_file():copy(path,DEST/'evidence'/path.relative_to(ROOT))
    for name in ['author_path_successor.py','check_queued_wrapper.py','run_path_control.py','freeze_path_successor.py']:
        copy(ROOT/name,DEST/'authoring'/name)
    copy(FIRST/'checkpoint.json',DEST/'parent-checkpoint.json')
    copy(FIRST/'blocker.json',DEST/'retained-parent-blocker.json')
    copy(ROOT/'source-01/.github/workflows/day-numeric-method-probe.yml',DEST/'retained-parent-workflow.yml')
    save(DEST/'proposed-active-files.json',proposed)
    save(DEST/'result.json',{
        'status':'CORRECTED_NUMERIC_ART_WORKFLOW_READY_FOR_FINAL_REVIEW',
        'parent_checkpoint_sha256':PARENT_SHA,
        'unchanged_source_roles':11,'changed_source_roles':1,
        'workflow':identity(ROOT/'source-02/.github/workflows/day-numeric-method-probe.yml'),
        'focused_static_control_passed':True,'focused_tests_executed':1,
        'old_queued_path_rejected':True,'corrected_positive_and_restoration_passed':True,
        'prior_30_offline_checks_preserved_without_rerun':True,
        'full_42_host_controls_rerun_locally':False,'hosted_full_42_suite_required':True,
        'android_executed':False,'application_build_executed':False,
        'workflow_activated':False,'full_runtime_1_to_1_established':False})
    (DEST/'README.md').write_text('''# Corrected neutral numeric ART workflow

This successor corrects one queued Python filename in the preserved first workflow. The command now invokes `tools/day_numeric_art/android_day_numeric_method_probe.py`, which is the exact pinned executable wrapper role. All other eleven source roles, including the preflight, runtime manifest and nine frozen probe/test inputs, are byte-for-byte unchanged. The original wrong spelling and all 30 actual offline outcomes remain in the immutable parent capsule.

## Exact correction and measured control

`evidence/reports/path-correction-01/derivation.patch` is the complete one-line workflow difference. One focused static unittest extracted the child command after the runtime queue's `--` boundary, parsed the actual queued argv, and required the script path to equal the unique pinned wrapper role. It accepted the corrected workflow, rejected the retained old spelling, and accepted the corrected workflow again. It did not execute probe or application code. All 166 source and preserved parent payloads checked around this test remained unchanged.

The final workflow is 14,360 bytes with SHA-256 `f5f37bab137d67bb9499f6e44749139213108814ff88636c864065ce45b23368`. The unchanged preflight and runtime manifest remain `61ac7a308128661eda663d1c36ee47baba238c2aa8ded9e0545fe5939e3cffd5` and `e3e6b34e6a531c1fe1ba2d82aef1a25fbb5fbd4535028564d8e7af6c3b8b0be3` respectively.

## Inherited measured scope

Parent checkpoint `3945eb046eaf5019099349383c3557ca752e27866b27dc80a9272af2ab2bf6ab` preserves the literal 43-role input positive, actual original/0762 APK preflight, two full multipart verification commands, fourteen rejection cases, three owned-cleanup results, seven shell syntax checks, six parsed Python snippets and both CLI imports. Its 30-command PASS remains literal historical evidence; the later-discovered queued-path blocker is explicit. Those checks were not repeated after the one-token path correction.

The exact nine source roles remain bound to schema-successor checkpoint `4d2bc4d8c9c5350b9572d5fa0b384438faf0a7b550156486da1e6701cc5eee1a`. The prior 41 wrapper controls and one focused schema control remain separate measured evidence. This preparation did not rerun the full 42-suite locally. The workflow requires all 42 in hosted CI.

## Runtime and publication boundaries

The future job uses immutable parent `fc825ede39a40249e33c8ba75b93128a98bd5e3c`, exact original `84333011…` and numeric candidate `0762aad9…`. Each APK gets one separate 120-second verification-enabled app_process64 process for the same 1,291 cases. Job, service, readiness, queue and owned cleanup bounds are unchanged. Complete raw and partial evidence and executed small sources are retained. No app is installed, no UI input is sent, and no macro or alarm is configured by this probe.

`proposed-active-files.json` specifies exactly twelve new paths. They are proposals for separately reviewed activation; this capsule itself applies none. No Android execution, application build, or new runtime parity result occurred during preparation.
''')
    files=[{'path':str(path.relative_to(DEST)),**identity(path)} for path in sorted(DEST.rglob('*')) if path.is_file()]
    checkpoint={'schema':1,'status':'CLOSED_WORKFLOW_PATH_SUCCESSOR_AND_ONE_FOCUSED_STATIC_CONTROL',
        'created_utc':datetime.now(timezone.utc).isoformat(),'repo_target':TARGET,'active_files':[],
        'parent_checkpoint_sha256':PARENT_SHA,'proposed_active_paths':12,'changed_from_parent_paths':1,
        'focused_static_tests_passed':1,'full_30_or_42_suites_rerun':False,
        'android_executed':False,'application_build_executed':False,'workflow_activated':False,
        'full_runtime_1_to_1_established':False,'frozen_payload_count':len(files),
        'frozen_payload_bytes':sum(row['bytes'] for row in files),'files':files}
    save(DEST/'checkpoint.json',checkpoint)
    print(json.dumps({'checkpoint':str(DEST/'checkpoint.json'),**identity(DEST/'checkpoint.json'),
                      'files':len(files),'payload_bytes':checkpoint['frozen_payload_bytes']},indent=2))


if __name__=='__main__':main()
