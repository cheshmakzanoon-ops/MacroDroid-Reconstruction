# Fresh rerun after the session-wide evidence fix

Run **38208764356**, source commit **`47458097056fd023bad8b47b6464978b0d02e85c`**, executed the corrected verifier on a fresh disposable Android environment. **This new paired session did not pass.** The original and candidate raw artifacts and unmodified reports are already committed at `../editor-journey/run-38208764356-attempt-1/`.

## Actual outcome

| Variant | Recorded progress | Recorder outcome |
| --- | --- | --- |
| Supplied original | Five screens through the notification request; five input transitions recorded | FAILED while acquiring the reference-promotion surface: `Device command failed: ['pidof', 'com.arlosoft.macrodroid']` |
| Rebuilt candidate | All 16 screens and 15 transitions through the final return to the editor | COMPLETE; before/after environment dictionaries unchanged |

The paired editor replay correctly reports **REJECTED**, reason `Incomplete run or changed environment`. Because the reference sequence is incomplete, this run establishes no paired editor-screen equality, even though the candidate continued through its sequence. The six download transport tests and **105 parity-tool host tests passed**; the latter completed in 29.775 seconds on the runner. Passing host tests are not a substitute for the missing paired Android observation.

The exact `ci-editor/lifecycle.log` records the same promotion-dialog exception in both APKs:

```text
java.lang.IllegalStateException: Fragment LB{...} not attached to Activity
    at android.app.Fragment.getResources(Fragment.java:785)
    at com.zx.lbua80.onShow(Unknown Source:22)
```

The two captured fatal events use PIDs 4077 and 5434. The raw log preserves each actual fragment identity and timestamp. The reference capture happened during the process-loss interval, so it failed its live-process check rather than acquiring a later restarted screen. This is not evidence that only the reconstruction crashes. No delay, crop, permission change, screenshot substitution or ignored PID was used to turn the run green.

## Exact identities and independent archive check

The original reference SHA-256 remains `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`. The candidate SHA-256 remains `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`.

The GitHub artifact has **7,835,649 bytes**, SHA-256 **`a1ab0fe1f622e591eba1d41b80297b9593abcad76963ef5c46097a499aa1c72f`**. A read-only local check reproduced the API digest and verified ZIP CRCs for all **1,408 members**. The exact `journey.json` SHA-256 is `85e2eb9802e37423e5881a909fce08ee5725aa6c1ce94ec743687fbda463f223`.

## Relationship to the earlier successful editor measurement

The earlier run **38206460588** did capture both completed editor sessions. All ten full 720 x 1280 image pairs and full XML pairs match exactly. Its unchanged archive was subsequently replayed through the corrected verifier: **294 distinct observation files, zero evidence reuse, and ten exact screen pairs**. That completed read-only result is [runtime-replay.json](runtime-replay.json); its precise scope and synthetic guard controls are in [README.md](README.md).

These are two separate measurements. The earlier result remains an exact match for its observed post-onboarding session. The fresh incomplete run remains failed. Neither establishes reliable uninterrupted onboarding, macro saving/execution, scheduling, persistence, external integrations, animation behavior, physical-device behavior, or whole-app 1:1 parity. The supplied APK includes a third-party promotion and is not an independently authenticated publisher release.
