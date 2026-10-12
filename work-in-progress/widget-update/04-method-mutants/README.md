# Widget compiled method controls, inactive checkpoint

All **24 compiled Widget method-body mutants** were detected by their named behavioral cases. Two additional class-origin controls were rejected before parity execution. The clean helper source, loaded class, and full positive report were restored exactly. The [original control report](evidence/run/result.json), [method-control documentation](WIDGET_MUTANTS.md), and [frozen checkpoint](checkpoint.json) retain the measured details.

This proof uses the fixed original/JVM host paths from [the positive Widget checkpoint](../04-original-jvm/README.md). Each parity execution preserves 2,342 cases, 198 independent original expectations, all 194 original instructions, and all 20 conditional edges; every mutant has zero unsupported executions. It does not add the method to the active registry or establish a signed Widget APK or Android Widget behavior.

The exact 1,085,801-byte [evidence archive](../04-method-mutants-evidence/manifest.json) has SHA-256 `a9c9b9b35b44c4cd56d4529509c3c9f2990255a903dce061fe08da827694ce0e`. All **219 members** were checked against both the frozen checkpoint and source files before publication. The expanded `evidence/` review contains 171 unchanged compact source, log, and report copies, including every authored mutant Java file. The other 48 compiled binary or larger detailed parity artifacts are retained in full in the archive. The [extraction receipt](../04-method-mutants-evidence/extraction-receipt.json) maps every file.

The existing harness retains its first 80 detailed failures plus all failed labels. This publication preserves that original output exactly; it does not claim that an abbreviated detailed-failure list enumerates every mismatch.

```sh
python scripts/assemble_artifact.py work-in-progress/widget-update/04-method-mutants-evidence/manifest.json --verify-only
python scripts/assemble_artifact.py work-in-progress/widget-update/04-method-mutants-evidence/manifest.json
```
