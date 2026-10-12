"""Acquisition retry controls; no Android process is executed by these tests."""
import json
import unittest
from unittest.mock import Mock, patch
import xml.etree.ElementTree as ET
import editor_journey as runner
from robust_capture import EvidenceRecorder

BASE = EvidenceRecorder.__mro__[1]

class AcquisitionTests(unittest.TestCase):
    def setUp(self):
        self.recorder = object.__new__(EvidenceRecorder)
        self.recorder.save = Mock()

    def test_missing_remote_xml_retries_fresh_name_then_accepts_valid_snapshot(self):
        with patch.object(BASE, 'snapshot', side_effect=[ET.ParseError('syntax error'), {'valid': True}]) as acquire, patch('robust_capture.time.sleep'):
            self.assertEqual(self.recorder.snapshot('original-home', runner.PACKAGE), {'valid': True})
        self.assertEqual([call.args[0] for call in acquire.call_args_list], ['original-home-acquisition-1', 'original-home-acquisition-2'])
        diagnostic = json.loads(self.recorder.save.call_args.args[1])
        self.assertFalse(diagnostic['accepted_as_evidence'])

    def test_three_bad_acquisitions_become_caught_journey_error(self):
        with patch.object(BASE, 'snapshot', side_effect=ET.ParseError('bad')) as acquire, patch('robust_capture.time.sleep'):
            with self.assertRaisesRegex(runner.JourneyError, 'three fresh attempts'):
                self.recorder.snapshot('candidate-home', runner.PACKAGE)
        self.assertEqual(acquire.call_count, 3)
        self.assertEqual(self.recorder.save.call_count, 3)

    def test_semantic_or_process_failure_is_not_retried_or_weakened(self):
        with patch.object(BASE, 'snapshot', side_effect=runner.JourneyError('PID changed')) as acquire:
            with self.assertRaisesRegex(runner.JourneyError, 'PID changed'):
                self.recorder.snapshot('candidate-home', runner.PACKAGE)
        self.assertEqual(acquire.call_count, 1)
        self.recorder.save.assert_not_called()

if __name__ == '__main__':
    unittest.main()
