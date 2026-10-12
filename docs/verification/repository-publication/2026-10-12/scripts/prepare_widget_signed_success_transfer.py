from pathlib import Path, PurePosixPath
import hashlib
import io
import json
import re
import subprocess
import tarfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
SOURCE = ROOT / 'widget-recovery/checkpoints/06-signed-five-gate-success'
EXPORT = ROOT / 'widget-signed-success-transfer'
PREFIX = 'work-in-progress/widget-update/06-signed-five-gate-success'
EXPORT.mkdir(exist_ok=True)
paths = set()
def sha(b): return hashlib.sha256(b).hexdigest()
def oid(b): return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
def safe(name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts
    return p.as_posix()
def save(name, data, mode=0o644):
    name = safe(name); p = REPO / name
    assert not p.is_symlink() and (not p.exists() or p.read_bytes() == data), name
    p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data); p.chmod(mode); paths.add(name)
def jsave(name, value): save(name, (json.dumps(value, indent=2) + '\n').encode())

raw = (SOURCE / 'checkpoint.json').read_bytes()
assert sha(raw) == '51091cf5f03ff60306fccbbb1b8f612c582aa2de489a42bed73a91676662656e'
checkpoint = json.loads(raw)
assert len(checkpoint['files']) == 75 and checkpoint['passed'] is True
for row in checkpoint['files']:
    p = SOURCE / safe(row['path']); data = p.read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
    save(PREFIX + '/' + row['path'], data, 0o755 if p.stat().st_mode & 0o111 else 0o644)
save(PREFIX + '/checkpoint.json', raw)
inventory = json.loads((SOURCE / 'complete-reports-manifest.json').read_text())
parts = []; data_parts = []
for row in inventory['parts']:
    data = (SOURCE / safe(row['path'])).read_bytes()
    assert len(data) == row['bytes'] <= 8388608 and sha(data) == row['sha256']
    parts.append(dict(path=PREFIX + '/' + row['path'], size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data)))
    data_parts.append(data)
archive = b''.join(data_parts)
assert len(archive) == inventory['bytes'] == checkpoint['report_archive']['bytes'] == 16120088
assert sha(archive) == inventory['sha256'] == checkpoint['report_archive']['sha256']
expected = {r['path']: r for r in inventory['files']}
seen = set(); input_manifest_verified = False
with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as t:
    for member in t.getmembers():
        if member.isdir(): continue
        assert member.isfile()
        name = safe(member.name); assert name in expected and name not in seen; seen.add(name)
        data = t.extractfile(member).read(); row = expected[name]
        assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
        if name == 'release-input-snapshot.json':
            assert len(data) == checkpoint['input_manifest']['bytes'] and sha(data) == checkpoint['input_manifest']['sha256']
            snapshot = json.loads(data)
            assert snapshot['snapshot_sha256'] == checkpoint['input_snapshot_sha256']
            assert snapshot['files'] == len(snapshot['entries']) == 81266
            input_manifest_verified = True
assert seen == set(expected) and len(seen) == 71 and input_manifest_verified
manifest = dict(format='macrodroid-multipart-artifact', format_version=1,
                id='widget-06-signed-five-gate-success-reports', filename='Widget-06-signed-five-gate-success-reports.tar.gz',
                media_type='application/gzip', purpose='Complete exact reports for the inactive signed Widget five-gate proof',
                size_bytes=len(archive), sha256=sha(archive), parts=parts)
jsave(PREFIX + '/artifact-manifest.json', manifest)
result = json.loads((SOURCE / 'result.json').read_text())
assert result['passed'] is True and len(result['commands']) == 5
for row in result['fresh_reports'].values(): assert isinstance(row['bytes'], int) and len(row['sha256']) == 64
for name, row in result['fresh_reports'].items():
    data = (SOURCE / 'reviewable' / name).read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
parity = json.loads((SOURCE / 'reviewable/java-all-path-parity.json').read_text())
assert parity['passed'] is True
assert result['cases'] == checkpoint['cases'] == 191133 and result['registered_methods'] == 1241 and result['paths'] == 3
log = (SOURCE / 'reviewable/python-unit-tests.log').read_text()
successes = len(re.findall(r'^test[^\n]+ \.\.\. ok$', log, re.M))
assert successes == 265 and re.search(r'Ran 265 tests in [0-9.]+s\s+OK\s*$', log)
apk_manifest = json.loads((REPO / checkpoint['apk']['manifest_path']).read_text())
assert apk_manifest['sha256'] == checkpoint['apk']['sha256'] == result['apk']['sha256']
assert apk_manifest['size_bytes'] == checkpoint['apk']['bytes'] == result['apk']['bytes']
jsave(PREFIX + '/publication-verification.json', dict(
    frozen_checkpoint_sha256=sha(raw), declared_files_verified=75, complete_report_members_verified=71,
    full_input_manifest_entries_verified=81266, publisher_rehashed_materialized_input_files=False,
    fresh_report_hashes_verified=len(result['fresh_reports']), python_individual_successes=successes,
    exact_archive_sha256=sha(archive), exact_archive_bytes=len(archive), archive_manifest='artifact-manifest.json',
    apk_reused_from=checkpoint['apk']['manifest_path'], apk_durable_commit='5024b1b46056de6a6e76a61883b469521a89ea44',
    duplicate_archive_or_apk_assembly_created=False, active_source_or_apk_changed=False, actual_android_execution=False))

baselines = {}
for name, addition in [('.gitignore', '\n# Exact inactive signed Widget fixture\n!' + PREFIX + '/project/tests/fixtures/original-methods.dex\n'),
                       ('.gitattributes', '\n# Exact complete signed Widget proof archive parts\n' + PREFIX + '/complete-reports.tar.gz.part* -text -diff -merge\n')]:
    p = REPO / name; before = p.read_bytes(); baselines[name] = sha(before)
    assert addition.encode() not in before
    p.write_bytes(before + addition.encode()); paths.add(name)
known = {line.split(b' ', 1)[0].decode() for line in subprocess.check_output(['git', 'rev-list', '--objects', '--all'], cwd=REPO).splitlines()}
rows = []; blobs = []; texts = []
for name in sorted(paths):
    p = REPO / name; data = p.read_bytes()
    row = dict(path=name, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data), mode='100755' if p.stat().st_mode & 0o111 else '100644')
    rows.append(row)
    try: content = data.decode('utf-8'); binary = '\0' in content
    except UnicodeDecodeError: binary = True
    if row['git_blob_sha1'] in known or binary or len(data) > 250000:
        blobs.append(row | dict(known=row['git_blob_sha1'] in known, encoding='base64'))
    else: texts.append(dict(path=name, mode=row['mode'], type='blob', content=content))
chunks = []; chunk = []
for entry in texts:
    if chunk and len(json.dumps(chunk + [entry], ensure_ascii=False).encode()) > 650000: chunks.append(chunk); chunk = []
    chunk.append(entry)
if chunk: chunks.append(chunk)
for i, entries in enumerate(chunks): (EXPORT / f'text-{i:02d}.json').write_text(json.dumps(entries, ensure_ascii=False))
for name, data in [('manifest.json', rows), ('blobs.json', blobs)]: (EXPORT / name).write_text(json.dumps(data, indent=2) + '\n')
summary = dict(files=len(rows), bytes=sum(r['size_bytes'] for r in rows), text_chunks=len(chunks), text_entries=len(texts),
               new_unique_blobs=len({r['git_blob_sha1'] for r in blobs if not r['known']}), baselines=baselines,
               report_members_verified=71, input_manifest_entries_verified=81266, active_source_or_apk_changed=False)
(EXPORT / 'preparation.json').write_text(json.dumps(summary, indent=2) + '\n'); print(json.dumps(summary))
