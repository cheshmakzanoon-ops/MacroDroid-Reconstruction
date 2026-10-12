# Complete immutable preparation evidence

The eleven declared source, package and documentation files and the original checkpoint are copied unchanged. All 6,051 declared evidence files are preserved in the exact archive described by `evidence-archive/manifest.json`; every member size and SHA-256 was independently verified. Compact review files are also available under `evidence/`, with their list in `publication-verification.json`.

The archive retains historical build, audit, race and packaging failures along with the successful preparation. The wrapper's 27 host controls used simulated ADB. No actual Android execution or active app/source promotion is claimed by this checkpoint.

```bash
python3 scripts/assemble_artifact.py work-in-progress/widget-art/01-wrapper-review/evidence-archive/manifest.json --verify-only
```

The exact b79 candidate APK is already preserved by `work-in-progress/widget-update/06-initial-signed-failure/apk/manifest.json` at commit `5024b1b46056de6a6e76a61883b469521a89ea44`.
