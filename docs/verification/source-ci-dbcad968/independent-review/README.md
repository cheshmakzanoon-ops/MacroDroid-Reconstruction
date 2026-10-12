# Independent review of the dbcad source-build job

The exact hosted source artifact passes this closed evidence review. **All sixteen configured host gates passed, and the freshly built hybrid APK has the exact committed candidate identity.** This is a source-build and bounded host-verification result. The separate Android job at the same workflow run retains its intro pixel failure.

Source job `114695960566` belongs to [run 38214498395](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38214498395), commit `dbcad968c5c3e8f084205393a6c0d2d06a203c71`. Its acceptance starts at 06:51:46.140289 UTC and finishes at 07:13:55.222515 UTC on 2026-10-12. The latest result is byte-identical to its uniquely dated result file. The independent review checks all sixteen corresponding log SHA256 values and actual exit codes, plus all twenty-two fresh report bindings.

## Actual gate results

| Gate | Exit code | Seconds | Timeout budget | Evidence |
| --- | ---: | ---: | ---: | --- |
| input-integrity | 0 | 5.276 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/01-input-integrity.log) |
| baseline-build | 0 | 67.659 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/02-baseline-build.log) |
| hybrid-build | 0 | 45.733 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/03-hybrid-build.log) |
| baseline-code | 0 | 32.194 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/04-baseline-code.log) |
| hybrid-code | 0 | 31.538 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/05-hybrid-code.log) |
| baseline-resources | 0 | 7.840 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/06-baseline-resources.log) |
| hybrid-resources | 0 | 6.688 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/07-hybrid-resources.log) |
| positive-host-tests | 0 | 92.373 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/08-positive-host-tests.log) |
| reference-status | 0 | 0.264 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/09-reference-status.log) |
| engine-negative-controls | 0 | 11.672 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/10-engine-negative-controls.log) |
| ui-negative-controls | 0 | 725.704 | 5400 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/11-ui-negative-controls.log) |
| core-negative-controls | 0 | 13.750 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/12-core-negative-controls.log) |
| environment-negative-controls | 0 | 50.542 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/13-environment-negative-controls.log) |
| legacy-negative-control | 0 | 93.486 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/14-legacy-negative-control.log) |
| signed-source-edit | 0 | 48.308 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/15-signed-source-edit.log) |
| final-positive-host-tests | 0 | 91.023 | 1200 | [actual log](compact-evidence/reports/acceptance-20261012T065140692696Z/16-final-positive-host-tests.log) |

The larger UI control budget is confined to that one gate. Its actual completion took 725.704 seconds, below its 5,400-second limit. All other gate limits remain 1,200 seconds. The signed-source-edit experiment was actually run; it was not skipped.

## Source and APK identities

The complete input manifest has 81,291 entries and snapshot SHA256 `b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`. This review recomputed the canonical ordered-entry digest and compared the entire 14,502,990-byte manifest with the exact `project/reports/release-input-snapshot.json` Git blob at the tested commit. The bytes match. The host result reports that the before/after build inputs are unchanged. This review does not claim an additional remote source-filesystem rehash; it checks the complete preserved inventory and its immutable source binding.

The archive's APK members were read and SHA256-hashed as streams, without extracting another APK copy:

| APK | Bytes | SHA256 |
| --- | ---: | --- |
| Fresh baseline | 94,677,674 | `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096` |
| Fresh hybrid | 94,683,119 | `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182` |

Both identities match the acceptance result and their actual build reports. The hybrid also matches the exact committed candidate manifest. The hosted candidate-versus-fresh-build comparison step succeeded independently of this replay.

## Host semantics and retained controls

The recorded three-path result contains 193,489 cases, 1,242 covered/expected methods, zero failed cases and zero unsupported executions. Its suites contain 95,262 legacy, 34,753 core, 30,684 environment, 9,616 engine and 23,174 UI cases. The result verifies the exact method-key partition and binds the rebuilt DEX comparison to the same hybrid APK and fixture identity.

All 78 UI mutation controls report the required rejection with zero unsupported executions. This review checks the SHA256 of every retained mutant Java source and compiled class against its individual report, confirms that each mutant class differs from its positive class, and checks the source/fixture/APK preservation fields. The complete restored UI result object equals the complete positive baseline object, including its cases and coverage, with all 23,174 UI cases passing. The [78 individual checks](all-78-retained-mutant-checks.json) and [original control report](compact-evidence/reports/ui-negative-controls.json) retain those bindings.

The actual Python regression log contains 273 individual successes and a matching `Ran 273 tests in 6.611s` summary. The exact Git-bound `test.py` invokes that suite as part of the positive host commands. The copied acceptance runner, test runner, release-integrity code and workflow explain the actual orchestration. The Java staging receipt is retained with the compact proof; no new compiler invocation or broader test suite was performed by this review.

## Complete archive preservation and scope

The original source artifact is 188,134,390 bytes, SHA256 `da5668cb030718c72a557179b3d38e33769531d497ec5e16d0a45ea2c8f53d88`, artifact ID `11731218792`. All 1,136 archive members, totaling 450,752,098 uncompressed bytes, were independently streamed and checked, with CRC and SHA256 metadata in the [complete inventory](all-1136-member-identities.json). The archive also retains historical reports; this review selects the actual dated acceptance result and its fresh bindings rather than mistaking older evidence for the current run.

Only compact current reports and gate logs were copied into this review. The two APK members, large resource tables and full duplicate report tree were not expanded. The immutable original container is preserved by the repository publisher under the parent evidence directory. After successful verification, this reviewer closed all ZIP readers and required no further source-archive reads, allowing the separately authorized disk-aware publication and retirement procedure.

The source job's availability probe reports `BLOCKED` and `android_runtime_executed=false`; that probe is not an Android acceptance test. The parallel Android job has its own actual evidence and failure. No full runtime 1:1, complete high-level Java/Kotlin source, animation parity or general feature parity is inferred from these host results.

The [independent result](independent-source-review.json), [actual review log](review.stdout.log), exact [source pins](source-commit-pins.json), [twenty-two fresh-report checks](all-22-fresh-evidence-checks.json), reviewer and freezer preserve this closed review. The raw ZIP and application inputs were not modified.
