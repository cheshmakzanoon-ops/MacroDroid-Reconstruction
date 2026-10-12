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
        for run in self.report['runs']:
            for index in range(self.start, len(self.plan)):
                shot = run['screens'][index]
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
                'foreground': self.command(run, name+'-foreground', ['dumpsys','activity','activities'], self.home())}
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
            return {'returncode':0,'argv':['shell',shlex.join(argv)]},values[tuple(argv)],b''
        recorder.shell=shell
        with patch.object(session.EvidenceRecorder,'snapshot',return_value=shot):
            actual=recorder.snapshot('original-home',runner.PACKAGE)
        session.checked_identity(self.root,run,actual,self.proof)
        self.assertEqual(len(commands),4)
    def test_non_endpoint_does_not_collect_identity(self):
        recorder=object.__new__(session.SessionRecorder)
        with patch.object(session.EvidenceRecorder,'snapshot',return_value={'ordinary':True}):
            self.assertEqual(recorder.snapshot('original-action-catalog',runner.PACKAGE),{'ordinary':True})


if __name__=='__main__':
    unittest.main()
