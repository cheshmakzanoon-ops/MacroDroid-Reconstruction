# Final isolated plugin signed proof

This directory preserves the complete 191-file evidence archive from the final
plugin lookup recovery checkpoint, plus ten compact original reports for direct
review. The archive is the exact frozen file supplied by the recovery worker;
its SHA-256 is
`69991a63f058fbec2d86a212a7e9db22a3a07253584e4ec27adb6d9da9aef4de`.
All archive entry sizes and SHA-256 values were checked against both the frozen
checkpoint inventory and the original files.

[plugin-lookup-recovery.json](plugin-lookup-recovery.json) records 188,791 passing
original/JVM/signed-rebuilt cases with zero mismatches or unsupported executions.
The plugin body covers all 198 original instructions and 34 conditional edges.
All 37 deliberate-fault controls passed, including 15 plugin-specific controls;
the final clean 18,476-case UI restoration passed. The independent DEX roundtrip
and 161 Python tests also passed.

These are isolated, bounded host and structural artifact results. They do not
execute Android plugin/network/scheduler behavior or establish full application
parity. The 1,240-body / 603-class registry is inactive until a separately
reviewed, pinned integration is published. The current source checkpoint and
its completed hosted acceptance remain distinct.

Assemble the archive from the repository root:

```bash
python scripts/assemble_artifact.py work-in-progress/plugin-lookup/04-signed-proof-evidence/manifest.json
```

The output is `workspace/artifacts/plugin-lookup-signed-proof-evidence.tar.gz`.
Archive entries begin with `reports/`. The original frozen checkpoint stores the
same files under `evidence/`; [extraction-receipt.json](extraction-receipt.json)
records the explicit path mapping and all 191 exact hashes.

The final proof uses the same immutable APK already committed with checkpoint 03:
[artifact reference](../04-signed-proof/artifact-reference.json). The first staging
failure, successful retry, negative-control outputs and final restoration are all
retained in the archive without altering their original outcomes.
