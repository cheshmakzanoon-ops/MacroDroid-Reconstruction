# Separate combined DayTrigger host acceptance: design for review

This proposes one additive hosted workflow for the exact numeric and lookup source combination. It does not activate a workflow, change the current application, materialize an application tree, build or sign an APK, or claim a completed combined run. The existing isolated numeric workflow remains independent.

The proposal derives from the frozen numeric tooling checkpoint `815612f827f1b0d2bcec90bbb1ae8a35a8c76ced8f6b5f44cf413bc40b81f493`. The final application inputs combine Numeric08 checkpoint `d9ddd3e0f692c66e2cd47870ff3cf95bfa0a2b1cd50fc2fd55a3c09e66df9bcf`, Lookup08 dependency merge `56aa7bfc05286d9fc474d24e6afc33fbd3a664e9dc731f70912df1a9e375b350`, and the two-path Lookup09 recorder successor `87c2a01a627590b62017eae8145db92d1a7593d5cf127114a9812ec13cd756f5`. Their historical failures and narrower completed proofs remain unchanged.

## 1. What was independently checked for this design

The source-only collector in `evidence/22-combined-host-design-source/executed-collector.py` verified the five exact ancestor checkpoints, all nine proposed parent tooling inputs, both complete manifest transformations, all 25 final application payloads, the original-fixture method definitions, and the complete prepared 101-mutation inventory. All 125 read-input identities were unchanged at completion. Preparing mutations computes strings and hashes; it does not compile or execute a mutant.

The collector parsed the actual fixture's DEX class-data method definitions. Its exact key set equals the 1,244 registered methods plus the five explicitly uncredited getters; it contains 1,249 bodies in 607 classes. It also bound the existing 371-case lookup proof's raw report, configuration and production method-body record back to the immutable Lookup07 evidence inventory. Those prior cases were not rerun for this design.

The first collector attempt correctly stopped on an overly broad assumption that every existing test name remained identical. `tests/test_v9.py` changes `test_exact_eleven_methods_and_classes` to `test_exact_twelve_methods_and_eleven_classes`; the file still has 48 tests. The second attempt permits only that exact rename and records the before/after names. Both actual attempts are retained. This was a design-collector assertion failure, not an application failure.

The initial interactive manifest inspection also made a schema mistake by treating `files` as a list; the snapshot uses an integer `files` count and an `entries` object. That inspection traceback is retained separately. The closed collector validates the complete actual schema through the pinned `inputs.validate_snapshot` implementation.

No whole-project physical scan, Python test suite, Java execution, D8 invocation or acceptance gate was run here. The statements below describe requirements for a future run unless explicitly identified as source inspection or a prior measured result.

## 2. Preserve the two preparation boundaries

Start from fixed baseline commit `dbcad968c5c3e8f084205393a6c0d2d06a203c71`, not a moving current checkout. Use fixed Numeric08 commit `811f979eda1b937917c18defef38455c49a59062`. The publisher must supply a fixed commit containing both frozen lookup capsules before the new workflow can be made runnable; checkpoint hashes alone are not a checkout ref.

| Boundary | Required operation | Complete input count | Snapshot SHA-256 |
|---|---|---:|---|
| Baseline | Materialize the pinned 1,242-method project and physically verify every included input | 81,291 | `b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553` |
| Numeric | Check all 19 Numeric08 before hashes/absence guards, apply the exact 19 payloads, then physically verify the complete intermediate tree | 81,298 | `f8fc1cadac8213468e42ac99a2cd5d807827dcdeee25166b8025620ff39a6545` |
| Combined | Check all 21 final lookup before hashes/absence guards against that intermediate tree, apply the exact final 21 payloads, then physically verify the complete final tree | 81,304 | `b981dd67fd84ddf8dc026b2aed0ede7f1770c48ef64acc9009f5eaa076f34a0c` |

The corresponding complete manifest identities are:

| Manifest | Bytes | SHA-256 |
|---|---:|---|
| Baseline | 14,502,990 | `ca3bed290f18a378c7a3d6cc70d924c8d6ec85481e236b4e7561c31fedafdfbe` |
| Numeric | 14,504,095 | `896f3eb29dc832eb245fee8dcb70b0e8c8935c9635bf1ccc54c09987b26c91c6` |
| Combined | 14,505,034 | `cd89966dae610579966c7d0ebfd62861ce3468c43c25427c738b369d98727b1a` |

Numeric08 adds seven inputs and the lookup delta adds six. The union contains **25 distinct final application paths and 13 new inputs**. Twelve existing baseline entries change; all other 81,279 existing entries remain byte-identical. This union is a descriptive inventory, not a replacement for the two before-hash boundaries. The actual pinned `inputs.derive` rejected applying the final lookup delta directly to the 1,242-method baseline; the exact rejection is retained in `direct-baseline-rejection.json`.

The four numeric-only final paths must remain explicitly pinned:

| Numeric-only path | Bytes | SHA-256 |
|---|---:|---|
| `source/java/recovered/ui/DayTriggerValueMethods.java` | 651 | `b99984c0ca9128f9def8658d874f98d9a8e4529433d0f76f7f86e9e8299cc792` |
| `tests/fixtures/day-numeric-mutants.json` | 6,366 | `1e008b16aa92c2e7c42aa88ecea9913391ee4f41b95ed73cd7a4ea17c914f4de` |
| `tests/java/DayNumericControlHarness.java` | 10,394 | `01db7b22f414527e516b9e7da1685e778a13c737c719358f86defe901ebbb4b9` |
| `tools/src/ExtractOracle.java` | 7,703 | `5ebe80c06ddd26a5d495d2a3a3c0bd4056846b231e30127cba90026ec26842ae` |

The final lookup payload resolver uses nineteen unchanged `project/` files from Lookup08 and only `day_lookup_dex_controls.py` plus `tests/test_day_lookup.py` from Lookup09. The exact 21-row manifest retains the Numeric08 before identity for each changed existing file and a true absence requirement for each new file. Its canonical source role remains `project/<path>`; the resolver separately records the immutable capsule and physical payload path. It must reject unlisted substitutions, duplicate paths, a missing successor file, or use of an older recorder.

Retain the exact baseline, intermediate and final manifests; both source change lists; each source capsule checkpoint; all executed overlay payloads; the actual complete before/intermediate/after scan receipts; and the materializer command/streams. Keep the parent preparation rule that verifies all before states before starting that stage's changes. Use fresh owned workspace/output roots outside the input checkouts, retain displaced historical reports/APKs separately, and create fresh reports/dist only after the final source scan. A failed stage remains failed with its actual partial preparation evidence.

`two-stage-source-contract.json` is the complete machine-readable design contract. Its manifest derivations are executed checks; its required physical full-tree scans remain pending.

## 3. Smallest proposed tooling surface

Add nine files in a new namespace. Do not edit any `tools/day_numeric_acceptance/` file or the isolated numeric workflow.

| New path | Necessary change from the frozen numeric tool |
|---|---|
| `.github/workflows/day-trigger-wip-acceptance.yml` | Dedicated trigger, concurrency, artifact name and workspace; add the fixed lookup-capsule checkout; invoke the new namespace |
| `tools/day_trigger_acceptance/README.md` | Exact combined scope, two boundaries, derived counts, artifacts and remaining limits |
| `tools/day_trigger_acceptance/inputs.py` | Retain generic strict path/JSON/hash/snapshot utilities; add the explicit second source contract and final 21-payload resolver |
| `tools/day_trigger_acceptance/pins.json` | Pin both source stages, all ancestor/source identities, final snapshot, counts, 101 prepared controls and both method-proof contracts |
| `tools/day_trigger_acceptance/prepare.py` | Retain fresh materialization; verify/apply/scan Numeric19 and then Lookup21 separately; retain both receipts |
| `tools/day_trigger_acceptance/run_acceptance.py` | Change namespace/preparation contract and descriptive fields; retain subprocess recording and owned process-group cleanup verbatim |
| `tools/day_trigger_acceptance/runtime-files.json` | Exact inventory of the seven sibling tooling files; the workflow separately pins this inventory's bytes |
| `tools/day_trigger_acceptance/test_day_trigger_acceptance.py` | Adapt the parent control fixtures to the combined fixed contract; preserve every parent guard and add the bounded combined-specific controls below |
| `tools/day_trigger_acceptance/verify.py` | Derive combined totals; verify both source stages; retain numeric checks; add exact lookup proof/19-command checks and cross-method preservation |

No additional application source path is required by this design. The application-side 16-gate runner already lists the lookup report; the UI control runner already requires 101 compiled faults followed by both method-control runners. Its final literal status is `ALL_101_JAVA_AND_FOUR_DAY_DEX_FAULTS_DETECTED_EXACT_POSITIVE_RESTORED`.

Retain the parent command-stream schema-2 implementation and verifier without weakening their file ownership or clock requirements. The shared numeric recorder in the application remains SHA-256 `2608a9a0a9d5b44627595fcbb696f2ec3f70213eb6af88a7282ec818d53e92f4`. The lookup runner is `0b72325dbdaf60525f07a7b72708b9096d1e585ef5e1601332ceaac9aa67c8c9`; it directly uses `numeric.CommandStreamEvidence` and `numeric.command_clock`, with its additional final-row fields. Record exact before/after function text and AST comparisons for the unchanged generic utilities, shared recorder, cleanup code and numeric verification logic when implementation is authored.

The parent has 92 closed tooling tests. Their guards must all remain exercised after fixture adaptation. Do not predeclare the new tooling test total; derive it from actual discovery and record the full execution log after adding the new guards. The separate project's 357 expected tests below are a different inventory.

## 4. Counts derived from the final source

| Item | Numeric parent | Combined expectation | Basis |
|---|---:|---:|---|
| Registered recovered bodies | 1,243 | **1,244** | Exact registry key set |
| Target application classes | 605 | **605** | Unique registry targets |
| UI recovered methods/classes | 11 / 11 | **12 / 11** | Exact UI registry |
| Original fixture bodies/classes | 1,246 / 607 | **1,249 / 607** | Actual fixture class-data definitions |
| Uncredited original dependencies | 3 | **5** | Three numeric getters plus two lookup getters |
| UI cases per full positive run | 24,465 | **24,836** | Add the frozen 371-case lookup inventory |
| All five suites per full positive run | 194,780 | **195,151** | Exact unchanged four suites plus UI |
| Project Python tests | 308 | **357 expected** | Existing test counts unchanged; 49 added lookup tests |
| Actual Java UI faults | 91 | **101 required** | Exact old 91-entry prefix plus ten lookup faults |
| Actual method DEX faults | 2 | **4 required** | Two numeric and two lookup faults |
| Method provenance rejections | 2 | **4 required** | Original-as-rebuilt and wrong-helper for each method |
| Fresh top-level evidence reports | 23 | **24 required** | Add `day-lookup-dex-controls.json` |

The four unchanged suite case counts are legacy 95,262, core 34,753, environment 30,684 and engine 9,616. Require the exact five-suite method partition, three execution paths and zero failures/unsupported executions. Each full positive invocation must independently meet these totals; do not sum its two invocations into a larger unique-case claim.

The future Python total is a source-derived expectation. Full project discovery/execution has not happened for this source. The retained AST count record shows `test_build.py` 52→52, `test_day_numeric.py` 35→35, `test_v9.py` 48→48 and new `test_day_lookup.py` 0→49. The final job must verify the actual complete successful test listing and count, without skips or an arithmetic-only success claim.

The fixture is 531,256 bytes, SHA-256 `410ebd6bd6455863812b1c3b34148f6717c6824cb2bdf8d8490323832543f802`. The five-getter declaration is 2,232 bytes, SHA-256 `159061ce552e3364c113f28e72e5a4c1bc091a21153d0d5e0a793d2f773b0229`. Getters remain test-only dependencies and earn no recovery credit.

## 5. Preserve all sixteen acceptance gates

Use the unchanged order from the actual final `acceptance.py`:

1. Input integrity.
2. Baseline APK build.
3. Hybrid APK build.
4. Baseline code roundtrip.
5. Hybrid code roundtrip.
6. Baseline resource comparison.
7. Hybrid resource comparison.
8. First full positive host test run with `--three-way`.
9. Fresh reference-status inventory.
10. Engine fault controls.
11. All 101 UI Java faults, numeric DEX controls and lookup DEX controls, with exact restoration.
12. Core fault controls.
13. Environment fault controls.
14. Legacy fault control.
15. Actual signed source-edit probe.
16. Final full positive host test run with `--three-way`.

Do not pass `--skip-edit-probe`. Keep each UI mutant and its positive restoration bounded at 300 seconds, each method-control child at 120 seconds, the UI gate at 5,400 seconds, every other gate at 1,200 seconds, the owned outer acceptance child at 6,600 seconds, and the hosted job at 120 minutes. Materialization remains bounded at 900 seconds. These are inherited limits, not a prediction that the expanded run will finish. A timeout is retained as a failure; any later bound change needs the actual elapsed evidence and a separate review.

The exact argument vectors, method-control order and 24 report names are in `proposed-command-and-report-contract.json`. Require all 16 actual subprocesses in order, actual zero exits, complete fresh report hashes, both actual APK bindings, a complete final 81,304-input recheck, and unskipped source editing. The preserved project Android probe is an availability check only; a blocked/no-device result cannot become an Android success claim.

## 6. Bind both ordinary methods to the actual signed APK

The class registry contains exactly three DayTrigger mappings: the pre-existing `requiresScheduleExactAlarm()Z` constant, recovered `r0(DictionaryEntry)I`, and recovered `p0(Dictionary,String)DictionaryEntry`. Preserve the complete constant mapping byte-for-byte. Only the two latter methods are new ordinary-method work in this combined proof.

The complete code/resource gates bind the exact newly signed hybrid. The independent method verifier must also require that each positive micro-transplant's inspected instructions equal that method's instructions read from the actual signed `classes3.dex` member. Verify the APK has exactly one such member and its bytes equal the local DEX used by the harness. Both methods and all five getter dependencies must bind to this same observed APK identity. Do not fill in a predicted new APK size or hash; measure it only after the actual build.

Each standalone micro-DEX intentionally replaces only its own target method in the preserved original class. It therefore leaves the other 33 original methods/text unchanged and contains no constructor-owner correction. Its full class is not expected to equal the signed class, which legitimately contains all three registered mappings. The signed comparison is to each primary method's instructions; the complete application code gate separately validates the registered class changes.

Retain the numeric verifier's positive production-pipeline identity, 1,291 three-path cases, 32/32 original and 25/25 rebuilt instructions, four/four conditional edges, 13 compiled Java faults, two actual DEX faults, two provenance rejections, 23 loaded runtime-class identities, and byte-exact restoration. The merged numeric source already understands the combined five-row declaration while returning only its unchanged three consumer getters.

Add an explicit lookup verifier requiring:

- The exact lookup method and source/helper identities; the frozen 371-input hash `02dd119966191ad2f56937eda28e63644979080158465ffb13767710f34e32e6`; zero mismatches, unsupported executions or expected-result failures; all three paths.
- Complete original 26/26 and rebuilt 23/23 instruction coverage, including the two original field getters, and all four conditional edges per path. No getter recovery credit or offset exemptions.
- The actual positive compiler/transplant bindings and the signed primary instruction comparison. The frozen source-only proposal retains the earlier measured lookup pipeline pins for exact future comparison; any compiler/body difference must fail for review.
- The exact 26-class loaded-runtime inventory, bound to actual current class files and configuration; preserve raw configuration and loaded origins for every execution. Retain all original/helper/fixture/APK/class identities before and after.
- Ten distinct compiled Java faults, linked to the actual 101-control suite's retained mutant source and class. Preserve the measured required labels and failure counts `[127, 3, 2, 3, 233, 1, 369, 233, 25, 6]` in their catalog order.
- Actual rebuilt DEX faults `case-sensitive` and `last-match`, producing 127 and 233 mismatches respectively, expected exit 3, exact required labels and unchanged positive original/JVM observations. Only the target-DEX configuration role may change.
- Original-as-rebuilt and wrong-helper provenance attempts each actually exit 1, retain the expected rejection reason and altered configuration, and produce no accepted result file. Keep these distinct from application cases.
- Raw positive and final-restoration JSON byte equality, independently recomputed normalized outcome equality, and source/class/fixture/APK identity stability.
- Raw `numeric-before-instructions.json` and `numeric-after-instructions.json` equality, both bound to `r0` in the same signed DEX. The lookup study may not alter the already recovered numeric method.

Lookup exception comparison remains narrow: only generated diagnostic text for seven named null-receiver cases is excluded from equality; every raw message stays in evidence. The names are `dictionary-null`, `entries-null`, `iterator-null`, `null-first-entry`, `null-query-and-null-key`, `null-query-nonempty`, and `null-second-entry`. Injected exception type, message, object identity and ordered trace still compare exactly, including when a case label resembles an excluded case. Keep the five existing observer-record controls separate and uncredited. This scope does not establish exhaustive cross-runtime Unicode or platform exception-message equivalence.

## 7. Exact schema-2 receipt requirements

There are **17 numeric and 19 lookup production child commands**, hence **72 method-command stdout/stderr streams**. The lookup sequence adds its numeric-before and numeric-after inspections to the analogous pipeline/positive/fault/provenance/restoration sequence. The outer wrapper separately retains its three process receipts: `java -version`, `javac -version`, and full acceptance.

Reconstruct the command vectors from the pinned source/roles, never from recorded argv alone. Require exact Java executable, JVM policy, classpath order, D8 options, smali/baksmali class names, target method, source/config/output paths, expected exit, timeout and command order. Do not accept just 19 rows of arbitrary successful commands.

The individual numeric and lookup rows do **not** independently record `cwd`. Bind their working directory through the byte-pinned producer AST (`subprocess.run(..., cwd=root)` after `root = root.resolve()`), the exact UI caller using `build.ROOT`, the pinned build module's resolved project root, and the outer acceptance receipt's explicit project cwd. Do not invent a row field or label this source-derived binding an independent child observation. The parent reviewed and accepted this distinction for the closed Lookup09 source; that source and its final input snapshot remain unchanged.

For both methods, reuse the parent verifier's schema-2 checks: literal integer Unix/monotonic clocks with matching UTC text; successful exclusive creation of distinct regular single-link stdout/stderr files; observed fstat/path/device/inode ownership; exact stream hashes and sizes; lifecycle chronology; same-directory filesystem witnesses; the first valid bracket under the bounded 16-attempt/5-ms policy; and checks against the live files before upload. Retain all witnesses and raw streams in the artifact. Downloaded copies cannot recreate the original live inode checks, so later archive review verifies the actual job receipt plus exact bytes rather than asserting new inode equality.

The lookup report must additionally have `schema: 2`, `command_stream_evidence_schema: 2` and the exact provider string `day_numeric_dex_controls.CommandStreamEvidence`. For each successfully completed production command, require `stream_context_entered: true`, `timed_out: false`, `error_type: null`, `error: null`, and the exact `expected_returncode` as well as the actual return code. Expected fault exits 3 and provenance exits 1 are successful recorder observations because the producer expected those codes.

Validate each actual `recording_finalized` clock with the same strict clock parser: shared `stream_evidence.invocation_finished` must precede or equal shared context `finished`, which must precede or equal wrapper finalization, which must precede or equal the next command start and overall lookup report completion in both clock domains. Do not substitute that clock for a missing stream-context finish. Keep exact report start/finish nesting within the owned acceptance invocation. A failed stream open, child launch, timeout, flush or close produces a failed command row; missing finalization or a populated error field cannot pass the success verifier.

The prior sixteen production-recorder tests already show finalized failed rows survive the measured failures, preserve the actual primary exception and close owned handles. They also show that hardlink and inode-substitution attempts are rejected and actual timed-out children are reaped. All those runner attempts intentionally left acceptance failed. They do not substitute for executing the 19 real production commands in the future signed run, nor do they prove recovery from an unwritable report destination.

## 8. Workflow and artifact contract

Use a new workflow that triggers only on its own file and `tools/day_trigger_acceptance/**`, with manual dispatch available. Retain `contents: read`, credentials-disabled shallow sparse checkouts and a dedicated concurrency group with cancellation disabled. Separate source checkouts are: exact triggering tooling, fixed baseline, fixed Numeric08 capsule and the fixed commit containing Lookup08/09. Only baseline inputs are materialized into the application workspace.

Retain the parent's exact action pins: checkout `11d5960a326750d5838078e36cf38b85af677262`, setup-java `cf277c60eb25467037889841efdb72551f06f6c3`, and upload-artifact `ea165f8d65b6e75b540449e92b4886f43607fa02`. Use the same Ubuntu 24.04/Temurin 21 setup and record the actual JDK/VM identities and effective UI policy. Verify the new seven-file runtime inventory and the workflow-pinned inventory SHA before executing any new tooling. The new runtime hash is unknown until the implementation is frozen; it must not be guessed or copied from the parent.

Run the bounded tooling controls first; then preparation; the owned full acceptance child; independent final verification whenever tooling preflight passed, including after failures; and an always-run upload. The upload must include hidden files only under the explicitly owned evidence/input roots, error if no files exist, and retain 30 days. Keep the three input checkouts and unrelated runner paths out of the upload.

Retain the full owned preparation/execution/final-verification evidence, both source-boundary receipts, 24 named fresh reports, every gate log, both signed APKs, the 101 Java mutant sources/classes and their complete reports, both sets of positive/fault/provenance/restoration method artifacts, all 36 method command rows and 72 raw streams with their witnesses, actual loaded-class copies, tooling control artifacts, exact executed tooling/runtime inventory and the workflow copy. Retain source-edit proof and literal Android availability status. Total report member count and archive size must be measured from the completed tree; this proposal does not invent them.

A combined success means the configured host reconstruction gates passed for those exact bytes. It must keep `android_runtime_executed`, `full_runtime_1_to_1_established` and `complete_high_level_java_kotlin_source` false unless independent work actually establishes them. This workflow does not install an app, interact with calendar services or establish a UI journey result.

## 9. Focused controls required before activation

Preserve the parent 92 tooling guards and add combined-specific controls without running a full app locally. Use retained small fixtures and real bounded subprocesses where the recording/cleanup contract requires them. Exercise both the preparation entry point and independent verifier boundary for input-policy faults; assert the concrete rejection reason to avoid false passes from unrelated earlier failures.

| Area | Required deliberate faults |
|---|---|
| Two source stages | Apply Lookup21 directly to the baseline; skip Numeric19; wrong intermediate snapshot; old lookup recorder; duplicate/missing successor payload; altered numeric-only file; nonexistent before hash or wrong absence flag |
| Source/count partition | Drop the constant mapping; register a getter; omit or duplicate a getter/consumer; use 1,243 or 1,249 as recovered credit; wrong final fixture; dropped lookup suite cases or a duplicate method in two suites |
| Java control inventory | Keep only the old 91; reorder or duplicate controls; relabel an old fault as lookup; reuse a positive class as mutant; omit a required failing case; change the preserved old 91 prefix |
| Signed method identity | Reuse the numeric report as lookup; bind either method to an old APK; use a non-unique/wrong signed member; omit the signed primary comparison; change `r0` between lookup inspections; compare a whole micro-class in place of the specific signed method |
| Lookup commands | Missing/reordered/extra command; changed method/argv/classpath/timeout/expected exit; reused stream role; old schema; wrong provider; boolean/float clocks; absent/early/late finalization; false success/error/timeout fields |
| Filesystem receipts | Preserve every parent exclusive-stream, hardlink, inode replacement, bracket, ownership, close/flush and timeout guard for the new lookup command verifier; add a missing-final-row failure artifact |
| Observation/provenance | Broaden one of the seven message exclusions; normalize an injected message or identity; grant observer-control recovery credit; wrong loaded-class inventory; provenance rejection emits a result; wrong rejection reason |
| Restoration and terminal gate | Changed positive restoration bytes; omitted numeric or lookup DEX controls; wrong 24-report inventory; skipped signed source-edit probe; any acceptance command missing/nonzero; changed final complete input tree |

All simulation/fixture results must be labeled as such. Preserve actual failed attempts, the exact executed inputs and the full final discovered tooling test count. After the implementation and its offline controls close, freeze the proposed nine files, exact diffs, new runtime inventory, both source-stage contracts and the resolved lookup Git commit. Parent review and publisher activation come after that concrete handoff. The existing numeric run may continue throughout; it is neither replaced nor relabeled by this proposal.

## 10. Current decision boundary

The source derivation and bounded lookup recorder successor are closed. The separate combined tooling is still a design. Its new nine paths, expanded verifier, control suite, runtime hash, workflow, actual hosted source scans, signed primary comparisons and all sixteen acceptance gates remain pending. The next authorized implementation can be confined to this nine-file tooling surface and small evidence fixtures; no new application-source edit is required.
