#!/usr/bin/env python3
"""Freeze the exact two-role successor and every owned attempt; no external mutation."""
from __future__ import annotations

from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import stat
import tarfile

OWN = Path('/dev/shm/macrodroid-day-numeric-art-schema-02')
CAP = OWN / 'checkpoints/01-literal-schema-successor-and-review'
DEPENDENCIES = [
    ('wrapper-source.checkpoint.json', Path('/dev/shm/macrodroid-day-numeric-art/wrapper-draft-01/checkpoint.json'),
     '6ca4711b330c64f72c0df716e4a8c407360297a9bbc09e634bd88feb295a6dd6'),
    ('wrapper-host-controls.checkpoint.json', Path('/dev/shm/macrodroid-day-numeric-art/checkpoints/04-wrapper-host-controls/checkpoint.json'),
     '14bd536aa8af2e8458d8c3b1d45de6c770e55ce4e7f0f5e152a70bc6ed79e0bb'),
    ('neutral-source-review.checkpoint.json', Path('/dev/shm/macrodroid-day-numeric-art-independent-review/checkpoint.json'),
     '47a90e4ac7d13e50f4151f07417a8952907a269e382a1370a33406f105b69e67'),
]


def identity(path):
    a = path.lstat()
    assert stat.S_ISREG(a.st_mode), str(path)
    with path.open('rb') as stream:
        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    b = path.lstat()
    assert (a.st_dev, a.st_ino, a.st_size, a.st_mtime_ns, a.st_ctime_ns) == (
        b.st_dev, b.st_ino, b.st_size, b.st_mtime_ns, b.st_ctime_ns)
    return {'bytes': b.st_size, 'sha256': sha, 'mode': stat.S_IMODE(b.st_mode)}


def save(path, value):
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def copy_file(source, relative):
    expected = identity(source)
    target = CAP / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    assert not target.exists()
    shutil.copyfile(source, target)
    target.chmod(expected['mode'])
    assert identity(target) == identity(source) == expected


def main():
    counter = json.loads((OWN / 'reports/counterexample-01/result.json').read_bytes())
    focused = json.loads((OWN / 'reports/focused-01/command.json').read_bytes())
    review = json.loads((OWN / 'reports/closed-review-01/result.json').read_bytes())
    assert counter['counterexample_reproduced'] is True and counter['literal_integer_schema_contract_passed'] is False
    assert focused['returncode'] == 0 and focused['timed_out'] is False
    assert review['passed'] is True and review['all_reviewed_inputs_unchanged'] is True
    bindings = json.loads((OWN / 'source-bindings.json').read_bytes())
    assert len(bindings) == 9
    for row in bindings:
        assert identity(OWN / 'source' / row['path']) == row['after']
    CAP.mkdir(parents=True, exist_ok=False)
    for name, path, sha in DEPENDENCIES:
        assert identity(path)['sha256'] == sha
        copy_file(path, 'dependencies/' + name)
    for row in bindings:
        copy_file(OWN / 'source' / row['path'], 'source/' + row['path'])
    for name in ['README.md', 'source-successor.patch', 'source-bindings.json', 'ast-derivation.json',
                 'counterexample.py', 'author_successor.py', 'run_retained.py', 'review_closed.py', 'freeze.py']:
        copy_file(OWN / name, name)
    report_root = OWN / 'reports'
    reports = sorted(path for path in report_root.rglob('*') if path.is_file())
    inventory = [{'path': path.relative_to(report_root).as_posix(), **identity(path)} for path in reports]
    assert len({row['path'] for row in inventory}) == len(reports)
    save(CAP / 'evidence-inventory.json', inventory)
    with (CAP / 'evidence.tar.gz').open('xb') as raw:
        with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode='w|') as archive:
                for path, row in zip(reports, inventory):
                    info = tarfile.TarInfo(row['path'])
                    info.size, info.mode, info.mtime = row['bytes'], row['mode'], 0
                    info.uid = info.gid = 0
                    info.uname = info.gname = ''
                    with path.open('rb') as stream:
                        archive.addfile(info, stream)
    wanted = {row['path']: row for row in inventory}
    seen = set()
    with tarfile.open(CAP / 'evidence.tar.gz', 'r:gz') as archive:
        for member in archive:
            assert member.isfile() and member.name not in seen and member.name in wanted
            row = wanted[member.name]
            sha = hashlib.file_digest(archive.extractfile(member), 'sha256').hexdigest()
            assert (member.size, member.mode, sha) == (row['bytes'], row['mode'], row['sha256'])
            seen.add(member.name)
    assert seen == set(wanted)
    assert inventory == [{'path': path.relative_to(report_root).as_posix(), **identity(path)} for path in reports]
    selected = [
        'counterexample-01/result.json', 'counterexample-01/observations.json', 'counterexample-01/command.json',
        'counterexample-01/stdout.txt', 'counterexample-01/stderr.txt',
        'counterexample-01/float-provenance-input.json', 'counterexample-01/float-report-input.json',
        'author-01/command.json', 'author-01/stdout.txt', 'author-01/stderr.txt',
        'focused-01/command.json', 'focused-01/stdout.txt', 'focused-01/stderr.txt',
        'focused-01/inputs-before.json', 'focused-01/inputs-after.json',
        'focused-01/host-evidence/test_literal_integer_schema_is_required_for_provenance_and_result_replay/result/schema-observations.json',
        'closed-review-01/result.json',
    ]
    for name in selected:
        copy_file(report_root / name, 'reports/' + name)
    source_files = [{'path': 'source/' + row['path'], **identity(CAP / 'source' / row['path'])} for row in bindings]
    payloads = [{'path': path.relative_to(CAP).as_posix(), **identity(path)}
                for path in sorted(CAP.rglob('*')) if path.is_file()]
    value = {'schema': 1, 'status': 'CLOSED_TWO_SCHEMA_GUARDS_ONE_FOCUSED_CONTROL_AND_REVIEW',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'repo_target': 'work-in-progress/day-numeric-art/05-literal-schema-successor-and-review',
        'active_files': [], 'android_executed': False, 'application_build_executed': False,
        'workflow_activated': False, 'full_42_suite_executed_locally': False,
        'prior_41_tests_passed_on_old_source': True, 'new_focused_test_passed_on_successor': True,
        'prior_41_test_bodies_unchanged': True, 'final_named_host_test_count': 42,
        'old_float_counterexample_reproduced': True, 'old_literal_integer_contract_passed': False,
        'source_draft_sha256': DEPENDENCIES[0][2], 'full_old_host_proof_sha256': DEPENDENCIES[1][2],
        'old_wrapper_sha256': 'cc8b400f419ae9dc47677bcc9c71257440d46c8278ab32dd5a759378a45e7c96',
        'successor_wrapper_sha256': identity(CAP / 'source/android_day_numeric_method_probe.py')['sha256'],
        'source_file_count': len(source_files), 'source_files': source_files,
        'archived_evidence_files': len(inventory), 'archived_uncompressed_bytes': sum(row['bytes'] for row in inventory),
        'evidence_archive': identity(CAP / 'evidence.tar.gz'), 'files': payloads}
    save(CAP / 'checkpoint.json', value)
    print(json.dumps({'checkpoint': str(CAP / 'checkpoint.json'), **identity(CAP / 'checkpoint.json'),
                      'payloads': len(payloads), 'source_files': len(source_files),
                      'archive_members': len(inventory), 'archive': value['evidence_archive']}, indent=2))


if __name__ == '__main__':
    main()
