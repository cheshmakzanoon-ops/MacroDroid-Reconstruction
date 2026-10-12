# Label-two retry-delay cases

Checkpoint 12 matched the original, recovered Java and method-only rebuilt DEX on 1,118 cases. The rebuilt body nevertheless had a genuine unvisited conditional edge, `81:88`. D8 emitted a distinct copy of the delay after the label-two resumed-result exception handler. Previous cases suspended at that delay; synchronous delay returns had been exercised only in the later loop copy. Original coverage therefore had all 46 conditional edges while rebuilt coverage had 47 of 48.

The additional cases append one method and one invocation to `VideoParityCases.java`. The prior 1,118 cases, exception observer, recovered helper, oracle and host dependencies are unchanged. Each new case enters label two with valid saved casts and a controlled checked exception in the resumed input. The recording flag is false, so a synchronous retry completes without entering any file or storage operations.

| Retry-delay response | Independently required outcome |
| --- | --- |
| Real Unit | Return the captured Unit identity |
| Real suspension marker | Return the marker identity |
| Null | Return the captured Unit identity |
| Thrown checked exception | Escape the second external exception identity and exact message |
| Thrown Error | Escape the second external Error identity and exact message |
| Object equal to the marker | Return Unit, with zero equality calls |
| Exception object returned normally | Return Unit, without throwing that object |

Every case independently requires label three, both saved slots cleared, exactly one delay, no dispatch or callback, an unchanged false recording flag, five observed boundaries, and the correct return/throw identity. The first failure's message is read once. For a second observed checked failure, its message is not read by app code. The complete differential observations also compare exact delay duration, boundary order, every boundary's state, logged text and all owner/file fields.

The original/JVM run in `reports/original-jvm-13-retry-delay` completed with **1,125 cases, 237 independent expected-result checks, zero mismatches, zero unsupported executions and zero expected-result failures**. Raw original coverage remains **259/262 instructions and 46/46 conditional edges**, so its strict coverage gate remains failed. The seven cases add no dynamic original instruction coverage.

The rebuilt-edge result will be measured in a separate method-only D8 run. This original/JVM checkpoint does not claim that the rebuilt edge was visited. The two unvisited rebuilt handler instructions and three original handler instructions remain separately recorded. No exemption, active registry entry, APK or Android execution is introduced here.

The 57 compiled Java faults and 68 observer controls already preserved under checkpoints 10 and 07 remain scoped to their exact 1,118-case harness. This checkpoint does not relabel those historical runs as executions of the expanded harness.
