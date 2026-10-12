"""Prepare exact inactive capsules and operation receipts in an owned staging tree."""
from pathlib import Path, PurePosixPath
import argparse, errno, hashlib, json, os, shutil, stat, subprocess

p = argparse.ArgumentParser()
p.add_argument('--configuration', type=Path, required=True)
p.add_argument('--git-dir', type=Path, required=True)
p.add_argument('--repository', type=Path, required=True)
p.add_argument('--tree', type=Path, required=True)
p.add_argument('--export', type=Path, required=True)
a = p.parse_args()
cfg = json.loads(a.configuration.read_text())
parent = cfg['parent']
a.tree.mkdir(exist_ok=False)
a.export.mkdir(exist_ok=False)
names, prefixes, checks, baselines = set(), [], {}, {}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def safe(name):
    value = PurePosixPath(name)
    assert not value.is_absolute() and '..' not in value.parts and value.as_posix() == name
    return name

def git(*args):
    return subprocess.check_output(['git', '--git-dir=' + str(a.git_dir), *args])

def staged(source, name):
    name = safe(name)
    assert name.startswith(('docs/', 'work-in-progress/')) and name not in names
    before = source.lstat()
    assert stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode) in (0o644, 0o755)
    target = a.tree / name
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(source, target)
    except OSError as error:
        if error.errno != errno.EXDEV:
            raise
        with source.open('rb') as src, target.open('xb') as dst:
            shutil.copyfileobj(src, dst)
        target.chmod(stat.S_IMODE(before.st_mode))
    assert source.read_bytes() == target.read_bytes()
    names.add(name)

for item in cfg['capsules']:
    source, prefix = Path(item['source']), safe(item['target'])
    raw = (source / 'checkpoint.json').read_bytes()
    assert sha(raw) == item['checkpoint_sha256']
    cp = json.loads(raw)
    assert not cp.get('active_files') and not cp.get('active_changes') and not cp.get('android_executed_here')
    assert len(cp['files']) == len({safe(r['path']) for r in cp['files']}) == item['files']
    for row in cp['files']:
        path = source / row['path']
        data = path.read_bytes()
        assert len(data) == row['bytes'] and sha(data) == row['sha256']
        if 'mode' in row:
            mode = int(row['mode'], 8) & 0o777 if isinstance(row['mode'], str) else row['mode']
            assert type(mode) is int and stat.S_IMODE(path.lstat().st_mode) == mode
        mapping = item.get('archive_mapping')
        if mapping and row['path'] == mapping['logical_path']:
            assert item['checkpoint_sha256'] == '14bd536aa8af2e8458d8c3b1d45de6c770e55ce4e7f0f5e152a70bc6ed79e0bb'
            assert prefix == 'work-in-progress/day-numeric-art/04-wrapper-host-controls'
            assert row['path'] == 'evidence.tar.gz' and row['bytes'] == 16898593
            assert row['sha256'] == '56e15009933932b5f197d4f985f4cd7677116b74bf5b3484a36fcbb4088ee47f'
            transport_root = Path(mapping['source'])
            manifest_raw = (transport_root / 'manifest.json').read_bytes()
            assert sha(manifest_raw) == mapping['manifest_sha256']
            transport = json.loads(manifest_raw)
            assert transport['format'] == 'macrodroid-multipart-artifact' and transport['format_version'] == 1
            assert transport['filename'] == row['path'] and transport['mode'] == '100644'
            assert transport['logical_repository_path'] == prefix + '/' + row['path']
            assert transport['source_checkpoint']['sha256'] == item['checkpoint_sha256']
            assert len(transport['parts']) == 3 and len({x['path'] for x in transport['parts']}) == 3
            checksum, byte_count = hashlib.sha256(), 0
            for index, part in enumerate(transport['parts'], 1):
                part_name = 'parts/evidence.' + str(index).zfill(4) + '.part'
                assert part['path'] == prefix + '/archive-layout/' + part_name
                part_file = transport_root / part_name
                info = part_file.lstat()
                assert stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o644
                payload = part_file.read_bytes()
                assert len(payload) == part['size_bytes'] and 0 < len(payload) <= 8388608
                assert sha(payload) == part['sha256']
                assert hashlib.sha1(b'blob ' + str(len(payload)).encode() + b'\0' + payload).hexdigest() == part['git_blob_sha1']
                assert payload == data[byte_count:byte_count + len(payload)]
                checksum.update(payload)
                byte_count += len(payload)
            assert byte_count == row['bytes'] == transport['size_bytes']
            assert checksum.hexdigest() == row['sha256'] == transport['sha256']
        else:
            staged(path, prefix + '/' + row['path'])
    staged(source / 'checkpoint.json', prefix + '/checkpoint.json')
    prefixes.append(prefix)
    checks[prefix] = dict(checkpoint_sha256=item['checkpoint_sha256'], files=item['files'],
                          bytes=sum(r['bytes'] for r in cp['files']), exact_bytes_and_modes_verified=True)
    if item.get('archive_mapping'):
        checks[prefix]['archive_transport'] = dict(logical_path=item['archive_mapping']['logical_path'],
            direct_original_payloads=25, original_checkpoint_preserved=True,
            manifest_path=prefix + '/archive-layout/manifest.json',
            manifest_sha256=item['archive_mapping']['manifest_sha256'],
            complete_original_archive_byte_equality_verified=True,
            complete_capsule_requires_archive_reassembly=True)
ops = cfg['operations_prefix']
staged(Path(__file__), ops + '/prepare_standard_capsules.py')
staged(a.configuration, ops + '/configuration.json')
for row in cfg.get('operations', []):
    source = Path(row['source'])
    if 'sha256' in row:
        assert sha(source.read_bytes()) == row['sha256']
    staged(source, ops + '/' + safe(row['name']))
prefixes.append(ops)

ignored = subprocess.run(['git', 'check-ignore', '--stdin', '-z'], cwd=a.repository,
                         input=b'\0'.join(n.encode() for n in sorted(names)) + b'\0', capture_output=True)
assert ignored.returncode in (0, 1)
exceptions = [n.decode() for n in ignored.stdout.split(b'\0') if n]
for name, additions in [('.gitignore', ''.join('!' + n + '\n' for n in exceptions)),
                        ('.gitattributes', ''.join(n + '/** -text\n' for n in prefixes))]:
    if additions:
        old = git('show', parent + ':' + name)
        baselines[name] = sha(old)
        (a.tree / name).write_bytes(old + ('\n# Preserve exact closed capsule bytes\n' + additions).encode())
        (a.tree / name).chmod(0o644)
        names.add(name)
known = {r.split(b' ', 1)[0].decode() for r in git('rev-list', '--objects', parent).splitlines()}
manifest, blobs, texts = [], [], []
for name in sorted(names):
    path = a.tree / name
    raw = path.read_bytes()
    oid = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    row = dict(path=name, local_path=str(path), size_bytes=len(raw), sha256=sha(raw), git_blob_sha1=oid,
               mode='100755' if path.stat().st_mode & 0o111 else '100644')
    manifest.append(row)
    try:
        content = raw.decode('utf-8')
        binary = '\0' in content
    except UnicodeDecodeError:
        binary = True
    if oid in known or binary or len(raw) > 250000:
        blobs.append(row | dict(known=oid in known, encoding='base64'))
    else:
        texts.append(dict(path=name, mode=row['mode'], type='blob', content=content))
chunks, chunk = [], []
for entry in texts:
    if chunk and len(json.dumps(chunk + [entry], ensure_ascii=False).encode()) > 650000:
        chunks.append(chunk)
        chunk = []
    chunk.append(entry)
if chunk:
    chunks.append(chunk)
for index, chunk in enumerate(chunks):
    (a.export / ('text-' + str(index).zfill(2) + '.json')).write_text(json.dumps(chunk, ensure_ascii=False))
for name, value in [('manifest.json', manifest), ('blobs.json', blobs)]:
    (a.export / name).write_text(json.dumps(value, indent=2) + '\n')
prepared = dict(parent=parent, paths=len(manifest), bytes=sum(r['size_bytes'] for r in manifest),
                text_chunks=len(chunks), baselines=baselines, checks=checks,
                new_unique_blobs=len({r['git_blob_sha1'] for r in blobs if not r['known']}),
                active_source_apk_or_workflow_changed=False)
(a.export / 'preparation.json').write_text(json.dumps(prepared, indent=2) + '\n')
print(json.dumps(prepared))
