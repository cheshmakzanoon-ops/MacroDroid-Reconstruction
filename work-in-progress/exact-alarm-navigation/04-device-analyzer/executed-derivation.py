#!/usr/bin/env python3
"""Derive a separate exact-alarm device-artifact analyzer from its frozen parent."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

PARENT = Path('/dev/shm/macrodroid-notification-readiness/analyze_device_run.py')
OUTPUT = Path('/dev/shm/macrodroid-exact-alarm-navigation/device-analysis-01')
PARENT_SHA = '84bee2f7254d47bd049d3a273f1f401981a42b6af22670fa47fc3ed20131d2fe'


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    OUTPUT.mkdir(exist_ok=False)
    before = identity(PARENT)
    assert before == {'bytes': 22959, 'sha256': PARENT_SHA}
    original = PARENT.read_text()
    source = original
    edits = []

    def replace(old, new, count=1):
        nonlocal source
        actual = source.count(old)
        if actual != count:
            raise ValueError('Unexpected derivation boundary: ' + repr(old) + ': ' + str(actual))
        source = source.replace(old, new)
        edits.append({'old': old, 'new': new, 'occurrences': count})

    replace('one exact readiness CI artifact', 'one exact fourteen-screen exact-alarm CI artifact')
    replace('from datetime import datetime, timezone', 'from contextlib import ExitStack\nfrom datetime import datetime, timezone')
    replace('work-in-progress/notification-readiness-workflow/01-thirteen-screen',
            'work-in-progress/exact-alarm-navigation-workflow/01-fourteen-screen')
    replace('.github/workflows/editor-day-time-readiness.yml', '.github/workflows/editor-exact-alarm-navigation.yml')
    replace('56808b331ec8995c5ebf82a5a55972dfa75c078233247543a5f526f2f0949930',
            '575a8ccb4909ba526e4c29ba7695cc8486538885b017f29093c00344214bed1f')
    replace('7c9bcd22d8a14463766bb053e87d56167581052a9f91d7005e2cd85f7a002195',
            'd59a45832aa2bf40530dc0d057339cac564ce29d4c3cfe42e8cf02505c060ad7')
    replace('99f365ff58605f1f768ee9ac1715a1a47f280b4a06a18ad549bd71d03191486c',
            '80dd3f2db42cd154e7ee0df037fbf48bf63d87268b1128e33bd55812286fa40e')
    replace("with tempfile.TemporaryDirectory(prefix='readiness-device-replay-') as temporary:",
            "with tempfile.TemporaryDirectory(prefix='exact-alarm-device-replay-') as temporary, ExitStack() as configured_scope:")
    replace('day-time-readiness-verification.json', 'exact-alarm-navigation-verification.json', 2)
    replace('len(prepared) == 252', 'len(prepared) == 295')
    replace('independently-reconstructed-252-inputs.json', 'independently-reconstructed-295-inputs.json')
    replace('import day_time_journey as daytime', 'import exact_alarm_journey as alarm')
    replace('import notification_readiness as readiness', 'import exact_alarm_readiness as readiness')
    replace("            folder = shadow / 'journey'\n", "            configured_scope.enter_context(alarm.configured_plan())\n            folder = shadow / 'journey'\n")
    replace('            with daytime.configured_plan():\n                readiness.require_policy(report)\n                replayed = runner.compare(folder, report, proof)',
            '            alarm.require_navigation_policy(report)\n            readiness.require_policy(report)\n            replayed = runner.compare(folder, report, proof)')
    replace("[('journey-host-tests.log', 166),", "[('journey-host-tests.log', 209),")
    replace('(preparation, verification, scales, daytime, readiness, observed, chronology, runner, proof)',
            '(preparation, verification, scales, alarm, readiness, observed, chronology, runner, proof)')
    replace('EXACT_READINESS_DEVICE_ARTIFACT_REPLAYED', 'EXACT_ALARM_DEVICE_ARTIFACT_REPLAYED')
    replace('independently_reconstructed_input_copy_roles=252', 'independently_reconstructed_input_copy_roles=295')
    replace('INDEPENDENT_READINESS_REPLAY_REJECTED', 'INDEPENDENT_EXACT_ALARM_REPLAY_REJECTED')
    replace('independent-readiness-analysis.json', 'independent-exact-alarm-analysis.json')
    replace("                trigger_configuration_confirmed=False, private_replay_directory_removed=True)",
            "                trigger_configuration_confirmed=False, private_replay_directory_removed=True,\n"
            "                literal_exact_alarm_ok_tapped=replayed.get('exact_alarm_explanation_ok_tapped'),\n"
            "                literal_settings_navigation_observed=replayed.get('settings_navigation_observed'),\n"
            "                literal_settings_inputs=replayed.get('settings_inputs'),\n"
            "                literal_permission_granted_flag=replayed.get('permission_granted'),\n"
            "                literal_global_command_observations=replayed.get('global_command_observations'))")
    # Small inventories remain untouched; the main function is the sole functional derivation.
    old_tree, new_tree = ast.parse(original), ast.parse(source)
    old_functions = {node.name: node for node in old_tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    new_functions = {node.name: node for node in new_tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    assert old_functions.keys() == new_functions.keys()
    unchanged = []
    for name in old_functions.keys() - {'main'}:
        assert ast.dump(old_functions[name], include_attributes=False) == ast.dump(new_functions[name], include_attributes=False)
        unchanged.append(name)
    assert identity(PARENT) == before
    path = OUTPUT / 'analyze_device_run.py'
    path.write_text(source)
    compile(source, str(path), 'exec')
    shutil.copyfile(Path(__file__), OUTPUT / 'executed-derivation.py')
    (OUTPUT / 'parent-to-exact-alarm.patch').write_text(''.join(difflib.unified_diff(
        original.splitlines(keepends=True), source.splitlines(keepends=True),
        fromfile='readiness13/analyze_device_run.py', tofile='exact-alarm14/analyze_device_run.py')))
    with (OUTPUT / 'help.stdout').open('xb') as out, (OUTPUT / 'help.stderr').open('xb') as err:
        process = subprocess.run([sys.executable, '-B', str(path), '--help'], stdout=out, stderr=err, timeout=30)
    assert process.returncode == 0
    report = {'schema': 1, 'status': 'EXACT_ALARM_ANALYZER_PREPARED_NO_DEVICE_REPLAY_EXECUTED',
              'created_utc': datetime.now(timezone.utc).isoformat(), 'parent': {'path': str(PARENT), **before},
              'derived_analyzer': identity(path), 'edits': edits, 'unchanged_helper_asts': sorted(unchanged),
              'parent_unchanged': identity(PARENT) == before, 'in_memory_compile_passed': True,
              'cli_help_exit_code': process.returncode, 'new_device_replay_executed': False,
              'android_actions_executed': False, 'device_result_or_parity_claimed': False,
              'configured_plan_scope': 'Covers the complete independent replay including all manual accepted-snapshot and capture-event inspections',
              'raw_zip_bytes_preserved': True, 'apk_transports': 'Read-only hardlinks or exact private copies only',
              'new_expected_prepared_input_roles': 295, 'new_expected_host_test_successes': 209}
    (OUTPUT / 'derivation.json').write_text(json.dumps(report, indent=2) + '\n')
    (OUTPUT / 'README.md').write_text('# Fourteen-screen exact-alarm artifact analyzer\n\n'
        'This additive analyzer is prepared for the forthcoming exact-alarm navigation run. It binds the reviewed '
        'fourteen-screen workflow and both helper hashes, reconstructs all 295 prepared input roles, and replays '
        'the captured comparison plus outer verifier using exact copied sources. The new configured-plan context '
        'also covers manual inspection of Settings snapshots and capture ledgers. It expects the complete 209 '
        'host-control log, retains full frames and hierarchy nodes, and records the literal navigation and '
        'global-command results.\n\n'
        'The original thirteen-screen analyzer is unchanged. All inventory/helper functions keep their '
        'exact ASTs; the patch and derivation recipe are included. Only syntax and CLI help have run so far. '
        'This preparation establishes no Android result or visual parity. The actual run ID, artifact ID, '
        'commit, downloaded ZIP hash and unchanged compared APKs are required at execution.\n')
    files = [{'path': p.relative_to(OUTPUT).as_posix(), 'mode': '100644', **identity(p)}
             for p in sorted(OUTPUT.rglob('*')) if p.is_file()]
    checkpoint = {'schema': 1, 'status': report['status'], 'repo_target':
                  'work-in-progress/exact-alarm-navigation/04-device-analyzer',
                  'active_files': [], 'files': files, 'file_count': len(files),
                  'payload_bytes': sum(row['bytes'] for row in files)}
    (OUTPUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'output': str(OUTPUT), 'checkpoint': identity(OUTPUT / 'checkpoint.json'),
                      'files': len(files), 'payload_bytes': checkpoint['payload_bytes']}))


if __name__ == '__main__':
    main()
