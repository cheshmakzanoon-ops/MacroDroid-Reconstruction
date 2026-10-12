# MacroDroid Reconstruction

**The complete source snapshot, editable recovery code, original reference APK,
and current rebuilt APK are stored in this repository.** The current candidate
contains 1,240 recovered Java method bodies across 603 classes and builds the
remaining code from preserved smali. Whole-app 1:1 Android runtime behavior has
not been established.

The current source checkpoint is described in
[RECONSTRUCTION_STATUS.md](project/RECONSTRUCTION_STATUS.md); completed hosted
results are recorded below. The new combined checkpoint passed all five planned
clean host/artifact checks and reproduced its signed candidate exactly. Its full
hosted acceptance and new Android measurements remain pending. The previous
1,239-body checkpoint passed all 16 hosted source gates and exact cold-launch/
four-page intro still comparisons. The [verification workflow](.github/workflows/reconstruction.yml)
rebuilds the committed source and separately measures cold launch, four English
intro pages, the observed post-intro surface, and a bounded ART constructor probe; its
[actual runs](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions)
show whether those checks have completed and passed.

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
94,683,497 bytes, SHA-256
`9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`.
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

The active 1,240-body plugin/runtime checkpoint passed five clean integration
checks: fresh signed hybrid assembly, complete code and resource verification,
the full three-path host suite, and final source-input integrity. It ran 188,791
cases with zero mismatches or unsupported executions, and 259 Python tests. The
separate integrated Android-tooling suite passed 27 host tests. Every closed report
and source-merge receipt is retained in [the combined evidence](docs/verification/plugin-runtime-integration/).
The matching isolated plugin proof also passed all 37 UI deliberate-fault controls.
Its new full hosted acceptance and Android scopes are not yet measured.

The previous combined 1,239-body scene, recorder and device-helper checkpoint
`95077fcb1d3c86f3b1c91026619642d99198f149` passed all 16 configured hosted source
acceptance gates on 12 October 2026. Its fresh-built APK exactly matches the
committed `be1138a5…` candidate. The separate Android job also passed the declared
cold-launch and four-page still scope. Complete original reports are preserved
for both jobs; the isolated recovery proof remains separately identified.

| Check | Measured result | Evidence |
| --- | --- | --- |
| Active combined host/artifact proof | All five planned checks; 188,791 three-path cases across 1,240 bodies; 259 Python tests; exact signed candidate reproduced | [Complete combined evidence](docs/verification/plugin-runtime-integration/) |
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

## Measured Android cold launch and four intro stills

[The latest hosted Android evidence](docs/verification/android-ci-95077fc/) records
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
| `artifacts/current/` | Current rebuilt APK in 12 checksum-pinned ordinary Git parts. |
| `artifacts/baseline/` | Rebuilt baseline APK, retained separately as a code-preservation control. |
| `vendor/original/` | Exact supplied original APK in 12 checksum-pinned ordinary Git parts. |
| `scripts/materialize_v9.py` | Verified archive assembly, safe extraction and overlay application. |
| `scripts/import_v9.py` | Import the exact historical source/toolchain ZIPs when supplied separately. |
| `docs/verification/restored-v9/` | Fresh v9 host build and test evidence from the restored full snapshot. |
| `docs/verification/current/` | Earlier 1,238-body recovery and verification results; report identities retain their original scope. |
| `docs/verification/plugin-runtime-integration/` | Active 1,240-body source merge, five-check clean proof, complete reports and new Android-tooling host checks. |
| `docs/verification/source-ci-95077fc/` | Successful 16-gate hosted source acceptance for the previous 1,239-body scene/runtime checkpoint. |
| `docs/verification/source-ci-bebf448/` | Successful 16-gate hosted source acceptance for the previous 1,238-body checkpoint. |
| `docs/verification/android-ci-*/` | Exact hosted Android evidence, including the latest cold-launch/four-page still match and earlier failed comparisons or preparation. |
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
