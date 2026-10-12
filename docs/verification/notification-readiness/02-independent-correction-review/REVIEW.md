# Independent review of the corrected readiness guard

The corrected guard rejects both independently reproduced acceptance gaps. The full synthetic thirteen-screen comparison now rejects a whole readiness command block moved ahead of its denial input. The phase verifier now rejects the same two HOME observations whose raw command span is only 0.55 seconds even when their wrapper span is extended to 1.35 seconds. The positive synthetic comparison is still accepted and is restored exactly after the controls.

This checkpoint validates a private host-side evidence guard. It is not an Android run, a new application recovery, an app-parity pass, a full parent test-suite result, or a workflow activation. The older acceptance gaps remain preserved in the independent counterexample capsule; this result does not relabel them.

## Exact source and relationship to the first review

The corrected `notification_readiness.py` is **20,336 bytes**, SHA-256 `08a838681c6b3ece018240d54013996bafd4204133bdd3eaa6a6c2dddeea6f85`. The closed source snapshot includes that module, the two integration modules, and the then-current fixture/test source. The independent probe invokes the real validators and the fixture helpers; it does not execute the entire parent unittest module.

The former 18,934-byte module, SHA-256 `c61e2d2e3981939d024b70a7442e8b6b0e1e59f80418fa5fc5bffa18b0202f86`, remains unchanged in the earlier capsule whose checkpoint SHA-256 is `dcbb18a66a636718edc2bb680298e82db8464fb0d4905e6d2e73563ab039658a`. The parent accepted both counterexamples before correcting its source. No Android workflow ran that earlier guard.

The new independent probe is a recorded derivative of the exact old probe `73d210a6e5572e30f6c243e5426676dab24e4cea1b73b58219d5f6817a651021`. Its new source SHA-256 is `476704651ae52f2a663d9669e82c37d3f6d66898fd258c8d1b58f392adebdba9`. The complete derivation patch and source identities are retained. The derivative changes the source/output locations to the separate temporary filesystem, turns the original wrong-acceptance observations into required rejection checks, and adds independent primitive-format and timeout-boundary cases. It does not patch the validator functions or replace their raw-output parser.

The original and corrected stages derive from the frozen thirteen-screen DayTime source checkpoint `0e010cfbace03cffa6d45e8c9157402b1b68c9a392249eb2aeae39445dc57a7d`. The parent recorded an 83-file, 11,852,112-byte exact memory-stage copy before making the correction. All Python source dependencies actually bound by this independent probe remained unchanged for its entire execution. The parent later made a test-only placement correction after this probe closed; this capsule retains the exact earlier test source that the probe used. The production readiness module remained the same.

## Source review

The corrected `_sequence` uses the first ready `pidof` command's `started_monotonic` and the final ready `pidof` command's `finished_monotonic`. The fixed policy now names those two endpoints. A non-ready observation or a changed PID still resets the contiguous sequence. Acceptance still stops at the first eligible sequence, requires at least two ready observations and a 1.05-second raw-command span, and remains bounded by the same 16 observations and ten-second phase.

The complete global command ledger must now have finite start/finish values, a start no later than its own finish, and a start no earlier than the previous command's finish. Readiness commands still must be unique, internally ordered, and contiguous in that ledger. The denial-input command must occur exactly once and immediately precede the readiness block. Existing physical path/inode uniqueness checks still reject sharing a command output with another readiness command or another evidence role. The phase is bound to the exact denial boundary, its prior permission component/PID, its run label, the fixed post-input wait, and the resulting full-frame observation's PID.

The phase schema, observation indices, accepted-sequence indices, and gap indices now require literal integers where appropriate. The strict policy identity and exact schema-five report requirement remain. Older reports cannot carry the new evidence keys, and the new report cannot omit or misplace either run's readiness artifact.

The timeout correction is appropriately scoped. `Recorder.cmd` allocates its remaining timeout before recording the command's start timestamp. Therefore adding that timeout to the later start does not reconstruct the allocation deadline. The corrected verifier checks the observed command endpoints within the ten-second phase and requires a recorded timeout in `(0, 10]`; the live recorder continues to apply its absolute deadline. No process-gap tolerance was added to full-frame acquisition.

The existing notification input, two-second post-input wait, strict first-identical-full-frame capture, pixel/XML comparison, process continuity during capture, and separate post-capture crash/installed-APK handoff checks remain active. Readiness uses only `pidof` and `dumpsys activity activities`. It neither restarts the app nor adds a UI input. The schema-five result labels the readiness evidence as lifecycle observations and does not claim crash-free startup or uninterrupted PID identity across denial.

## Fresh independent results

The closed run took **15.860035061 seconds** and returned `CORRECTED_GUARD_INDEPENDENT_REVIEW_PASSED`. Its baseline and restored complete comparison results were exactly equal. All bound source hashes stayed unchanged.

| Targeted check | Observed result |
|---|---|
| Move the complete original readiness block from indices 22–34 to indices 0–12 | Full comparison rejects: `Global command ledger is not chronological and nonoverlapping` |
| Repeat the original compound boolean schema/index mutation | Full comparison rejects at phase validation |
| Extend only the wrapper around two short HOME observations | Phase rejects at the first-eligible-sequence guard |
| Boolean phase schema alone | Full comparison rejects at phase validation |
| Boolean accepted-sequence index alone | Full comparison rejects at the first-eligible-sequence guard |
| Boolean gap index alone | Full comparison rejects the fixed gap |
| Ten-second timeout allocated before a later recorded start, with actual endpoints inside a 1.65-second phase | Phase remains accepted |
| Actual command finish later than its phase | Phase rejects the actual endpoint bound |
| Delete the denial input's global-ledger entry, leaving all other records in chronological order | Full comparison rejects the unique immediate-predecessor requirement |

The span counterexample retained exactly the earlier numeric distinction: raw HOME command span `0.5499999999997272` seconds, wrapper span `1.3499999999994543` seconds, policy minimum `1.05` seconds. Its result remains explicitly phase-only; this review does not turn it into a claim about a complete forged report.

Each primitive-format case starts from the restored positive phase and report. This avoids a prior fault supplying the rejection for a later case. The controls require the intended rejection messages. The valid timeout-allocation case is a positive control for avoiding a spurious timing rejection; the separate late-endpoint fault demonstrates that an actual endpoint outside the phase is still rejected.

All 1,344 physical synthetic artifact payloads are retained with a per-member hash inventory. The complete synthetic positive report, each returned comparison result, the changed phase inputs, the exact restored result, the reviewed source snapshot, and before/after dependency hashes are included. The synthetic artifact archive is 72,364 bytes, SHA-256 `61547995b14261484c0238e6881aabc1e3b58ed2582c3e45a7981c21ddb00faf`.

## Remaining gates and storage scope

No blocking defect remains from these nine targeted checks or the independent source review. The parent still owns the complete parent-plus-new test corpus, literal replays of the retained Zero12 five-pixel failure and DayTime13 incomplete result, the frozen workflow proposal, and any authorized fresh Android run. Those outcomes are not inferred from this checkpoint.

All new output and test temporary files for this correction review used a narrowly owned `/dev/shm` directory because the overlay filesystem was full. The overlay stayed read-only. No source cache, original report, APK, or active repository path was removed or rewritten. The publisher is the sole remote writer and receives this frozen checkpoint for durable publication.
