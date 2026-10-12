# MacroDroid Reconstruction

**The complete source snapshot, editable recovery code, original reference APK,
and current rebuilt APK are stored in this repository.** The current candidate
contains 1,243 recovered Java method bodies across 605 classes and builds the
remaining code from preserved smali. Whole-app 1:1 Android runtime behavior has
not been established.

The current numeric source and signed candidate passed all 16 configured hosted
acceptance gates: 194,780 three-path cases, 308 project Python tests, 91 compiled
Java UI fault controls, two actual numeric DEX fault controls, exact positive
restoration and the signed source-edit experiment. The job also passed 92 tooling
host controls. Its UI group ran 24,465 cases. The
[complete numeric artifact](docs/verification/day-numeric-hosted-run-3d91187/) and
[independent streamed review](docs/verification/day-numeric-hosted-run-3d91187/analysis/)
preserve the exact result, all 23 fresh reports, and the full 81,298-input snapshot
`f8fc1cadac8213468e42ac99a2cd5d807827dcdeee25166b8025620ff39a6545`.
The [nineteen-file source checkpoint](work-in-progress/day-trigger-numeric/08-command-filesystem-source-successor/)
is the exact overlay used by that job. **Android behavior for this new `0762aad9…`
APK has not yet been observed.** The existing device observations below belong
to their explicitly recorded earlier APKs.

The previous 1,242-body source checkpoint is described in
[RECONSTRUCTION_STATUS.md](project/RECONSTRUCTION_STATUS.md). The combined plugin
upload and Widget candidate passed all 16 configured host acceptance gates,
193,489 three-path cases, 273 Python tests, all 78 UI fault controls with exact
positive restoration, and the signed source-edit experiment. Its exact source,
signed APK and every closed report are retained in the
[complete combined proof](work-in-progress/combined-recovery/05-full-acceptance/).
The clean [hosted source reproduction](docs/verification/source-ci-dbcad968/)
has now passed the same 16 gates and reproduced the exact committed APK.
The [Android capture](docs/verification/android-ci-dbcad968/) records an exact
cold launch, a 35-pixel TRIGGERS difference and a successful bounded constructor
ART probe. The separately reviewed
[post-home session](docs/verification/editor-journey/run-38214498414-attempt-1/analysis/)
has ten exact scoped still pairs while preserving the recorded startup crashes
and restarts. These measured outcomes retain their separate acceptance scopes.

## Latest trigger-navigation observations

The completed [thirteen-screen readiness observation](docs/verification/android-day-time-readiness-e1ade015/)
at commit `e1ade015` reached all thirteen screens with both fixed APKs. The
[independent replay](docs/verification/android-day-time-readiness-e1ade015/analysis/)
reproduced the complete recorded verdict and comparison: all thirteen UI
hierarchies and twelve full screenshot pairs are byte-identical, while the second
introduction screen has **26 different pixels**, all inside the observed page
indicator. The exact comparison therefore remains failed. Both runs reach the
same exact-alarm permission explanation after the Day/Time trigger tap; neither
run presses its OK button or confirms a trigger configuration.

Both bounded notification-readiness phases passed their actual raw command and
chronology checks before full-frame capture. Both runs also preserve the known
Fragment exception, replacement process and observed continuation, so a crash-free
run is not established. The replay verified all 3,258 raw artifact files, 252
prepared input roles, 50 accepted snapshot ledgers and 100 frame observations.
All 166 journey, six downloader and ten animation host tests passed in this job.
No pixel region was masked and no mismatch tolerance was applied.

The earlier [twelve-screen trigger-catalog comparison](docs/verification/android-trigger-category-6331410/)
completed both runs at animation scale zero with a five-pixel second-introduction
difference. The earlier [thirteen-screen Day/Time observation](docs/verification/android-day-time-trigger-e610d98/analysis/)
recorded five matching pairs before the original run failed at the
notification-result boundary with an absent main PID; only its candidate reached
all thirteen screens. These historical outcomes remain unchanged.

The [corrected notification-readiness guard](work-in-progress/notification-readiness/01-corrected-host-guard/)
preserves both initial counterexamples and their corrections. Its 21 focused
tests and exact historical replays pass. The
[separate readiness workflow](work-in-progress/notification-readiness-workflow/01-thirteen-screen/)
passed its 55 offline validation commands before the completed Android execution
above. Source acceptance, evidence completeness, process behavior and exact pixel
equality retain their separately recorded results.

## Get the working source

Clone this repository, install Python 3.11 or newer, then run:

```sh
python3 scripts/materialize_v9.py
cd workspace/MacroDroid_v9
python3 release_integrity.py verify
python3 build.py build --variant hybrid
python3 acceptance.py
```

Java 21 is required for the source build. The materializer verifies every committed
archive part and the two complete ZIP SHA-256 values, extracts the historical
snapshot, and applies the current authored source overlay from `project/` when
present. Existing working directories are preserved; use a fresh `--destination`
to create another checkout. To inspect historical v9 without current changes, use
`--without-overlay`. To check the archive bytes without extraction, use
`--verify-only`.

## Assemble the committed APKs

The current candidate is stored as ordinary Git binary parts, with each part and
the assembled APK checked by SHA-256. From the repository root:

```sh
python3 scripts/assemble_artifact.py artifacts/current/manifest.json
```

This produces `workspace/artifacts/MacroDroid-5.67.8-current-hybrid.apk`:
94,683,136 bytes, SHA-256
`0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd`.
The build scripts retain their historical `v9-hybrid.apk` output filename; the
candidate manifest and checksum identify the actual development checkpoint.

The baseline is a separate code-preservation control:

```sh
python3 scripts/assemble_artifact.py artifacts/baseline/manifest.json
```

For reference-device comparisons, assemble the exact supplied original separately:

```sh
python3 scripts/assemble_artifact.py vendor/original/manifest.json
```

The original is a comparison input, not a build input. See the
[candidate manifest](artifacts/current/manifest.json),
[reference manifest](vendor/original/manifest.json), and
[Android runtime instructions](tools/android/README.md).

## What has actually passed

The active 1,243-body numeric candidate passed all 16 configured acceptance
gates in hosted run `38238858564`, job `114776169911`. Its 194,780 cases include
24,465 UI cases; all 308 project Python tests and 92 tooling host tests passed.
All 91 compiled Java UI faults and both actual numeric DEX faults were detected,
and the exact positive result and signed source-edit probe passed. The complete
3,308-member artifact, all 23 fresh reports and the separate review are retained
in [the numeric host evidence](docs/verification/day-numeric-hosted-run-3d91187/).
This is host/source/APK evidence; its Android probe remains unexecuted.

The previous 1,242-body combined source passed all 16 configured acceptance gates:
signed baseline/hybrid builds, complete code and resource verification, the full
three-path host suite, all fault families, the signed source-edit experiment,
final positive restoration and unchanged source-input checks. It ran 193,489
cases with zero mismatches or unsupported executions and passed 273 Python tests.
The ten-method UI group passed 23,174 cases with 15,326 independent expectations;
all 78 deliberate UI faults were detected and the full positive baseline restored.
All 551 closed reports and the exact signed artifact are preserved in
[the previous combined evidence](work-in-progress/combined-recovery/05-full-acceptance/).

Hosted source job 114695960566 independently passed all 16 gates for commit
`dbcad968c5c3e8f084205393a6c0d2d06a203c71`, with the same 193,489 cases,
273 Python tests, 78 UI faults and exact `5f635e16…` APK. The complete original
1,136-member ZIP, all gate logs and a separate streamed review are preserved in
[the hosted source artifact](docs/verification/source-ci-dbcad968/). Its source
success remains separate from the Android job's failed intro comparison.

The prior 1,240-body source separately passed two complete hosted acceptance runs,
38200503458 and 38202401393, with 188,791 cases and 259 Python tests each. Its
9108 candidate also has a complete ten-screen Android observation with a remaining
26-pixel intro indicator difference. The isolated Widget candidate passed a
separate eight-case ART probe. These historical measurements do not certify the
later candidates beyond their separately recorded device scopes.

The previous combined 1,239-body scene, recorder and device-helper checkpoint
`95077fcb1d3c86f3b1c91026619642d99198f149` passed all 16 configured hosted source
acceptance gates on 12 October 2026. Its fresh-built APK exactly matches the
committed `be1138a5…` candidate. The separate Android job also passed the declared
cold-launch and four-page still scope. Complete original reports are preserved
for both jobs; the isolated recovery proof remains separately identified.

| Check | Measured result | Evidence |
| --- | --- | --- |
| Current numeric host/source/APK proof | All 16 configured gates; 194,780 three-path cases across 1,243 bodies; 308 project Python and 92 tooling tests; 91 Java UI faults, two actual numeric DEX faults and exact restoration | [Complete numeric artifact and independent review](docs/verification/day-numeric-hosted-run-3d91187/) |
| Current numeric Android behavior | Not yet observed for the `0762aad9…` candidate; earlier APK results remain separately recorded | [Pinned current candidate](artifacts/current/manifest.json) |
| Previous 1,242-body combined host/artifact proof | All 16 configured gates; 193,489 three-path cases across 1,242 bodies; 273 Python tests; all 78 UI faults and exact restoration | [Complete combined evidence](work-in-progress/combined-recovery/05-full-acceptance/) |
| Previous 1,242-body hosted source reproduction | All 16 gates, 22 fresh report hashes and 78 retained mutants verified; both APK hashes reproduce; all 1,136 original artifact members preserved | [Exact source CI artifact and independent review](docs/verification/source-ci-dbcad968/) |
| Previous `5f635e16…` cold launch, intro and constructor probe | Cold launch exact; TRIGGERS differs by 35 pixels; other measured intro and raw post-intro pairs exact; constructor ART probe passes | [Unchanged Android evidence](docs/verification/android-ci-dbcad968/) |
| Previous `5f635e16…` scoped post-home editor session | Ten full-frame/XML/component pairs match; recorded startup crashes and restarts retained; continuous startup remains rejected | [Independent session replay](docs/verification/editor-journey/run-38214498414-attempt-1/analysis/) |
| Isolated plugin lookup proof | 3,053 cases; all 198 instructions and 34 conditional edges; all 37 UI fault controls and clean restoration | [Signed plugin checkpoint](work-in-progress/plugin-lookup/04-signed-proof/) |
| Previous hosted 1,239-body source checkpoint | All 16 configured acceptance gates; 185,738 three-path cases; all 1,239 methods; zero mismatches/unsupported executions; 203 Python tests passed | [Fresh source CI evidence](docs/verification/source-ci-95077fc/) |
| Previous hosted UI deliberate-fault checks | All 22 controls passed; the restored 15,423-case UI suite passed; inputs unchanged | [Actual control report](docs/verification/source-ci-95077fc/reports/ui-negative-controls.json) |
| Isolated scene build: original instructions, recovered JVM code, and signed rebuilt DEX | 185,738 cases; all 1,239 registered methods covered; zero mismatches or unsupported executions | [Signed scene recovery report](work-in-progress/custom-scene/02-signed-proof-evidence/custom-scene-recovery.json) |
| New custom-scene recovery | 4,070 cases; all 405 original instructions and 40 conditional branch edges visited | [Source and recovery account](project/SCENE_RECOVERY.md) |
| Isolated scene build: full hybrid bytecode round trip | 71,267 classes / 349,972 method definitions; exactly 1,239 intended body changes and no unexpected changes | [Signed scene recovery report](work-in-progress/custom-scene/02-signed-proof-evidence/custom-scene-recovery.json) |
| Isolated scene build: UI deliberate-fault detection | All 22 controls rejected their intended defect; the restored 15,423-case, seven-method UI suite passed | [Complete 135-report proof archive](work-in-progress/custom-scene/02-signed-proof-evidence/manifest.json) |
| Previous 1,238-body source checkpoint on GitHub | All 16 configured acceptance gates passed; 181,668 host cases; freshly built APK exactly matched its committed `2eabb2d8…` candidate | [Fresh source CI evidence](docs/verification/source-ci-bebf448/) |
| Earlier touch-blocking recovery | 2,420 cases; all 162 original instructions and 30 conditional branch edges visited | [Recovery report](docs/verification/current/block-touches-recovery.json) |

These are bounded host and artifact checks. They do not execute Android services
or establish complete feature parity. The complete configured acceptance run and
actual Android comparisons have separate reports; an unstarted or incomplete run
is not a pass.

## Historical Android cold launch and four intro stills

[The preserved 1,239-body hosted Android evidence](docs/verification/android-ci-95077fc/) records
one fresh installation of each APK on the same API 35 emulator configuration.
The recorder verified the distinct original and candidate APK identities on the
device, then captured `MACRODROID`, `TRIGGERS`, `ACTIONS` and `CONSTRAINTS`. All four
pairs of complete 720 × 1280 PNG screenshots and UI hierarchy XML files are
byte-identical. Each full image contains 921,600 pixels; every paired comparison
found zero changed pixels, including the status and navigation bars.

All three observed Next-button taps reached matching next-page stills. Before
each tap, fresh hierarchy evidence, the foreground intro activity and the live
process were checked. The complete screenshots use no masks, crops, resizes or
pixel tolerance. Independent comparison replay reproduced both original CI
reports exactly, and a separate image decode confirmed the zero-pixel result.

This is a declared still-capture configuration: Android animation scales were
set to zero and read back, and SystemUI demo mode displayed 12:00 for both apps.
The helper recorded stable computed signal level and retained all raw signal
measurements. Those controls are part of the published environment evidence;
animation motion and timing were not compared. Final intro completion, app home,
permissions, macro execution, services, persistence, other screens and other
devices remain outside this result. See the
[precise capture account](docs/verification/android-ci-95077fc/README.md) and
[capture evidence rules](project/RUNTIME_CAPTURE.md).

The earlier [75-pixel status-icon difference](docs/verification/android-ci-ba52fd6/)
and subsequent [pre-installation signal-preparation failure](docs/verification/android-ci-bebf448/)
remain preserved with their actual failed outcomes. The latest success does not
rewrite either historical run or establish whole-app 1:1 behavior.

## Repository contents

| Location | Contents |
| --- | --- |
| `vendor/v9/` | Complete immutable v9 source/toolchain archives in 40 ordinary Git binary parts, with a checksum manifest. No LFS download is required. |
| `project/` | Current authored source, build and verification overlay, as development checkpoints add or update it. |
| `artifacts/current/` | Current candidate manifest references 12 checksum-pinned ordinary Git parts; historical parts remain preserved. |
| `artifacts/baseline/` | Rebuilt baseline APK, retained separately as a code-preservation control. |
| `vendor/original/` | Exact supplied original APK in 12 checksum-pinned ordinary Git parts. |
| `scripts/materialize_v9.py` | Verified archive assembly, safe extraction and overlay application. |
| `scripts/import_v9.py` | Import the exact historical source/toolchain ZIPs when supplied separately. |
| `docs/verification/restored-v9/` | Fresh v9 host build and test evidence from the restored full snapshot. |
| `docs/verification/current/` | Earlier 1,238-body recovery and verification results; report identities retain their original scope. |
| `docs/verification/plugin-runtime-integration/` | Previous 1,240-body source merge, five-check clean proof, complete reports and its Android-tooling host checks. |
| `docs/verification/day-numeric-hosted-run-3d91187/` | Complete numeric 16-gate host artifact, exact signed `0762aad9…` APK input and independent review for the active 1,243-body candidate. |
| `docs/verification/source-ci-dbcad968/` | Exact complete ZIP and independently verified 16-gate hosted source reproduction for the previous 1,242-body candidate. |
| `docs/verification/source-ci-95077fc/` | Successful 16-gate hosted source acceptance for the previous 1,239-body scene/runtime checkpoint. |
| `docs/verification/source-ci-bebf448/` | Successful 16-gate hosted source acceptance for the previous 1,238-body checkpoint. |
| `docs/verification/android-ci-*/` | Exact hosted Android evidence, including scoped matches and preserved failed visual comparisons or device preparation. |
| `work-in-progress/` | Immutable recovery checkpoints and proof archives, including incomplete work; the materializer does not apply these directories. |
| `tools/android/` | Reproducible JDK/SDK pins, disposable emulator setup, and runtime orchestration. |
| `docs/v9/` and `docs/history/` | Historical quality reports, delivery records, provenance and checksums. |
| `source/java/recovered/` | Historical and independent recovered-source samples. Active build inputs are under `project/`. |

The committed source archive contains **81,903 files**; the toolchain archive
contains **14 files**. Together, the two original ZIP byte streams are 328,955,278
bytes and expand to 1,015,640,489 bytes. This includes the build scripts, recovered
source/smali, Android resources/assets, native payload and the v9 build dependencies.
See [snapshot documentation](vendor/v9/README.md) for the storage format and
[transfer status](docs/TRANSFER_STATUS.md) for what is committed.

## Verified historical artifact identities

| Artifact | Size (bytes) | SHA-256 |
| --- | ---: | --- |
| MacroDroid_v9_Source.zip | 225,574,530 | `c11f2d4727a6882943ffccbd81fa45dc738b6fe9c1c5a1c620564e90d8824e01` |
| MacroDroid_v9_Toolchain.zip | 103,380,748 | `ffb8ea58d6f44dc3b70064a58fc36ead75833d2a2bc14690708248e5640de68d` |
| MacroDroid_v9_Hybrid.apk | 94,682,999 | `ebd8628eb69f71fc54d70bf87889a11d7b9a673e20b318233c7c30b489d8ff31` |
| MacroDroid_v9_Baseline.apk | 94,677,674 | `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096` |

The source and toolchain ZIPs are committed as multipart byte streams. The baseline
APK is also committed under `artifacts/baseline/`. The historical hybrid row
identifies the earlier v9 output; the current candidate has the separate checksum
listed above. The fresh restored v9 source build reproduced that historical hybrid
SHA-256 exactly. Host tests and artifact integrity are documented separately from
Android runtime acceptance; see the [restored-v9 evidence](docs/verification/restored-v9/)
and [v9 quality report](docs/v9/quality-report.md).

## Identity and remaining acceptance work

Target: the user-supplied MacroDroid 5.67.8 APK. The original high-level application
source and the publisher's private signing key have not been recovered. Rebuilt
APKs use the openly distributed development test identity retained in the v9
snapshot, so update identity and signature-sensitive integrations can differ.

Compilation, checksums, host tests and selected instruction comparisons are
insufficient to establish whole-app equivalence. Installation, launch, UI flows,
triggers, actions, constraints, permissions, scheduling and external integrations
need measured Android runtime comparisons against the supplied reference.

This reconstruction is not affiliated with or endorsed by MacroDroid or its
publisher. See [provenance](docs/PROVENANCE.md) for the supplied input identity and
the precise scope of historical measurements.
