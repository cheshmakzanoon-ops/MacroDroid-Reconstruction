"""Freeze the private 934c654-based prototype before adapting external 4745809."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'checkpoints/01-against-934c654'
CHANGED = ['tools/parity_journeys/' + name for name in
           ('post_onboarding.py', 'test_post_onboarding.py', 'POST_ONBOARDING.md')]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy(src, rel):
    dest = OUT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    assert sha(src) == sha(dest)


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    source_manifest = json.loads((ROOT / 'input-manifest.json').read_bytes())
    for row in source_manifest['all_copied_files']:
        source = ROOT / 'inputs' / row['path']
        assert source.stat().st_size == row['bytes'] and sha(source) == row['sha256']
        copy(source, 'inputs/' + row['path'])
    proposals = []
    patch = ''
    for rel in CHANGED:
        before, after = ROOT / 'inputs' / rel, ROOT / 'worktree' / rel
        copy(after, 'proposed_files/' + rel)
        proposals.append({'path': rel, 'baseline_sha256': sha(before),
                          'proposed_sha256': sha(after), 'bytes': after.stat().st_size})
        patch += ''.join(difflib.unified_diff(before.read_text().splitlines(True),
                                            after.read_text().splitlines(True),
                                            fromfile='a/' + rel, tofile='b/' + rel))
    for path in sorted((ROOT / 'reports').rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts:
            copy(path, str(path.relative_to(ROOT)))
    for name in ('input-manifest.json', 'reproduce_existing_cases.py', 'independent-reproduction.log',
                 'targeted-tests-01.log', 'targeted-tests-02.log', 'integration-tests.log',
                 'integration-tests-02.log', 'link_test_fixtures.py', 'fixture-linking.log',
                 'fixture-references.json', 'replay_external_session.py', 'actual-session-replay.log',
                 'freeze_historical_prototype.py'):
        copy(ROOT / name, name)
    log = (ROOT / 'integration-tests-02.log').read_text()
    assert len(re.findall(r'^test_.* \.\.\. ok$', log, re.M)) == 114
    assert '\nRan 114 tests in 72.638s\n\nOK\n' in log
    # The exact failed-fixture attempt used the same final Python input bytes.
    for name in ('post_onboarding.py', 'test_post_onboarding.py'):
        assert sha(ROOT / 'reports/05-full-discovery-missing-fixtures' / name) == sha(ROOT / 'worktree/tools/parity_journeys' / name)
    result = {'schema': 1, 'status': 'HOST_INTEGRATION_PASSED_INACTIVE_PROTOTYPE',
              'command': ['python', '-m', 'unittest', 'discover', '-s', 'tools/parity_journeys', '-p', 'test_*.py', '-v'],
              'working_directory': str(ROOT / 'worktree'), 'observed_command_exit_code': 0,
              'tests_run': 114, 'individual_test_success_lines': 114, 'seconds': 72.638,
              'log_sha256': sha(ROOT / 'integration-tests-02.log'),
              'source_unchanged_since_preserved_failed_fixture_attempt': True,
              'android_executed': False, 'active_files_changed': False,
              'new_chronology_runtime_result': 'PENDING_FRESH_CAPTURE',
              'superseding_external_source': '47458097056fd023bad8b47b6464978b0d02e85c',
              'activation_status': 'HISTORICAL_PRIVATE_PROTOTYPE_ONLY; preserve external ledger and rebase remaining chronology guards'}
    (OUT / 'integration-result.json').write_text(json.dumps(result, indent=2) + '\n')
    (OUT / 'proposed-source.patch').write_text(patch)
    readme = '''# Private session chronology prototype against 934c654

This immutable checkpoint preserves the independent review and first private correction of the post-onboarding session evidence gate. It is **inactive**. External commit `47458097056fd023bad8b47b6464978b0d02e85c` arrived while the correction was being validated and adds a stronger session-wide resolved-path and inode ledger. That external change is retained unchanged in the repository. This older prototype must not replace it. A follow-up will retain that ledger and adapt only the remaining component and timing guards.

## Findings and proposed checks

The independently hash-copied historical source is commit `934c6543dce0897975f52457717b3a70bd27ce00`. The original comparator accepted three preserved synthetic failures after the actual final identity or immediate input files had been removed and replaced with earlier observations, including resolved dot aliases. A wrong installed APK digest remained rejected. `reports/01-independent-reproduction/independent-reproduction.json` records independent replay of the publisher's four exact cases; all results reproduce. Their complete original evidence is preserved at `docs/verification/editor-session-review/01-read-only-guard-gaps/`.

The private prototype adds session-wide resolved-path uniqueness, ordered finite command intervals, explicit absolute observation intervals on every captured snapshot, after-input result ordering, and endpoint component continuity. It keeps the complete pixel/XML comparison, installed identity, environment, stable PID and input-selector checks. Equal bytes in distinct new observation files remain valid. This prototype's path-only ledger is superseded by the external path-and-inode ledger; the additional chronology checks are separate.

The existing session capture stores a sample duration but no absolute screenshot acquisition interval. The proposed recorder therefore writes `session_observation` with version 1 and host monotonic start/finish times around every snapshot, including pre-input snapshots. It changes no app, selector, tap, screenshot or XML content. The verifier requires those intervals, rejects missing/invalid/nonfinite/bool values, requires endpoint commands after the captured endpoint, orders inputs after the prior boundary and result captures after their input, and binds the endpoint foreground component to its snapshot. A fresh Android run is required to satisfy this proposed policy.

## Preserved validation

The initial path/command-order slice passed 27 focused session tests. The explicit capture-chronology slice passed 33 focused tests. Both exact intermediate sources and logs are retained in numbered report directories. The final source includes the stricter boolean/schema rejection control.

The first complete parity-tool discovery ran 114 tests: 112 passed and two errored because the small private source copy omitted two existing immutable ZIP fixtures used by the unchanged reference-plan tests. The exact failure, final Python sources and traceback remain in `reports/05-full-discovery-missing-fixtures/`. No implementation was altered to address that fixture issue. `link_test_fixtures.py` verified the two already published archive hashes and made local read-only fixture references without copying archive payloads. Their exact repository paths and hashes are recorded in `fixture-references.json`; absolute local symlinks are intentionally not part of this checkpoint.

The required full discovery then exited 0: **114 tests in 72.638 seconds**, with all 114 individual success lines present. The final Python source bytes equal the preserved first-discovery source bytes. `integration-result.json` binds that result to its exact log and source proposal. No Android command was executed by these host tests.

## Actual historical device evidence

The separate read-only replay binds run `38206460588`, captured from commit `934c6543dce0897975f52457717b3a70bd27ce00`. Its original ZIP is already published at `docs/verification/editor-journey/run-38206460588-attempt-1/evidence.zip`: 11,576,977 bytes, SHA-256 `d22377dacd276c2c8ab2d52bfa639a912d1871c90757ebefc71af16d106cdff6`. The replay checks all 2,034 member identities and all nine historical source pins. Its exact historical comparator result reproduces `EXACT_POST_ONBOARDING_EDITOR_MATCH_ONLY`. Independent full RGBA and XML decoding finds ten zero-pixel-difference session pairs. The earlier continuous-startup report remains `REJECTED` because the app PID changed. This is the declared home-to-empty-editor catalog scope after onboarding, not startup, crash-free or complete runtime parity.

The proposed chronology comparator rejects that same untouched historical report because `session_observation` is absent. The missing timing evidence is not invented or backfilled. `reports/04-actual-external-session/` retains both exact replays, independent image findings, raw command-window inspection, archive/source binding and logs. This does not change any historical status; it establishes that the new proposed gate is pending a fresh recorded capture. The complete raw artifact is referenced rather than copied again.

## Reproduction and publication

The input manifest binds the 26 source/fixture/workflow files copied for this study. Apply only the three files in `proposed_files/` over those historical inputs to reconstruct this inactive prototype. The full host command is recorded in `integration-result.json`. Supply the two immutable fixture ZIPs at their recorded repository-relative paths before running the unchanged reference tests. The included helpers preserve the exact local execution paths used for this study; the archive/source pins and report bindings remain explicit.

`proposed-source.patch` is review evidence against 934c654, not an instruction to overwrite active 4745809. `checkpoint.json` declares no active files. All complete reports, prior failed attempts, authored replay/freezing helpers, source proposals, source baselines and host logs are hash-bound by this checkpoint. The frozen current ten-screen failure, including its 26 TRIGGERS pixels and recorded crashes, is unchanged.
'''
    (OUT / 'README.md').write_text(readme)
    files = [{'path': str(path.relative_to(OUT)), 'bytes': path.stat().st_size, 'sha256': sha(path)}
             for path in sorted(OUT.rglob('*')) if path.is_file()]
    manifest = {'schema': 1, 'status': 'FROZEN_INACTIVE_SUPERSEDED_BASELINE_PROTOTYPE',
                'publication_path': 'work-in-progress/editor-session-chronology/01-against-934c654',
                'baseline_commit': source_manifest['base_commit'], 'superseding_external_commit': result['superseding_external_source'],
                'active_files': [], 'inactive_proposals': proposals, 'android_executed': False,
                'full_runtime_1_to_1_established': False, 'files': files, 'file_count': len(files),
                'total_bytes': sum(row['bytes'] for row in files)}
    (OUT / 'checkpoint.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), 'sha256': sha(OUT / 'checkpoint.json'),
                      'bytes': (OUT / 'checkpoint.json').stat().st_size,
                      'file_count': len(files), 'total_bytes': manifest['total_bytes']}, indent=2))


if __name__ == '__main__':
    main()
