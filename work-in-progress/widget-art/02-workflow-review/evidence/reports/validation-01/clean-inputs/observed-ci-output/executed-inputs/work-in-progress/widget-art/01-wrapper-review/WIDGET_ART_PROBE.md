# Widget method ART probe: compiled, reviewed, execution pending

This inactive checkpoint prepares eight bounded Android cases for the exact recovered `WidgetUpdateManager.m(Context, List, o73)` body. It contains a real compiled standalone DEX, an exact original/candidate APK binding, a guarded AndroidRuntime wrapper, complete simulated host controls, a workflow step proposal and preserved preparation failures. **No Widget Android execution occurred while preparing this checkpoint.** Publication and a separate disposable-device execution are the next stages.

The probe complements the existing signed Widget static, resource and original/JVM/rebuilt work. It does not register another recovered method, modify either APK or change the active reconstruction. The existing independent ART constructor-allocation probe remains unchanged.

## Exact inputs

| Input | Bytes | SHA-256 |
|---|---:|---|
| Supplied original APK | 95,725,918 | `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800` |
| Widget candidate APK | 94,683,439 | `b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f` |
| Standalone Widget probe DEX | 7,580 | `79bd3b46e71253b17ec75099cce3611df1735b8f74e8bdcb61c61e5a37ae1a07` |
| Exact probe provenance JSON | 3,225 | `31e7ebb8bebaa12210d1486b87b864e9ed7cf9771dde4488ffe435dd4e434901` |

The target is `Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->m(Landroid/content/Context;Ljava/util/List;Lo73;)Ljava/lang/Object;`. Its preserved original method-body hash is `a1dd490bbfd6837fa72e6bf8ae4c75736612989fcba050fe2f0582aa03640e34`; the recovered helper source hash is `dbcb1a98d25ae4637531644da37d24f6e1bc494f941d4212da03c360fe315d79`. The original method definition remains the authority for case behavior.

The candidate preparation used a private byte-verified, read-only copy because the parent was rebuilding the same dist pathname. `input-snapshot.json` preserves the source pathname and exact snapshot binding. The parent coordinates publication of those exact APK bytes separately. This checkpoint does not introduce another APK build or alter the release manifest.

## What executes inside the guest

`WidgetMethodProbe.java` is reflection-only and compiled with `javac --release 8 -g:none`, using no Android or application compile classpath. D8 receives a JAR containing that one class. The final DEX defines exactly `recovered.probe.WidgetMethodProbe`; it defines zero application or Android host boundary classes and has zero direct application/Android type references. The only non-Java reference metadata is the standard Dalvik Signature/Throws annotations. The builder disassembles, reassembles and redisassembles the DEX and requires byte-identical smali text.

At runtime the probe prepares a real main Looper on its current thread, then loads the actual Widget manager, its continuation, the continuation base and Unit class from the single bound APK. It checks their classloader identities, the manager/Unit singleton identities, the precise method owner/return type/modifiers and the real continuation constructor. No application Context, nonempty widget list, renderer or logger substitute is provided. The manager's static Context field must remain null before and after every case.

| Case | Required observation |
|---|---|
| Fresh empty list | Returns the real `blg.a` Unit singleton by identity. |
| Reused label zero, empty list | Reuses the real high-bit continuation, clears only its high bit and returns Unit. |
| Resumed label two, empty iterator | Returns Unit while preserving every supplied saved slot and integer. |
| Invalid saved label | Throws exactly IllegalStateException with the preserved original literal message. |
| Label-two dead cast in L$7 | Throws exactly ClassCastException before service work; saved state remains intact except the high-bit clear. |
| Label-two dead cast in L$4 | Same typed exception/state check for the dead list cast. |
| Label-two dead cast in L$1 | Same typed exception/state check for the other dead list cast. |
| Fresh null list | Throws exactly NullPointerException. |

Each saved-state case checks all eight object-slot identities, all three saved integers, result/owner identities and the cleared continuation label. A deliberately non-null arbitrary object remains in the unread L$6 slot. VM-generated ClassCastException/NullPointerException message wording is not asserted; the invalid-label literal message is exact. The body is neither patched nor instrumented.

Every successful case writes exactly one `WIDGET_ART_CASE_OK` line; the final line is `WIDGET_METHOD_ART_OK cases=8`. The wrapper requires the exact nine-line UTF-8 stdout byte sequence and process exit 0. It does not accept a marker embedded in extra output or a successful-looking marker from a nonzero/timeout result.

These eight cases do not execute a nonempty widget update, first/second renderer suspension, real widget factory allocation, Exception/logging handler, service lookup or widget display. They establish only their observed body-loading and execution paths when a later actual Android result succeeds. Enabled verification is not a claim that all APK classes or all application behavior were exercised.

## Why app_process64

The real Looper constructs a MessageQueue and needs framework native registration. The source-backed assessment in `ANDROID_RUNTIME_SOURCE_ASSESSMENT.md` checks AndroidRuntime's registration sequence, the MessageQueue JNI table, tool-mode stdout preservation and ART classpath/verification parsing against eight saved Android15 primary source files.

The wrapper uses app_process64 with explicit `-cp` containing the bound probe DEX followed by exactly one APK. Inherited CLASSPATH is only an ART fallback when no explicit ClassPath option is supplied. The late `dalvik.vm.extra-opts` property must be empty before setup, before each guest invocation and afterward. The two guest commands use separate processes, real framework/app classes and `-Xverify:all`; no verifier-disabling or hidden-API exemption option is supplied.

## Host and device safeguards

The wrapper first checks exact local input/provenance hashes, DEX structure and APK archive shape. It requires an explicit `emulator-NNNN` serial and the existing `MacroDroid_API35_Disposable` AVD, along with the pinned Android15 fingerprint, boot/emulator status, ABI and native bridge. It does not accept a physical device or another AVD. The ADB binary hash is recorded; app_process64 and the guest timeout executable are checked and their actual hashes are bound before and after.

A fresh UUID directory under `/data/local/tmp` is created without accepting an existing directory. All three files are pushed unchanged, chmodded to 444, checked for that mode and hashed on-device. Each guest has a 120-second device timeout and 150-second host timeout. The complete normal successful trace contains 60 exact commands, including environment checks before each VM, post-run input/binary checks and cleanup. Only the freshly owned directory can be removed. Failures preserve raw command output, completed case prefixes, timeouts, original failure reasons, postcheck errors and cleanup status.

Semantic outcomes and diagnostic acceptance are separate fields. Both case sets may have produced the exact success output even if stderr contains an unreviewed diagnostic; that circumstance fails the strict overall gate while retaining the actual semantic observations. A cleanup or post-run hash failure likewise cannot become a successful overall result. The wrapper does not broadly suppress AndroidRuntime warnings or errors.

The independent result validator reconstructs the entire successful command sequence and rehashes every stdout/stderr artifact. It verifies the copied wrapper, exact provenance, one-class DEX, original/candidate paths and hashes, verifier option, environment properties, guest argv, return codes, case output and owned cleanup. An extra/missing command, altered output, unbound classpath or stale nested report fails. Simulated runner reports have an explicit host-control backend and cannot pass the ordinary Android-evidence verifier.

## Measured preparation and controls

Probe03 completed javac, D8, disassembly, assembly and redisassembly successfully with the original and immutable candidate APK identities unchanged. It contains no Android execution result. Build stdout/stderr remain separate; a compile-time deprecation warning is retained rather than silently discarded.

The final wrapper control suite has **27 passing Python tests**. Every ADB reply is simulated. These tests include real exact-Dex/provenance validation, byte-corrupted DEX, wrong original/candidate/provenance, physical/wrong/unbooted devices, timeout bounds, all late-option-check phases, input hash/mode errors, failed mkdir/push, original-failure short-circuit, candidate missing/extra output, nonzero/bool exit status, partial timeout output, diagnostics distinct from semantics, post-run APK/DEX/binary/local-file changes, cleanup failure, tampered command/result/artifact data and nonempty-output protection. All simulated command artifacts are retained. The first 27-test result is also preserved; the final rerun changes only default packaged probe/provenance paths, using identical DEX bytes.

Preparation failures remain part of the record. Probe01 compiled and disassembled correctly, then failed an overbroad descriptor-text audit that mistook method-name substrings for type descriptors and did not yet list compiler annotations. The corrected audit keeps a strict application/Android type exclusion. Probe02 failed candidate binding while the parent was rewriting that dist path; its old recorder did not capture the mismatching intermediate hash, so none is invented. The subsequent private snapshot has the exact b79 identity. All old scripts, source/class/DEX outputs, failed reports and later successful preparation are preserved.

The first checkpoint-packaging attempt used the wrong result field name (`apk_bindings` instead of `apks`) after completing its copies and evidence archive. That packaging failure, exact old script, traceback and complete incomplete archive are preserved in `freeze-attempt-01`. Its duplicate staging directory was retired only after every file matched the separately retained sources/reports. The corrected packager validates the APK field before creating a new checkpoint. This did not change the probe, wrapper or any test outcome.

## Proposed execution and integration scope

`workflow-proposal.yml` is an inactive step fragment for the existing disposable Android job. Its parent must supply the published immutable probe checkpoint, original APK and exact b79 Widget candidate, and boot the existing pinned AVD. The wrapper supplies the remaining guards. It is intentionally outside `.github/workflows`; source preparation did not start a hosted job, install an app or update any active project/runtime source.

The reviewed command can also be run directly after those inputs and device are prepared:

```bash
python3 android_widget_method_probe.py \
  --serial emulator-5560 \
  --original /absolute/path/original.apk \
  --candidate /absolute/path/widget-b79.apk \
  --output /absolute/path/new-widget-art-evidence
```

The package's default probe/provenance files are under `probes/`; their exact bytes are validated. The output directory must be new or empty. A later actual Android checkpoint must identify its immutable published input commit and preserve its complete result independently from this compilation-and-host-control checkpoint.
