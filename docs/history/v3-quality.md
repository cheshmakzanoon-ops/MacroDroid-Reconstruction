# Reconstruction v3 — measured quality gates

Date: October 9, 2026. Target: the user-supplied MacroDroid 5.67.8 APK, package `com.arlosoft.macrodroid`, version code `896700008`, minimum SDK 23, target SDK 36.

## What has actually been built

All nine DEX files are now assembled from real, editable smali. The manifest and Android resources compile from source using a pinned AAPT2 with explicit stable resource IDs. The APK is signed with a new development key using AOSP apksig. The original APK and original application DEX files are not build inputs.

The result is a real low-level source reconstruction, not a copy of the original compiled DEX with fixed-width patches. It is still not a complete Java/Kotlin reconstruction, original publisher-signed binary, or proven runtime-equivalent app.

## Verified code and resource fidelity

| Gate | Observed result |
|---|---|
| Executable code partitions | 9/9 assembled successfully: 8 root DEX plus the embedded audience-network DEX. |
| Canonical class round trip | 71,267/71,267 class disassemblies match; zero missing, extra or altered classes in the unchanged build. |
| Method definitions covered by class comparison | 349,972, including application code and dependencies. |
| Decoded Android manifest/resource files | 7,212 total: 7,211 byte-identical; one XML file has equivalent enum/flag declaration ordering. No missing, extra or semantically changed files. |
| Resource name/ID assignments | All 23,854 original assignments retained. |
| Baseline opaque payload | 9,234 non-DEX, non-signature entries preserved in the input carrier. |
| Native library preservation | All 22 original libraries retained unchanged. |
| Native ELF load-segment alignment | All 22 libraries have checked 16 KiB-compatible LOAD segment alignment. This is not a device compatibility test. |
| APK alignment | Stored native libraries aligned to 16 KiB; other stored entries checked for 4-byte alignment. |
| AOSP APK signature verification | v1, v2 and v3 pass over the API 23–36 verification range. |
| APK ZIP integrity / DEX checksums | Pass. |
| Compiler/source regression tests | 12 executed; 12 passed. |
| New method compilation | A real WidgetItem class copy was extended from 26 to 27 methods, including a new string-pool entry and conditional branches. Existing methods remained intact. |
| Growing method edit in a complete APK | A temporary larger `supportsChildren()` implementation was assembled and signed into the full app. Only the intended class changed in primary DEX; only `classes.dex` and signing metadata changed in the APK. The shipped source remains unchanged. |
| Windows path collision checks | Zero remaining case-fold file collisions. The executable source includes normalized case-colliding/reserved paths without altering class descriptors. Execution on Windows has not been tested. |

A canonical class comparison includes the instructions, declarations, annotations, exception-handling structures and debug information represented by the disassembler. It does not mean the original and rebuilt DEX files are byte-for-byte identical: physical table layout and padding can differ.

### Resource defects caught and fixed

The initial successful Apktool build was not accepted as proof of equivalence. Comparison identified 35 generated drawable IDs that had been reassigned, PNG transformations affecting hidden RGB values under fully transparent pixels, an inlined manifest resource reference, and enum declaration reordering. The final direct AAPT2 pipeline uses the complete original `--stable-ids` map and `--no-crunch`. Final re-decoding confirms the manifest, images, ID assignments and other resources match, apart from equivalent ordering of named enum/flag declarations in `attrs.xml`.

## Java and native-source status

JADX recovered 1,906 actual Java files, approximately 22.6 MB of high-level source, rather than the earlier empty class outlines. There were 81 reported processing errors and 286 warnings. The emitted Java includes 42 methods not reconstructed by JADX. It has not been repaired into a compilable Java/Kotlin application. That Java is **reference only**, while the complete smali implementations are the actual compiled code.

Native `.so` libraries are preserved as binary dependencies. Their original C/C++ source has not been recovered. See `HIGH_LEVEL_JAVA_STATUS.md` for the exact unfinished Java methods.

## Signing, input trust and optimization metadata

The new certificate is not the publisher's certificate. Its SHA-256 fingerprint is `de1dc56ea09e441d211d51f026148c01ba762a7b637174796795511a190ec14b`. The bundled signing identity is an explicitly public, development-only test key.

AOSP verification of the original upload reports valid v2/v3 signatures but a failing v1 signature because its JAR manifest references a missing `classes9.dex` entry. The uploaded baseline optimization profile also has checksums inconsistent with all six DEX entries that it names. Those inconsistencies already exist in the uploaded APK; the profile was preserved rather than silently rewritten using potentially incorrect method mappings. Runtime profile installation and performance are untested. These findings do not, by themselves, establish malware or authenticate the upload as a clean publisher release.

Certificate-bound app updates, signature permissions, purchases, account integrations, external services and integrity-sensitive behavior remain unverified. No licensing, payment, authentication or integrity-check bypass was introduced.

## Unverified gates

No Android emulator or connected ADB device is available in this environment. APK installation, cold launch, permission flows, screenshots, UI interaction, macro creation/execution, triggers, constraints, actions, accessibility services, notifications, background scheduling, persistence, real-device performance and multi-version compatibility have **not** been tested.

`device_smoke.py` is an optional, explicit installation/launch recorder for a disposable ARM64 device. Its no-ADB failure path was exercised; an Android execution was not. Even a successful smoke run would not establish complete 1:1 functionality.

**Verdict:** The code/resource source-build milestone is verified. Complete runtime 1:1 quality and a conventional high-level Java/Kotlin Android Studio reconstruction are not yet verified.

## Evidence inside this project

`final-source-build-summary.json` identifies the final APK and summary measurements. The detailed evidence is in `reports/latest-source-roundtrip.json`, `reports/latest-resource-roundtrip.json`, `reports/latest-resource-build.json`, `reports/resource-source-latest-source-build.json`, `reports/resource-source-aosp-sign-and-verify.log`, `reports/manifest-and-package-badging.json`, `reports/unit-tests.log`, `reports/full-apk-source-edit.json`, `reports/source-edit-demonstration.json`, `reports/native-elf-alignment.json`, `reports/original-aosp-verification.log`, `reports/baseline-profile-compatibility.json`, and `reports/android-runtime-availability.json`.

Clean export **passed**: the source ZIP was extracted into a new directory with no original APK, application DEX files or build cache. The default source build, full class/resource round-trip verification and all 12 regression tests succeeded there. The independently rebuilt signed APK was byte-for-byte identical to the primary build. See `reports/clean-export-verification.json`. The final export contains the exact tested build inputs plus this final evidence; no device result is inferred from this test.