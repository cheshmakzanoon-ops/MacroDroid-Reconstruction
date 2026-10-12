"""Preserve exact inactive proofs, bounded preparer failure, and fetched activation."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat

ROOT=Path('/dev/shm/macrodroid-transfer-space-20261012')
OUTPUT=ROOT/'indicator-activation-receipts'
TARGET='docs/verification/indicator-fixed-sampling/activation'
OUTPUT.mkdir(exist_ok=False)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def copy(source,name):
    info=source.lstat()
    assert stat.S_ISREG(info.st_mode)
    raw=source.read_bytes()
    path=OUTPUT/name
    path.parent.mkdir(parents=True,exist_ok=True)
    os.link(source,path)
    assert path.read_bytes()==source.read_bytes()==raw

def write(name,value):
    path=OUTPUT/name
    with path.open('xb') as stream:stream.write(value)
    path.chmod(0o644)

for name in (
 'prepare_indicator_fixed_sampling_activation.py',
 'derive_indicator_activation_preparer02.py',
 'prepare_indicator_fixed_sampling_activation02.py',
 'indicator-activation-preparer02.patch',
 'verify_indicator_activation_postconditions.py',
 'freeze_indicator_activation_receipts.py',
):
    copy(ROOT/name,'publication/'+name)
for name in ('executed-preparer.py','observed-execution-output.txt','result.json'):
    copy(ROOT/'indicator-activation-preparer-attempt-01'/name,'attempt-01/'+name)
for name in ('manifest.json','tree-elements.json','preparation.json','remote-verification.json','protected-trees-after.json'):
    copy(ROOT/'indicator-fixed-sampling-activation-export-02'/name,'activation/'+name)
for folder,label in (
 ('indicator-and-numeric-art-progress-export','implementation-publication'),
 ('reviewed-indicator-and-numeric-android-export','reviews-publication'),
):
    for name in ('precommit-guard.json','remote-verification.json'):
        copy(ROOT/folder/name,label+'/'+name)
for name in ('github-runs.json','github-jobs.json'):
    copy(ROOT/'indicator-activation-observations'/name,name)
receipt=json.loads((OUTPUT/'activation/remote-verification.json').read_bytes())
post=json.loads((OUTPUT/'activation/protected-trees-after.json').read_bytes())
assert receipt['commit']=='89c21bff74b854927a25bd33a9f772a59e849321'
assert receipt['verified_paths']==receipt['changed_paths']==16
assert receipt['git_mode_size_sha1_sha256_verified'] is True
assert post['commit']==receipt['commit'] and post['active_application_and_apk_unchanged'] is True
runs=json.loads((OUTPUT/'github-runs.json').read_bytes())['workflow_runs']
assert len(runs)==1 and runs[0]['id']==38252005551 and runs[0]['head_sha']==receipt['commit']
jobs=json.loads((OUTPUT/'github-jobs.json').read_bytes())['jobs']
assert len(jobs)==1 and jobs[0]['id']==114820426338
write('README.md',b"""# Reviewed indicator diagnostic activation

Commit 89c21bff74b854927a25bd33a9f772a59e849321 added exactly the sixteen mappings from the closed implementation 89064abe, after both independent and root review capsules were pushed and fetched. Every target was absent, all source bytes and modes were checked, and all sixteen fetched active files matched. The pinned AAPT2 retains executable mode 100755.

The experiment uses its fixed original and historical 5f635e16 APK pair. The current 0762aad9 application, artifacts, vendor inputs, documentation, work-in-progress history and every other workflow remain unchanged. The exact five protected tree identities and complete changed-path set are recorded.

The initial publisher preparer failed because it looked for the whole candidate APK digest literally inside pins.json. The actual frozen source binds that digest through an exact immutable manifest. The failed source and observed output remain in attempt-01; the narrow successor verifies the actual parent commit, full manifest identity, its old APK digest and the unchanged current APK. No diagnostic source or acceptance rule was altered.

One automatic workflow run was observed: [38252005551](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38252005551), job 114820426338. At the retained observation it was in progress in the bounded synthetic controls. No completed Android or parity outcome is claimed by this activation receipt, and no duplicate dispatch occurred.
""")
files=[]
for path in sorted(OUTPUT.rglob('*')):
    if path.is_file():
        raw=path.read_bytes()
        files.append(dict(path=str(path.relative_to(OUTPUT)),bytes=len(raw),sha256=sha(raw),mode=stat.S_IMODE(path.stat().st_mode)))
write('checkpoint.json',(json.dumps(dict(schema=1,repo_target=TARGET,active_files=[],
    status='EXACT_SIXTEEN_PATH_ACTIVATION_AND_AUTOMATIC_RUN_RECORDED',
    created_utc=datetime.now(timezone.utc).isoformat(),files=files),indent=2)+'\n').encode())
print(json.dumps(dict(source=str(OUTPUT),target=TARGET,files=len(files),
    bytes=sum(r['bytes'] for r in files),checkpoint_sha256=sha((OUTPUT/'checkpoint.json').read_bytes()))))
