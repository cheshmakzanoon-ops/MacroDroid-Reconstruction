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
`artifacts/current/`; it is 94,683,342 bytes with SHA-256
`be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce`.
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


## Latest scene and runtime checkpoint

The active overlay now contains 1,239 recovered bodies across 602 classes. Its
81,211 build inputs are pinned by canonical SHA-256
`8c8999f971f61def792cdf4ecd7999220c2fa2e56a5bdfecf3b04dee113bf7b0`.
The candidate manifest binds the new APK bytes to that input snapshot and the
[exact integration checkpoint](verification/scene-runtime-integration/checkpoint.json).
The isolated scene proof passed 185,738 three-path host cases and all 22 UI
negative controls. Full acceptance of the combined scene, strict four-page
recorder and corrected device helper remains pending a fresh completed run.

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
All three plugin checkpoints retain inactive registries. The materializer applies only `project/`, so
preserving unfinished work does not adopt it as active application source.
