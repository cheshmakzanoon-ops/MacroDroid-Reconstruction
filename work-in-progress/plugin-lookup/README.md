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


## 03: Signed proof and roundtrip passed; controls still running

[The third frozen checkpoint](03-signed-controls-pending/checkpoint.json) retains
40 source/test/document/fixture paths, 75 closed evidence files and two narrow
merge patches. Its SHA-256 is
`d8ef00d69158325e4c03292a53a980712cfbdcbd882f04293ac5c13a48e3053b`.

All 188,791 original-instruction/JVM/rebuilt-APK comparisons passed, including
3,053 plugin cases and 18,476 total UI cases. There were zero mismatches and zero
unsupported executions. All 198 plugin instructions and 34 conditional branch
edges were visited; the independent signed DEX roundtrip also passed. All 37
deliberate-fault controls and final positive restoration remained incomplete at
this freeze. The 1,240-body / 603-class registry and APK remain inactive.

The [complete evidence archive](03-signed-controls-pending/evidence-archive/manifest.json)
preserves all 75 closed files with an [entry-by-entry verification receipt](03-signed-controls-pending/evidence-archive/extraction-receipt.json).
Seventy-four compact files are also visible normally in
[evidence/](03-signed-controls-pending/evidence/). The 18 MB resource table is
retained inside the archive. The earlier failed staging attempt and successful
retry are preserved with their actual outcomes. Running control logs are excluded
from this immutable checkpoint.

The [inactive APK manifest](03-signed-controls-pending/artifact/manifest.json)
pins 94,683,497 bytes and SHA-256
`9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`.
Assemble it without changing the current application:

```bash
python scripts/assemble_artifact.py work-in-progress/plugin-lookup/03-signed-controls-pending/artifact/manifest.json
```

To restore the complete evidence, assemble its manifest and extract the resulting
`workspace/artifacts/plugin-signed-proof-controls-pending-evidence.tar.gz` into
`work-in-progress/plugin-lookup/03-signed-controls-pending/`. Archive entry paths
start at `evidence/`; exact hashes are listed in the receipt and original checkpoint.
Future integration must retain parent build/runtime changes and apply the two
provided merge patches only after their recorded baseline checks.


## 04: Signed proof, all controls and clean restoration passed

[The final isolated checkpoint](04-signed-proof/checkpoint.json) preserves 40
source/test/document/fixture files, two narrow merge patches and a complete
[191-file evidence archive](04-signed-proof-evidence/manifest.json). Checkpoint
SHA-256:
`43ec5fd958e43258f62b3639aac275cccff2333435c7f48bc8fd6f3717cd958d`.

The signed three-path suite passed all 188,791 cases, with zero failures or
unsupported executions. All 198 original plugin instructions and all 34
conditional branch edges were covered. All 37 deliberate-fault controls passed,
including 15 plugin controls, and the final clean 18,476-case UI restoration
passed. The independent DEX roundtrip and 161 Python tests also passed. See the
[complete recovery report](04-signed-proof-evidence/plugin-lookup-recovery.json)
for precise exception, retry and injected-boundary scope.

The APK remains exactly the checkpoint-03 artifact (`9108b581…`, 94,683,497 bytes);
[its reference](04-signed-proof/artifact-reference.json) binds the final proof
without duplicating or changing the active candidate. The 1,240-body / 603-class
source remains inactive. Combined parent acceptance and Android plugin behavior
are separate, unmeasured scopes for this checkpoint. Earlier failed and pending
checkpoint reports remain unchanged.
