# Measured Android capture contract

The runtime tools compare the supplied MacroDroid 5.67.8 original with the committed reconstructed candidate on one explicitly selected disposable device. A passing report establishes only its named capture scope. It does not establish whole-application behavior or animation parity.

## Actual measurements so far

The hosted run at source commit `ba52fd6` installed and launched both APKs on the pinned API 35 emulator with ARM64 translation. Both remained alive and foreground for the captured interval. Their complete UI hierarchies were byte-identical, with 16 application-owned nodes. The 720 × 1280 screenshots differed in 75 decoded pixels, all inside Android's signal-strength icon at x=614..630, y=17..33 inclusive. The comparator correctly returned `CAPTURE_DIFFERENCE`.

The next hosted run at source commit `bebf448` stopped at device configuration, before app installation. Its old gate required identical raw signal measurements even when Android's computed signal level remained 4. The corrected helper requires a stable primary radio type and computed level while retaining the varying raw observations. A new device run must measure the effect of this correction.

Both complete failed artifacts and their analyses are retained under `docs/verification/android-ci-ba52fd6/` and `docs/verification/android-ci-bebf448/` in the repository. The successful 16-command source acceptance for the 1,238-body candidate is separately preserved under `docs/verification/source-ci-bebf448/`. Host source acceptance is not a device result. The four-page recorder described below has synthetic regression coverage; no four-page device result is claimed by this source checkpoint.

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

## Declared device settings

The hosted orchestration uses `configure_capture_device.py` from `tools/android/`. It verifies the expected disposable AVD, stabilizes the real primary radio type and computed level, enables SystemUI demo mode, and requests a displayed clock of 12:00. The device's actual wall clock and battery readings remain recorded. Demo mode can hold other status indicators at their entry state.

For this still-capture scenario, the orchestration explicitly requests `--disable-animations`. The helper records and verifies zero for `animator_duration_scale`, `window_animation_scale`, and `transition_animation_scale` before either APK starts. The recorder includes all three values and both SystemUI demo settings in each APK's environment record. The original intro layouts use looping Lottie animations; the original drawable responds to the system animation scale. Direct disassembly of the supplied APK verified the relevant recovered Lottie source byte-for-byte. The complete source analysis and original-file hashes are recorded in `docs/verification/android-environment/lottie-still-capture-analysis.json`.

These are full-page still comparisons under explicitly reduced system animation settings. Animated frame sequences, transition timing, frame rate, scheduling, permission behavior, and features beyond the intro are untested by this scenario. A match must not be described as full 1-to-1 acceptance.

## Run and preserve the outcome

On an already configured disposable ARM64 environment with ADB available:

```sh
python3 android_acceptance.py \
  --serial DISPOSABLE_SERIAL \
  --original /absolute/path/to/original.apk \
  --candidate dist/MacroDroid-5.67.8-v9-hybrid.apk \
  --accept-package-data-removal \
  --intro-pages \
  --output reports/new-intro-capture
python3 android_compare.py reports/new-intro-capture
python3 android_intro.py reports/new-intro-capture
```

The recorder does not configure animation or demo settings itself. `tools/android/run_ci_runtime.py` creates the declared environment, runs both comparisons, requires their actual successful exits and results, and stops only its own emulator. Successful and failed results retain their commands, device configuration, APK identities, complete captures, and comparison reports. Synthetic test fixtures exercise rejection behavior; they are never Android execution evidence.
