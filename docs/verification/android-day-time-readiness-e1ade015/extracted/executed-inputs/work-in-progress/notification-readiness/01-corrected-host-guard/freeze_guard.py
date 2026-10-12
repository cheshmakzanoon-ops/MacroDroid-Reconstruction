#!/usr/bin/env python3
"""Freeze the corrected guard, every closed attempt and literal historical replay."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import difflib
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def inventory(folder):
    return {path.relative_to(folder).as_posix(): identity(path)
            for path in sorted(folder.rglob('*')) if path.is_file()
            and '__pycache__' not in path.parts and path.suffix not in ('.pyc', '.pyo')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    workspace, output = args.workspace.resolve(), args.output.resolve()
    stage = ROOT / 'stage-02'
    repository = stage / 'repository'
    focused = stage / 'reports/focused-03'
    historical = stage / 'reports/historical-01'
    result = json.loads((focused / 'result.json').read_text())
    replay = json.loads((historical / 'result.json').read_text())
    actual = inventory(repository)
    if (result['status'] != 'HOST_CONTROLS_PASSED_INACTIVE' or result['exit_code'] != 0
            or result['source_bytes_unchanged'] is not True
            or '\nRan 21 tests in ' not in (focused / 'tests.log').read_text()
            or not (focused / 'tests.log').read_text().endswith('\nOK\n')):
        raise RuntimeError('Exact corrected focused host controls are not closed and passing')
    for name in ('inputs-before.json', 'inputs-after.json'):
        if json.loads((focused / name).read_text()) != actual:
            raise RuntimeError('Source differs from the executed focused controls')
    if replay['status'] != 'BOTH_LITERAL_HISTORICAL_FAILURES_PRESERVED':
        raise RuntimeError('Historical failure replay is not closed')
    for name in ('source-before.json', 'source-after.json'):
        if json.loads((historical / name).read_text()) != actual:
            raise RuntimeError('Source differs from the exact historical replay')
    parent = json.loads((stage / 'parent-source-identities.json').read_text())
    expected_changed = {'tools/parity_journeys/editor_journey.py', 'tools/parity_journeys/observed_journey.py'}
    expected_added = {'tools/parity_journeys/notification_readiness.py', 'tools/parity_journeys/test_notification_readiness.py'}
    if (set(parent) - set(actual) or {name for name in parent if parent[name] != actual[name]} != expected_changed
            or set(actual) - set(parent) != expected_added):
        raise RuntimeError('Guard source changes exceeded the two reviewed existing and two new files')
    output.mkdir(parents=True, exist_ok=False)

    def copy(source, name):
        target = output / name
        if source.is_symlink() or not source.is_file():
            raise RuntimeError('Unexpected checkpoint source: ' + str(source))
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if identity(source) != identity(target):
            raise RuntimeError('Checkpoint copy changed: ' + name)

    def tree(source, prefix):
        for name in inventory(source):
            copy(source / name, prefix + '/' + name)

    external = {name: row for name, row in actual.items() if name.endswith('/evidence.zip')}
    if len(external) != 2:
        raise RuntimeError('Expected exactly two external historical ZIP fixtures')
    for name in actual:
        if name not in external:
            copy(repository / name, 'replay-source/' + name)
        if name in expected_changed | expected_added:
            copy(repository / name, 'repository-overlay/' + name)
    for name in ('parent-checkpoint.json', 'parent-source-identities.json', 'preparation.json',
                 'memory-preparation.json', 'pre-correction-source-identities.json'):
        copy(stage / name, 'preparation/' + name)
    for name in ('prepare_stage.py', 'run_controls.py', 'replay_historical.py', 'DESIGN.md'):
        copy(workspace / 'notification-readiness-forward' / name, 'initial-operations/' + name)
    for name in expected_changed | expected_added:
        copy(workspace / 'notification-readiness-forward/stage-01/repository' / name,
             'initial-working-source/' + name)
    for name in ('prepare_memory_stage.py', 'run_controls.py', 'replay_historical.py', 'freeze_guard.py',
                 'DESIGN.md', 'CORRECTION.md'):
        copy(ROOT / name, name)
    tree(workspace / 'notification-readiness-forward/stage-01/reports/focused-01', 'attempts/01-initial-focused-pass')
    tree(stage / 'reports/focused-02', 'attempts/02-corrected-guard-test-expectation-failure')
    tree(focused, 'reports')
    tree(historical, 'historical-replay')
    (output / 'external-historical-inputs.json').write_text(json.dumps(external, indent=2) + '\n')
    patch = ''
    parent_root = workspace / 'day-time-trigger-forward/checkpoints/02-host-success/replay-source'
    for name in sorted(expected_changed | expected_added):
        before = (parent_root / name).read_text() if name in parent else ''
        after = (repository / name).read_text()
        patch += ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                             fromfile='parent/' + name, tofile='readiness/' + name))
    (output / 'source.patch').write_text(patch)
    (output / 'README.md').write_text('''# Notification readiness: corrected inactive guard

This checkpoint adds a bounded read-only lifecycle observation before the promotion capture in the exact thirteen-screen Day/Time journey. It adds no app input. Report schema 5 requires its exact policy, raw command evidence, first eligible HOME/PID sequence and unique ordered denial boundary. Existing full-frame, crash and zero-pixel checks remain in force.

The final 21 focused tests pass. The initial 15-test passing attempt is retained together with the independently demonstrated command-log placement and wrapper-span defects; CORRECTION.md describes their repairs. The corrected guard's first 21-test attempt retains a test-message failure at an earlier unchanged snapshot guard. The final follow-up changes only that test's synthetic field placement. No Android workflow used either earlier guard.

The exact prior Zero12 complete five-pixel failure and DayTime13 incomplete process failure have both been replayed using this corrected source. Their complete comparison objects are unchanged, as are every original raw input and ZIP. The replay does not supply a new Android run or relabel either failure.

This is a focused host checkpoint. The complete parent-plus-new regression corpus will run through the separately prepared workflow's offline validation before activation, and is also a required step in the device workflow. It is not claimed complete here. The compared APKs remain separately bound by the workflow.

All source versions, operations, closed test attempts, literal historical verdicts and raw-input identities are retained. The two large historical ZIP fixtures are named by exact hashes and durable repository paths instead of duplicated. A separately owned temporary filesystem provided capacity after the workspace filled; the source-copy receipt proves the original overlay inputs stayed unchanged.
''')
    files = [{'path': name, **pin} for name, pin in inventory(output).items()]
    checkpoint = {'status': 'TARGETED_HOST_CONTROLS_PASSED_INACTIVE',
                  'created_utc': datetime.now(timezone.utc).isoformat(), 'android_executed': False,
                  'active_changes': False, 'scope': 'Corrected notification readiness;21 focused controls and exact historical replay',
                  'complete_regression_corpus_executed_here': False,
                  'repo_target': 'work-in-progress/notification-readiness/01-corrected-host-guard',
                  'files': files}
    (output / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    for row in files:
        if identity(output / row['path']) != {key: row[key] for key in ('bytes', 'sha256')}:
            raise RuntimeError('Closed checkpoint changed')
    print(json.dumps({'status': checkpoint['status'], 'files': len(files),
                      'bytes': sum(row['bytes'] for row in files), 'checkpoint': identity(output / 'checkpoint.json')}, indent=2))


if __name__ == '__main__':
    main()
