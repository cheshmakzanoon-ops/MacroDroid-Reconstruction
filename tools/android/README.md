# MacroDroid Android runtime tooling

This directory records the Linux toolchain prepared for the MacroDroid reconstruction on 2026-10-12. The JDK and SDK archives are development infrastructure; the source, package pins, commands, and validation evidence are the reproducible deliverables.

## Installed packages

| Package | Version | Verification |
| --- | --- | --- |
| Eclipse Temurin JDK | 21.0.12.1+1 | SHA-256 from the official Adoptium release checksum |
| Android SDK Platform-Tools | 37.0.1 | Exact archive size and SHA-1 from Google's SDK repository metadata |
| Android Emulator | 37.2.12, build 16428233, stable channel | Exact archive size and SHA-1 from Google's SDK repository metadata |
| Google APIs x86_64 system image | Android 15 / API 35, revision 9 | Exact archive size and SHA-1 from Google's system-image metadata |

The download URLs, exact byte counts, published checksums, installation locations, and source URLs are in `android-toolchain-pins.json`. All four downloaded archives passed their published integrity checks before extraction.

## Reproduce the installation

Use Linux x86_64, Python 3.12 or later, and `curl`. Choose a tooling directory outside the Git checkout. Allow approximately 10 GiB of free disk for downloaded archives, extracted packages, and the disposable AVD's writable data.

Run from the directory containing these scripts:

```bash
python3 bootstrap_android_runtime.py \
  --root /absolute/path/to/tooling \
  --create-avd
```

The installer reuses installations whose pinned version metadata matches, verifies downloaded archives before extraction, and refuses to overwrite an existing installation with different metadata. It deletes only the specific downloaded archive files it created unless `--keep-archives` is supplied. It does not change system-wide Java settings or install an Android Studio desktop application.

To check an existing installation without downloading:

```bash
python3 bootstrap_android_runtime.py \
  --root /absolute/path/to/tooling \
  --verify-only
```

This runs Java, `javac`, ADB, and the headless emulator version commands and checks the system image's advertised ARM64 ABI and native-bridge properties. These checks passed for the installation created in this session. They do not establish application behavior.

The current installation root is `/workspace/scratch/4130730d15aa/tooling`. Its JDK executables are `jdk21/bin/java` and `jdk21/bin/javac`; ADB is `android/platform-tools/adb`.

## Disposable AVD configuration

The setup creates `MacroDroid_API35_Disposable` under the chosen tooling root's `android-user/avd` directory. Existing AVD data is reused without wiping or overwriting it.

| Setting | Value |
| --- | --- |
| System image | API 35 Google APIs x86_64 revision 9 |
| Console port / serial | 5560 / `emulator-5560` |
| Guest RAM | 3072 MiB |
| Virtual CPU cores | 2 |
| Display | 720 × 1280, 320 dpi |
| Renderer | SwiftShader |
| CPU acceleration | Off, with the documented `ANDROID_I_WANT_MY_TCG=yes` opt-in |
| Camera / audio | Disabled |
| Snapshots | Disabled |

The host's actual cgroup limit was 8 GiB RAM and 8 CPU-equivalents; `/dev/kvm` was absent. The ordinary graphical emulator binary reported a missing `libxkbfile.so.1`, while the required headless `-no-window` executable ran successfully without that GUI dependency. Android documents software CPU emulation as unsupported and very slow, so boot duration and test responsiveness must be measured rather than assumed.

The checksum-verified system image's `build.prop` directly contains:

```properties
ro.system.product.cpu.abilist=x86_64,arm64-v8a
ro.system.product.cpu.abilist64=x86_64,arm64-v8a
ro.dalvik.vm.native.bridge=libndk_translation.so
ro.enable.native.bridge.exec=1
ro.ndk_translation.version=0.2.3
```

These are observations from the actual API 35 archive. `runtime-properties.json`, when present, records the corresponding properties observed through ADB after Android reports a completed boot.

## Keep emulator and ADB in the same execution session

This executor's completed command invocations do not preserve a shared ADB server/localhost lifetime. A detached emulator launch therefore cannot be controlled reliably from an independent invocation. `android_runtime_service.py` starts ADB and the emulator in one persistent invocation and services explicit command requests through shared files. It uses ordinary subprocesses and never reassigns namespaces or bypasses network restrictions.

Start it in a persistent execution session:

```bash
python3 -u android_runtime_service.py \
  --tooling /absolute/path/to/tooling \
  --evidence /absolute/path/to/runtime-evidence
```

Keep that process alive. `runtime-status.json` reports boot state and observed properties. Wait for `state` to become `ready` and verify the expected serial and native bridge before installing an application.

On a Linux CI runner with working KVM, add `--acceleration on` to the service command. `on` requires hardware acceleration and fails if it is unavailable; `auto` lets the emulator select it. The default remains `off` for this session's software-emulation host. This option affects the next service invocation and does not change a running emulator.

Use the bounded readiness helper before installing applications:

```bash
python3 wait_android_ready.py \
  --evidence /absolute/path/to/runtime-evidence \
  --timeout 900
```

The helper requires a matching current launch, Android's `sys.boot_completed=1`, the ARM64 ABI, and the expected native bridge. It exits with failure on a stopped/exited service or an expired deadline. It never installs an application or changes device settings.

From a separate invocation, submit an explicit command:

```bash
python3 runtime_job.py \
  --queue /absolute/path/to/runtime-evidence/queue \
  --timeout 30 \
  -- /absolute/path/to/tooling/android/platform-tools/adb \
  -s emulator-5560 shell getprop ro.product.cpu.abilist
```

Existing test scripts can run in the same service session without an ADB wrapper:

```bash
python3 runtime_job.py \
  --queue /absolute/path/to/runtime-evidence/queue \
  --timeout 600 \
  --cwd /absolute/path/to/reconstruction \
  -- python3 /absolute/path/to/acceptance-script.py
```

Supply the acceptance script's actual arguments after its filename. The service adds the installed JDK and platform-tools directories to `PATH` and defines the matching Java and Android environment variables. Optional `--env NAME=VALUE` flags add explicit per-command values. Request arguments are JSON arrays executed directly; the service does not evaluate shell strings.

For binary output such as a screenshot, use the client's `--stdout-file` option:

```bash
python3 runtime_job.py \
  --queue /absolute/path/to/runtime-evidence/queue \
  --timeout 60 \
  --stdout-file /absolute/path/to/screenshot.png \
  -- /absolute/path/to/tooling/android/platform-tools/adb \
  -s emulator-5560 exec-out screencap -p
```

Each request leaves a JSON result containing its argv, timestamps, exit code, and stdout/stderr paths under `queue/responses`. The initial queue control check succeeded and observed `emulator-5560` in its early `offline` boot state. App installation and app behavior are separate validation steps.

Create the `queue/STOP` file to stop this disposable emulator service. That operation targets the emulator started by this service; it does not stop other devices. Remove that stop marker explicitly before starting the service again.

## GitHub verification

The repository's `reconstruction.yml` workflow runs two independent jobs. The source job materializes the committed inputs, runs the complete configured host acceptance suite, and compares its freshly built hybrid APK byte-for-byte against the committed candidate. Its artifact includes the actual `reports/java-staging.json` report. The Android job uses the exact same committed candidate and original reference APK, downloads the pinned runtime, requires the runner's allocated KVM device, and records the requested surfaces on a fresh disposable emulator. It also runs the separate, pinned constructor-allocation probe described below.

`run_ci_runtime.py` starts the service, waits up to 900 seconds for a completed boot and the required ARM64 bridge, verifies the pinned image's observed properties, configures and observes the capture environment, runs the probe and recorder through the command queue, and compares complete screenshots and UI hierarchies. It records each command's actual exit code, deadline, stdout and stderr, then stops its own emulator. The recorder removes the known MacroDroid package and its app data between the two installs on this disposable device. It does not accept account, payment, or permission prompts.

Before either installation, `configure_capture_device.py` verifies the selected disposable AVD, requests real modem home registration and signal profile 4, and requires one primary Android radio type and its computed signal level 4 to remain the same throughout a sampling window of at least 15 seconds. Raw signal measurements may vary within that computed level; all measurements remain in the evidence. It then enables the documented SystemUI demo mode and requests a displayed clock of 12:00. Demo mode can also hold other status indicators at their state when enabled. The helper records the actual mode-controller state, modem measurements, battery state, device wall clock, and every ADB command; the recorder includes the two demo settings in both capture environments. The device's wall clock and battery values are left at their observed values. The helper has a 240-second queue deadline, and a configuration failure stops the run with its evidence preserved under `capture-device/`.

These controls address the first measured hosted comparison: both APKs launched and produced byte-identical UI hierarchies, while 75 decoded pixels differed within Android's signal-strength icon. The complete failed comparison remains in [`docs/verification/android-ci-ba52fd6/`](../../docs/verification/android-ci-ba52fd6/). Every pixel is still compared after configuring the environment; no screenshot regions, application content, or comparison thresholds were changed. A newly configured device run must establish the result independently.

The first configuration attempt failed before either app was installed because its gate also required identical raw measurement strings. Its 18 samples all reported level 4; after an initial LTE-to-WCDMA transition, WCDMA RSSI changed from -53 to -73 dBm while the primary type and computed level remained stable. The complete failed artifact and analysis are preserved in [`docs/verification/android-ci-bebf448/`](../../docs/verification/android-ci-bebf448/). The corrected gate uses the primary type and computed level, which Android uses for general signal quality, and verifies both again at configuration completion. Run `38194498356` subsequently configured the actual emulator and measured byte-identical full PNG and XML captures for all four intro pages; its complete evidence is preserved in [`docs/verification/android-ci-95077fc/`](../../docs/verification/android-ci-95077fc/). That measured result precedes the new post-intro and ART scopes.

The focused host regressions exercise the actual helper loop with the preserved signal observations and simulated ADB/time. They cover raw readings changing within one level, a genuine level drop, a primary-radio change, missing or multiple modem entries, and a radio change at completion. Run them from the repository root:

```bash
python3 -B -m unittest discover -s tools/android -p test_configure_capture_device.py -v
```

These regressions do not execute an emulator or establish a runtime comparison result.

### Still-frame intro captures

`configure_capture_device.py --disable-animations` is an explicit option for the four-page intro still-capture scenario. It writes `0` to the global `animator_duration_scale`, `window_animation_scale`, and `transition_animation_scale` settings on the selected disposable emulator. The helper records all three values before and after configuration, preserves each command's output, and fails if any requested zero value is not observed. Without the option, it only reads those settings. The recorder must include all three settings in both app capture environments.

This configuration follows the original app's existing reduced-motion behavior. Its three intro layouts enable looping Lottie animations and omit the override that would ignore disabled system animations. The Lottie drawable reads `animator_duration_scale`; with a zero value, it selects a reduced-motion marker or a terminal frame and ends the animator. These three animation files contain no reduced-motion markers. Direct disassembly of the original APK reproduced the complete recovered `LottieDrawable` and `LottieAnimationView` smali files byte-for-byte. The source observations, original-APK proof, and file hashes are in [`lottie-still-capture-analysis.json`](../../docs/verification/android-environment/lottie-still-capture-analysis.json). The actual displayed frames and complete original/candidate captures from run `38194498356` are in the linked Android evidence archive.

The read-only disassembly check uses the existing pinned Apktool bundle and JDK 21, with a new output directory:

```bash
/absolute/path/to/tooling/jdk21/bin/java \
  -cp /absolute/path/to/reconstruction/tools/apktool_v3.0.3-26-0a1c54f7-SNAPSHOT.jar \
  tools/android/InspectOriginalLottie.java \
  /absolute/path/to/original.apk /absolute/path/to/new-lottie-disassembly
```

The option configures the test device before either app starts. APKs, resources, and capture bytes are preserved, and the full pixel/XML comparison remains strict. **Animation timing and motion parity are untested in this scenario.** A still-frame match covers the declared device configuration and captured pages; it does not establish matching animated frames, frame rates, transitions, or synchronization.

### First surface after intro completion

The CI recorder now requests `--intro-pages --post-intro`. After recording all four pages, it rechecks the installed APK's device-side SHA-256, environment, live PID, foreground IntroActivity, and a fresh hierarchy that must still exactly match the recorded `CONSTRAINTS` page. The observed final control remains `com.arlosoft.macrodroid:id/button_next`, an enabled, clickable `ImageButton` with description `Next`; the original activity changes its listener and icon on the final page. The recorder derives its bounds and center from the fresh hierarchy and issues exactly one completion tap. It never assumes a `Done` selector or a clean home screen.

The resulting full PNG, hierarchy, foreground and PID observations are saved before the recorder classifies the surface. It accepts only the app's `NewHomeScreenActivity` as an observed app landing surface, or the Android notification-permission activity with the expected MacroDroid notification message and both permission controls. It makes **zero permission choices**. Unexpected surfaces fail the new scope with their initial evidence preserved. An app landing capture does not establish usable home features or dismiss any app dialog.

`android_post_intro.py` rechecks the installed identity, fresh completion preconditions, command evidence, stable resulting hierarchy/foreground, live interval and environment. It compares every decoded pixel and the complete XML state, including a system-owned permission dialog when observed. A claimed match requires the previous complete intro comparison too. The new post-intro scope remains Android-pending until a real run records and compares it.

### Standalone constructor allocation on ART

[`probes/constructor-probe.dex`](probes/constructor-probe.dex) contains exactly one runtime class, `Lrecovered/probe/ConstructorProbe;`: 1,436 bytes, SHA-256 `85f53ad51a1a85fd2161bd485db9f12556f737b0745f6e26ffdff31a927d5281`. The adjacent [`constructor-probe.json`](probes/constructor-probe.json) binds it to the frozen constructor proof at commit `c7abf086ebffbc70cb3143f909a7f48648de22bc`, [`work-in-progress/constructor-owner/02-pipeline-proof/checkpoint.json`](../../work-in-progress/constructor-owner/02-pipeline-proof/checkpoint.json), manifest SHA-256 `98d73cb9f3c73731e2a376bfdb446704674b2019e996a59483263f0d37b31e9a`. That checkpoint preserves the Java source, direct original-APK observations, actual D8 output, transformed smali, and byte-identical roundtrip proof. CI uses these exact DEX bytes; it does not perform a fresh compiler stage for this narrow probe.

`android_constructor_probe.py` validates the original APK's exact size/hash, the DEX's complete hash and internal checksums, its single class, and the frozen provenance before any device mutation. It requires the explicitly selected disposable AVD and the pinned Android 15 image properties. It pushes only the probe and unchanged original APK into a fresh UUID-named `/data/local/tmp/md-constructor-*` directory, makes both files read-only, and observes their exact device-side SHA-256 values. Compile-only stubs are absent from the runtime classpath; the original APK supplies the real `Lzhh;`, `Lrff;` and other referenced classes.

The helper invokes `/apex/com.android.art/bin/dalvikvm64 -Xverify:all` with the probe and original APK as its classpath. Android 15 maps that verification option to enabled verification. A guest `/system/bin/timeout -s KILL 120` bounds the VM, while a longer host command deadline preserves diagnostic output and permits cleanup. The queue permits at most 780 seconds for all preflight, transfer, VM and cleanup commands. Every command and output is retained. Success requires exit zero and exactly `CONSTRUCTOR_ALLOCATION_OK class=zhh arity=2` on stdout, with no ART error or exception in stderr. The helper then removes only its own temporary directory and verifies its absence. The driver rechecks the report's input/device identities, VM invocation, and hashed command-output artifacts before accepting its result.

This probe installs no app and makes no UI interaction. Its result concerns the legality of this single allocation through the original public `Lrff;` constructor. It does not execute a reconstructed Widget workflow or establish Widget behavior, native-library parity, or app parity. **Actual ART execution remains pending for this new scope.**

### Independent outcomes and failure evidence

After the requested device stages, the driver always attempts all three comparators, including after a failed boot, configuration, probe, recorder or earlier comparator. Missing and malformed reports produce explicit report errors and false gates. Each accepted comparison must have the expected success status, a true boolean result, observed Android execution, and the exact original/candidate input hash pair. The cold result must also establish installed APK identities; the longer scopes must establish all of their required observations.

| Runtime report field | Required evidence |
|---|---|
| `cold_launch_capture_equal` | Successful strict cold comparator for the current installed input pair |
| `intro_sequence_equal` | Successful strict four-page and three-transition comparator |
| `post_intro_surface_equal` | Successful strict comparison after one completion tap per APK |
| `requested_capture_gate_passed` | Recorder exit zero, configured device, and all three comparison gates |
| `constructor_allocation_on_art_verified` | Independently rechecked ART invocation, input identities and exact command-output artifacts |
| `constructor_probe_gate_passed` | Observed allocation, helper exit zero, success status and completed cleanup |
| `all_requested_runtime_checks_passed` | Both requested gates, successful service exit, and no recorded stage failure |

All measured pass fields begin false. A post-intro failure preserves completed cold and intro evidence and permits those narrower comparators to report their actual results. An ART failure still permits both app captures and all comparisons; a capture failure does not erase a completed ART result. The final CI exit fails unless every requested gate passes. `full_runtime_1_to_1_established`, animation parity and home-feature parity remain false.

The new helper and orchestration host controls use simulated ADB/process responses to exercise rejected inputs, ART errors, guest/host deadlines, cleanup failures, later-scope failures and invalid comparison reports. They establish host behavior only. Run all Android tooling controls from the repository root:

```bash
python3 -B -m unittest discover -s tools/android -p 'test_*.py' -v
```

The workflow preserves this log in a separate `android-tooling-host-tests-*` artifact. Actual Android outputs remain in `android-cold-launch-*`: `constructor-probe/`, `capture/`, `capture-device/`, individual command logs under `stages/`, selected runtime environment files, and `runtime-run.json`. No screenshot regions or UI attributes are ignored. A successful requested capture covers only those measured surfaces and intervals; triggers, actions, constraints, scheduling and external integrations still require their own execution evidence.

The same orchestration can be run directly after installing the toolchain, using a new output directory:

```bash
python3 tools/android/run_ci_runtime.py \
  --tooling /absolute/path/to/tooling \
  --source workspace/MacroDroid_v9 \
  --original workspace/artifacts/MacroDroid-5.67.8-original.apk \
  --candidate workspace/artifacts/MacroDroid-5.67.8-current-hybrid.apk \
  --output /absolute/path/to/new-runtime-evidence \
  --acceleration on
```

## Evidence handling

Publish the authored Python files, pin manifest, setup notes, and the relevant completed validation outputs. The SDK/JDK binaries and writable AVD disks should remain outside the repository. Inspect emulator logs before publication and omit transient ADB key material or unrelated runtime noise; observed ABI properties, command outcomes, and application captures are the useful evidence.

Source references:

- [Official Adoptium JDK checksum](https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk_x64_linux_hotspot_21.0.12.1_1.tar.gz.sha256.txt)
- [Google SDK repository metadata](https://dl.google.com/android/repository/repository2-3.xml)
- [Google APIs system-image metadata](https://dl.google.com/android/repository/sys-img/google_apis/sys-img2-3.xml)
- [Android emulator command-line documentation](https://developer.android.com/studio/run/emulator-commandline)
- [Android emulator telephony controls](https://developer.android.com/studio/run/emulator-console#telephony-emulation)
- [Android 15 primary signal and computed level](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/telephony/java/android/telephony/SignalStrength.java)
- [Android 15 SystemUI demo mode](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/packages/SystemUI/docs/demo_mode.md)
- [Android global animation-scale settings](https://developer.android.com/reference/android/provider/Settings.Global#ANIMATOR_DURATION_SCALE)
- [Lottie's disabled-animation frame selection](https://github.com/airbnb/lottie-android/blob/master/lottie/src/main/java/com/airbnb/lottie/LottieDrawable.java)
- [Android's ARM translation background](https://android-developers.googleblog.com/2020/03/run-arm-apps-on-android-emulator.html)
- [GitHub-hosted runner hardware acceleration](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
