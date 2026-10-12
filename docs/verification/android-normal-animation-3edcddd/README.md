# Normal animation diagnostic: retained clock animation, incomplete journey

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
| original | 1 | 2.001123 | 6.120884 | 4.119762 |
| original | 2 | 7.831400 | 12.010705 | 4.179306 |
| original | 3 | 13.620030 | 17.840118 | 4.220088 |
| original | 4 | 19.400280 | 23.853535 | 4.453255 |
| original | 5 | 25.386477 | 29.569699 | 4.183222 |
| candidate | 1 | 2.000889 | 4.743395 | 2.742506 |
| candidate | 2 | 5.857096 | 8.574645 | 2.717549 |
| candidate | 3 | 9.678593 | 12.458028 | 2.779435 |
| candidate | 4 | 13.638911 | 16.425305 | 2.786394 |
| candidate | 5 | 17.671872 | 20.401394 | 2.729522 |
| candidate | 6 | 21.578324 | 24.297517 | 2.719193 |

All complete observations remained in the same single app PID and `com.arlosoft.macrodroid.intro.IntroActivity` within each APK's attempt. The retained [original ledger](extracted/journey/original-intro-2-acquisition-1-settling.json) and [candidate ledger](extracted/journey/candidate-intro-2-acquisition-1-settling.json) contain every completed attempt; raw command logs also preserve the original timeout.

## Full-frame measurements

Every PNG is 720×1280. The actual XML identifies `lottieAnimationView` at **[0,531,720,1011)** and `indicator` at **[128,1184,592,1200)**. The moving clock hands are visible in the unmodified full images. These regions were used only to describe already-measured full-frame differences. They are not masks, acceptance crops, tolerance regions or frame-selection criteria.

| APK | Consecutive frames | Changed full-frame pixels | Difference bounding box |
| --- | --- | ---: | --- |
| original | 1 → 2 | 8,223 | `[228, 590, 444, 890]` |
| original | 2 → 3 | 13,973 | `[228, 583, 444, 785]` |
| original | 3 → 4 | 8,451 | `[283, 583, 440, 768]` |
| original | 4 → 5 | 13,755 | `[332, 583, 492, 785]` |
| candidate | 1 → 2 | 10,396 | `[196, 654, 404, 948]` |
| candidate | 2 → 3 | 16,181 | `[196, 639, 513, 896]` |
| candidate | 3 → 4 | 16,312 | `[229, 639, 513, 948]` |
| candidate | 4 → 5 | 10,359 | `[173, 657, 450, 948]` |
| candidate | 5 → 6 | 15,736 | `[173, 607, 477, 783]` |

All 55 possible pairings among the eleven retained frames were measured: ten original-with-original, fifteen candidate-with-candidate and thirty cross-APK pairs. **All 55 differ, and every changed pixel is inside the actual Lottie view.** No frames were chosen by similarity to the other APK. This exhaustive cross-APK diagnostic matrix records full-frame changed pixels; its independently timed rows cannot establish animation timing equivalence.

| | Candidate 1 | Candidate 2 | Candidate 3 | Candidate 4 | Candidate 5 | Candidate 6 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Original 1 | 12,272 | 12,117 | 15,374 | 16,538 | 16,325 | 12,857 |
| Original 2 | 16,418 | 15,997 | 15,058 | 13,601 | 12,948 | 12,584 |
| Original 3 | 16,217 | 15,569 | 16,115 | 16,233 | 11,926 | 10,726 |
| Original 4 | 15,632 | 15,825 | 14,338 | 15,902 | 15,441 | 6,861 |
| Original 5 | 16,437 | 16,528 | 16,131 | 16,621 | 15,888 | 11,744 |

All eleven XML files are byte-identical (`840d3f966746dea5dffe838eda7b46b0c7f48ee37b59d33cbcb28336f199dfd8`). The whole observed indicator region also has exactly one RGBA hash (`4726a3e2979323e8aa6f02bbfdc213644cfda00f8a2ba07a637a089befc8d299`), including the earlier 26-pixel difference rectangle [313,1184,352,1200). The stable indicator rendering in this separate scale-one run does not erase or explain away the actual scale-zero failure.

The [complete measurement JSON](analysis/frame-measurements.json) records every frame's raw PNG/XML hashes, absolute and relative timing, all 55 full-frame pixel counts, exact exclusive bounds, maximum RGBA differences and changed-row counts. It verifies all 952 raw files before and after measurement. The [compact summary](analysis/analysis-summary.json) records the finite conclusion.

| Unmodified retained example | Image | Hierarchy |
| --- | --- | --- |
| original frame 1 | [Full PNG](extracted/journey/original-intro-2-acquisition-1-frame-1.png) | [Full XML](extracted/journey/original-intro-2-acquisition-1-frame-1.xml) |
| original frame 5 | [Full PNG](extracted/journey/original-intro-2-acquisition-1-frame-5.png) | [Full XML](extracted/journey/original-intro-2-acquisition-1-frame-5.xml) |
| candidate frame 1 | [Full PNG](extracted/journey/candidate-intro-2-acquisition-1-frame-1.png) | [Full XML](extracted/journey/candidate-intro-2-acquisition-1-frame-1.xml) |
| candidate frame 6 | [Full PNG](extracted/journey/candidate-intro-2-acquisition-1-frame-6.png) | [Full XML](extracted/journey/candidate-intro-2-acquisition-1-frame-6.xml) |

## Consequence and limits

This measured scale-one run could not satisfy the unchanged full-frame stability rule on TRIGGERS while the clock animation continued. A proposed twelve-screen run using the same setting therefore remains inactive. A separately declared still-frame configuration may be assessed in a new run while preserving these originals and the earlier scale-zero failure. No screenshot normalization, timing-based cross-APK selection, pixel tolerance or app/resource change was introduced here.

The evidence establishes a failed, bounded diagnostic plus an exact intro-1 still. It does not establish ten-screen parity, animation timing parity, crash-free execution, a completed notification boundary, macro creation/execution or full 1:1 runtime behavior.

## Reproduction

The frozen [measurement program](analysis/operations/analyze_frames.py), [literal-source replay program](analysis/operations/replay_frozen_evidence.py), [exact extractor](analysis/operations/extract_run.py) and [freezer](analysis/operations/freeze_analysis.py) are retained. The replay uses private hardlinks only for fixed read inputs and a separate writable result inode; all raw evidence and both APKs are rehashed afterward. Its temporary tree was removed after the successful offline replay. The [actual replay log](analysis/replay.stdout.log) records its result. Run these programs on an extracted copy of the pinned archive, with the exact 8433/9108 APKs and new empty output directories.
