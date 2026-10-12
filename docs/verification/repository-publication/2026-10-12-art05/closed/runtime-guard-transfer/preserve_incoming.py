from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'runtime-guard-transfer'
OLD = '3d4527fbd3d89f2bc27a952f7f7a54aaa0546c3a'
HEAD = '67c85e4e750d539d84bcdb919cb6baf0aa7766f6'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

assert subprocess.run(['git', 'merge-base', '--is-ancestor', OLD, HEAD], cwd=REPO).returncode == 0
ours = {row['path'] for row in json.loads((EXPORT / 'manifest.json').read_text())}
rows = []
for line in git('diff', '--name-status', OLD, HEAD).decode().splitlines():
    status, name = line.split('\t')
    assert status in ('A', 'M'), (status, name)
    assert not PurePosixPath(name).is_absolute() and '..' not in PurePosixPath(name).parts
    assert name not in ours, name
    data = git('show', HEAD + ':' + name)
    mode = git('ls-tree', HEAD, '--', name).decode().split()[0]
    assert mode in ('100644', '100755')
    target = REPO / name
    assert not target.is_symlink()
    if target.exists():
        old = git('show', OLD + ':' + name) if status == 'M' else None
        assert target.is_file() and target.read_bytes() in (data, old), name
    else:
        assert status == 'A', name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    target.chmod(int(mode, 8) & 0o777)
    rows.append(dict(path=name, size_bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                     git_blob_sha1=hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest(), mode=mode))
assert len(rows) == 12
archives = [row for row in rows if row['path'].endswith('/evidence.zip')]
assert len(archives) == 2
for row in archives:
    manifest = json.loads((REPO / row['path']).with_name('manifest.json').read_text())
    assert row['size_bytes'] == manifest['artifact_bytes']
    assert 'sha256:' + row['sha256'] == manifest['artifact_digest']
result = dict(previous_head=OLD, commit=HEAD, files=rows, disjoint_from_pending_publication=True,
              existing_local_files_guarded_against_previous_or_incoming_bytes=True,
              independent_authored_code_not_retested_by_publisher=True)
(EXPORT / 'external-preservation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(dict(paths=len(rows), bytes=sum(row['size_bytes'] for row in rows), head=HEAD)))
