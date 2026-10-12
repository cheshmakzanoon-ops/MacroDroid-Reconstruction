#!/usr/bin/env python3
"""Derive the separately pinned Settings-enable/return workflow after source closure."""
from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import stat
import sys

PARENT = Path('/dev/shm/macrodroid-exact-alarm-navigation/checkpoints/04-fourteen-screen-workflow')
PARENT_SHA256 = '805c4574f6047edd3d553715d83c48448d49fddd3f4d22807ebb3e0d5663b066'
BASE = Path('/dev/shm/macrodroid-exact-alarm-enable-return')
OLD_GUARD = 'work-in-progress/exact-alarm-navigation/03-corrected-source-and-host-controls'
OLD_PACKAGE = 'work-in-progress/exact-alarm-navigation-workflow/01-fourteen-screen'
PACKAGE = 'work-in-progress/exact-alarm-enable-return-workflow/01-sixteen-screen'
CANDIDATE_MANIFEST = 'work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json'
CANDIDATE_MANIFEST_SHA256 = 'e1e9c5713c83981cc85ec84e0ce25bfe3fe3a4918d8ff35744ff86194cad0152'
CANDIDATE_FILENAME = 'MacroDroid-5.67.8-day-numeric-0762aad9.apk'
CANDIDATE_SHA256 = '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd'
OLD_APK_MANIFEST = 'work-in-progress/combined-recovery/05-full-acceptance/apk/manifest.json'
OLD_APK_FILENAME = 'MacroDroid-5.67.8-combined-plugin-widget-hybrid.apk'
OLD_PLAN_SHA256 = '4133e9410db84ac5636ece780b67331bf139afaa2de6b5c110c5ef5679fda85c'
PLAN_SHA256 = 'ca597b23d9c2d11ebce1ed3953d609189476d7179635f2a4c4068df0795f2211'
CONTRACT_SHA256 = '379544de4e9e5d84138959f1e1552fcc9b2e52d7264d30e324c63f2a82814c07'


def identity(path):
    assert stat.S_ISREG(path.lstat().st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def once(text, old, new):
    if text.count(old) != 1:
        raise ValueError('Expected one exact source anchor: ' + repr(old[:180]))
    return text.replace(old, new, 1)


def checked_capsule(root, digest):
    assert identity(root / 'checkpoint.json')['sha256'] == digest
    value = json.loads((root / 'checkpoint.json').read_bytes())
    for row in value['files']:
        assert identity(root / row['path']) == {key: row[key] for key in ('bytes', 'sha256')}, row['path']
    return value


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--guard', type=Path, required=True)
    ap.add_argument('--guard-sha256', required=True)
    ap.add_argument('--guard-repo-path', required=True)
    ap.add_argument('--candidate-manifest', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    guard, output = args.guard.resolve(), args.output.resolve()
    parent = checked_capsule(PARENT, PARENT_SHA256)
    source = checked_capsule(guard, args.guard_sha256)
    assert source['source_files'] == 102 and source['android_executed'] is False
    assert type(source['distinct_host_tests_passed']) is int and source['distinct_host_tests_passed'] > 209
    assert len([row for row in source['files'] if row['path'].startswith('source/')]) == 102
    assert source['status'] == 'EXACT_ALARM_ENABLE_RETURN_HOST_AND_HISTORICAL_CONTROLS_PASSED_INACTIVE'
    assert source['complete_historical_schema6_verdict_unchanged'] is True
    assert identity(args.candidate_manifest) == {'bytes': 5189, 'sha256': CANDIDATE_MANIFEST_SHA256}
    candidate = json.loads(args.candidate_manifest.read_bytes())
    assert (candidate['filename'], candidate['size_bytes'], candidate['sha256']) == (CANDIDATE_FILENAME, 94683136, CANDIDATE_SHA256)
    sys.dont_write_bytecode = True
    sys.path[:0] = [str(guard / 'source/tools/parity_journeys'), str(guard / 'source/project')]
    import exact_alarm_enable_return as alarm
    import exact_alarm_enable_return_readiness as readiness
    import editor_journey as runner
    with alarm.configured_plan():
        plan = alarm.expected_plan()
        positive = {'schema': 7, 'plan': plan, 'plan_sha256': PLAN_SHA256,
                    alarm.POLICY_KEY: alarm.POLICY, readiness.POLICY_KEY: readiness.POLICY}
        alarm.require_navigation_policy(positive)
        readiness.require_policy(positive)
    assert len(plan) == 16 and runner.fingerprint(plan) == PLAN_SHA256
    assert alarm.CONTRACT_SHA256 == CONTRACT_SHA256 and alarm.REPORT_SCHEMA == 7
    assert alarm.POLICY_KEY == 'exact_alarm_enable_return_policy'
    assert alarm.POLICY['predicted_on_previously_observed'] is False
    assert alarm.POLICY['settings_inputs_total'] == 4 and alarm.POLICY['permission_api_result_observed'] is False
    readiness_sha = runner.fingerprint(readiness.POLICY)
    navigation_sha = runner.fingerprint(alarm.POLICY)
    output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(__file__, output / 'derive_workflow.py')
    before = {str(PARENT / row['path']): identity(PARENT / row['path']) for row in parent['files']}
    before.update({str(guard / row['path']): identity(guard / row['path']) for row in source['files']})
    before[str(args.candidate_manifest.resolve())] = identity(args.candidate_manifest)
    replacements = [(OLD_PACKAGE, PACKAGE), (OLD_GUARD, args.guard_repo_path),
        ('exact-alarm-navigation', 'exact-alarm-enable-return'),
        ('EXACT_ALARM_NAVIGATION', 'EXACT_ALARM_ENABLE_RETURN'),
        (OLD_APK_MANIFEST, CANDIDATE_MANIFEST), (OLD_APK_FILENAME, CANDIDATE_FILENAME),
        ('fourteen', 'sixteen'), ('FOURTEEN', 'SIXTEEN'),
        ('replay-source/', 'source/'),
        ('exact_alarm_journey', 'exact_alarm_enable_return'),
        ('exact_alarm_readiness', 'exact_alarm_enable_return_readiness')]
    changes, patch = [], ''
    for name in ('prepare_trigger_journey.py', 'verify_trigger_journey.py', 'validate_workflow.py'):
        original = (PARENT / name).read_text()
        value = original
        for old, new in replacements:
            value = value.replace(old, new)
        if name == 'prepare_trigger_journey.py':
            value = once(value, "'459960a6afc81fc0119cd66f3a9f6be823f7947ae90cd74c902d1a8a1e010afc'", repr(CANDIDATE_MANIFEST_SHA256))
            value = once(value, "'8deeece1c51d4320a72b065679f22a56242ea6769ed526e0c6436df405430857'", repr(args.guard_sha256))
            value = once(value, '[(GUARD, 166), (ANIMATION, 9)]', '[(GUARD, ' + str(len(source['files'])) + '), (ANIMATION, 9)]')
            row_fields = sorted(set(source['files'][0]))
            assert row_fields in [sorted(['path', 'bytes', 'sha256']), sorted(['path', 'bytes', 'sha256', 'mode'])]
            assert all(sorted(row) == row_fields for row in source['files'])
            if 'mode' in row_fields:
                value = once(value, "set(row) != {'path', 'bytes', 'sha256'}", "set(row) != ({'path', 'bytes', 'sha256', 'mode'} if package == GUARD else {'path', 'bytes', 'sha256'})")
            value = once(value, 'REPORT_SCHEMA = 6', 'REPORT_SCHEMA = 7')
            value = once(value, "READINESS_POLICY_SHA256 = 'ddcaa7d3751e701b923d382a2a4662514f79b9bdc9096f1e62600dffef5f3583'", 'READINESS_POLICY_SHA256 = ' + repr(readiness_sha))
            value = once(value, "NAVIGATION_POLICY_SHA256 = 'db0c6bc7802788fc649b47909500b050d173da62d0eb7bc9d226e4b824b63994'", 'NAVIGATION_POLICY_SHA256 = ' + repr(navigation_sha) + '\nSETTINGS_CONTRACT_SHA256 = ' + repr(CONTRACT_SHA256))
            value = value.replace(OLD_PLAN_SHA256, PLAN_SHA256)
            value = value.replace('exact_alarm_navigation_policy_sha256', 'exact_alarm_enable_return_policy_sha256')
            value = once(value, '94683119', '94683136')
            value = once(value, '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182', CANDIDATE_SHA256)
            value = once(value, "            or report.get('exact_alarm_enable_return_policy_sha256') != NAVIGATION_POLICY_SHA256\n", "            or report.get('exact_alarm_enable_return_policy_sha256') != NAVIGATION_POLICY_SHA256\n            or report.get('settings_contract_sha256') != SETTINGS_CONTRACT_SHA256\n")
            value = once(value, '                      exact_alarm_enable_return_policy_sha256=NAVIGATION_POLICY_SHA256,\n', '                      exact_alarm_enable_return_policy_sha256=NAVIGATION_POLICY_SHA256,\n                      settings_contract_sha256=SETTINGS_CONTRACT_SHA256,\n')
        elif name == 'verify_trigger_journey.py':
            value = value.replace('thirteen inputs', 'fifteen inputs')
            value = once(value, "len(run['screens']) != 14 or len(run['transitions']) != 13", "len(run['screens']) != 16 or len(run['transitions']) != 15")
            value = once(value, "len(replayed.get('screens', [])) != 14", "len(replayed.get('screens', [])) != 16")
            value = once(value, "                or replayed.get('settings_inputs') != 0\n                or replayed.get('permission_granted') is not False\n", "                or replayed.get('settings_inputs') != 4\n                or replayed.get('settings_inputs_per_run') != 2\n                or replayed.get('settings_enabled_state_observed') is not True\n                or replayed.get('settings_return_navigation_observed') is not True\n                or replayed.get('permission_api_result_observed') is not False\n")
            value = once(value, ".get('planned_inputs') != 26", ".get('planned_inputs') != 30")
            value = once(value, ".get('settings_inputs') != 0", ".get('settings_inputs') != 4")
            value = once(value, 'EXACT_ALARM_SETTINGS_OBSERVATION_ONLY', 'EXACT_ALARM_ENABLED_RETURN_OBSERVATION_ONLY')
        else:
            value = once(value, "    parser.add_argument('--output', type=Path, required=True)\n", "    parser.add_argument('--output', type=Path, required=True)\n    parser.add_argument('--candidate-manifest', type=Path, required=True)\n    parser.add_argument('--candidate-apk', type=Path, required=True)\n")
            value = once(value, "return workspace / 'combined-recovery/checkpoints/05-full-acceptance/apk/manifest.json'", 'return args.candidate_manifest.resolve()')
            value = once(value, "Path(json.loads((workspace / 'combined-recovery/reports/05-full-acceptance/result.json').read_text())['project']) / 'dist/MacroDroid-5.67.8-v9-hybrid.apk'", 'args.candidate_apk.resolve()')
            value = value.replace('exact_alarm_navigation_policy_sha256', 'exact_alarm_enable_return_policy_sha256')
            value = once(value, "            ('older-thirteen-plan-pin', 'older-plan', False, False),\n", "            ('older-fourteen-plan-pin', 'older-plan', False, False),\n            ('missing-settings-contract-pin', 'omit-settings-contract', False, False),\n            ('changed-settings-contract-pin', 'changed-settings-contract', False, False),\n")
            value = once(value, "            elif mode == 'omit-reviewed':\n", "            elif mode == 'omit-settings-contract':\n                del declared['settings_contract_sha256']\n            elif mode == 'changed-settings-contract':\n                declared['settings_contract_sha256'] = '0' * 64\n            elif mode == 'omit-reviewed':\n")
            value = once(value, "declared['plan_sha256'] = '42ece5a06a280186ddf9796a4524975d478263e545260674e2b1b4cf718d46fb'", "declared['plan_sha256'] = " + repr(OLD_PLAN_SHA256))
            # The small literal policy program is stored as a string in the predecessor.
            start = value.index('        policy_script.write_text(')
            end = value.index('\n        policy_result = ', start)
            expression = value[start:end].strip()
            call = ast.parse(expression).body[0].value
            program = ast.literal_eval(call.args[0])
            program = once(program, "positive = {'schema': 6", "positive = {'schema': 7")
            program = once(program, "if label == 'legacy-schema': value['schema'] = 5", "if label == 'legacy-schema': value['schema'] = 6")
            program = once(program, "elif label == 'unregistered-schema': value['schema'] = 7", "elif label == 'unregistered-schema': value['schema'] = 8")
            program = once(program, "value[alarm.POLICY_KEY]['settings_inputs'] = 1", "value[alarm.POLICY_KEY]['settings_inputs_total'] = 1")
            program = program.replace('Missing, altered or misplaced exact-alarm navigation policy or plan', 'Missing, altered or misplaced exact-alarm enable/return policy or plan')
            value = value[:start] + '        policy_script.write_text(' + repr(program) + ')' + value[end:]
            start = value.index("        host = next(step['run'] for step in steps if step['name'].startswith('Run the frozen capture'))")
            end = value.index("        runtime = next(step['run']", start)
            value = value[:start] + "        closed_source = json.loads((args.guard.resolve() / 'checkpoint.json').read_bytes())\n        if (closed_source['source_files'] != 102 or closed_source['android_executed'] is not False\n                or closed_source['distinct_host_tests_passed'] != " + str(source['distinct_host_tests_passed']) + "):\n            raise ValueError('Closed source host-control evidence differs')\n        report['source_host_controls_reused'] = {'checkpoint_sha256': preparation.PINS[preparation.GUARD + '/checkpoint.json'],\n            'distinct_tests': closed_source['distinct_host_tests_passed'], 'locally_reexecuted': False,\n            'hosted_workflow_still_executes_full_suite': True}\n" + value[end:]
        ast.parse(value, filename=name)
        target = output / name
        with target.open('x') as stream:
            stream.write(value)
        changes.append({'path': name, 'before': identity(PARENT / name), 'after': identity(target)})
        patch += ''.join(difflib.unified_diff(original.splitlines(True), value.splitlines(True), fromfile='parent/' + name, tofile='successor/' + name))
    old_workflow = '.github/workflows/editor-exact-alarm-navigation.yml'
    new_workflow = '.github/workflows/editor-exact-alarm-enable-return.yml'
    original = (PARENT / old_workflow).read_text()
    workflow = original
    for old, new in replacements:
        workflow = workflow.replace(old, new)
    for name in ('prepare_trigger_journey.py', 'verify_trigger_journey.py'):
        workflow = once(workflow, identity(PARENT / name)['sha256'], identity(output / name)['sha256'])
    target = output / new_workflow
    target.parent.mkdir(parents=True)
    with target.open('x') as stream:
        stream.write(workflow)
    changes.append({'path': new_workflow, 'before': identity(PARENT / old_workflow), 'after': identity(target)})
    patch += ''.join(difflib.unified_diff(original.splitlines(True), workflow.splitlines(True), fromfile='parent/' + old_workflow, tofile='successor/' + new_workflow))
    (output / 'derivation.patch').write_text(patch)
    after = {name: identity(Path(name)) for name in before}
    assert after == before
    (output / 'source-bindings.json').write_text(json.dumps({
        'schema': 1, 'status': 'INACTIVE_WORKFLOW_DERIVED_NOT_YET_VALIDATED',
        'parent_checkpoint': {'path': str(PARENT), 'sha256': PARENT_SHA256},
        'guard_checkpoint': {'path': str(guard), 'sha256': args.guard_sha256},
        'guard_repo_path': args.guard_repo_path, 'workflow_package': PACKAGE,
        'source_files': 102, 'guard_payloads': len(source['files']),
        'host_tests_in_closed_source': source['distinct_host_tests_passed'],
        'report_schema': 7, 'plan_sha256': PLAN_SHA256, 'settings_contract_sha256': CONTRACT_SHA256,
        'readiness_policy_sha256': readiness_sha, 'enable_return_policy_sha256': navigation_sha,
        'candidate_manifest_sha256': CANDIDATE_MANIFEST_SHA256,
        'candidate_apk_sha256': CANDIDATE_SHA256, 'screens_per_run': 16, 'inputs_per_run': 15,
        'settings_inputs_total': 4, 'predicted_on_previously_observed': False,
        'android_executed': False, 'active_files': [], 'changes': changes,
        'before': before, 'after': after, 'all_inputs_unchanged': True,
    }, indent=2) + '\n')
    print(json.dumps({'output': str(output), 'workflow': identity(target), 'source_files': 102,
                      'plan_sha256': PLAN_SHA256, 'android_executed': False}, indent=2))


if __name__ == '__main__':
    main()
