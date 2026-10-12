#!/usr/bin/env python3
"""Preserve the measured offline pass and later runtime-path review blocker unchanged."""
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat

ROOT = Path('/dev/shm/day-numeric-art-workflow-01')
DEST = ROOT / 'checkpoints/01-offline-validated-runtime-path-blocker'
TARGET = 'work-in-progress/day-numeric-art/06-offline-workflow-path-blocker'
EXPECTED_WORKFLOW = 'ac001726f95a7e055d888e0ccc16ce5354c4832c75e6259019adfa41b9b39127'
CACHE = {}


def identity(path):
    a = path.lstat()
    if not stat.S_ISREG(a.st_mode):
        raise ValueError('Expected regular frozen input')
    key = (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns,a.st_mode)
    if key not in CACHE:
        with path.open('rb') as stream:
            sha = hashlib.file_digest(stream,'sha256').hexdigest()
        b = path.lstat()
        if key != (b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns,b.st_ctime_ns,b.st_mode):
            raise ValueError('Frozen input changed while read')
        CACHE[key] = {'bytes':b.st_size,'sha256':sha,'mode':'100755' if b.st_mode&0o111 else '100644'}
    return CACHE[key].copy()


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value,indent=2)+'\n')
    path.chmod(0o644)


def copy(path,target):
    before=identity(path)
    target.parent.mkdir(parents=True,exist_ok=True)
    with path.open('rb') as source,target.open('xb') as output:
        shutil.copyfileobj(source,output,1024*1024)
    target.chmod(0o755 if before['mode']=='100755' else 0o644)
    if identity(path)!=before or identity(target)!=before:
        raise ValueError('Frozen copy identity differs')
    return before


def main():
    started=datetime.now(timezone.utc).isoformat()
    source=ROOT/'source-01'
    workflow=source/'.github/workflows/day-numeric-method-probe.yml'
    if identity(workflow)['sha256']!=EXPECTED_WORKFLOW:
        raise ValueError('Original reviewed workflow draft changed')
    results=json.loads((ROOT/'reports/validation-01/result.json').read_bytes())
    if not results['passed'] or len(results['commands'])!=30 or len(results['checks'])!=17:
        raise ValueError('Literal original offline pass differs')
    wrong='tools/day_numeric_art/android_numeric_method_probe.py'
    right='tools/day_numeric_art/android_day_numeric_method_probe.py'
    if workflow.read_text().count('$GITHUB_WORKSPACE/'+wrong)!=1 or (source/wrong).exists() or not (source/right).is_file():
        raise ValueError('Exact later-discovered runtime path blocker differs')
    before=json.loads((ROOT/'reports/validation-01/inputs-after.json').read_bytes())
    if any(identity(Path(name))!=expected for name,expected in before.items()):
        raise ValueError('Validated inputs changed before freezing')
    parents=[
      ('source-design','/dev/shm/macrodroid-day-numeric-art/source-draft-02/checkpoint.json','707afe796307be6044a5571cc39d4480ec032d2bf3d0ad87eb9a75118959deda'),
      ('compiled-probe','/dev/shm/macrodroid-day-numeric-art/checkpoints/02-compiled-probe-and-corpus/checkpoint.json','e3c67ab9f469e39b637cba2efd0ca6bd1a0892e49cc6333638b0b6aab66fd5ad'),
      ('independent-source-review','/dev/shm/macrodroid-day-numeric-art-independent-review/checkpoint.json','47a90e4ac7d13e50f4151f07417a8952907a269e382a1370a33406f105b69e67'),
      ('root-schema-review','/dev/shm/macrodroid-day-numeric-art-schema-root-review/review-01/checkpoint.json','49b84bf68c2bac9e88bdd9a9e28f87ac13259fba705480701ddb1b616e8ff097'),
    ]
    for label,name,sha in parents:
        path=Path(name)
        if identity(path)['sha256']!=sha:
            raise ValueError('Closed provenance checkpoint changed')
        copy(path,ROOT/'inputs/provenance'/(label+'-checkpoint.json'))
    blocker={'status':'REVIEWED_QUEUED_WRAPPER_PATH_DOES_NOT_EXIST',
        'workflow':identity(workflow),'queued_wrapper_path':wrong,'queued_path_exists':False,
        'required_pinned_wrapper_path':right,'required_wrapper':identity(source/right),
        'cause':'The general widget_ to numeric_ replacement preceded the intended wrapper-specific replacement.',
        'offline_30_result_preserved':True,'android_command_executed':False,
        'activation_blocked':True,'required_successor':'Change only the queued filename and add a focused queued-script-to-pinned-source-role check.'}
    save(ROOT/'reports/runtime-path-review-blocker.json',blocker)
    # Inventory every owned regular path and symlink before creating the capsule.
    paths=sorted(path for path in ROOT.rglob('*') if 'checkpoints' not in path.relative_to(ROOT).parts and (path.is_file() or path.is_symlink()))
    DEST.mkdir(parents=True,exist_ok=False)
    source_rows=[]
    local_refs={}
    def remember(path,relative):
        value=copy(path,DEST/relative)
        local_refs[(value['bytes'],value['sha256'],value['mode'])]={'kind':'local','path':relative}
        return value
    for path in sorted(source.rglob('*')):
        if path.is_file():
            relative=str(path.relative_to(source))
            value=remember(path,'source/'+relative)
            source_rows.append({'path':relative,**value})
    # Retain parent small source once. Large immutable APK parts use exact Git references.
    manifest=json.loads((source/'tools/day_numeric_art/runtime-files.json').read_bytes())
    external={}
    for row in manifest['parent_roles']:
        key=(row['bytes'],row['sha256'],row['mode'])
        if row['retain_copy']:
            remember(ROOT/'inputs/parent'/row['path'],'parent-source/'+row['path'])
        else:
            external[key]={'kind':'git_blob','commit':manifest['parent_commit'],'path':row['path'],
                           'git_blob_sha1':row['git_blob_sha1']}
    for name in ('vendor/original/manifest.json','work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json'):
        path=ROOT/'inputs/parent'/name
        value=json.loads(path.read_bytes())
        external[(value['size_bytes'],value['sha256'],'100644')]={
            'kind':'multipart_manifest','commit':manifest['parent_commit'],'path':name,
            'manifest_bytes':path.stat().st_size,'manifest_sha256':identity(path)['sha256']}
    index=[]
    logical=0
    for path in paths:
        relative=str(path.relative_to(ROOT))
        if path.is_symlink():
            index.append({'path':relative,'type':'symlink','target':os.readlink(path),'retained_as_inert_metadata':True})
            continue
        value=identity(path)
        key=(value['bytes'],value['sha256'],value['mode'])
        reference=local_refs.get(key) or external.get(key)
        if reference is None:
            if value['bytes']>8*1024*1024:
                raise ValueError('Unexpected large unbound owned payload: '+relative)
            target='review/'+relative
            remember(path,target)
            reference=local_refs[key]
        index.append({'path':relative,'type':'regular',**value,'reference':reference})
        logical+=value['bytes']
    inventory={'schema':1,'scope':'Complete owned files at closure; raw case-tree bytes are retained once or bound to immutable existing Git/APK containers.',
               'regular_paths':sum(row['type']=='regular' for row in index),
               'symlink_paths':sum(row['type']=='symlink' for row in index),
               'logical_regular_bytes':logical,'files':index}
    raw=(json.dumps(inventory,separators=(',',':'))+'\n').encode()
    compressed=gzip.compress(raw,compresslevel=9,mtime=0)
    with (DEST/'complete-evidence-index.json.gz').open('xb') as stream:stream.write(compressed)
    save(DEST/'complete-evidence-index.metadata.json',{
        'compressed':identity(DEST/'complete-evidence-index.json.gz'),
        'decompressed':{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},
        'paths':len(index),'logical_regular_bytes':logical})
    save(DEST/'source-files.json',source_rows)
    save(DEST/'blocker.json',blocker)
    save(DEST/'closed-result.json',{
        'literal_offline_status':results['status'],'offline_checks_passed':True,
        'offline_commands':30,'rejection_cases':14,'owned_cleanup_controls':3,
        'bash_syntax_checks':7,'python_snippets_parsed':6,'protected_inputs_unchanged':48,
        'hosted_42_suite_required':True,'full_42_suite_executed_locally':False,
        'activation_blocked':True,'android_executed':False,'application_build_executed':False,
        'full_runtime_1_to_1_established':False,'complete_evidence_paths':len(index)})
    (DEST/'README.md').write_text('''# Neutral numeric ART workflow: offline pass and reviewed path blocker

This immutable first workflow draft passed its 30 executed offline checks, but root review then found a blocking queued wrapper filename. It is historical preparation evidence and must not be activated. No Android command or application build ran.

The queued path is `tools/day_numeric_art/android_numeric_method_probe.py`; that file does not exist. The exact reviewed source role is `tools/day_numeric_art/android_day_numeric_method_probe.py`. The broad `widget_` to `numeric_` derivation ran before the wrapper-specific substitution. The 30 checks validated the correct direct CLI path, complete inputs, APKs, shell syntax and cleanup; they did not bind the queued script name to the manifest role. `blocker.json` retains the literal mismatch. A separately frozen successor is required.

## Actual offline evidence

The unchanged run completed at 2026-10-12 12:56:45 UTC in 103.13 seconds. Seven shell blocks and six Python heredoc snippets were parsed. Both CLI entry points ran. The literal 43-role positive and actual original/0762 APK preflight passed, and the unchanged assembler verified both complete multipart containers without assembling a duplicate APK. Fourteen input, output, and final-evidence faults were rejected, including the explicit simulated-report-as-Android rejection. Three simulated owned-cleanup paths produced the required exits 0, 7 and 1. All 48 protected file bytes and modes remained exact.

The full 42 wrapper controls were not rerun locally. The closed old 41-control proof and focused one-control schema successor are retained as separate prior evidence. The future workflow requires all 42 controls on its exact final source. Numeric cases remain the same 1,291 per APK, with separate verification-enabled 120-second app_process64 invocations; no app installation, UI, macro configuration, or alarm scheduling is authorized by this probe.

## Exact source and storage

`source/` contains the nine unchanged schema-successor roles, the new preflight and runtime manifest, and this blocked workflow. `parent-source/` preserves the small immutable parent tools. `review/` retains authored scripts, raw commands and all unique new evidence bytes. The complete compressed index covers every owned regular path and the inert symlink fault; repeated large case inputs refer to exact immutable Git blobs or the original/candidate multipart manifests at parent `fc825ede39a40249e33c8ba75b93128a98bd5e3c`.

The approved offline transport copied 95,725,918 original-part bytes once across filesystems. Numeric parts and both existing complete APKs were hardlinked read-only. The receipt records each part and unchanged source bytes/modes; it does not claim unchanged link-count/ctime metadata. No APK data file was duplicated or assembled. All large bytes were already durable repository inputs.

This capsule establishes the stated offline observations and their publication bindings. It does not establish a usable activated workflow, real ART success, or whole-application parity.
''')
    # Confirm closure still binds every protected input and the exact original workflow.
    if any(identity(Path(name))!=expected for name,expected in before.items()):
        raise ValueError('Protected input changed during freezing')
    files=[{'path':str(path.relative_to(DEST)),**identity(path)} for path in sorted(DEST.rglob('*')) if path.is_file()]
    checkpoint={'schema':1,'status':'OFFLINE_CHECKS_PASSED_WITH_REVIEWED_RUNTIME_PATH_BLOCKER',
        'created_utc':datetime.now(timezone.utc).isoformat(),'started_utc':started,
        'repo_target':TARGET,'active_files':[],'activation_authorized':False,
        'source_roles':12,'workflow_sha256':EXPECTED_WORKFLOW,'offline_commands':30,
        'offline_checks_passed':True,'runtime_path_blocker_preserved':True,
        'android_executed':False,'application_build_executed':False,'full_runtime_1_to_1_established':False,
        'indexed_paths':len(index),'indexed_logical_bytes':logical,
        'frozen_payload_count':len(files),'frozen_payload_bytes':sum(row['bytes'] for row in files),'files':files}
    save(DEST/'checkpoint.json',checkpoint)
    print(json.dumps({'checkpoint':str(DEST/'checkpoint.json'),**identity(DEST/'checkpoint.json'),
                      'files':len(files),'payload_bytes':checkpoint['frozen_payload_bytes'],
                      'indexed_paths':len(index),'indexed_logical_bytes':logical},indent=2))


if __name__=='__main__':main()
