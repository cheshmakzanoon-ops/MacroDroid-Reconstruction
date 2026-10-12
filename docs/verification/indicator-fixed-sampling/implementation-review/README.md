# Independent review of the fixed indicator sampling implementation

The exact inactive indicator implementation **passed this independent review**. No concrete source, protocol, evidence-verifier or workflow blocker was found. This clears the implementation for the root agent's activation decision; it does not establish Android behavior, equal pixels, animation parity or the cause of the historical indicator differences.

The reviewed final source is the sixteen-path capsule `89064abe581191cd0690eda4e739a91a9b5bae3c56cb9156533ddd78a857f7be`, at `work-in-progress/indicator-fixed-sampling/04-closed-synthetic-and-test-correction`. Its workflow is **`64bcf452be163872aca494294c0e57117d7e15436c21cbc0f13c80ce539c1aeb`**. The original APK remains `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`; this experiment deliberately retains the older candidate `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`. It does not substitute the newly recovered numeric candidate.

## What I independently executed

The retained `audit_review.py` is a read-only analysis of frozen inputs and existing evidence. It does not import or execute the application, recorder, verifier, preparer or their test suites. It performed these checks:

- Rehashed all **3,660 declared payload rows** across the approved design, root design review, incomplete draft, implemented/offline capsule and final correction. All sizes, SHA256 values and declared Git modes match. The final capsule contributes 3,422 rows. Repeated identical files in different capsules count as separate declared rows, not unique byte sets.
- Compared all sixteen final source identities with the implemented parent. The only three changed paths are the test, `runtime-files.json` and the workflow. The test contains exactly one assertion-string replacement. The other forty test method ASTs are unchanged. The workflow differs only in the exact test metadata entry, including its byte count; all fifteen runtime-manifest rows match the actual final files.
- Compared the protocol's behavioral fields, all sixteen parent pins and all four observed XML fixtures with the approved design. The actual retained parent files also match their pins.
- Parsed the exact named outcomes in the existing full and focused logs. The forty unchanged passing test bodies plus the corrected test's one passing body cover the same forty-one named bodies. This is a union of retained results; no fresh final full-suite success is asserted.
- Independently decoded the forty existing synthetic full PNGs, enumerated the fixed sixty cross-run and thirty-two temporal pairs, and verified all ninety-two compressed difference files. Full-frame RGBA histograms, record counts, sorted coordinates, both actual pixel values and compressed/expanded hashes agree. Every pair has exactly one differing pixel. Both literal and full-tree XML differ in every pair. The forty additive indicator arrays and all their historical coordinate values also match the source PNGs.
- Rehashed the twenty-four raw stdout/stderr streams associated with the twelve already-closed offline commands and checked their literal exits, including owned cleanup results 0, 7 and 1. I inspected those existing commands; I did not run them again.

`attempt-02/result.json` records the successful independent audit. `attempt-02/verified-capsule-payloads.json` binds every reviewed payload. The source and fixed checkpoint identities were checked again at closure.

## Source and workflow assessment

I read the protocol, preparation, common evidence helpers, recorder, verifier, test fixture and workflow. The implementation preserves the approved schedule:

| Slots | Animator scale | APK order | Post-input observations |
|---|---|---|---|
| 1–4, condition A | 0 | original, candidate, candidate, original | Five per slot |
| 5–8, condition B | 1 | original, candidate, candidate, original | Five per slot |

One checksum-pinned disposable API 35 AVD hosts the entire schedule. Both window and transition scales remain zero. Each slot verifies the fixed device environment, removes the preceding install, verifies package/PID absence, writes and verifies the three intended scales, installs the exact input, verifies the installed digest, resolves the launcher and checks its actual component. The fixed radio/home and demo-clock setup is retained once, with prerequisites and subsequent readbacks bound into the evidence.

The sole input comes from the fresh observed NEXT node, with exact resource, class, enabled/clickable state, bounds and ancestor checks. Its center is (640, 1152). The initial and fresh pre-input full XML must agree, and the immediate PID/component checks remain mandatory. The four-second post-launch wait, two-second post-tap wait and one-second gaps use recorded command/observation endpoints. Images never select a wait duration, retry, sample or alternate frame.

Each slot is reserved before preflight. Immutable attempt and slot receipts, fixed indices and prior-prefix validation prevent a repaired failure from being retried. A failed slot stops the remaining schedule. The 900-second slot bound and single 7,200-second experiment deadline remain unchanged; the global start is not reset by subsequent queued invocations. Evidence finalization belongs to that bounded experiment. Per-command, pre-input and observation bounds remain explicit.

The verifier preserves all ninety-two predetermined comparison rows, including unavailable endpoints on an incomplete run. Full RGBA and full XML comparisons retain their literal result. Its streamed lossless difference format stores the row-major index and both RGBA values for every changed pixel; strict decoding checks the complete record set against the images. Indicator arrays and historical coordinates have zero parity weight and cannot function as masks. Evidence-complete status does not mean equal pixels. Runtime, animation, cause and crash-free success flags remain false.

Live verification binds actual file ownership, one-link regular files, unique stream paths, recorded creation identities, command chronology and immutable attempt receipts. Archive replay explicitly verifies relocated input bytes while keeping the original host metadata as historical evidence; it does not pretend a newly extracted inode or ctime is the original one.

The additive workflow uses pinned checkout/upload actions, the fixed parent commit `6331410cfd2391389270564803623079e8355ad8`, a complete own-source preflight and hidden-workflow retention. It runs full host discovery before preparation or Android, verifies both actual APKs with the pinned read-only AAPT2, creates an owned disposable service/queue, invokes the eight fixed indices and preserves failed or partial evidence. Cleanup sends STOP only to that owned service, retains its outcome and does not turn an earlier failed slot into success. Independent verification and complete owned-artifact upload run on failure as well. Existing app sources, APKs and other workflows are outside its proposed delta.

## Literal host evidence and its limits

The original full run remains **FAILED: forty passed, one assertion failed**, in 851.940 seconds, or 852.341924428 seconds including its wrapper, under the unchanged 900-second timeout. The production guard correctly rejected a changed local APK identity. Only the test's case-sensitive expected regex was wrong. Its final assertion was exercised once against the exact closed Recorder-produced fixture and passed in 7.576 seconds. The focused wrapper explicitly reuses the original fixture/runtime context and overrides only fixture creation; it does not claim a new source-preparation, fresh recorder run or full final-suite run. The hosted workflow still requires all forty-one tests. The small remaining headroom in that earlier full invocation is visible rather than hidden by a timeout change.

The synthetic trace uses a simulated executor and clock and marker files explicitly identified as non-application APK fixtures. It mocks the APK-preparation boundary for capture-protocol testing while executing the real Recorder, verifier and pinned radio-policy code. Its deliberately unequal frames prove retention and accounting behavior within that simulation. They are not Android screenshots or application parity evidence. Separately retained offline validation checked the two real APKs' full ZIP/CRC/AAPT2 identities and all forty fetched parent/part bindings; that read-only work is distinct from executing the final device workflow end to end.

The fixed A-then-B experiment can reveal a bounded association between the scale condition and retained frames. Time, installation order and persistent device history remain potential confounders. It does not observe private indicator fields or callbacks and cannot by itself prove a timing cause. Every predetermined full frame must remain available, even when the normal-scale Lottie animation does not settle. No frame selection, region tolerance or historical-result rewrite is permitted.

## Preserved review attempts and disposition

My first read-only audit stopped at a reviewer parser assertion: I expected the unittest parenthesized identifier to end at the class name, while the actual log includes the method name too. `attempt-01/` retains that exact collector, traceback and result. The corrected parser requires the short and fully qualified method names to agree. This was a reviewer error; no producer, test or evidence file changed.

The owner's separate failed binding-checker and freezer-order assumptions remain in the final source capsule, along with the literal full host failure. Nothing in this review relabels them. `review-inputs/` contains small exact copies of the source delta and outcome records for convenient review; the large synthetic dataset remains bound to its original frozen capsule.

**Disposition:** no blocking defect found in the exact final implementation. Actual Android execution and independent complete-artifact review remain pending. This review authorizes no app promotion, code alteration, relaxed comparison rule or runtime parity credit.
