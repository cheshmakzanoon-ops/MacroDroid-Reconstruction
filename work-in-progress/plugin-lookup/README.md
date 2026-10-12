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
