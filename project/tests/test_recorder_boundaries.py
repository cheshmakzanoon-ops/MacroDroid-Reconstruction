"""Host-only recorder failure cases; mocked ADB never installs an application."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import android_acceptance as recorder
from test_intro_capture import hierarchy, png


class RecorderBoundaryTests(unittest.TestCase):
    def test_slow_xml_fetch_expires_before_any_intro_tap(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pair = []
            for label in ['original', 'candidate']:
                path = root / (label + '.apk')
                path.write_bytes(('synthetic-' + label).encode())
                pair.append({'label': label, 'path': str(path), 'apk_sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
            clock = [0.0]
            active = [-1]
            xml_reads = [0]
            taps = []
            def sleep(seconds):
                clock[0] += seconds
            def command(argv, **kwargs):
                text = ' '.join(map(str, argv))
                code, stdout, stderr = 0, '', ''
                if 'install' in argv:
                    active[0] += 1
                    xml_reads[0] = 0
                    stdout = 'Success\n'
                elif 'uninstall' in argv:
                    active[0] = -1 if active[0] < 0 else active[0]
                    stdout = 'Success\n'
                elif 'get-state' in argv:
                    stdout = 'device\n'
                elif 'getprop ro.product.cpu.abilist' in text:
                    stdout = 'arm64-v8a\n'
                elif 'getprop ro.kernel.qemu' in text:
                    stdout = '1\n'
                elif 'pm path ' in text:
                    # The uninstall immediately precedes the absence query.
                    previous = calls[-2] if len(calls) > 1 else []
                    if 'uninstall' in previous:
                        code = 1
                    else:
                        stdout = 'package:/data/app/synthetic/base.apk\n'
                elif 'sha256sum ' in text:
                    stdout = pair[active[0]]['apk_sha256'] + '  /data/app/synthetic/base.apk\n'
                elif 'resolve-activity' in text:
                    stdout = recorder.PACKAGE + '/.intro.IntroActivity\n'
                elif 'am start -W' in text:
                    stdout = 'Status: ok\n'
                elif 'pidof ' in text:
                    stdout = '31\n'
                elif 'dumpsys activity activities' in text:
                    stdout = 'topResumedActivity=' + recorder.PACKAGE + '/.intro.IntroActivity\n'
                elif 'exec-out' in argv and 'cat' in argv:
                    xml_reads[0] += 1
                    if xml_reads[0] == 2:
                        clock[0] += 11  # XML retrieval succeeds after the precondition expires.
                    stdout = hierarchy(1)
                elif 'exec-out' in argv and 'screencap' in argv:
                    stdout = png(1)
                elif 'input tap' in text:
                    taps.append(argv)
                elif 'getprop ' in text or 'settings get ' in text or 'wm ' in text:
                    stdout = 'synthetic\n'
                if kwargs.get('text') is False:
                    stdout = stdout.encode() if isinstance(stdout, str) else stdout
                    stderr = stderr.encode()
                return subprocess.CompletedProcess(argv, code, stdout, stderr)
            calls = []
            def tracked_command(argv, **kwargs):
                calls.append(argv)
                return command(argv, **kwargs)
            arguments = ['android_acceptance.py', '--serial', 'emulator-5560', '--original', pair[0]['path'],
                         '--candidate', pair[1]['path'], '--accept-package-data-removal', '--intro-pages',
                         '--output', str(root / 'capture')]
            with patch.object(sys, 'argv', arguments), patch('android_acceptance.shutil.which', return_value='/synthetic/adb'), \
                 patch('android_acceptance.subprocess.run', side_effect=tracked_command), \
                 patch('android_acceptance.prevalidate_pair', return_value=pair), \
                 patch('android_acceptance.time.monotonic', side_effect=lambda: clock[0]), \
                 patch('android_acceptance.time.sleep', side_effect=sleep), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(recorder.main(), 2)
            self.assertEqual(taps, [])
            result = json.loads((root / 'capture/result.json').read_text())
            self.assertEqual(result['status'], 'COLD_CAPTURES_RECORDED_INTRO_INCOMPLETE')
            self.assertFalse(result['requested_capture_complete'])
            for run in result['runs']:
                self.assertEqual(run['status'], 'APP_CAPTURE_RECORDED')
                self.assertEqual(run['intro_sequence']['status'], 'INTRO_CAPTURE_FAILED')
                self.assertIn('expired before input', run['intro_sequence']['reason'])
                self.assertEqual(run['intro_sequence']['transitions'][0]['precondition_age_seconds'], 11)

    def test_existing_capture_is_refused_before_device_work(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'result.json'
            previous = '{"status":"previous-capture"}\n'
            path.write_text(previous)
            with patch.object(sys, 'argv', ['android_acceptance.py', '--output', directory]), \
                 patch('android_acceptance.shutil.which', side_effect=AssertionError('Device lookup reached')), \
                 contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
                recorder.main()
            self.assertEqual(caught.exception.code, 2)
            self.assertEqual(path.read_text(), previous)

    def test_non_success_report_precedes_first_device_command(self):
        with tempfile.TemporaryDirectory() as directory:
            observed = []
            def command(argv, **kwargs):
                report = json.loads((Path(directory) / 'result.json').read_text())
                observed.append(report)
                raise OSError('Synthetic ADB transport failure')
            with patch.object(sys, 'argv', ['android_acceptance.py', '--serial', 'emulator-5560', '--output', directory]), \
                 patch('android_acceptance.shutil.which', return_value='/synthetic/adb'), \
                 patch('android_acceptance.subprocess.run', side_effect=command), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(recorder.main(), 2)
            self.assertEqual(len(observed), 1)
            self.assertEqual(observed[0]['status'], 'BLOCKED')
            self.assertEqual(observed[0]['schema_version'], 3)
            self.assertFalse(observed[0]['android_runtime_executed'])

    def test_package_query_error_prevents_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pair = []
            for label in ['original', 'candidate']:
                path = root / (label + '.apk')
                path.write_bytes(('synthetic-' + label).encode())
                pair.append({'label': label, 'path': str(path), 'apk_sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
            output = root / 'capture'
            installs = []
            def command(argv, **kwargs):
                text = ' '.join(map(str, argv))
                if 'install' in argv:
                    installs.append(argv)
                    raise AssertionError('Installation reached after failed absence check')
                if 'get-state' in argv:
                    code, stdout, stderr = 0, 'device\n', ''
                elif 'getprop ro.product.cpu.abilist' in text:
                    code, stdout, stderr = 0, 'arm64-v8a\n', ''
                elif 'getprop ro.kernel.qemu' in text:
                    code, stdout, stderr = 0, '1\n', ''
                elif 'pm path ' in text:
                    code, stdout, stderr = 1, '', 'adb: device offline\n'
                else:
                    code, stdout, stderr = 0, 'synthetic\n', ''
                return subprocess.CompletedProcess(argv, code, stdout, stderr)
            arguments = ['android_acceptance.py', '--serial', 'emulator-5560', '--original', pair[0]['path'],
                         '--candidate', pair[1]['path'], '--accept-package-data-removal', '--output', str(output)]
            with patch.object(sys, 'argv', arguments), patch('android_acceptance.shutil.which', return_value='/synthetic/adb'), \
                 patch('android_acceptance.subprocess.run', side_effect=command), \
                 patch('android_acceptance.prevalidate_pair', return_value=pair), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(recorder.main(), 2)
            self.assertEqual(installs, [])
            result = json.loads((output / 'result.json').read_text())
            self.assertEqual(result['status'], 'CAPTURE_INCOMPLETE')
            self.assertTrue(all('absence was not verified' in run['reason'] for run in result['runs']))
            self.assertFalse(result['android_runtime_executed'])


if __name__ == '__main__':
    unittest.main()
