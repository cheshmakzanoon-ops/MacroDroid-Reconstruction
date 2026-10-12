# Actual numeric hosted policy-test failure

The bounded policy and subprocess controls failed after exact checkouts, Java setup and tool identity checks passed. Source materialization and the sixteen-gate build were skipped. The final verifier failed and complete failure evidence upload succeeded. No candidate APK or full source acceptance was produced by this run.

Run [38232050667](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38232050667) used exact commit `5c402b43ce7851a49072e8a36e93c3d88b615f75`. Artifact `11739380591` is 52,475 bytes, SHA-256 `b37c338cbfea7f6ce48e35c055e4b3ff1e501247526146a76dfdcf8a6141013e`. All 12 original members (191,877 bytes) were compared byte-for-byte with [extracted/](extracted/) and are preserved unchanged.

## Reassemble the exact container

From the repository root:

```bash
python3 scripts/assemble_artifact.py docs/verification/day-numeric-hosted-run-5c402b4/manifest.json --verify-only
python3 scripts/assemble_artifact.py docs/verification/day-numeric-hosted-run-5c402b4/manifest.json
```

[manifest.json](manifest.json) binds every repository part. [extraction-receipt.json](extraction-receipt.json) and [archive-member-metadata.json](archive-member-metadata.json) retain all member identities and original ZIP mode metadata. The complete archive keeps the original ZIP bytes, timestamps and modes. The extraction scan found no key or token pattern. 

These files preserve an actual failed run. They do not establish full runtime parity or relabel a failed result as a success. No application source, APK or workflow is changed by this evidence publication.
