# Inactive plugin-lookup recovery checkpoints

These immutable checkpoints preserve incomplete work as it progresses. They are
not applied by `scripts/materialize_v9.py` and do not change the active method
registry, candidate APK or acceptance result.

## 01: Original/JVM comparison, coverage pending

[The frozen checkpoint](01-original-jvm-coverage-pending/checkpoint.json) retains
38 changed or new source/test/document/fixture files and 12 exact evidence files.
Its SHA-256 is
`17cc2231ad39c16ef1fac30058a6586c7440f79f490989beb144675bb56a9ecb`.

The plugin lookup cases agree between original instructions and recovered JVM
code: 2,047 plugin cases and 17,470 total UI cases, with zero mismatches and zero
unsupported executions. The coverage gate nevertheless **failed**: only 194 of
198 instructions and 33 of 34 conditional branch edges were visited. No signed
rebuilt-APK comparison or plugin-specific negative controls had run at this freeze.
The checkpoint's 1,240-body / 603-class registry is inactive and must not be cited
as the current application's accepted registry.

[PLUGIN_RECOVERY.md](01-original-jvm-coverage-pending/PLUGIN_RECOVERY.md) describes
the bounded body recovery. [FOLLOWON_ASSESSMENT.md](01-original-jvm-coverage-pending/FOLLOWON_ASSESSMENT.md)
records the separate widget-constructor pipeline gap. Existing root-owned build
and runtime changes must be preserved during any future deliberate integration.


## 02: Original/JVM coverage passed; signed proof and controls pending

[The second frozen checkpoint](02-original-jvm/checkpoint.json) preserves
39 source/test/document/fixture paths and 19 exact evidence files. Its SHA-256 is
`8ac757470ddbca4ad6a36e73201e78875057dac99b2ccd333010669e503501ec`.

The expanded two-path suite passed 3,053 plugin cases and 18,476 total UI cases,
with 14,552 independent expected-result checks, zero mismatches and zero unsupported
executions. Coverage reached all 198 instructions and all 34 conditional branch
edges. All 161 Python tests passed. This is a new measured checkpoint; the first
checkpoint's failed coverage report remains unchanged.

All 37 control anchors (including 15 plugin controls) were authored and validated,
but deliberate-fault execution and signed rebuilt-APK comparisons had not run at
this freeze. Those pending stages prevent promotion to active application inputs.
The checkpoint's 1,240-body registry remains inactive. See
[PLUGIN_RECOVERY.md](02-original-jvm/PLUGIN_RECOVERY.md) for its exact scope.
