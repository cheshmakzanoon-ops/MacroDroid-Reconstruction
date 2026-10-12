# Custom scene dispatch recovery

## Checkpoint status

The Java recovery of `CustomSceneAction.W(int, TriggerContextInfo, boolean, Stack, ResumeMacroInfo)` compiles through Java and D8. Its first completed original-instruction/JVM comparison passes **4,070 scene cases**, within **15,423 UI cases across seven methods**, with no mismatches or unsupported executions. The UI suite makes **13,555 independent expected-result/state checks** in addition to differential comparisons. This checkpoint has not yet completed rebuilt-APK comparison or its new deliberate-fault controls.

The recovery registry contains **1,239 method bodies across 602 original classes**. This adds one recovered body; the target class already contained registered methods. No helper or test-support class is an APK input, and no preserved smali is modified.

## Behavior retained

The method chooses among the accessibility overlay, regular overlay service, dialog activity, and full-screen activity. It preserves the repeated macro, scene configuration, context and identifier lookups, including their null checks and original order. Action blocks enter the displaying-scene state before scene validation. The background/overlay-permission warning logs and prompts, then continues into display selection.

Activity display looks up the scene name in the original concurrent activity map. It reuses a present activity only when the original short-circuit checks find it neither finishing nor destroyed. The original Runnable constructor retains its distinct dialog/full-screen discriminator and exact argument identities. New activities receive the original typed extras and flags; the clear-by-exact-name event is constructed and posted before launch. Accessibility overlay construction/start alone has the original narrow `Exception` handler; errors and all failures outside that range propagate.

## Evidence and limits

The test-only original fixture is re-extracted from the unchanged user-uploaded APK using `ExtractOracle`. The preserved original method contains **405 instructions and 40 conditional edges**, all visited by the bounded host suite. Its source-body SHA-256 is `ce0e77c600d3f6fc6a956b507133969f4f8250b8b2d73171b0d481a496d77bbb`.

The tests observe ordered calls, typed and ordered Intent payloads, partial construction effects, state changes, exact object identities, long identifiers, activity-liveness short-circuiting, null/cast failures, dependency-result changes, and injected checked exceptions and errors. VM-generated null/cast exception text is not an equality claim; exception class, ordering and partial effects are compared. External exception messages and injected exception identities are compared where applicable.

The `j68.h0` dependency normally throws the original uninitialized-property exception. Eight explicitly labeled fault cases let this boundary return so that each defensive `throw null` instruction can also be checked. These injected-return cases are identified in the JSON coverage report. They do not assert that the original null-guard implementation returns.

Android activity/service delivery, scene rendering, the dispatched Runnable body, actual permission APIs, event-bus subscribers and real Parcel encoding remain external dependencies. The host comparison provides bounded evidence for the selected method body; it is not full Android scene parity or whole-application 1-to-1 acceptance.
