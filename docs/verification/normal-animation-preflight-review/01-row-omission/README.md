# Mutable preflight inventory omission review

This inactive evidence checkpoint proves two source-provenance false acceptances in the unchanged normal-animation workflow-02 materialized-input gate. It changes no active source, app, APK, runtime configuration or workflow. The code under `inputs/` is the exact reviewed source, not a proposed correction. Root owns the correction in a later workflow checkpoint.

The gate accepts `input-preflight.json` with `passed: true`, then rechecks only the source/copy rows present in its mutable `files` array. It does not independently require the expected complete inventory. The exact successful preflight has 182 rows.

Four bounded controls use the real fixed original and current APKs plus the preserved AAPT2, in private hard-link fixtures. Every deliberately altered file is unlinked before replacement; no shared source inode is edited. The only source change is a private comment appended to both copies of `tools/android/bootstrap_android_runtime.py`. No downloader or Android command is executed by this review.

| Case | Inventory rows | Source changed privately | Process exit | Materialized result |
| --- | ---: | --- | ---: | --- |
| Positive | 182 | No | 0 | Passed |
| Changed source with its row retained | 182 | Yes | 1 | Rejected as a changed prepared input |
| Same changed source, its one row omitted | 181 | Yes | 0 | Incorrectly passed |
| Same changed source, all rows omitted | 0 | Yes | 0 | Incorrectly passed |

Both false acceptances return `EXACT_APKS_AND_AAPT2_VERIFIED_OFFLINE` with `passed: true`. The real APK/AAPT2 validation still runs; it does not compensate for the missing prepared-source binding. The exact before/after preflight documents, mutated source bytes, command arguments, outputs, materialized result and fixture-source references are retained for every case. All 305 distinct original source, tool, APK and evidence file hashes match afterward, as do all three original workflow-02 source/workflow hashes.

The same unchecked iteration over `preflight['files']` appears in the final `verify_normal_journey.verify` function before it imports copied comparator and animation code. This source review identifies the same omitted-row risk there. This checkpoint executes and proves the **materialized gate** false acceptance only; it does not claim a complete synthetic or real final normal-animation verification pass. No new Android runtime test occurred.

The smallest correction is to reconstruct the expected path/copy/size/SHA-256 inventory from the independently pinned source map and both frozen package manifests, including every reviewed-source and historical fixture copy. Require the exact complete inventory at both materialized and final checks before importing or executing copied code. Missing, extra, repeated, or rebound rows should reject. Preserve the actual old failed checks and historical device results.

`reproduce_preflight_omission.py` is the exact executed helper. It uses the already validated workflow-02 input tree, records all original source references and hashes, and creates private fixtures without modifying their source inodes. The private APK hard links are not duplicated in this publication; their exact existing identities and locations are bound by the fixture manifests and before/after controls. The workflow-02 validation package and the already published APK artifacts provide those reproducible inputs. `review-result.json` is a complete compact result; individual cases preserve their full reports and logs.

`checkpoint.json` declares no active files. This review is separate from the previously found capture hard-link alias issue and from the session chronology overlay. It establishes neither normal-animation parity nor whole-app parity.
