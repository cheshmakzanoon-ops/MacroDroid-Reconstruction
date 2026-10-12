#!/usr/bin/env python3
"""Preserve the failed first attempt and derive its narrowly corrected successor."""
from pathlib import Path
import difflib
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
CHECKPOINT_SHA = '53ab171c643dbebb7093ec4b625ba1f32f6d6950017c6ef7d1890e791975f2fc'


def identity(path):
    return {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def once(value, before, after):
    if value.count(before) != 1:
        raise ValueError('A correction anchor is no longer unique')
    return value.replace(before, after, 1)


def main():
    frozen = ROOT / 'checkpoints/01-host-plan-rejection-controls'
    if identity(frozen / 'checkpoint.json')['sha256'] != CHECKPOINT_SHA:
        raise ValueError('The failed first-attempt checkpoint changed')
    manifest = json.loads((frozen / 'checkpoint.json').read_text())
    for row in manifest['files']:
        if identity(frozen / row['path']) != {key: row[key] for key in ('bytes', 'sha256')}:
            raise ValueError('A frozen first-attempt file changed: ' + row['path'])
    prior = ROOT / 'stage-01'
    expected = json.loads((prior / 'reports/host-controls-01/inputs-after.json').read_text())
    for relative, row in expected.items():
        if identity(prior / 'repository' / relative) != row:
            raise ValueError('The measured first-attempt stage changed')
    stage = ROOT / 'stage-02'
    stage.mkdir(exist_ok=False)
    shutil.copytree(prior / 'repository', stage / 'repository')
    shutil.copytree(prior / 'syntax-preflight', stage / 'syntax-preflight')
    for name in ['parent-source-identities.json', 'parent-checkpoint.json']:
        shutil.copy2(prior / name, stage / name)
    folder = stage / 'repository/tools/parity_journeys'
    changes = []
    patch = (prior / 'derivation.patch').read_text()
    path = folder / 'observed_journey.py'
    before = path.read_text()
    after = once(before,
        '    if len(runner.PLAN) in (10, 12, 13):\n        information_adapter().require_plan()\n',
        '    if len(runner.PLAN) in (10, 12, 13):\n        information_adapter().require_plan()\n'
        "    elif runner.fingerprint(runner.PLAN) != '69bae4f2af8e2f14c407808dbcdea91cdca009af2ae390e13b5c7fbf035a3065':\n"
        "        raise runner.JourneyError('Historical fourteen-screen plan differs from its reviewed complete identity')\n")
    path.write_text(after)
    changes.append({'path': path.relative_to(stage / 'repository').as_posix(),
                    'before_sha256': hashlib.sha256(before.encode()).hexdigest(), 'after': identity(path)})
    patch += ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                       fromfile='attempt-01/observed_journey.py', tofile='attempt-02/observed_journey.py'))
    path = folder / 'test_day_time_journey.py'
    before = path.read_text()
    after = once(before,
        '        with category.configured_plan():\n            self.assertEqual(len(runner.PLAN), 12); observed.require_plan()\n',
        '        # The existing reference context only enters from the original base plan.\n'
        '        with self.assertRaises(runner.JourneyError):\n'
        '            with category.configured_plan():\n                pass\n'
        '        self.assertEqual(len(runner.PLAN), 13); observed.require_plan()\n'
        "        with patch.object(runner, 'PLAN', twelve):\n"
        '            self.assertEqual(len(runner.PLAN), 12); observed.require_plan()\n')
    after = once(after, '    def test_terminal_is_a_stable_unassumed_app_surface_with_no_configuration_confirmation(self):\n',
        '    def test_all_historical_fourteen_steps_must_match_the_fixed_complete_plan(self):\n'
        '        from test_observed_journey import reviewed_historical_plan\n'
        '        historical = reviewed_historical_plan()\n'
        "        with patch.object(runner, 'PLAN', historical):\n            observed.require_plan()\n"
        '        for index in range(14):\n'
        '            changed = copy.deepcopy(historical)\n'
        "            changed[index][3] = {'text': 'Unobserved Action'}\n"
        "            with self.subTest(step=index), patch.object(runner, 'PLAN', changed), self.assertRaises(runner.JourneyError):\n"
        '                observed.require_plan()\n\n'
        '    def test_terminal_is_a_stable_unassumed_app_surface_with_no_configuration_confirmation(self):\n')
    path.write_text(after)
    changes.append({'path': path.relative_to(stage / 'repository').as_posix(),
                    'before_sha256': hashlib.sha256(before.encode()).hexdigest(), 'after': identity(path)})
    patch += ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                       fromfile='attempt-01/test_day_time_journey.py', tofile='attempt-02/test_day_time_journey.py'))
    (stage / 'derivation.patch').write_text(patch)
    record = {'failed_parent_checkpoint_sha256': CHECKPOINT_SHA, 'changes': changes,
              'first_attempt_outcome': '144 tests: one plan-identity bypass failure and one invalid nested-context test assumption',
              'android_executed': False, 'active_changes': False}
    (stage / 'correction.json').write_text(json.dumps(record, indent=2) + '\n')
    (stage / 'CORRECTION.md').write_text('# Correction after the measured first attempt\n\n'
        'The complete first attempt remains frozen in checkpoint 01. Its arbitrary fourteen-step '
        'plan passed the old policy because only three prefix steps and the total length were '
        'checked. The corrected guard binds every step of the already reviewed historical '
        'fourteen-step plan to its canonical SHA256; adding a screen to the new thirteen-step '
        'plan now rejects. The historical positive remains supported with its exact identity.\n\n'
        'The other error came from a test assuming the existing reference context could be '
        'entered while already inside the new context. The reference context correctly rejects '
        'a changed base plan. The corrected test asserts that rejection, confirms the current '
        'plan is preserved and checks the twelve-screen router under a temporary explicit plan. '
        'No existing reference-context implementation changes.\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
