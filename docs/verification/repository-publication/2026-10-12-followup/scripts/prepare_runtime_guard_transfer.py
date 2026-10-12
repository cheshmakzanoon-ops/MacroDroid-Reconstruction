from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'runtime-guard-transfer'
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

art03_source = ROOT / 'widget-art-probe/checkpoints/03-hosted-avd-failure'
art03_prefix = 'work-in-progress/widget-art/03-hosted-avd-failure'
art03 = copy_checkpoint(art03_source, art03_prefix, 'ea5a1eef38b70cb45c0079aa4f63b48b66dedecf636a10b00157b571f3969eb3', 'visible_files')
assert len(art03['visible_files']) == 146 and art03['whole_job_passed'] is False and art03['historical_report_relabelled'] is False
assert art03['full_runtime_1_to_1_established'] is False
with zipfile.ZipFile(art03_source / 'artifact.zip') as archive:
    members = {safe(item.filename): item for item in archive.infolist() if not item.is_dir()}
    assert len(members) == len(art03['archive_members']) == 3171
    for row in art03['archive_members']:
        data = archive.read(members[safe(row['path'])])
        assert len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
avd = (art03_source / art03['avd_stdout']['path']).read_bytes()
assert avd == b'MacroDroid_API35_Disposable\r\nOK\r\n'
probe = json.loads((art03_source / art03['original_probe_result']['path']).read_text())
assert probe['status'] == 'ART_WIDGET_EVIDENCE_INVALID'
jsave(art03_prefix + '/publication-verification.json', dict(
    checkpoint_sha256='ea5a1eef38b70cb45c0079aa4f63b48b66dedecf636a10b00157b571f3969eb3',
    visible_files_verified=146, complete_zip_members_verified=3171,
    exact_recorded_avd_bytes_verified=True, historical_status_preserved='ART_WIDGET_EVIDENCE_INVALID',
    whole_job_passed=False, independent_android_rerun=False))
receipts['widget-art03'] = dict(files=146, archive_members=3171, historical_job_passed=False)

art04_source = ROOT / 'widget-art-probe/checkpoints/04-avd-parser-fix'
art04_prefix = 'work-in-progress/widget-art/04-avd-parser-fix'
art04 = copy_checkpoint(art04_source, art04_prefix, '3f1126ec9ee00af1f8b2ca3bcbdb36cbfee1545b229a5cb29705d7bfee3e35dc')
assert len(art04['files']) == 8 and art04['android_executed_during_correction_validation'] is False
assert art04['historical_job_outcome_relabelled'] is False and art04['fresh_android_rerun_required'] is True
artifact = ROOT / 'widget-art-probe/checkpoints/04-avd-parser-fix-evidence.tar.gz'
data = artifact.read_bytes()
assert len(data) == art04['evidence_bundle']['bytes'] == 2065688
assert sha(data) == art04['evidence_bundle']['sha256'] == 'c8db1a8e8722f1c4fff7085a1a9a4c5a7dcc4098be20bafdd755cabccaafe879'
archive_path = art04_prefix + '/evidence-archive/complete-evidence.tar.gz'
save(archive_path, data)
jsave(art04_prefix + '/evidence-archive/manifest.json', dict(
    format='macrodroid-multipart-artifact', format_version=1,
    id='widget-art04-avd-parser-fix-evidence', filename='widget-art04-avd-parser-fix-evidence.tar.gz',
    media_type='application/gzip', purpose='Complete frozen host correction evidence, including every simulated control and old/new recorded-command replay; no new Android execution.',
    size_bytes=len(data), sha256=sha(data), parts=[dict(path=archive_path, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data))]))
compact = []
with tarfile.open(artifact, 'r:gz') as archive:
    members = {safe(item.name): item for item in archive.getmembers() if item.isfile()}
    assert len(members) == len(art04['evidence_files']) == 7297
    for row in art04['evidence_files']:
        name = safe(row['path'])
        data = archive.extractfile(members[name]).read()
        assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
        if '/host-control-evidence/' not in name:
            save(art04_prefix + '/evidence/' + name, data, 0o755 if members[name].mode & 0o111 else 0o644)
            compact.append(name)
fixture = (art04_source / 'fixtures/observed-avd-name-crlf.stdout.txt').read_bytes()
assert fixture == avd and sha(fixture) == '8522ad4bd14867dd505fdecb0e0657c506a22c36d86c8a8634fdfda384bae977'
validation = art04['validation']
assert validation['passed'] is True and validation['historical_android_job_stays_failed'] is True
assert [row['returncode'] for row in validation['replays']] == [2, 0]
assert all(row['command_count'] == 60 and row['android_executed_during_replay'] is False for row in validation['replays'])
jsave(art04_prefix + '/publication-verification.json', dict(
    checkpoint_sha256='3f1126ec9ee00af1f8b2ca3bcbdb36cbfee1545b229a5cb29705d7bfee3e35dc',
    source_package_files_verified=8, full_archive_members_verified=7297,
    directly_readable_evidence_files=len(compact), exact_crlf_fixture_preserved=True,
    old_new_replay_exit_codes=[2, 0], replays_are_host_simulations=True,
    historical_job_status_unchanged=True, fresh_android_run_still_required=True,
    active_workflow_modified=False))
save(art04_prefix + '/PUBLICATION_NOTE.md', b'''# Preserved AVD parser correction

All eight frozen source/package files and the original checkpoint are unchanged. The exact complete archive is available through `evidence-archive/manifest.json`; all 7,297 member sizes and hashes were independently verified. Non-control evidence, both full 60-command host replay streams, original policy source and diffs are directly readable under `evidence/`. All individual synthetic control artifacts remain intact in the complete archive.

The 33-byte CRLF fixture is copied byte-for-byte and marked `-text` in the repository attributes. The old actual Android job remains failed. The new parser's host replay and 31-test result are separate evidence; this inactive checkpoint neither activates a workflow nor claims a fresh Android pass.
''')
receipts['widget-art04'] = dict(source_files=8, archive_members=7297, visible_evidence=len(compact), android_executed=False)

review_source = ROOT / 'editor-session-review/checkpoints/01-read-only-guard-gaps'
review_prefix = 'docs/verification/editor-session-review/01-read-only-guard-gaps'
review = copy_checkpoint(review_source, review_prefix, '6d60482fda212c3cd1d0d8f7aeefa0db138ca94e426de25aae80900d39233ad6')
assert len(review['files']) == 29 and review['active_source_modified'] is False and review['android_executed'] is False
rows = json.loads((review_source / 'synthetic-members.json').read_text())
with zipfile.ZipFile(review_source / 'complete-synthetic-evidence.zip') as archive:
    assert len(archive.infolist()) == len(rows) == 2315
    for row in rows:
        data = archive.read(safe(row['path']))
        assert len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
receipts['editor-session-review'] = dict(files=29, synthetic_members=2315, stale_evidence_false_positive_cases=3, rejecting_digest_control_cases=1, active_code_modified=False)

trigger_source = ROOT / 'trigger-catalog-forward/checkpoints/01-initial-host-failure'
trigger_prefix = 'work-in-progress/trigger-category/01-initial-host-failure'
trigger = copy_checkpoint(trigger_source, trigger_prefix, 'da71fc0760d352cc3f5b58207a1e0c7fc0ce2ffce037717637ba793c8a60166b')
assert len(trigger['files']) == 64 and trigger['android_executed'] is False and trigger['active_changes'] is False
receipts['trigger-category-failure'] = dict(files=64, android_executed=False, active_changes=False)

ops_prefix = 'docs/verification/repository-publication/2026-10-12-followup'
ops_rows = []
for source in [ROOT / 'prepare_runtime_guard_transfer.py', *[ROOT / 'combined-retirement-transfer' / name for name in
        ['manifest.json', 'blobs.json', 'preparation.json', 'external-preservation.json', 'preserve_incoming.py', 'verify_remote.py', 'remote-verification.json']]]:
    name = ('scripts/' + source.name) if source.parent == ROOT else 'closed/combined-retirement-transfer/' + source.name
    data = source.read_bytes()
    save(ops_prefix + '/' + name, data, 0o755 if source.stat().st_mode & 0o111 else 0o644)
    ops_rows.append(dict(path=name, source_path=source.relative_to(ROOT).as_posix(), bytes=len(data), sha256=sha(data)))
jsave(ops_prefix + '/checkpoint.json', dict(scope='Closed transfer receipt and exact authoring scripts', files=ops_rows,
    previous_verified_commit='3d4527fbd3d89f2bc27a952f7f7a54aaa0546c3a', operational_evidence_only=True))

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
rules += ''.join(prefix + '/** -text\n' for prefix in [art03_prefix, art04_prefix, review_prefix, trigger_prefix])
rules += art04_prefix + '/fixtures/observed-avd-name-crlf.stdout.txt -text\n'
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
    baselines=baselines, receipts=receipts, active_app_apk_or_workflow_modified=False)
(EXPORT / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
