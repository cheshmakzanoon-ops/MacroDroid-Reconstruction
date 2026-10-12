from pathlib import Path
import hashlib,json,subprocess,shutil
ROOT=Path('/workspace/scratch/4130730d15aa'); REPO=ROOT/'MacroDroid-Reconstruction'
SOURCE=ROOT/'tooling-validation/reconstruction-run-38214498395.zip'
EXPORT=ROOT/'dbcad-source-transfer'; EXPORT.mkdir(exist_ok=True)
PREFIX='docs/verification/source-ci-dbcad968'
EXPECTED_SIZE=188134390
EXPECTED_SHA='da5668cb030718c72a557179b3d38e33769531d497ec5e16d0a45ea2c8f53d88'
known={r.split(b' ',1)[0].decode() for r in subprocess.check_output(['git','rev-list','--objects','--all'],cwd=REPO).splitlines()}
parts=[];virtual=[];whole=hashlib.sha256();offset=0
with SOURCE.open('rb') as f:
 while True:
  data=f.read(8*1024*1024)
  if not data: break
  whole.update(data);digest=hashlib.sha256(data).hexdigest();oid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  path=PREFIX+'/archive/part-'+str(len(parts)+1).zfill(4)+'.bin'
  assert not (REPO/path).exists(),path
  row={'path':path,'size_bytes':len(data),'sha256':digest,'git_blob_sha1':oid,'mode':'100644'}
  parts.append({k:v for k,v in row.items() if k!='mode'})
  virtual.append(row|{'known':oid in known,'encoding':'base64','source_path':str(SOURCE),'source_offset':offset})
  offset+=len(data)
assert offset==EXPECTED_SIZE and whole.hexdigest()==EXPECTED_SHA
manifest={'format':'macrodroid-multipart-artifact','format_version':1,'id':'source-ci-dbcad968-complete-original-zip',
'filename':SOURCE.name,'media_type':'application/zip','purpose':'Exact unmodified original complete hosted source-build artifact ZIP, including all1136 members; runtime scopes are recorded separately.',
'size_bytes':offset,'sha256':whole.hexdigest(),'parts':parts,'source_commit':'dbcad968c5c3e8f084205393a6c0d2d06a203c71',
'workflow_run_id':38214498395,'source_job_id':114695960566,'artifact_id':11731218792,'source_job_conclusion':'success','overall_workflow_conclusion':'failure',
'whole_application_1_to_1_established':False}
target=REPO/PREFIX/'manifest.json';target.parent.mkdir(parents=True,exist_ok=True)
data=(json.dumps(manifest,indent=2)+'\n').encode();assert not target.exists() or target.read_bytes()==data;target.write_bytes(data)
(EXPORT/'virtual-blobs.json').write_text(json.dumps(virtual,indent=2)+'\n')
(EXPORT/'virtual-range-preparation.json').write_text(json.dumps({'source':str(SOURCE),'bytes':offset,'sha256':whole.hexdigest(),'parts':len(parts),'all_part_sha256_git_sha1_verified':True,'repository_parts_materialized':False,'free_bytes':shutil.disk_usage(ROOT).free,'expected_fetch_pack_additional_bytes_upper_estimate':offset+10000000,'projected_free_after_fetch_and_final_materialization':shutil.disk_usage(ROOT).free-offset-10000000},indent=2)+'\n')
print(json.dumps({'parts':len(parts),'virtual_bytes':offset,'free_bytes':shutil.disk_usage(ROOT).free,'projected_final_free_upper_conservative':shutil.disk_usage(ROOT).free-offset-10000000}))

