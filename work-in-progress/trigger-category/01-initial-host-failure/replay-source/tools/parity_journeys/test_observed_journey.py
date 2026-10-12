"""Synthetic rejection controls and raw-fixture checks; no Android execution."""
from __future__ import annotations

import copy
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import editor_journey as runner
import observed_journey as observed
from robust_capture import EvidenceRecorder
import test_editor_journey as legacy

proof = legacy.proof


def reviewed_historical_plan():
    data = (Path(__file__).with_name('fixtures') / 'reviewed-reference-plan14.json').read_bytes()
    if hashlib.sha256(data).hexdigest() != 'ff578443029fff6da5056f0e8eb30e07cc7c74c8bada126939062e5bbc311df3':
        raise runner.JourneyError('Pinned historical fourteen-step test fixture changed')
    return json.loads(data)


@contextmanager
def configured_historical_plan():
    # Retain the original synthetic controls without replacing the external
    # sixteen-step adapter or enabling any new device action in this test policy.
    with patch.object(runner, 'PLAN', reviewed_historical_plan()), \
            patch.object(runner, 'Recorder', EvidenceRecorder):
        yield runner.PLAN


class ObservedFixture:
    def __init__(self):
        self.legacy = legacy.JourneyTests()
        plan = runner.PLAN
        try:
            if len(plan) == 10:
                runner.PLAN = reviewed_historical_plan()
            self.legacy.setUp()
        finally:
            runner.PLAN = plan
        self.folder = self.legacy.root
        self.base = copy.deepcopy(self.legacy.report)
        self.sequence = 0
        self.build()

    def close(self):
        self.legacy.tearDown()

    def put(self, name, data):
        return self.legacy.put(name, data)

    def command(self, args, out, start):
        self.sequence += 1
        name = 'command-observed-' + str(self.sequence)
        return {'argv': ['shell', shlex.join(args)], 'returncode': 0, 'timed_out': False,
                'started_monotonic': start, 'finished_monotonic': start + 0.05,
                'stdout': self.put(name + '.stdout', out), 'stderr': self.put(name + '.stderr', b'')}

    def front(self, index):
        if index == 4:
            return observed.PERMISSION_ACTIVITY
        if len(runner.PLAN) == 10 and index >= 7:
            import favourite_info_journey as favourite
            return favourite.EDITOR
        if index >= 5:
            return observed.HOME
        return runner.PACKAGE + '/' + runner.PACKAGE + '.intro.IntroActivity'

    def xml(self, index):
        if len(runner.PLAN) == 10 and index >= 8:
            import favourite_info_journey as favourite
            root = ET.Element('hierarchy')
            attributes = {'package': runner.PACKAGE, 'enabled': 'true', 'clickable': 'true',
                          'bounds': '[0,0][4,4]', 'class': 'android.widget.Button'}
            if index == 8:
                for selector, kind in [(favourite.TITLE, 'android.widget.TextView'),
                                       ({'resource-id': 'android:id/message', 'text': favourite.MESSAGE}, 'android.widget.TextView'),
                                       (favourite.OK, 'android.widget.Button')]:
                    ET.SubElement(root, 'node', {**attributes, **selector, 'class': kind})
            else:
                ET.SubElement(root, 'node', {**attributes, **runner.TRIGGER})
            return ET.tostring(root)
        root = ET.fromstring(legacy.xml(index))
        for node in root.iter('node'):
            if node.get('text') == 'LITEAPKS':
                node.set('class', 'android.widget.TextView')
                node.set('clickable', 'false')
            else:
                node.set('class', 'android.widget.Button')
        return ET.tostring(root)

    def stable(self, label, index, pid, start):
        shots = []
        for number in range(2):
            name = label + '-frame-' + str(number + 1)
            timestamp = start + number * 1.2
            contents = {'hierarchy': self.xml(index), 'screenshot': legacy.png(index + 1),
                        'pid_first': pid.encode(), 'pid_final': pid.encode(),
                        'foreground': ('topResumedActivity=' + self.front(index) + '\n').encode(),
                        'foreground_final': ('topResumedActivity=' + self.front(index) + '\n').encode()}
            shots.append({'owner': runner.PLAN[index][1], 'sample_interval_seconds': 1.1,
                          'observation': {'started_monotonic': timestamp, 'finished_monotonic': timestamp + 1.1},
                          'artifacts': {key: self.put(name + '-' + key, data) for key, data in contents.items()}})
        event = {'schema': 1, 'status': 'CONSECUTIVE_FULL_FRAMES_IDENTICAL', 'label': label,
                 'owner': runner.PLAN[index][1], 'max_attempts': 6, 'max_seconds': 30,
                 'started_monotonic': start, 'finished_monotonic': start + 2.31, 'seconds': 2.31,
                 'attempts': shots, 'accepted_pair': [0, 1]}
        record = self.put(label + '-settling.json', json.dumps(event).encode())
        self.report['capture_events'].append(record)
        result = copy.deepcopy(shots[-1])
        result['settling'] = record
        return result

    def diagnostics(self, start):
        return {'processes': self.command(['dumpsys', 'activity', 'processes', runner.PACKAGE], b'raw processes\n', start),
                'crash': self.command(['logcat', '-d', '-b', 'crash', '-v', 'threadtime'], b'', start + 0.1)}

    def boundary(self, run, transition, prior, shot, old, new, start):
        process_data = ('PID NAME\n1 init\n' + new + ' ' + runner.PACKAGE + '\n500 adbd\n').encode()
        command_data = [
            ('pid_first', ['pidof', runner.PACKAGE], new.encode()),
            ('process_list_first', ['ps', '-A', '-o', 'PID,NAME'], process_data),
            ('installed_path', ['pm', 'path', runner.PACKAGE], b'package:/data/app/test/base.apk\n'),
            ('installed_checksum', ['sha256sum', '/data/app/test/base.apk'],
             (run['apk_sha256'] + '  /data/app/test/base.apk\n').encode()),
            ('foreground', ['dumpsys', 'activity', 'activities'], ('topResumedActivity=' + observed.HOME + '\n').encode()),
            ('process_list_final', ['ps', '-A', '-o', 'PID,NAME'], process_data),
            ('pid_final', ['pidof', runner.PACKAGE], new.encode()),
        ]
        record = {'schema': 1, 'status': 'OBSERVED_NOTIFICATION_BOUNDARY', 'old_pid': old, 'new_pid': new,
                  'started_monotonic': start, 'finished_monotonic': start + 1.1,
                  'commands': {key: self.command(args, out, start + number * 0.1)
                               for number, (key, args, out) in enumerate(command_data)},
                  'after_diagnostics': self.diagnostics(start + 0.8)}
        crash = observed.crash_observation(self.folder, transition['pre_denial_diagnostics'], record['after_diagnostics'], old, proof)
        record.update(crash_observation=crash, outcome=observed.outcome(old, new, crash))
        transition['process_handoff'] = self.put(run['label'] + '-notification-boundary.json', json.dumps(record).encode())

    def build(self, candidate_replaced=True):
        self.report = copy.deepcopy(self.base)
        self.report.update(schema=3, capture_policy=copy.deepcopy(observed.POLICY), capture_events=[])
        self.report['plan_sha256'] = runner.fingerprint(runner.PLAN)
        for run_number, run in enumerate(self.report['runs']):
            old = '31' if run_number == 0 else '51'
            new = '41' if run_number == 0 else ('61' if candidate_replaced else '51')
            run['screens'], run['transitions'] = [], []
            now = 1000.0 + run_number * 1000
            for index, (name, owner, required, action) in enumerate(runner.PLAN):
                prefix = run['label'] + '-' + name
                if index:
                    before_start = now + (0.3 if action == runner.DENY or name == 'after-favourite-info' else 0)
                    before = self.stable(prefix + '-before', index - 1, old if index <= 5 else new, before_start)
                    front = ('topResumedActivity=' + self.front(index - 1) + '\n').encode()
                    pid = (old if index <= 5 else new).encode()
                    live_commands = {'pid': self.command(['pidof', runner.PACKAGE], pid, before_start + 2.4),
                                     'foreground': self.command(['dumpsys', 'activity', 'activities'], front, before_start + 2.5)}
                    input_start = before_start + 2.6
                    argv = ['input', 'keyevent', '4'] if action == 'BACK' else ['input', 'tap', '2', '2']
                    transition = {'to': name, 'action': action, 'before': before,
                                  'observation_started_monotonic': now,
                                  'precondition_age_seconds': input_start - now,
                                  'preinput_artifacts': {'pid': self.put(prefix + '-preinput-pid', pid),
                                                         'foreground': self.put(prefix + '-preinput-foreground', front)},
                                  'preinput_commands': live_commands,
                                  'command': self.command(argv, b'', input_start)}
                    if action == runner.DENY:
                        transition['pre_denial_diagnostics'] = self.diagnostics(now)
                    if name == 'after-favourite-info':
                        transition['pre_ok_installed_identity'] = {
                            'installed_path': self.command(['pm', 'path', runner.PACKAGE], b'package:/data/app/test/base.apk\n', now),
                            'installed_checksum': self.command(['sha256sum', '/data/app/test/base.apk'],
                                (run['apk_sha256'] + '  /data/app/test/base.apk\n').encode(), now + 0.1)}
                    run['transitions'].append(transition)
                    now = input_start + 0.15
                shot = self.stable(prefix, index, old if index < 5 else new, now)
                shot['name'] = name
                run['screens'].append(shot)
                now += 2.5
                if index == 5:
                    self.boundary(run, run['transitions'][-1], run['screens'][-2], shot, old, new, now)
                    now += 1.2

    def result(self):
        return runner.compare(self.folder, self.report, proof)

    def candidate(self):
        return self.report['runs'][1]

    def change_boundary(self, edit):
        transition = self.candidate()['transitions'][4]
        artifact = transition['process_handoff']
        value = json.loads(proof.artifact(self.folder, artifact))
        edit(value)
        transition['process_handoff'] = self.put(artifact['path'], json.dumps(value).encode())

    def replace_output(self, record, data):
        record['stdout'] = self.put(record['stdout']['path'], data)

    def edit_stable(self, shot, edit):
        artifact = shot['settling']
        event = json.loads(proof.artifact(self.folder, artifact))
        for attempt in event['attempts']:
            edit(attempt)
        name = shot.get('name')
        shot.clear()
        shot.update(copy.deepcopy(event['attempts'][-1]))
        record = self.put(artifact['path'], json.dumps(event).encode())
        shot['settling'] = record
        if name is not None:
            shot['name'] = name
        self.report['capture_events'] = [record if item['path'] == record['path'] else item
                                         for item in self.report['capture_events']]

    def raw_value(self, shot, key, data):
        shot['artifacts'][key] = self.put(shot['artifacts'][key]['path'], data)


class ObservedVerifierTests(unittest.TestCase):
    def setUp(self):
        self.context = configured_historical_plan()
        self.context.__enter__()
        self.addCleanup(self.context.__exit__, None, None, None)
        self.fixture = ObservedFixture()
        self.addCleanup(self.fixture.close)

    def rejected(self, text=None):
        result = self.fixture.result()
        self.assertFalse(result['journey_equal'], result)
        if text:
            self.assertIn(text, result.get('reason', ''), result)
        return result

    def test_two_proved_replacements_keep_all_full_screens_and_narrow_scope(self):
        result = self.fixture.result()
        self.assertTrue(result['journey_equal'], result)
        self.assertEqual(len(result['screens']), 14)
        self.assertTrue(result['process_handoff_outcomes_equal'])
        self.assertTrue(all(item['pid_replaced'] for item in result['process_handoff_outcomes']))
        self.assertFalse(result['process_handoff_cause_established'])
        self.assertFalse(result['full_runtime_1_to_1_established'])

    def test_continuity_in_only_one_variant_is_a_real_outcome_difference(self):
        self.fixture.build(candidate_replaced=False)
        result = self.rejected()
        self.assertEqual(result['status'], 'JOURNEY_DIFFERENCE', result)
        self.assertFalse(result['process_handoff_outcomes_equal'])
        self.assertTrue(all(item['changed_pixels'] == 0 for item in result['screens']))

    def test_old_pid_in_either_all_process_sample_rejects_replacement(self):
        for key in ['process_list_first', 'process_list_final']:
            with self.subTest(sample=key):
                self.fixture.build()
                self.fixture.change_boundary(lambda r: self.fixture.replace_output(
                    r['commands'][key], b'PID NAME\n1 init\n51 old-app\n61 com.arlosoft.macrodroid\n'))
                self.rejected('Old PID remains present')

    def test_truncated_or_ambiguous_main_process_listing_is_rejected(self):
        values = [b'PID NAME\n61 com.arlosoft.macrodroid\n',
                  b'PID NAME\n1 init\n61 com.arlosoft.macrodroid\n62 com.arlosoft.macrodroid\n',
                  b'PID NAME\n1 init\n61 other.package\n']
        for value in values:
            with self.subTest(value=value):
                self.fixture.build()
                self.fixture.change_boundary(lambda r: self.fixture.replace_output(r['commands']['process_list_first'], value))
                self.rejected()

    def test_fresh_device_apk_checksum_and_path_are_required(self):
        for key, data in [('installed_checksum', b'9999999999999999999999999999999999999999999999999999999999999999  /data/app/test/base.apk\n'),
                          ('installed_path', b'package:/data/app/replaced/base.apk\n')]:
            with self.subTest(field=key):
                self.fixture.build()
                self.fixture.change_boundary(lambda r: self.fixture.replace_output(r['commands'][key], data))
                self.rejected()

    def test_initial_checksum_artifact_cannot_be_reused_as_a_fresh_measurement(self):
        old = self.fixture.candidate()['installed_checksum']['stdout']
        self.fixture.change_boundary(lambda r: r['commands']['installed_checksum'].update(stdout=old))
        self.rejected('reused an earlier artifact')

    def test_process_list_samples_require_independent_files(self):
        self.fixture.change_boundary(lambda r: r['commands']['process_list_final'].update(
            stdout=r['commands']['process_list_first']['stdout']))
        self.rejected('reused an earlier artifact')

    def test_late_pid_or_foreground_change_during_boundary_rejects(self):
        for key, data in [('pid_final', b'62'), ('foreground', b'topResumedActivity=com.arlosoft.macrodroid/.OtherActivity\n')]:
            with self.subTest(field=key):
                self.fixture.build()
                self.fixture.change_boundary(lambda r: self.fixture.replace_output(r['commands'][key], data))
                self.rejected()

    def test_changed_pid_inside_a_snapshot_is_still_rejected(self):
        shot = self.fixture.candidate()['screens'][8]
        self.fixture.edit_stable(shot, lambda s: self.fixture.raw_value(s, 'pid_final', b'62'))
        self.rejected('PID changed')

    def test_new_restart_after_denial_boundary_is_not_another_allowed_handoff(self):
        shot = self.fixture.candidate()['screens'][-1]
        def edit(value):
            for key in ['pid_first', 'pid_final']:
                self.fixture.raw_value(value, key, b'62')
        self.fixture.edit_stable(shot, edit)
        self.rejected('PID changed')

    def test_late_preinput_pid_after_the_boundary_is_rejected(self):
        transition = self.fixture.candidate()['transitions'][6]
        transition['preinput_artifacts']['pid'] = self.fixture.put('candidate-late-input-pid', b'62')
        self.rejected('PID changed')

    def test_multiple_live_pids_are_not_a_single_stable_process(self):
        shot = self.fixture.candidate()['screens'][5]
        def edit(value):
            for key in ['pid_first', 'pid_final']:
                self.fixture.raw_value(value, key, b'61 62')
        self.fixture.edit_stable(shot, edit)
        self.rejected('Exactly one live main app PID')

    def test_boundary_cannot_move_to_an_unobserved_step(self):
        run = self.fixture.candidate()
        run['transitions'][5]['process_handoff'] = run['transitions'][4]['process_handoff']
        self.rejected('Unplanned process-boundary evidence')

    def test_forged_handoff_boolean_or_missing_diagnostics_is_rejected(self):
        self.fixture.change_boundary(lambda r: r['outcome'].update(pid_replaced=False))
        self.rejected('differs from observed command bytes')
        self.fixture.build()
        self.fixture.candidate()['transitions'][4].pop('pre_denial_diagnostics')
        self.rejected()

    def test_stale_boundary_and_reversed_command_order_are_rejected(self):
        for edit in [lambda r: r.update(started_monotonic=0),
                     lambda r: r['commands']['pid_final'].update(started_monotonic=0)]:
            self.fixture.build()
            self.fixture.change_boundary(edit)
            self.rejected()

    def test_freshness_cannot_restart_after_slow_acquisition(self):
        transition = self.fixture.candidate()['transitions'][0]
        transition['observation_started_monotonic'] = transition['command']['started_monotonic'] - 0.1
        transition['precondition_age_seconds'] = 0.1
        self.rejected('does not include its full acquisition')

    def test_fresh_preinput_records_must_match_captured_immediate_bytes(self):
        transition = self.fixture.candidate()['transitions'][0]
        self.fixture.replace_output(transition['preinput_commands']['pid'], b'999')
        self.rejected('bytes or timing are inconsistent')

    def test_stable_but_different_final_pixels_are_never_normalized(self):
        shot = self.fixture.candidate()['screens'][-1]
        self.fixture.edit_stable(shot, lambda s: self.fixture.raw_value(s, 'screenshot', legacy.png(222)))
        result = self.rejected()
        self.assertEqual(result['status'], 'JOURNEY_DIFFERENCE')
        self.assertEqual(result['screens'][-1]['changed_pixels'], 16)

    def test_stable_but_changed_xml_attribute_is_preserved(self):
        shot = self.fixture.candidate()['screens'][-1]
        def edit(value):
            data = proof.artifact(self.fixture.folder, value['artifacts']['hierarchy'])
            self.fixture.raw_value(value, 'hierarchy', data.replace(b'<hierarchy>', b'<hierarchy changed="yes">'))
        self.fixture.edit_stable(shot, edit)
        result = self.rejected()
        self.assertEqual(result['status'], 'JOURNEY_DIFFERENCE')
        self.assertFalse(result['screens'][-1]['hierarchy_equal'])

    def test_missing_or_altered_settling_policy_is_rejected(self):
        for edit in [lambda r: r.pop('capture_policy'), lambda r: r['capture_policy'].update(settling_max_attempts=100),
                     lambda r: r.update(schema=2), lambda r: r['capture_events'].pop()]:
            self.fixture.build()
            edit(self.fixture.report)
            self.rejected()


class VirtualRecorder(EvidenceRecorder):
    """Run the real base snapshot and external XML-retry adapter on virtual ADB."""
    def __init__(self, folder, clock, frames):
        with patch.object(runner.shutil, 'which', return_value='/virtual/adb'):
            super().__init__(folder, 'virtual-emulator', proof)
        self.clock, self.frames = clock, list(frames)
        self.capture_policy = observed.POLICY
        self.inputs = []
        self.frame = None
        self.pid_reads = 0

    def _snapshot_once(self, label, owner):
        if not self.frames:
            raise AssertionError('Test frame supply exhausted')
        self.frame = self.frames.pop(0)
        self.pid_reads = 0
        self.foreground_reads = 0
        return super()._snapshot_once(label, owner)

    def cmd(self, args, timeout=120):
        if self.deadline is not None and self.clock['now'] >= self.deadline:
            raise runner.JourneyError('Observed command deadline expired before execution')
        self.count += 1
        started = self.clock['now']
        self.clock['now'] += 0.05
        data = b''
        if args[0] == 'shell':
            argv = shlex.split(args[1])
            if argv[0] == 'pidof':
                self.pid_reads += 1
                data = self.frame.get('late_pid', b'31') if self.pid_reads > 2 else self.frame.get('pid', b'31')
            elif argv[:3] == ['dumpsys', 'activity', 'activities']:
                self.foreground_reads += 1
                front = self.frame.get('foreground', ('topResumedActivity=' + runner.PACKAGE + '/' + runner.PACKAGE + '.intro.IntroActivity\n').encode())
                data = self.frame.get('late_foreground', front) if self.foreground_reads > 2 else front
            elif argv[:2] == ['pm', 'path']:
                data = b'package:/data/app/test/base.apk\n'
            elif argv[0] == 'sha256sum':
                data = (getattr(self, 'device_apk_sha256', '2' * 64) + '  /data/app/test/base.apk\n').encode()
            elif argv[0] == 'input':
                self.inputs.append(argv)
            elif argv[0] not in ('uiautomator', 'rm'):
                raise AssertionError('Unexpected virtual command: ' + str(argv))
        elif args[:2] == ['exec-out', 'cat']:
            self.clock['now'] += self.frame.get('delay', 0)
            data = self.frame.get('xml', legacy.xml(0))
        elif args == ['exec-out', 'screencap', '-p']:
            data = self.frame.get('png', legacy.png(1))
        else:
            raise AssertionError('Unexpected virtual ADB: ' + str(args))
        name = 'command-virtual-' + str(self.count)
        item = {'argv': args, 'returncode': 0, 'timed_out': False,
                'started_monotonic': started, 'finished_monotonic': self.clock['now'],
                'stdout': self.save(name + '.stdout', data), 'stderr': self.save(name + '.stderr', b'')}
        self.log.append(item)
        return item, data, b''


class AcquisitionControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.clock = {'now': 0.0}

    def capture(self, frames, budget=30):
        recorder = VirtualRecorder(self.folder, self.clock, frames)
        self.recorder = recorder
        def sleep(seconds):
            self.clock['now'] += seconds
        with patch.object(runner.time, 'monotonic', side_effect=lambda: self.clock['now']), \
                patch.object(runner.time, 'sleep', side_effect=sleep), observed.command_budget(recorder, budget):
            return recorder.snapshot('candidate-intro-1', runner.PACKAGE)

    def test_first_identical_pair_is_accepted_and_unequal_intermediate_is_retained(self):
        shot = self.capture([{'png': legacy.png(9)}, {}, {}])
        event = json.loads(proof.artifact(self.folder, shot['settling']))
        self.assertEqual(event['accepted_pair'], [1, 2])
        self.assertEqual(len(event['attempts']), 3)
        self.assertNotEqual(proof.artifact(self.folder, event['attempts'][0]['artifacts']['screenshot']),
                            proof.artifact(self.folder, event['attempts'][1]['artifacts']['screenshot']))
        observed.stable_snapshot(self.folder, shot, proof, 'candidate')
        self.assertEqual(self.recorder.frames, [])

    def test_capture_stops_at_the_first_pair_without_reading_a_later_frame(self):
        shot = self.capture([{}, {}, {'png': legacy.png(99)}])
        self.assertEqual(len(self.recorder.frames), 1)
        self.assertEqual(json.loads(proof.artifact(self.folder, shot['settling']))['accepted_pair'], [0, 1])

    def test_six_unstable_full_frames_fail_with_all_raw_attempts_preserved(self):
        with self.assertRaisesRegex(runner.JourneyError, 'within six attempts'):
            self.capture([{'png': legacy.png(n)} for n in range(6)])
        event = json.loads(proof.artifact(self.folder, self.recorder.capture_events[-1]))
        self.assertEqual(event['status'], 'FAILED')
        self.assertEqual(len(event['attempts']), 6)
        self.assertEqual(len(list(self.folder.glob('*-frame-*.png'))), 6)
        self.assertEqual(self.recorder.inputs, [])

    def test_whole_hierarchy_must_be_identical_even_when_png_is_static(self):
        altered = legacy.xml(0).replace(b'<hierarchy>', b'<hierarchy changed="yes">')
        shot = self.capture([{'xml': altered}, {}, {}])
        event = json.loads(proof.artifact(self.folder, shot['settling']))
        self.assertEqual(event['accepted_pair'], [1, 2])

    def test_process_change_between_valid_frames_is_not_retried(self):
        with self.assertRaisesRegex(runner.JourneyError, 'Process or component changed'):
            self.capture([{}, {'pid': b'32'}, {}])
        self.assertEqual(len(self.recorder.frames), 1)
        self.assertEqual(len(self.recorder.capture_events), 1)

    def test_actual_parse_error_keeps_external_retry_and_resets_the_pair(self):
        shot = self.capture([{}, {'xml': b'cat: /missing: No such file or directory\n'}, {}, {}])
        self.assertEqual(len(self.recorder.capture_events), 2)
        first = json.loads(proof.artifact(self.folder, self.recorder.capture_events[0]))
        self.assertEqual(first['error_type'], 'ParseError')
        retained = json.loads(proof.artifact(self.folder, first['last_raw_snapshot']))
        self.assertIn(b'No such file', proof.artifact(self.folder, retained['artifacts']['hierarchy']))
        self.assertTrue((self.folder / 'candidate-intro-1-acquisition-1-acquisition-error.json').is_file())
        last = json.loads(proof.artifact(self.folder, shot['settling']))
        self.assertEqual(last['accepted_pair'], [0, 1])
        self.assertEqual(len(last['attempts']), 2)

    def test_three_bad_xml_attempts_still_fail_without_semantic_retry(self):
        with self.assertRaisesRegex(runner.JourneyError, 'three fresh attempts'):
            self.capture([{'xml': b'bad xml'}] * 3)
        self.assertEqual(len(self.recorder.capture_events), 3)
        self.assertEqual(len(list(self.folder.glob('*acquisition-error.json'))), 3)

    def test_capture_deadline_preserves_failure_before_any_input(self):
        with self.assertRaisesRegex(runner.JourneyError, 'deadline'):
            self.capture([{'delay': 31}, {}, {}])
        self.assertEqual(self.recorder.inputs, [])
        self.assertEqual(json.loads(proof.artifact(self.folder, self.recorder.capture_events[-1]))['status'], 'FAILED')

    def test_reused_acquisition_path_or_skipped_first_match_is_rejected(self):
        shot = self.capture([{}, {}])
        meta = shot['settling']
        event = json.loads(proof.artifact(self.folder, meta))
        event['attempts'][0]['artifacts']['hierarchy'] = event['attempts'][1]['artifacts']['hierarchy']
        shot['settling'] = self.recorder.save(meta['path'], json.dumps(event).encode())
        with self.assertRaisesRegex(runner.JourneyError, 'reused an earlier artifact'):
            observed.stable_snapshot(self.folder, shot, proof, 'candidate')

    def test_real_adb_timeout_retains_partial_outputs_and_uses_remaining_budget(self):
        with patch.object(runner.shutil, 'which', return_value='/virtual/adb'):
            recorder = runner.Recorder(self.folder, 'virtual', proof)
        recorder.deadline = 5
        timeout = subprocess.TimeoutExpired(['/virtual/adb'], 5, output=b'partial XML', stderr=b'transfer stalled')
        with patch.object(runner.time, 'monotonic', side_effect=[0, 0, 1]), \
                patch.object(runner.subprocess, 'run', side_effect=timeout) as execute:
            with self.assertRaisesRegex(runner.JourneyError, 'partial output retained'):
                recorder.cmd(['exec-out', 'cat', '/data/local/tmp/owned.xml'])
        self.assertEqual(execute.call_args.kwargs['timeout'], 5)
        self.assertEqual(len(recorder.log), 1)
        self.assertIsNone(recorder.log[0]['returncode'])
        self.assertTrue(recorder.log[0]['timed_out'])
        self.assertEqual(proof.artifact(self.folder, recorder.log[0]['stdout']), b'partial XML')
        self.assertEqual(proof.artifact(self.folder, recorder.log[0]['stderr']), b'transfer stalled')

    def test_decode_cache_uses_exact_bytes_and_decoder_and_is_bounded(self):
        from types import SimpleNamespace
        observed._decoded_png.cache_clear()
        calls = []
        def decode(data):
            calls.append(data)
            return proof.png_pixels(data)
        wrapped = SimpleNamespace(png_pixels=decode)
        first = legacy.png(1)
        self.assertEqual(observed.png_pixels(first, wrapped), observed.png_pixels(bytes(first), wrapped))
        self.assertEqual(len(calls), 1)
        self.assertNotEqual(observed.png_pixels(legacy.png(2), wrapped), observed.png_pixels(first, wrapped))
        corrupt = first[:-1] + bytes([first[-1] ^ 1])
        with self.assertRaises(ValueError):
            observed.png_pixels(corrupt, wrapped)
        # Another decoder cannot reuse the first decoder's result.
        other = SimpleNamespace(png_pixels=lambda data: ('other decoder', data))
        self.assertEqual(observed.png_pixels(first, other), ('other decoder', first))
        for value in range(3, 9):
            observed.png_pixels(legacy.png(value), wrapped)
        self.assertEqual(observed._decoded_png.cache_info().maxsize, 4)
        self.assertLessEqual(observed._decoded_png.cache_info().currsize, 4)
        observed._decoded_png.cache_clear()


if __name__ == '__main__':
    unittest.main()
