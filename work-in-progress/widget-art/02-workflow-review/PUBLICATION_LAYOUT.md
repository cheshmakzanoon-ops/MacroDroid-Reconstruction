# Independent Widget ART workflow publication

The five declared source, workflow, documentation and validation files and the original checkpoint are preserved unchanged. The new active workflow is `.github/workflows/widget-method-probe.yml`; all 22 frozen dependency/package hashes and the new-path absence guard were checked against the observed repository head before publication. Existing workflows and active app/APK inputs remain unchanged.

The exact evidence archive preserves all 3,202 members with individually verified sizes and SHA-256 hashes. Its 208 compact files are also copied under `evidence/`; the full simulated wrapper cases remain in the archive. The original host results include nine preflight fault rejections, four cleanup controls, six downloader tests and 27 packaged wrapper tests. They are offline measurements, with actual Android execution pending at this checkpoint.

```bash
python3 scripts/assemble_artifact.py work-in-progress/widget-art/02-workflow-review/evidence-archive/manifest.json --verify-only
```

The own-path workflow trigger requests a fresh independent Android run using the original APK, the unchanged b79 Widget APK and the already published ART01 probe package. Future measured results must be retained separately; this publication does not establish whole-app parity.
