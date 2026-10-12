"""Prepare nine absent combined tooling paths from fetched reviewed Git blobs."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, stat, subprocess

p = argparse.ArgumentParser()
p.add_argument('--parent', required=True)
p.add_argument('--receipt', type=Path, required=True)
a = p.parse_args()
ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012')
GIT = ROOT / 'verification.git'
PACKAGE = 'work-in-progress/day-trigger-lookup/12-combined-tooling-host-controls'
LOCAL = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/08-combined-tooling-controls')
REVIEW = 'docs/verification/day-trigger-combined/tooling-review'
TARGET = 'docs/verification/day-trigger-combined/tooling-activation'
EXPORT = ROOT / 'combined-tooling-activation-export'
TREE = ROOT / 'combined-tooling-activation-tree'
EXPECTED = {
    '.github/workflows/day-trigger-wip-acceptance.yml',
    'tools/day_trigger_acceptance/README.md',
    'tools/day_trigger_acceptance/inputs.py',
    'tools/day_trigger_acceptance/pins.json',
    'tools/day_trigger_acceptance/prepare.py',
    'tools/day_trigger_acceptance/run_acceptance.py',
    'tools/day_trigger_acceptance/runtime-files.json',
    'tools/day_trigger_acceptance/test_day_trigger_acceptance.py',
    'tools/day_trigger_acceptance/verify.py',
}
CHECKPOINTS = {
    PACKAGE: ('4447e68a4c26b3a0214f1376e22bf97da250809d553c3102481d1196660bbc88', 65),
    REVIEW: ('25fe5ae3fc77498856248d19afcf4dfaa8ab4a3c3bb7d89dcb07a8e532986ef9', 24),
}
os.environ['GIT_OPTIONAL_LOCKS'] = '0'
def git(*args):
    return subprocess.check_output(['git', '--git-dir=' + str(GIT), *args])
def digest(raw): return hashlib.sha256(raw).hexdigest()
def identity(raw): return {'bytes':len(raw), 'sha256':digest(raw)}
def oid(raw): return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
assert git('rev-parse', 'refs/heads/main').decode().strip() == a.parent
entries = {}
for item in git('ls-tree', '-rz', '--full-tree', a.parent).split(b'\0'):
    if item:
        header, name = item.split(b'\t', 1)
        entries[name.decode()] = tuple(header.decode().split())
def fetched(name):
    mode, kind, blob = entries[name]
    assert kind == 'blob' and mode == '100644', name
    raw = git('cat-file', 'blob', blob)
    assert oid(raw) == blob
    return raw
checkpoint_proofs=[]
for prefix, (expected_sha,count) in CHECKPOINTS.items():
    raw = fetched(prefix + '/checkpoint.json')
    assert digest(raw) == expected_sha
    cp = json.loads(raw)
    assert len(cp['files']) == count == len({r['path'] for r in cp['files']})
    for row in cp['files']:
        content = fetched(prefix + '/' + row['path'])
        assert identity(content) == {k:row[k] for k in ('bytes','sha256')}
        if 'mode' in row:
            mode = int(row['mode'],8) & 0o777 if isinstance(row['mode'],str) else row['mode']
            assert mode == 0o644
    checkpoint_proofs.append({'path':prefix + '/checkpoint.json',**identity(raw),'payloads':count,'fetched_payloads_verified':True})
source_cp = json.loads(fetched(PACKAGE + '/checkpoint.json'))
assert fetched(PACKAGE + '/checkpoint.json') == (LOCAL/'checkpoint.json').read_bytes()
assert source_cp['active_source_changed'] is False and source_cp['active_workflow_changed'] is False
assert source_cp['full_host_acceptance_executed'] is False
rows = json.loads(fetched(PACKAGE + '/nine-path-bindings.json'))['files']
assert len(rows) == 9 and {r['path'] for r in rows} == EXPECTED
assert not any(path in entries for path in EXPECTED)
manifest=[]; elements=[]; bindings=[]
for row in rows:
    name=row['path']; candidate=row['candidate']
    assert row['active_path_must_be_absent'] is True and candidate['mode'] == 0o644
    source_path=PACKAGE+'/source/'+name
    raw=fetched(source_path)
    assert identity(raw) == {k:candidate[k] for k in ('bytes','sha256')}
    previous=fetched(row['parent_tooling_path'])
    assert identity(previous) == {k:row['parent_tooling'][k] for k in ('bytes','sha256')}
    local=LOCAL/'source'/name
    st=local.lstat()
    assert stat.S_ISREG(st.st_mode) and stat.S_IMODE(st.st_mode) == 0o644
    assert raw == local.read_bytes()
    elements.append({'path':name,'mode':'100644','type':'blob','sha':entries[source_path][2]})
    manifest.append({'path':name,'local_path':str(local),'size_bytes':len(raw),'sha256':digest(raw),'git_blob_sha1':oid(raw),'mode':'100644'})
    bindings.append({'path':name,'mode':'100644','baseline':'ABSENT','candidate':identity(raw),'git_blob_sha1':oid(raw),'fetched_source_path':source_path,'parent_tooling_unchanged':row['parent_tooling_path']})
assert next(r['candidate']['sha256'] for r in bindings if r['path'].startswith('.github/')) == '443e184bc3185593e1a8c268d60200ada2b1cdb6df2b8e551e51ae52dae0c6eb'
assert next(r['candidate']['sha256'] for r in bindings if r['path'].endswith('/runtime-files.json')) == '07b58ce29d4db875ef349d23aa05b8b75145ea4f7338b7dd2943db10129a0d32'
receipt_raw=a.receipt.read_bytes(); receipt=json.loads(receipt_raw)
assert receipt['commit'] == a.parent and receipt['git_mode_size_sha1_sha256_verified'] is True
assert receipt['staged_bytes_and_modes_equal_fetched_git'] is True
protected={name:git('rev-parse',a.parent+':'+name).decode().strip() for name in ('project','artifacts/current','vendor')}
guard={'schema':1,'status':'NINE_ABSENT_COMBINED_TOOLING_PATHS_VERIFIED_FOR_ACTIVATION',
       'parent_commit':a.parent,'completed_utc':datetime.now(timezone.utc).isoformat(),
       'checkpoint_proofs':checkpoint_proofs,'active_path_bindings':bindings,
       'latest_fetched_review_receipt':identity(receipt_raw),'protected_tree_oids':protected,
       'all_nine_remote_paths_absent':True,'all_nine_modes':'100644',
       'source_package_and_root_review_fetched':True,'active_application_source_or_apk_promoted':False,
       'full_combined_acceptance_result':'PENDING_ISOLATED_HOSTED_RUN',
       'existing_numeric_and_device_workflows_unchanged':True,'workspace_or_index_mutated':False}
EXPORT.mkdir(exist_ok=False)
doc_root=TREE/TARGET; doc_root.mkdir(parents=True,exist_ok=False)
readme='''# Combined DayTrigger tooling activation

This checkpoint adds the exact nine previously absent tooling/workflow paths from the frozen `4447e68a` package after its complete 65-file source/evidence capsule and the `25fe5ae3` root review were fetched and rehashed. All nine files have mode `100644`.

The frozen package records 153 tooling host controls. The new workflow runs isolated full acceptance of the numeric and lookup source union. That new application's full hosted outcome is pending at activation. This commit does not promote application source or an APK.

The [activation guard](activation-guard.json) records every absent target, exact reviewed candidate, unchanged numeric tooling parent, checkpoint hash, and protected application tree. Existing numeric and Android workflows remain intact. The [executed preparer](executed-prepare.py) performs read verification and prepares these bounded evidence files; the remote ref update and fetched commit verification are separate, guarded steps.
'''
docs={'activation-guard.json':(json.dumps(guard,indent=2)+'\n').encode(),
      'executed-prepare.py':Path(__file__).read_bytes(),
      'review-publication-fetch-verification.json':receipt_raw,'README.md':readme.encode()}
for name,raw in docs.items():
    path=TARGET+'/'+name; assert path not in entries
    local=doc_root/name; local.write_bytes(raw); local.chmod(0o644)
    elements.append({'path':path,'mode':'100644','type':'blob','content':raw.decode()})
    manifest.append({'path':path,'local_path':str(local),'size_bytes':len(raw),'sha256':digest(raw),'git_blob_sha1':oid(raw),'mode':'100644'})
assert len(manifest)==13 and len({r['path'] for r in manifest})==13
for name,value in [('manifest.json',manifest),('tree-elements.json',elements),('preparation.json',guard)]:
    (EXPORT/name).write_text(json.dumps(value,indent=2)+'\n')
print(json.dumps({'parent':a.parent,'paths':13,'active_tooling_paths':9,'evidence_paths':4,'application_promoted':False,'exact_fetched_candidates_and_absence_guards_passed':True}))
