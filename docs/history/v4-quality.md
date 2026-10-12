# MacroDroid reconstruction v4 — measured verification report

**Date: October 9, 2026. Complete Android runtime 1:1 equivalence is NOT established.**

The user-supplied MacroDroid 5.67.8 APK is the comparison target. This release advances
from an instruction-source build to a tested **hybrid smali/Java source build**. It is
not an assertion that the original Java/Kotlin project, native source or publisher
signing identity has been recovered.

## Delivered variants

**Baseline:** all nine DEX files assembled from preserved, editable smali; Android
manifest/resources rebuilt from source; original resource paths and visibility restored.

**Hybrid:** the same project, with 74 existing method bodies across 11 classes compiled
from readable Java using javac and D8. Only those method bodies are transplanted into the
original class structures. All 349,898 other method definitions remain unchanged in the
canonical comparison. Compile/test stubs do not enter the APK.

## Verified results

| Gate | Observed result |
|---|---|
| DEX source assembly | 9/9 partitions compile, including the embedded advertising DEX |
| Baseline canonical comparison | 71,267/71,267 class definitions match; 349,972 method definitions covered |
| Hybrid change isolation | Exactly 11 classes / 74 method bodies changed; no unexpected method/class changes |
| Original source integrity | All indexed smali hashes match their preserved baseline |
| Decoded manifest and resources | 7,212 files: 7,211 byte-identical; one equivalent enum/flag-order difference in `attrs.xml` |
| Resource IDs | 23,854/23,854 retained |
| Original resource paths | All 6,898 paths retained; 6,670 required renaming after AAPT2 compilation |
| Resource visibility | Original public/private visibility retained; no resources spuriously made public |
| Non-signature APK entry set | All 9,243 original names retained, with no extra/missing entries |
| Original ZIP compression choices | Retained for all original non-signature entries |
| Opaque asset/native payload | Preserved bytes; no original application DEX or compiled resource table used as carrier inputs |
| Native libraries | 22/22 original ARM64 libraries preserved; ELF LOAD segment 16 KiB compatibility checked |
| APK alignment | All stored libraries 16 KiB-aligned after signing; other stored entries 4-byte-aligned |
| APK signing | AOSP apksig verifies new v1, v2 and v3 signatures |
| Python regression tests | 23 executed, 23 passed |
| Three-way host comparison | 28,477 cases across the 74 selected methods; zero mismatches |
| Negative control | Deliberately incorrect lowercase-to-uppercase change rejected in 100 cases |
| Clean archive extraction build | Both APK variants rebuilt without an original APK, original DEX build inputs, compiled helper cache or prior build directory |
| Reproducibility | Each clean-build APK is byte-for-byte identical to its corresponding working-build v4 APK, not to the uploaded original |
| Android install/launch/UI/automation | Not executed |

Canonical class comparison covers the declarations, instructions, annotations, debug
information and exception structures represented by the disassembler. It is partition-
aware because some library descriptors occur both in the embedded DEX and the main app.
It is not a byte-for-byte comparison of the original and reassembled DEX table layouts.

## Java reconstruction and test scope

The migrated methods include lowercase/uppercase conversion, trimming, substring bounds,
regex extraction/removal/replacement, escaped-newline decoding, direction-mark removal,
preview strings and configuration accessors. The split-array implementation, expression
evaluator, Android integration, constructors and remaining application methods are not
claimed migrated to Java.

The independent host comparison executes:

1. Original DEX instructions from a pinned, test-only class fixture.
2. The newly compiled Java implementations on the host JVM.
3. The freshly assembled hybrid DEX instructions.

The instruction execution uses `tests/java/BytecodeOracle.java`, a deliberately limited
interpreter, **not ART or Android**. Android resource lookups, macro/magic-text expansion,
integer-expression evaluation, constructors, enum setup and Parcel are controlled test
doubles. JDK string/regex/collection behavior supplies the host library boundary.
Unsupported executed instructions fail the harness. Values, exception **types**, selected
side effects, list identity and boundary call order are checked; exception messages,
stack traces, Android lifecycle and actual UI/service behavior are not.

A development test-harness error that confused boxed `Integer(0)` with a Dalvik zero/null
literal was found and fixed before the final runs. The complete positive suite was rerun.
The negative-control run changed a temporary compiled class only, confirmed 100 failures,
and reran the correct implementation. No regression was left in either downloadable APK.
These checks are bounded evidence, not exhaustive proof for every input or a whole-app
functional completion percentage.

The reference tree contains **1,893 `.java` files** and 42 `Method not decompiled` markers.
Those files remain reference-only; they are not a complete compilable Android Studio
Java/Kotlin project. The shipped native libraries remain binary dependencies, not recovered
C/C++ source.

## Packaging defects addressed

Simply reassembling code and signing was not accepted as a fidelity check. This release
also corrects recompiled resource paths, preservation of public/private flags, ZIP
compression choices and native-library alignment after signing. It uses the original
resource ID map and `--no-crunch`, and compares decoded image/resource files.
The only normalized XML difference is ordering of named enum/flag declarations within
`attrs.xml`; order-sensitive layouts, arrays and other XML are not normalized away.

The original DEX version is 035. Smali assembly uses its API-23 opcode/version setting
for that reason. The app's target SDK remains 36, its minimum SDK 23, and its original
compile-SDK metadata remains 37. A compilation or signature check is not a device/API
compatibility test.

## Original input and signing identity

Original APK SHA-256:
`84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`.

Fresh AOSP verification of that input reports v2/v3 signatures valid but v1 invalid:
`classes9.dex` is referenced by its JAR manifest but missing from the APK. This finding
does not by itself classify the APK as malware or authenticate it as a clean publisher
release. Previously reported baseline-profile inconsistencies were not converted into
an unverified optimization fix; original opaque metadata is retained.

New v4 development certificate SHA-256:
`ca86cb5c4b75d5730f68d21cd0c196bfb93a849634924bcb1b9a1385073d6737`.

The signing identity is openly distributed for isolated testing, not the publisher key.
Signature-bound app updates, helper integrations, permissions, accounts, purchases,
remote services and integrity-sensitive behavior remain unverified. No licensing,
authentication, payment or integrity-check bypass was introduced.

## Clean rebuild evidence

The source and toolchain archives were extracted into a fresh directory. Their 80,437
pinned source/tool/test input files were checked before and after the build. Both source
builds, complete class/resource checks and the 23 Python plus 28,477 three-way host cases
passed there. Final packaging adds documentation and the resulting evidence without
changing those pinned build/test inputs.

Input snapshot SHA-256:
`dd93a0051216ca7633ad8ab7c841512b1d69f9c1d06942dd27210d8bbd2e0361`.

Baseline v4 APK SHA-256:
`02ad2d56643fdf5464ab6e7bb122e292a1678bd6f002cdc307bfeba8ee595740`.

Hybrid v4 APK SHA-256:
`d2395979c40031a1cb626c3c12059974b05d244148c464c2cdc51f20266d00b1`.

## Remaining acceptance gates

No emulator, ADB device or Android execution was available. The environment has JDK 21
and the bundled build components, but no installed ADB/emulator/SDK manager/Gradle;
SDK-download DNS resolution failed. No installation, cold launch, macro execution,
permission flow, screenshot parity, accessibility/background-service test, native load,
server/account integration or performance claim follows from the host results.

`ANDROID_ACCEPTANCE.md` records the remaining real-device comparisons as **not executed**.
A full Java/Kotlin project and those runtime comparisons remain outstanding. Use only an
isolated disposable ARM64 environment for the experimental APKs, not a primary phone
with valuable macros or credentials.

## Reproducible evidence files

- `reports/baseline-roundtrip.json`, `reports/hybrid-roundtrip.json`
- `reports/baseline-resource-parity.json`, `reports/hybrid-resource-parity.json`
- `reports/baseline-signature-verification.log`, `reports/hybrid-signature-verification.log`
- `reports/java-three-path-parity.json`, `reports/negative-control.json`
- `reports/python-unit-tests.log`, `reports/java-integration.json`
- `reports/clean-export-verification.json`, `reports/release-input-snapshot.json`
- `reports/original-signature-verification.log`, `reports/android-runtime-availability.json`

**Verdict:** reproducible source builds and the stated bounded checks pass. Complete
1:1 Android functionality and a complete high-level source reconstruction are not yet
verified.
