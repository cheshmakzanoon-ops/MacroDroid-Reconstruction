# Plugin lookup coroutine recovery

## Inactive original/JVM checkpoint

The Java/D8 replacement for `com.arlosoft.macrodroid.plugins.j.invokeSuspend(Object)` compiles and passes static migration/linkage validation. The expanded original/JVM proof passes **3,053 plugin cases** within **18,476 UI cases across eight methods**, with **zero mismatches and zero unsupported executions**. The UI suite makes **14,552 independent expected-result/state checks**, and all **161 Python tests** pass in this isolated source baseline.

The mandatory coverage gate now passes: the cases visit **198/198 original instructions and 34/34 conditional edges**. They include invalid labels, repeated suspension and resumption, dynamic dependency changes, integer boundaries, injected checked exceptions and errors, and distinct objects that compare equal to the suspension marker. The marker comparisons preserve object identity. All **37 deliberate-fault source anchors** are present and unique, including 15 newly authored plugin controls; execution of those controls and rebuilt/signed-APK proof are still pending. This is an inactive checkpoint, not final application acceptance.

The initial diagnostic is retained in `reports/plugin-initial-two-path.json` and its log. Its 2,047 plugin cases had zero mismatches, but visited only 194/198 instructions and 33/34 edges, so that earlier report correctly has `passed: false`. The first expanded run, before three additional marker-identity cases, is also retained separately. The current report is `reports/java-ui-two-path-parity.json`.

The registry contains 1,240 bodies across 603 original classes. Only the selected compiled body is an APK candidate; test doubles and helper classes are excluded. The original fixture was re-extracted from the unchanged uploaded APK and contains 522,988 bytes, SHA-256 `d2a5e077f11552b462abbe9e10c96a0b1702dca479c8b8d7aeb081ad209d669c`.

The selected original body SHA-256 is `eb4a45092aa01eecae259829e2039400556139fb5bcc56006fef6cd463b743fa`. The existing user-not-allowed, duplicate-package and attempt-limit gates, coroutine labels, repeated status reads, original retry behavior, analytics ordering and narrow exception ranges are retained. The literal original loop repeatedly selects key index 0; it is not repaired in this recovery.

The harness uses controlled dependency responses and observes continuation fields, ordered boundary states, result publication attempts and completions, constructed payload identities, analytics bundles, API arguments, returned marker/Unit identities and exception effects. Explicit sequence cases execute a precheck suspension, an API suspension, and one or more resumptions against the same continuation instance. Mutation cases alter owners, sinks, keys, counters, package names and continuation fields at observed dependency boundaries to distinguish captured references from later reads.

The invalid-label boundary normally throws `IllegalStateException` with the original text. Exactly one case, `plugin-invalid-label-injected-return`, intentionally substitutes a returning `e6d.r` boundary to exercise the original defensive `return null`; it is not a claim that the original guard returns. All ordinary invalid-label cases verify the exception. The analogous scene defensive-return cases retain their previously documented injected-boundary scope.

The harness does not perform a real API/analytics request, run a coroutine scheduler, or establish Android lifecycle behavior. Only VM-generated null/cast exception wording is excluded from comparison. Exception types, boundary order, state effects and observable exception identity remain checked; exact injected/external messages remain checked, including injected `NullPointerException` and `ClassCastException` messages. An exception swallowed by the selected method is verified through its exposed effects rather than an unobservable identity claim.

All work is in a separate isolation based on the frozen 1,239-body scene source. The frozen scene proof and parent current/restored trees are unchanged. See `FOLLOWON_ASSESSMENT.md` for the deferred WidgetUpdateManager subclass-allocation/super-constructor tooling gap.
