# Actual thirteen-screen readiness attempt

The observation and independent comparison steps failed. Setup, source checks, host controls, APK identity checks, runtime installation and evidence upload passed. Detailed raw-result replay is preserved separately when closed.

Run [38230072388](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38230072388) used exact commit `e1ade015f938339479216a1a91518e556902fce8`. Artifact `11739145683` is 44,543,663 bytes, SHA-256 `c8f0af87e5d91efe2dfc49b8ca76acc1a0943b2a2b8e17ffe279892726d2c80f`. All 3,258 original members (70,899,613 bytes) were compared byte-for-byte with [extracted/](extracted/) and are preserved unchanged.

## Reassemble the exact container

From the repository root:

```bash
python3 scripts/assemble_artifact.py docs/verification/android-day-time-readiness-e1ade015/manifest.json --verify-only
python3 scripts/assemble_artifact.py docs/verification/android-day-time-readiness-e1ade015/manifest.json
```

[manifest.json](manifest.json) binds every repository part. [extraction-receipt.json](extraction-receipt.json) and [archive-member-metadata.json](archive-member-metadata.json) retain all member identities and original ZIP mode metadata. The complete archive keeps the original ZIP bytes, timestamps and modes. The emulator log contains one ephemeral ADB public-key line. The raw value is retained only in the original evidence; it is omitted from summaries. The extraction scan found no private-key or token pattern. 

These files preserve an actual failed run. They do not establish full runtime parity or relabel a failed result as a success. No application source, APK or workflow is changed by this evidence publication.
