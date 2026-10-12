# DayTrigger numeric value: rebuilt bytecode and compiled fault proof

This private checkpoint extends the original/Java proof in checkpoint 01. It
recovers one method, `DayTrigger.r0(VariableValue.DictionaryEntry)I`, and does not
change the active registry, APK, Android lifecycle, or calendar implementation.

## Result

The measured run from 2026-10-12 07:21:49 to 07:23:52 UTC passed all 1,291 cases
across original instructions, compiled Java, and rebuilt instructions. Each case
has an independently computed expected result. There were zero mismatches,
unsupported executions, or independent expected-result failures.

The original path executed all 25 primary-method instructions and four conditional
edges. Its three original getter dependencies contributed seven more instructions.
The rebuilt path executed all 18 primary-method instructions and four conditional
edges, plus those same seven original getter instructions. No static coverage
credit or excluded offsets are used.

## Exact production pipeline

The run imports the unchanged preserved `build.py` and `constructor_owner.py`,
verifies their bytes, and uses their class relocation, method extraction,
constructor-owner check, annotation handling, and DEX integrity functions. Only
the compiled recovered helper is sent to D8. No host class is sent to the compiler
or transplanted into the target.

D8 receives the same release, no-desugaring, and minimum-API-23 options as the
production build. The compiled helper method replaces only the selected method
inside the preserved DayTrigger class. All 33 other original methods and all class
text outside that replacement remain identical. No constructor correction is
needed. The assembled, test-only DEX is:

`867e137f65908d8360f307cdd0f23b3f910e5606d6b5916f876e85186b813b47`

The full original fixture, compiled classes, helper DEX, disassemblies, target
DEX, method-body binding, command ledger and reports are preserved. The fixture
includes the actual original getter bodies, which the instruction interpreter
executes against the small host field containers.

## Actual faults

Thirteen separately compiled Java faults were all detected by named cases:
integer-zero, decimal-zero, integer saturation, integer conversion through double,
integer conversion through byte, decimal rounding, decimal floor, NaN-to-one,
infinity-to-zero, other-value-to-minus-one, string parsing, contained-null failure,
and null-entry-to-zero. These produced between 1 and 509 mismatching cases each.
The original and rebuilt reference outcomes stayed identical for every case.

The integer-zero and decimal-zero faults were also passed through the actual D8
and method-transplant pipeline. Running their rebuilt DEX with the unchanged
positive Java helper produced 509 and 406 named mismatches, respectively. The
original and Java reference outcomes stayed identical. No control depended on an
uncompiled source edit or an unsupported instruction.

Two provenance controls rejected before producing a comparison report: an original
fixture substituted for the rebuilt method and a wrong loaded-helper hash. The
final positive run restored the entire comparison report byte for byte. All
baseline evidence, source, class, toolchain, and JDK file identities were unchanged.

The runner records 41 completed command invocations. The full observations retain
the same narrow null-entry exception rule as checkpoint 01, including raw messages.
This remains a JVM/interpreter study. Independent review and integration validation
are required before promoting the method into the active reconstruction.
