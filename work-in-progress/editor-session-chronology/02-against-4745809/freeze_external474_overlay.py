"""Freeze the reviewed, tested session-only overlay without activating it."""
from __future__ import annotations
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'checkpoints/02-against-4745809'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(source, relative):
    target = OUT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(source) == sha(target)


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((ROOT / 'external474-input-manifest.json').read_bytes())
    adaptation = json.loads((ROOT / 'external474-adaptation.json').read_bytes())
    proposals = {row['path']: row for row in adaptation['changed_paths']}
    assert set(proposals) == {'tools/parity_journeys/' + name for name in
                              ('post_onboarding.py', 'test_post_onboarding.py', 'POST_ONBOARDING.md')}
    for row in manifest['all_copied_files']:
        original = ROOT / 'external474-inputs' / row['path']
        current = ROOT / 'external474-worktree' / row['path']
        assert sha(original) == row['sha256'] and original.stat().st_size == row['bytes']
        expected = proposals.get(row['path'], {}).get('proposed_sha256', row['sha256'])
        assert sha(current) == expected, row['path']
        copy(original, 'inputs/' + row['path'])
    patch = ''
    for relative in sorted(proposals):
        original, current = ROOT / 'external474-inputs' / relative, ROOT / 'external474-worktree' / relative
        copy(current, 'proposed_files/' + relative)
        patch += ''.join(difflib.unified_diff(original.read_text().splitlines(True), current.read_text().splitlines(True),
                                            fromfile='a/' + relative, tofile='b/' + relative))
    for path in sorted((ROOT / 'external474-reports').rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts:
            copy(path, 'reports/' + str(path.relative_to(ROOT / 'external474-reports')))
    names = ('external474-input-manifest.json', 'external474-adaptation.json', 'external474-fixture-references.json',
             'external474-ledger-tests.log', 'external474-published-guard-recheck.json',
             'external474-published-guard-recheck.log', 'external474-chronology-focused.log',
             'external474-retained-ledger-focused.log', 'external474-integration-tests.log',
             'external474-remaining-recheck.log', 'external474-runtime-review.log',
             'adapt_external474.py', 'recheck_remaining_chronology.py', 'review_external474_runtime.py',
             'freeze_external474_overlay.py')
    for name in names:
        copy(ROOT / name, name)
    test_rows = []
    for filename, count, seconds in (
        ('external474-ledger-tests.log', 12, 4.989),
        ('external474-chronology-focused.log', 26, 19.208),
        ('external474-retained-ledger-focused.log', 12, 3.462),
        ('external474-integration-tests.log', 119, 50.261),
    ):
        data = (ROOT / filename).read_text()
        assert len(re.findall(r'^test_.* \.\.\. ok$', data, re.M)) == count
        assert f'\nRan {count} tests in {seconds:.3f}s\n\nOK\n' in data
        test_rows.append({'log': filename, 'tests': count, 'individual_success_lines': count,
                          'seconds': seconds, 'sha256': sha(ROOT / filename), 'observed_exit_code': 0})
    reproduced = json.loads((ROOT / 'external474-reports/01-distinct-file-chronology-cases/recheck-result.json').read_bytes())
    assert reproduced['status'] == 'FOUR_DISTINCT_FILE_GAPS_REPRODUCED_AND_REJECTED'
    runtime = json.loads((ROOT / 'external474-reports/02-actual-runtime-review/runtime-review.json').read_bytes())
    assert len(runtime['runs']) == 2 and not runtime['new_android_execution_performed']
    result = {'schema': 1, 'status': 'HOST_VALIDATED_INACTIVE_SESSION_CHRONOLOGY_OVERLAY',
              'baseline_commit': manifest['baseline_commit'], 'changed_files': list(proposals.values()),
              'retained_external_paths_byte_identical': ['tools/parity_journeys/' + name for name in
                 ('session_evidence.py', 'test_session_evidence.py', 'recheck_guard_regressions.py', 'SESSION_EVIDENCE.md')],
              'host_gates': test_rows, 'full_discovery_tests': 119, 'new_session_tests': 14,
              'distinct_file_false_positive_cases_rejected': 4, 'wrong_apk_control_rejected_by_both': True,
              'runtime_review': runtime['runs'], 'new_android_execution_performed': False,
              'new_chronology_runtime_gate': 'PENDING_FRESH_CAPTURE', 'active_repository_modified': False}
    (OUT / 'validation-result.json').write_text(json.dumps(result, indent=2) + '\n')
    (OUT / 'proposed-source.patch').write_text(patch)
    readme = '''# Session chronology follow-up retaining external 4745809

This is a **frozen inactive overlay** against commit `47458097056fd023bad8b47b6464978b0d02e85c`. It proposes only `tools/parity_journeys/post_onboarding.py`, `test_post_onboarding.py` and `POST_ONBOARDING.md`. The published `session_evidence.py`, its twelve tests, the four-case reproduction helper and `SESSION_EVIDENCE.md` remain byte-identical. No app/APK, reference plan, animation configuration, shared observed-capture policy or workflow changes are included.

## What the independent review established

The external file ledger works for the three originally reviewed reuse cases. Its twelve host controls pass, and its exact published reproduction shows all three old stale-file false positives now rejected while the wrong installed APK digest control remains rejected. The ledger checks resolved paths, file identities, exact role sets, content hashes and lengths across both variants; equal bytes in distinct observation files remain legitimate.

Four additional synthetic cases demonstrate the boundary of file uniqueness. Each retains 294 distinct in-scope observation files, yet external 474 accepts the altered report:

| Altered recorded evidence | External 474 | Proposed follow-up |
| --- | --- | --- |
| Final endpoint command times moved before the final input | Accepted | Rejected before its captured observation |
| Distinct final capture given the prior capture's earlier interval | Accepted | Rejected because result begins before input finishes |
| Later input times moved before the earlier input | Accepted | Rejected as an out-of-order input acquisition |
| Final identity foreground changes to another component in the same app | Accepted | Rejected because it differs from the captured component |

Both comparators accept the unchanged positive for every case. The wrong installed hash control rejects under both. Every case preserves complete synthetic artifacts in a deterministic ZIP, its member hash manifest, before/after report, both baseline results and both mutated results. These are host tests of recorded evidence, not device captures or cryptographic attestation of an untrusted recorder.

## Narrow proposed behavior

The exact external path-and-inode ledger is evaluated before chronology. Every `SessionRecorder.snapshot` records a versioned absolute monotonic start/finish interval around the full acquisition, including snapshots immediately before input, and preserves a separate raw JSON record. It adds no tap, selector, screenshot transformation or animation setting. The existing bounded XML acquisition retries remain unchanged.

The comparator requires finite non-boolean timing values, successful non-timeout command windows, endpoint commands after their own capture in order, the home identity before the first session input acquisition, each fresh pre-input capture after the prior result/boundary, and each resulting capture after its actual input command finishes. Capture-to-input time remains subject to the existing 15-second freshness budget. Final endpoint evidence follows the final capture and retains the exact installed APK digest and continuous PID checks. The endpoint's resumed component must match its capture, accepting Android's equivalent abbreviated/full activity spelling.

The output result advances to schema 3 to distinguish this mandatory chronology policy. Generic journey capture schema 2 remains the outer report with additional versioned `session_observation` records. A historical capture without those records cannot satisfy the new gate. Timing is not inferred from sample durations or backfilled into old evidence. Full pixels, color metadata and UI hierarchy comparison remain exact, with all startup/crash and whole-app limitations retained.

## Host verification and exact source scope

The proposed session tests pass **26/26**; the retained external ledger tests pass **12/12** against the proposal. The complete workflow discovery command passes **119/119 in 50.261 seconds**, with all 119 individual success lines checked. Fourteen new session test methods cover the remaining timing/component behavior, including nonfinite, boolean, missing, reversed and timeout intervals, stale distinct captures and endpoint component changes. Seven duplicate file-reuse controls from the earlier private prototype were removed in favor of retaining the external controls unchanged.

`validation-result.json` binds all source hashes and exact logs. The two immutable fixture ZIPs needed by unchanged reference-plan tests were referenced from their existing repository paths with hash checks; no ZIP payload was copied for those tests and absolute local symlinks are not published. The older private prototype, failed missing-fixture attempt, independent original reuse reproductions and 114-test result remain in `../01-against-934c654/`; that prototype was never activated over external 474.

## Actual device evidence remains separately scoped

The read-only runtime review verifies every ZIP member and captured comparator source binding for two already published artifacts. It executes only the exact pinned repository comparison code, never an APK or an Android command, and does not duplicate their immutable ZIPs.

Run **38206460588**, captured from 934c654, contains the earlier complete home-to-editor session. Replaying it with the exact external 474 ledger validates all 294 distinct observation files and ten zero-pixel/full-XML matching session pairs. Its original continuous startup comparison remains rejected because the app process changed. The proposed chronology gate rejects that untouched artifact because `session_observation` is absent. That is a pending fresh-capture requirement, not a rewritten historical result or a claim of whole-app parity.

Run **38208764356**, captured from external 474, is a new actual workflow failure. The original stops at `reference-promotion` after five screenshots and notification denial: the next `pidof com.arlosoft.macrodroid` exits 1 with empty stdout and stderr. The candidate completes all sixteen screenshots. Both preserved startup and session comparisons reject the incomplete pair; the exact external replay reproduces that result and the proposed gate also rejects it. This provides no new paired editor-session pass. Complete raw artifacts and lifecycle evidence remain in the bot's existing run archive; the review retains the relevant raw logs and failing command streams. Partial full-image measurements are diagnostic only and cannot override that failure.

The new chronology runtime gate remains **pending a fresh recorded Android capture**. The earlier measured ten-screen TRIGGERS difference and recorded crashes remain unchanged. This overlay does not establish startup parity, absence of crashes, animation parity, saved or executed macros, services, schedules, or complete runtime 1:1.

## Review and reproduction

`inputs/` binds the 30 exact source/fixture/workflow files copied from external 474. `proposed_files/` and `proposed-source.patch` contain only the three proposed replacements. All unchanged dependencies, host logs, complete synthetic evidence, actual artifact reviews and authored helpers are included in the checkpoint. The helpers retain the exact local paths used during this study; immutable repository archive paths and SHA-256 pins are explicit. To reconstruct the private test tree, overlay the three proposed files over those inputs and supply the two fixture archives at the repository-relative paths in `external474-fixture-references.json`.

Run `python -m unittest discover -s tools/parity_journeys -p 'test_*.py' -v` from that reconstructed tree. Do not apply this overlay without checking the declared baseline hashes against the current main branch; concurrent external work must be preserved. `checkpoint.json` declares no automatic active-file mutation. Root review controls any later coherent activation.
'''
    (OUT / 'README.md').write_text(readme)
    files = [{'path': str(path.relative_to(OUT)), 'bytes': path.stat().st_size, 'sha256': sha(path)}
             for path in sorted(OUT.rglob('*')) if path.is_file()]
    checkpoint = {'schema': 1, 'status': 'FROZEN_INACTIVE_SESSION_CHRONOLOGY_OVERLAY',
                  'publication_path': 'work-in-progress/editor-session-chronology/02-against-4745809',
                  'baseline_commit': manifest['baseline_commit'], 'active_files': [],
                  'inactive_proposals': list(proposals.values()), 'files': files, 'file_count': len(files),
                  'total_bytes': sum(row['bytes'] for row in files), 'host_tests': 119,
                  'new_android_execution_performed': False, 'new_chronology_runtime_gate': 'PENDING_FRESH_CAPTURE'}
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), 'sha256': sha(OUT / 'checkpoint.json'),
                      'bytes': (OUT / 'checkpoint.json').stat().st_size, 'file_count': len(files),
                      'total_bytes': checkpoint['total_bytes']}, indent=2))


if __name__ == '__main__':
    main()
