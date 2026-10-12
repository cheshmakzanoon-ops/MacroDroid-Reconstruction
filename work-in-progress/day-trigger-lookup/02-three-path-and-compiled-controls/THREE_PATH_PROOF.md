# DayTrigger dictionary lookup: three paths and compiled faults

The second inactive study completed successfully from 08:19:11 to 08:20:57 UTC on 2026-10-12. Its 371 declared inputs matched across the original method interpreter, compiled Java helper, and the actual D8-produced method transplanted into the preserved DayTrigger class. All three paths matched the independent expected return identity, exception behavior and full iterator event trace. The positive run recorded zero mismatches, unsupported observations, or expected-value failures.

This extends the first study documented in `ORIGINAL_JAVA_PROOF.md`; its immutable checkpoint has SHA-256 `4a39dd17902f68c5cba369fc927f08117ba9905556c7cf2890db8c29e46e9899`.

## Actual production bytecode path

The 991-byte compiled helper class, SHA-256 `d0ff3559a30190eb120161faa943700d5a2e6bfeaba85cb97807c19fa219ad61`, was the only class passed to D8. No host stubs were sent to the Android compiler. D8 ran in release mode, without desugaring, at minimum API 23. The unchanged production relocation and method-transplant helpers produced the replacement for the single original `p0(Dictionary, String)` method.

The selected original method text has SHA-256 `afdaa9b0977db46a2f333cccb0de57a401b77e2e3b66b535b2bff50991e4614e`. The other 33 original DayTrigger methods and every non-target part of its class text were checked unchanged. No constructor-owner corrections were necessary. The rebuilt selected-class DEX has SHA-256 `cf79aff20187504abf4168c081b0cbd7d80ac664bce7ead175db835d8d06e596`.

The original primary body executed 21 of 21 instructions and four of four conditional branch edges; its two original getter dependencies executed five of five additional instructions. The rebuilt primary executed 18 of 18 instructions and four of four conditional edges, again with the five original getter instructions counted separately. There are no try regions, missing coordinates, or statically substituted coverage entries.

## Actual compiled rejection controls

Each Java fault was compiled from a separately retained source file, loaded from its explicitly bound class path, and executed over all 371 cases. The original and rebuilt observations stayed exactly equal to their positive observations. Every planned required failing case was observed, and all fault runs had zero unsupported observations.

| Actual Java fault | Cases detecting the fault |
| --- | ---: |
| Case-sensitive comparison | 127 |
| Reversed comparison receiver | 3 |
| Skip null entries | 2 |
| Return early on a null query | 3 |
| Return the last matching entry | 233 |
| Trim the query | 1 |
| Replace iterator traversal with indexed access | 369 |
| Perform another iterator operation after a match | 233 |
| Swallow iterator exceptions | 25 |
| Replace an injected NPE with a different exception object carrying the same message | 6 |

The case-sensitive and last-match helper classes were also independently passed through the real D8 and transplant pipeline. Executing the resulting faulty DEX bodies detected 127 and 233 mismatches respectively, while the original and Java positive paths stayed byte-for-byte equal in their recorded observations.

Two provenance controls separately rejected an original fixture presented as rebuilt and a wrong loaded-helper hash. Both rejected before writing a parity report. After all faults, the complete positive three-path report was restored exactly: 617,109 bytes, SHA-256 `5c96ace92ac83a7eaf191881431154649437c816c46db74d5947abebb0782d07`.

The 35-command ledger retains exact arguments, time bounds, return codes, stdout and stderr identities. Every immutable source, first-stage artifact, compiled class, original APK, tool JAR, JDK executable, JDK modules file, and libjvm input was verified unchanged after the experiment. The source derivation, exact fault catalog, classes, compiler inputs, DEX outputs, transplanted smali, observations and restored result are included in this checkpoint's archive.

## Scope and next gate

The expected return and protocol observations, explicit VM-null diagnostic scope and exact UTF-16 input encoding remain the same as the first study. The five observer-record controls remain separately reported with zero application execution or coverage credit.

This proof uses the pinned host JDK's implementation of `String.equalsIgnoreCase` and the existing instruction interpreter. It does not execute Android/ART or a newly signed full APK, establish exhaustive Unicode or ill-typed erased-list behavior, or prove full application parity. The recovered helper is still unregistered. Independent review and a separately scoped integration are required before promotion; the active numeric `r0` integration is a different change set.
