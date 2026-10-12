# All rebuilt conditional edges now execute

The closed run in `reports/method-only-three-path-14-retry-delay` compared **1,125 cases across the original DEX, recovered Java and method-only rebuilt DEX**. All **237 independent expected-result checks** passed, with zero semantic mismatches, zero unsupported executions and zero expected-result failures.

The seven appended label-two retry-delay cases dynamically cover the specific rebuilt conditional edge `81:88` that was missing in checkpoint 12. All earlier cases and observer behavior remain unchanged. The recovered helper, oracle, host dependencies, D8 flags and body-transplant implementation are unchanged; the only micro-study wrapper changes are the frozen baseline binding, study path and expected case/check counts.

| Executed body | Dynamically visited instructions | Unvisited offsets | Conditional edges visited |
| --- | ---: | --- | ---: |
| Original DEX | 259 / 262 | 232, 233, 235 | 46 / 46 |
| Rebuilt DEX | 288 / 290 | 235, 236 | 48 / 48 |

The study deliberately retains status `THREE_PATH_SEMANTIC_MATCH_CONTROLS_PASSED_RAW_COVERAGE_GATE_FAILED` and `passed: false`. There is no raw-coverage exemption. `REBUILT_HANDLER_DATAFLOW.md` separately analyzes the actual remaining rebuilt handler bytes; it supplies no dynamic coverage credit.

The assembled one-class DEX is exactly the same 4,484 bytes as in checkpoint 12, SHA256 `9a8770cfc8c438a08d6ebf87983767af878b01de39a93562e7bf9122c3c921b5`. Only the selected compiled method body is inserted into the original target class; the other three original methods and all non-target class text remain byte-identical. No host support class is inserted into this fixture.

Two provenance controls reject substitution of the original fixture for the expected rebuilt fixture and a wrong loaded-helper hash before parity. A third control assembles a real rebuilt-body mutation, changing the initial delay from 5,000 to 4,000 milliseconds. It causes 30 semantic mismatches across the same 1,125 cases, including the required `video-entry:0:false:0`, while unsupported and original expected-result failures remain zero.

The exact positive fixture is then executed again. Its entire parity report is byte-identical, SHA256 `d859500ad81b7ad6656a4c50e6855b45f3ab5e7ac71b702adf6a1fddd0bd2f31`. The original source, helper class, rebuilt DEX, complete fixed class inventories, every copied/frozen input, JDK binaries/module image/release and tool JAR all retain their exact hashes. The actual executing JVM's before/after runtime records are identical and match the four separately reviewed JRT class identities.

The run completed from 07:21:04.070788 to 07:22:08.546890 UTC on 2026-10-12. Each subprocess has a 300-second timeout and separate retained stdout/stderr, arguments, exit code, duration and hashes. The outer invocation recorded a 96 MiB minimum free-space requirement and 691,281,920 bytes available before starting.

This checkpoint is an inactive method-only compiler and host semantic study. It does not build a full signed APK, prove full application linkage/resources, execute this method on Android, or register the body. A separately running 58-control Java mutation study will retain its own final result; no pending control is counted here. Earlier failed wrapper and incomplete-coverage studies remain unchanged.
