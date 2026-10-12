#!/usr/bin/env python3
"""Preserve the exact first compiled video source overlay and its bounded logs."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(path, base):
    return {'path': path.relative_to(base).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def main():
    result_path = HERE / 'reports/draft-compile-02/result.json'
    result = json.loads(result_path.read_text())
    if result.get('passed') is not True or result['status'] != 'UNREGISTERED_DRAFT_COMPILED_DIFFERENTIAL_PENDING':
        raise RuntimeError('Exact compiled draft required')
    inputs = json.loads((result_path.parent / 'inputs.json').read_text())['files']
    for item in inputs:
        if sha(Path(item['source'])) != item['sha256'] or sha(Path(item['private_copy'])) != item['sha256']:
            raise RuntimeError('Compiled source input changed')
    destination = HERE / 'checkpoints/02-draft-compile'
    destination.mkdir(parents=True, exist_ok=False)
    names = [path.relative_to(HERE).as_posix() for tree in ('source/java', 'test-support/java', 'tests/java')
             for path in (HERE / tree).rglob('*.java')]
    names += ['DRAFT_SCOPE.md', 'compile_video_draft.py', 'freeze_video_draft.py',
              'proposed-method-entry.json', 'shared-baseline.json']
    for name in names:
        source, target = HERE / name, destination / name
        if source.is_symlink():
            raise RuntimeError('Source symlink refused')
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if sha(source) != sha(target) or (source.stat().st_dev, source.stat().st_ino) == (target.stat().st_dev, target.stat().st_ino):
            raise RuntimeError('Frozen byte copy failed')
    files = [row(path, destination) for path in sorted(destination.rglob('*')) if path.is_file()]
    evidence = destination / 'evidence'
    shutil.copytree(result_path.parent, evidence / 'reports/draft-compile-02')
    for name in ('draft-compile-stdout.txt', 'draft-compile-stderr.txt'):
        shutil.copyfile(HERE / name, evidence / name)
    evidence_files = [row(path, evidence) for path in sorted(evidence.rglob('*')) if path.is_file()]
    archive = HERE / 'checkpoints/02-draft-compile-evidence.tar.gz'
    if archive.exists():
        raise FileExistsError(archive)
    with tarfile.open(archive, 'w:gz') as stream:
        for item in evidence_files:
            stream.add(evidence / item['path'], arcname=item['path'], recursive=False)
    remaining = {item['path']: item for item in evidence_files}
    with tarfile.open(archive, 'r:gz') as stream:
        for member in stream:
            item = remaining.pop(member.name)
            data = stream.extractfile(member).read()
            if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise RuntimeError('Archive member mismatch')
    if remaining:
        raise RuntimeError('Archive omitted files')
    checkpoint = {'status': result['status'], 'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'First private javac-only overlay. No selected method execution, visited coverage, deliberate-fault proof, registration, signed build or Android execution.',
        'target': 'Lcom/arlosoft/macrodroid/action/services/a;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;',
        'baseline_registered_bodies': 1242, 'source_files': 841, 'overlay_java_files': 23,
        'class_files': 881, 'compile_result_sha256': sha(result_path),
        'original_assessment_checkpoint_sha256': 'b367416660ecca26762c0c3e0323de738cb136258817ed219ba78e7d75597029',
        'registered': False, 'app_method_executed': False, 'android_executed': False,
        'full_runtime_1_to_1_established': False, 'files': files, 'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True}
    manifest = destination / 'checkpoint.json'
    manifest.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(manifest), 'sha256': sha(manifest), 'files': len(files),
        'evidence_files': len(evidence_files), 'evidence_bundle': checkpoint['evidence_bundle']}, indent=2))


if __name__ == '__main__':
    main()
