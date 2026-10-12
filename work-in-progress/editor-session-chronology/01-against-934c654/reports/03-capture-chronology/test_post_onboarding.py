"""Synthetic evidence/recorder controls; no Android calls are made here."""
import copy
import json
import shlex
import struct
import zlib
import unittest
from unittest.mock import patch
import editor_journey as runner
import supplied_reference_journey as adapter
import test_editor_journey as fixtures
import post_onboarding as session


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.plan = adapter.load_plan()
        with adapter.configured_plan():
            self.fixture = fixtures.JourneyTests()
            self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        self.root = self.fixture.root
        self.proof = fixtures.proof
        self.report = self.fixture.report
        self.report['plan'] = copy.deepcopy(self.plan)
        self.start = [s[0] for s in self.plan].index('home')
        for run_number, run in enumerate(self.report['runs']):
            for index in range(self.start, len(self.plan)):
                shot = run['screens'][index]
                capture_start = (run_number + 1) * 1000 + index * 10 + 0.2
                shot['session_observation'] = {'schema': 1, 'started_monotonic': capture_start,
                                               'finished_monotonic': capture_start + 1.2}
                for key in ('pid_first', 'pid_final'):
                    shot['artifacts'][key] = self.put(run, f'{index}-session-{key}', b'44')
                if index == self.start:
                    shot['artifacts']['foreground'] = self.put(run, 'home-resumed', self.home())
                if index > self.start:
                    t = run['transitions'][index - 1]
                    for key in ('pid_first', 'pid_final'):
                        t['before']['artifacts'][key] = self.put(run, f'{index}-before-{key}', b'44')
                    t['preinput_artifacts']['pid'] = self.put(run, f'{index}-immediate-pid', b'44')
                if index in (self.start, len(self.plan) - 1):
                    shot['session_identity'] = self.identity(run, index)
                    for command_number, key in enumerate(('package_path', 'checksum', 'pid', 'foreground')):
                        start = (run_number + 1) * 1000 + index * 10 + 2 + command_number / 10
                        shot['session_identity'][key].update(
                            timed_out=False, started_monotonic=start,
                            finished_monotonic=start + 0.05, timeout_seconds=120)
                if index > self.start:
                    start = (run_number + 1) * 1000 + index * 10
                    transition = run['transitions'][index - 1]
                    transition['precondition_age_seconds'] = 2.5
                    transition['before']['session_observation'] = {
                        'schema': 1, 'started_monotonic': start - 2.4,
                        'finished_monotonic': start - 1.2}
                    transition['command'].update(
                        timed_out=False, started_monotonic=start,
                        finished_monotonic=start + 0.05, timeout_seconds=120)
    def put(self, run, name, data):
        return self.fixture.put(run['label'] + '-' + name, data)
    def home(self):
        return ('topResumedActivity=' + runner.PACKAGE + '/' + session.HOME_CLASS).encode()
    def command(self, run, name, argv, data):
        return {'argv': ['shell', shlex.join(argv)], 'returncode': 0,
                'stdout': self.put(run, name + '-out', data), 'stderr': self.put(run, name + '-err', b'')}
    def identity(self, run, index):
        path = '/data/app/test/base.apk'
        name = f'{index}-identity'
        return {'environment': run['environment'].copy(),
                'package_path': self.command(run, name+'-path', ['pm','path',runner.PACKAGE], ('package:'+path+'\n').encode()),
                'checksum': self.command(run, name+'-sha', ['sha256sum',path], (run['apk_sha256']+'  '+path+'\n').encode()),
                'pid': self.command(run, name+'-pid', ['pidof',runner.PACKAGE], b'44'),
                'foreground': self.command(run, name+'-foreground', ['dumpsys','activity','activities'],
                    (self.root / run['screens'][index]['artifacts']['foreground']['path']).read_bytes())}
    def result(self):
        return session.compare_session(self.root, self.report, self.plan, self.proof)
    def test_exact_session_does_not_turn_shared_startup_restart_into_a_pass(self):
        result = self.result()
        self.assertTrue(result['editor_session_equal'], result)
        self.assertEqual(len(result['screens']), len(self.plan)-self.start)
        self.assertFalse(result['startup_parity_established'])
        self.assertFalse(result['full_runtime_1_to_1_established'])
        with adapter.configured_plan():
            self.assertFalse(runner.compare(self.root, self.report, self.proof)['journey_equal'])
    def test_missing_endpoint_identity_fails_closed(self):
        del self.report['runs'][1]['screens'][-1]['session_identity']
        self.assertFalse(self.result()['editor_session_equal'])
    def test_each_pixel_defect_remains_visible(self):
        for i in range(self.start,len(self.plan)):
            with self.subTest(screen=i):
                shot=self.report['runs'][1]['screens'][i]; old=shot['artifacts']['screenshot']
                shot['artifacts']['screenshot']=self.put(self.report['runs'][1],f'{i}-pixel-fault',fixtures.png(200))
                self.assertFalse(self.result()['editor_session_equal'])
                shot['artifacts']['screenshot']=old
    def test_adversarial_session_mutations(self):
        mutations = [
            lambda r: r.update(plan_sha256='bad'),
            lambda r: r['runs'][1].update(status='FAILED'),
            lambda r: r['runs'][1]['screens'].pop(),
            lambda r: r['runs'][1]['environment_after'].update(serial='other'),
            lambda r: r['runs'][1]['screens'][self.start]['session_identity']['environment'].update(serial='other'),
            lambda r: r['runs'][1]['screens'][self.start]['session_identity']['checksum'].update(returncode=1),
            lambda r: r['runs'][1]['screens'][self.start]['session_identity']['checksum'].update(argv=['shell','echo fake']),
            lambda r: r['runs'][1]['screens'][self.start].update(owner='other'),
            lambda r: r['runs'][1]['screens'][self.start]['session_identity'].update(checksum=r['runs'][0]['screens'][self.start]['session_identity']['checksum']),
            lambda r: r['runs'][1]['transitions'][self.start].update(precondition_age_seconds=16),
            lambda r: r['runs'][1]['transitions'][self.start].update(precondition_age_seconds=float('nan')),
            lambda r: r['runs'][1]['transitions'][self.start].update(precondition_age_seconds=True),
            lambda r: r['runs'][1]['transitions'][self.start].pop('preinput_artifacts'),
            lambda r: r['runs'][1]['transitions'][self.start]['command'].update(argv=['shell','input tap 0 0']),
            lambda r: r['runs'][1]['transitions'][self.start]['command'].update(returncode=True),
            lambda r: r['runs'][1]['transitions'][self.start].update(before=r['runs'][1]['screens'][self.start]),
        ]
        original=copy.deepcopy(self.report)
        for index,mutation in enumerate(mutations):
            with self.subTest(fault=index):
                self.report=copy.deepcopy(original);mutation(self.report)
                self.assertFalse(self.result()['editor_session_equal'])
    def test_pid_restart_inside_editor_is_rejected(self):
        run=self.report['runs'][1]
        run['transitions'][self.start]['preinput_artifacts']['pid']=self.put(run,'wrong-pid',b'45')
        self.assertFalse(self.result()['editor_session_equal'])
    def test_wrong_installed_endpoint_hash_is_rejected(self):
        run=self.report['runs'][1]
        run['screens'][self.start]['session_identity']['checksum']['stdout']=self.put(run,'wrong-sha',('f'*64+'  /data/app/test/base.apk\n').encode())
        self.assertFalse(self.result()['editor_session_equal'])
    def test_wrong_home_activity_is_rejected(self):
        run=self.report['runs'][1]
        run['screens'][self.start]['artifacts']['foreground']=self.put(run,'wrong-home',('topResumedActivity='+runner.PACKAGE+'/.Other').encode())
        self.assertFalse(self.result()['editor_session_equal'])
    def test_modified_artifact_bytes_fail(self):
        record=self.report['runs'][1]['screens'][self.start]['artifacts']['hierarchy']
        (self.root/record['path']).write_bytes(b'invalid')
        self.assertFalse(self.result()['editor_session_equal'])
    def test_invalid_compressed_pixels_return_rejection(self):
        def chunk(kind, data):
            return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
        picture = self.proof.PNG_MAGIC + chunk(b'IHDR', struct.pack('>IIBBBBB',4,4,8,6,0,0,0)) + chunk(b'IDAT',b'not-zlib') + chunk(b'IEND',b'')
        run=self.report['runs'][1]
        run['screens'][self.start]['artifacts']['screenshot']=self.put(run,'invalid-deflate',picture)
        self.assertFalse(self.result()['editor_session_equal'])

    def test_duplicate_screenshot_path_is_rejected(self):
        run=self.report['runs'][1]
        run['screens'][self.start+1]['artifacts']['screenshot']=run['screens'][self.start]['artifacts']['screenshot']
        self.assertFalse(self.result()['editor_session_equal'])
    def test_recorder_captures_real_identity_commands_at_home(self):
        run=self.report['runs'][0]; shot=copy.deepcopy(run['screens'][self.start]);shot.pop('session_identity')
        recorder=object.__new__(session.SessionRecorder)
        recorder.folder=self.root;recorder.proof=self.proof;recorder.save=self.fixture.put
        recorder.environment=lambda:run['environment'].copy()
        commands=[]
        def shell(argv):
            commands.append(argv)
            values={('pm','path',runner.PACKAGE):b'package:/data/app/test/base.apk\n',
                    ('sha256sum','/data/app/test/base.apk'):(run['apk_sha256']+'  /data/app/test/base.apk\n').encode(),
                    ('pidof',runner.PACKAGE):b'44',('dumpsys','activity','activities'):self.home()}
            return {'returncode':0,'argv':['shell',shlex.join(argv)], 'timed_out':False,
                    'started_monotonic':float(len(commands) + 2), 'finished_monotonic':len(commands)+2.05,
                    'timeout_seconds':120},values[tuple(argv)],b''
        recorder.shell=shell
        with patch.object(session.EvidenceRecorder,'snapshot',return_value=shot), patch.object(
                session.time, 'monotonic', side_effect=[0.0, 2.0]):
            actual=recorder.snapshot('original-home',runner.PACKAGE)
        session.checked_identity(self.root,run,actual,self.proof)
        self.assertEqual(len(commands),4)
    def test_non_endpoint_does_not_collect_identity(self):
        recorder=object.__new__(session.SessionRecorder)
        recorder.save = self.fixture.put
        with patch.object(session.EvidenceRecorder,'snapshot',return_value={'ordinary':True}), patch.object(
                session.time, 'monotonic', side_effect=[1.0, 3.0]):
            result = recorder.snapshot('original-action-catalog',runner.PACKAGE)
            self.assertEqual(result, {'ordinary': True, 'session_observation': {
                'schema': 1, 'started_monotonic': 1.0, 'finished_monotonic': 3.0}})
            self.assertNotIn('session_identity', result)

    def test_final_identity_cannot_reuse_home_after_all_final_outputs_are_deleted(self):
        run = self.report['runs'][1]
        initial, final = run['screens'][self.start], run['screens'][-1]
        for key in ('package_path', 'checksum', 'pid', 'foreground'):
            for stream in ('stdout', 'stderr'):
                (self.root / final['session_identity'][key][stream]['path']).unlink()
        final['session_identity'] = copy.deepcopy(initial['session_identity'])
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('Reused session artifact', result['reason'])

    def test_final_identity_cannot_reuse_resolved_aliases_of_home_outputs(self):
        run = self.report['runs'][1]
        initial, final = run['screens'][self.start], run['screens'][-1]
        (self.root / 'candidate-endpoint-alias').mkdir()
        for key in ('package_path', 'checksum', 'pid', 'foreground'):
            for stream in ('stdout', 'stderr'):
                record = initial['session_identity'][key][stream]
                fresh = self.fixture.put('candidate-endpoint-alias/' + key + '-' + stream,
                                         (self.root / record['path']).read_bytes())
                initial['session_identity'][key][stream] = fresh
                (self.root / final['session_identity'][key][stream]['path']).unlink()
        final['session_identity'] = copy.deepcopy(initial['session_identity'])
        for key in ('package_path', 'checksum', 'pid', 'foreground'):
            for stream in ('stdout', 'stderr'):
                row = final['session_identity'][key][stream]
                row['path'] = row['path'].replace('candidate-endpoint-alias/', 'candidate-endpoint-alias/./')
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('Reused session artifact', result['reason'])

    def test_later_input_cannot_reuse_earlier_live_files_after_own_files_are_deleted(self):
        run = self.report['runs'][1]
        first, later = run['transitions'][self.start:self.start + 2]
        for record in later['preinput_artifacts'].values():
            (self.root / record['path']).unlink()
        later['preinput_artifacts'] = copy.deepcopy(first['preinput_artifacts'])
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('Reused session artifact', result['reason'])

    def test_later_input_cannot_reuse_earlier_live_files_through_resolved_aliases(self):
        run = self.report['runs'][1]
        first, later = run['transitions'][self.start:self.start + 2]
        (self.root / 'candidate-live-alias').mkdir()
        for key, record in list(first['preinput_artifacts'].items()):
            fresh = self.fixture.put('candidate-live-alias/' + key, (self.root / record['path']).read_bytes())
            first['preinput_artifacts'][key] = fresh
            (self.root / later['preinput_artifacts'][key]['path']).unlink()
            later['preinput_artifacts'][key] = {**fresh, 'path': 'candidate-live-alias/./' + key}
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('Reused session artifact', result['reason'])

    def test_snapshot_pid_evidence_cannot_be_reused_from_an_earlier_screen(self):
        run = self.report['runs'][1]
        run['screens'][self.start + 2]['artifacts']['pid_final'] = copy.deepcopy(
            run['screens'][self.start]['artifacts']['pid_final'])
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('Reused session artifact', result['reason'])

    def test_before_input_pid_cannot_reuse_a_previous_input_observation(self):
        run = self.report['runs'][1]
        first, later = run['transitions'][self.start:self.start + 2]
        later['before']['artifacts']['pid_final'] = copy.deepcopy(first['preinput_artifacts']['pid'])
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('Reused session artifact', result['reason'])

    def test_input_command_streams_cannot_reuse_prior_command_outputs(self):
        run = self.report['runs'][1]
        first, later = run['transitions'][self.start:self.start + 2]
        later['command']['stdout'] = copy.deepcopy(first['command']['stdout'])
        later['command']['stderr'] = copy.deepcopy(first['command']['stderr'])
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('Reused session artifact', result['reason'])

    def test_final_identity_requires_times_after_the_final_input_even_with_distinct_files(self):
        run = self.report['runs'][1]
        initial, final = run['screens'][self.start]['session_identity'], run['screens'][-1]['session_identity']
        for key in ('package_path', 'checksum', 'pid', 'foreground'):
            for stamp in ('started_monotonic', 'finished_monotonic'):
                final[key][stamp] = initial[key][stamp]
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('endpoint command precedes its captured observation', result['reason'])

    def test_endpoint_command_order_is_verified(self):
        identity = self.report['runs'][1]['screens'][-1]['session_identity']
        first, last = identity['package_path'], identity['foreground']
        for stamp in ('started_monotonic', 'finished_monotonic'):
            first[stamp], last[stamp] = last[stamp], first[stamp]
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('endpoint commands are out of order', result['reason'])

    def test_first_input_acquisition_must_follow_home_identity(self):
        run = self.report['runs'][1]
        transition = run['transitions'][self.start]
        start = run['screens'][self.start]['session_identity']['foreground']['finished_monotonic'] + 0.1
        transition['command'].update(started_monotonic=start, finished_monotonic=start + 0.05)
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('input acquisition precedes', result['reason'])

    def test_later_input_time_cannot_precede_an_earlier_input(self):
        run = self.report['runs'][1]
        first, later = run['transitions'][self.start:self.start + 2]
        for stamp in ('started_monotonic', 'finished_monotonic'):
            later['command'][stamp] = first['command'][stamp]
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('input acquisition precedes', result['reason'])

    def test_incomplete_nonfinite_or_timed_out_session_commands_reject(self):
        original = copy.deepcopy(self.report)
        mutations = [
            lambda item: item.pop('started_monotonic'),
            lambda item: item.update(started_monotonic=float('nan')),
            lambda item: item.update(finished_monotonic=float('inf')),
            lambda item: item.update(started_monotonic=True),
            lambda item: item.update(started_monotonic=-1),
            lambda item: item.update(finished_monotonic=item['started_monotonic'] - 1),
            lambda item: item.update(timeout_seconds=0),
            lambda item: item.update(timeout_seconds=False),
            lambda item: item.update(timeout_seconds=0.001),
            lambda item: item.update(timed_out=True),
            lambda item: item.pop('timed_out'),
        ]
        for location in ('endpoint', 'input'):
            for index, mutation in enumerate(mutations):
                with self.subTest(location=location, mutation=index):
                    self.report = copy.deepcopy(original)
                    run = self.report['runs'][1]
                    item = (run['screens'][-1]['session_identity']['pid'] if location == 'endpoint'
                            else run['transitions'][self.start]['command'])
                    mutation(item)
                    result = self.result()
                    self.assertFalse(result['editor_session_equal'])
                    self.assertIn('session command timing', result['reason'])

    def test_endpoint_foreground_must_equal_its_captured_component(self):
        run = self.report['runs'][1]
        item = run['screens'][-1]['session_identity']['foreground']
        item['stdout'] = self.put(run, 'different-final-component', self.home())
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('captured foreground component', result['reason'])

    def test_distinct_fresh_files_may_have_identical_bytes_and_unshared_dot_aliases(self):
        run = self.report['runs'][1]
        (self.root / 'candidate-fresh-only').mkdir()
        shot = run['screens'][self.start + 2]
        record = shot['artifacts']['screenshot']
        fresh = self.fixture.put('candidate-fresh-only/picture.png', (self.root / record['path']).read_bytes())
        shot['artifacts']['screenshot'] = {**fresh, 'path': 'candidate-fresh-only/./picture.png'}
        result = self.result()
        self.assertTrue(result['editor_session_equal'], result)

    def test_endpoint_component_accepts_equivalent_abbreviated_activity_not_another_activity(self):
        run = self.report['runs'][1]
        item = run['screens'][-1]['session_identity']['foreground']
        item['stdout'] = self.put(run, 'fully-qualified-final-component',
                                 ('topResumedActivity=' + runner.PACKAGE + '/' + runner.PACKAGE + '.Activity').encode())
        result = self.result()
        self.assertTrue(result['editor_session_equal'], result)

    def test_session_result_capture_cannot_precede_the_input_even_with_distinct_files(self):
        run = self.report['runs'][1]
        result_shot = run['screens'][self.start + 1]
        result_shot['session_observation'] = copy.deepcopy(run['screens'][self.start]['session_observation'])
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('result capture began before its input finished', result['reason'])

    def test_final_result_cannot_reuse_an_earlier_capture_window_with_its_own_files(self):
        run = self.report['runs'][1]
        run['screens'][-1]['session_observation'] = copy.deepcopy(run['screens'][-2]['session_observation'])
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('result capture began before its input finished', result['reason'])

    def test_preinput_capture_must_follow_the_prior_result_observation(self):
        run = self.report['runs'][1]
        before = run['transitions'][self.start + 1]['before']
        before['session_observation'] = copy.deepcopy(run['screens'][self.start]['session_observation'])
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('pre-input capture timing is stale or out of order', result['reason'])

    def test_preinput_capture_cannot_extend_past_the_input_start(self):
        run = self.report['runs'][1]
        transition = run['transitions'][self.start]
        transition['before']['session_observation']['finished_monotonic'] = transition['command']['started_monotonic'] + 1
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('pre-input capture timing is stale or out of order', result['reason'])

    def test_endpoint_identity_cannot_precede_its_own_capture_even_after_all_inputs(self):
        run = self.report['runs'][1]
        identity = run['screens'][-1]['session_identity']
        final_input_finish = run['transitions'][-1]['command']['finished_monotonic']
        for index, key in enumerate(('package_path', 'checksum', 'pid', 'foreground')):
            start = final_input_finish + index / 10
            identity[key].update(started_monotonic=start, finished_monotonic=start + 0.05)
        result = self.result()
        self.assertFalse(result['editor_session_equal'])
        self.assertIn('endpoint command precedes its captured observation', result['reason'])

    def test_missing_or_malformed_capture_intervals_are_not_inferred(self):
        original = copy.deepcopy(self.report)
        mutations = [
            lambda shot: shot.pop('session_observation'),
            lambda shot: shot['session_observation'].update(schema=2),
            lambda shot: shot['session_observation'].update(started_monotonic=float('nan')),
            lambda shot: shot['session_observation'].update(finished_monotonic=float('inf')),
            lambda shot: shot['session_observation'].update(started_monotonic=True),
            lambda shot: shot['session_observation'].update(started_monotonic=-1),
            lambda shot: shot['session_observation'].update(finished_monotonic=shot['session_observation']['started_monotonic'] + 0.1),
        ]
        for index, mutation in enumerate(mutations):
            with self.subTest(mutation=index):
                self.report = copy.deepcopy(original)
                mutation(self.report['runs'][1]['screens'][-1])
                result = self.result()
                self.assertFalse(result['editor_session_equal'])


if __name__=='__main__':
    unittest.main()
