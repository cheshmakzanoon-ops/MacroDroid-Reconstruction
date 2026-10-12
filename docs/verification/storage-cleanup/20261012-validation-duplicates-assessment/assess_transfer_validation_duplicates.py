from pathlib import Path
import collections
import datetime
import gzip
import hashlib
import json
import os
import stat
import subprocess
import zipfile

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
COMMIT = '55db6717d2ede0f1732b258d97d3106e23a33de5'
OUT = ROOT / 'transfer-validation-assessment'
TARGETS = ['overlay-bootstrap-validation', 'transfer-validation']

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

manifest = json.loads(git('show', COMMIT + ':vendor/v9/manifest.json'))
p = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=REPO,
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE)
archives = []
members = {}
for archive in manifest['archives']:
    whole = hashlib.sha256()
    total = 0
    for part in archive['parts']:
        oid = git('rev-parse', COMMIT + ':' + part['path']).decode().strip()
        assert oid == part['git_blob_sha1']
        p.stdin.write((oid + '\n').encode()); p.stdin.flush()
        actual_oid, kind, size = p.stdout.readline().decode().split()
        assert actual_oid == oid and kind == 'blob' and int(size) == part['size_bytes']
        b = p.stdout.read(int(size)); assert p.stdout.read(1) == b'\n'
        assert hashlib.sha256(b).hexdigest() == part['sha256']
        assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == oid
        whole.update(b); total += len(b)
    assert total == archive['size_bytes'] and whole.hexdigest() == archive['sha256']
    path = ROOT / 'recovered' / archive['filename']
    assert path.stat().st_size == total and digest(path) == whole.hexdigest()
    z = zipfile.ZipFile(path)
    archives.append((archive, z))
    for info in z.infolist():
        assert info.filename not in members
        members[info.filename] = (archive, z, info)
p.stdin.close(); assert p.wait() == 0

rows = []
cache = {}
for name in TARGETS:
    base = ROOT / name
    assert base.is_dir() and not base.is_symlink()
    for folder, dirs, files in os.walk(base, followlinks=False):
        for entry in dirs[:]:
            candidate = Path(folder) / entry
            if candidate.is_symlink():
                dirs.remove(entry)
                rows.append({'path': str(candidate.relative_to(ROOT)), 'kind': 'symlink',
                             'target': os.readlink(candidate), 'removal_candidate': False})
        for entry in files:
            path = Path(folder) / entry
            metadata = path.lstat()
            if not stat.S_ISREG(metadata.st_mode):
                rows.append({'path': str(path.relative_to(ROOT)), 'kind': 'nonregular',
                             'removal_candidate': False})
                continue
            row = {'path': str(path.relative_to(ROOT)), 'kind': 'file',
                   'bytes': metadata.st_size, 'allocated_bytes': metadata.st_blocks * 512,
                   'mode': oct(stat.S_IMODE(metadata.st_mode)), 'sha256': digest(path),
                   'removal_candidate': False}
            parts = path.relative_to(base).parts
            if parts[0].startswith('.materialize-v9-'):
                parts = parts[1:]
            member_name = '/'.join(parts)
            if member_name in members:
                archive, z, info = members[member_name]
                if info.file_size == row['bytes']:
                    if member_name not in cache:
                        h = hashlib.sha256()
                        with z.open(info) as f:
                            for b in iter(lambda: f.read(1024 * 1024), b''):
                                h.update(b)
                        cache[member_name] = h.hexdigest()
                    if row['sha256'] == cache[member_name]:
                        row.update(removal_candidate=True, durable_archive_id=archive['id'],
                                   durable_archive_sha256=archive['sha256'], archive_member=member_name)
            for archive, _ in archives:
                if path.name == archive['filename'] and row['bytes'] == archive['size_bytes'] and row['sha256'] == archive['sha256']:
                    row.update(removal_candidate=True, durable_archive_id=archive['id'],
                               durable_archive_sha256=archive['sha256'], complete_archive=True)
            rows.append(row)
for _, z in archives:
    z.close()

OUT.mkdir(exist_ok=True)
inventory = (json.dumps(rows, sort_keys=True, separators=(',', ':')) + '\n').encode()
with (OUT / 'inventory.json.gz').open('wb') as f:
    with gzip.GzipFile(fileobj=f, mode='wb', mtime=0, filename='') as g:
        g.write(inventory)
summary = {'status': 'READ_ONLY_REMOVAL_CANDIDATE_ASSESSMENT',
           'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'verified_repository_commit': COMMIT, 'source_and_toolchain_git_parts_rehashed': True,
           'no_files_removed': True, 'authoritative_archives_preserved': True,
           'inventory_bytes': len(inventory), 'inventory_sha256': hashlib.sha256(inventory).hexdigest(),
           'targets': {}}
for name in TARGETS:
    group = [row for row in rows if row['path'].startswith(name + '/')]
    candidates = [row for row in group if row['removal_candidate']]
    summary['targets'][name] = {'files': len(group), 'matched_durable_archive_files': len(candidates),
       'matched_logical_bytes': sum(row.get('bytes', 0) for row in candidates),
       'matched_allocated_bytes': sum(row.get('allocated_bytes', 0) for row in candidates),
       'retained_unmatched': [row for row in group if not row['removal_candidate']]}
(OUT / 'assessment.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
