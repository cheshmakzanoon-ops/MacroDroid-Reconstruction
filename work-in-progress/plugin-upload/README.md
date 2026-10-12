# Plugin-upload recovery checkpoints

These immutable snapshots preserve work on the plugin upload coroutine `k.invokeSuspend`. They are inactive; the build materializer only overlays `project/`.

- [01: draft compilation](01-draft-compile/checkpoint.json) preserves the first unregistered Java translation and its host compilation evidence.
- [02: original/JVM proof](02-original-jvm/checkpoint.json) preserves all 35 source, test, documentation and fixture paths, three narrow integration patches, and the complete [68-file evidence archive](02-original-jvm-evidence/README.md). The 191,147 two-path comparisons and full upload coverage passed. Signed APK comparisons, roundtrip, 54 behavioral controls and Android execution remain pending at that freeze.

The parent build, runtime and constructor changes are deliberately absent from these inactive merge patches. Any later activation requires a separately verified coherent source checkpoint.
