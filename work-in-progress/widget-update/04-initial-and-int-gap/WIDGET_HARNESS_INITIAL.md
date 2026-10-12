# Widget harness: first failing original/JVM study

This inactive checkpoint preserves the exact Widget overlay and test inputs used by the first standalone study. It does not replace the parent's subsequently updated Widget helper or oracle. No Widget body is registered and no application APK was built.

The runner copied and hash-checked its Java inputs into an independent private directory, compiled Java host and harness classes, and extracted the one selected method directly from the pinned original APK. The fixture is 4,220 bytes with SHA-256 `21fa3b34730a902713b14ee8ada375d4fdca3edf481dc3caabcd7bd1d3f22a0a`. It is test-only.

The gate correctly failed: **1,710 cases, 120 failed cases, 125 unsupported executions, 136/194 original instructions and 16/20 conditional edges**. The original high-bit test uses `AND_INT`, which this oracle rejects. Unsupported counts also include bounded case-construction probes used to locate observed dependency boundaries. High-bit reuse and resumed entry paths therefore remain unproved at this snapshot. The report preserves actual mismatches and coverage; no failed gate was converted into a pass.

The exact method-scoped parent-constructor adapter was explicitly configured and validated against the original method. It recorded 1,958 calls on the fresh paths reached by this run. It constructs only a compile-only child adapter on the host; this count is not Android ART verification.

The helper used here has SHA-256 `ab1829ac48bb32c6348239145cdde915722964b1784fd626cae9d1a8bb250e4c` and the oracle used here has SHA-256 `482af8ecd9db285e1f88fbf9a5bd934262f4182772e49c9a70f91ea66aaa5bca`. Both exact source copies are included. Subsequent work adds a separately tested AND_INT opcode and captures exception messages before constructing log text; those later versions and their proof must be assessed separately.

The harness observes continuation fields and identities, provider lookups, iterator calls and positions, manager/renderer/identifier/factory construction, both suspension calls, external exception identities, logging and explicit resume sequences. It uses the existing UI comparison implementation. Controlled dependencies do not implement Android widget services, rendering or coroutine scheduling.

All command logs, input hashes, full failure/coverage report, original-method smali and DEX, and compiled class archive are retained in the adjacent evidence bundle. Signed rebuilt comparison, structural APK proof and deliberate application fault controls remain pending.
