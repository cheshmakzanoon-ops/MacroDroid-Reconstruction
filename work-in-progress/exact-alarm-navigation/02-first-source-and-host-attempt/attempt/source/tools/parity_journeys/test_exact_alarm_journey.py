"""Observed dialog fixtures and synthetic process/policy controls; no Android run."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zlib

import day_time_journey as day
import editor_journey as runner
import exact_alarm_journey as alarm
import exact_alarm_readiness as ready
import observed_journey as observed
import test_editor_journey as legacy
import test_notification_readiness as prior_ready
from test_day_time_journey import ThirteenFixture
from test_observed_journey import VirtualRecorder, proof, reviewed_historical_plan

FIXTURES = Path(__file__).with_name('fixtures') / 'exact-alarm'
BASE = 'original-after-day-time-trigger-acquisition-1-frame-2'
SUFFIXES = {'pid_first': '-pid-first.txt', 'foreground': '-foreground.txt',
            'hierarchy': '.xml', 'screenshot': '.png',
            'foreground_final': '-foreground-final.txt', 'pid_final': '-pid-final.txt'}


def synthetic_settings_png(value=1):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
    rows = (b'\x00' + bytes([value, 32, 48, 255]) * 720) * 1280
    return (proof.PNG_MAGIC + chunk(b'IHDR', struct.pack('>IIBBBBB', 720, 1280, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b''))


def settings_xml():
    root = ET.Element('hierarchy', {'rotation': '0'})
    ET.SubElement(root, 'node', {'package': alarm.SETTINGS, 'class': 'android.widget.TextView',
        'enabled': 'true', 'clickable': 'false', 'bounds': '[0,0][720,1280]',
        'text': 'Synthetic destination; no actual Settings page has been observed'})
    return ET.tostring(root)


class FourteenFixture(ThirteenFixture):
    """The old authored prefix plus the exact raw dialog and an authored Settings page."""
    def front(self, index):
        return alarm.SETTINGS + '/.SyntheticDestination' if index == 13 else super().front(index)

    def xml(self, index):
        if index == 12:
            return (FIXTURES / (BASE + '.xml')).read_bytes()
        if index == 13:
            return settings_xml()
        return super().xml(index)

    def stable(self, label, index, pid, start):
        if index < 12:
            return super().stable(label, index, pid, start)
        label += '-acquisition-1'
        shots = []
        screenshot = ((FIXTURES / (BASE + '.png')).read_bytes() if index == 12 else synthetic_settings_png())
        for number in range(2):
            stem = label + '-frame-' + str(number + 1)
            timestamp = start + number * 1.2
            contents = {'hierarchy': self.xml(index), 'screenshot': screenshot,
                        'pid_first': pid.encode(), 'pid_final': pid.encode(),
                        'foreground': ('topResumedActivity=' + self.front(index) + '\n').encode(),
                        'foreground_final': ('topResumedActivity=' + self.front(index) + '\n').encode()}
            shots.append({'owner': runner.PLAN[index][1], 'sample_interval_seconds': 1.1,
                          'observation': {'started_monotonic': timestamp, 'finished_monotonic': timestamp + 1.1},
                          'artifacts': {key: self.put(stem + SUFFIXES[key], data) for key, data in contents.items()}})
        event = {'schema': 1, 'status': 'CONSECUTIVE_FULL_FRAMES_IDENTICAL', 'label': label,
                 'owner': runner.PLAN[index][1], 'max_attempts': 6, 'max_seconds': 30,
                 'started_monotonic': start, 'finished_monotonic': start + 2.31, 'seconds': 2.31,
                 'attempts': shots, 'accepted_pair': [0, 1]}
        record = self.put(label + '-settling.json', json.dumps(event).encode())
        self.report['capture_events'].append(record)
        result = copy.deepcopy(shots[-1]); result['settling'] = record
        return result

    def build(self, candidate_replaced=True):
        super().build(candidate_replaced)
        self.report['plan'] = copy.deepcopy(runner.PLAN)
        for run in self.report['runs']:
            run['transitions'][-1]['command']['argv'] = ['shell', 'input tap 560 809']


def add_readiness(fixture):
    harness = prior_ready.ReadinessReportControls()
    harness.fixture, harness.folder, harness.report = fixture, fixture.folder, fixture.report
    with patch.object(prior_ready, 'ready', ready):
        harness.add_phases()
    fixture.report[alarm.POLICY_KEY] = copy.deepcopy(alarm.POLICY)


class ExactAlarmGeometryControls(unittest.TestCase):
    def setUp(self):
        context = alarm.configured_plan(); context.__enter__()
        self.addCleanup(context.__exit__, None, None, None)
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.folder, self.sequence = Path(temp.name), 0

    def put(self, data, name=None):
        self.sequence += 1
        name = name or ('fixture-' + str(self.sequence))
        (self.folder / name).write_bytes(data)
        return {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

    def frame(self, label='original'):
        stem = label + '-after-day-time-trigger-acquisition-1-frame-2'
        return {'xml': (FIXTURES / (stem + '.xml')).read_bytes(),
                'png': (FIXTURES / (stem + '.png')).read_bytes(),
                'foreground': (FIXTURES / (stem + '-foreground.txt')).read_bytes(),
                'foreground_final': (FIXTURES / (stem + '-foreground-final.txt')).read_bytes()}

    def shot(self, frame):
        return {'name': alarm.DIALOG, 'owner': runner.PACKAGE, 'artifacts': {
            'hierarchy': self.put(frame['xml']), 'screenshot': self.put(frame['png']),
            'foreground': self.put(frame['foreground']),
            'foreground_final': self.put(frame.get('foreground_final', frame['foreground']))}}

    def test_both_actual_dialogs_have_the_exact_observed_center_and_panel(self):
        for label in ('original', 'candidate'):
            frame = self.frame(label)
            self.assertEqual(hashlib.sha256(frame['png']).hexdigest(),
                             '3d7c58b3e7c1c8e84964ab504ab69c00b970ee6e493904ec5d03b9b41d26a7c7')
            self.assertEqual(hashlib.sha256(frame['xml']).hexdigest(),
                             'd9e3f0fcb4139e4cfbaa6fe4b856159157136e82775cad4c45746abeef10d076')
            self.assertEqual(alarm.alarm_dialog_identity(self.folder, self.shot(frame), proof), [560, 809])
        self.assertEqual(hashlib.sha256(alarm.CONTRACT_PATH.read_bytes()).hexdigest(), alarm.CONTRACT_SHA256)

    def test_each_of_nine_positive_ancestor_roles_rejects_changed_attributes(self):
        for depth in range(9):
            for key, value in [('package', 'other.app'), ('class', 'android.widget.EditText'),
                               ('bounds', '[0,0][1,1]'), ('enabled', 'false')]:
                frame = self.frame(); root = ET.fromstring(frame['xml'])
                node = next(n for n in root.iter('node') if n.get('resource-id') == 'android:id/button1')
                parents = {child: parent for parent in root.iter() for child in parent}
                for _ in range(depth): node = parents[node]
                node.set(key, value); frame['xml'] = ET.tostring(root)
                with self.subTest(depth=depth, field=key), self.assertRaises(runner.JourneyError):
                    alarm.alarm_dialog_identity(self.folder, self.shot(frame), proof)

    def test_title_message_cancel_and_positive_roles_reject_text_and_duplicate_ids(self):
        for resource in ('android:id/button1', 'android:id/button2', 'android:id/message',
                         runner.PACKAGE + ':id/alertTitle'):
            for mutation in ('text', 'duplicate'):
                frame = self.frame(); root = ET.fromstring(frame['xml'])
                node = next(n for n in root.iter('node') if n.get('resource-id') == resource)
                if mutation == 'text': node.set('text', 'Unobserved text')
                else:
                    duplicate = copy.deepcopy(node); duplicate.set('text', 'Different label, same ID')
                    root.append(duplicate)
                frame['xml'] = ET.tostring(root)
                with self.subTest(resource=resource, mutation=mutation), self.assertRaises(runner.JourneyError):
                    alarm.alarm_dialog_identity(self.folder, self.shot(frame), proof)

    def test_interposed_ancestor_extra_panel_child_foreign_node_and_root_rotation_reject(self):
        for mutation in ('ancestor', 'panel_child', 'foreign_node', 'rotation'):
            frame = self.frame(); root = ET.fromstring(frame['xml'])
            if mutation == 'ancestor':
                node = next(n for n in root.iter('node') if n.get('resource-id') == 'android:id/button1')
                parents = {child: parent for parent in root.iter() for child in parent}; parent = parents[node]
                parent.remove(node); ET.SubElement(parent, 'node', parent.attrib).append(node)
            elif mutation == 'panel_child':
                panel = next(n for n in root.iter('node') if n.get('resource-id') == runner.PACKAGE + ':id/parentPanel')
                ET.SubElement(panel, 'node', {'package': runner.PACKAGE})
            elif mutation == 'foreign_node': ET.SubElement(root, 'node', {'package': 'other.app'})
            else: root.set('rotation', '1')
            frame['xml'] = ET.tostring(root)
            with self.subTest(mutation=mutation), self.assertRaises(runner.JourneyError):
                alarm.alarm_dialog_identity(self.folder, self.shot(frame), proof)

    def test_both_activity_samples_full_image_size_and_contract_bytes_are_required(self):
        for role in ('foreground', 'foreground_final', 'png'):
            frame = self.frame()
            frame[role] = legacy.png(1) if role == 'png' else ('topResumedActivity=' + day.EDITOR + '\n').encode()
            with self.subTest(role=role), self.assertRaises(runner.JourneyError):
                alarm.alarm_dialog_identity(self.folder, self.shot(frame), proof)
        with patch.object(Path, 'read_bytes', return_value=b'{}'), self.assertRaisesRegex(runner.JourneyError, 'contract changed'):
            alarm._contract()

    def test_complete_new_plan_preserves_twelve_entries_and_changes_only_the_observed_boundary(self):
        prefix = day.expected_plan()
        self.assertEqual(runner.PLAN[:12], prefix[:12])
        self.assertEqual(runner.PLAN[12], [alarm.DIALOG, runner.PACKAGE, alarm.OK, day.DAY_TIME])
        self.assertEqual(runner.PLAN[13], [alarm.TERMINAL, alarm.SETTINGS, None, alarm.OK])
        self.assertEqual(sum(bool(step[3]) for step in runner.PLAN), 13)
        self.assertEqual(runner.fingerprint(runner.PLAN), alarm.PLAN_SHA256)
        observed.require_plan()
        historical = reviewed_historical_plan()
        self.assertNotEqual(runner.fingerprint(historical), alarm.PLAN_SHA256)
        with patch.object(runner, 'PLAN', historical): observed.require_plan()
        self.assertEqual(runner.fingerprint(runner.PLAN), alarm.PLAN_SHA256)

    def test_every_plan_step_and_policy_identity_remains_exact(self):
        for index in range(14):
            changed = copy.deepcopy(runner.PLAN); changed[index][3] = {'text': 'Unobserved input'}
            with self.subTest(step=index), patch.object(runner, 'PLAN', changed), self.assertRaises(runner.JourneyError):
                observed.require_plan()
        for changed in (runner.PLAN[:-1], runner.PLAN + [runner.PLAN[-1]]):
            with patch.object(runner, 'PLAN', changed), self.assertRaises(runner.JourneyError): alarm.require_plan()

    def input(self, edit=None):
        clock = {'now': 0.0}
        frames = [self.frame() for _ in range(4)]
        if edit:
            for frame in frames[2:]: edit(frame)
        self.recorder = VirtualRecorder(self.folder, clock, frames)
        def sleep(seconds): clock['now'] += seconds
        with patch.object(runner.time, 'monotonic', side_effect=lambda: clock['now']), \
                patch.object(runner.time, 'sleep', side_effect=sleep):
            previous = observed.capture(self.recorder, 'candidate-' + alarm.DIALOG, runner.PACKAGE)
            previous['name'] = alarm.DIALOG
            return runner.capture_transition(self.recorder, previous, 'candidate-' + alarm.TERMINAL,
                                             alarm.TERMINAL, alarm.OK, proof)

    def test_actual_recorder_command_generation_uses_one_fresh_observed_ok(self):
        transition = self.input()
        self.assertEqual(self.recorder.inputs, [['input', 'tap', '560', '809']])
        self.assertLess(transition['precondition_age_seconds'], 15)
        self.assertEqual(transition['action'], alarm.OK)
        self.assertEqual(len(self.recorder.frames), 0)

    def test_late_app_pid_component_and_entire_preinput_age_remain_checked(self):
        for edit in (lambda f: f.update(late_pid=b'32'),
                     lambda f: f.update(late_foreground=('topResumedActivity=' + day.EDITOR + '\n').encode()),
                     lambda f: f.update(delay=16)):
            with self.assertRaises(ValueError): self.input(edit)
            self.assertEqual(self.recorder.inputs, [])


class SettingsBoundaryControls(unittest.TestCase):
    def setUp(self):
        context = alarm.configured_plan(); context.__enter__(); self.addCleanup(context.__exit__, None, None, None)
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name)
        self.clock = {'now': 0.0}

    def capture(self, label='candidate-after-exact-alarm-ok', owner=alarm.SETTINGS, frames=None):
        frame = {'xml': settings_xml(), 'png': synthetic_settings_png(), 'pid': b'41',
                 'foreground': (b'topResumedActivity=com.android.settings/.SyntheticDestination\n')}
        self.recorder = VirtualRecorder(self.folder, self.clock, frames or [copy.deepcopy(frame), copy.deepcopy(frame)])
        def sleep(seconds): self.clock['now'] += seconds
        with patch.object(runner.time, 'monotonic', side_effect=lambda: self.clock['now']), \
                patch.object(runner.time, 'sleep', side_effect=sleep):
            return observed.capture(self.recorder, label, owner)

    def test_new_plan_records_settings_with_main_app_pid_and_no_settings_input(self):
        shot = self.capture(); shot['name'] = alarm.TERMINAL
        state = observed.stable_snapshot(self.folder, shot, proof, 'candidate')
        self.assertEqual(state[1:3], (720, 1280))
        terminal = alarm.required_surface(self.folder, shot, None, proof)
        self.assertEqual(terminal['component'], 'com.android.settings/com.android.settings.SyntheticDestination')
        self.assertFalse(terminal['permission_granted']); self.assertEqual(terminal['settings_inputs'], 0)
        self.assertEqual(self.recorder.inputs, [])
        pid_commands = [c['argv'] for c in self.recorder.log if c['argv'][0] == 'shell' and c['argv'][1].startswith('pidof ')]
        self.assertEqual(pid_commands, [['shell', 'pidof ' + runner.PACKAGE]] * 4)

    def test_settings_owner_is_rejected_for_each_old_plan_and_for_other_labels(self):
        import favourite_info_journey as favourite
        import trigger_category_journey as category
        shot = self.capture()
        for plan in (favourite.expected_plan(), category.expected_plan(), day.expected_plan(), reviewed_historical_plan()):
            with self.subTest(screens=len(plan)), patch.object(runner, 'PLAN', plan), self.assertRaises(runner.JourneyError):
                runner.validate_snapshot(self.folder, shot, proof)
        for label in ('candidate-home', 'candidate-after-exact-alarm-ok-before', 'unreviewed-after-exact-alarm-ok'):
            with self.subTest(label=label), self.assertRaises(runner.JourneyError): self.capture(label)

    def test_terminal_artifact_roles_cannot_mix_frames_or_use_alias_labels(self):
        shot = self.capture()
        for role in SUFFIXES:
            changed = copy.deepcopy(shot)
            changed['artifacts'][role]['path'] = changed['artifacts'][role]['path'].replace('-frame-2', '-frame-1')
            with self.subTest(role=role), self.assertRaises(runner.JourneyError):
                alarm.validate_settings_snapshot(self.folder, changed, proof)
        for suffix in ('-acquisition-4-frame-2.png', '-acquisition-1-frame-7.png'):
            changed = copy.deepcopy(shot)
            changed['artifacts']['screenshot']['path'] = 'candidate-' + alarm.TERMINAL + suffix
            with self.assertRaises(runner.JourneyError): alarm.validate_settings_snapshot(self.folder, changed, proof)

    def test_new_settings_capture_keeps_semantic_process_and_component_failures(self):
        base = {'xml': settings_xml(), 'png': synthetic_settings_png(), 'pid': b'41',
                'foreground': b'topResumedActivity=com.android.settings/.SyntheticDestination\n'}
        for mutation in ('owner', 'component', 'pid'):
            frames = [copy.deepcopy(base), copy.deepcopy(base)]
            if mutation == 'owner': frames[0]['xml'] = frames[0]['xml'].replace(b'com.android.settings', b'other.app')
            elif mutation == 'component': frames[1]['foreground'] = b'topResumedActivity=com.android.settings/.OtherDestination\n'
            else: frames[1]['pid'] = b'42'
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): self.capture(frames=frames)
            self.assertEqual(self.recorder.inputs, [])
            self.assertTrue(self.recorder.capture_events)


class ExactAlarmComparisonControls(unittest.TestCase):
    def setUp(self):
        context = alarm.configured_plan(); context.__enter__(); self.addCleanup(context.__exit__, None, None, None)
        self.fixture = FourteenFixture(); self.addCleanup(self.fixture.close)
        add_readiness(self.fixture)

    def test_complete_authored_pair_has_fourteen_screens_and_only_settings_observation_scope(self):
        result = self.fixture.result()
        self.assertTrue(result['journey_equal'], result)
        self.assertEqual(len(result['screens']), 14)
        self.assertEqual(result['status'], 'EXACT_ALARM_SETTINGS_OBSERVATION_ONLY')
        self.assertTrue(result['exact_alarm_explanation_ok_tapped'])
        self.assertEqual(len(result['notification_readiness_observations']), 2)
        self.assertEqual(result['settings_inputs'], 0)
        for key in ('permission_granted', 'trigger_configuration_confirmed', 'full_runtime_1_to_1_established',
                    'macros_saved', 'macros_executed', 'crash_free_run_established'):
            self.assertFalse(result[key])

    def test_schema_plan_and_policy_substitutions_fail_before_observation_comparison(self):
        base = self.fixture.report
        changes = [lambda r: r.update(schema=3), lambda r: r.update(schema=5), lambda r: r.update(schema=True),
                   lambda r: r.pop(alarm.POLICY_KEY), lambda r: r[alarm.POLICY_KEY].update(settings_inputs=1),
                   lambda r: r['runs'][0].update({alarm.POLICY_KEY: copy.deepcopy(alarm.POLICY)}),
                   lambda r: r['plan'][-1].__setitem__(3, {'text': 'Allow'}),
                   lambda r: r.update(plan_sha256=day.TWELVE_PLAN_SHA256)]
        for change in changes:
            value = copy.deepcopy(base); change(value)
            with self.subTest(change=change):
                result = runner.compare(self.fixture.folder, value, proof)
                self.assertFalse(result['journey_equal'], result)
                self.assertEqual(result['screens'], [])

    def test_missing_extra_terminal_input_and_wrong_ok_command_are_rejected(self):
        for edit in ('missing', 'extra', 'wrong_command'):
            value = copy.deepcopy(self.fixture.report); run = value['runs'][1]
            if edit == 'missing': run['transitions'].pop()
            elif edit == 'extra': run['transitions'].append(copy.deepcopy(run['transitions'][-1]))
            else: run['transitions'][-1]['command']['argv'] = ['shell', 'input tap 2 2']
            with self.subTest(edit=edit): self.assertFalse(runner.compare(self.fixture.folder, value, proof)['journey_equal'])

    def test_every_changed_terminal_pixel_remains_in_exact_comparison(self):
        self.fixture.edit_stable(self.fixture.candidate()['screens'][-1],
            lambda shot: self.fixture.raw_value(shot, 'screenshot', synthetic_settings_png(199)))
        result = self.fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertEqual(result['status'], 'JOURNEY_DIFFERENCE')
        self.assertEqual(result['screens'][-1]['changed_pixels'], 720 * 1280)
        self.assertFalse(result['masks_used'])

    def test_different_stable_settings_component_is_preserved_and_fails_pair_identity(self):
        def edit(shot):
            for role in ('foreground', 'foreground_final'):
                self.fixture.raw_value(shot, role, b'topResumedActivity=com.android.settings/.OtherDestination\n')
        self.fixture.edit_stable(self.fixture.candidate()['screens'][-1], edit)
        result = self.fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertFalse(result.get('terminal_surface_identities_equal', True), result)


if __name__ == '__main__':
    unittest.main()
