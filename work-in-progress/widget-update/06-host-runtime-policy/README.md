# Explicit host UI exception runtime policy

The default HotSpot runtime had fast-throw stack/message omission enabled. In the
full UI suite its warmed-up reflection call site logged a null NPE message, while
the direct Java call retained a helpful message. The earlier complete failed
report is preserved in `06-corrected-message-failure`; no failure was rewritten.

The unchanged full UI harness passed all 20,818 cases across nine methods and
three paths when `-XX:-OmitStackTraceInFastThrow` was supplied. All 901 bound files
(APK, fixtures, classpath code and critical source inputs), method/case inventory,
and original instruction/branch coverage stayed identical. Exact raw messages
from all three paths are retained. The narrow existing message normalizer and
its injected/external lookalike cases were not changed.

Five host test/acceptance inputs now consistently apply and verify that flag plus
explicit `-XX:+ShowCodeDetailsInExceptionMessages`. Both the positive UI command,
all deliberate UI mutations and final restoration receive the same policy. The
effective runtime report records the Java binary, HotSpot library, effective
flags and raw command output. Six focused policy rejection tests pass. Full
acceptance also requires fresh hashes for both new oracle-conformance reports
and the runtime-policy report.

Application inputs and the signed `b79b0010…` APK remain unchanged. The new input
pin is `00634710968ddf2fcd7400699ea3c1bb179209ff13e8062d28e64dc098fd7c99`
(81,266 files). The exact manifest is retained in `input-snapshot.tar.gz`.
The final full signed five-gate rerun is separate and pending in this checkpoint.
