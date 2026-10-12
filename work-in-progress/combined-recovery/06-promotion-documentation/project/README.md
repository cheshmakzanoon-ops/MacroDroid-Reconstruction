# MacroDroid 5.67.8 — editable reconstruction v9

**Executable source reconstruction with selected Java methods. Not a verified 1:1
Android replacement or the publisher's original source project.**

The uploaded APK is the comparison target, package `com.arlosoft.macrodroid`, version
code `896700008`. Eight main DEX files plus one embedded DEX build from editable smali;
1,242 selected method bodies across 605 classes in the hybrid are compiled from Java.
The manifest and resources rebuild from source. Original native libraries and opaque
assets remain binary dependencies. The original APK and application DEX files are
not build inputs. A selected original-instruction fixture is used only by tests.

## Current candidate and evidence

This combined candidate adds plugin upload and Widget update bodies to the prior
1,240-method source. Its complete configured acceptance passed on 12 October 2026:
all 16 gates, 193,489 three-path cases across 1,242 methods, 273 Python tests, all 78
UI faults with exact positive restoration, and the signed source-edit experiment.
The [closed proof](../work-in-progress/combined-recovery/05-full-acceptance/result.json) binds the exact source and signed APK.
Android observations for this new combined APK remain pending. See
`RECONSTRUCTION_STATUS.md` and `COMBINED_RECOVERY.md` for measured scopes.

## Extract and build

Extract **both** `MacroDroid_v9_Source.zip` and `MacroDroid_v9_Toolchain.zip` into the
same parent directory. Together they create one `MacroDroid_v9` directory.

Requirements: JDK 21 (`java` and `javac`) and Python 3.11 or newer. The compilation,
DEX assembly, resource and signing components are bundled. The offline build does
not require Gradle, SDK Manager, an emulator or a network connection. Those missing
runtime facilities must not be confused with Android testing.

From this directory:

```sh
python release_integrity.py verify
python build.py build --variant hybrid
python build.py verify --variant hybrid
python resource_verify.py --variant hybrid
python test.py --three-way
```

Use `python3` where appropriate. On Windows PowerShell, use a short extraction path
and set `$env:PYTHONUTF8="1"` before running these commands. The source paths have been
normalized for case/reserved-name collisions. Actual Windows/macOS execution has
not been verified; the executed build evidence is from Linux x86-64 and JDK 21.

Output: `dist/MacroDroid-5.67.8-v9-hybrid.apk`.

To also build the preserved instruction-level control:

```sh
python build.py build --variant baseline
```

Output: `dist/MacroDroid-5.67.8-v9-baseline.apk`. This control remains unchanged from
the verified v5–v8 baseline; it is not advertised as a newly changed application.

## Full configured offline acceptance

```sh
python acceptance.py
```

This builds both variants; compares their class/method and resource inventories;
runs the Python, primitive-opcode and all five migration suites; checks deliberate
faults; proves an isolated Java edit reaches a signed APK; reruns the correct
positive suites; and verifies the pinned input files did not change. It records
actual subprocess exit codes and evidence hashes under `reports/acceptance-*` and
`reports/acceptance-latest.json`. It stops on failure. It does not install an APK.
The availability probe and the whole-app 1:1 status remain separately recorded.

`--skip-edit-probe` omits the isolated signed-edit experiment and records that omission;
it is not the complete release acceptance configuration.

## Editing

Recovered text, core, environment, engine and UI implementations are under `source/java/`.
Touch events, selection validation, scene state/dispatch, plugin lookup/upload and
Widget update bodies are under `source/java/recovered/ui/`; dispatcher helpers remain
under `source/java/recovered/engine/`. `source/java-method-map.json` maps compiled helper
bodies back into the original class structures. Only registered bodies are
transplanted; test-support classes and helper classes never ship in the APK.

Remaining executable logic is under `source/smali/`; use
`python build.py find-class WidgetItem` (or another class name) to locate it.
Android manifest, strings, layouts, images and ID maps are under `source/android/`.
`reference/java/` is historical decompiler output, not a separately compilable app.

After a deliberate change, the original delivery-integrity manifest is expected to
report a mismatch. That is not a build failure, and recording a new manifest by itself
does not validate the change. Rebuild and run the relevant comparisons. Changes to
preserved baseline smali also require intentional review of the original comparison
inventory; do not delete checks merely to make them green.

`UI_RECOVERY.md`, `ENGINE_RECOVERY.md`, `CORE_RECOVERY.md` and `ENVIRONMENT_RECOVERY.md` explain the
method mappings and boundaries. `RECONSTRUCTION_STATUS.md` distinguishes current measured results from unresolved
gates. `QUALITY_REPORT.md` and older reports retain their historical scope.

## Signing and runtime limitations

The signing key is an openly distributed development-only identity, not the
publisher's. Do not use it for production credentials or interpret its signatures
as publisher authenticity. Certificate-dependent updates, permissions, integrations,
accounts, purchases and remote services may behave differently. No licensing,
authentication, payment or integrity bypass is introduced.

The historical Android runs retain their exact source/APK identities. The prior
9108 candidate's ten-screen observation completed and retained a 26-pixel indicator
difference on the second intro page; all ten XML pairs matched. Both APKs also
encountered the supplied promotion-listener exception. The isolated Widget APK
passed a separate eight-case ART method probe. Those results do not execute this
new combined APK or establish full macro, service, persistence or device behavior.
The host interpreter and controlled dependencies have their own explicit scope.

`android_acceptance.py` is a separate explicit cold-launch recorder for a disposable ARM64
device. It requires an explicit serial and consent to removal of this package's data;
it does not silently choose a phone, grant permissions, log in or click consent.
Both APKs must pass identity and package preflight before removal of any package.
Successful installation alone does not count as application execution. Live PID samples,
foreground activity, app-owned UI XML and a valid screenshot are required for a
completed capture. `android_compare.py CAPTURE_DIRECTORY` then checks the same device
settings and exact full pixels/UI attributes. Even a match establishes only that
cold-launch capture, not full 1:1 functionality. The schema-3 recorder also offers four
English intro pages with three observed Next transitions. See
[RUNTIME_CAPTURE.md](RUNTIME_CAPTURE.md) for actual outcomes, installed-APK identity
checks, declared device settings, and the still-capture scope. Its new rejection
rules use synthetic host tests; a fresh device run must establish the result.

Use experimental APKs only in an isolated disposable test environment, not on a
primary phone containing valuable macros or credentials.
