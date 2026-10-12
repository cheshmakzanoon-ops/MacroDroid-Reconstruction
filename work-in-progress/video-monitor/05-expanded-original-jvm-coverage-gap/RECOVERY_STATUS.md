# Video monitor: expanded differential result and unresolved coverage gate

The expanded original/JVM study completed with **1,111 cases, zero mismatches,
zero unsupported executions, and 223 passing independent expected-result checks**.
All **46 of 46 conditional IF edges** were visited. The unmodified original
method's instruction coverage is **259 of 262**, so the overall gate **failed**.
No active registry or APK was changed.

The three unvisited offsets are exactly **232, 233 and 235**, the
`move-exception`, register move and branch in the original `:catch_e8` handler.
The protected region contains the captured storage owner's `x` field operations,
constant long arithmetic, and the default StringBuilder construction. Whether
this Exception-only handler is unreachable under the pinned host/runtime will
be reviewed using a separate, explicit data-flow proof. It is not assumed
covered, and the passing conditional-edge count does not substitute for those
three instructions.

The actual bounded commands are recorded in
`reports/original-jvm-05-expanded/result.json`: extractor compilation, harness
compilation, fresh original-APK method extraction, and original/JVM execution.
The existing javac host output was reused only after every one of its 881 class
files matched the frozen compiled archive and all 841 source hashes matched.
The normal strict oracle was copied unchanged; no constructor-owner adapter or
new opcode handler was used. The fresh original fixture is retained.

Cases cover all entry labels, invalid-label behavior, both saved-state casts,
storage thresholds, file-size and stall-counter values including integer
wraparound, delay/dispatch identity, injected checked exceptions and Errors,
owner/file/counter changes at call boundaries, and initial resume sequences.
The expansion adds synchronous and asynchronous multi-resume chains, nested
exception-message and logger failures, strict storage reporting thresholds,
counter overflow/long-seconds contracts, dead casts after stop suspension, and
captured-owner versus fresh-owner mutations. Boundary discovery executions are
reported separately and do not inflate the positive case count.
All injected exception identities and messages and all logged text are exact.
Only VM-generated escaped null/cast wording is excluded, with every raw message
retained in the report. No logged message is normalized in this checkpoint.

The earlier 1,014-case/126-check study is immutable under checkpoint03. The
expanded result is a separate study; its successful cases do not turn the
unresolved coverage gate into a pass. A separate collected data-flow argument
examines those three handler instructions without changing this gate or oracle.
Any separate constructor-fault experiment will be labelled as modified
host-boundary evidence and will receive no credit toward unmodified original
instruction coverage or promotion counts. The unchanged 1,014-case result
remains a real coverage failure, as does the expanded study. There is no
signed-build, rebuilt-Dex, Android,
nonempty recording-service or complete application 1:1 claim here.
