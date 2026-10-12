"""Synthetic rejection tests; these fixtures do not execute Android."""
import copy
import json
import subprocess
import unittest

import android_compare as cold
import android_intro as intro
import android_post_intro as post
import test_intro_capture as fixture


PERMISSION = 'com.google.android.permissioncontroller'
PERMISSION_FRONT = ('topResumedActivity=' + PERMISSION + '/com.android.permissioncontroller.permission.ui.GrantPermissionsActivity\n').encode()
INTRO_FRONT = b'topResumedActivity=com.arlosoft.macrodroid/.intro.IntroActivity\n'


def final_hierarchy():
    return fixture.hierarchy(4).replace(b'clickable="true"', b'clickable="true" class="android.widget.ImageButton" content-desc="Next"')


def permission_hierarchy(message='Allow MacroDroid to send you notifications?'):
    return (f'<hierarchy><node package="{PERMISSION}" resource-id="{PERMISSION}:id/permission_message" text="{message}"/>'
            f'<node package="{PERMISSION}" resource-id="{PERMISSION}:id/permission_allow_button" text="Allow" enabled="true" clickable="true"/>'
            f'<node package="{PERMISSION}" resource-id="{PERMISSION}:id/permission_deny_button" text="Don’t allow" enabled="true" clickable="true"/></hierarchy>').encode()


class PostIntroFixture:
    def setUp(self):
        self.fixture = fixture.IntroComparisonTests()
        self.fixture.setUp()
        self.root = self.fixture.root
        self.report = self.fixture.report
        self.report.update(post_intro_requested=True, cold_intro_capture_complete=True)
        for run in self.report['runs']:
            label = run['label']
            final = run['intro_sequence']['pages'][-1]
            final['artifacts']['hierarchy'] = self.put(label + '-final-ui', final_hierarchy())
            before = {'hierarchy': self.put(label + '-completion-before-ui', final_hierarchy()),
                      'pid': self.put(label + '-completion-before-pid', b'31'),
                      'foreground': self.put(label + '-completion-before-front', INTRO_FRONT)}
            surface, _ = post.surface_state(permission_hierarchy(), PERMISSION_FRONT.decode())
            installed = {'sha256': run['apk_sha256']}
            for key in ['package_path', 'checksum']:
                old = run['installed_apk'][key]
                installed[key] = self.fixture.command(label + '-post-installed-' + key, old['returncode'],
                    cold.artifact(self.root, old['stdout']), cold.artifact(self.root, old['stderr']))
            run['post_intro'] = {'status': 'POST_INTRO_SURFACE_RECORDED', 'completion_input_count': 1,
                'permission_actions_taken': 0, 'sample_interval_seconds': 2,
                'environment_before': run['environment'].copy(), 'environment_after': run['environment'].copy(),
                'installed_apk_before_completion': installed,
                'precondition_artifacts': before,
                'completion_transition': {'from_page': 4, 'selector': intro.NEXT_ID, 'coordinates': [3, 3],
                    'precondition_hierarchy': before['hierarchy'], 'precondition_age_seconds': 0.5,
                    'shell_argv': ['input', 'tap', '3', '3'],
                    'command': self.fixture.command(label + '-completion-tap', 0, b'', b'')},
                'artifacts': {key: self.put(label + '-post-' + key, value) for key, value in {
                    'pid_first': b'31', 'pid_final': b'31', 'foreground': PERMISSION_FRONT,
                    'foreground_after': PERMISSION_FRONT, 'hierarchy': permission_hierarchy(),
                    'hierarchy_after': permission_hierarchy(), 'screenshot': fixture.png(5)}.items()},
                'surface': surface, 'screen_size': [4, 4]}

    def tearDown(self):
        self.fixture.tearDown()

    def put(self, name, data):
        return self.fixture.put(name, data)

    def candidate(self):
        return self.report['runs'][1]['post_intro']

    def result(self):
        (self.root / 'result.json').write_text(json.dumps(self.report))
        return post.compare_post_intro(self.root)


class PostIntroComparisonTests(PostIntroFixture, unittest.TestCase):
    def test_exact_synthetic_prompt_has_only_first_surface_scope(self):
        result = self.result()
        self.assertTrue(result['post_intro_surface_equal'])
        self.assertEqual(result['changed_pixels'], 0)
        self.assertFalse(result['home_feature_parity_established'])
        self.assertFalse(result['animation_parity_established'])
        self.assertFalse(result['full_runtime_1_to_1_established'])

    def test_landing_activity_can_be_observed_without_claiming_home_features(self):
        xml = f'<hierarchy><node package="{cold.PACKAGE}" text="Synthetic app dialog"/></hierarchy>'.encode()
        front = f'topResumedActivity={cold.PACKAGE}/.homescreen.NewHomeScreenActivity\n'.encode()
        for run in self.report['runs']:
            record = run['post_intro']
            for key in ['foreground', 'foreground_after']:
                record['artifacts'][key] = self.put(run['label'] + '-landing-' + key, front)
            for key in ['hierarchy', 'hierarchy_after']:
                record['artifacts'][key] = self.put(run['label'] + '-landing-' + key, xml)
            record['surface'] = post.surface_state(xml, front.decode())[0]
        result = self.result()
        self.assertTrue(result['post_intro_surface_equal'])
        self.assertEqual(result['surfaces'][0]['kind'], 'app_landing_surface')
        self.assertFalse(result['home_feature_parity_established'])

    def test_full_pixels_and_full_xml_attributes_are_compared(self):
        self.candidate()['artifacts']['screenshot'] = self.put('different-post-pixels', fixture.png(6))
        self.assertEqual(self.result()['changed_pixels'], 16)
        self.candidate()['artifacts']['screenshot'] = self.put('restored-post-pixels', fixture.png(5))
        changed = permission_hierarchy().replace(b'text="Allow"', b'text="Allow" focused="true"')
        for key in ['hierarchy', 'hierarchy_after']:
            self.candidate()['artifacts'][key] = self.put('changed-attribute-' + key, changed)
        result = self.result()
        self.assertEqual(result['changed_pixels'], 0)
        self.assertFalse(result['hierarchy_equal'])
        self.assertFalse(result['post_intro_surface_equal'])

    def test_unknown_foreground_and_other_permission_prompt_are_rejected(self):
        self.candidate()['artifacts']['foreground'] = self.put('browser-front', b'topResumedActivity=com.android.chrome/.Main\n')
        self.assertIn('Unexpected foreground', self.result()['reason'])
        self.candidate()['artifacts']['foreground'] = self.put('permission-front', PERMISSION_FRONT)
        self.candidate()['artifacts']['hierarchy'] = self.put('other-permission', permission_hierarchy('Allow MacroDroid to access your camera?'))
        self.assertIn('notification request', self.result()['reason'])

    def test_result_cannot_reuse_the_final_intro_hierarchy_as_fresh(self):
        old = self.report['runs'][1]['intro_sequence']['pages'][-1]['artifacts']['hierarchy'].copy()
        old['extra'] = 'metadata does not make this a new observation'
        self.candidate()['precondition_artifacts']['hierarchy'] = old
        self.candidate()['completion_transition']['precondition_hierarchy'] = old.copy()
        self.assertIn('reused an old hierarchy', self.result()['reason'])

    def test_precondition_must_identify_the_observed_constraints_button(self):
        original = final_hierarchy()
        for changed in [original.replace(b'CONSTRAINTS', b'ACTIONS'),
                        original.replace(b'clickable="true"', b'clickable="false"'),
                        original.replace(b'[2,2][4,4]', b'[2,2][5,5]'),
                        original.replace(b'content-desc="Next"', b'content-desc="Done"')]:
            with self.subTest(changed=changed):
                self.candidate()['precondition_artifacts']['hierarchy'] = self.put('wrong-final-precondition', changed)
                self.assertFalse(self.result()['post_intro_surface_equal'])

    def test_preinput_process_foreground_and_age_are_enforced(self):
        before = self.candidate()['precondition_artifacts']
        before['pid'] = self.put('changed-preinput-pid', b'32')
        self.assertFalse(self.result()['post_intro_surface_equal'])
        before['pid'] = self.put('restored-preinput-pid', b'31')
        before['foreground'] = self.put('permission-over-intro', PERMISSION_FRONT + INTRO_FRONT.replace(b'topResumedActivity', b'mResumedActivity'))
        self.assertFalse(self.result()['post_intro_surface_equal'])
        before['foreground'] = self.put('restored-preinput-front', INTRO_FRONT)
        for age in [11, float('nan'), float('inf'), True]:
            with self.subTest(age=age):
                self.candidate()['completion_transition']['precondition_age_seconds'] = age
                self.assertFalse(self.result()['post_intro_surface_equal'])

    def test_installed_identity_and_environment_cannot_change(self):
        self.candidate()['installed_apk_before_completion']['sha256'] = '3' * 64
        self.assertIn('Installed identity', self.result()['reason'])
        self.candidate()['installed_apk_before_completion']['sha256'] = '2' * 64
        self.candidate()['environment_after']['font_scale'] = '2'
        self.assertIn('environment changed', self.result()['reason'])

    def test_completion_identity_requires_a_new_device_observation(self):
        self.candidate()['installed_apk_before_completion'] = copy.deepcopy(self.report['runs'][1]['installed_apk'])
        self.assertIn('reuses the initial installed-APK', self.result()['reason'])

    def test_no_extra_input_or_permission_action_can_pass(self):
        record = self.candidate()
        for count in [0, 2, True]:
            with self.subTest(count=count):
                record['completion_input_count'] = count
                self.assertFalse(self.result()['post_intro_surface_equal'])
        record['completion_input_count'] = 1
        record['permission_actions_taken'] = 1
        self.assertFalse(self.result()['post_intro_surface_equal'])
        record['permission_actions_taken'] = 0
        record['completion_transition']['shell_argv'] = ['input', 'tap', '0', '0']
        self.assertFalse(self.result()['post_intro_surface_equal'])

    def test_tap_failure_and_silent_error_output_are_rejected(self):
        for code, output in [(1, b''), (0, b'Error: invalid tap\n')]:
            with self.subTest(code=code):
                self.candidate()['completion_transition']['command'] = self.fixture.command('bad-completion-tap', code, output, b'')
                self.assertFalse(self.result()['post_intro_surface_equal'])

    def test_surface_must_remain_stable_and_process_alive(self):
        self.candidate()['artifacts']['hierarchy_after'] = self.put('changed-after-ui', permission_hierarchy().replace(b'text="Allow"', b'text="Allow" selected="true"'))
        self.assertIn('surface identity changed', self.result()['reason'])
        self.candidate()['artifacts']['hierarchy_after'] = self.put('restored-after-ui', permission_hierarchy())
        self.candidate()['artifacts']['pid_final'] = self.put('changed-post-pid', b'32')
        self.assertFalse(self.result()['post_intro_surface_equal'])

    def test_surface_stability_requires_a_second_hierarchy_file(self):
        self.candidate()['artifacts']['hierarchy_after'] = self.candidate()['artifacts']['hierarchy'].copy()
        self.assertIn('reuses the initial hierarchy', self.result()['reason'])

    def test_failed_post_scope_keeps_real_cold_and_intro_checks_available(self):
        self.report['status'] = post.PARTIAL_STATUS
        self.report['requested_capture_complete'] = False
        self.candidate()['status'] = 'POST_INTRO_CAPTURE_FAILED'
        self.candidate()['artifacts'].pop('hierarchy_after')
        result = self.result()
        self.assertTrue(result['intro']['cold_launch']['cold_launch_capture_equal'])
        self.assertTrue(result['intro']['intro_sequence_equal'])
        self.assertFalse(result['post_intro_surface_equal'])
        self.report['cold_intro_capture_complete'] = False
        self.assertFalse(self.result()['intro']['intro_sequence_equal'])

    def test_post_status_never_overrides_an_incomplete_cold_run(self):
        self.report['status'] = post.PARTIAL_STATUS
        self.report['requested_capture_complete'] = False
        self.report['runs'][1]['status'] = 'CAPTURE_FAILED'
        self.assertFalse(self.result()['android_runtime_executed'])

    def test_tampered_artifact_cannot_pass(self):
        path = self.root / self.candidate()['artifacts']['screenshot']['path']
        path.write_bytes(fixture.png(9))
        self.assertIn('artifact was changed', self.result()['reason'])


class FakeClock:
    def __init__(self):
        self.now = 0.0
    def monotonic(self):
        return self.now
    def sleep(self, seconds):
        self.now += seconds


class PostIntroRecorderTests(PostIntroFixture, unittest.TestCase):
    """Exercise the actual input path with simulated ADB; not Android evidence."""
    def fake_io(self, *, fresh=None, resulting_front=PERMISSION_FRONT, resulting_xml=None, delay=0):
        clock = FakeClock()
        calls = []
        tapped = False
        fresh = fresh if fresh is not None else final_hierarchy()
        resulting_xml = resulting_xml if resulting_xml is not None else permission_hierarchy()
        def result(argv, value=b'', binary=False):
            return subprocess.CompletedProcess(argv, 0, value if binary else value.decode(), b'' if binary else '')
        def shell(argv, **kwargs):
            nonlocal tapped
            calls.append(argv)
            clock.now += delay
            if argv[:2] == ['pm', 'path']:
                return result(argv, b'package:/data/app/synthetic/base.apk\n')
            if argv[0] == 'sha256sum':
                return result(argv, ('2' * 64 + '  /data/app/synthetic/base.apk\n').encode())
            if argv[0] == 'pidof':
                return result(argv, b'31')
            if argv[0] == 'dumpsys':
                return result(argv, resulting_front if tapped else INTRO_FRONT)
            if argv[:2] == ['input', 'tap']:
                tapped = True
            return result(argv)
        def device(argv, **kwargs):
            calls.append(argv)
            if argv[:2] == ['exec-out', 'cat']:
                return result(argv, resulting_xml if tapped else fresh, binary=True)
            if argv[:2] == ['exec-out', 'screencap']:
                return result(argv, fixture.png(5), binary=True)
            raise AssertionError('Unexpected simulated ADB command: ' + repr(argv))
        def save(name, value):
            stdout = value.stdout.encode() if isinstance(value.stdout, str) else value.stdout
            stderr = value.stderr.encode() if isinstance(value.stderr, str) else value.stderr
            return self.fixture.command(name, value.returncode, stdout, stderr)
        def checked(name, value):
            return save(name, value)['stdout']
        io = post.CaptureIO(self.root, 10, shell, device, save, checked, self.put,
            lambda: self.report['runs'][1]['environment'].copy(), lambda: None)
        return io, clock, calls

    def test_actual_capture_path_issues_one_completion_input_and_no_more(self):
        io, clock, calls = self.fake_io()
        post.capture_after_intro(self.report['runs'][1], 'candidate', io, clock=clock)
        self.assertEqual([c for c in calls if c[0] == 'input'], [['input', 'tap', '3', '3']])
        self.assertEqual(self.candidate()['status'], 'POST_INTRO_SURFACE_RECORDED')
        self.assertEqual(self.candidate()['permission_actions_taken'], 0)
        self.assertTrue(self.result()['post_intro_surface_equal'])

    def test_changed_or_expired_precondition_issues_no_input(self):
        for kwargs in [{'fresh': final_hierarchy().replace(b'CONSTRAINTS', b'UNKNOWN')}, {'delay': 4}]:
            with self.subTest(kwargs=kwargs):
                io, clock, calls = self.fake_io(**kwargs)
                with self.assertRaises(cold.CaptureError):
                    post.capture_after_intro(self.report['runs'][1], 'candidate', io, clock=clock)
                self.assertEqual([c for c in calls if c[0] == 'input'], [])

    def test_unknown_surface_is_saved_without_further_input_or_loss_of_intro(self):
        old_cold = copy.deepcopy(self.report['runs'][1]['artifacts'])
        old_intro = copy.deepcopy(self.report['runs'][1]['intro_sequence'])
        io, clock, calls = self.fake_io(resulting_front=b'topResumedActivity=com.android.chrome/.Main\n')
        with self.assertRaisesRegex(cold.CaptureError, 'Unexpected foreground'):
            post.capture_after_intro(self.report['runs'][1], 'candidate', io, clock=clock)
        self.assertEqual([c for c in calls if c[0] == 'input'], [['input', 'tap', '3', '3']])
        for key in ['hierarchy', 'screenshot', 'foreground']:
            self.assertTrue((self.root / self.candidate()['artifacts'][key]['path']).is_file())
        self.assertEqual(self.report['runs'][1]['artifacts'], old_cold)
        self.assertEqual(self.report['runs'][1]['intro_sequence'], old_intro)


if __name__ == '__main__':
    unittest.main()
