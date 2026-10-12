# MacroDroid reconstruction v8 — measured acceptance report

**Complete Android runtime 1:1 equivalence is NOT established.**

Target: the supplied MacroDroid 5.67.8 APK, package `com.arlosoft.macrodroid`,
version code `896700008`, minimum API 23, target API 36. This is a reproducible
editable smali/selected-Java reconstruction, not the publisher's original complete
Java/Kotlin project, recovered native C/C++ source, or publisher-signed application.

## 1. What changed from the unverified checkpoint

The checkpoint contains candidate Java bodies for the main action dispatcher,
eight action-structure navigation methods, a loop-rate guard and two GOTO scope
methods. Those 12 bodies are now compiled and included in the verified hybrid.
The full registry contains **1,232 bodies across 599 classes**. Of these, 1,119 are
the earlier simple constant/no-op bodies; migration counts are not feature coverage.

The candidate engine implementation itself did not need a behavior change to resolve
the recorded checkpoint failure. Original, recovered-Java and rebuilt traces agreed:
the group-end marker reaches generic action invocation. The saved expected trace
incorrectly omitted that boundary call. The real marker action body is a no-op.
Original DEX inspection and separate group-end/ENDIF stack tests justify the corrected
expectation. The old failing diagnostic is preserved, not relabeled as a pass.

The old default runner silently omitted the engine comparison suite. The new runner
requires all four suites, all registered method counts, nonempty case counts and the
correct two/three-path mode, rejects missing or stale output, and checks interpreted
rebuilt DEX bytes against the signed APK. Static change isolation now also rejects a
registered Java replacement that was accidentally omitted from the APK.

Additional engine vectors cover missing loop/ENDIF markers, dictionary BREAK cleanup,
ELSEIF variants, controlled state changes, exceptions inside the debugger monitor and
a bounded actual JVM wait/notify wake-up. This is not Android concurrency coverage.

## 2. Independent clean verification actually completed

The provisional source/toolchain archives were closed, reopened, read member-by-member
and extracted into a new directory. Previous reports were removed except the pinned
input manifest. The extraction had no build directory, output APK, helper classes or
assembly cache. HOME and Java temporary paths were isolated. Its only APK-shaped input
was the pinned resource compiler framework, not the target application.

**All 14 configured acceptance commands exited successfully.** All nine baseline DEX
partitions were freshly assembled from smali. The hybrid reused only unchanged,
validated partitions derived by that same clean run. The final positive suites were
rerun after all negative controls and the signed source-edit experiment.

All **79,251 pinned source/test/tool/signing input files** matched before
and after. Snapshot SHA-256:
`6fe077dcb64a21abd82fb92f3633941235675cf5ecc0c29c86980f5534d42d1a`.

Each independent clean APK matched its corresponding working v8 APK byte-for-byte.
That is **v8-to-v8 reproducibility, not byte identity with the original uploaded APK**.
The delivered APK copies come from this clean build.

| Gate | Observed result |
|---|---|
| Fresh complete original-to-preserved-source audit | 71,267 classes / 349,972 method definitions; all 7,212 manifest/resource sources match |
| Editable DEX assembly | 9/9 partitions, including the embedded DEX |
| Baseline canonical class comparison | 71,267 classes; no altered, extra or missing classes |
| Hybrid change isolation | Exactly 1,232 method bodies / 599 classes; no unexpected or omitted registered changes |
| Recompiled manifest/resources | 7,211 byte-identical decoded files; one equivalent enum/flag-order difference in attrs.xml |
| Resource IDs / paths / visibility | All 23,854 IDs and original resource filenames and visibility retained |
| Opaque payload and ZIP compression | Preserved; original 9,243 non-signature payload names retained |
| Native dependencies | All 22 ARM64 libraries unchanged; ELF and stored ZIP alignment checked |
| Signing | New v1/v2/v3 signatures verified with bundled AOSP apksig |
| Python regressions | 106/106 passed |
| Primitive and monitor/numeric conformance | 6,603 cases passed |
| All four selected-method host suites | 170,315 three-way cases; zero failures/unsupported executions |
| New engine suite | 9,616 cases over 12 methods; 474 independent expected-result checks across paths |
| Deliberate defects | All 10 host mutants rejected; correct suite restored |
| Complete signed-APK source-edit probe | Real Java edit compiled; only dispatcher body changed; wrong behavior rejected |
| Actual Android installation, launch or macro execution | NOT EXECUTED |

Class/method totals include dependencies. Canonical disassembly comparisons include
represented declarations, instructions, annotations, exceptions and debug structures;
they do not prove identical original/reassembled physical DEX table layouts. The only
resource normalization is enum/flag declaration ordering, not arbitrary layout/array
reordering. APK signature verification retains its warnings about legacy v1 coverage
of certain META-INF metadata entries; it is not a claim of warning-free verification.

Suite case counts: legacy 95,262; core 34,753;
environment 30,684; engine 9,616.
Each case compares original selected instructions, recovered Java and rebuilt selected
instructions. These are bounded cases, not Android UI tests or all possible inputs.

## 3. Genuine editable-source experiment and defect detection

`full_apk_edit_probe.py` created an isolated source project and deliberately added
premature termination after a pause handoff in the recovered Java dispatcher. It
compiled and signed the complete experimental APK before adding the original-method
fixture for testing. All 9,243 payload entry names were
retained. Only classes3.dex changed outside signing metadata. All
9,842 classes in that partition were
compared; only Macro.invokeActions changed, with class metadata/other methods intact.

The original/Java/rebuilt comparison rejected that actual signed APK in
**113 cases**, with zero unsupported instructions, including
the required fixed-pause case. Release source, original fixture and release APK hashes
remained unchanged. The deliberately incorrect APK is diagnostic-only and is excluded
from both deliverable archives.

Temporary host mutations were independently rejected as follows. Failure counts below
are successful defect detections, not positive application test passes.

| Deliberate defect | Failing cases |
|---|---:|
| pause-must-not-terminate | 113 |
| group-marker-must-dispatch | 2 |
| goto-must-respect-scopes | 2 |
| strict-sixty-second-boundary | 25 |
| macro-all-disabled | 104 |
| light-equality | 53 |
| invalid-integer-default | 190 |
| hotspot-api-29-boundary | 160 |
| sunrise-widened-catch | 192 |
| lowercase-to-uppercase | 1110 |

All four new engine controls must fail a named targeted case; unsupported execution
cannot satisfy their rejection criteria. Correct host comparisons ran again afterward.

## 4. Coverage and explicit test boundaries

All represented original instruction offsets in the 11 supporting engine methods were
visited. The dispatcher visited 1,131 of 1,134 represented instructions. The remaining
three offsets (0x65c, 0x65d, 0x65f) are a later synchronous ShellScriptAction assignment.
In the supplied APK that final class implements ud1; the earlier ud1 handoff returns.
This local reachability argument is documented rather than changing the test hierarchy
to manufacture coverage. Instruction coverage is not exhaustive path/input coverage.

The interpreter is **not ART**, and host JDK libraries are **not Android libraries**.
Permissions, action implementations, resources, handlers, stores, constructors,
parent-thread scheduling and selected clocks remain controlled boundaries. A test-only
Java agent redirects selected host-loaded recovered classes, never the APK. Values,
selected state/identity, ordered boundary calls and exception types are compared;
selected VM-generated exception text, Android stack traces, scheduling, native behavior
and real app lifecycle are outside the comparison. Additional invocation/access checks
are explicitly bounded static checks, not the Android verifier.

The exact selected original fixture was freshly extracted from the supplied APK and
matches the test fixture byte-for-byte: 510,424 bytes, SHA-256
`930f65851078e8c23c52eb54499c8f751f528654686728800e0904392bd9b048`.
The separate fresh complete original decode also matches all preserved source.
Neither original APK nor original application DEX is a build input.

## 5. APK identities and remaining requirements

Baseline: 94,677,674 bytes, SHA-256
`aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096`.
This is the unchanged preservation control from v5–v7, not a newly modified app.

Hybrid: 94,682,893 bytes, SHA-256
`ae03a70edcf35c3c2b4f7c8a3b10594a75cb5e16893fd25d262a1e7e6d6e86e8`.
This contains the additional 12 engine Java bodies.

The original APK SHA-256 is
`84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`.
The new public test certificate SHA-256 is
`ca86cb5c4b75d5730f68d21cd0c196bfb93a849634924bcb1b9a1385073d6737`.
It is not the publisher's identity. Certificate-bound updates, permissions, integrations,
accounts, purchases and remote-service behavior remain unverified. No licensing,
authentication, payment or integrity-check bypass was introduced.

The fresh environment probe found no ADB, emulator, SDK Manager or Gradle and no
/dev/kvm. The official Android platform-tools download failed DNS resolution. The
executed availability recorder returns BLOCKED, not a successful device test.
No Android installation, launch, UI/screenshots, real macro execution, permission or
accessibility flow, background operation, native loading, persistence/reboot,
performance or external integration has been compared. Even an eventual smoke capture
would not prove all features equivalent. The Java reference tree remains noncompilable
as a complete application; most executable implementation remains editable smali, and
native C/C++ source has not been recovered. Actual Windows/macOS builds are untested.

## 6. Delivery and reproducibility

`acceptance.py` runs the full configured offline acceptance and records fresh exits/log
hashes. `release_integrity.py verify` checks exact pinned inputs. `package_release.py`
finishes each ZIP, reopens its central directory and reads every member for CRC and
SHA-256 validation before publishing the final filename. Final archive entries must
match the exact clean-tested input manifest. Only completed documentation/evidence is
updated after clean testing; no pinned implementation is silently changed.

See reports/clean-export-verification.json, acceptance-latest.json, the timestamped
acceptance logs, fresh-original-source-audit-v8.json, fresh-fixture-comparison.json,
*-roundtrip.json, *-resource-parity.json, *-signature-verification.log,
java-all-path-parity.json, java-engine-three-path-parity.json, *negative-control*.json,
full-apk-edit-probe.json, environment-v8.json and android-runtime/result.json.
External delivery verification and SHA256SUMS identify the final archive bytes.

**Verdict: the dispatcher checkpoint is now accepted as a reproducible editable-source
build with the stated static and bounded host evidence. Complete 1:1 Android behavior
and a full high-level source reconstruction remain unverified.**
