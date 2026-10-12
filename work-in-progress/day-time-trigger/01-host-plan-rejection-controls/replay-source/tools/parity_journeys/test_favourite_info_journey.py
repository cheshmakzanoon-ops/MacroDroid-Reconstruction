"""Actual XML/log fixtures and synthetic controls; no device execution."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import editor_journey as runner
import favourite_info_journey as favourite
import observed_journey as observed
import supplied_reference_journey as reference
from test_observed_journey import ObservedFixture, VirtualRecorder, proof, reviewed_historical_plan

FIXTURES = Path(__file__).with_name('fixtures')


class DialogControls(unittest.TestCase):
    def setUp(self):
        self.context = favourite.configured_plan()
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

    def frame(self):
        return {'xml': (FIXTURES / 'favourite-triggers-api35.xml').read_bytes(),
                'png': (FIXTURES / 'favourite-triggers-api35.png').read_bytes(),
                'foreground': ('topResumedActivity=' + favourite.EDITOR + '\n').encode()}

    def shot(self, frame):
        return {'owner': runner.PACKAGE, 'artifacts': {
            'hierarchy': self.put(frame['xml']), 'screenshot': self.put(frame['png']),
            'foreground': self.put(frame['foreground']), 'foreground_final': self.put(frame['foreground'])}}

    def test_exact_observed_fixture_has_one_ok_target_at_recorded_center(self):
        frame = self.frame()
        self.assertEqual(hashlib.sha256(frame['xml']).hexdigest(), 'af7f2d14b631c0762a065a831f8247d9ca194f7fd755d0d30f2e2ba63d5b85b2')
        self.assertEqual(favourite.dialog_identity(self.folder, self.shot(frame), proof), [560, 828])

    def test_changed_message_title_role_owner_and_duplicate_button_fail(self):
        edits = [
            ('android:id/message', 'text', 'Different information'),
            (runner.PACKAGE + ':id/alertTitle', 'text', 'Favourite Actions'),
            ('android:id/button1', 'enabled', 'false'),
            ('android:id/button1', 'clickable', 'false'),
            ('android:id/button1', 'class', 'android.widget.TextView'),
            ('android:id/button1', 'text', 'DOWNLOAD'),
            ('android:id/button1', 'package', 'other.package'),
        ]
        for target, key, value in edits:
            with self.subTest(target=target, field=key):
                frame = self.frame()
                tree = ET.fromstring(frame['xml'])
                next(n for n in tree.iter('node') if n.get('resource-id') == target).set(key, value)
                frame['xml'] = ET.tostring(tree)
                with self.assertRaises(runner.JourneyError):
                    favourite.dialog_identity(self.folder, self.shot(frame), proof)
        frame = self.frame()
        tree = ET.fromstring(frame['xml'])
        node = copy.deepcopy(next(n for n in tree.iter('node') if n.get('resource-id') == 'android:id/button1'))
        node.set('text', 'Other button')
        tree.append(node)
        frame['xml'] = ET.tostring(tree)
        with self.assertRaisesRegex(runner.JourneyError, 'ambiguous'):
            favourite.dialog_identity(self.folder, self.shot(frame), proof)

    def input(self, edit=None, digest='2' * 64):
        clock = {'now': 0.0}
        frames = [self.frame() for _ in range(4)]
        # Geometry on the complete unchanged 720x1280 fixture is tested above.
        # Virtual process/input controls use tiny synthetic frames so repeated
        # PNG decoding does not dominate the suite; no actual capture is edited.
        from test_editor_journey import png
        for frame in frames:
            tree = ET.fromstring(frame['xml'])
            for node in tree.iter('node'):
                node.set('bounds', '[0,0][4,4]')
            frame['xml'] = ET.tostring(tree)
            frame['png'] = png(1)
        if edit:
            for frame in frames[2:]:
                edit(frame)
        recorder = VirtualRecorder(self.folder, clock, frames)
        self.recorder = recorder
        def sleep(seconds):
            clock['now'] += seconds
        with patch.object(runner.time, 'monotonic', side_effect=lambda: clock['now']), \
                patch.object(runner.time, 'sleep', side_effect=sleep):
            installed = recorder.shell(['pm', 'path', runner.PACKAGE])[0]
            run = {'label': 'candidate', 'apk_sha256': '2' * 64, 'installed_path': installed}
            previous = observed.capture(recorder, 'candidate-favourite-triggers-info', runner.PACKAGE)
            previous['name'] = 'favourite-triggers-info'
            recorder.device_apk_sha256 = digest
            return runner.capture_transition(recorder, previous, 'candidate-after-favourite-info',
                                             'after-favourite-info', favourite.OK, proof, run)

    def test_real_recorder_path_taps_only_the_fresh_observed_ok_once(self):
        transition = self.input()
        self.assertEqual(self.recorder.inputs, [['input', 'tap', '2', '2']])
        self.assertIn('pre_ok_installed_identity', transition)
        self.assertLess(transition['precondition_age_seconds'], 15)

    def test_real_recorder_late_pid_or_component_change_prevents_input(self):
        edits = [(lambda frame: frame.update(late_pid=b'32'), 'App PID changed'),
                 (lambda frame: frame.update(late_foreground=('topResumedActivity=' + observed.HOME + '\n').encode()),
                  'Expected component left')]
        for edit, reason in edits:
            with self.subTest(reason=reason), self.assertRaisesRegex(ValueError, reason):
                self.input(edit)
            self.assertEqual(self.recorder.inputs, [])

    def test_real_recorder_wrong_device_apk_prevents_ok(self):
        with self.assertRaisesRegex(runner.JourneyError, 'identity changed'):
            self.input(digest='9' * 64)
        self.assertEqual(self.recorder.inputs, [])

    def test_new_plan_stops_after_one_ok_and_preserves_reference_bytes(self):
        plan = runner.PLAN
        old = json.loads(reference.PLAN_PATH.read_text())
        self.assertEqual(len(old), 16)
        self.assertEqual(len(plan), 10)
        self.assertEqual(plan[:8], old[:8])
        self.assertEqual(plan[:8], reviewed_historical_plan()[:8])
        self.assertEqual(plan[-1], ['after-favourite-info', runner.PACKAGE, None, favourite.OK])
        self.assertEqual(sum(step[3] == favourite.OK for step in plan), 1)
        self.assertEqual(hashlib.sha256(reference.PLAN_PATH.read_bytes()).hexdigest(), '28ea38698dcfcf0146955be9ddd07d1df0fe01a234c13633dac85628edbbc448')
        with patch.object(runner, 'PLAN', plan + [old[-1]]), self.assertRaises(runner.JourneyError):
            favourite.require_plan()

    def test_historical_fixture_drift_is_rejected(self):
        with patch.object(Path, 'read_bytes', return_value=b'[]'), self.assertRaisesRegex(runner.JourneyError, 'historical'):
            reviewed_historical_plan()

    def test_new_external_plan_drift_is_not_silently_adopted(self):
        plan = json.loads(reference.PLAN_PATH.read_text())
        plan[-1][0] = 'unreviewed-external-step'
        with patch.object(Path, 'read_text', return_value=json.dumps(plan)), \
                self.assertRaisesRegex(runner.JourneyError, 'reference plan changed'):
            favourite.expected_plan()

    def test_observation_policy_does_not_implicitly_enable_external_sixteen_steps(self):
        plan = json.loads(reference.PLAN_PATH.read_text())
        with patch.object(runner, 'PLAN', plan), self.assertRaises(runner.JourneyError):
            observed.require_plan()


class ContinuationControls(unittest.TestCase):
    def setUp(self):
        self.context = favourite.configured_plan()
        self.context.__enter__()
        self.addCleanup(self.context.__exit__, None, None, None)
        self.fixture = ObservedFixture()
        self.addCleanup(self.fixture.close)

    def inject_crash(self, run, mutate=None):
        transition = run['transitions'][4]
        artifact = transition['process_handoff']
        value = json.loads(proof.artifact(self.fixture.folder, artifact))
        data = (FIXTURES / 'fragment-fatal-api35-original.txt').read_text()
        data = re.sub(r'\b3947\b', value['old_pid'], data).encode()
        if mutate:
            data = mutate(data)
        self.fixture.replace_output(value['after_diagnostics']['crash'], data)
        crash = observed.crash_observation(self.fixture.folder, transition['pre_denial_diagnostics'],
                                            value['after_diagnostics'], value['old_pid'], proof)
        value.update(crash_observation=crash, outcome=observed.outcome(value['old_pid'], value['new_pid'], crash))
        transition['process_handoff'] = self.fixture.put(artifact['path'], json.dumps(value).encode())

    def test_full_ten_screen_synthetic_scope_preserves_terminal_component(self):
        result = self.fixture.result()
        self.assertTrue(result['journey_equal'], result)
        self.assertEqual(len(result['screens']), 10)
        self.assertEqual(result['status'], 'EXACT_OBSERVED_DIALOG_JOURNEY_MATCH_ONLY')
        self.assertTrue(result['terminal_surface_identities_equal'])
        self.assertFalse(result['catalog_navigation_established'])

    def test_shared_known_fatal_is_classified_as_post_crash_continuation(self):
        for run in self.fixture.report['runs']:
            self.inject_crash(run)
        result = self.fixture.result()
        self.assertTrue(result['journey_equal'], result)
        self.assertEqual(result['status'], 'MATCHED_POST_CRASH_CONTINUATION_ONLY')
        self.assertTrue(result['post_crash_continuation_observed_in_both'])
        self.assertFalse(result['crash_free_run_established'])
        self.assertFalse(result['full_runtime_1_to_1_established'])

    def test_known_fatal_in_only_one_run_is_an_outcome_difference(self):
        self.inject_crash(self.fixture.candidate())
        result = self.fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertEqual(result['status'], 'JOURNEY_DIFFERENCE')
        self.assertFalse(result['process_handoff_outcomes_equal'])

    def test_stale_or_wrong_pre_ok_installed_identity_is_rejected(self):
        transition = self.fixture.candidate()['transitions'][-1]
        records = transition['pre_ok_installed_identity']
        records['installed_checksum']['stdout'] = self.fixture.candidate()['installed_checksum']['stdout']
        result = self.fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertIn('reused earlier', result['reason'])

    def test_terminal_pixel_difference_is_retained_after_shared_crash(self):
        for run in self.fixture.report['runs']:
            self.inject_crash(run)
        shot = self.fixture.candidate()['screens'][-1]
        from test_editor_journey import png
        self.fixture.edit_stable(shot, lambda value: self.fixture.raw_value(value, 'screenshot', png(199)))
        result = self.fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertTrue(result['post_crash_continuation_observed_in_both'])
        self.assertEqual(result['screens'][-1]['changed_pixels'], 16)


class CrashFixtureControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.number = 0

    def diagnostics(self, data):
        self.number += 1
        prefix = str(self.number)
        records = {}
        for stream, value in [('stdout', data), ('stderr', b'')]:
            name = prefix + '-' + stream
            (self.folder / name).write_bytes(value)
            records[stream] = {'path': name, 'bytes': len(value), 'sha256': hashlib.sha256(value).hexdigest()}
        return {'crash': {'returncode': 0, **records}}

    def test_exact_two_actual_fatal_blocks_share_type_stack_but_keep_literal_messages(self):
        results = []
        for label, pid in [('original', '3947'), ('candidate', '5811')]:
            data = (FIXTURES / ('fragment-fatal-api35-' + label + '.txt')).read_bytes()
            results.append(observed.crash_observation(self.folder, self.diagnostics(b''), self.diagnostics(data), pid, proof))
        self.assertEqual(results[0]['classification'], results[1]['classification'])
        self.assertNotEqual(results[0]['new_fatal_blocks'][0]['literal_exception'], results[1]['new_fatal_blocks'][0]['literal_exception'])

    def test_old_buffer_entry_is_not_a_new_crash_and_empty_buffer_is_not_crash_free(self):
        data = (FIXTURES / 'fragment-fatal-api35-original.txt').read_bytes()
        result = observed.crash_observation(self.folder, self.diagnostics(data), self.diagnostics(data), '3947', proof)
        self.assertEqual(result['classification'], {'status': 'NO_NEW_JAVA_FATAL_EXCEPTION_OBSERVED'})

    def test_changed_stack_message_missing_process_or_truncation_rejects_classification(self):
        data = (FIXTURES / 'fragment-fatal-api35-original.txt').read_bytes()
        for changed in [data.replace(b'lbua80.onShow', b'Other.onShow'),
                        data.replace(b'not attached to Activity', b'other failure'),
                        data.replace(b'Process: com.arlosoft.macrodroid', b'Process: other.package'),
                        b'\n'.join(data.splitlines()[:-1]) + b'\n']:
            with self.subTest(data=changed[:40]), self.assertRaisesRegex(runner.JourneyError, 'Unreviewed new fatal'):
                observed.crash_observation(self.folder, self.diagnostics(b''), self.diagnostics(changed), '3947', proof)


if __name__ == '__main__':
    unittest.main()
