from pathlib import Path
import ast,hashlib,json,re
root=Path('/dev/shm/macrodroid-day-lookup-integration/combined-host-01/repository')
tools=root/'tools/day_trigger_acceptance'
rows=[]
for p in sorted(tools.iterdir()):
 if p.is_file() and p.name!='runtime-files.json':
  raw=p.read_bytes();rows.append({'path':p.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
  if p.suffix=='.py':ast.parse(raw)
assert len(rows)==7
manifest=tools/'runtime-files.json';manifest.write_text(json.dumps({'schema':1,'scope':'Exact isolated combined DayTrigger job tooling; excluded self is pinned by the workflow','files':rows},indent=2,sort_keys=True)+'\n')
digest=hashlib.sha256(manifest.read_bytes()).hexdigest();workflow=root/'.github/workflows/day-trigger-wip-acceptance.yml'
text,n=re.subn(r"DAY_TRIGGER_RUNTIME_MANIFEST_SHA256: '[0-9a-f]{64}'","DAY_TRIGGER_RUNTIME_MANIFEST_SHA256: '"+digest+"'",workflow.read_text());assert n==1;workflow.write_text(text)
print(json.dumps({'runtime_sha256':digest,'workflow_sha256':hashlib.sha256(workflow.read_bytes()).hexdigest(),'source_files':sum(p.is_file() for p in root.rglob('*'))}))
