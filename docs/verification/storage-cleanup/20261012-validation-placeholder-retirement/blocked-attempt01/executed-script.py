from pathlib import Path
import datetime
import gzip
import hashlib
import json
import os
import shutil
import stat
import subprocess

ROOT = Path('/workspace/scratch/4130730d15aa')
REPO = ROOT / 'MacroDroid-Reconstruction'
COMMIT = 'dbbb89cf4ca65edd3d2c2b96151dadf41aaec514'
PREFIX = 'docs/verification/storage-cleanup/20261012-validation-duplicates-assessment'
OUT = ROOT / 'transfer-validation-assessment' / 'retirement'
NAMES = ('overlay-bootstrap-validation', 'transfer-validation')
TARGETS = tuple(ROOT / name for name in NAMES)
INVENTORY_SHA = '4a3ee9bdc09451080da9e0a2acd021126a86b33c15ba4f84c1681b715db773b0'

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

def write(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2) + '\n')

def under_target(text):
    text = text.removesuffix(' (deleted)')
    return any(text == str(path) or text.startswith(str(path) + '/') for path in TARGETS)

def process_guard():
    physical_self = os.readlink('/proc/self')
    assert physical_self.isdigit()
    matches = []
    unreadable = []
    scanned = 0
    for proc in Path('/proc').iterdir():
        if not proc.name.isdigit() or proc.name == physical_self:
            continue
        scanned += 1
        try:
            cwd = os.readlink(proc / 'cwd')
            if under_target(cwd):
                matches.append({'physical_pid': proc.name, 'kind': 'cwd'})
        except (FileNotFoundError, ProcessLookupError):
            pass
        except PermissionError:
            unreadable.append({'physical_pid': proc.name, 'kind': 'cwd'})
        try:
            argv = (proc / 'cmdline').read_bytes().split(b'\0')
            if any(str(path).encode() in item for path in TARGETS for item in argv):
                matches.append({'physical_pid': proc.name, 'kind': 'argv'})
        except (FileNotFoundError, ProcessLookupError):
            pass
        except PermissionError:
            unreadable.append({'physical_pid': proc.name, 'kind': 'argv'})
        try:
            for fd in (proc / 'fd').iterdir():
                try:
                    target = os.readlink(fd)
                    if under_target(target):
                        matches.append({'physical_pid': proc.name, 'kind': 'fd', 'fd': fd.name})
                except (FileNotFoundError, ProcessLookupError):
                    pass
        except (FileNotFoundError, ProcessLookupError):
            pass
        except PermissionError:
            unreadable.append({'physical_pid': proc.name, 'kind': 'fd'})
    result = dict(physical_self_pid=physical_self, python_namespace_pid=os.getpid(),
                  process_count=scanned, matching_users=matches, unreadable=unreadable)
    assert not matches and not unreadable, result
    return result

OUT.mkdir(parents=True, exist_ok=False)
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
assert subprocess.run(['git', 'merge-base', '--is-ancestor', COMMIT, 'origin/main'], cwd=REPO).returncode == 0
for name in ('checkpoint.json', 'assessment.json', 'inventory.json.gz', 'assess_transfer_validation_duplicates.py'):
    assert git('show', COMMIT + ':' + PREFIX + '/' + name) == (REPO / PREFIX / name).read_bytes()
compressed = (REPO / PREFIX / 'inventory.json.gz').read_bytes()
assert hashlib.sha256(compressed).hexdigest() == INVENTORY_SHA
summary = json.loads((REPO / PREFIX / 'assessment.json').read_text())
raw = gzip.decompress(compressed)
assert len(raw) == summary['inventory_bytes'] and hashlib.sha256(raw).hexdigest() == summary['inventory_sha256']
rows = json.loads(raw)
assert len(rows) == 60809 and all(row['removal_candidate'] and row['kind'] == 'file' for row in rows)
assert all(Path(row['path']).parts[0] in NAMES and '..' not in Path(row['path']).parts for row in rows)

protected = [ROOT / 'recovered', REPO, ROOT / 'current', ROOT / 'restored', ROOT / 'scene-recovery',
             ROOT / 'plugin-recovery', ROOT / 'plugin-upload-recovery', ROOT / 'widget-recovery',
             ROOT / 'combined-recovery', ROOT / 'tooling-validation', ROOT / 'widget-art-probe']
protected_directories = {}
for path in protected:
    assert path.is_dir() and not path.is_symlink()
    assert all(path != target and target not in path.parents and path not in target.parents for target in TARGETS)
    metadata = path.stat()
    protected_directories[str(path)] = [metadata.st_dev, metadata.st_ino]
retained_files = sorted(path for path in (ROOT / 'recovered').iterdir() if path.is_file())
retained_files += [REPO / PREFIX / name for name in ('checkpoint.json', 'assessment.json', 'inventory.json.gz')]
retained_before = {str(path): {'bytes': path.stat().st_size, 'sha256': sha(path)} for path in retained_files}
write('retained-before.json', retained_before)
guard_before = process_guard()
write('process-guard-before.json', guard_before)

actual = set()
for target in TARGETS:
    assert target.is_dir() and not target.is_symlink()
    for directory, dirs, files in os.walk(target, followlinks=False):
        assert not any((Path(directory) / name).is_symlink() for name in dirs)
        for name in files:
            path = Path(directory) / name
            assert not path.is_symlink() and path.is_file()
            actual.add(str(path.relative_to(ROOT)))
assert actual == {row['path'] for row in rows}
for row in rows:
    path = ROOT / row['path']
    metadata = path.lstat()
    assert stat.S_ISREG(metadata.st_mode) and metadata.st_size == row['bytes']
    assert oct(stat.S_IMODE(metadata.st_mode)) == row['mode'] and sha(path) == row['sha256'], row['path']
guard_immediate = process_guard()
write('process-guard-immediate.json', guard_immediate)
disk_before = shutil.disk_usage(ROOT)._asdict()
write('pre-removal.json', dict(commit=COMMIT, inventory_compressed_sha256=INVENTORY_SHA,
      all_candidate_files_rehashed=len(rows), retained_files=retained_before,
      protected_directory_identities=protected_directories, disk=disk_before))

retired = []
for index, target in enumerate(TARGETS):
    temporary = ROOT / ('.retired-validation-' + str(os.getpid()) + '-' + str(index))
    assert not temporary.exists()
    os.rename(target, temporary)
    retired.append({'original': str(target), 'temporary': str(temporary), 'renamed': True, 'removed': False})
    write('removal-progress.json', retired)
    shutil.rmtree(temporary)
    assert not temporary.exists() and not target.exists()
    retired[-1]['removed'] = True
    write('removal-progress.json', retired)

retained_after = {str(path): {'bytes': path.stat().st_size, 'sha256': sha(path)} for path in retained_files}
write('retained-after.json', retained_after)
assert retained_after == retained_before
for path, identity in protected_directories.items():
    metadata = Path(path).stat()
    assert [metadata.st_dev, metadata.st_ino] == identity
assert all(not target.exists() for target in TARGETS)
disk_after = shutil.disk_usage(ROOT)._asdict()
write('receipt.json', dict(status='CLOSED_VALIDATION_DUPLICATES_RETIRED', started_utc=started,
      finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), verified_assessment_commit=COMMIT,
      exact_removed_roots=list(NAMES), removed_files=len(rows), removed_logical_bytes=sum(row['bytes'] for row in rows),
      previously_measured_allocated_file_bytes=sum(row['allocated_bytes'] for row in rows),
      full_original_inventory_compressed_sha256=INVENTORY_SHA, all_candidate_files_rehashed_before_removal=True,
      process_guards_passed=2, physical_process_ids_used=True, retained_files_rehashed_before_after=len(retained_before),
      all_rehashed_retained_files_unchanged=True, protected_directory_identities_unchanged=True,
      current_and_private_acceptance_trees_not_modified=True, authored_sources_or_unpublished_evidence_removed=False,
      disk_before=disk_before, disk_after=disk_after, free_space_delta_bytes=disk_after['free']-disk_before['free'],
      disk_delta_observational_due_to_concurrent_work=True, removed_roots_still_absent_at_final_check=True))
print((OUT / 'receipt.json').read_text())
