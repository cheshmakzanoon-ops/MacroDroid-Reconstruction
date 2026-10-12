from pathlib import Path, PurePosixPath
import hashlib
import gzip
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'daytime13-raw-transfer'
EXPORT.mkdir(exist_ok=True)
paths = set()
receipts = {}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def oid(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def safe(name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts
    return p.as_posix()

def save(name, data, mode=0o644):
    name = safe(name)
    p = REPO / name
    assert not p.is_symlink() and (not p.exists() or p.read_bytes() == data), name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    p.chmod(mode)
    paths.add(name)

def jsave(name, value):
    save(name, (json.dumps(value, indent=2) + '\n').encode())

def copy_checkpoint(source, prefix, expected_sha, list_key='files'):
    raw = (source / 'checkpoint.json').read_bytes()
    assert sha(raw) == expected_sha
    cp = json.loads(raw)
    for row in cp[list_key]:
        p = source / safe(row['path'])
        data = p.read_bytes()
        assert not p.is_symlink()
        assert len(data) == row.get('bytes', row.get('size_bytes')) and sha(data) == row['sha256'], row['path']
        mode = '100755' if p.stat().st_mode & 0o111 else '100644'
        if 'mode' in row:
            assert row['mode'] == ((p.stat().st_mode & 0o777) if type(row['mode']) is int else mode), row['path']
        save(prefix + '/' + row['path'], data, int(mode, 8) & 0o777)
    save(prefix + '/checkpoint.json', raw)
    return cp

prefixes=[]

def package(local, target, digest, key='files'):
 cp=copy_checkpoint(ROOT/local,target,digest,key)
 prefixes.append(target)
 receipts[target]=dict(files=len(cp[key]),checkpoint_sha256=digest)
 return cp

def tar_bundle(cp,target):
 source=Path(cp['evidence_bundle']['path']);data=source.read_bytes()
 assert len(data)==cp['evidence_bundle']['bytes'] and sha(data)==cp['evidence_bundle']['sha256']
 path=target+'/evidence-archive/complete-evidence.tar.gz';save(path,data)
 jsave(target+'/evidence-archive/manifest.json',dict(format='macrodroid-multipart-artifact',format_version=1,id=target.replace('/','-'),
 filename='complete-evidence.tar.gz',media_type='application/gzip',purpose='Exact closed inactive study evidence with the original checkpoint scope preserved.',
 size_bytes=len(data),sha256=sha(data),parts=[dict(path=path,size_bytes=len(data),sha256=sha(data),git_blob_sha1=oid(data))]))
 with tarfile.open(source,'r:gz') as archive:
  members={safe(item.name):item for item in archive.getmembers() if item.isfile()}
  assert len(members)==len(cp['evidence_files'])
  assert all(item.isfile() or item.isdir() for item in archive.getmembers())
  for row in cp['evidence_files']:
   data=archive.extractfile(members[safe(row['path'])]).read()
   assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
   save(target+'/evidence/'+row['path'],data,0o755 if members[row['path']].mode & 0o111 else 0o644)
 receipts[target]['complete_archive_members']=len(cp['evidence_files'])

import os

raw_prefix = 'docs/verification/android-day-time-trigger-e610d98'
source_zip = ROOT / 'ci-run-analysis/daytime13-run-38221713675.zip'
source_dir = ROOT / 'ci-run-analysis/daytime13-run-38221713675-extracted'
receipt_raw = (ROOT / 'ci-run-analysis/daytime13-run-38221713675-extracted-extraction.json').read_bytes()
assert sha(receipt_raw) == '2a76ef4932584ac36223430572710d75aea367631cc4f56f1ffaaedf4b0bd489'
receipt = json.loads(receipt_raw)
assert receipt['run_id'] == 38221713675
assert receipt['head_sha'] == 'e610d98812f3d26da732035e039a1250b8afe9f3'
assert receipt['artifact_id'] == 11735470323
assert receipt['member_count'] == len(receipt['files']) == 2395
assert receipt['expanded_bytes'] == 57260609
assert receipt['github_digest_matches'] and receipt['all_extracted_bytes_reverified']
assert receipt['artifact_transformations'] == []
assert receipt['key_scan_findings'] == ['environment/emulator-boot.log']
classification_raw = (ROOT / 'ci-run-analysis/daytime13-key-scan-classification.json').read_bytes()
classification = json.loads(classification_raw)
assert classification['ephemeral_adb_public_key_setting_lines'] == 1
assert classification['private_key_headers'] == classification['github_token_pattern_matches'] == 0
assert classification['raw_modified'] is False
# Public material remains in the exact authorized raw archive. Its actual value
# is never printed or copied into the publisher's derived summaries.
archive_hash = hashlib.sha256()
parts = []
with source_zip.open('rb') as stream:
    while data := stream.read(8 * 1024 * 1024):
        archive_hash.update(data)
        name = raw_prefix + '/archive/part-' + str(len(parts) + 1).zfill(4) + '.bin'
        save(name, data)
        parts.append(dict(path=name, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data)))
archive_digest = archive_hash.hexdigest()
assert sum(p['size_bytes'] for p in parts) == 38451864
assert archive_digest == 'ad31af7b9fb237dbca1285a671a3e12fdcd9c3cd3754f55064055066043dffa4'
save(raw_prefix + '/extraction-receipt.json', receipt_raw)
save(raw_prefix + '/key-scan-classification.json', classification_raw)
jsave(raw_prefix + '/manifest.json', dict(
    format='macrodroid-multipart-artifact', format_version=1,
    id='android-day-time-trigger-run-38221713675', filename=source_zip.name,
    media_type='application/zip', size_bytes=38451864, sha256=archive_digest,
    parts=parts, source_commit=receipt['head_sha'], run_id=receipt['run_id'],
    artifact_id=receipt['artifact_id'],
    purpose='Exact unchanged hosted thirteen-screen attempt with an incomplete original run and failed final verification.',
    whole_application_1_to_1_established=False))

expected = {row['path']: row for row in receipt['files']}
assert len(expected) == 2395
seen = set()
expanded_bytes = 0
hardlinked = 0
with zipfile.ZipFile(source_zip) as archive:
    members = [member for member in archive.infolist() if not member.is_dir()]
    assert len(members) == 2395
    for member in members:
        name = safe(member.filename)
        assert name in expected and name not in seen
        assert (member.external_attr >> 16) & 0o170000 != 0o120000
        data = archive.read(member)
        row = expected[name]
        assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
        original = source_dir / name
        assert not original.is_symlink() and original.read_bytes() == data, name
        target_name = raw_prefix + '/extracted/' + name
        target = REPO / safe(target_name)
        assert not target.is_symlink()
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert target.samefile(original) and target.read_bytes() == data, name
        else:
            # Exact, closed raw evidence only; never mutable project inputs.
            # Each original member keeps its own inode identity. No content
            # deduplication or chmod/write is performed on either hardlink.
            os.link(original, target)
        assert target.stat().st_ino == original.stat().st_ino
        assert target.stat().st_dev == original.stat().st_dev
        paths.add(target_name)
        expanded_bytes += len(data)
        hardlinked += 1
        seen.add(name)
assert seen == set(expected) and expanded_bytes == 57260609
prefixes.append(raw_prefix)
receipts[raw_prefix] = dict(raw_members=2395, expanded_bytes=expanded_bytes,
    archive_bytes=38451864, archive_sha256=archive_digest, archive_parts=len(parts))
jsave(raw_prefix + '/publication-verification.json', dict(
    all_members_verified=2395, expanded_bytes=expanded_bytes,
    archive_sha256=archive_digest, exact_extraction_receipt_sha256=sha(receipt_raw),
    all_raw_bytes_preserved=True, recompressed=False, executed_artifacts=False,
    immutable_raw_worktree_hardlinks=hardlinked,
    hardlinks_do_not_deduplicate_distinct_raw_member_paths=True,
    approved_raw_public_material_finding_count=1,
    public_material_value_repeated_in_publisher_summary=False,
    whole_application_1_to_1_established=False))
save(raw_prefix + '/RAW_EVIDENCE.md', b'''# Unchanged thirteen-screen Android attempt

Run 38221713675 checked out e610d98812f3d26da732035e039a1250b8afe9f3.
Its original run records FAILED and its candidate run records COMPLETE.
The final verifier records DAY_TIME_TRIGGER_EVIDENCE_INCOMPLETE. These original
results are retained literally; this attempt does not establish a paired
thirteen-screen comparison or whole-application runtime parity.

The original 38,451,864-byte ZIP is preserved without recompression in five
ordered archive parts. `manifest.json` binds the complete container for
`scripts/assemble_artifact.py`. All 2,395 unchanged members are under
`extracted/`; the original extraction receipt is retained. Detailed independent
replay and follow-on observations are separate from these raw bytes.

The source-control worktree uses hardlinks to closed, immutable extracted files
to avoid a second expanded local copy. Each raw member retains its individual
physical identity, and Git independently stores and verifies its content.

One ephemeral ADB public-key line remains in the original emulator log as
authorized public material; its value is omitted from this summary. The scoped
classification found no private-key header or GitHub-token pattern in that
flagged log. Any separately labeled transformed review copy does not replace
the raw member or the original archive.
''')

for local, target, digest in [
    ('day-trigger-lookup-recovery/checkpoints/01-original-java-proof',
     'work-in-progress/day-trigger-lookup/01-original-java-proof',
     '4a39dd17902f68c5cba369fc927f08117ba9905556c7cf2890db8c29e46e9899'),
    ('day-trigger-lookup-recovery/checkpoints/02-three-path-and-compiled-controls',
     'work-in-progress/day-trigger-lookup/02-three-path-and-compiled-controls',
     '6b3cbd47969b8f10675afd8b63dcac40967a7b30748f04b60af4989bea071c29'),
]:
    cp = package(local, target, digest, 'sourceFiles')
    assert cp['activeRegistryChanged'] is False and cp['apkChanged'] is False
    a = cp['evidenceArchive']
    original = ROOT / local / safe(a['path'])
    data = original.read_bytes()
    assert len(data) == a['bytes'] and sha(data) == a['sha256']
    save(target + '/' + a['path'], data)
    with tarfile.open(original, 'r:gz') as archive:
        members = {safe(m.name): m for m in archive.getmembers() if m.isfile()}
        assert all(m.isfile() or m.isdir() for m in archive.getmembers())
        assert len(members) == len(cp['evidenceFiles'])
        for row in cp['evidenceFiles']:
            member = members[safe(row['path'])]
            data = archive.extractfile(member).read()
            assert len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
            save(target + '/evidence/' + row['path'], data,
                 0o755 if member.mode & 0o111 else 0o644)
    receipts[target]['complete_archive_members'] = len(cp['evidenceFiles'])

ops = 'docs/verification/repository-publication/2026-10-12-daytime13-raw'
for p in [ROOT / 'prepare_daytime13_raw_transfer.py', ROOT / 'daytime13_raw_body.py',
          ROOT / 'ci-run-analysis/download_daytime13_38221713675.py',
          ROOT / 'ci-run-analysis/extract_artifact.py',
          ROOT / 'ci-run-analysis/daytime13-run-38221713675.download.json',
          *[ROOT / 'zero12-complete-transfer' / name for name in [
              'manifest.json', 'blobs.json', 'preparation.json', 'publication_guard.py',
              'publication-guard.json', 'external-preservation.json',
              'verify_remote.py', 'remote-verification.json']]]:
    name = ('scripts/' if p.suffix == '.py' else 'receipts/') + p.parent.name + '-' + p.name
    save(ops + '/' + name, p.read_bytes())
prefixes.append(ops)

baselines = {}
ignored_result = subprocess.run(['git', 'check-ignore', '--stdin', '-z'], cwd=REPO,
    input=b'\0'.join(name.encode() for name in sorted(paths)) + b'\0', capture_output=True)
assert ignored_result.returncode in (0, 1)
ignored = [name.decode() for name in ignored_result.stdout.split(b'\0') if name]
if ignored:
    path = REPO / '.gitignore'
    old = path.read_bytes(); baselines['.gitignore'] = sha(old)
    path.write_bytes(old + ('\n# Exact closed runtime and guard-review evidence\n' + ''.join('!' + name + '\n' for name in ignored)).encode())
    paths.add('.gitignore')
path = REPO / '.gitattributes'
old = path.read_bytes(); baselines['.gitattributes'] = sha(old)
rules = '\n# Preserve exact raw device, protocol and synthetic evidence bytes\n'
rules += ''.join(prefix + '/** -text\n' for prefix in prefixes)
path.write_bytes(old + rules.encode()); paths.add('.gitattributes')

known = {line.split(b' ', 1)[0].decode() for line in subprocess.check_output(['git', 'rev-list', '--objects', '--all'], cwd=REPO).splitlines()}
manifest = []; blobs = []; texts = []
for name in sorted(paths):
    p = REPO / name; data = p.read_bytes()
    row = dict(path=name, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data), mode='100755' if p.stat().st_mode & 0o111 else '100644')
    manifest.append(row)
    try:
        content = data.decode('utf-8'); binary = '\0' in content
    except UnicodeDecodeError:
        binary = True
    if row['git_blob_sha1'] in known or binary or len(data) > 250000:
        blobs.append(row | dict(known=row['git_blob_sha1'] in known, encoding='utf-8' if len(data) > 12500000 and data.isascii() else 'base64'))
    else:
        texts.append(dict(path=name, mode=row['mode'], type='blob', content=content))
chunks = []; chunk = []
for entry in texts:
    if chunk and len(json.dumps(chunk + [entry], ensure_ascii=False).encode()) > 650000:
        chunks.append(chunk); chunk = []
    chunk.append(entry)
if chunk:
    chunks.append(chunk)
for index, chunk in enumerate(chunks):
    (EXPORT / f'text-{index:02d}.json').write_text(json.dumps(chunk, ensure_ascii=False))
for name, data in [('manifest.json', manifest), ('blobs.json', blobs)]:
    (EXPORT / name).write_text(json.dumps(data, indent=2) + '\n')
result = dict(files=len(manifest), bytes=sum(row['size_bytes'] for row in manifest), text_chunks=len(chunks),
    text_entries=len(texts), new_unique_blobs=len({row['git_blob_sha1'] for row in blobs if not row['known']}),
    baselines=baselines, receipts=receipts, active_workflow_modified=False, active_app_or_apk_modified=False)
(EXPORT / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))

