# MacroDroid reconstruction v6 — measured quality report

**October 10, 2026. Complete Android runtime 1:1 equivalence is NOT established.**

Target: the user-supplied MacroDroid 5.67.8 APK, package `com.arlosoft.macrodroid`,
version code `896700008`, minimum API 23, target API 36. This is an executable low-level
source reconstruction with selected readable Java replacements, not the publisher's
original Java/Kotlin project, recovered native C/C++ source, or publisher-signed APK.

## 1. Input continuity

The received v5 source/toolchain ZIPs were checked again, including their closed
central directories, complete member CRCs and SHA-256 hashes. They matched their
recorded sizes and hashes. Unlike the historical v4 source archive, these inputs
were not truncated. See `reports/v5-input-integrity.json`.

The preserved original class inventory remains unchanged. The v5 original-to-source
fresh decoding evidence is retained under history; v6 separately checks the baseline
source hashes and full source-to-APK round trip. The selected original-method test
fixture was freshly extracted from the uploaded original for the v6 additions;
`tests/fixtures/provenance.json` pins its actual bytes. The fixture is test-only,
not an APK build input.

Original upload SHA-256:
`84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`.
The target is this exact upload, not an independently authenticated publisher release.

## 2. New Java recovery

The hybrid compiles **1,205 method bodies across 589 classes** from Java. This is ten
new methods in seven classes beyond v5, not a claim of whole-class recovery.

| Method family | Methods | Scope |
|---|---:|---|
| Previously migrated text/split/configuration logic | 76 | Existing v5 implementations retained |
| Previously migrated constant-return/no-op bodies | 1,119 | Simple bodies, not 1,119 complex app features |
| Macro invocation eligibility | 3 | The `Macro.canInvoke` overloads |
| Macro-running and light-level constraints | 2 | Each selected constraint evaluation method |
| Weather crossing, grouping, conversion | 3 | WeatherTrigger.z0, WeatherTrigger.x0 and cah.a |
| Variable/summary-event equality | 2 | Original identity and null-sensitive semantics |

The ten new methods are written as readable helpers under `source/java/recovered/core/`.
Original class fields, access flags, inheritance, annotations and method declarations
remain intact. Helpers are compiled by javac/D8 and transplanted as method bodies.
Compile/test stubs do not enter the APK. `source/core-methods.json` records original
method signatures and source hashes; `CORE_RECOVERY.md` describes their edge cases.

Six methods whose historical JADX output said `Method not decompiled` now have these
compiled, tested replacements. The reference tree is deliberately not cosmetically
rewritten: it still contains 1,893 files and 42 markers. Six markers are superseded by
the new executable helpers, while the other 36 marked failures and broader Java
compiler reconstruction remain unresolved. `Macro.invokeActions` is not migrated here.

## 3. Executed working-build checks

| Gate | Actual observed result |
|---|---|
| Baseline source assembly | All 9 DEX partitions freshly assembled from smali |
| Baseline class comparison | 71,267 classes / 349,972 method definitions; zero unexpected changes |
| Hybrid change isolation | Exactly 1,205 method bodies across 589 classes changed |
| Unmigrated method definitions | 348,767 preserved in the canonical comparison |
| Original source hashes | All preserved class hashes match the original inventory |
| Android manifest/resources | 7,212 decoded files; 7,211 byte-identical, one equivalent enum-order difference |
| Resource identifiers | All 23,854 retained |
| Resource paths / public-private visibility | Preserved |
| APK non-signature entry names | All 9,243 original names retained, no extra or missing payload entries |
| ZIP compression | Original per-entry compression choices retained |
| Native libraries | 22 original ARM64 libraries unchanged; ELF and ZIP alignment checks pass |
| APK signing | New v1/v2/v3 signatures verified by bundled AOSP apksig |
| Python tests | 66 executed; 66 passed |
| Primitive opcode conformance | 928 executed; passed |
| Selected-method three-way comparison | 130,015 cases over 1,205 methods; zero mismatches or unsupported executions |
| New core-method cases | 34,753, including 25,289 separately specified expected outcomes |
| Constant-body static proof | 1,119 recognized original/compiled bodies match |
| Migrated member references | 176 distinct references checked; 124 resolve inside original app/dependency hierarchy; no new unreviewed external references |
| All-disabled OR negative control | Rejected in 104 cases |
| Strict-light threshold negative control | Rejected in 53 cases |
| Lowercase-to-uppercase negative control | Rejected in 1,110 cases |
| Android install, launch, UI or automation | NOT EXECUTED |

Class/method totals include bundled dependencies and the embedded advertising DEX.
Canonical disassembly comparisons cover the represented declarations, instructions,
fields, annotations, exceptions and debug structures. They are partition-aware; they
do not prove byte identity of original versus rebuilt physical DEX table layouts.
The single normalized resource difference is enum/flag declaration ordering within
`attrs.xml`, not layout, array or other order-sensitive XML.

### Actual output APK identities

Baseline: 94,677,674 bytes,
SHA-256 `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096`.
This is byte-identical to v5's preservation-baseline APK. The baseline is retained as
a control, not advertised as a newly changed application.

Hybrid: 94,680,988 bytes,
SHA-256 `6324f2a1ba7ef005de24f23e9382662a39dddcc3d4b3ffec44aa67dca3acea62`.
This is the variant containing the ten new Java method replacements.

## 4. Host comparison scope and limitations

The three paths are original selected instructions from the pinned fixture, recovered
Java on the host JVM, and rebuilt selected instructions. The rebuilt DEX files are
checked against the signed hybrid APK before interpretation. The interpreter is
**not ART**, and JDK library behavior is **not Android library execution**.

The core vectors exercise macro gate states, OR/AND short-circuits, disabled constraints,
selected logging/call ordering and owner assignment, first name-match lookup, GUID/name
fallback, null cases, strict light comparisons, NaN/infinities/signed zero, weather
threshold crossings, weather-code groups, ordered conversions and equality decisions.
All represented original instruction offsets in the selected ten methods were visited
by the host vectors. This is not exhaustive path/input coverage, Android coverage or
coverage of called dependencies. Separately specified expected results supplement the
original/Java/rebuilt comparisons; they do not turn them into a general formal proof.

Store lookups, matching, debugger state, configuration accessors, macro/magic-text
expansion, resources, expression handling, constructors, enum/Parcel setup and
DictionaryEntry equality include controlled host doubles. In the actual APK those
calls still reference the preserved app/dependency implementations. Logs, selected
side effects, values, exception types, list/identity behavior and selected boundary
call order are checked. Concurrency, Android exception text/stack traces, lifecycle,
permission flows, scheduling and services are not covered.

The primitive test fixture checks AOSP-style NaN cmpg/cmpl, signed zero, integer widths,
raw float values and operation ordering. Uninitialized register reads and unsupported
executed instructions fail explicitly. Primary instruction context:
https://source.android.com/docs/core/runtime/dalvik-bytecode

Negative controls change temporary compiled helper classes only, require observable
comparison failures, verify source/APK preservation, and rerun the correct suite.
The deliberately failing cases are not counted as positive application test passes.

## 5. Source-derived assembly cache

The first ordinary build attempt exceeded the command limit and was not accepted as
a completed APK build. The subsequently completed run assembled all nine baseline
partitions, then built the hybrid using a validated source-derived cache for unchanged
partitions. Each cache key covers sorted source paths/contents, the pinned compiler
bundle and API/opcode settings. DEX size, SHA-1, Adler32 and SHA-256 are validated before
reuse. Cache corruption and invalidation paths are regression-tested.

Caches and output APKs are excluded from the archives. An empty-cache extraction must
assemble all nine baseline partitions again. Only these newly source-built outputs may
be reused by the hybrid. The cache is not original bytecode repackaging; per-partition
source fingerprints, output hashes and origins appear in `*-assembly-inputs.json`.

## 6. Independent archive rebuild and delivery verification

**Independent clean archive-extraction verification passed.** Both source and toolchain
archives were extracted into a new directory without build outputs, helper classes,
assembly caches or an original APK. An isolated HOME/temp environment was used for
the command run. All nine baseline DEX partitions were freshly assembled from smali;
the hybrid reused only the unchanged, source-derived partitions from that clean run.
Both code and resource verifiers, the 66 Python tests, 928 opcode cases, 130,015 selected
three-way cases and both negative-control scripts completed successfully. Correct
positive tests were rerun after the controls.

All **79,152 pinned build/test/tool/signing inputs** matched before and after.
Input snapshot SHA-256: `219652d86c75754ea19f06609dcf2a3d5ba29261d9980e34159bce3695edd1a8`.
Each clean APK is byte-for-byte identical to its corresponding working v6 APK,
**not** the original uploaded APK. Detailed commands, exit codes, input checks and
output hashes are recorded in `reports/clean-export-verification.json` and
`reports/clean-export-v6/`.

Final repackaging adds completed report/evidence and omits redundant superseded
historical resource dumps/input inventories, without altering the pinned build inputs.
Omitted historical dump hashes are recorded in `reports/history-dump-index.json`. Final archives are closed, reopened and checked member-by-member;
the external delivery-verification JSON and SHA256SUMS identify the final bytes.

## 7. Android, signing and high-level source gates remain open

This host has JDK 21 and the bundled offline build tools, but no ADB, emulator,
sdkmanager or Gradle, and no `/dev/kvm`. Official Android platform-tools downloads
failed. The executed recorder probe reports **BLOCKED** and
`android_runtime_executed: false`. No device result is inferred from the host tests,
assembler, signature checks or file comparisons.

No Android installation, cold launch, screenshot/UI parity, actual macro execution,
permission/accessibility flow, background service, notification, native load,
persistence/reboot, runtime performance, helper, account, purchase or server integration
has been tested. `ANDROID_ACCEPTANCE.md` records the required device comparisons.
The optional ADB recorder's fail-closed host paths are tested; its Android execution
path is not. Even a successful smoke capture would not establish whole-app parity.

The certificate is still the publicly distributed test identity, SHA-256
`ca86cb5c4b75d5730f68d21cd0c196bfb93a849634924bcb1b9a1385073d6737`,
not the publisher's. Certificate-dependent updates, permissions and integrations may
differ. No licensing, authentication, payment or integrity bypass has been introduced.
Original native libraries and opaque assets remain binary dependencies; native C/C++
source and the complete Java/Kotlin Android Studio build graph are not recovered.
Use only an isolated disposable ARM64 environment for the experimental APKs.

## Evidence navigation

- `reports/v5-input-integrity.json`, `tests/fixtures/provenance.json`
- `reports/baseline-build.json`, `reports/hybrid-build.json`
- `reports/baseline-roundtrip.json`, `reports/hybrid-roundtrip.json`
- `reports/baseline-resource-parity.json`, `reports/hybrid-resource-parity.json`
- `reports/baseline-assembly-inputs.json`, `reports/hybrid-assembly-inputs.json`
- `reports/baseline-signature-verification.log`, `reports/hybrid-signature-verification.log`
- `reports/java-all-path-parity.json`, `reports/java-core-three-path-parity.json`
- `reports/java-three-path-parity.json`, `reports/oracle-semantics.json`
- `reports/core-negative-controls.json`, `reports/negative-control.json`
- `reports/python-unit-tests.log`, `reports/migration-static-proof.json`
- `reports/release-input-snapshot.json`, `reports/clean-export-verification.json`
- `reports/environment.json`, `reports/android-runtime/result.json`

Historical v4/v5 evidence is not substituted for the fresh v6 results. This report
separates actual source/build/host evidence from the unexecuted Android acceptance gate.

**Verdict: the executable source build and the stated bounded checks pass. Full 1:1
Android functionality and a complete high-level source reconstruction remain unverified.**
