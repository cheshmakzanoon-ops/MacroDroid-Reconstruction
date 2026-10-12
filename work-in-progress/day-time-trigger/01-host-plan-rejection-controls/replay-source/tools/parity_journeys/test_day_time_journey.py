"""Exact raw Day/Time geometry and adversarial thirteen-screen controls; no Android execution."""
from __future__ import annotations

import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import day_time_journey as day
import editor_journey as runner
import observed_journey as observed
import trigger_category_journey as category
import test_editor_journey as legacy
from test_observed_journey import VirtualRecorder, proof
from test_trigger_category_journey import TwelveFixture, synthetic_xml as category_xml

FIXTURES = Path(__file__).with_name('fixtures') / 'day-time-trigger'


def synthetic_xml(index):
    if index != 11:
        return category_xml(index)
    root = ET.Element('hierarchy')
    attrs = {'package': runner.PACKAGE, 'enabled': 'true', 'clickable': 'false', 'bounds': '[0,0][4,4]'}
    for selector in (day.CATALOG_TITLE, day.DATE_TIME):
        ET.SubElement(root, 'node', {**attrs, **selector, 'class': 'android.widget.TextView'})
    row = ET.SubElement(root, 'node', {**attrs, 'class': 'android.widget.LinearLayout',
        'resource-id': runner.PACKAGE + ':id/select_item_row_frame', 'clickable': 'true'})
    frame = ET.SubElement(row, 'node', {**attrs, 'class': 'android.widget.FrameLayout',
        'resource-id': runner.PACKAGE + ':id/select_item_container'})
    label = ET.SubElement(frame, 'node', {**attrs, 'class': 'android.widget.LinearLayout', 'resource-id': ''})
    ET.SubElement(label, 'node', {**attrs, **day.DAY_TIME, 'class': 'android.widget.TextView'})
    return ET.tostring(root)


class ThirteenFixture(TwelveFixture):
    def xml(self, index):
        return synthetic_xml(index) if index >= 7 else super().xml(index)


class DayTimeGeometryControls(unittest.TestCase):
    def setUp(self):
        self.context = day.configured_plan()
        self.context.__enter__()
        self.addCleanup(self.context.__exit__, None, None, None)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name); self.number = 0

    def put(self, data):
        self.number += 1; name = 'fixture-' + str(self.number)
        (self.folder / name).write_bytes(data)
        return {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

    def frame(self, label='original'):
        return {'xml': (FIXTURES / (label + '-date-time.xml')).read_bytes(),
                'png': (FIXTURES / (label + '-date-time.png')).read_bytes(),
                'foreground': (FIXTURES / (label + '-date-time-foreground.txt')).read_bytes(),
                'foreground_final': (FIXTURES / (label + '-date-time-foreground-final.txt')).read_bytes()}

    def shot(self, frame, name='after-trigger-date-category'):
        return {'name': name, 'owner': runner.PACKAGE, 'artifacts': {
            'hierarchy': self.put(frame['xml']), 'screenshot': self.put(frame['png']),
            'foreground': self.put(frame['foreground']),
            'foreground_final': self.put(frame.get('foreground_final', frame['foreground']))}}

    def test_both_unmodified_raw_surfaces_resolve_the_exact_observed_day_time_center(self):
        for label in ('original', 'candidate'):
            with self.subTest(label=label):
                frame = self.frame(label)
                self.assertEqual(hashlib.sha256(frame['png']).hexdigest(), '7057b96a46d56c0e53a3b42a3475a24812b5867a753bcf81b528e9a8a6aefa92')
                self.assertEqual(hashlib.sha256(frame['xml']).hexdigest(), '9bb3a60891fc9194b2f9ae493e513a041a6ee2e395125c13dbeb8cef648abcd0')
                self.assertEqual(day.day_time_identity(self.folder, self.shot(frame), proof), [184, 626])

    def test_all_four_ancestor_roles_reject_changed_owner_class_enabled_and_geometry(self):
        edits = [('package', 'other.package'), ('class', 'android.widget.Button'), ('enabled', 'false'),
                 ('bounds', '[0,1279][720,1377]'), ('bounds', 'malformed')]
        for depth in range(4):
            for key, value in edits:
                with self.subTest(depth=depth, field=key):
                    frame = self.frame(); root = ET.fromstring(frame['xml'])
                    node = next(item for item in root.iter('node') if item.get('text') == 'Day/Time')
                    parents = {child: parent for parent in root.iter() for child in parent}
                    for _ in range(depth): node = parents[node]
                    node.set(key, value); frame['xml'] = ET.tostring(root)
                    with self.assertRaises(runner.JourneyError): day.day_time_identity(self.folder, self.shot(frame), proof)

    def test_clickability_resource_identity_text_and_nested_bounds_are_not_relaxed(self):
        changes = [(0, 'clickable', 'true'), (1, 'clickable', 'true'), (2, 'clickable', 'true'),
                   (3, 'clickable', 'false'), (0, 'resource-id', runner.PACKAGE + ':id/wrong_name'),
                   (1, 'resource-id', runner.PACKAGE + ':id/extra_parent'),
                   (2, 'resource-id', runner.PACKAGE + ':id/wrong_container'),
                   (3, 'resource-id', runner.PACKAGE + ':id/wrong_row'),
                   (0, 'text', 'Regular Interval'), (0, 'bounds', '[0,0][100,30]')]
        for depth, key, value in changes:
            with self.subTest(depth=depth, field=key):
                frame = self.frame(); root = ET.fromstring(frame['xml'])
                node = next(item for item in root.iter('node') if item.get('text') == 'Day/Time')
                parents = {child: parent for parent in root.iter() for child in parent}
                for _ in range(depth): node = parents[node]
                node.set(key, value); frame['xml'] = ET.tostring(root)
                with self.assertRaises(runner.JourneyError): day.day_time_identity(self.folder, self.shot(frame), proof)

    def test_duplicate_tile_and_interposed_parent_are_rejected(self):
        for change in ('duplicate', 'interposed'):
            frame = self.frame(); root = ET.fromstring(frame['xml'])
            node = next(item for item in root.iter('node') if item.get('text') == 'Day/Time')
            parents = {child: parent for parent in root.iter() for child in parent}; parent = parents[node]
            if change == 'duplicate': root.append(copy.deepcopy(parent))
            else:
                parent.remove(node)
                middle = ET.SubElement(parent, 'node', {'package': runner.PACKAGE, 'class': 'android.widget.LinearLayout',
                    'resource-id': '', 'enabled': 'true', 'clickable': 'false', 'bounds': parent.get('bounds')})
                middle.append(node)
            frame['xml'] = ET.tostring(root)
            with self.subTest(change=change), self.assertRaises(runner.JourneyError):
                day.day_time_identity(self.folder, self.shot(frame), proof)

    def test_both_catalog_component_samples_must_match_the_observed_activity(self):
        for role in ('foreground', 'foreground_final'):
            frame = self.frame(); frame[role] = ('topResumedActivity=' + day.EDITOR + '\n').encode()
            with self.subTest(role=role), self.assertRaises(runner.JourneyError):
                day.day_time_identity(self.folder, self.shot(frame), proof)

    def test_exact_thirteen_plan_preserves_prior_prefix_and_one_new_input(self):
        twelve = category.expected_plan()
        self.assertEqual(runner.fingerprint(twelve), day.TWELVE_PLAN_SHA256)
        self.assertEqual(len(runner.PLAN), 13)
        self.assertEqual(runner.PLAN[:11], twelve[:11])
        self.assertEqual(runner.PLAN[11], ['after-trigger-date-category', runner.PACKAGE, day.DAY_TIME, day.DATE_TIME])
        self.assertEqual(runner.PLAN[12], ['after-day-time-trigger', runner.PACKAGE, None, day.DAY_TIME])
        self.assertEqual(sum(step[3] == day.DAY_TIME for step in runner.PLAN), 1)
        self.assertEqual(sum(step[3] == day.OK for step in runner.PLAN), 1)
        observed.require_plan()
        with category.configured_plan():
            self.assertEqual(len(runner.PLAN), 12); observed.require_plan()
        self.assertEqual(len(runner.PLAN), 13); observed.require_plan()

    def test_changed_plan_action_order_and_assumed_terminal_selector_are_rejected(self):
        variants = []
        for key, value in ((3, day.DATE_TIME), (2, {'text': 'Day/Time'}), (0, 'another-surface')):
            variant = copy.deepcopy(runner.PLAN); variant[-1][key] = value; variants.append(variant)
        variants += [runner.PLAN + [runner.PLAN[-1]], runner.PLAN[:-1]]
        for variant in variants:
            with self.subTest(plan=variant[-1]), patch.object(runner, 'PLAN', variant), self.assertRaises(runner.JourneyError):
                observed.require_plan()

    def test_terminal_is_a_stable_unassumed_app_surface_with_no_configuration_confirmation(self):
        frame = {'xml': synthetic_xml(12), 'png': legacy.png(1),
                 'foreground': ('topResumedActivity=' + day.CATALOG + '\n').encode()}
        shot = self.shot(frame, 'after-day-time-trigger')
        terminal = day.required_surface(self.folder, shot, None, proof)
        self.assertTrue(terminal['trigger_type_tapped']); self.assertFalse(terminal['trigger_configuration_confirmed'])
        self.assertEqual(terminal['subsequent_inputs'], 0)
        with self.assertRaises(runner.JourneyError): day.required_surface(self.folder, shot, {'text': 'OK'}, proof)
        for edit in ('name', 'owner', 'component'):
            wrong = copy.deepcopy(shot)
            if edit == 'name': wrong['name'] = 'after-trigger-date-category'
            elif edit == 'owner': wrong['owner'] = 'other.package'
            else: wrong['artifacts']['foreground_final'] = self.put(('topResumedActivity=' + day.EDITOR + '\n').encode())
            with self.subTest(edit=edit), self.assertRaises(runner.JourneyError): day.terminal_surface(self.folder, wrong, proof)

    def input(self, edit=None):
        clock = {'now': 0.0}
        frames = [{'xml': synthetic_xml(11), 'png': legacy.png(1),
                   'foreground': ('topResumedActivity=' + day.CATALOG + '\n').encode()} for _ in range(4)]
        if edit:
            for frame in frames[2:]: edit(frame)
        self.recorder = VirtualRecorder(self.folder, clock, frames)
        def sleep(seconds): clock['now'] += seconds
        with patch.object(runner.time, 'monotonic', side_effect=lambda: clock['now']), patch.object(runner.time, 'sleep', side_effect=sleep):
            previous = observed.capture(self.recorder, 'candidate-after-trigger-date-category', runner.PACKAGE)
            previous['name'] = 'after-trigger-date-category'
            return runner.capture_transition(self.recorder, previous, 'candidate-after-day-time-trigger',
                                             'after-day-time-trigger', day.DAY_TIME, proof)

    def test_real_recorder_uses_one_fresh_observed_day_time_tap(self):
        transition = self.input()
        self.assertEqual(self.recorder.inputs, [['input', 'tap', '2', '2']])
        self.assertLess(transition['precondition_age_seconds'], 15)

    def test_late_process_and_component_changes_block_the_new_input(self):
        for edit in (lambda frame: frame.update(late_pid=b'32'),
                     lambda frame: frame.update(late_foreground=('topResumedActivity=' + day.EDITOR + '\n').encode())):
            with self.assertRaises(ValueError): self.input(edit)
            self.assertEqual(self.recorder.inputs, [])


class ThirteenContinuationControls(unittest.TestCase):
    def setUp(self):
        context = day.configured_plan(); context.__enter__(); self.addCleanup(context.__exit__, None, None, None)
        self.fixture = ThirteenFixture(); self.addCleanup(self.fixture.close)

    def test_complete_synthetic_thirteen_pair_has_only_the_declared_scope(self):
        result = self.fixture.result()
        self.assertTrue(result['journey_equal'], result)
        self.assertEqual(len(result['screens']), 13)
        self.assertEqual(result['status'], 'EXACT_DAY_TIME_TRIGGER_OBSERVATION_ONLY')
        self.assertTrue(result['terminal_surface_identities_equal'])
        self.assertTrue(result['catalog_navigation_established']); self.assertTrue(result['trigger_type_tapped'])
        self.assertFalse(result['trigger_configuration_confirmed']); self.assertFalse(result['macros_saved'])
        self.assertFalse(result['macros_executed']); self.assertFalse(result['full_runtime_1_to_1_established'])

    def test_full_terminal_pixel_difference_is_retained(self):
        shot = self.fixture.candidate()['screens'][-1]
        self.fixture.edit_stable(shot, lambda value: self.fixture.raw_value(value, 'screenshot', legacy.png(199)))
        result = self.fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertEqual(result['status'], 'JOURNEY_DIFFERENCE')
        self.assertEqual(result['screens'][-1]['changed_pixels'], 16)

    def test_a_different_stable_terminal_component_cannot_pass_equal_images(self):
        shot = self.fixture.candidate()['screens'][-1]
        changed = ('topResumedActivity=' + day.EDITOR + '\n').encode()
        def change(value):
            for role in ('foreground', 'foreground_final'): self.fixture.raw_value(value, role, changed)
        self.fixture.edit_stable(shot, change)
        result = self.fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertFalse(result.get('terminal_surface_identities_equal', True), result)

    def test_wrong_tap_and_stale_precondition_remain_rejected(self):
        transition = self.fixture.candidate()['transitions'][-1]
        original = copy.deepcopy(transition)
        transition['command']['argv'] = ['shell', 'input tap 1 1']
        result = self.fixture.result(); self.assertFalse(result['journey_equal'], result)
        self.assertIn('Input command differs', result['reason'])
        transition.clear(); transition.update(original); transition['precondition_age_seconds'] = 15.01
        result = self.fixture.result(); self.assertFalse(result['journey_equal'], result)
        self.assertIn('Expired input precondition', result['reason'])


if __name__ == '__main__': unittest.main()
