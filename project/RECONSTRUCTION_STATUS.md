# Current reconstruction progress

## Active 1,244-body source checkpoint — 13 October 2026

The active hybrid compiles **1,244 registered Java method bodies across 605 classes**.
The latest recovered body is the DayTrigger dictionary-entry lookup `p0`; the
previous numeric `r0` recovery remains integrated. Other executable application
code builds from preserved editable smali. Original native libraries and opaque
assets remain binary dependencies. **Neither complete original Java/Kotlin source
nor whole-application 1:1 Android behaviour is established.**

Run **38365018305**, source-selection commit
`daf58639000f449a55ac1985746925cd2a1816e8`, passed all sixteen configured hosted gates
and the separate live-host closing verifier. The result includes 195,151 bounded
original/JVM/rebuilt-DEX cases, 357 Python tests, all 101 compiled Java UI fault
controls, numeric and lookup DEX fault controls, exact positive restoration, a
signed source-edit experiment and 24 hash-bound fresh reports. No test was skipped
or timeout relaxed to obtain this result.

## Input and artifact identities

| Item | Exact value |
| --- | --- |
| Complete input files | 81,304 |
| Canonical source snapshot SHA-256 | `5df3f861db4fd2f372edbad1d4ff6fc3df701ed70adf4737024baffd722dab2c` |
| Input manifest file bytes / SHA-256 | 14,505,034 / `223c0f13a6075e036b5878cb523297ba985e37308f1e2213dd034a17c71e3598` |
| Registered bodies / classes | 1,244 / 605 |
| Signed hybrid APK bytes | 94,683,170 |
| Signed hybrid APK SHA-256 | `bb527f25da36b55fe91a166043e297158213a7458bf3f901e2199adfc21668a2` |
| Test-only original fixture SHA-256 | `410ebd6bd6455863812b1c3b34148f6717c6824cb2bdf8d8490323832543f802` |
| Preserved baseline APK SHA-256 | `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096` |

The fixture includes five uncredited original getter dependencies, separate from
the recovered-body count. The method count is not a percentage of functional parity.

The [complete hosted checkpoint](../docs/verification/lookup-hosted-daf5863/) retains
all 6,115 ZIP members and their identities, both original CI APK outputs, selected
readable reports and the exact immutable current candidate. Its original closing
report's `active_promoted: false` value describes the run before this publication;
it is intentionally unchanged. Archived inode/time receipts remain historical
live-host observations, not purported observations of a later archive extraction.

## Newly integrated behaviour

The dictionary lookup returns the first case-insensitive matching entry, preserving
its object identity and the original list/iterator access order. Its 371 target
cases cover duplicates, significant whitespace, Unicode case comparisons, empty
and null boundaries, injected iteration failures and exact exception propagation.
These are host-side observations; Android execution of `bb527f25…` is separate.

The final UI report writer now serializes explicit null fields using a writer-local
Gson configuration. This corrects the earlier closing-report omission without
changing application logic, the shared Gson instance, expected results or the strict
finalizer. The earlier failed run 38248170022 remains preserved.

## Remaining acceptance

The new APK has not earned the previous candidates' Android results. Bounded prior
editor/navigation captures, the supplied reference's promotion-dialog crash,
exact-alarm settings observations and limited ART probes retain their own source,
APK and environment bindings. Macro saving, reopening, execution, alarm delivery,
permissions, persistence, background services, external integrations, animations
and physical-device coverage remain independent work.

Rebuilt APKs use the development signing key, not the publisher's private identity.
The supplied reference is not an independently authenticated publisher release.
A source build and bounded comparisons are not whole-app equivalence proofs.
