python3 -B - <<'PY'
import hashlib, json, os
from pathlib import Path
root = Path('job-source/tools/day_numeric_acceptance')
manifest = root / 'runtime-files.json'
if hashlib.sha256(manifest.read_bytes()).hexdigest() != os.environ['DAY_NUMERIC_RUNTIME_MANIFEST_SHA256']:
    raise SystemExit('Exact hosted tooling manifest differs')
value = json.loads(manifest.read_text())
names = {row['path'] for row in value['files']}
if len(names) != len(value['files']) or names != {path.name for path in root.iterdir() if path.is_file() and path.name != 'runtime-files.json'}:
    raise SystemExit('Hosted tooling inventory differs')
for row in value['files']:
    path = root / row['path']
    if path.is_symlink() or not path.is_file() or path.parent != root:
        raise SystemExit('Invalid hosted tooling file')
    raw = path.read_bytes()
    if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
        raise SystemExit('Hosted tooling bytes differ: ' + row['path'])
Path('hosted-tool-source-verification.json').write_text(json.dumps({'passed': True, 'manifest_sha256': os.environ['DAY_NUMERIC_RUNTIME_MANIFEST_SHA256'], 'files': value['files']}, indent=2) + '\n')
PY
