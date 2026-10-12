# Successful source CI for the 1,239-body scene/runtime checkpoint

The source-build job for commit `95077fcb1d3c86f3b1c91026619642d99198f149`
completed successfully on 12 October 2026. All 16 configured acceptance gates
passed, including both builds, code/resource checks, deliberate-fault controls,
signed source editing and the final positive restoration. The fresh source build
produced the exact committed scene APK. This is a completed combined checkpoint
result, separate from the earlier isolated scene proof and the failed local runs.

## Identities and original evidence

- Workflow: [38194498356](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38194498356).
- Source job: `114634084877`, conclusion `success`, completed at 02:30:56 UTC.
- Artifact: `11723168069`, 127,144,217 bytes, SHA-256
  `7508365f22e56e14acdca1f7f8ae589cfe738fd37e68a463eb9dd6ecefdcbd85`.
- Frozen input set: 81,211 files, canonical SHA-256
  `8c8999f971f61def792cdf4ecd7999220c2fa2e56a5bdfecf3b04dee113bf7b0`
  before and after all acceptance gates.
- Fresh hybrid: 94,683,342 bytes, SHA-256
  `be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce`.
- Fresh baseline: 94,677,674 bytes, SHA-256
  `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096`.

[manifest.json](manifest.json) inventories every one of the artifact's 107 payload
files. All 105 report files are preserved here byte for byte; the two APK payloads
are already preserved exactly by the pinned current and baseline multipart
manifests at the source checkpoint. Their SHA-256 values were independently
checked from the downloaded artifact. The artifact digest matched GitHub's
reported digest. [job-metadata.json](job-metadata.json) preserves the public job
steps and artifact metadata.

The fresh acceptance run is
[acceptance-20261012T021913041490Z/result.json](reports/acceptance-20261012T021913041490Z/result.json),
started at 02:19:17.806093 UTC and finished at 02:30:51.400307 UTC. All 16 command
log hashes and all 19 pinned fresh report hashes match the actual artifact bytes.
The migration static/linkage reports are present in this artifact. Older
acceptance folders shipped with the baseline remain unchanged as historical
evidence; they are not the current run.

## Measured host result

[java-all-path-parity.json](reports/java-all-path-parity.json) reports 185,738
cases across original instructions, recovered JVM code and signed rebuilt DEX.
All 1,239 registered methods were covered, with zero mismatches and zero
unsupported executions. The suite partition is 95,262 legacy, 34,753 core,
30,684 environment, 9,616 engine and 15,423 UI cases. It binds the rebuilt DEX
comparison to the exact scene APK above.

[ui-negative-controls.json](reports/ui-negative-controls.json) records all 22 UI
deliberate-fault checks and successful 15,423-case positive restoration. Separate
engine, core, environment and legacy controls also passed. The signed source-edit
probe passed, followed by another complete positive three-path run; the source
input snapshot remained unchanged. The code and resource parity reports,
signature logs, the actual 203-test Python run (all passed in 6.072 seconds),
and exact command output are retained in
[reports/](reports/).

## Runtime scope

This source job did not have ADB available. Its optional Android probe correctly
recorded `BLOCKED`, `android_runtime_executed: false` and exit code 2; those reports
remain unchanged here. The separate Android workflow job has its own actual
cold-launch/four-page captures under [android-ci-95077fc](../android-ci-95077fc/).
The successful host gates do not establish complete high-level source recovery
or whole-application Android equivalence.
