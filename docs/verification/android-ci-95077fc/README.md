# Exact cold launch and four intro page stills — `95077fcb`

The Android job for source checkpoint `95077fcb1d3c86f3b1c91026619642d99198f149` completed successfully on 12 October 2026. It installed the original APK and the current candidate in turn, verified each installed APK's SHA-256 on the device, and recorded the cold launch plus all four English intro pages. Each pair of complete 720 × 1280 screenshots and UI hierarchy files is byte-identical. All three recorded Next-button transitions also match.

This establishes the declared cold-launch and intro-still scope on the recorded emulator configuration. It does not establish complete application, feature, or animation parity. Both comparison reports retain those explicit limitations.

## Provenance

| Item | Recorded identity |
| --- | --- |
| Source checkpoint | `95077fcb1d3c86f3b1c91026619642d99198f149` |
| Workflow run | [38194498356](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38194498356) |
| Android job | `114634085047`, conclusion `success` |
| GitHub artifact | [11723551688](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38194498356/artifacts/11723551688) |
| Artifact archive | 803,571 bytes; 296 files; 1,846,979 uncompressed bytes |
| Archive SHA-256 | `0f82b5480cf7a3d38c766cfed81a9a2f47087e057d03329c7953cb8df5608739` |
| Original APK | 95,725,918 bytes; `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800` |
| Candidate APK | 94,683,342 bytes; `be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce` |

The downloaded archive hash matches GitHub's artifact digest. All 296 extracted files were checked byte for byte against the archive. The original evidence is retained unchanged alongside the archive part, its manifest, and its extraction receipt. This README and [independent-capture-analysis.json](independent-capture-analysis.json) are derived analysis, separate from the original CI files.

The APK preflight and installed identities are recorded in [capture/result.json](capture/result.json). Both packages report MacroDroid 5.67.8, version code `896700008`, minimum SDK 23 and target SDK 36. The original and candidate are distinct APKs; each observed device-side installed hash matches its own prevalidated input.

## Measured comparisons

[capture/cold-launch-comparison.json](capture/cold-launch-comparison.json) reports `EXACT_COLD_LAUNCH_MATCH_ONLY`. [capture/intro-comparison.json](capture/intro-comparison.json) reports `EXACT_FOUR_PAGE_INTRO_MATCH_ONLY`.

| Page | Original capture | Candidate capture | Changed pixels | Paired PNG/XML bytes | App-owned UI nodes |
| --- | --- | --- | ---: | --- | ---: |
| MACRODROID / cold launch | [original.png](capture/original.png) | [candidate.png](capture/candidate.png) | 0 | Identical / identical | 16 / 16 |
| TRIGGERS | [original-intro-2.png](capture/original-intro-2.png) | [candidate-intro-2.png](capture/candidate-intro-2.png) | 0 | Identical / identical | 18 / 18 |
| ACTIONS | [original-intro-3.png](capture/original-intro-3.png) | [candidate-intro-3.png](capture/candidate-intro-3.png) | 0 | Identical / identical | 18 / 18 |
| CONSTRAINTS | [original-intro-4.png](capture/original-intro-4.png) | [candidate-intro-4.png](capture/candidate-intro-4.png) | 0 | Identical / identical | 18 / 18 |

Each image comparison covers all 921,600 pixels, including the status and navigation bars. The checks use no masks, crops, resizes, ignored app attributes, or pixel tolerance. PNG color metadata also matches.

For each APK, the recorder observed `com.arlosoft.macrodroid:id/button_next` in a fresh UI hierarchy before each input, checked that the target intro activity remained foreground and the process stayed alive, and tapped the observed center `(640, 1152)`. The six input preconditions were approximately 2.09–2.23 seconds old. The recorder captured three distinct transitions and four distinct titled pages. The final Done/checkmark button was not pressed in this run.

An independent read-only check verified 202 recorded artifact references covering 186 distinct files. It called both comparison functions again using source files verified against the published checkpoint; both results reproduced the complete CI JSON reports. A separate Pillow RGBA decode found zero changed pixels for every pair. The complete PNG files and complete hierarchy XML files were additionally checked for byte equality. The four original images were visually inspected; the candidate image bytes are identical to those inspected originals. These checks are recorded in the derived analysis file, without rewriting the CI reports.

## Controlled device state

The disposable API 35 Android emulator used hardware acceleration and booted in 42.082 seconds. Its recorded ABI list is `x86_64,arm64-v8a`; `libndk_translation.so` supplies the native bridge, with `ro.dalvik.vm.isa.arm64=x86_64`. The display is 720 × 1280 at density 320, font scale 1.0, timezone `Etc/UTC`. Both captures have identical environment records. The visible intro text is English; the recorded `persist.sys.locale` property is empty.

[capture-device/capture-device.json](capture-device/capture-device.json) records successful preparation before either app launch:

- Emulator console commands set home voice/data registration and signal profile 4. The primary radio changed from LTE to WCDMA. WCDMA's computed level remained 4 for 15.108 seconds before acceptance, while the raw measured signal changed from −55 to −57 dBm. The complete raw observations remain in the artifact. The corrected gate checks the primary radio type and computed level; it does not require all raw measurement fields to be constant.
- The helper set `animator_duration_scale`, `window_animation_scale`, and `transition_animation_scale` to `0` and verified every readback. Their previous stored values were `null`, `1.0`, and `1.0`, respectively. The same three zero values are recorded in both app capture environments.
- The helper set `sysui_demo_allowed=1` and `sysui_tuner_demo_on=1`, observed `isInDemoMode=true` and `isDemoModeAllowed=true` from SystemUI, and sent the clock demo command with `hhmm=1200`. Every observed screenshot displays 12:00. Both demo settings are recorded in both capture environments. SystemUI demo mode can also hold other status indicators at their entry state.
- The helper did not alter either APK, app resources, screenshot data, the battery, or the actual device wall clock. The wall clock advanced normally from 02:25:52 to 02:26:19 UTC during preparation. Battery state remained unchanged at 100% with AC charging.

The device helper completed in 27.739 seconds. Original/candidate recording took 98.382 seconds. Both strict comparisons returned exit code 0, and the runtime service stopped with exit code 0. [runtime-run.json](runtime-run.json) preserves the commands, durations, report hashes, and complete outcome flags.

The declared zero-animation configuration permits reproducible still captures. [The original-APK Lottie analysis](../android-environment/lottie-still-capture-analysis.json) records why these settings affect the bundled intro animations. This run does not compare animation timing or motion. No source or screenshot adjustment was used to force the images to match.

## Evidence handling and remaining scope

The CI sanitizer omitted two emulator diagnostic lines containing generated ADB key material before artifact upload. A pattern-based review of all 296 downloaded files found no matches for the tested ADB key settings, private-key headers, standalone SSH public-key lines, or GitHub token prefixes. The temporary download URL was not persisted. The downloadable artifact itself was not modified after retrieval.

There was one fresh installation per APK in this workflow job and one recorded emulator configuration. Final intro completion, the first landing dialog, app home, permissions, macro execution, background services, persistence, sensor events, other screens, locales, devices, and animation behavior remain outside this result. The earlier status-icon difference and signal-preparation failure remain preserved as failed runs in their own evidence directories.

The source-build job is a separate workflow job. This Android evidence does not imply a source-build result; use that job's own preserved acceptance reports for its outcome.
