# Plugin and runtime integration: closed host proof

This checkpoint activates the reviewed plugin lookup recovery, fresh-generation build staging, guarded constructor-owner support with zero active mappings, and post-intro Android capture/tooling. It preserves all prior measurements under their original source and APK identities.

The source pin covers 81,245 files, canonical SHA-256 `19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183`. The same value is machine-readable in `checkpoint.json` and the active `project/reports/release-input-snapshot.json`.

## Actual combined result

The clean private source copy passed all five commands between 03:04:59 and 03:17:13 UTC on 12 October 2026: hybrid assembly, whole hybrid code comparison, resources, all three-path host tests, and final input integrity. The fresh signed APK is 94,683,497 bytes, SHA-256 `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`, exactly matching the earlier isolated plugin candidate.

| Measurement | Result |
| --- | --- |
| Original instructions / recovered JVM / signed rebuilt DEX | 188,791 cases over all 1,240 registered bodies; zero mismatches and unsupported executions |
| UI scope | 18,476 cases over eight bodies, with 14,552 independent expected-result checks |
| New plugin body | 3,053 cases covering all 198 original instructions and all 34 conditional edges |
| Whole signed hybrid round trip | 71,267 classes, 349,972 methods, exactly 1,240 intended body changes; no unexpected changes |
| Resource comparison | 7,212 expected and actual files; 7,211 byte-identical, one equivalent enum-order difference; all 23,854 resource IDs preserved |
| Python tests in the actual clean host run | 259 passed |
| Integrated Android-tooling host tests | 27 passed; no Android executed by this host suite |
| Guarded constructor support | Zero active rules and zero corrections reported in build/static/linkage gates |

`complete-combined-reports.tar.gz` contains every closed report and command log, including the exact input snapshot. Its unchanged compressed bytes are committed as two bounded binary parts. Assemble or verify them from the repository root:

```sh
python3 scripts/assemble_artifact.py docs/verification/plugin-runtime-integration/complete-combined-reports-manifest.json
python3 scripts/assemble_artifact.py docs/verification/plugin-runtime-integration/complete-combined-reports-manifest.json --verify-only
```

The assembled file is placed under `workspace/artifacts/` by default. Its inventory pins every extracted member and the whole compressed file. `reports/` exposes the main results directly. `verification-recheck.json` records the independent checks of all five command-log hashes, ten declared fresh-report hashes, and the exact APK identity. `integration/` retains the source-copy hash inventory, merge receipts and parent host-check logs.

`complete-runtime-forward.tar.gz` preserves all authored runtime/tooling files, patches, baselines, synthetic controls, reviewed constructor provenance, the actual 27-test integration result and documentation verification. Its per-member inventory is separate. The active source/tooling paths are also individually listed in the checkpoint's file manifest with baseline hashes for conflict-safe publication.

## Scope

This is a five-command combined proof, not a completed 16-gate acceptance run or an Android result. The separate final plugin checkpoint previously passed all 37 UI deliberate-fault controls and clean restoration; those controls were not rerun by this five-command integration. The next hosted workflow runs the complete configured source acceptance plus device capture and the independent constructor probe. Cold launch and four intro stills already matched for the earlier `be1138a5…` candidate under its recorded environment. New post-intro and ART scopes remain pending here.

No full Widget body, plugin-upload body, real external API, coroutine scheduler, macro feature journey, animation-motion comparison, native source, or publisher signing identity is established by this checkpoint. Preserved smali and native payload still implement most of the application.
