"""Regression tests for the three reviewed stale-file false positives and aliases."""
import copy
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import test_post_onboarding as fixtures
from session_evidence import EvidenceLedger, verify_session_evidence
import editor_journey as runner


class SessionEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.SessionTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.run = self.fixture.report['runs'][1]
        self.start = self.fixture.start

    def rejected(self):
        result = self.fixture.result()
        self.assertFalse(result['editor_session_equal'], result)
        self.assertEqual(result['status'], 'REJECTED')
        self.assertIn('Reused session evidence:', result['reason'])

    def test_legitimate_equal_bytes_are_distinct_observations(self):
        result = self.fixture.result()
        self.assertTrue(result['editor_session_equal'], result)
        self.assertEqual(result['evidence_identity_check']['unique_observation_files'], 294)
        self.assertFalse(result['startup_parity_established'])

    def test_deleted_endpoint_outputs_cannot_be_replaced_by_start_identity(self):
        initial = self.run['screens'][self.start]['session_identity']
        final = self.run['screens'][-1]['session_identity']
        for key in ('package_path', 'checksum', 'pid', 'foreground'):
            for stream in ('stdout', 'stderr'):
                (self.fixture.root / final[key][stream]['path']).unlink()
        self.run['screens'][-1]['session_identity'] = copy.deepcopy(initial)
        self.rejected()

    def test_deleted_immediate_outputs_cannot_reuse_an_earlier_input(self):
        first, later = self.run['transitions'][self.start:self.start + 2]
        for record in later['preinput_artifacts'].values():
            (self.fixture.root / record['path']).unlink()
        later['preinput_artifacts'] = copy.deepcopy(first['preinput_artifacts'])
        self.rejected()

    def test_resolved_dot_alias_of_earlier_input_is_rejected(self):
        first, later = self.run['transitions'][self.start:self.start + 2]
        (self.fixture.root / 'candidate-reused').mkdir()
        for key, record in list(first['preinput_artifacts'].items()):
            data = (self.fixture.root / record['path']).read_bytes()
            fresh = self.fixture.fixture.put('candidate-reused/' + key + '.txt', data)
            first['preinput_artifacts'][key] = fresh
            (self.fixture.root / later['preinput_artifacts'][key]['path']).unlink()
            later['preinput_artifacts'][key] = dict(fresh, path='candidate-reused/./' + key + '.txt')
        self.rejected()

    def test_hard_linked_immediate_outputs_are_rejected(self):
        first, later = self.run['transitions'][self.start:self.start + 2]
        for key in ('pid', 'foreground'):
            src = self.fixture.root / first['preinput_artifacts'][key]['path']
            dst = self.fixture.root / later['preinput_artifacts'][key]['path']
            dst.unlink()
            os.link(src, dst)
            later['preinput_artifacts'][key].update(bytes=src.stat().st_size,
                                                   sha256=self.fixture.proof.sha(src.read_bytes()))
        self.rejected()

    def test_symlinked_endpoint_output_is_rejected(self):
        first = self.run['screens'][self.start]['session_identity']['checksum']['stdout']
        final = self.run['screens'][-1]['session_identity']['checksum']['stdout']
        src = self.fixture.root / first['path']
        dst = self.fixture.root / final['path']
        dst.unlink()
        dst.symlink_to(src.name)
        final.update(bytes=first['bytes'], sha256=first['sha256'])
        self.rejected()

    def test_snapshot_pid_cannot_reuse_earlier_frame_pid(self):
        first = self.run['screens'][self.start]['artifacts']
        later = self.run['screens'][self.start + 1]['artifacts']
        later['pid_first'] = copy.deepcopy(first['pid_first'])
        self.rejected()

    def test_before_snapshot_cannot_reuse_an_earlier_before_pid(self):
        first, later = self.run['transitions'][self.start:self.start + 2]
        later['before']['artifacts']['pid_first'] = copy.deepcopy(first['before']['artifacts']['pid_first'])
        self.rejected()

    def test_empty_input_outputs_must_also_be_distinct_files(self):
        first, later = self.run['transitions'][self.start:self.start + 2]
        later['command']['stdout'] = copy.deepcopy(first['command']['stdout'])
        self.rejected()

    def test_cross_run_hard_link_is_rejected(self):
        original = self.fixture.report['runs'][0]['screens'][self.start]['artifacts']['screenshot']
        candidate = self.run['screens'][self.start]['artifacts']['screenshot']
        src = self.fixture.root / original['path']
        dst = self.fixture.root / candidate['path']
        dst.unlink()
        os.link(src, dst)
        self.rejected()

    def test_modified_hash_fails_before_identity_registration(self):
        record = self.run['screens'][self.start]['artifacts']['hierarchy']
        (self.fixture.root / record['path']).write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'changed'):
            EvidenceLedger(self.fixture.root, self.fixture.proof).claim(record, 'changed-artifact')

    def test_unknown_artifact_role_is_rejected(self):
        self.run['screens'][self.start]['artifacts']['extra'] = self.run['screens'][self.start]['artifacts']['pid_first']
        with self.assertRaisesRegex(runner.JourneyError, 'Unexpected session evidence group'):
            verify_session_evidence(self.fixture.root, self.fixture.report['runs'], self.start, self.fixture.proof)


if __name__ == '__main__':
    unittest.main()
