# Widget update method: original/JVM harness proof

## Measured result and exact scope

The isolated study of `com.arlosoft.macrodroid.widget.custom.WidgetUpdateManager.m(Context, List, o73)` passes **2,342 original/JVM cases**, with **zero failed cases, zero unsupported executions and 198 independent expected-result/state checks**. It visits **194/194 original instructions and 20/20 conditional edges**. Both coverage measures are hard gates. The exact final command results, source hashes, original fixture and complete observations are in `reports/widget-study-04-final/`.

This is a **single-method, two-path host result**. The Widget body is not registered in the active project. No application APK was assembled by this study, no rebuilt Widget body was compared, and no Android widget service, renderer, coroutine scheduler or lifecycle was executed. Parent-owned D8/static/linkage/constructor-owner integration, the separate ART constructor probe, signed application proof and full application acceptance have their own evidence. They must not be inferred from this host result.

The exact final helper is 6,169 bytes, SHA-256 `dbcb1a98d25ae4637531644da37d24f6e1bc494f941d4212da03c360fe315d79`. The oracle is SHA-256 `d91ddcd8ec3d67d41d69b8252835e747c2cad2c6d5ea898323794ceec30e6b56`. The standalone runner copied and hash-checked all 802 host Java inputs, including the 18 Widget overlays, plus the harness and extraction tool inputs into a fresh private directory. Mutable inputs were not hardlinked and active project files were not changed.

## Original fixture and constructor adaptation

The selected key is:

```text
Lcom/arlosoft/macrodroid/widget/custom/WidgetUpdateManager;->m(Landroid/content/Context;Ljava/util/List;Lo73;)Ljava/lang/Object;
```

Its preserved source is `source/smali/classes/67/WidgetUpdateManager_6791e8994482f6df.smali`, with original class SHA-256 `3ad59b363eaf1f1816d31a951867dcbf202702152148f6404d3426a8ed68818d` and method SHA-256 `a1dd490bbfd6837fa72e6bf8ae4c75736612989fcba050fe2f0582aa03640e34`. The runner checks the class index, class hash and exact method body hash before running the study.

The test fixture was freshly extracted from the unchanged uploaded APK, SHA-256 `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`. The fixture contains exactly this one method in one class. It is **4,220 bytes**, SHA-256 `21fa3b34730a902713b14ee8ada375d4fdca3edf481dc3caabcd7bd1d3f22a0a`. The fixture retains the original `new-instance Lzhh;` followed by `Lrff;-><init>(ILm73;)V`. It is a test input, never an application build input.

Before any original instruction runs, `WidgetParityCases.configure` checks that the proposed entry has exactly the expected allocation, original constructor owner, descriptor and occurrence count. It calls the oracle's explicit method-scoped adapter validator. The oracle checks the selected DEX method, concrete child/direct parent relationship, constructor parameters and exact occurrence count. Unconfigured constructor-owner mismatches continue to fail closed. Host reflection uses the compile-only child constructor adapter; this does not prove ART constructor legality or add a constructor to the APK.

The first study correctly rejected the unsupported three-register `AND_INT` used by the continuation high-bit check. The parent added that single opcode and separately validated 4,546 numeric cases and all 16 constructor-owner guard controls. Those parent conformance results are separate from the 2,342 Widget case count. The Widget suite continues to use the same strict constructor guards.

## Behavior observed by the harness

The entry matrix covers null and unrelated completions, existing continuations with and without the high bit, all three supported labels, invalid labels, empty and nonempty lists, and forced `isEmpty` outcomes. The high bit is cleared only for a reused continuation. A continuation without the high bit causes a new continuation to be constructed with the supplied owner and completion. The incoming result and saved fields on that unused continuation are ignored.

For restored labels 1 and 2, the harness checks all saved cast positions, including otherwise unused identifier, iterable and list casts. Wrong types escape before guarded resumed work. Null values that pass a cast retain their original subsequent behavior. `L$6` is not restored; explicit cases supply an arbitrary object there. Continuation snapshots expose all eight object slots, all three integer slots, label, result, owner and completion at every controlled boundary and after each explicit resume.

The iteration cases observe `List.isEmpty`, `Iterable.iterator`, `Iterator.hasNext`, `Iterator.next` and `Number.intValue` in order. Custom numbers, signed integer limits, floating-point narrowing, invalid/null elements and list mutation cases preserve the original call and conversion behavior. Initial result validation, initialization, manager/renderer construction and iterator operations remain outside the per-widget handler. Invalid provider information creates the original error text and continues to later widget IDs.

Construction observations include manager context/backend identity, renderer identity, widget identifier value, factory class, arity 2 and null completion. The two suspension calls record receiver, context, identifier, factory, continuation identity and a complete state snapshot before their controlled boundary executes. The code must clear/save the original fields and set the correct label before each call. Tests separately verify the unchanged saved index, restored phase, literal fresh phase zero, and the distinction between captured locals and later mutation of continuation fields.

Fresh and resumed flows distinguish ordinary returns, null, integer values, a Throwable returned as a value, wrapped failures, suspension markers and a distinct object that compares equal to the marker. Suspension depends on identity. Fresh non-suspended return values are ignored. Explicit sequences suspend at both calls for one widget and at all four calls for two widgets, then resume the same continuation. Sequence preconditions reject an attempt to resume a call that already completed.

Boundary fault matrices inject state/null/cast/security/argument exceptions, checked I/O exceptions and `AssertionError`. `Exception` is caught only within the original handler regions; `Error` escapes. Explicit expectations check checked failures both inside and outside the handler, invalid-provider continuation, constructor failure before state publication, logger failure escape, and failure from an exception's message accessor. Controlled message accessors record how often they are read. Logging remains outside the handler, after the message read; a logger failure must escape rather than be caught again.

Mutation matrices change continuation labels/slots, backend references, provider maps, list contents, saved results and suspension-return plans at observed boundaries. The comparison records partial construction effects, attempted API calls, iterator position, initialized owners, messages, state snapshots and exposed exception identities. The harness uses independent expectations for important transitions in addition to original/JVM equality.

## Exception-message comparison limits

Exception classes, catch/escape behavior, ordered calls, partial state and observable injected/external exception identity compare. Injected/external messages remain exact, including injected NPE and CCE text. Generated escaped null/cast wording is excluded because the original instructions use host reflection while the recovered body runs directly on the JVM.

There is one additional, narrowly identified **logged** message exclusion: `widget-saved-cast:1:3:false` deliberately supplies a null saved renderer. Reflection generates an NPE message about `Object.getClass()/obj`; direct javac execution generates a message about `rx6.d/<local13>`. Both paths log the same widget ID and prefix, return the same result and preserve the same calls and state. Only those recognized generated null-receiver suffixes are normalized for comparison in this single fixture. Unknown wording is retained in the comparison. The complete raw pair is preserved in the final report's `generatedNullMessageExclusions` and in the earlier, correctly failing expanded study.

The exclusion is disabled whenever an injected or external exception is present. Two explicit cases use injected NPE/CCE messages identical to the generated text and require the exact original messages to remain. There is no generic log normalization and no exclusion of injected exception text.

Exactly one separate case, `widget-invalid-label-injected-return`, makes the invalid-resume guard return so the original defensive return-null instruction can be visited. It does not claim that the ordinary guard returns. Normal invalid labels must throw the original `IllegalStateException` with its exact message.

## Preserved progress and remaining gates

| Study | Cases | Failed | Unsupported | Instructions | Conditional edges | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `widget-study-04-initial` | 1,710 | 120 | 125 | 136/194 | 16/20 | Failed closed on unsupported AND_INT; exact initial sources retained |
| `widget-study-04-expanded` | 2,340 | 1 | 0 | 194/194 | 20/20 | Failed on the raw generated null-receiver message difference |
| `widget-study-04-original-jvm` | 2,342 | 0 | 0 | 194/194 | 20/20 | Passed with the intermediate a075 helper and exact message controls |
| `widget-study-04-final` | 2,342 | 0 | 0 | 194/194 | 20/20 | Passed with the final dbcb helper and d91 oracle |

The final helper makes the original `rx6.d`, `Iterable.iterator` and `Throwable.getMessage` owners explicit through safe upcasts. Every caught message is read before allocating `StringBuilder(prefix)` and appending the widget ID, separator and message. This source-order refinement is retained alongside the initial and intermediate source hashes. The harness does not inject allocation failure into JDK StringBuilder or claim exhaustive resource-failure equivalence.

Method-only deliberate-fault execution and exact positive restoration are the next separate checkpoint. Signed rebuilt Widget comparison, static/linkage checks, D8 constructor-owner restoration and whole-application/runtime gates remain parent-owned work. Full instruction and branch-edge coverage is bounded evidence, not exhaustive input/path coverage.

## Reproduction

From this standalone study directory, use a new output path:

```sh
python3 widget_original_jvm_study.py \
  --project /path/to/MacroDroid_v9 \
  --original-apk /path/to/original.apk \
  --jdk /path/to/jdk21 \
  --output /path/to/new-widget-report-directory
```

The runner refuses an existing output directory, pins the uploaded APK and original method, captures exact argv/return codes/timeouts/logs, and preserves failed gates. It creates no active migration registry entry. `WidgetParityStudy` calls the same case and comparison code that the narrow `UiParityTests` integration will use after the parent registers the method.
