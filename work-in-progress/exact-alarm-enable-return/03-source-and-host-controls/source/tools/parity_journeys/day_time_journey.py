#!/usr/bin/env python3
"""Tap the exact observed Day/Time trigger tile after the twelve-screen prefix.

The next app surface is recorded without an assumed selector. This proves only
the declared type tap and ensuing observation; no configuration is confirmed.
"""
from __future__ import annotations

from contextlib import contextmanager
import copy
import re

import editor_journey as runner
import favourite_info_journey as favourite
import observed_journey as observed
import trigger_category_journey as category

TWELVE_PLAN_SHA256 = '940be18b226ab29de46ea48a1496238b8a2221a52077466693a34a2113bc24cc'
EDITOR = favourite.EDITOR
CATALOG = runner.PACKAGE + '/' + runner.PACKAGE + '.selectableitemlist.AddTriggerActivity'
TITLE = favourite.TITLE
OK = favourite.OK
DATE_TIME = {'resource-id': runner.PACKAGE + ':id/category_name', 'text': 'Date/Time'}
CATALOG_TITLE = {'text': 'Add Trigger'}
DAY_TIME = {'resource-id': runner.PACKAGE + ':id/select_item_name', 'text': 'Day/Time'}


def expected_plan():
    prefix = category.expected_plan()
    if runner.fingerprint(prefix) != TWELVE_PLAN_SHA256:
        raise runner.JourneyError('Reviewed twelve-screen prefix changed')
    plan = copy.deepcopy(prefix)
    plan[-1][2] = DAY_TIME
    return plan + [['after-day-time-trigger', runner.PACKAGE, None, DAY_TIME]]


def require_plan():
    if runner.fingerprint(runner.PLAN) != runner.fingerprint(expected_plan()):
        raise runner.JourneyError('Day/Time sequence differs from the reviewed one additional input')


@contextmanager
def configured_plan():
    with category.configured_plan():
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


def day_time_identity(folder, shot, proof):
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
        bounds = re.fullmatch(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', item.get('bounds', ''))
        if bounds is None:
            raise runner.JourneyError('Observed Day/Time row bounds are invalid')
        left, top, right, bottom = map(int, bounds.groups())
        if not (containing[0] <= left < right <= containing[2]
                and containing[1] <= top < bottom <= containing[3]):
            raise runner.JourneyError('Observed Day/Time row bounds are inconsistent or off screen')
        containing = (left, top, right, bottom)
    return runner.target(data, runner.PACKAGE, DAY_TIME, width, height)


def terminal_surface(folder, shot, proof):
    require_plan()
    if shot.get('name') != 'after-day-time-trigger' or shot['owner'] != runner.PACKAGE:
        raise runner.JourneyError('Unexpected terminal Day/Time trigger observation')
    first = observed.component(proof.artifact(folder, shot['artifacts']['foreground']), proof)
    last = observed.component(proof.artifact(folder, shot['artifacts']['foreground_final']), proof)
    if first != last or last.split('/', 1)[0] != runner.PACKAGE:
        raise runner.JourneyError('Terminal app component is not stable')
    return {'name': shot['name'], 'owner': runner.PACKAGE, 'component': last,
            'surface_after_one_observed_day_time_tap': True, 'subsequent_inputs': 0,
            'trigger_type_tapped': True, 'trigger_configuration_confirmed': False}


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
        day_time_identity(folder, shot, proof)
    elif name == 'after-day-time-trigger':
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
    elif name == 'after-day-time-trigger':
        if previous.get('name') != 'after-trigger-date-category' or action != DAY_TIME:
            raise runner.JourneyError('Day/Time tap is outside its observed expanded-category boundary')
        day_time_identity(folder, before, proof)


def main():
    with configured_plan():
        return runner.main()


if __name__ == '__main__':
    raise SystemExit(main())
