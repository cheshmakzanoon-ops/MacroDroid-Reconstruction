# Independent review of combined05 full acceptance

The closed combined source/APK capsule passed an independent read-only coherence review. The reviewed capsule is `work-in-progress/combined-recovery/05-full-acceptance/checkpoint.json`, SHA-256 `e4cd0b6af4cf95d7131138b3ad3dab8a070042cea077a80cf83c322168457063`; its prepared source is bound to reviewed checkpoint04 `da0a1a8944e24f2d559083ac7232634be257756a5073ea1755eb5006761191e6`.

**Verdict: approved as scoped closed host, source and APK evidence.** This review ran no build, test suite, APK or Android command and changed no active source, artifact or generated cache. Android acceptance for this particular combined APK remains pending. The prior normal-animation diagnostic uses its separately reviewed 9108 candidate and is not evidence for this new APK.

## Independently checked evidence

| Evidence | Actual verification |
| --- | --- |
| Combined capsule | All 125 declared files, with exact complete path inventory, lengths and SHA-256 hashes |
| Reviewed preparation | All 90 declared checkpoint04 files and the identical archived full input manifest |
| Complete reports archive | All 551 unique regular members, paths, lengths and hashes, streamed without extraction |
| Acceptance outputs | All 22 fresh-report hashes and all sixteen ordered gate logs, each bound to both the readable copy and archive |
| UI negative controls | All 78 retained Java source/class pairs and actual required failed-case labels, with zero unsupported executions and unchanged original method, case and instruction inventories |
| Positive restoration | Complete parsed positive UI report equals the original positive baseline object |
| Python result | All 273 individual success lines and the final 273-test success summary, 17.639 seconds |
| Three-path host result | 193,489 cases over all 1,242 registered bodies, three paths, zero failed or unsupported executions |
| Candidate APK | All twelve ordered part SHA-256 and Git blob SHA1 identities, streamed into the exact aggregate digest; both closed dist APKs also rehashed |

The candidate is exactly **94,683,119 bytes**, SHA-256 `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`. Its source input pin is `b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`. No APK payload, report archive, private signing material, or large source tree is duplicated in this review capsule; their immutable paths and hashes are bound by the review results.

## Complete source coherence

The full current baseline input inventory was independently enumerated and rehashed: **81,245 files / 819,399,298 bytes**, canonical pin `19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183`. The closed candidate was independently enumerated and rehashed: **81,291 files / 819,562,916 bytes**, canonical pin `b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`. Missing or extra pinned-source inputs would reject the review; these are full inventories, not samples.

The exact source delta is **46 additions, 17 changes and zero removals**, totaling 63 files. Every changed file equals its reviewed checkpoint04 source and its candidate manifest entry, while every old/absent file matches the current and repository baseline. Replacing only those 63 entries in the full baseline manifest reconstructs the complete candidate manifest and canonical pin exactly. The 1,240 old registered entries remain unchanged; the only appended bodies are the reviewed plugin-upload `k.invokeSuspend` and Widget update method, yielding 1,242 bodies in 605 classes and ten UI methods.

## Scope and reproduction

`review_closed_combined.py` is the exact independent reviewer source and `01-review-driver.log` is its actual output. The eight JSON receipts preserve complete per-member, fresh-report, gate, mutant, APK-part and delta checks along with full source-rehash timings and the final verdict. It was executed from 06:34:07.691305 to 06:36:58.681825 UTC on 2026-10-12. Its input capsules and project locations remain explicitly bound; replay requires those unchanged source and evidence inputs.

This review confirms evidence coherence and the measured finite host result. It does not establish complete Java/Kotlin recovery, startup or lifecycle parity, animation parity, native behavior, absence of crashes, or whole-application 1:1. The retained historical runtime failures and 26-pixel TRIGGERS difference are unchanged. Existing raw evidence is not normalized or relabeled.
