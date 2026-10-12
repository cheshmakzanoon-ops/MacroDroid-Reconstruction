# Widget original/JVM proof, inactive checkpoint

The final isolated Widget study passed **2,342 original/JVM cases**, 198 independent expectations, and every one of the original method's **194 instructions and 20 conditional edges**, with zero mismatches or unsupported executions. These are two host execution paths. The method is not registered in the active project, and this checkpoint does not claim a signed Widget APK or Widget execution on Android. The [full study](evidence/widget-study-04-final/study.json), [parity report](evidence/widget-study-04-final/parity.json), and [harness documentation](WIDGET_HARNESS.md) retain the exact scope.

The exact [checkpoint](checkpoint.json) binds 29 source, fixture, documentation, and narrow merge-patch files. Source here remains inactive and must not overwrite later root or plugin-upload changes without the recorded baseline checks. The sibling [evidence manifest](../04-original-jvm-evidence/manifest.json) preserves every byte of the 2,413,234-byte original archive (SHA-256 `61d87b53993fe0a7b121c09dc26121989d0501d1bfbbabb0b2bdc8d5f4949877`).

All **3,290 archive members** were compared to both frozen hashes and source files before publication. They include four complete 811-file private input copies, compiled class archives, and the exact failed and passing logs. `evidence/` exposes all 46 compact non-input reports and archives unchanged; the other 3244 exact input copies are retained in full in the archive. [The extraction receipt](../04-original-jvm-evidence/extraction-receipt.json) maps every member.

The first study failed with unsupported `AND_INT`; the expanded study then exposed one return-value mismatch. Both remain failed in their original reports. The two later positive reports do not rewrite these earlier findings. Separate method-only controls and signed integration were pending at freeze time.

```sh
python scripts/assemble_artifact.py work-in-progress/widget-update/04-original-jvm-evidence/manifest.json --verify-only
python scripts/assemble_artifact.py work-in-progress/widget-update/04-original-jvm-evidence/manifest.json
```
