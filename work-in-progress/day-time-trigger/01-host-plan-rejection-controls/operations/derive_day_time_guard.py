#!/usr/bin/env python3
"""Derive a separately reviewed thirteen-screen adapter from the unchanged twelve-screen source."""
from pathlib import Path
import difflib, hashlib, json

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'stage-01/repository/tools/parity_journeys'

def replace_once(text, old, new):
    if text.count(old) != 1: raise RuntimeError('Derivation anchor must be unique: ' + repr(old[:100]))
    return text.replace(old, new, 1)

def main():
    target = SOURCE / 'day_time_journey.py'
    if target.exists(): raise RuntimeError('Derived adapter already exists')
    category = (SOURCE / 'trigger_category_journey.py').read_text()
    text = category
    start, end = text.index('"""'), text.index('"""', text.index('"""') + 3) + 3
    text = text[:start] + '''"""Tap the exact observed Day/Time trigger tile after the twelve-screen prefix.

The next app surface is recorded without an assumed selector. This proves only
the declared type tap and ensuing observation; no configuration is confirmed.
"""''' + text[end:]
    text = replace_once(text, 'import observed_journey as observed', 'import observed_journey as observed\nimport trigger_category_journey as category')
    text = replace_once(text, "TEN_PLAN_SHA256 = '5a8ca21b8e96b0ae2cfe55bc944e93749534209ca81b04141ce77eef0416c453'",
                        "TWELVE_PLAN_SHA256 = '940be18b226ab29de46ea48a1496238b8a2221a52077466693a34a2113bc24cc'")
    text = replace_once(text, "CATALOG_TITLE = {'text': 'Add Trigger'}", "CATALOG_TITLE = {'text': 'Add Trigger'}\nDAY_TIME = {'resource-id': runner.PACKAGE + ':id/select_item_name', 'text': 'Day/Time'}")
    start, end = text.index('def expected_plan():'), text.index('\n\ndef require_plan():')
    text = text[:start] + '''def expected_plan():
    prefix = category.expected_plan()
    if runner.fingerprint(prefix) != TWELVE_PLAN_SHA256:
        raise runner.JourneyError('Reviewed twelve-screen prefix changed')
    plan = copy.deepcopy(prefix)
    plan[-1][2] = DAY_TIME
    return plan + [['after-day-time-trigger', runner.PACKAGE, None, DAY_TIME]]
''' + text[end:]
    text = replace_once(text, 'Trigger-category sequence differs from the reviewed two additional inputs',
                        'Day/Time sequence differs from the reviewed one additional input')
    text = replace_once(text, 'with favourite.configured_plan():', 'with category.configured_plan():')
    identity = '''def day_time_identity(folder, shot, proof):
    require_plan()
    exact_component(folder, shot, CATALOG, proof)
    data = proof.artifact(folder, shot['artifacts']['hierarchy'])
    root = runner.tree(data, runner.PACKAGE)
    title = runner.select(root, runner.PACKAGE, CATALOG_TITLE)
    heading = runner.select(root, runner.PACKAGE, DATE_TIME)
    node = runner.select(root, runner.PACKAGE, DAY_TIME)
    if (title.get('class') != 'android.widget.TextView' or title.get('enabled') != 'true'
            or heading.get('class') != 'android.widget.TextView' or heading.get('enabled') != 'true'):
        raise runner.JourneyError('Observed Date/Time catalog title or heading changed')
    parents = {child: parent for parent in root.iter() for child in parent}
    chain = [node]
    for _ in range(3):
        if chain[-1] not in parents:
            raise runner.JourneyError('Observed Day/Time row ancestor is missing')
        chain.append(parents[chain[-1]])
    roles = [
        ('android.widget.TextView', runner.PACKAGE + ':id/select_item_name', 'false'),
        ('android.widget.LinearLayout', '', 'false'),
        ('android.widget.FrameLayout', runner.PACKAGE + ':id/select_item_container', 'false'),
        ('android.widget.LinearLayout', runner.PACKAGE + ':id/select_item_row_frame', 'true'),
    ]
    for item, (kind, resource, clickable) in zip(chain, roles):
        if (item.get('package') != runner.PACKAGE or item.get('class') != kind
                or item.get('resource-id', '') != resource or item.get('enabled') != 'true'
                or item.get('clickable') != clickable):
            raise runner.JourneyError('Observed Day/Time row ancestor chain changed')
    width, height, _ = observed.png_pixels(proof.artifact(folder, shot['artifacts']['screenshot']), proof)
    containing = (0, 0, width, height)
    for item in reversed(chain):
        bounds = re.fullmatch(r'\\[(\\d+),(\\d+)\\]\\[(\\d+),(\\d+)\\]', item.get('bounds', ''))
        if bounds is None:
            raise runner.JourneyError('Observed Day/Time row bounds are invalid')
        left, top, right, bottom = map(int, bounds.groups())
        if not (containing[0] <= left < right <= containing[2]
                and containing[1] <= top < bottom <= containing[3]):
            raise runner.JourneyError('Observed Day/Time row bounds are inconsistent or off screen')
        containing = (left, top, right, bottom)
    return runner.target(data, runner.PACKAGE, DAY_TIME, width, height)


'''
    text = replace_once(text, 'def terminal_surface(folder, shot, proof):', identity + 'def terminal_surface(folder, shot, proof):')
    text = replace_once(text, "if shot.get('name') != 'after-trigger-date-category' or shot['owner'] != runner.PACKAGE:",
                        "if shot.get('name') != 'after-day-time-trigger' or shot['owner'] != runner.PACKAGE:")
    text = replace_once(text, 'Unexpected terminal trigger-category observation', 'Unexpected terminal Day/Time trigger observation')
    text = replace_once(text, "'surface_after_one_observed_date_category_tap': True, 'subsequent_inputs': 0", "'surface_after_one_observed_day_time_tap': True, 'subsequent_inputs': 0,\n            'trigger_type_tapped': True, 'trigger_configuration_confirmed': False")
    text = replace_once(text, "    elif name == 'after-trigger-date-category':\n        if required is not None:",
                        "    elif name == 'after-trigger-date-category':\n        day_time_identity(folder, shot, proof)\n    elif name == 'after-day-time-trigger':\n        if required is not None:")
    text = replace_once(text, "        category_identity(folder, before, proof)\n\n\ndef main():",
                        "        category_identity(folder, before, proof)\n    elif name == 'after-day-time-trigger':\n        if previous.get('name') != 'after-trigger-date-category' or action != DAY_TIME:\n            raise runner.JourneyError('Day/Time tap is outside its observed expanded-category boundary')\n        day_time_identity(folder, before, proof)\n\n\ndef main():")
    target.write_text(text)

    observed_path = SOURCE / 'observed_journey.py'; old_observed = observed_path.read_text(); new_observed = old_observed
    new_observed = replace_once(new_observed, "    elif len(runner.PLAN) == 12:\n        import trigger_category_journey as adapter\n",
                                "    elif len(runner.PLAN) == 12:\n        import trigger_category_journey as adapter\n    elif len(runner.PLAN) == 13:\n        import day_time_journey as adapter\n")
    new_observed = replace_once(new_observed, 'len(runner.PLAN) not in (10, 12, 14)', 'len(runner.PLAN) not in (10, 12, 13, 14)')
    new_observed = replace_once(new_observed, 'len(runner.PLAN) in (10, 12):', 'len(runner.PLAN) in (10, 12, 13):')
    new_observed = replace_once(new_observed, '    if len(runner.PLAN) == 12:\n        return information_adapter().required_surface',
                                '    if len(runner.PLAN) in (12, 13):\n        return information_adapter().required_surface')
    new_observed = replace_once(new_observed, '    if len(runner.PLAN) == 12:\n        information_adapter().input_identity',
                                '    if len(runner.PLAN) in (12, 13):\n        information_adapter().input_identity')
    observed_path.write_text(new_observed)

    runner_path = SOURCE / 'editor_journey.py'; old_runner = runner_path.read_text(); new_runner = old_runner
    new_runner = replace_once(new_runner,
        "                result['status'] = 'EXACT_TRIGGER_CATEGORY_OBSERVATION_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'",
        "                result['status'] = 'EXACT_TRIGGER_CATEGORY_OBSERVATION_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'\n"
        "            elif len(PLAN) == 13:\n"
        "                result['scope'] = 'Observed first-use dialog, trigger catalog, Date/Time category and one Day/Time trigger-type tap; the resulting app surface only'\n"
        "                result['catalog_navigation_established'] = True\n"
        "                result['trigger_type_tapped'] = True\n"
        "                result['trigger_configuration_confirmed'] = False\n"
        "                result['status'] = 'EXACT_DAY_TIME_TRIGGER_OBSERVATION_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'")
    runner_path.write_text(new_runner)
    patch = ''.join(difflib.unified_diff(category.splitlines(True), text.splitlines(True),
                                         fromfile='parent/trigger_category_journey.py', tofile='proposed/day_time_journey.py'))
    for name, before, after in [('observed_journey.py', old_observed, new_observed), ('editor_journey.py', old_runner, new_runner)]:
        patch += ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='parent/' + name, tofile='proposed/' + name))
    (ROOT / 'stage-01/derivation.patch').write_text(patch)
    print(json.dumps({'status': 'PRIVATE_THIRTEEN_SCREEN_GUARD_DERIVED',
                      'derivedAdapterSha256': hashlib.sha256(target.read_bytes()).hexdigest(),
                      'activeWorkflowChanged': False, 'androidExecuted': False}, indent=2))

if __name__ == '__main__': main()
