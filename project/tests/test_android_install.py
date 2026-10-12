"""Regressions for real ADB transport banners and package-manager failures."""
import unittest

from android_acceptance import install_ok


class InstallStatusTests(unittest.TestCase):
    def test_accepts_success_with_adb_transport_output(self):
        for output in [
            'Success\n',
            'Performing Push Install\nSuccess\n',
            'Performing Streamed Install\r\nSuccess\r\n',
            'Performing Push Install\napp.apk: 1 file pushed, 0 skipped.\nSuccess\n\n',
        ]:
            with self.subTest(output=output):
                self.assertTrue(install_ok(0, output))

    def test_nonzero_exit_cannot_be_overridden_by_success_text(self):
        for code in [1, 2, 124, -15]:
            with self.subTest(code=code):
                self.assertFalse(install_ok(code, 'Performing Push Install\nSuccess\n'))

    def test_requires_exact_terminal_package_manager_success(self):
        for output in ['', 'Performing Push Install\n', 'Not Success\n',
                       'Successfully queued\n', 'Success\nInstalling\n']:
            with self.subTest(output=output):
                self.assertFalse(install_ok(0, output))

    def test_explicit_failure_in_either_stream_rejects_mixed_output(self):
        for diagnostic in ['Failure [INSTALL_FAILED_INVALID_APK]',
                           'adb: error: closed', 'Exception occurred while executing install',
                           'adb: failed to install app.apk']:
            with self.subTest(diagnostic=diagnostic):
                self.assertFalse(install_ok(0, diagnostic + '\nSuccess\n'))
                self.assertFalse(install_ok(0, 'Success\n', diagnostic))


if __name__ == '__main__':
    unittest.main()
