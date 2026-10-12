# Fourteen-screen archive reference addendum

The frozen analysis names `artifact.zip` as the original logical container. Its exact bytes are committed as six parts through [the artifact manifest](../manifest.json). The complete 46,626,337-byte container has SHA-256 `c34d417c0b5d996e62d403023e9f9c9d122633c2ea65fb1cf45599643abdcf04`.

The six fetched Git blobs were independently rehashed and streamed in order at commit `d51f1b8d2b7972619bd69d6d8d1456a73e753e3e`; no assembled duplicate was written. To validate the committed parts from the repository root:

```bash
python3 scripts/assemble_artifact.py docs/verification/android-exact-alarm-navigation-3f0ebc9/manifest.json --verify-only
```

To produce the precise logical ZIP path used in the frozen external-evidence record:

```bash
python3 scripts/assemble_artifact.py docs/verification/android-exact-alarm-navigation-3f0ebc9/manifest.json --output docs/verification/android-exact-alarm-navigation-3f0ebc9/artifact.zip
```

The record also calls the extraction receipt `extracted-extraction.json`. Those identical receipt bytes are committed as [extraction-receipt.json](../extraction-receipt.json), with SHA-256 `4d0c142fa40cc52c909d59e2183392425e08cea3e04800d3e04b2afe897a2f28`. The raw member root remains [extracted/](../extracted/).

[reference-resolution.json](reference-resolution.json) binds both logical names to the published layout. The frozen `57a5a23f...` analysis and all raw members remain unchanged. This addendum supplies storage references only; it does not alter the measured fourteen-screen difference or add a runtime result.
