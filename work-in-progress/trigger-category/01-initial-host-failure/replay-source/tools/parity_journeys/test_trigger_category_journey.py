"""Raw observed geometry and adversarial synthetic controls; no Android run."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import editor_journey as runner
import favourite_info_journey as favourite
import observed_journey as observed
import supplied_reference_journey as reference
import trigger_category_journey as category
import test_editor_journey as legacy
from test_observed_journey import ObservedFixture, VirtualRecorder, proof, reviewed_historical_plan

FIXTURES = Path(__file__).with_name('fixtures') / 'trigger-category'


def synthetic_xml(index):
    """Small, authored states for process guards, separate from raw captures."""
    root = ET.Element('hierarchy')
    attrs = {'package': runner.PACKAGE, 'enabled': 'true', 'clickable': 'true',
             'bounds': '[0,0][4,4]', 'class': 'android.widget.Button'}
    if index == 8:
        for selector, kind in [(favourite.TITLE, 'android.widget.TextView'),
                               ({'resource-id': 'android:id/message', 'text': favourite.MESSAGE}, 'android.widget.TextView'),
                               (favourite.OK, 'android.widget.Button')]:
            ET.SubElement(root, 'node', {**attrs, **selector, 'class': kind})
    elif index in (7, 9):
        ET.SubElement(root, 'node', {**attrs, **runner.TRIGGER, 'class': 'android.widget.ImageButton',
                                   'content-desc': 'Add Trigger'})
    elif index == 10:
        ET.SubElement(root, 'node', {**attrs, **category.CATALOG_TITLE, 'class': 'android.widget.TextView'})
        parent = ET.SubElement(root, 'node', {**attrs, 'class': 'android.widget.LinearLayout',
                                            'resource-id': runner.PACKAGE + ':id/category_container'})
        ET.SubElement(parent, 'node', {**attrs, **category.DATE_TIME,
                                      'class': 'android.widget.TextView', 'clickable': 'false'})
    else:
        ET.SubElement(root, 'node', {**attrs, 'text': 'Synthetic terminal observation'})
    return ET.tostring(root)


class TwelveFixture(ObservedFixture):
    def __init__(self):
        self.legacy = legacy.JourneyTests()
        with patch.object(runner, 'PLAN', reviewed_historical_plan()):
            self.legacy.setUp()
        self.folder = self.legacy.root
        self.base = copy.deepcopy(self.legacy.report)
        self.sequence = 0
        self.build()

    def front(self, index):
        if index >= 10:
            return category.CATALOG
        if index >= 7:
            return category.EDITOR
        return super().front(index)

    def xml(self, index):
        return synthetic_xml(index) if index >= 7 else super().xml(index)


class CategoryGeometryControls(unittest.TestCase):
    def setUp(self):
        self.context = category.configured_plan()
        self.context.__enter__()
        self.addCleanup(self.context.__exit__, None, None, None)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.number = 0

    def put(self, data):
        self.number += 1
        name = 'fixture-' + str(self.number)
        (self.folder / name).write_bytes(data)
        return {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

    def frame(self, stem='original-trigger-catalog-acquisition-1'):
        return {'xml': (FIXTURES / (stem + '.xml')).read_bytes(),
                'png': (FIXTURES / (stem + '.png')).read_bytes(),
                'foreground': (FIXTURES / (stem + '-foreground.txt')).read_bytes()}

    def shot(self, frame, name='trigger-catalog'):
        return {'name': name, 'owner': runner.PACKAGE, 'artifacts': {
            'hierarchy': self.put(frame['xml']), 'screenshot': self.put(frame['png']),
            'foreground': self.put(frame['foreground']),
            'foreground_final': self.put(frame.get('foreground_final', frame['foreground']))}}

    def test_both_raw_trigger_captures_have_exact_observed_date_time_center(self):
        for label, png_hash in [('original', 'c1e40ac122d1a0393d685c6f3018c9569b5cd731f803760d96ee75abc9a05048'),
                                ('candidate', '8e77f9a5c01e2eacb1d96205cf6ffca8a372ab3ab6fc4af2e815add992aec051')]:
            with self.subTest(label=label):
                frame = self.frame(label + '-trigger-catalog-acquisition-1')
                self.assertEqual(hashlib.sha256(frame['xml']).hexdigest(), '3245d595f8bb661282aa228c7012169daa768fe3d874eb8f949bc5e022680bbc')
                self.assertEqual(hashlib.sha256(frame['png']).hexdigest(), png_hash)
                self.assertEqual(category.category_identity(self.folder, self.shot(frame), proof), [360, 1028])

    def test_raw_editor_after_tip_has_exact_trigger_add_center(self):
        frame = self.frame('original-editor-after-favourites-tip-acquisition-1')
        self.assertEqual(hashlib.sha256(frame['xml']).hexdigest(), 'b679312fb987cebf3d8ff1423937e00e02ee283612d74b3027937336d9377275')
        self.assertEqual(category.editor_identity(self.folder, self.shot(frame, 'after-favourite-info'), proof), [652, 228])

    def test_changed_category_parent_role_owner_enabled_and_geometry_are_rejected(self):
        edits = [
            ('leaf', 'class', 'android.widget.Button'), ('leaf', 'enabled', 'false'),
            ('leaf', 'clickable', 'true'), ('leaf', 'text', 'Date & Time'),
            ('leaf', 'package', 'other.package'), ('parent', 'class', 'android.widget.FrameLayout'),
            ('parent', 'resource-id', runner.PACKAGE + ':id/other_container'),
            ('parent', 'enabled', 'false'), ('parent', 'clickable', 'false'),
            ('parent', 'package', 'other.package'), ('parent', 'bounds', '[8,1279][712,1377]'),
        ]
        for target, key, value in edits:
            with self.subTest(target=target, field=key, value=value):
                frame = self.frame()
                root = ET.fromstring(frame['xml'])
                node = next(n for n in root.iter('node') if n.get('text') == 'Date/Time')
                parents = {child: parent for parent in root.iter() for child in parent}
                (node if target == 'leaf' else parents[node]).set(key, value)
                frame['xml'] = ET.tostring(root)
                with self.assertRaises(runner.JourneyError):
                    category.category_identity(self.folder, self.shot(frame), proof)

    def test_duplicate_category_and_interposed_parent_are_rejected(self):
        for edit in ('duplicate', 'interpose'):
            with self.subTest(edit=edit):
                frame = self.frame()
                root = ET.fromstring(frame['xml'])
                node = next(n for n in root.iter('node') if n.get('text') == 'Date/Time')
                parents = {child: parent for parent in root.iter() for child in parent}
                parent = parents[node]
                if edit == 'duplicate':
                    root.append(copy.deepcopy(parent))
                else:
                    parent.remove(node)
                    middle = ET.SubElement(parent, 'node', {'package': runner.PACKAGE,
                        'class': 'android.widget.FrameLayout', 'enabled': 'true',
                        'clickable': 'false', 'bounds': parent.get('bounds')})
                    middle.append(node)
                frame['xml'] = ET.tostring(root)
                with self.assertRaises(runner.JourneyError):
                    category.category_identity(self.folder, self.shot(frame), proof)

    def test_wrong_or_changed_catalog_component_is_rejected(self):
        for key in ('foreground', 'foreground_final'):
            frame = self.frame()
            frame[key] = ('topResumedActivity=' + category.EDITOR + '\n').encode()
            with self.subTest(sample=key), self.assertRaises(runner.JourneyError):
                category.category_identity(self.folder, self.shot(frame), proof)

    def test_exact_twelve_plan_and_external_sixteen_bytes_are_preserved(self):
        ten = favourite.expected_plan()
        self.assertEqual(runner.fingerprint(ten), category.TEN_PLAN_SHA256)
        self.assertEqual(len(runner.PLAN), 12)
        self.assertEqual(runner.PLAN[:9], ten[:9])
        self.assertEqual(runner.PLAN[9], ['after-favourite-info', runner.PACKAGE, runner.TRIGGER, favourite.OK])
        self.assertEqual(runner.PLAN[-1], ['after-trigger-date-category', runner.PACKAGE, None, category.DATE_TIME])
        self.assertEqual(sum(step[3] == favourite.OK for step in runner.PLAN), 1)
        self.assertEqual(sum(step[3] == category.DATE_TIME for step in runner.PLAN), 1)
        self.assertEqual(len(json.loads(reference.PLAN_PATH.read_text())), 16)
        self.assertEqual(hashlib.sha256(reference.PLAN_PATH.read_bytes()).hexdigest(), '28ea38698dcfcf0146955be9ddd07d1df0fe01a234c13633dac85628edbbc448')
        observed.require_plan()
        with favourite.configured_plan():
            self.assertEqual(len(runner.PLAN), 10)
            observed.require_plan()

    def test_modified_or_implicit_external_plans_are_rejected(self):
        altered = copy.deepcopy(runner.PLAN)
        altered[-1][3] = {'text': 'Battery/Power'}
        for value in (altered, json.loads(reference.PLAN_PATH.read_text()), runner.PLAN + [runner.PLAN[-1]]):
            with self.subTest(length=len(value)), patch.object(runner, 'PLAN', value), self.assertRaises(runner.JourneyError):
                observed.require_plan()

    def test_terminal_requires_exact_name_stable_app_component_and_no_assumed_selector(self):
        frame = {'xml': synthetic_xml(11), 'png': legacy.png(1),
                 'foreground': ('topResumedActivity=' + category.CATALOG + '\n').encode()}
        shot = self.shot(frame, 'after-trigger-date-category')
        result = category.required_surface(self.folder, shot, None, proof)
        self.assertEqual(result['subsequent_inputs'], 0)
        self.assertEqual(result['component'], category.CATALOG)
        with self.assertRaises(runner.JourneyError):
            category.required_surface(self.folder, shot, {'text': 'Day/Time'}, proof)
        for edit in ('name', 'foreign', 'unstable'):
            invalid = copy.deepcopy(shot)
            if edit == 'name':
                invalid['name'] = 'some-other-observation'
            elif edit == 'foreign':
                invalid['owner'] = 'other.package'
            else:
                invalid['artifacts']['foreground_final'] = self.put(('topResumedActivity=' + category.EDITOR + '\n').encode())
            with self.subTest(edit=edit), self.assertRaises(runner.JourneyError):
                category.terminal_surface(self.folder, invalid, proof)

    def input(self, name='after-trigger-date-category', edit=None):
        index = 10 if name == 'after-trigger-date-category' else 9
        component = category.CATALOG if index == 10 else category.EDITOR
        previous_name = 'trigger-catalog' if index == 10 else 'after-favourite-info'
        action = category.DATE_TIME if index == 10 else runner.TRIGGER
        clock = {'now': 0.0}
        frames = [{'xml': synthetic_xml(index), 'png': legacy.png(1),
                   'foreground': ('topResumedActivity=' + component + '\n').encode()} for _ in range(4)]
        if edit:
            for frame in frames[2:]:
                edit(frame)
        recorder = VirtualRecorder(self.folder, clock, frames)
        self.recorder = recorder
        def sleep(seconds):
            clock['now'] += seconds
        with patch.object(runner.time, 'monotonic', side_effect=lambda: clock['now']), \
                patch.object(runner.time, 'sleep', side_effect=sleep):
            previous = observed.capture(recorder, 'candidate-' + previous_name, runner.PACKAGE)
            previous['name'] = previous_name
            return runner.capture_transition(recorder, previous, 'candidate-' + name, name, action, proof)

    def test_real_recorder_taps_each_new_observed_target_once(self):
        for name in ('trigger-catalog', 'after-trigger-date-category'):
            with self.subTest(name=name):
                transition = self.input(name)
                self.assertEqual(self.recorder.inputs, [['input', 'tap', '2', '2']])
                self.assertLess(transition['precondition_age_seconds'], 15)

    def test_real_recorder_late_pid_and_component_changes_block_both_new_inputs(self):
        for name in ('trigger-catalog', 'after-trigger-date-category'):
            for edit in (lambda frame: frame.update(late_pid=b'32'),
                         lambda frame: frame.update(late_foreground=('topResumedActivity=' + observed.HOME + '\n').encode())):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    self.input(name, edit)
                self.assertEqual(self.recorder.inputs, [])


class TwelveContinuationControls(unittest.TestCase):
    def setUp(self):
        self.context = category.configured_plan()
        self.context.__enter__()
        self.addCleanup(self.context.__exit__, None, None, None)
        self.fixture = TwelveFixture()
        self.addCleanup(self.fixture.close)

    def test_full_twelve_screen_synthetic_run_has_only_the_declared_scope(self):
        result = self.fixture.result()
        self.assertTrue(result['journey_equal'], result)
        self.assertEqual(len(result['screens']), 12)
        self.assertEqual(result['status'], 'EXACT_TRIGGER_CATEGORY_OBSERVATION_ONLY')
        self.assertTrue(result['terminal_surface_identities_equal'])
        self.assertTrue(result['catalog_navigation_established'])
        self.assertFalse(result['trigger_selected'])
        self.assertFalse(result['full_runtime_1_to_1_established'])

    def test_terminal_full_frame_difference_is_retained(self):
        shot = self.fixture.candidate()['screens'][-1]
        self.fixture.edit_stable(shot, lambda value: self.fixture.raw_value(value, 'screenshot', legacy.png(199)))
        result = self.fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertEqual(result['status'], 'JOURNEY_DIFFERENCE')
        self.assertEqual(result['screens'][-1]['changed_pixels'], 16)

    def test_wrong_new_tap_is_rejected_even_with_matching_terminal_screens(self):
        transition = self.fixture.candidate()['transitions'][-1]
        transition['command']['argv'] = ['shell', 'input tap 1 1']
        result = self.fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertIn('Input command differs', result['reason'])

    def test_wrong_fresh_installed_apk_before_ok_still_rejects_entire_twelve_screen_run(self):
        transition = self.fixture.candidate()['transitions'][8]
        self.fixture.replace_output(transition['pre_ok_installed_identity']['installed_checksum'],
                                    ('9' * 64 + '  /data/app/test/base.apk\n').encode())
        result = self.fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertIn('Installed APK identity changed before OK', result['reason'])

    def test_stale_freshness_bound_is_not_relaxed_for_category_input(self):
        self.fixture.candidate()['transitions'][-1]['precondition_age_seconds'] = 15.01
        result = self.fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertIn('Expired input precondition', result['reason'])


if __name__ == '__main__':
    unittest.main()
