# Compiled dead-cast-order fault was not detected by checkpoint05

The actual method-only control changed only the two label-two saved-state casts
from File-then-qnc to qnc-then-File. The altered helper compiled successfully and
its different class bytes were loaded from the intended private origin. All
1,111 original/JVM cases ran, with **zero reported mismatches**, zero unsupported
executions, and unchanged raw coverage at 259/262 instructions and 46/46 edges.
The control gate therefore correctly reports **failure: zero of one faults
detected**. Exit 2 was already expected from the positive coverage gap and was
not accepted as evidence that the mutant was detected.

The lost distinction is visible in retained raw exceptions for
`video-dead-casts:2:2`: the original File cast rejects a qnc instance, whereas the
swapped Java body first rejects a VideoFile instance at the qnc cast. The prior
video observer excluded both CCE message strings entirely. As a result, it kept
the same exception type and final state but lost the failing source type. This
is an observed harness limitation; it is not a claim of equivalent cast order.

The unchanged positive helper was recompiled and restored afterward. Its source
hash, class hash and entire positive parity report match checkpoint05 exactly.
Two separate origin controls rejected a wrong helper hash and a classpath that
would load the positive helper in place of the expected mutant, before any
parity case ran. All original fixture, source and fixed class inventories are
unchanged. No APK, active source, oracle opcode, or coverage rule was changed.

The following separate harness correction will retain the source class from the
three exact original-oracle forms and four observed pinned-JDK generated forms.
Unknown forms must fail closed; external and injected exception messages remain
exact. This can establish the differing-source-type cast-order case. Invalid
values of the same source class do not distinguish order by this observation and
will not be described as doing so. Checkpoint05 and this failed control remain
immutable after that correction.
