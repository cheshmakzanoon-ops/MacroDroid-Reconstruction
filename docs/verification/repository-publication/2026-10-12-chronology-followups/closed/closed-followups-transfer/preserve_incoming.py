from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'closed-followups-transfer'
OLD = 'dbbb89cf4ca65edd3d2c2b96151dadf41aaec514'
HEAD = 'b84f3210b5b5dc6652017080498436f628c22c3a'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

assert git('rev-parse', HEAD + '^').decode().strip() == OLD
own = {r['path'] for r in json.loads((EXPORT / 'manifest.json').read_text())}
changes = git('diff', '--name-status', OLD, HEAD).decode().splitlines()
assert changes == ['A\tdocs/verification/editor-session-guard-fix/FRESH_RERUN.md']
rows = []
for item in changes:
    status, name = item.split('\t')
    assert name not in own and status == 'A'
    data = git('show', HEAD + ':' + name)
    info = git('ls-tree', HEAD, '--', name).decode().strip().split('\t')[0].split()
    mode, kind, oid = info
    assert kind == 'blob' and mode == '100644'
    target = REPO / name
    assert not target.is_symlink()
    if target.exists():
        assert target.read_bytes() == data
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(0o644)
    rows.append(dict(path=name, mode=mode, size_bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), git_blob_sha1=oid))
preparation = json.loads((EXPORT / 'preparation.json').read_text())
for name, expected in preparation['baselines'].items():
    assert hashlib.sha256(git('show', HEAD + ':' + name)).hexdigest() == expected, name
result = dict(old=OLD, head=HEAD, tree=git('rev-parse', HEAD + '^{tree}').decode().strip(), files=rows, baseline_guards_passed=True, external_source_changed=False)
(EXPORT / 'external-preservation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
