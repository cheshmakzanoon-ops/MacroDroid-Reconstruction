# Editor run 38202401351: identical later stills, a shared crash, and a page-dot difference

The [actual hosted run](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38202401351) remains **failed**. Both APKs reached home, the empty editor, and the **Favourite Triggers** information dialog. Neither reached the requested Add Trigger catalog. Eight of nine complete screenshot pairs are identical; the TRIGGERS page differs by 26 pixels. Both processes also logged the same Java exception type and stack before continuing in new processes.

This analysis adds observations to the preserved failure. It does not change the original fourteen-step plan, the archived comparison, either APK, or any screenshot.

## Exact inputs and archive

The tested commit was `cada56c8a11ff5cbd892ec6d0beaeab60b3e644d`. Its exact artifact is already preserved by archive commit `4c279db5619b2d22fdb12d6f084e740bfc5ce20c` in the [parent evidence directory](../README.md).

| Item | Exact identity |
| --- | --- |
| Original installed APK | `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800` |
| Candidate installed APK | `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2` |
| Artifact | 6,517,530 bytes; SHA-256 `fa2eca5f893ae181b91aa7a7bf5df8320620bbc8da21b87eacffb1de0c3bc7ee` |
| Artifact ID | `11725238666` |
| Archive verification | All 1,042 member paths, lengths, and hashes checked |
| Recorder evidence | All 904 distinct referenced artifact paths checked |
| Host gates | 31 journey tests and 6 download tests passed |

The analysis independently replayed the exact pinned comparator under its unchanged reference-plan adapter. It reproduced `REJECTED`, with reason `Incomplete run or changed environment`. Both actual run records are `FAILED` at `trigger-catalog`, with reason `Missing or ambiguous selector: {'text': 'Add Trigger'}`. Both contain nine captured screens and eight inputs. The recorded pre-run environments match; failed runs do not contain completed post-run environment records. All fresh-install, launch, and installed-APK checksum evidence was verified directly.

## Complete images and hierarchies

Each measurement includes all 720 × 1,280 RGBA pixels. Every complete XML byte pair is identical, and all PNG color metadata pairs match. No crop, mask, tolerance, attribute removal, or image rewrite was used.

| Recorded screen name | Actually observed surface | Changed pixels | Raw PNG bytes equal |
| --- | --- | ---: | --- |
| intro-1 | MACRODROID | 0 | Yes |
| intro-2 | TRIGGERS | **26** | No |
| intro-3 | ACTIONS | 0 | Yes |
| intro-4 | CONSTRAINTS | 0 | Yes |
| notification-request | Notification permission prompt | 0 | Yes |
| reference-promotion | App-owned LITEAPKS dialog | 0 | Yes |
| home | NewHomeScreenActivity | 0 | Yes |
| empty-editor | EditMacroActivity | 0 | Yes |
| trigger-catalog | **Favourite Triggers information dialog** | 0 | Yes |

The TRIGGERS difference occupies `[313,1184,352,1200)` in the full image. Visual inspection places it on the first and second page indicators below the example caption. The original full image is [original-intro-2-acquisition-1.png](captures/original-intro-2-acquisition-1.png); the corresponding candidate is [candidate-intro-2-acquisition-1.png](captures/candidate-intro-2-acquisition-1.png). This identifies the rendered element, not the cause of the different pixels. The run did not collect consecutive identical full-frame observations, so this evidence cannot establish that those indicators had settled.

The [earlier run](../../run-38199371948-attempt-1/analysis/README.md) retains its separate 35-pixel intro difference and 570,819-pixel permission-background difference. Those failures are not replaced by this run's measurements.

## Shared fatal exception and observed process replacement

The unchanged [lifecycle.log](lifecycle.log) contains each fatal block followed by a process-death event and a new main-process start at NewHomeScreenActivity:

| Variant | Fatal exception UTC | Old PID | New PID |
| --- | --- | ---: | ---: |
| Original | 2026-10-12 04:11:08.873 | 3947 | 5039 |
| Candidate | 2026-10-12 04:12:40.576 | 5811 | 6498 |

Both fatal blocks report `java.lang.IllegalStateException`, with `Fragment LB{…} not attached to Activity`, then this stack:

```text
at android.app.Fragment.getResources(Fragment.java:785)
at com.zx.lbua80.onShow(Unknown Source:22)
at android.app.Dialog$ListenersHandler.handleMessage(Dialog.java:1500)
at android.os.Handler.dispatchMessage(Handler.java:107)
at android.os.Looper.loopOnce(Looper.java:232)
at android.os.Looper.loop(Looper.java:317)
at android.app.ActivityThread.main(ActivityThread.java:8705)
at java.lang.reflect.Method.invoke(Native Method)
at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:580)
at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:886)
```

The literal fragment instances differ: original `LB{3bdefc2}`, candidate `LB{445de12}`. The unchanged [original fatal block](original-fatal.txt) and [candidate fatal block](candidate-fatal.txt) retain those messages, timestamps, and process IDs. The exception types and all ten stack frames match; literal messages are not claimed to be byte-identical. The independent JSON records exact source-log line numbers and both process lifecycle events.

The first five captures in each run retain their original PID; the final four have the respective new PID, with matching first/final samples within each recorded capture. The evidence therefore shows **post-crash continuation in both APKs**. It does not establish a benign restart, a crash-free run, or that notification denial itself caused the exception. Earlier process-lifetime notes that lacked this log remain unchanged historical findings.

## Observed information-dialog input for the next bounded capture

Both [original](captures/original-trigger-catalog-acquisition-1.png) and [candidate](captures/candidate-trigger-catalog-acquisition-1.png) full images show the same information dialog. Their [original XML](captures/original-trigger-catalog-acquisition-1.xml) and [candidate XML](captures/candidate-trigger-catalog-acquisition-1.xml) are identical. Foreground evidence records `com.arlosoft.macrodroid/.editscreen.EditMacroActivity`.

The title is the enabled TextView `com.arlosoft.macrodroid:id/alertTitle`, text `Favourite Triggers`. The app-owned `android:id/message` contains the exact two-paragraph text in the XML, separated by two newline characters. There is exactly one app-owned `android:id/button1`, text `OK`, class `android.widget.Button`, enabled and clickable, with bounds `[496,780][624,876]`; its center is `(560,828)`.

No OK input was issued in this run. A separate next plan may verify this exact title, message, button role, fresh installed identity, stable PID, and EditMacroActivity; tap that OK once; then record the first resulting app surface and stop. A catalog or any further action must not be inferred from this dialog capture.

## Reproducible evidence

[independent-analysis.json](independent-analysis.json) contains all bindings, nine full-image comparisons, exact input geometry, foreground/PID observations, selectors, and crash records. [analyze_preserved_run.py](analyze_preserved_run.py) verifies the immutable archive and calls only the pure evidence-reading functions in the pinned reviewed source files. It does not install an APK, execute app code, or send an Android command. The `captures/` files are exact copies from the archive. The checkpoint binds every published analysis file.
