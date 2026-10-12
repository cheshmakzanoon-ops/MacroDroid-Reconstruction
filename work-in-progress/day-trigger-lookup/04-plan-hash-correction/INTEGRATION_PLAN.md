# DayTrigger.p0: bounded integration plan after the numeric overlay

This is a read-only integration design. It does not register another method, edit application source, compile a new candidate, rerun the application harness, or promote an APK. The proposed starting point is the frozen 19-path numeric overlay, checkpoint `c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f`, published as `work-in-progress/day-trigger-numeric/06-source-integration`. Its full acceptance remains a separate pending gate. The lookup implementation and its actual 371-case proof come from checkpoint `6b3cbd47969b8f10675afd8b63dcac40967a7b30748f04b60af4989bea071c29`.

The lookup is small enough to integrate through the existing method-body pipeline. The important work is preserving the shared dependency declaration, the identity-sensitive observer, and the complete fault gates. The recommended scope is **21 source/test/fixture paths: six new and fifteen modified**. The exact baseline source location, size, SHA-256 and mode for every modified path, and the verified absence of each new path, are in [prospective-source-paths.json](evidence/prospective-source-paths.json).

## Exact body and existing proof

The target is:

```text
Lcom/arlosoft/macrodroid/triggers/DayTrigger;->p0(Lcom/arlosoft/macrodroid/variables/VariableValue$Dictionary;Ljava/lang/String;)Lcom/arlosoft/macrodroid/variables/VariableValue$DictionaryEntry;
```

Its original method text hash is `afdaa9b0977db46a2f333cccb0de57a401b77e2e3b66b535b2bff50991e4614e`. The proved helper source, `DayTriggerLookupMethods.java`, is 580 bytes with SHA-256 `d3261f820de3d197f947e65b576cb74e40153ab811dc7ed0a907dd06791b00c0`. It traverses the returned list through its iterator, invokes `key.equalsIgnoreCase(entry.getKey())` in that order, returns the first matching entry object, and otherwise returns null. Reversing the comparison receiver, adding null handling, changing iteration style, or continuing after a match changes observed behavior.

The closed private proof executed 371 inputs across the original instruction interpreter, compiled Java and a real production-D8/transplant result. It recorded zero mismatches, unsupported observations and independent expected failures. The original primary body covered 21/21 instructions and 4/4 conditional edges; the two original getter dependencies covered another 5/5 instructions. The rebuilt primary covered 18/18 instructions and 4/4 edges, plus those five getter instructions. There are no unvisited instructions, try-region exemptions or static coverage substitutions in this proof.

Ten actual compiled Java faults were detected, as were two separately compiled and transplanted DEX faults. The positive report was restored byte-exactly: 617,109 bytes, SHA-256 `5c96ace92ac83a7eaf191881431154649437c816c46db74d5947abebb0782d07`. This review rehashed that exact archived member; it did not repeat its execution.

## Source paths

| Proposed path | Change relative to numeric overlay |
| --- | --- |
| `source/java/recovered/ui/DayTriggerLookupMethods.java` | New helper, preserving the proved executable body. If its private-draft Javadoc is updated, retain that text-only delta and rebind the source/catalog hash. |
| `source/java-method-map.json` | Append one static helper mapping for `p0`, with the exact original method hash. |
| `source/ui-methods.json` | Append the identical `v9-ui` mapping; preserve the complete family partition. |
| `test-support/java/com/arlosoft/macrodroid/variables/VariableValue.java` | Add only the two missing getter methods to the existing host types. |
| `tests/fixtures/original-dependencies.json` | Append the two lookup getter declarations under the lookup consumer. |
| `tests/fixtures/original-methods.dex` | Fresh extraction from the pinned original APK with both recovery mappings and all five uncredited getters. |
| `tests/fixtures/provenance.json` | Record fresh fixture/declaration identities and complete counts. |
| `tests/java/DayLookupParityCases.java` | New UI adapter for the exact 371 inputs, expected observations, raw diagnostics and coverage. |
| `tests/java/DayLookupControlHarness.java` | New bounded one-method harness for real signed/micro-DEX control binding. |
| `tests/java/UiParityTests.java` | Wire the lookup adapter, dependency union, identity outcome and separate coverage report. |
| `tests/java/DayTriggerParityCases.java` | Extend declaration validation to the exact combined inventory while retaining its three-getter numeric result. |
| `tests/fixtures/day-lookup-mutants.json` | New frozen catalog containing all ten lookup faults and required labels. |
| `day_lookup_dex_controls.py` | New signed-positive and two-fault production D8/transplant gate. |
| `day_numeric_dex_controls.py` | Extend only declaration validation and its pin as required; keep the numeric proof/control behavior. |
| `ui_mutation_catalog.py` | Append ten lookup jobs after the unchanged first 91 jobs. |
| `ui_negative_control.py` | Bind and execute the resulting 101 Java controls and both two-control DEX families. |
| `tests/test_day_lookup.py` | New targeted catalog, dependency, observer, coverage and provenance guard tests. |
| `tests/test_day_numeric.py` | Update global counts while preserving numeric partition assertions and its 35 meaningful tests. |
| `tests/test_build.py` | Update registry, fixture and provenance expectations. |
| `tests/test_v9.py` | Require twelve UI methods in eleven UI classes. |
| `acceptance.py` | Add the separate lookup DEX-control report to the evidence inventory. |

The existing `build.py`, constructor-owner correction, bytecode oracle, `test.py`, `release_integrity.py`, runtime policy, generic `ExtractOracle.java`, numeric executable helper, numeric control harness and numeric mutant catalog need no planned changes. Their exact inspected baseline identities are in [unchanged-production-inputs.json](evidence/unchanged-production-inputs.json). Java and Python discovery already include the proposed new test files. The release-input collector already includes root Python files, all source, fixtures and tests.

This source-path inventory excludes generated release snapshots/reports and later delivery documentation. Those must be regenerated or updated after actual execution. Their future bytes and the total future Python test count cannot be established by this plan. No workflow, Android runtime policy, canonical smali, signing input, or original APK change is proposed.

## Shared dependency declaration

The numeric overlay declares three uncredited original getters. Its Java `DayTriggerParityCases.loadDependencies` and Python `day_numeric_dex_controls.validate_dependencies` each pin the **whole declaration** and assume that every row belongs to `r0`. Merely appending the two lookup rows would therefore fail both loaders.

Retain one exact combined declaration, with the original three rows unchanged and the following two added:

| Consumer | Original dependency | Original method text SHA-256 |
| --- | --- | --- |
| `p0` | `VariableValue$Dictionary.getEntries()Ljava/util/List;` | `f3959381d2067a3611069ac45c01a34078ef9e718f9c4906f74bb545da48be0e` |
| `p0` | `VariableValue$DictionaryEntry.getKey()Ljava/lang/String;` | `41c4ec0e7f0ec7f3b6638765a92670cdbae7c839b794b8f3de9ba1c2b431b1a3` |

The complete proposed five-row partition is in [proposed-dependency-partitions.json](evidence/proposed-dependency-partitions.json). It is plan data, not a replacement application declaration.

Both existing numeric validators should validate the same exact combined bytes and both exact consumer partitions before returning only the three numeric keys. A shared validation function within the existing module/class can provide the two-key lookup partition to the new adapter. Preserve global uniqueness, exact schema/row fields, declared original method hashes, registered consumer existence and the prohibition on giving a dependency recovery credit. Reject unknown consumers or extra rows; do not accept them by filtering first. The new getter rows must not increase either method's recovered-method count.

The generic `ExtractOracle.selection` already supports multiple registered consumers and validates dependencies strictly. No extractor rewrite is needed. Re-extract from original APK SHA-256 `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`, then verify that all 1,246 previously selected method bodies remain identical and that the only additions are `p0`, `getEntries` and `getKey`. DEX container bytes and indexes will change; compare selected instruction/body identity rather than expecting old whole-file equality.

Keep the numeric coverage partition at one credited primary plus three getters. Its test of `registered keys union numeric dependency keys` becomes **1,247**, while the generic full selector becomes **1,249**. Setting both assertions to 1,249 would hide the intended per-consumer distinction.

## Shared host types and observation boundary

Do not copy the standalone lookup study's minimal `VariableValue` stub over the active one. Its class flags and constructor signatures differ from the shared contracts used by earlier suites. The numeric baseline already has public `Dictionary.entries` and `DictionaryEntry.key`, both with the original field names. Add a getter returning each existing field. Preserve the existing three-argument constructors, all public fields, `DictionaryEntry.equals`, nested-class flags and the transient numeric getter aliases. Adapt lookup fixture construction to those existing constructors. No getter implementation or host fake goes into the APK.

A fresh compilation must bind its actual class files. The standalone proof's helper class hash must not be forced by changing shared types: compiler `InnerClasses` metadata can differ when the host class flags differ. Measure the integration helper and D8 output and retain any metadata-only explanation. The numeric helper source and its class behavior should remain unchanged; prove the class identity after compilation rather than assume it.

The lookup observer must run before generic Gson serialization. Duplicate entries may serialize identically while being different objects. For a returned object, record its index by `==` in the plain backing entries, `-1` for null and a rejecting sentinel for a foreign object. This must not perform another operation on the traced iterator/list after the method returns. Retain the exact `iterator`, `hasNext@n`, `next@n` event sequence, including the absence of a further iterator operation after a match.

Wire a lookup-specific state reset, return observer, exception observer and final snapshot into `UiParityTests`; avoid changing canonicalization for unrelated methods. Route every lookup input through the normal case/method accounting, and enforce the independently expected identity and trace on all paths. Preserve the exact raw exception record separately from compared fields.

The existing proof excludes VM-generated message text only for its seven explicitly authored null-receiver cases. Retain their case identities, NPE class and full trace. Every injected NPE/CCE/other exception must retain its exact message and the same injected object identity. Keep the five observer-record tampering controls separately labeled with zero application execution/coverage credit. Replacing an injected NPE by another object with the same message must still be detected.

The [ordered input inventory](evidence/lookup-ordered-inputs.json), SHA-256 `78c52e4b3493ba4712c9fa88edb10ffc80c68e0df18e16594dc9f83ae4c00c63`, was derived from all 371 saved positive rows. It retains the exact input/expected-observation fields and UTF-16 hexadecimal encoding, including unpaired surrogates. This is a newly derived review inventory, not a hash that the old standalone harness previously enforced. Bind the new UI adapter to these exact ordered fields when it is authored.

## Fault gates and signed body binding

Preserve the exact order and prepared bytes of the first 91 Java faults. Append the ten lookup faults with prefixed unique names and unchanged required case identities. Their actual private detection counts are:

| Fault | Detected cases |
| --- | ---: |
| Case-sensitive comparison | 127 |
| Reversed comparison receiver | 3 |
| Skip null entries | 2 |
| Early return for null query | 3 |
| Last matching entry | 233 |
| Trim query | 1 |
| Indexed traversal | 369 |
| Extra iterator operation after match | 233 |
| Swallow iterator exception | 25 |
| Replace injected NPE object, retaining its message | 6 |

The last-match and case-sensitive classes must also pass through the real production D8/transplant path and produce the corresponding 233 and 127 failing observations. Reuse the retained classes actually compiled by the Java fault gate, with exact loaded-class/hash/path validation. Keep both existing numeric DEX faults and both lookup DEX faults in separate named reports. Retain the original-as-rebuilt and wrong-helper provenance rejections and exact positive restoration.

The lookup DEX control must compare the full positive primary instruction listing with the body in the freshly signed APK and bind the two getter methods to the same signed member, as the numeric control now does for its own method. The private lookup study legitimately reported 33 other original DayTrigger methods unchanged because it modified only `p0`. A combined signed class will also contain the recovered `r0` body. Do not repeat that private claim for the combined class: require the exact two-body target set, the unchanged positive numeric body, all remaining original methods and unchanged non-method class text. A one-method micro-DEX may still use original `r0` outside its selected scope, provided it is explicitly scoped and the signed `p0` instruction identity is independently checked.

Keep the current sixteen acceptance commands and the 5,400-second UI-control gate, with 300-second individual UI invocation/restoration bounds. No timing change is justified by this read-only plan; retain measured elapsed values and change a bound only if a concrete run requires it. The added report must be collected on failure as well as success.

## Expected deltas, not newly observed combined results

| Measure | Frozen numeric overlay | With lookup, projected |
| --- | ---: | ---: |
| Registered recovered bodies | 1,243 | 1,244 |
| Recovered target classes | 605 | 605 |
| UI recovered methods | 11 | 12 |
| UI target classes | 11 | 11 |
| Uncredited original getter dependencies | 3 | 5 |
| Selected fixture methods | 1,246 | 1,249 |
| Selected fixture classes | 607 | 607 |
| UI case inventory | 24,465 | 24,836 |
| All-suite case inventory | 194,780 | 195,151 |
| Actual Java UI controls required | 91 | 101 |
| Separate production DEX controls required | 2 numeric | 2 numeric + 2 lookup |

The case projections are arithmetic from the preserved 1,242-method report: 193,489 total cases and 23,174 UI cases, plus the numeric 1,291 and lookup 371 inventories. This review rehashed and read those baseline reports; neither projected combined total has been executed here. The `Dictionary` class is already registered, and `DictionaryEntry` is already present as a numeric dependency, so the two new getter selections add no fixture class. The existing `test_v9` count of 1,893 reference Java files is unrelated and remains unchanged.

## Concrete next work and review boundary

Author a small source overlay against all recorded baseline hashes. First close the shared stub/consumer-partition changes, the unchanged 91-job prefix check and the new 371-input adapter, then perform a bounded fresh original/JVM/D8 study and the complete fault checks. Preserve any failed attempt and rebind actual helper/fixture identities. A separately coordinated full build must then pass signed bytecode, static/linkage, resources, all-suite three-path and complete acceptance gates before promotion. Input snapshots and delivery documentation follow the measured results.

The proof continues to use the pinned host JDK's `String.equalsIgnoreCase`; it does not establish ART Unicode behavior, exhaustive Unicode, malformed erased-list behavior, scheduling, persistence or full application parity. The independent Android readiness run remains higher priority than this prospective integration.

## What this review actually did

The retained [inspection command](inspection-command.json) executed only a read-only Python source/evidence inspector in 0.555 seconds. It verified all 113 numeric capsule files and all 31 lookup source files against their checkpoints, the exact lookup archive and positive member, the 19 numeric source changes, the planned six new-path absences, dependency set arithmetic and the two retained baseline reports. All 155 inspected file roles were byte/mode-identical before and after. The derived outputs occupy less than one MiB in the owned temporary review directory. There was no app execution, host compilation, full source copy or active-source mutation.
