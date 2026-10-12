# Independent review: actual thirteen-screen readiness run

The closed Android run **38230072388** records a valid, complete thirteen-screen observation with a remaining visual difference. The literal final status is `DAY_TIME_READINESS_THIRTEEN_SCREEN_DIFFERENCE`, and the literal comparison is `JOURNEY_DIFFERENCE`. This independent audit confirms that result; it does not convert the run to a parity pass.

The single downloaded ZIP is 44,543,663 bytes, SHA-256 `c8f0af87e5d91efe2dfc49b8ca76acc1a0943b2a2b8e17ffe279892726d2c80f`. It belongs to artifact 11739145683 and head `e1ade015f938339479216a1a91518e556902fce8`. The retained extraction receipt has SHA-256 `61c47bb315336958869a5cf3b945c7cbdb649de65786495f04b105ce5fa33419`.

## Actual independent execution

The retained analyzer executed successfully from 09:49:20.151051 to 09:49:27.572134 UTC on 2026-10-12. Its wrapper took 8.079 seconds, returned zero and produced empty stderr. No Android command was executed again, and no raw evidence was modified.

It independently rehashed all **3,258 ZIP members and extracted files**, totaling 70,899,613 bytes, against the receipt and against each other. It then rechecked all **252 executed-input copy roles**, all **81 reviewed runtime files** against the independently pinned corrected guard, and the exact executed workflow hash `56808b331ec8995c5ebf82a5a55972dfa75c078233247543a5f526f2f0949930`. It did not perform a network refetch.

All **1,021 recorded journey commands** have finite, chronological, nonoverlapping intervals and unique stdout ownership. Their 2,042 stdout/stderr files were rehashed. There are no timed-out commands; 1,018 commands returned zero and three returned one. These are the recorded command outcomes, not newly executed checks against the device.

The parent separately reran the complete pinned production analyzer and froze that result as checkpoint `716e3cd70c54659f1b0b84a68a875d61d8c3b1b41e864eb36756938660612439`. This capsule contains the independent raw-interval, settling, terminal-control and pixel work rather than repeating the parent's complete replay.

## Notification readiness observations

Both runs completed the readiness phase after four observations of the home activity with the same PID within each observation sequence. The independent audit read each raw PID output, matched the top resumed activity to its actual `ProcessRecord`, checked the three-command order, and verified each copied command's unique adjacent position in the global ledger immediately after the denial input.

| Measurement | Original | Candidate |
| --- | ---: | ---: |
| Old PID | 4049 | 7262 |
| Ready PID | 5474 | 8331 |
| Observations / read-only commands | 4 / 12 | 4 / 12 |
| Accepted sequence | `[0,3]` | `[0,3]` |
| Post-denial wait | 2.005084972 s | 2.002384160 s |
| Complete readiness phase | 1.101786011 s | 1.221094301 s |
| Span from first PID command start to final PID command finish | **1.099872771 s** | **1.218252554 s** |
| First strict capture begins after phase finish | 0.000529860 s | 0.000892400 s |

In both cases, the third observation still spans less than 1.05 seconds from the first raw PID-command start. The fourth is the first eligible sequence endpoint. All three 0.25-second gaps are correctly ordered, the entire phase is within ten seconds, and strict screenshot capture begins after the phase finishes. The old PID is bound to the actual pre-denial read, and the promotion capture uses the ready PID.

The retained comparison records the known Fragment LB fatal exception and subsequent process replacement in both apps. Its `crash_free_run_established` flag remains false. These bounded observations establish neither continuous liveness between reads nor a crash-free execution.

## Full-frame comparison and settling

Both apps completed **13 screens and 12 inputs**. The independent decoder compared all four RGBA channels over each full 720×1280 image. It used no crop, mask, tolerance or cross-frame selection. PNG chunk CRCs and non-IDAT metadata were checked independently.

The thirteen changed-pixel counts, in recorded screen order, are:

```text
0, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
```

All thirteen XML hierarchies are byte-identical. Twelve full PNG/RGBA pairs are identical. The only differing pair is `intro-2`. Its 26 exact RGBA differences are retained in `paired-full-frames.json`, within inclusive bounding box **[313,1184,351,1199]**. That box lies inside the actual XML indicator node, `com.arlosoft.macrodroid:id/indicator`, whose bounds are **[128,1184][592,1200]**. This locates the difference; it does not establish its cause.

All **50 settling events and 100 frames** were checked. Each event accepts its first consecutive byte-identical PNG-and-XML pair, stays within the six-attempt/thirty-second policy, and retains matching first/final app PIDs for each frame. The audit also verifies that accepted screen paths bind back to the recorded artifacts. The detailed event list and the raw readiness endpoint list are included.

Earlier five-pixel, zero-pixel and other recorded indicator outcomes remain unchanged. This actual run contributes a separate 26-pixel observation and does not resolve the proposed timing hypothesis.

## Terminal controls and current boundary

Both final XMLs show the same `Permission Required` dialog asking for exact-alarm access. The enabled, clickable controls are:

| Text | Resource ID | Bounds |
| --- | --- | --- |
| CANCEL | `android:id/button2` | `[342,761][496,857]` |
| OK | `android:id/button1` | `[496,761][624,857]` |

The foreground activity is `com.arlosoft.macrodroid.selectableitemlist.AddTriggerActivity`. There is no recorded input after the Day/Time trigger tap. `trigger_configuration_confirmed`, `macros_saved` and `macros_executed` remain false. This review does not perform either dialog action.

## Evidence scope

The capsule retains the exact executed analyzer, wrapper logs, input identities, every independently counted pixel coordinate, all readiness intervals, all settling-event results and the observed terminal controls. Small raw excerpts are copied unchanged for review. The complete original ZIP remains with the publisher's separately retained raw-artifact package.

The independent analyzer used Pillow 12.3.0 and NumPy 2.3.5 for full-image RGBA decoding. All 3,258 raw files were rechecked unchanged at the end of execution. The result is **`INDEPENDENT_ACTUAL_READINESS_DIFFERENCE_CONFIRMED`**, while full runtime 1:1 remains unestablished.
