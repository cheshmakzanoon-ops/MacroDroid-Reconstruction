#!/usr/bin/env python3
"""Freeze a reviewable full workflow and its complete offline control evidence."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

HERE = Path(__file__).resolve().parent
REPOSITORY = Path('/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(path, root):
    return {'path': path.relative_to(root).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def copied(source, target, expected=None):
    expected = expected or sha(source)
    if source.is_symlink() or sha(source) != expected:
        raise RuntimeError('Baseline or frozen input changed')
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise FileExistsError(target)
    shutil.copyfile(source, target)
    if sha(target) != expected or (source.stat().st_ino == target.stat().st_ino and source.stat().st_dev == target.stat().st_dev):
        raise RuntimeError('Checkpoint copy failed or used a hardlink')


def main():
    validation = json.loads((HERE / 'reports/validation-01/result.json').read_text())
    workflow = HERE / '.github/workflows/widget-method-probe.yml'
    if validation.get('passed') is not True or validation['workflow_sha256'] != sha(workflow) or validation['android_executed'] is not False:
        raise RuntimeError('Exact complete offline validation required')
    inputs = json.loads((HERE / 'baseline-inputs.json').read_text())
    destination = HERE.parent / 'checkpoints/02-workflow-review'
    destination.mkdir(parents=True, exist_ok=False)
    for name in ('.github/workflows/widget-method-probe.yml', 'baseline-inputs.json', 'validate_widget_workflow.py',
                 'WORKFLOW_REVIEW.md', 'freeze_workflow_checkpoint.py'):
        copied(HERE / name, destination / name)
    files = [row(p, destination) for p in sorted(destination.rglob('*')) if p.is_file()]
    evidence = destination / 'evidence'
    shutil.copytree(HERE / 'reports', evidence / 'reports')
    for name in ('validation-stdout.txt', 'validation-stderr.txt'):
        copied(HERE / name, evidence / name)
    for item in inputs['files']:
        copied(REPOSITORY / item['path'], evidence / 'baseline-inputs' / item['path'], item['sha256'])
    evidence_files = [row(p, evidence) for p in sorted(evidence.rglob('*')) if p.is_file()]
    archive = HERE.parent / 'checkpoints/02-workflow-review-evidence.tar.gz'
    if archive.exists():
        raise FileExistsError(archive)
    with tarfile.open(archive, 'w:gz') as stream:
        for item in evidence_files:
            stream.add(evidence / item['path'], arcname=item['path'], recursive=False)
    remaining = {r['path']: r for r in evidence_files}
    with tarfile.open(archive, 'r:gz') as stream:
        for member in stream:
            item = remaining.pop(member.name)
            data = stream.extractfile(member).read()
            if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise RuntimeError('Evidence archive mismatch')
    if remaining:
        raise RuntimeError('Evidence archive omitted files')
    for item in inputs['files']:
        if sha(REPOSITORY / item['path']) != item['sha256']:
            raise RuntimeError('Selected baseline changed during freeze')
    checkpoint = {
        'status': 'FULL_WORKFLOW_OFFLINE_CONTROLS_PASSED_ANDROID_PENDING',
        'frozen_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope': 'New independent Widget ART workflow only; no current app or existing workflow changes, no Android execution at this freeze.',
        'proposed_repository_path': '.github/workflows/widget-method-probe.yml',
        'workflow_sha256': sha(workflow), 'baseline_inputs': inputs,
        'frozen_probe_checkpoint_sha256': 'aa979100f925ba216d1a78dbb9de9c293d5b2e4b771210c2862556bf6946585a',
        'original_apk_sha256': '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800',
        'candidate_apk_sha256': 'b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f',
        'probe_dex_sha256': '79bd3b46e71253b17ec75099cce3611df1735b8f74e8bdcb61c61e5a37ae1a07',
        'validation': validation, 'android_executed': False, 'files': files,
        'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True,
    }
    path = destination / 'checkpoint.json'
    path.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(path), 'sha256': sha(path), 'workflow_sha256': sha(workflow),
        'source_files': len(files), 'evidence_files': len(evidence_files), 'evidence_bundle': checkpoint['evidence_bundle']}, indent=2))


if __name__ == '__main__':
    main()
