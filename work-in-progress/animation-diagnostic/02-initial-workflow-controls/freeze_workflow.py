#!/usr/bin/env python3
"""Freeze diagnostic source and complete offline evidence with input references."""
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
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--status', required=True)
    parser.add_argument('--note', required=True)
    args = parser.parse_args()
    args.source, args.evidence, args.output = [p.resolve() for p in (args.source, args.evidence, args.output)]
    result = json.loads((args.evidence / 'result.json').read_text())
    workflow = args.source / '.github/workflows/editor-normal-animation.yml'
    if identity(workflow)['sha256'] != result['workflow_sha256']:
        raise ValueError('Workflow no longer matches its actual validation')
    for item in json.loads((args.evidence / 'inputs-before.json').read_text()):
        if identity(Path(item['source'])) != {key: item[key] for key in ('bytes', 'sha256')}:
            raise ValueError('Measured source input changed: ' + item['source'])
    args.output.mkdir(parents=True, exist_ok=False)
    files = []
    def copy(source, relative):
        expected = identity(source)
        target = args.output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if identity(target) != expected or identity(source) != expected:
            raise ValueError('Source changed while freezing')
        files.append({'path': relative, **expected})
    for name in ['prepare_normal_journey.py', 'verify_normal_journey.py', 'build_workflow.py', 'validate_workflow.py',
                 '.github/workflows/editor-normal-animation.yml']:
        copy(args.source / name, name)
    for path in sorted((args.source / 'drafts').rglob('*')) if (args.source / 'drafts').exists() else []:
        if path.is_file():
            copy(path, path.relative_to(args.source).as_posix())
    copy(Path(__file__), 'freeze_workflow.py')
    references = {}
    for row in json.loads((args.evidence / 'runtime-inputs-before.json').read_text()):
        relative = 'private-inputs/' + row['path']
        expected = {key: row[key] for key in ('bytes', 'sha256')}
        if identity(args.evidence / relative) != expected or identity(Path(row['source'])) != expected:
            raise ValueError('Already published APK/tool bytes changed')
        references[relative] = row
    entries, links = [], []
    bundle = args.output / 'offline-evidence.tar.gz'
    with tarfile.open(bundle, 'w:gz', format=tarfile.PAX_FORMAT) as archive:
        for path in sorted(args.evidence.rglob('*')):
            relative = path.relative_to(args.evidence).as_posix()
            if path.is_symlink():
                links.append({'path': relative, 'target': str(path.readlink()), 'restored_as_symlink': False})
                continue
            if not path.is_file() or relative in references:
                continue
            raw = path.read_bytes()
            expected = {'path': relative, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
            entries.append(expected)
            info = tarfile.TarInfo(relative)
            info.size, info.mode, info.mtime = len(raw), 0o644, 0
            archive.addfile(info, io.BytesIO(raw))
    with tarfile.open(bundle, 'r:gz') as archive:
        members = {item.name: item for item in archive.getmembers()}
        if len(members) != len(entries):
            raise ValueError('Evidence archive inventory differs')
        for row in entries:
            item = members[row['path']]
            if not item.isfile():
                raise ValueError('Only inert regular evidence files are permitted')
            raw = archive.extractfile(item).read()
            if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
                raise ValueError('Evidence archive bytes differ')
    files.append({'path': bundle.name, **identity(bundle)})
    manifest = args.output / 'offline-evidence-manifest.json'
    manifest.write_text(json.dumps({'android_executed': False, 'files': entries,
        'inert_symlink_controls': links,
        'already_published_apk_and_tool_inputs_not_duplicated_in_archive': references,
        'references_verified_before_and_after': True}, indent=2) + '\n')
    files.append({'path': manifest.name, **identity(manifest)})
    readme = args.output / 'README.md'
    readme.write_text('# Independent normal-animation diagnostic proposal\n\n' + args.note + '\n\n'
        'This package is inactive until explicitly reviewed and published as an active workflow. '
        'Offline host controls and APK metadata inspection are not Android execution. '
        'The exact current candidate and supplied original APK remain unchanged. '
        'The workflow observes ten full frames per APK with the existing zero-pixel comparison rule; '
        'it does not establish animation timing, crash-free lifecycle, or whole-application parity.\n\n'
        'The offline archive retains every regular test input and output except three already-published '
        'large APK/tool inputs, whose exact identities and source references are retained separately. '
        'Deliberate symlink controls are recorded as inert metadata and never restored automatically.\n')
    files.append({'path': readme.name, **identity(readme)})
    checkpoint = {'status': args.status, 'android_executed': False, 'active_changes': False,
                  'created_utc': datetime.now(timezone.utc).isoformat(), 'note': args.note,
                  'workflow_sha256': identity(workflow)['sha256'], 'offline_validation': result,
                  'evidence_files': len(entries), 'inert_symlinks': len(links),
                  'files': sorted(files, key=lambda row: row['path'])}
    path = args.output / 'checkpoint.json'
    path.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'path': str(path), **identity(path), 'files': len(files),
                      'evidence_files': len(entries)}, indent=2))


if __name__ == '__main__':
    main()
