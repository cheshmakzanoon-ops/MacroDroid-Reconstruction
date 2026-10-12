# Readiness guard counterexamples before correction

This capsule preserves a closed, independent synthetic review of the first notification-readiness implementation. It contains two observed acceptance gaps. It is not an Android run, an app parity pass, or an activation request.

## Exact reviewed implementation

The tested `notification_readiness.py` is 18,934 bytes, SHA-256 `c61e2d2e3981939d024b70a7442e8b6b0e1e59f80418fa5fc5bffa18b0202f86`. Its exact executed snapshot is included with `editor_journey.py`, `observed_journey.py`, and `test_notification_readiness.py`. The probe also binds every Python dependency in the private stage before/after; all those hashes stayed unchanged. The unchanged base is the already frozen thirteen-screen DayTime checkpoint `0e010cfbace03cffa6d45e8c9157402b1b68c9a392249eb2aeae39445dc57a7d`.

The independent probe is `probe_initial_guard.py`, SHA-256 `73d210a6e5572e30f6c243e5426676dab24e4cea1b73b58219d5f6817a651021`. It uses the real validator and the parent's synthetic thirteen-screen fixture; the validator functions are not patched. Its fake device command clock/data are explicitly synthetic. The closed run took 6.734147644 seconds. No Android, APK build/install, app code change, or active workflow change occurred.

## Confirmed whole-report ledger-order gap

The original positive synthetic thirteen-screen report passed. The probe then moved the complete original readiness command block from global indices 22 through 34 to indices 0 through 12. Each command's bytes, timestamps, raw stdout/stderr references, and the block's internal order stayed unchanged; only its position in the global ledger changed.

The complete comparison still returned `journey_equal: true` with no rejection reason. The old guard required its phase records to form a unique contiguous block and rejected timestamp overlaps, but did not bind the block's position to the denial input or require the whole ledger to follow chronological order. This was an actual wrong acceptance by the full synthetic comparison, not just an inferred source risk.

The exact positive report and the probe's deterministic index transformation are retained, along with the complete returned result. All 1,344 physical synthetic artifact payloads are retained in `synthetic-artifacts.tar.gz`, with a per-member byte/hash inventory. Those payloads are synthetic fixtures and receive no Android or application coverage credit.

## Confirmed phase-only span gap

A separate probe retained the absent-PID row and the first two HOME rows, then extended only the final row's wrapper finish time to the original phase finish. Its actual HOME command span was 0.5499999999997272 seconds. Its wrapper span was 1.3499999999994543 seconds. The policy requires at least 1.05 seconds.

`verify_phase` accepted that altered phase because the initial implementation measured the wrapper span. The complete altered phase is retained. This is deliberately a phase-only result: the probe did not claim that the shortened phase passed the complete report/global-ledger guard. The correction should measure from the first ready pidof command's start to the final ready pidof command's finish if the readiness claim is to be supported by the command observations themselves.

## Other observed result and exact restoration

A combined boolean schema/index mutation was rejected with `Notification readiness observations are out of order`. That demonstrates the row-index type guard for that compound input. It does not separately prove rejection of boolean phase schema, accepted-sequence indices, or gap indices; those require separate controls in the corrected source.

After the counterexamples, the positive report and original phase bytes were restored. The complete synthetic comparison result was exactly equal to the initial positive result. All bound source files remained unchanged. The original acceptance gaps remain recorded as such even after a future correction.

## Corrective contract handed to the integration owner

The parent accepted a targeted correction: finite, chronological, nonoverlapping global command records; the unique denial input immediately preceding the readiness block; readiness span based on raw first/last PID command times; and literal integer schema/index checks. The live recorder deadline and actual command endpoints within the ten-second phase remain required. A timeout allocation made before the recorded start must not be treated as though it were allocated at that start; the independent source review identified that timing distinction without claiming an actual Android failure from it.

This capsule does not contain or validate the corrected implementation. The original stage and this evidence stay unchanged. Future corrected-source validation will be a separate checkpoint.

## Preservation

The overlay filesystem reached zero free bytes only after this counterexample run had fully closed. Its complete 721,741-byte report tree was copied into a narrowly owned `/dev/shm` capsule and archived after before/after byte checks. No overlay source, report, or cache was changed during that freeze. All archive members and all synthetic fixture archive members were independently rehashed. The publisher is the only remote writer.
