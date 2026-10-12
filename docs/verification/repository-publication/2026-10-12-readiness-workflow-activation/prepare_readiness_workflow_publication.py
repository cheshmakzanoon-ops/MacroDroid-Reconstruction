from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess

BASE = Path('/dev/shm/macrodroid-transfer-space-20261012')
REPO = Path('/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction')
GIT = BASE / 'verification.git'
PARENT = '152a4f28aca596fb6891b14121d0a15dfd1a5283'
TREE = BASE / 'readiness-workflow-tree'
EXPORT = BASE / 'readiness-workflow-export'
TREE.mkdir(exist_ok=False)
EXPORT.mkdir(exist_ok=False)
paths, prefixes, checks, baselines = set(), [], {}, {}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def safe(value):
    path = PurePosixPath(value)
    assert not path.is_absolute() and '..' not in path.parts and path.as_posix() == value
    return value

def git(*args):
    return subprocess.check_output(['git', '--git-dir=' + str(GIT), *args])

def save(name, data):
    name = safe(name)
    assert name not in paths
    p = TREE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(data)
    p.chmod(0o644)
    paths.add(name)

def jsave(name, obj):
    save(name, (json.dumps(obj, indent=2) + '\n').encode())

def link(source, name):
    name = safe(name)
    assert name not in paths and source.is_file() and not source.is_symlink()
    target = TREE / name
    target.parent.mkdir(parents=True, exist_ok=True)
    os.link(source, target)
    paths.add(name)

def capsule(source, target, digest, count):
    source = Path(source)
    raw = (source / 'checkpoint.json').read_bytes()
    assert sha(raw) == digest
    cp = json.loads(raw)
    assert len(cp['files']) == len({safe(r['path']) for r in cp['files']}) == count
    assert not cp.get('android_executed') and not cp.get('active_changes')
    for row in cp['files']:
        p = source / safe(row['path'])
        assert stat.S_ISREG(p.lstat().st_mode) and not p.is_symlink()
        data = p.read_bytes()
        assert len(data) == row['bytes'] and sha(data) == row['sha256']
        mode = stat.S_IMODE(p.stat().st_mode)
        assert mode in (0o644, 0o755)
        if 'mode' in row:
            expected = int(row['mode'], 8) & 0o777 if isinstance(row['mode'], str) else row['mode']
            assert type(expected) is int and expected == mode
        link(p, target + '/' + row['path'])
    link(source / 'checkpoint.json', target + '/checkpoint.json')
    checks[target] = dict(checkpoint_sha256=digest, declared_files=count,
                          bytes=sum(r['bytes'] for r in cp['files']),
                          all_bytes_and_modes_verified=True)
    prefixes.append(target)
    return cp

workflow_source = Path('/dev/shm/macrodroid-notification-readiness/checkpoints/02-thirteen-screen-readiness-workflow')
workflow_target = 'work-in-progress/notification-readiness-workflow/01-thirteen-screen'
capsule(workflow_source, workflow_target,
        '3ca1103f0e247cb827be1d654ce082989658a54cfb8b6b7c4f2c655fd553c50b', 13)
transfer = json.loads((BASE / 'readiness-workflow-verification.json').read_text())
assert transfer['all_frozen_bytes_unchanged'] and transfer['exact_regular_evidence_roles'] == 8641
assert transfer['verified_unique_archive_payloads'] == 276 and transfer['verified_external_runtime_inputs'] == 3
review = capsule('/dev/shm/macrodroid-readiness-workflow-review-03/checkpoints/03-independent-workflow-review',
                 'docs/verification/notification-readiness/03-independent-workflow-review',
                 '1f085ba6562259ee3983d38d084f5ec8d0d1c2f3c23443695e069c50697fddd4', 25)
doc_source = Path('/dev/shm/macrodroid-notification-readiness/checkpoints/03-repository-status-update')
doc = capsule(doc_source, 'work-in-progress/notification-readiness-workflow/02-repository-status-update',
              'c2fe721e7b968356259d151bcf80d61072bd7e73ad0c1683fee720074aadbf3e', 4)
old = git('show', PARENT + ':README.md')
assert len(old) == doc['expected_before']['bytes'] and sha(old) == doc['expected_before']['sha256']
baselines['README.md'] = sha(old)
assert sha((doc_source / 'README.md').read_bytes()) == doc['expected_after']['sha256']
link(doc_source / 'README.md', 'README.md')
active = '.github/workflows/editor-day-time-readiness.yml'
listed = {r.split(b'\t', 1)[1].decode() for r in git('ls-tree', '-rz', PARENT).split(b'\0') if r}
assert active not in listed
assert sha((workflow_source / active).read_bytes()) == '56808b331ec8995c5ebf82a5a55972dfa75c078233247543a5f526f2f0949930'
link(workflow_source / active, active)

ops = 'docs/verification/repository-publication/2026-10-12-readiness-workflow-activation'
for p in (Path(__file__), BASE / 'verify_readiness_workflow_capsule.py', BASE / 'readiness-workflow-verification.json'):
    link(p, ops + '/' + p.name)
link(BASE / 'publication-proof-export/remote-verification.json', ops + '/previous-commit-fetch-verification.json')
jsave(ops + '/activation-scope.json', dict(parent=PARENT,
      prepared_utc=datetime.now(timezone.utc).isoformat(),
      root_activation_clearance_received=True, reviewed_workflow_sha256='56808b331ec8995c5ebf82a5a55972dfa75c078233247543a5f526f2f0949930',
      active_workflow_added=active, expected_workflow_absent=True,
      existing_workflows_preserved=True, application_source_or_apk_changed=False,
      new_android_result_pending=True, checks=checks))
prefixes.append(ops)

ignored = subprocess.run(['git', 'check-ignore', '--stdin', '-z'], cwd=REPO,
                         input=b'\0'.join(p.encode() for p in sorted(paths)) + b'\0', capture_output=True)
assert ignored.returncode in (0, 1)
names = [p.decode() for p in ignored.stdout.split(b'\0') if p]
if names:
    old = git('show', PARENT + ':.gitignore')
    baselines['.gitignore'] = sha(old)
    save('.gitignore', old + ('\n# Preserve reviewed readiness workflow evidence\n' + ''.join('!' + p + '\n' for p in names)).encode())
old = git('show', PARENT + ':.gitattributes')
baselines['.gitattributes'] = sha(old)
save('.gitattributes', old + ('\n# Exact reviewed readiness workflow and evidence bytes\n' + ''.join(p + '/** -text\n' for p in prefixes) + active + ' -text\n').encode())
known = {r.split(b' ', 1)[0].decode() for r in git('rev-list', '--objects', PARENT).splitlines()}
manifest, blobs, texts = [], [], []
for name in sorted(paths):
    p = TREE / name
    data = p.read_bytes()
    oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    row = dict(path=name, local_path=str(p), size_bytes=len(data), sha256=sha(data),
               git_blob_sha1=oid, mode='100755' if p.stat().st_mode & 0o111 else '100644')
    manifest.append(row)
    try:
        content = data.decode('utf-8')
        binary = '\0' in content
    except UnicodeDecodeError:
        binary = True
    if oid in known or binary or len(data) > 250000:
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
for i, chunk in enumerate(chunks):
    (EXPORT / ('text-' + str(i).zfill(2) + '.json')).write_text(json.dumps(chunk, ensure_ascii=False))
for name, obj in [('manifest.json', manifest), ('blobs.json', blobs)]:
    (EXPORT / name).write_text(json.dumps(obj, indent=2) + '\n')
prep = dict(parent=PARENT, paths=len(manifest), bytes=sum(r['size_bytes'] for r in manifest),
            text_chunks=len(chunks), baselines=baselines,
            expected_absent=[active], active_workflow=active,
            active_workflow_sha256='56808b331ec8995c5ebf82a5a55972dfa75c078233247543a5f526f2f0949930',
            new_unique_blobs=len({r['git_blob_sha1'] for r in blobs if not r['known']}), checks=checks)
(EXPORT / 'preparation.json').write_text(json.dumps(prep, indent=2) + '\n')
print(json.dumps(prep))
