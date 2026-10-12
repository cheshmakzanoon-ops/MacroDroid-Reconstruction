# Preserved-smali baseline control

This artifact is the generated development-signed baseline APK assembled from the preserved smali partitions. It is the control used to detect accidental source or packaging changes before applying recovered Java method bodies. It does not contain the Java replacements from the current hybrid candidate.

The exact output is 94,677,674 bytes with SHA-256 `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096`. Its 12 ordinary Git parts are individually pinned in `manifest.json`. The copied build, code round-trip, resource and signature reports identify this exact APK.

Reassemble it from a repository checkout:

```sh
python3 scripts/assemble_artifact.py artifacts/baseline/manifest.json
```

The assembler verifies every part and the complete output before publishing `workspace/artifacts/MacroDroid-5.67.8-v9-baseline.apk`. The original test-reference APK is not a build input. These reports establish the stated build and preservation checks; they do not establish complete Android runtime or feature parity.
