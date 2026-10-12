# Reference-plan compatibility checkpoint 02

This capsule activates the previously reviewed ten-screen observation policy against the exact incoming reference plan from commit `736da1920f7dada1d0c3444032ffcf4eb8759888`. The current external adapter, its sixteen-step JSON plan, its tests, and the XML ParseError retry adapter remain unchanged. The earlier checkpoint is preserved as immutable, inactive evidence at `docs/verification/editor-observation-policy/01-observed-device-policy/`, published in commit `21d82c86c13a6b3ec2f707e1a237eabb61d1f3af`.

## Why a follow-up was required

The original checkpoint pinned the fourteen-step reference plan. Before activation, an external commit added the observed first-use information dialog and its acknowledgement to that reference adapter. Applying the original dependency pin would reject the new plan before recording anything. Checkpoint 01 was therefore published without applying its active files. This follow-up updates the pin to the exact sixteen-step dependency and retains the old fourteen-step JSON as a separately named, SHA-256 checked test fixture.

The new external plan has the same first eight steps. The complete independent ten-screen plan is unchanged: capture the four intro pages and notification prompt, deny once, record the actual app-owned promotion and process/crash evidence, close the observed promotion, open the empty editor, record Favourite Triggers information, verify and tap its exact OK button once, capture the actual resulting app surface, and stop. No later catalog action is enabled by this checkpoint. The final surface is not assumed in advance.

## Exact change and verification

`compatibility-from-01.patch` contains the complete follow-up delta. Production recorder and observed-process/frame policy bytes are unchanged from reviewed checkpoint 01. The information adapter changes only its dependency fingerprint and introductory documentation. Synthetic controls explicitly load the historical fourteen-step fixture instead of the changed external adapter. Its filename, original source provenance, size, and hash are recorded separately from actual Android fixtures.

The required journey discovery command passed **81 tests in 39.604 seconds**, with exit code zero and 81 individual success lines in `reports/host-tests-01.log`. The suite retains the prior 76 controls, includes the external commit's two additional tests unchanged, and adds three dependency controls: historical fixture drift is rejected; a changed external reference plan is rejected; and the observation policy does not implicitly enable the external sixteen-step sequence. Existing external tests also replay the exact observed information-dialog XML from the preserved artifact. Complete unmodified ZIP dependencies remain at their existing repository paths; their byte lengths and SHA-256 values are bound in `reports/host-result.json`.

All 42 manifest members of checkpoint 01 were verified unchanged. `reports/dependency-rebase.json` records the exact incoming copies and equal eight-step prefix. `reports/host-result.json` binds the current test inputs, complete ten-screen plan, workflow delta, host result, and archive dependencies. `host-inputs/` includes the unchanged small test dependencies and exact project comparator for review.

## Applying this capsule

`checkpoint.json` lists every active repository path, source copy, final size/hash, and required current baseline hash or absence guard. These fourteen paths comprise the original reviewed thirteen-file policy slice and the additional historical JSON fixture. Only the base recorder and editor workflow modify existing active files. The workflow changes only the entry point and adds the two required opt-in flags; existing downloader tests, bootstrap logging, lifecycle capture, timeout budgets, and artifact upload paths remain intact. External adapter/plan/test files and other workflows are dependencies, not active files in this capsule. Apply only with the listed baseline checks; `active.patch` is a review aid, while the source copies include the exact binary fixture.

## Scope of the pending Android result

This is host verification, not a new device result. The first consecutive full PNG/XML pair is selected independently for each APK, every earlier frame remains in evidence, and all pixels and hierarchy attributes remain compared. The denial-only process boundary verifies old-PID absence, a single new main process, exact installed APK identity, and the observed component. The known fatal exception remains a recorded crash: a later matching continuation can only receive the scoped post-crash-continuation status. The earlier 26-pixel intro difference, other preserved visual failures, and actual fatal logs remain unchanged. No crash-free, catalog-navigation, animation, or full runtime 1:1 claim is established here.
