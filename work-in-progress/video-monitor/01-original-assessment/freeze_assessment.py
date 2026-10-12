#!/usr/bin/env python3
"""Preserve the original-bytecode inventory before isolated video-monitor authoring."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

HERE = Path(__file__).resolve().parent


def sha(path):
    with path.open('rb') as stream:
        value = hashlib.file_digest(stream, 'sha256').hexdigest()
    return value


def row(path, base):
    return {'path': path.relative_to(base).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def main():
    result = json.loads((HERE / 'reports/original-inventory-01/result.json').read_text())
    if result['status'] != 'EXACT_21_METHOD_ORIGINAL_DEX_METADATA_RECORDED' or any(
            command['returncode'] != 0 for command in result['commands']):
        raise RuntimeError('Successful original-only inventory required')
    for item in result['source_classes']:
        path = Path(item['path'])
        if sha(path) != item['sha256'] or path.stat().st_size != item['bytes']:
            raise RuntimeError('Original source input changed')
    registry = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/source/java-method-map.json')
    if sha(registry) != '73a37f1ac4148c03a1dc0df9810e899ebb8ff7bcc6f1df7c1672fd525d66a20e':
        raise RuntimeError('Assessed registry baseline changed')
    destination = HERE.parent / 'video-monitor-recovery/checkpoints/01-original-assessment'
    destination.mkdir(parents=True, exist_ok=False)
    names = ['ASSESSMENT.md', 'OriginalMethodInventory.java', 'assess_original_methods.py',
             'freeze_assessment.py', 'fresh-registry-inventory.json', 'remaining-method-metadata.json']
    names += [path.relative_to(HERE).as_posix() for path in sorted((HERE / 'original-methods').rglob('*')) if path.is_file()]
    for name in names:
        source, target = HERE / name, destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if source.is_symlink() or sha(target) != sha(source) or source.stat().st_ino == target.stat().st_ino:
            raise RuntimeError('Source copy identity failed')
    files = [row(path, destination) for path in sorted(destination.rglob('*')) if path.is_file()]
    evidence = destination / 'evidence'
    shutil.copytree(HERE / 'reports', evidence / 'reports')
    for name in ('assessment-stdout.txt', 'assessment-stderr.txt'):
        shutil.copyfile(HERE / name, evidence / name)
    evidence_files = [row(path, evidence) for path in sorted(evidence.rglob('*')) if path.is_file()]
    archive = destination.parent / '01-original-assessment-evidence.tar.gz'
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
                raise RuntimeError('Archived evidence differs')
    if remaining:
        raise RuntimeError('Archived evidence is incomplete')
    checkpoint = {
        'status': 'ORIGINAL_21_METHOD_INVENTORY_AND_VIDEO_MONITOR_CASE_PLAN',
        'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Original APK metadata and unexecuted semantic case design only. No app source registration, method execution, signed build or Android proof.',
        'baseline_registered_bodies': 1242, 'remaining_decompiler_failure_methods': 21,
        'registry_sha256': sha(registry),
        'target': 'Lcom/arlosoft/macrodroid/action/services/a;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;',
        'original_instructions': 262, 'original_code_units': 534, 'original_conditional_if_edges': 46,
        'counts_are_visited_coverage': False, 'app_method_executed': False,
        'registered': False, 'android_executed': False, 'full_runtime_1_to_1_established': False,
        'files': files, 'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True,
    }
    manifest = destination / 'checkpoint.json'
    manifest.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(manifest), 'sha256': sha(manifest), 'source_files': len(files),
        'evidence_files': len(evidence_files), 'evidence_bundle': checkpoint['evidence_bundle']}, indent=2))


if __name__ == '__main__':
    main()
