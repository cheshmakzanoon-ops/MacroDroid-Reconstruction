import datetime,hashlib,json,os,pathlib,shutil,sys,urllib.request
out=pathlib.Path(sys.argv[2]); expected_size=int(sys.argv[3]); expected_sha=sys.argv[4]
assert not out.exists(), 'refuse overwriting an existing artifact'
assert shutil.disk_usage(out.parent).free > expected_size + 120_000_000, 'insufficient bounded download headroom'
h=hashlib.sha256(); n=0
with urllib.request.urlopen(sys.argv[1],timeout=60) as src, out.open('xb') as dst:
 while True:
  block=src.read(1024*1024)
  if not block: break
  dst.write(block); h.update(block); n+=len(block)
  if n>expected_size: raise ValueError('artifact size exceeds pinned bytes')
assert n==expected_size and h.hexdigest()==expected_sha, 'artifact identity mismatch'
receipt={'path':str(out),'bytes':n,'sha256':h.hexdigest(),'artifact_id':11731218792,'run_id':38214498395,'head_sha':'dbcad968c5c3e8f084205393a6c0d2d06a203c71','downloaded_and_sha256_verified':True,'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'free_bytes_after':shutil.disk_usage(out.parent).free}
out.with_suffix('.download.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
