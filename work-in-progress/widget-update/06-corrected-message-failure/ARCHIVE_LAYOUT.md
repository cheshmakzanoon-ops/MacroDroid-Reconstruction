# Exact archive publication layout

The original `checkpoint.json` is unchanged. Its declared `complete-reports.tar.gz` is preserved as two binary parts under `complete-reports/` because the exact 16,111,788-byte archive exceeds the connector's encoded single-request limit. Every other declared checkpoint file is copied unchanged.

The parts reconstruct SHA-256 `0da10cc39ea2cc9c6a26bc2719b6ccc5a2dd71615b1aee9b6b12bbee374849f4`. All 68 archive members were independently checked against `complete-reports-inventory.json`. The one UI message mismatch remains a failed result, with zero unsupported executions; this publication makes no active source, APK or Android change.

Verify the complete archive without creating another copy:

```bash
python3 scripts/assemble_artifact.py work-in-progress/widget-update/06-corrected-message-failure/complete-reports/manifest.json --verify-only
```

To materialize the exact path declared by the frozen checkpoint:

```bash
python3 scripts/assemble_artifact.py work-in-progress/widget-update/06-corrected-message-failure/complete-reports/manifest.json --output work-in-progress/widget-update/06-corrected-message-failure/complete-reports.tar.gz
```

The unchanged b79 APK is already preserved by `../06-initial-signed-failure/apk/manifest.json` at commit `5024b1b46056de6a6e76a61883b469521a89ea44`.
