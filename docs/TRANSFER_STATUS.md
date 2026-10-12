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

The original supplied reference APK and generated APK outputs are separate from
the v9 source/toolchain snapshot; their preservation is tracked in subsequent
checkpoints. Android SDK and emulator caches are reproducible environment tools,
not project source. The development signing identity inside the historical snapshot
is an openly distributed test identity, not the publisher's signing key.

All older repository documentation, quality reports and recovered Java samples
remain available. There is no assertion that GitHub release attachments exist.
