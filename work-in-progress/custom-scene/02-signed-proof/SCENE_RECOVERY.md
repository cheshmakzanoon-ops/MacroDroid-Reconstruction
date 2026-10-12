# Custom scene dispatch recovery

## Verified checkpoint

The Java recovery of `CustomSceneAction.W(int, TriggerContextInfo, boolean, Stack, ResumeMacroInfo)` passes **4,070 scene cases** comparing the original selected instructions, recovered Java on the JVM, and rebuilt DEX instructions from the signed APK. The full UI suite passes **15,423 cases across seven methods** with **13,555 independently specified result/state checks**. There are no mismatches or unsupported executions. All **405 original instructions and 40 conditional edges** of the scene method are visited; the runner requires that coverage, with the injected-return qualification described below.

The complete `test.py --three-way` run passes **185,738 cases across all 1,239 registered method bodies**. All **22 UI deliberate-fault controls**, including ten added for scene dispatch, reject their required named cases. The final clean **15,423-case positive restoration** also passes. These are bounded host comparisons; Android scene rendering and whole-application 1-to-1 acceptance remain separate work.

The recovery registry contains **1,239 method bodies across 602 original classes**. This adds one recovered body; the target class already contained registered methods. Only the compiled replacement body is transplanted into its existing class. No helper or test-support class is an APK input, and no preserved smali is modified.

## Recovered implementation

The original method is preserved in `source/smali/classes3/07/CustomSceneAction_07d523cc90d06db2.smali`. Its 1,218 smali lines contain 405 instructions. The replacement is `source/java/recovered/ui/CustomSceneMethods.java`; both `source/ui-methods.json` and `source/java-method-map.json` pin its exact descriptor and original method hash.

The method first checks whether the macro is an action block, re-reads the macro, and marks it as displaying a scene before validating the scene description. Repeated scene-description, scene-configuration, display-option, context and identifier reads retain their original order. Explicit null checks, casts and companion reads remain at their original boundaries. The four dispatch paths are kept separate because their call order, payload keys and exception behavior differ.

| Path | Dispatch and description key | Preserved behavior |
|---|---|---|
| Accessibility overlay | `MacroDroidAccessibilityServiceJellyBean`, `scene_description` | Original `SHOW_SCENE_OVERLAY` action; only Intent construction/configuration/start is inside the `Exception` handler |
| Regular overlay | `SceneOverlayDisplayService`, `sceneDescription` | Original service target, camelCase description key, no action string and no added handler |
| Dialog | Existing scene or `SceneDialogActivity`; new activity reads `SceneBaseActivity.E` | Existing-scene Runnable discriminator 0; dialog companion read and separate display companion check retain their order |
| Full-screen activity | Existing scene or `SceneDisplayActivity`; new activity reads `SceneBaseActivity.E` | Existing-scene Runnable discriminator 1; original display companion capture/check and map lookup |

### Overlay payloads and exception boundaries

Both overlay paths preserve this typed extra order:

1. Description: Parcelable, using the path-specific key above.
2. `MacroGuid`: long.
3. `SelectableItemId`: long.
4. `TriggerContextInfo`: Parcelable.
5. `SkipEndifIndex`: Serializable.
6. `IsTest`: boolean.
7. `resume_macro_info`: Parcelable.
8. `NextActionIndex`: int.
9. `force_not_enabled`: boolean false.

The accessibility path captures its service companion before obtaining the context. It checks the context, reads the description, unboxes the macro GUID, reads the selectable-item ID, and checks the companion and stack before entering the handler range. Only Intent construction, configuration and `startService` are caught. The handler passes the **same caught exception object** to `ku1.A` with the original `Could not show scene overlay: ` prefix. Checked exceptions are caught; `Error` escapes. Failures in the earlier lookups/checks remain outside that handler. The regular overlay path remains unguarded. Both ignore the service return value.

### Permission warning and activity selection

For a non-overlay display, the method checks the application companion, application instance and foreground flag. When the app is not foreground and the overlay-permission boundary rejects the context, it logs the original warning using the action name and macro GUID and invokes the original permission prompt. **This warning falls through into scene selection.** No early return or feature restriction was added.

The method re-reads the scene description and display option to choose dialog or full-screen behavior. Each path captures its original companion, obtains context and identifiers, and reads the description in the original sequence. Dialog dispatch also preserves the separate display companion check before activity-map lookup.

Both paths read the captured description's configured scene name and look it up in the original concurrent activity map. An existing activity is reused only when non-null and neither finishing nor destroyed, with the original short-circuit order. The method constructs the original `eld` Runnable with the exact activity, context, description, trigger, stack and resume identities, long identifiers, boolean, next-action index and path discriminator. It then calls `runOnUiThread`. It does not construct a launch Intent or post a clear event on this reuse path.

For a new activity, it constructs the correct activity Intent, captures/checks the base companion, and reads the description key from the original mutable `SceneBaseActivity.E` field. The activity extra order is description, trigger context, macro GUID, selectable-item ID, stack, resume info, next-action index, test boolean and `force_not_enabled=false`. It adds the original `0x18000000` flags.

The event bus is captured **before** the captured description's configuration and name are re-read. A `ClearSceneByExactNameEvent` is constructed and posted before `startActivity`. The tests observe the captured bus receiver as well as the payload and ordering, including changes made by intervening dependency calls.

## Executed evidence

The original fixture was re-extracted with `ExtractOracle` from the unchanged uploaded APK. It is a test input, not an APK assembly input. All nine candidate DEX partitions were freshly assembled from preserved smali plus registered body replacements in the isolated build.

| Check | Verified result | Evidence |
|---|---|---|
| Full original/JVM/rebuilt comparison | 185,738 cases; 1,239 exact, non-overlapping method keys; 3 paths; 0 failures/unsupported | `reports/java-all-path-parity.json` |
| UI comparison | 15,423 cases; 7 methods; 13,555 independent expected-result/state checks | `reports/java-ui-three-path-parity.json` |
| Scene coverage | 4,070 cases; 405/405 original instructions; 40/40 conditional edges | Scene entries in the UI report |
| Python unit tests | 161 passed | `reports/python-unit-tests.log` |
| Static body validation | 1,239 methods; 574 member references checked; 376 app members resolved; 0 errors/new external refs | `reports/migration-static-proof.json` |
| Invocation/field linkage checks | Passed; 0 errors | `reports/migration-linkage-check.json` |
| Independent hybrid round trip | 71,267 classes and 349,972 methods compared; exactly 1,239 changed bodies in 602 classes | `reports/hybrid-roundtrip.json` |
| Deliberate-fault controls | 22/22 passed, then 15,423 clean positive cases | `reports/ui-negative-controls.json`, `reports/ui-positive-restoration.json` |

The round-trip verifier found no missing/extra classes, baseline-source hash mismatches, unexpected body changes, omitted registered changes, altered opaque payload or alignment failures. Every interpreted rebuilt DEX was checked byte-for-byte against the signed APK. The assembly, compilation, resource, signing and verification logs are retained alongside the reports.

The five host-suite counts are 95,262 legacy, 34,753 core, 30,684 environment, 9,616 engine and 15,423 UI. The reference-failure inventory now records 18 of 42 decompiler failure markers with registered replacements, leaving 24 markers without replacements across the 1,893-file reference tree. This inventory is exact-signature metadata; the reference tree is not a compilable application and the marker count is not a runtime-parity measure.

### Deliberate scene defects rejected

Each mutation is compiled into a temporary host directory, must fail its named case with exit code 2, and must produce zero unsupported executions. No mutated APK is built or distributed. Every control checks that recovery sources, the original fixture and signed APK remain unchanged.

| Control | Failed cases | Required rejected case |
|---|---:|---|
| Return after the permission warning | 549 | `scene:2:2:false:false:0:true:0` |
| Change the accessibility description key | 619 | `scene:1:2:true:true:0:true:0` |
| Change the dialog Runnable discriminator | 144 | `scene:2:2:true:true:1:true:0` |
| Reuse a destroyed activity | 247 | `scene:2:2:true:true:3:true:0` |
| Launch before posting the clear event | 862 | `scene:3:2:true:true:0:true:0` |
| Substitute macro GUID for the long item ID | 609 | `scene:1:2:true:true:0:true:0` |
| Omit the description reread after context lookup | 3 | `scene-description-after-context:1` |
| Narrow the handler to `RuntimeException` | 13 | `scene-fault:accessibility:22:4` |
| Widen the handler to swallow `Error` | 61 | `scene-fault:accessibility:22:3` |
| Hard-code the activity description key | 2 | `scene-dynamic-key-bus:3:0:false` |

The twelve existing drag, selection, serialization and touch-blocking controls also pass. Every complete negative-case report, compilation log and run log is preserved under `reports/`. The positive suite ran again after all 22 mutations and passed all 15,423 cases.

## Test boundaries and qualifications

`tests/java/SceneParityCases.java` observes ordered calls, receiver and argument identities, typed and ordered Intent payloads, raw long identifiers, partial construction effects, ActionBlock state, repeated reads, activity-liveness short-circuiting, queued Runnable fields and event payloads. Cases change dependency results during calls, inject null/cast failures, and inject checked exceptions and errors at observed boundaries. Exception type, escape/catch behavior, call order and partial state effects are compared across original, JVM and rebuilt execution.

**VM-generated exception-message text has a narrow exclusion.** The first original/JVM run found nine differences solely in VM-generated `ClassCastException` text: the interpreter used the offending class name, whereas the JVM included its own class/module/loader wording. That complete diagnostic remains in `reports/scene-first-run-vm-message-diagnostics.json`. The final observation excludes the message wording of VM-generated null/cast exceptions; their exception class, order and partial effects still compare. This exclusion does **not** hide messages or identity of injected boundary exceptions. The exact message and identity of an injected exception are checked even when that exception is a `NullPointerException` or `ClassCastException`. The default `kotlin.UninitializedPropertyAccessException` message is also checked. No recovery-body change was needed to resolve the diagnostic; it identified a host-VM formatting difference, not an application effect.

**Eight coverage cases deliberately let a normally throwing boundary return.** The `j68.h0` dependency normally throws the original uninitialized-property exception. Eight explicitly labeled fault cases let it return so that each following defensive `throw null` instruction can be checked. The JSON flag `customSceneDefensiveNullThrowsUseInjectedReturningLateinitBoundary` records this scope. These cases are injected dependency faults; they do not assert that the original null-guard implementation returns. The 405-instruction coverage result includes these eight cases.

The host boundaries do not deliver Android activities/services, render a scene, execute the dispatched original Runnable body, marshal real Parcel bytes, implement the platform permission APIs or execute event-bus subscribers. Those dependencies remain original APK implementations. The bounded interpreter is not ART, and the linkage check does not prove all Android verifier/API/classloader behavior. This checkpoint establishes the reported body-level comparisons and structural APK checks; it does not establish full Android scene parity or whole-application 1-to-1 acceptance.

## Artifact identity

| Artifact | Size | SHA-256 |
|---|---:|---|
| Original user-uploaded APK | Pinned by extraction provenance | `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800` |
| Original `CustomSceneAction.W` smali method body | 405 instructions | `ce0e77c600d3f6fc6a956b507133969f4f8250b8b2d73171b0d481a496d77bbb` |
| `tests/fixtures/original-methods.dex` | 520,564 bytes | `e2309e0e26b73981349840d93f8ff31f805c9c43c0cdddff368c6f726381aae1` |
| `dist/MacroDroid-5.67.8-v9-hybrid.apk` | 94,683,342 bytes | `be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce` |

`reports/custom-scene-recovery.json` records the verified report identities, source-change manifest and merge boundaries for this checkpoint. The release retains the v9 filename for compatibility with the existing build and acceptance tooling.
