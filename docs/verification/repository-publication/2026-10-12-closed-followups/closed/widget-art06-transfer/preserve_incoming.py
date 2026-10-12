from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile
import io
import subprocess

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'widget-art06-transfer'
OLD = '55db6717d2ede0f1732b258d97d3106e23a33de5'
HEAD = '827776523128f003761cfb33936b7075ae063271'

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
assert len(rows) == 20
verified_archives = []
for row in rows:
    if not row['path'].endswith('/manifest.json'):
        continue
    path = REPO / row['path']
    metadata = json.loads(path.read_text())
    archive_path = path.parent / 'evidence.zip'
    if 'artifact_bytes' in metadata:
        data = archive_path.read_bytes()
        assert len(data) == metadata['artifact_bytes']
        assert hashlib.sha256(data).hexdigest() == metadata['artifact_digest'].removeprefix('sha256:')
    else:
        assert metadata['format'] == 'macrodroid-multipart-artifact'
        parts = []
        for part in metadata['parts']:
            raw = (REPO / part['path']).read_bytes()
            assert len(raw) == part['size_bytes'] and hashlib.sha256(raw).hexdigest() == part['sha256']
            assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == part['git_blob_sha1']
            parts.append(raw)
        data = b''.join(parts)
        assert len(data) == metadata['size_bytes'] and hashlib.sha256(data).hexdigest() == metadata['sha256']
        archive_path = path
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        members = {item.filename:item for item in z.infolist() if not item.is_dir()}
        assert len(members) == len(metadata['members'])
        for item in metadata['members']:
            raw = z.read(item['path'])
            assert len(raw) == item.get('bytes', item.get('size_bytes')) and hashlib.sha256(raw).hexdigest() == item['sha256']
    verified_archives.append(dict(path=str(archive_path.relative_to(REPO)), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), members=len(members), conclusion=metadata.get('conclusion', 'HISTORICAL_CONTROL_AND_REPLAY_EVIDENCE')))
result = dict(previous_head=OLD, commit=HEAD, files=rows, disjoint_from_pending_publication=True,
              existing_local_files_guarded_against_previous_or_incoming_bytes=True,
              independent_authored_code_not_retested_by_publisher=True, verified_archives=verified_archives)
(EXPORT / 'external-preservation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(dict(paths=len(rows), bytes=sum(row['size_bytes'] for row in rows), head=HEAD)))
