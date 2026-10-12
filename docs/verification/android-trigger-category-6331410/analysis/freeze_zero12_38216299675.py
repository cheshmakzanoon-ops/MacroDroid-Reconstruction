#!/usr/bin/env python3
"""Freeze the closed zero-scale twelve-screen replay without duplicating raw payloads."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent
RESULT = BASE / 'zero12-run-38216299675-analysis'
RAW = BASE / 'zero12-run-38216299675-extracted'
OUT = BASE / 'checkpoints/05-zero12-actual-five-pixel-failure'


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def link_checked(source, relative):
    assert source.is_file() and not source.is_symlink(), source
    expected = identity(source)
    target = OUT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    os.link(source, target)
    assert identity(target) == expected


def main():
    result = json.loads((RESULT / 'independent-zero12-analysis.json').read_text())
    frames = json.loads((RESULT / 'frame-and-selector-observations/result.json').read_text())
    assert result['status'] == 'EXACT_COMPLETE_ZERO12_EVIDENCE_REPLAYED_WITH_FIVE_PIXEL_INTRO_DIFFERENCE'
    assert result['evidence_valid'] and not result['journey_equal']
    assert result['full_rgba_pixel_vector'] == [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert frames['status'] == 'RECORDED_ZERO12_STILL_FRAMES_AND_OBSERVED_SELECTORS_VERIFIED'
    assert frames['within_variant_changed_pixels'] == [0] * 12
    assert frames['cross_variant_changed_pixels'] == [5] * 16
    OUT.mkdir(parents=True, exist_ok=False)
    for source in sorted(RESULT.rglob('*')):
        if source.is_file():
            link_checked(source, source.relative_to(RESULT))
    extra = {
        'freeze_zero12_38216299675.py': Path(__file__).resolve(),
        'extract_artifact.py': BASE / 'extract_artifact.py',
        'replay.stdout.log': BASE / 'zero12-38216299675-replay.stdout.log',
        'inspect_zero12_frames_and_selectors.py': BASE / 'inspect_zero12_frames_and_selectors.py',
        'frame-selector.stdout.log': BASE / 'zero12-frame-selector.stdout.log',
        'artifact-metadata.json': BASE / 'zero12-artifact-metadata.json',
        'github-final-dbcad-source-and-zero12.json': BASE / 'github-final-dbcad-source-and-zero12.json',
        'original-extraction-receipt.json': BASE / 'zero12-run-38216299675-extracted-extraction.json',
    }
    for relative, source in extra.items():
        link_checked(source, relative)
    lifecycle = []
    for variant in ('original', 'candidate'):
        boundary_path = RAW / 'journey' / f'{variant}-notification-boundary.json'
        boundary = json.loads(boundary_path.read_text())
        link_checked(boundary_path, f'lifecycle/{variant}/notification-boundary.json')
        streams = []
        for command in list(boundary['commands'].values()) + list(boundary['after_diagnostics'].values()):
            assert command['returncode'] == 0 and not command['timed_out']
            for stream in ('stdout', 'stderr'):
                declared = command[stream]
                source = RAW / 'journey' / declared['path']
                assert identity(source) == {key: declared[key] for key in ('bytes', 'sha256')}
                link_checked(source, f'lifecycle/{variant}/{declared["path"]}')
                streams.append(declared)
        crash_stream = boundary['after_diagnostics']['crash']['stdout']
        lifecycle.append({
            'variant': variant,
            'old_pid': boundary['old_pid'],
            'new_pid': boundary['new_pid'],
            'outcome': boundary['outcome'],
            'raw_crash_stream': crash_stream,
            'raw_streams_checked': streams,
            'literal_raw_crash_output_preserved': True,
            'literal_crash_messages_claimed_equal': False,
        })
    (OUT / 'recorded-process-boundaries.json').write_text(json.dumps(lifecycle, indent=2) + '\n')
    pairs = json.loads((RESULT / 'all-twelve-full-frame-pairs.json').read_text())
    table = []
    for pair in pairs:
        name = pair['name']
        left = pair['original']['artifacts']['screenshot']['path']
        right = pair['candidate']['artifacts']['screenshot']['path']
        table.append(f'| {name} | {pair["changed_rgba_pixels"]} | Yes | [original](review-captures/{left}) / [candidate](review-captures/{right}) |')
    (OUT / 'README.md').write_text('''# Zero-scale twelve-screen run: exact evidence replay, five-pixel failure

Both apps complete all twelve declared screens, including the expanded Date/Time trigger category. **The full journey comparison fails because five pixels differ on the TRIGGERS introduction page.** All twelve hierarchy files match byte for byte, and the other eleven full PNGs match byte for byte. No mask, crop, pixel tolerance, or cross-app frame selection was used.

This is [run 38216299675](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38216299675), job `114701722464`, commit `6331410cfd2391389270564803623079e8355ad8`. The installed original is SHA256 `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`; the installed candidate is SHA256 `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`. The workflow changes only the disposable-device observation procedure and uses the already published candidate. The exact APK and complete frozen workflow input identities are rechecked by the preserved final verifier.

## Full-frame results

| Declared screen | Changed RGBA pixels | Exact XML bytes | Complete unmodified screenshots |
| --- | ---: | --- | --- |
''' + '\n'.join(table) + '''

The actual final status is `TRIGGER_CATEGORY_TWELVE_SCREEN_DIFFERENCE`, with `evidence_valid=true` and `journey_equal=false`. The comparison reports `catalog_navigation_established=true` and `trigger_selected=false`. The final independent verifier reproduces that result; its nonzero result is a retained visual failure. Both journey records are complete, with twelve captures and eleven inputs each. No input follows the Date/Time category capture.

The five changed coordinates are `(317,1186)`, `(319,1189)`, `(335,1192)`, `(319,1194)`, and `(336,1195)`, inside exclusive bounds `[317,1186,337,1196)`. Their exact original/candidate RGBA values are retained in [all twelve full-frame pairs](all-twelve-full-frame-pairs.json). They lie in the existing introduction page indicator region; this observation does not identify a new app-source cause. The previous runs and their different measured pixel counts remain separate evidence.

All 46 acquisition ledgers accept the first two consecutive identical full PNG/XML frames. The diagnostic verifies 552 physically distinct observation artifacts. Four retained TRIGGERS frames per app include the accepted screen and the fresh pre-input capture. All twelve within-app frame-pair comparisons contain zero changed pixels; all sixteen cross-app combinations retain exactly five changed pixels. The complete timings, identities and frame comparisons are in [the frame diagnostic](frame-and-selector-observations/result.json), [all 46 ledgers](frame-and-selector-observations/all46-stabilization-ledgers.json), and [all 28 pair comparisons](frame-and-selector-observations/all28-within-and-cross-trigger-frame-pairs.json). No intermediate frame was discarded to obtain equality.

## Recorded crashes and continuation

Both apps retain an actual Java fatal exception during the notification-denial boundary: `java.lang.IllegalStateException` from `android.app.Fragment.getResources`, reached through `com.zx.lbua80.onShow`. The original process changes from PID 4191 to 5414, and the candidate from PID 7055 to 8118. The guarded boundary verifies the old PID is absent in both process lists, verifies the new single process and expected `NewHomeScreenActivity`, and obtains a fresh installed-APK hash before continuing.

The [recorded process-boundary summary](recorded-process-boundaries.json) links the exact command outputs, boundary records and literal crash buffers. The candidate buffer also retains earlier buffer contents; the recorded policy classifies the newly observed exception. Object identifiers and literal crash messages have not been normalized in those raw outputs. The paired continuation classification is equal, but no claim of equal literal crash messages or a crash-free run is made. `crash_free_run_established=false` remains explicit.

## Observed Date/Time category and next-step boundary

The final screen is foreground `com.arlosoft.macrodroid/com.arlosoft.macrodroid.selectableitemlist.AddTriggerActivity`. Both complete PNGs have SHA256 `7057b96a46d56c0e53a3b42a3475a24812b5867a753bcf81b528e9a8a6aefa92`; both XMLs have SHA256 `9bb3a60891fc9194b2f9ae493e513a041a6ee2e395125c13dbeb8cef648abcd0`.

The actual hierarchy contains seven enabled clickable rows: Calendar Event, Day of Week/Month, Day/Time, Regular Interval, Stopwatch, Sunset/Sunrise, and System Time. The `Day/Time` text node has resource ID `com.arlosoft.macrodroid:id/select_item_name` and is not itself clickable. Its unique enabled clickable ancestor is `com.arlosoft.macrodroid:id/select_item_row_frame`, with bounds `[14,574][354,678]`. Its center would be `(184,626)` for a future input after fresh identity/PID/component/XML guards. This run did not select that row or create, save, or execute a macro. The exact original and candidate selectors and all visible row bounds are preserved in [observed rows](frame-and-selector-observations/observed-date-time-category-rows.json).

## Device configuration and complete replay

The device configuration finishes with primary WCDMA signal level 4 after a 15.329-second stable interval and a declared SystemUI demo clock of `1200`. All 36 configuration commands and their 72 output hashes are verified. A separate explicit nineteen-command helper sets and verifies `animator_duration_scale`, `window_animation_scale`, and `transition_animation_scale` to `0`. All original/candidate before/after recorded environments match. The actual commands and observations remain in the raw evidence and [configuration summary](configuration-summary.json). This still-frame configuration does not establish animation timing parity.

The independent replay reconstructs all 192 expected input-copy roles from the pinned preparer, rather than trusting a mutable preflight row list. It verifies all 2,944 raw files before and after replay, all 46 capture ledgers and 92 observations, and 2,498 unique referenced journey artifacts. It replays the exact pinned final verifier and captured comparator, matching both result objects except the explicitly fresh verification timestamp. A private hardlink view is used for the large immutable inputs; the generated final report has a distinct inode, and the view is removed afterward. No original archive, APK, source, screenshot, or runtime record is modified.

The actual hosted logs contain 130 guard-test successes in 37.469 seconds, ten zero-scale helper successes in 0.209 seconds, and six downloader successes in 0.004 seconds. The job's bounded owned-service cleanup succeeds despite the visual failure. The complete result, import pins, all member identities, reconstructed inventory, observation records, host-test summaries and actual replay logs accompany this README. This evidence establishes neither complete high-level source reconstruction nor full runtime 1:1.

## Original archive and explicitly labeled review log

Artifact `11732104868` is exactly 42,199,893 bytes, SHA256 `1ea3ad6302d53c2fcc8341c03deec7ccd04d729facaf5658acb87e4aebc6f4b3`. Its 2,944 members total 65,045,879 bytes. The publisher preserves the whole unchanged ZIP through the parent directory's manifest and all unchanged members under `../extracted/`; the [complete member identities](all-2944-member-identities.json) and [original extraction receipt](original-extraction-receipt.json) bind them. No second raw archive or APK copy is created by this freeze.

The raw emulator boot log contains one ephemeral ADB public-key value. The original log and ZIP are preserved unchanged; public material alone is not a private credential. Only the clearly labeled [review-log copy](emulator-boot-public-value-omitted.review.log) omits that one value for readability, with the exact one-line transformation and both hashes in [its receipt](review-log-transformation.json). The extractor's documented scan of every member found no matching private-key pattern; that statement is limited to the actual scan, not a universal secret audit. The public value is not repeated in this summary.

This is an additive evidence capsule with no active-file changes. Existing complete analysis and selected raw review files are hardlinked during the local freeze to avoid duplicate payload allocation under disk pressure. Their exact content hashes are frozen in `checkpoint.json` and are not edited afterward.
''')
    files = [{'path': p.relative_to(OUT).as_posix(), **identity(p)}
             for p in sorted(OUT.rglob('*')) if p.is_file()]
    checkpoint = {
        'schema': 1,
        'status': 'FROZEN_COMPLETE_ZERO12_EVIDENCE_WITH_FIVE_PIXEL_FAILURE',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'repo_target': 'docs/verification/android-trigger-category-6331410/analysis',
        'run_id': 38216299675,
        'head_sha': result['head_sha'],
        'active_files': [],
        'raw_archive': result['archive'],
        'original_raw_evidence_modified': False,
        'hardlinks_used_for_closed_review_files': True,
        'files': files,
    }
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'),
                      **identity(OUT / 'checkpoint.json'),
                      'files': len(files), 'bytes_total': sum(r['bytes'] for r in files),
                      'repo_target': checkpoint['repo_target']}, indent=2))


if __name__ == '__main__':
    main()
