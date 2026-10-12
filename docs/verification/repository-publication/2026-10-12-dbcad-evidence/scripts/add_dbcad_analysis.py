from pathlib import Path
import hashlib
import json
import subprocess

ROOT=Path('/workspace/scratch/4130730d15aa')
REPO=ROOT/'MacroDroid-Reconstruction'
EXPORT=ROOT/'dbcad-evidence-transfer'
source=ROOT/'ci-run-analysis/checkpoints/01-dbcad-reconstruction-actual'
prefix='docs/verification/android-ci-dbcad968'
raw=(source/'checkpoint.json').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='a850babb64ceba561fe2adaba04bdcf25545d9091e1a2c6cd99637efe9225e83'
cp=json.loads(raw);assert len(cp['files'])==16 and cp['active_files']==[]
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
name='docs/verification/repository-publication/2026-10-12-dbcad-evidence/scripts/add_dbcad_analysis.py'
target=REPO/name;assert not target.exists();target.write_bytes(Path(__file__).read_bytes());paths.add(name)
ignored=subprocess.run(['git','check-ignore','--stdin','-z'],cwd=REPO,input=b'\0'.join(p.encode() for p in sorted(paths))+b'\0',capture_output=True)
assert ignored.returncode in (0,1)
names=[n.decode() for n in ignored.stdout.split(b'\0') if n]
if names:
    p=REPO/'.gitignore';p.write_bytes(p.read_bytes()+('\n# Exact independent dbcad reconstruction analysis\n'+''.join('!'+n+'\n' for n in names)).encode())
    paths.add('.gitignore')
receipts[prefix]['independent_analysis_checkpoint_sha256']=sha(raw)
receipts[prefix]['independent_analysis_files']=16
# Reuse the exporter without repeating the original archive copy or attributes.
script=(ROOT/'prepare_dbcad_evidence_transfer.py').read_text()
exec(compile(script[script.index('known = {'):],str(ROOT/'prepare_dbcad_evidence_transfer.py')+':export','exec'))
