"""Preserve one complete CI ZIP and its reviewed candidate without full expansion."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import shutil
import stat
import zipfile

BASE = Path('/dev/shm/macrodroid-transfer-space-20261012')
DOWNLOAD = BASE / 'numeric-run-38238858564'
ARCHIVE = DOWNLOAD / 'artifact.zip'
ROOT = BASE / 'numeric-success-raw-capsule'
CANDIDATE = BASE / 'numeric-success-candidate-capsule'
PREFIX = 'docs/verification/day-numeric-hosted-run-3d91187'
APK_PREFIX = 'work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact'
ARCHIVE_BYTES = 222144520
ARCHIVE_SHA = 'a7b52e6096db27cf9854671fcd3f6d1b7c3f73f5cf0255fcb9fc6fdc5afc117c'
APK_MEMBER = 'numeric-workspace/MacroDroid_v9/dist/MacroDroid-5.67.8-v9-hybrid.apk'
APK_BYTES = 94683136
APK_SHA = '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd'
HEAD = '3d91187924af10457366ede7a1a8f10d3a1a6ac4'
RUN = 38238858564
ARTIFACT = 11741869868
CHUNK = 8 * 1024 * 1024

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def identity(path):
    st = path.lstat(); assert stat.S_ISREG(st.st_mode)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes':st.st_size,'sha256':digest,'mode':stat.S_IMODE(st.st_mode)}

def write(root, name, value):
    path = root / name; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')

def link(source, destination):
    destination.parent.mkdir(parents=True,exist_ok=True)
    os.link(source,destination)
    assert identity(source)==identity(destination)

def part(root, prefix, number, raw):
    local = 'parts/part-' + str(number).zfill(4) + '.bin'
    path=root/local;path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream:stream.write(raw)
    assert identity(path)['sha256']==sha(raw)
    return {'path':prefix+'/'+local,'size_bytes':len(raw),'sha256':sha(raw),
            'git_blob_sha1':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}

def freeze(root, target, status):
    shutil.copy2(Path(__file__),root/'publication/prepare_numeric_hosted_container.py')
    rows=[]
    for path in sorted(root.rglob('*')):
        if path.is_file():rows.append({'path':path.relative_to(root).as_posix(),**identity(path)})
    write(root,'checkpoint.json',{'schema':1,'status':status,'created_utc':datetime.now(timezone.utc).isoformat(),
        'repo_target':target,'active_files':[],'run_id':RUN,'head_sha':HEAD,'artifact_id':ARTIFACT,
        'android_runtime_executed_here':False,'active_application_promoted':False,'files':rows})
    return {'source':str(root),'target':target,'checkpoint_sha256':identity(root/'checkpoint.json')['sha256'],
            'files':len(rows),'payload_bytes':sum(r['bytes'] for r in rows)}

started = datetime.now(timezone.utc).isoformat()
assert identity(ARCHIVE)=={'bytes':ARCHIVE_BYTES,'sha256':ARCHIVE_SHA,'mode':0o644}
ROOT.mkdir(exist_ok=False);CANDIDATE.mkdir(exist_ok=False)
(ROOT/'publication').mkdir();(CANDIDATE/'publication').mkdir()
raw_names=set();members=[];selected=[];apk_parts=[];apk_hash=hashlib.sha256();apk_total=0
selected_reports={'acceptance-latest.json','day-numeric-dex-controls.json','full-apk-edit-probe.json',
    'python-unit-tests.json','reference-status.json','hybrid-build.json','baseline-build.json',
    'ui-negative-controls.json','baseline-resource-parity.json','hybrid-resource-parity.json'}
with zipfile.ZipFile(ARCHIVE) as archive:
    assert len(archive.infolist())==3308
    literal=json.loads(archive.read('hosted-proof/verification.json'))
    assert literal['status']=='ISOLATED_DAY_NUMERIC_ALL_16_HOST_GATES_VERIFIED' and literal['passed'] is True
    assert literal['gates_verified']==16 and literal['fresh_reports_verified']==23
    assert literal['source_snapshot']=={'files':81298,'snapshot_sha256':'f8fc1cadac8213468e42ac99a2cd5d807827dcdeee25166b8025620ff39a6545'}
    assert literal['apks']['hybrid']=={'bytes':APK_BYTES,'sha256':APK_SHA}
    for info in archive.infolist():
        name=info.filename;pure=PurePosixPath(name);mode=info.external_attr>>16
        assert not info.is_dir() and not pure.is_absolute() and '..' not in pure.parts and pure.as_posix()==name and '\\' not in name
        assert name not in raw_names and not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in (0,stat.S_IFREG)
        raw_names.add(name)
        report_name=name.removeprefix('numeric-workspace/MacroDroid_v9/reports/')
        keep=(name.startswith('job-source/') or name in ('hosted-tool-host-tests.log','hosted-tool-source-verification.json')
              or (name.startswith('hosted-proof/') and name.count('/')==1)
              or (name.startswith('numeric-workspace/MacroDroid_v9/reports/') and
                  (report_name in selected_reports or re.fullmatch(r'acceptance-[^/]+/[^/]+',report_name))))
        keep=keep and info.file_size<=1024*1024
        saved=None
        if keep:
            saved=ROOT/'selected'/name;saved.parent.mkdir(parents=True,exist_ok=True)
        digest=hashlib.sha256();size=0
        with archive.open(info) as stream:
            output=saved.open('xb') if saved else None
            try:
                while chunk:=stream.read(CHUNK if name==APK_MEMBER else 1024*1024):
                    digest.update(chunk);size+=len(chunk)
                    if output:output.write(chunk)
                    if name==APK_MEMBER:
                        apk_parts.append(part(CANDIDATE,APK_PREFIX,len(apk_parts)+1,chunk))
                        apk_hash.update(chunk);apk_total+=len(chunk)
            finally:
                if output:output.close()
        assert size==info.file_size
        row={'path':name,'bytes':size,'sha256':digest.hexdigest(),'zip_crc32':info.CRC,
             'zip_mode':mode,'zip_timestamp':list(info.date_time),'selected_direct_copy':bool(saved)}
        members.append(row)
        if saved:
            assert identity(saved)['sha256']==row['sha256']
            selected.append({'path':'selected/'+name,'archive_member':name,'bytes':size,'sha256':row['sha256']})
assert len(members)==3308 and sum(r['bytes'] for r in members)==568138240
assert apk_total==APK_BYTES and apk_hash.hexdigest()==APK_SHA and len(apk_parts)==12
assert identity(ARCHIVE)=={'bytes':ARCHIVE_BYTES,'sha256':ARCHIVE_SHA,'mode':0o644}
parts=[];whole=hashlib.sha256();total=0
with ARCHIVE.open('rb') as stream:
    while chunk:=stream.read(CHUNK):
        parts.append(part(ROOT,PREFIX,len(parts)+1,chunk));whole.update(chunk);total+=len(chunk)
assert total==ARCHIVE_BYTES and whole.hexdigest()==ARCHIVE_SHA and len(parts)==27
write(ROOT,'manifest.json',{'format':'macrodroid-multipart-artifact','format_version':1,
    'id':'day-numeric-wip-run-38238858564','filename':'day-numeric-wip-run-38238858564.zip','media_type':'application/zip',
    'size_bytes':ARCHIVE_BYTES,'sha256':ARCHIVE_SHA,'parts':parts,'source_commit':HEAD,'run_id':RUN,'artifact_id':ARTIFACT,
    'purpose':'Exact complete successful isolated numeric source-job artifact; all original ZIP bytes retained.',
    'active_application_promoted':False,'whole_application_1_to_1_established':False})
write(ROOT,'archive-member-metadata.json',{'schema':1,'archive_sha256':ARCHIVE_SHA,'member_count':len(members),
    'expanded_bytes':sum(r['bytes'] for r in members),'all_members_streamed_and_crc_verified':True,
    'full_archive_extracted':False,'files':members})
write(ROOT,'selected-member-copies.json',{'schema':1,'scope':'Bounded readable subset; every other exact member remains in the complete ZIP.',
    'files':selected,'copied_bytes':sum(r['bytes'] for r in selected)})
write(ROOT,'publication/container-verification.json',{'schema':1,'started_utc':started,
    'completed_utc':datetime.now(timezone.utc).isoformat(),'archive_bytes':ARCHIVE_BYTES,'archive_sha256':ARCHIVE_SHA,
    'member_count':3308,'expanded_bytes':568138240,'part_count':27,'all_parts_sha256_and_git_sha1_verified':True,
    'whole_zip_identity_verified_before_after':True,'duplicate_zip_assembly_written':False,'full_archive_extracted':False,
    'candidate_part_count':12,'candidate_apk_sha256':APK_SHA,'candidate_full_file_written':False,
    'acceptance_or_android_reexecuted_here':False})
for name in ('github-run.json','github-jobs.json','github-artifacts.json'):
    link(DOWNLOAD/name,ROOT/name)
link(DOWNLOAD/'artifact.zip.download.json',ROOT/'download-receipt.json')
link(DOWNLOAD/'download_verified_artifact.py',ROOT/'publication/download_verified_artifact.py')
write(CANDIDATE,'manifest.json',{'format':'macrodroid-multipart-artifact','format_version':1,
    'id':'day-numeric-hosted-accepted-0762aad9','filename':'MacroDroid-5.67.8-day-numeric-0762aad9.apk',
    'media_type':'application/vnd.android.package-archive','size_bytes':APK_BYTES,'sha256':APK_SHA,'parts':apk_parts,
    'source_commit':HEAD,'source_baseline_commit':BASELINE if False else 'dbcad968c5c3e8f084205393a6c0d2d06a203c71',
    'source_overlay_commit':'811f979eda1b937917c18defef38455c49a59062',
    'source_overlay_checkpoint_sha256':'d9ddd3e0f692c66e2cd47870ff3cf95bfa0a2b1cd50fc2fd55a3c09e66df9bcf',
    'source_snapshot':literal['source_snapshot'],'source_manifest':literal['future_manifest'],
    'run_id':RUN,'artifact_id':ARTIFACT,'container_manifest':PREFIX+'/manifest.json',
    'container_sha256':ARCHIVE_SHA,'container_member':APK_MEMBER,
    'registered_recovered_bodies':1243,'reported_host_cases':194780,'reported_host_gates_passed':16,
    'purpose':'Immutable host-accepted numeric candidate for separately reviewed Android observation; active application promotion is separate.',
    'active_application_promoted':False,'android_runtime_parity_established':False,'whole_application_1_to_1_established':False})
write(CANDIDATE,'apk-container-binding.json',{'schema':1,'source_zip':{'bytes':ARCHIVE_BYTES,'sha256':ARCHIVE_SHA},
    'exact_unique_member':next(r for r in members if r['path']==APK_MEMBER),'artifact_id':ARTIFACT,'run_id':RUN,
    'all_twelve_parts_streamed_from_exact_member':True,'whole_apk_sha256':APK_SHA,
    'full_apk_duplicate_file_created':False,'active_application_or_workflow_changed':False})
link(ROOT/'selected/hosted-proof/verification.json',CANDIDATE/'reported-host-verification.json')
link(ROOT/'publication/container-verification.json',CANDIDATE/'publication/container-verification.json')
(ROOT/'README.md').write_text(f'''# Complete successful isolated numeric host run

[Run {RUN}](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/{RUN}) used tooling commit `{HEAD}` and completed its sixteen source acceptance gates and independent live verifier. The literal result is `ISOLATED_DAY_NUMERIC_ALL_16_HOST_GATES_VERIFIED`. It reports 194,780 three-path cases, 1,243 registered bodies, 308 Python tests, 23 fresh reports, 91 Java UI faults, and the separately bound numeric method controls. Its Android probe remains blocked; this is host/source evidence. Active application promotion is separate.

Artifact `{ARTIFACT}` is exactly {ARCHIVE_BYTES:,} bytes, SHA-256 `{ARCHIVE_SHA}`. All 3,308 members ({568138240:,} expanded bytes) were streamed, CRC-checked and hashed without a full expansion. [archive-member-metadata.json](archive-member-metadata.json) preserves every member identity, ZIP mode, CRC and timestamp. [selected/](selected/) contains only the explicitly inventoried readable subset; all remaining complete raw files, historical attempts, classes, reports, source copies and APKs remain in the unchanged container. [selected-member-copies.json](selected-member-copies.json) documents that subset.

From the repository root, verify or assemble the exact ZIP:

```bash
python3 scripts/assemble_artifact.py {PREFIX}/manifest.json --verify-only
python3 scripts/assemble_artifact.py {PREFIX}/manifest.json
```

The 94,683,136-byte hybrid APK has SHA-256 `{APK_SHA}`. Its exact member bytes are also published in [{APK_PREFIX}/manifest.json](../../../{APK_PREFIX}/manifest.json) for a separately reviewed runtime experiment. The baseline APK and every other ZIP member remain preserved in the full artifact. Independent source and signed-output analysis is additive under `analysis/`; raw reports are never rewritten to match later conclusions.
''')
(CANDIDATE/'README.md').write_text(f'''# Immutable host-accepted numeric APK

This exact 94,683,136-byte APK, SHA-256 `{APK_SHA}`, was produced by successful isolated numeric host run [{RUN}](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/{RUN}). The complete source manifest binds 81,298 inputs to snapshot `f8fc1cadac8213468e42ac99a2cd5d807827dcdeee25166b8025620ff39a6545`. The host result covers 1,243 registered bodies and 194,780 three-path cases. No runtime parity or active application promotion is claimed here.

All twelve parts were streamed directly from the unique APK member in artifact `{ARTIFACT}`. [apk-container-binding.json](apk-container-binding.json) and [manifest.json](manifest.json) retain the exact container, source, run and byte bindings. No second APK download or full duplicate APK file was created.

```bash
python3 scripts/assemble_artifact.py {APK_PREFIX}/manifest.json --verify-only
python3 scripts/assemble_artifact.py {APK_PREFIX}/manifest.json
```

The existing fixed indicator experiment keeps its own previous APK pin. This candidate is available only to workflows that explicitly bind this immutable manifest and commit. Changing the active project/current manifest requires a separate coherent promotion.
''')
results=[freeze(ROOT,PREFIX,'EXACT_SUCCESSFUL_NUMERIC_CI_CONTAINER_PRESERVED'),
         freeze(CANDIDATE,APK_PREFIX,'EXACT_HOST_ACCEPTED_NUMERIC_APK_PRESERVED_INACTIVE')]
write(BASE,'numeric-success-capsules.json',results)
print(json.dumps(results))
