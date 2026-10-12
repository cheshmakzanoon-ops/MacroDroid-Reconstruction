# Current reconstruction progress

This working tree layers the current recovery code over the complete, checksum-pinned
v9 source and toolchain snapshot. The comparison target remains the supplied
MacroDroid 5.67.8 APK (`com.arlosoft.macrodroid`, version code `896700008`).

## Current source change

`source/java/recovered/ui/BlockTouchesMethods.java` now supplies the executable Java
body for `BlockTouchesAction.invokeAction(TriggerContextInfo)`. It preserves the
original trigger rejection, block/unblock/toggle selection, service call order,
configuration reads, Intent extras, and accessibility-only exception boundary.
The original Android services and framework remain dependencies.

The registry contains **1,238 recovered method bodies across 602 classes**. This is
one additional editable Java body; the action was already present in preserved smali.
Method counts are not a percentage of feature completeness. Most code still builds
from smali, and the reference Java tree is not a complete Android Studio project.

The new original-instruction versus JVM comparison passed **2,420 cases**, visiting
all **162 original instructions** and both outcomes of **15 conditional branches**.
The six-method UI suite has **11,353 cases**. Signed rebuilt-DEX comparisons,
deliberate-fault rejection, and whole-build acceptance are separate reports.
Host comparisons do not execute Android services.

## Reproduce from GitHub

From the repository root, run `python3 scripts/materialize_v9.py`. The script checks
every committed archive part, verifies the original source/toolchain archive hashes,
extracts the full baseline, and applies the tracked `project/` source overlay.
It refuses to overwrite an existing working directory.

Use Python 3.11+ and JDK 21, then from `workspace/MacroDroid_v9` run:

```sh
python3 release_integrity.py verify
python3 acceptance.py
```

The existing build entry points retain the filenames
`dist/MacroDroid-5.67.8-v9-baseline.apk` and
`dist/MacroDroid-5.67.8-v9-hybrid.apk`. Identify a candidate by its SHA-256 and
Git commit, not by that compatibility filename. The original APK is test-only and
is not required to compile either variant.

## Android runtime work

The recorder now records the native translation configuration and network settings,
and accepts bounded install/launch/UI command budgets for slow emulators. Extending
a timeout does not turn a failed command into a passed test. An explicit disposable
device and explicit package-data-removal flag are still required.

JDK 21 and a pinned Android 15/API 35 emulator image with ARM64 translation have been
installed in the current environment. Completed app execution is established only by
actual capture reports. Historical v9 reports in this tree describe the earlier
environment and earlier 1,237-method build; they are retained as historical evidence.

**Full functional 1:1 parity, a complete conventional Java/Kotlin app project, native
C/C++ source recovery, and the publisher's signing identity remain unestablished.**
