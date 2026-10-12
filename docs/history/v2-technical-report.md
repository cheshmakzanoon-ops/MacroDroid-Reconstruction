# Technical recovery report

## Identity and coverage

- MacroDroid 5.67.8, package `com.arlosoft.macrodroid`, versionCode 896700008.
- Android minSdk=23, targetSdk=36; 119 uses-permission entries in compiled manifest.
- 9 DEX files (8 top-level, plus 1 embedded advertising DEX), total of 71,267 defined classes.
- App namespace: 3,306 classes and 31,284 methods.
- 4,349 compiled XML views recovered; XML numeric references remapped to semantic resource names in 29,282 places.
- 23,854 namespaced resource identifiers recovered.
- This is NOT a fully recompilable Java/Kotlin version. The authoritative executable code is still DEX.

## APK provenance and warnings

The PKCS#7 v1 signing certificate in the uploaded APK has subject `CN=LyerXz99,C=ES`. **The JAR v1 signature is invalid** (`jarsigner -verify -strict` reports `SHA-256 digest error for classes3.dex`). The APK also includes v2 and v3 signing blocks for a *different* certificate subject `C=IN`; a custom read-only signing-block parser cryptographically verified their RSA signatures and their complete 1 MB chunk content digests. See `inventory/apk-signing-block-check.json`. This mixed state can cause compatibility problems and is consistent with a modified or resigned APK, but does not by itself prove malware.
A string in recovered application DEX says `Smob - Mod obfuscation tool v1.4 by Kirlif`; this indicates additional build-time processing may be present.
Neither provenance nor malware safety have been established. The certificate is not the original signing private key.

## Native libraries

- `lib/arm64-v8a/libCrashGuard.so`
- `lib/arm64-v8a/libandroidx.graphics.path.so`
- `lib/arm64-v8a/libapkdaddy.so`
- `lib/arm64-v8a/libapminsighta.so`
- `lib/arm64-v8a/libapminsightb.so`
- `lib/arm64-v8a/libbuffer_pgl.so`
- `lib/arm64-v8a/libc++_shared.so`
- `lib/arm64-v8a/libdatastore_shared_counter.so`
- `lib/arm64-v8a/libfile_lock_pgl.so`
- `lib/arm64-v8a/libgifimage.so`
- `lib/arm64-v8a/libglide-webp.so`
- `lib/arm64-v8a/libimage_processing_util_jni.so`
- `lib/arm64-v8a/libimagepipeline.so`
- `lib/arm64-v8a/libnative-filters.so`
- `lib/arm64-v8a/libnative-imagetranscoder.so`
- `lib/arm64-v8a/libnms.so`
- `lib/arm64-v8a/libpglarmor.so`
- `lib/arm64-v8a/libquickjs.so`
- `lib/arm64-v8a/libstatic-webp.so`
- `lib/arm64-v8a/libsurface_util_jni.so`
- `lib/arm64-v8a/libtranslate_jni.so`
- `lib/arm64-v8a/libtt_ugen_layout.so`

## Recovered first-party entry points

Examples to explore under `reference/dalvik/com/arlosoft/macrodroid`: `LauncherActivity`, `MacroDroidService`, `AppContext`, `StartupReceiver`, `action/`, `triggers/`, `constraint/`, `variables/`, `plugins/` (where present).

## Rebuild expectations

- *Strongest fidelity*: preserve original DEX/resources; bytecode-level patch/rebuild with Apktool; understand limits of re-signing.
- *Most readable*: run JADX on the entire APK or on primary application DEX files; treat results as reference, not a source build.
- *Maintainable app*: replace the application module incrementally with authored Kotlin/Java code, test automation action/trigger/constraint behavior and permissions across Android versions, and replace removed proprietary service integrations as appropriate. This is significant engineering work and has not been done here.

## Validation limitations

Original v1 signature verification failed, while v2/v3 verification passed. No Apktool or Android SDK build-tools are installed in this runtime; the APK was not reassembled or executed. Instruction listings are for inspection and cover app-specific code, not every third-party class; complex switch payload and catch metadata may need manual inspection in APKTool.

## Main app module class counts

| Module | Defined classes |
|---|---:|
| `action` | 1130 |
| `triggers` | 717 |
| `constraint` | 350 |
| `scene` | 196 |
| `widget` | 103 |
| `variables` | 82 |
| `ai` | 65 |
| `(root)` | 54 |
| `data` | 49 |
| `templatestore` | 35 |
| `plugins` | 33 |
| `events` | 30 |
| `upgrade` | 28 |
| `common` | 24 |
| `utils` | 23 |
| `uicomponent` | 20 |
| `extras` | 18 |
| `settings` | 18 |
| `celltowers` | 16 |
| `drawer` | 14 |
| `firebase` | 14 |
| `geofences` | 14 |

Counts include compiler-generated inner classes and nested classes, not independent fully recovered Kotlin/Java files.
