from pathlib import Path
import hashlib,json,subprocess

ROOT=Path('/workspace/scratch/4130730d15aa');REPO=ROOT/'MacroDroid-Reconstruction';EXPORT=ROOT/'dbcad-source-transfer'
SOURCE=ROOT/'combined-cache-retirement/checkpoints/04-hybrid-retirement-receipt'
TARGET='docs/verification/storage-cleanup/combined-cache-retirement/04-hybrid-retirement-receipt'
def sha(data):return hashlib.sha256(data).hexdigest()
def oid(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
prep=json.loads((EXPORT/'preparation.json').read_text())
paths={r['path'] for r in json.loads((EXPORT/'manifest.json').read_text())}
raw=(SOURCE/'checkpoint.json').read_bytes()
assert sha(raw)=='3ad7e773d6e46010ec352f0cd028de4f43b16ed5a6f56eaee9b98ea514b5c2f0'
cp=json.loads(raw)
def save(name,data,mode=0o644):
 p=REPO/name;assert not p.is_symlink() and (not p.exists() or p.read_bytes()==data),name
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);p.chmod(mode);paths.add(name)
for row in cp['files']:
 p=SOURCE/row['path'];data=p.read_bytes()
 assert not p.is_symlink() and len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
 save(TARGET+'/'+row['path'],data,0o755 if p.stat().st_mode&0o111 else 0o644)
save(TARGET+'/checkpoint.json',raw)
save('docs/verification/source-ci-dbcad968/publication/add_hybrid_retirement_to_source.py',Path(__file__).read_bytes())
attrs=REPO/'.gitattributes';data=attrs.read_bytes()
rule=(TARGET+'/** -text\n').encode();assert rule not in data
attrs.write_bytes(data+b'\n# Preserve the exact closed hybrid cache retirement evidence\n'+rule);paths.add('.gitattributes')
virtual={r['path']:r for r in json.loads((EXPORT/'virtual-blobs.json').read_text())}
known={x.split(b' ',1)[0].decode() for x in subprocess.check_output(['git','rev-list','--objects','--all'],cwd=REPO).splitlines()}
manifest=[];blobs=[];texts=[]
for name in sorted(paths):
 if name in virtual:
  v=virtual[name];manifest.append({k:v[k] for k in ['path','size_bytes','sha256','git_blob_sha1','mode']});blobs.append(v);continue
 p=REPO/name;data=p.read_bytes();row={'path':name,'size_bytes':len(data),'sha256':sha(data),'git_blob_sha1':oid(data),'mode':'100755' if p.stat().st_mode&0o111 else '100644'};manifest.append(row)
 try:content=data.decode('utf-8');binary='\0' in content
 except UnicodeDecodeError:binary=True
 if row['git_blob_sha1'] in known or binary or len(data)>250000:
  blobs.append(row|{'known':row['git_blob_sha1'] in known,'encoding':'base64'})
 else:texts.append({'path':name,'mode':row['mode'],'type':'blob','content':content})
chunks=[];chunk=[]
for row in texts:
 if chunk and len(json.dumps(chunk+[row],ensure_ascii=False).encode())>650000:chunks.append(chunk);chunk=[]
 chunk.append(row)
if chunk:chunks.append(chunk)
for i,chunk in enumerate(chunks):(EXPORT/('text-'+str(i).zfill(2)+'.json')).write_text(json.dumps(chunk,ensure_ascii=False))
for name,value in [('manifest.json',manifest),('blobs.json',blobs)]:(EXPORT/name).write_text(json.dumps(value,indent=2)+'\n')
prep.update(files=len(manifest),bytes=sum(r['size_bytes'] for r in manifest),text_chunks=len(chunks),text_entries=len(texts),new_unique_blobs=len({r['git_blob_sha1'] for r in blobs if not r['known']}))
prep['receipts'][TARGET]={'files':len(cp['files']),'checkpoint_sha256':sha(raw)}
(EXPORT/'preparation.json').write_text(json.dumps(prep,indent=2)+'\n')
print(json.dumps(prep))

