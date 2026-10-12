# Why the Widget probe uses AndroidRuntime

This is a source-backed launcher assessment, not an Android execution result. The eight complete primary source files were fetched from the immutable `android-15.0.0_r1` tag on 12 October 2026, retaining their Apache 2.0 headers, exact bytes and SHA-256 identities in `reports/primary-sources/`. The first web page reads of AndroidRuntime and app_main used the Android15 release branch; the final conclusions below were checked against the saved tag files. Failed web retrievals were resolved by the official Gitiles `?format=TEXT` endpoint, without substituting third-party source.

## Framework native registration

`Looper.prepareMainLooper()` calls `prepare(false)`, and the Looper constructor creates a real MessageQueue. The MessageQueue constructor immediately calls `nativeInit()`. These are actual framework operations, not host substitutes. See [Looper.java](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/core/java/android/os/Looper.java), saved lines 110–136 and 365–367, and [MessageQueue.java](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/core/java/android/os/MessageQueue.java), saved lines 77–87.

The Widget manager's preserved static initializer constructs a Handler using the main Looper. It also constructs coroutine/context, collection and receiver objects. The eight cases therefore need framework initialization even though they do not call widget services or provide an application Context. The initializer is not described as a Handler-only operation.

`AndroidRuntime::start` creates the VM, then calls `startReg` before invoking RuntimeInit's Java main method. `startReg` processes `gRegJNI`, whose table includes `register_android_os_MessageQueue`. That registration function registers the MessageQueue native method table, including nativeInit. See [AndroidRuntime.cpp](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/core/jni/AndroidRuntime.cpp), saved lines 1244–1259, 1588 and 1690–1718, and [android_os_MessageQueue.cpp](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/core/jni/android_os_MessageQueue.cpp), saved lines 246–266.

The standalone ART `dalvikvm` entrypoint directly starts the VM and invokes its requested class; it does not perform AndroidRuntime's framework registration sequence. This makes missing MessageQueue JNI registration a concrete source-based risk for the Widget probe on that launcher. No failed Widget dalvikvm run was observed or invented. The existing successful constructor allocation probe has a smaller dependency scope and is left unchanged. See [dalvikvm.cc](https://android.googlesource.com/platform/art/+/refs/tags/android-15.0.0_r1/dalvikvm/dalvikvm.cc), saved VM startup and invocation code.

## Classpath, verifier and stdout

The chosen launcher is `/system/bin/app_process64` in tool mode. `app_main.cpp` forwards VM options before the unused parent-directory argument and explicitly handles `-cp` as an option with a following value. It supplies the `tool` argument to RuntimeInit when `--application` is absent. RuntimeInit redirects System.out/System.err only for `application`, so tool mode preserves the probe's stdout. See [app_main.cpp](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/cmds/app_process/app_main.cpp), saved lines 191–254, 284–293 and 335–340, and [RuntimeInit.java](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/core/java/com/android/internal/os/RuntimeInit.java), saved lines 354–369.

ART's option parser records explicit `-cp` as ClassPath. It uses inherited `CLASSPATH` only if ClassPath is missing. The wrapper therefore supplies exactly the bound probe DEX and one bound APK via `-cp`, with no application flag, inherited classpath fallback, extra Java archive or host boundary on the application classpath. A preliminary command proposal used only a Java property; the source assessment replaced that proposal with the parser's explicit ClassPath option before any execution. See [parsed_options.cc](https://android.googlesource.com/platform/art/+/refs/tags/android-15.0.0_r1/runtime/parsed_options.cc), saved lines 88–94 and 712–714.

The same parser maps `-Xverify:all` to enabled verification, not the none or soft-fail modes. AndroidRuntime can append `dalvik.vm.extra-opts` after command-line options; the wrapper requires that property to be empty before device mutation, before each guest process and after both processes. This keeps an inherited late option from replacing the verifier or classpath. The wrapper changes no system property. See parsed_options.cc lines 380–385 and AndroidRuntime.cpp lines 1011–1013.

## Exact final guest commands

For the newly created owned directory `R`, matching `/data/local/tmp/md-widget-method-[0-9a-f]{32}`, the original command is:

```text
/system/bin/timeout -s KILL 120 /system/bin/app_process64 -Xverify:all -cp R/widget-method-probe.dex:R/original.apk R recovered.probe.WidgetMethodProbe
```

The candidate command changes only `original.apk` to `candidate.apk`. They run in separate processes, so the manager singleton, continuation classes and static state are loaded independently. The parent directory argument is unused by app_main; using the same fresh owned directory keeps the full recorded invocation explicit. A host timeout bounds each guest command to 150 seconds, while the device timeout bounds the guest process to 120 seconds. Every argument and both output byte streams are retained.

Before and after execution, the wrapper measures app_process64 and the timeout executable hashes, along with all three pushed input hashes. The device image, ABI, native bridge, emulator/boot status and AVD are checked against the existing disposable Android 15 environment. A binary hash is an observed binding to that environment, not a claim that the binary was rebuilt from these reference sources.

## Saved source identities

| Saved file | Bytes | SHA-256 |
|---|---:|---|
| app_main.cpp | 11,658 | `50e38aed3d9debefc075c5644306eeea17c335a0b1d37c4166a3685772a2d1d3` |
| AndroidRuntime.cpp | 71,462 | `8afdfcaf65fe556219a5a4e05468ea7b8329961b9afc0ecbbc6e0deda3a88ade` |
| android_os_MessageQueue.cpp | 8,977 | `674cf31cc260d17a1d1ee302f1817dad7cd98211cac3d8608546d498da0ff092` |
| RuntimeInit.java | 22,755 | `c3379d7911685dc50d3082f09ca32a3b4aaec4b9431ae4b1c0c5c18ca468ee97` |
| Looper.java | 18,976 | `80d59764067ebaa35dc3113bbd06607f772101b05345e344a4792fd22291af2d` |
| MessageQueue.java | 43,701 | `d4cd24d94c8d64e788937c49ee2b86427bd38d004066d2a0abd4993df65af62d` |
| parsed_options.cc | 33,939 | `d2f297f90c0fb1efa36815995dcdce1337b3b28b32e672e8b0fc8104b3ba31c8` |
| dalvikvm.cc | 7,328 | `b685e53f81650df930723193f74e125747801216160fdd527eedb3bb1191a52f` |
