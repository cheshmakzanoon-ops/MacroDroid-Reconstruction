# Complete isolated f83 host acceptance

The unchanged f83 input snapshot passed all 16 configured host acceptance gates in a private temporary checkout. The run finished at **2026-10-12 03:23:14.787813 UTC**. This follow-up preserves the complete final reports tree, the original per-gate logs and console output, the full input manifest, and an independent verification of their recorded hashes. The earlier failed workspace run remains separate evidence.

## Measured result and scope

| Check | Actual result |
|---|---|
| Configured acceptance sequence | All 16 gates returned exit code 0; all 16 recorded log hashes match the preserved bytes |
| Fresh evidence binding | All 19 recorded report hashes match the preserved bytes |
| Python controls | 209 individual `ok` outcomes; terminal summary `Ran 209 tests in 25.161s` and `OK` |
| Three-path bounded host comparison | 185,738 cases; all 1,239 expected methods covered; zero failed cases or unsupported executions |
| Input identity | All 81,212 current input files independently rehashed; exact manifest equality and snapshot `f83e1b06145a67238a722fe088c35525de359f1b20c72c06d7931c3dcc825d85` |
| Original f83 before/after binding | Identical input snapshots and `build_inputs_unchanged: true` |
| Baseline APK | 94,677,674 bytes; SHA-256 `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096` |
| Hybrid APK | 94,683,342 bytes; SHA-256 `be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce` |
| Android in this acceptance invocation | Not executed; its availability probe recorded `BLOCKED` because ADB was absent from that process's PATH |

The hybrid output is byte-identical to the separately archived 95077 candidate. That historical candidate has its own installed-identity and four-page still-capture evidence. This host run does not extend that Android scope, establish animation parity, or validate the later 1,240-method candidate. Its regenerated Java/source edit and negative-control gates are bounded host evidence. The report continues to set `full_runtime_1_to_1_established` and `complete_high_level_java_kotlin_source` to false. See the exact [acceptance result](reports/acceptance-latest.json), [independent verification](independent-verification.json), [Python log](reports/python-unit-tests.log), and [host comparison](reports/java-all-path-parity.json).

## Complete evidence and unchanged input binding

`reports/` contains every file present in the completed private checkout's reports tree: 219 files totaling 87,310,797 bytes. This includes all resource tables, individual negative-control failure evidence, compiler and test logs, Android availability results, the final acceptance run directory, and the 14,489,911-byte release input manifest. No report contents were sanitized, truncated, summarized in place, or rewritten. `reports-manifest.json` binds every relative path, byte count, and SHA-256. The independent scan found no private-key PEM blocks, GitHub access tokens, or signed download queries in these reports.

`input-binding/` preserves the exact acceptance runner, input-manifest implementation, test runner, and prior frozen staging checkpoint. The independent verifier did not execute those copied modules. It re-enumerated and hashed the configured input directories itself, compared every entry to the manifest, and checked all eight source entries from the prior checkpoint. The pinned input-manifest file SHA-256 is `5604f592394768e2ac8183cfd767f059a87cf0507d90237cb3a949df4b4f40b3`.

The source checkpoint was previously published at [ef1bcbd / 01-fresh-generations](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/blob/ef1bcbd5087b4959a0bc103b5400e51cd731a095/work-in-progress/staging-cleanup/01-fresh-generations/checkpoint.json). Its `FROZEN_LOCAL_ACCEPTANCE_IN_PROGRESS` status describes that earlier freeze; this immutable follow-up records the eventual completed private run. The [02-local-verification-failure checkpoint](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/56327dd3ddd04c78ebf461cdf810e209fd571f10/work-in-progress/staging-cleanup/02-local-verification-failure) remains a failed attempt and is not converted into a pass. The private run succeeded after moving the unchanged inputs outside the shared workspace. This observation does not establish the underlying filesystem synchronization mechanism.

The independently measured APK bytes remain in the private checkout's `dist/`; the source and dist directories are outside the report capsule. The byte-identical historical outputs and complete hosted source evidence are separately preserved in [source-ci-95077fc](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/3b2b7e8f539e746c9b99fbeb9a093bda1074fb92/docs/verification/source-ci-95077fc), and the separate still captures are in [android-ci-95077fc](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/0c5913324bcf60bacdb46554d80b3eda684dd79d/docs/verification/android-ci-95077fc).

`freeze_full_acceptance.py` is the exact authoring/verifying program. The companion ZIP preserves the entire checkpoint tree with fixed archive timestamps and permissions; the delivery receipt records its SHA-256 and a full extraction-byte check. `checkpoint.json` binds the frozen tree. Publication may retain the ZIP alongside expanded review files; extracting it reproduces every complete report.

## Cleanup boundary

No cleanup is performed by this freeze. Generated-cache removal is authorized only after the publishing agent confirms the complete evidence is durable. Any later cleanup must have a separate receipt, remove only closed generated build caches from the private f83 checkout, and preserve all source, reports, and dist files. A successful host acceptance does not erase the earlier failures or imply an Android runtime pass.
