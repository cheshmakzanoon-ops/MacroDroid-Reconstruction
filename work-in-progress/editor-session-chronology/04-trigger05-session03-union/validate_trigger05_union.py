"""Validate the exact Trigger05 replay tree with only the frozen session03 delta."""
from __future__ import annotations
import contextlib
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
REPO = BASE / 'MacroDroid-Reconstruction'
TRIGGER = BASE / 'trigger-catalog-forward/checkpoints/05-physical-identity-host-success'
SESSION = ROOT / 'checkpoints/03-paired-components'
OUT = ROOT / 'union-trigger05-session03'
WORK = OUT / 'worktree'
TPIN = '8c985ee7da3a2f3d0dab9a9b93cac49b07246f9f78f8b0b897144c60c085f743'
SPIN = '88d3794b4343165321b14e520a8805db7cd1ebd10c97af6529f99441ec5eaa5c'


def meta(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def write(name, value):
    with (OUT / name).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def verify_capsule(folder, pin):
    assert meta(folder / 'checkpoint.json')['sha256'] == pin
    result = json.loads((folder / 'checkpoint.json').read_bytes())
    for row in result['files']:
        assert meta(folder / row['path']) == {key: row[key] for key in ('bytes', 'sha256')}, row['path']
    return result


def inventory(folder):
    return {p.relative_to(folder).as_posix(): meta(p) for p in sorted(folder.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts}


def head():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()


def main():
    sys.dont_write_bytecode = True
    OUT.mkdir(parents=True, exist_ok=False)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    trigger, session = verify_capsule(TRIGGER, TPIN), verify_capsule(SESSION, SPIN)
    preparation = json.loads((TRIGGER / 'preparation.json').read_bytes())
    replay = {row['path'].removeprefix('replay-source/'): row for row in trigger['files']
              if row['path'].startswith('replay-source/')}
    assert len(replay) == 64 and len(preparation['changes']) == 17
    before = inventory(REPO / 'tools/parity_journeys')
    expected = {path.removeprefix('tools/parity_journeys/'): value for path, value in preparation['baseline'].items()
                if path.startswith('tools/parity_journeys/')}
    assert before == expected, 'Concurrent parity source differs from Trigger05 baseline; no overlay applied'
    baseline_head = head()
    write('repository-parity-before.json', {'head': baseline_head, 'files': before})
    changed = {row['path']: row for row in preparation['changes']}
    for relative, row in replay.items():
        target = WORK / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((TRIGGER / row['path']).read_bytes())
        assert meta(target) == {key: row[key] for key in ('bytes', 'sha256')}
        if relative in changed:
            assert meta(target) == changed[relative]['after']
            assert (meta(REPO / relative) if (REPO / relative).exists() else None) == changed[relative]['before']
    for proposal in session['inactive_proposals']:
        relative = proposal['path']
        assert meta(WORK / relative) == proposal['external474_baseline']
        assert meta(REPO / relative) == proposal['external474_baseline']
        (WORK / relative).write_bytes((SESSION / 'proposed_files' / relative).read_bytes())
        assert meta(WORK / relative) == proposal['proposed']
    assert len(session['inactive_proposals']) == 3
    fixtures = []
    for relative, expected_meta in preparation['baseline'].items():
        if not relative.startswith('docs/'):
            continue
        source = REPO / relative
        assert meta(source) == expected_meta
        target = WORK / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(source)
        fixtures.append({'path': relative, **expected_meta, 'local_fixture_link': str(source), 'payload_copied': False})
    source_before = inventory(WORK)
    write('inputs-before.json', source_before)
    write('preparation.json', {'schema': 1, 'trigger_checkpoint': TPIN, 'session_checkpoint': SPIN,
          'baseline_head': baseline_head, 'repository_parity_files_verified': len(before),
          'trigger_replay_files': 64, 'trigger_changes_over_current_baseline': 17,
          'session_replacement_paths': session['inactive_proposals'], 'fixture_references': fixtures,
          'active_repository_modified': False, 'android_executed': False})
    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tools/parity_journeys', '-p', 'test_*.py', '-v']
    start = time.monotonic()
    timed_out, exit_code = False, None
    with (OUT / 'full-union-tests.log').open('xb') as log:
        try:
            exit_code = subprocess.run(command, cwd=WORK, stdout=log, stderr=subprocess.STDOUT,
                                       timeout=300, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}).returncode
        except subprocess.TimeoutExpired:
            timed_out = True
    elapsed = time.monotonic() - start
    text = (OUT / 'full-union-tests.log').read_text()
    successes = re.findall(r'^test_.* \.\.\. ok$', text, re.M)
    summary = re.search(r'\nRan (\d+) tests in ([0-9.]+)s\n\nOK\n', text)
    required_controls = [
        'test_final_capture_and_own_identity_cannot_jointly_change_to_another_activity',
        'test_matching_wrong_final_activity_in_both_variants_is_rejected',
        'test_each_intermediate_paired_component_difference_remains_visible_with_equal_pixels',
        'test_paired_components_accept_equivalent_fully_qualified_activity_spelling',
        'test_deleted_actual_terminal_frames_cannot_be_replaced_by_prior_capture',
        'test_independent_terminal_files_with_pre_input_times_are_rejected',
        'test_distinct_paths_cannot_hide_a_reused_physical_pid_artifact',
        'test_cross_run_hard_link_is_rejected',
        'test_deleted_endpoint_outputs_cannot_be_replaced_by_start_identity',
    ]
    controls = {name: any(line.startswith(name + ' ') for line in successes) for name in required_controls}
    host_ok = (exit_code == 0 and not timed_out and summary is not None
               and int(summary[1]) == len(successes) == 148 and all(controls.values()))
    test_result = {'argv': command, 'cwd': str(WORK), 'timeout_seconds': 300, 'timed_out': timed_out,
                   'exit_code': exit_code, 'elapsed_seconds': elapsed, 'individual_successes': len(successes),
                   'reported_tests': int(summary[1]) if summary else None,
                   'reported_seconds': float(summary[2]) if summary else None,
                   'meaningful_control_successes': controls, 'passed': host_ok,
                   'log': meta(OUT / 'full-union-tests.log')}
    write('host-test-result.json', test_result)
    print(json.dumps({'stage': 'full_union_tests', **test_result}), flush=True)
    assert host_ok, 'Full union suite failed; all logs retained'
    # Reuse the exact complete synthetic archive, now with the final union imports.
    spec = importlib.util.spec_from_file_location('union_component_recheck', ROOT / 'recheck_paired_component_gap.py')
    recheck = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recheck)
    recheck.WORK, recheck.OUT = WORK, OUT / 'paired-component-replay'
    with (OUT / 'paired-component-replay.log').open('x') as log, contextlib.redirect_stdout(log):
        recheck.main()
    replay_result = json.loads((OUT / 'paired-component-replay/recheck-result.json').read_bytes())
    assert replay_result['status'] == 'PRESERVED_PAIRED_COMPONENT_FALSE_POSITIVE_NOW_REJECTED'
    after = inventory(WORK)
    write('inputs-after.json', after)
    repository_after = inventory(REPO / 'tools/parity_journeys')
    write('repository-parity-after.json', {'head': head(), 'files': repository_after})
    assert after == source_before and repository_after == before
    verify_capsule(TRIGGER, TPIN)
    verify_capsule(SESSION, SPIN)
    result = {'schema': 1, 'status': 'EXACT_TRIGGER05_SESSION03_UNION_HOST_VALIDATED',
              'started_utc': started, 'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'trigger_checkpoint_sha256': TPIN, 'session_checkpoint_sha256': SPIN,
              'copied_replay_source_files': 64, 'session_only_replacements': 3,
              'full_suite_tests': 148, 'host_test_result': test_result,
              'paired_component_archive_members_replayed': 584,
              'all_union_inputs_unchanged': True, 'all_current_main_parity_inputs_unchanged': True,
              'both_frozen_capsules_unchanged': True, 'android_executed': False,
              'active_repository_modified': False, 'new_runtime_gate': 'PENDING_FRESH_CAPTURE',
              'full_runtime_1_to_1_established': False}
    write('result.json', result)
    print(json.dumps({'status': result['status'], 'tests': 148, 'result': str(OUT / 'result.json')}), flush=True)


if __name__ == '__main__':
    main()
