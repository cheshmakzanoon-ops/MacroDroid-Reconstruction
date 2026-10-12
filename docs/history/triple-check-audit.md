# Independent reconstruction quality audit

**Date:** 2026-10-08 (America/Halifax)

## Required standard

The requested deliverable was source code that **builds into** an app behaviorally indistinguishable from the supplied APK and is maintainable in an Android development environment. A high-level code reconstruction must have executable implementations, valid resources, complete dependencies/build files, and proven runtime behavior.

**Verdict:** That standard is **NOT met**.

## Gate A: Actually reconstructed source

| Test | Observed | Outcome |
| --- | --- | --- |
| First-party `.java` files | 3,306, all marked `DO NOT recreate app behavior` | Reference only |
| Executable Java method bodies | 0 in generated class outlines | FAIL |
| Assemblable `.smali` files delivered | 0 | FAIL |
| Gradle build files / wrapper delivered | 0 | FAIL |
| Decompiled instruction listings | 3,306 first-party `.dalvik.txt`, not real smali | Reference only |
| Ability to execute original supplied build script | `apktool: command not found` | NOT EXECUTABLE in current environment |
| Android SDK, ADB, Gradle, emulator | Not installed in this runtime | NOT EXECUTABLE |

The generated `.java` files are effectively annotated class shells. The source generator itself deliberately writes all field/method declarations as comments. A rebuild **from those Java files** would not reproduce the APK's functionality.

## Gate B: Exact static executable payload (new experiment)

| Test | Outcome |
| --- | --- |
| Original APK SHA256 | `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800` |
| Experimental repacked APK SHA256 | `63da03d5187ac8cc1fb92e61df77cc6531215e0012718fb18776a43413c7beba` |
| Non-signature payload entries | 9,243 exactly content-identical |
| Missing/extraneous non-signature entries | 0 / 0 |
| APK ZIP CRC | Original PASS / Repacked PASS |
| DEX files | 9, all unchanged |
| DEX class definitions | 71,267 |
| DEX internal SHA1 / Adler32 | PASS on all 9 |
| Binary AndroidManifest.xml | Exact content match |
| Compiled resource table (`resources.arsc`) | Exact content match |
| 22 native `.so` files | Exact content match |

**Interpretation:** If the original logic resided in a DEX file, it is retained byte-for-byte. This is **repackaging executable bytecode**, not generating new executable code from the recovered Java files.

## Gate C: APK format and functionality

| Test | Outcome |
| --- | --- |
| Original v1 signature | FAIL (`classes3.dex` digest mismatch) |
| Original v2 + v3 signatures | PASS verified signatures and chunk digests |
| New v1 JAR signature | PASS (`jarsigner -verify`) — self-signed debug certificate warnings |
| New v2 APK signing block | PASS independently checked RSA signature and signed-content digest |
| 4-byte aligned `resources.arsc` | PASS |
| 16 KiB aligned stored native libraries | PASS, 22 of 22 |
| Same signing certificate as original | NO — original private key not available |
| Android `apksigner` verification | UNTESTED — SDK unavailable |
| Install/launch on Android emulator | UNTESTED — SDK + emulator unavailable |
| UI screenshot and interaction comparison | UNTESTED |
| Trigger/action/constraint automation parity | UNTESTED |
| Notification, accessibility and background service parity | UNTESTED |
| Google Play, purchases, server and signature-bound integrations | UNTESTED; may fail with different certificate |

**Conclusion:** Three static checks were completed successfully for the **new repackaged binary**. The requested 1:1 maintainable source reconstruction has **not** been achieved or demonstrated.

## Trust and scope limitations

The original appears to have been tampered with or repackaged: invalid v1 signature, different valid v2/v3 signing identity, and a `Smob` modification-tool string. This is not enough to classify it as malicious. Treat both the supplied and repacked APK as untrusted. Testing the repack will only compare against the **uploaded version**, not necessarily a clean publisher version.

Real emulator/device tests, deep feature parity tests, and compiling from recovered high-level source are still necessary before claiming equivalence. No percentage estimate of functional parity is defensible from these static checks alone.

## Controlled modification test

A separate temporary rebuild deliberately replaced the existing entry `META-INF/androidx.appcompat_appcompat.version`. The build tool detected **exactly that one changed payload entry**, no other changed payload entries, no missing entries, valid ZIP CRCs, valid v1/v2 signatures and 16 KiB native-library alignment. The modified test APK was deleted afterwards. This proves raw ZIP-entry replacement works; it does **not** prove that arbitrary DEX or resource changes will run or that the app's Java/Kotlin source was reconstructed.
