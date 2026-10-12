from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,shutil,stat

root=Path('/dev/shm/macrodroid-transfer-space-20261012/numeric-timestamp-review')
shutil.copyfile(Path(__file__),root/Path(__file__).name)
rows=[]
for path in sorted(root.iterdir()):
    value=path.lstat();assert stat.S_ISREG(value.st_mode)
    raw=path.read_bytes();rows.append({'path':path.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'mode':stat.S_IMODE(value.st_mode)})
value={'schema':1,'status':'FROZEN_DETERMINISTIC_TIMESTAMP_PRECISION_REVIEW','created_utc':datetime.now(timezone.utc).isoformat(),
       'repo_target':'docs/verification/day-numeric-hosted-review/04-timestamp-precision','active_files':[],
       'scope':'Read-only invocation of old epoch conversion and a synthetic completion predicate; no full build or Android execution',
       'files':rows}
raw=(json.dumps(value,indent=2)+'\n').encode();(root/'checkpoint.json').write_bytes(raw)
print(json.dumps({'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'files':len(rows),'payload_bytes':sum(r['bytes'] for r in rows)}))
