# Bounded notification readiness before the unchanged full-frame capture

## Concrete reason for this change

The retained DayTime13 run `38221713675`, from commit `e610d98812f3d26da732035e039a1250b8afe9f3`, failed on the original at the first promotion acquisition. Its `pidof` returned exit 1 with empty stdout and stderr after the original main process emitted the recorded Fragment-not-attached exception. That acquisition lasted 0.0626 seconds, had no valid frames, and remains failed. The candidate later supplied the existing strict post-crash continuation evidence and reached an exact-alarm permission explanation. The thirteen-screen pair remains incomplete.

This proposal adds a separate, explicit phase between the notification denial and the first promotion capture. It observes the process and foreground component for a bounded interval. It records absence and replacement as lifecycle observations. They are not frames, and receive no frame-stability or process-continuity credit. No historical capture is retried or reclassified.

## Fixed contract

- Opt in using `--observe-notification-readiness`, together with the existing denial-handoff and full-frame switches.
- Use the exact thirteen-screen plan `42ece5a06a280186ddf9796a4524975d478263e545260674e2b1b4cf718d46fb`. No input or surface is added.
- Use report schema 5, with a complete fixed policy and exactly one readiness artifact for each run's notification-denial transition. Schema 2/3 evidence cannot carry this new artifact or policy. The new workflow must explicitly require schema 5 so removing the new proof cannot downgrade that workflow's evidence contract.
- Run only after the existing two-second post-input wait and before promotion full-frame acquisition. There are at most 16 observations within 10 seconds, separated by 0.25-second requested sleeps. The existing recorder deadline bounds each command.
- In each observation, read `pidof com.arlosoft.macrodroid`. Exact exit 1 with empty stdout and stderr means no main PID. Otherwise require successful output with exactly one positive PID. For a present PID, read `dumpsys activity activities`, then a second `pidof`.
- Only the already observed permission component or the home component is permitted. Reject malformed output, command errors, unknown or ambiguous components, and timeouts. A missing second PID or a changed PID resets the ready sequence.
- A ready observation has the same single PID before and after the exact home component. Accept the first contiguous ready sequence for the same PID with at least two observations spanning at least 1.05 seconds. A bounded wait which never meets that rule remains failed.
- Retain every command, output, monotonic interval, requested inter-observation sleep, recomputed state, failed phase, and accepted sequence. Failed command attempts remain in the global command ledger and in the partial phase record.

## Evidence binding

Replay must recompute all observation states from the raw command outputs. It must bind each command to one unique complete global-ledger entry in the correct order; raw output paths and physical files cannot be reused across this phase or another evidence role. Readiness begins after the recorded input completes and ends before the first promotion acquisition. Its final ready PID must equal the promotion observation PID.

The existing full-frame capture, first-identical-pair rule, pixel and XML equality, input identity, process checks, and post-capture crash/installed-APK handoff checks remain active. A process gap or change during full-frame acquisition still fails immediately. Readiness does not establish crash-free startup or continuous process identity across notification denial.

## Validation and rollout

Before activation, run deterministic host fixtures for valid absence/replacement and ongoing-process paths, plus raw-output, command-order, timing, schema, policy, provenance and missing-proof faults. Replay the retained actual failed DayTime13 evidence and complete Zero12 five-pixel failure with the new guard: both must preserve their exact prior verdicts. Run the full existing host suite. Keep all attempts and corrections.

After independent review, publish a separate workflow with unchanged APK identities and all three animation scales zero. Keep the previous twelve- and thirteen-screen workflows unchanged. The next device result must satisfy the same complete thirteen-screen and zero-pixel contract. Permission-dialog interaction remains a subsequent step.
