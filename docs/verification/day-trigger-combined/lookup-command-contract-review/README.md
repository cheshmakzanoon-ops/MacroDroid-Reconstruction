# Independent lookup command and signed-method contract review

The bounded source/design review passed. It found no concrete blocker in the frozen Lookup09 producer and the proposed combined workflow contract. This review executes no Java, D8, application method, Android command, full project build, or tooling test suite. The combined signed acceptance and the new tooling implementation remain separate work.

The reviewed source is Lookup09 checkpoint `87c2a01a627590b62017eae8145db92d1a7593d5cf127114a9812ec13cd756f5`, using the nineteen unchanged Lookup08 payloads plus the two exact Lookup09 replacements. The design is checkpoint `3da7b4fa3707c301256c8dd7236c18f7680d2fb5bd72595d353e8a01b223830f`. [result.json](result.json) records the verdict, and [read-inputs-before-after.json](read-inputs-before-after.json) binds every read source before and after the operation. Exact review inputs and the executed reviewer are retained here.

## Nineteen source-derived commands

The reviewer parses the producer and symbolically expands its actual command expressions and finite loops. The symbolic evaluator supports immutable strings, paths, lists, and constants; it cannot execute arbitrary Python calls. The independently expanded rows equal every field of the design's nineteen-row lookup contract.

| Role | Commands | Expected exits |
|---|---:|---|
| Positive and two fault pipelines: D8, disassembly, assembly | 9 | 0 |
| Signed lookup, positive transplant, numeric before and after inspection | 4 | 0 |
| Positive and exact restoration harnesses | 2 | 0 |
| Two changed-DEX behavioral harnesses | 2 | 3 |
| Two provenance rejection harnesses | 2 | 1 |

Every command has a 120-second bound. All 38 stdout/stderr roles are distinct. Java executable, JVM flags, classpath order, compiler options, target methods, source/config/result paths and command order are taken from the frozen source. The exact rows and source expressions are in [source-derived-nineteen-commands.json](source-derived-nineteen-commands.json). These are static command expectations, not new execution receipts.

## Working directory and finalization

Both method producers call `subprocess.run(..., cwd=root)` after resolving `root`. Their pinned UI caller supplies `build.ROOT`, and the pinned build module derives that root from its own file. Individual method rows do not record a separate cwd field; the outer acceptance receipt does. The design preserves that distinction. [cwd-and-provider-binding.json](cwd-and-provider-binding.json) contains the exact source chain and shared recorder comparisons.

The numeric clock, file-stat helper and complete `CommandStreamEvidence` implementation are text- and AST-identical to the reviewed Numeric08 provider. Lookup adds the explicit schema-2 provider identity, expected return code, entered-context, timeout and error fields, and a real finalization clock after the shared context receipt. Expected fault exits 3 and provenance exits 1 remain successful recorder observations when the expected code is returned. The future verifier must reject missing finishes, errors, populated cleanup failures, stale streams, physical aliases, or nonchronological finalization. [lookup-finalization-contract.json](lookup-finalization-contract.json) records the exact success contract without manufacturing a failed context's completion.

## Signed method and existing mapping

The lookup positive micro-transplant is compared byte-for-byte at the instruction-report boundary with `p0` inspected from `build/hybrid/classes3.dex`. The Java harness requires exactly one matching APK member and hashes it against that local DEX, then rechecks the fixture, APK, signed getter DEX, target DEX and class origins after execution. The numeric-before and numeric-after inspections select `r0` in that same local signed DEX and require exact report equality. Both source producers use the same literal APK and `classes3.dex` roles. [signed-method-source-contract.json](signed-method-source-contract.json) records the reviewed links and the remaining combined-verifier obligation to bind both reports to one measured final APK identity.

Each micro-DEX preserves all other original methods and class text. Its whole class intentionally differs from the signed class, which contains three registered mappings. The complete pre-existing `requiresScheduleExactAlarm()Z` mapping is unchanged as both a parsed object and its raw JSON object bytes across the 1,242-method baseline, 1,243-method numeric overlay and proposed 1,244-method combined overlay. Every prior registry object remains in order. [unchanged-constant-and-stage-bindings.json](unchanged-constant-and-stage-bindings.json) records these exact checks and all 21 final payload identities.

## Retained reviewer correction

The first reviewer attempt selected argv positions 6:8 instead of 5:7 for the DEX/method comparison. It therefore compared a method plus two intentionally different before/after output filenames and stopped on its own assertion. The source-derived nineteen-command comparison had already passed. The exact first reviewer, all partial evidence and its failure description are preserved in [initial-reviewer-attempt/](initial-reviewer-attempt/). Only that one reviewer slice was corrected. Production source and the frozen design were unchanged; the corrected review passed and rehashed all its read inputs again. No application failure or additional recovery credit is inferred from either reviewer attempt.
