from pathlib import Path
import argparse,gzip,hashlib,json,os
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
r=Path(__file__).resolve().parent;j=json.loads((r/'publication-layout.json').read_text())['payload_mapping'][0]
z=r/j['stored_path'];assert z.stat().st_size==j['stored_bytes'] and hashlib.sha256(z.read_bytes()).hexdigest()==j['stored_sha256']
assert not a.output.exists() and not a.output.is_symlink()
a.output.parent.mkdir(parents=True,exist_ok=True);tmp=a.output.with_name(a.output.name+'.partial');h=hashlib.sha256();size=0
owned=False
try:
 with gzip.open(z,'rb') as src,tmp.open('xb') as dst:
  owned=True
  while b:=src.read(1024*1024):dst.write(b);h.update(b);size+=len(b)
 assert size==j['original_bytes'] and h.hexdigest()==j['original_sha256']
 os.chmod(tmp,j['original_mode']);os.link(tmp,a.output);tmp.unlink();owned=False
except BaseException:
 if owned and tmp.exists():tmp.unlink()
 raise
print(json.dumps({'path':str(a.output),'bytes':size,'sha256':h.hexdigest()}))
