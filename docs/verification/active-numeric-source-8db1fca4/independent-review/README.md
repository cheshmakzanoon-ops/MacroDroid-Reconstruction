# Independent review of the active numeric source build

**The active numeric source job passes its recorded 16-gate acceptance, and its fresh hybrid APK is byte-identical to the committed `0762aad9…` candidate.** This is a review of the closed source-build evidence. The sibling Android job failed, so this capsule does not describe the entire workflow or full runtime parity as successful.

## Exact evidence and review scope

The reviewed run is `38247941263`, head `8db1fca4f03532ee2e5a8791fde7ea18126c237f`. GitHub's retained job record identifies source job `114806466819` as successful and Android job `114806467130` as failed. The source acceptance ran from `2026-10-12T12:17:14.216867Z` to `2026-10-12T12:47:53.253608Z`; the source job's comparison step also succeeded. The Android failure cause is outside this source artifact review.

The publisher downloaded the sole source artifact ZIP. The independent collector made one streaming content pass over that existing file, without extracting either APK:

| Evidence | Exact identity |
|---|---|
| Raw artifact ZIP | 188,572,653 bytes; SHA-256 `4824e07658f0e5a808a9dc0b10615b030e3d5f3d030b0fa4ff40096060a34159` |
| Complete ZIP inventory | 1,304 members; 456,205,098 uncompressed bytes; each member has SHA-256, verified CRC32, length, mode and ZIP metadata |
| Fresh baseline APK | 94,677,674 bytes; SHA-256 `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096` |
| Fresh hybrid APK | 94,683,136 bytes; SHA-256 `0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd` |
| Promoted source proposal | Checkpoint SHA-256 `0695be31f63f25952d8236d403206a2b292eef4b4e28ab7fd071c045f0401e14` |
| Current build-input snapshot | 81,298 entries; canonical SHA-256 `f8fc1cadac8213468e42ac99a2cd5d807827dcdeee25166b8025620ff39a6545` |

ZipFile first read 134,626 bytes of central metadata. Thereafter the physical member-order content pass had zero overlapping reads; container gaps and the final central directory were included in the same full-archive digest. The collector checked stable device/inode/size/mtime/ctime before and after the pass. It retained 207 compact files, 20,302,103 original bytes and 10,723,485 stored bytes; the large input inventory is stored as a lossless gzip copy. It did not materialize an APK, build directory or application tree. The complete inventory is `collection-01/zip-member-inventory.json`; retained-copy identities are `collection-01/retained-file-bindings.json`.

The subsequent analyzer reads only these retained files, the inventory and the frozen promotion proposal. It does not reread the raw ZIP. All files read by each closed attempt have complete before/after hash and mode records. The review ran no build, compiler, JVM application test, host suite or Android command.

## Fresh source and committed-candidate binding

The exact bytes of the produced release-input snapshot equal the frozen promotion proposal's snapshot. The analyzer independently recalculated the canonical hash of all 81,298 inventory entries and compared the 19 promoted source rows against their exact size/SHA-256 declarations. The acceptance records the same snapshot before and after execution and reports unchanged inputs. The ordinary lookup runner is absent from this numeric-only snapshot; the separate combined lookup run has not been credited here.

The current artifact manifest in the approved proposal and the independently streamed fresh hybrid APK both identify the exact 94,683,136-byte `0762aad9…` payload. The source artifact contains the build inventory and producer reports, not all 81,298 source files. Therefore this review independently verifies the complete inventory, its exact promotion binding and the actual output APK bytes; it does not claim a new physical rehash of every hosted source file.

The ZIP contains older reports. Only `acceptance-20261012T121707487120Z/result.json`, its byte-identical `acceptance-latest.json`, all 16 exact log hashes and all 23 `fresh_evidence_sha256` report bindings determine the current conclusions. The retained `release-summary-v9.json` still reports 1,237 methods from October 11 and is explicitly excluded from current metrics.

## Actual source-gate findings

All 16 commands returned literal integer zero and passed, in the prescribed order. The UI mutation command retains its 5,400-second bound; every other gate retains 1,200 seconds. The signed source-edit gate ran and the final positive suite followed it.

| Gate | Recorded seconds |
|---|---:|
| Input integrity | 6.679 |
| Baseline build | 80.987 |
| Hybrid build | 54.019 |
| Baseline code | 37.870 |
| Hybrid code | 39.028 |
| Baseline resources | 10.150 |
| Hybrid resources | 7.697 |
| Positive host tests | 118.238 |
| Reference status | 0.315 |
| Engine deliberate faults | 13.826 |
| UI deliberate faults | 1,093.598 |
| Core deliberate faults | 16.860 |
| Environment deliberate faults | 63.868 |
| Legacy deliberate fault | 114.126 |
| Signed source edit | 58.581 |
| Final positive host tests | 116.467 |

The five suite inventories form an exact disjoint partition of the 1,243 registered method keys. Their actual 194,780 cases report zero mismatches and zero unsupported executions across original DEX, recovered Java and rebuilt DEX. Every suite binds the same original fixture and actual signed hybrid APK.

| Suite | Cases | Registered methods |
|---|---:|---:|
| Legacy | 95,262 | 1,195 |
| Core | 34,753 | 10 |
| Environment | 30,684 | 15 |
| Engine | 9,616 | 12 |
| UI | 24,465 | 11 |
| Total | 194,780 | 1,243 |

The final unit-test log contains 308 distinct passing test names and the literal `Ran 308 tests in 11.284s` / `OK` ending. The integration report records 605 recovered classes, 1,243 bodies and zero runtime stubs included. The one existing Widget constructor-owner correction remains explicitly recorded.

Full code comparison reports 71,267 classes and 349,972 methods: the baseline is unchanged, while the hybrid has exactly 605 registered changed classes and 1,243 registered changed methods, with no missing, extra, unexpected, opaque-payload or alignment differences. Each resource report covers 7,212 files, 23,854 resource IDs and 22 native libraries. It records 7,211 byte-identical files and the one existing equivalent enum-order case, with no unexpected changes.

The fresh static proof reports 1,119 constant methods, 675 member references, 465 app-member resolutions, no new external references and no errors. The linkage report has no errors but retains its stated limits: it is a bounded declaration/access check, not ART verification. The reference marker inventory still has 21 unreplaced markers out of 42; the reference Java tree is not claimed to be a compilable application.

## Deliberate faults and restoration

All 91 UI Java controls record nonzero mismatch detection, required-case rejection, zero unsupported executions, unchanged source/fixture/APK and unchanged original instruction inventory. The independent ZIP inventory binds every retained mutant source and class hash. This review checks their recorded result rows and exact mutant byte identities; it does not reparse all 91 larger failure-body reports. The original and restored UI JSON objects are exactly equal. Final UI output adds only its three fixture/APK provenance fields; raw JSON serialization is not claimed byte-identical for this UI restoration.

The numeric runner's 17 literal child-command rows have the expected role order and exits, each with a 120-second timeout. The reviewer checked 34 raw stdout/stderr identities, 34 empty filesystem-witness identities, exclusive creation, recorded integer clocks, chronological invocation boundaries, one-link regular-file declarations, unique retained inode identities and the exact filesystem bracket. These are independently verified archived receipt fields and stream bytes; relocated archived evidence cannot establish new live filesystem inode or ctime observations. Individual child rows do not record cwd, and this review does not invent one.

For the 1,291 numeric inputs, coverage is complete over 25 original primary instructions plus seven original getter instructions (32 total), and 18 rebuilt primary instructions plus the same seven getter instructions (25 total), with all four conditional edges on each path. The two real D8 faults produce 509 and 406 mismatches, respectively, without unsupported operations. Both provenance controls reject. The positive signed-primary instruction JSON equals the transplanted-primary JSON byte for byte, and the final numeric positive restoration is byte-identical to its original positive report.

The original getter dependencies remain separate from the one recovered primary method. The null-entry case retains exact `NullPointerException` type with raw messages preserved under its documented class-only comparison scope. This source evidence does not turn host exception-message behavior into an Android claim.

The signed source-edit control records exactly one changed DEX payload entry and one changed method in the relevant partition, detects 113 failing cases, rejects its required pause case and leaves the distributed APK and release inputs unchanged. Its experimental APK is expressly not distributed. No independent hash claim is made for an absent experimental APK file.

## Preserved reviewer attempts and practical limit

The first ad hoc summary assumed a numeric command used `label`; its actual field is `name`. The first retained analyzer later assumed the engine suite had `androidRuntime`, whereas that suite uses an exact textual scope explicitly ending `not Android runtime`. Both reviewer-only mistakes are preserved. The second analyzer reads the actual engine schema and closed successfully at `2026-10-12T13:05:43.326167Z`, with all read inputs unchanged. Neither mistake changed the raw evidence or an application gate.

The source acceptance's Android environment probe returned code 2 / `BLOCKED`; it did not execute an Android runtime. Separately, GitHub records a failed sibling Android job. These facts remain distinct. The conclusion is successful bounded source acceptance and exact committed-candidate reproduction, with **full runtime 1:1 still false**.
