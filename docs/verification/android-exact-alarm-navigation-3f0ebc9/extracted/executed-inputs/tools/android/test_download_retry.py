"""Offline transport tests: mock curl; never contact a package host."""
import hashlib
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import bootstrap_android_runtime as bootstrap

class DownloadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.archive = Path(self.temp.name) / 'sdk.zip'
        self.partial = self.archive.with_suffix('.zip.partial')
        self.data = b'exact official archive fixture'
        self.package = {'id': 'test', 'url': 'https://example.invalid/sdk.zip',
                        'download_bytes': len(self.data), 'checksum_algorithm': 'sha256',
                        'checksum': hashlib.sha256(self.data).hexdigest()}
    def success(self, command, **kwargs):
        self.assertIn('--http1.1', command)
        self.assertEqual(command[command.index('--proto') + 1], '=https')
        self.assertEqual(command[command.index('--proto-redir') + 1], '=https')
        self.assertNotIn('--insecure', command)
        self.assertEqual(kwargs, {'check': True, 'timeout': 625})
        Path(command[-1]).write_bytes(self.data)
    def test_verified_bytes_promoted_only_after_success(self):
        with patch.object(bootstrap.subprocess, 'run', side_effect=self.success):
            bootstrap.download_verified(self.package, self.archive)
        self.assertEqual(self.archive.read_bytes(), self.data)
        self.assertFalse(self.partial.exists())
    def test_stream_92_retries_from_empty_file(self):
        calls = []
        def download(command, **kwargs):
            self.assertFalse(self.partial.exists())
            calls.append(command)
            if len(calls) == 1:
                self.partial.write_bytes(b'truncated')
                raise subprocess.CalledProcessError(92, command)
            self.success(command, **kwargs)
        with patch.object(bootstrap.subprocess, 'run', side_effect=download), patch.object(bootstrap.time, 'sleep'):
            bootstrap.download_verified(self.package, self.archive)
        self.assertEqual(len(calls), 2)
        self.assertEqual(self.archive.read_bytes(), self.data)
    def test_timeout_exhaustion_is_bounded_and_cleans_partial(self):
        def timeout(command, **kwargs):
            self.partial.write_bytes(b'truncated')
            raise subprocess.TimeoutExpired(command, 625)
        with patch.object(bootstrap.subprocess, 'run', side_effect=timeout) as run, patch.object(bootstrap.time, 'sleep'):
            with self.assertRaises(subprocess.TimeoutExpired):
                bootstrap.download_verified(self.package, self.archive)
        self.assertEqual(run.call_count, 3)
        self.assertFalse(self.archive.exists())
        self.assertFalse(self.partial.exists())
    def test_certificate_failure_is_not_retried(self):
        with patch.object(bootstrap.subprocess, 'run', side_effect=subprocess.CalledProcessError(60, ['curl'])) as run:
            with self.assertRaises(subprocess.CalledProcessError):
                bootstrap.download_verified(self.package, self.archive)
        self.assertEqual(run.call_count, 1)
        self.assertFalse(self.archive.exists())
    def test_size_and_hash_failures_are_never_promoted(self):
        for changed in [{'download_bytes': 1}, {'checksum': '0' * 64}]:
            with self.subTest(changed=changed), patch.object(bootstrap.subprocess, 'run', side_effect=self.success) as run:
                with self.assertRaises(ValueError):
                    bootstrap.download_verified(self.package | changed, self.archive)
                self.assertEqual(run.call_count, 1)
                self.assertFalse(self.archive.exists())
                self.assertFalse(self.partial.exists())
    def test_non_https_url_is_rejected_before_command(self):
        with patch.object(bootstrap.subprocess, 'run') as run:
            with self.assertRaises(ValueError):
                bootstrap.download_verified(self.package | {'url': 'http://example.invalid'}, self.archive)
            run.assert_not_called()

if __name__ == '__main__':
    unittest.main()
