#!/usr/bin/env python3
"""Derive an additive readiness workflow from the exact thirteen-screen parent."""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import sys

PARENT_SHA = '2510711052d2f41bde1a7a583e4bd42f1aab2e1f2001b3bd03d5e2b9eff29229'
GUARD_SHA = 'b9d069a653b3ecc483f8e6579ccfb13e5a70450c00015f9a3a31c5277c9a84b3'


def identity(path):
    digest = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        while data := stream.read(1024 * 1024):
            digest.update(data)
            size += len(data)
    return {'bytes': size, 'sha256': digest.hexdigest()}


def once(value, before, after):
    if value.count(before) != 1:
        raise ValueError('Expected one workflow derivation anchor: ' + repr(before[:100]))
    return value.replace(before, after, 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parent', type=Path, required=True)
    parser.add_argument('--guard', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    parent, guard, output = [path.resolve() for path in (args.parent, args.guard, args.output)]
    if identity(parent / 'checkpoint.json')['sha256'] != PARENT_SHA:
        raise ValueError('The closed parent workflow checkpoint changed')
    if identity(guard / 'checkpoint.json')['sha256'] != GUARD_SHA:
        raise ValueError('The closed corrected readiness guard changed')
    parent_manifest = json.loads((parent / 'checkpoint.json').read_text())
    manifest = json.loads((guard / 'checkpoint.json').read_text())
    for folder, value in [(parent, parent_manifest), (guard, manifest)]:
        for row in value['files']:
            if identity(folder / row['path']) != {key: row[key] for key in ('bytes', 'sha256')}:
                raise ValueError('Closed derivation input changed: ' + str(folder / row['path']))
    if (manifest['status'] != 'TARGETED_HOST_CONTROLS_PASSED_INACTIVE'
            or manifest['android_executed'] is not False or len(manifest['files']) != 140):
        raise ValueError('The exact closed corrected host guard is required')
    parent_files = {row['path']: {key: row[key] for key in ('bytes', 'sha256')}
                    for row in parent_manifest['files']}
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(guard / 'replay-source/tools/parity_journeys'))
    import day_time_journey as day
    import editor_journey as runner
    import notification_readiness as readiness
    with day.configured_plan():
        readiness.require_plan()
        plan = day.expected_plan()
        readiness.require_policy({'schema': 5, readiness.POLICY_KEY: readiness.POLICY})
    plan_sha = runner.fingerprint(plan)
    policy_sha = runner.fingerprint(readiness.POLICY)
    if (len(plan) != 13 or plan[-1] != ['after-day-time-trigger', runner.PACKAGE, None, day.DAY_TIME]
            or readiness.REPORT_SCHEMA != 5 or plan_sha != readiness.PLAN_SHA256):
        raise ValueError('The reviewed plan or readiness schema changed')
    output.mkdir(parents=True, exist_ok=False)
    source_names = ['prepare_trigger_journey.py', 'verify_trigger_journey.py',
                    'build_workflow.py', 'validate_workflow.py', 'freeze_day_time_workflow.py']
    replacements = [
        ('work-in-progress/day-time-trigger-workflow/01-zero-scale-workflow',
         'work-in-progress/notification-readiness-workflow/01-thirteen-screen'),
        ('work-in-progress/day-time-trigger/02-host-success',
         'work-in-progress/notification-readiness/01-corrected-host-guard'),
        ('editor-day-time-trigger', 'editor-day-time-readiness'),
        ('ci-day-time-trigger', 'ci-day-time-readiness'),
        ('macrodroid-day-time-trigger-tooling', 'macrodroid-day-time-readiness-tooling'),
        ('--id day-time-trigger-', '--id day-time-readiness-'),
        ('day-time-trigger-verification.json', 'day-time-readiness-verification.json'),
        ("'DAY_TIME_TRIGGER_", "'DAY_TIME_READINESS_"),
        ('FROZEN_DAY_TIME_TRIGGER_', 'FROZEN_DAY_TIME_READINESS_'),
        ('OFFLINE_DAY_TIME_TRIGGER_', 'OFFLINE_DAY_TIME_READINESS_'),
        ('freeze_day_time_workflow.py', 'freeze_readiness_workflow.py'),
    ]
    bindings, changes, patch = {}, [], ''
    for name in source_names:
        original = parent / name
        bindings[name] = parent_files[name]
        before = original.read_text()
        after = before
        for old, new in replacements:
            after = after.replace(old, new)
        if name == 'prepare_trigger_journey.py':
            after = once(after, "GUARD + '/checkpoint.json': '0e010cfbace03cffa6d45e8c9157402b1b68c9a392249eb2aeae39445dc57a7d'",
                         "GUARD + '/checkpoint.json': '" + GUARD_SHA + "'")
            after = once(after, '[(GUARD, 114), (ANIMATION, 9)]', '[(GUARD, 140), (ANIMATION, 9)]')
            after = once(after, '\nAPKS = [', '\nREPORT_SCHEMA = 5\nREADINESS_POLICY_SHA256 = ' + repr(policy_sha) + '\nAPKS = [')
            after = once(after, "            or report.get('requested_scales') != '0'\n",
                         "            or report.get('requested_scales') != '0'\n"
                         "            or type(report.get('requested_report_schema')) is not int\n"
                         "            or report['requested_report_schema'] != REPORT_SCHEMA\n"
                         "            or report.get('notification_readiness_policy_sha256') != READINESS_POLICY_SHA256\n")
            after = once(after, "                      requested_scales='0', full_runtime_1_to_1_established=False)",
                         "                      requested_scales='0', requested_report_schema=REPORT_SCHEMA,\n"
                         "                      notification_readiness_policy_sha256=READINESS_POLICY_SHA256,\n"
                         "                      full_runtime_1_to_1_established=False)")
        if name == 'verify_trigger_journey.py':
            helper = '''
def require_notification_policy(report):
    """Require this workflow's schema even if a legacy comparison could pass.

    This checks the requested policy format only. Actual phase artifacts,
    chronology, commands, ownership and both references are verified by compare.
    """
    import day_time_journey
    import notification_readiness
    with day_time_journey.configured_plan():
        notification_readiness.require_policy(report)


'''
            after = once(after, '\ndef verify(root, output):', '\n' + helper + 'def verify(root, output):')
            after = once(after, "        report = json.loads((journey / 'journey.json').read_text())\n",
                         "        report = json.loads((journey / 'journey.json').read_text())\n"
                         "        require_notification_policy(report)\n")
            after = once(after, 'at animation scale zero\',', 'at animation scale zero, with bounded notification readiness\',')
        if name == 'build_workflow.py':
            after = once(after, '--accept-package-data-removal --observe-denial-handoff --settle-full-frames',
                         '--accept-package-data-removal --observe-denial-handoff --settle-full-frames --observe-notification-readiness')
            after = once(after, 'name: Independent trigger-category thirteen-screen comparison at scale zero',
                         'name: Independent Day/Time thirteen-screen comparison with notification readiness')
            after = after.replace('trigger-category runtime', 'Day/Time readiness runtime')
            after = once(after, 'Verify and copy the frozen thirteen-screen guard and diagnostic source',
                         'Verify and copy the frozen readiness guard and thirteen-screen source')
            after = once(after, 'Observe the thirteen declared screens with explicit zero animation scales',
                         'Observe the thirteen declared screens with bounded notification readiness')
            after = once(after, 'Recheck raw animation settings, ordered captures and exact pixels',
                         'Recheck raw readiness, animation settings, ordered captures and exact pixels')
        if name == 'validate_workflow.py':
            after = once(after, "    parser.add_argument('--workspace', type=Path, required=True)\n",
                         "    parser.add_argument('--workspace', type=Path, required=True)\n"
                         "    parser.add_argument('--guard', type=Path, required=True)\n")
            after = once(after, "(preparation.GUARD, workspace / 'day-time-trigger-forward/checkpoints/02-host-success')",
                         '(preparation.GUARD, args.guard.resolve())')
            after = once(after, "                or 'favourite_info_journey.py\\\"' in workflow.read_text()):".replace('\\\"', '"'),
                         "                or 'favourite_info_journey.py\"' in workflow.read_text()\n"
                         "                or workflow.read_text().count('--observe-notification-readiness') != 1):")
            after = once(after, "            ('changed-animation-helper', preparation.ANIMATION + '/enable_still_animations.py', 'bytes'),\n",
                         "            ('changed-animation-helper', preparation.ANIMATION + '/enable_still_animations.py', 'bytes'),\n"
                         "            ('changed-readiness-guard', preparation.GUARD + '/replay-source/tools/parity_journeys/notification_readiness.py', 'bytes'),\n")
            after = once(after, '            os.link(original, target)\n',
                         '            if original.stat().st_dev == root.stat().st_dev:\n'
                         '                os.link(original, target)\n'
                         '            else:\n'
                         '                shutil.copy2(original, target)\n'
                         '            if preparation.identity(target) != preparation.identity(original):\n'
                         "                raise ValueError('Exact offline runtime input transport changed')\n")
            after = once(after, "            ('omit-reviewed-copy-role', 'omit-reviewed', False, False),\n",
                         "            ('omit-reviewed-copy-role', 'omit-reviewed', False, False),\n"
                         "            ('legacy-readiness-schema', 'schema-three', False, False),\n"
                         "            ('boolean-readiness-schema', 'schema-bool', False, False),\n"
                         "            ('missing-readiness-policy-pin', 'omit-policy', False, False),\n"
                         "            ('changed-readiness-policy-pin', 'changed-policy', False, False),\n")
            after = once(after, "            elif mode == 'omit-reviewed':\n",
                         "            elif mode == 'schema-three':\n"
                         "                declared['requested_report_schema'] = 3\n"
                         "            elif mode == 'schema-bool':\n"
                         "                declared['requested_report_schema'] = True\n"
                         "            elif mode == 'omit-policy':\n"
                         "                del declared['notification_readiness_policy_sha256']\n"
                         "            elif mode == 'changed-policy':\n"
                         "                declared['notification_readiness_policy_sha256'] = '0' * 64\n"
                         "            elif mode == 'omit-reviewed':\n")
            after = once(after, "                        'Prepared input changed before execution:'])):",
                         "                        'Prepared input changed before execution:',\n"
                         "                        'Frozen diagnostic plan or preparation scope changed'])):")
            policy_program = '''import copy
import json
from pathlib import Path
import sys
sys.path[:0] = [sys.argv[1], sys.argv[2], sys.argv[3]]
import verify_trigger_journey as verifier
import notification_readiness as readiness
positive = {'schema': 5, readiness.POLICY_KEY: copy.deepcopy(readiness.POLICY)}
verifier.require_notification_policy(positive)
controls = []
for label in ['legacy-schema', 'unregistered-schema', 'boolean-schema', 'missing-policy', 'changed-policy']:
    value = copy.deepcopy(positive)
    if label == 'legacy-schema':
        value['schema'] = 3
    elif label == 'unregistered-schema':
        value['schema'] = 4
    elif label == 'boolean-schema':
        value['schema'] = True
    elif label == 'missing-policy':
        del value[readiness.POLICY_KEY]
    else:
        value[readiness.POLICY_KEY]['max_seconds'] = 11
    try:
        verifier.require_notification_policy(value)
    except Exception as error:
        if 'Missing or altered notification readiness policy' not in str(error):
            raise
        controls.append({'label': label, 'rejected': True, 'reason': str(error)})
    else:
        raise AssertionError('Workflow policy downgrade accepted: ' + label)
verifier.require_notification_policy(positive)
result = {'passed': True, 'android_executed': False, 'scope': 'Workflow-required policy format only; complete raw evidence is independently required by compare', 'positive_and_restore': True, 'negative_controls': controls}
Path(sys.argv[4]).write_text(json.dumps(result, indent=2) + '\\n')
print(json.dumps(result, indent=2))
'''
            block = "        policy_script = output / 'workflow-policy-controls.py'\n"
            block += '        policy_script.write_text(' + repr(policy_program) + ')\n'
            block += "        policy_result = output / 'workflow-policy-controls.json'\n"
            block += "        row = execute('workflow-policy-controls', [sys.executable, '-B', str(policy_script), str(home),\n"
            block += "            str(root / 'ci-day-time-readiness/reviewed-source/tools/parity_journeys'),\n"
            block += "            str(root / 'ci-day-time-readiness/reviewed-source/project'), str(policy_result)])\n"
            block += "        if row['exit_code'] or json.loads(policy_result.read_text()).get('passed') is not True:\n"
            block += "            raise ValueError('Workflow readiness policy controls failed')\n"
            block += "        report['checks'].append(json.loads(policy_result.read_text()))\n\n"
            after = once(after, "        host = next(step['run'] for step in steps if step['name'].startswith('Run the frozen capture'))\n",
                         block + "        host = next(step['run'] for step in steps if step['name'].startswith('Run the frozen capture'))\n")
        if name == 'freeze_day_time_workflow.py':
            start = after.index('    readme.write_text(')
            end = after.index("    files.append({'path': readme.name", start)
            description = (
                '# Day/Time trigger: thirteen screens with bounded notification readiness\n\n'
                'This additive workflow retains the exact thirteen-screen plan and both frozen APKs. '
                'After the observed notification-denial input and its existing two-second wait, '
                'it records a bounded read-only process/foreground phase before the original full-frame capture. '
                'The first eligible contiguous HOME/same-PID sequence must span at least 1.05 seconds '
                'between actual raw PID command endpoints; the phase stops within sixteen observations '
                'and ten seconds. No readiness sample receives screenshot or process-continuity credit.\n\n'
                'The workflow explicitly requires schema 5 and the exact policy. Both phase references, '
                'all raw commands and streams, global chronology and exclusive evidence ownership remain '
                'independently checked. The existing full-frame stability, known-crash continuation and '
                'zero changed-pixel checks remain required for every paired screen. Input coordinates, '
                'APK identities, API35 runtime, zero animation settings, demo clock and owned cleanup '
                'are inherited from the exact parent workflow.\n\n'
                'The original thirteen-screen run 38221713675 failed when its main PID was absent after '
                'the notification boundary; the candidate reached an exact-alarm explanation. The earlier '
                'twelve-screen run 38216299675 retains its five-pixel introduction difference. Neither '
                'historical outcome is rewritten. This workflow has not tapped the exact-alarm OK control '
                'or configured a trigger.\n\n'
                'The guard checkpoint preserves the initial false-acceptance counterexamples and corrected '
                'focused tests. This workflow capsule preserves the complete packaged host regression, '
                'raw input and policy fault controls, real offline APK inspections, and owned cleanup '
                'controls. These are host/offline results; fresh Android execution and whole-application '
                'parity remain separate claims. Exact APK/tool duplicates retain durable manifest references; '
                'every other raw offline file is mapped to verified archive bytes and mode, while deliberate '
                'symlink controls remain inert metadata.\n'
            )
            after = after[:start] + '    readme.write_text(' + repr(description) + ')\n\n' + after[end:]
        target_name = 'freeze_readiness_workflow.py' if name == 'freeze_day_time_workflow.py' else name
        target = output / target_name
        target.write_text(after)
        changes.append({'parent_path': name, 'path': target_name, 'before': parent_files[name], 'after': identity(target)})
        patch += ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                           fromfile='parent-thirteen-screen/' + name, tofile='readiness-thirteen-screen/' + target_name))
    shutil.copy2(Path(__file__), output / 'derive_workflow.py')
    (output / 'derivation.patch').write_text(patch)
    record = {'parent_checkpoint_sha256': PARENT_SHA, 'parent_sources': bindings, 'changes': changes,
              'guard_checkpoint': identity(guard / 'checkpoint.json'), 'guard_file_count': len(manifest['files']),
              'plan_sha256': plan_sha, 'requested_report_schema': 5,
              'notification_readiness_policy_sha256': policy_sha,
              'complete_host_regression_pending': True, 'android_executed': False, 'active_changes': False}
    (output / 'parent-source-identities.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
