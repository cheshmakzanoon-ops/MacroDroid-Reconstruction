# Current reconstruction progress

The current candidate contains **1,239 recovered Java method bodies across 602
classes**, with the remaining implementation built from the preserved smali,
resources and native payload. The target remains the supplied MacroDroid 5.67.8
APK (`com.arlosoft.macrodroid`, version code `896700008`). Method counts do not
measure the percentage of complete application behavior.

**The isolated scene recovery passed its signed three-path proof and all 22
negative controls. Full acceptance of the combined scene, recorder and device
helper checkpoint is pending a fresh completed run. Whole-app 1:1 runtime parity
has not been established.**

## Current Java recovery

`source/java/recovered/ui/CustomSceneMethods.java` now supplies the executable Java
body for `CustomSceneAction.W(int, TriggerContextInfo, boolean, Stack,
ResumeMacroInfo)`. The recovery preserves permission and accessibility branches,
scene lookup and configuration, activity reuse decisions, event order, Intent
payloads, deferred dialog work and the original exception boundaries. Android
services and framework behavior remain runtime dependencies.

The isolated signed build completed these bounded checks:

| Check | Measured result |
| --- | --- |
| New scene body | 4,070 original-instruction/JVM/rebuilt-DEX cases; zero mismatches or unsupported executions |
| Original scene control-flow coverage | All 405 instructions and all 40 conditional branch edges visited |
| Complete registered host suite | 185,738 cases across 1,239 bodies and all three execution paths |
| UI suite | 15,423 cases across seven methods, with 13,555 independent expected-result checks |
| Deliberate-fault detection | All 22 controls rejected their intended defect, then the clean 15,423-case suite passed again |
| Signed APK round trip | 71,267 classes and 349,972 method definitions checked; exactly 1,239 intended body changes and zero unexpected changes |

The source, merge boundaries and precise proof scope are in
[SCENE_RECOVERY.md](SCENE_RECOVERY.md) and [UI_RECOVERY.md](UI_RECOVERY.md). The
[immutable signed scene report](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/blob/b260db63712b0049e587ef4dfe5598d1c93df1b7/work-in-progress/custom-scene/02-signed-proof-evidence/custom-scene-recovery.json)
and its complete 135-report archive retain the isolated build's evidence. Those
results do not claim that a custom scene has been exercised on Android.

The preceding `BlockTouchesAction.invokeAction(TriggerContextInfo)` recovery is
retained. Its 2,420 cases visited all 162 instructions and 30 conditional branch
edges. It contributes to the current seven-method UI suite.

## Candidate identity and reproduction

The current hybrid APK is 94,683,342 bytes with SHA-256:

`be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce`

From the repository root, run:

```sh
python3 scripts/materialize_v9.py
python3 scripts/assemble_artifact.py artifacts/current/manifest.json
```

The materializer verifies every baseline archive part and the two complete archive
hashes, extracts the full baseline, and applies the tracked `project/` overlay.
It preserves existing working directories; choose a fresh destination to make
another checkout. Inactive recovery checkpoints under `work-in-progress/` are
preserved for review and are never applied by the materializer.

Use Python 3.11+ and JDK 21, then from `workspace/MacroDroid_v9` run:

```sh
python3 release_integrity.py verify
python3 acceptance.py
```

The build entry points retain the compatibility filenames
`dist/MacroDroid-5.67.8-v9-baseline.apk` and
`dist/MacroDroid-5.67.8-v9-hybrid.apk`. The manifest, SHA-256 and source checkpoint
identify the actual candidate. The original APK is a test reference and is not
required to compile either variant.

## Previous hosted source acceptance has passed

The `source-build` job for
[GitHub Actions run 38191908311](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38191908311)
completed all 16 configured gates successfully at source commit
`bebf4482eac9d122c44511b52f28638ce4e61d94`. That previous 1,238-body checkpoint
passed 181,668 host cases and reproduced its committed hybrid APK exactly:
`2eabb2d883598254ca71f99999297e1b98fa9ea56fb24c200d5f053456cff4d6`.
The same 81,191-file input digest was verified before and after the run.

This fresh hosted result includes the earlier Java staging cleanup fix, signed
source-edit rejection and final positive restoration. It supersedes the earlier
interrupted acceptance attempt for that checkpoint; the failure diagnostics
remain preserved. The complete report and exact output identities are in
[source-ci-bebf448](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/56bff54c905e45dd7ce8776c96b54ff9a0608bf9/docs/verification/source-ci-bebf448).
The new 1,239-body combined checkpoint requires its own completed acceptance run.

## Actual Android results and next capture

The first hosted device comparison installed and launched both earlier APKs.
Their intro UI hierarchies matched, but their full screenshots differed by
75 pixels in the signal-strength icon. Its actual result remains
[CAPTURE_DIFFERENCE](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/2fe15d9057495d6ccdfec99ccd3807f224fe5d34/docs/verification/android-ci-ba52fd6).

The next hosted Android run booted successfully with KVM and ARM64 translation,
then failed during device preparation before installing either APK. All measured
primary signal levels were 4, but the helper's former requirement for identical
raw radio measurements reset its stability timer. The complete failure and raw
observations remain in
[android-ci-bebf448](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/5d2b3c7e4c7bab7061725762418801ab53cf28a1/docs/verification/android-ci-bebf448).
No app runtime result is inferred from that preparation failure.

The revised helper checks the stable primary radio and computed level while
retaining every raw measurement. It records and verifies the requested SystemUI
clock, and can disable all three Android animation scales for still captures.
The app's source, resources and screenshots are not changed by this device setup.

The schema-3 recorder validates both APK inputs before package removal, verifies
package absence and successful installation, and compares the installed base APK's
actual checksum with the intended input. It records foreground and live process
observations, fresh UI preconditions and clean input-command results. The optional
intro sequence captures the four English pages `MACRODROID`, `TRIGGERS`, `ACTIONS`
and `CONSTRAINTS` through three observed Next buttons. Every complete screenshot
and hierarchy is compared. Failed or incomplete intro navigation cannot establish
intro equality; completed cold captures retain their narrower evidence.

These recorder and helper changes have host-only adversarial regression coverage.
A new Android capture is still required. Still-frame agreement would cover only
those observed pages and transitions, not animation or all application features.
See [RUNTIME_CAPTURE.md](RUNTIME_CAPTURE.md) and
[ANDROID_ACCEPTANCE.md](ANDROID_ACCEPTANCE.md) for the exact scope and commands.

## Remaining work

The reference Java tree is not a complete conventional Android application
project. Full functional 1:1 parity, complete Java/Kotlin source recovery, native
C/C++ source recovery and the publisher's signing identity remain unestablished.
Rebuilt APKs use the openly distributed development test identity retained in the
v9 snapshot. Historical 1,237- and 1,238-body reports keep their original scope;
new code requires fresh measurements.
