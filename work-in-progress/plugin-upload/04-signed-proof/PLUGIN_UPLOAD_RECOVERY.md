# Plugin upload coroutine recovery

## Signed three-path, resource and deliberate-fault proof complete

The replacement for `com.arlosoft.macrodroid.plugins.k.invokeSuspend(Object)` compiles through Java 21 and D8, passes static migration and linkage validation, and passes **2,356 upload cases** within **20,832 UI cases across nine methods**. The original/JVM comparison has **zero mismatches and zero unsupported executions**, with **15,128 independent expected-result/state checks** across the UI suite. The new method visits **163/163 original instructions and 26/26 conditional edges**; both coverage measures are hard gates.

All **161 Python tests** pass in this isolated baseline. The complete five-suite original/JVM/rebuilt acceptance run passes **191,147 cases across exactly all 1,241 registered bodies and all three paths**, with zero failures/unsupported executions and an exact, non-overlapping method-key partition. All nine rebuilt DEX partitions are bound to the signed APK. The private registry contains **1,241 bodies across 604 original classes**, including the unchanged 1,119 prior constant/no-op bodies. Independent full-code roundtrip and resource verification pass on the same artifact. This is bounded host and APK-preservation evidence; Android runtime and whole-application equivalence are not established by this checkpoint.

All **54 deliberate-fault UI controls** compile and are behaviorally rejected by their required named cases, with zero unsupported executions. These comprise the 17 new upload defects and all 37 existing controls. The final clean **20,832-case three-path restoration** passes. Recovered source, original fixture and the signed APK remain unchanged throughout the run. Earlier compile-only and host-only checkpoints retain their original pending labels as historical evidence; their later gates are completed by the signed proof recorded here.

The test-only original fixture was extracted again from the unchanged uploaded APK. It contains **525,652 bytes**, SHA-256 `3038175ccb3eba87ee326352e123aed81ac8f69317283387ca3fa2f136b48bf7`. It covers exactly the 1,241 registered original methods across 604 classes. Neither the fixture nor the uploaded APK is an application build input.

## Exact signed artifact and measured gates

The signed artifact is `dist/MacroDroid-5.67.8-v9-hybrid.apk`, **94,683,177 bytes**, SHA-256 `e4643b554429743703bed5c1aa5e3541dbfc0705d9fd87c353bd968f348baf80`. Its independent roundtrip compares **71,267 classes and 349,972 methods**. Exactly the 1,241 registered bodies in 604 classes change; no classes/methods are missing or extra, no unregistered body changes, and no structural or opaque payload change is accepted.

Resource verification checks **7,212 decoded manifest/resource files**: 7,211 are byte-identical and the sole accepted canonical difference is enum/flag ordering in `res/values/attrs.xml`. All **23,854 resource IDs**, public-visibility values, ZIP entry names and compression methods match. All **22 preserved ARM64 libraries** retain their exact original bytes and pass the bounded ELF 16 KiB load-segment alignment check. These native checks do not execute native code.

| Measured gate | Result | Elapsed seconds | Complete record |
| --- | --- | ---: | --- |
| Java/D8 assembly and signing | Passed | 370.740 | `reports/upload-signed-build-03/result.json` |
| Five-suite original/JVM/rebuilt comparison | 191,147 cases, 1,241 bodies, three paths; no failures/unsupported executions | 331.358 | `reports/upload-signed-proof-03/result.json` and `reports/java-all-path-parity.json` |
| Independent full-code roundtrip | All 71,267 classes and 349,972 methods accounted for | 202.202 | `reports/hybrid-roundtrip.json` |
| All UI deliberate faults and clean restoration | 54/54 controls rejected; 20,832 clean cases passed | 1,962.871 | `reports/ui-negative-controls.json` and `reports/upload-signed-proof-03/all-54-ui-negative-controls.log` |
| Resource/ID/ZIP/native preservation | Passed on the exact signed APK | 28.537 | `reports/upload-resource-proof-03/result.json` and `reports/hybrid-resource-parity.json` |

The signed proof finished on 2026-10-12 at 04:44:15 UTC, and the separate resource gate finished at 04:47:29 UTC. All 35 source/test/doc/fixture paths from the original/JVM checkpoint stayed byte-identical through both gates. Only this document, `UI_RECOVERY.md` and `FOLLOWON_ASSESSMENT.md` were updated afterward to report the measured outcomes; all 32 implementation/test/fixture paths remained unchanged. The complete raw reports and all 54 executed mutant source/class artifacts are retained in the final evidence archive.

## Exact source and preserved entry behavior

The selected method is `Lcom/arlosoft/macrodroid/plugins/k;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;`, preserved in `source/smali/classes3/52/k_5259e6b9bbdca2b7.smali`. Its original body SHA-256 is `e1e358c48fd74e5bff3dae102917559cbc463795413aa0d329f3bede881609fe`. The recovered helper is `source/java/recovered/ui/PluginUploadMethods.java`. Only that registered compiled body can be transplanted into the original class. The helper class, continuation doubles and boundary classes are excluded from the APK.

The method first captures the suspension marker and then reads the continuation label. All original entry modes remain distinct:

| Entry | Original behavior retained |
| --- | --- |
| Label 0 | Check the initial result outside the API handler, then read the drawable. A null drawable skips icon processing. |
| Label 1 | Cast `L$4` to multipart part, `L$3` to request body, `L$2` to byte array, `L$1` to byte stream and `L$0` to bitmap, in that order, outside the handler. Check the resumed result inside the handler, then cast the icon result to String. |
| Label 2 | Cast `L$1` to upload body and `L$0` to String outside the handler. Check the resumed result inside the handler, then publish success. No icon conversion, user lookup or new API call occurs. |
| Other labels | Call the original invalid-resume guard. The normal exception and the explicitly injected returning-boundary case are tested separately. |

The saved values are not subsequently used, but their casts remain capable of throwing. Null saved values pass the casts; wrong types fail before any guarded API work. Removing those casts would change observable behavior.

Exactly one case, `upload-invalid-label-injected-return`, substitutes a returning `e6d.r` boundary to visit the original defensive return-null. It does not claim that the original guard returns. The normal invalid-label cases require `IllegalStateException` with the original message. The preceding lookup and scene injected-return cases retain their separate documented scopes.

## Icon conversion and payload construction

A present drawable is passed to the original bitmap conversion boundary. The method constructs a byte stream and requests PNG compression with quality 100. The Boolean compression result is ignored. It reads the resulting byte array, captures the request-body companion, and only then reads and checks the media-type companion.

Parsing `image/*` has a nested `IllegalArgumentException` handler that supplies a null media type. Other `Exception` values reach the outer handler and `Error` escapes. The byte-array null check occurs after that nested parse region. Request-body creation receives the captured companion, selected media type, exact byte array, offset 0 and default-argument mask 12. The multipart companion is checked before creating the part named `icon`.

The icon API is read from the current owner before `L$0` through `L$4` are cleared in order and label 1 is stored. The call receives the original part and the same continuation identity. A result suspends only when it is the same object as the entry suspension marker. Other results are cast to String inside the handler.

The upload body is allocated before evaluating its constructor arguments. The current owner and user provider are read, the user ID is obtained, and the name, developer, description, package and download link follow. A null uploaded icon uses the stored icon URL; otherwise the uploaded icon is retained. Website and the original `en` language complete the constructor arguments. The next owner/API and hash reads occur after payload construction. All five saved object fields are then cleared in order and label 2 is stored before upload.

A fresh non-suspended plugin-upload return is ignored; this includes null, an ordinary object, a failure-wrapper object, or an exception object returned as a value by a controlled API. Only the exact suspension marker returns early. By contrast, a failure wrapper supplied on resumption is checked by the original result boundary. The tests distinguish returned values from exceptions actually thrown by an API; they do not silently treat every Throwable-shaped value as an exception.

Success captures the current sink before reading the name and constructing the success payload. Publication uses that captured sink even if a constructor boundary changes the owner or sink field. This upload body does not reset the lookup attempt counter.

## Error paths and exception boundaries

The outer handler catches `Exception`, including checked exceptions. It does not catch `Error`. The saved-field casts, initial-result check and invalid-label guard remain outside it. Constructor, icon/API, resumed-result and success-publication failures have their original catch behavior.

An HTTP exception's status accessor is called twice: first to test 409, then to test 403. A first 409 result takes priority even if the second result is 403. The owner is captured after those status reads. The already-exists path publishes `g(ALREADY_EXISTS)`. The denied path sets that owner's denial flag before reading its sink and publishing `g(USER_NOT_ALLOWED)`. The generic path publishes `g(CONNECTION_ERROR)` before the logger companion check and logger call. Dependencies throwing from the error handler itself escape.

Only VM-generated null/cast exception message wording is excluded from equality. Exception classes, catch/escape behavior, boundary order, partial state and observable injected/external exception identities compare. Exact injected/external messages remain checked, including injected NullPointerException and ClassCastException messages. A swallowed exception's identity is only claimed where its effects expose that identity.

## Differential cases and deliberate defects

`PluginUploadParityCases` records API arguments and receivers, complete continuation snapshots at every controlled boundary, payload constructor arguments and partial fields, attempted/completed publications, compression parameters and bytes, companion identities, request-body defaults, multipart names, status-read counts and logger ordering. Explicit sequence cases suspend at both API boundaries and resume the same continuation. Other cases mutate owners, sinks, API/user dependencies, strings, companions, continuation fields and bitmap data at observed boundaries or while suspended.

The cases include all labels, every saved-field cast position, null collaborators, integer user-ID limits, nullable and empty payload fields, false compression, nested media parsing, distinct objects equal to the suspension marker, returned failure/exception values, checked exceptions, errors and the repeated status-code priority. Boundary fault and mutation matrices compare all exposed state across original instructions and the compiled Java body. Independently specified expectations additionally check key outcomes, identities, exact payload ordering and captured-reference behavior.

The 17 new deliberate defects remove a saved cast, obey the ignored compression Boolean, change the nested handler, re-read the request companion, change the request default mask, alter each suspension label, omit one saved-field clear, omit icon fallback, collapse the status reads, delay the denied flag, move success sink capture, narrow/widen the outer catch, move logging before publication and replace each suspension-identity comparison with equality. Each must produce a behavioral rejection in its named case with zero unsupported executions. All 37 existing UI defects remain required in the same runner. Faulty classes are confined to temporary host directories; no faulty APK is distributed.

## Scope and integration boundaries

Bitmap compression is a scripted byte-write boundary, not an Android image encoder. User access, API calls, request/part construction and publication are controlled host dependencies. The harness runs no real upload, network request, scheduler, Android lifecycle or LiveData lifecycle. Full instruction and branch-edge coverage remains bounded evidence rather than exhaustive path/input coverage.

The two shared-stub edits are narrow: `plugins.b` adds the original typed API and user-provider fields, and `PluginControl` adds an optional continuation snapshot callback used only when its lookup-continuation field is absent. Reset clears the callback. Existing lookup snapshots remain unchanged. There are no upload-specific edits to `u2f.P`, `e6d.r`, `hb9`, the HTTP exception stub, or BytecodeOracle. Parent-owned constructor, Android recorder, shared JVM runtime policy and build cleanup changes must be merged separately and retained. The inactive `ui_negative_control.py` contributes only its 17 upload controls during integration; it must not replace those newer parent policies. A later combined Widget/upload candidate needs its own fresh 1,242-body acceptance and is not validated by this isolated 1,241-body result.

This work uses an independent private copy of all **81,249 frozen lookup input files**, with every copied hash verified and no mutable hardlinks. Generated build/cache outputs, reports and APKs were excluded. The source copy occupied 819,374,473 logical bytes. The original frozen lookup source, signed APK and complete proof remain unchanged. Root-authorized closed generated-cache cleanup receipts are preserved separately; source, dist, reports and checkpoints were retained.

The reference-marker inventory maps 20 of 42 failed-decompiler markers to registered replacements and leaves 22 unmapped. It is signature metadata, not proof that the reference tree is a compilable application or that all remaining application behavior has been tested.

## Reproduction

Use the repository's Java/tooling prerequisites. From this project directory:

```sh
python3 test.py
python3 build.py build --variant hybrid
python3 test.py --three-way
python3 -c 'import build; build.verify("hybrid")'
python3 ui_negative_control.py
python3 resource_verify.py --variant hybrid
python3 reference_status.py
```

All listed signed comparison, roundtrip, resource and 54-control gates have completed in this isolation. The Python count is 161 here; the parent's newer runtime and constructor tests are counted separately. The measured control stage exceeded 1,200 seconds on this host. This executed recipe bounded the complete control stage at 5,400 seconds and each faulty subprocess at 300 seconds; its final clean restoration relied on the outer bound. The parent is adding a separate 300-second restoration timeout for future combined runs. That tighter launcher is not retroactively claimed as part of this isolated run.
