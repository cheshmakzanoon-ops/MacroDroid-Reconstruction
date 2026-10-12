# First measured Android cold-launch comparison

This directory preserves the complete, unmodified 66-file capture artifact from
[GitHub Actions run 38190452684](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38190452684),
source checkpoint `ba52fd6d55e41fa9dd934b491c506ffcb212091b`. The original and current
candidate APKs both executed on the pinned Android 15/API 35 emulator with KVM and
ARM64 translation. The recorded launch component was the app's `IntroActivity`.

**The exact complete-frame comparison failed.** Its recorded outcome is
`CAPTURE_DIFFERENCE`: the hierarchy and screen dimensions matched, but the images
differed at 75 pixels. `pixel-difference-location.json` localizes all differences
to inclusive coordinates **x=614..630, y=17..33** in the 720×1280 capture. Every
pixel below the top 48 rows matched. This localization does not establish the
cause, change the failed result, or establish whole-app functional equivalence.
No mask, pixel tolerance, or ignored app attribute was introduced.

The original and candidate APK SHA-256 identities, command outcomes, captures,
device properties, and logs are retained in the original artifact files. The
`extraction-receipt.json` pins all 66 extracted file byte identities. The exact
207,281-byte artifact ZIP is also preserved as one binary part, SHA-256:

`c4d6ceb07411d7e9a2a709807187e5b72f0e73b9e58a4767668545639482fd9a`

To recreate that exact original ZIP from the repository root:

```sh
python3 scripts/assemble_artifact.py docs/verification/android-ci-ba52fd6/manifest.json
```

The failed result remains available for investigation and comparison with later
controlled runs. The separate source-build job and wider feature/runtime acceptance
are not established by this cold-launch record.
