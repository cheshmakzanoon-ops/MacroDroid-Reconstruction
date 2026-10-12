# MacroDroid 5.67.8 — APK reverse-engineering work package

**IMPORTANT: This is a partial code-recovery work package, NOT a finished 1:1 high-level Java/Kotlin reconstruction.**

## Original binary identity

- Package: `com.arlosoft.macrodroid`, version 5.67.8, versionCode 896700008
- Minimum SDK 23, target SDK 36; compiled SDK reported in manifest: 37
- SHA-256 of uploaded file: `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`
- ZIP integrity: PASS (all entry CRCs tested)
- App-specific classes: 3,306; app-specific methods: 31,284; overall DEX classes: 71,267
- 8 main DEX files plus 1 nested advertising DEX; 22 native ELF `.so` files
- APK **v1** signature certificate subject `CN=LyerXz99,C=ES`; Java `jarsigner -verify` FAILS on `classes3.dex` (SHA-256 digest mismatch). The APK also has cryptographically verified **v2 and v3** signing blocks with a different certificate subject `C=IN`. Android 6 requires v1; its installation may fail. An embedded string references "Smob - Mod obfuscation tool v1.4 by Kirlif". **This file may be a repacked or modified build; its provenance and trustworthiness have NOT been verified.**

## What is in the project?

- `original/`: byte-identical supplied APK. Includes all dex, assets, resource binaries, and native libraries.
- `dex/`: extracted primary compiled code; original runtime logic resides here.
- `extracted/`: all `assets/`, native `lib/`, `tables/`, and resource files that are not XML; retained from APK without editing.
- `reference/xml/`: 4,349 readable XML representations, with 29,282 internal resource references resolved to names. These are **inspection copies**, not a fully valid Android resource compiler source tree.
- `reference/dalvik/`: all 3,306 application-specific class listings with 31,284 method bodies disassembled into readable register-level Dalvik instructions; code addresses and source references are recorded. Listings are NOT syntax-checked smali.
- `reference/java-signatures/`: 3,306 **API outlines only** (.java) with class names, superclasses, field/method prototypes. **Methods are comments, not executable recovered code.**
- `inventory/all-classes.tsv`: 71,267 DEX class inventory.
- `inventory/first-party-api.jsonl`: searchable first-party field and method inventory.
- `inventory/resource-ids.tsv`: 23,854 resource ID→type/name/value mappings.
- `tools/`: fully offline Python source used to generate inventory and reference files. Requires Python 3.10+, plus `lxml` for XML decoding.
- `scripts/`: commands to do **real, editable smali decoding and rebuilding** on your computer with Apktool + Android SDK, and to produce reference Java decompilation with JADX.

## Work on the running app: bytecode-level build workflow

Prerequisites: Java/JDK 17 or later; [Apktool](https://apktool.org/); Android SDK build-tools (`apksigner`, `zipalign`); optional [JADX](https://github.com/skylot/jadx) for readable Java. Test devices need Android 6.0 or later; API 36 behavior must be tested separately. Apktool 3.x with `-a` is recommended to handle the nested dex.

### Windows PowerShell — from project root

```powershell
.\scripts\recover-and-build.ps1 decode
# Edit workspace\apktool-rebuildable\smali* and decoded res/XML as needed
.\scripts\recover-and-build.ps1 build
# Output: dist\macrodroid-rebuilt-debug-signed.apk

# Optional readable Java decompiler output (does not drive the build):
.\scripts\recover-and-build.ps1 java
```

If you use the standalone Apktool `.jar`, set `$env:APKTOOL_JAR` to its absolute path before running the script. Ensure `apktool` (or the jar), and Android build-tools, are installed.

### macOS/Linux — from project root

```bash
bash scripts/recover-and-build.sh decode
# Edit workspace/apktool-rebuildable/smali*/... and resources
bash scripts/recover-and-build.sh build
# Output: dist/macrodroid-rebuilt-debug-signed.apk

# Optional readable Java decompiler output:
bash scripts/recover-and-build.sh java
```

### What is actually compiled?

**Apktool assembles smali back to DEX and compiles the decoded resources.** This preserves much more executable behavior than compiling the API-only `.java` scaffolds. The resulting APK must be zipaligned and signed. The provided debug key is NOT the original publisher's key. It will not be a byte-for-byte match; update installation against an existing installation may be rejected by Android, and signature-bound APIs, licensing, and third-party services may fail.

## Why there is no fully reconstructed Android Studio source project yet

This APK was generated from heavily optimized/obfuscated Android code (R8 + signs of additional modifications). Decompiled Java cannot restore all original Kotlin constructs, sources, original symbol names, Gradle module structure, resources/build-time inputs, signing private key, backend services, nor the native C/C++ source for its shared libraries. Decompiled Java can have syntax errors and control-flow recovery failures; simply clicking Build in a generated Gradle project is unlikely to reproduce behavior.

**Do not compile the `java-signatures` directory expecting a working application.** It is a code-navigation aid. The bytecode-level edit/rebuild path is the workable first step toward a closer reconstruction.

## Verification status

- PASSED: complete uploaded ZIP CRC scan and v2/v3 signature + signed-content digest verification.
- FAILED: v1 JAR signature verification (`SHA-256 digest error for classes3.dex`). This is not a clean conventional signing state.
- PASSED: all 9 DEX files parsed; 71,267 class definitions indexed; 31,284 app method bodies walked with no fatal disassembly exceptions.
- PASSED: 4,349 readable XML files generated, 23,854 resource IDs mapped, 29,282 internal refs substituted.
- NOT EXECUTED: apktool decoding/assembly, Android SDK signing, installation, runtime and UI equivalence tests; toolchain was not available in the analysis runtime.
- NOT CLAIMED: 1:1 original Java/Kotlin source, byte-for-byte rebuild, or feature parity of a rebuilt APK.

### Integrity check

```bash
python scripts/verify-inventory.py
```

### Navigation

For example, the service entry point's recovered register-level instructions are at `reference/dalvik/com/arlosoft/macrodroid/MacroDroidService.dalvik.txt`. The corresponding API outline is in `reference/java-signatures/com/arlosoft/macrodroid/MacroDroidService.java`. Once Apktool is installed, its canonical **editable and assemblable smali** source will appear under `workspace/apktool-rebuildable/`.

All APK contents remain subject to applicable third-party copyrights, redistribution terms, and permissions.
