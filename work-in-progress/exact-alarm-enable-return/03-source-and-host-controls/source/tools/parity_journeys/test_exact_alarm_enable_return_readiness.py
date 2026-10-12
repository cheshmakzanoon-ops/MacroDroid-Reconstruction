"""Re-run the established readiness controls under the new exact sixteen-screen plan."""
from __future__ import annotations
import copy
from unittest.mock import patch
import unittest

import editor_journey as runner
import exact_alarm_enable_return as alarm
import exact_alarm_enable_return_readiness as ready
import test_notification_readiness as prior
from test_exact_alarm_enable_return import SixteenFixture


class EnableReturnPhaseControls(prior.ReadinessControls):
    def setUp(self):
        for name, value in (('day', alarm), ('ready', ready)):
            context = patch.object(prior, name, value); context.start(); self.addCleanup(context.stop)
        super().setUp()


class EnableReturnReadinessReportControls(prior.ReadinessReportControls):
    def setUp(self):
        for name, value in (('day', alarm), ('ready', ready), ('ThirteenFixture', SixteenFixture)):
            context = patch.object(prior, name, value); context.start(); self.addCleanup(context.stop)
        super().setUp()

    def add_phases(self):
        super().add_phases()
        self.report[alarm.POLICY_KEY] = copy.deepcopy(alarm.POLICY)

    def test_complete_synthetic_pair_requires_readiness_and_keeps_thirteen_screen_scope(self):
        # The inherited control's algorithm is unchanged; this explicit successor
        # asserts the new screen count and visible enabled-state and return scope.
        self.add_phases()
        result = self.fixture.result()
        self.assertTrue(result['journey_equal'], result)
        self.assertEqual(len(result['notification_readiness_observations']), 2)
        self.assertEqual(len(result['screens']), 16)
        self.assertEqual(result['settings_inputs'], 4)
        self.assertFalse(result['permission_api_result_observed'])
        self.assertFalse(result['full_runtime_1_to_1_established'])
        self.assertFalse(result['crash_free_run_established'])
        self.assertFalse(result['trigger_configuration_confirmed'])

    def test_older_schema_unchanged_and_mixed_new_evidence_rejected(self):
        # New-plan reports cannot use an older schema even before a readiness
        # field is added. The original old-plan test remains byte-identical.
        result = self.fixture.result()
        self.assertFalse(result['journey_equal'])
        self.assertIn('requires schema7', result['reason'])
        self.add_phases()
        for schema in (2, 3, 5, 6):
            value = copy.deepcopy(self.report); value['schema'] = schema
            self.assertFalse(runner.compare(self.folder, value, prior.proof)['journey_equal'])


if __name__ == '__main__':
    unittest.main()
