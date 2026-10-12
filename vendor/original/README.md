# Immutable supplied comparison APK

This directory preserves the exact original user-supplied APK, originally named
`automation android app`, as 12 ordinary Git binary parts. The pinned reference
contains 95,725,918 bytes with SHA-256:

`84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`

The original APK is a differential-test reference. It is not an input to the
reconstruction build and does not replace recovered source or generated DEX files.
See `docs/PROVENANCE.md` for the reference's recorded package and signature scope.

Verify the committed bytes:

```sh
python3 scripts/assemble_artifact.py vendor/original/manifest.json --verify-only
```

Reassemble the exact APK:

```sh
python3 scripts/assemble_artifact.py vendor/original/manifest.json
```

The default result is
`workspace/artifacts/MacroDroid-5.67.8-original.apk`. Use `--output /path/name.apk`
to choose another location. Each part and the complete result are SHA-256 verified.
An existing identical output is retained; an existing differing output is refused.
Assembly does not install or execute the APK.
