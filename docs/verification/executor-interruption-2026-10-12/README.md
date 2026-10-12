# Recovery checkpoint after local execution stopped responding

Recorded on 2026-10-12 at 14:13 UTC. This is an inactive status and recovery record.
It does not establish whole-application 1:1 parity or activate any application,
workflow, or pending source capsule.

## Publication boundary

The last commit verified by a local fetch before the interruption was
[46a7e331771da1b6559cf817dc776ebc3024739f](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/commit/46a7e331771da1b6559cf817dc776ebc3024739f),
with tree 7d7f9b88ebcfd65b7f3ef4e4470ebd4d024484a9.
Fresh GitHub API reads during recovery still reported that main head.

That commit preserves the inactive UI report serializer source capsule:
work-in-progress/day-trigger-lookup/14-ui-report-null-preservation.
Its checkpoint is 23,328 bytes, SHA-256
e14ff0e88f121acfa228a349b805f59ce3d703f377718df574021b07471f7ed4.
The publisher previously checked all 104 changed paths, modes, byte counts,
Git object identities, and SHA-256 values against the fetched commit.

A fresh remote source read confirms that the shared Gson initializer remains
unchanged and the final report writer uses
G.newBuilder().serializeNulls().create().toJson(report).
The successor UiParityTests.java is 48,347 bytes, SHA-256
7801ac35079d0aa364c53632d15c8e3ef211a5d956f601cb1c59e8f78edbbb42.
Its boundary evidence preserves the original writer failure and corrected
writer success. This correction has not yet passed a new full combined run.

## Actual completed CI outcomes

| Run | Result and exact limit |
| --- | --- |
| [Numeric ART 38254524859](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38254524859) | Success. The neutral probe executed 1,291 cases per original and accepted numeric candidate APK on Android. All job steps passed. This is method-scope parity, not whole-app parity. |
| [Settings16 38253349348](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38253349348) | Failure with complete evidence. Both APKs completed all 16 observed screens and 15 inputs each. The second onboarding frame differs by 29 pixels; the other 15 full frames and all 16 canonical UI hierarchies agree. No masks were used. |
| [Combined 38248170022](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38248170022) | Failure. Both APK builds and all 16 application acceptance gates passed, then the independent finalizer rejected the UI observer controls. The five absent explicit-null returnIndex fields explain that report mismatch; the historical result remains failed. |
| [Indicator 38252005551](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38252005551) | Incomplete failure. Slots 1 and 2 completed; slot 3 stopped before package removal, installation, or app input when the primary WCDMA level changed from 4 to 3. Slots 4 through 8 were not attempted. This experiment deliberately used the older fixed candidate 5f635, not the current numeric APK. |

Root additionally fetched and parsed the completed numeric, Settings, and
combined job logs through the GitHub connector during the local outage.
This was independent reading of remote reports, not another execution.

The numeric final report states EXACT_NUMERIC_ART_FINAL_VERIFIED, passed true,
43 verified input roles, and 3 retained entry points. Its runtime report is
690,636 bytes, SHA-256
870e62cbdb2c841b6c3f465191f990e208bbf7c2118a304a03189a1cb784a028.
It records verified_without_simulation, both_semantic_case_sets_passed,
strict_diagnostics_passed, and cleanup_complete as true.
The same final report explicitly sets full_runtime_1_to_1_established to false.
The job log records all 6 downloader and 42 wrapper controls passing.

The Settings final report states
EXACT_ALARM_ENABLE_RETURN_SIXTEEN_SCREEN_DIFFERENCE, evidence_valid true,
journey_equal false, and full_runtime_1_to_1_established false.
Its full-frame changed-pixel array is
[0,29,0,0,0,0,0,0,0,0,0,0,0,0,0,0].
Both APKs showed the known post-notification crash and continued afterward;
crash_free_run_established is false. The report observes the Settings switch
checked on and the Navigate up return to the trigger catalogue.
It does not establish the permission API result or trigger configuration.
No macro was saved or executed. Host controls were 6 downloader, 259 journey,
and 10 animation tests.

The combined finalizer logged:
"UI lookup coverage, exact exception scope or observer controls differ".
The strict finalizer remains unchanged. The corrected serializer preserves
the JSON members instead of weakening the comparison.

## Frozen work still pending publication

These are known local checkpoints, not claims that their payloads are in Git.
Preserve the original failures and every frozen capsule when resuming.

| Checkpoint | Exact identity |
| --- | --- |
| Combined run independent review | /dev/shm/macrodroid-combined-run-97322-independent-review/checkpoints/01-literal-failure-independent-review/checkpoint.json ; 10,911 bytes ; SHA-256 89d97a49cd2be5fb23fad7f4272739942150e01f97db338e22276e61e6b9d96e |
| Serializer source peer review | /dev/shm/macrodroid-ui-report-null-independent-review/checkpoints/01-source-boundary-independent-review/checkpoint.json ; 12,939 bytes ; SHA-256 76d4ae18506fec00351bd013306aab8737e54e7b24415875693ea97a9295d82e |
| Tooling capsule 15, inactive historical stage | /dev/shm/macrodroid-ui-report-null-fix/checkpoints/02-reviewed-source-selection-tooling/checkpoint.json ; 13,366 bytes ; SHA-256 ee6343045fb31f28a17b962c0376e4586e432ecbae8b7354c8893a15a2ecae27 |
| Tooling capsule 16, proposed activation source | /dev/shm/macrodroid-ui-report-null-fix/checkpoints/03-pinned-documentation-successor/checkpoint.json ; 29,523 bytes ; SHA-256 6489ec0fee209e0c52082e6e18eebe36e09cd6a809fd1bb337605b1b9478964a |
| Indicator independent review | /dev/shm/indicator-run-analysis-38252005551/checkpoint.json ; SHA-256 b7add0811c5b485dc63bac27c0ee4c7a40bdc6f27b48b6e21ebaba7354c262a1 |
| Ten DayTrigger state-method design | /dev/shm/day-trigger-state-recovery-01/checkpoints/01-ten-method-state-design/checkpoint.json ; 11,239 bytes ; SHA-256 61df149e30608aeef74b424078699e8aa04c00fc7a8a4725bf0aceff2ca29361 |

Tooling capsule 15 passed 159 actual host tests but retained a stale README
snapshot row. Preserve it inactive. Capsule 16 corrects that documentation
and the dependent runtime-manifest/workflow identities. The remaining six
source files are byte-identical to the full-tested stage; six focused
workflow/layout tests passed. Final independent tooling-review closure was
not confirmed after the local service stopped responding. Do not activate
capsule 15 or claim a new combined run passed.

The proposed final runtime manifest is 1,184 bytes, SHA-256
3fb25c64e1b8b03d705d9d8e4c1602af34e2e5516052e4c47f7e8c676303a236.
The proposed final workflow is 6,914 bytes, SHA-256
762375c948d457f34cc4f25230cc1d777e2f4110ff1b30933886d10c32b96354.
The complete corrected logical source inventory is 81,304 entries with
canonical SHA-256
5df3f861db4fd2f372edbad1d4ff6fc3df701ed70adf4737024baffd722dab2c.
Logical derivation is not a substitute for the pending physical CI scan.

The numeric ART independent review had reported PASS after comparing all
1,291 paired results against independent arithmetic, the 60 commands and
120 streams, input identities, strict diagnostics, and cleanup. Its final
freeze receipt was not confirmed in root recovery context. Recover the exact
owned state rather than inventing or repeating that receipt.

Root Settings reader attempt-01 exited 2 with an AssertionError before
reporting changed_pixels. Its failed attempt and executed reader are at
/dev/shm/macrodroid-settings16-root-review/.
The traceback and remaining independent PNG replay could not be inspected
after the file service stopped responding. The CI values above are not a
claim that this independent reader passed.

The ten-state-method capsule contains design only. It does not add recovered
body or executed-case credit. Pending oracle work must narrowly handle
SPUT_OBJECT and reject malformed fractional Number references instead of
treating every Number whose longValue is zero as null. Identity, fresh-array,
mutation, exception, and static-state-isolation cases remain required.

## Interrupted inactive preservation batch

The publisher prepared 210 inactive/metadata paths in:
/dev/shm/macrodroid-transfer-space-20261012/active-source-raw-v2-configuration.json
and /dev/shm/macrodroid-transfer-space-20261012/active-source-raw-v2-export.

Twelve of seventeen new blobs had confirmed successful uploads before the
interruption. No tree, commit, or branch update was made for that batch.
Its in-memory upload bookkeeping was lost at continuation; recover from the
preserved export files and actual remote object responses. Do not claim
dangling uploaded blobs constitute committed or pushed checkpoints.

The batch covers the complete successful active-source CI artifact through
23 exact parts, its 1,304-member inventory and selected reports, numeric ART
activation receipts, the state-method design, and the serializer peer review.

## Sole retained artifact inputs

All paths below refer to already downloaded inputs. Do not download them again.

| Run | Local ZIP | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Active numeric source 38247941263 | /dev/shm/macrodroid-transfer-space-20261012/active-numeric-source-run-38247941263/artifact.zip | 188572653 | 4824e07658f0e5a808a9dc0b10615b030e3d5f3d030b0fa4ff40096060a34159 |
| Numeric ART 38254524859 | /dev/shm/macrodroid-transfer-space-20261012/numeric-art-run-38254524859/artifact.zip | 19878082 | 17549c58cc48e365a1033829851b6944b22e85ee42cee7c6c92bbf1eb2a6b38e |
| Settings16 38253349348 | /dev/shm/macrodroid-transfer-space-20261012/settings-run-38253349348/artifact.zip | 76017011 | 8e0c53c024805fd5c4cd72ad9ee24133bb4b1d0fc19a23645c97ddb484b171f5 |
| Combined 38248170022 | /dev/shm/macrodroid-transfer-space-20261012/combined-run-38248170022/artifact.zip | 241915713 | 3ad31b610aa01ea4b0490fe9c2238e9a919f5e38be3df923ec453e3afc117d16 |
| Indicator 38252005551 | /dev/shm/macrodroid-transfer-space-20261012/indicator-run-38252005551/artifact.zip | 11282767 | cc05c94fc7cdfd75587dabd1fc9a65b96aa85932e80e57df850993b5597fa49d |

Settings already has a closed extraction inventory for all 3,935 members.
The numeric ART review streamed all 7,963 members and retained only 228
non-simulated review inputs. The combined review streamed all 6,115 members.
The indicator extraction and independent analysis cover all 4,417 members.
Do not print the retained ephemeral ADB public-key setting in summaries.
The previous scan found no private-key header or GitHub token.

The last measured free space was approximately 1 GB in tmpfs and 92 MB on
the overlay, before the outage. This is not a current measurement.
Preserve frozen capsules, original raw captures, and unrelated workspace
contents when reclaiming owned reproducible temporary copies.

## Resume sequence

1. Restore supported local command/file access, then inspect the exact owned
   pending processes and receipts. Do not infer success from an interrupted
   orchestration call.
2. Reconcile remote main and any already uploaded objects with the frozen
   export. Finish inactive preservation through expected-head fast-forwards,
   then fetch and verify exact payload bytes, modes, Git OIDs, and SHA-256.
3. Close the final tooling peer review and preserve capsules 15, 16 and that
   review. Activate only the six exact mappings from capsule 16 after closure.
   Allow one automatic fresh combined acceptance run; do not duplicate it.
   The strict finalizer and full physical source verification must pass before
   application promotion.
4. Finish and preserve the numeric ART review receipt and the Settings reader
   correction/replay. Preserve the failed Settings reader attempt unchanged.
5. Recover the ten state methods after design review, using the corrected
   combined parent and the explicit oracle/identity safeguards above.
6. Extend the Settings journey by one observed Day/Time tap after return.
   Its current terminal surface is AddTriggerActivity with the Day/Time
   label visible at bounds [102,609][206,642]. Capture the resulting app
   surface without assuming the configuration dialog or saving a macro.
7. Diagnose the actual pinned modem backend before another indicator run.
   The current setup selects signal profile 4 once and confirms primary
   level 4 for at least 15 seconds; later per-slot checks correctly rejected
   a drift to level 3. That setup does not prove the radio remains stable
   throughout eight slots. Review a bounded explicit successor protocol and
   retain all full-frame differences.

The current promoted application remains the 1,243-body/605-class numeric
hybrid from 8db1fca4f03532ee2e5a8791fde7ea18126c237f.
Its APK is 94,683,136 bytes, SHA-256
0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd.
The original APK is 95,725,918 bytes, SHA-256
84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800.
This record promotes neither source nor an APK.

## Local service interruption and this record

The publisher and root observed local Bash invocations fail to return a
result or process session, including a plain directory check. Root also
observed the direct local image reader stop returning. Completed-process
lookup and GitHub connector reads still responded. Root closed its two
read-only orchestration cells. The Settings process 20520 was already
closed and reported the reader failure described above.

No filesystem permission, credential, access-control rule, or unrelated
process was changed to work around the interruption. No extra Android
execution, build, macro, or CI dispatch was started.

Root temporarily took ownership of this one inactive recovery file after
interrupting the publisher turn and directing it not to update refs.
Publication of this file requires an expected-head, non-forced branch update
and exact GitHub API readback with a one-file commit diff.
That verification is remote readback, not a local Git fetch.
All pending source/artifact publication remains explicitly pending.
