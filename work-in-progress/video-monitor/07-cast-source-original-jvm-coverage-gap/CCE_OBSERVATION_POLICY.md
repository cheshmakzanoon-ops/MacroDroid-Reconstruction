# Exact generated-cast forms retain the failing source type

Checkpoint06 records an actual compiled cast-order mutant that checkpoint05
missed. The correction is confined to the video observer and its tests; the
production helper, unchanged original interpreter, original DEX fixture, and
raw instruction-coverage gate are not modified.

The original oracle constructs a generated cast failure containing the actual
source class name. Three such source names occur in this bounded case space:
`java.lang.String`, `defpackage.qnc`, and `defpackage.VideoFile`. The installed
JDK emits four corresponding full messages, accounting for String-to-File,
String-to-qnc, qnc-to-File, and VideoFile-to-qnc. The observer accepts only those
exact recorded forms for their respective execution paths. It retains and
compares the failing **source class**, while preserving the full raw messages
outside the cross-runtime comparison. An unrecognized form, changed loader,
extra whitespace, changed target, or unknown source type fails closed.

This establishes the order distinction for two invalid saved objects with
different source types: the original File-first cast rejects qnc; the swapped
qnc-first cast rejects VideoFile. Two invalid String objects have the same
source type. Their cast order is not distinguished by this observation, and
the report explicitly limits its claim accordingly.

The injected/external-identity check precedes generated-message handling. Any
injected exception remains exact even if its text imitates one of the accepted
generated forms. The new original/JVM study contains seven such explicit
lookalike cases. Separate observation conformance exercises both CCE and NPE
lookalikes from three independently tracked error sources, all exact forms,
source-type mismatch, altered target, unknown forms, changed loader, null text,
and whitespace changes. All **68 controls passed**. These are observer checks;
they execute no original or recovered app method and add no app-case or
instruction-coverage credit.

The fresh positive study measures **1,118 original/JVM cases**, zero mismatches,
zero unsupported executions, and 230 independent expected-result checks. Its
full original coverage gate remains failed at **259/262 instructions**, with
the same unvisited offsets 232/233/235 and all 46 conditional edges visited.
The strengthened observer does not exempt the earlier handler gap. Compiled
application-fault detection remains a separate follow-up proof.
