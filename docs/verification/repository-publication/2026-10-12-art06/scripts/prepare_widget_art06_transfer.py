from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'widget-art06-transfer'
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
            assert row['mode'] == mode, row['path']
        save(prefix + '/' + row['path'], data, int(mode, 8) & 0o777)
    save(prefix + '/checkpoint.json', raw)
    return cp

art_source = ROOT / 'widget-art-probe/checkpoints/06-art-pass-hidden-workflow-gap'
art_prefix = 'work-in-progress/widget-art/06-art-pass-hidden-workflow-gap'
art = copy_checkpoint(art_source, art_prefix, '6f12e96586f845000f0fe5cbb2f95c8e65e83de6c46113bdf92031ff75a423e4', 'visible_files')
assert len(art['visible_files']) == 158
assert art['status'] == 'ACTUAL_EIGHT_CASE_ART_SUCCESS_WITH_MISSING_ARCHIVED_WORKFLOW_COPY'
assert art['actual_probe_status'] == 'ART_WIDGET_CASES_VERIFIED' and art['actual_job_success'] is True
assert art['complete_artifact_input_copy_audit_passed'] is False
assert art['downloaded_zip_or_report_rewritten'] is False
assert art['full_runtime_1_to_1_established'] is False
archive_path = art_prefix + '/artifact.zip'
archive_data = (REPO / archive_path).read_bytes()
assert len(archive_data) == art['archive']['bytes'] == 4778227
assert sha(archive_data) == art['archive']['sha256'] == '6e6124822bb17bf89b75a1683445b67c527d84ea575776bce315aff0e84a2607'
with zipfile.ZipFile(art_source / 'artifact.zip') as archive:
    infos = {safe(item.filename): item for item in archive.infolist()}
    assert len(infos) == len(archive.infolist()) == len(art['archive_members']) == 7213
    assert 'executed-inputs/.github/workflows/widget-method-probe.yml' not in infos
    for row in art['archive_members']:
        data = archive.read(infos[safe(row['path'])])
        assert len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
    for row in art['visible_files']:
        if row['path'].startswith('extracted/'):
            member = row['path'][len('extracted/'):]
            assert member in infos
            assert (art_source / row['path']).read_bytes() == archive.read(infos[member]), row['path']
workflow = (art_source / 'supplemental-provenance/published-workflow.yml').read_bytes()
assert sha(workflow) == 'b694b68e29dcb815c4dded4aed48773999f1800d5fd489dacbca067926ac32c7'
assert workflow == subprocess.check_output(['git','show','c1a6d71d2e290d16ea3a047d036996f79005883a:.github/workflows/widget-method-probe.yml'],cwd=REPO)
jsave(art_prefix + '/manifest.json', dict(format='macrodroid-multipart-artifact',format_version=1,
    id='widget-art06-actual-guest-success-input-copy-gap',filename='widget-art-run-38207925500.zip',media_type='application/zip',
    purpose='Exact successful eight-case Android ART probe artifact with a separately preserved missing hidden-workflow input-copy audit failure.',
    size_bytes=len(archive_data),sha256=sha(archive_data),parts=[dict(path=archive_path,size_bytes=len(archive_data),sha256=sha(archive_data),git_blob_sha1=oid(archive_data))]))
jsave(art_prefix + '/publication-verification.json',dict(checkpoint_sha256='6f12e96586f845000f0fe5cbb2f95c8e65e83de6c46113bdf92031ff75a423e4',
    frozen_visible_files_verified=158,complete_unchanged_zip_members_verified=7213,visible_extracted_files_match_archive=True,
    actual_probe_status='ART_WIDGET_CASES_VERIFIED',actual_eight_case_probe_success=True,
    complete_artifact_input_copy_audit_passed=False,missing_archived_workflow_not_inserted=True,
    supplemental_published_workflow_git_bytes_verified=True,historical_failed_runs_unchanged=True,
    new_android_commands_executed_by_publisher=False,full_runtime_1_to_1_established=False))
receipts['widget-art06']=dict(visible_files=158,archive_members=7213,actual_guest_probe='ART_WIDGET_CASES_VERIFIED',
    complete_input_copy_audit_passed=False,full_runtime_parity=False)

animation_source = ROOT / 'animation-diagnostic/checkpoints/01-normal-animation-source'
animation_prefix = 'work-in-progress/animation-diagnostic/01-normal-animation-source'
animation = copy_checkpoint(animation_source,animation_prefix,'42a37e351e0a5ef782f12de9b8140f84eebea4363ec39d4a833fc78122acdcad')
assert len(animation['files']) == 7 and animation['android_executed'] is False
inventory=json.loads((animation_source/'host-evidence-manifest.json').read_text())
assert len(inventory['regular_files']) == 512 and len(inventory['symbolic_links_as_inert_metadata']) == 1
with tarfile.open(animation_source/'host-evidence.tar.gz','r:gz') as archive:
    members = {safe(item.name):item for item in archive.getmembers()}
    assert len(members) == len(archive.getmembers()) == 512
    assert all(item.isfile() for item in members.values())
    for row in inventory['regular_files']:
        data=archive.extractfile(members[safe(row['path'])]).read()
        assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
        if '/' not in row['path']:
            save(animation_prefix+'/host-evidence/'+row['path'],data)
receipts['normal-animation01']=dict(source_files=7,regular_archive_members=512,inert_symlink_metadata=1,
    android_executed=False,workflow_activated=False)

ops_prefix = 'docs/verification/repository-publication/2026-10-12-art06'
ops_rows=[]
for source in [ROOT/'prepare_widget_art06_transfer.py',*[ROOT/'ten-indicator-transfer'/name for name in
        ['manifest.json','blobs.json','preparation.json','external-preservation.json','preserve_incoming.py','verify_remote.py','remote-verification.json']]]:
    name=('scripts/'+source.name) if source.parent==ROOT else 'closed/ten-indicator-transfer/'+source.name
    data=source.read_bytes()
    save(ops_prefix+'/'+name,data,0o755 if source.stat().st_mode & 0o111 else 0o644)
    ops_rows.append(dict(path=name,source_path=source.relative_to(ROOT).as_posix(),bytes=len(data),sha256=sha(data)))
jsave(ops_prefix+'/checkpoint.json',dict(scope='Closed transfer receipt and exact authoring scripts',files=ops_rows,
    previous_verified_commit='55db6717d2ede0f1732b258d97d3106e23a33de5',operational_evidence_only=True))

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
rules += ''.join(prefix + '/** -text\n' for prefix in [art_prefix, animation_prefix])
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
        blobs.append(row | dict(known=row['git_blob_sha1'] in known, encoding='base64'))
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
