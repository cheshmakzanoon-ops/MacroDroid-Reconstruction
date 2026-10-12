from pathlib import Path
import hashlib
import json
import subprocess

ROOT=Path('/workspace/scratch/4130730d15aa')
REPO=ROOT/'MacroDroid-Reconstruction'
EXPORT=ROOT/'normal-failure-transfer'
source=ROOT/'normal-animation-analysis/checkpoints/02-actual-normal-scale-failure'
prefix='docs/verification/android-normal-animation-3edcddd'
raw=(source/'checkpoint.json').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='6b2acd0dba931cf866c59ca0271361f0cce7f52aa276c400921b73c41bc32ba9'
cp=json.loads(raw);assert len(cp['files'])==19 and cp['active_files']==[]
paths={r['path'] for r in json.loads((EXPORT/'manifest.json').read_text())}
preparation=json.loads((EXPORT/'preparation.json').read_text());baselines=preparation['baselines'];receipts=preparation['receipts']
def sha(data):return hashlib.sha256(data).hexdigest()
def oid(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
for row in cp['files']+[dict(path='checkpoint.json',bytes=len(raw),sha256=sha(raw))]:
    data=(source/row['path']).read_bytes();assert len(data)==row['bytes'] and sha(data)==row['sha256']
    name=prefix+'/'+row['path'];target=REPO/name
    assert not target.exists() and not target.is_symlink(),name
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    target.chmod(0o755 if (source/row['path']).stat().st_mode&0o111 else 0o644);paths.add(name)
name='docs/verification/repository-publication/2026-10-12-normal-failure/scripts/add_normal_failure_analysis.py'
target=REPO/name;assert not target.exists();target.write_bytes(Path(__file__).read_bytes());paths.add(name)
ignored=subprocess.run(['git','check-ignore','--stdin','-z'],cwd=REPO,input=b'\0'.join(p.encode() for p in sorted(paths))+b'\0',capture_output=True)
assert ignored.returncode in (0,1)
names=[n.decode() for n in ignored.stdout.split(b'\0') if n]
if names:
    p=REPO/'.gitignore';p.write_bytes(p.read_bytes()+('\n# Exact independent Normal03 failure analysis\n'+''.join('!'+n+'\n' for n in names)).encode())
    paths.add('.gitignore')
receipts[prefix]['independent_analysis_checkpoint_sha256']=sha(raw)
receipts[prefix]['independent_analysis_files']=19
# Reuse the exporter without repeating the original archive copy or attributes.
script=(ROOT/'prepare_normal_failure_transfer.py').read_text()
exec(compile(script[script.index('known = {'):],str(ROOT/'prepare_normal_failure_transfer.py')+':export','exec'))
