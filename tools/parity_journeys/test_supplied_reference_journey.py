"""Use preserved real Android evidence to test the reference-only dialog adapter."""
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import zipfile
import editor_journey as runner
import supplied_reference_journey as adapter
import test_editor_journey as fixtures

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / 'docs/verification/editor-journey/run-38198783416-attempt-1/evidence.zip'
DIGEST = 'abf947195917bb8f090cee7ae2eff250963c8d0ddd5d5663d7b76103a850c46e'


class ReferencePlanTests(unittest.TestCase):
    def test_only_observed_promotion_close_is_added(self):
        plan = adapter.load_plan()
        self.assertEqual(len(plan), 14)
        self.assertEqual(plan[5], ['reference-promotion', runner.PACKAGE, {'text': 'LITEAPKS'}, runner.DENY])
        self.assertEqual(plan[6][3], {'text': 'CLOSE'})
        self.assertNotIn('DOWNLOAD', json.dumps([s[3] for s in plan]))

    def test_observed_original_and_candidate_dialog_targets(self):
        self.assertEqual(hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(), DIGEST)
        with zipfile.ZipFile(ARCHIVE) as archive:
            for label in ['original', 'candidate']:
                data = archive.read('ci-editor/journey/' + label + '-home.xml')
                runner.select(runner.tree(data, runner.PACKAGE), runner.PACKAGE, {'text': 'LITEAPKS'})
                self.assertEqual(runner.target(data, runner.PACKAGE, {'text': 'CLOSE'}, 720, 1280), [234, 880])

    def test_configuration_is_restored_after_failure(self):
        previous = runner.PLAN
        with self.assertRaisesRegex(RuntimeError, 'injected'):
            with adapter.configured_plan():
                self.assertEqual(len(runner.PLAN), 14)
                raise RuntimeError('injected')
        self.assertIs(runner.PLAN, previous)

    def test_plan_tampering_is_rejected(self):
        plan = adapter.load_plan()
        plan[6][3] = {'text': 'DOWNLOAD'}
        with patch.object(adapter.PLAN_PATH.__class__, 'read_text', return_value=json.dumps(plan)):
            with self.assertRaises(runner.JourneyError):
                adapter.load_plan()

    def test_complete_extended_plan_has_same_strict_verifier(self):
        with adapter.configured_plan():
            fixture = fixtures.JourneyTests()
            fixture.setUp()
            try:
                result = fixture.result()
                self.assertTrue(result['journey_equal'], result)
                self.assertEqual(len(result['screens']), 14)
                self.assertFalse(result['full_runtime_1_to_1_established'])
                # Removing the promotion must not be accepted as a completed run.
                fixture.candidate()['screens'].pop(5)
                self.assertFalse(fixture.result()['journey_equal'])
            finally:
                fixture.tearDown()


if __name__ == '__main__':
    unittest.main()
