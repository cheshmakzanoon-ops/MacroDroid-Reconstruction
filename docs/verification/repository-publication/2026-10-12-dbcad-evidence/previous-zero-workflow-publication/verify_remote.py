from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'zero-trigger-transfer'
COMMIT = '6331410cfd2391389270564803623079e8355ad8'
PARENT = 'd5a805d53b7fe166e2c81ed1439d0449defc4dc6'

def run(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

assert run('rev-parse', COMMIT + '^').decode().strip() == PARENT
assert subprocess.run(['git', 'merge-base', '--is-ancestor', COMMIT, 'origin/main'], cwd=REPO).returncode == 0
rows = json.loads((EXPORT / 'manifest.json').read_text())
external = json.loads((EXPORT / 'external-preservation.json').read_text())['files']
rows += external
assert len({r['path'] for r in rows}) == len(rows) == 185
tree = {}
for raw in run('ls-tree', '-rz', '--full-tree', COMMIT).split(b'\0'):
    if not raw:
        continue
    info, path = raw.split(b'\t', 1)
    mode, kind, oid = info.decode().split()
    tree[path.decode()] = (mode, kind, oid)

objects = {}
for row in rows:
    assert tree[row['path']] == (row['mode'], 'blob', row['git_blob_sha1']), row['path']
    objects.setdefault(row['git_blob_sha1'], []).append(row)

p = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=REPO, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
for oid, bound in objects.items():
    p.stdin.write((oid + '\n').encode()); p.stdin.flush()
    actual_oid, kind, size = p.stdout.readline().decode().strip().split()
    assert actual_oid == oid and kind == 'blob'
    data = p.stdout.read(int(size)); assert p.stdout.read(1) == b'\n'
    digest = hashlib.sha256(data).hexdigest()
    git_digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert git_digest == oid
    for row in bound:
        assert len(data) == row['size_bytes'] and digest == row['sha256'], row['path']
p.stdin.close(); assert p.wait() == 0

pending = run('status', '--porcelain=v1', '-z', '--untracked-files=all').split(b'\0')
names = {r['path'] for r in rows}
i = 0
while i < len(pending):
    item = pending[i]; i += 1
    if not item:
        continue
    status = item[:2].decode(); names.add(item[3:].decode())
    if 'R' in status or 'C' in status:
        names.add(pending[i].decode()); i += 1

def fingerprint(name):
    p = REPO / name
    if p.is_symlink():
        return ('symlink', p.readlink().as_posix())
    if not p.exists():
        return None
    assert p.is_file(), name
    return (p.stat().st_mode & 0o777, p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest())

before = {name: fingerprint(name) for name in names}
for row in rows:
    current = before[row['path']]
    assert current is not None and current[1:] == (row['size_bytes'], row['sha256']), row['path']
reset = subprocess.run(['git', 'reset', '--mixed', COMMIT], cwd=REPO, capture_output=True, text=True)
assert reset.returncode == 0, reset.stderr
assert {name: fingerprint(name) for name in names} == before, 'Mixed reset changed working files'
result = dict(commit=COMMIT, parent=PARENT, tree=run('rev-parse', COMMIT + '^{tree}').decode().strip(),
              verified_paths=len(rows), newly_published_paths=185, preserved_external_paths=0,
              verified_unique_blobs=len(objects), verified_total_bytes=sum(r['size_bytes'] for r in rows),
              git_mode_size_sha1_sha256_verified=True, mixed_reset_preserved_fingerprints=len(before),
              status=run('status', '--short', '--untracked-files=normal').decode())
(EXPORT / 'remote-verification.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
