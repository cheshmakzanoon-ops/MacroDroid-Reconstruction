from pathlib import Path, PurePosixPath
import hashlib
import gzip
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'zero12-evidence-transfer'
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

raw_prefix = 'docs/verification/android-trigger-category-6331410'
source_zip = ROOT / 'ci-run-analysis/zero12-run-38216299675.zip'
source_dir = ROOT / 'ci-run-analysis/zero12-run-38216299675-extracted'
receipt_path = ROOT / 'ci-run-analysis/zero12-run-38216299675-extracted-extraction.json'
receipt_raw = receipt_path.read_bytes()
assert sha(receipt_raw) == 'edb351c8e12f61ee0732643205c98cea7b08af9156e83f72f02736a703773d18'
receipt = json.loads(receipt_raw)
assert receipt['run_id'] == 38216299675
assert receipt['head_sha'] == '6331410cfd2391389270564803623079e8355ad8'
assert receipt['artifact_id'] == 11732104868
assert receipt['member_count'] == len(receipt['files']) == 2944
assert receipt['expanded_bytes'] == 65045879
assert receipt['github_digest_matches'] and receipt['all_extracted_bytes_reverified']
assert receipt['artifact_transformations'] == []
# The exact pinned archive/receipt contains one already-reviewed ephemeral ADB
# public-key line. Root explicitly approved unchanged raw preservation. Its value
# is never printed or copied into a derived summary by this publisher.
assert len(receipt['key_scan_findings']) == 1
assert source_zip.stat().st_size == 42199893
archive_hash = hashlib.sha256()
parts = []
with source_zip.open('rb') as stream:
    while data := stream.read(8 * 1024 * 1024):
        archive_hash.update(data)
        name = raw_prefix + '/archive/part-' + str(len(parts) + 1).zfill(4) + '.bin'
        save(name, data)
        parts.append(dict(path=name, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data)))
archive_digest = archive_hash.hexdigest()
assert archive_digest == '1ea3ad6302d53c2fcc8341c03deec7ccd04d729facaf5658acb87e4aebc6f4b3'
assert sum(p['size_bytes'] for p in parts) == 42199893
save(raw_prefix + '/extraction-receipt.json', receipt_raw)
jsave(raw_prefix + '/manifest.json', dict(
    format='macrodroid-multipart-artifact', format_version=1,
    id='android-trigger-category-run-38216299675', filename=source_zip.name,
    media_type='application/zip', size_bytes=42199893, sha256=archive_digest,
    parts=parts, source_commit=receipt['head_sha'], run_id=receipt['run_id'],
    artifact_id=receipt['artifact_id'],
    purpose='Exact unchanged twelve-screen hosted evidence, including its measured five-pixel rejection and recorded process events.',
    whole_application_1_to_1_established=False))
expected = {row['path']: row for row in receipt['files']}
assert len(expected) == 2944
seen = set()
expanded_bytes = 0
with zipfile.ZipFile(source_zip) as archive:
    members = [member for member in archive.infolist() if not member.is_dir()]
    assert len(members) == 2944
    for member in members:
        name = safe(member.filename)
        assert name in expected and name not in seen
        assert (member.external_attr >> 16) & 0o170000 != 0o120000
        data = archive.read(member)
        row = expected[name]
        assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
        original = source_dir / name
        assert not original.is_symlink() and original.read_bytes() == data, name
        save(raw_prefix + '/extracted/' + name, data,
             0o755 if original.stat().st_mode & 0o111 else 0o644)
        expanded_bytes += len(data)
        seen.add(name)
assert seen == set(expected) and expanded_bytes == 65045879
prefixes.append(raw_prefix)
receipts[raw_prefix] = dict(raw_members=2944, expanded_bytes=expanded_bytes,
    archive_bytes=42199893, archive_sha256=archive_digest, archive_parts=len(parts))
jsave(raw_prefix + '/publication-verification.json', dict(
    all_members_verified=2944, expanded_bytes=expanded_bytes,
    archive_sha256=archive_digest, exact_extraction_receipt_sha256=sha(receipt_raw),
    all_raw_bytes_preserved=True, recompressed=False, executed_artifacts=False,
    approved_raw_public_material_finding_count=1,
    public_material_value_repeated_in_publisher_summary=False,
    whole_application_1_to_1_established=False))
save(raw_prefix + '/RAW_EVIDENCE.md', b'''# Unchanged twelve-screen Android evidence

Run 38216299675 checked out commit
6331410cfd2391389270564803623079e8355ad8. Both original and combined-candidate
journeys completed all twelve declared screens. The exact comparator rejected
five changed pixels on the TRIGGERS intro page; the other eleven paired frames,
including the Date/Time category, matched. Recorded crashes and process events
remain part of the evidence. This is a finite measured journey, and whole-app
runtime parity remains unestablished.

The original 42,199,893-byte ZIP is preserved without recompression in six
ordered archive parts. `manifest.json` binds the complete container for
`scripts/assemble_artifact.py`. All 2,944 exact members are under `extracted/`;
the original extraction receipt is unchanged. Independent replay, full-frame
measurements, source bindings and scope details are under `analysis/`.

The raw emulator log includes one ephemeral ADB public-key line. Its original
bytes are retained as authorized public material, and the value is omitted from
this summary. Any separate review log is explicitly labeled as transformed and
does not replace the original raw member. No private-key finding was reported
by the preserved scan.
''')

cp = package('ci-run-analysis/checkpoints/05-zero12-actual-five-pixel-failure',
    raw_prefix + '/analysis',
    'e918ea97a3f2c217997559430182195d022b1211a31d68aea04b90e1574d3676')
assert cp['active_files'] == [] and cp['original_raw_evidence_modified'] is False

for local, target, digest in [
    ('video-monitor-recovery/checkpoints/15-compiled-retry-controls',
     'work-in-progress/video-monitor/15-compiled-retry-controls',
     '4798b73b02e9e39fe7d4253f8695b393a789bba5b9697e0ca7bc06def2b23c05'),
    ('video-monitor-recovery/checkpoints/16-private-accounting-proposal',
     'work-in-progress/video-monitor/16-private-accounting-proposal',
     'e034fc10772e838eb2a3f5ba225822936da1dbf273141c2cd96b643de03630e2'),
]:
    cp = package(local, target, digest)
    assert cp['raw_original_coverage_gate_passed'] is False
    assert cp['android_executed'] is False and cp['apk_built'] is False
    tar_bundle(cp, target)

for local, target, digest in [
    ('day-time-trigger-forward/checkpoints/01-host-plan-rejection-controls',
     'work-in-progress/day-time-trigger/01-host-plan-rejection-controls',
     '53ab171c643dbebb7093ec4b625ba1f32f6d6950017c6ef7d1890e791975f2fc'),
    ('day-time-trigger-forward/checkpoints/02-host-success',
     'work-in-progress/day-time-trigger/02-host-success',
     '0e010cfbace03cffa6d45e8c9157402b1b68c9a392249eb2aeae39445dc57a7d'),
    ('day-time-trigger-forward/checkpoints/03-zero-scale-thirteen-screen-workflow',
     'work-in-progress/day-time-trigger-workflow/01-zero-scale-workflow',
     '2510711052d2f41bde1a7a583e4bd42f1aab2e1f2001b3bd03d5e2b9eff29229'),
    ('day-trigger-review/checkpoints/01-independent-numeric-review',
     'docs/verification/day-trigger-numeric/01-independent-review',
     '30567165fc992e16e52ef0ba90636d13c17f7560b70c00b4fe1478cf00fbbf4f'),
    ('day-time-trigger-review/checkpoints/01-daytime13-zero12-regression',
     'docs/verification/day-time-trigger/01-source-and-zero12-review',
     '56e52d79069a95d9c503bf643956a6c69a085abc1c7142136a5ff7543625cc51'),
    ('day-trigger-integration/checkpoints/01-integration-design',
     'work-in-progress/day-trigger-numeric/03-integration-design',
     'b04bac0f02ce15afd45039997a4abc1c743d00a2c9108385b4686c58ce16b4cd'),
]:
    package(local, target, digest)

active_workflow = '.github/workflows/editor-day-time-trigger.yml'
workflow_source = ROOT / 'day-time-trigger-forward/checkpoints/03-zero-scale-thirteen-screen-workflow' / active_workflow
workflow_bytes = workflow_source.read_bytes()
assert sha(workflow_bytes) == '74ebef4583e28e345d91c8aa01c0e0723c57c13e6e209084f48e8423751ccbf3'
assert not (REPO / active_workflow).exists()
save(active_workflow, workflow_bytes)
jsave(raw_prefix + '/thirteen-screen-workflow-activation.json', dict(
    reviewed_checkpoint_sha256='2510711052d2f41bde1a7a583e4bd42f1aab2e1f2001b3bd03d5e2b9eff29229',
    workflow_path=active_workflow, workflow_sha256=sha(workflow_bytes),
    root_final_clearance_received=True, independent_review_passed=True,
    prior_twelve_screen_workflow_modified=False, application_or_apk_modified=False,
    new_thirteen_screen_android_result_pending=True))

ops = 'docs/verification/repository-publication/2026-10-12-zero12-evidence'
for p in [ROOT / 'prepare_zero12_evidence_transfer.py', ROOT / 'zero12_evidence_body.py',
          ROOT / 'zero12-evidence-transfer/preparation-attempt01.py',
          ROOT / 'zero12-evidence-transfer/preparation-attempt01.json',
          *[ROOT / 'dbcad-source-transfer' / name for name in [
              'manifest.json', 'blobs.json', 'preparation.json', 'publication_guard.py',
              'publication-guard.json', 'external-preservation.json',
              'remote-byte-verification.json', 'source-download-retirement.json',
              'remote-verification.json']]]:
    name = ('scripts/' if p.parent == ROOT else 'previous-source-publication/') + p.name
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
    baselines=baselines, receipts=receipts, active_workflow_modified=True, active_app_or_apk_modified=False)
(EXPORT / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))

