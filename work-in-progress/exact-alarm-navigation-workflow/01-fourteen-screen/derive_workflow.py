#!/usr/bin/env python3
"""Derive one additive fourteen-screen workflow from the closed readiness workflow."""
from __future__ import annotations

import ast
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path('/dev/shm/macrodroid-exact-alarm-navigation')
PARENT = Path('/dev/shm/macrodroid-notification-readiness/checkpoints/02-thirteen-screen-readiness-workflow')
GUARD = ROOT / 'checkpoints/03-corrected-source-and-host-controls'
OUTPUT = ROOT / 'workflow-01'
PARENT_SHA = '3ca1103f0e247cb827be1d654ce082989658a54cfb8b6b7c4f2c655fd553c50b'
GUARD_SHA = '8deeece1c51d4320a72b065679f22a56242ea6769ed526e0c6436df405430857'
GUARD_PACKAGE = 'work-in-progress/exact-alarm-navigation/03-corrected-source-and-host-controls'
WORKFLOW_PACKAGE = 'work-in-progress/exact-alarm-navigation-workflow/01-fourteen-screen'


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def once(value, old, new):
    if value.count(old) != 1:
        raise RuntimeError('Expected one exact derivation anchor: ' + repr(old[:160]))
    return value.replace(old, new, 1)


def main():
    for path, digest in ((PARENT, PARENT_SHA), (GUARD, GUARD_SHA)):
        if identity(path / 'checkpoint.json')['sha256'] != digest:
            raise RuntimeError('Closed workflow derivation checkpoint changed')
        value = json.loads((path / 'checkpoint.json').read_text())
        for row in value['files']:
            if identity(path / row['path']) != {key: row[key] for key in ('bytes', 'sha256')}:
                raise RuntimeError('Closed workflow derivation payload changed')
    guard = json.loads((GUARD / 'checkpoint.json').read_text())
    if (guard['status'] != 'CORRECTED_EXACT_ALARM_HOST_CONTROLS_PASSED_INACTIVE'
            or guard['source_files'] != 98 or len(guard['files']) != 166
            or guard['distinct_host_tests_passed'] != 209 or guard['android_executed'] is not False):
        raise RuntimeError('Expected the exact corrected source guard')
    sys.path[:0] = [str(GUARD / 'replay-source/tools/parity_journeys'), str(GUARD / 'replay-source/project')]
    import exact_alarm_journey as alarm
    import exact_alarm_readiness as readiness
    import editor_journey as runner
    with alarm.configured_plan():
        plan = alarm.expected_plan()
        positive = {'schema': 6, 'plan': plan, 'plan_sha256': alarm.PLAN_SHA256,
                    alarm.POLICY_KEY: alarm.POLICY, readiness.POLICY_KEY: readiness.POLICY}
        readiness.require_policy(positive)
    if len(plan) != 14 or plan[-1] != ['after-exact-alarm-ok', 'com.android.settings', None, alarm.OK]:
        raise RuntimeError('New terminal plan differs')
    plan_sha = runner.fingerprint(plan)
    readiness_sha, navigation_sha = runner.fingerprint(readiness.POLICY), runner.fingerprint(alarm.POLICY)
    OUTPUT.mkdir(exist_ok=False)
    replacements = [
        ('work-in-progress/notification-readiness-workflow/01-thirteen-screen', WORKFLOW_PACKAGE),
        ('work-in-progress/notification-readiness/01-corrected-host-guard', GUARD_PACKAGE),
        ('day-time-readiness', 'exact-alarm-navigation'),
        ('DAY_TIME_READINESS', 'EXACT_ALARM_NAVIGATION'),
        ('freeze_readiness_workflow.py', 'freeze_alarm_workflow.py'),
    ]
    names = ['prepare_trigger_journey.py', 'verify_trigger_journey.py', 'build_workflow.py',
             'validate_workflow.py', 'freeze_readiness_workflow.py']
    changes, patch = [], ''
    for name in names:
        before = (PARENT / name).read_text()
        after = before
        for old, new in replacements:
            after = after.replace(old, new)
        if name == 'prepare_trigger_journey.py':
            after = after.replace('thirteen-screen trigger-category', 'fourteen-screen exact-alarm navigation')
            after = once(after, "GUARD + '/checkpoint.json': 'b9d069a653b3ecc483f8e6579ccfb13e5a70450c00015f9a3a31c5277c9a84b3'",
                         "GUARD + '/checkpoint.json': '" + GUARD_SHA + "'")
            after = once(after, '[(GUARD, 140), (ANIMATION, 9)]', '[(GUARD, 166), (ANIMATION, 9)]')
            after = once(after, 'REPORT_SCHEMA = 5', 'REPORT_SCHEMA = 6')
            after = once(after, "READINESS_POLICY_SHA256 = 'bec477b5b3792d6270dec999dfb5d08094a01fc3a9ad186a2a44b38d8f6967a4'",
                         'READINESS_POLICY_SHA256 = ' + repr(readiness_sha) + '\nNAVIGATION_POLICY_SHA256 = ' + repr(navigation_sha))
            after = after.replace('42ece5a06a280186ddf9796a4524975d478263e545260674e2b1b4cf718d46fb', plan_sha)
            after = once(after, "            or report.get('notification_readiness_policy_sha256') != READINESS_POLICY_SHA256\n",
                         "            or report.get('notification_readiness_policy_sha256') != READINESS_POLICY_SHA256\n"
                         "            or report.get('exact_alarm_navigation_policy_sha256') != NAVIGATION_POLICY_SHA256\n")
            after = once(after, '                      notification_readiness_policy_sha256=READINESS_POLICY_SHA256,\n',
                         '                      notification_readiness_policy_sha256=READINESS_POLICY_SHA256,\n'
                         '                      exact_alarm_navigation_policy_sha256=NAVIGATION_POLICY_SHA256,\n')
        elif name == 'verify_trigger_journey.py':
            after = after.replace('thirteen-screen trigger-category', 'fourteen-screen exact-alarm navigation')
            after = after.replace('thirteen full-frame still observations and twelve inputs',
                                  'fourteen full-frame still observations and thirteen inputs')
            after = after.replace('thirteen-screen observation', 'fourteen-screen observation')
            after = after.replace('THIRTEEN_SCREEN', 'FOURTEEN_SCREEN')
            after = after.replace('require_notification_policy', 'require_workflow_policies')
            after = once(after, '    import day_time_journey\n    import notification_readiness\n    with day_time_journey.configured_plan():\n        notification_readiness.require_policy(report)',
                         '    import exact_alarm_journey\n    import exact_alarm_readiness\n    with exact_alarm_journey.configured_plan():\n        exact_alarm_journey.require_navigation_policy(report)\n        exact_alarm_readiness.require_policy(report)')
            after = once(after, 'import day_time_journey as category', 'import exact_alarm_journey as category')
            after = once(after, "len(run['screens']) != 13 or len(run['transitions']) != 12", "len(run['screens']) != 14 or len(run['transitions']) != 13")
            after = once(after, "len(replayed.get('screens', [])) != 13", "len(replayed.get('screens', [])) != 14")
            after = once(after, "                or replayed.get('trigger_configuration_confirmed') is not False\n",
                         "                or replayed.get('trigger_configuration_confirmed') is not False\n"
                         "                or replayed.get('exact_alarm_explanation_ok_tapped') is not True\n"
                         "                or replayed.get('settings_navigation_observed') is not True\n"
                         "                or replayed.get('settings_inputs') != 0\n"
                         "                or replayed.get('permission_granted') is not False\n"
                         "                or replayed.get(category.POLICY_KEY) != category.POLICY\n"
                         "                or replayed.get('global_command_observations', {}).get('planned_inputs') != 26\n"
                         "                or replayed.get('global_command_observations', {}).get('setup_mutations') != 6\n"
                         "                or replayed.get('global_command_observations', {}).get('unbound_mutations') != 0\n"
                         "                or replayed.get('global_command_observations', {}).get('settings_inputs') != 0\n")
            after = once(after, "'EXACT_DAY_TIME_TRIGGER_OBSERVATION_ONLY'", "'EXACT_ALARM_SETTINGS_OBSERVATION_ONLY'")
        elif name == 'build_workflow.py':
            after = after.replace('day_time_journey.py', 'exact_alarm_journey.py')
            after = after.replace('thirteen-screen', 'fourteen-screen').replace('thirteen declared', 'fourteen declared')
            after = once(after, 'name: Independent Day/Time fourteen-screen comparison with notification readiness',
                         'name: Independent exact-alarm fourteen-screen comparison with bounded notification readiness')
            after = once(after, 'frozen readiness guard and fourteen-screen source',
                         'frozen exact-alarm guard and fourteen-screen source')
        elif name == 'validate_workflow.py':
            after = after.replace('day_time_journey.py', 'exact_alarm_journey.py')
            after = after.replace('thirteen declared', 'fourteen declared')
            after = once(after, "            ('changed-readiness-guard', preparation.GUARD + '/replay-source/tools/parity_journeys/notification_readiness.py', 'bytes'),\n",
                         "            ('changed-readiness-guard', preparation.GUARD + '/replay-source/tools/parity_journeys/exact_alarm_readiness.py', 'bytes'),\n"
                         "            ('changed-navigation-guard', preparation.GUARD + '/replay-source/tools/parity_journeys/exact_alarm_journey.py', 'bytes'),\n"
                         "            ('changed-observed-dialog', preparation.GUARD + '/replay-source/tools/parity_journeys/fixtures/exact-alarm/dialog-contract.json', 'bytes'),\n")
            after = once(after, "            ('changed-readiness-policy-pin', 'changed-policy', False, False),\n",
                         "            ('changed-readiness-policy-pin', 'changed-policy', False, False),\n"
                         "            ('missing-navigation-policy-pin', 'omit-navigation', False, False),\n"
                         "            ('changed-navigation-policy-pin', 'changed-navigation', False, False),\n"
                         "            ('older-thirteen-plan-pin', 'older-plan', False, False),\n")
            after = once(after, "            elif mode == 'omit-reviewed':\n",
                         "            elif mode == 'omit-navigation':\n"
                         "                del declared['exact_alarm_navigation_policy_sha256']\n"
                         "            elif mode == 'changed-navigation':\n"
                         "                declared['exact_alarm_navigation_policy_sha256'] = '0' * 64\n"
                         "            elif mode == 'older-plan':\n"
                         "                declared['plan_sha256'] = '42ece5a06a280186ddf9796a4524975d478263e545260674e2b1b4cf718d46fb'\n"
                         "            elif mode == 'omit-reviewed':\n")
            start = after.index("        policy_script.write_text(")
            end = after.index("        policy_result = ", start)
            policy_program = '''import copy
import json
from pathlib import Path
import sys
sys.path[:0] = [sys.argv[1], sys.argv[2], sys.argv[3]]
import verify_trigger_journey as verifier
import exact_alarm_journey as alarm
import exact_alarm_readiness as readiness
positive = {'schema': 6, 'plan': alarm.expected_plan(), 'plan_sha256': alarm.PLAN_SHA256,
            alarm.POLICY_KEY: copy.deepcopy(alarm.POLICY), readiness.POLICY_KEY: copy.deepcopy(readiness.POLICY)}
verifier.require_workflow_policies(positive)
controls = []
for label in ['legacy-schema', 'unregistered-schema', 'boolean-schema', 'missing-readiness', 'changed-readiness',
              'missing-navigation', 'changed-navigation', 'nested-navigation', 'changed-plan', 'changed-plan-hash']:
    value = copy.deepcopy(positive)
    if label == 'legacy-schema': value['schema'] = 5
    elif label == 'unregistered-schema': value['schema'] = 7
    elif label == 'boolean-schema': value['schema'] = True
    elif label == 'missing-readiness': del value[readiness.POLICY_KEY]
    elif label == 'changed-readiness': value[readiness.POLICY_KEY]['max_seconds'] = 11
    elif label == 'missing-navigation': del value[alarm.POLICY_KEY]
    elif label == 'changed-navigation': value[alarm.POLICY_KEY]['settings_inputs'] = 1
    elif label == 'nested-navigation': value['unexpected'] = {alarm.POLICY_KEY: copy.deepcopy(alarm.POLICY)}
    elif label == 'changed-plan': value['plan'][-1][1] = 'com.example.foreign'
    elif label == 'changed-plan-hash': value['plan_sha256'] = '0' * 64
    try:
        verifier.require_workflow_policies(value)
    except Exception as error:
        if not any(text in str(error) for text in ['Missing or altered notification readiness policy',
                                                  'Missing, altered or misplaced exact-alarm navigation policy or plan']):
            raise
        controls.append({'label': label, 'rejected': True, 'reason': str(error)})
    else:
        raise AssertionError('Workflow policy substitution accepted: ' + label)
verifier.require_workflow_policies(positive)
result = {'passed': True, 'android_executed': False,
          'scope': 'Required complete plan and both policy formats only; compare separately requires complete raw evidence and every command role.',
          'positive_and_restore': True, 'negative_controls': controls}
Path(sys.argv[4]).write_text(json.dumps(result, indent=2) + '\\n')
print(json.dumps(result, indent=2))
'''
            after = after[:start] + '        policy_script.write_text(' + repr(policy_program) + ')\n' + after[end:]
            # This runs the larger, complete 209-test package once. It changes no device deadline.
            after = once(after, "['bash', '-o', 'pipefail', '-c', script], timeout=300)",
                         "['bash', '-o', 'pipefail', '-c', script], timeout=600)")
            # All test temporaries belong to this newly allocated validation directory.
            after = once(after, "    root.mkdir()\n", "    root.mkdir()\n    temporary = output / 'host-temporary'; temporary.mkdir()\n")
            after = once(after, "'GITHUB_SHA': 'offline-control-no-git-or-android-execution'}",
                         "'GITHUB_SHA': 'offline-control-no-git-or-android-execution', 'TMPDIR': str(temporary)}")
        elif name == 'freeze_readiness_workflow.py':
            after = after.replace('thirteen-screen', 'fourteen-screen')
            after = once(after, "    readme.write_text(", "    readme.write_text(")
            start = after.index('    readme.write_text(')
            end = after.index("    files.append({'path': readme.name", start)
            description = '''# Exact-alarm explanation: one observed OK tap and a Settings observation

This additive workflow extends the unchanged thirteen-screen Day/Time prefix by one observed OK tap and one full Settings observation. It requires the exact schema-6 plan, complete observed dialog contract, bounded notification readiness, stable full frames and main-app PID continuity. No Settings class, Settings control, permission grant, trigger configuration, saved macro or macro execution is assumed.

The whole global command log is independently checked. Every one of the 26 paired planned inputs and six setup mutations must match its exact declared run role in order; other commands must match the finite evidence grammar. Both APKs, API35 runtime, zero animation settings, demo clock and owned cleanup are inherited from the closed readiness workflow. The raw full-image comparison retains every changed pixel, XML attribute and recorded process-boundary outcome.

The source capsule preserves the first extra-input false acceptance, its independent correction, all closed host attempts and the two corrected historical-fixture tests. This workflow's offline validation additionally runs the complete 209-test source package together with both exact historical ZIPs, validates required plan/policy pins and complete preparation membership, inspects both actual APKs with preserved AAPT2, and measures the owned cleanup behavior. All offline attempts and original evidence bytes remain retained. Large already-published APK/tool copies are referenced by their exact durable manifest identities.

The historical run 38230072388 remains a thirteen-screen visual difference with 26 changed introduction-indicator pixels and the recorded known crash continuation. It is not rewritten by this new workflow. Host and offline results do not establish the next actual Android destination or whole-application parity.
'''
            after = after[:start] + '    readme.write_text(' + repr(description) + ')\n\n' + after[end:]
        ast.parse(after, filename=name)
        target_name = 'freeze_alarm_workflow.py' if name == 'freeze_readiness_workflow.py' else name
        with (OUTPUT / target_name).open('x') as stream:
            stream.write(after)
        changes.append({'parent_path': name, 'path': target_name,
                        'before': identity(PARENT / name), 'after': identity(OUTPUT / target_name)})
        patch += ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                         fromfile='parent/' + name, tofile='successor/' + target_name))
    with (OUTPUT / 'derivation.patch').open('x') as stream:
        stream.write(patch)
    bindings = {'schema': 1, 'parent_checkpoint': {'path': str(PARENT), 'sha256': PARENT_SHA},
                'guard_checkpoint': {'path': str(GUARD), 'sha256': GUARD_SHA},
                'source_changes': changes, 'plan_sha256': plan_sha,
                'readiness_policy_sha256': readiness_sha, 'navigation_policy_sha256': navigation_sha,
                'source_files': 98, 'guard_payloads': 166, 'paired_screens': 14, 'inputs_per_run': 13,
                'new_inputs_per_run': 1, 'settings_inputs': 0,
                'owned_tmpfs_budget_bytes': 805306368, 'android_executed': False,
                'source_guard_and_parent_unchanged': True}
    with (OUTPUT / 'parent-source-identities.json').open('x') as stream:
        stream.write(json.dumps(bindings, indent=2) + '\n')
    shutil.copy2(Path(__file__), OUTPUT / 'derive_workflow.py')
    print(json.dumps(bindings, indent=2))


if __name__ == '__main__':
    main()
