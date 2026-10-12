# Plugin lookup coroutine recovery

## Inactive working checkpoint

The Java/D8 replacement for `com.arlosoft.macrodroid.plugins.j.invokeSuspend(Object)` compiles and passes static migration/linkage validation. The first original/JVM diagnostic executes **2,047 plugin cases** within **17,470 UI cases across eight methods**, with **zero mismatches and zero unsupported executions**. The UI suite makes 14,510 independent expected-result/state checks.

The mandatory coverage gate still fails: this first checkpoint visits **194/198 instructions and 33/34 conditional edges**. The invalid-label branch and its defensive return have not yet been added to the case set. Consequently the first report correctly has `passed: false`; it is not final acceptance. Multi-resume sequences, dynamic dependency changes, additional deliberate-fault controls and rebuilt/signed-APK proof are still in progress.

The registry contains 1,240 bodies across 603 original classes. Only the selected compiled body is an APK candidate; test doubles and helper classes are excluded. The original fixture was re-extracted from the unchanged uploaded APK and contains 522,988 bytes, SHA-256 `d2a5e077f11552b462abbe9e10c96a0b1702dca479c8b8d7aeb081ad209d669c`.

The selected original body SHA-256 is `eb4a45092aa01eecae259829e2039400556139fb5bcc56006fef6cd463b743fa`. The existing user-not-allowed, duplicate-package and attempt-limit gates, coroutine labels, repeated status reads, original retry behavior, analytics ordering and narrow exception ranges are retained. The literal original loop repeatedly selects key index 0; it is not repaired in this recovery.

The harness uses controlled dependency responses and observes continuation fields, ordered boundary states, result publication, constructed payload identities, analytics bundles, API arguments and exception effects. It does not perform a real API/analytics request or run a coroutine scheduler. VM-generated null/cast message wording is excluded; exact injected/external exception messages and identities are retained where observable.

All work is in a separate isolation based on the frozen 1,239-body scene source. The frozen scene proof and parent current/restored trees are unchanged. See `FOLLOWON_ASSESSMENT.md` for the deferred WidgetUpdateManager subclass-allocation/super-constructor tooling gap.
