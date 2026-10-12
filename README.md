# MacroDroid Reconstruction — research archive

**Latest produced build: v9 (October 11, 2026).** Status: **incomplete, experimental source reconstruction; full 1:1 Android functionality NOT verified.**

## What's in this public repository

- Provenance, build history, published quality reports, integrity checksums and acceptance status from the v3–v9 reconstruction sessions.
- A checksum-verifying importer under `scripts/import_v9.py`, for assembling the latest **source and toolchain ZIPs downloaded from the original ChatGPT conversation** into an isolated local workspace.
- Transfer/status notes distinguishing what has actually been pushed from what remains attached to the conversation.

**The large v9 source ZIP, toolchain ZIP, APKs, original proprietary APK and the 81,000+ extracted source files are NOT yet committed to GitHub.** This repository must not be mistaken for the full runnable v9 project. There is no claim of a successful GitHub CI build based solely on these documents.

## Latest available artifact identities

| File from conversation | Size (bytes) | SHA-256 |
| --- | ---: | --- |
| MacroDroid_v9_Source.zip | 225,574,530 | `c11f2d4727a6882943ffccbd81fa45dc738b6fe9c1c5a1c620564e90d8824e01` |
| MacroDroid_v9_Toolchain.zip | 103,380,748 | `ffb8ea58d6f44dc3b70064a58fc36ead75833d2a2bc14690708248e5640de68d` |
| MacroDroid_v9_Hybrid.apk | 94,682,999 | `ebd8628eb69f71fc54d70bf87889a11d7b9a673e20b318233c7c30b489d8ff31` |
| MacroDroid_v9_Baseline.apk | 94,677,674 | `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096` |

The complete measured results are in [v9 quality report](docs/v9/quality-report.md) and [delivery verification](docs/v9/delivery-verification.json).

## Reconstruct the *local* working directory from the conversation attachments

After downloading both v9 ZIPs and checking Python 3.11+:

```sh
python scripts/import_v9.py --source /path/to/MacroDroid_v9_Source.zip --toolchain /path/to/MacroDroid_v9_Toolchain.zip --destination workspace
cd workspace/MacroDroid_v9
python release_integrity.py verify
python build.py build --variant hybrid
python acceptance.py
```

Java 21 is needed for the source build. The importer verifies both official v9 archive SHA-256 values, prevents path traversal and symlink extraction, and refuses to silently overwrite differing files. It does not execute builds, install APKs, or push to GitHub. The `workspace/` directory is gitignored.

**This local build is not proof of Android runtime equivalence.** Device installation, launch, UI, triggers/actions/constraints, permissions, scheduling and external integrations have never been verified end-to-end against the original. The publisher's signing key and original high-level source are not recovered.

## Copyright, credentials and public-repository caution

MacroDroid is third-party proprietary software. This repository is **not affiliated with or endorsed by its publisher** and does not grant redistribution rights to application code, assets or APKs. Do not publicly upload third-party binaries, recovered code, keystores or account material unless you have the necessary rights. The chat source ZIP contains a development signing key; `signing/` and binary artifacts are deliberately excluded here.

See [transfer status](docs/TRANSFER_STATUS.md) and [provenance](docs/PROVENANCE.md).

## Checked-in source samples

A few exact recovered Java helper files are checked in under [`source/java/recovered/`](source/java/recovered/) as examples. These are **not** enough to build the app. The full set of smali classes, Android resources and binary dependencies still lives in the separately delivered v9 ZIPs.
