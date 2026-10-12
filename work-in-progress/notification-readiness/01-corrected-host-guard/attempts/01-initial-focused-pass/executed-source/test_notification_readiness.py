"""Synthetic lifecycle and evidence faults; no Android or parity credit."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import shlex
import tempfile
import unittest
from unittest.mock import patch

import day_time_journey as day
import editor_journey as runner
import notification_readiness as ready
import observed_journey as observed
from test_day_time_journey import ThirteenFixture
from test_observed_journey import proof


def home(pid='41'):
    return [(0, (pid + '\n').encode(), b''),
            (0, ('topResumedActivity=' + observed.HOME + '\n').encode(), b''),
            (0, (pid + '\n').encode(), b'')]


class FakeRecorder:
    """Replay an explicit command-result queue against the real readiness runner."""
    save = runner.Recorder.save

    def __init__(self, folder, queue, clock, stem='synthetic', duration=0.05):
        self.folder, self.queue, self.clock = folder, list(queue), clock
        self.proof, self.log, self.deadline = proof, [], None
        self.stem, self.duration = stem, duration

    def shell(self, args):
        if not self.queue:
            raise AssertionError('Unexpected extra readiness command')
        code, out, err = self.queue.pop(0)
        start = self.clock['now']
        timeout = min(120, self.deadline - start)
        if timeout <= 0:
            raise runner.JourneyError('Observed command deadline expired before execution')
        self.clock['now'] += self.duration
        name = self.stem + '-command-' + str(len(self.log))
        command = {'argv': ['shell', shlex.join(args)], 'returncode': code, 'timed_out': code is None,
                   'started_utc': '2026-01-01T00:00:00+00:00', 'started_monotonic': start,
                   'finished_monotonic': self.clock['now'], 'timeout_seconds': timeout,
                   'stdout': self.save(name + '.stdout', out), 'stderr': self.save(name + '.stderr', err)}
        self.log.append(command)
        if code is None:
            raise runner.JourneyError('Device command timed out; partial output retained')
        return command, out, err


class ReadinessControls(unittest.TestCase):
    def setUp(self):
        context = day.configured_plan(); context.__enter__()
        self.addCleanup(context.__exit__, None, None, None)
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name)
        self.clock = {'now': 102.25}
        self.sequence = 0

    def put(self, name, data):
        (self.folder / name).write_bytes(data)
        return {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

    def boundary(self):
        self.sequence += 1
        return {'to': 'reference-promotion', 'action': runner.DENY,
                'command': {'finished_monotonic': 100.0},
                'preinput_artifacts': {
                    'pid': self.put('old-' + str(self.sequence), b'31\n'),
                    'foreground': self.put('front-' + str(self.sequence),
                        ('topResumedActivity=' + observed.PERMISSION_ACTIVITY + '\n').encode())}}

    def run_phase(self, queue, duration=0.05):
        self.transition = self.boundary()
        self.recorder = FakeRecorder(self.folder, queue, self.clock, 'run-' + str(self.sequence), duration)
        def sleep(seconds): self.clock['now'] += seconds
        with patch.object(ready.time, 'monotonic', side_effect=lambda: self.clock['now']), \
                patch.object(ready.time, 'sleep', side_effect=sleep):
            return ready.observe(self.recorder, {'label': 'original'}, self.transition,
                                 {'name': 'notification-request', 'owner': runner.PERMISSION})

    def phase(self):
        return json.loads(proof.artifact(self.folder, self.transition[ready.REFERENCE_KEY]))

    def test_absence_then_first_contiguous_home_sequence_is_retained_and_replayed(self):
        value = self.run_phase([(1, b'', b'')] + home() * 5)
        self.assertEqual([row['observation']['state'] for row in value['observations']],
                         ['MAIN_PID_ABSENT'] + ['HOME_WITH_SAME_PID'] * 4)
        self.assertEqual(value['accepted_sequence'], [1, 4])
        self.assertEqual(value['ready_pid'], '41')
        self.assertEqual(len(self.recorder.queue), 3)
        self.assertEqual(len(ready.verify_phase(self.folder, value, proof)), 13)
        self.assertEqual(self.phase(), value)
        self.assertIsNone(self.recorder.deadline)

    def test_same_process_home_path_has_no_required_crash_or_restart(self):
        value = self.run_phase(home('31') * 5)
        self.assertEqual(value['ready_pid'], value['old_pid'])
        self.assertEqual(value['accepted_sequence'], [0, 3])
        self.assertTrue(all(command['argv'][1].startswith(('pidof ', 'dumpsys activity activities'))
                            for command in ready.verify_phase(self.folder, value, proof)))

    def test_permission_missing_second_pid_and_pid_change_reset_ready_sequence(self):
        permission = home(); permission[1] = (0, ('topResumedActivity=' + observed.PERMISSION_ACTIVITY + '\n').encode(), b'')
        missing = home(); missing[-1] = (1, b'', b'')
        replaced = home(); replaced[-1] = (0, b'42\n', b'')
        value = self.run_phase(home() + permission + missing + replaced + home('42') * 5)
        self.assertEqual([row['observation']['state'] for row in value['observations'][:4]],
                         ['HOME_WITH_SAME_PID', 'PERMISSION_STILL_FOREGROUND',
                          'MAIN_PID_ABSENT_AFTER_FOREGROUND', 'MAIN_PID_CHANGED'])
        self.assertEqual(value['accepted_sequence'], [4, 7])
        ready.verify_phase(self.folder, value, proof)

    def test_pid_errors_multivalue_empty_success_stderr_and_timeout_remain_failed(self):
        for result in [(2, b'', b''), (1, b'41\n', b''), (1, b'', b'error'),
                       (0, b'', b''), (0, b'41 42\n', b''), (0, b'0\n', b''),
                       (0, b'41\n', b'warning'), (None, b'partial', b'timeout')]:
            with self.subTest(result=result), self.assertRaises(runner.JourneyError):
                self.run_phase([result])
            self.assertEqual(self.phase()['status'], 'FAILED')
            self.assertEqual(len(self.phase()['observations'][0]['commands']), 1)
            self.assertIsNone(self.recorder.deadline)

    def test_unknown_ambiguous_and_failed_foreground_stop_without_extra_commands(self):
        for result in [(0, b'topResumedActivity=other.app/.Activity\n', b''),
                       (0, b'no resumed component\n', b''),
                       (0, ('topResumedActivity=' + observed.HOME + '\n'
                            + 'topResumedActivity=' + observed.PERMISSION_ACTIVITY + '\n').encode(), b''),
                       (1, b'', b''), (0, b'', b'error')]:
            queue = home(); queue[1] = result
            with self.subTest(result=result), self.assertRaises(runner.JourneyError):
                self.run_phase(queue)
            self.assertEqual(len(self.phase()['observations'][0]['commands']), 2)
            self.assertEqual(len(self.recorder.queue), 1)

    def test_observation_limit_and_time_budget_fail_with_all_attempts_preserved(self):
        with self.assertRaisesRegex(runner.JourneyError, 'limit exhausted'):
            self.run_phase([(1, b'', b'')] * 16)
        self.assertEqual(len(self.phase()['observations']), 16)
        self.assertEqual(len(self.phase()['gaps']), 15)
        with self.assertRaisesRegex(runner.JourneyError, 'deadline expired'):
            self.run_phase(home() * 5, duration=4.0)
        self.assertEqual(self.phase()['status'], 'FAILED')

    def test_post_input_wait_and_exact_boundary_are_required(self):
        self.clock['now'] = 101.99
        with self.assertRaisesRegex(runner.JourneyError, 'fixed post-input wait'):
            self.run_phase(home())
        self.assertEqual(self.phase()['observations'], [])
        wrong = self.boundary(); wrong['to'] = 'home'
        with self.assertRaises(runner.JourneyError):
            ready._boundary(self.folder, {'label': 'original'}, wrong,
                            {'name': 'notification-request', 'owner': runner.PERMISSION}, proof)

    def test_rehashed_phase_state_order_deadline_and_first_sequence_mutations_fail(self):
        value = self.run_phase([(1, b'', b'')] + home() * 5)
        changes = [
            lambda p: p.update(status='FAILED'),
            lambda p: p['policy'].update(max_seconds=11),
            lambda p: p.update(finished_monotonic=p['started_monotonic'] + 11, seconds=11),
            lambda p: p['observations'][0]['observation'].update(state='HOME_WITH_SAME_PID'),
            lambda p: p['observations'][1].update(index=0),
            lambda p: p['observations'][1]['commands'].reverse(),
            lambda p: p['observations'][1]['commands'][0].update(timeout_seconds=11),
            lambda p: p['observations'][1]['commands'][0].update(started_monotonic=0),
            lambda p: p['gaps'][0].update(requested_seconds=0.1),
            lambda p: p['gaps'][0].update(finished_monotonic=p['gaps'][0]['started_monotonic']),
            lambda p: p.update(accepted_sequence=[2, 4]),
            lambda p: p.update(ready_pid='99'),
        ]
        for change in changes:
            bad = copy.deepcopy(value); change(bad)
            with self.subTest(change=change), self.assertRaises(runner.JourneyError):
                ready.verify_phase(self.folder, bad, proof)
        early = copy.deepcopy(value)
        early['observations'] = early['observations'][:3]; early['gaps'] = early['gaps'][:2]
        early['accepted_sequence'] = [1, 2]
        with self.assertRaises(runner.JourneyError): ready.verify_phase(self.folder, early, proof)
        extra = copy.deepcopy(value)
        last = copy.deepcopy(extra['observations'][-1]); last['index'] += 1
        extra['observations'].append(last); extra['gaps'].append(copy.deepcopy(extra['gaps'][-1]))
        with self.assertRaises(runner.JourneyError): ready.verify_phase(self.folder, extra, proof)

    def test_raw_output_tampering_is_detected_and_rehashed_wrong_output_still_fails(self):
        value = self.run_phase(home() * 5)
        item = value['observations'][0]['commands'][0]['stdout']
        (self.folder / item['path']).write_bytes(b'41 42\n')
        with self.assertRaises(ValueError): ready.verify_phase(self.folder, value, proof)
        item.update(bytes=6, sha256=hashlib.sha256(b'41 42\n').hexdigest())
        with self.assertRaises(runner.JourneyError): ready.verify_phase(self.folder, value, proof)


def shift_times(value, threshold, delta):
    if isinstance(value, dict):
        for key, item in value.items():
            if key.endswith('_monotonic') and isinstance(item, (int, float)) and item >= threshold:
                value[key] += delta
            else:
                shift_times(item, threshold, delta)
    elif isinstance(value, list):
        for item in value: shift_times(item, threshold, delta)


def command_records(value):
    if isinstance(value, dict):
        if {'returncode', 'stdout', 'stderr'} <= set(value):
            yield value
        else:
            for item in value.values(): yield from command_records(item)
    elif isinstance(value, list):
        for item in value: yield from command_records(item)


class ReadinessReportControls(unittest.TestCase):
    def setUp(self):
        context = day.configured_plan(); context.__enter__()
        self.addCleanup(context.__exit__, None, None, None)
        self.fixture = ThirteenFixture(); self.addCleanup(self.fixture.close)
        self.folder, self.report = self.fixture.folder, self.fixture.report

    def add_phases(self):
        ledger = []
        for run in self.report['runs']:
            transition = run['transitions'][4]
            cutoff = transition['command']['finished_monotonic'] + 0.01
            shift_times(run, cutoff, 5)
            for reference in self.report['capture_events']:
                if reference['path'].startswith(run['label'] + '-'):
                    value = json.loads(proof.artifact(self.folder, reference)); shift_times(value, cutoff, 5)
                    reference.update(self.fixture.put(reference['path'], json.dumps(value).encode()))
            reference = transition['process_handoff']
            handoff = json.loads(proof.artifact(self.folder, reference)); shift_times(handoff, cutoff, 5)
            reference.update(self.fixture.put(reference['path'], json.dumps(handoff).encode()))
            old = proof.artifact(self.folder, transition['preinput_artifacts']['pid']).decode().strip()
            pid = proof.artifact(self.folder, run['screens'][5]['artifacts']['pid_first']).decode().strip()
            clock = {'now': transition['command']['finished_monotonic'] + 2.25}
            recorder = FakeRecorder(self.folder, [(1, b'', b'')] + home(pid) * 5, clock, run['label'] + '-readiness')
            def sleep(seconds): clock['now'] += seconds
            with patch.object(ready.time, 'monotonic', side_effect=lambda: clock['now']), \
                    patch.object(ready.time, 'sleep', side_effect=sleep):
                ready.observe(recorder, run, transition, run['screens'][4])
            ledger += recorder.log
            for source in (run, handoff):
                for index, command in enumerate(command_records(source)):
                    row = copy.deepcopy(command)
                    row.setdefault('started_monotonic', (990 if run['label'] == 'original' else 1990) + index * 0.01)
                    row.setdefault('finished_monotonic', row['started_monotonic'] + 0.005)
                    ledger.append(row)
        self.report.update(schema=ready.REPORT_SCHEMA, notification_readiness_policy=copy.deepcopy(ready.POLICY),
                           commands=sorted(ledger, key=lambda row: row['started_monotonic']))

    def edit_phase(self, edit, update_ledger=False):
        transition = self.report['runs'][1]['transitions'][4]
        reference = transition[ready.REFERENCE_KEY]
        phase = json.loads(proof.artifact(self.folder, reference))
        old = [copy.deepcopy(command) for row in phase['observations'] for command in row['commands']]
        edit(phase)
        if update_ledger:
            new = [command for row in phase['observations'] for command in row['commands']]
            for a, b in zip(old, new):
                for index, command in enumerate(self.report['commands']):
                    if command == a: self.report['commands'][index] = copy.deepcopy(b)
        reference.update(self.fixture.put(reference['path'], json.dumps(phase).encode()))

    def test_complete_synthetic_pair_requires_readiness_and_keeps_thirteen_screen_scope(self):
        self.add_phases()
        result = self.fixture.result()
        self.assertTrue(result['journey_equal'], result)
        self.assertEqual(len(result['notification_readiness_observations']), 2)
        self.assertEqual(len(result['screens']), 13)
        self.assertFalse(result['full_runtime_1_to_1_established'])
        self.assertFalse(result['crash_free_run_established'])
        self.assertFalse(result['trigger_configuration_confirmed'])

    def test_older_schema_unchanged_and_mixed_new_evidence_rejected(self):
        original = self.fixture.result()
        self.assertTrue(original['journey_equal'], original)
        self.report[ready.POLICY_KEY] = copy.deepcopy(ready.POLICY)
        self.assertFalse(self.fixture.result()['journey_equal'])
        del self.report[ready.POLICY_KEY]
        self.report['runs'][0]['transitions'][4][ready.REFERENCE_KEY] = {'path': 'missing'}
        self.assertFalse(self.fixture.result()['journey_equal'])

    def test_missing_policy_missing_phase_and_schema_downgrade_fail(self):
        self.add_phases()
        for field in ('policy', 'phase', 'schema'):
            with self.subTest(field=field):
                value = copy.deepcopy(self.report)
                if field == 'policy': del value[ready.POLICY_KEY]
                elif field == 'phase': del value['runs'][1]['transitions'][4][ready.REFERENCE_KEY]
                else: value['schema'] = 3
                self.assertFalse(runner.compare(self.folder, value, proof)['journey_equal'])

    def test_wrong_boundary_run_pid_and_pre_capture_timing_fail(self):
        self.add_phases()
        reference = copy.deepcopy(self.report['runs'][1]['transitions'][4][ready.REFERENCE_KEY])
        original = proof.artifact(self.folder, reference)
        for change in [lambda p: p.update(label='original-notification-readiness'),
                       lambda p: p.update(old_pid='999'), lambda p: p.update(ready_pid='999'),
                       lambda p: shift_times(p, 0, -4), lambda p: shift_times(p, 0, 4)]:
            self.edit_phase(change, update_ledger=True)
            self.assertFalse(self.fixture.result()['journey_equal'])
            current = self.report['runs'][1]['transitions'][4][ready.REFERENCE_KEY]
            current.update(self.fixture.put(current['path'], original))

    def test_missing_duplicate_changed_or_interleaved_global_command_is_rejected(self):
        self.add_phases()
        original = copy.deepcopy(self.report['commands'])
        phase = json.loads(proof.artifact(self.folder, self.report['runs'][1]['transitions'][4][ready.REFERENCE_KEY]))
        command = phase['observations'][0]['commands'][0]
        index = self.report['commands'].index(command)
        for change in ('missing', 'duplicate', 'changed', 'interleaved'):
            self.report['commands'] = copy.deepcopy(original)
            if change == 'missing': del self.report['commands'][index]
            elif change == 'duplicate': self.report['commands'].insert(index, copy.deepcopy(command))
            elif change == 'changed': self.report['commands'][index]['argv'] = ['shell', 'input tap 2 2']
            else: self.report['commands'].insert(index + 1, copy.deepcopy(original[0]))
            with self.subTest(change=change), self.assertRaises(runner.JourneyError):
                ready.verify_report(self.folder, self.report, proof)

    def test_rehashed_readiness_output_cannot_alias_another_evidence_file(self):
        self.add_phases()
        foreign = self.report['runs'][1]['screens'][5]['artifacts']['pid_first']
        def alias(phase):
            command = phase['observations'][1]['commands'][0]
            path = self.folder / command['stdout']['path']
            path.unlink(); os.link(self.folder / foreign['path'], path)
            command['stdout'].update(bytes=foreign['bytes'], sha256=foreign['sha256'])
        self.edit_phase(alias, update_ledger=True)
        with self.assertRaisesRegex(runner.JourneyError, 'reused a command artifact'):
            ready.verify_report(self.folder, self.report, proof)


if __name__ == '__main__':
    unittest.main()
