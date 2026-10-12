"""Synthetic adversarial fixtures only; these tests do not execute Android."""
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zlib

import android_compare as cold
import android_intro as intro


def png(value):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
    pixels = bytes([value, 32, 48, 255]) * 4
    raw = (b'\x00' + pixels) * 4
    return cold.PNG_MAGIC + chunk(b'IHDR', struct.pack('>IIBBBBB', 4, 4, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b'')


def hierarchy(page, button='enabled="true" clickable="true" bounds="[2,2][4,4]"'):
    title = intro.EXPECTED_TITLES[page - 1] if type(page) is int and 1 <= page <= 4 else 'UNKNOWN'
    return (f'<hierarchy><node package="{cold.PACKAGE}" resource-id="{cold.PACKAGE}:id/titleText" text="{title}"/>'
            f'<node package="{cold.PACKAGE}" text="Intro {page}"/>'
            f'<node package="{cold.PACKAGE}" resource-id="{intro.NEXT_ID}" {button}/></hierarchy>').encode()


class IntroComparisonTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        environment = {key: 'synthetic-fixture' for key in ['serial', 'ro.product.cpu.abilist', 'ro.build.version.sdk',
                      'ro.build.fingerprint', 'ro.kernel.qemu', 'persist.sys.locale', 'persist.sys.timezone',
                      'display_size', 'display_density', 'font_scale']}
        environment['ro.product.cpu.abilist'] = 'arm64-v8a'
        self.report = {'schema_version': 3, 'status': 'CAPTURES_RECORDED_NOT_PARITY',
                       'intro_pages_requested': True, 'requested_capture_complete': True, 'apk_preflight': [], 'runs': []}
        for label, digest in [('original', cold.ORIGINAL_SHA256), ('candidate', '2' * 64)]:
            self.report['apk_preflight'].append({'label': label, 'apk_sha256': digest, 'bytes': 1,
                'metadata': {'package': cold.PACKAGE, 'version_code': '896700008', 'version_name': '5.67.8', 'min_sdk': 23, 'target_sdk': 36}})
            run = {'label': label, 'apk_sha256': digest, 'environment': environment.copy(),
                   'component': cold.PACKAGE + '/.intro.IntroActivity', 'status': 'APP_CAPTURE_RECORDED',
                   'android_runtime_executed': True, 'sample_interval_seconds': 2, 'launch_exit': 0,
                   'artifacts': {}, 'intro_sequence': {'status': 'INTRO_PAGES_RECORDED', 'pages': [], 'transitions': []}}
            run['install'] = self.command(label + '-install', 0, b'Performing Push Install\nSuccess\n', b'')
            run['after_uninstall'] = self.command(label + '-absent', 1, b'', b'')
            run['installed_apk'] = {'sha256': digest,
                'package_path': self.command(label + '-installed-path', 0, b'package:/data/app/synthetic/base.apk\n', b''),
                'checksum': self.command(label + '-installed-checksum', 0, (digest + '  /data/app/synthetic/base.apk\n').encode(), b'')}
            for kind, data in {'launch': b'Status: ok\n', 'pid_first': b'31', 'pid_second': b'31', 'pid_final': b'31',
                               'foreground': b'mResumedActivity: com.arlosoft.macrodroid/.intro.IntroActivity\n',
                               'hierarchy': hierarchy(1), 'screenshot': png(1)}.items():
                run['artifacts'][kind] = self.put(label + '-' + kind, data)
            for number in range(1, 5):
                if number == 1:
                    artifacts = {key: run['artifacts'][key] for key in ['pid_first', 'pid_final', 'foreground', 'hierarchy', 'screenshot']}
                else:
                    artifacts = {key: self.put(f'{label}-page-{number}-{key}', data) for key, data in {
                        'pid_first': b'31', 'pid_final': b'31', 'foreground': b'mResumedActivity: com.arlosoft.macrodroid/.intro.IntroActivity\n',
                        'hierarchy': hierarchy(number), 'screenshot': png(number)}.items()}
                run['intro_sequence']['pages'].append({'page': number, 'sample_interval_seconds': 2, 'artifacts': artifacts})
                if number < 4:
                    before = {'hierarchy': self.put(f'{label}-before-{number}-hierarchy', hierarchy(number)),
                              'pid': self.put(f'{label}-before-{number}-pid', b'31'),
                              'foreground': self.put(f'{label}-before-{number}-foreground', b'topResumedActivity=com.arlosoft.macrodroid/.intro.IntroActivity\n')}
                    run['intro_sequence']['transitions'].append({'from_page': number, 'to_page': number + 1,
                        'selector': intro.NEXT_ID, 'coordinates': [3, 3], 'precondition_hierarchy': before['hierarchy'],
                        'precondition_artifacts': before, 'precondition_age_seconds': 0.5,
                        'shell_argv': ['input', 'tap', '3', '3'], 'command': {'returncode': 0,
                            'stdout': self.put(f'{label}-tap-{number}-stdout', b''),
                            'stderr': self.put(f'{label}-tap-{number}-stderr', b'')}})
            self.report['runs'].append(run)

    def tearDown(self):
        self.temp.cleanup()

    def put(self, name, data):
        (self.root / name).write_bytes(data)
        return {'path': name, 'bytes': len(data), 'sha256': cold.sha(data)}

    def command(self, name, code, stdout, stderr):
        return {'returncode': code, 'stdout': self.put(name + '-stdout', stdout), 'stderr': self.put(name + '-stderr', stderr)}

    def result(self):
        (self.root / 'result.json').write_text(json.dumps(self.report))
        return intro.compare_intro(self.root)

    def candidate(self):
        return self.report['runs'][1]['intro_sequence']

    def test_equal_synthetic_sequence_has_only_intro_scope(self):
        result = self.result()
        self.assertTrue(result['intro_sequence_equal'])
        self.assertEqual([page['changed_pixels'] for page in result['pages']], [0, 0, 0, 0])
        self.assertFalse(result['feature_parity_established'])
        self.assertFalse(result['full_runtime_1_to_1_established'])

    def test_later_page_pixels_are_compared(self):
        self.candidate()['pages'][3]['artifacts']['screenshot'] = self.put('changed-last-page', png(5))
        result = self.result()
        self.assertFalse(result['intro_sequence_equal'])
        self.assertEqual(result['pages'][3]['changed_pixels'], 16)

    def test_later_page_text_is_compared(self):
        self.candidate()['pages'][3]['artifacts']['hierarchy'] = self.put('changed-page-text', hierarchy('different'))
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_repeated_page_cannot_count_as_progression(self):
        self.candidate()['pages'][3]['artifacts']['hierarchy'] = self.candidate()['pages'][0]['artifacts']['hierarchy']
        self.assertIn('repeats a page', self.result()['reason'])

    def test_missing_page_is_rejected(self):
        self.candidate()['pages'].pop()
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_incomplete_intro_keeps_completed_cold_capture_evidence(self):
        self.report['status'] = 'COLD_CAPTURES_RECORDED_INTRO_INCOMPLETE'
        self.report['requested_capture_complete'] = False
        self.candidate()['status'] = 'INTRO_CAPTURE_FAILED'
        self.candidate()['pages'].pop()
        result = self.result()
        self.assertTrue(result['android_runtime_executed'])
        self.assertTrue(result['cold_launch']['cold_launch_capture_equal'])
        self.assertFalse(result['complete_intro_sequences_observed'])
        self.assertFalse(result['intro_sequence_equal'])

    def test_intro_incomplete_status_cannot_override_incomplete_cold_run(self):
        self.report['status'] = 'COLD_CAPTURES_RECORDED_INTRO_INCOMPLETE'
        self.report['runs'][1]['status'] = 'CAPTURE_FAILED'
        result = self.result()
        self.assertFalse(result['android_runtime_executed'])
        self.assertFalse(result['intro_sequence_equal'])

    def test_incomplete_top_status_cannot_be_overridden_by_page_records(self):
        self.report['status'] = 'COLD_CAPTURES_RECORDED_INTRO_INCOMPLETE'
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_false_requested_completion_cannot_be_overridden_by_page_records(self):
        self.report['requested_capture_complete'] = False
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_old_hierarchy_with_extra_metadata_is_still_reused(self):
        previous = self.candidate()['pages'][0]['artifacts']['hierarchy'].copy()
        previous['extra'] = 'cannot make an old file fresh'
        transition = self.candidate()['transitions'][0]
        transition['precondition_artifacts']['hierarchy'] = previous
        transition['precondition_hierarchy'] = previous.copy()
        self.assertIn('reused an old UI capture', self.result()['reason'])

    def test_coordinate_must_come_from_observed_button(self):
        self.candidate()['transitions'][1]['coordinates'] = [0, 0]
        self.assertIn('observed Next button', self.result()['reason'])

    def test_unrelated_selector_is_rejected(self):
        self.candidate()['transitions'][0]['selector'] = cold.PACKAGE + ':id/button_skip'
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_stale_ui_precondition_is_rejected(self):
        self.candidate()['transitions'][1]['precondition_hierarchy'] = self.candidate()['pages'][0]['artifacts']['hierarchy']
        self.assertIn('recorded UI precondition', self.result()['reason'])

    def test_shell_coordinates_must_match_selected_target(self):
        self.candidate()['transitions'][0]['shell_argv'] = ['input', 'tap', '0', '0']
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_failed_tap_is_rejected(self):
        self.candidate()['transitions'][1]['command']['returncode'] = 1
        self.assertIn('tap command', self.result()['reason'])

    def test_command_diagnostics_are_not_silently_accepted(self):
        self.candidate()['transitions'][0]['command']['stdout'] = self.put('tap-error', b'Error: invalid input\n')
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_tampered_transition_evidence_is_rejected(self):
        (self.root / self.candidate()['transitions'][1]['command']['stdout']['path']).write_bytes(b'changed')
        self.assertIn('artifact was changed', self.result()['reason'])

    def test_first_page_must_reference_cold_capture(self):
        self.candidate()['pages'][0]['artifacts']['screenshot'] = self.put('unrelated-first-page', png(1))
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_process_restart_on_later_page_is_rejected(self):
        self.candidate()['pages'][3]['artifacts']['pid_final'] = self.put('restarted-pid', b'32')
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_live_samples_require_time_separation(self):
        self.candidate()['pages'][2]['sample_interval_seconds'] = 0
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_permission_dialog_is_not_an_intro_page(self):
        self.candidate()['pages'][2]['artifacts']['foreground'] = self.put('permission-front', b'mResumedActivity: com.android.permissioncontroller/.Grant\n')
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_sequence_must_be_explicitly_requested(self):
        self.report['intro_pages_requested'] = False
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_failed_install_cannot_be_overridden_by_valid_pictures(self):
        self.report['runs'][1]['install'] = self.command('failed-install', 1, b'Failure [INSTALL_FAILED]\n', b'')
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_still_installed_package_cannot_pass_absence(self):
        self.report['runs'][1]['after_uninstall'] = self.command('present-after-removal', 0, b'package:/data/app/old/base.apk\n', b'')
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_transport_error_cannot_pass_as_package_absence(self):
        self.report['runs'][1]['after_uninstall'] = self.command('transport-error', 1, b'', b'adb: device offline\n')
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_installed_apk_must_have_the_input_hash(self):
        self.report['runs'][1]['installed_apk']['checksum'] = self.command('wrong-installed-apk', 0, ('3' * 64 + '  /data/app/synthetic/base.apk\n').encode(), b'')
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_nonfinite_or_boolean_sample_intervals_are_rejected(self):
        for value in [float('nan'), float('inf'), -float('inf'), True]:
            with self.subTest(value=value):
                self.candidate()['pages'][2]['sample_interval_seconds'] = value
                self.assertFalse(self.result()['intro_sequence_equal'])
        self.candidate()['pages'][2]['sample_interval_seconds'] = 2
        self.report['runs'][1]['sample_interval_seconds'] = float('nan')
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_null_sequence_is_rejected_without_crashing(self):
        self.report['runs'][1]['intro_sequence'] = None
        result = self.result()
        self.assertFalse(result['intro_sequence_equal'])
        self.assertTrue(result['android_runtime_executed'])
        self.assertFalse(result['complete_intro_sequences_observed'])

    def test_arbitrary_changed_text_cannot_identify_an_intro_page(self):
        for run in self.report['runs']:
            run['intro_sequence']['pages'][3]['artifacts']['hierarchy'] = self.put(run['label'] + '-unknown-page', hierarchy('unknown'))
        self.assertIn('expected English intro page', self.result()['reason'])

    def test_first_page_pid_evidence_is_bound_to_cold_capture(self):
        self.candidate()['pages'][0]['artifacts']['pid_final'] = self.put('unrelated-first-pid', b'31')
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_preinput_process_restart_is_rejected(self):
        self.candidate()['transitions'][1]['precondition_artifacts']['pid'] = self.put('restarted-before-input', b'32')
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_preinput_foreground_uses_top_resumed_activity(self):
        self.candidate()['transitions'][1]['precondition_artifacts']['foreground'] = self.put('other-top-before-input',
            b'topResumedActivity=com.android.permissioncontroller/.Grant\n mResumedActivity: com.arlosoft.macrodroid/.intro.IntroActivity\n')
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_preinput_ui_change_is_rejected(self):
        self.candidate()['transitions'][1]['precondition_artifacts']['hierarchy'] = self.put('changed-before-input', hierarchy('changed'))
        self.assertFalse(self.result()['intro_sequence_equal'])

    def test_expired_and_nonfinite_preconditions_are_rejected(self):
        for value in [11, float('nan'), float('inf'), True]:
            with self.subTest(value=value):
                self.candidate()['transitions'][1]['precondition_age_seconds'] = value
                self.assertFalse(self.result()['intro_sequence_equal'])


class NextSelectorTests(unittest.TestCase):
    def test_rejects_disabled_nonclickable_and_offscreen_targets(self):
        for attributes in ['enabled="false" clickable="true" bounds="[2,2][4,4]"',
                           'enabled="true" clickable="false" bounds="[2,2][4,4]"',
                           'enabled="true" clickable="true" bounds="[2,2][5,4]"',
                           'enabled="true" clickable="true" bounds="[4,2][2,4]"']:
            with self.subTest(attributes=attributes), self.assertRaises(cold.CaptureError):
                intro.next_target(hierarchy(1, attributes), 4, 4)

    def test_ambiguous_next_button_is_rejected(self):
        data = hierarchy(1).replace(b'</hierarchy>', hierarchy(1).split(b'<hierarchy>')[1])
        with self.assertRaises(cold.CaptureError):
            intro.next_target(data, 4, 4)

    def test_foreground_requires_the_actual_intro_activity(self):
        self.assertTrue(intro.intro_foreground('mResumedActivity: com.arlosoft.macrodroid/com.arlosoft.macrodroid.intro.IntroActivity\n'))
        self.assertFalse(intro.intro_foreground('mResumedActivity: com.arlosoft.macrodroid/.intro.IntroActivityFake\n'))

    def test_explicit_other_top_activity_overrides_resumed_app(self):
        text = 'topResumedActivity=com.android.settings/.Main\nmResumedActivity: com.arlosoft.macrodroid/.intro.IntroActivity\n'
        self.assertFalse(intro.intro_foreground(text))
        self.assertFalse(cold.foreground_ok(text))


if __name__ == '__main__':
    unittest.main()
