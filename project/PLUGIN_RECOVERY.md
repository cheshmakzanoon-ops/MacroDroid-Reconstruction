# Plugin lookup coroutine recovery

## Completed isolated signed proof and deliberate-fault gate

The Java/D8 replacement for `com.arlosoft.macrodroid.plugins.j.invokeSuspend(Object)` compiles and passes static migration/linkage validation. The signed original/JVM/rebuilt proof passes **3,053 plugin cases** within **18,476 UI cases across eight methods**, with **zero mismatches and zero unsupported executions**. The UI suite makes **14,552 independent expected-result/state checks**, and all **161 Python tests** pass in this isolated source baseline. Across all five suites, **188,791 cases cover exactly all 1,240 registered method bodies**, without duplicate or omitted method keys.

The mandatory coverage gate passes: the cases visit **198/198 original instructions and 34/34 conditional edges**. They include invalid labels, repeated suspension and resumption, dynamic dependency changes, integer boundaries, injected checked exceptions and errors, and distinct objects that compare equal to the suspension marker. The marker comparisons preserve object identity. All **37 deliberate-fault controls pass**, including the 15 new plugin controls: every defect rejects its required named case, exits with the required behavioral-failure status and produces zero unsupported executions. The final unmodified **18,476-case three-path restoration passes** with zero mismatches and unchanged source, fixture and signed APK hashes. This completed isolated checkpoint is awaiting the parent's combined application acceptance.

The initial diagnostic is retained in `reports/plugin-initial-two-path.json` and its log. Its 2,047 plugin cases had zero mismatches, but visited only 194/198 instructions and 33/34 edges, so that earlier report correctly has `passed: false`. The first expanded run, before three additional marker-identity cases, is also retained separately. The current signed report is `reports/java-ui-three-path-parity.json`, aggregated by `reports/java-all-path-parity.json`.

The signed APK contains **94,683,497 bytes**, SHA-256 `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`. Its v1/v2/v3 signatures verify. All nine rebuilt DEX partitions match the signed APK bytes. An independent disassembly/roundtrip compares **71,267 classes and 349,972 methods**, finds exactly **1,240 changed bodies across 603 classes**, and reports no omitted/unregistered changes, missing/extra classes, altered baseline source, opaque payload changes or alignment failures.

The registry contains 1,240 bodies across 603 original classes. Only the selected compiled body is an APK candidate; test doubles and helper classes are excluded. The original fixture was re-extracted from the unchanged uploaded APK and contains 522,988 bytes, SHA-256 `d2a5e077f11552b462abbe9e10c96a0b1702dca479c8b8d7aeb081ad209d669c`.

The selected original body SHA-256 is `eb4a45092aa01eecae259829e2039400556139fb5bcc56006fef6cd463b743fa`. The existing user-not-allowed, duplicate-package and attempt-limit gates, coroutine labels, repeated status reads, original retry behavior, analytics ordering and narrow exception ranges are retained. The literal original loop repeatedly selects key index 0; it is not repaired in this recovery.

The harness uses controlled dependency responses and observes continuation fields, ordered boundary states, result publication attempts and completions, constructed payload identities, analytics bundles, API arguments, returned marker/Unit identities and exception effects. Explicit sequence cases execute a precheck suspension, an API suspension, and one or more resumptions against the same continuation instance. Mutation cases alter owners, sinks, keys, counters, package names and continuation fields at observed dependency boundaries to distinguish captured references from later reads.

The invalid-label boundary normally throws `IllegalStateException` with the original text. Exactly one case, `plugin-invalid-label-injected-return`, intentionally substitutes a returning `e6d.r` boundary to exercise the original defensive `return null`; it is not a claim that the original guard returns. All ordinary invalid-label cases verify the exception. The analogous scene defensive-return cases retain their previously documented injected-boundary scope.

The harness does not perform a real API/analytics request, run a coroutine scheduler, or establish Android lifecycle behavior. Only VM-generated null/cast exception wording is excluded from comparison. Exception types, boundary order, state effects and observable exception identity remain checked; exact injected/external messages remain checked, including injected `NullPointerException` and `ClassCastException` messages. An exception swallowed by the selected method is verified through its exposed effects rather than an unobservable identity claim.

All work is in a separate isolation based on the frozen 1,239-body scene source. The frozen scene proof and parent current/restored trees are unchanged. See `FOLLOWON_ASSESSMENT.md` for the deferred WidgetUpdateManager subclass-allocation/super-constructor tooling gap.

## Preserved control flow and state

The selected body is `Lcom/arlosoft/macrodroid/plugins/j;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;`. The original smali is `source/smali/classes3/ce/j_ce7086bcfa493132.smali`; the replacement source is `source/java/recovered/ui/PluginLookupMethods.java`. The helper is an input to the existing body transplant. Its class and the compile/test doubles are excluded from the application.

| Entry | Original behavior retained |
| --- | --- |
| Label 0 | Check the incoming result before the guarded API work. Publish the user-denied, known-package or attempt-limit result when applicable. Otherwise store label 1 before calling the precheck. A suspended precheck returns the captured suspension marker. |
| Label 1 | Check the resumed result outside the API catch. A false Boolean returns Unit; a true Boolean increments the current owner's attempt counter once, including Java/Dalvik integer overflow. A null or wrong Boolean fails outside the API catch. |
| Label 2 | Read `I$1` before `I$0`, then check the resumed result inside an `Exception` handler. The precheck and attempt increment are skipped. |
| Other labels | Call the original invalid-resume guard. The ordinary guard exception and the explicitly injected returning-boundary case are tested separately. |

Each fresh API request creates a Bundle, writes integer `key_index = 0`, and records `app_brain_api_call_made` before looking up the API key. It captures the owner before the companion/key access, re-reads the package name afterward, then stores `I$0 = 0`, `I$1 = 0` and label 2 before reading the captured owner's API dependency. A return is considered suspended only when it is the same object as the captured marker.

Result publication has its own `Exception` boundary. The method casts the result, captures the current sink, constructs the found-package payload, publishes it, then re-reads the owner and resets its attempt count. Constructor or publication failure does not perform that success reset. Dependencies may change other fields during a call, so the tests distinguish each captured reference from each subsequent read.

Error processing runs outside those handlers. An HTTP error's status accessor is called once to test 400 and again to test 429. A first result of 400 takes priority even if the second result is 429. The 400 path adds the current package to the known list, then re-reads owner and package for the not-found publication. A 429 increments the restored/local error index and reads the current key-list size. It either sets the retry flag or records `app_brain_calls_exceeded`; exhaustion does not clear a previously restored nonzero retry flag. Other errors publish the existing connection-error singleton and likewise retain the flag. Errors and exceptions raised by these handler dependencies escape.

The original request loop always selects key index 0 and stores zero into both continuation integer fields for every new API call. Repeated 429 responses with more than one key can therefore repeatedly request the same key. Finite scripted response sequences prove the observed repeated-key behavior and later suspension/success/failure transitions. They do not change this behavior or establish termination for an endless external failure stream.

## Differential evidence and controls

The original path interprets the selected instructions extracted from the unchanged uploaded APK. The Java path runs the compiled recovered body against the same controlled dependency surface. The rebuilt path interprets the transplanted DEX and requires its bytes to match the signed APK before its result is accepted. Reports identify this as a bounded host comparison and set `androidRuntime: false`.

The independently asserted cases check gates, precheck and API call counts, continuation states, counter values, result categories, receiver identities, repeated key use, repeated HTTP status reads, package/owner changes, publication order and suspension identity. The remaining generated fault/mutation cases compare complete exposed traces and state across the original and recovered paths. Full instruction and conditional-edge coverage is a hard acceptance gate; equal outputs alone did not accept the first incomplete checkpoint.

Fifteen plugin controls deliberately alter: the denied gate, the attempt threshold, the false precheck, each suspension label, the original key selection, repeated status reads, counter reset order, checked-exception coverage, Error escape, the restored error index, retained retry flag, owner capture order, analytics index and suspension identity. All 15 reject their named cases with behavioral failures and zero unsupported executions, as do all 22 existing UI controls in the same runner. Faulty classes are confined to temporary host class directories; source, fixture and signed APK hashes remain unchanged throughout. The final unmodified positive run passes all 18,476 cases across three paths and all 14,552 independent expected-result/state checks. Aggregate records are in `reports/ui-negative-controls.json` and `reports/ui-positive-restoration.json`; every full negative report, compilation log and execution log is retained in the final evidence bundle.

## Preserved staging diagnostic and integration boundaries

The first full-test attempt stopped before differential execution with `FileExistsError` for `build/java/dex`. The loaded `compile_java` code already called strict `shutil.rmtree` without suppressing errors, yet older generated children remained or reappeared after compilation. The exact emitted failure message, build-source hash, runtime module path, bytecode metadata and file timestamps/inodes are preserved in `reports/plugin-staging-failure.json` and `reports/plugin-three-way-staging-failure.log`. The runner caught the exception and did not print a Python traceback; none is reconstructed as evidence.

Only the isolated generated `build/java` directory was then removed in a completed separate operation, with nonexistence asserted. A fresh standard `test.py --three-way` run passed all 161 Python tests and all 188,791 signed comparisons. No `exist_ok` workaround, stale-DEX acceptance or application-source change was used. This records a successful retry; it does not establish the environmental cause or prove that strict cleanup alone fixes repeated staging reuse.

The parent workstream owns its newer generated-directory cleanup and Android recorder changes. Integration must retain those changes. In particular, `ui_negative_control.py` needs the 15 added control entries merged while retaining the parent's strict cleanup call; `tests/test_v9.py` needs only the seven-to-eight method-count update while retaining the parent's installation-evidence fixture additions. The final handoff supplies narrow patches for these two non-overlapping deltas. `build.py` remains parent-owned.

## Reproduction

Use the repository's Java/tooling prerequisites, then run these commands from the project directory:

```sh
python3 build.py build --variant hybrid
python3 test.py --three-way
python3 -c 'import build; build.verify("hybrid")'
python3 ui_negative_control.py
python3 reference_status.py
```

The isolated baseline has 161 Python tests. Parent-owned Android recorder and runtime acceptance changes are integrated and counted separately. The reference-failure inventory currently maps 19 of 42 decompiler markers to registered replacements and leaves 23 unmapped; this inventory is metadata, not evidence that the entire reference tree is compilable or that whole-application equivalence has been reached.
