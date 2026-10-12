# DayTrigger dictionary lookup: original and Java study

This inactive study recovers the single static `DayTrigger.p0(Dictionary, String)` body as `DayTriggerLookupMethods.findEntry`. The original method is extracted directly from the supplied APK, alongside the original `Dictionary.getEntries` and `DictionaryEntry.getKey` getters. The getters are dependencies, with separate coverage accounting. No active registry, signed APK, or Android workflow changes are included.

## Actual result

The run in `reports/original-java-01` completed on 2026-10-12 from 08:14:59 to 08:15:14 UTC. All 371 declared inputs matched between the original instruction interpreter and the compiled Java helper. Both paths also matched the separately declared expected return identity, exception behavior, and complete list/iterator event sequence. There were zero mismatches, unsupported observations, or independent expected-value failures.

The original primary method executed all 21 instructions and all four conditional branch edges. Its two original getter dependencies executed their five additional instructions. The combined original coverage is therefore 26 of 26 instructions and four of four conditional edges. No static exception exclusions or synthetic execution credit are used.

The inputs cover empty lists, a null query with an empty list, first and later matches, duplicate entry identities, null entry keys, significant whitespace and punctuation, 312 ASCII case/position combinations, 18 explicitly declared Unicode case pairs, composed/decomposed and multi-character nonmatches, exact lone UTF-16 surrogates, null dictionaries/lists/iterators/entries/queries, faults at each iterator protocol event, and stopping before a later null or iterator fault. Every query and key is recorded as exact UTF-16 code units so the evidence preserves lone surrogates.

For successful returns, each path must return the actual entry reference at the expected index. A copied or foreign entry is unsupported and fails. The trace records `iterator`, every `hasNext` and `next`, and any unexpected indexed `size`/`get` operations. Injected exceptions must preserve their exact type, message, and object identity. Only the explicitly declared VM-null inputs compare the required exception class plus the full trace while retaining both raw VM-generated diagnostic messages; the study does not claim those diagnostics are identical.

## Identity and rejection evidence

The original APK has SHA-256 `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`. The extracted three-method fixture is 8,296 bytes with SHA-256 `261b88a32666b00ce1225c1ba03150b39f36edf0d13df5d36e05bcfd1953c568`. The complete positive report is 495,733 bytes with SHA-256 `abbc8f5e9cc1856a8f6319e9c69089ddd535b1f7316c66d421f3574c6fab4d10`.

All 21 compiled host/harness classes are bound to their actual loaded file origins and hashes. The active production BytecodeOracle was copied unchanged. Exact input, fixture, JDK modules, executable, tool JAR, and compiled-class identities were checked before and after the measured run. A deliberately wrong helper hash rejected before producing a report. Restoring the unchanged configuration reproduced the entire positive report byte for byte.

Five separately reported observer-record controls reject changed injected messages, exception identities, event traces, return values, and unsupported markers. These controls are not application executions and receive zero application coverage credit. Actual compiled helper mutation and rebuilt DEX controls are the next stage; this checkpoint makes no claim that they have already run.

## Reproduction and limits

`prepare_inputs.py` records the three exact original bodies and read-only production pipeline inputs. `derive_lookup_pipeline.py`, its identity receipt and patch, and `compose_study.py` preserve the derivation from the previously closed numeric study. The composed Java study includes the exact previously reviewed provenance and coverage utilities, with new explicit dictionary cases and observations. `run_day_study.py --output <fresh-directory>` compiles fresh classes, extracts the original fixture, runs both paths, checks the rejecting origin control, and verifies restoration. Existing result directories are never overwritten.

This is a bounded interpreter/JVM study. `String.equalsIgnoreCase` executes against the pinned host JDK in both paths. The evidence therefore does not establish Android/ART string behavior, exhaustive Unicode equivalence, ill-typed erased list elements, calendar scheduling, UI behavior, process continuity, or full application 1:1 parity. The helper remains unregistered pending a real D8/transplant proof, compiled fault controls, and independent review.
