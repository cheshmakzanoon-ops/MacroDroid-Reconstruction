# Video monitor handler 232/233/235: scoped data-flow argument

This is a review argument about **synchronous `Exception` dispatch in one exact
original method**. It does not change the original/JVM coverage gate, inject an
exception into the original program, add coverage credit, or establish Android
execution of the video-monitor method. Both measured positive studies still
fail that gate: the initial 1,014 cases and expanded 1,111 cases each visit
259 of 262 instructions and all 46 conditional edges, with zero mismatches.
The three unvisited code-unit offsets remain 232, 233, and 235.

## Bound inputs

The target is
`Lcom/arlosoft/macrodroid/action/services/a;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;`.
The original APK is 95,725,918 bytes with SHA-256
`84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`.
Fresh extraction gives the 4,552-byte one-method DEX with SHA-256
`940aee4861d9bd52951ccc835e91a917bb56748b4eaad5deb8a0fa1c7d2c3254`.
Its inventory has 262 instructions, 534 code units, and six Exception-only
protected regions. The complete exact operands are retained in
`reports/handler-dataflow-04/original-instructions.json` (SHA-256
`2d368ab110348b3934f217d084d0b66df4d61a0ef3ddb41d3e804ec876efcfda`).

`verify_handler_dataflow.py` checks the original operands and all collected
evidence hashes. It builds ordinary and conservative exceptional control-flow
edges, checks domination and register writes, and checks the actual installed
JRT constructor disassembly. Its nine deliberately invalid structural inputs
must be rejected. Those nine checks are proof-tool guards, **not application
fault controls or additional original executions**.

## Only one protected region enters this handler

The handler applies to the half-open code-unit interval **[122,159)** and catches
`java.lang.Exception`. Its 17 protected instructions are:

| Offset(s) | Original operation | Relevant fact |
| --- | --- | --- |
| 122 | Read `v14.x` into wide `v5` | The captured receiver `v14` is non-null. |
| 124 | Compare `v5` to zero | Primitive comparison does not throw. |
| 126, 129 | Assign wide `v19 = 1048576` twice | Both assignments are preserved in the original; the divisor is nonzero. |
| 132 | Branch if previous availability is nonpositive | No call or state mutation. |
| 134, 137 | Assign wide `v21 = 104857600` twice | Primitive constant assignments. |
| 140, 142 | Subtract and compare availability | Long arithmetic/comparison does not produce a synchronous Exception. |
| 144, 146, 147, 149 | Conditional branch, branch, register move, branch | Primitive control flow. |
| 150 | Store available bytes into `v14.x` | Uses the same captured non-null receiver. |
| 152 | Divide available bytes by `v19` | The divisor is exactly 1,048,576. |
| 154, 156 | Allocate `StringBuilder`, invoke its default constructor | Fresh receiver, zero supplied arguments, fixed valid capacity 16. |

The interval ends immediately after the default constructor. Appending the
prefix/number/`MB`, converting to a string, reading the logging identifier, and
calling the logger occur later, in a different protected region. Faults at those
observable boundaries already exercise that other catch. They cannot supply
legitimate coverage for this earlier handler.

At 232 the original moves the caught exception into `v0`; at 233 it moves `v10`
into `v21`; at 235 it branches to the shared error path at 495. There is no
ordinary predecessor of 232, only predecessor 232 for 233, and only predecessor
233 for 235. The preceding instruction 231 branches to 244 rather than falling
through. No other exception-table entry targets any of these three offsets.
The conservative graph retains **all 262 instructions as reachable**, since it
intentionally includes even semantically infeasible declared exception edges.
The synchronous argument below is separate from graph reachability.

## Captured storage receiver cannot become null in the interval

At 112, the method loads `self.this$0` into local register `v14`. At 116, it invokes
`BaseVideoRecordingService.c(File)` with that register as receiver. A null
receiver or an Exception from this call follows the earlier handler at 52; it
does not enter 122. A successful return is moved into `v12/v13` at 119, followed
by the constant at 120. In the graph including all exception edges, 112, 116,
119, and 120 still dominate 122. Its only ordinary predecessor is 120.

No instruction from 114 through 158 writes `v14`, including through an
overlapping wide destination. Both the read at 122 and write at 150 reference
the same original public long field `BaseVideoRecordingService.x` and the same
local receiver. The original coroutine's `this$0` field is final synthetic; the
host deliberately permits stronger adversarial owner changes at call boundaries
to check read order. Even changing `self.this$0` to null or another owner during
`c(directory)` does not replace the already captured local reference. The
expanded cases exercise this using the original interpreter and Java helper.

Concurrent mutation of the owner's `x` value can alter a value read by the
monitor. Because it is an ordinary long field, this argument does not require
atomic or consistent concurrent reads. Any resulting primitive long value still
leaves the receiver and divisor non-null/nonzero. Another thread changing fields
or the owner field cannot rewrite a live local reference. GC cannot turn that
strong reference into null. There is no later owner reload inside [122,159).

## Arithmetic cannot enter this Exception handler

Both assignments to `v19/v20` dominate division at 152, and neither register is
overwritten afterward before that division. The divisor is 1,048,576, so integer
division cannot throw `ArithmeticException`. Signed long subtraction or overflow
does not throw in Java/DEX semantics. In fact, the subtraction is reached only
when the prior value is positive, so subtracting 104,857,600 cannot overflow its
lower bound. Extreme available-byte values may affect comparisons, the quotient,
and stored state, but do not create a synchronous Exception here.

## The pinned host constructor has a valid fixed allocation size

The host is the installed Temurin **21.0.12.1+1-LTS** JDK. Its release metadata,
three installed source files, and four **actual JRT class files** are retained.
`javap -c -p -s` was run on those saved class bytes. This avoids relying solely on
a source archive that could differ from the running class library.

| Actual JRT class | SHA-256 |
| --- | --- |
| `StringBuilder` | `14c9ab4b30fdb96f62b74b2cd6a53c3a790a221981f59a1d349b0dc09ecc592e` |
| `AbstractStringBuilder` | `f1ccca2afbe6d7d0ba5a1f19b7095b555796701dfafd5c529366350f7c9c94e4` |
| `StringUTF16` | `e03e9a012b6c29de2130ef49badab77d421f5272e1c72224838545e1091488b5` |
| `Object` | `10cc90d16479279e1d6ee258fdaea4c5640ac6125acb5a7100a7b0a20237a9f2` |

The default `StringBuilder` constructor passes exactly 16 to
`AbstractStringBuilder(int)`. Its `Object` constructor immediately returns.
The compact-string branch creates `byte[16]`; the other branch invokes
`StringUTF16.newBytesFor(16)`, whose length check returns 32 before creating
`byte[32]`. The negative-length branch is false. The installed UTF16 size check
compares against 1,073,741,823, so its oversized-length branch is also false.
There is no application callback, file access, logger, array indexing operation,
cast, or argument-dependent method call in this constructor path.

At original offset 156, the receiver comes directly from successful allocation
at 154 with no intervening instruction and no alternative ordinary predecessor.
It cannot be null. Class/field/method resolution or initialization failures have
Error-family outcomes under ordinary verified linkage. Memory exhaustion and
stack exhaustion likewise produce Error-family outcomes. Those outcomes are
outside the original `catch (Exception)`, and must continue to escape. The proof
does not replace them with a caught Exception or simulate them as original
positive cases.

## Android corroboration and remaining scope

The saved primary [Android 15 `StringBuilder` source](https://android.googlesource.com/platform/libcore/+/refs/tags/android-15.0.0_r1/ojluni/src/main/java/java/lang/StringBuilder.java),
[`AbstractStringBuilder` source](https://android.googlesource.com/platform/libcore/+/refs/tags/android-15.0.0_r1/ojluni/src/main/java/java/lang/AbstractStringBuilder.java),
and [`StringUTF16` source](https://android.googlesource.com/platform/libcore/+/refs/tags/android-15.0.0_r1/ojluni/src/main/java/java/lang/StringUTF16.java)
show the same default capacity, positive 16/32-byte array lengths, and excluded
negative-size branch. Exact request URLs, HTTP results, raw Base64 responses,
decoded source hashes, and source licenses are retained. Android's oversized
check uses `>` whereas this installed host uses `>=`; that difference cannot
affect the argument for capacity 16.

This is **tagged AOSP source corroboration**, not a byte-for-byte extraction of
the Google APIs image's boot library. The recorded prior Widget ART environment
is Android API35, build
`google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.043/12960925:userdebug/dev-keys`.
That earlier eight-case Widget proof did not execute this video method. No new
Android claim is made here.

The conclusion is limited to the unchanged, normally linked classes and
synchronous language/runtime behavior. It excludes arbitrary asynchronous
exception injection by debugging/instrumentation agents, privileged corruption
of locals/runtime metadata, replacement bootstrap classes, and unrelated
interpreter/reflection implementation failures. The host oracle resolves
members reflectively; tooling failures must remain failures, not be relabelled
as original application behavior. There is no configured constructor adapter.

Under these stated conditions, every operation in [122,159) lacks a feasible
synchronous `Exception` source, so 232/233/235 have a specific argument for
semantic unreachability. **Independent review and an explicit policy decision
remain required before any coverage accounting change.** The actual positive
coverage remains 259/262 and the gate remains failed. A separately instrumented
constructor-fault study could examine handler routing, but would be modified
program evidence with zero positive original-coverage credit.
