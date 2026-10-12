# Explicit process-boundary and full-frame observations

The new capture policy is opt-in. The existing thirteen-step `editor_journey.py` and external sixteen-step `supplied_reference_journey.py` plans retain their current action sequences and default initial-PID continuity checks. The external adapter, its tests, `editor-plan.json`, and XML ParseError retry adapter remain byte-identical to the preserved incoming files.

`favourite_info_journey.py` selects a separate ten-screen plan. It preserves the first eight reference steps, records the observed Favourite Triggers information dialog, taps its verified OK button once, records the actual first resulting app surface, and stops. It requires both `--observe-denial-handoff` and `--settle-full-frames`. The workflow uses that entry point and both flags; downloader tests, bootstrap logging, raw lifecycle logging, and artifact preservation from `cada56c8` remain intact.

The reference dependency is pinned to the exact sixteen-step plan from commit `736da1920f7dada1d0c3444032ffcf4eb8759888` (JSON fingerprint `735a31dfda8ed8ebdcf718e5c52f5d5fabd24c608acbd4644e94d13911316b22`). Its first eight steps equal those of the previous fourteen-step plan, so this dependency update leaves the complete ten-screen action sequence unchanged. The previous fourteen-step JSON is preserved as the hash-pinned `fixtures/reviewed-reference-plan14.json` for the historical synthetic verifier controls. It is not installed as the external plan or selected by the workflow. The new observation policy does not implicitly enable the later actions in the external sixteen-step journey. [Checkpoint 01](../../docs/verification/editor-observation-policy/01-observed-device-policy/) remains immutable, inactive evidence of the earlier dependency and host tests.

## What is accepted as a stable observation

For each capture, including the fresh snapshot immediately before an input, the recorder accepts the **first two consecutive observations with identical full PNG bytes and full XML bytes**. Each observation has its own raw files, before/final PID samples, before/final resumed component, and monotonic timestamps. The same single main app PID and component must remain stable across the observations. Every earlier unequal frame/hierarchy and failed acquisition ledger is retained.

There are at most six full-frame attempts within a shared 30-second deadline. The existing adapter may retry only a real XML ParseError, at most three acquisitions, still within the same outer deadline. It does not retry a semantic, identity, or process failure. The input freshness deadline remains 15 seconds and includes diagnostics or installed-APK checks, full-frame acquisition, immediate PID/component checks, and input dispatch. Device-command timeouts preserve any partial stdout/stderr.

No frame is chosen by comparing it with the other APK. The final comparison still includes every pixel, every hierarchy attribute, and PNG color metadata. No screenshot is cropped, masked, recolored, or averaged. A persistent difference or failure to reach stability remains a failure.

The new observation path retains at most four pure PNG decode results, keyed by the complete PNG bytes and decoder function. Identical bytes therefore do not consume the input deadline repeatedly decoding the same image. Each artifact is still read and hash-checked; different or corrupt bytes must go through the decoder, and raw frame equality is unchanged. This cache does not store a selected screenshot or skip a device observation.

## One explicitly observed process boundary

Only the transition from the notification prompt to the observed app-owned LITEAPKS dialog may establish a new PID anchor. The pre-input notification controller, unique denial button, and prior live PID are verified. After the first stable resulting app capture, independent commands record:

- A single live main app PID before and after the boundary checks.
- Two complete `ps -A -o PID,NAME` listings containing PID 1, the expected sole main app process, and no old PID anywhere if replacement is claimed.
- A fresh package path and SHA-256 matching the exact installed APK from this run.
- NewHomeScreenActivity as the resumed component.
- Raw process and Java crash diagnostics before and after the boundary, without clearing a log buffer.

The seven identity commands and diagnostics must be fresh, ordered, independently stored, and completed within 30 seconds. Subsequent captures and inputs retain the new anchor; another restart or a PID change inside an input guard still fails. The paired comparison includes whether each APK replaced its PID, so different lifecycle outcomes cannot become an image-only match. The primary [Toybox ps source](https://android.googlesource.com/platform/external/toybox/+/08dc20ad276251f61a9a4036f9d17ee601a4b3a0/toys/posix/ps.c) documents the all-process selection and PID/NAME fields used here.

## Crash evidence is part of the outcome

The [actual run 38202401351](../../docs/verification/editor-journey/run-38202401351-attempt-1/) recorded a `java.lang.IllegalStateException` in both APKs: the LB fragment was detached when `com.zx.lbua80.onShow` called `Fragment.getResources`. Both original processes died, and both continued in new main processes. The new classifier recognizes only that exact observed exception shape and ten-frame stack in a new fatal block for the old PID. An unexpected new fatal stack fails closed for review. The full raw logs, literal exception messages, fragment instances, timestamps, and PIDs remain in the evidence.

Comparable crash outcomes contain the recorded exception type, message shape, and exact stack. Runtime fragment instance IDs are preserved in the literal blocks; their equality is not claimed. A fatal block already present before the input is not classified as newly observed. An empty or unavailable Java crash buffer never proves that a run was crash-free.

If every full capture and paired lifecycle outcome matches after the known shared crash, the result is `MATCHED_POST_CRASH_CONTINUATION_ONLY`. It is not a crash-free result, nor a claim of complete runtime or feature parity. A pixel difference continues to produce `JOURNEY_DIFFERENCE`, including when both crashes match.

## Favourite Triggers is a separate final observation

The new adapter requires the exact observed app-owned Favourite Triggers title, two-paragraph message, and unique enabled/clickable `android:id/button1` with text `OK` and Button class. It verifies EditMacroActivity before and after the fresh snapshot, and checks the actual installed APK path/hash before the snapshot, inside the same 15-second input deadline. A fresh PID and resumed-component check immediately precede the one tap. Geometry is computed from the observed button bounds, never a hard-coded input coordinate.

The final surface is captured in full, with stable process and component observations. Its actual component must match between the APKs for a matching result. No assumed Add Trigger selector or subsequent catalog action is inserted. Unexpected ownership, a changed process, or unstable frames preserve the raw evidence and fail the capture.

## Verification and limits

Host tests exercise the actual recorder/input paths with a virtual ADB, the complete legacy verifier suites, synthetic positive and rejection cases, and exact observed XML/PNG/crash fixtures. They do not establish an Android result. The new device policy and the single OK input remain pending until a hosted run supplies their actual evidence. The preserved 26-pixel page-dot difference, prior intro differences, prior permission-background difference, and recorded crashes remain failures within their original measured scopes.
