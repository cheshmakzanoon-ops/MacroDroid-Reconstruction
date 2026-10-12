"""Freeze the closed exact Trigger05/session03 integration result without activation."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
STUDY = ROOT / 'union-trigger05-session03'
OUT = ROOT / 'checkpoints/04-trigger05-session03-union'
TRIGGER = ROOT.parent / 'trigger-catalog-forward/checkpoints/05-physical-identity-host-success'
SESSION = ROOT / 'checkpoints/03-paired-components'
REPO = ROOT.parent / 'MacroDroid-Reconstruction'


def meta(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def copy(source, relative):
    destination = OUT / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    assert meta(source) == meta(destination)


def main():
    result = json.loads((STUDY / 'result.json').read_bytes())
    assert result['status'] == 'EXACT_TRIGGER05_SESSION03_UNION_HOST_VALIDATED'
    assert result['full_suite_tests'] == 148 and result['paired_component_archive_members_replayed'] == 584
    assert result['all_union_inputs_unchanged'] and result['all_current_main_parity_inputs_unchanged']
    assert meta(TRIGGER / 'checkpoint.json')['sha256'] == result['trigger_checkpoint_sha256']
    assert meta(SESSION / 'checkpoint.json')['sha256'] == result['session_checkpoint_sha256']
    assert (STUDY / 'inputs-before.json').read_bytes() == (STUDY / 'inputs-after.json').read_bytes()
    inputs = json.loads((STUDY / 'inputs-after.json').read_bytes())
    for relative, expected in inputs.items():
        assert meta(STUDY / 'worktree' / relative) == expected
    log = (STUDY / 'full-union-tests.log').read_text()
    assert len(re.findall(r'^test_.* \.\.\. ok$', log, re.M)) == 148
    assert '\nRan 148 tests in ' in log and log.endswith('\nOK\n')
    OUT.mkdir(parents=True, exist_ok=False)
    for relative in sorted(inputs):
        if not relative.startswith('docs/'):
            copy(STUDY / 'worktree' / relative, 'replay-source/' + relative)
    assert len([path for path in inputs if not path.startswith('docs/')]) == 64
    for path in sorted(STUDY.rglob('*')):
        if path.is_file() and 'worktree' not in path.relative_to(STUDY).parts:
            copy(path, 'reports/' + path.relative_to(STUDY).as_posix())
    for name in ('validate_trigger05_union.py', 'freeze_trigger05_union.py', 'union-trigger05-session03-driver.log'):
        copy(ROOT / name, name)
    copy(ROOT / 'recheck_paired_component_gap.py', 'recheck_paired_component_gap.py')
    old = json.loads((TRIGGER / 'preparation.json').read_bytes())
    changed = {row['path']: row for row in old['changes']}
    session = json.loads((SESSION / 'checkpoint.json').read_bytes())
    for proposal in session['inactive_proposals']:
        assert proposal['path'] not in changed
        changed[proposal['path']] = {'path': proposal['path'], 'before': proposal['external474_baseline'],
                                     'after': proposal['proposed']}
    assert len(changed) == 20
    patch, paths = '', []
    for relative, row in sorted(changed.items()):
        baseline = REPO / relative
        current = STUDY / 'worktree' / relative
        assert (meta(baseline) if baseline.exists() else None) == row['before']
        assert meta(current) == row['after']
        paths.append(row)
        if current.suffix in ('.py', '.md', '.json', '.xml', '.txt'):
            before = baseline.read_text().splitlines(True) if baseline.exists() else []
            patch += ''.join(difflib.unified_diff(before, current.read_text().splitlines(True),
                fromfile='a/' + relative if baseline.exists() else '/dev/null', tofile='b/' + relative))
    (OUT / 'proposed-text-diff-from-current.patch').write_text(patch)
    (OUT / 'union-proposal-paths.json').write_text(json.dumps(paths, indent=2) + '\n')
    seconds = result['host_test_result']['reported_seconds']
    (OUT / 'README.md').write_text(f'''# Exact Trigger05 and session03 integration

This immutable host proof combines the **64 exact replay-source files from Trigger05** with **only the three frozen session03 replacements**. Current main's entire parity source inventory matched Trigger05's declared baseline before the overlay, all seventeen Trigger changes retained their old/new hash or absence guards, and each session replacement matched its external474 baseline in both the Trigger tree and current main. No active repository file was changed by this study.

The complete workflow command `python -B -m unittest discover -s tools/parity_journeys -p 'test_*.py' -v` passed **148/148 tests in {seconds:.3f} seconds**, exit 0, within the recorded 300-second bound. All 148 individual success lines and the final unittest count were independently checked. This is the exact union source, including the original external path/inode ledger and all retained concurrent reference/session code.

The complete suite includes the demonstrated component, stale-capture and physical-file rejection controls: jointly changing the candidate final capture/endpoint component, equal wrong final components in both variants, every intermediate paired component mismatch, equivalent Android component spelling, deleted terminal artifacts replaced by a prior capture, independent files with pre-input timestamps, physical PID-artifact hard links, cross-run hard links, and deleted endpoint evidence reused from home. `reports/host-test-result.json` identifies the actual successful test lines. Ten/twelve variants remain covered by the shared guard's retained tests.

After that full suite, a separate replay against the **same union imports** verifies all 584 members of the immutable session03 synthetic archive, literally reproduces the session02 positive and false-pass outputs, accepts the valid positive with the correction, and rejects the candidate's different final Activity. All 294 semantic observation files remain distinct. The complete archive and old results remain in session03; this follow-up preserves new replay outputs and pins without another archive payload copy.

All 66 union input/fixture hashes are identical before and after testing. The two existing historical fixture ZIPs were hash-verified and referenced by local symlinks for the test only; their bytes are not duplicated in this capsule. All current main parity file hashes also remain identical, and both frozen input capsules are reverified after the test. A docs-only Git head advance, if any, is recorded separately from source identity.

`replay-source/` preserves all 64 final source and small fixture files. `reports/preparation.json` supplies the two immutable repository ZIP paths/hashes. `proposed-text-diff-from-current.patch` and `union-proposal-paths.json` describe the twenty potential parity paths: the seventeen separately reviewed Trigger changes and three session changes. Existing-file and new-file absence guards must still be checked against main before a later activation. `checkpoint.json` contains no automatic active mutation.

This is a **host integration success**, not a fresh Android run. The corrected schema-4 session gate and any new twelve-screen or normal-animation scope still require their own actual capture evidence. Historical crashes, startup rejection and the measured 26-pixel TRIGGERS difference remain unchanged. Full pixels, XML and foreground components are compared without masks or tolerance; complete app or activity-lifecycle 1:1 is not established.
''')
    files = [{'path': path.relative_to(OUT).as_posix(), **meta(path)}
             for path in sorted(OUT.rglob('*')) if path.is_file()]
    checkpoint = {'schema': 1, 'status': 'FROZEN_HOST_VALIDATED_TRIGGER05_SESSION03_UNION',
                  'publication_path': 'work-in-progress/editor-session-chronology/04-trigger05-session03-union',
                  'active_files': [], 'inactive_union_proposals': paths,
                  'trigger_checkpoint_sha256': result['trigger_checkpoint_sha256'],
                  'session_checkpoint_sha256': result['session_checkpoint_sha256'],
                  'files': files, 'file_count': len(files), 'total_bytes': sum(row['bytes'] for row in files),
                  'full_suite_tests': 148, 'android_executed': False,
                  'new_runtime_gate': 'PENDING_FRESH_CAPTURE'}
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **meta(OUT / 'checkpoint.json'),
                      'file_count': len(files), 'total_bytes': checkpoint['total_bytes']}, indent=2))


if __name__ == '__main__':
    main()
