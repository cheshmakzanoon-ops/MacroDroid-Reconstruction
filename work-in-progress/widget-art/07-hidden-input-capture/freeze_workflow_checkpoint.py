#!/usr/bin/env python3
"""Freeze the exact owned-artifact upload proposal and measured offline evidence."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPOSITORY = ROOT.parent / 'MacroDroid-Reconstruction'
BASELINE_SHA = 'b694b68e29dcb815c4dded4aed48773999f1800d5fd489dacbca067926ac32c7'
PROPOSED_SHA = 'f0d210cc3f877f407a33df84e7e15b3e5a9179288ffb640e3aabf9eb499fffba'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(path, root):
    return {'path': path.relative_to(root).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def copy(source, target, expected=None):
    expected = expected or sha(source)
    if source.is_symlink() or not source.is_file() or sha(source) != expected:
        raise RuntimeError('Source identity changed: ' + str(source))
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise FileExistsError(target)
    shutil.copyfile(source, target)
    if sha(target) != expected or (source.stat().st_dev, source.stat().st_ino) == (target.stat().st_dev, target.stat().st_ino):
        raise RuntimeError('Frozen byte copy failed or used a hardlink')


def main():
    validation = json.loads((HERE / 'reports/validation-01/result.json').read_text())
    if (validation.get('passed') is not True or validation.get('android_executed') is not False or
            validation.get('uploader_executed') is not False or
            validation['baseline_workflow_sha256'] != BASELINE_SHA or
            validation['proposed_workflow_sha256'] != PROPOSED_SHA):
        raise RuntimeError('Exact successful scoped validation is required')
    workflow_path = '.github/workflows/widget-method-probe.yml'
    if sha(REPOSITORY / workflow_path) != BASELINE_SHA or sha(HERE / workflow_path) != PROPOSED_SHA:
        raise RuntimeError('Reviewed workflow bytes changed')
    actual = ROOT / 'hosted-run-38207925500'
    preflight = json.loads((actual / 'extracted/input-preflight.json').read_text())
    dependencies = []
    for item in preflight['files']:
        path = REPOSITORY / item['path']
        if path.stat().st_size != item['bytes'] or sha(path) != item['sha256']:
            raise RuntimeError('Reviewed baseline dependency changed: ' + str(path))
        dependencies.append({'path': item['path'], 'source': str(path), 'bytes': item['bytes'], 'sha256': item['sha256']})
    (HERE / 'baseline-inputs.json').write_text(json.dumps({
        'baseline_commit': 'c1a6d71d2e290d16ea3a047d036996f79005883a',
        'baseline_workflow_sha256': BASELINE_SHA, 'files': dependencies,
    }, indent=2) + '\n')
    destination = ROOT / 'checkpoints/07-hidden-input-capture'
    destination.mkdir(parents=True, exist_ok=False)
    for name in (workflow_path, 'WORKFLOW_REVIEW.md', 'validate_artifact_scope.py',
                 'freeze_workflow_checkpoint.py', 'baseline-inputs.json'):
        copy(HERE / name, destination / name)
    copy(HERE / 'reports/validation-01/workflow.patch', destination / 'workflow.patch')
    files = [row(path, destination) for path in sorted(destination.rglob('*')) if path.is_file()]
    evidence = destination / 'evidence'
    shutil.copytree(HERE / 'reports', evidence / 'reports')
    for name in ('validation-stdout.txt', 'validation-stderr.txt'):
        copy(HERE / name, evidence / name)
    for item in dependencies:
        copy(Path(item['source']), evidence / 'baseline-inputs' / item['path'], item['sha256'])
    for name in ('upload-artifact-action.yml', 'upload-artifact-action.yml.source.json',
                 'published-workflow.yml', 'published-workflow.yml.source.json', 'source-bindings.json'):
        copy(actual / 'supplemental-provenance' / name, evidence / 'supplemental-provenance' / name)
    evidence_files = [row(path, evidence) for path in sorted(evidence.rglob('*')) if path.is_file()]
    archive = ROOT / 'checkpoints/07-hidden-input-capture-evidence.tar.gz'
    if archive.exists():
        raise FileExistsError(archive)
    with tarfile.open(archive, 'w:gz') as stream:
        for item in evidence_files:
            stream.add(evidence / item['path'], arcname=item['path'], recursive=False)
    remaining = {item['path']: item for item in evidence_files}
    with tarfile.open(archive, 'r:gz') as stream:
        for member in stream:
            if not member.isfile() or member.name not in remaining:
                raise RuntimeError('Unexpected or duplicate archive member')
            item = remaining.pop(member.name)
            data = stream.extractfile(member).read()
            if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise RuntimeError('Evidence archive identity mismatch')
    if remaining:
        raise RuntimeError('Archive omitted evidence')
    for item in dependencies:
        if sha(Path(item['source'])) != item['sha256']:
            raise RuntimeError('Baseline changed during freeze')
    checkpoint = {
        'status': 'OWNED_HIDDEN_INPUT_CAPTURE_OFFLINE_VALIDATED_FRESH_ARTIFACT_PENDING',
        'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Exactly one upload option for ci-widget-method/; no guest, APK, probe, or other workflow changes.',
        'proposed_repository_path': workflow_path,
        'baseline_workflow_sha256': BASELINE_SHA, 'workflow_sha256': PROPOSED_SHA,
        'baseline_inputs': dependencies,
        'historical_art_checkpoint_sha256': '6f12e96586f845000f0fe5cbb2f95c8e65e83de6c46113bdf92031ff75a423e4',
        'historical_run_id': 38207925500,
        'historical_probe_passed': True, 'historical_complete_artifact_audit_passed': False,
        'historical_zip_or_reports_rewritten': False,
        'probe_checkpoint_sha256': '3f1126ec9ee00af1f8b2ca3bcbdb36cbfee1545b229a5cb29705d7bfee3e35dc',
        'validation_result_sha256': sha(HERE / 'reports/validation-01/result.json'),
        'validation_passed': True, 'android_executed': False, 'uploader_executed': False,
        'fresh_complete_artifact_run_required': True, 'full_runtime_1_to_1_established': False,
        'files': files, 'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True,
    }
    manifest = destination / 'checkpoint.json'
    manifest.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(manifest), 'sha256': sha(manifest),
        'source_files': len(files), 'evidence_files': len(evidence_files),
        'workflow_sha256': PROPOSED_SHA, 'evidence_bundle': checkpoint['evidence_bundle']}, indent=2))


if __name__ == '__main__':
    main()
