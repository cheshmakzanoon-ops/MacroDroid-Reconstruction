# Hosted source acceptance for the 1,240-method checkpoint

The source job for commit `3a2e6ea9ef9e18d38d5921bb18c77e1c2eb13677` completed successfully at **2026-10-12 03:57:56 UTC**. The fresh host acceptance passed all **16 configured gates**, and the workflow's subsequent comparison confirmed that the rebuilt hybrid APK exactly matches the committed candidate. The independently downloaded artifact matches GitHub's recorded SHA-256. See [job metadata](source-job.json), [the original acceptance result](reports/acceptance-latest.json), and [the independent verification](independent-verification.json).

| Measured check | Result |
| --- | --- |
| Configured host gates | 16 exits of zero; all 16 original log hashes verified |
| Fresh report bindings | All 19 recorded SHA-256 values match preserved files |
| Bounded original/JVM/rebuilt comparison | 188,791 cases across all 1,240 expected methods; zero mismatches or unsupported executions |
| Python controls | 259 individual passing tests; `Ran 259 tests in 8.174s` and `OK` |
| UI deliberate fault controls | All 37 controls rejected their named behavioral case with zero unsupported executions |
| Clean UI restoration | 18,476 cases passed after the controls |
| Input identity | The CI before/after pin is unchanged: `19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183`, with 81,245 files |
| Hybrid APK | 94,683,497 bytes; SHA-256 `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2` |
| Baseline APK | 94,677,674 bytes; SHA-256 `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096` |
| Active constructor owner corrections | Zero in the fresh static and linkage reports |

The supporting [aggregate host result](reports/java-all-path-parity.json), [Python log](reports/python-unit-tests.log), and [UI control report](reports/ui-negative-controls.json) remain unchanged. The publisher checked the input-manifest bytes against the source commit and all 81,245 manifest entries; it did not independently rebuild or rehash every source input during publication. The actual CI input-integrity gate and final unchanged-input check are preserved in their original logs and report.

## Complete artifact payload preservation

GitHub artifact **11725498323** is 127,146,436 bytes with SHA-256 `2feb32620277777c7375cd9d2e3686c03be94f022a0e5d2dbdaeec53d524cbca`. Every one of its 108 payloads was read and hashed. All **106 report files (613,910 bytes)** are copied here exactly, including historical reports that the workflow retained. The two APK payloads match the already committed binary parts at source commit 3a2e6ea. The [manifest](manifest.json) maps every original archive entry to its exact repository bytes or the immutable APK manifest. This preserves all artifact payloads without adding another compressed copy of the same APKs.

The fresh run directory is `reports/acceptance-20261012T033957617151Z/`. Older run directories and the retained two-path UI report are historical evidence; their presence in the artifact does not make them fresh results for this checkpoint. No file is edited to change a failure into a pass. The source snapshot is pinned by commit, path, byte count, SHA-256, and Git blob identity in the manifest.

## Separate Android result and remaining scope

This host acceptance invocation did not execute Android; its availability probe reported blocked. The independent Android job in the same workflow did execute the original and candidate and verified the separate ART constructor allocation probe. Its exact cold launch passed, but its strict intro check found **34 changed pixels on TRIGGERS**. The raw notification surface matched while its aggregate post-intro gate remained failed because intro equality is a prerequisite. See the [complete Android evidence and scoped analysis](../android-ci-3a2e6ea/README.md).

A successful source job therefore does not make the combined workflow, Android visual gate, or whole application 1:1. The reference is the exact supplied APK, as documented in [its provenance](../../SUPPLIED_APK_PROVENANCE.md). Complete high-level source recovery, feature parity, and full runtime parity remain unestablished.
