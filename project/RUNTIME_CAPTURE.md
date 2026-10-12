# Measured Android capture contract

The runtime tools compare the supplied MacroDroid 5.67.8 original with the committed reconstructed candidate on one explicitly selected disposable device. A passing report establishes only its named capture scope. It does not establish whole-application behavior or animation parity.

## Actual measurements so far

Hosted run `38194498356`, at source commit `95077fcb1d3c86f3b1c91026619642d99198f149`, successfully installed and launched the exact original and reconstructed candidate on the pinned API 35 Google APIs x86_64 emulator with ARM64 translation. Device-side `base.apk` hashes matched the prevalidated local inputs before either launch. The original was 95,725,918 bytes, SHA-256 `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`; the tested 1,239-body hybrid was 94,683,342 bytes, SHA-256 `be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce`. These identities and the complete recorded command evidence are preserved in the [successful capture archive][android-success] and [recorder result][recorder-success].

The strict reports returned `EXACT_COLD_LAUNCH_MATCH_ONLY` and `EXACT_FOUR_PAGE_INTRO_MATCH_ONLY`. All four 720 × 1280 PNG pairs and all four complete UI XML pairs were byte-identical. Independent RGBA comparison found **zero changed pixels on each page**, including the system bars, and reproduced both comparator reports. The original and candidate completed the three observed Next transitions. This is actual device evidence for the declared English still-capture scenario, recorded with the real signal configuration, SystemUI demo clock and zero animation scales described below. See the [cold report][cold-success], [four-page report][intro-success] and [independent verification][independent-success].

The earlier hosted run at source commit `ba52fd6` installed and launched both APKs but reported `CAPTURE_DIFFERENCE`: the complete hierarchies matched, while 75 screenshot pixels differed inside Android's signal-strength icon. The subsequent `bebf448` run stopped before app installation because its configuration gate required identical raw signal measurements despite a stable computed level. Both failures remain unchanged in their [first comparison archive][signal-failure] and [configuration-failure archive][configuration-failure]. The successful `95077fcb` run measured the corrected primary-radio/level gate on the real emulator; it did not replace the failed records.

The [separate source acceptance archive][source-success] records all 16 source/host gates for `95077fcb`; those gates are distinct from the Android measurements. The installed-identity, cold and four-page results belong to the exact APK pair above. **The newly added `--post-intro` capture and independent ART constructor probe remain pending, as do device results for later candidate identities.** No full-app, animation, home-feature or permission-choice parity is established.

## Cold-capture prerequisites

`android_acceptance.py` requires a new or empty output directory and writes a current non-success report before issuing any ADB command. It selects only the explicit serial. The default refuses physical devices, and the selected environment must advertise ARM64 support. Both APKs pass ZIP structure/CRC, package/version/SDK metadata, distinct-identity, and original-file SHA-256 validation before the first package removal.

For each APK, the recorder removes the known target package and verifies absence. It requires a clean absence query, an actual successful installation, and the installed monolithic `base.apk` path. It then hashes that file on the device and requires the checksum to equal the prevalidated local input before launching. Package paths, checksum outputs, install diagnostics, and capture artifacts are retained with byte counts and SHA-256 hashes.

Completed cold captures require a successful activity start, stable nonempty process IDs sampled at separated times and again after collection, the target foreground activity, application-owned UI nodes, and a valid complete PNG. Foreground parsing honors the highest-priority resumed-activity field; a lower app activity cannot override a different `topResumedActivity`. A device/settings change rejects the capture.

`android_compare.py` validates those recorded prerequisites before comparing all decoded RGBA pixels, PNG color metadata, and every UI XML attribute and child ordering. No image region, dynamic text, attribute, or difference threshold is ignored. Schema 3 requires the installed-file checksum and both APK preflight records. Historical schema-2 evidence remains readable but cannot claim installed-file checksum verification or satisfy the intro comparator.

## Four English intro pages

The optional `--intro-pages` flow captures the following sequence. These titles come from the original preserved intro layouts and default strings; each title must occur in the unique application `titleText` node.

| Page | Required title | Input after capture |
| --- | --- | --- |
| 1 | `MACRODROID` | Observed enabled Next button |
| 2 | `TRIGGERS` | Observed enabled Next button |
| 3 | `ACTIONS` | Observed enabled Next button |
| 4 | `CONSTRAINTS` | None |

The anchors are `source/android/res/layout/fragment_welcome_onboard.xml`, `fragment_trigger_onboard.xml`, `fragment_action_onboard.xml`, `fragment_constraint_onboard.xml`, and `source/android/res/values/strings.xml`. Their application order is preserved in `source/smali/classes3/35/IntroActivity_358c0b9ba8db2248.smali`.

Before each of the three taps, the recorder collects a fresh hierarchy, checks it against the previous captured page, resamples the original process ID, and observes `IntroActivity` as the top foreground activity. The precondition must be at most ten seconds old. The tap coordinates are derived from the unique, enabled, clickable `com.arlosoft.macrodroid:id/button_next` node's observed on-screen bounds. The evidence records the selector, fresh artifacts, age, coordinates, exact shell argument list, exit code, stdout, and stderr. Any mismatch or command diagnostic prevents a successful transition.

Each subsequent page must preserve the original process, remain in the intro activity, expose its expected distinct title, and retain the same recorded device settings. The comparator binds all five first-page process/foreground/XML/PNG artifacts to the actual cold capture and validates every later page and transition. It compares the complete screenshots and XML for all four pages. No final-page action, account entry, consent, or permission prompt is part of this sequence.

A failed intro sequence preserves a fully completed cold capture as a separate measured result. The recorder still exits unsuccessfully if either requested sequence is incomplete. `EXACT_FOUR_PAGE_INTRO_MATCH_ONLY` requires both complete sequences, matching three input targets, matching four full captures, and a matching cold capture.

## First surface after completion — pending

The separate optional `--post-intro` flag requires `--intro-pages`. Before acting on the fourth page, the recorder again observes the installed APK path and SHA-256, unchanged device settings, a fresh complete `CONSTRAINTS` hierarchy, the same live process, and foreground `IntroActivity`. The fresh precondition must be no more than ten seconds old. The already recorded fourth-page hierarchies expose the same enabled, clickable `button_next` ImageButton with description `Next`. Its center is derived again from the fresh observed bounds. See the [recorded final-page hierarchy][final-page].

The recorder issues **exactly one** completion tap, then saves the resulting full PNG, hierarchy, foreground and process evidence before classifying the surface. It accepts the app's `NewHomeScreenActivity` as an observed landing surface, or Android's notification-permission activity with the expected MacroDroid notification message and both permission controls. It makes **zero permission choices** and does not dismiss app dialogs. An unexpected surface fails this scope while preserving its initial captured evidence.

`android_post_intro.py` revalidates the fresh completion input, installed identity, process continuity, before/after environment and stable resulting hierarchy/foreground. It compares the entire PNG and XML, including a system-owned permission prompt if that is the observed surface. `EXACT_POST_INTRO_SURFACE_MATCH_ONLY` additionally requires the prior full intro comparison to pass. A matching landing surface does not establish working home features. Host controls cover this new flow, but its actual device result is still pending.

A later post-intro failure retains completed cold and four-page evidence under `COLD_AND_INTRO_CAPTURES_RECORDED_POST_INTRO_INCOMPLETE`. The two earlier comparators may report their actual narrower success while the requested post-intro capture and overall recorder exit remain unsuccessful.

## Independent ART constructor probe — pending

The repository's `tools/android/android_constructor_probe.py` runs a separate, pinned single-class DEX against the unchanged original APK. The 1,436-byte probe has SHA-256 `85f53ad51a1a85fd2161bd485db9f12556f737b0745f6e26ffdff31a927d5281`; its provenance binds the [frozen constructor Java/D8/roundtrip checkpoint][constructor-proof]. It contains no compile-only stub classes. The original APK supplies the real application classes. This probe installs no app, changes no app resource and makes no UI interaction.

Before execution, the helper checks the local original/probe identities and the selected pinned disposable emulator, pushes both files into a fresh owned temporary directory, makes them read-only, and verifies their device-side hashes. It invokes Android 15 ART with `-Xverify:all` and a bounded guest timeout. A successful allocation requires the exact output `CONSTRUCTOR_ALLOCATION_OK class=zhh arity=2`, a zero exit and no ART error; cleanup is checked separately. Raw commands, outputs and the actual VM identity are retained in `constructor-probe/probe-result.json` and its referenced files.

This scope concerns one `Lzhh;` allocation through the original public `Lrff;` constructor. It does not execute a reconstructed Widget flow or establish Widget behavior. Actual ART execution is pending. The CI driver keeps its result independent: an ART failure still permits the app captures and all three comparators, while a later capture failure preserves an already observed constructor result.

## Declared device settings

The hosted orchestration uses `configure_capture_device.py` from `tools/android/`. It verifies the expected disposable AVD, stabilizes the real primary radio type and computed level, enables SystemUI demo mode, and requests a displayed clock of 12:00. The device's actual wall clock and battery readings remain recorded. Demo mode can hold other status indicators at their entry state.

For this still-capture scenario, the orchestration explicitly requests `--disable-animations`. The helper records and verifies zero for `animator_duration_scale`, `window_animation_scale`, and `transition_animation_scale` before either APK starts. The recorder includes all three values and both SystemUI demo settings in each APK's environment record. The original intro layouts use looping Lottie animations; the original drawable responds to the system animation scale. Direct disassembly of the supplied APK verified the relevant recovered Lottie source byte-for-byte. The complete source analysis and original-file hashes are recorded in `docs/verification/android-environment/lottie-still-capture-analysis.json`.

These are full-page still comparisons under explicitly reduced system animation settings. Animated frame sequences, transition timing, frame rate, scheduling, permission behavior, and features beyond the intro are untested by this scenario. A match must not be described as full 1-to-1 acceptance.

## Run and preserve the outcome

On an already configured disposable ARM64-capable environment with ADB available, the complete requested still-capture scenario is:

```sh
python3 android_acceptance.py \
  --serial DISPOSABLE_SERIAL \
  --original /absolute/path/to/original.apk \
  --candidate dist/MacroDroid-5.67.8-v9-hybrid.apk \
  --accept-package-data-removal \
  --intro-pages --post-intro \
  --output reports/new-intro-capture
python3 android_compare.py reports/new-intro-capture
python3 android_intro.py reports/new-intro-capture
python3 android_post_intro.py reports/new-intro-capture
```

Omit `--post-intro` and its comparator to request only the already measured cold/four-page scope. The recorder does not configure animation or demo settings itself. `tools/android/run_ci_runtime.py` creates the declared environment, requests all three capture comparisons plus the independent ART probe, and stops only its own emulator. It always attempts all three comparators, including after a previous stage fails, so completed narrower evidence remains reviewable.

`requested_capture_gate_passed` requires a configured device, successful recorder exit and all three actual comparison statuses/booleans bound to the current input pair. `constructor_probe_gate_passed` requires the independently rechecked ART result, successful helper exit and completed cleanup. The overall CI gate requires both and a successful service exit; all pass fields begin false. Successful and failed results retain their commands, device configuration, APK identities, complete captures and comparison reports. Synthetic test fixtures exercise rejection behavior; they are never Android execution evidence.

[android-success]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/blob/0c5913324bcf60bacdb46554d80b3eda684dd79d/docs/verification/android-ci-95077fc/README.md
[recorder-success]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/blob/0c5913324bcf60bacdb46554d80b3eda684dd79d/docs/verification/android-ci-95077fc/capture/result.json
[cold-success]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/blob/0c5913324bcf60bacdb46554d80b3eda684dd79d/docs/verification/android-ci-95077fc/capture/cold-launch-comparison.json
[intro-success]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/blob/0c5913324bcf60bacdb46554d80b3eda684dd79d/docs/verification/android-ci-95077fc/capture/intro-comparison.json
[independent-success]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/blob/0c5913324bcf60bacdb46554d80b3eda684dd79d/docs/verification/android-ci-95077fc/independent-capture-analysis.json
[final-page]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/blob/0c5913324bcf60bacdb46554d80b3eda684dd79d/docs/verification/android-ci-95077fc/capture/original-intro-4-hierarchy.xml
[signal-failure]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/0c5913324bcf60bacdb46554d80b3eda684dd79d/docs/verification/android-ci-ba52fd6
[configuration-failure]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/0c5913324bcf60bacdb46554d80b3eda684dd79d/docs/verification/android-ci-bebf448
[source-success]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/3b2b7e8f539e746c9b99fbeb9a093bda1074fb92/docs/verification/source-ci-95077fc
[constructor-proof]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/c7abf086ebffbc70cb3143f909a7f48648de22bc/work-in-progress/constructor-owner/02-pipeline-proof
