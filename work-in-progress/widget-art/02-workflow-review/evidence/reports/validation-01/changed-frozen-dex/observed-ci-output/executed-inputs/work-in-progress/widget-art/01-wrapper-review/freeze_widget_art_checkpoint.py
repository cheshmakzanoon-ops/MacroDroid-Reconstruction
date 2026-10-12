#!/usr/bin/env python3
"""Freeze the reviewed standalone Widget probe and all preparation evidence."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

HERE = Path(__file__).resolve().parent
FILES = [
    'source/recovered/probe/WidgetMethodProbe.java', 'build_widget_art_probe.py',
    'android_widget_method_probe.py', 'test_android_widget_method_probe.py',
    'probes/widget-method-probe.dex', 'probes/widget-method-probe.json',
    'WIDGET_ART_PROBE.md', 'ANDROID_RUNTIME_SOURCE_ASSESSMENT.md',
    'workflow-proposal.yml', 'input-snapshot.json', 'freeze_widget_art_checkpoint.py',
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source, destination, expected=None):
    expected = expected or sha(source)
    if source.is_symlink() or sha(source) != expected:
        raise RuntimeError('Source identity changed or is symlinked: ' + str(source))
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    if source.stat().st_ino == destination.stat().st_ino or sha(destination) != expected:
        raise RuntimeError('Frozen copy differs or is hardlinked')


def entries(root):
    return [{'path': path.relative_to(root).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}
            for path in sorted(root.rglob('*')) if path.is_file()]


def main():
    result = json.loads((HERE / 'reports/probe-03/build-result.json').read_text())
    controls = json.loads((HERE / 'reports/wrapper-controls-02/result.json').read_text())
    if (result.get('passed') is not True or result.get('android_executed') is not False or
            set(result.get('apks', {})) != {'original', 'candidate'} or
            result.get('disassembled_roundtrip_byte_identical') is not True or
            controls['returncode'] != 0 or controls['android_executed'] is not False or
            controls['wrapper_sha256'] != sha(HERE / 'android_widget_method_probe.py') or
            controls['test_sha256'] != sha(HERE / 'test_android_widget_method_probe.py') or
            'Ran 27 tests' not in (HERE / 'reports/wrapper-controls-02/stderr.txt').read_text()):
        raise RuntimeError('A complete exact preparation and host control result are required')
    if (sha(HERE / 'probes/widget-method-probe.dex') != result['probe']['sha256'] or
            sha(HERE / 'probes/widget-method-probe.json') != result['provenance_sha256'] or
            sha(HERE / 'source/recovered/probe/WidgetMethodProbe.java') != result['source']['sha256']):
        raise RuntimeError('Packaged source or DEX differs from compiled preparation')
    output = HERE / 'checkpoints/01-wrapper-review'
    output.mkdir(parents=True, exist_ok=False)
    for name in FILES:
        copy(HERE / name, output / name)
    source_entries = entries(output)
    evidence_entries = entries(HERE / 'reports')
    evidence = output / 'evidence'
    for row in evidence_entries:
        copy(HERE / 'reports' / row['path'], evidence / row['path'], row['sha256'])
    archive = HERE / 'checkpoints/01-wrapper-review-evidence.tar.gz'
    if archive.exists():
        raise RuntimeError('Evidence archive already exists')
    with tarfile.open(archive, 'w:gz') as stream:
        for row in evidence_entries:
            stream.add(evidence / row['path'], arcname=row['path'], recursive=False)
    remaining = {row['path']: row for row in evidence_entries}
    with tarfile.open(archive, 'r:gz') as stream:
        for member in stream.getmembers():
            row = remaining.pop(member.name)
            data = stream.extractfile(member).read()
            if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
                raise RuntimeError('Archived evidence differs')
    if remaining:
        raise RuntimeError('Archived evidence is incomplete')
    checkpoint = {
        'status': 'COMPILED_REVIEWED_HOST_CONTROLS_PASSED_ANDROID_EXECUTION_PENDING',
        'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Inactive standalone probe preparation; zero actual Android commands, no active source/APK promotion',
        'proposed_repository_path': 'work-in-progress/widget-art/01-wrapper-review',
        'runtime_cases': result['runtime_cases'], 'runtime_cases_count': 8,
        'host_tests_passed': 27, 'host_adb_simulated': True,
        'android_executed': False, 'full_runtime_1_to_1_established': False,
        'app_apk_modified': False, 'app_installed': False,
        'target_method': result['target_method'], 'original_method_sha256': result['original_method_sha256'],
        'probe': result['probe'], 'apks': result['apks'],
        'provenance_sha256': result['provenance_sha256'],
        'wrapper_sha256': controls['wrapper_sha256'], 'test_sha256': controls['test_sha256'],
        'workflow_proposal_sha256': sha(HERE / 'workflow-proposal.yml'),
        'source_unchanged_from_compiled_preparation': True,
        'disassembled_roundtrip_byte_identical': True,
        'scope_limitations': [
            'Actual original/candidate Android execution remains pending',
            'Eight entry/restoration/type-check paths only; no nonempty widget rendering, factory, service or logging paths',
            'VM-generated NPE/CCE wording is not asserted; invalid-label literal is exact',
            'Framework source assessment supports launcher selection, not a claim about a measured runtime outcome',
            'workflow-proposal.yml is an inactive fragment for the existing pinned disposable Android job',
        ],
        'files': source_entries, 'evidence_files': evidence_entries,
        'evidence_bundle': {'path': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive)},
        'archive_members_hash_verified': True,
    }
    path = output / 'checkpoint.json'
    path.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(path), 'sha256': sha(path),
        'source_files': len(source_entries), 'evidence_files': len(evidence_entries),
        'archive': checkpoint['evidence_bundle'], 'wrapper_sha256': checkpoint['wrapper_sha256'],
        'workflow_proposal_sha256': checkpoint['workflow_proposal_sha256']}, indent=2))


if __name__ == '__main__':
    main()
