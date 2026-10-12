# Widget method: compiled deliberate-fault controls

## Measured result

All **24 deliberately altered Java method bodies were compiled and rejected** by the fixed original/JVM comparison. Every mutant ran the complete **2,342-case** Widget suite against the unchanged, original-APK-derived one-method DEX. Every run retained **194/194 original instructions and 20/20 conditional edges**, zero unsupported executions and zero failures among the 198 independent expectations applied to the original path. Each mutant exited with code 2 and rejected its catalogued case labels.

The positive helper passed before the mutations and was freshly compiled again afterward. Its restored source SHA-256 is `dbcb1a98d25ae4637531644da37d24f6e1bc494f941d4212da03c360fe315d79`; its restored class SHA-256 is `ac0e6d32c3ef3b54435f5028071cfa4524b20358dfe2cc48debde13ff108ab7e`. Both match the frozen positive inputs exactly. The complete restored parity JSON matches the frozen 2,342-case positive report. The original fixture, every fixed class and all frozen source files remained unchanged.

This evidence is a **single-method, two-path host comparison**. These are 24 controls over the same 2,342 cases, not 24 new application methods or additional independent case families. The runner builds no APK and does not execute ART, an Android widget service, rendering, coroutine scheduling or application lifecycle. The parent's signed Widget integration and separate constructor ART probe have their own reports.

## What was deliberately changed

Each control changes only the recovered `WidgetUpdateMethods.update` helper. The exact source substitutions and required failure labels are declared in `widget_method_mutants.json`. Anchor counts are checked against the pinned source before every compile. Original DEX, oracle, fixtures, host boundaries, independent expectations and comparison code are fixed.

| Compiled fault | Rejected cases | Required named failures |
| --- | ---: | --- |
| `reuse-requires-high-bit` | 734 | `widget-no-high-bit-creates-new:1`, `widget-entry:3:false` |
| `reuse-clears-high-bit` | 725 | `widget-entry:3:false`, `widget-two-suspensions` |
| `first-suspension-label` | 1556 | `widget-flow:1:0`, `widget-two-suspensions` |
| `second-suspension-label` | 1454 | `widget-flow:0:1`, `widget-two-suspensions` |
| `retain-label-two-dead-identifier-cast` | 1 | `widget-saved-cast:2:7:true` |
| `retain-dead-list-casts` | 2 | `widget-saved-cast:1:1:true`, `widget-saved-cast:2:1:true` |
| `leave-saved-L6-unread` | 707 | `widget-saved-unread-L6:1`, `widget-saved-unread-L6:2` |
| `saved-index-does-not-increment` | 1652 | `widget-resumed-index-never-increments`, `widget-multiple-widgets-four-suspensions` |
| `restore-saved-phase` | 273 | `widget-saved-integers:-1:37`, `widget-saved-integers:-2147483648:2147483647` |
| `second-call-clears-saved-identifier` | 1453 | `widget-resumed-result:1:0`, `widget-flow:0:1` |
| `second-label-precedes-call` | 1454 | `widget-flow:0:1`, `widget-flow:0:3` |
| `factory-precedes-state-publication` | 1563 | `widget-factory-before-state-clear` |
| `factory-arity-is-two` | 1603 | `widget-factory-arity-and-null-completion` |
| `catch-includes-checked-exception` | 736 | `widget-checked-failure-inside-handler:widget.first:`, `widget-checked-failure-inside-handler:widget.second:` |
| `catch-excludes-error` | 84 | `widget-flow:4:0`, `widget-suspended-failure:2:4` |
| `logger-failure-escapes` | 31 | `widget-logger-failure-escapes` |
| `message-accessor-read-once` | 661 | `widget-flow:3:0`, `widget-flow:0:3` |
| `first-suspension-uses-identity` | 9 | `widget-first-result-uses-identity` |
| `second-suspension-uses-identity` | 6 | `widget-second-result-uses-identity` |
| `has-next-remains-outside-handler` | 136 | `widget-checked-failure-outside-handler:iterator.hasNext:` |
| `iterator-next-remains-outside-handler` | 94 | `widget-checked-failure-outside-handler:iterator.next:` |
| `invalid-provider-continues-iteration` | 789 | `widget-invalid-provider-continues` |
| `initial-result-remains-outside-handler` | 39 | `widget-checked-failure-outside-handler:coroutine.result:` |
| `resume-locals-captured-before-result-validation` | 5 | `widget-resume-captured-fields:1` |

The low failure counts for the unused casts are useful: removing the label-2 identifier cast fails precisely its malformed saved-field case, and removing both saved-list casts fails the two corresponding cases. This demonstrates that otherwise unused original operations remain observable and tested. Larger failure counts reflect state or event-order changes affecting many inputs; they are not separate proof counts.

Suspension identity controls use a distinct object that reports equality with the marker. Constructor controls change the actual arity supplied to the compiled host adapter; the fixed original path continues to validate its exact method-scoped `Lzhh` allocation and `Lrff` constructor owner. Handler controls distinguish checked `Exception`, `Error`, logger failure and failures outside the per-widget handler. The restored-phase, saved-index, publication-order and captured-local controls observe continuation state at the controlled boundary where it matters.

## Loaded-class and restoration checks

`WidgetMutationLauncher` verifies the actual loaded class resource path and SHA-256 for the target helper, oracle, UI comparison, Widget cases/study and selected constructor/API boundaries before invoking the suite. Each mutation compiles to exactly one class, which is placed ahead of the fixed positive classes. Its class bytes must differ from the positive helper. The fixed compiled class inventory is checked again after the complete control run.

Two additional launcher controls deliberately supply a wrong expected helper hash or expect a mutant while the positive helper is first on the actual classpath. Both executions fail with code 1 before any parity report is written. They are loader-gate controls, not Widget behavior cases. Their actual logs and return codes are retained.

Positive restoration recompiles the exact frozen source into another fresh directory, verifies its class hash against the original positive class, runs the complete original/JVM suite and compares the whole resulting JSON with the frozen positive report. The runner does not treat a saved prior result as restoration.

## Evidence and comparison limits

The complete run is `reports/widget-method-mutants-04-initial/`. It contains exact command arguments, return codes, bounded timeouts, command logs and hashes; every compiled mutant source/class; original DEX; fixed class archive and inventory; actual class-origin observations; full parity reports; the two loader rejections; and positive runs before and after mutation. The run passed on its first execution. The name retains its initial-run provenance.

Parity reports retain all failed case labels and the first 80 detailed original/JVM failure observations, following the existing UI harness bound. The control gate checks every required label against the complete label set. It does not claim that every failed case has a separately saved raw observation pair.

The exact exception-message scope remains the frozen positive scope documented in `WIDGET_HARNESS.md`. The runner does not broaden it. The single recognized VM-generated logged null-receiver difference still preserves both raw messages; injected/external messages stay exact, and the two normalization guard cases execute in every complete suite. Exception type, ordered calls, partial state and exposed injected/external identities remain compared. The one injected invalid-label return case retains its explicit defensive-return coverage scope.

The positive source/evidence dependency is `checkpoints/04-original-jvm/checkpoint.json`, SHA-256 `c448b645b27f98918fab3369d9b72a408a0a16cab217f8684f2733247b6a8b1b`. The runner requires that exact checkpoint and its verified final compiled class archive. The original one-method fixture is SHA-256 `21fa3b34730a902713b14ee8ada375d4fdca3edf481dc3caabcd7bd1d3f22a0a`. All generated mutant folders are private and no frozen positive file is overwritten.

## Reproduction

Provide the frozen positive checkpoint with its evidence archive extracted under `evidence/`, the same pinned tool JAR, Java 21 and a new output directory:

```sh
python3 widget_method_negative_control.py \
  --positive-checkpoint /path/to/04-original-jvm \
  --tool-jar /path/to/jadx-r2721.4574686-all.jar \
  --jdk /path/to/jdk21 \
  --output /path/to/new-widget-mutant-report-directory
```

The runner refuses an existing output directory, checks all source and archive identities, verifies each actual loaded class, and fails the overall gate for compile errors, timeouts, missing reports, unsupported instructions, missed named failures, changed original coverage or unsuccessful exact restoration.
