#!/usr/bin/env python3
"""Close the actual 41-control run without rerunning it."""
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
from pathlib import Path
import shutil
import stat
import tarfile

BASE = Path('/dev/shm/macrodroid-day-numeric-art')
RUN = BASE / 'wrapper-controls-01'
OUT = BASE / 'checkpoints/04-wrapper-host-controls'


def identity(path):
    a = path.lstat(); assert stat.S_ISREG(a.st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    b = path.lstat()
    assert (a.st_dev, a.st_ino, a.st_size, a.st_mtime_ns, a.st_ctime_ns) == (b.st_dev, b.st_ino, b.st_size, b.st_mtime_ns, b.st_ctime_ns)
    return {'bytes': b.st_size, 'sha256': digest, 'mode': stat.S_IMODE(b.st_mode)}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def copy(source, target):
    expected = identity(source); target.parent.mkdir(parents=True, exist_ok=True)
    with source.open('rb') as reader, target.open('xb') as writer:
        shutil.copyfileobj(reader, writer)
    target.chmod(expected['mode']); assert identity(target) == identity(source) == expected


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    copy(Path(__file__), OUT / 'executed-freezer.py')
    result = json.loads((RUN / 'result.json').read_bytes())
    assert result['passed'] is True and result['actual_named_test_count'] == 41
    assert result['android_executed'] is result['app_build_executed'] is False
    assert (RUN / 'inputs-before.json').read_bytes() == (RUN / 'inputs-after.json').read_bytes()
    for command in result['commands']:
        assert command['returncode'] == 0 and command['timed_out'] is False
        for name in ('stdout', 'stderr'):
            assert identity(RUN / 'commands' / command['label'] / (name + '.txt')) == command[name]
    rows = [{'path': p.relative_to(RUN).as_posix(), **identity(p)} for p in sorted(RUN.rglob('*')) if p.is_file()]
    assert len(rows) == 7629
    save(OUT / 'evidence-inventory.json', rows)
    archive = OUT / 'evidence.tar.gz'
    with archive.open('xb') as raw, gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0, compresslevel=6) as compressed:
        with tarfile.open(fileobj=compressed, mode='w|', format=tarfile.PAX_FORMAT) as stream:
            for row in rows:
                data = (RUN / row['path']).read_bytes()
                assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
                info = tarfile.TarInfo(row['path']); info.size = len(data); info.mode = row['mode']
                info.uid = info.gid = info.mtime = 0; info.uname = info.gname = ''
                stream.addfile(info, io.BytesIO(data))
    observed = []
    with tarfile.open(archive, 'r|gz') as stream:
        for member in stream:
            assert member.isfile()
            with stream.extractfile(member) as payload:
                value = hashlib.file_digest(payload, 'sha256').hexdigest()
            observed.append({'path': member.name, 'bytes': member.size, 'sha256': value, 'mode': member.mode})
    assert observed == rows
    after = [{'path': row['path'], **identity(RUN / row['path'])} for row in rows]
    assert rows == after
    for row in rows:
        name = row['path']
        if not name.startswith('host-evidence/'):
            target = ('source/' + name[len('executed-source/'):]) if name.startswith('executed-source/') else 'reports/' + name
            copy(RUN / name, OUT / target)
    copy(BASE / 'wrapper-draft-01/checkpoint.json', OUT / 'source-draft-checkpoint.json')
    save(OUT / 'closure.json', {'status': 'ALL_7629_RAW_FILES_EXACTLY_ARCHIVED_AND_REVERIFIED',
         'archive': identity(archive), 'archive_members': len(rows),
         'expanded_bytes': sum(row['bytes'] for row in rows), 'all_run_files_unchanged': True,
         'android_executed': False, 'new_suite_execution': False})
    (OUT / 'README.md').write_text('''# Numeric ART wrapper: actual read-only preflight and 41 host controls

The exact wrapper-source draft `6ca4711b330c64f72c0df716e4a8c407360297a9bbc09e634bd88feb295a6dd6` passed its actual read-only preflight against original APK 84333011, candidate 0762aad9, compiled neutral DEX 7cf6f317, exact provenance and all 1,291 fixed corpus inputs. That command exited zero in 2.493 seconds under the unchanged 120-second bound.

All **41 named host controls passed**, with no failure, error or skipped test. The actual unittest log reports 25.433 seconds; its outer command completed in 25.957 seconds under a 240-second bound. These controls use an explicitly injected simulated ADB runner and cannot establish Android execution. They retain all 31 inherited bounded-lifecycle control names and ten numeric corpus/wire/exception controls. The test source is the exact frozen draft.

The controls cover altered source inputs, physical/wrong devices, exact LF/CRLF AVD identity, late verifier/classpath overrides, failed transfers, read-only modes and hashes, separate original/candidate processes, a failed original stopping the candidate, timeout prefixes/diagnostics, changed post-identities, owned cleanup, modified/rehashed evidence, strict complete case ordering and numeric values, sole null-entry NPE-class normalization with lossless raw UTF16 messages, and rejection of host inventory output as Android evidence. No APK is installed and no actual ADB command is executed in these controls.

`evidence.tar.gz` contains all 7,629 owned regular files and their complete literal command/fixture evidence. `evidence-inventory.json` pins every member, and closure independently streamed and rehashed the entire archive. Read-only input identities and all run files remained unchanged. `source/` is an exact convenient copy of the executed source. This capsule adds no workflow activation, application build, runtime parity or numeric method credit. Actual Android execution remains pending separate workflow review.
''')
    files = [{'path': p.relative_to(OUT).as_posix(), **identity(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
    save(OUT / 'checkpoint.json', {'schema': 1, 'status': 'CLOSED_NUMERIC_ART_WRAPPER_PREFLIGHT_AND_41_HOST_CONTROLS',
         'created_utc': datetime.now(timezone.utc).isoformat(), 'repo_target': 'work-in-progress/day-numeric-art/04-wrapper-host-controls',
         'source_draft_sha256': '6ca4711b330c64f72c0df716e4a8c407360297a9bbc09e634bd88feb295a6dd6',
         'active_files': [], 'android_executed': False, 'application_build_executed': False,
         'host_controls_passed': 41, 'archive_members': len(rows), 'files': files})
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
                      'payloads': len(files), 'payload_bytes': sum(row['bytes'] for row in files), 'archive': identity(archive)}))


if __name__ == '__main__':
    main()
