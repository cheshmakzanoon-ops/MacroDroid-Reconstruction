from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import subprocess

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
SOURCE = ROOT / 'editor-observation-forward/checkpoints/02-reference16-compatibility'
EXPORT = ROOT / 'editor02-transfer'
PREFIX = 'docs/verification/editor-observation-policy/02-reference16-compatibility'
HEAD = '590fddb2a4703c56c5520886e68f8366d3727ceb'
OLD = 'a17e119f90418fb642aea4777c0f920bbf9fb92c'
EXPORT.mkdir(exist_ok=True)
paths = set()
def sha(b): return hashlib.sha256(b).hexdigest()
def oid(b): return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
def safe(name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts
    return p.as_posix()
def git(*args): return subprocess.check_output(['git', *args], cwd=REPO)
def save(name, data, mode=0o644):
    name = safe(name); p = REPO / name
    assert not p.is_symlink() and (not p.exists() or p.read_bytes() == data), name
    p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data); p.chmod(mode); paths.add(name)
def jsave(name, value): save(name, (json.dumps(value, indent=2) + '\n').encode())
def row_for(name):
    p = REPO / name; data = p.read_bytes()
    return dict(path=name, size_bytes=len(data), sha256=sha(data), git_blob_sha1=oid(data), mode='100755' if p.stat().st_mode & 0o111 else '100644')

assert git('rev-parse', HEAD + '^').decode().strip() == OLD
external = []
for line in git('diff', '--name-status', OLD, HEAD).decode().splitlines():
    status, name = line.split('\t'); assert status == 'A'
    data = git('show', HEAD + ':' + name)
    mode = git('ls-tree', HEAD, '--', name).decode().split()[0]
    p = REPO / name; assert not p.exists() or p.read_bytes() == data, name
    p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data); p.chmod(int(mode, 8))
    external.append(row_for(name))
assert len(external) == 5
(EXPORT / 'external-preservation.json').write_text(json.dumps(dict(commit=HEAD, files=external), indent=2) + '\n')

raw = (SOURCE / 'checkpoint.json').read_bytes()
assert sha(raw) == 'f8e9e2bdc7d53127a85154b335a9597594ec0d535df7db6b8899938086a855a5'
cp = json.loads(raw); assert len(cp['files']) == 27 and len(cp['active_files']) == 14
assert cp['actual_new_android_result'] == 'PENDING' and cp['full_runtime_1_to_1_established'] is False
for row in cp['files']:
    p = SOURCE / safe(row['path']); data = p.read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
for row in cp['preserved_dependency_bindings']:
    name = safe(row['repository_path']); data = (REPO / name).read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
    assert git('show', HEAD + ':' + name) == data, name
prior = cp['supersedes_inactive_checkpoint']; data = (REPO / prior['repository_path']).read_bytes()
assert len(data) == prior['bytes'] and sha(data) == prior['sha256']
assert git('show', HEAD + ':' + prior['repository_path']) == data

active = []
for row in cp['active_files']:
    name = safe(row['repository_path']); source = SOURCE / safe(row['source_path']); data = source.read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
    p = REPO / name
    if row['baseline_required_absent']:
        absent = subprocess.run(['git', 'cat-file', '-e', HEAD + ':' + name], cwd=REPO, capture_output=True)
        assert absent.returncode != 0 and not p.exists(), name
    else:
        before = p.read_bytes(); assert sha(before) == row['baseline_sha256'], name
        assert git('show', HEAD + ':' + name) == before, name
    active.append((name, data, 0o755 if source.stat().st_mode & 0o111 else 0o644))

log = (SOURCE / 'reports/host-tests-01.log').read_text()
assert sha(log.encode()) == cp['host_gate']['log_sha256']
assert len(re.findall(r'^test[^\n]+ \.\.\. ok$', log, re.M)) == 81
assert re.search(r'Ran 81 tests in 39\.604s\s+OK\s*$', log)
for row in cp['files']:
    p = SOURCE / row['path']; save(PREFIX + '/' + row['path'], p.read_bytes(), 0o755 if p.stat().st_mode & 0o111 else 0o644)
save(PREFIX + '/checkpoint.json', raw)
for name, data, mode in active:
    p = REPO / name; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data); p.chmod(mode); paths.add(name)
jsave(PREFIX + '/publication-verification.json', dict(
    frozen_checkpoint_sha256=sha(raw), observed_parent=HEAD, declared_evidence_files_verified=27,
    active_paths=14, baseline_existing_files_verified=2, baseline_absence_guards_verified=12,
    preserved_dependency_bindings_verified=len(cp['preserved_dependency_bindings']),
    preserved_external_bot_paths=5, host_individual_successes=81, host_seconds=39.604,
    historical_checkpoint01_unchanged=True, actual_new_android_result='PENDING', active_app_or_apk_changed=False))
known = {line.split(b' ', 1)[0].decode() for line in git('rev-list', '--objects', '--all').splitlines()}
rows = []; blobs = []; texts = []
for name in sorted(paths):
    row = row_for(name); rows.append(row); data = (REPO / name).read_bytes()
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
               new_unique_blobs=len({r['git_blob_sha1'] for r in blobs if not r['known']}), parent=HEAD,
               base_tree=git('rev-parse', HEAD + '^{tree}').decode().strip(), active_paths=14,
               preservation_bindings=6, host_tests=81, active_app_or_apk_changed=False)
(EXPORT / 'preparation.json').write_text(json.dumps(summary, indent=2) + '\n'); print(json.dumps(summary))
