#!/usr/bin/env python3
"""Verify the declared twelve-screen trigger-category observation at scale one."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import prepare_trigger_journey as preparation


def verify(root, output):
    result = {'status': 'TRIGGER_CATEGORY_EVIDENCE_INCOMPLETE', 'evidence_valid': False,
              'full_runtime_1_to_1_established': False, 'animation_timing_parity_established': False,
              'scope': 'Two fixed APKs, twelve full-frame still observations and eleven inputs each at animation scale one',
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
        import enable_normal_animations as scales
        import trigger_category_journey as category
        import editor_journey as runner
        import android_compare as proof
        folder = output / 'animation-settings'
        settings = json.loads((folder / 'animation-scales.json').read_text())
        if settings.get('status') != 'ANIMATION_SCALE_ONE_VERIFIED' or settings.get('android_executed') is not True:
            raise ValueError('Actual normal animation configuration was not observed')
        scales.verify_report(folder, settings)
        device = json.loads((output / 'device/capture-device.json').read_text())
        if (device.get('status') != 'CAPTURE_DEVICE_CONFIGURED' or device.get('demo_clock_requested') != '1200'
                or device.get('disable_animations_requested') is not False
                or device.get('systemui_demo_mode_observed') is not True):
            raise ValueError('The declared radio and demo-clock preparation differs')
        journey = output / 'journey'
        report = json.loads((journey / 'journey.json').read_text())
        captured = json.loads((journey / 'comparison.json').read_text())
        if (report.get('status') != 'RECORDED_NOT_PARITY' or len(report.get('runs', [])) != 2
                or [run['apk_sha256'] for run in report['runs']] != [row[3] for row in preparation.APKS]
                or report.get('plan_sha256') != preflight['plan_sha256']):
            raise ValueError('The exact two-APK twelve-screen observation is incomplete')
        for run in report['runs']:
            if (run.get('status') != 'COMPLETE' or len(run['screens']) != 12 or len(run['transitions']) != 11
                    or settings['finished_monotonic'] > run['launch']['started_monotonic']):
                raise ValueError('Configuration and complete journey are not in order')
            for name in ('environment', 'environment_after'):
                environment = run[name]
                if (environment.get('serial') != scales.SERIAL
                        or environment.get('ro.build.fingerprint') != scales.FINGERPRINT
                        or environment.get('ro.build.version.sdk') != '35'
                        or any(environment.get('global:' + key) not in ('1', '1.0') for key in scales.SCALES)):
                    raise ValueError('Normal animation settings or pinned device changed during a run')
        with category.configured_plan():
            replayed = runner.compare(journey, report, proof)
        if (replayed != captured or len(replayed.get('screens', [])) != 12
                or 'reason' in replayed or replayed.get('android_runtime_executed') is not True
                or replayed.get('catalog_navigation_established') is not True
                or replayed.get('trigger_selected') is not False
                or replayed.get('status') not in ('JOURNEY_DIFFERENCE',
                    'EXACT_TRIGGER_CATEGORY_OBSERVATION_ONLY', 'MATCHED_POST_CRASH_CONTINUATION_ONLY')):
            raise ValueError('Independent full-frame replay differs from the recorded comparison')
        result.update(status=('TRIGGER_CATEGORY_TWELVE_SCREEN_MATCH_ONLY' if replayed['journey_equal']
                              else 'TRIGGER_CATEGORY_TWELVE_SCREEN_DIFFERENCE'), evidence_valid=True,
                      journey_equal=replayed['journey_equal'], comparison=replayed,
                      changed_pixels=[row['changed_pixels'] for row in replayed['screens']],
                      animation_configuration_sha256=hashlib.sha256((folder / 'animation-scales.json').read_bytes()).hexdigest(),
                      historical_results_rewritten=False)
    except Exception as error:
        result['reason'] = type(error).__name__ + ': ' + str(error)
    (output / 'trigger-category-verification.json').write_text(json.dumps(result, indent=2) + '\n')
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
