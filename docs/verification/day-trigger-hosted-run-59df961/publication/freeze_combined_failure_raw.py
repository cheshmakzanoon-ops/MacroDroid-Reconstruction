"""Freeze the exact failed combined tooling CI artifact and every extracted member."""
from pathlib import Path
from datetime import datetime, timezone
import errno, hashlib, json, os, shutil, stat, zipfile
ROOT=Path('/dev/shm/macrodroid-transfer-space-20261012')
SRC=ROOT/'combined-run-38245093369'
OUT=ROOT/'combined-failure-raw-capsule-02'
TARGET='docs/verification/day-trigger-hosted-run-59df961'
OUT.mkdir(exist_ok=False)
def digest(raw): return hashlib.sha256(raw).hexdigest()
def copy(source,name):
    s=source.lstat();assert stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode)==0o644
    dest=OUT/name;dest.parent.mkdir(parents=True,exist_ok=True)
    try: os.link(source,dest)
    except OSError as error:
        if error.errno != errno.EXDEV: raise
        with source.open('rb') as src, dest.open('xb') as dst: shutil.copyfileobj(src,dst)
        dest.chmod(stat.S_IMODE(s.st_mode))
    assert source.read_bytes()==dest.read_bytes()
def put(name,value):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(value)
    p.chmod(0o644)
receipt=json.loads((SRC/'extracted-extraction.json').read_text())
assert receipt['archive']=={'bytes':4960179,'sha256':'cc5afbb6833350ec9693b361ee63dae961587a30e90c35e57850c835e4b7f833'}
assert receipt['member_count']==4355 and receipt['expanded_bytes']==21756616
assert receipt['key_scan_findings']==[]
raw=(SRC/'artifact.zip').read_bytes();assert len(raw)==4960179 and digest(raw)==receipt['archive']['sha256']
with zipfile.ZipFile(SRC/'artifact.zip') as z:
    assert len(z.infolist())==4355
    for row in receipt['files']:
        p=SRC/'extracted'/row['path'];raw=p.read_bytes()
        assert len(raw)==row['bytes'] and digest(raw)==row['sha256']
        assert z.read(row['path'])==raw
        copy(p,'extracted/'+row['path'])
for src,name in [('artifact.zip','artifact.zip'),('artifact.zip.download.json','download-receipt.json'),
                 ('extracted-extraction.json','extraction-receipt.json'),('github-jobs.json','github-jobs.json'),
                 ('github-run.json','github-run.json'),('github-artifacts.json','github-artifacts.json'),
                 ('expected-artifact.json','expected-artifact.json')]: copy(SRC/src,name)
copy(ROOT/'download_verified_artifact.py','publication/download_verified_artifact.py')
copy(Path('/workspace/scratch/4130730d15aa/ci-run-analysis/extract_artifact.py'),'publication/extract_artifact.py')
copy(Path(__file__),'publication/freeze_combined_failure_raw.py')
job=json.loads((SRC/'github-jobs.json').read_text())['jobs'][0]
steps={r['number']:r for r in job['steps']}
assert job['id']==114796870050 and job['conclusion']=='failure'
assert steps[8]['conclusion']=='failure' and steps[9]['conclusion']==steps[10]['conclusion']=='skipped'
assert steps[11]['conclusion']=='failure' and steps[12]['conclusion']=='success'
verdict=json.loads((SRC/'extracted/hosted-proof/verification.json').read_text())
status={'schema':1,'run_id':38245093369,'job_id':job['id'],'head_sha':'59df96186fefb2bf883031c09562af08b48bde16',
        'artifact_id':11744651182,'archive':receipt['archive'],'raw_members':4355,'expanded_bytes':21756616,
        'tooling_controls':'FAILURE','physical_source_preparation':'SKIPPED','full_sixteen_application_gates':'SKIPPED',
        'final_verifier':'FAILURE','evidence_upload':'SUCCESS','literal_verification':verdict,
        'new_application_build_or_android_claim':False,'artifact_transformations':[],
        'raw_transport_verified_utc':datetime.now(timezone.utc).isoformat()}
put('transport-status.json',(json.dumps(status,indent=2)+'\n').encode())
put('README.md',b'''# Combined DayTrigger tooling run: pre-application failure

The single original artifact from run `38245093369`, job `114796870050`, at commit `59df96186fefb2bf883031c09562af08b48bde16` is preserved unchanged as [artifact.zip](artifact.zip). It is 4,960,179 bytes with SHA-256 `cc5afbb6833350ec9693b361ee63dae961587a30e90c35e57850c835e4b7f833`.

The tooling host-control step failed. Physical source preparation and all sixteen application acceptance gates were skipped; the final verifier reported failure and artifact upload succeeded. This run supplies no new application build or Android result. Its exact [host-control log](extracted/hosted-tool-host-tests.log), [final verification](extracted/hosted-proof/verification.json) and [job step metadata](github-jobs.json) remain the primary observations.

All 4,355 original ZIP members, totaling 21,756,616 bytes, are also directly available under [extracted/](extracted/). Every extracted file was compared against its size/SHA-256 inventory and the original ZIP member again at freezing. [extraction-receipt.json](extraction-receipt.json) records their identities. No raw member was edited, and the recorded key-pattern scan found no matches.

The successful numeric-only source run and its signed APK retain their separate proof. Diagnosis or corrections for this failed combined tooling run must be published as additive successors; this immutable failure remains unchanged.
''')
for p in sorted((ROOT/'combined-failure-freeze-attempt01').iterdir()): copy(p,'publication/first-freezer-attempt/'+p.name)
files=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file():
        raw=p.read_bytes();files.append({'path':p.relative_to(OUT).as_posix(),'bytes':len(raw),'sha256':digest(raw),'mode':stat.S_IMODE(p.stat().st_mode)})
cp={'schema':1,'status':'IMMUTABLE_COMBINED_TOOLING_HOST_FAILURE_BEFORE_APPLICATION_EXECUTION','repo_target':TARGET,
    'active_files':[],'run_id':38245093369,'artifact_id':11744651182,'files':files}
put('checkpoint.json',(json.dumps(cp,indent=2)+'\n').encode())
print(json.dumps({'source':str(OUT),'target':TARGET,'checkpoint_sha256':digest((OUT/'checkpoint.json').read_bytes()),'files':len(files),'payload_bytes':sum(r['bytes'] for r in files)}))
