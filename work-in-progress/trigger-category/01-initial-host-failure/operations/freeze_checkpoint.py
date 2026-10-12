#!/usr/bin/env python3
"""Freeze an inactive trigger-category stage and its actual host outcome."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil


def identity(path):
    return {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', type=Path, required=True)
    parser.add_argument('--reports', type=Path, required=True)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--note', required=True)
    args = parser.parse_args()
    args.stage, args.reports, args.checkpoint = (p.resolve() for p in (args.stage, args.reports, args.checkpoint))
    args.checkpoint.mkdir(parents=True, exist_ok=False)
    project = args.stage / 'repository'
    prep = json.loads((args.stage / 'preparation.json').read_text())
    result = json.loads((args.reports / 'result.json').read_text())
    if not result['source_bytes_unchanged']:
        raise RuntimeError('Host controls mutated staged source')
    before = json.loads((args.reports / 'inputs-before.json').read_text())
    for relative, expected in before.items():
        if identity(project / relative) != expected:
            raise RuntimeError('Staged input changed after its measured run: ' + relative)
    sources = []
    def put(source, relative):
        destination = args.checkpoint / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        expected = identity(source)
        shutil.copy2(source, destination)
        if identity(source) != expected or identity(destination) != expected:
            raise RuntimeError('Checkpoint changed while copying')
        sources.append({'path': relative, **expected})
    put(args.stage / 'preparation.json', 'preparation.json')
    for change in prep['changes']:
        if identity(project / change['path']) != change['after']:
            raise RuntimeError('Proposed overlay differs from recorded preparation')
        put(project / change['path'], 'repository-overlay/' + change['path'])
    # Exact staged core dependencies permit standalone replay without installing
    # this proposal. Large unchanged observed archives stay pinned by reference.
    for relative in sorted(before):
        path = project / relative
        if path.suffix == '.py' or (relative.startswith('tools/parity_journeys/') and path.suffix == '.json'):
            put(path, 'replay-source/' + relative)
    for source in sorted(args.reports.rglob('*')):
        if source.is_file():
            put(source, 'reports/' + source.relative_to(args.reports).as_posix())
    root = Path(__file__).resolve().parent
    for name in ['prepare.py', 'run_host_controls.py', 'freeze_checkpoint.py']:
        put(root / name, 'operations/' + name)
    note = args.checkpoint / 'README.md'
    note.write_text('# Inactive Date/Time trigger observation\n\n' + args.note + '\n\n'
        'The proposal adds one observed trigger-add tap and one observed Date/Time category tap after the existing ten-screen sequence. '
        'It stops on the next app surface without selecting a trigger or saving or executing a macro. '
        'Full-frame, process, APK, artifact and freshness checks remain required. '
        'No Android run or active workflow change is included in this checkpoint.\n')
    sources.append({'path': 'README.md', **identity(note)})
    checkpoint = {'status': result['status'], 'android_executed': False, 'active_changes': False,
                  'scope': 'Inactive twelve-screen observation proposal and actual host controls only',
                  'note': args.note, 'files': sorted(sources, key=lambda row: row['path'])}
    path = args.checkpoint / 'checkpoint.json'
    path.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'path': str(path), **identity(path), 'files': len(sources)}, indent=2))


if __name__ == '__main__':
    main()
