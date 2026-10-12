# Process lifetime finding after notification denial

The preserved Android captures show a process-ID change between the notification permission surface and the supplied reference's promotion/home surface. This occurs in both the supplied original and the rebuilt APK, not just in a reconstructed candidate.

| Preserved run | Variant | PID at notification surface | PID at next captured surface |
| --- | --- | ---: | ---: |
| 38198783416 | original | 4129 | 5081 |
| 38198783416 | candidate | 5597 | 6260 |
| 38199371948 | original | 4062 | 4985 |
| 38199371948 | candidate | 5545 | 6288 |
| 38200622944 | original | 3953 | 4960 |

These numbers were read from the captured PID artifacts referenced by `journey.json` and, for the last incomplete acquisition, `original-reference-promotion-snapshot.json`. The complete raw archives are committed in each corresponding `run-<id>-attempt-1/` directory. Each snapshot separately retained first and final PID observations; this table concerns the boundary between two different snapshots.

## Exact scope

A changed PID establishes that the observed main process identity is different. It does **not**, by itself, establish whether the cause was an application crash, deliberate restart, framework-driven restart, or another lifecycle event. The test must not call it a reconstruction-only regression because the original reference also exhibited the change.

The current strict whole-journey verifier requires continuity from the first introduction-page PID. It therefore cannot certify a completed journey spanning this boundary merely because subsequent screenshots are available. The failed and incomplete runs remain failed; no PID comparison, screenshot area or UI attribute has been masked or ignored to manufacture a pass.

In run 38200622944, UI Automator additionally reported `ERROR: null root node returned by UiTestAutomationBridge.` The following `cat` returned a missing-file message rather than XML. That acquisition error interrupted reporting with an XML parser exception. The committed bounded acquisition-retry adapter preserves the failed raw observation, attempts a fresh dump at most three times and converts exhaustion into a handled journey rejection. It does not retry or suppress semantic/PID failures.

## Required diagnostic follow-through

Collect process/crash evidence around the same user action for both APKs before deciding whether this is an expected lifecycle boundary or a crash that needs remediation. The current CI now preserves the crash buffer on exit. A separately scoped post-introduction editor journey can be useful, but must name its starting state explicitly and must not retroactively relabel failed cold-start/onboarding runs as passing. Immediate pre-input process and foreground checks must remain enforced even if a future, evidence-supported cross-phase lifecycle transition is modeled.

No whole-app 1:1 runtime claim follows from this finding.
