# Hosted reproduction of the active combined candidate

Source job **114695960566** in [run 38214498395](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38214498395) completed successfully for commit `dbcad968c5c3e8f084205393a6c0d2d06a203c71`. It passed all 16 configured acceptance gates and reproduced the exact committed baseline and hybrid APKs. The workflow's separate Android job failed its intro comparison; the overall workflow therefore remains failed.

## What was independently checked

The [frozen independent review](independent-review/README.md) streamed all **1,136 original artifact members**, totaling **450,752,098 expanded bytes**, without extracting duplicate APKs or the large resource tables. It verified all 16 actual gate logs, all 22 fresh report hashes, all 78 retained mutant source/class identities and the exact complete positive restoration. The measured host totals are **193,489 original/JVM/rebuilt cases across 1,242 recovered methods**, with zero semantic mismatches or unsupported executions, and **273 Python tests**.

The complete 81,291-entry input manifest is byte-identical to the committed manifest, and its canonical digest recomputes to `b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`. The acceptance result reports that this input pin remained unchanged. The review binds those actual gate results and manifest bytes; it does not claim to have extracted and independently executed all source inputs again.

| Output | Bytes | SHA-256 |
| --- | ---: | --- |
| Baseline APK | 94,677,674 | `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096` |
| Combined hybrid APK | 94,683,119 | `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182` |

The current fresh run is `reports/acceptance-20261012T065140692696Z/`. Historical report members elsewhere in the ZIP retain their original identities and scope. The [complete member inventory](independent-review/all-1136-member-identities.json) and [independent review result](independent-review/independent-source-review.json) distinguish the actual fresh evidence from those historical files.

## Exact original archive

The original GitHub artifact is **188,134,390 bytes**, with SHA-256:

`da5668cb030718c72a557179b3d38e33769531d497ec5e16d0a45ea2c8f53d88`

[manifest.json](manifest.json) binds all 23 parts under `archive/`. The parts preserve the original ZIP byte for byte; neither the container nor its members were recompressed. Both APKs, every nested mutant source/class/report and every retained historical report are present in the archive. Compact actual reports, all gate logs, the reviewer source and the frozen provenance are also directly readable under [independent-review/](independent-review/).

From the repository root, verify every committed part and the complete ZIP identity:

```sh
python3 scripts/assemble_artifact.py docs/verification/source-ci-dbcad968/manifest.json --verify-only
```

To materialize an ordinary ZIP when needed:

```sh
python3 scripts/assemble_artifact.py docs/verification/source-ci-dbcad968/manifest.json --output /tmp/reconstruction-run-38214498395.zip
```

The [GitHub metadata](github-metadata.json) binds the source job and artifact. The [publication scripts](publication/) preserve the bounded range-transfer procedure and the exact review of repository documentation changes. The download is only eligible for retirement after fetched Git blobs reconstruct its complete original identity and the independent review has closed every reader; the committed parts remain the durable source.

## Runtime scope

This source job performed host, artifact and source-edit checks. It did not run the app on Android. The separately preserved [Android capture](../android-ci-dbcad968/) has an exact cold launch, a 35-pixel TRIGGERS difference and a successful bounded constructor ART probe. Its raw post-intro pair is exact, while that gate retains the failed intro prerequisite. The [scoped post-home session](../editor-journey/run-38214498414-attempt-1/analysis/) has ten exact full-frame/XML/component pairs and preserves the observed startup crashes and restarts. Neither result establishes whole-application 1:1 parity.
