from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess, tarfile

BASE = Path('/dev/shm/macrodroid-transfer-space-20261012')
REPO = Path('/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction')
GIT = BASE / 'verification.git'
PARENT = '573370e92ca9736c2ae47862989e72ff8c7b8700'
TREE = BASE / 'readiness-publication-tree'
EXPORT = BASE / 'readiness-export'
TREE.mkdir(exist_ok=False)
EXPORT.mkdir(exist_ok=False)
paths, prefixes, checks = set(), [], {}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def safe(name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts and str(p) not in ('', '.')
    return p.as_posix()

def git(*args):
    return subprocess.check_output(['git', '--git-dir=' + str(GIT), *args])

def save(name, data, mode=0o644):
    name = safe(name)
    assert name not in paths
    p = TREE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(data)
    p.chmod(mode)
    paths.add(name)

def jsave(name, obj):
    save(name, (json.dumps(obj, indent=2) + '\n').encode())

def checked(source, row):
    p = source / safe(row['path'])
    s = p.lstat()
    assert stat.S_ISREG(s.st_mode) and not p.is_symlink(), p
    data = p.read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256'], p
    actual = stat.S_IMODE(s.st_mode)
    mode = row.get('mode')
    if mode is not None:
        expected = int(mode, 8) & 0o777 if isinstance(mode, str) else mode
        assert type(expected) is int and expected == actual, (p, expected, actual)
    assert actual in (0o644, 0o755), (p, actual)
    return p

def link(p, name):
    name = safe(name)
    assert name not in paths and p.is_file() and not p.is_symlink()
    dst = TREE / name
    dst.parent.mkdir(parents=True, exist_ok=True)
    os.link(p, dst)
    paths.add(name)

def standard(source, target, expected_sha, count):
    source = Path(source)
    raw = (source / 'checkpoint.json').read_bytes()
    assert sha(raw) == expected_sha
    cp = json.loads(raw)
    assert len(cp['files']) == count
    assert not cp.get('active_files') and not cp.get('active_changes') and not cp.get('android_executed')
    assert len({safe(r['path']) for r in cp['files']}) == count
    for row in cp['files']:
        link(checked(source, row), target + '/' + row['path'])
    link(source / 'checkpoint.json', target + '/checkpoint.json')
    checks[target] = dict(checkpoint_sha256=expected_sha, declared_files=count,
                          bytes=sum(r['bytes'] for r in cp['files']),
                          all_declared_bytes_and_modes_verified=True,
                          active_paths_applied=False)
    prefixes.append(target)
    return cp

target = 'work-in-progress/notification-readiness/01-corrected-host-guard'
cp = standard('/dev/shm/macrodroid-notification-readiness/checkpoints/01-corrected-host-guard',
              target, 'b9d069a653b3ecc483f8e6579ccfb13e5a70450c00015f9a3a31c5277c9a84b3', 140)
assert cp['repo_target'] == target and cp['complete_regression_corpus_executed_here'] is False

target = 'docs/verification/storage-cleanup/combined-generated-cache/03-expanded-report-retirement'
standard(BASE / 'expanded-report-retirement', target,
         'e12a0ea3bdb8d817e4d4952d6e1501a3048537635645f35f55c7ca1b95acf123', 4)
receipt = json.loads((BASE / 'expanded-report-retirement/receipt.json').read_text())
assert receipt['status'] == 'EXACT_PUBLISHED_EXPANDED_REPORT_DUPLICATE_RETIRED'
assert receipt['before']['bytes'] == 97324105 and receipt['after']['bytes'] == 0
assert receipt['protected_control_files_unchanged'] == 1479
assert receipt['source_apk_or_generated_cache_modified'] is False
assert receipt['free_bytes_before'] == 0 and receipt['free_bytes_after'] == 90648576
save(target + '/README.md', b'''# Exact expanded report retirement

Only the redundant expanded retained-classes.json assessment payload was changed.
The fetched compressed representation in commit
573370e92ca9736c2ae47862989e72ff8c7b8700 was compared byte-for-byte with all
97,324,105 original bytes before the exact regular, single-link inode was
truncated to a zero-byte placeholder. Its device, inode and 0644 mode were kept.
The immutable original checkpoint, compressed bytes and decompression/mode
mapping remain preserved in the preceding assessment directory.

All 1,479 protected controls were rehashed unchanged. No canonical source, APK,
generated cache, other report or original checkpoint was retired. The separate
hybrid-smali assessment found zero eligible cache files, so that cache remains
intact. Process visibility limitations in the preceding evidence stay explicit.

Observed free workspace space rose from zero to 90,648,576 bytes at closure on
2026-10-12 at 09:07:15 UTC. This is a point-in-time measurement. The exact executed
operation, before/after inventories and receipt are retained here.
''')

source = Path('/dev/shm/macrodroid-readiness-independent-review-02/checkpoints/02-independent-correction-review')
target = 'docs/verification/notification-readiness/02-independent-correction-review'
raw = (source / 'checkpoint.json').read_bytes()
assert sha(raw) == 'cc55e33d4e115d9240b9ce528c2759bc7a2256ea8a5812eaa206a5c061bdc3f6'
cp = json.loads(raw)
assert cp['activeSourceChanged'] is False and cp['activeRegistryChanged'] is False and cp['androidExecuted'] is False
assert len(cp['sourceFiles']) == 8 and len(cp['readableEvidenceFiles']) == 15
for row in cp['sourceFiles'] + cp['readableEvidenceFiles']:
    link(checked(source, row), target + '/' + row['path'])
a = cp['evidenceArchive']
ap = checked(source, a)
assert a['bytes'] == 140262 and a['sha256'] == '6f5ae6aec4247a1607dc43634f810f7fb3533bc0be680db7a1344ea9a37052cb'
link(ap, target + '/' + a['path'])
with tarfile.open(ap, 'r:gz') as archive:
    all_members = archive.getmembers()
    assert all(m.isfile() or m.isdir() for m in all_members)
    members = {safe(m.name): m for m in all_members if m.isfile()}
    assert len(members) == len([m for m in all_members if m.isfile()]) == len(cp['evidenceFiles']) == 22
    assert set(members) == {safe(r['path']) for r in cp['evidenceFiles']}
    for row in cp['evidenceFiles']:
        m = members[safe(row['path'])]
        data = archive.extractfile(m).read()
        assert len(data) == row['bytes'] and sha(data) == row['sha256']
        assert (m.mode & 0o777) == int(row['mode'], 8)
link(source / 'checkpoint.json', target + '/checkpoint.json')
checks[target] = dict(checkpoint_sha256=sha(raw), source_files=8, readable_reports=15,
                      archive_members=22, archive_sha256=a['sha256'],
                      all_member_bytes_and_modes_verified=True, android_executed=False)
prefixes.append(target)

ops = 'docs/verification/repository-publication/2026-10-12-corrected-readiness-and-report-retirement'
link(Path(__file__), ops + '/prepare_readiness_checkpoint.py')
link(BASE / 'export/remote-verification.json', ops + '/previous-commit-fetch-verification.json')
link(BASE / 'export/publication-guard.json', ops + '/previous-publication-guard.json')
jsave(ops + '/publication-scope.json', dict(parent=PARENT,
      prepared_utc=datetime.now(timezone.utc).isoformat(),
      source_repository_read_only_during_preparation=True,
      active_source_apk_or_workflow_changes=False, checks=checks))
prefixes.append(ops)

baselines = {}
ignored = subprocess.run(['git', 'check-ignore', '--stdin', '-z'], cwd=REPO,
                         input=b'\0'.join(p.encode() for p in sorted(paths)) + b'\0', capture_output=True)
assert ignored.returncode in (0, 1)
names = [v.decode() for v in ignored.stdout.split(b'\0') if v]
if names:
    old = git('show', PARENT + ':.gitignore')
    baselines['.gitignore'] = sha(old)
    save('.gitignore', old + ('\n# Exact corrected readiness and retirement evidence\n' + ''.join('!' + p + '\n' for p in names)).encode())
old = git('show', PARENT + ':.gitattributes')
baselines['.gitattributes'] = sha(old)
save('.gitattributes', old + ('\n# Preserve exact corrected readiness and retirement evidence\n' + ''.join(p + '/** -text\n' for p in prefixes)).encode())
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
prep = dict(parent=PARENT, files=len(manifest), bytes=sum(r['size_bytes'] for r in manifest),
            text_chunks=len(chunks), baselines=baselines,
            new_unique_blobs=len({r['git_blob_sha1'] for r in blobs if not r['known']}),
            checks=checks, active_source_apk_or_workflows_changed=False)
(EXPORT / 'preparation.json').write_text(json.dumps(prep, indent=2) + '\n')
print(json.dumps(prep))
