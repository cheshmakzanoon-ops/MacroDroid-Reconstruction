# The two unvisited rebuilt handler instructions

This is a separate analysis of the exact method-only rebuilt DEX. It supplies no dynamic instruction coverage, exemption, registry entry or Android claim. The original three-instruction argument is not used as an automatic exemption for new bytecode.

## Bound input and metadata

The rebuilt one-class DEX is 4,484 bytes with SHA256 `9a8770cfc8c438a08d6ebf87983767af878b01de39a93562e7bf9122c3c921b5`. The unchanged recovered helper and production D8/transplant pipeline produced the same bytes in studies 12 and 14.

The independent read-only collection in `reports/rebuilt-handler-inventory-14` loads those DEX bytes with the original reviewed metadata collector. Its input is explicitly identified as rebuilt in the wrapper report. The reused collector's historical output filename `original-instructions.json` and stdout label do not change that input identity. The exact 290-row instruction inventory has SHA256 `c270e94e6afdc667399844f2ddeb5207baac0d9315ed1227b3071bb3a276fc0c`. No app instruction is executed by this collection.

The only exception-table entry targeting offset 235 is the `java.lang.Exception` handler for the half-open interval **[132,163)**. Its handler chain is `235: move-exception v0`, then `236: goto/16 522`. These are the two unvisited instructions. Ordinary control flow has no entry into 235, and 236 follows 235 only.

## Protected operands

| Property | Exact rebuilt operands and consequence |
| --- | --- |
| Captured storage owner | Offset 122 loads `self.this$0` into v15. Offset 126 invokes `v15.c(directory)`, and 129 records its successful result before the protected region is entered at 132. Normal completion proves v15 non-null. |
| No captured-owner reload | v15 is not overwritten in the protected interval. A callback changing `self.this$0` cannot change this captured receiver. |
| Field operations | Offset 132 reads v15.x; offset 154 writes v15.x. Both use the captured non-null receiver. The fields are present in the pinned host class. |
| Nonzero divisor | Offset 136 initializes v20/v21 to 1,048,576. It precedes every path to the division at 156, and the pair is not overwritten before that division. |
| Arithmetic | Comparisons and signed long subtraction preserve Java/DEX overflow behavior. Division by the fixed positive divisor has no arithmetic-exception path. |
| Fresh builder | Offset 158 creates a StringBuilder in v0, and 160 calls exactly `StringBuilder.<init>()` on that fresh allocation. It is the only invocation inside the protected interval. |
| Constructor extent | The interval ends at 163, before builder append operations beginning at 165/167. Those append operations are not part of this handler's protected region. |

The complete protected instruction offsets are **132, 134, 136, 139, 141, 144, 146, 148, 150, 151, 153, 154, 156, 158, 160**. The intermediate moves and branches do not introduce another exception-producing call or receiver read.

On the exact normally linked synchronous host used by these studies, the default StringBuilder constructor has fixed capacity 16. The independently reviewed complete JRT class and javap identities in checkpoint 04b bind both compact and UTF16 allocation paths, whose array lengths are 16 and 32. The negative-size and excessive-capacity exception branches cannot be taken for that input. Allocation/linkage failures are Errors, which this Exception-only handler does not catch.

The executing three-path JVM in study 14 recorded the same four actual bootstrap `java.base` class hashes and release before and after its cases. Those live bytes agree with the reviewed constructor identities. Consequently the two-instruction chain has the same narrowly stated synchronous infeasibility rationale as the original, after separately checking these rebuilt operands and region boundaries. This is an inference from the exact metadata and pinned-runtime constructor proof, not dynamic execution evidence or an approved accounting implementation.

Asynchronous exception injection, instrumentation replacing boot classes, corrupted state outside the controlled boundaries and another runtime are outside the argument. No Google APIs Android boot-library byte match or execution of this video-monitor body on ART has been established.

## Coverage is unchanged by this document

Study 14 dynamically visited **288 of 290 rebuilt instructions and all 48 conditional edges**. The earlier missing edge `81:88` was a real case gap and was dynamically covered by the seven added label-two retry-delay response cases. The two handler offsets remain unvisited. The original likewise remains **259 of 262 instructions and 46 of 46 edges**. Both raw instruction-coverage gaps stay explicit.
