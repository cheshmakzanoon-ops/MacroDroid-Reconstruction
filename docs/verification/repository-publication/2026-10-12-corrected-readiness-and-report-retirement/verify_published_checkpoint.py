"""Read-only Git and staged-byte verification for a closed publication manifest."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, stat, subprocess

p = argparse.ArgumentParser()
p.add_argument('--git-dir', type=Path, required=True)
p.add_argument('--export', type=Path, required=True)
p.add_argument('--commit', required=True)
p.add_argument('--parent', required=True)
a = p.parse_args()
os.environ['GIT_OPTIONAL_LOCKS'] = '0'

def git(*args):
    return subprocess.check_output(['git', '--git-dir=' + str(a.git_dir), *args])

assert git('rev-parse', a.commit + '^').decode().strip() == a.parent
assert subprocess.run(['git', '--git-dir=' + str(a.git_dir), 'merge-base',
                       '--is-ancestor', a.commit, 'refs/heads/main']).returncode == 0
rows = json.loads((a.export / 'manifest.json').read_text())
assert len({r['path'] for r in rows}) == len(rows)
tree = {}
for raw in git('ls-tree', '-rz', '--full-tree', a.commit).split(b'\0'):
    if raw:
        info, path = raw.split(b'\t', 1)
        mode, kind, oid = info.decode().split()
        tree[path.decode()] = (mode, kind, oid)
changed = {n.decode() for n in git('diff-tree', '--no-commit-id', '--name-only', '-r', '-z',
                                 a.parent, a.commit).split(b'\0') if n}
assert changed <= {r['path'] for r in rows}, sorted(changed - {r['path'] for r in rows})
objects = {}
for row in rows:
    assert tree[row['path']] == (row['mode'], 'blob', row['git_blob_sha1']), row['path']
    objects.setdefault(row['git_blob_sha1'], []).append(row)

proc = subprocess.Popen(['git', '--git-dir=' + str(a.git_dir), 'cat-file', '--batch'],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
for oid, bound in objects.items():
    proc.stdin.write((oid + '\n').encode())
    proc.stdin.flush()
    actual_oid, kind, size = proc.stdout.readline().decode().strip().split()
    assert actual_oid == oid and kind == 'blob'
    data = proc.stdout.read(int(size))
    assert proc.stdout.read(1) == b'\n'
    digest = hashlib.sha256(data).hexdigest()
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == oid
    for row in bound:
        assert len(data) == row['size_bytes'] and digest == row['sha256'], row['path']
        path = Path(row['local_path'])
        mode = path.lstat().st_mode
        assert stat.S_ISREG(mode) and not path.is_symlink()
        assert ('100755' if mode & 0o111 else '100644') == row['mode']
        assert path.read_bytes() == data, row['path']
proc.stdin.close()
assert proc.wait() == 0
result = dict(commit=a.commit, parent=a.parent,
              tree=git('rev-parse', a.commit + '^{tree}').decode().strip(),
              verified_paths=len(rows), changed_paths=len(changed),
              verified_unique_blobs=len(objects),
              verified_total_bytes=sum(r['size_bytes'] for r in rows),
              git_mode_size_sha1_sha256_verified=True,
              staged_bytes_and_modes_equal_fetched_git=True,
              source_worktree_or_index_mutated=False,
              source_worktree_alignment_pending=True,
              completed_utc=datetime.now(timezone.utc).isoformat())
(a.export / 'remote-verification.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
