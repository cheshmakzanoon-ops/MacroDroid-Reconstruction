#!/usr/bin/env python3
"""Freeze corrected workflow evidence once per payload with exact path mapping."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import shutil
import tarfile


def identity(path):
    digest = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        while data := stream.read(1024 * 1024):
            digest.update(data)
            size += len(data)
    return {'bytes': size, 'sha256': digest.hexdigest()}


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--candidate-commit', required=True)
    args = parser.parse_args()
    if len(args.candidate_commit) != 40 or any(c not in '0123456789abcdef' for c in args.candidate_commit):
        raise ValueError('The exact published candidate commit is required')
    source, evidence, output = [path.resolve() for path in (args.source, args.evidence, args.output)]
    result = json.loads((evidence / 'result.json').read_text())
    if result.get('passed') is not True or result.get('status') != 'OFFLINE_TRIGGER_CATEGORY_WORKFLOW_VALIDATED':
        raise ValueError('A complete closed positive offline validation is required')
    workflow = source / '.github/workflows/editor-trigger-category.yml'
    if identity(workflow)['sha256'] != result['workflow_sha256']:
        raise ValueError('Workflow differs from the measured validation')
    originals = json.loads((evidence / 'inputs-before.json').read_text())
    runtime = json.loads((evidence / 'runtime-inputs-before.json').read_text())
    for row in originals + runtime:
        if identity(Path(row['source'])) != {key: row[key] for key in ('bytes', 'sha256')}:
            raise ValueError('Measured source bytes changed: ' + row['source'])
    output.mkdir(parents=True, exist_ok=False)
    files = []

    def copy(path, relative):
        expected = identity(path)
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        if identity(target) != expected or identity(path) != expected:
            raise ValueError('Source changed while copying: ' + str(path))
        files.append({'path': relative, **expected})

    for name in ('prepare_trigger_journey.py', 'verify_trigger_journey.py', 'build_workflow.py',
                 'validate_workflow.py', '.github/workflows/editor-trigger-category.yml',
                 'parent-source-identities.json'):
        copy(source / name, name)
    copy(Path(__file__), 'freeze_trigger_workflow.py')
    copy(evidence / 'result.json', 'offline-validation.json')

    external = {row['sha256']: {key: row[key] for key in ('source', 'path', 'bytes', 'sha256')}
                for row in runtime}
    durable = {
        '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800': 'vendor/original/manifest.json',
        '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182': 'work-in-progress/combined-recovery/05-full-acceptance/apk/manifest.json',
        '6fbed5edaddcfbee99a3ae6e7208c8654c6cb2bedb4ed5cbbf4e154d7d38a745': 'vendor/v9/manifest.json',
    }
    if set(external) != set(durable):
        raise ValueError('Unexpected external runtime input identity')
    for digest, row in external.items():
        row['durable_repository'] = 'https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction.git'
        row['durable_commit'] = (args.candidate_commit if digest == '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'
                                 else 'dbbb89cf4ca65edd3d2c2b96151dadf41aaec514')
        row['durable_manifest'] = durable[digest]
    entries, links, payloads = [], [], {}
    evidence_paths = sorted(evidence.rglob('*'))
    for path in evidence_paths:
        relative = path.relative_to(evidence).as_posix()
        if path.is_symlink():
            links.append({'path': relative, 'target': str(path.readlink()), 'restored_as_symlink': False})
        elif path.is_file():
            row = {'path': relative, **identity(path), 'mode': path.stat().st_mode & 0o777}
            digest = row['sha256']
            if digest in external and row['bytes'] == external[digest]['bytes']:
                row['external_input_sha256'] = digest
            else:
                row['archive_member'] = 'blobs/sha256/' + digest + '.bin'
                payloads.setdefault(digest, (path, row))
            entries.append(row)
    archive = output / 'offline-evidence-blobs.tar.gz'
    with tarfile.open(archive, 'w:gz', format=tarfile.PAX_FORMAT) as target:
        for digest, (path, row) in sorted(payloads.items()):
            raw = path.read_bytes()
            if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != digest:
                raise ValueError('Closed evidence changed before archiving')
            info = tarfile.TarInfo(row['archive_member'])
            info.size, info.mode, info.mtime = len(raw), 0o644, 0
            target.addfile(info, io.BytesIO(raw))
    with tarfile.open(archive, 'r:gz') as target:
        members = target.getmembers()
        if len(members) != len(payloads) or len({member.name for member in members}) != len(members):
            raise ValueError('Unique payload inventory differs')
        for member in members:
            digest = member.name.removeprefix('blobs/sha256/').removesuffix('.bin')
            if digest not in payloads or not member.isfile():
                raise ValueError('Unrecognized or non-regular payload')
            raw = target.extractfile(member).read()
            if len(raw) != payloads[digest][1]['bytes'] or hashlib.sha256(raw).hexdigest() != digest:
                raise ValueError('Archived evidence payload differs')
    files.append({'path': archive.name, **identity(archive)})
    for row in entries:
        if identity(evidence / row['path']) != {key: row[key] for key in ('bytes', 'sha256')}:
            raise ValueError('Closed evidence changed after archiving: ' + row['path'])
    observed_paths = sorted(path.relative_to(evidence).as_posix() for path in evidence.rglob('*')
                            if path.is_file() or path.is_symlink())
    if observed_paths != sorted([row['path'] for row in entries] + [row['path'] for row in links]):
        raise ValueError('Evidence inventory changed during freezing')
    for row in originals + runtime:
        if identity(Path(row['source'])) != {key: row[key] for key in ('bytes', 'sha256')}:
            raise ValueError('Measured original changed during freezing')
    manifest = output / 'offline-evidence-manifest.json'
    save(manifest, {'schema': 2, 'android_executed': False, 'file_count': len(entries), 'files': entries,
                    'unique_archived_payloads': len(payloads), 'inert_symlink_controls': links,
                    'exact_already_published_runtime_inputs': external,
                    'all_source_and_evidence_files_rehashed_before_and_after': True,
                    'all_archive_members_verified': True,
                    'restoration': 'For each regular file, copy its archive_member bytes or exact external_input_sha256 bytes to path with mode; never restore symlink controls automatically.'})
    files.append({'path': manifest.name, **identity(manifest)})
    readme = output / 'README.md'
    readme.write_text('''# Twelve-screen trigger-category observation workflow

This reviewed proposal extends the declared first-use journey by two observed
inputs: the editor's Add Trigger button and the Date/Time category. The category
selector is bound to the preserved actual AddTriggerActivity hierarchy and its
clickable ancestor; the final surface is freshly observed after that input.
The recorder stops without selecting a trigger, saving or executing a macro.

The original APK and the exact combined 5f635e candidate are pinned independently
of artifacts/current. This experiment explicitly uses normal animation scales
of one, with monotonic raw configuration evidence before capture and repeated
settings/identity checks around both runs. It compares twelve full PNG/XML pairs
using the existing zero-pixel rule and binds the paired terminal components.
Motion, timing, crash-free lifecycle and whole-application parity remain outside
this still-observation result. Prior scale-zero and ten-screen results remain
separate and are not relabelled as this new measurement.

The workflow derives from the reviewed Normal03 input-completeness and owned
runtime lifecycle implementation. Both materialized and final verification
independently reconstruct the full ordered inventory from immutable file and
checkpoint pins; missing, empty, duplicate, reordered, extra or rehashed rows
cannot omit a dependency. The full Trigger05 capture guard enforces chronology
and physical-file identity. All declared raw input and output paths are retained
with a deduplicated payload mapping; exact separately published APK/tool bytes
have pinned commit/manifest references. Deliberate symlinks remain inert metadata.

The included offline controls are host/metadata checks, not Android execution.
This package remains inactive until independently reviewed and its exact
workflow is published. Its complete fresh Android result must be evaluated
with the unchanged twelve-screen comparator and preserved input copies.
''')
    files.append({'path': readme.name, **identity(readme)})
    checkpoint = {'status': 'TRIGGER_CATEGORY_WORKFLOW_OFFLINE_CONTROLS_PASSED_REVIEW_PENDING',
                  'created_utc': datetime.now(timezone.utc).isoformat(), 'android_executed': False,
                  'active_changes': False, 'workflow_sha256': identity(workflow)['sha256'],
                  'offline_validation': result, 'evidence_files': len(entries),
                  'unique_archived_payloads': len(payloads), 'files': sorted(files, key=lambda row: row['path'])}
    path = output / 'checkpoint.json'
    save(path, checkpoint)
    print(json.dumps({'checkpoint': str(path), **identity(path), 'files': len(files),
                      'evidence_files': len(entries), 'unique_archived_payloads': len(payloads)}, indent=2))


if __name__ == '__main__':
    main()
