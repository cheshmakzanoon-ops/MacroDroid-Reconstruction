"""Freeze the actual one-workflow Settings activation and fetched verification."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,stat

BASE=Path('/dev/shm/macrodroid-transfer-space-20261012')
OUT=BASE/'settings-activation-receipts'
TARGET='docs/verification/exact-alarm-enable-return/activation'
COMMIT='88f35e5f1ff52236e8cd51fe0188eabcb4d7bec4'
OUT.mkdir(exist_ok=False)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def copy(src,name):
    path=BASE/src;info=path.lstat();assert stat.S_ISREG(info.st_mode)
    out=OUT/name;out.parent.mkdir(parents=True,exist_ok=True);os.link(path,out)
    assert path.read_bytes()==out.read_bytes()
sources={
 'prepare_settings_enable_return_activation.py':'source/executed-preparer.py',
 'verify_settings_activation_postconditions.py':'source/executed-postconditions-verifier.py',
 'settings-workflow-ready-export/precommit-guard.json':'inactive-publication/precommit-guard.json',
 'settings-workflow-ready-export/remote-verification.json':'inactive-publication/fetched-verification.json',
 'settings-enable-return-activation-export/preparation.json':'activation/preparation.json',
 'settings-enable-return-activation-export/manifest.json':'activation/manifest.json',
 'settings-enable-return-activation-export/tree-elements.json':'activation/tree-elements.json',
 'settings-enable-return-activation-export/remote-verification.json':'activation/fetched-verification.json',
 'settings-enable-return-activation-export/protected-trees-after.json':'activation/protected-trees-after.json',
 'settings-activation-observations/github-runs.json':'github/automatic-runs.json',
 'settings-activation-observations/github-jobs.json':'github/initial-jobs.json',
}
for src,name in sources.items():copy(src,name)
receipt=json.loads((OUT/'activation/fetched-verification.json').read_bytes())
post=json.loads((OUT/'activation/protected-trees-after.json').read_bytes())
runs=json.loads((OUT/'github/automatic-runs.json').read_bytes())['workflow_runs']
jobs=json.loads((OUT/'github/initial-jobs.json').read_bytes())['jobs']
assert receipt['commit']==COMMIT and receipt['verified_paths']==1
assert post['changed_paths']==['.github/workflows/editor-exact-alarm-enable-return.yml']
assert len(post['existing_helpers'])==3 and all(r['unchanged'] for r in post['existing_helpers'])
assert len(runs)==1 and runs[0]['id']==38253349348 and runs[0]['head_sha']==COMMIT
assert len(jobs)==1 and jobs[0]['id']==114824974154
readme=(
 '# Settings enable-and-return activation\n\n'
 'The fetched commit '+COMMIT+' adds exactly one root workflow: .github/workflows/editor-exact-alarm-enable-return.yml '
 '(11,735 bytes, SHA-256 f0b063179dd0f01330787b65908ca861926f16576add80392d5922d2cfd5bbd3). '
 'The inactive package, content-reference reader and final root review were already fetched and verified at a12369837cdd5d6c795726c0de646be5cc52c0d2.\n\n'
 'The three helper paths were already published at their final immutable package locations. Their exact hashes and modes were checked and left unchanged. '
 'All six protected source/artifact/vendor/documentation/package/tool trees and every existing workflow remain unchanged; only the absent root workflow was added.\n\n'
 'One automatic run was observed: 38253349348, job 114824974154. The retained initial metadata records checkout in progress; this checkpoint makes no completed Android claim and no manual dispatch occurred. '
 'The sixteen-screen plan uses the observed off toggle and requires the resulting checked surface before the observed Navigate up input. '
 'Both full-frame and process evidence gates remain strict. The original and numeric 0762 APKs are unchanged.\n')
(OUT/'README.md').write_text(readme)
os.link(Path(__file__),OUT/'source/executed-freezer.py')
files=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file():
        raw=p.read_bytes();files.append(dict(path=p.relative_to(OUT).as_posix(),bytes=len(raw),sha256=digest(raw),mode=stat.S_IMODE(p.lstat().st_mode)))
cp=dict(schema=1,repo_target=TARGET,active_files=[],status='EXACT_SETTINGS_ACTIVATION_AND_AUTOMATIC_RUN_PRESERVED',
        created_utc=datetime.now(timezone.utc).isoformat(),files=files)
raw=(json.dumps(cp,indent=2)+'\n').encode();(OUT/'checkpoint.json').write_bytes(raw)
print(json.dumps(dict(source=str(OUT),target=TARGET,files=len(files),bytes=sum(r['bytes'] for r in files),checkpoint_sha256=digest(raw))))

