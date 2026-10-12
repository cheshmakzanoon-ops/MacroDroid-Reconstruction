# GitHub transfer status — October 12, 2026

## Complete v9 snapshot committed

The complete previously delivered v9 source and toolchain snapshot is now stored
on `main`, beginning with the completed archive checkpoint
`5911da0a2d228337a408ed80278160d6b0885b69`.

| Snapshot | Original ZIP bytes | Files after extraction | Committed parts |
| --- | ---: | ---: | ---: |
| Source | 225,574,530 | 81,903 | 27 |
| Toolchain | 103,380,748 | 14 | 13 |
| Total | 328,955,278 | 81,917 | 40 |

The ordinary Git binary parts are in `vendor/v9/`, each at most 8 MiB. The manifest
pins every part's size, SHA-256 and Git blob identity, as well as the full original
ZIP identities. All uploaded blob identities matched their locally computed Git
identities. No external conversation attachment or LFS fetch is required to obtain
the full historical project.

`python3 scripts/materialize_v9.py --verify-only` verified the complete byte streams
against the original delivered ZIP SHA-256 values. A fresh materialization extracted
all 81,917 files successfully. Repeating extraction into that same working directory
was rejected as designed, preserving existing edits. The materializer can then apply
the separately versioned `project/` overlay without claiming that current edits are
the immutable historical v9 input.

## Build and validation evidence

The freshly restored v9 hybrid build reproduced the historical APK SHA-256 exactly.
The recorded host run passed all 179,248 selected three-way comparison cases with
zero unsupported cases or failures, and all 154 Python tests. The actual reports
and build logs are committed under `docs/verification/restored-v9/`.

This evidence establishes archive preservation and measured host behavior. It does
not establish whole-app 1:1 Android runtime equivalence. Current Android comparison
results and later reconstruction changes must be reported separately.

## Separate inputs and outputs

The exact supplied reference APK is committed in 12 parts under `vendor/original/`.
It is 95,725,918 bytes with SHA-256
`84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`.
The current reconstructed candidate is committed in 12 parts under
`artifacts/current/`; it is 94,683,119 bytes with SHA-256
`5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`.
The baseline control is separately preserved under `artifacts/baseline/`:
94,677,674 bytes, SHA-256
`aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096`.
`scripts/assemble_artifact.py` reconstructs each file from its committed manifest,
verifying every part and the complete APK. Earlier candidate bytes remain available
at their historical commits, including the 1,238-body candidate at `bebf448`.

The editable Java recovery and its build/test inputs are committed in `project/`,
beginning with the 1,238-body checkpoint `06bbded7b0428144a0da24308b76bc6148b97ec0`.
The candidate APK and reproducible Android tooling were added at
`8cb274e1e17a0563691c6accc905c9f686c3dc46`. The automated build and Android capture
workflow was added at `5d8c6ff25503b225929eb8443f04570f872b4a08`.
Later commits update the recorder and evidence while preserving the candidate's
identity until application source changes require another rebuilt artifact.

Android SDK and emulator caches are reproducible environment tools, not project
source; the official package pins and setup scripts are committed under
`tools/android/`. The development signing identity inside the historical snapshot
is an openly distributed test identity, not the publisher's signing key.

All older repository documentation, quality reports and recovered Java samples
remain available. There is no assertion that GitHub release attachments exist.


## Previous scene and runtime checkpoint

That checkpoint introduced 1,239 recovered bodies across 602 classes. Its
81,211 build inputs are pinned by canonical SHA-256
`8c8999f971f61def792cdf4ecd7999220c2fa2e56a5bdfecf3b04dee113bf7b0`.
The candidate manifest at that historical commit binds its APK bytes to that input snapshot and the
[exact integration checkpoint](verification/scene-runtime-integration/checkpoint.json).
The isolated scene proof passed 185,738 three-path host cases and all 22 UI
negative controls. The combined source checkpoint `95077fcb` subsequently passed
all 16 configured hosted acceptance gates, with 185,738 three-path cases, all
1,239 methods covered, 203 Python tests and the exact committed candidate APK.
All 105 source-job reports are preserved at
[source-ci-95077fc](verification/source-ci-95077fc/), commit
`3b2b7e8f539e746c9b99fbeb9a093bda1074fb92`. All 16 command-log hashes and
19 pinned fresh-evidence hashes matched the downloaded artifact bytes.

The separate Android job of workflow run `38194498356` passed the declared cold
launch and four English intro stills on its recorded API 35 configuration. All
four complete PNG/XML pairs were byte-identical, and the three observed Next taps
reached matching next-page stills. The exact 803,571-byte artifact, all 296
extracted files and independently reproduced comparison results are preserved
at [android-ci-95077fc](verification/android-ci-95077fc/). Its archive SHA-256 is
`0f82b5480cf7a3d38c766cfed81a9a2f47087e057d03329c7953cb8df5608739`.
Animation scales were zero and SystemUI demo state was recorded; this does not
establish animation, feature or whole-app parity.

The previous 1,238-body source checkpoint already passed all 16 configured hosted
acceptance gates. Its complete report files, verified output identities and job
metadata are preserved at [source-ci-bebf448](verification/source-ci-bebf448/),
commit `56bff54c905e45dd7ce8776c96b54ff9a0608bf9`. The exact Android capture
failure and later preparation failure remain under
[android-ci-ba52fd6](verification/android-ci-ba52fd6/) and
[android-ci-bebf448](verification/android-ci-bebf448/), respectively.

Immutable scene checkpoints and their complete signed proof archive are preserved
under `work-in-progress/custom-scene/`, ending with checkpoint commit
`b260db63712b0049e587ef4dfe5598d1c93df1b7`. The incomplete plugin lookup
initial checkpoint is preserved under `work-in-progress/plugin-lookup/` at
`88155fd82c5b894649c9257e0e2bb03b85c33593`; its coverage gate remains failed.
The subsequent `02-original-jvm` checkpoint passed 3,053 plugin cases and complete
198-instruction / 34-edge coverage. Signed rebuilt proof and control execution
were still pending at that freeze. The subsequent `03-signed-controls-pending`
checkpoint passed all 188,791 signed three-path cases and an independent DEX
roundtrip; its exact APK and complete closed evidence are now preserved beside
the source. All 37 control executions were still pending at that checkpoint.
The final `04-signed-proof` checkpoint passed all 37 controls and clean
18,476-case UI restoration, with the same exact signed APK. Its complete
191-file archive and 40 source files are preserved alongside the previous
checkpoints. All four plugin checkpoints retain inactive registries. The materializer applies only `project/`, so
preserving unfinished work does not adopt it as active application source.

The inactive constructor-owner prototype and its exact original/Java/D8 outputs
are preserved under `work-in-progress/constructor-owner/`. Initial checkpoint 01
passed 20 focused host regressions and the standalone DEX roundtrip. Reviewed
pipeline checkpoint 02 preserves 102 files, 31 passing regressions, the repeated
D8 proof and unchanged/static/linkage checks for 1,239 existing methods. Android
proof and active integration were still pending at that historical freeze. The generated-directory cleanup proposal and subsequent local failed
acceptance are retained under `work-in-progress/staging-cleanup/`. The initial constructor and staging-failure checkpoints were
published at `56327dd3ddd04c78ebf461cdf810e209fd571f10` without changing active
application inputs; subsequent checkpoint directories retain their own frozen
manifests. Their frozen reports retain their actual failure and pending
scopes even though the separate clean hosted checkpoint succeeded.

## Previous 1,240-body plugin and runtime integration

That overlay contained 1,240 recovered bodies across 603 classes. Its 81,245 build/test inputs have canonical SHA-256 `19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183`. The exact input-manifest file SHA-256 is `713c40cfcab17ce42294e37af68f758d0c0f488748c47aaba3a2e54f9b3e7883`. The [integration checkpoint](verification/plugin-runtime-integration/checkpoint.json) preserves the 54 changed build/test inputs, six current project documents, eight Android tooling/workflow files and full evidence archives. The prior scene APK remains preserved by its manifest and historical commits.

All five planned clean integration checks passed: hybrid assembly, full code/resource verification, all three-path host suites, and final unchanged-input verification. The fresh APK reproduced the already preserved final plugin candidate exactly. Actual counts were 188,791 cases, 1,240 methods, zero mismatches/unsupported executions and 259 Python tests. The independent integrated Android-tooling host suite passed all 27 tests. The original plugin checkpoint's 37 deliberate-fault controls retain their isolated scope.

The guarded constructor-owner facility is now integrated with zero active mappings and zero applied corrections in all three build/static/linkage gates. Fresh-generation compiler staging and the reviewed post-intro recorder are also active. The updated workflow requests full source acceptance and actual cold/intro/post-intro measurements plus a separate bounded ART allocation probe. Those hosted outcomes were pending at that historical freeze; subsequent exact reports are retained separately. No Widget recovery or plugin-upload body was activated by that integration.

## Current combined source, artifact, and capture guards

The active overlay now contains 1,242 recovered bodies across 605 classes. Its
81,291 build/test inputs have canonical SHA-256
`b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`;
the complete manifest file SHA-256 is
`ca3bed290f18a378c7a3d6cc70d924c8d6ec85481e236b4e7561c31fedafdfbe`.
The exact delta is 46 additions and 17 changes, with no removed input. It combines
the plugin-upload and Widget implementations with their fixtures and controls.

All 16 configured clean host acceptance gates passed: 193,489 original/JVM/rebuilt
cases across all 1,242 methods, 273 Python tests, 23,174 UI cases with 15,326
independent checks, all 78 actual UI fault controls, and exact positive restoration.
The accepted APK is the current 94,683,119-byte `5f635e16…` artifact. The complete
[immutable proof](../work-in-progress/combined-recovery/05-full-acceptance/),
including all 551 reports, 22 fresh evidence hashes, 16 command logs, every retained
source/class mutant, and all twelve APK parts, was published and fetched at
`c9373851d4408fb4db63c21873ac2d0bb6867270`. The complete report archive retains its
original bytes through three verified parts and an explicit reassembly mapping.
The [independent review](verification/combined-recovery/05-full-acceptance-independent-review/)
rechecked both full input inventories, all 63 delta inputs, every report member,
all fault artifacts, and every APK part.

The reviewed Trigger05/session03 guard union is activated with its exact 148-test
host proof. It rejects stale capture order and resolved-path/physical-file reuse,
and verifies paired final activity components. The source workflow allows 120
minutes and preserves the complete nested reports tree; its Android job is
unchanged. Fresh hosted source, Android, and editor results for this promoted
candidate remain pending at this publication.

The separate normal-animation diagnostic checked out its frozen original/9108
inputs at `3edcddd86660ea10c8aff71b651b446f86412525` before this promotion.
[Run 38212813248](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38212813248)
failed to obtain stable consecutive TRIGGERS frames for both APKs with animation
scales verified as 1. Its incomplete runtime result is preserved separately;
it does not establish an outcome for the new combined candidate. Historical
26-pixel differences and earlier failure reports remain unchanged. No whole-app
1:1 runtime claim is made.
