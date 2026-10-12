# Independent review of the DayTrigger dictionary lookup

The frozen lookup checkpoint is supported within its stated scope. A fresh independent run rebuilt the host helper and harness, extracted the original methods again from the exact original APK, compiled the helper through the frozen production D8/transplant functions, and reproduced all 371 original/JVM/rebuilt observations. It found no semantic mismatch or unsupported instruction. The complete positive report was restored exactly after fresh compiled faults and provenance controls.

This is an independent review of one proposed method body. It adds no active registration, app code, signed APK, Android execution, or new globally counted parity cases. The 371 inputs repeat the existing bounded corpus; repeated executions are not additional distinct cases.

## Frozen subject and provenance

The reviewed checkpoint is `day-trigger-lookup-recovery/checkpoints/02-three-path-and-compiled-controls/checkpoint.json`, SHA-256 `6b3cbd47969b8f10675afd8b63dcac40967a7b30748f04b60af4989bea071c29`. The independent preflight checked all 31 frozen source files and every one of the 150 archive members against this fixed checkpoint. It also verified the exact 282,949-byte archive, SHA-256 `a5326a18c8577b5113c4fea32745d9abfb6e19f66f0de406f136f2df94309bee`; the archive holds 9,386,062 bytes of source, classes, fixtures, reports, and command evidence. No archive member was extracted over a working source path.

The 35 historical bounded commands and their stdout/stderr bindings were reviewed, including all ten actual Java mutants, both actual rebuilt-DEX mutants, the two provenance failures, and exact positive restoration. The historical Java mismatch counts were `[127, 3, 2, 3, 233, 1, 369, 233, 25, 6]`; the two rebuilt mismatch counts were `[127, 233]`. These historical outcomes are preserved as historical evidence and are distinct from the smaller fresh control set below.

The input APK is the unchanged 95,725,918-byte original with SHA-256 `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`. The tool JAR is pinned to `354b10af74c09f5d2ab139def4231f0906dc6cc75738b1057e5a8263a412848e`. The JDK release, java/javac launchers, libjvm, and modules were recorded and checked unchanged before/after. The active oracle source remains `d91ddcd8ec3d67d41d69b8252835e747c2cad2c6d5ea898323794ceec30e6b56`; the production build source remains `dd599090fc075fed0835875937a2c2b76d91381936c26f4275f876edf47345f0`. No oracle or build implementation was edited for this review.

## Original behavior and source correspondence

The exact target is:

```text
Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;
```

The original body obtains `dictionary.getEntries()`, obtains that list's iterator once, checks `hasNext()` before each `next()`, casts the returned element to `DictionaryEntry`, reads its key, and invokes `equalsIgnoreCase` on the supplied query. It returns the first matching entry reference immediately and returns null only after exhaustion. It has no exception handler. Its irrelevant constant loads affect no externally visible operation.

The 580-byte helper's enhanced-for loop preserves that operation order and comparator receiver. In particular:

- A null query on an empty list still returns null, because no comparison occurs.
- A non-null query safely compares against a null entry key and can proceed to a later match.
- A null entry itself fails when its key is read. The helper does not skip it.
- Matching returns the original first entry reference and performs no later `hasNext()` call.
- Iterator exceptions escape with their original type, message, and object identity. The helper contains no catch or wrapper.
- An indexed loop, an eager null-query check, query trimming, reversed comparator receiver, and a last-match policy would change observable behavior; the preserved compiled controls exercise these differences.

The two original getter dependencies are included as actual DEX methods. `Dictionary.getEntries()` reads the `entries` field; `DictionaryEntry.getKey()` reads the `key` field. For the interpreter paths these getters are executed by the unchanged oracle from the selected original fixture, not substituted with helper code. The Java path uses the compile-only host data classes with matching field reads. The scope is controlled dictionary/list state, not a proof of every constructor or Android lifecycle surrounding it.

## Fresh measured execution

The independent run is `reports/fresh-review-01/`, from 2026-10-12 08:42:28.363023 UTC through 08:43:28.618457 UTC. It completed in **60.255499 seconds**, with **20 subprocess commands**, each bounded to 120 seconds. Its result is `INDEPENDENT_THREE_PATH_REVIEW_PASSED`.

Every one of the 21 host/harness classes was freshly compiled from the frozen sources into the new private run. Each newly compiled class was byte-identical to the historical class of the same name. Actual loaded class origins were bound to the new files; the only field excluded when comparing the full new report with the historical report was the deliberately changed absolute class-origin map. Class membership and the byte hash of every class in that map were checked separately before execution. No semantic observation, raw exception text, expected result, case row, or coverage field was excluded from that historical reproduction check.

| Fresh artifact | Bytes | SHA-256 |
|---|---:|---|
| Original three-method fixture | 8,296 | `261b88a32666b00ce1225c1ba03150b39f36edf0d13df5d36e05bcfd1953c568` |
| Positive helper class | 991 | `d0ff3559a30190eb120161faa943700d5a2e6bfeaba85cb97807c19fa219ad61` |
| Rebuilt DayTrigger fixture | 18,464 | `cf79aff20187504abf4168c081b0cbd7d80ac664bce7ead175db835d8d06e596` |
| Fresh positive report | 617,046 | `a8adb83c6f7a94dc5f8c6a3182751f582d7747e2eb7bd60b8e7521f7b2cf26fe` |

The first three identities are exactly the prior checkpoint's identities. The fresh report has different absolute origin paths and therefore a different whole-file identity from the historical 617,109-byte report. The fresh final restoration is byte-identical to the fresh positive report, including all new origins.

| Measured property | Original path | Rebuilt path |
|---|---:|---:|
| Primary lookup instructions dynamically visited | 21 / 21 | 18 / 18 |
| Original getter instructions dynamically visited | 5 / 5 | 5 / 5 |
| Total selected instructions dynamically visited | 26 / 26 | 23 / 23 |
| Conditional branch edges dynamically visited | 4 / 4 | 4 / 4 |
| Exception regions in the primary body | 0 | 0 |

All 371 inputs ran through all three paths. There were zero mismatches, zero unsupported results, and zero independent expected-result failures. There is no static reachability exemption, ignored instruction, or coverage adjustment in this study.

For each positive and faulty micro-build, exactly one helper class entered D8. The input JAR contained no host stub classes. The emitted helper method was transplanted with the unchanged production functions into the original target class. The other 33 original methods and all non-target class text were byte-identical to their original source text. The production constructor-owner hook returned no corrections, and the output body had no runtime helper or `defpackage` stub references. This proves the bounded method transplant, not a full APK build or installation.

## Fresh deliberate faults and provenance checks

The fresh controls compiled real changed Java or DEX code into separate directories. They did not alter positive class files or the original fixture.

| Fresh control | Expected outcome | Observed result |
|---|---|---|
| Reverse the Java comparator receiver | A null entry key must expose the changed behavior | 3 mismatching cases; required null-key case detected |
| Make Java comparison case-sensitive | Case variants must stop matching | 127 mismatching cases; first-entry identity case detected |
| Compile/transplant the case-sensitive method into rebuilt DEX | Rebuilt execution must expose the altered bytecode | 127 mismatching cases; required identity case detected |
| Wrong original fixture hash | Stop before parity output | Exit 1 with exact original-identity rejection |
| Supply original fixture as the rebuilt fixture | Stop before parity output | Exit 1 with exact alias rejection |
| Wrong loaded helper hash | Stop before parity output | Exit 1 with exact helper-hash rejection |

Every code mutant ran all 371 cases on all three paths and reported zero unsupported instructions. In both Java mutants, every original and rebuilt observation stayed exactly equal to the positive run. In the DEX mutant, every original and Java observation stayed exactly equal. Thus the failed comparisons came from the deliberately changed path. All three mutant runs exited 3 as required; a crash, missing case, unsupported operation, or wrong reference-path result could not satisfy the fresh control checks.

Afterward, the unchanged positive config and classes ran again and produced an exactly identical positive report. The source/checkpoint/archive/APK/tool/JDK hashes and all freshly compiled positive class hashes remained unchanged.

## Comparison limits and review conclusion

The declared corpus covers empty and nonempty lists; the three null container/iterator states; null queries, null keys, and null entries; identity-sensitive duplicates; exhaustive ASCII letter/case placements; 22 expressly authored Unicode/surrogate cases; exact whitespace/punctuation; and three injected exception types at each iterator boundary. It does not claim all erased ill-typed lists, arbitrary concurrent list implementations, every Unicode code point, calendar behavior, Android UI, or ART execution.

Both interpreter paths and the JVM helper call the pinned host JDK's real `String.equalsIgnoreCase`. Consequently this is strong evidence for the recovered call order, receiver, list traversal, identity, and exception propagation over the declared inputs. It does not independently test Android's implementation of Unicode case comparison. The source preserves the original platform call rather than implementing a replacement case-folding algorithm.

The unchanged observer excludes only the raw VM-generated NPE text for seven explicitly authored inputs: null dictionary, null entries list, null iterator, null query on a nonempty list, null query with null key, null first entry, and null second entry. In those cases it still requires the exact exception class, full event trace, absence of a returned entry, and absence of injected exception identity. All raw messages remain in the reports. Injected NPE, ClassCastException, and IllegalStateException messages and exception-object identity remain exact comparison fields. The historical observer-record controls and actual replacement-exception mutant remain bound and verified. This review adds no normalization.

No blocking semantic or proof-scope defect was found in the frozen lookup checkpoint. The next integration still needs the separately owned registration, full build/static/linkage/acceptance gates, and any Android claims appropriate to that integration. None is implied by this method-only result.

## Retained execution and storage notes

The complete command ledger, stdout/stderr, fresh class files, original extractor inventory and fixture, both micro-D8 pipelines, fault sources/classes, complete positive/fault/restored observations, and protected-input hashes are retained in the evidence archive. The fresh run wrote approximately 3.62 MB before its final result record and stayed within the requested small-output budget. No existing build cache or evidence was retired.

A subsequent read-only console summarizer attempted to index an observation's expected-exception field at the top level and raised `KeyError: 'expectedException'`. This was outside the completed 20-command study; it changed no source or report and did not affect the result. The seven null cases above are read from the reviewed harness source. The actual study result and reports were not rerun or modified to hide this incidental inspection error.
