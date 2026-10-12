#!/usr/bin/env python3
"""Freeze the corrected host policy and all recorded replay/fault evidence."""
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'checkpoints/01-wrapper-review'
FAILED = ROOT.parent / 'checkpoints/03-hosted-avd-failure/checkpoint.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(path, root):
    return {'path': path.relative_to(root).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def copy(source, target):
    before = sha(source)
    if source.is_symlink():
        raise RuntimeError('Symlinked checkpoint input')
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise FileExistsError(target)
    shutil.copyfile(source, target)
    if sha(target) != before or sha(source) != before:
        raise RuntimeError('Checkpoint input changed while copied')


def main():
    result = json.loads((ROOT / 'reports/validation-01/result.json').read_text())
    if (result['passed'] is not True or result['android_executed_during_validation'] is not False or
            result['wrapper_sha256'] != sha(ROOT / 'android_widget_method_probe.py') or
            result['tests_sha256'] != sha(ROOT / 'test_android_widget_method_probe.py') or
            [value['returncode'] for value in result['replays']] != [2, 0] or
            sha(FAILED) != 'ea5a1eef38b70cb45c0079aa4f63b48b66dedecf636a10b00157b571f3969eb3'):
        raise RuntimeError('Exact completed validation and preserved failure required')
    destination = ROOT.parent / 'checkpoints/04-avd-parser-fix'
    destination.mkdir(parents=True, exist_ok=False)
    for name in ('android_widget_method_probe.py', 'test_android_widget_method_probe.py',
                 'probes/widget-method-probe.dex', 'probes/widget-method-probe.json',
                 'fixtures/observed-avd-name-crlf.stdout.txt', 'validate_avd_fix.py',
                 'AVD_EVIDENCE_FIX.md', 'freeze_avd_fix_checkpoint.py'):
        copy(ROOT / name, destination / name)
    files = [row(path, destination) for path in sorted(destination.rglob('*')) if path.is_file()]
    evidence = destination / 'evidence'
    shutil.copytree(ROOT / 'reports', evidence / 'reports')
    for name in ('validation-stdout.txt', 'validation-stderr.txt'):
        copy(ROOT / name, evidence / name)
    for name in ('android_widget_method_probe.py', 'test_android_widget_method_probe.py'):
        copy(BASE / name, evidence / 'original-policy' / name)
        patch = ''.join(difflib.unified_diff((BASE / name).read_text().splitlines(keepends=True),
            (ROOT / name).read_text().splitlines(keepends=True), fromfile='original/' + name, tofile='corrected/' + name))
        target = evidence / 'changes' / (name + '.patch')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(patch)
    copy(FAILED, evidence / 'preserved-failed-job-checkpoint.json')
    evidence_files = [row(path, evidence) for path in sorted(evidence.rglob('*')) if path.is_file()]
    archive = ROOT.parent / 'checkpoints/04-avd-parser-fix-evidence.tar.gz'
    if archive.exists():
        raise FileExistsError(archive)
    with tarfile.open(archive, 'w:gz') as stream:
        for item in evidence_files:
            stream.add(evidence / item['path'], arcname=item['path'], recursive=False)
    expected = {item['path']: item for item in evidence_files}
    with tarfile.open(archive, 'r:gz') as stream:
        for member in stream:
            item = expected.pop(member.name)
            data = stream.extractfile(member).read()
            if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise RuntimeError('Archive member differs')
    if expected:
        raise RuntimeError('Missing archive members')
    checkpoint = {
        'status': 'EXACT_AVD_POLICY_HOST_CONTROLS_PASSED_FRESH_ANDROID_REQUIRED',
        'frozen_utc': datetime.now(timezone.utc).isoformat(), 'files': files,
        'source_package_file_count': len(files),
        'parent_original_package_sha256': sha(BASE / 'checkpoint.json'),
        'failed_android_evidence_sha256': sha(FAILED),
        'old_wrapper_sha256': sha(BASE / 'android_widget_method_probe.py'),
        'new_wrapper_sha256': sha(ROOT / 'android_widget_method_probe.py'),
        'probe_dex_sha256': sha(ROOT / 'probes/widget-method-probe.dex'),
        'probe_provenance_sha256': sha(ROOT / 'probes/widget-method-probe.json'),
        'android_executed_during_correction_validation': False,
        'historical_job_outcome_relabelled': False, 'fresh_android_rerun_required': True,
        'validation': result, 'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True,
    }
    target = destination / 'checkpoint.json'
    target.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(target), 'sha256': sha(target), 'source_files': len(files),
        'evidence_files': len(evidence_files), 'evidence_bundle': checkpoint['evidence_bundle']}, indent=2))


if __name__ == '__main__':
    main()
