"""Recheck exact staged identities and append-only inactive publication boundaries."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--git-dir', required=True)
parser.add_argument('--export', type=Path, required=True)
args = parser.parse_args()
prepared = json.loads((args.export / 'preparation.json').read_bytes())
manifest = json.loads((args.export / 'manifest.json').read_bytes())
parent = prepared['parent']
git = ['git', '--git-dir=' + args.git_dir, '--literal-pathspecs']
assert len(manifest) == len({row['path'] for row in manifest}) == prepared['paths']
assert prepared['active_source_apk_or_workflow_changed'] is False
assert set(prepared['baselines']).issubset({'.gitignore', '.gitattributes'})
entries = {}
for offset in range(0, len(manifest), 150):
    names = [row['path'] for row in manifest[offset:offset + 150]]
    raw = subprocess.check_output(git + ['ls-tree', '-z', parent, '--', *names])
    for item in raw.split(b'\0'):
        if not item:
            continue
        header, name = item.split(b'\t', 1)
        mode, kind, oid = header.decode().split(' ')
        assert kind == 'blob'
        entries[name.decode()] = (mode, oid)
changes, unchanged = [], []
for row in manifest:
    name = row['path']
    pure = PurePosixPath(name)
    assert not pure.is_absolute() and '..' not in pure.parts and pure.as_posix() == name
    assert name.startswith(('docs/', 'work-in-progress/')) or name in prepared['baselines']
    path = Path(row['local_path'])
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode)
    assert ('100755' if mode & 0o111 else '100644') == row['mode']
    raw = path.read_bytes()
    assert len(raw) == row['size_bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == row['git_blob_sha1']
    before = entries.get(name)
    if before == (row['mode'], row['git_blob_sha1']):
        unchanged.append(name)
    elif before is None:
        assert name not in prepared['baselines']
        changes.append(name)
    else:
        assert name in prepared['baselines'] and before[0] == row['mode']
        previous = subprocess.check_output(git + ['cat-file', 'blob', before[1]])
        assert hashlib.sha256(previous).hexdigest() == prepared['baselines'][name]
        assert raw.startswith(previous), 'Repository metadata must only be appended'
        changes.append(name)
result = dict(parent=parent, staged_paths=len(manifest), changed_paths=len(changes),
              unchanged_selected_paths=len(unchanged), staged_exact_bytes_and_modes=True,
              prior_capsules_not_overwritten=True, only_guarded_metadata_appended=True,
              active_source_apk_or_workflow_changed=False,
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              completed_utc=datetime.now(timezone.utc).isoformat())
with (args.export / 'precommit-guard.json').open('x') as stream:
    stream.write(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
