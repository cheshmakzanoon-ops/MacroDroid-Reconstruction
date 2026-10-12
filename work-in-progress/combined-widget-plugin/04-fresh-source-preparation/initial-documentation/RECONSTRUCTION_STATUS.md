# Current reconstruction progress

This source copy is the **private combined candidate: 1,242 registered Java method
bodies across 605 classes**, including ten UI-family methods. The full combined
acceptance run is pending. The currently published APK remains the separately
verified 1,240-method candidate until a coherent new source/APK promotion.

The comparison target is the supplied MacroDroid 5.67.8 APK, package
`com.arlosoft.macrodroid`, version code `896700008`. Most application code still
builds from preserved smali; native libraries and opaque assets remain binary
dependencies. Method counts do not measure the percentage of application parity.

## Evidence by exact scope

| Scope | Completed measurement | Remaining requirement |
| --- | --- | --- |
| Published 1,240-method source | Two hosted runs passed all 16 gates, 188,791 three-path cases, 259 Python tests, all 37 UI faults and clean restoration | Those reports retain their original source/APK identity |
| Isolated plugin upload | Signed build, full code/resources, 191,147 three-path cases and all 54 UI faults passed | Actual plugin/network behavior on Android |
| Isolated Widget | Five planned signed/host/integrity gates, 191,133 three-path cases and 265 Python tests passed; prior 24 compiled faults rejected | Separate actual Android method probe and Widget feature behavior |
| Combined source copy | All 81,245 baseline inputs independently copied and verified; fresh 1,242-method original fixture; exact source delta pinned | Full 16-gate combined acceptance and all 78 actual UI faults |
| Original constructor ART probe | Exact original allocation succeeded on the pinned API 35 emulator with verification enabled | This does not execute the Widget method |
| Editor journey | Actual original and candidate captures, installed hashes and lifecycle/crash records retained | Strict full comparison rejected PID changes and one observed intro-frame difference; updated bounded policy has its own device run |

The current source input pin covers 81,291 files:

`b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`

The combined build is expected to execute 193,489 cases across all 1,242 methods
and three paths, including 23,174 UI cases and 15,326 independent UI expectations.
All 78 deliberate UI faults, 273 Python tests, the signed source-edit experiment
and final positive run remain required. Expected counts are not reported as passes.

## Reproduction

The repository materializer verifies the committed multipart source/toolchain
archives and applies only the active `project/` overlay. Historical
`work-in-progress/` checkpoints are never applied automatically. From a fresh
materialized source tree with Python 3.11+ and JDK 21:

```sh
python3 release_integrity.py verify
python3 acceptance.py
```

`acceptance.py` records each subprocess, budget, exit code and evidence hash. UI
fault execution receives the measured 5,400-second suite budget and individual
300-second execution limits. All other gate budgets remain 1,200 seconds. A failed
gate stops acceptance and retains its evidence. The Android availability probe is
not an Android feature test.

## Limits and next measurements

Both observed APKs encountered the same supplied promotion-listener exception
after notification denial. The saved raw stack reports a Fragment not attached to
Activity in `com.zx.lbua80.onShow`. Matching stack evidence does not make this
crash-free behavior. The new opt-in journey policy preserves raw crash logs and
verifies an installed-identity/process boundary before subsequent observations.
It uses full consecutive byte-identical PNG and XML captures, without cropping,
masking, cross-APK frame selection or pixel tolerance.

The app uses the openly distributed development signing identity, not the
publisher's. Complete high-level Java/Kotlin and native source recovery, the
publisher's signing identity and full application runtime equivalence remain
unestablished. Real macro execution, permissions/services, persistence/reboot,
widgets, integrations, locales/devices/API versions and performance each require
their own observed evidence. See `COMBINED_RECOVERY.md`, `UI_RECOVERY.md` and the
immutable verification checkpoints for method and test details.
