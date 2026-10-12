#!/usr/bin/env python3
"""Verify the declared sixteen-screen exact-alarm navigation observation at scale zero."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import prepare_trigger_journey as preparation



def require_workflow_policies(report):
    """Require this workflow's schema even if a legacy comparison could pass.

    This checks the requested policy format only. Actual phase artifacts,
    chronology, commands, ownership and both references are verified by compare.
    """
    import exact_alarm_enable_return
    import exact_alarm_enable_return_readiness
    with exact_alarm_enable_return.configured_plan():
        exact_alarm_enable_return.require_navigation_policy(report)
        exact_alarm_enable_return_readiness.require_policy(report)


def verify(root, output):
    result = {'status': 'EXACT_ALARM_ENABLE_RETURN_EVIDENCE_INCOMPLETE', 'evidence_valid': False,
              'full_runtime_1_to_1_established': False, 'animation_timing_parity_established': False,
              'scope': 'Two fixed APKs, sixteen full-frame still observations and fifteen inputs each at animation scale zero, with bounded notification readiness',
              'verified_at_utc': datetime.now(timezone.utc).isoformat()}
    try:
        preflight = json.loads((output / 'input-preflight.json').read_text())
        preparation.verify_prepared_inputs(root, output, preflight)
        materialized = json.loads((output / 'materialized-inputs.json').read_text())
        if materialized.get('passed') is not True:
            raise ValueError('Materialized APK preflight did not pass')
        if (materialized.get('status') != 'EXACT_APKS_AND_AAPT2_VERIFIED_OFFLINE'
                or materialized.get('aapt2') != {
                    'source': 'workspace/MacroDroid_v9/tools/prebuilt/linux/aapt2',
                    'executed_copy': 'reviewed-source/project/tools/prebuilt/linux/aapt2',
                    **preparation.AAPT}
                or preparation.identity(preparation.checked_file(output,
                    'reviewed-source/project/tools/prebuilt/linux/aapt2')) != preparation.AAPT):
            raise ValueError('Executed AAPT2 changed')
        for _, filename, size, digest in preparation.APKS:
            if preparation.identity(root / 'workspace/artifacts' / filename) != {'bytes': size, 'sha256': digest}:
                raise ValueError('APK changed during the diagnostic')
        sys.dont_write_bytecode = True
        sys.path[:0] = [str(output / 'reviewed-source/tools/parity_journeys'),
                       str(output / 'reviewed-source/project'), str(root / preparation.ANIMATION)]
        import enable_still_animations as scales
        import exact_alarm_enable_return as category
        import editor_journey as runner
        import android_compare as proof
        folder = output / 'animation-settings'
        settings = json.loads((folder / 'animation-scales.json').read_text())
        if settings.get('status') != 'ANIMATION_SCALE_ZERO_VERIFIED' or settings.get('android_executed') is not True:
            raise ValueError('Actual zero animation configuration was not observed')
        scales.verify_report(folder, settings)
        device = json.loads((output / 'device/capture-device.json').read_text())
        if (device.get('status') != 'CAPTURE_DEVICE_CONFIGURED' or device.get('demo_clock_requested') != '1200'
                or device.get('disable_animations_requested') is not False
                or device.get('systemui_demo_mode_observed') is not True):
            raise ValueError('The declared radio and demo-clock preparation differs')
        journey = output / 'journey'
        report = json.loads((journey / 'journey.json').read_text())
        require_workflow_policies(report)
        captured = json.loads((journey / 'comparison.json').read_text())
        if (report.get('status') != 'RECORDED_NOT_PARITY' or len(report.get('runs', [])) != 2
                or [run['apk_sha256'] for run in report['runs']] != [row[3] for row in preparation.APKS]
                or report.get('plan_sha256') != preflight['plan_sha256']):
            raise ValueError('The exact two-APK sixteen-screen observation is incomplete')
        for run in report['runs']:
            if (run.get('status') != 'COMPLETE' or len(run['screens']) != 16 or len(run['transitions']) != 15
                    or settings['finished_monotonic'] > run['launch']['started_monotonic']):
                raise ValueError('Configuration and complete journey are not in order')
            for name in ('environment', 'environment_after'):
                environment = run[name]
                if (environment.get('serial') != scales.SERIAL
                        or environment.get('ro.build.fingerprint') != scales.FINGERPRINT
                        or environment.get('ro.build.version.sdk') != '35'
                        or any(environment.get('global:' + key) not in ('0', '0.0') for key in scales.SCALES)):
                    raise ValueError('Zero animation settings or pinned device changed during a run')
        with category.configured_plan():
            replayed = runner.compare(journey, report, proof)
        if (replayed != captured or len(replayed.get('screens', [])) != 16
                or 'reason' in replayed or replayed.get('android_runtime_executed') is not True
                or replayed.get('catalog_navigation_established') is not True
                or replayed.get('trigger_type_tapped') is not True
                or replayed.get('trigger_configuration_confirmed') is not False
                or replayed.get('exact_alarm_explanation_ok_tapped') is not True
                or replayed.get('settings_navigation_observed') is not True
                or replayed.get('settings_inputs') != 4
                or replayed.get('settings_inputs_per_run') != 2
                or replayed.get('settings_enabled_state_observed') is not True
                or replayed.get('settings_return_navigation_observed') is not True
                or replayed.get('permission_api_result_observed') is not False
                or replayed.get(category.POLICY_KEY) != category.POLICY
                or replayed.get('global_command_observations', {}).get('planned_inputs') != 30
                or replayed.get('global_command_observations', {}).get('setup_mutations') != 6
                or replayed.get('global_command_observations', {}).get('unbound_mutations') != 0
                or replayed.get('global_command_observations', {}).get('settings_inputs') != 4
                or replayed.get('status') not in ('JOURNEY_DIFFERENCE',
                    'EXACT_ALARM_ENABLED_RETURN_OBSERVATION_ONLY', 'MATCHED_POST_CRASH_CONTINUATION_ONLY')):
            raise ValueError('Independent full-frame replay differs from the recorded comparison')
        result.update(status=('EXACT_ALARM_ENABLE_RETURN_SIXTEEN_SCREEN_MATCH_ONLY' if replayed['journey_equal']
                              else 'EXACT_ALARM_ENABLE_RETURN_SIXTEEN_SCREEN_DIFFERENCE'), evidence_valid=True,
                      journey_equal=replayed['journey_equal'], comparison=replayed,
                      changed_pixels=[row['changed_pixels'] for row in replayed['screens']],
                      animation_configuration_sha256=hashlib.sha256((folder / 'animation-scales.json').read_bytes()).hexdigest(),
                      historical_results_rewritten=False)
    except Exception as error:
        result['reason'] = type(error).__name__ + ': ' + str(error)
    (output / 'exact-alarm-enable-return-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.root.resolve(), args.output.resolve())
    print(json.dumps(result, indent=2))
    return 0 if result['evidence_valid'] and result.get('journey_equal') else 2


if __name__ == '__main__':
    raise SystemExit(main())
