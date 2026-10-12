# MacroDroid reconstruction v5 — measured quality and delivery recovery

**October 9, 2026. Full runtime 1:1 equivalence is NOT established.**

Comparison target: the supplied MacroDroid 5.67.8 APK (`com.arlosoft.macrodroid`,
version code `896700008`). This release is an editable hybrid source build, not the
publisher's original Java/Kotlin project or a publisher-signed replacement.

## 1. The v4 source delivery was actually damaged

The mounted `MacroDroid_v4_Source.zip` was **97,442,662 bytes**, ended partway through
the source inventory, and lacked a ZIP central directory. Its actual SHA-256 was
`501a3523430d5eee96ecad0f9a0451e46125b643b8f2ceff11c2eb681174f224`.
That is not the previously advertised source ZIP hash. An intentional second
materialization returned the same incomplete bytes. The v4 toolchain and both v4
APKs did match their prior recorded hashes; the defect concerned the source delivery.

Recovered 38,685 complete local ZIP entries with CRC checks, then regenerated 41,736
missing smali files from the original uploaded APK using the pinned disassembler.
**All 71,267 restored class files match the recorded v4 class-source hashes**, with
zero mismatches. The missing signing/build helpers and compile/host-test boundaries
were recreated and re-tested; they were not recovered verbatim from the damaged ZIP.

A final independent check freshly decoded **all nine partitions of the original
uploaded APK**, including the initially salvaged classes rather than trusting only
the earlier index. All **71,267 source classes** match that fresh original disassembly,
with zero missing, extra or different classes. All **7,212 source manifest/resource
files** match a fresh decode of the original byte-for-byte; the 23,854 resource IDs,
public/private state and opaque payload also match. This original-to-source check is
separate from the source-to-rebuilt-resource check below, which has one equivalent
enum-order difference. See `reports/fresh-original-source-audit.json` and the fresh
original decode logs. This does not execute the application.

The resulting build does not require the original APK or original application DEX
files. Original-bytecode fixtures are isolated test inputs. Original native libraries
and opaque assets remain binary dependencies. Evidence: `reports/archive-recovery.json`,
`reports/v5-source-recovery.json`, and the complete source hash checks.

## 2. New Java source work

The hybrid now compiles **1,195 existing method bodies across 582 classes** from Java:

| Family | Methods | Meaning |
|---|---:|---|
| Prior text/string/preview/configuration migrations | 74 | Restored v4 Java implementations |
| Newly recovered constant/no-op bodies | 1,119 | Simple, strictly recognized instruction forms, not complex features |
| Split-array execution and enum names | 2 | New Java implementations of `SplitManipulation.applyArray` and `getEnumNames` |

The split implementation preserves literal-delimiter processing, supported leading
zero-width/direction markers, escaped newlines/carriage returns, trailing empty-field
handling, string/integer/decimal/boolean outputs, unknown type behavior and numeric
conversion failures. Integer parsing remains 32-bit before widening to a stored long.
Macro expansion and Android integration are still controlled boundaries in host tests.

Constant/no-op recovery excludes constructors, class initializers, field access,
branches, calls and exception handlers. The static proof independently parses original
and compiled instruction bodies, compares their return kind/value, checks original
method hashes and verifies argument-register widths. Unused Object bridge arguments do
not change the original APK method declaration. These are source migrations, not a
completion percentage for application behavior.

The migrated body reference check covered **88 distinct method/field references**,
resolved 51 in the preserved application/dependency hierarchy, and found zero new
unreviewed external references. It caught a compile-signature issue and an inherited
method-owner mismatch during development; both were fixed before final verification.

## 3. Actual working-build checks

| Gate | Observed result |
|---|---|
| Baseline source assembly | All nine DEX partitions compile, including embedded advertising code |
| Baseline code round trip | 71,267 class definitions, 349,972 methods; no changed/missing/extra classes |
| Hybrid change isolation | Exactly 1,195 method bodies in 582 classes changed; no unexpected method/class changes |
| Unmigrated method definitions | 348,777 remain unchanged in the canonical comparison |
| Preserved baseline source hashes | All 71,267 match the recorded class index |
| Manifest/resource round trip | 7,212 decoded files: 7,211 byte-identical; one equivalent enum/flag ordering difference in `attrs.xml` |
| Stable resource IDs | All 23,854 assignments preserved |
| APK payload entry names | All 9,243 original non-signature entry names retained, no extra/missing entries |
| Resource paths | All 6,898 retained; 6,670 paths restored after resource compilation |
| ZIP compression / resource visibility | Original choices and public/private state preserved |
| Native payload | 22/22 original ARM64 libraries unchanged; ELF and stored ZIP alignment checks pass |
| New APK signatures | AOSP apksig validates v1/v2/v3 over the stated API verification range |
| Python regression tests | 52 tests executed, 52 passed |
| Selected-method host comparison | 95,262 three-way cases; zero mismatches or unsupported executed instructions |
| Constant-body static checks | 1,119 recognized bodies checked; zero proof errors |
| Negative control | Deliberate lowercase-to-uppercase error rejected in 1,110 cases; correct tests rerun |
| Android execution | Not performed; ADB/emulator unavailable |

Canonical code comparison includes class declarations, fields, instructions, annotations,
exception-handling structures and represented debug information. It is partition-aware.
It does not assert original and regenerated DEX physical table layouts are identical.

Baseline APK SHA-256:
`aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096`.

Hybrid APK SHA-256:
`700e0f1d937a2a156ecdf597417477a4788843765283de6558ccd168b8d0baa4`.

## 4. Test coverage is bounded, not Android equivalence

The three paths are original DEX instructions in the pinned fixture, recovered Java on
the JVM, and rebuilt DEX instructions. The interpreted rebuilt DEX files are checked
against the bytes in the signed hybrid APK before testing.

Cases include null/empty/invalid configuration, selected Unicode and UTF-16 boundaries,
escaped newlines, regex errors/group references, type and integer overflow boundaries,
delimiters, array conversion, configuration access and deterministic generated strings.
Nonconstant families run under root, Turkish and German locales. All 1,195 registered
methods are covered; the counts are 3,357 constant-family cases, 15,723 split-family cases,
and 76,182 prior text/string-family cases.

`tests/java/BytecodeOracle.java` is a **strict, limited host instruction interpreter,
not ART**. Android resource lookups, macro/magic-text expansion, integer-expression
handling, constructors, enums and Parcel are controlled test doubles. JDK libraries
supply string/regex/collection semantics. Unsupported executed instructions fail the
harness rather than being silently skipped. Outcomes compare values, exception types,
selected side effects, list identity and selected boundary-call order. Exception
messages, stack traces, Android-library differences and app lifecycle are not covered.

The negative control mutates only a temporary compiled helper. The shipped source and
APKs remain unmodified. Its expected failure is kept separately; positive results were
produced by rerunning the correct implementation, not by editing pass flags.

## 5. Delivery verification and clean rebuild

Release creation uses `package_release.py`: it finishes and closes each ZIP, reopens
its central directory, checks the exact unique entry set, reads every member for CRC
validation, and compares decompressed SHA-256 hashes to its input. Only then is the
`.partial` archive renamed to the final `.zip`. This directly addresses the observed
v4 source-delivery defect.

**Clean-export verification passed.** Both source/toolchain archives were extracted
into a new directory with no previous build output or compiled helper cache. The
original APK was not present there as a build input. Both baseline and hybrid APKs
were assembled, signed, fully compared against the source/class/resource inventories,
and tested there. The 52 Python tests, 95,262 three-way host cases, 1,119 constant-body
checks and deliberately failing negative control passed their stated acceptance rules.
The correct positive suite was rerun after the negative control.

All **79,122 pinned build/test/tool/signing input files** matched before and after the
clean run. Input snapshot SHA-256:
`024d30b15ceb9d30775f9e475fa51a099252b994a2dd290520331e6eeea9cfdf`.

The independently built baseline and hybrid APKs each match their corresponding
working-build v5 APK **byte-for-byte**. This is v5-to-v5 reproducibility, **not** a claim
that either APK is byte-identical to the original uploaded APK. The complete outcome
is recorded in `reports/clean-export-verification.json`; the copied clean-run outputs
are under `reports/clean-export/`.

Final packaging adds documentation and completed evidence without changing the pinned
inputs used by that successful clean run. The final archives are again closed and
member-checked; the external delivery verification and checksum files identify their
actual bytes. No Android execution is inferred from archive or host-test success.

## 6. Remaining acceptance gates

The reference Java tree contains **1,893 files and 42 “Method not decompiled” markers**.
It is not a complete compilable Android Studio Java/Kotlin project. Native C/C++ source
has not been recovered. Most executable implementation remains editable smali.

No installation, cold launch, screenshot/UI parity, real macro execution, trigger or
constraint engine, permission flow, background/accessibility service, notification,
native load, persistence/reboot, performance, helper integration, server/account or
payment test has been observed on Android. See `ANDROID_ACCEPTANCE.md`. The optional
ADB recorder's no-ADB/no-serial safety paths pass host tests; its Android execution
path has not been run. `reports/android-runtime/result.json` correctly says BLOCKED.

The development certificate remains
`ca86cb5c4b75d5730f68d21cd0c196bfb93a849634924bcb1b9a1385073d6737`,
not the publisher's certificate. The bundled signing identity is intentionally public
and test-only. Certificate-dependent updates, permissions and integrations may differ.
No license, authentication, payment or integrity bypass has been added. The comparison
is to the supplied APK, whose legacy signature/optimization metadata is inconsistent,
not to a separately authenticated publisher release.

**Verdict: complete editable low-level source recovery and expanded Java migration with
measured build/static/host-test evidence. Whole-app Android runtime 1:1 quality and a
complete high-level source reconstruction remain unverified.**

## Current evidence

- `reports/archive-recovery.json`, `reports/v5-source-recovery.json`, `reports/fresh-original-source-audit.json`
- `reports/baseline-build.json`, `reports/hybrid-build.json`
- `reports/baseline-roundtrip.json`, `reports/hybrid-roundtrip.json`
- `reports/baseline-resource-parity.json`, `reports/hybrid-resource-parity.json`
- `reports/baseline-signature-verification.log`, `reports/hybrid-signature-verification.log`
- `reports/java-three-path-parity.json`, `reports/migration-static-proof.json`
- `reports/python-unit-tests.log`, `reports/negative-control.json`
- `reports/release-input-snapshot.json`, `reports/clean-export-verification.json`
- `reports/android-runtime/result.json`, `reports/environment.json`

Historical v4 reports under `reports/history-v4/` describe earlier work. They are not
substitutes for fresh v5 results, particularly given the actual source-archive defect.
