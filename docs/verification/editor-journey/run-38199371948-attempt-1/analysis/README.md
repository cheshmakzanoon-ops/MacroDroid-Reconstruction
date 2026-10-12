# Actual partial editor journey: run 38199371948

The [hosted editor run](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38199371948) at commit `3f584e6c958958a5d823e33f8facd0dcdae906f8` **failed before reaching an editor screen**. Both supplied APKs were freshly installed with their installed SHA-256 identities verified. Each completed the four introduction pages, opened the notification permission request, and tapped its observed denial button. The next capture showed an app-owned LITEAPKS dialog over `NewHomeScreenActivity`. The planned `navigation_home` selector was absent from that dialog's hierarchy, so both recorders stopped at the step named `home`.

The full editor comparator remains `REJECTED` with reason `Incomplete run or changed environment`. Replaying the exact comparator source from the tested commit against the preserved artifact reproduces that result. This analysis does not turn the failed run into an editor-parity pass. Its narrower measurements include two actual screenshot differences that remain failures.

## Exact evidence and identities

The evidence bot preserved the immutable ZIP and original reports at commit [4f7e19d](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/4f7e19d4d63c2f6ac4b3eba2cfa2de8604099ebb/docs/verification/editor-journey/run-38199371948-attempt-1). The ZIP is 4,058,327 bytes with SHA-256 `5edc5aa2a46b2281432c082046400474f53a466ed8c77f6747c5e11a2f0adc70`; GitHub artifact ID is `11724069270`. All 740 archive members and all 628 unique artifact paths referenced by the journey were independently checked against their byte counts and hashes. The raw reports were not rewritten. The expanded `captures/` files here are exact copies from that ZIP.

| Installed input | Verified SHA-256 |
|---|---|
| Supplied original | `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800` |
| Tested 1,239-method candidate | `be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce` |

This run predates the subsequent 1,240-method candidate. Its result must not be attributed to that later APK. The 23 verifier host controls passed in 2.167 seconds; this is independently recorded host testing and does not change the failed device-journey outcome.

The device was the explicitly selected API 35 emulator, serial `emulator-5560`, fingerprint `google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.043/12960925:userdebug/dev-keys`, advertising `x86_64,arm64-v8a`. Both initial recorded environments match: 720×1280, density 320, font scale 1.0, UTC, SystemUI demo mode enabled, and all three animation scales zero. The separate configuration records requested the 12:00 demo clock and stabilized the real cellular presentation. Neither failed journey recorded an end-of-journey environment sample. These limits remain explicit in [independent-analysis.json](independent-analysis.json).

## Full screenshot and hierarchy measurements

All comparisons below use the complete 720×1280 RGBA image and complete UI hierarchy. A second decoder independently confirmed each changed-pixel count. No crop, mask, tolerance, or ignored XML attribute was applied.

| Recorded step | Changed RGBA pixels | Full XML | Full PNG bytes |
|---|---:|---|---|
| intro-1 / MACRODROID | 0 | Identical | Identical |
| intro-2 / TRIGGERS | **35** | Identical | Different |
| intro-3 / ACTIONS | 0 | Identical | Identical |
| intro-4 / CONSTRAINTS | 0 | Identical | Identical |
| notification-request | **570,819** | Identical | Different |
| home / actual LITEAPKS dialog | 0 | Identical | Identical |

The 35-pixel difference lies within `[313,1184][352,1200]`, using exclusive upper bounds, around the pager indicators. The permission images show different background dimming behind the same dialog: the original capture is dimmed and the candidate capture is undimmed. This is a visual observation; the cause has not been established. Their full-image difference remains recorded even though the permission hierarchy matches.

Review the actual [original permission PNG](captures/original-notification-request.png) and [candidate permission PNG](captures/candidate-notification-request.png), and the [original TRIGGERS PNG](captures/original-intro-2.png) and [candidate TRIGGERS PNG](captures/candidate-intro-2.png). The historical 95077 exact-still result remains a separate run; it does not override the differences measured here.

## Observed landing surface and inputs

Both landing captures have resumed component `com.arlosoft.macrodroid/.homescreen.NewHomeScreenActivity`. The UI dump contains only the app-owned dialog, so its expected home navigation selector has zero matches. The screenshot shows the home behind the dialog, but no unobstructed home hierarchy or editor screen was recorded.

| Observed node | Exact evidence |
|---|---|
| Title | App-owned `android.widget.TextView`, text `LITEAPKS`, bounds `[334,375][560,449]` |
| Close | App-owned `android.widget.Button`, text `CLOSE`, enabled and clickable, bounds `[124,832][344,928]`; center `(234,880)` |
| Download | Separate app-owned `android.widget.Button`, text `DOWNLOAD✅`, bounds `[376,832][596,928]` |
| Don't show again | Unchecked switch; no input was sent to it |

The landing PNGs are byte-identical, SHA-256 `01aab2a065e5087416e74ce96b22050673a3fe675d51716f34c81f038ada4023`; the landing XMLs are byte-identical, SHA-256 `77ccbb1de2f4ce42c402f25c80404b74eece18943f5d003e6cb15c9478d0a4f2`. See [original PNG](captures/original-home.png), [candidate PNG](captures/candidate-home.png), [original XML](captures/original-home.xml), [candidate XML](captures/candidate-home.xml), and the two exact foreground records in `captures/`.

Exactly ten input commands were recorded: four validated Next taps at `(640,1152)` and one validated notification-denial tap at `(360,820)` for each APK. Each transition's newly acquired hierarchy, PID continuity, immediate foreground/PID observations, input bounds, command outcome, and freshness budget were checked. No CLOSE, DOWNLOAD, permission grant, editor selection, macro save, or macro execution input was issued. A future recorder change can target the now-observed CLOSE button only after revalidating this specific dialog and foreground component; this analysis performs no device action.

## Process continuity is a separate unresolved gate

The original app used PID `4062` through the notification request and PID `4985` at the landing dialog. The candidate used PID `5545` through the request and PID `6288` at the dialog. Both landing samples have equal first/final PIDs and the expected resumed home component. The records demonstrate a PID change, but do not establish its cause or prove a legitimate handoff.

The existing complete-journey comparator requires its initial PID throughout the journey. That gate is retained. A later successful navigation could still be rejected by this continuity requirement. Supporting a deliberate handoff would require an explicit, narrowly recorded boundary with renewed installed identity and live-process evidence; simply dropping PID checks would weaken the proof. Unexpected restarts during a fresh input guard must continue to reject input.

The preserved comparator's `android_runtime_executed: false` is set only after a complete journey validates. In this failed run, actual installs, live Android processes, inputs and screenshots did occur. The independent analysis names those observations explicitly while keeping `requested_editor_journey_passed` and `full_runtime_1_to_1_established` false.

`analyze_preserved_run.py` is the exact analysis program. `pinned-source/` contains the reviewed source used for its read-only comparator replay, with exact commit and hash provenance. The analysis did not start an emulator or execute artifact recorder entry points.
