# Reconstruction acceptance gates — October 9, 2026

## Objective
A high-fidelity, *workable source representation* of the uploaded MacroDroid 5.67.8 APK, ultimately able to compile and behave identically to the uploaded application. A high-level Android Studio source project is distinct from lossless binary repackaging.

| Test / required property | Actual observed result | Status |
| --- | --- | --- |
| All uploaded APK payload intact, no code edit | 9,243 / 9,243 non-signature ZIP members unchanged | **PASS** |
| Uploaded native libraries / assets / binary resources | All preserved exactly in zero-edit APK | **PASS** |
| Signed/debug APK production (zero edit) | Created APK; valid new v1 and v2 signatures | **PASS** |
| Stored native libraries 16 KiB ZIP aligned | 22/22 aligned | **PASS** |
| Readable instruction-level source for owned code | 3,306 classes with actual bytecode bodies | **PASS** |
| Source vs original first-party DEX | All 3,306 files regenerated and checked | **PASS** |
| Compiling a real user edit into DEX | `WidgetItem.supportsChildren()Z`: `0112` to `1112` | **PASS** |
| Mutation isolation | One executable byte changes outside DEX header; only `classes.dex` APK entry changed | **PASS** |
| Patched DEX SHA-1 and Adler32 | Both valid | **PASS** |
| Patched APK v1/v2 signatures / ZIP CRC | All valid | **PASS** |
| Automated local compiler regression suite | Six tests run, six passed | **PASS** |
| Unrestricted Dalvik method/resource editing | Fixed-width subset only | **NOT MET** |
| Original Java/Kotlin implementations reconstructed | No high-level runnable Java/Kotlin implementation | **NOT MET** |
| Native C/C++ original source recovered | Native `.so` preserved but not decompiled | **NOT MET** |
| Open and build as a standard Android Studio AGP project | No Android Gradle Plugin source build | **NOT MET** |
| Test APK installation and launch | No emulator/ADB available locally | **NOT TESTED** |
| UI, macro actions, triggers, background permissions behave identically | No device runtime comparison | **NOT TESTED** |
| Identical signing identity, signature permissions, licensing behavior | Publisher private key unavailable | **NOT MET** |

## Why the word “1:1” is not justified yet

Static preservation of executable bytecode strongly supports code *payload* fidelity, but a newly signed copy of an APK may not work exactly the same on Android due to signature-bound app identity, package updates, privileged permissions, and integrations. In addition, instruction-level overlay editing is not maintainable high-level source. Runtime instrumentation is essential before claiming feature parity.

## Evidence

- `reports/zero_edit_audit.log`, `reports/zero_edit_static_audit.json`: byte-for-byte payload audit and v1/v2 signature verification of new zero-edit APK.
- `reports/full_source_comparison.log`: all source files re-decoded from DEX and compared.
- `reports/unit_tests.log`: actual Python unit test run.
- `reports/demonstrated_real_code_edit.json`: method and exact offset of actual DEX change, checksum and signing validation.
- `reports/actual_build.log`, `reports/verified_rebuild_audit.json`: real patched-code APK build and audit (patched test APK not intended as release).

## Next actual engineering gates

1. Obtain a real Apktool 3.x and JADX runtime, decode *all* smali and resources, prove an Apktool reassembly build without errors and compare DEX class/method counts and resources.
2. Create a standard Android Gradle project with recovered source modules and dependencies, progressively replace bytecode with compilable Java/Kotlin and test each module. The original source, variable names, and build graph cannot be mechanically reconstructed exactly.
3. Test the repackaged APK on an isolated Android emulator; capture cold launch, crash traces, screen flows, macro creation, triggers, constraints, actions, background operation, and permission/UI differences.
4. Re-run multi-version and API 23–36 tests, then quantify validated feature parity only after execution evidence exists.
