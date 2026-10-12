# Proposed bounded indicator timing experiment

**Proposal only.** Root must review the implemented actions and evidence contract before a workflow is activated. No Android command in this document has been executed by this study.

## Question

Does the persistent indicator difference depend on the indicator's ValueAnimator finishing before the unchanged ViewPager Scroller, leaving a last sampled joining fraction behind?

The exact-source dossier establishes that this retained state is possible. It does not establish that the historical capture had that state. This experiment tests a timing dependency using ordinary app input and explicit environment settings; it will not directly read the private fraction.

The retained all-scales-one run `38212813248` failed full-frame settling on intro2's continuous Lottie clock. It used the earlier `9108b581…` candidate, and is not a scale-one execution of combined candidate `5f635e…`. Accordingly, this proposal is a separate **fixed-sample diagnostic**, and does not require or claim full-frame settling. Continuous animation remains visible in the retained complete frames and in every full-frame difference result. Indicator-local observations cannot substitute for full-frame equality.

## Fixed inputs

- Original APK: SHA-256 `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`, 95,725,918 bytes.
- Candidate APK: SHA-256 `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`, 94,683,119 bytes.
- Existing checksum-pinned disposable API35 AVD/toolchain, exact serial and boot/device checks, display 720 × 1280 and density 320.
- Existing observed first two intro screens and exact next-button selector, taken from the frozen accepted prefix. Input consists of the same single next-button tap for each fresh process.
- Existing fixed package-data-removal/install/launch contract. Each run starts from fresh app data and records fresh PID and exact installed APK checksum.
- Radio, demo mode, font scale, locale, timezone, system bars, permissions, and supplied app data remain the same across every original/candidate pair.

The implementation should consume immutable artifact manifests and a frozen two-screen plan. It must not materialize or select an unbound current APK.

## Two explicit conditions

| Condition | animator_duration_scale | window_animation_scale | transition_animation_scale |
| --- | --- | --- | --- |
| A | `0` | `0` | `0` |
| B | `1` | `0` | `0` |

Settings are written before a fresh app process is launched, then read back before input, after capture, and at job completion. The exact ordinary shell commands and raw output are retained. Both APKs receive identical settings within a condition.

The source predicts a 200 ms Scroller for the assumed one-page, zero-velocity, zero-margin move. At scale one, the indicator's explicit delay and retreat duration should ordinarily place its reset after that scroll. No runtime result may silently substitute this prediction for an actual observation.

## Fixed execution sequence

Execute exactly eight fresh runs, in this preregistered order:

1. A original.
2. A candidate.
3. A candidate.
4. A original.
5. B original.
6. B candidate.
7. B candidate.
8. B original.

For every run, install and launch the bound APK, validate the initial intro component and exact observed hierarchy/selector, acquire one complete initial-screen observation, resolve the exact next selector, and issue one recorded tap at its validated center. Wait exactly two seconds after the input command returns, then acquire five complete TRIGGERS observations sequentially, with exactly one second between completion of one observation and the start of the next. Each observation retains the complete existing PID/component/XML/PNG evidence sequence and its actual monotonic timestamps. Stop before any further app input. Every run has the same app interaction sequence and fixed observation count.

Preserve all five predetermined observations regardless of their pixels. Do not stop sampling after an equal pair, wait for a preferred animation phase, reuse a frame, or repeat an observation to obtain equality. XML/component validation is still required before treating an observation as belonging to TRIGGERS. Record every failed attempt and stop that run on an invalid process/component/input boundary. The separate active journey settling and process rules remain unchanged.

Bound every adb command, each run, and the whole disposable runtime job. Eight runs should have an explicit aggregate limit and owned service/queue cleanup with final setting readback. Avoid a retry that changes the sample count or order. A failed run remains failed and retains its output.

## Evidence and comparison contract

Retain the workflow, all source/tool/plan manifests, both APK identities, installed checksums, environment observations, exact argv/exit codes, stdout and stderr, run chronology, input journal, fresh PID/component samples, every full PNG/XML capture, and cleanup result. Archive the owned output root with its hidden provenance files included. No additional filesystem roots belong in the artifact.

For each predetermined sample index, compute all six unordered cross-run comparisons within each condition: one original-original, one candidate-candidate, and all four original-candidate combinations. Compare the complete frame and complete XML, retaining exact changed coordinates and RGBA values for every unequal pair. Also compare each run's consecutive full-frame samples, recording any continuous animation. Preserve hashes for every frame; no cross-run frame selection, mask, tolerance, pixel normalization, or historical result relabeling is permitted.

As an explicitly additional diagnostic, report the complete raw indicator-bounds pixel array and the original five coordinates for every sample. The bounds must come from that sample's unique observed indicator XML node. Any local region statistic must remain labeled as an indicator observation, with the corresponding full-frame comparison beside it. It supplies no full-frame parity acceptance criterion.

Keep evidence completeness separate from semantic equality. Diagnostic success means the predefined experiment ran with complete bound evidence. Every nonzero full-frame difference remains a nonzero result. This experiment cannot by itself promote a full app parity claim.

## Falsifiable expectations and interpretation

- Variation between two original runs or between two candidate runs under A would show that APK identity alone does not fix the retained raster under that environment. The two already retained zero-scale runs establish this variation (31 original/original pixels and 34 candidate/candidate pixels); the remaining experiment would test the controlled scale dependency.
- A stable pattern in which A retains facing-lobe differences and B produces identical plain-dot geometry would support the proposed ordering dependency. A change in exact mismatch count alone would be weaker evidence.
- Persisting equal-size differences under B would weaken the scale-zero explanation and require renewed investigation. It must not trigger an unreviewed renderer setting change or a looser comparison.
- Equal frames in all eight runs would remain a bounded observation. It would not explain away the historical five-pixel failure.

Because this experiment does not record private animation state or callback arguments, even a supporting outcome would leave a causal gap. If needed afterward, a separate reviewed real-class tracing probe could directly record raw float bits, callback order, and Path construction. Such instrumentation is outside this proposal and must not be introduced into either compared APK.
