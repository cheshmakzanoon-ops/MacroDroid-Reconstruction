#!/usr/bin/env python3
"""Freeze the failed Normal03 analysis separately from the unchanged raw ZIP."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil

BASE = Path(__file__).resolve().parent
WORK = BASE.parent
OUT = BASE / 'checkpoints/01-actual-normal-scale-failure'
RAW = WORK / 'tooling-validation/normal-animation-run-38212813248'
TARGET = 'docs/verification/android-normal-animation-3edcddd'


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    measurements = json.loads((BASE / '01-full-frame-measurements/frame-measurements.json').read_text())
    replay = json.loads((BASE / '02-frozen-replay/replay-result.json').read_text())
    receipt = json.loads((WORK / 'tooling-validation/normal-animation-run-38212813248-extraction.json').read_text())
    config = json.loads((BASE / '02-frozen-replay/verified-configuration-summary.json').read_text())
    pairs = measurements['all_55_frame_pair_measurements']
    assert replay['status'] == 'EXACT_FAILED_NORMAL03_EVIDENCE_REPLAYED'
    assert measurements['all_55_pair_differences_confined_to_actual_lottie_view']
    assert all(row['changed_pixels'] > 0 for row in pairs)
    assert len(measurements['intro2_indicator_region_distinct_rgba_sha256']) == 1
    summary = {
        'schema': 1, 'status': 'NORMAL_SCALE_ONE_JOURNEY_INCOMPLETE_WITH_RETAINED_ANIMATION',
        'run_id': 38212813248, 'job_id': 114690610883,
        'head_sha': '3edcddd86660ea10c8aff71b651b446f86412525',
        'raw_archive': receipt['archive'], 'raw_files': receipt['member_count'],
        'raw_expanded_bytes': receipt['expanded_bytes'], 'literal_rejections_reproduced': True,
        'original_retained_intro2_frames': 5, 'candidate_retained_intro2_frames': 6,
        'all_frame_pair_count': 55, 'cross_apk_pair_count': 30,
        'full_frame_cross_apk_changed_pixel_range': [
            min(row['changed_pixels'] for row in pairs if row['kind'] == 'cross_apk_diagnostic_only'),
            max(row['changed_pixels'] for row in pairs if row['kind'] == 'cross_apk_diagnostic_only')],
        'consecutive_full_frame_changed_pixels': {
            label: [row['changed_pixels'] for row in pairs if row['consecutive'] and row['left'][0] == label]
            for label in ('original', 'candidate')},
        'all_55_pair_differences_confined_to_xml_lottie_view': True,
        'lottie_xml_bounds': [0, 531, 720, 1011], 'indicator_xml_bounds': [128, 1184, 592, 1200],
        'all_11_xml_bytes_identical': True,
        'all_11_indicator_region_rgba_identical': True,
        'indicator_region_rgba_sha256': measurements['intro2_indicator_region_distinct_rgba_sha256'][0],
        'intro2_xml_sha256': measurements['intro2_xml_distinct_sha256'][0],
        'accepted_intro1_full_state_equal': True,
        'pinned_input_copy_roles_independently_reconstructed': 190,
        'observations_verified': 19, 'fresh_next_inputs_verified': 2,
        'installed_identities_verified': [row['apk_sha256'] for row in measurements['runs']],
        'already_executed_host_tests_verified_from_individual_results': 145,
        'new_android_execution_by_analysis': False,
        'source_or_apk_or_raw_evidence_changed': False,
        'acceptance_regions_or_masks_or_tolerances_added': False,
        'cross_apk_frame_selection': False,
        'historical_scale_zero_failure_rewritten': False,
        'ten_screen_parity_established': False,
        'animation_timing_parity_established': False,
        'full_runtime_1_to_1_established': False,
        'raw_archive_publication_owned_by': 'repository_transfer',
    }
    (OUT / 'analysis').mkdir()
    (OUT / 'analysis/analysis-summary.json').write_text(json.dumps(summary, indent=2) + '\n')

    rows = []
    for label in ('original', 'candidate'):
        for frame in measurements['all_retained_intro2_frames'][label]:
            rows.append(f"| {label} | {frame['frame_number']} | {frame['started_seconds_after_tap_completed']:.6f} | "
                        f"{frame['finished_seconds_after_tap_completed']:.6f} | {frame['observation_seconds']:.6f} |")
    difference_rows = []
    for row in pairs:
        if row['consecutive']:
            difference_rows.append(f"| {row['left'][0]} | {row['left'][1]} → {row['right'][1]} | {row['changed_pixels']:,} | `{row['difference_bounds_exclusive']}` |")
    matrix = {(row['left'][1], row['right'][1]): row['changed_pixels'] for row in pairs if row['kind'] == 'cross_apk_diagnostic_only'}
    matrix_rows = ['| Original ' + str(a) + ' | ' + ' | '.join(f'{matrix[a, b]:,}' for b in range(1, 7)) + ' |' for a in range(1, 6)]
    gallery = []
    for label, numbers in [('original', [1, 5]), ('candidate', [1, 6])]:
        for number in numbers:
            name = f'{label}-intro-2-acquisition-1-frame-{number}'
            gallery.append(f'| {label} frame {number} | [Full PNG](extracted/journey/{name}.png) | [Full XML](extracted/journey/{name}.xml) |')
    readme = f'''# Normal animation diagnostic: retained clock animation, incomplete journey

**The ten-screen diagnostic failed at TRIGGERS in both APKs.** With all three animation scales explicitly set to one, none of the retained TRIGGERS frames formed the required consecutive identical full PNG/XML pair. Every measured difference lies inside the actual Lottie clock view. The whole indicator view and all eleven hierarchies are identical in this run. These findings preserve the failed run and the earlier scale-zero 26-pixel failure; they do not establish animation timing parity or full runtime parity.

## Exact run and inputs

[GitHub Actions run 38212813248](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38212813248), job `114690610883`, checked out `3edcddd86660ea10c8aff71b651b446f86412525`. Setup, pinned-source preparation, host controls, APK inspection and runtime installation passed. Both the observation step and independent final verifier failed; the evidence upload succeeded. The [captured GitHub metadata](analysis/github-final-metadata.json) records those step conclusions and artifact binding.

| Input | Bytes | SHA256 |
| --- | ---: | --- |
| Supplied original APK | 95,725,918 | `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800` |
| Candidate APK used by this diagnostic | 94,683,497 | `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2` |
| Exact GitHub artifact ZIP | 28,080,813 | `93cfed4c5f5c17170a926bd79781807422698c22b26cf7afc60430b2a7183d92` |

The run predates the later combined `5f635e…` candidate. Its conclusions apply to these exact two APKs. The exact ZIP contains **952 regular files / 37,695,272 expanded bytes**. [manifest.json](manifest.json) and [extraction-receipt.json](extraction-receipt.json) bind the raw archive and unchanged members under [extracted](extracted/). This derived capsule does not replace or re-encode them.

## What actually completed

Both fresh package removals, installations, installed-path checks, installed APK SHA checks and launches succeeded. Each app recorded one accepted `intro-1` still and one fresh, validated Next tap at `(640,1152)`. The two accepted intro-1 states are identical in full decoded pixels, XML, dimensions and color metadata. No later page was accepted. The run did not reach notification denial, restart handling, the app-owned dialog or the editor.

The captured [journey comparison](extracted/journey/comparison.json) is `REJECTED`, with reason `Incomplete run or changed environment`. Its default `android_runtime_executed: false` is a rejected-comparison flag; successful install/launch records and nineteen retained device observations independently prove that device execution occurred. The [normal-animation result](extracted/normal-animation-verification.json) is `NORMAL_ANIMATION_EVIDENCE_INCOMPLETE`, with reason `ValueError: Configuration and complete journey are not in order`. No completion label has been substituted.

The local replay used the exact captured verifier and independently reconstructed **all 190 pinned input-copy roles**. It reproduced both rejection objects, allowing only the new verifier's timestamp to differ. It additionally verified all nineteen complete retained observations, 114 distinct physical observation artifacts, both installed identities and both fresh pre-input sequences. The recorded 130 capture tests, nine animation-helper tests and six downloader tests all have individual successes and matching summaries: **145 hosted host tests**. No new Android commands or unrelated tests were executed by this analysis. See [replay result](analysis/replay/replay-result.json), [exact input inventory](analysis/replay/independently-reconstructed-190-inputs.json), [partial observation verification](analysis/replay/verified-partial-observations.json) and [host-log checks](analysis/replay/verified-host-test-summaries.json).

## Declared device settings

The pinned disposable API35 emulator used its original radio controls and the explicit `12:00` SystemUI demo clock. All 37 device-configuration command results and their 74 streams were hash-checked. The signal profile settled on `CellSignalStrengthWcdma`, level 4. Battery and APK/resources were not modified.

The separate normal-animation helper then executed and verified its exact nineteen-command sequence, including fresh `settings get` results showing `animator_duration_scale`, `window_animation_scale` and `transition_animation_scale` all equal to `1`. Its sequence finished before either app launched. Both captured starting environments also report all three values as `1`. Because capture stopped early, no ending environment was recorded. [Raw scale evidence](extracted/animation-settings/animation-scales.json) and the [configuration replay summary](analysis/replay/verified-configuration-summary.json) retain that scope.

## All retained TRIGGERS attempts

The original retained five complete frames. Its sixth attempt began, but `uiautomator dump` timed out as the thirty-second acquisition deadline expired; no sixth complete PNG/XML observation exists. The failed ledger lasted **30.003975 seconds** and reports `Observed command deadline expired before execution`. The candidate retained all six complete frames, then reports `No consecutive identical full frames within six attempts`; its ledger lasted **23.422514 seconds**. These are the actual two failure paths.

Times below are seconds after that APK's Next command completed. The interval covers PID/foreground, hierarchy, screenshot and final PID/foreground acquisition; it is not a claim that all pixels were rendered at one exact timestamp.

| APK | Frame | Observation began after tap | Observation ended after tap | Observation duration |
| --- | ---: | ---: | ---: | ---: |
{chr(10).join(rows)}

All complete observations remained in the same single app PID and `com.arlosoft.macrodroid.intro.IntroActivity` within each APK's attempt. The retained [original ledger](extracted/journey/original-intro-2-acquisition-1-settling.json) and [candidate ledger](extracted/journey/candidate-intro-2-acquisition-1-settling.json) contain every completed attempt; raw command logs also preserve the original timeout.

## Full-frame measurements

Every PNG is 720×1280. The actual XML identifies `lottieAnimationView` at **[0,531,720,1011)** and `indicator` at **[128,1184,592,1200)**. The moving clock hands are visible in the unmodified full images. These regions were used only to describe already-measured full-frame differences. They are not masks, acceptance crops, tolerance regions or frame-selection criteria.

| APK | Consecutive frames | Changed full-frame pixels | Difference bounding box |
| --- | --- | ---: | --- |
{chr(10).join(difference_rows)}

All 55 possible pairings among the eleven retained frames were measured: ten original-with-original, fifteen candidate-with-candidate and thirty cross-APK pairs. **All 55 differ, and every changed pixel is inside the actual Lottie view.** No frames were chosen by similarity to the other APK. This exhaustive cross-APK diagnostic matrix records full-frame changed pixels; its independently timed rows cannot establish animation timing equivalence.

| | Candidate 1 | Candidate 2 | Candidate 3 | Candidate 4 | Candidate 5 | Candidate 6 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(matrix_rows)}

All eleven XML files are byte-identical (`840d3f966746dea5dffe838eda7b46b0c7f48ee37b59d33cbcb28336f199dfd8`). The whole observed indicator region also has exactly one RGBA hash (`4726a3e2979323e8aa6f02bbfdc213644cfda00f8a2ba07a637a089befc8d299`), including the earlier 26-pixel difference rectangle [313,1184,352,1200). The stable indicator rendering in this separate scale-one run does not erase or explain away the actual scale-zero failure.

The [complete measurement JSON](analysis/frame-measurements.json) records every frame's raw PNG/XML hashes, absolute and relative timing, all 55 full-frame pixel counts, exact exclusive bounds, maximum RGBA differences and changed-row counts. It verifies all 952 raw files before and after measurement. The [compact summary](analysis/analysis-summary.json) records the finite conclusion.

| Unmodified retained example | Image | Hierarchy |
| --- | --- | --- |
{chr(10).join(gallery)}

## Consequence and limits

This measured scale-one run could not satisfy the unchanged full-frame stability rule on TRIGGERS while the clock animation continued. A proposed twelve-screen run using the same setting therefore remains inactive. A separately declared still-frame configuration may be assessed in a new run while preserving these originals and the earlier scale-zero failure. No screenshot normalization, timing-based cross-APK selection, pixel tolerance or app/resource change was introduced here.

The evidence establishes a failed, bounded diagnostic plus an exact intro-1 still. It does not establish ten-screen parity, animation timing parity, crash-free execution, a completed notification boundary, macro creation/execution or full 1:1 runtime behavior.

## Reproduction

The frozen [measurement program](analysis/operations/analyze_frames.py), [literal-source replay program](analysis/operations/replay_frozen_evidence.py), [exact extractor](analysis/operations/extract_run.py) and [freezer](analysis/operations/freeze_analysis.py) are retained. The replay uses private hardlinks only for fixed read inputs and a separate writable result inode; all raw evidence and both APKs are rehashed afterward. Its temporary tree was removed after the successful offline replay. The [actual replay log](analysis/replay.stdout.log) records its result. Run these programs on an extracted copy of the pinned archive, with the exact 8433/9108 APKs and new empty output directories.
'''
    (OUT / 'README.md').write_text(readme)
    mappings = {
        'analysis/frame-measurements.json': BASE / '01-full-frame-measurements/frame-measurements.json',
        'analysis/github-final-metadata.json': BASE / 'github-final-metadata.json',
        'analysis/replay.stdout.log': BASE / '02-frozen-replay.stdout.log',
    }
    for name in ['extract_run.py', 'analyze_frames.py', 'replay_frozen_evidence.py', 'freeze_analysis.py']:
        mappings['analysis/operations/' + name] = BASE / name
    for source in (BASE / '02-frozen-replay').iterdir():
        assert source.is_file()
        mappings['analysis/replay/' + source.name] = source
    for target, source in mappings.items():
        destination = OUT / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        assert identity(source) == identity(destination)
    # Every evidence link points either to this capsule or an exact raw member.
    for target in re.findall(r'\]\(([^)]+)\)', readme):
        if target.startswith('https://') or target in ('manifest.json', 'extraction-receipt.json', 'extracted/'):
            continue
        path = RAW / target.removeprefix('extracted/') if target.startswith('extracted/') else OUT / target
        assert path.is_file(), target
    forbidden = re.compile(rb'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}')
    files = []
    for path in sorted(OUT.rglob('*')):
        if path.is_file():
            assert not forbidden.search(path.read_bytes()), path
            files.append({'path': path.relative_to(OUT).as_posix(), **identity(path)})
    checkpoint = {
        'schema': 1, 'status': 'FROZEN_FAILED_NORMAL03_ANALYSIS',
        'created_utc': datetime.now(timezone.utc).isoformat(), 'repo_target': TARGET,
        'run_id': 38212813248, 'head_sha': summary['head_sha'], 'raw_archive': receipt['archive'],
        'raw_members_are_preserved_separately_unchanged': True,
        'active_files': [], 'files': files,
    }
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
                      'files': len(files), 'logical_bytes': sum(row['bytes'] for row in files),
                      'repo_target': TARGET, 'active_files': []}, indent=2))


if __name__ == '__main__':
    main()
