from pathlib import Path, PurePosixPath
import hashlib
import io
import json
import shutil
import subprocess
import tarfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'signed-build-failure-transfer'
EXPORT.mkdir(exist_ok=True)
PART_SIZE = 8 * 1024 * 1024
paths = set()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def oid(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def relative(path):
    p = PurePosixPath(path)
    assert not p.is_absolute() and '..' not in p.parts
    return p.as_posix()


def save(path, data, mode=0o644):
    path = relative(path)
    dst = REPO / path
    assert not dst.is_symlink(), path
    assert not dst.exists() or dst.read_bytes() == data, path
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)
    dst.chmod(mode)
    paths.add(path)


def json_save(path, value):
    save(path, (json.dumps(value, indent=2) + '\n').encode())


def copy_checkpoint(source, destination, digest):
    raw = (source / 'checkpoint.json').read_bytes()
    assert sha(raw) == digest
    checkpoint = json.loads(raw)
    for row in checkpoint['files']:
        path = relative(row['path'])
        src = source / path
        assert not src.is_symlink(), path
        data = src.read_bytes()
        assert len(data) == row.get('bytes', row.get('size_bytes'))
        assert sha(data) == row['sha256'], path
        save(destination + '/' + path, data, 0o755 if src.stat().st_mode & 0o111 else 0o644)
    save(destination + '/checkpoint.json', raw)
    return checkpoint


def multipart_bytes(manifest):
    chunks = []
    for row in manifest['parts']:
        data = (REPO / relative(row['path'])).read_bytes()
        assert len(data) == row['size_bytes'] and sha(data) == row['sha256']
        chunks.append(data)
    data = b''.join(chunks)
    assert len(data) == manifest['size_bytes'] and sha(data) == manifest['sha256']
    return data


def archive_rows(data, expected, review_prefix=None):
    expected = {relative(row['path']): row for row in expected}
    rows = []
    seen = set()
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
        for member in archive.getmembers():
            if member.isdir():
                continue
            assert member.isfile()
            name = relative(member.name)
            assert name not in seen and name in expected, name
            seen.add(name)
            content = archive.extractfile(member).read()
            row = expected[name]
            assert len(content) == row.get('bytes', row.get('size_bytes'))
            assert sha(content) == row['sha256'], name
            rows.append(dict(path=name, size_bytes=len(content), sha256=sha(content)))
            if review_prefix:
                save(review_prefix + '/' + name, content)
    assert seen == set(expected)
    return rows


widget_source = ROOT / 'widget-recovery/checkpoints/06-initial-signed-failure'
widget_prefix = 'work-in-progress/widget-update/06-initial-signed-failure'
widget = copy_checkpoint(widget_source, widget_prefix, '538e2252699bde6e089f49ff0167e620e3b13811cc62b9bff2c3ca7ef947e0ce')
widget_report_manifest = json.loads((REPO / widget_prefix / 'complete-reports/manifest.json').read_text())
widget_inventory = json.loads((REPO / widget_prefix / 'complete-reports-inventory.json').read_text())
widget_report_bytes = multipart_bytes(widget_report_manifest)
widget_members = archive_rows(widget_report_bytes, widget_inventory['files'])
assert len(widget_members) == 40 and sha(widget_report_bytes) == widget_inventory['archive_sha256']
del widget_report_bytes
widget_apk_manifest = json.loads((REPO / widget_prefix / 'apk/manifest.json').read_text())
widget_apk = multipart_bytes(widget_apk_manifest)
assert sha(widget_apk) == widget['apk_sha256']
del widget_apk
json_save(widget_prefix + '/publication-verification.json', dict(
    checkpoint_sha256='538e2252699bde6e089f49ff0167e620e3b13811cc62b9bff2c3ca7ef947e0ce',
    exact_checkpoint_files=len(widget['files']),
    all_listed_bytes_verified=True,
    complete_report_members=len(widget_members),
    complete_report_member_hashes_verified=True,
    complete_report_archive_sha256=widget_inventory['archive_sha256'],
    apk_size_bytes=widget_apk_manifest['size_bytes'],
    apk_sha256=widget_apk_manifest['sha256'],
    all_apk_part_hashes_and_assembly_verified=True,
    status=widget['status'],
    active_source_or_artifact_promoted=False,
))

k_source = ROOT / 'plugin-upload-recovery/checkpoints/03-signed-build'
k_prefix = 'work-in-progress/plugin-upload/03-signed-build'
k = copy_checkpoint(k_source, k_prefix, 'ead8459763abe54786861748b8f8d02bb62625bf986a1bff50cf0ba365c6f746')
k_archive = Path(k['evidence_bundle']['path']).read_bytes()
assert len(k_archive) == k['evidence_bundle']['bytes'] and sha(k_archive) == k['evidence_bundle']['sha256']
k_members = archive_rows(k_archive, k['evidence_files'], k_prefix + '/evidence')
save(k_prefix + '/evidence-archive/evidence.0001.part', k_archive)
json_save(k_prefix + '/evidence-archive/manifest.json', dict(
    format='macrodroid-multipart-artifact', format_version=1,
    id='plugin-upload-03-signed-build-evidence',
    filename='Plugin-upload-03-signed-build-evidence.tar.gz',
    media_type='application/gzip',
    purpose='Complete immutable build-only evidence; subsequent signed proof and controls were pending at freeze',
    size_bytes=len(k_archive), sha256=sha(k_archive),
    parts=[dict(path=k_prefix + '/evidence-archive/evidence.0001.part', size_bytes=len(k_archive), sha256=sha(k_archive), git_blob_sha1=oid(k_archive))],
))
json_save(k_prefix + '/evidence-archive/extraction-receipt.json', dict(
    archive_sha256=sha(k_archive), member_count=len(k_members),
    extracted_bytes=sum(row['size_bytes'] for row in k_members),
    all_member_hashes_match_frozen_checkpoint=True,
    exact_review_copy_prefix=k_prefix + '/evidence', files=k_members,
))

k_apk_path = Path(k['apk']['path'])
before = k_apk_path.stat()
parts = []
total_hash = hashlib.sha256()
total_bytes = 0
with k_apk_path.open('rb') as stream:
    index = 0
    while data := stream.read(PART_SIZE):
        index += 1
        path = k_prefix + f'/artifact/hybrid.{index:04d}.part'
        save(path, data)
        parts.append(dict(path=path, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data)))
        total_hash.update(data)
        total_bytes += len(data)
after = k_apk_path.stat()
assert (before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns)
assert total_bytes == k['apk']['bytes'] and total_hash.hexdigest() == k['apk']['sha256']
json_save(k_prefix + '/artifact/manifest.json', dict(
    format='macrodroid-multipart-artifact', format_version=1,
    id='plugin-upload-03-signed-build-hybrid',
    filename='MacroDroid-5.67.8-plugin-upload-03.apk',
    media_type='application/vnd.android.package-archive',
    purpose='Inactive signed plugin-upload build, before subsequent three-path and 54-control results; not an active release',
    size_bytes=total_bytes, sha256=total_hash.hexdigest(), parts=parts,
    frozen_build_checkpoint_sha256='ead8459763abe54786861748b8f8d02bb62625bf986a1bff50cf0ba365c6f746',
    source_checkpoint_sha256=k['source_checkpoint']['sha256'],
    build_recipe_sha256=k['build_recipe_sha256'],
    recovered_method_bodies=k['registered_bodies'],
    signed_build_passed=True,
    three_path_and_54_controls_complete_at_freeze=False,
    android_runtime_executed=False,
    active_source_or_artifact_promoted=False,
    full_functional_parity_established=False,
))
save(k_prefix + '/README.md', b'''# Inactive plugin-upload signed build

The exact frozen source and isolated build recipe produced the signed APK preserved by `artifact/manifest.json`. Its bytes are bound to the original/JVM checkpoint02 and the immutable build-only `checkpoint.json` in this directory. The complete 14-file build evidence archive and unchanged review copies are retained under `evidence-archive/` and `evidence/`.

This freeze records build completion. Full original/JVM/rebuilt comparison, independent APK verification, all 54 fault controls and positive restoration were pending at freeze; later completion belongs to a separate checkpoint. No Android execution, active registry change or active APK promotion is asserted here. `SIGNED_BUILD_SCOPE.md` records the exact limits and integration boundaries.

The isolated build recipe is evidence. It must not overwrite the active parent's later generated-directory cleanup implementation. The current application remains bound to its separate active manifest.

From the repository root, verify or assemble the exact artifact:

```bash
python3 scripts/assemble_artifact.py work-in-progress/plugin-upload/03-signed-build/artifact/manifest.json --verify-only
python3 scripts/assemble_artifact.py work-in-progress/plugin-upload/03-signed-build/artifact/manifest.json
```
''')
json_save(k_prefix + '/publication-verification.json', dict(
    checkpoint_sha256='ead8459763abe54786861748b8f8d02bb62625bf986a1bff50cf0ba365c6f746',
    exact_checkpoint_files=len(k['files']), all_listed_bytes_verified=True,
    evidence_members=len(k_members), all_evidence_member_hashes_verified=True,
    apk_size_bytes=total_bytes, apk_sha256=total_hash.hexdigest(),
    all_parts_created_from_exact_immutable_apk=True,
    active_source_or_artifact_promoted=False,
))

baselines = {}
amendments = {
    '.gitignore': '\n# Exact original-instruction fixture for inactive signed plugin-upload build\n!work-in-progress/plugin-upload/03-signed-build/tests/fixtures/original-methods.dex\n',
    '.gitattributes': '\n# Immutable inactive signed-build and failure evidence\nwork-in-progress/plugin-upload/03-signed-build/artifact/*.part -text -diff -merge\nwork-in-progress/plugin-upload/03-signed-build/evidence-archive/*.part -text -diff -merge\nwork-in-progress/widget-update/06-initial-signed-failure/apk/*.bin -text -diff -merge\nwork-in-progress/widget-update/06-initial-signed-failure/complete-reports/*.bin -text -diff -merge\n',
}
for name, suffix in amendments.items():
    p = REPO / name
    old = p.read_bytes()
    baselines[name] = sha(old)
    assert suffix.encode() not in old
    p.write_bytes(old + suffix.encode())
    paths.add(name)

known = {line.split(b' ', 1)[0].decode() for line in subprocess.check_output(['git', 'rev-list', '--objects', '--all'], cwd=REPO).splitlines()}
manifest = []
blobs = []
text_entries = []
for path in sorted(paths):
    p = REPO / path
    data = p.read_bytes()
    row = dict(path=path, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data), mode='100755' if p.stat().st_mode & 0o111 else '100644')
    manifest.append(row)
    try:
        text = data.decode('utf-8')
        binary = '\0' in text
    except UnicodeDecodeError:
        binary = True
    if row['git_blob_sha1'] in known or binary or len(data) > 250000:
        blob = row | dict(known=row['git_blob_sha1'] in known)
        if not blob['known']:
            blob['encoding'] = 'base64' if binary or len(data) < 11000000 else 'utf-8'
        blobs.append(blob)
    else:
        text_entries.append(dict(path=path, mode=row['mode'], type='blob', content=text))
chunks = []
chunk = []
for entry in text_entries:
    if chunk and len(json.dumps(chunk + [entry], ensure_ascii=False).encode()) > 650000:
        chunks.append(chunk)
        chunk = []
    chunk.append(entry)
if chunk:
    chunks.append(chunk)
for index, chunk in enumerate(chunks):
    (EXPORT / f'text-{index:02d}.json').write_text(json.dumps(chunk, ensure_ascii=False))
(EXPORT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
(EXPORT / 'blobs.json').write_text(json.dumps(blobs, indent=2) + '\n')
result = dict(files=len(manifest), bytes=sum(r['size_bytes'] for r in manifest), baselines=baselines,
              text_chunks=len(chunks), text_entries=len(text_entries), blob_paths=len(blobs),
              new_blob_paths=sum(not r['known'] for r in blobs),
              new_unique_blobs=len({r['git_blob_sha1'] for r in blobs if not r['known']}),
              new_unique_blob_bytes=sum(r['size_bytes'] for r in {r['git_blob_sha1']:r for r in blobs if not r['known']}.values()),
              frozen_widget_files=len(widget['files']), frozen_plugin_files=len(k['files']),
              widget_report_members=len(widget_members), plugin_report_members=len(k_members))
(EXPORT / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
