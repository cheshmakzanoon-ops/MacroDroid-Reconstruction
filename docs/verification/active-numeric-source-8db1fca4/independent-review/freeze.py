#!/usr/bin/env python3
"""Freeze only the owned independent review; never reopen the original ZIP."""
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
from pathlib import Path
import shutil
import stat
import tarfile

ROOT = Path('/dev/shm/macrodroid-active-numeric-independent-review')
OUT = ROOT / 'checkpoints/01-source-artifact-review'


def identity(path, base):
    data = path.read_bytes()
    st = path.lstat()
    assert stat.S_ISREG(st.st_mode)
    return {'path': path.relative_to(base).as_posix(), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(),
            'mode': '100755' if st.st_mode & 0o111 else '100644'}


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    assert json.loads((ROOT / 'analysis-02/result.json').read_text())['passed'] is True
    executed = ROOT / 'analysis-02/executed-analyzer.py'
    assert not executed.exists()
    shutil.copyfile(ROOT / 'analyze-02.py', executed)
    source_paths = sorted(p for p in ROOT.rglob('*') if p.is_file() and 'checkpoints' not in p.relative_to(ROOT).parts)
    before = [identity(p, ROOT) for p in source_paths]
    archive = OUT / 'evidence.tar.gz'
    with archive.open('xb') as raw, gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as compressed:
        with tarfile.open(mode='w|', fileobj=compressed, format=tarfile.PAX_FORMAT) as tar:
            for path, row in zip(source_paths, before):
                data = path.read_bytes()
                assert hashlib.sha256(data).hexdigest() == row['sha256']
                info = tarfile.TarInfo(row['path'])
                info.size = len(data); info.mode = int(row['mode'][-3:], 8); info.mtime = 0
                tar.addfile(info, io.BytesIO(data))
    checked = []
    with tarfile.open(archive, 'r|gz') as tar:
        for member in tar:
            assert member.isfile()
            data = tar.extractfile(member).read()
            checked.append({'path': member.name, 'bytes': len(data),
                            'sha256': hashlib.sha256(data).hexdigest(),
                            'mode': '100755' if member.mode & 0o111 else '100644'})
    assert checked == before
    assert [identity(p, ROOT) for p in source_paths] == before
    selected = [
        'README.md', 'collect.py', 'analyze.py', 'analyze-02.py', 'freeze.py', 'inspection-01-note.md',
        'collection-01/result.json', 'collection-01/zip-member-inventory.json',
        'collection-01/retained-file-bindings.json', 'collection-01/github/github-jobs.json',
        'collection-01/github/github-artifacts.json', 'collection-01/github/artifact.zip.download.json',
        'analysis-01/REVIEWER_FAILURE.md', 'analysis-01/result.json',
        'analysis-02/result.json', 'analysis-02/inputs-before.json', 'analysis-02/inputs-after.json',
        'collection-01/retained/reports/acceptance-latest.json',
        'collection-01/retained/reports/java-all-path-parity.json',
    ]
    for name in selected:
        destination = OUT / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, destination)
    (OUT / 'evidence-members.json').write_text(json.dumps(before, indent=2) + '\n')
    result = json.loads((ROOT / 'analysis-02/result.json').read_text())
    checkpoint = {
        'schema': 1, 'kind': 'CLOSED_INDEPENDENT_ACTIVE_NUMERIC_SOURCE_ARTIFACT_REVIEW',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'target': 'docs/verification/active-numeric-source-8db1fca4/independent-review',
        'passed': True, 'run_id': 38247941263, 'source_head_sha': result['head_sha'],
        'source_job_passed': True, 'sibling_android_job_passed': False,
        'raw_archive_sha256': '4824e07658f0e5a808a9dc0b10615b030e3d5f3d030b0fa4ff40096060a34159',
        'raw_archive_bytes': 188572653, 'raw_archive_members': 1304,
        'single_content_pass': True, 'raw_archive_reread_by_analysis': False,
        'apks_materialized': False, 'application_builds_repeated': 0, 'suites_repeated': 0,
        'android_repeated': False, 'active_source_modified': False,
        'gates_passed': 16, 'fresh_report_bindings': 23,
        'source_input_files': 81298, 'source_snapshot_sha256': result['snapshot_sha256'],
        'promoted_source_rows_bound': 19, 'registered_methods': 1243, 'recovered_classes': 605,
        'host_cases': 194780, 'python_named_tests': 308,
        'fresh_hybrid_matches_committed_sha256': result['fresh_hybrid_matches_committed_sha256'],
        'java_controls': 91, 'numeric_schema2_commands': 17,
        'full_runtime_parity_established': False,
        'reviewer_schema_failures_preserved': True,
        'evidence_archive': {**identity(archive, OUT), 'members': len(before),
                             'member_bytes': sum(row['bytes'] for row in before)},
    }
    rows = [identity(p, OUT) for p in sorted(OUT.rglob('*')) if p.is_file()]
    checkpoint.update(files=rows, payload_count=len(rows), payload_bytes=sum(row['bytes'] for row in rows))
    with (OUT / 'checkpoint.json').open('x') as stream:
        stream.write(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'),
                      **identity(OUT / 'checkpoint.json', OUT),
                      'payload_count': len(rows), 'evidence_members': len(before),
                      'evidence_archive': checkpoint['evidence_archive']}, indent=2))


if __name__ == '__main__':
    main()
