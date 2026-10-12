"""Preserve the closed Settings source capsule's exact archive as bounded parts."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import stat
import subprocess
import sys
import tarfile

BASE = Path('/dev/shm/macrodroid-transfer-space-20261012')
SOURCE = Path('/dev/shm/macrodroid-exact-alarm-enable-return/checkpoints/03-source-and-host-controls')
OUTPUT = BASE / 'settings-source03-archive-layout'
PREFIX = 'work-in-progress/exact-alarm-enable-return/03-source-and-host-controls'
LAYOUT = PREFIX + '/archive-layout'
CP_SHA = '6a4ea8e2794a5459bcb699bb314c9b9b14fe538f45b8e06a9c2aee66a5d08051'
ARCHIVE_SHA = '51749196bbc80e9ac82beb4821cb15253c7d94122b628f7ecfd624cc398d6755'
ARCHIVE_BYTES = 13014001
GIT = ['git', '--git-dir=' + str(BASE / 'verification.git')]
PARENT = '636004a01b11fc7ac307abc9df022898b7738e62'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def safe(name):
    value = PurePosixPath(name)
    assert not value.is_absolute() and '..' not in value.parts and value.as_posix() == name
    return name

def identity(path):
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode)
    data = path.read_bytes()
    return dict(bytes=len(data), sha256=sha(data), mode=stat.S_IMODE(info.st_mode))

def write(name, raw):
    destination = OUTPUT / safe(name)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('xb') as stream:
        stream.write(raw)
    destination.chmod(0o644)

def write_json(name, value):
    write(name, (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode())

cp_raw = (SOURCE / 'checkpoint.json').read_bytes()
assert sha(cp_raw) == CP_SHA
cp = json.loads(cp_raw)
assert len(cp['files']) == 181 and len({safe(row['path']) for row in cp['files']}) == 181
before = {}
for row in cp['files']:
    actual = identity(SOURCE / row['path'])
    assert actual == {key: row[key] for key in ('bytes', 'sha256', 'mode')}
    before[row['path']] = actual
assert before['evidence.tar.gz'] == dict(bytes=ARCHIVE_BYTES, sha256=ARCHIVE_SHA, mode=0o644)
inventory_raw = (SOURCE / 'evidence-inventory.json').read_bytes()
inventory = json.loads(inventory_raw)
expected = {safe(row['path']): row for row in inventory}
assert len(inventory) == len(expected) == 353
members = []
with tarfile.open(SOURCE / 'evidence.tar.gz', 'r:gz') as archive:
    for member in archive:
        assert member.isfile() and member.name in expected
        assert member.name not in {row['path'] for row in members}
        data = archive.extractfile(member).read()
        actual = dict(path=member.name, bytes=len(data), sha256=sha(data), mode=member.mode & 0o777)
        assert actual == expected[member.name]
        members.append(actual)
assert len(members) == 353

OUTPUT.mkdir(exist_ok=False)
parts, combined, total = [], hashlib.sha256(), 0
with (SOURCE / 'evidence.tar.gz').open('rb') as stream:
    for index in range(1, 3):
        data = stream.read(8 * 1024 * 1024)
        assert data and len(data) <= 8 * 1024 * 1024
        name = 'parts/evidence.' + str(index).zfill(4) + '.part'
        write(name, data)
        parts.append(dict(path=LAYOUT + '/' + name, size_bytes=len(data), sha256=sha(data),
                          git_blob_sha1=hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest(),
                          mode='100644'))
        combined.update(data)
        total += len(data)
    assert not stream.read(1)
assert total == ARCHIVE_BYTES and combined.hexdigest() == ARCHIVE_SHA
manifest = dict(format='macrodroid-multipart-artifact', format_version=1,
                filename='evidence.tar.gz', size_bytes=ARCHIVE_BYTES, sha256=ARCHIVE_SHA,
                mode='100644', parts=parts,
                source_checkpoint=dict(path=PREFIX + '/checkpoint.json', bytes=len(cp_raw), sha256=CP_SHA),
                logical_repository_path=PREFIX + '/evidence.tar.gz',
                evidence_inventory=dict(path=PREFIX + '/evidence-inventory.json', bytes=len(inventory_raw),
                                        sha256=sha(inventory_raw), members=353))
write_json('manifest.json', manifest)
write_json('archive-members-verification.json', dict(source_archive_sha256=ARCHIVE_SHA,
           inventory_sha256=sha(inventory_raw), exact_member_count=353, members=members,
           member_names_bytes_modes_verified=True))
write_json('layout-addendum.json', dict(schema=1, original_checkpoint_sha256=CP_SHA,
           original_checkpoint_preserved=True, logical_path=PREFIX + '/evidence.tar.gz',
           logical_file=dict(bytes=ARCHIVE_BYTES, sha256=ARCHIVE_SHA, mode='100644'),
           committed_manifest=LAYOUT + '/manifest.json', parts=parts,
           all_other_180_original_payloads_committed_unchanged=True,
           archive_content_or_compression_changed=False,
           integration_order=['Verify original checkpoint, transport manifest and both part identities.',
                              'Reassemble to the logical evidence.tar.gz path before complete-capsule validation.',
                              'Verify complete archive size and SHA-256, set mode 0644, then validate all 181 original payloads and all 353 archived members.'],
           no_application_or_workflow_activation=True))

assembler = subprocess.check_output(GIT + ['show', PARENT + ':scripts/assemble_artifact.py'])
write('reviewed-assemble-artifact.py', assembler)
virtual = BASE / 'settings-source03-assembly-validation'
virtual.mkdir(exist_ok=False)
for row in parts:
    target = virtual / row['path']
    target.parent.mkdir(parents=True, exist_ok=True)
    os.link(OUTPUT / row['path'].removeprefix(LAYOUT + '/'), target)
spec = importlib.util.spec_from_file_location('settings03_exact_assembler', OUTPUT / 'reviewed-assemble-artifact.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.REPOSITORY = virtual
saved_argv, stdout, stderr = sys.argv, io.StringIO(), io.StringIO()
try:
    sys.argv = ['reviewed-assemble-artifact.py', str(OUTPUT / 'manifest.json'), '--verify-only']
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        module.main()
finally:
    sys.argv = saved_argv
assert not stderr.getvalue()
write('assembler.stdout.log', stdout.getvalue().encode())
write('assembler.stderr.log', stderr.getvalue().encode())
write_json('verification.json', dict(status='EXACT_SETTINGS03_ARCHIVE_MULTIPART_VERIFIED', passed=True,
           source_checkpoint_sha256=CP_SHA, original_payloads_verified=181, archived_members_verified=353,
           part_count=2, total_bytes=total, archive_sha256=combined.hexdigest(),
           part_sizes=[row['size_bytes'] for row in parts], no_assembled_archive_copy_created=True,
           assembler_source=dict(commit=PARENT, path='scripts/assemble_artifact.py', sha256=sha(assembler)),
           actual_entry_point='main', argv=['reviewed-assemble-artifact.py', 'manifest.json', '--verify-only'],
           repository_override='Owned directory containing only hardlinks to the two exact new parts.',
           exit_code=0, original_checkpoint_unchanged=True,
           application_source_changed=False, android_executed=False,
           completed_utc=datetime.now(timezone.utc).isoformat()))
readme = f'''# Exact Settings03 archive layout

The original source checkpoint `{CP_SHA}` and all 180 non-archive payloads are preserved byte-for-byte at `../`. Its original `evidence.tar.gz` is represented by two exact binary parts because a single base64 transport request would exceed the connector request bound. The archive was neither recompressed nor edited.

The logical archive is **{ARCHIVE_BYTES:,} bytes**, SHA-256 **{ARCHIVE_SHA}**, mode **0644**. `manifest.json` binds both canonical repository part paths, their byte counts, SHA-256 values and Git blob identities. `archive-members-verification.json` records all **353** exact member byte/mode checks against the original inventory.

From the repository root, reconstruct the logical file before validating the complete original 181-file capsule:

```sh
python3 scripts/assemble_artifact.py {LAYOUT}/manifest.json --output {PREFIX}/evidence.tar.gz
chmod 0644 {PREFIX}/evidence.tar.gz
```

Then recheck the whole archive digest, the unchanged original `checkpoint.json`, all 181 declared payload byte/mode identities, and the 353 archived member identities. An absent archive is not a complete capsule; the parts are its published transport representation.

The existing fetched assembler was actually invoked with `--verify-only` against both exact parts in an owned repository layout. That check created no assembled duplicate. Its source and actual stdout/stderr are retained here. This publication activates no source, APK, device input, or workflow.
'''
write('README.md', readme.encode())
write('executed-freezer.py', Path(__file__).read_bytes())
for name, value in before.items():
    assert identity(SOURCE / name) == value
assert (SOURCE / 'checkpoint.json').read_bytes() == cp_raw
files = [dict(path=str(path.relative_to(OUTPUT)), **identity(path))
         for path in sorted(OUTPUT.rglob('*')) if path.is_file()]
write_json('checkpoint.json', dict(schema=1, status='EXACT_MULTIPART_TRANSPORT_ONLY', repo_target=LAYOUT,
           active_files=[], original_checkpoint_sha256=CP_SHA, logical_archive_sha256=ARCHIVE_SHA,
           files=files))
print(json.dumps(dict(output=str(OUTPUT), repo_target=LAYOUT, checkpoint=identity(OUTPUT / 'checkpoint.json'),
      files=len(files), manifest=identity(OUTPUT / 'manifest.json'), addendum=identity(OUTPUT / 'layout-addendum.json'),
      parts=parts, original_source_unchanged=True)))
