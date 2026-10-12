#!/usr/bin/env python3
"""Freeze the 19-path inactive integration and its closed source controls."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent
GOOD = BASE / 'reports/07-source-and-validator-controls'
OUT = BASE / 'checkpoints/04-source-acceptance-integration'


def identity(path):
    with path.open('rb') as stream: digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def link_tree(source, target):
    for path in sorted(source.rglob('*')):
        assert not path.is_symlink()
        if path.is_file():
            destination = target / path.relative_to(source); destination.parent.mkdir(parents=True, exist_ok=True)
            os.link(path, destination)


def main():
    result = json.loads((GOOD / 'result.json').read_text())
    assert result['passed'] is True and result['focused_tests'] == 43 and result['skips'] == 0
    assert result['existing_controls_byte_and_job_exact'] == 78 and result['source_paths'] == 19
    assert result['new_numeric_controls'] == 13 and result['prior_validator_faults_rejected'] == 6
    bindings = json.loads((GOOD / 'source-bindings.json').read_text())['approved_paths']
    assert len(bindings) == 19 and len({row['path'] for row in bindings}) == 19
    for row in bindings:
        assert identity(GOOD / 'view' / row['path']) == row['candidate']
        assert identity(BASE / 'overlay-01/project' / row['path']) == row['candidate']
    for stream in ('stdout', 'stderr'):
        assert identity(GOOD / ('focused-tests.' + stream + '.log')) == result['test_command'][stream]
    commands = [json.loads(line) for line in (GOOD / 'java-selector-command-streams.jsonl').read_text().splitlines()]
    assert len(commands) == 11 and commands[0]['returncode'] == 0
    assert sum(row['returncode'] == 0 for row in commands) == 2
    assert all(row['timeout_seconds'] in (30, 60) for row in commands)
    failed = json.loads((BASE / 'reports/06-source-and-validator-controls/result.json').read_text())
    assert failed['passed'] is False and failed['test_command']['returncode'] == 2
    failed_log = (BASE / 'reports/06-source-and-validator-controls/focused-tests.stderr.log').read_text()
    assert 'Ran 43 tests' in failed_log and 'FAILED (failures=1)' in failed_log
    review = json.loads((BASE / 'reports/05-numeric-report-guard-review/result.json').read_text())
    assert review['concrete_false_acceptances'] == 6

    OUT.mkdir(parents=True, exist_ok=False)
    source_changes = []
    for row in bindings:
        source = GOOD / 'view' / row['path']; target = OUT / 'project' / row['path']
        target.parent.mkdir(parents=True, exist_ok=True); os.link(source, target)
        source_changes.append({**row, 'source': 'project/' + row['path']})
    for name, source in [('report-guard-review', BASE / 'reports/05-numeric-report-guard-review'),
                         ('first-source-test-attempt', BASE / 'reports/06-source-and-validator-controls'),
                         ('source-controls-pass', GOOD)]:
        link_tree(source, OUT / 'evidence' / name)
    for name in ('freeze_source_controls.py', 'run_source_controls.py', 'review_numeric_report_guards.py'):
        (OUT / name).write_bytes((BASE / name).read_bytes())
    (OUT / 'source.patch').write_bytes((GOOD / 'source.patch').read_bytes())
    (OUT / 'overlay-preparation.json').write_bytes((BASE / 'overlay-01/preparation.json').read_bytes())
    (OUT / 'README.md').write_text('''# DayTrigger.r0: inactive acceptance integration

This checkpoint contains exactly the approved 19 application/build/test source paths. It remains inactive. The [source delta](source.patch), original baseline identities and all candidate bytes are recorded by `checkpoint.json`. The existing application and signed candidate stay unchanged until a separate, reviewed hosted WIP job completes every required build and acceptance gate.

The [focused run](evidence/source-controls-pass/result.json) passed 43 tests with no skips on 2026-10-12 from 08:44:54.938911 to 08:45:07.366911 UTC. Thirty-five new numeric tests run alongside all eight unchanged Widget catalog tests. The exact 54 existing literal mutations plus 24 Widget catalog mutations produce byte-identical prepared jobs, in the same order; thirteen new numeric mutations are appended, giving 91. The [complete prepared inventory](evidence/source-controls-pass/mutation-inventory.json) binds each source, mutation hash and required case label. These are preparation and guard checks; they do not claim execution of the 91 complete UI fault runs.

## Rejection controls and preserved failures

The real `ExtractOracle.selection` implementation executes against the integrated registry and dependency declaration. It selects 1,243 registered methods and three uncredited getters, 1,246 total methods in 607 classes. Actual Java controls reject duplicate registry entries, duplicate dependencies, unregistered consumers, dependency/recovery overlap, extra fields, a boolean schema, malformed provenance and an invalid method descriptor. The real extraction entry point also rejects an unpinned APK before replacing an existing fixture. All eleven Java child commands and their complete streams are retained in [the command ledger](evidence/source-controls-pass/java-selector-command-streams.jsonl).

The [report review](evidence/report-guard-review/result.json) preserves six concrete false acceptances in the earlier private validator: another primary method name, boolean method credit, a duplicate dependency entry, a boolean zero count, and deleted per-method coverage arrays under either original or rebuilt summary counters. The actual numeric execution report itself was not changed or invalidated. The corrected validator requires exact primary/dependency identity, integer counters, four unique method rows, per-method credit, complete offset/edge lists and counts consistent with those rows. The [replay](evidence/source-controls-pass/validator-replay.json) rejects all six modified reports while retaining acceptance of every unchanged actual positive and thirteen Java/two D8 fault report from the [targeted integration](../05-targeted-integration/README.md).

The first focused test run is retained at [first-source-test-attempt](evidence/first-source-test-attempt/result.json). Its one failure was an over-specific test expectation: the deliberately invalid branch list was also unsorted, so the validator rejected its ordering before checking the nonexistent destination. The follow-up sorts that synthetic list to reach the intended destination check. No production rejection rule or observed outcome was relaxed.

## Required later acceptance

The source changes preserve the active interpreter, existing VariableValue public contracts and every earlier recovery mapping. Only `DayTrigger.r0` gains recovered-method credit. `UiParityTests` loads the three original getter dependencies separately and requires the exact primary/dependency instruction and conditional-edge coverage. The fresh original fixture remains test-only.

The existing 16 acceptance gates and their timeouts stay intact. The UI fault gate runs all 91 Java controls and restores the full positive UI report exactly. It then independently requires two actual production D8/transplant faults, using the exact retained classes compiled by the corresponding UI faults. Before any numeric control can pass, the positive transplant's complete instruction listing must match the freshly signed APK, and the getter partition must match that APK's exact member bytes. The numeric report, provenance rejections and final source/class/fixture/APK restoration are retained separately and bound into the final acceptance evidence inventory.

Full UI execution, all 91 Java fault executions, current signed-primary packaging and the complete 16-gate acceptance remain pending at this checkpoint. The hosted proposal will materialize the exact immutable baseline plus this delta and verify a precomputed complete input manifest; no full local source tree or APK was copied for these controls.
''')
    files = [{'path': p.relative_to(OUT).as_posix(), **identity(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
    checkpoint = {'schema': 1, 'status': 'FROZEN_INACTIVE_DAY_SOURCE_INTEGRATION_WITH_43_FOCUSED_TESTS',
                  'created_utc': datetime.now(timezone.utc).isoformat(),
                  'repo_target': 'work-in-progress/day-trigger-numeric/06-source-integration',
                  'active_files': [], 'source_changes': source_changes, 'files': files}
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
                      'files': len(files), 'bytes_total': sum(row['bytes'] for row in files),
                      'source_changes': len(source_changes), 'repo_target': checkpoint['repo_target']}, indent=2))


if __name__ == '__main__': main()
