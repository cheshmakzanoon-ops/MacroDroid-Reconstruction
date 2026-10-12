# Fixed indicator sampling: eight-install diagnostic design

**Design only.** This capsule authorizes no workflow activation, Android action, APK build, application edit, or parity promotion. It makes the source dossier's proposed experiment concrete enough for implementation review. The eight-run order, one observed input, and all predetermined captures are fixed before a device run.

## Question and limits

The retained `InkPageIndicator` source permits a joining fraction to remain after its animator finishes before the independent ViewPager scroll. The source dossier's checkpoint is `00cde07343d7d7a106171070b462b4b2879705d3f926f6f22abcaae90a97fce3`. This design varies only `animator_duration_scale` to test an association with the recorded raster variation. It does not read callback order or private fields and cannot prove the proposed cause.

The comparison APKs remain original `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800` (95,725,918 bytes) and combined candidate `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182` (94,683,119 bytes). Their immutable container manifests and assembly helper are bound in `evidence/parent-bindings.json`. An independently running numeric source study supplies no APK to this diagnostic.

The proposed condition order is deliberately fixed, not randomized. Condition B always follows A on one disposable AVD. Time, installation order, and any unobserved device history remain possible confounders. A result would be a bounded scale-dependency observation, not a general causal or deterministic claim.

## Actual history, with explicit run identities

All times below are GitHub run creation times on 2026-10-12 UTC. Exact metadata, source heads, and final update times are retained in `historical-run-metadata.json`.

| Run | Created UTC | Candidate | Recorded intro2 result and remaining scope |
| --- | --- | --- | --- |
| `38205737183` | 04:55:18 | `9108b581…`, the older candidate | 26 differing pixels in every one of four retained TRIGGERS frames per APK. This is the separate failed ten-screen observation. |
| `38216299675` | 07:10:39 | `5f635e16…` | Five differing intro2 pixels in the completed twelve-screen run; its full comparison remains failed. |
| `38221713675` | 08:07:53 | `5f635e16…` | Zero differing pixels among five available paired screens, including intro2. Original is incomplete while candidate has thirteen screens. No complete thirteen-screen match follows. |
| `38230072388` | 09:28:07 | `5f635e16…` | Both thirteen-screen captures completed. The exact pixel vector is `[0,26,0,0,0,0,0,0,0,0,0,0,0]`, with equal XML. Known fatal exception and process replacement/continuation are still recorded for both applications. |

The design collector rehashed 69 read inputs, verified all 135 members of the closed source-dossier archive, read 16 exact parent Git blobs, and independently decoded the complete accepted intro2 pair in the three `5f635e16…` runs. It reproduced pixel counts 5, 0, and 26. It did not replay those complete journeys or re-verify their entire raw ZIP containers; the prior closed analyses retain that responsibility. The older 26-pixel coordinate record is copied as a source-bound prior result, not newly re-executed.

The prior all-scales-one run `38212813248` used the older `9108b581…` candidate and failed consecutive full-frame settling during intro2's continuing Lottie animation. Its exact source-dossier account remains relevant background, not a B-condition measurement of `5f635e16…`.

## Observed input and indicator coordinates

The original and candidate readiness13 preinput XML copies are retained under `evidence/observed-xml/`. Both identify the initial title as `MACRODROID` and the unique NEXT node as:

| Field | Actual XML observation |
| --- | --- |
| Package | `com.arlosoft.macrodroid` |
| Resource ID | `com.arlosoft.macrodroid:id/button_next` |
| Class | `android.widget.ImageButton` |
| Content description | `Next` |
| Enabled / clickable | `true` / `true` |
| Bounds | `[592,1104][688,1200]` |
| Center | `(640,1152)` |
| Resumed component | `com.arlosoft.macrodroid/.intro.IntroActivity` |

Each of the three inspected run journals contains the actual command `input tap 640 1152`. These coordinates are recorded input evidence, not inferred from source geometry. The future tap must still resolve the same unique semantic node and its full clickable ancestor chain from that install's fresh XML, require the recorded bounds on the pinned 720×1280 display, and derive the center again. A mismatched or ambiguous control fails before input.

Every inspected intro2 XML exposes a single indicator node `com.arlosoft.macrodroid:id/indicator` at `[128,1184][592,1200]`. The readiness13 complete-frame comparison independently reproduces 26 coordinates inside `[313,1184,352,1200)`; their two RGBA values are in `evidence/fixed-historical-capture-bindings.json`. The five coordinates from run `38216299675` are `(317,1186)`, `(319,1189)`, `(335,1192)`, `(319,1194)`, and `(336,1195)`. Neither these coordinates nor the dossier's source-derived dot centers are input targets or a comparison mask.

## Fixed device and eight-install sequence

Use the existing pinned API35 Google APIs x86_64 image with the observed ARM64 native bridge, a newly created disposable `MacroDroid_API35_Disposable` AVD, serial `emulator-5560`, and the existing KVM/headless/SwiftShader service configuration. Require the exact parent fingerprint, 720×1280 physical display, density 320, font scale 1, locale/timezone, and recorded native-bridge/ABI predicates. Start one AVD for the eight installs.

Run the unchanged radio/demo-clock helper once with `--demo-clock 1200`, preserving its actual signal-level stability result. Fix window and transition scales to zero in both conditions. Set/read animator scale before every install slot while no app process is running; never change scale during an observed app process.

| Slot | Condition | APK | Animator scale | Window scale | Transition scale |
| --- | --- | --- | --- | --- | --- |
| 1 | A | Original | 0 | 0 | 0 |
| 2 | A | Candidate | 0 | 0 | 0 |
| 3 | A | Candidate | 0 | 0 | 0 |
| 4 | A | Original | 0 | 0 | 0 |
| 5 | B | Original | 1 | 0 | 0 |
| 6 | B | Candidate | 1 | 0 | 0 |
| 7 | B | Candidate | 1 | 0 | 0 |
| 8 | B | Original | 1 | 0 | 0 |

For every slot, uninstall without retaining package data, prove package and main-process absence, install the locally hash-verified exact APK, verify its installed path and SHA-256, resolve the actual launcher, and launch. The consecutive candidate slots still perform a full uninstall/reinstall. This is eight fresh application installations, not eight independently booted devices.

Retain the complete environment before launch and after the last sample. Read all three scale keys before input and after the last sample, with exact raw commands and values. Within a condition all fixed environment fields must match. Across conditions the declared animator scale is the only allowed configured difference. A device configuration failure supplies no app/pixel result.

## Single-input and fixed-sample protocol

After the existing fixed four-second post-launch wait, retain one initial full-screen observation. Establish a fresh installed-APK guard, a separate fresh full preinput observation, and immediate main-PID and resumed-component checks. Require the same single main PID and normalized `IntroActivity` throughout that slot. Initial and preinput full hierarchies must agree; both must satisfy the exact observed title/NEXT/ancestor/bounds identity. Keep the existing 15-second input-freshness budget, including acquisition and identity reads. Then send exactly one clean NEXT tap.

After the tap command returns, request a fixed two-second wait. Acquire five full TRIGGERS observations. Between completion of one observation and the start of the next, request exactly one second. This is an **observation-completion gap**, not a claim that screenshots occur at one-second start-to-start cadence: XML and foreground acquisition take real time.

The wait journal records requested nanoseconds, monotonic start, target, and actual finish. Every observation and command retains its actual operation endpoints and latency. A wait may overshoot under scheduling; its measured time is reported literally and never relabeled as exact. No delay is changed after inspecting an image.

Each observation preserves the existing full sequence: main PID; resumed activity; unique remote XML dump and retrieval; complete PNG; final resumed activity; final main PID. The future sampler adds explicit chronological records and fresh artifact identities while retaining the existing minimum observation interval. It validates `TRIGGERS`, the unique indicator, unchanged app PID, and exact `IntroActivity` for every sample. It retains unexpected or partial output before recording failure.

There is no settling loop, image-dependent retry, duplicate sample substitution, page2 recapture for equality, or second app input. Forty post-tap samples are planned, plus eight initial and eight fresh preinput observations. A failing slot retains its output and may be followed only by the next fixed uninstall/install slot if the same disposable device can be freshly verified. An unusable shared device leaves remaining slots explicitly unattempted. Failed slots are never replaced or reordered.

## Exact parents and a separate diagnostic policy

`evidence/parent-bindings.json` pins every source below to fetched commit `6331410cfd2391389270564803623079e8355ad8`, including full SHA-256, bytes, Git mode, and function locations.

| Parent | Proposed use |
| --- | --- |
| `tools/android/bootstrap_android_runtime.py` and toolchain pins | Verified downloads, safe extraction, fresh AVD creation, exact installed tooling verification. |
| `android_runtime_service.py`, `runtime_job.py`, `wait_android_ready.py` | One owned ADB/emulator session, explicit argv queue, bounded readiness, native bridge checks, and owned STOP cleanup. |
| `configure_capture_device.py` | Actual cellular profile/registration and documented demo clock; complete raw configuration evidence. A new small condition setter writes and verifies the declared 0/1/0/0 settings only. |
| Trigger05 `replay-source/tools/parity_journeys/editor_journey.py` | `Recorder.cmd/shell/save/environment`, XML parsing/selection, ancestor and bounds checks, and the existing single-acquisition command sequence. Do not invoke its complete journey `main`. |
| Trigger05 `replay-source/tools/parity_journeys/observed_journey.py` | Exact full-frame decoder, single-PID/component predicates, and six-artifact observation validation. Do not invoke `settle`, change `POLICY`, or configure a different existing plan. |
| Trigger05 `replay-source/project/android_compare.py` and `android_acceptance.py` | Existing strict install/absence/installed-digest/launch checks, exact package metadata prevalidation, full RGBA and color metadata checks, and complete XML comparison. |
| Zero12 `prepare_trigger_journey.py`, `verify_trigger_journey.py`, and workflow | Structural parent for independently reconstructed input inventory, immutable APK manifests, artifact completeness, and owned cleanup. Their twelve-screen equality gate is not reused as a diagnostic success label. |

Implementation would use a new owned fixed sampler and a new report/plan identity. It would derive a literal single-acquisition routine with both foreground endpoints; it would not abuse an existing `capture_policy` sentinel, patch imported globals, or switch off the active journey guard. Existing thirteen-/fourteen-/sixteen-step plans, settling policy, and comparators remain byte-identical.

The independent diagnostic verifier must reconstruct exact input and output roles, all eight slot identities, per-slot action count, and all five sample indices. It must reject reused canonical paths or physical files while live, source/report inventory omissions, stale command streams, chronology before the tap, PID/component changes, and scale drift. After archive extraction, recorded host inode/timestamp observations remain serialized evidence; replay must not equate newly extracted inode/ctime with the original host values.

## Comparisons and interpretation

For each of five sample indices and each condition, compute all six unordered pairs among the four fixed slots: one original/original, one candidate/candidate, and four original/candidate. This gives 60 cross-run full-observation comparisons. Also compare each slot's four consecutive sample pairs, giving 32 temporal comparisons. Their 92 predetermined pair roles are fixed in `protocol.json`; none is chosen using visual similarity.

For every pair, report complete decoded RGBA difference count, exact changed coordinates and both RGBA values, PNG byte equality, complete XML byte and canonical attribute equality, dimensions, and color metadata. Preserve every nonzero full-frame difference, including the scale-one Lottie region. Hash and retain all original files.

As additional diagnosis only, retain the indicator's complete RGBA array from the unique XML bounds for each sample and values at the previously recorded five/26 coordinates. These numerical region observations accompany the complete-frame comparisons and carry no parity acceptance weight. No cropped screenshot, pixel replacement, mask, tolerance, or cross-app frame selection is introduced.

`INDICATOR_FIXED_SAMPLE_EVIDENCE_COMPLETE` would mean only that the fixed experiment and evidence contract completed. Differences may be present under that status. A missing/invalid slot or sample yields `INDICATOR_FIXED_SAMPLE_EVIDENCE_INCOMPLETE`. In either case, full app 1:1, method credit, macro functionality, causal callback ordering, animation parity, and a crash-free run remain unestablished. No historical failed comparison is relabeled.

## Bounds and implementation review gate

The proposed upper bounds are: 15 seconds for the fresh input boundary; 30 seconds for each complete observation; 120 seconds for an ordinary ADB command, clipped by its enclosing bound; 600 seconds for install and 180 for launch; 900 seconds per slot; 7,200 seconds for the eight-slot experiment; 900 for boot readiness; 240 for radio/demo setup; and a 150-minute outer workflow bound. These are hard ceilings, not reasons to extend or retry a failed slot. Record partial output at every failed boundary. Use the parent's owned service PID and exact queue for cleanup, with final setting readback and a cleanup receipt.

A later reviewed source capsule would add only a small preparation helper, condition setter/fixed sampler, independent verifier, tests, protocol/pins, and README under a new inactive `work-in-progress/indicator-fixed-sampling/` path. A separate `.github/workflows/indicator-fixed-sampling.yml` would be proposed only after review. No such implementation or workflow is included here.

The required future host controls should reject wrong APK/order/condition, omitted/extra sample, second input, stale or physically aliased evidence, a capture that predates its tap, a borrowed installed checksum, PID or component change, duplicate/disabled/out-of-bounds NEXT, changed scale, timeout/partial XML, and an omitted input inventory row. The positive control must retain exactly 40 scheduled full post-tap frames even when every pair differs. These controls are planned, not executed by this design capsule.
