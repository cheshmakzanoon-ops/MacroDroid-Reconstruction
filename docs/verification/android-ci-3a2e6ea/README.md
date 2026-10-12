# Hosted Android evidence for active checkpoint 3a2e6ea

Run [38200503458](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38200503458), Android job `114652621919`, tested source commit [`3a2e6ea9ef9e18d38d5921bb18c77e1c2eb13677`](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/commit/3a2e6ea9ef9e18d38d5921bb18c77e1c2eb13677) on 2026-10-12. **The standalone constructor allocation passed on ART and cold launch matched exactly. The requested expanded capture gate failed because the TRIGGERS still differs by 34 pixels.** The failure remains recorded as `REQUESTED_RUNTIME_SCOPES_INCOMPLETE_OR_DIFFERENT` in [runtime-run.json](runtime-run.json).

The raw archive and all 426 extracted files are retained unchanged. [manifest.json](manifest.json) and [extraction-receipt.json](extraction-receipt.json) bind their provenance. The runtime artifact is 1,016,845 bytes, SHA-256 `fb22f6daa60ae9806b6c1e1980e3e129c7454337100779b5ac79f278c06471db`. Derived checks and the exact read-only analysis program are in [analysis/](analysis/), with results in [independent-analysis.json](analysis/independent-analysis.json). This analysis performed no Android actions.

## Exact tested inputs and device

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| Supplied original APK | 95,725,918 | `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800` |
| Active candidate APK | 94,683,497 | `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2` |
| Standalone constructor probe DEX | 1,436 | `85f53ad51a1a85fd2161bd485db9f12556f737b0745f6e26ffdff31a927d5281` |

[capture/result.json](capture/result.json) records the original and candidate installations, device-side APK hashes, launch results, environments, raw capture artifacts, and input observations. The cold comparator verified both installed identities. The candidate is the active 1,240-body checkpoint; the earlier successful 95077fc capture used a different candidate and remains separate evidence.

The disposable emulator was `emulator-5560`, AVD `MacroDroid_API35_Disposable`, API 35, fingerprint `google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.043/12960925:userdebug/dev-keys`. It ran with hardware acceleration enabled, 3,072 MB RAM, two virtual cores, and the SwiftShader renderer. It reported `x86_64,arm64-v8a` and `libndk_translation.so`. The captured display was 720 × 1280 at density 320. [The device configuration report](capture-device/capture-device.json) preserves actual commands and observations for the cellular profile, SystemUI demo clock `1200`, and the three animation scales set to zero. Both capture environments record the corresponding settings. This is a still-capture configuration; animation parity is untested.

The service's live status file was updated to `stopped` during clean shutdown. Its earlier ready report survives as literal bytes at offset 148 of [boot-readiness.stdout.txt](stages/boot-readiness.stdout.txt). [boot-ready-snapshot.json](analysis/boot-ready-snapshot.json) is that exact 1,481-byte suffix, SHA-256 `b379f4686a10bd972b86eda539b8ce80f495a4f3fcf3b7663f0cbc231b782863`, matching the ready-report binding in `runtime-run.json`. It was extracted without re-encoding JSON. The final stopped status is retained separately in [environment/runtime-status.json](environment/runtime-status.json).

## Constructor allocation verified on ART

[constructor-probe/probe-result.json](constructor-probe/probe-result.json) records `ART_CONSTRUCTOR_ALLOCATION_VERIFIED`. The fixed one-class DEX and supplied original APK were hashed on the device and set to mode `444` before execution. The command used `/apex/com.android.art/bin/dalvikvm64 -Xverify:all`, with the probe DEX and original APK as its only classpath entries and a 120-second guest timeout. The ART binary hash was `f96a70a7360448b0178f9e8b745b5362663f437116e17ff541cfc0e482c08a18`.

The actual command completed in 1.209 seconds, exit code 0, with empty stderr and the exact stdout line:

```text
CONSTRUCTOR_ALLOCATION_OK class=zhh arity=2
```

The [stdout bytes](constructor-probe/022-execute-constructor-probe.stdout.txt), all 24 command records with their stdout/stderr artifacts, local and remote input identities, read-only modes, and successful removal of the owned device directory are preserved. The pinned helper's independent `verify_result` accepted this evidence. The probe used no compile-only stubs on the runtime classpath, did not modify or install an app APK, and performed no app UI interaction. It establishes the particular constructor allocation's legality on this ART runtime. Widget behavior, broader constructor behavior, and complete app parity remain untested by this probe.

The DEX's Java/D8/original-class provenance remains bound to the frozen [constructor pipeline proof](../../../work-in-progress/constructor-owner/02-pipeline-proof/checkpoint.json), checkpoint SHA-256 `98d73cb9f3c73731e2a376bfdb446704674b2019e996a59483263f0d37b31e9a`, published at commit `c7abf086ebffbc70cb3143f909a7f48648de22bc`.

## Full-frame capture results

The independent analysis decoded every full original/candidate PNG into RGBA and counted unequal pixels without masks, crops, tolerance, or attribute omissions. Every corresponding raw hierarchy is byte-identical. The pinned cold, intro, and post-intro comparators were rerun read-only and reproduced the preserved reports exactly.

| Recorded surface | Changed pixels | Full XML | Formal scope outcome |
| --- | ---: | --- | --- |
| Cold launch / MACRODROID | 0 | Byte-identical | `EXACT_COLD_LAUNCH_MATCH_ONLY` |
| Intro page 2 / TRIGGERS | **34** | Byte-identical | Unequal still; causes `INTRO_DIFFERENCE` |
| Intro page 3 / ACTIONS | 0 | Byte-identical | Exact recorded still |
| Intro page 4 / CONSTRAINTS | 0 | Byte-identical | Exact recorded still |
| First surface after intro completion | 0 | Byte-identical | Raw notification surface exact; full post-intro gate remains failed |

The three observed intro Next transition targets match. The 34 unequal pixels lie in the exclusive bounding rectangle `[313,1184,352,1200]`, near the page indicators. Their full PNGs are [original-intro-2.png](capture/original-intro-2.png) and [candidate-intro-2.png](capture/candidate-intro-2.png). The recorded frames provide one final still per variant at this step; they do not establish whether the difference is transient rendering or a persistent behavior difference. No settling or normalization was applied retrospectively.

The completion capture performed exactly one further tap on the freshly observed final-page `button_next` for each APK. Both resulting surfaces were the system notification permission dialog, owned by `com.google.android.permissioncontroller` and resumed in `com.google.android.permissioncontroller/com.android.permissioncontroller.permission.ui.GrantPermissionsActivity`, with message “Allow MacroDroid to send you notifications?”. The full [original](capture/original-post-intro.png) and [candidate](capture/candidate-post-intro.png) PNG bytes match, as do the full hierarchies and completion targets. **No permission option was selected.**

[post-intro-comparison.json](capture/post-intro-comparison.json) still reports `POST_INTRO_SURFACE_DIFFERENCE` and `post_intro_surface_equal: false`, because its complete-scope gate requires the preceding four-page sequence to be equal. The exact raw notification pair does not override that failed prerequisite. The recorder itself completed the requested observations with exit 0; intro and post-intro comparators returned exit 2. The driver retained all earlier artifacts and the independent ART result, and failed the expanded capture gate.

## Host checks, replay, and limits

The separate [tooling host test artifact](tooling-host-tests/) contains 27 passing individual tests and `Ran 27 tests in 1.165s`. Its exact ZIP is 1,105 bytes, SHA-256 `c680c039c4c89461398dffa4432126c7d165136e84f2454d9d8b6ec20912a102`. The readable log is also retained in [analysis/android-tooling-host-tests.log](analysis/android-tooling-host-tests.log).

The analysis checked all 426 extracted member hashes, 136 distinct capture artifact bindings, 48 constructor command output bindings, and all six runtime report bindings. The exact source verifier hashes are included in its JSON. [The preserved analysis program](analysis/analyze_android_38200503458.py) shows the actual invocation's path layout; replay requires supplying the same extracted archives and verifier files at those configured paths, preserving the recorded hashes, and choosing a fresh output directory. It only reads evidence and writes derived files.

This run does not establish whole-app 1:1 parity, home or editor functionality, post-denial process behavior, permission outcomes, animation timing, or widget execution. The previous [95077fc exact still success](../android-ci-95077fc/README.md), [bebf448 device-configuration failure](../android-ci-bebf448/README.md), and [independent editor journey evidence](../editor-journey/run-38199371948-attempt-1/analysis/README.md) remain separate measured results. The source acceptance job for this commit is preserved separately by its publication owner.
