"""Offline publication controls. These fixtures never execute an app or contact GitHub."""
from __future__ import annotations
import copy
import hashlib
import io
import json
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import Mock, patch
import zipfile

import stage_lookup_acceptance as stage


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def archive(self, names):
        path = self.root / 'input.zip'
        with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as source:
            for name in names:
                source.writestr(name, b'literal test bytes')
        return path, 'sha256:' + stage.digest(path.read_bytes())

    def test_exact_zip_inventory(self):
        path, sha = self.archive(['hosted-proof/result.json', 'combined-workspace/report.txt'])
        rows = stage.checked_archive(path, sha)
        self.assertEqual(2, len(rows))
        self.assertEqual(stage.identity(b'literal test bytes'), {key: rows[0][key] for key in ('bytes', 'sha256')})

    def test_wrong_digest_and_missing_digest_reject(self):
        path, _ = self.archive(['hosted-proof/result.json'])
        for sha in (None, '', 'sha256:' + '0' * 64, 'md5:' + 'a' * 32):
            with self.subTest(sha=sha), self.assertRaises(stage.PublicationError):
                stage.checked_archive(path, sha)

    def test_path_and_duplicate_controls(self):
        for names in (['../escape'], ['/absolute'], ['a/./b'], ['a//b'], ['a\\b'], ['a', 'a']):
            with self.subTest(names=names):
                path, sha = self.archive(names)
                with self.assertRaises(stage.PublicationError):
                    stage.checked_archive(path, sha)

    def test_symlink_member_rejects(self):
        entry = zipfile.ZipInfo('link'); entry.create_system = 3; entry.external_attr = (stat.S_IFLNK | 0o777) << 16
        path, sha = self.archive([entry])
        with self.assertRaises(stage.PublicationError):
            stage.checked_archive(path, sha)

    def test_outer_symlink_rejects(self):
        path, sha = self.archive(['hosted-proof/result.json'])
        alias = self.root / 'alias.zip'; alias.symlink_to(path)
        with self.assertRaises(stage.PublicationError): stage.checked_archive(alias, sha)

    def test_bounded_archive_rejects(self):
        path, sha = self.archive(['hosted-proof/result.json'])
        with patch.object(stage, 'MAX_ARCHIVE', 4), self.assertRaises(stage.PublicationError):
            stage.checked_archive(path, sha)
        with patch.object(stage, 'MAX_EXPANDED', 4), self.assertRaises(stage.PublicationError):
            stage.checked_archive(path, sha)

    def test_modified_member_fails_crc(self):
        path = self.root / 'bad.zip'
        with zipfile.ZipFile(path, 'w', zipfile.ZIP_STORED) as archive: archive.writestr('record', b'known-content')
        path.write_bytes(path.read_bytes().replace(b'known-content', b'wrong-content', 1))
        with self.assertRaises(zipfile.BadZipFile):
            stage.checked_archive(path, 'sha256:' + stage.digest(path.read_bytes()))


class ContractTests(unittest.TestCase):
    def test_only_exact_successful_source_run(self):
        run = {'id':stage.RUN_ID, 'repository':{'id':stage.REPO_ID}, 'head_repository':{'id':stage.REPO_ID},
               'head_branch':'main', 'head_sha':stage.SOURCE_COMMIT, 'path':stage.WORKFLOW,
               'event':'push', 'status':'completed', 'conclusion':'success', 'run_attempt':1}
        stage.checked_run(run)
        for mutation in ({'id':1}, {'head_sha':'a' * 40}, {'head_branch':'other'}, {'event':'pull_request'},
                         {'status':'in_progress'}, {'conclusion':'failure'}, {'run_attempt':True},
                         {'path':'.github/workflows/other.yml'}, {'head_repository':{'id':1}}, {'repository':{'id':1}}):
            with self.subTest(mutation=mutation), self.assertRaises(stage.PublicationError): stage.checked_run(run | mutation)

    def test_json_rejects_duplicate_keys_and_nonfinite_values(self):
        self.assertEqual({'a':None}, stage.document(b'{"a":null}'))
        for data in (b'{"a":1,"a":2}', b'{"v":NaN}', b'{"v":Infinity}', b'{"v":-Infinity}'):
            with self.subTest(data=data), self.assertRaises(stage.PublicationError): stage.document(data)

    def test_success_flags_and_counts_are_not_truthy_approximations(self):
        pins = {'future_snapshot': {'files':81304, 'snapshot_sha256':'f' * 64}, 'future_manifest':{'bytes':14, 'sha256':'b' * 64},
                'suite_cases':{'synthetic':195151}, 'lookup_commit':'c' * 40}
        report = {'status':'ISOLATED_DAY_TRIGGER_NUMERIC_LOOKUP_ALL_16_HOST_GATES_VERIFIED', 'passed':True,
                  'active_promoted':False, 'android_runtime_executed':False, 'full_runtime_1_to_1_established':False,
                  'candidate_is_wip_only':True, 'gates_verified':16, 'fresh_reports_verified':24, 'actual_cases':195151,
                  'registered_methods':1244, 'target_classes':605, 'actual_ui_java_controls':101,
                  'source_snapshot':pins['future_snapshot'], 'future_manifest':pins['future_manifest'],
                  'suite_cases':pins['suite_cases'], 'lookup_source_commit':pins['lookup_commit'],
                  'apks':{'hybrid':{'sha256':stage.LOCAL_APK_SHA256}}}
        stage.strict_success(report, pins)
        for mutation in ({'passed':1}, {'gates_verified':16.0}, {'fresh_reports_verified':True}, {'actual_cases':195150},
                         {'registered_methods':1243}, {'actual_ui_java_controls':100}, {'candidate_is_wip_only':False},
                         {'active_promoted':True}, {'android_runtime_executed':True}, {'full_runtime_1_to_1_established':True},
                         {'apks':{'hybrid':{'sha256':'d' * 64}}}, {'future_manifest':{}}, {'source_snapshot':{}},
                         {'suite_cases':{}}, {'lookup_source_commit':'d' * 40}):
            with self.subTest(mutation=mutation), self.assertRaises(stage.PublicationError): stage.strict_success(report | mutation, pins)

    def test_multipart_bytes_reassemble_exactly(self):
        with patch.object(stage, 'PART_BYTES', 4):
            files, manifest = stage.multipart(b'0123456789', 'owned/evidence', 'evidence.zip', 'test fixture')
        self.assertEqual(3, len(manifest['parts']))
        self.assertEqual(b'0123456789', b''.join(files[row['path']] for row in manifest['parts']))
        self.assertEqual(stage.digest(b'0123456789'), manifest['sha256'])
        for row in manifest['parts']:
            self.assertEqual(row['size_bytes'], len(files[row['path']]))
            self.assertEqual(row['sha256'], stage.digest(files[row['path']]))

    def test_blob_returned_oid_is_independently_checked(self):
        client = stage.Github('fake-offline-token')
        raw = b'fixture'; oid = hashlib.sha1(b'blob 7\0fixture').hexdigest()
        with patch.object(client, 'json', return_value={'sha':oid}) as call:
            self.assertEqual(oid, client.blob('owned/file', raw)['sha'])
            self.assertEqual('/git/blobs', call.call_args.args[0])
        with patch.object(client, 'json', return_value={'sha':'0' * 40}), self.assertRaises(stage.PublicationError):
            client.blob('owned/file', raw)

    def test_auth_redirect_is_not_followed(self):
        self.assertIsNone(stage.NoRedirect().redirect_request(Mock(), None, 302, '', {}, 'https://other.invalid'))
        with self.assertRaises(stage.PublicationError): stage.Github('fake').request('//other.invalid')


if __name__ == '__main__': unittest.main()
