# Original, recovered Java and rebuilt one-method DEX agree on 1,118 cases

The corrected run in `reports/method-only-three-path-12` completed with zero semantic mismatches across 1,118 cases, three execution paths, and 230 independent expected-result checks. There were zero unsupported executions and zero expected-result failures. Its status is `THREE_PATH_SEMANTIC_MATCH_CONTROLS_PASSED_RAW_COVERAGE_GATE_FAILED`, with `passed: false`: the raw original coverage requirement is still not satisfied.

## Exact build and comparison inputs

The study verifies frozen original/JVM checkpoint 07 and compiled-host checkpoint 02. It uses the unchanged recovered Java helper, unchanged observer and bounded interpreter, and exact original-method fixture. Only the 96 MiB free-space preflight and two corrected assembler command names distinguish the subsequent launch from the separately frozen command failure; no production source body changed.

The actual pinned production `build.py` supplies constant-pool relocation, method parsing, annotation handling, and the selected body insertion pattern. Its SHA256 is `dd599090fc075fed0835875937a2c2b76d91381936c26f4275f876edf47345f0`. The pinned constructor-owner guard is called unchanged and produces zero corrections. D8 receives exactly one relocated recovered helper class and zero host stubs. The selected compiled method body is inserted into an independently copied complete original target class. The other three original methods and all non-target class text match exactly.

The assembled target DEX SHA256 is `9a8770cfc8c438a08d6ebf87983767af878b01de39a93562e7bf9122c3c921b5`. It contains exactly the original target class. The origin-checking launcher verifies the actual recovered helper, unchanged oracle, frozen harness and controlled dependencies, plus the new study/launcher classes, before parity. The selected original fixture and rebuilt DEX identities are checked inside the executing JVM.

This is a one-class fixture assembly. It is not a full signed APK build, full-application linkage/resource proof, or Android execution of the video-monitor method.

## Meaningful wrong-input and rebuilt-body controls

Substituting the original fixture for the expected rebuilt DEX is rejected before any parity execution. A deliberately wrong loaded-helper hash is also rejected before parity. The third control assembles an actual changed target DEX: only the initial delay literal is changed from 5,000 to 4,000 milliseconds. That rebuilt body produces 30 semantic mismatches, including `video-entry:0:false:0`, while the original and Java paths remain the intended ones. Unsupported and original expected-result failures remain zero, and original raw coverage is unchanged.

The exact positive DEX is then used again. The complete positive report, original source, rebuilt DEX, helper class, all fixed class inventories, frozen dependencies, copied inputs, JDK binaries/module image/release, and compiler tool JAR match the recorded identities. Every subprocess is bounded to 300 seconds and retains separate stdout/stderr, arguments, return code, duration and hashes.

## Raw coverage remains visible

| Executed body | Dynamically visited instructions | Unvisited offsets | Conditional edges visited | Unvisited edge |
| --- | ---: | --- | ---: | --- |
| Original DEX | 259 / 262 | 232, 233, 235 | 46 / 46 | None |
| Rebuilt DEX | 288 / 290 | 235, 236 | 47 / 48 | 81:88 |

The actual visited offset and edge sets are retained, as well as these aggregates. The original three-instruction handler argument remains a separately reviewed, pinned synchronous-runtime proof. No instruction is counted as dynamically visited by that argument, and no coverage exemption is applied. The rebuilt unvisited edge is being investigated separately: it is the synchronous return from the delay reached after a label-two resumed failure, which the compiler emitted as a distinct conditional. The two rebuilt unvisited instructions are an exception-handler entry and jump; the existing original-body proof is not silently extended to these different bytecode offsets.

## Runtime evidence collected by the executing JVM

The three-path study itself reads the actual bootstrap-loader `java.base` resources for `StringBuilder`, `AbstractStringBuilder`, `StringUTF16`, and `Object` immediately before and after the case run. The exact class bytes, `jrt:` origins, release, VM version and arguments are preserved. All four live class hashes and the release hash match the independently reviewed checkpoint 04b identities. The before/after runtime records are identical.

The wrapper independently records and rechecks the actual Java executable, javac executable, libjvm, module image and release. The owned subprocess uses an explicit classpath, and Java option environment variables are removed. These facts support review of the separate private accounting proposal; they do not by themselves change any coverage result or acceptance policy. No active registry, production pipeline, APK or shared protected project file was edited.
