# Inactive plugin-upload original/JVM evidence

This archive retains all 68 closed report and log files from checkpoint 02, byte for byte. The checkpoint records 191,147 original/JVM comparisons across 1,241 methods, including 2,356 upload cases with all 163 instructions and 26 conditional edges visited. There were no mismatches or unsupported executions. The 161 Python tests passed. The 17 new mutant sources compiled; execution of all 54 behavioral controls, signed APK proof and Android execution remain pending.

The exact original archive is stored as one Git part, with its SHA-256 and member inventory in `manifest.json` and `extraction-receipt.json`. Sixty-seven compact reports are also visible in the adjacent checkpoint's `evidence/` directory. The 15,714,983-byte private input inventory is retained in the complete archive.

From the repository root, reconstruct and inspect it with:

```sh
python scripts/assemble_artifact.py work-in-progress/plugin-upload/02-original-jvm-evidence/manifest.json
tar -tzf workspace/artifacts/plugin-upload-original-jvm-evidence.tar.gz
```

Every archive member is beneath `evidence/`. Extracting into the adjacent checkpoint directory restores its complete frozen report set. Materialization of the active application only uses `project/`; this inactive checkpoint does not change its registry or candidate APK.
