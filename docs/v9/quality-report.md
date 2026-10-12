# MacroDroid reconstruction v9 — measured acceptance report

**October 11, 2026. Full Android runtime 1:1 equivalence is NOT established.**

The comparison target is the exact user-supplied MacroDroid 5.67.8 APK,
`com.arlosoft.macrodroid`, version code `896700008`, minimum API 23 and target API 36.
This is an editable smali reconstruction with selected Java-compiled method bodies.
It is not the publisher's original complete Java/Kotlin project, recovered native
C/C++ source, or an APK signed with the original signing identity.

## 1. Changes in this release

The hybrid now compiles **1,237 method bodies across 602 classes** from Java. Five
additional bodies are registered under `source/ui-methods.json` and implemented in
`source/java/recovered/ui/`. Original class declarations, inheritance, fields,
annotations and unregistered methods remain preserved. Compile/test stubs and helper
classes are not shipped in the APK. Of the total, **1,119 are the existing simple
constant-return/no-op bodies**; migration counts are not completed-feature counts.

| Recovered method | Preserved details | New three-way cases |
|---|---|---:|
| `DragLinearLayout.onTouchEvent(MotionEvent)` | Touch state and visibility checks, pointer changes, float-to-integer cast before subtraction, reset order and partial mutations | 1,494 |
| `PlaySoundAction.Z(String)` | Stop token, localized lookup, generic bracket tokens, null/empty handling and Exception-only boundary | 1,271 |
| `IncomingSMSTrigger.isValid()` | Original contact sentinels, cached group lookup, local negative-option normalization and provider exception boundary | 2,065 |
| `SceneTextConfig$a.createFromParcel(Parcel)` | The exact 21-field read order, nonzero booleans, nested types and loader calls | 945 |
| `SceneTextConfig.writeToParcel(Parcel,int)` | The exact 21-field write order, canonical boolean values and forwarded flags | 3,158 |

These are selected bodies, not recovery of each entire Android component. Gesture
movement/animation, actual contacts, nested Parcelable implementations and scene
construction still call preserved application/framework dependencies. No alternative
behavior was substituted to make the code appear cleaner. For example, the original
SMS check's cursor handling is retained rather than silently changed.

The new suite has **8,933 cases and 7,129 independently specified expected checks**.
Every represented original instruction in these five methods was visited: **401/401**.
That is not exhaustive path/input coverage, coverage of called dependencies, or proof
of Android behavior. `UI_RECOVERY.md` identifies the mappings and boundaries.

## 2. Issues actually caught and corrected

The first UI comparison exposed a missing `FLOAT_TO_INT` opcode in the bounded host
interpreter. Its failed diagnostic remains under
`reports/development-v9/ui-missing-float-to-int.json`; it was not relabeled as a pass.
The conversion was implemented, then tested with **6,270 primitive cases**, including
21 fixed expected edge values. The correct full comparison subsequently passed.

The five-suite runner now checks the exact partition of registered method signatures,
not just a total count. Missing, duplicated or substituted method keys, malformed case
counts, stale results, and a rebuilt DEX that does not belong to the signed candidate
are rejected. Unsupported executed instructions still fail explicitly.

The old device recorder could confuse a command completing with a live app launch.
The recorder now requires live, stable app PID samples, a foreground target activity,
app-owned UI XML and a valid screenshot. Installation alone is not execution evidence.
The new comparison checks environment identity, evidence hashes, full decoded pixels,
PNG color metadata and all UI attribute values/child order. No image masks or automatic
text exclusions are applied. These device paths remain unexecuted on Android; their
guards and failure cases were tested with synthetic host data.

## 3. Fresh verification results

| Check | Observed result |
|---|---|
| Fresh original-to-preserved-source audit | 71,267 class sources and 349,972 method definitions; no missing, extra or altered classes |
| Fresh original resource-source audit | All 7,212 manifest/resource sources byte-identical; 23,854 original IDs, visibility and opaque entries retained |
| Clean baseline source assembly | All nine DEX partitions freshly assembled from smali, including the embedded advertising partition |
| Baseline canonical code comparison | All 71,267 classes match; zero unexpected changes |
| Hybrid code-change isolation | Exactly 1,237 method bodies in 602 classes changed; no unexpected or omitted registered replacements |
| Recompiled Android resources | 7,211 decoded files byte-identical; one equivalent enum/flag-order difference in `res/values/attrs.xml` |
| APK payload names and compression | All 9,243 original non-signature entry names and original compression choices retained |
| Resource identifiers and filenames | All 23,854 IDs, original resource paths and public/private state preserved |
| Native dependencies | All 22 original ARM64 libraries unchanged; ELF LOAD and stored ZIP alignment checked |
| Signing | New APK v1/v2/v3 signatures verified by the pinned AOSP signing components |
| Python regressions | **154/154 passed** in the final clean run |
| Primitive/monitor conformance | **12,873 cases passed**: 2,458 existing, 4,145 engine, 6,270 UI conversion |
| Five selected-method suites | **179,248 three-way cases**, zero mismatches or unsupported executed instructions |
| Deliberate incorrect implementations | All **15 host faults** rejected, with correct implementations retested |
| Real signed source-edit experiment | Incorrect dispatcher edit reaches the APK, changes only its intended method, and is rejected in 113 cases |
| Independent clean acceptance | All **16 configured commands** exited zero; all 81,177 pinned inputs unchanged |
| Android installation, launch, UI or macro execution | **NOT EXECUTED** |

Class/method totals include dependencies and the embedded DEX. Canonical comparison
covers represented declarations, instructions, annotations, exception regions and
debug structures, not byte identity of original versus regenerated DEX table layouts.
The one resource normalization is named enum/flag declaration ordering, not arbitrary
layout/array reordering. Signature logs retain their warnings about legacy v1 coverage
of some META-INF metadata; this is not a claim of warning-free verification.

Suite case counts are legacy **95,262**, core **34,753**, environment **30,684**,
engine **9,616**, and UI **8,933**. The exact union of method keys is the 1,237-entry
migration registry, with no overlap or missing method hidden by aggregate counts.

## 4. Defect-detection experiments

The five new temporary incorrect implementations were rejected:

| Intentional defect | Failing cases |
|---|---:|
| Subtracting the drag anchor before casting instead of afterward | 112 |
| Treating only integer one as a true Parcel boolean | 256 |
| Writing italic state in the bold field's position | 1,952 |
| Catching Throwable rather than Exception around the SMS provider call | 72 |
| Rejecting generic bracket sound tokens | 27 |

Each requires a named targeted case to fail; unsupported interpretation cannot count
as a successful rejection. The existing ten engine/core/environment/text controls
also passed their rejection criteria. These failures are defect detections, not added
positive application-test passes. Source, fixture and release APK hashes remained
unchanged, and correct positive suites ran again afterward.

Separately, `full_apk_edit_probe.py` changed a Java dispatcher helper to terminate
incorrectly after a pause handoff, compiled and signed the entire experimental APK,
and compared all 9,243 payload names and 9,842 classes in its changed partition.
Only `Macro.invokeActions` changed, within `classes3.dex`, outside signing metadata.
The three-way engine tests rejected the signed incorrect app in **113 cases** with
zero unsupported executions. The incorrect APK is not included in the deliverables.

## 5. What the host tests do and do not prove

The three paths are selected original DEX instructions from a freshly extracted
fixture, recovered Java on the host JVM, and rebuilt instructions whose DEX bytes
are checked against the signed hybrid APK. The fixture is test-only, not a build
input. Its SHA-256 is
`b0ece2f31a81e1d646f366b5e83fb674adee916dea3aeb5447eaf840da197e45`.

The interpreter is **not ART**, and Java host-library semantics are **not execution
of Android framework libraries**. For the new methods, MotionEvent, View, animation,
interception, content providers, cursors, contacts and Parcel are controlled host
boundaries. Typed Parcel tests check call order and values, not Android's serialized
binary format. They do not demonstrate rendered gestures, working contacts/SMS,
scene restoration on Android or real sound output. Existing action scheduling,
permission, lifecycle, resource, constructor and other test boundaries remain.

Tests compare values, selected identity/state and ordered boundary calls, partial
mutations and exception types. They do not exhaustively compare framework exception
messages, Android stack traces, asynchronous timing, real services or native behavior.
A separate **66-case synthetic PNG interoperability audit** passed against Pillow;
it tests the screenshot decoder, not a screenshot of this app on a device.

## 6. Independently extracted source build

The provisional archives were closed, reopened, CRC/hash-checked and extracted into a
new directory. Prior reports were excluded except the pinned input manifest. There
was no output APK, build directory, assembly cache or compiled helper cache. HOME and
Java temporary directories were isolated. This was an independent directory on the
same Linux host, not another operating system or independent physical machine.

The only initially APK/DEX-shaped files were the resource compiler's framework APK
and the explicitly test-only original-method fixture. No original target APK or
original application DEX was used to build the application. All nine baseline
partitions were assembled from smali. The hybrid reused only validated unchanged
partitions produced from source by that clean run.

All **16 final acceptance commands exited zero**. The final correct positive suites
ran after all deliberate-defect checks and the signed source-edit experiment. Every
command, exit, log hash and input/output identity is recorded in
`reports/acceptance-latest.json` and `reports/clean-export-verification.json`.

The final snapshot contains **81,177 source/test/tool/signing/reference input files**:
`6f9e0f823f85c89c45cf2d23672fac246b526a5d389a04a9348aaeaeefe3c65c`.
All matched before and after. Each clean APK is byte-for-byte identical to its
corresponding working v9 build, **not to the uploaded original APK**.

The earlier working acceptance used a 79,284-file snapshot and 153 Python tests.
The final manifest was expanded to pin all 1,893 reference Java files used by the
new reference-status check, and one integrity regression was added. No application
source changed. The complete final clean run used the stronger 81,177-file manifest
and **154 tests**. This distinction is recorded in
`reports/delivery-input-pin-expansion.json`, not concealed by reusing old pass files.

Final packaging adds completed reports/documentation only; no pinned build/test input
is modified after clean acceptance. The final archives are closed, reopened and checked
member-by-member, then checked against that exact clean-tested manifest. The external
delivery JSON identifies final archive bytes; provisional archive hashes inside the
clean-run report identify the earlier inputs to the clean extraction.

## 7. High-level source and Android gates remain open

The historical Java reference tree has **1,893 files and 42 failed-decompilation
markers**. Exact signature matching now maps **16 markers to registered executable
replacements**, with **26 not mapped**. Four additional markers were superseded by
this release's five bodies. These counts are not all remaining engineering work.
Many other reference files still require compiler and semantic repairs; most executable
code remains editable smali. There is no complete conventional Java/Kotlin Android
Studio application build graph. Native C/C++ source remains unrecovered.

The environment has JDK 21 and the bundled offline build tools, but no ADB, emulator,
SDK Manager, Gradle or `/dev/kvm`. The actual official platform-tools download probe
failed DNS resolution. Connected-source and browser-profile checks did not produce a
usable authenticated Android test environment. No cloud device test was started.
The recorder's availability check returned **BLOCKED**, not a device success.

The original/candidate APK identity preflight did execute offline and passed for their
package, version, SDK and ZIP metadata. The first preflight exposed the parser's
assumption that AAPT always emitted `sdkVersion`; supporting its actual
`minSdkVersion` output was then tested. This is still not installation evidence.

`android_acceptance.py` requires explicit selection of an ARM64 device and permission
to remove the target package and its data; physical devices require another opt-in.
Both APK identities are checked before removal. It does not silently grant permissions,
log in or dismiss consent. `android_compare.py` rejects missing, altered, stale,
wrong-environment or non-app evidence, but even a future successful run would establish
only the captured cold-launch comparison, not feature parity.

No real Android install, launch, screenshot/UI comparison, macro execution, permission,
accessibility/background service, notification, persistence/reboot, native load,
performance, helper, account, purchase or server integration has been tested.
Use only an isolated disposable ARM64 environment, not a primary phone with valuable
macros, credentials or personal data.

## 8. APK and signing identities

Original uploaded APK SHA-256:
`84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`.

Baseline: **94,677,674 bytes**, SHA-256
`aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096`.
This is the unchanged preservation control from v5–v8, not a newly changed app.

Hybrid: **94,682,999 bytes**, SHA-256
`ebd8628eb69f71fc54d70bf87889a11d7b9a673e20b318233c7c30b489d8ff31`.
This includes the five additional Java method bodies. Delivered APK copies come from
the successful final clean run.

The certificate extracted from the upload's v2/v3 signing blocks has SHA-256
`3b61c2a82aff9f7652ffe0b04be3c8f248b5e1aa7063f1a3846f0cf5c778628a`.
That observation does not authenticate this upload as a clean publisher release.
The new APKs use the openly distributed development certificate SHA-256
`ca86cb5c4b75d5730f68d21cd0c196bfb93a849634924bcb1b9a1385073d6737`.
The original private signing key is not available. Certificate-bound updates,
permissions and integrations cannot be presumed identical. No licensing,
authentication, payment or integrity-check bypass was introduced.

## 9. Evidence and official technical references

Current evidence is under `reports/`: `release-summary-v9.json`,
`clean-export-verification.json`, `acceptance-latest.json`, `release-input-snapshot.json`,
`fresh-original-source-audit-v9.json`, `*-roundtrip.json`, `*-resource-parity.json`,
`*-assembly-inputs.json`, `*-signature-verification.log`, `python-unit-tests.log`,
`java-all-path-parity.json`, the five `java-*-parity.json` suite reports,
`ui-oracle-semantics.json`, `*negative-control*.json`, `full-apk-edit-probe.json`,
`reference-failures-status-v9.json`, `reference-continuity-v9.json`,
`android-apk-preflight-v9.json`, `environment-v9.json`, and `android-runtime/result.json`.
Historical and failed-development reports are retained as history, not current acceptance.

Official instruction semantics: https://source.android.com/docs/core/runtime/dalvik-bytecode

Official ADB documentation: https://developer.android.com/tools/adb

Official app-signing documentation: https://developer.android.com/studio/publish/app-signing

**Verdict: the v9 editable source build, static comparisons and stated bounded host
tests pass. Full 1:1 Android functionality and a complete high-level source
reconstruction remain unverified.**
