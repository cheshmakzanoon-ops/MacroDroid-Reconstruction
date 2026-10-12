"""Synthetic verifier tests. These do not execute Android or establish app parity."""
import copy
import json
from pathlib import Path
import shlex
import struct
import sys
import tempfile
import unittest
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'project'))
import android_compare as proof
import editor_journey as journey


def png(value=1):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
    return proof.PNG_MAGIC + chunk(b'IHDR', struct.pack('>IIBBBBB', 4, 4, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress((b'\x00' + bytes([value, 32, 48, 255]) * 4) * 4)) + chunk(b'IEND', b'')


def xml(index):
    name, owner, required, _ = journey.PLAN[index]
    selectors = [required]
    if index + 1 < len(journey.PLAN):
        action = journey.PLAN[index + 1][3]
        if isinstance(action, dict) and action != required:
            selectors.append(action)
    return ('<hierarchy>' + ''.join('<node package="' + owner + '" enabled="true" clickable="true" bounds="[0,0][4,4]" ' + ' '.join(k + '="' + v + '"' for k, v in selector.items()) + '/>' for selector in selectors) + '</hierarchy>').encode()


class JourneyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        env = {'serial': 'emulator-5560', 'display_size': '4x4', 'display_density': 'synthetic',
               **{p: 'synthetic' for p in journey.PROPERTIES},
               **{namespace + ':' + name: '0' for namespace, name in journey.SETTINGS}}
        env.update({'ro.build.version.sdk': '35', 'ro.kernel.qemu': '1', 'ro.product.cpu.abilist': 'x86_64,arm64-v8a'})
        self.report = {'schema': 1, 'status': 'RECORDED_NOT_PARITY', 'plan_sha256': journey.fingerprint(journey.PLAN), 'runs': []}
        for label, digest in [('original', proof.ORIGINAL_SHA256), ('candidate', '2' * 64)]:
            run = {'label': label, 'status': 'COMPLETE', 'apk_sha256': digest,
                   'environment': env.copy(), 'environment_after': env.copy(), 'screens': [], 'transitions': []}
            for key, data in [('absence', b''), ('install', b'Success\n'),
                              ('installed_path', b'package:/data/app/test/base.apk\n'),
                              ('installed_checksum', (digest + '  /data/app/test/base.apk\n').encode()),
                              ('launch', b'Status: ok\n')]:
                run[key] = self.command(label + '-' + key, data)
            run['absence']['returncode'] = 1
            for index, (name, owner, required, action) in enumerate(journey.PLAN):
                run['screens'].append(self.snapshot(label + '-' + name, index))
                if index:
                    before = self.snapshot(label + '-before-' + name, index - 1)
                    argv = ['input', 'keyevent', '4'] if action == 'BACK' else ['input', 'tap', '2', '2']
                    command = self.command(label + '-input-' + name, b'')
                    command['argv'] = ['shell', shlex.join(argv)]
                    run['transitions'].append({'to': name, 'action': action, 'before': before,
                                               'precondition_age_seconds': 0.25, 'command': command})
            self.report['runs'].append(run)
    def tearDown(self):
        self.temp.cleanup()
    def put(self, name, data):
        (self.root / name).write_bytes(data)
        return {'path': name, 'bytes': len(data), 'sha256': proof.sha(data)}
    def command(self, name, data):
        return {'returncode': 0, 'stdout': self.put(name + '-out', data), 'stderr': self.put(name + '-err', b'')}
    def snapshot(self, name, index):
        owner = journey.PLAN[index][1]
        return {'name': journey.PLAN[index][0], 'owner': owner, 'sample_interval_seconds': 1.1,
                'artifacts': {key: self.put(name + '-' + key, data) for key, data in {
                    'hierarchy': xml(index), 'screenshot': png(index + 1), 'pid_first': b'31', 'pid_final': b'31',
                    'foreground': ('topResumedActivity=' + owner + '/.Activity\n').encode()}.items()}}
    def result(self):
        return journey.compare(self.root, self.report, proof)
    def candidate(self):
        return self.report['runs'][1]
    def test_complete_equal_synthetic_journey_is_narrowly_scoped(self):
        result = self.result()
        self.assertTrue(result['journey_equal'], result)
        self.assertEqual(len(result['screens']), 13)
        self.assertFalse(result['full_runtime_1_to_1_established'])
        self.assertFalse(result['macros_saved'])
        self.assertFalse(result['macros_executed'])
    def test_each_screen_pixel_change_is_detected(self):
        for i in range(len(journey.PLAN)):
            with self.subTest(screen=i):
                screen = self.candidate()['screens'][i]
                old = screen['artifacts']['screenshot']
                screen['artifacts']['screenshot'] = self.put('candidate-changed-pixel', png(200))
                self.assertFalse(self.result()['journey_equal'])
                screen['artifacts']['screenshot'] = old
    def test_structural_faults_fail_closed(self):
        mutations = [
            lambda r: r.update(schema=2), lambda r: r.update(status='INCOMPLETE'),
            lambda r: r.update(plan_sha256='x'), lambda r: r['runs'].pop(),
            lambda r: r['runs'][1].update(status='FAILED'),
            lambda r: r['runs'][1].update(apk_sha256=proof.ORIGINAL_SHA256),
            lambda r: r['runs'][0].update(apk_sha256='1' * 64),
            lambda r: r['runs'][1]['environment'].update(serial='other'),
            lambda r: r['runs'][1]['environment_after'].update(serial='other'),
            lambda r: r['runs'][1]['screens'].pop(),
            lambda r: r['runs'][1]['transitions'].pop(),
            lambda r: r['runs'][1]['install'].update(returncode=1),
            lambda r: r['runs'][1]['launch'].update(returncode=True),
            lambda r: r['runs'][1]['screens'][0].update(name='wrong'),
            lambda r: r['runs'][1]['screens'][0].update(owner='other'),
            lambda r: r['runs'][1]['screens'][0].update(sample_interval_seconds=float('nan')),
            lambda r: r['runs'][1]['transitions'][0].update(precondition_age_seconds=20),
            lambda r: r['runs'][1]['transitions'][0].update(precondition_age_seconds=True),
            lambda r: r['runs'][1]['transitions'][0].update(to='wrong'),
            lambda r: r['runs'][1]['transitions'][0].update(action='BACK'),
            lambda r: r['runs'][1]['transitions'][0]['command'].update(argv=['shell', 'input tap 0 0']),
            lambda r: r['runs'][1]['transitions'][0]['command'].update(returncode=1),
            lambda r: r['runs'][1]['transitions'][0].update(before=r['runs'][1]['screens'][0]),
            lambda r: r['runs'][1]['screens'][0].update(artifacts=r['runs'][0]['screens'][0]['artifacts']),
        ]
        original = copy.deepcopy(self.report)
        for i, mutate in enumerate(mutations):
            with self.subTest(fault=i):
                self.report = copy.deepcopy(original)
                mutate(self.report)
                self.assertFalse(self.result()['journey_equal'])
    def test_changed_artifact_bytes_are_rejected(self):
        a = self.candidate()['screens'][0]['artifacts']['hierarchy']
        (self.root / a['path']).write_bytes(b'changed')
        self.assertIn('changed', self.result()['reason'])
    def test_wrong_installed_apk_is_rejected(self):
        self.candidate()['installed_checksum']['stdout'] = self.put('candidate-wrong-hash', b'bad  /data/app/test/base.apk\n')
        self.assertFalse(self.result()['journey_equal'])
    def test_changed_pid_is_rejected(self):
        self.candidate()['screens'][-1]['artifacts']['pid_final'] = self.put('candidate-wrong-pid', b'32')
        self.assertFalse(self.result()['journey_equal'])
    def test_input_stderr_is_rejected(self):
        self.candidate()['transitions'][0]['command']['stderr'] = self.put('candidate-input-error', b'error')
        self.assertFalse(self.result()['journey_equal'])
    def test_historical_resumed_app_does_not_override_actual_top_app(self):
        self.assertFalse(journey.resumed('topResumedActivity=other/.Activity\nmResumedActivity: ' + journey.PACKAGE + '/.Activity', journey.PACKAGE))
    def test_selector_uses_clickable_ancestor(self):
        data = ('<hierarchy><node package="' + journey.PACKAGE + '" enabled="true" clickable="true" bounds="[0,0][4,4]"><node package="' + journey.PACKAGE + '" enabled="true" text="Add Macro"/></node></hierarchy>').encode()
        self.assertEqual(journey.target(data, journey.PACKAGE, {'text': 'Add Macro'}, 4, 4), [2, 2])
    def test_disabled_ambiguous_and_out_of_screen_targets_rejected(self):
        base = xml(0)
        for value in [base.replace(b'enabled="true"', b'enabled="false"'), base.replace(b'[0,0][4,4]', b'[0,0][5,5]'),
                      base.replace(b'</hierarchy>', base.split(b'<hierarchy>')[1]), base.replace(b'com.arlosoft.macrodroid', b'other')]:
            with self.subTest(value=value):
                with self.assertRaises(journey.JourneyError):
                    journey.target(value, journey.PACKAGE, journey.NEXT, 4, 4)
    def test_xml_declarations_are_rejected(self):
        with self.assertRaises(journey.JourneyError):
            journey.tree(b'<!DOCTYPE hierarchy><hierarchy/>', journey.PACKAGE)

if __name__ == '__main__':
    unittest.main()
