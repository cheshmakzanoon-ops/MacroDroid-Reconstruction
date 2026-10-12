"""Freeze the three-path paired-component correction and its exact host proof."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'checkpoints/03-paired-components'
BASELINE = ROOT / 'checkpoints/02-against-4745809'
WORK = ROOT / 'component-pair-worktree'
NAMES = ('post_onboarding.py', 'test_post_onboarding.py', 'POST_ONBOARDING.md')


def meta(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def copy(path, relative):
    output = OUT / relative
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, output)
    assert meta(path) == meta(output)


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    inputs = json.loads((ROOT / 'component-pair-input-manifest.json').read_bytes())
    assert meta(BASELINE / 'checkpoint.json')['sha256'] == inputs['baseline_checkpoint_sha256']
    proposals, incremental_patch, cumulative_patch = [], '', ''
    for row in inputs['files']:
        baseline = BASELINE / row['source']
        current = WORK / row['path']
        assert meta(baseline) == {key: row[key] for key in ('bytes', 'sha256')}
        copy(baseline, 'inputs/' + row['path'])
        if row['path'] in {'tools/parity_journeys/' + name for name in NAMES}:
            assert meta(current) != meta(baseline)
            external = ROOT / 'external474-inputs' / row['path']
            copy(current, 'proposed_files/' + row['path'])
            proposals.append({'path': row['path'], 'baseline02': meta(baseline),
                              'external474_baseline': meta(external), 'proposed': meta(current)})
            incremental_patch += ''.join(difflib.unified_diff(
                baseline.read_text().splitlines(True), current.read_text().splitlines(True),
                fromfile='a/' + row['path'], tofile='b/' + row['path']))
            cumulative_patch += ''.join(difflib.unified_diff(
                external.read_text().splitlines(True), current.read_text().splitlines(True),
                fromfile='a/' + row['path'], tofile='b/' + row['path']))
        else:
            assert meta(current) == meta(baseline), row['path']
    assert len(proposals) == 3
    for path in sorted((ROOT / 'component-pair-reports').rglob('*')):
        if path.is_file():
            copy(path, 'reports/' + path.relative_to(ROOT / 'component-pair-reports').as_posix())
    for name in ('component-pair-input-manifest.json', 'component-pair-frozen02-repro.log',
                 'component-pair-focused-tests.log', 'component-pair-corrected-replay.log',
                 'component-pair-observed-provenance.log', 'prepare_component_overlay.py',
                 'reproduce_paired_component_gap.py', 'recheck_paired_component_gap.py',
                 'record_final_component_provenance.py', 'freeze_component_overlay.py'):
        copy(ROOT / name, name)
    test_log = (ROOT / 'component-pair-focused-tests.log').read_text()
    assert len(re.findall(r'^test_.* \.\.\. ok$', test_log, re.M)) == 42
    assert '\nRan 42 tests in 19.340s\n\nOK\n' in test_log
    replay = json.loads((ROOT / 'component-pair-reports/02-corrected-replay/recheck-result.json').read_bytes())
    assert replay['status'] == 'PRESERVED_PAIRED_COMPONENT_FALSE_POSITIVE_NOW_REJECTED'
    assert replay['archive_members_verified'] == 584 and replay['source02_unchanged']
    assert replay['source_after'] == meta(WORK / 'tools/parity_journeys/post_onboarding.py')
    provenance = json.loads((ROOT / 'component-pair-reports/03-observed-final-component/provenance.json').read_bytes())
    assert provenance['status'] == 'EXACT_HISTORICAL_FINAL_EDITOR_COMPONENT_BOUND'
    result = {'schema': 1, 'status': 'HOST_VALIDATED_INACTIVE_PAIRED_COMPONENT_OVERLAY',
              'baseline_checkpoint_sha256': inputs['baseline_checkpoint_sha256'],
              'baseline_publication_commit': inputs['baseline_publication_commit'],
              'changed_files': proposals, 'focused_tests': 42, 'session_tests': 30,
              'retained_external_ledger_tests': 12, 'new_test_methods': 4,
              'focused_test_seconds': 19.340, 'observed_test_exit_code': 0,
              'full_union_suite': 'PENDING_SEPARATE_TRIGGER05_INTEGRATION',
              'false_positive_replayed_with_exact_584_member_archive': True,
              'unchanged_positive_accepted_and_mutated_final_rejected': True,
              'semantic_observation_files_verified_in_each_case': 294,
              'captured_editor_component_provenance_run': 38206460588,
              'new_runtime_gate': 'PENDING_FRESH_CAPTURE', 'android_executed': False,
              'active_repository_modified': False, 'full_runtime_1_to_1_established': False}
    (OUT / 'validation-result.json').write_text(json.dumps(result, indent=2) + '\n')
    (OUT / 'incremental-from-session02.patch').write_text(incremental_patch)
    (OUT / 'cumulative-from-external474.patch').write_text(cumulative_patch)
    (OUT / 'README.md').write_text('''# Paired foreground component correction

This is a frozen inactive follow-up to session chronology checkpoint 02. It proposes only the same three files: `post_onboarding.py`, `test_post_onboarding.py`, and `POST_ONBOARDING.md`. The external 4745809 path-and-inode ledger, its twelve tests, shared observed-capture policy, reference plan, workflows, and all app/APK inputs remain unchanged. Neither this checkpoint nor its earlier session02 baseline has been activated by this study.

## Exact false pass retained

The session02 verifier correctly required an endpoint foreground record to match its own capture, but omitted the paired foreground component from its comparison. The preserved synthetic reproduction first sets both final captures and endpoints to the **actually observed EditMacroActivity**, and verifies a passing positive. It then changes only the candidate final capture foreground and its separate endpoint foreground to `.DifferentFinalActivity`. All 294 semantic observation files remain distinct; timestamps, PIDs, installed APK identities, all ten full screenshots and all ten hierarchies stay valid and unchanged. Session02 incorrectly returns `EXACT_POST_ONBOARDING_EDITOR_MATCH_ONLY` again.

The complete before/after reports, literal old results, 584-file deterministic synthetic artifact ZIP and member hash manifest are retained under `reports/01-frozen02-false-positive/`. A separate read-only replay verifies every archive member, exactly reproduces both old results, and shows that this correction accepts the positive and rejects the mutation. This is a host test of recorded evidence; it is not an Android observation or an attestation of an untrusted recorder.

## Narrow correction

Every paired scoped screenshot now compares normalized foreground components in addition to unchanged full RGBA pixels, dimensions, color metadata and full hierarchy. Each result row exposes the original and candidate component strings and `foreground_component_equal`; a component difference makes that row unequal even when pixels/XML match. Abbreviated and fully qualified spellings of the same Android component normalize equally.

The final `editor-after-constraint-back` endpoint additionally requires `com.arlosoft.macrodroid.editscreen.EditMacroActivity`. This is bound to the exact final capture and separate endpoint command in **both variants of preserved run 38206460588**, with the observed enabled/clickable `edit_macro_addTriggerButton` selector. `reports/03-observed-final-component/` retains those four foreground records and two complete hierarchies byte-for-byte, their original archive-member/hash identities, exact resumed lines, and the pinned original journey/ZIP metadata. No component was inferred solely from a screen label or matching image.

The result advances to schema 4. Endpoint-to-own-capture matching, command/capture/input chronology, exact installed identity, process continuity, raw file uniqueness, input guards and the external physical-file ledger are retained. The comparison covers observed activity identities at scoped capture boundaries; it does **not** establish complete activity lifecycle equivalence, startup parity, absence of crashes, animation parity, macro execution, or whole-app 1:1.

## Measured host checks

All **42 focused tests pass in 19.340 seconds**: thirty session tests and all twelve unchanged external ledger tests. Four new methods reject a jointly changed candidate final capture/endpoint, reject the same wrong final class in both variants, detect activity differences at every intermediate paired screen with equal full pixels/XML, and accept equivalent component spelling. The final positive fixture now uses the actually observed editor class. The complete integration suite with the independently corrected Trigger05 overlay is pending a separate immutable follow-up; this checkpoint does not claim that unexecuted result.

The schema-4 Android gate remains **pending a fresh capture**. Historical artifacts and previous schema results are unchanged. The prior startup crashes and 26-pixel TRIGGERS failure remain failures. No screenshot is cropped, masked, rewritten or compared with tolerance.

## Review and integration

`inputs/` contains the thirty exact session02 baseline files; `proposed_files/` contains only the three replacements. Both an incremental patch from session02 and a cumulative patch from external 4745809 are provided. `validation-result.json` binds each old/new hash and actual test count. Check the declared baseline hashes and preserve concurrent changes before any later active integration. `checkpoint.json` deliberately has no automatic active-file mutations.
''')
    files = [{'path': path.relative_to(OUT).as_posix(), **meta(path)} for path in sorted(OUT.rglob('*')) if path.is_file()]
    checkpoint = {'schema': 1, 'status': 'FROZEN_INACTIVE_SESSION_PAIRED_COMPONENT_OVERLAY',
                  'publication_path': 'work-in-progress/editor-session-chronology/03-paired-components',
                  'active_files': [], 'inactive_proposals': proposals, 'files': files,
                  'file_count': len(files), 'total_bytes': sum(row['bytes'] for row in files),
                  'focused_tests': 42, 'new_android_execution_performed': False,
                  'full_union_suite': 'PENDING_SEPARATE_TRIGGER05_INTEGRATION'}
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **meta(OUT / 'checkpoint.json'),
                      'file_count': len(files), 'total_bytes': checkpoint['total_bytes']}, indent=2))


if __name__ == '__main__':
    main()
