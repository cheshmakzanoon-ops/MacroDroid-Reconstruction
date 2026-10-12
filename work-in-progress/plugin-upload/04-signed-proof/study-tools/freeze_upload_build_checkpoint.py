#!/usr/bin/env python3
"""Preserve the exact inactive upload APK/source binding while later gates run."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import tarfile


HERE = Path(__file__).resolve().parent
PROJECT = Path('/tmp/macrodroid-plugin-upload-tynqcwun/MacroDroid_v9')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source, destination, expected=None):
    expected = expected or sha(source)
    if sha(source) != expected:
        raise RuntimeError('Source identity changed: ' + str(source))
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    if sha(destination) != expected or source.stat().st_ino == destination.stat().st_ino:
        raise RuntimeError('Copy identity mismatch or hardlink')


def entries(root):
    return [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)}
            for p in sorted(root.rglob('*')) if p.is_file()]


def main():
    prior_path = HERE / 'checkpoints/02-original-jvm/checkpoint.json'
    prior = json.loads(prior_path.read_text())
    build_result = PROJECT / 'reports/upload-signed-build-03/result.json'
    build = json.loads(build_result.read_text())
    if build.get('passed') is not True or build['checkpoint_sha256'] != sha(prior_path):
        raise RuntimeError('Signed build is not bound to the frozen positive source')
    apk = Path(build['apk']['path'])
    if sha(apk) != build['apk']['sha256'] or apk.stat().st_size != build['apk']['bytes']:
        raise RuntimeError('Signed APK changed')
    output = HERE / 'checkpoints/03-signed-build'
    output.mkdir(parents=True, exist_ok=False)
    for row in prior['files']:
        copy(PROJECT / row['path'], output / row['path'], row['sha256'])
    copy(PROJECT / 'build.py', output / 'isolated-build-recipe/build.py', build['build_script_sha256'])
    for name in ('run_upload_signed_build.py', 'run_upload_signed_proof.py', 'freeze_upload_build_checkpoint.py'):
        copy(HERE / name, output / 'study-tools' / name)
    (output / 'SIGNED_BUILD_SCOPE.md').write_text('''# Plugin upload: inactive signed build checkpoint

The frozen 1,241-body plugin-upload source produced a signed hybrid APK successfully. The build command exited 0, and all 35 source/test/doc/fixture paths from checkpoint02 remained byte-identical. Exact command, timing, build recipe hash, signing log, partition-assembly logs and APK identity are preserved here.

This checkpoint preserves **build completion only**. The full original/JVM/rebuilt run, hybrid roundtrip verification, all 54 deliberate-fault UI controls and final positive restoration were still running when this checkpoint was frozen. Their completion must come from a later measured checkpoint. No Android runtime was executed and no active registry or APK was promoted.

The source files are unchanged from the original/JVM checkpoint02, including its 2,356 upload cases and full 163/163-instruction, 26/26-edge host coverage. Those earlier host results are separately durable; building an APK does not extend them to rebuilt execution.

`isolated-build-recipe/build.py` records the exact private recipe used for this artifact. It is evidence and must not overwrite the parent's newer strict generated-directory cleanup implementation during integration. Likewise the source `ui_negative_control.py` is the inactive upload version; integration must apply only its 17 new controls while retaining parent cleanup changes. The APK contains no compile-only host boundary classes.

The attached study tools run the frozen build and subsequent proof stages in the private candidate. The later proof runner source is included for reproducibility; its eventual result is not asserted by this build-only checkpoint.
''')
    source_files = entries(output)
    evidence = output / 'evidence'
    for name in ('result.json', 'build.log'):
        copy(PROJECT / 'reports/upload-signed-build-03' / name, evidence / 'signed-build' / name)
    for path in sorted((PROJECT / 'reports').glob('hybrid-assemble-*.log')):
        copy(path, evidence / path.name)
    for name in ('hybrid-sign.log', 'hybrid-signature-verification.log', 'hybrid-zipalign.log'):
        if (PROJECT / 'reports' / name).exists():
            copy(PROJECT / 'reports' / name, evidence / name)
    copy(prior_path, evidence / 'positive-source-checkpoint.json')
    evidence_files = entries(evidence)
    archive = HERE / 'checkpoints/03-signed-build-evidence.tar.gz'
    if archive.exists():
        raise RuntimeError('Archive already exists')
    with tarfile.open(archive, 'w:gz') as stream:
        for row in evidence_files:
            stream.add(evidence / row['path'], arcname=row['path'], recursive=False)
    remaining = {row['path']: row for row in evidence_files}
    with tarfile.open(archive, 'r:gz') as stream:
        for member in stream.getmembers():
            row = remaining.pop(member.name)
            data = stream.extractfile(member).read()
            if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
                raise RuntimeError('Archive member mismatch')
    if remaining:
        raise RuntimeError('Archive omitted evidence')
    checkpoint = {
        'status': 'SIGNED_BUILD_PASSED_THREE_PATH_AND_54_CONTROLS_PENDING',
        'frozen_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope': 'Inactive upload candidate; exact APK/source binding, no active promotion or Android claim',
        'source_checkpoint': {'path': str(prior_path), 'sha256': sha(prior_path)},
        'apk': build['apk'], 'build_result_sha256': sha(build_result),
        'build_recipe_sha256': build['build_script_sha256'], 'registered_bodies': 1241,
        'ui_methods': 9, 'signed_build_passed': True, 'rebuilt_proof_complete': False,
        'ui_deliberate_fault_controls_complete': False, 'android_executed': False,
        'files': source_files, 'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True,
    }
    (output / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(output / 'checkpoint.json'), 'sha256': sha(output / 'checkpoint.json'),
                      'files': len(source_files), 'evidence_files': len(evidence_files),
                      'archive': checkpoint['evidence_bundle'], 'apk': checkpoint['apk']}, indent=2))


if __name__ == '__main__':
    main()
