#!/usr/bin/env python3
"""Derive a separate thirteen-screen workflow from the frozen twelve-screen experiment."""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import sys

PARENT_SHA = 'a6a279c48af61b553728eeaf05f92c8cf15e34bd5b4fdd907e193d31a63a5af0'


def identity(path):
    return {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def once(value, before, after):
    if value.count(before) != 1:
        raise ValueError('Expected one workflow derivation anchor: ' + repr(before[:80]))
    return value.replace(before, after, 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--guard', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    workspace = Path(__file__).resolve().parent.parent
    parent = workspace / 'trigger-catalog-forward/checkpoints/08-zero-scale-twelve-screen-workflow'
    if identity(parent / 'checkpoint.json')['sha256'] != PARENT_SHA:
        raise ValueError('The closed parent workflow checkpoint changed')
    parent_manifest = json.loads((parent / 'checkpoint.json').read_text())
    parent_files = {row['path']: {key: row[key] for key in ('bytes', 'sha256')}
                    for row in parent_manifest['files']}
    guard = args.guard.resolve()
    manifest = json.loads((guard / 'checkpoint.json').read_text())
    if manifest['status'] != 'HOST_CONTROLS_PASSED_INACTIVE' or manifest['android_executed'] is not False:
        raise ValueError('A closed positive host guard is required')
    for row in manifest['files']:
        if identity(guard / row['path']) != {key: row[key] for key in ('bytes', 'sha256')}:
            raise ValueError('The closed guard input changed: ' + row['path'])
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(guard / 'replay-source/tools/parity_journeys'))
    import day_time_journey as day
    import editor_journey as runner
    plan = day.expected_plan()
    if len(plan) != 13 or plan[-1] != ['after-day-time-trigger', runner.PACKAGE, None, day.DAY_TIME]:
        raise ValueError('The new guard no longer declares one additional Day/Time tap')
    plan_sha = runner.fingerprint(plan)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source_names = ['prepare_trigger_journey.py', 'verify_trigger_journey.py',
                    'build_workflow.py', 'validate_workflow.py', 'freeze_trigger_zero_workflow.py']
    replacements = [
        ('work-in-progress/trigger-category-workflow/02-zero-scale-workflow',
         'work-in-progress/day-time-trigger-workflow/01-zero-scale-workflow'),
        ('work-in-progress/trigger-category/05-physical-identity-host-success',
         'work-in-progress/day-time-trigger/02-host-success'),
        ('trigger-catalog-forward/checkpoints/05-physical-identity-host-success',
         'day-time-trigger-forward/checkpoints/02-host-success'),
        ('editor-trigger-category', 'editor-day-time-trigger'),
        ('ci-trigger-category', 'ci-day-time-trigger'),
        ('macrodroid-trigger-category-tooling', 'macrodroid-day-time-trigger-tooling'),
        ('--id trigger-category-', '--id day-time-trigger-'),
        ('trigger-category-verification.json', 'day-time-trigger-verification.json'),
        ('trigger_category_journey', 'day_time_journey'),
        ('TRIGGER_CATEGORY', 'DAY_TIME_TRIGGER'),
        ('TWELVE_SCREEN', 'THIRTEEN_SCREEN'),
        ('twelve-screen', 'thirteen-screen'),
        ('twelve full-frame', 'thirteen full-frame'),
        ('eleven inputs each', 'twelve inputs each'),
        ('Observe the twelve declared', 'Observe the thirteen declared'),
        ('the twelve declared screens', 'the thirteen declared screens'),
        ('freeze_trigger_zero_workflow.py', 'freeze_day_time_workflow.py'),
    ]
    bindings, changes, patch = {}, [], ''
    for name in source_names:
        original = parent / name
        if identity(original) != parent_files[name]:
            raise ValueError('A bound parent workflow source changed: ' + name)
        bindings[name] = parent_files[name]
        before = original.read_text()
        after = before
        for old, new in replacements:
            after = after.replace(old, new)
        if name == 'prepare_trigger_journey.py':
            after = once(after, "GUARD + '/checkpoint.json': '8c985ee7da3a2f3d0dab9a9b93cac49b07246f9f78f8b0b897144c60c085f743'",
                         "GUARD + '/checkpoint.json': '" + identity(guard / 'checkpoint.json')['sha256'] + "'")
            after = once(after, '[(GUARD, 97), (ANIMATION, 9)]',
                         '[(GUARD, ' + str(len(manifest['files'])) + '), (ANIMATION, 9)]')
            after = after.replace('940be18b226ab29de46ea48a1496238b8a2221a52077466693a34a2113bc24cc', plan_sha)
        if name == 'verify_trigger_journey.py':
            after = after.replace("len(run['screens']) != 12", "len(run['screens']) != 13")
            after = after.replace("len(run['transitions']) != 11", "len(run['transitions']) != 12")
            after = after.replace("len(replayed.get('screens', [])) != 12", "len(replayed.get('screens', [])) != 13")
            after = once(after, "                or replayed.get('trigger_selected') is not False\n",
                "                or replayed.get('trigger_type_tapped') is not True\n"
                "                or replayed.get('trigger_configuration_confirmed') is not False\n")
        if name == 'freeze_trigger_zero_workflow.py':
            start = after.index("    readme.write_text('''")
            end = after.index("''')", start) + 4
            after = after[:start] + '''    readme.write_text(''' + repr(
                '# Day/Time trigger: thirteen observed screens at animation scale zero\n\n'
                'This separate workflow adds one Day/Time type tap to the exact twelve-screen '
                'prefix. Both raw AddTriggerActivity captures identify the nearest clickable '
                'row at (184, 626). The resulting app surface is observed without assuming its '
                'activity or controls. Its terminal component must be stable and equal in both '
                'runs; no trigger configuration is confirmed and no macro is saved or executed.\n\n'
                'The original84333011 and combined5f635e APKs, API35 runtime, nineteen raw zero-scale '
                'configuration commands, radio/demo-clock preparation, exact input inventory, '
                'owned service cleanup and complete raw artifact preservation remain independently '
                'bound. Every one of the thirteen PNG/XML pairs is compared in full with a zero '
                'changed-pixel threshold. Shared crash continuation remains explicitly scoped.\n\n'
                'The earlier twelve-screen run38216299675 has a real five-pixel intro difference. '
                'It remains a failure. This new workflow extends the observed interaction space; '
                'its fresh Android outcome must be evaluated independently. Offline host and '
                'workflow controls are not an Android or whole-application parity result.\n\n'
                'Checkpoint01 preserves the first guard attempt, including a fourteen-step plan '
                'identity bypass and an unsupported nested-context test assumption. Guard02 fixes '
                'the complete historical plan identity and records corrected host controls. '
                'All input copies and raw offline outputs are mapped to exact deduplicated '
                'payloads. Exact previously published APK/tool bytes retain commit/manifest '
                'references, and deliberate symlink controls remain inert metadata.\n'
            ) + ')\n' + after[end:]
            after = once(after, "                 'parent-source-identities.json', 'derivation.patch'):",
                         "                 'parent-source-identities.json', 'derivation.patch', 'derive_workflow.py'):")
        target_name = 'freeze_day_time_workflow.py' if name == 'freeze_trigger_zero_workflow.py' else name
        target = output / target_name
        target.write_text(after)
        changes.append({'parent_path': name, 'path': target_name, 'before': parent_files[name], 'after': identity(target)})
        patch += ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                           fromfile='twelve-screen/' + name, tofile='thirteen-screen/' + target_name))
    shutil.copy2(Path(__file__), output / 'derive_workflow.py')
    (output / 'derivation.patch').write_text(patch)
    record = {'parent_checkpoint_sha256': PARENT_SHA, 'parent_sources': bindings, 'changes': changes,
              'guard_checkpoint': identity(guard / 'checkpoint.json'), 'guard_file_count': len(manifest['files']),
              'plan_sha256': plan_sha, 'android_executed': False, 'active_changes': False}
    (output / 'parent-source-identities.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
