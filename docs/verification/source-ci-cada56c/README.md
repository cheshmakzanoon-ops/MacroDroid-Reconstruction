# Hosted source verification: cada56c

The source-build job in [run 38202401393](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38202401393) completed successfully at 04:21:56 UTC on 2026-10-12 for commit `cada56c8a11ff5cbd892ec6d0beaeab60b3e644d`.

All 16 configured host acceptance gates passed. Independent artifact review verified all 16 gate-log hashes and all 19 fresh evidence hashes. The fresh reports contain 188,791 original/JVM/rebuilt cases across exactly 1,240 methods, with zero mismatches or unsupported executions, all 259 Python tests passed in 6.340 seconds, and all 37 UI fault controls rejected their required case before an 18,476-case clean restoration. Static and linkage reports record zero constructor-owner corrections for this active source.

The before/after source-input pin is unchanged: `19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183`, covering 81,245 files. CI performed the input verification. The publisher separately verified the exact committed manifest bytes and 81,245 entries; it did not independently rehash every materialized source input during artifact review.

The rebuilt hybrid APK is 94,683,497 bytes, SHA-256 `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`. The baseline is 94,677,674 bytes, SHA-256 `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096`. Both exact byte sequences are already durably represented by their multipart manifests at commit `3a2e6ea9ef9e18d38d5921bb18c77e1c2eb13677`.

## Complete artifact contents

The 127,146,419-byte GitHub source artifact has SHA-256 `6e4290fb8e54265cb441db0317a771ea9320be0b720d241b36ac6a7dc94f575f`. All 108 payloads were read and hash-verified. All 106 exact report/log files are included here; the two APK payloads map to their immutable existing manifests in [manifest.json](manifest.json). Earlier retained report directories remain historical files, and the fresh run is `reports/acceptance-20261012T040751585250Z/`.

[Independent verification](independent-verification.json) records the individual checks and preservation mappings. [The executed verifier](verify_source_38202401393.py), original GitHub job and artifact metadata are included for review. The fresh gate report is [acceptance-latest.json](reports/acceptance-latest.json).

This source job did not execute Android; its ADB capability probe reported BLOCKED. The separate Android job failed its strict intro-dependent capture gate despite exact cold launch and a successful standalone ART allocation probe. Its actual results are preserved in [android-ci-cada56c](../android-ci-cada56c/README.md). These source checks do not establish complete high-level Java/Kotlin recovery or whole-app runtime parity.
