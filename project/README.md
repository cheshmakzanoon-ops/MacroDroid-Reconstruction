# MacroDroid 5.67.8 — editable reconstruction

The current hybrid compiles **1,244 recovered Java method bodies across 605 classes**.
Remaining application code builds from editable smali; native libraries and opaque
assets remain binary dependencies. This is not the publisher's original high-level
source project or a proven whole-app 1:1 replacement.

## Accepted source checkpoint

The numeric and lookup DayTrigger integration passed all sixteen hosted source
gates in run 38365018305 on 13 October 2026. It completed 195,151 original/JVM/rebuilt
DEX cases, 357 Python tests, all 101 compiled UI fault controls, both target DEX
fault suites, exact positive restoration and a signed source-edit experiment.
The independent closing verifier passed. See `RECONSTRUCTION_STATUS.md` for exact
source, APK and evidence identities. Earlier recovery documents are historical
accounts of their explicitly named checkpoints.

Current signed APK: 94,683,170 bytes; SHA-256
`bb527f25da36b55fe91a166043e297158213a7458bf3f901e2199adfc21668a2`.
Input snapshot: 81,304 files; canonical SHA-256
`5df3f861db4fd2f372edbad1d4ff6fc3df701ed70adf4737024baffd722dab2c`.

## Build the restored project

Restore the repository with `scripts/materialize_v9.py`; extracting only the two
historical v9 archives does not apply current recovery changes. Use Java 21 and
Python 3.12 or newer, then run from this restored project directory:

```sh
python3 release_integrity.py verify
python3 build.py build --variant hybrid
python3 test.py --three-way
python3 acceptance.py
```

The bundled compiler/assembler/resource/signing dependencies support the source
build without SDK Manager or Gradle. Android execution requires a separate runtime
and separate measurements. Build output retains the historical filename
`dist/MacroDroid-5.67.8-v9-hybrid.apk`; its hash identifies the actual checkpoint.
The original supplied APK is not an application build input. Its selected test
fixture is used for instruction comparisons only.

No source-test result establishes macro execution, alarm delivery, crash-free
onboarding, services, persistence, external integrations or physical-device parity.
The development signing identity is not the publisher's private signing key.
