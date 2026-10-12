# DayTrigger numeric value recovery: original and Java checkpoint

This is a private recovery of `DayTrigger.r0(VariableValue.DictionaryEntry)I`.
It does not change the active method registry or the APK. The method is a numeric
conversion used by the preserved DayTrigger implementation; calendar scheduling,
Android parcel construction, and the trigger lifecycle are outside this study.

The recovered Java reads the entry's value once. Integer values narrow a signed
64-bit value to a signed 32-bit value with wraparound. Decimal values truncate
toward zero, saturate outside the integer range, and produce zero for NaN. Other
value types, including a null contained value, return zero. A null entry throws
`NullPointerException`.

## Measured result

The fresh run on 2026-10-12, from 07:17:16 to 07:17:29 UTC, passed 1,291 cases
across the actual original instructions and the compiled Java helper. It produced
zero mismatches, zero unsupported executions, and zero independent expected-value
failures. All 25 original primary-method instructions and all four conditional
edges executed. The three original dependency getters contributed another seven
executed instructions; they are not counted as newly recovered methods.

The cases include integer wrap boundaries and individual bits, seeded 64-bit
integers, decimal values immediately above and below integer boundaries, both
zero signs, subnormal values, NaN payloads, infinities, seeded double bit patterns,
and nonnumeric/null values. Integer expectations use arbitrary-precision modulo
and sign conversion. Decimal expectations use explicit NaN/saturation rules and
exact `BigDecimal(double)` truncation, without a narrowing numeric cast.

The original fixture contains the actual original method and its three original
getter bodies. The unchanged instruction interpreter executes those getters
against small host field containers. The Java path invokes matching host getters.
The loaded helper, interpreter, study, and boundary classes are bound to their
actual file paths and hashes. A deliberately wrong loaded-helper hash was rejected
before a report could be written. Repeating the positive run restored the entire
report byte for byte, with every input and compiled class unchanged.

Only the explicit null-entry case compares the required exception class. Its raw
VM messages remain in the report. All other cases compare their complete observed
outcomes. This is a JVM/interpreter result, not execution on Android/ART.

The source, original fixture, complete reports, command ledger, standard output and
errors, class files, and exact input identities are preserved with this checkpoint.
The toolchain JAR, JDK and supplied original APK are identified as existing external
inputs; they are not recopied into this small experiment.

## Remaining work

Compile the helper through the preserved production D8 and method-transplant
pipeline, compare the resulting method against the same independent expectations,
exercise meaningful compiled faults, and obtain independent review before any
active integration. No rebuilt-bytecode, signed APK, UI, or whole-app parity claim
is made by this checkpoint.
