# Capture-device preparation failure

This directory preserves the complete, unmodified 71-file runtime artifact from
[GitHub Actions run 38191908311](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38191908311),
source checkpoint `bebf4482eac9d122c44511b52f28638ce4e61d94`. Its Android job
`114626343687` failed while preparing the disposable capture device, before either
MacroDroid APK was installed or launched.

**The recorded result is `CAPTURE_DEVICE_CONFIGURATION_FAILED`.** Android booted
successfully with KVM and the ARM64 native bridge; the readiness command completed
in 42.048 seconds. The configuration command then reached its 90-second signal
deadline and returned exit code 2 after 90.584 seconds. The service stopped with
exit code 0. These are the outcomes in [`runtime-run.json`](runtime-run.json).

## What the measurements show

All 18 current primary-signal observations reported Android's computed level 4.
The first observation used LTE. The remaining 17 observations used WCDMA, from
01:32:08 through 01:33:29 UTC. Within those WCDMA observations, `ss` changed from
-53 to -73 dBm while `ber`, `rscp`, `ecno`, and the computed `level` stayed the
same. The complete registry lines and the original output of every ADB command
remain in [`capture-device/`](capture-device/).

The helper at this checkpoint required the primary radio **and its entire raw
measurement string** to remain identical for 15 seconds. Each changing `ss`
reading restarted that timer, although the primary radio type and computed level
were stable. Thus the saved message, “Primary modem signal did not settle at
level 4 within the deadline,” described the failed gate too broadly: all measured
levels were already 4. The narrower cause is the raw-measurement equality rule.
[`signal-stability-analysis.json`](signal-stability-analysis.json) records the
varying fields and a replay of the old criterion using the saved timestamps.

Android's [`SignalStrength.getLevel()` implementation](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/telephony/java/android/telephony/SignalStrength.java)
returns the primary radio's computed level. A corrected preparation gate can
therefore require one primary radio type and computed level 4 throughout the
15-second observation window while continuing to record every raw measurement.
The replay of these historical samples supports that correction; it is not a new
device run and does not turn this recorded failure into a pass.

All 32 recorded ADB commands returned exit code 0. The genuine emulator console
accepted home voice registration, home data registration, and signal profile 4.
The helper stopped before its later registration confirmation and before any
SystemUI demo settings or clock broadcast were issued. The requested clock value
`1200` in the report records intent only. There are no app screenshots, UI
hierarchies, or app-comparison results in this artifact. Full runtime equivalence
remains unestablished.

## Artifact provenance

The original [GitHub artifact 11721842620](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38191908311/artifacts/11721842620)
contains 134,332 bytes and has SHA-256:

`9e608ab98ca6e1999f174c70fcae823718752007cb8ed565780c60b5231e3aa5`

The exact ZIP is preserved as one binary part. `manifest.json` pins that archive,
and `extraction-receipt.json` pins the byte identities of all 71 original extracted
files. The original runtime process had already omitted two emulator-log lines
containing transient ADB key material, as recorded in `runtime-run.json`; the
downloaded artifact is preserved without further changes.

To recreate the exact original ZIP from the repository root:

```sh
python3 scripts/assemble_artifact.py docs/verification/android-ci-bebf448/manifest.json
```

This README and the signal analysis are derived documentation, separate from the
71 original artifact files. The earlier failed complete-frame app comparison is
preserved in [`android-ci-ba52fd6`](../android-ci-ba52fd6/). Any corrected helper
must establish device preparation and app comparison in a subsequent actual run.
