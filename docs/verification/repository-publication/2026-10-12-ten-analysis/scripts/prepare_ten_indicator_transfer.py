from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess
import tarfile
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
EXPORT = ROOT / 'ten-indicator-transfer'
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

ten_source = ROOT / 'tooling-validation/editor-run-38205737183/analysis'
ten_prefix = 'docs/verification/editor-journey/run-38205737183-attempt-1/analysis'
ten = copy_checkpoint(ten_source, ten_prefix, '89e713db9460523c159dd24387c3401ad7f3551ccd4e1a1b8e2e56457f4e2da7')
assert len(ten['files']) == 764 and ten['active_files'] == [] and ten['full_runtime_1_to_1_established'] is False
assert ten['actual_comparison_status'] == 'JOURNEY_DIFFERENCE'
receipts['ten-analysis'] = dict(files=764, raw_archive_reused=True, actual_verdict_unchanged='JOURNEY_DIFFERENCE')

chronology_source = ROOT / 'tooling-validation/editor-run-38205737183/chronology-followup'
chronology_prefix = 'docs/verification/editor-journey/run-38205737183-attempt-1/analysis-chronology-followup'
chronology = copy_checkpoint(chronology_source, chronology_prefix, '50b8c5997a366f0ddb607fb075009940348e2ba7907ed2c2ca7f1d873682f7d2')
assert len(chronology['files']) == 4
receipts['actual-ten-chronology'] = dict(files=4, frozen_main_analysis_unchanged=True)

indicator_source = ROOT / 'indicator-diagnosis/checkpoints/01-preserved-source-audit'
indicator_prefix = 'docs/verification/indicator-source-audit'
indicator = copy_checkpoint(indicator_source, indicator_prefix, '8792b2936e0d2832361c98699b707ceb7982373cbb661048b549bedfcce174ab')
assert len(indicator['files']) == 28
save(indicator_prefix + '/README.md', b"""# Preserved intro and indicator source audit

The 28 frozen files preserve the exact18 focused intro/indicator classes, the executed audit, context and four existing code/resource reports. The audit concerns source identity and previously measured code roundtrip results. It records no registered reconstruction bodies in those18 classes and keeps the active and inactive build contexts distinct.

This checkpoint does not build an APK, execute Android, or establish the cause of the observed26 TRIGGERS pixels. The exact source, raw retained reports and result remain unchanged. Any diagnostic animation experiment requires its own separately declared run and evidence.
""")
receipts['indicator-source-audit'] = dict(files=28, classes_in_scope=18, android_executed=False, cause_established=False)

review_source = ROOT / 'trigger-category-review/checkpoints/01-stale-terminal-observations'
review_prefix = 'docs/verification/capture-order-review/01-stale-terminal-observations'
review = copy_checkpoint(review_source, review_prefix, '3999f2235075e978ed103fa9c07d87209b79d3fdbba9c1d37f17c6c891d7c741')
assert len(review['files']) == 106 and review['active_source_modified'] is False and review['android_executed'] is False
members = json.loads((review_source / 'synthetic-members.json').read_text())
with zipfile.ZipFile(review_source / 'synthetic-comparator-inputs.zip') as archive:
    assert len(archive.infolist()) == len(members) == 2256
    for row in members:
        data = archive.read(safe(row['path']))
        assert len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
receipts['stale-terminal-review'] = dict(files=106, exact_frozen_input_files=81, synthetic_members=2256,
    incorrect_acceptance_cases=2, rejecting_wrong_tap_controls=2, actual_ten_verdict_unchanged=True)

ops_prefix = 'docs/verification/repository-publication/2026-10-12-ten-analysis'
ops_rows = []
for source in [ROOT / 'prepare_ten_indicator_transfer.py', *[ROOT / 'widget-art05-transfer' / name for name in
        ['manifest.json', 'blobs.json', 'preparation.json', 'verify_remote.py', 'remote-verification.json']]]:
    name = ('scripts/' + source.name) if source.parent == ROOT else 'closed/widget-art05-transfer/' + source.name
    data = source.read_bytes()
    save(ops_prefix + '/' + name, data, 0o755 if source.stat().st_mode & 0o111 else 0o644)
    ops_rows.append(dict(path=name, source_path=source.relative_to(ROOT).as_posix(), bytes=len(data), sha256=sha(data)))
jsave(ops_prefix + '/checkpoint.json', dict(scope='Closed transfer receipt and exact authoring scripts', files=ops_rows,
    previous_verified_commit='c1a6d71d2e290d16ea3a047d036996f79005883a', operational_evidence_only=True))

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
rules += ''.join(prefix + '/** -text\n' for prefix in [ten_prefix, chronology_prefix, indicator_prefix, review_prefix])

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
