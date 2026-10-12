# Independent review of the corrected numeric hosted run

The complete saved evidence from [run 38238858564](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38238858564), job `114776169911`, passed this bounded independent review. The run used tooling commit `3d91187924af10457366ede7a1a8f10d3a1a6ac4` and the immutable source successor at `811f979eda1b937917c18defef38455c49a59062`. Its sixteen host gates and final independent hosted verifier passed. This review closed at **2026-10-12 11:30:04 UTC**; see the exact [review result](attempt-02/result.json), [execution receipt](attempt-02/run-execution.json), and [saved final hosted verifier](attempt-02/review-copies/hosted-proof/verification.json).

## Container and executed inputs

The publisher downloaded the artifact once. The unchanged 222,144,520-byte ZIP has SHA-256 `a7b52e6096db27cf9854671fcd3f6d1b7c3f73f5cf0255fcb9fc6fdc5afc117c`; its complete container is bound by the parent [manifest](../manifest.json). The reviewer streamed all **3,308 unique members**, totaling 568,138,240 uncompressed bytes, through SHA-256 and ZIP CRC validation. The complete [member inventory](attempt-02/complete-archive-members.json) retains every original name, size, hash, and compressed size. Neither APK nor the full report tree was extracted.

The [input binding](attempt-02/complete-source-binding.json) checks all nine executed tooling/workflow files and all nineteen proposed source files against the frozen reviewed packages. It independently derives the entire 81,298-entry future manifest from the unchanged baseline plus the exact nineteen replacements. The resulting snapshot is `f8fc1cadac8213468e42ac99a2cd5d807827dcdeee25166b8025620ff39a6545`, matching the manifest actually recorded by the host run. All 3,372 source/tooling checkpoint payloads were rehashed after this read-only review and remain exact; the [post-review check](frozen-inputs-after-review.json) preserves those results.

## Actual host result

| Evidence | Verified result |
| --- | --- |
| Required acceptance commands | 16, in the exact expected order, with exit zero and retained log hashes |
| Fresh report inventory | All 23 exact required reports |
| Final produced report/APK inventory | All 720 declared paths and original serialized metadata rows |
| Original / Java / rebuilt-DEX cases | 194,780 |
| Credited recovered bodies / target classes | 1,243 / 605 |
| Selected original fixture declarations | 1,246 methods / 607 classes |
| Separately reported original getter dependencies | 3, with zero recovered-method credit |
| Project Python tests | 308 individual successes, 9.567 seconds |
| Hosted tooling controls | 92 individual successes, 2.317 seconds |
| Retained positive runtime classes | 31; the numeric harness binds 23 of them |
| Compiled Java controls | 91 |
| Additional actual numeric DEX faults | Integer-zero: 509 mismatches; decimal-zero: 406 mismatches |

The [sixteen gate rows and twenty-three report hashes](attempt-02/sixteen-gates-and-fresh-reports.json) are preserved exactly. The five suite totals are legacy 95,262; core 34,753; environment 30,684; engine 9,616; and UI 24,465. The numeric method contributes **1,291 bit-precise cases across three execution paths**, all 32 selected original instructions and 25 rebuilt instructions, and four conditional edges on each measured path. The review replays the unchanged pure validators against the actual positive, restoration, and fault reports; it does not launch a new test suite or compiler.

The selected original DEX was read directly. Its encoded declarations are exactly the registered 1,243 bodies plus three disjoint original getter dependencies, all with code. The [declaration inventory](attempt-02/actual-fixture-declarations.json) and the copied original fixture retain this check separately from report-count assertions.

The actual helper-class, D8, and transplanted-method identities equal the reviewed positive pipeline pins. The signed-APK and positive-transplant instruction reports are byte-identical. The review also streamed `classes3.dex` directly from the nested signed APK and verified its getter-partition hash against the actual harness input. All positive/restoration report bytes match; both provenance controls reject before producing a result report.

| Signed artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Baseline | 94,677,674 | `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096` |
| Numeric WIP hybrid | 94,683,136 | `0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd` |

Both hashes were independently read from the exact archive members, then checked against the acceptance and final-verification reports. Promotion is a separate action; the recorded run and this review both retain `active_promoted=false`.

## Filesystem-clock evidence

All **17 numeric child commands and three outer wrapper commands** passed the unchanged exact argv, role, monotonic chronology, exclusive-creation, inode/link, hash, and filesystem-witness predicates using the original saved records. Every one of the 20 commands achieved its first valid after-witness bracket on its first attempt. The [per-command replay](attempt-02/actual-command-clock-and-stream-replay.json) preserves all measured values and the exact production verifier and pure-validator identities.

Among their 40 output streams, 31 were empty. **34 initial filesystem ctimes preceded the finer recorded command-start time**, with deltas ranging from -438,283 to +101,673 nanoseconds overall. This is the concrete hosted evidence that the approved same-directory witness contract handles the measured filesystem-clock granularity without an arbitrary timestamp allowance. The [compact clock summary](actual-host-clock-summary.json) is derived from the retained per-command records.

The host verifier originally checked live file metadata. This later ZIP review checks the saved bytes and the original serialized metadata through those predicates. It does **not** claim that an extracted file's ctime or inode reproduces the original host value. No extracted metadata was substituted for the historical records.

## Preserved independent-reader failure

The initial analyzer reached its new direct-DEX declaration check, then failed when it attempted to decode an unrelated DEX modified-UTF-8 string with Python's plain UTF-8 decoder. Its [original source](analyze.py), [literal stderr](run-01.stderr), [result](result.json), and all completed review outputs remain unchanged.

The separate [second source](attempt-02/analyze.py) decodes only the exact ASCII descriptor and method-name roles needed by this bounded check, with their declared UTF-16 lengths verified. All unrelated string literals remain raw hash-bound DEX bytes. It uses no lossy replacement or ignored decoding errors. The [narrow correction](attempt-02/reader-correction.patch) and [source binding](attempt-02/reader-correction.json) preserve this distinction. The corrected complete review passed in 13.34 seconds.

## Scope

The hosted run records Android validation as `BLOCKED`; no Android execution occurred in this source-only job or this independent review. This capsule establishes the closed host build, the exact signed WIP output, and the retained evidence relationships. It provides no additional full-runtime, complete high-level source, visual, lifecycle, or 1:1 parity claim. The separately measured indicator and journey failures remain unchanged.
