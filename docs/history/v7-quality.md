# MacroDroid reconstruction v7 — measured quality report

**October 10, 2026. Full Android runtime 1:1 equivalence is NOT established.**

Comparison target: the user-supplied MacroDroid 5.67.8 APK, package
`com.arlosoft.macrodroid`, version code `896700008`, minimum API 23, target API 36.
This is an editable low-level reconstruction with selected Java-compiled bodies,
not the original Java/Kotlin project, recovered native source or publisher-signed APK.

## 1. Input continuity and original comparison

Both received v6 archives passed new SHA-256, central-directory and full-member CRC
checks and matched the recorded delivery hashes. No archive truncation was observed.
`reports/v6-input-integrity.json` records the exact inputs. Historical v6 acceptance
reports are under `reports/history-v6/`; they are not substituted for v7 results.

Original upload SHA-256:
`84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`.

The new test fixture was freshly extracted from the exact original APK. It contains
selected original implementations for 596 classes / 1,220 method bodies; its SHA-256
is `dd099d9e39a8197fa3c337a9e012a1bf15be0eec8425c039a83b730abd1ba962`.
The fixture and original APK are not application build inputs. Their source and
selection are pinned in `tests/fixtures/provenance.json`.

A fresh complete decode of all nine original DEX partitions matched all 71,267 preserved class sources, covering 349,972 method definitions. All 7,212 original manifest/resource source files matched byte-for-byte, all 23,854 IDs and original resource visibility matched, and original opaque payload, 9,243 non-signature names and compression choices matched. This is an original-to-preserved-source check, distinct from the rebuilt-resource check with one equivalent enum-order difference. See `reports/fresh-original-source-audit-v7.json`; rerun the optional, test-only `audit_original.py ORIGINAL.apk` to reproduce it. The original is not a build input and was not executed.

## 2. Actual Java recovery

The hybrid compiles **1,220 existing method bodies across 596 classes** from Java,
15 more methods in seven classes than v6. Counts are not feature-completion percentages.

| Family | Bodies | Scope |
|---|---:|---|
| Prior constant-return/no-op recovery | 1,119 | Simple strictly recognized bodies, not complex features |
| Prior text/split/configuration logic | 76 | Existing implementations retained |
| Prior macro/weather/constraint/equality logic | 10 | Existing v6 helpers retained |
| New system-setting evaluation | 3 | System/Secure/Global dispatch and numeric/text comparisons |
| New Wi-Fi and hotspot evaluation | 2 | Original permissions, states, aliases and API branches |
| New sunrise/sunset constraint | 1 | Location parsing, clock comparison and error boundaries |
| New pattern matching | 4 | Wildcard/regex/full/contains operations and logging |
| New long parsing | 1 | Overflow, signs, malformed strings and Unicode digits |
| New solar computations | 4 | Original BigDecimal/trigonometric and Calendar operations |

The new helpers are in `source/java/recovered/environment/`, with original method
signatures and source hashes in `source/environment-methods.json`. The javac/D8 pipeline
replaces only registered method bodies; original class metadata, method signatures,
fields, constructors, annotations and unregistered methods stay intact. Compile/test
stubs are not included in the APK. The project does not include a runnable Java
replacement for the whole application.

### Semantics that were preserved rather than silently corrected

Settings-name expansion remains outside the provider-read catch region; unknown
value types and invalid numeric text retain their original defaults. Wi-Fi location
permission checks still apply on API 27 and later, even to some state queries. Legacy
SSID migration precedes the switch, and all 33 original localized any-network aliases
are retained. Hotspot client-count handling changes at API 29, and the original
reflection/error fall-through behavior remains.

Solar results use the original ordered BigDecimal and trigonometric calculations,
including four-place HALF_EVEN rounding, BigDecimal(double), DST handling, minute
rollover and polar null results. No alternative astronomical algorithm was substituted.
The focused decompiler widened a NumberFormatException handler; the recovered Java
instead follows the original DEX exception region. Coordinate construction and solar
calculation outside that region do not silently become a false constraint result.

`ENVIRONMENT_RECOVERY.md` describes the exact recovered methods and test boundaries.

## 3. Completed working-build verification

| Gate | Observed result |
|---|---|
| Baseline source assembly | All 9 DEX partitions assembled from editable smali |
| Baseline canonical code comparison | 71,267 classes / 349,972 method definitions; no unexpected changes |
| Hybrid change isolation | Exactly 1,220 bodies in 596 classes changed; no unexpected changes |
| Unmigrated method definitions | 348,752 unchanged in canonical comparison |
| Preserved source hashes | All match the original class inventory |
| Manifest/resource round trip | 7,212 files: 7,211 byte-identical and one equivalent enum-order difference |
| Stable resource identifiers | 23,854 preserved |
| APK payload names | All 9,243 original non-signature names retained |
| Resource paths, visibility, compression | Original choices retained |
| Native binaries | All 22 ARM64 libraries unchanged; ELF and stored ZIP alignment checked |
| APK signatures | New v1/v2/v3 verified by bundled AOSP apksig |
| Python tests | 85 executed; 85 passed |
| Primitive opcode conformance | 2,458 cases passed |
| Selected-method three-way comparison | 160,699 cases across 1,220 methods; zero mismatches/unsupported execution |
| New environment comparison | 30,684 cases, including 15,536 separately specified expected checks |
| Simple-body static checks | All 1,119 recognized original/compiled bodies match |
| Member-reference provenance | 313 distinct references; 179 resolve in original app; no new unreviewed external references |
| Additional invocation/access check | Passed within its stated static scope |
| Android installation or execution | NOT EXECUTED |

The 160,699 cases comprise 95,262 legacy, 34,753 core and 30,684 environment cases.
The environment suite additionally exercises three previously recovered Macro.canInvoke
overloads through selected real recovered constraint, matcher and parser bodies.
Its exact before/equal/after solar-event vectors and polar/no-event vectors add 250
boundary cases. Unvisited instruction offsets remain explicitly reported; the suite
is not exhaustive path/input coverage.

Class/method counts include bundled libraries and the embedded advertising DEX.
Canonical comparison covers the represented declarations, instructions, exceptions,
annotations and debug information. It does not assert identical physical DEX layout.
The only normalized resource difference is enum/flag ordering in `attrs.xml`, not
layout ordering, arrays or arbitrary XML normalization.

### Working output identities

Baseline: 94,677,674 bytes; SHA-256
`aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096`.
This is byte-identical to the v5/v6 preservation baseline, retained as a control.

Hybrid: 94,682,288 bytes; SHA-256
`460340b04ee7ef05ddb9f11898d2d13f055ce951662ee97631213283754ba9ec`.
This is the APK containing the additional v7 Java method bodies.

## 4. Negative controls and comparison scope

Three new temporary incorrect implementations were rejected: replacing the invalid
integer default with one, mishandling hotspot API 29, and widening the sunrise catch.
Their observed failing cases were 190, 160 and 192 respectively. The retained macro,
light-threshold and lowercase controls also rejected their intentional defects
(104, 53 and 1,110 cases). Failure counts are not counted as positive test passes.
The scripts check source/APK preservation and rerun the correct implementations.

The three paths are original selected DEX instructions, recovered Java on the host
JVM, and freshly built selected DEX instructions. Rebuilt DEX bytes are compared to
the signed hybrid APK before interpretation. The oracle is a deliberately limited
instruction interpreter, **not ART**, and JDK behavior is **not Android execution**.

Settings providers, radio/permission state, location storage, logging/macro expansion,
float parsing, constructors/static setup and other explicit integration boundaries
use controlled host doubles. Selected matching, long parsing and solar helpers are
interpreted as nested calls, rather than substituted with expected outcomes.

A test-only Java agent fixes Calendar.getInstance in host-loaded recovered code only;
it does not modify the APK, original DEX, source or Java framework classes. Tests
compare return values, BigDecimal values/scales, exception types, selected log/call
order, mutable state and identity. VM-generated NPE message text is excluded in one
hotspot-null-manager case; the type and ordered log prefixes still compare. Android
exception text, stack traces, scheduling, concurrency and service behavior are outside
these tests. Primitive opcode fixtures cover widths, overflow, signed zero, NaNs,
conversions, division and operation ordering; unsupported executed instructions and
uninitialized registers fail explicitly.

The new `linkage_verify.py` checks invocation kind and selected static/private access
against original declarations. Its report records 779 invocation and 185 field
occurrences, of which 229 invocation and 175 field accesses are checked against the
preserved app hierarchy. External/unresolved occurrences are separately reported.
This is not the ART verifier and does not prove protected/package access, receiver
flow, framework availability, initialization or classloader behavior.

## 5. Independent delivery verification

**Independent clean archive-extraction verification passed.** Both provisional
source/toolchain archives were extracted into a new directory. Working reports were
removed before testing except the pinned input manifest, so prior pass files could
not substitute for clean results. The extraction initially had no build outputs,
application APKs, assembler cache or compiled helper classes. HOME and Java temporary
paths were isolated. The original APK was not a build input; the selected original
instruction fixture remained explicitly test-only.

All nine baseline DEX partitions were freshly assembled. The hybrid reused only
unchanged partitions assembled from source by that clean run. Both code/resource
checks, 85 Python tests, 2,458 primitive cases, 160,699 three-way method cases and all
six deliberate-defect controls completed successfully. The full correct suite was
rerun after all controls. Every command exit code and evidence path is recorded in
`reports/clean-export-verification.json` and `reports/clean-export-v7/`.

All **79,193 pinned build/test/tool/signing input files** matched before and
after the clean run. Input snapshot SHA-256:
`09a7c8322b43c5b6537bc4a2b4393f3730863c500b1101a3fcad6a393b35ddd5`.
Each clean APK is byte-for-byte identical to its corresponding working v7 APK,
**not** the original upload. Delivered APK copies come from that clean run.

Final packaging updates completed reports/documentation without changing these
pinned inputs. Four large, byte-identical duplicate clean-report files are stored
once at their parent report paths. `reports/clean-export-v7/deduplicated-reports.json`
records the exact retained paths, sizes and hashes; no build/test/tool/signing input
is omitted. Archives are closed, reopened, checked member-by-member for CRC and
SHA-256, and checked against the exact clean-tested input manifest. External delivery
verification and checksum files identify the final archive bytes. No Android result
is inferred from source, host or archive checks.

## 6. Open Android and high-level-source gates

The fresh environment probe found no ADB, emulator, sdkmanager, Gradle or /dev/kvm.
A new official platform-tools download attempt failed with DNS resolution error.
A targeted connector search did not supply a usable Android-device testing provider.
The recorder probe actually returned BLOCKED with android_runtime_executed=false.
See `reports/environment-v7.json` and `reports/android-runtime/result.json`.

No Android install, cold launch, UI screenshot parity, real macro run, permission
prompt, native library load, accessibility/background service, persistence/reboot,
performance, helper, account, payment or server-integration test has run here.
`ANDROID_ACCEPTANCE.md` records these unexecuted gates. No pass is inferred from
host cases, static preservation, signatures or an APK build.

The historical reference tree contains 1,893 Java files and 42 failed-decompilation
markers. **11 now map to registered executable Java replacements; 31 do not.**
These marker counts are not the total remaining engineering effort. Many other
reference files still need compiler/semantic repair, and most code remains smali.
There is no complete Android Studio Java/Kotlin build graph or recovered native C/C++.

The retained public test certificate SHA-256 is
`ca86cb5c4b75d5730f68d21cd0c196bfb93a849634924bcb1b9a1385073d6737`,
not the publisher's identity. Certificate-bound updates, permissions and integrations
may differ. No licensing, authentication, payment or integrity-check bypass was added.
Original native libraries and opaque assets remain binary dependencies. The comparison
target is the supplied APK, not an independently authenticated publisher release.
Use only an isolated disposable ARM64 test environment, not a primary phone with
valuable macros or credentials.

## Evidence

Current reports: `fresh-original-source-audit-v7.json`, `v6-input-integrity.json`,
`baseline-build.json`, `hybrid-build.json`, `*-roundtrip.json`, `*-resource-parity.json`,
`*-assembly-inputs.json`, `*-signature-verification.log`, `java-all-path-parity.json`,
`java-environment-three-path-parity.json`, `java-core-three-path-parity.json`,
`java-three-path-parity.json`, `oracle-semantics.json`, `python-unit-tests.log`,
`environment-negative-controls.json`, `core-negative-controls.json`, `negative-control.json`,
`migration-static-proof.json`, `migration-linkage-check.json`, `reference-failures-status.json`,
`release-input-snapshot.json`, `clean-export-verification.json` and `clean-export-v7/`.
All are inside `reports/`. Historical/development files are not acceptance substitutes.

**Verdict: measured editable-source/build/static/host evidence has advanced. Complete
Android runtime 1:1 equivalence and a complete high-level source reconstruction remain
unverified.**
