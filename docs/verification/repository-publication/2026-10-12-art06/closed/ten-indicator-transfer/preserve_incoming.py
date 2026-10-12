from pathlib import Path, PurePosixPath
import hashlib
import json
import io
import zipfile
import subprocess

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'ten-indicator-transfer'
OLD = 'c1a6d71d2e290d16ea3a047d036996f79005883a'
HEAD = '47458097056fd023bad8b47b6464978b0d02e85c'

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
assert len(rows) == 13
manifest = json.loads((REPO / 'docs/verification/editor-navigation-736da19/manifest.json').read_text())
parts = []
for part in manifest['parts']:
    data = (REPO / part['path']).read_bytes()
    assert len(data) == part['size_bytes']
    assert hashlib.sha256(data).hexdigest() == part['sha256']
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == part['git_blob_sha1']
    parts.append(data)
archive = b''.join(parts)
assert len(archive) == manifest['size_bytes'] == 10661
assert hashlib.sha256(archive).hexdigest() == manifest['sha256'] == '2031b3c1e8989883191966ba9097383717514c63eee76db3c4f3bbc8ca629f00'
with zipfile.ZipFile(io.BytesIO(archive)) as z:
    assert sorted(z.namelist()) == sorted(row['path'] for row in manifest['members'])
    for row in manifest['members']:
        data = z.read(row['path'])
        assert len(data) == row['bytes']
        assert hashlib.sha256(data).hexdigest() == row['sha256']
result = dict(previous_head=OLD, commit=HEAD, files=rows, disjoint_from_pending_publication=True,
              existing_local_files_guarded_against_previous_or_incoming_bytes=True,
              independent_authored_code_not_retested_by_publisher=True, multipart_parts_verified=6, archive_members_verified=6)
(EXPORT / 'external-preservation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(dict(paths=len(rows), bytes=sum(row['size_bytes'] for row in rows), head=HEAD)))
