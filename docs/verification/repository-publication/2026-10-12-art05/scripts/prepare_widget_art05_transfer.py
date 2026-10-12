from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'widget-art05-transfer'
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

art_source = ROOT / 'widget-art-probe/checkpoints/05-rerun-workflow'
art_prefix = 'work-in-progress/widget-art/05-rerun-workflow'
art = copy_checkpoint(art_source, art_prefix, '670bb7a33921547e74460669d940da8cb4f223d17366e28eab7430ac7276c501')
assert len(art['files']) == 6 and art['android_executed'] is False and art['historical_job_relabelled'] is False
baseline = json.loads((art_source / 'baseline-inputs.json').read_text())
assert len(baseline['files']) == 20
for row in baseline['files']:
    p = REPO / safe(row['path'])
    data = p.read_bytes()
    assert not p.is_symlink() and len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
    assert data == subprocess.check_output(['git', 'show', 'bb20c0b5980f8655f30f825b3e7bb95557da2c45:' + row['path']], cwd=REPO), row['path']
artifact = ROOT / 'widget-art-probe/checkpoints/05-rerun-workflow-evidence.tar.gz'
data = artifact.read_bytes()
assert len(data) == art['evidence_bundle']['bytes'] == 2482258
assert sha(data) == art['evidence_bundle']['sha256'] == '72e732b1253e0bbb14990fc2c5b101b30bd70aee6f0561ca94454543f57d402a'
archive_path = art_prefix + '/evidence-archive/complete-evidence.tar.gz'
save(archive_path, data)
jsave(art_prefix + '/evidence-archive/manifest.json', dict(format='macrodroid-multipart-artifact', format_version=1,
    id='widget-art05-rerun-workflow-evidence', filename='widget-art05-rerun-workflow-evidence.tar.gz', media_type='application/gzip',
    purpose='Complete frozen workflow preflight and host control evidence, with historical failure preserved and fresh Android execution pending.',
    size_bytes=len(data), sha256=sha(data), parts=[dict(path=archive_path, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data))]))
compact = []
with tarfile.open(artifact, 'r:gz') as archive:
    members = {safe(item.name): item for item in archive.getmembers() if item.isfile()}
    assert len(members) == len(art['evidence_files']) == 7239
    for row in art['evidence_files']:
        name = safe(row['path']); data = archive.extractfile(members[name]).read()
        assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
        if '/packaged-wrapper-control-evidence/' not in name:
            save(art_prefix + '/evidence/' + name, data, 0o755 if members[name].mode & 0o111 else 0o644)
            compact.append(name)
assert len(compact) == 200
assert art['validation']['passed'] is True and art['validation']['android_executed'] is False
assert len(art['validation']['commands']) == 21
workflow_path = '.github/workflows/widget-method-probe.yml'
workflow = (art_source / workflow_path).read_bytes()
assert sha(workflow) == art['workflow_sha256'] == 'b694b68e29dcb815c4dded4aed48773999f1800d5fd489dacbca067926ac32c7'
assert sha((REPO / workflow_path).read_bytes()) == art['baseline_workflow_sha256'] == '43cf0363c9382083bdeed97f33fd71cfe2905eada2f34dd9e5698900ce226149'
(REPO / workflow_path).write_bytes(workflow)
(REPO / workflow_path).chmod(0o644)
paths.add(workflow_path)
jsave(art_prefix + '/publication-verification.json', dict(frozen_checkpoint_sha256='670bb7a33921547e74460669d940da8cb4f223d17366e28eab7430ac7276c501',
    source_files_verified=6, baseline_dependency_files_verified_in_worktree_and_git=20, complete_archive_members_verified=7239,
    directly_readable_evidence_files=200, offline_command_outcomes_verified=21, workflow_baseline_guard_verified=True,
    active_workflow_sha256=sha(workflow), original_failed_job_status_unchanged=True, fresh_android_result='PENDING',
    application_source_or_apk_modified=False))
receipts['widget-art05'] = dict(source_files=6, complete_archive_members=7239, active_workflow=workflow_path,
    prior_failed_job_preserved=True, android_result_pending=True)

trigger_source = ROOT / 'trigger-catalog-forward/checkpoints/02-reviewed-host-success'
trigger_prefix = 'work-in-progress/trigger-category/02-reviewed-host-success'
trigger = copy_checkpoint(trigger_source, trigger_prefix, '4e3d1ec8d3eec36d6db4685fef8d827c84b4c38e2c550e4a9896fba46eb90f92')
assert len(trigger['files']) == 81 and trigger['android_executed'] is False and trigger['active_changes'] is False
receipts['trigger-category02'] = dict(files=81, android_executed=False, active_changes=False)

ops_prefix = 'docs/verification/repository-publication/2026-10-12-art05'
ops_rows = []
for source in [ROOT / 'prepare_widget_art05_transfer.py', *[ROOT / 'runtime-guard-transfer' / name for name in
        ['manifest.json', 'blobs.json', 'preparation.json', 'external-preservation.json', 'preserve_incoming.py', 'verify_remote.py', 'remote-verification.json']]]:
    name = ('scripts/' + source.name) if source.parent == ROOT else 'closed/runtime-guard-transfer/' + source.name
    data = source.read_bytes()
    save(ops_prefix + '/' + name, data, 0o755 if source.stat().st_mode & 0o111 else 0o644)
    ops_rows.append(dict(path=name, source_path=source.relative_to(ROOT).as_posix(), bytes=len(data), sha256=sha(data)))
jsave(ops_prefix + '/checkpoint.json', dict(scope='Closed transfer receipt and exact authoring scripts', files=ops_rows,
    previous_verified_commit='bb20c0b5980f8655f30f825b3e7bb95557da2c45', operational_evidence_only=True))

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
rules += ''.join(prefix + '/** -text\n' for prefix in [art_prefix, trigger_prefix])
rules += art_prefix + '/evidence/baseline-inputs/work-in-progress/widget-art/04-avd-parser-fix/fixtures/observed-avd-name-crlf.stdout.txt -text\n'
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
    baselines=baselines, receipts=receipts, active_workflow_modified=workflow_path, active_app_or_apk_modified=False)
(EXPORT / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
