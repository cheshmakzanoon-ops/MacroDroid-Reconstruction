# Inactive plugin-upload signed build

The exact frozen source and isolated build recipe produced the signed APK preserved by `artifact/manifest.json`. Its bytes are bound to the original/JVM checkpoint02 and the immutable build-only `checkpoint.json` in this directory. The complete 14-file build evidence archive and unchanged review copies are retained under `evidence-archive/` and `evidence/`.

This freeze records build completion. Full original/JVM/rebuilt comparison, independent APK verification, all 54 fault controls and positive restoration were pending at freeze; later completion belongs to a separate checkpoint. No Android execution, active registry change or active APK promotion is asserted here. `SIGNED_BUILD_SCOPE.md` records the exact limits and integration boundaries.

The isolated build recipe is evidence. It must not overwrite the active parent's later generated-directory cleanup implementation. The current application remains bound to its separate active manifest.

From the repository root, verify or assemble the exact artifact:

```bash
python3 scripts/assemble_artifact.py work-in-progress/plugin-upload/03-signed-build/artifact/manifest.json --verify-only
python3 scripts/assemble_artifact.py work-in-progress/plugin-upload/03-signed-build/artifact/manifest.json
```
