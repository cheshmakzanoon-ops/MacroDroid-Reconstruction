# Complete closed acceptance publication

The original checkpoint and all 124 other listed files retain their exact bytes and modes. The original `complete-reports.tar.gz` is preserved without recompression as three ordered parts under `complete-reports/`; its 22,556,868-byte stream retains SHA-256 `a28998f55b333503050320465e1c977bcca11be7a81374169a810878476bca90`. Every one of its 551 original members was checked against `complete-reports-manifest.json`.

From the repository root, verify or reconstruct the exact report archive:

```sh
python3 scripts/assemble_artifact.py work-in-progress/combined-recovery/05-full-acceptance/complete-reports/manifest.json --verify-only
python3 scripts/assemble_artifact.py work-in-progress/combined-recovery/05-full-acceptance/complete-reports/manifest.json --output /path/to/complete-reports.tar.gz
```

The twelve APK parts and their literal `apk/manifest.json` paths remain unchanged. Their assembled stream is 94,683,119 bytes with SHA-256 `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`. Both manifests were verified without creating another assembled file. Compact exact gate logs and reports are already visible under `commands/` and `reviewable/`.

All 63 changed/new build inputs match the new 81,291-entry snapshot and the current 19ea baseline delta; no input was removed. This publication preserves the closed sixteen-gate host proof and its immutable candidate. Android execution and active source/APK promotion are separate steps, and whole-application 1:1 remains unestablished.
