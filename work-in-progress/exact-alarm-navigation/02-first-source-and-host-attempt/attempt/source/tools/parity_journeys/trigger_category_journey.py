#!/usr/bin/env python3
"""Observe one Date/Time trigger-category expansion after the verified first-use tip.

The twelve-screen sequence adds only the observed trigger + and Date/Time row.
It records the resulting app surface, then stops without selecting a trigger,
saving a macro, executing a macro, or changing an APK.
"""
from __future__ import annotations

from contextlib import contextmanager
import copy
import re

import editor_journey as runner
import favourite_info_journey as favourite
import observed_journey as observed

TEN_PLAN_SHA256 = '5a8ca21b8e96b0ae2cfe55bc944e93749534209ca81b04141ce77eef0416c453'
EDITOR = favourite.EDITOR
CATALOG = runner.PACKAGE + '/' + runner.PACKAGE + '.selectableitemlist.AddTriggerActivity'
TITLE = favourite.TITLE
OK = favourite.OK
DATE_TIME = {'resource-id': runner.PACKAGE + ':id/category_name', 'text': 'Date/Time'}
CATALOG_TITLE = {'text': 'Add Trigger'}


def expected_plan():
    prefix = favourite.expected_plan()
    if runner.fingerprint(prefix) != TEN_PLAN_SHA256:
        raise runner.JourneyError('Reviewed ten-screen prefix changed')
    plan = copy.deepcopy(prefix)
    # The prior actual sixteen-screen run observed this exact editor after OK.
    plan[-1][2] = runner.TRIGGER
    return plan + [
        ['trigger-catalog', runner.PACKAGE, CATALOG_TITLE, runner.TRIGGER],
        ['after-trigger-date-category', runner.PACKAGE, None, DATE_TIME],
    ]


def require_plan():
    if runner.fingerprint(runner.PLAN) != runner.fingerprint(expected_plan()):
        raise runner.JourneyError('Trigger-category sequence differs from the reviewed two additional inputs')


@contextmanager
def configured_plan():
    with favourite.configured_plan():
        previous = runner.PLAN
        try:
            runner.PLAN = expected_plan()
            yield runner.PLAN
        finally:
            runner.PLAN = previous


def dialog_identity(folder, shot, proof):
    require_plan()
    return favourite._dialog_identity(folder, shot, proof)


def installed_guard(recorder, run):
    require_plan()
    return favourite.installed_guard(recorder, run)


def verify_installed_guard(folder, transition, run, proof):
    require_plan()
    return favourite._verify_installed_guard(folder, transition, run, proof)


def exact_component(folder, shot, expected, proof):
    if shot['owner'] != runner.PACKAGE:
        raise runner.JourneyError('Observed surface belongs to another package')
    for key in ['foreground', 'foreground_final']:
        if observed.component(proof.artifact(folder, shot['artifacts'][key]), proof) != expected:
            raise runner.JourneyError('Observed editor/catalog component changed')


def editor_identity(folder, shot, proof):
    require_plan()
    exact_component(folder, shot, EDITOR, proof)
    data = proof.artifact(folder, shot['artifacts']['hierarchy'])
    root = runner.tree(data, runner.PACKAGE)
    node = runner.select(root, runner.PACKAGE, runner.TRIGGER)
    if (node.get('class') != 'android.widget.ImageButton' or node.get('enabled') != 'true'
            or node.get('clickable') != 'true' or node.get('content-desc') != 'Add Trigger'):
        raise runner.JourneyError('Observed editor trigger-add button changed')
    width, height, _ = observed.png_pixels(proof.artifact(folder, shot['artifacts']['screenshot']), proof)
    return runner.target(data, runner.PACKAGE, runner.TRIGGER, width, height)


def category_identity(folder, shot, proof):
    require_plan()
    exact_component(folder, shot, CATALOG, proof)
    data = proof.artifact(folder, shot['artifacts']['hierarchy'])
    root = runner.tree(data, runner.PACKAGE)
    title = runner.select(root, runner.PACKAGE, CATALOG_TITLE)
    node = runner.select(root, runner.PACKAGE, DATE_TIME)
    parents = {child: parent for parent in root.iter() for child in parent}
    background = parents.get(node)
    container = parents.get(background) if background is not None else None
    if (title.get('class') != 'android.widget.TextView' or title.get('enabled') != 'true'
            or node.get('class') != 'android.widget.TextView' or node.get('enabled') != 'true'
            or node.get('clickable') != 'false' or background is None or container is None
            or background.get('package') != runner.PACKAGE or background.get('class') != 'android.widget.LinearLayout'
            or background.get('resource-id') != runner.PACKAGE + ':id/background'
            or background.get('enabled') != 'true' or background.get('clickable') != 'false'
            or container.get('package') != runner.PACKAGE or container.get('class') != 'android.widget.LinearLayout'
            or container.get('resource-id') != runner.PACKAGE + ':id/category_container'
            or container.get('enabled') != 'true' or container.get('clickable') != 'true'):
        raise runner.JourneyError('Observed Date/Time category ancestor chain changed')
    width, height, _ = observed.png_pixels(proof.artifact(folder, shot['artifacts']['screenshot']), proof)
    containing = (0, 0, width, height)
    for item in (container, background, node):
        bounds = re.fullmatch(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', item.get('bounds', ''))
        if bounds is None:
            raise runner.JourneyError('Observed Date/Time ancestor bounds are invalid')
        left, top, right, bottom = map(int, bounds.groups())
        if not (containing[0] <= left < right <= containing[2]
                and containing[1] <= top < bottom <= containing[3]):
            raise runner.JourneyError('Observed Date/Time ancestor bounds are inconsistent or off screen')
        containing = (left, top, right, bottom)
    return runner.target(data, runner.PACKAGE, DATE_TIME, width, height)


def terminal_surface(folder, shot, proof):
    require_plan()
    if shot.get('name') != 'after-trigger-date-category' or shot['owner'] != runner.PACKAGE:
        raise runner.JourneyError('Unexpected terminal trigger-category observation')
    first = observed.component(proof.artifact(folder, shot['artifacts']['foreground']), proof)
    last = observed.component(proof.artifact(folder, shot['artifacts']['foreground_final']), proof)
    if first != last or last.split('/', 1)[0] != runner.PACKAGE:
        raise runner.JourneyError('Terminal app component is not stable')
    return {'name': shot['name'], 'owner': runner.PACKAGE, 'component': last,
            'surface_after_one_observed_date_category_tap': True, 'subsequent_inputs': 0}


def required_surface(folder, shot, required, proof):
    require_plan()
    name = shot['name']
    if name == 'favourite-triggers-info':
        dialog_identity(folder, shot, proof)
    elif name == 'after-favourite-info':
        editor_identity(folder, shot, proof)
    elif name == 'trigger-catalog':
        category_identity(folder, shot, proof)
    elif name == 'after-trigger-date-category':
        if required is not None:
            raise runner.JourneyError('The newly observed terminal surface has an assumed selector')
        return terminal_surface(folder, shot, proof)
    if required is None:
        raise runner.JourneyError('Only the exact reviewed terminal observation may omit a selector')
    runner.select(runner.tree(proof.artifact(folder, shot['artifacts']['hierarchy']), shot['owner']), shot['owner'], required)
    return None


def input_identity(folder, previous, before, action, name, proof):
    require_plan()
    if name == 'trigger-catalog':
        if previous.get('name') != 'after-favourite-info' or action != runner.TRIGGER:
            raise runner.JourneyError('Trigger-add tap is outside its observed editor boundary')
        editor_identity(folder, before, proof)
    elif name == 'after-trigger-date-category':
        if previous.get('name') != 'trigger-catalog' or action != DATE_TIME:
            raise runner.JourneyError('Date/Time tap is outside its observed catalog boundary')
        category_identity(folder, before, proof)


def main():
    with configured_plan():
        return runner.main()


if __name__ == '__main__':
    raise SystemExit(main())
