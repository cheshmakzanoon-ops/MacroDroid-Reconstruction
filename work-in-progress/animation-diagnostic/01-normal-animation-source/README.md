# Independent normal-animation diagnostic

The original APK has produced more than one stable intro-dot rendering across recorded runs. A separate diagnostic will set and verify all three Android animation scales to `1` before repeating the existing ten-screen journey with unchanged PNG, XML, process, input and APK checks. This package does not modify the active APK or the existing scale-zero workflow, and does not turn any prior mismatch into a pass.

The setting preparer pins the disposable emulator identity before its three writes, preserves all 19 raw command results, checks every readback and rechecks emulator identity afterward. Nine host tests passed using simulated ADB, including malformed identity, diagnostics, stale or reordered commands, changed file hashes, aliases and incorrect readbacks. These host tests do not execute Android.

The evidence archive retains every regular host-control file. One deliberate symlink fault is represented by its exact inert link metadata in `host-evidence-manifest.json`, so the archive itself installs no symlink. The manifest records the target bytes too.
