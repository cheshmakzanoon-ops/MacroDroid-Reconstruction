#!/usr/bin/env python3
"""Freeze a measured, inactive extension of the observed Date/Time journey."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil


def identity(path):
    return {'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', type=Path, required=True)
    parser.add_argument('--reports', type=Path, required=True)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--note', required=True)
    args = parser.parse_args()
    stage, reports, destination = (p.resolve() for p in (args.stage, args.reports, args.checkpoint))
    repository = stage / 'repository'
    before = json.loads((reports / 'inputs-before.json').read_text())
    after = json.loads((reports / 'inputs-after.json').read_text())
    outcome = json.loads((reports / 'result.json').read_text())
    if before != after or outcome['source_bytes_unchanged'] is not True:
        raise ValueError('Measured source changed during host controls')
    actual = {}
    for path in sorted(repository.rglob('*')):
        if path.is_symlink():
            raise ValueError('A staged symlink is not an authored source input')
        if path.is_file():
            if '__pycache__' in path.parts or path.suffix in ('.pyc', '.pyo'):
                raise ValueError('Import tree contains an unreviewed compiled Python file')
            actual[path.relative_to(repository).as_posix()] = identity(path)
    if actual != before:
        raise ValueError('Complete staged source inventory differs after measurement')
    parent = json.loads((stage / 'parent-source-identities.json').read_text())
    if not set(parent) <= set(before):
        raise ValueError('A parent input was removed')
    changes = [{'path': path, 'before': parent.get(path), 'after': value}
               for path, value in sorted(before.items()) if parent.get(path) != value]
    existing = {row['path'] for row in changes if row['before'] is not None}
    if existing != {'tools/parity_journeys/editor_journey.py',
                    'tools/parity_journeys/observed_journey.py'}:
        raise ValueError('The proposed existing-source change set broadened')
    external = {path: value for path, value in before.items() if path.endswith('/evidence.zip')}
    if len(external) != 2 or any(parent[path] != value for path, value in external.items()):
        raise ValueError('Historical archive dependency identities changed')
    destination.mkdir(parents=True, exist_ok=False)
    rows = []

    def put(source, relative):
        expected = identity(source)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if identity(source) != expected or identity(target) != expected:
            raise ValueError('Frozen copy changed: ' + relative)
        rows.append({'path': relative, **expected})

    for name in ['parent-source-identities.json', 'parent-checkpoint.json', 'derivation.patch']:
        put(stage / name, name)
    for name in ['correction.json', 'CORRECTION.md']:
        if (stage / name).is_file():
            put(stage / name, name)
    preparation = {'parent_checkpoint': identity(stage / 'parent-checkpoint.json'),
                   'changes': changes, 'external_historical_archives': external,
                   'android_executed': False, 'active_changes': False}
    save(destination / 'preparation.json', preparation)
    rows.append({'path': 'preparation.json', **identity(destination / 'preparation.json')})
    for row in changes:
        put(repository / row['path'], 'repository-overlay/' + row['path'])
    for relative in sorted(before):
        if relative not in external:
            put(repository / relative, 'replay-source/' + relative)
    for path in sorted(reports.rglob('*')):
        if path.is_file():
            put(path, 'reports/' + path.relative_to(reports).as_posix())
    for path in sorted((stage / 'syntax-preflight').rglob('*')):
        if path.is_file():
            put(path, 'syntax-preflight/' + path.relative_to(stage / 'syntax-preflight').as_posix())
    operations = Path(__file__).resolve().parent
    for name in ['prepare_stage.py', 'derive_day_time_guard.py', 'run_host_controls.py', 'freeze_checkpoint.py']:
        put(operations / name, 'operations/' + name)
    if (stage / 'correction.json').is_file():
        put(operations / 'correct_plan_guard.py', 'operations/correct_plan_guard.py')
    note = destination / 'README.md'
    note.write_text('# Observed Day/Time trigger: inactive thirteen-screen extension\n\n' + args.note + '\n\n'
        'The exact twelve-screen prefix gains one Day/Time type tap. Both unchanged Android captures '
        'from run 38216299675 identify its nearest clickable row at (184, 626). The next app surface '
        'is recorded without assuming its component or controls. The terminal component must still '
        'be stable, owned by the app and equal between the compared runs. No configuration is '
        'confirmed and no macro is saved or executed.\n\n'
        'Only editor_journey.py and observed_journey.py change among existing staged sources. '
        'The new adapter validates the exact four-level observed row ancestry. Host controls retain '
        'strict full-frame comparison, process identity, ordered acquisition, fresh input, physical '
        'artifact uniqueness and explicit crash scope. The host outcome is recorded literally; '
        'these synthetic controls do not establish an Android journey result.\n\n'
        'For private replay, copy replay-source/ into a new directory and obtain the two exact '
        'historical evidence.zip dependencies recorded in preparation.json. Run the command in '
        'reports/result.json with the new directory as its repository. Ordinary per-test temporary '
        'fixtures are disposable; their deterministic generators and complete measured test log '
        'are included. All actual Android observation fixtures remain byte-exact.\n\n'
        'syntax-preflight/ preserves the isolated file emitted by the explicit py_compile syntax '
        'check, with its receipt. That file is outside the executable import tree and is not an '
        'authored-source or runtime dependency.\n')
    rows.append({'path': 'README.md', **identity(note)})
    checkpoint = {'status': outcome['status'], 'created_utc': datetime.now(timezone.utc).isoformat(),
                  'android_executed': False, 'active_changes': False,
                  'scope': 'Inactive thirteen-screen observation proposal and actual host controls',
                  'note': args.note, 'files': sorted(rows, key=lambda row: row['path'])}
    save(destination / 'checkpoint.json', checkpoint)
    print(json.dumps({'path': str(destination / 'checkpoint.json'),
                      **identity(destination / 'checkpoint.json'), 'files': len(rows),
                      'status': checkpoint['status']}, indent=2))


if __name__ == '__main__':
    main()
