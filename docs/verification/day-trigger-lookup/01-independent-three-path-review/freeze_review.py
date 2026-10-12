#!/usr/bin/env python3
"""Freeze the closed lookup review without changing its inputs or raw reports."""
from pathlib import Path
import datetime
import gzip
import hashlib
import json
import shutil
import tarfile

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'reports/fresh-review-01'
DEST = ROOT / 'checkpoints/01-independent-three-path-review'


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'mode': oct(path.stat().st_mode & 0o777)}


def inventory(root):
    result = []
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise RuntimeError('Unexpected symlink: ' + str(path))
        if path.is_file():
            result.append({'path': path.relative_to(root).as_posix(), **identity(path)})
    return result


def main():
    if DEST.exists():
        raise RuntimeError('Frozen destination already exists')
    result = json.loads((EVIDENCE / 'result.json').read_text())
    if not result['passed'] or result['status'] != 'INDEPENDENT_THREE_PATH_REVIEW_PASSED':
        raise RuntimeError('Positive review not closed')
    if identity(ROOT / 'review_lookup.py') != identity(EVIDENCE / 'review_lookup.py'):
        raise RuntimeError('Executed reviewer source changed')
    evidence_rows = inventory(EVIDENCE)
    DEST.mkdir(parents=True)
    sources = []
    for name in ('REVIEW.md', 'review_lookup.py', 'freeze_review.py'):
        path = DEST / name
        shutil.copyfile(ROOT / name, path)
        shutil.copymode(ROOT / name, path)
        sources.append({'path': name, **identity(path)})
    readable = []
    for name in ('result.json', 'command-ledger.json', 'frozen-capsule-audit.json',
                 'fresh-original-method-inventory.json', 'fresh-class-identities.json',
                 'protected-inputs-before.json', 'protected-inputs-after.json',
                 'launcher-environment-policy.json', '05-positive-pipeline/method-body-binding.json',
                 '12-fault-pipeline/method-body-binding.json'):
        path = DEST / 'review-evidence' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(EVIDENCE / name, path)
        shutil.copymode(EVIDENCE / name, path)
        readable.append({'path': path.relative_to(DEST).as_posix(), **identity(path)})
    archive = DEST / 'evidence.tar.gz'
    with archive.open('xb') as target:
        with gzip.GzipFile(filename='', mode='wb', fileobj=target, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode='w') as stream:
                for row in evidence_rows:
                    path = EVIDENCE / row['path']
                    info = tarfile.TarInfo(row['path'])
                    info.size = row['bytes']; info.mode = int(row['mode'], 8); info.mtime = 0
                    with path.open('rb') as source:
                        stream.addfile(info, source)
    if inventory(EVIDENCE) != evidence_rows:
        raise RuntimeError('Closed evidence changed while freezing')
    expected = {row['path']: row for row in evidence_rows}
    with tarfile.open(archive, 'r:gz') as stream:
        members = stream.getmembers()
        if len(members) != len(expected) or {m.name for m in members} != set(expected):
            raise RuntimeError('Archive membership mismatch')
        for member in members:
            data = stream.extractfile(member).read()
            row = expected[member.name]
            if not member.isfile() or len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256'] or oct(member.mode) != row['mode']:
                raise RuntimeError('Archive payload mismatch: ' + member.name)
    checkpoint = {
        'status': 'INDEPENDENT_LOOKUP_REVIEW_PASSED',
        'createdUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope': 'Frozen-source review plus a fresh 371-input original/JVM/rebuilt method-only run; no active app registration, full APK build, ART, or new distinct-case count.',
        'parentCheckpoint': {
            'path': 'day-trigger-lookup-recovery/checkpoints/02-three-path-and-compiled-controls/checkpoint.json',
            'sha256': '6b3cbd47969b8f10675afd8b63dcac40967a7b30748f04b60af4989bea071c29'},
        'sourceFiles': sources, 'readableEvidenceFiles': readable,
        'evidenceArchive': {'path': archive.name, **identity(archive)}, 'evidenceFiles': evidence_rows,
        'result': {key: result[key] for key in (
            'status', 'passed', 'durationSeconds', 'cases', 'executionPaths', 'mismatchCount', 'unsupportedCount',
            'freshCompiledClassCount', 'freshOriginalFixture', 'freshRebuiltFixture', 'positiveReport',
            'positiveReportRestoredExactly', 'allProtectedBytesUnchanged')},
        'archivePayloadBytes': sum(row['bytes'] for row in evidence_rows),
        'activeSourceChanged': False, 'activeRegistryChanged': False, 'apkChanged': False,
        'androidExecuted': False, 'allArchiveMembersVerified': True}
    path = DEST / 'checkpoint.json'
    path.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(path), **identity(path), 'sourceFiles': len(sources),
                      'readableEvidenceFiles': len(readable), 'evidenceFiles': len(evidence_rows),
                      'evidenceArchive': checkpoint['evidenceArchive']}, indent=2))


if __name__ == '__main__':
    main()
