# Fresh source-build acceptance on GitHub

The `source-build` job for [run 38191908311](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38191908311), source commit `bebf4482eac9d122c44511b52f28638ce4e61d94`, completed successfully. It built both APKs from the repository inputs, passed all 16 configured acceptance commands, and confirmed that the freshly built hybrid APK exactly matched the committed candidate.

The fresh result is [acceptance-20261012T013048705584Z/result.json](reports/acceptance-20261012T013048705584Z/result.json). It records 81,191 input files and the same canonical input digest before and after the full run: `db8959566d0d31e2f36f1d9be16c09b18b4b8e298abbd622cdfd423c6884bafb`. The acceptance commands ran from 01:30:48 to 01:44:49 UTC on 2026-10-12. Every command passed, including signed-source-edit rejection and the final positive restoration check.

## Verified scope

[The host summary](reports/java-all-path-parity.json) reports 181,668 cases across all 1,238 registered method bodies, using original instructions, JVM source and rebuilt APK bodies. It records zero failed cases and zero unsupported executions. Code round-trip checks, resource checks, negative controls, and the signed-source-edit probe are included in the fresh acceptance report and its pinned evidence hashes.

These are host and build results. The source job's Android availability probe was blocked and did not execute an Android app. Its report explicitly leaves complete high-level source recovery and full runtime parity false. The independent Android job in the same workflow failed during device preparation; that complete record is preserved in [android-ci-bebf448](../android-ci-bebf448/).

## Exact outputs and provenance

The downloaded Actions artifact had 105 files. All 103 report and log files are copied here without changes. The two APKs exactly match the existing multipart artifacts at the pinned source commit:

| APK | Bytes | SHA-256 | Pinned manifest |
| --- | ---: | --- | --- |
| Baseline | 94,677,674 | `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096` | [baseline manifest at bebf448](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/blob/bebf4482eac9d122c44511b52f28638ce4e61d94/artifacts/baseline/manifest.json) |
| Hybrid | 94,683,307 | `2eabb2d883598254ca71f99999297e1b98fa9ea56fb24c200d5f053456cff4d6` | [candidate manifest at bebf448](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/blob/bebf4482eac9d122c44511b52f28638ce4e61d94/artifacts/current/manifest.json) |

Use `scripts/assemble_artifact.py` with those manifests in a checkout of commit `bebf4482eac9d122c44511b52f28638ce4e61d94` to recreate the exact binary outputs. Later active candidates may have different bytes.

[manifest.json](manifest.json) records every original artifact member's size, hash and repository location, plus the verified download identity (127,142,227-byte ZIP; SHA-256 `d9aeb7faffb0ac3ed11338e0e1dccb338f46763fc0212cd59a06fe831997b96b`). The ZIP served as a transport container; its complete output file contents are preserved through the report copies and pinned APK commits.

The workflow upload omitted `migration-static-proof.json` and `migration-linkage-check.json`. Existing local copies matched the exact hashes pinned by the fresh CI acceptance result, and those byte-identical reports are preserved here with supplemental provenance. All 19 fresh evidence hashes have been checked.

The artifact also included inherited acceptance directories dated 2026-10-10 and 2026-10-11. They remain intact as historical records. The run dated `20261012T013048705584Z` is the fresh successful acceptance run described above.
