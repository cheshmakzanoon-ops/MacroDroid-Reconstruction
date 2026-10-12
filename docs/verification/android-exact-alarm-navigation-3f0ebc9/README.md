# Actual fourteen-screen exact-alarm navigation difference

The observation and independent comparison steps failed after both fourteen-screen journeys completed. The literal reports record 35 differing pixels on intro-2, zero on the other thirteen screen pairs, and equal hierarchies. Both variants reached the Settings-owned surface after the observed explanation OK; no Settings input or permission grant occurred. Known post-crash continuations remain in the reports. These are the original reported outcomes; independent replay is preserved separately. Setup, all host controls, APK checks, runtime installation and complete evidence upload passed.

Run [38240023189](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38240023189) used exact commit `3f0ebc910be72beeb9d7f2443928df2df2258c7d`. Artifact `11742624179` is 46,626,337 bytes, SHA-256 `c34d417c0b5d996e62d403023e9f9c9d122633c2ea65fb1cf45599643abdcf04`. All 3,507 original members (74,601,455 bytes) were compared byte-for-byte with [extracted/](extracted/) and are preserved unchanged.

## Reassemble the exact container

From the repository root:

```bash
python3 scripts/assemble_artifact.py docs/verification/android-exact-alarm-navigation-3f0ebc9/manifest.json --verify-only
python3 scripts/assemble_artifact.py docs/verification/android-exact-alarm-navigation-3f0ebc9/manifest.json
```

[manifest.json](manifest.json) binds every repository part. [extraction-receipt.json](extraction-receipt.json) and [archive-member-metadata.json](archive-member-metadata.json) retain all member identities and original ZIP mode metadata. The complete archive keeps the original ZIP bytes, timestamps and modes. The emulator log contains one ephemeral ADB public-key line. The raw value is retained only in the original evidence; it is omitted from summaries. The extraction scan found no private-key or token pattern. 

These files preserve an actual failed run. They do not establish full runtime parity or relabel a failed result as a success. No application source, APK or workflow is changed by this evidence publication.
