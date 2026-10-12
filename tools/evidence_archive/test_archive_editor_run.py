"""Offline adversarial tests; no token, network request or Git mutation is used."""
import copy
import hashlib
import io
import unittest
import zipfile
from unittest.mock import Mock
import archive_editor_run as archive


class ArchiveTests(unittest.TestCase):
    def test_only_completed_own_main_runs(self):
        valid = {'id': 38197987986, 'run_attempt': 1, 'repository': {'id': archive.REPOSITORY_ID},
                 'head_repository': {'id': archive.REPOSITORY_ID}, 'head_branch': 'main', 'event': 'push',
                 'path': '.github/workflows/editor-journey.yml', 'status': 'completed', 'head_sha': 'a' * 40}
        archive.validate_run(valid)
        archive.validate_run(valid | {'path': '.github/workflows/editor-session.yml'})
        changes = [{'head_repository': {'id': 1}}, {'repository': {'id': 1}}, {'event': 'pull_request'},
                   {'head_branch': 'foreign'}, {'status': 'in_progress'}, {'head_sha': '../bad'},
                   {'run_attempt': True}, {'id': False}, {'path': 'unrelated.yml'}]
        for change in changes:
            with self.subTest(change=change), self.assertRaises(archive.ArchiveError):
                archive.validate_run(valid | change)

    def make_zip(self, names):
        out = io.BytesIO()
        with zipfile.ZipFile(out, 'w') as target:
            for name in names:
                target.writestr(name, b'not executed')
        data = out.getvalue()
        return data, 'sha256:' + hashlib.sha256(data).hexdigest()

    def test_exact_digest_and_inventory(self):
        data, digest = self.make_zip(['ci-editor/journey/record.json', 'tools/parity_journeys/test.py'])
        self.assertEqual(len(archive.validate_zip(data, digest)), 2)
        with self.assertRaises(archive.ArchiveError):
            archive.validate_zip(data + b'x', digest)
        with self.assertRaises(archive.ArchiveError):
            archive.validate_zip(data, None)

    def test_hostile_paths_and_duplicates(self):
        for names in [['../escape'], ['/absolute'], ['ci-editor/../escape'], ['.git/config'],
                      ['ci-editor\\evil'], ['ci-editor/duplicate', 'ci-editor/duplicate']]:
            with self.subTest(names=names), self.assertRaises(archive.ArchiveError):
                archive.validate_zip(*self.make_zip(names))

    def test_symlink_member_rejected(self):
        entry = zipfile.ZipInfo('ci-editor/link')
        entry.create_system = 3
        entry.external_attr = 0o120777 << 16
        with self.assertRaises(archive.ArchiveError):
            archive.validate_zip(*self.make_zip([entry]))

    def test_bounded_responses_and_no_auth_redirect(self):
        self.assertEqual(archive.bounded_read(io.BytesIO(b'ok'), 2), b'ok')
        with self.assertRaises(archive.ArchiveError):
            archive.bounded_read(io.BytesIO(b'long'), 2)
        redirect = archive.NoRedirect()
        self.assertIsNone(redirect.redirect_request(Mock(), None, 302, '', {}, 'https://elsewhere'))

if __name__ == '__main__':
    unittest.main()
