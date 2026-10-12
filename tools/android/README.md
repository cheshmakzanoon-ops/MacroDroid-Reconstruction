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

The repository's `reconstruction.yml` workflow runs two independent jobs. The source job materializes the committed inputs, runs the complete configured host acceptance suite, and compares its freshly built hybrid APK byte-for-byte against the committed candidate. The Android job uses the exact same committed candidate and original reference APK, downloads the pinned runtime, requires the runner's allocated KVM device, and records actual cold launches on a fresh disposable emulator.

`run_ci_runtime.py` starts the service, waits up to 900 seconds for a completed boot and the required ARM64 bridge, configures and observes the capture environment, runs the recorder through the command queue, and compares complete screenshots and UI hierarchies. It records each command's actual exit code and stops its own emulator when finished. The recorder removes the known MacroDroid package and its app data between the two installs on this disposable device. It does not accept account, payment, or permission prompts.

Before either installation, `configure_capture_device.py` verifies the selected disposable AVD, requests real modem home registration and signal profile 4, and requires the primary Android telephony signal to remain at level 4 with identical measurements for at least 15 seconds. It then enables the documented SystemUI demo mode and requests a displayed clock of 12:00. Demo mode can also hold other status indicators at their state when enabled. The helper records the actual mode-controller state, modem measurements, battery state, device wall clock, and every ADB command; the recorder includes the two demo settings in both capture environments. The device's wall clock and battery values are left at their observed values. The helper has a 240-second queue deadline, and a configuration failure stops the run with its evidence preserved under `capture-device/`.

These controls address the first measured hosted comparison: both APKs launched and produced byte-identical UI hierarchies, while 75 decoded pixels differed within Android's signal-strength icon. The complete failed comparison remains in [`docs/verification/android-ci-ba52fd6/`](../../docs/verification/android-ci-ba52fd6/). Every pixel is still compared after configuring the environment; no screenshot regions, application content, or comparison thresholds were changed. A newly configured device run must establish the result independently.

A failed install, launch, capture, or exact comparison fails the Android job. Both successful and failed runs preserve their evidence as workflow artifacts. A successful cold-launch comparison covers only that measured screen and execution interval; it does not establish triggers, actions, constraints, scheduling, permissions, or external integrations. No screenshot regions or UI attributes are ignored by the comparator.

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
- [Android's ARM translation background](https://android-developers.googleblog.com/2020/03/run-arm-apps-on-android-emulator.html)
- [GitHub-hosted runner hardware acceleration](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
