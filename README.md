# MacroDroid Reconstruction

**The complete source snapshot, editable recovery code, original reference APK,
and current rebuilt APK are stored in this repository.** The current candidate
contains 1,239 recovered Java method bodies across 602 classes and builds the
remaining code from preserved smali. Whole-app 1:1 Android runtime behavior has
not been established.

Current progress is in [RECONSTRUCTION_STATUS.md](project/RECONSTRUCTION_STATUS.md).
The [verification workflow](.github/workflows/reconstruction.yml) rebuilds the
committed source and separately measures Android cold launches and four English
intro pages; its
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
94,683,342 bytes, SHA-256
`be1138a5cb72c5f79efaa1490b4b9c74ccb637fbb6d0975f6680da48435c50ce`.
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

The new scene method passed the following checks in its isolated recovery build.
Its executable source is now included in the current overlay. **Full acceptance
of the combined scene, recorder and device-helper checkpoint remains pending**
until a fresh configured run completes. The isolated proof and the previous
successful CI run remain separate evidence.

| Check | Measured result | Evidence |
| --- | --- | --- |
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

## Android capture results and next measurement

The first hosted comparison installed and launched both earlier APKs. Their intro
hierarchies matched, but the complete screenshots differed by 75 pixels in the
signal-strength icon. Its recorded result remains
[`CAPTURE_DIFFERENCE`](docs/verification/android-ci-ba52fd6/). The next hosted
Android run booted successfully, then failed the device-preparation signal gate
before either APK was installed; the exact failure and measurements are retained
in [android-ci-bebf448](docs/verification/android-ci-bebf448/).

The updated helper checks the primary radio's computed signal level and records
all raw measurements. It can also disable the three Android animation scales
for explicitly scoped still captures. The schema-3 recorder verifies the installed
APK checksum, fresh package state, foreground activity and live process samples,
then records `MACRODROID`, `TRIGGERS`, `ACTIONS` and `CONSTRAINTS` using three observed
Next buttons. Every full screenshot and UI hierarchy remains part of the comparison.
These new checks need an actual device result; they do not establish animation,
feature or whole-app parity. See [capture scope and evidence rules](project/RUNTIME_CAPTURE.md).

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
| `docs/verification/source-ci-bebf448/` | Successful 16-gate hosted source acceptance for the previous 1,238-body checkpoint. |
| `docs/verification/android-ci-*/` | Exact hosted Android evidence and explicit comparison or preparation failures. |
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
