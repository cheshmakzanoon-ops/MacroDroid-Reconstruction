"""Adversarial observation chronology controls; every capture here is synthetic."""
from __future__ import annotations

import copy
import json
import unittest

import editor_journey as runner
import favourite_info_journey as favourite
import trigger_category_journey as category
from test_observed_journey import ObservedFixture, proof
from test_trigger_category_journey import TwelveFixture


class CaptureChronologyControls(unittest.TestCase):
    def fixture(self, length):
        context = favourite.configured_plan() if length == 10 else category.configured_plan()
        context.__enter__()
        self.addCleanup(context.__exit__, None, None, None)
        fixture = ObservedFixture() if length == 10 else TwelveFixture()
        self.addCleanup(fixture.close)
        return fixture

    def replace_event(self, fixture, shot, event):
        previous = shot['settling']
        updated = fixture.put(previous['path'], json.dumps(event).encode())
        shot['settling'] = updated
        fixture.report['capture_events'] = [updated if item['path'] == previous['path'] else item
                                            for item in fixture.report['capture_events']]

    def test_genuine_synthetic_ten_and_twelve_sequences_keep_finite_scope(self):
        for length in (10, 12):
            with self.subTest(length=length):
                fixture = self.fixture(length)
                result = fixture.result()
                self.assertTrue(result['journey_equal'], result)
                self.assertFalse(result['full_runtime_1_to_1_established'])
                self.doCleanups()

    def test_deleted_actual_terminal_frames_cannot_be_replaced_by_prior_capture(self):
        for length in (10, 12):
            with self.subTest(length=length):
                fixture = self.fixture(length)
                removed = []
                for run in fixture.report['runs']:
                    previous, terminal = run['screens'][-2:]
                    path = terminal['settling']['path']
                    event = json.loads(proof.artifact(fixture.folder, terminal['settling']))
                    names = {item['path'] for frame in event['attempts'] for item in frame['artifacts'].values()} | {path}
                    for name in names:
                        (fixture.folder / name).unlink()
                        removed.append(name)
                    fixture.report['capture_events'] = [item for item in fixture.report['capture_events'] if item['path'] != path]
                    substitute = copy.deepcopy(previous)
                    substitute['name'] = terminal['name']
                    run['screens'][-1] = substitute
                self.assertEqual(len(removed), 26)
                result = fixture.result()
                self.assertFalse(result['journey_equal'], result)
                self.assertIn('Accepted acquisition ledger reused', result['reason'])
                self.doCleanups()

    def test_new_ledger_paths_cannot_reuse_earlier_raw_frame_artifacts(self):
        fixture = self.fixture(12)
        for run in fixture.report['runs']:
            prior, terminal = run['screens'][-2:]
            prior_event = json.loads(proof.artifact(fixture.folder, prior['settling']))
            self.replace_event(fixture, terminal, prior_event)
            for key in ('artifacts', 'sample_interval_seconds', 'observation', 'owner'):
                terminal[key] = copy.deepcopy(prior[key])
        result = fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertIn('reused an artifact', result['reason'])

    def test_independent_terminal_files_with_pre_input_times_are_rejected(self):
        fixture = self.fixture(12)
        for run in fixture.report['runs']:
            terminal = run['screens'][-1]
            event = json.loads(proof.artifact(fixture.folder, terminal['settling']))
            shift = 10.0
            for key in ('started_monotonic', 'finished_monotonic'):
                event[key] -= shift
            for frame in event['attempts']:
                for key in ('started_monotonic', 'finished_monotonic'):
                    frame['observation'][key] -= shift
            terminal['observation'] = copy.deepcopy(event['attempts'][-1]['observation'])
            self.replace_event(fixture, terminal, event)
        result = fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertIn('Result acquisition started before', result['reason'])

    def test_earlier_first_attempt_cannot_hide_behind_a_post_input_accepted_frame(self):
        fixture = self.fixture(12)
        shot = fixture.candidate()['screens'][-1]
        transition = fixture.candidate()['transitions'][-1]
        event = json.loads(proof.artifact(fixture.folder, shot['settling']))
        event['started_monotonic'] = transition['command']['started_monotonic'] - 0.1
        event['seconds'] = event['finished_monotonic'] - event['started_monotonic']
        self.replace_event(fixture, shot, event)
        result = fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertIn('Result acquisition started before', result['reason'])

    def test_input_finish_is_finite_ordered_and_before_result_acquisition(self):
        for value in (True, float('nan'), float('inf'), -1.0, 10000.0):
            with self.subTest(value=value):
                fixture = self.fixture(12)
                fixture.candidate()['transitions'][-1]['command']['finished_monotonic'] = value
                result = fixture.result()
                self.assertFalse(result['journey_equal'], result)
                self.doCleanups()

    def test_initial_capture_requires_successful_ordered_launch(self):
        for fault in ('late', 'missing', 'wrong-command', 'timeout'):
            with self.subTest(fault=fault):
                fixture = self.fixture(10)
                command = fixture.candidate()['launch']
                if fault == 'late':
                    command['started_monotonic'] = command['finished_monotonic'] = 9000.0
                elif fault == 'missing':
                    del command['finished_monotonic']
                elif fault == 'wrong-command':
                    command['argv'] = ['shell', 'am start -W -n other.package/.Activity']
                else:
                    command['timed_out'] = True
                self.assertFalse(fixture.result()['journey_equal'])
                self.doCleanups()

    def test_unselected_successful_ledger_cannot_remain_in_completed_report(self):
        fixture = self.fixture(10)
        event = proof.artifact(fixture.folder, fixture.candidate()['screens'][-1]['settling'])
        fixture.report['capture_events'].append(fixture.put('candidate-unselected-settling.json', event))
        result = fixture.result()
        self.assertFalse(result['journey_equal'], result)
        self.assertIn('Unbound successful acquisition', result['reason'])

    def test_global_late_preinput_reuse_cannot_be_hidden_by_alias_or_command_copy(self):
        for fault in ('preinput-copy', 'preinput-alias', 'command-copy'):
            with self.subTest(fault=fault):
                fixture = self.fixture(12)
                earlier, later = fixture.candidate()['transitions'][-3], fixture.candidate()['transitions'][-1]
                if fault.startswith('preinput'):
                    later['preinput_artifacts']['pid'] = copy.deepcopy(earlier['preinput_artifacts']['pid'])
                    if fault == 'preinput-alias':
                        name = later['preinput_artifacts']['pid']['path']
                        # The run prefix remains valid, while normalized identity
                        # still resolves to the already claimed earlier file.
                        alias_dir = fixture.folder / 'candidate-alias'
                        alias_dir.mkdir()
                        later['preinput_artifacts']['pid']['path'] = 'candidate-alias/../' + name
                else:
                    later['preinput_commands']['pid']['stdout'] = copy.deepcopy(earlier['preinput_commands']['pid']['stdout'])
                result = fixture.result()
                self.assertFalse(result['journey_equal'], result)
                self.assertIn('reused an artifact', result['reason'])
                self.doCleanups()


if __name__ == '__main__':
    unittest.main()
