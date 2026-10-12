"""Build only a private chronology overlay while retaining external ledger bytes."""
from pathlib import Path
import ast
import hashlib
import json

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'external474-worktree/tools/parity_journeys'


def replace_once(source, before, after):
    if source.count(before) != 1:
        raise ValueError('Expected one exact frozen source fragment: ' + before[:80])
    return source.replace(before, after)


def main():
    manifest = json.loads((ROOT / 'external474-input-manifest.json').read_bytes())
    for row in manifest['all_copied_files']:
        path = ROOT / 'external474-worktree' / row['path']
        if hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Private baseline changed: ' + row['path'])
    source = (ROOT / 'worktree/tools/parity_journeys/post_onboarding.py').read_text()
    source = replace_once(source, 'from robust_capture import EvidenceRecorder\n',
                          'from robust_capture import EvidenceRecorder\nfrom session_evidence import verify_session_evidence\n')
    start, end = source.index('def claim_artifacts('), source.index('def command_window(')
    source = source[:start] + source[end:]
    source = replace_once(source, 'def checked_identity(folder, run, shot, proof, seen=None):\n    if seen is None:\n        seen = set()\n',
                          'def checked_identity(folder, run, shot, proof):\n')
    source = replace_once(source, 'def checked_transition(folder, run, prior, transition, step, anchor, prior_state, proof, seen, earliest):',
                          'def checked_transition(folder, run, prior, transition, step, anchor, prior_state, proof, earliest):')
    lines = source.splitlines(True)
    ranges = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'claim_artifacts':
            ranges.append((node.lineno - 1, node.end_lineno))
    if len(ranges) != 5:
        raise ValueError('Expected five superseded path-only claim calls')
    for start, end in sorted(ranges, reverse=True):
        del lines[start:end]
    source = ''.join(lines)
    source = replace_once(source, "result = {'schema': 2,", "result = {'schema': 3,")
    source = replace_once(source, "'evidence_policy': 'Distinct session observations with ordered captures, inputs and endpoints',",
                          "'evidence_policy': 'Ordered captures, inputs and endpoints with the retained external session evidence ledger',")
    source = replace_once(source,
        "        # Share resolved identities across both variants and every session role.\n        # Equal bytes in distinct fresh files are valid; one file reused is not.\n        seen = set()\n", '')
    source = replace_once(source,
        "            initial_window = checked_identity(folder, run, run['screens'][start], proof, seen)\n            final_window = checked_identity(folder, run, run['screens'][-1], proof, seen)\n",
        "        # Retain the published path-and-inode ledger and its exact role sets.\n        # Register distinct observations before inspecting their chronology.\n        result['evidence_identity_check'] = verify_session_evidence(folder, runs, start, proof)\n        for run in runs:\n            initial_window = checked_identity(folder, run, run['screens'][start], proof)\n            final_window = checked_identity(folder, run, run['screens'][-1], proof)\n")
    source = replace_once(source, 'step, anchor, series[-1], proof, seen, previous_finish)',
                          'step, anchor, series[-1], proof, previous_finish)')
    ast.parse(source)
    (DEST / 'post_onboarding.py').write_text(source)
    tests = (ROOT / 'worktree/tools/parity_journeys/test_post_onboarding.py').read_text()
    redundant = {
        'test_final_identity_cannot_reuse_home_after_all_final_outputs_are_deleted',
        'test_final_identity_cannot_reuse_resolved_aliases_of_home_outputs',
        'test_later_input_cannot_reuse_earlier_live_files_after_own_files_are_deleted',
        'test_later_input_cannot_reuse_earlier_live_files_through_resolved_aliases',
        'test_snapshot_pid_evidence_cannot_be_reused_from_an_earlier_screen',
        'test_before_input_pid_cannot_reuse_a_previous_input_observation',
        'test_input_command_streams_cannot_reuse_prior_command_outputs',
    }
    lines = tests.splitlines(True)
    ranges = [(node.lineno - 1, node.end_lineno) for node in ast.walk(ast.parse(tests))
              if isinstance(node, ast.FunctionDef) and node.name in redundant]
    if len(ranges) != len(redundant):
        raise ValueError('Superseded duplicate test names differ')
    for start, end in sorted(ranges, reverse=True):
        del lines[start:end]
    tests = ''.join(lines)
    while '\n\n\n' in tests:
        tests = tests.replace('\n\n\n', '\n\n')
    ast.parse(tests)
    (DEST / 'test_post_onboarding.py').write_text(tests)
    doc = (ROOT / 'worktree/tools/parity_journeys/POST_ONBOARDING.md').read_text()
    doc = replace_once(doc, 'The corrected session result has schema 2. It also requires `session_observation`',
                       'The proposed corrected session result has schema 3. It requires `session_observation`')
    doc = replace_once(doc, 'A single set of resolved artifact paths covers both variants and every in-scope',
                       'A single published ledger of resolved paths and file identities covers both variants and every in-scope')
    doc = replace_once(doc, 'alias, is rejected. Equal bytes in distinct observation files remain valid. These',
                       'alias or hard link, is rejected. Equal bytes in distinct observation files remain valid. These')
    doc = replace_once(doc, 'Older schema 1 session results and their exact source remain historical evidence.',
                       'Older schema 1 and schema 2 session results and their exact source remain historical evidence.')
    doc += '''
## Follow-up after the published file identity ledger

This proposed timing follow-up is based on commit `47458097056fd023bad8b47b6464978b0d02e85c`. It retains `session_evidence.py`, its exact path-and-inode ledger, all twelve published ledger tests, the reproduction helper, and `SESSION_EVIDENCE.md` unchanged. The ledger is checked before chronology so a reused observation remains an explicit file-identity rejection. Equal bytes in distinct fresh files remain valid.

The comparator result advances to schema 3 because the additional capture/input chronology is mandatory. Generic journey capture schema 2 remains the outer container, with versioned `session_observation` records added by this session recorder. Older schema-2 device artifacts lack those records: preserve and replay them with their exact historical source, and record the stronger gate as pending a fresh device run. Do not invent missing capture times or replace historical reports.

The separate current ten-screen observed policy and the twelve-screen trigger proposal are unchanged by this session-only overlay. No animation setting, reference plan, app APK, selector, screenshot, XML or workflow is changed here.
'''
    (DEST / 'POST_ONBOARDING.md').write_text(doc)
    changed = []
    for row in manifest['all_copied_files']:
        path = ROOT / 'external474-worktree' / row['path']
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != row['sha256']:
            changed.append({'path': row['path'], 'baseline_sha256': row['sha256'],
                            'proposed_sha256': digest, 'bytes': path.stat().st_size})
    expected = {'tools/parity_journeys/' + name for name in ('post_onboarding.py', 'test_post_onboarding.py', 'POST_ONBOARDING.md')}
    if {row['path'] for row in changed} != expected:
        raise ValueError('Unexpected private overlay scope')
    result = {'schema': 1, 'base_commit': manifest['baseline_commit'], 'status': 'PRIVATE_OVERLAY_PREPARED_NOT_ACTIVATED',
              'changed_paths': changed, 'external_ledger_and_tests_unchanged': True,
              'source_files_in_snapshot': len(manifest['all_copied_files']), 'android_executed': False,
              'duplicate_prototype_tests_removed': sorted(redundant)}
    (ROOT / 'external474-adaptation.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
