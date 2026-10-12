# Fixed indicator sampling diagnostic

This independent experiment records the actual intro indicator after a fixed input and fixed waits. It uses the reviewed [bounded design](../../work-in-progress/indicator-fixed-sampling/01-bounded-design/) and retains every planned observation. `INDICATOR_FIXED_SAMPLE_EVIDENCE_COMPLETE` means the declared evidence is complete. It does not mean that any original/candidate pair is equal, that animation or crash-free behavior is established, or that full runtime parity has been reached.

## Immutable applications and parent helpers

The original APK is 95,725,918 bytes / SHA-256 `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`. The candidate is the already published combined APK, 94,683,119 bytes / `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`. A new numeric or lookup APK is not substituted. Both twelve-part manifests, all twenty-four part hashes, all sixteen original helper declarations, and the complete executed diagnostic source inventory are checked before installation and after the observations.

All sixteen design parents remain pinned to commit `6331410cfd2391389270564803623079e8355ad8`; their exact paths and byte hashes are in [pins.json](pins.json). This successor adds the preserved AAPT2 binary explicitly: 6,135,688 bytes / `6fbed5edaddcfbee99a3ae6e7208c8654c6cb2bedb4ed5cbbf4e154d7d38a745`. It runs only read-only `dump badging`, bounded to 60 seconds. Both fixed APK hashes, full ZIP member uniqueness and CRC checks, and the actual parsed package/version metadata are required before any uninstall. Assembly is bounded to 120 seconds per APK. Partial command output is retained on failure.

## Eight fixed slots

| Slot | Animator scale | APK |
| ---: | ---: | --- |
| 1 | 0 | Original |
| 2 | 0 | Candidate |
| 3 | 0 | Candidate |
| 4 | 0 | Original |
| 5 | 1 | Original |
| 6 | 1 | Candidate |
| 7 | 1 | Candidate |
| 8 | 1 | Original |

Every slot removes the package and its data, proves package and old-process absence, writes the three declared animation scales while the app is absent, verifies the actual settings, installs the exact selected APK, and rehashes the installed package. Window and transition scales remain zero in both conditions. The pinned setup helper first establishes the one modem's actual home registration and level-four primary radio, then enables SystemUI clock demo `1200` and the initial zero scales. Its complete before/after report and raw command streams are retained. Battery and wall time receive no writes.

There is one fixed AVD and serial: `MacroDroid_API35_Disposable`, `emulator-5560`, API 35, 720 × 1280, density 320, with the exact published fingerprint and native bridge. A fresh AVD, boot, modem, ADB-file identity, and full environment guard precede each uninstall. Every capture and the sole input require one continuous app PID and the actual `IntroActivity` component.

After launch, the recorder waits four seconds from the launch command's return. It takes the initial full observation, then obtains a fresh installed hash, scales, full preinput observation, and immediate PID/component readings under a 15-second guard. The complete initial and preinput canonical hierarchies must be identical. The unique observed `button_next` must retain its exact enabled/clickable class, text/description, bounds, and ancestor attributes. Its actual center is **(640, 1152)** from bounds `[592,1104][688,1200]`; the fixed input is exactly one tap there. These coordinates are taken from the retained XML, not guessed from a screenshot.

The recorder then waits exactly two seconds from the tap command's return before starting sample 0. It always records samples 0 through 4. Each later observation starts after a fixed one-second wait measured from the preceding complete observation's closure. Actual start, return, closure, wait target, and overshoot times are retained. This is not a one-frame-per-second wall-clock promise: the full acquisition itself takes measured time. Each observation is bounded to 30 seconds and brackets its XML/PNG with fresh PID and foreground evidence.

The expected post-input title is `TRIGGERS`. The title and indicator identities, ancestry, and full viewport are checked. Other hierarchy changes remain measured full XML differences; the historical complete hierarchy is not imposed as a rendering template. No settling loop, image-dependent retry, preferred-frame selection, screenshot edit, crop, tolerance, or mask exists in this experiment.

## Explicit queue and failure contract

The parent service's 3,600-second request ceiling remains unchanged. This implementation uses eight separately queued, fixed-index invocations of at most 900 seconds each. This is an explicit implementation change from the single conceptual design operation. Each invocation has a new owned slot directory and an immutable attempt receipt, with all prior slot receipts rechecked before the next begins. One experiment start and 7,200-second deadline cover all eight slots and comparison finalization. The clock is never reset between invocations.

Any failed slot or preflight aborts the remaining slots. Its owned attempt and partial raw output remain; remaining indices are marked unattempted. An index cannot be retried, repaired in place, skipped, or reordered. The service is stopped only through this job's new owned queue, and the cleanup result is recorded. Boot is bounded to 900 seconds, configuration to 240 seconds, and the complete workflow to 150 minutes.

## Every predetermined comparison and value

The result retains all 40 post-input full PNGs and XML hierarchies, plus the eight initial and eight preinput observations. All six unordered pairs among the four slots in each condition are compared at each of the five sample indices: **60 cross-run pairs**. Four adjacent sample pairs within each of eight slots add **32 temporal pairs**, giving **92 predetermined comparisons**. A missing endpoint produces an explicit unavailable pair; it never reduces the denominator.

Each comparison decodes both complete PNGs, counts every unequal RGBA pixel, compares PNG color metadata, and compares both literal and canonical full XML. All changed coordinates and both RGBA values are saved losslessly in a streamed gzip file. Its fixed **12-byte record** is:

| Bytes | Encoding |
| --- | --- |
| 0–3 | Unsigned 32-bit big-endian row-major pixel index, `y × width + x` |
| 4–7 | First frame's four RGBA bytes |
| 8–11 | Second frame's four RGBA bytes |

Records are strictly increasing by index. JSON records width, height, count, expanded byte length and SHA-256, and compressed byte length and SHA-256. Independent decoding checks every saved record against both exact source frames and recounts the entire frame. There is no large in-memory list of changed pixels. A zero-difference pair still has a valid empty gzip stream and exact metadata.

Additional raw RGBA arrays for the observed indicator rectangle `[128,1184,592,1200]` and the exact historical coordinate union are numerical diagnostics only. They have zero parity weight and never replace a whole-frame comparison. [historical-coordinates.json](historical-coordinates.json) binds the actual runs by ID and timestamp: Zero12 `38216299675` has five intro-2 pixels; Day13 `38221713675` has zero among five comparable pairs but an incomplete original run; readiness13 `38230072388` completes both thirteen screens and has twenty-six intro-2 pixels. None of those results is rewritten.

## Independent verification and replay

`verify.py` reconstructs the complete fixed command/order/role inventory. It rejects omitted, borrowed, reordered, reused, physically aliased, or stale capture evidence, another AVD/APK/PID/component, a changed scale, an extra input, a missing frame, or an extended deadline. Exact saved slot and observation receipts bind every acquisition to its own command streams. The live mode checks actual final file metadata against the original exclusive-creation records.

An archive replay requires explicit `--archive-replay --archive-apks PATH`, with exact relocated `original.apk` and `candidate.apk` files plus the pinned parent parts and diagnostic source. It reads the immutable original argv/root strings and separately verifies the relocated bytes. For capture metadata it uses the original serialized host observations; it does not claim an extracted file's ctime or inode is the host value. Extracted physical aliases still reject. The raw experiment/comparison are not modified by replay.

Host controls use a clearly labeled synthetic command executor and clock. They do not run ADB or Android and confer no device parity credit. The executed source, all partial attempts, the complete actual raw capture tree, all 92 pair records, and the independent result belong in the workflow artifact, including hidden executed workflow copies.
