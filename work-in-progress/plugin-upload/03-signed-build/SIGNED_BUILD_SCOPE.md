# Plugin upload: inactive signed build checkpoint

The frozen 1,241-body plugin-upload source produced a signed hybrid APK successfully. The build command exited 0, and all 35 source/test/doc/fixture paths from checkpoint02 remained byte-identical. Exact command, timing, build recipe hash, signing log, partition-assembly logs and APK identity are preserved here.

This checkpoint preserves **build completion only**. The full original/JVM/rebuilt run, hybrid roundtrip verification, all 54 deliberate-fault UI controls and final positive restoration were still running when this checkpoint was frozen. Their completion must come from a later measured checkpoint. No Android runtime was executed and no active registry or APK was promoted.

The source files are unchanged from the original/JVM checkpoint02, including its 2,356 upload cases and full 163/163-instruction, 26/26-edge host coverage. Those earlier host results are separately durable; building an APK does not extend them to rebuilt execution.

`isolated-build-recipe/build.py` records the exact private recipe used for this artifact. It is evidence and must not overwrite the parent's newer strict generated-directory cleanup implementation during integration. Likewise the source `ui_negative_control.py` is the inactive upload version; integration must apply only its 17 new controls while retaining parent cleanup changes. The APK contains no compile-only host boundary classes.

The attached study tools run the frozen build and subsequent proof stages in the private candidate. The later proof runner source is included for reproducibility; its eventual result is not asserted by this build-only checkpoint.
