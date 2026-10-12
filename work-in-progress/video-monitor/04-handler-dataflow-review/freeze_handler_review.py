#!/usr/bin/env python3
"""Freeze scoped reachability evidence without altering failed positive coverage."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

HERE = Path(__file__).resolve().parent
PROJECT = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(path, base):
    return {'path': path.relative_to(base).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def copy(source, target, expected=None):
    digest = expected or sha(source)
    if source.is_symlink() or sha(source) != digest:
        raise RuntimeError('Input identity changed: ' + str(source))
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise FileExistsError(target)
    shutil.copyfile(source, target)
    if sha(target) != digest or (source.stat().st_dev, source.stat().st_ino) == (target.stat().st_dev, target.stat().st_ino):
        raise RuntimeError('Exact independent copy failed')


def main():
    collected = HERE / 'reports/handler-dataflow-04'
    verified = HERE / 'reports/handler-facts-04-review'
    facts = json.loads((verified / 'result.json').read_text())
    if (facts['status'] != 'STRUCTURAL_FACTS_VERIFIED_SYNCHRONOUS_HOST_ARGUMENT_FOR_REVIEW' or
            facts['original_coverage_credit_added'] != 0 or facts['coverage_exemption_implemented'] or
            not facts['original_coverage_gate_remains_failed'] or
            len(facts['synthetic_fact_guard_controls']) != 9 or
            not all(item['rejected'] for item in facts['synthetic_fact_guard_controls'])):
        raise RuntimeError('Expected scoped fact result differs')
    destination = HERE / 'checkpoints/04-handler-dataflow-review'
    destination.mkdir(parents=True, exist_ok=False)
    for name in ('HANDLER_DATAFLOW_REVIEW.md', 'VideoHandlerInventory.java', 'collect_handler_proof.py',
                 'verify_handler_dataflow.py', 'freeze_handler_review.py'):
        copy(HERE / name, destination / name)
    files = [row(path, destination) for path in sorted(destination.rglob('*')) if path.is_file()]
    evidence = destination / 'evidence'
    for folder in (collected, verified):
        for path in folder.rglob('*'):
            if path.is_file():
                copy(path, evidence / 'reports' / folder.name / path.relative_to(folder))
    for name in ('handler-proof-stdout.txt', 'handler-proof-stderr.txt', 'handler-facts-stdout.txt', 'handler-facts-stderr.txt'):
        copy(HERE / name, evidence / name)
    original = {
        'source/smali/classes/0d/a_0dfe0f87312c8ea9.smali': '05149221b78ddab67933f4aa8aba10330787889c9a3749d6d7296eaeb6cd6d4d',
        'source/smali/classes/ab/BaseVideoRecordingService_ab6e65d7c841bab5.smali': '7645b23e26a9e9e6be0f03bbe6b4c5702676af315fa17360c60790b0a8f915c7',
        'tests/java/BytecodeOracle.java': 'd91ddcd8ec3d67d41d69b8252835e747c2cad2c6d5ea898323794ceec30e6b56'}
    for name, digest in original.items():
        copy(PROJECT / name, evidence / 'bound-original-source-and-oracle' / name, digest)
    copy(HERE / 'reports/original-jvm-03-initial/original-video-monitor.dex', evidence / 'original-video-monitor.dex',
         '940aee4861d9bd52951ccc835e91a917bb56748b4eaad5deb8a0fa1c7d2c3254')
    positive_dependencies = []
    for rel in ('03-original-jvm-coverage-gap', '05-expanded-original-jvm-coverage-gap'):
        manifest = HERE / 'checkpoints' / rel / 'checkpoint.json'
        previous = json.loads(manifest.read_text())
        if previous['full_original_coverage_gate_passed'] or previous['original_instruction_coverage']['unvisitedOffsets'] != [232, 233, 235]:
            raise RuntimeError('Historical coverage failure changed')
        copy(manifest, evidence / 'positive-study-checkpoints' / rel / 'checkpoint.json')
        positive_dependencies.append({'path': str(manifest), 'sha256': sha(manifest), 'status': previous['status']})
    evidence_files = [row(path, evidence) for path in sorted(evidence.rglob('*')) if path.is_file()]
    archive = HERE / 'checkpoints/04-handler-dataflow-review-evidence.tar.gz'
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
                raise RuntimeError('Archive bytes differ')
    if remaining:
        raise RuntimeError('Archive omitted evidence')
    checkpoint = {'status': 'SCOPED_DATAFLOW_REVIEW_NO_COVERAGE_EXEMPTION',
        'frozen_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Original register/control-flow facts, installed JRT class bytes and pinned primary AOSP15 sources. Argument is for independent review; original coverage gate stays failed.',
        'target': 'Lcom/arlosoft/macrodroid/action/services/a;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;',
        'protected_interval': [122, 159], 'protected_instructions': 17,
        'handler_offsets': [232, 233, 235], 'catch_type': 'Ljava/lang/Exception;',
        'app_method_executions_added': 0, 'android_executed': False,
        'original_coverage_credit_added': 0, 'coverage_exemption_implemented': False,
        'positive_coverage_still_failed': True, 'synthetic_structural_guard_controls': 9,
        'synthetic_controls_rejected': 9, 'oracle_modified': False, 'active_source_changed': False,
        'host_scope': 'Actual installed Temurin21.0.12.1+1-LTS JRT classfiles, full collected byte hashes and disassembly.',
        'android_source_scope': 'android-15.0.0_r1 libcore source; hosted Google APIs boot-library bytes not extracted/matched.',
        'facts_result_sha256': sha(verified / 'result.json'), 'positive_study_dependencies': positive_dependencies,
        'files': files, 'evidence_files': evidence_files,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True}
    manifest = destination / 'checkpoint.json'
    manifest.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(manifest), 'sha256': sha(manifest), 'files': len(files),
                      'evidence_files': len(evidence_files), 'evidence_bundle': checkpoint['evidence_bundle']}, indent=2))


if __name__ == '__main__':
    main()
