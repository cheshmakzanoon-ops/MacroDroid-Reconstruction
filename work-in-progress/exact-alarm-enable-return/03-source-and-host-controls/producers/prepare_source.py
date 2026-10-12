from pathlib import Path
import hashlib,json,shutil,stat
from datetime import datetime,timezone
ROOT=Path('/dev/shm/macrodroid-exact-alarm-enable-return');DESIGN=ROOT/'design-01';PARENT=Path('/dev/shm/macrodroid-exact-alarm-navigation/source-01/repository');OUT=ROOT/'source-01'
assert not OUT.exists()
def identity(p):
 raw=p.read_bytes();return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
assert identity(DESIGN/'checkpoint.json')['sha256']=='d3a8623c00ec814fb92f2cf07d148110efc058c19d40d73450251adeafdd373c'
cp=json.loads((DESIGN/'checkpoint.json').read_text())
for row in cp['files']:assert identity(DESIGN/row['path'])=={k:row[k] for k in ('bytes','sha256')}
inputs=json.loads((DESIGN/'input-identities.json').read_text())['inputs'];rows=[]
for name,pin in inputs.items():
 p=Path(name)
 if not p.is_relative_to(PARENT):continue
 assert not p.is_symlink() and identity(p)==pin
 rows.append({'path':p.relative_to(PARENT).as_posix(),**pin,'mode':stat.S_IMODE(p.stat().st_mode)})
assert len(rows)==98
assert {p.relative_to(PARENT).as_posix() for p in PARENT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}=={r['path'] for r in rows}
OUT.mkdir()
for row in rows:
 p=PARENT/row['path'];t=OUT/'repository'/row['path'];t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,t);assert identity(t)=={k:row[k] for k in ('bytes','sha256')}
for row in rows:assert identity(PARENT/row['path'])=={k:row[k] for k in ('bytes','sha256')}
(OUT/'preparation.json').write_text(json.dumps({'schema':1,'status':'EXACT_98_FILE_GUARD_BASELINE_COPIED','created_utc':datetime.now(timezone.utc).isoformat(),'source':str(PARENT),'design_checkpoint_sha256':identity(DESIGN/'checkpoint.json')['sha256'],'parent_sources_unchanged':True,'files':sorted(rows,key=lambda r:r['path']),'android_actions':[]},indent=2)+'\n')
print('copied',len(rows),'guard source inputs')
