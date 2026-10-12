# MacroDroid Reconstruction

**The complete historical v9 source and toolchain snapshot is now stored in this
repository.** Reconstruction remains incomplete: whole-app 1:1 Android runtime
behavior has not been established.

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

## Repository contents

| Location | Contents |
| --- | --- |
| `vendor/v9/` | Complete immutable v9 source/toolchain archives in 40 ordinary Git binary parts, with a checksum manifest. No LFS download is required. |
| `project/` | Current authored source, build and verification overlay, as development checkpoints add or update it. |
| `scripts/materialize_v9.py` | Verified archive assembly, safe extraction and overlay application. |
| `scripts/import_v9.py` | Import the exact historical source/toolchain ZIPs when supplied separately. |
| `docs/verification/restored-v9/` | Fresh v9 host build and test evidence from the restored full snapshot. |
| `docs/v9/` and `docs/history/` | Historical quality reports, delivery records, provenance and checksums. |
| `source/java/recovered/` | Four original illustrative recovered-source samples retained from the initial repository. |

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

The source and toolchain ZIPs are committed as multipart byte streams. The APK rows
identify historical outputs; they do not by themselves claim those APK files are
checked in. The fresh restored v9 source build reproduced the historical hybrid APK
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
