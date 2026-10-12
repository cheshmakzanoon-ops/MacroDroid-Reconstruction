# Numeric ART wrapper: literal schema successor and source review

This inactive successor changes only the schema type checks in the reviewed numeric ART wrapper and adds one focused host control. The earlier wrapper accepted JSON `2.0` as schema version `2`. The concrete old behavior is retained, and the successor now requires the literal integer `2` in both provenance validation and report replay. No Android run, application build, application source edit, APK change or workflow activation occurred here.

The frozen starting source is `6ca4711b330c64f72c0df716e4a8c407360297a9bbc09e634bd88feb295a6dd6`. Its complete previously executed proof is `14bd536aa8af2e8458d8c3b1d45de6c770e55ce4e7f0f5e152a70bc6ed79e0bb`. Both remain unchanged. The neutral Java/DEX review is separately bound by `47a90e4ac7d13e50f4151f07417a8952907a269e382a1370a33406f105b69e67`.

## Exact source delta

`source-successor.patch` adds `type(info.get('schema_version')) is not int` to `validate_provenance` and `type(report.get('schema_version')) is not int` to `verify_result`. It adds no numeric conversion, parser, command, timeout, cleanup or claim-policy changes. Removing exactly those two AST expressions recovers the entire old wrapper AST, as recorded in `ast-derivation.json`.

| Source role | Prior SHA-256 | Successor SHA-256 |
| --- | --- | --- |
| `android_day_numeric_method_probe.py` | `cc8b400f419ae9dc47677bcc9c71257440d46c8278ab32dd5a759378a45e7c96` | `d406859fc2da0680cf1565c7c75740315c9fbd46cc68f933d12bd6e088356ea0` |
| `test_android_day_numeric_method_probe.py` | `4a7337cc580d0c9bafcbdfc3f8e9a421062902d5c99a2498c225ca6d0b009d42` | `6b10c91c23f12d5c99cf17c21ac1d74a3846375e65384e2f774aadf38e569b1e` |

All seven other source roles remain exact, including the 14,108-byte single-class DEX, its Java source, the 1,291-case corpus, provenance, the independent expected values and the exact CRLF AVD fixture. `source-bindings.json` records every before/after byte count, hash and mode. The original 41 named test bodies are unchanged; the final source contains 42 test names. The new name is `test_literal_integer_schema_is_required_for_provenance_and_result_replay`.

## Actual attempts and their limits

The old-policy counterexample in `reports/counterexample-01` loads the exact old wrapper and replays the already closed simulated positive read-only. It actually accepts `2.0` in both the provenance object and report object. Integer `2` passes, while string `"2"` and both Boolean values reject. The exact altered JSON objects, both gate observations, bounded command, raw streams and unchanged-input receipts are retained. Its successful reproduction is explicitly a **failed literal-integer contract**, not a new acceptance success. It does not invoke ADB or create another simulated probe run.

The successor's single focused test creates a new explicit simulated-ADB positive using the changed executed wrapper bytes. Both variants produce all 1,291 rows, all 60 lifecycle commands are recorded, and cleanup completes. The test then exercises the five schema values through both validation boundaries, retaining per-value observations. Only integer `2` passes. It restores and rechecks the unchanged positive object at the end.

| Evidence | Actual result | Executed source |
| --- | --- | --- |
| Earlier actual-input preflight | Exit 0; 2.493 seconds | Exact old wrapper; real pinned APK/DEX/corpus files read only |
| Earlier full host controls | 41 named tests pass; unittest 25.433 seconds, outer command 25.957 seconds | Exact old wrapper and its 41-test source |
| Old schema counterexample | Float `2.0` accepted at both boundaries; strict contract failure reproduced | Exact old wrapper and closed simulated evidence |
| Successor focused control | One test passes; unittest 0.898 seconds, outer command 8.179 seconds | Exact successor wrapper and new test |

The complete 42-test suite has not been rerun locally. The prior 41 successes and the new single success have distinct executed-source bindings. All 41 old test bodies are preserved, and a later hosted job can execute the complete final 42-test package. The five values in the focused control are subcases within one named test, not five additional test counts.

## Independent source and closed-evidence review

The source review read the full wrapper, the parent-to-numeric derivation, all inherited and added control bodies, the raw full-host log and its actual input validator. The independently executed `review_closed.py` does not import the wrapper, rerun its suite, compile code or use Android. It performed these checks:

- Rehashed all 20 source-draft payloads and all 26 full-proof payloads, then streamed all 7,629 archive members. Every archived file's name, size, mode and SHA-256 matched its declaration and corresponding closed raw file: 96,481,154 bytes in total.
- Reproduced both stored parent-to-numeric patches exactly. The 31 inherited test names are present among the old 41, the raw unittest log contains exactly those 41 named successes, and all 41 bodies are present unchanged in the successor's 42-name source.
- Recomputed all 1,291 expected results with independent rational/integer arithmetic. The frozen corpus contains 547 integer cases, 734 decimal cases, one null entry, one null value, four string cases, two Boolean cases, one dictionary and one nested entry. Every result matches the frozen independent expectation file.
- Independently expanded and checked the complete 60-command sequence, 120 raw stream bindings, fixed guest argv and all 1,291 output rows for each variant in three retained simulated positives: the old default success, the old differing-NPE-message success and the successor focused success. These are three existing host records, not three Android runs.
- Rehashed the actual APK inputs and all producer-declared input copies, checked the two original outer command receipts against their exact streams, and compared all reviewed input identities after the review. All 7,809 distinct reviewed file paths remained unchanged.

The closed review passed on its first execution, from 12:46:03.471547 to 12:46:49.599070 UTC on 2026-10-12. Its result is bound by SHA-256 `64fc9a9358a288eef42101290618a02b0e0b29a409a798715ca4f893fc37a084`. The source reviewer authored the subsequent two-guard correction under the parent's explicit scope; final parent review of that exact delta is still required before any workflow activation.

## Reviewed runtime contract

The wrapper requires the explicit disposable emulator serial, exact AVD name with the reviewed LF or CRLF response, boot completion, SDK/ABI/fingerprint and empty late runtime options. It hashes ADB, the guest executable and timeout binary, the original and candidate APKs, the DEX and local corpus. It copies the corpus, provenance, DEX and executed wrapper into the evidence directory. Device and local inputs are checked again after execution; a failed postcheck or cleanup preserves semantic observations and fails the overall result.

Each variant is invoked in its own process with exactly this structure, with no guest case selector or inventory argument:

```text
/system/bin/timeout -s KILL 120 /system/bin/app_process64 -Xverify:all -cp <owned>/day-numeric-method-probe.dex:<owned>/<variant>.apk <owned> recovered.probe.DayNumericMethodProbe
```

The guest timeout is exactly integer 120; the outer ADB execution bound is integer 150. The fixed classpath includes only the neutral probe and the one bound APK. All three device inputs are set and checked as mode 444. Cleanup is confined to the fresh UUID directory whose successful creation was recorded. Failure to create that directory does not authorize cleanup of it. The recorder retains separate raw stdout and stderr, partial timeout output and ordered command receipts. Those inherited lifecycle and cleanup bodies are unchanged by this successor.

The parser requires the exact LF-framed header, all 1,291 ordered case rows with the expected names/kinds/raw bits/results, and the exact terminal row. Missing, reordered, duplicated, noncanonical or extra rows reject. The one declared exception is the null-entry `java.lang.NullPointerException`. Its message may differ between runtimes; the exact `null` or lowercase UTF-16 code-unit representation and raw line bytes remain in the report. No other case receives an exception or message exemption. Semantic success is kept separate from nonempty diagnostic stderr, which still fails strict acceptance.

All Android execution, full runtime equality, macro configuration, scheduling, macro execution, UI and application modification claims remain false in the host evidence. This package establishes the bounded wrapper's reviewed behavior and the narrow schema correction. It does not establish actual numeric execution on ART or whole-application 1:1 parity.

## Contents

`source/` is the complete nine-role successor package. The patch, AST derivation, source identities and collector/authoring programs are retained directly. Selected closed results are readable under `reports/`; `evidence.tar.gz` and its inventory preserve every file from all owned counterexample, authoring, focused-control and review attempts. The earlier 96 MB raw proof remains separately bound to the immutable full-proof dependency, avoiding a second copy of that archive here. No earlier capsule or verdict is replaced.
