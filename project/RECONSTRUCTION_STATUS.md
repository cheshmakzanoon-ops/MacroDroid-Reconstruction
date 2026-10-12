# Current reconstruction progress

The integrated source contains **1,240 recovered Java method bodies across 603 classes**, with the remaining implementation built from preserved smali, resources and native payload. The comparison target remains the supplied MacroDroid 5.67.8 APK (`com.arlosoft.macrodroid`, version code `896700008`). Method counts do not measure the percentage of complete application behavior.

**The integrated checkpoint passed all five planned clean build/code/resource/host/integrity checks, including 188,791 three-path cases across all 1,240 methods and 259 Python tests. It reproduced the isolated signed plugin candidate exactly. The isolated plugin proof also passed all 37 UI fault controls. The next hosted full acceptance and newly added Android scopes remain pending. Whole-application 1:1 runtime parity is not established.**

## Latest executable source recovery

`source/java/recovered/ui/PluginLookupMethods.java` supplies the Java body for `com.arlosoft.macrodroid.plugins.j.invokeSuspend(Object)`. It preserves continuation labels and suspension identity, lookup guards, mutable dependency reads, the literal original retry key index, repeated HTTP status reads, publication/counter order, analytics values and the original catch boundaries. The controlled host dependencies make no network requests and implement no coroutine scheduler.

The isolated signed plugin checkpoint measured the following results:

| Check | Measured result |
| --- | --- |
| New plugin lookup body | 3,053 original-instruction/JVM/rebuilt-DEX cases; zero mismatches or unsupported executions |
| Original plugin control flow | All 198 instructions and all 34 conditional branch edges visited |
| Complete registered host suite | 188,791 cases across 1,240 bodies and all three execution paths |
| UI suite | 18,476 cases across eight methods; 14,552 independent expected-result checks |
| Deliberate-fault detection | All 37 UI controls rejected their intended defect, including 15 new plugin controls; the clean 18,476-case suite then passed again |
| Signed APK round trip | 71,267 classes and 349,972 method definitions checked; exactly 1,240 intended body changes, with zero unexpected changes |

The complete source, exact merge boundaries, failed attempts, reports and full proof archive are retained in the [immutable plugin checkpoint](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/f0b393e98774debd1e991ca91cb67c4e09c49444/work-in-progress/plugin-lookup/04-signed-proof). See [PLUGIN_RECOVERY.md](PLUGIN_RECOVERY.md) and [UI_RECOVERY.md](UI_RECOVERY.md) for the finite test scope and exclusions. These results do not establish actual plugin/network behavior on Android.

The previous custom-scene and touch-blocking recoveries remain active. The scene method contributes 4,070 cases covering 405 instructions and 40 conditional edges. Touch blocking contributes 2,420 cases covering 162 instructions and 30 conditional edges. Their original measured scope is retained in [SCENE_RECOVERY.md](SCENE_RECOVERY.md) and the historical verification records.

## Integration and reproducibility

The parent integrated the 40 frozen plugin paths with baseline hash checks. Two narrow patches preserve the parent's runtime tests and strict generated-directory cleanup. The Java/D8 compiler writes a fresh generation and publishes it only after all compiler and disassembly commands succeed. Removing an old generated directory fails explicitly if removal is incomplete or the retired path reappears. Six focused regression checks exercise those staging boundaries.

The reviewed constructor-owner facility is also integrated, with **zero mappings configured for the active 1,240 methods**. It is inactive unless a migration entry explicitly supplies a mapping. All three build/static/linkage gates share the same source hash, class declaration, loader-domain, direct-parent, descriptor, allocation and occurrence checks. The standalone proof passed 31 host regressions and actual D8/smali round trips. Before integration, it left all 1,239 existing helper bodies byte-unchanged and passed their actual static/linkage checks. The full [constructor checkpoint](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/c7abf086ebffbc70cb3143f909a7f48648de22bc/work-in-progress/constructor-owner/02-pipeline-proof) includes the review correction and its regression.

The freshly built integrated hybrid APK is 94,683,497 bytes, SHA-256:

`9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`

The integrated build/test-input snapshot covers 81,245 files, canonical SHA-256:

`19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183`

From the repository root, use:

```sh
python3 scripts/materialize_v9.py
python3 scripts/assemble_artifact.py artifacts/current/manifest.json
```

The materializer verifies each committed baseline archive part and both complete archive hashes, extracts the baseline and applies the tracked `project/` overlay. It preserves existing destinations; use a fresh directory for another checkout. Inactive `work-in-progress/` checkpoints are preserved for review and are never applied by the materializer.

With Python 3.11+ and JDK 21, run from `workspace/MacroDroid_v9`:

```sh
python3 release_integrity.py verify
python3 acceptance.py
```

The build retains the compatibility output filenames `dist/MacroDroid-5.67.8-v9-baseline.apk` and `dist/MacroDroid-5.67.8-v9-hybrid.apk`. The manifest, checksum and source snapshot identify the actual candidate. The original APK is a comparison input and is not required to compile either variant.

## Fresh combined host proof

A separate, fully hash-checked copy of all 81,245 pinned inputs passed hybrid assembly, complete hybrid bytecode verification, resource verification, the complete original/JVM/signed-DEX host suite, and final input integrity. All five command logs and ten declared fresh report hashes were independently rechecked against the closed output files. The build checked 71,267 classes and 349,972 method definitions, with exactly 1,240 intended body changes and zero unexpected changes. Resource verification preserved all 23,854 IDs: 7,211 of 7,212 files were byte-identical, with only the documented equivalent enum-order difference.

The complete [combined evidence](../docs/verification/plugin-runtime-integration/) retains every report, merge receipt, source-copy inventory and exact artifact identity. This run passed 259 Python tests and 188,791 cases over all three execution paths. The separate integrated Android-tooling host suite passed all 27 tests. No Android device was executed by either host run; the forthcoming 16-gate workflow and post-intro/ART measurements have their own acceptance results.

## Completed hosted source acceptance

The last completed hosted source checkpoint is `95077fcb1d3c86f3b1c91026619642d99198f149`, containing 1,239 recovered bodies. Its source job in [run 38194498356](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38194498356) passed **all 16 configured gates**, 185,738 three-path cases and 203 Python tests. All 22 then-configured UI fault controls passed, followed by the clean 15,423-case UI restoration. The signed source-edit probe rejected its intended defect and the final complete positive suite passed. The same 81,211-file input snapshot was verified before and after the run.

That fresh build reproduced the committed 94,683,342-byte hybrid exactly, SHA-256 `be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce`. The complete 105 source report files and their inventory are retained in [source-ci-95077fc](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/3b2b7e8f539e746c9b99fbeb9a093bda1074fb92/docs/verification/source-ci-95077fc). This result retains its 1,239-body scope; it does not certify later source changes.

Two later local attempts encountered generated-directory interference and remain recorded as failures. Their diagnostics include a reappearing generated staging path and an observed transient `.rsync-tmp` path. Verification then moved to independent, fully hash-checked copies outside the synchronized source tree. The prior failures are not relabeled as successful runs.

## Actual Android result

The separate Android job in run `38194498356` successfully installed the exact original and the `be1138a5…` candidate on the same pinned API 35 emulator configuration. Schema 3 verified each installed base APK's actual device-side SHA-256 before launch. Both apps retained the required live process and foreground activity.

The actual outcomes were `EXACT_COLD_LAUNCH_MATCH_ONLY` and `EXACT_FOUR_PAGE_INTRO_MATCH_ONLY`. All four pairs of full 720 × 1280 PNGs and UI hierarchy XML files were byte-identical for `MACRODROID`, `TRIGGERS`, `ACTIONS` and `CONSTRAINTS`. Independent decoding found zero differing RGBA pixels in every pair, including the status and navigation bars. All three observed Next-button transitions reached matching captured pages. The complete [Android evidence and independent replay](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/0c5913324bcf60bacdb46554d80b3eda684dd79d/docs/verification/android-ci-95077fc) preserve the commands, installed identities, environment, screenshots and hierarchies.

The device explicitly disabled all three animation scales and displayed 12:00 through SystemUI demo mode. The helper required a stable computed signal level and retained every raw observation. The comparator used no crop, mask, resized image or pixel tolerance. This measures declared still captures only; it does not compare animation motion or transition timing. The earlier 75-pixel system-icon difference and subsequent pre-installation preparation failure remain preserved with their actual failed outcomes.

## Next Android gates

The recorder now supports `--intro-pages --post-intro`. After four complete intro captures, it rechecks the installed file identity and a fresh final-page hierarchy, foreground and live process, then taps the observed final Next button once. It records the resulting full surface before classification. It accepts an observed app landing activity or the specific MacroDroid notification-permission prompt and makes no further input or permission choice. Unexpected surfaces preserve their evidence and fail this new scope. The post-intro comparator validates the prior scopes and compares every pixel and XML attribute.

An independent ART probe uses the exact 1,436-byte DEX from the reviewed constructor checkpoint alongside the unchanged original APK. It checks the single `Lzhh;` allocation through the original `Lrff;` constructor with `-Xverify:all`, exact device-side file hashes and a bounded guest process. The helper adds no application class or constructor. Its result cannot establish Widget behavior or app parity.

The driver records all three capture comparisons and the independent ART result separately. A failure in a later capture or the constructor probe preserves completed narrower measurements. The final requested CI gate requires all configured scopes to pass. **Actual post-intro and ART results are still pending for this checkpoint.** See [RUNTIME_CAPTURE.md](RUNTIME_CAPTURE.md), [ANDROID_ACCEPTANCE.md](ANDROID_ACCEPTANCE.md) and the repository's Android tooling documentation for exact commands and evidence requirements.

## Remaining recovery

The Widget update method and the next plugin-upload method are preserved in inactive checkpoints as their source and proof develop. They require their own complete evidence before activation. The Widget method depends on the guarded constructor-owner mapping and the independent ART result.

The reference Java tree is not a complete conventional Android source project. Complete Java/Kotlin recovery, native C/C++ source recovery, the publisher's signing identity and whole-application functional parity remain unestablished. Rebuilt APKs use the openly distributed development test identity retained in the supplied v9 snapshot. Macro creation/execution, real services and permissions, persistence, widgets, external integrations, other locales/devices/APIs and performance remain separately measurable work. Historical reports retain their original source and artifact identities.
