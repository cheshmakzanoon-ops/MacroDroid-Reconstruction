# DayTime13: original process failure, incomplete comparison

The supplied original app stops during the promotion-screen capture after notification denial. It records five screens. The reconstruction records all thirteen declared screens and reaches an exact-alarm permission explanation. **The requested thirteen-screen comparison remains incomplete and rejected.**

This is [run 38221713675](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38221713675), job `114719291293`, at commit `e610d98812f3d26da732035e039a1250b8afe9f3`. The fixed original APK is SHA-256 `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`; the fixed reconstruction is SHA-256 `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`. These are the same two APK identities used for the earlier Zero12 comparison.

## Preserved actual failure

The exact hosted final verifier reports `DAY_TIME_TRIGGER_EVIDENCE_INCOMPLETE`, `evidence_valid=false`, with reason `ValueError: Configuration and complete journey are not in order`. The inner comparator reports `REJECTED`, with an empty accepted comparison list and reason `Incomplete run or changed environment`. The independent replay reproduces both objects, excluding only the new outer verifier timestamp. Its diagnostic checks do not replace either verdict.

The original's immediate pre-input PID is `3891`. The freshly verified notification-denial tap succeeds at 08:14:17.444 UTC. The next promotion acquisition calls `pidof com.arlosoft.macrodroid` at 08:14:19.475 UTC; it returns exit code 1 with empty stdout and stderr. The acquisition fails after approximately 0.063 seconds, before recording a full-frame attempt. It does not reach or exhaust the thirty-second frame-settling bound.

The original's pre-denial crash buffer is empty. The later crash-buffer command, retained before the candidate's notification denial, contains an actual main-thread fatal exception for original PID 3891 at 08:14:19.124 UTC: `IllegalStateException` from `Fragment.getResources`, reached through `com.zx.lbua80.onShow`. The exact original stack is classified using the unchanged pinned observer. This establishes the recorded original fatal and the subsequent absent-process observation. The original's restart or continuation is not observed by this run, and notification denial is not asserted to be the underlying cause.

The candidate also records a fatal exception at its notification boundary. Its existing strict handoff verifier checks the replacement PID, old-process absence, foreground component and freshly installed APK identity before continuation. Its raw boundary record is under [lifecycle](lifecycle/candidate-notification-boundary.json). The [failure and handoff report](original-process-failure-and-candidate-handoff.json) binds the exact commands, original failure ledger, later original crash buffer and candidate classification; the referenced raw outputs are preserved under `lifecycle/`. Neither app is described as crash-free.

## Five available pairs: diagnostic observations

The five full-screen pairs that exist in both runs are pixel-identical, with byte-identical hierarchy XML. This partial result does not substitute for the missing eight original screens.

| Available screen | Changed RGBA pixels | Exact XML bytes | Full unmodified screenshots |
| --- | ---: | --- | --- |
| intro-1 | 0 | Yes | [original](review-captures/original-intro-1-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-intro-1-acquisition-1-frame-2.png) |
| intro-2 | 0 | Yes | [original](review-captures/original-intro-2-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-intro-2-acquisition-1-frame-2.png) |
| intro-3 | 0 | Yes | [original](review-captures/original-intro-3-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-intro-3-acquisition-1-frame-2.png) |
| intro-4 | 0 | Yes | [original](review-captures/original-intro-4-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-intro-4-acquisition-1-frame-2.png) |
| notification-request | 0 | Yes | [original](review-captures/original-notification-request-acquisition-1-frame-2.png) / [candidate](review-captures/candidate-notification-request-acquisition-1-frame-2.png) |

The [complete five-pair diagnostic](five-available-full-frame-pairs-diagnostic-only.json) records full PNG/XML identities and every measured pixel difference. The introduction indicator that differed by five pixels in the previous Zero12 run matches here. The older failure remains unchanged; these are separate actual runs, and the new equality does not establish the cause of the earlier difference.

## Candidate-only next surface

The last observed candidate surface is an app-owned `Permission Required` dialog over `AddTriggerActivity`. Its message states that MacroDroid needs permission to set exact alarms and asks for access on the next screen. The exact enabled buttons are `CANCEL` (`android:id/button2`) and `OK` (`android:id/button1`). The observed OK bounds are `[496,761][624,857]`, giving center `(560,809)` after a future fresh input guard.

The [terminal observation](candidate-only-observed-exact-alarm-dialog.json) preserves the literal XML node identities, component, raw artifacts and prior guarded Day/Time tap. [The full screenshot](review-captures/candidate-after-day-time-trigger-acquisition-1-frame-2.png) is unchanged. No input was made after this dialog. Exact-alarm permission was not granted and trigger configuration was not confirmed. There is no original counterpart to this screen in this run.

## Verification and preservation

The replay independently reconstructs all 224 input-copy roles from the exact pinned preparer. It verifies all 2,395 raw files before and after replay, all 717 recorded commands' referenced payloads, 37 capture ledgers, 1,927 unique referenced journey artifacts, and 35 accepted snapshot ledgers. Each accepted snapshot is rechecked with the original live-PID, stable-component, full PNG/XML equality and first-consecutive-pair requirements. The unchanged capture-event gate separately rejects the failed semantic/process acquisition, as required. No attempt is discarded, reclassified as a valid frame, or used to manufacture a complete original run.

The hosted guard logs contain 145 individual successes; the zero-animation helper has ten, and the downloader has six. The declared nineteen-command scale-zero configuration and all device command outputs are checked. The owned runtime cleanup succeeds while preserving the observation step's exit code 2. Complete source-origin hashes, host summaries, configuration data and replay logs accompany this report.

Artifact `11735470323` is exactly 38,451,864 bytes, SHA-256 `ad31af7b9fb237dbca1285a671a3e12fdcd9c3cd3754f55064055066043dffa4`. Its 2,395 unchanged members total 57,260,609 bytes. The parent publication preserves the complete original archive and extracted members. This capsule uses hardlinks for closed review payloads to avoid duplicate allocation; its content hashes are frozen and no linked file is edited afterward.

One emulator boot-log line contains ephemeral ADB public material. The raw ZIP and log remain unchanged. Only a separately labeled review-log copy omits that one value, with both hashes and the explicit transformation recorded. No raw value is repeated in this summary.

No APK, application source, workflow, historical result, runtime screenshot, or original archive is changed by this analysis. It establishes neither a complete thirteen-screen match nor full application 1:1 parity.
