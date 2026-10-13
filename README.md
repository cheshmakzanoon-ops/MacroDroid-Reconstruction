# MacroDroid Reconstruction

The complete historical source snapshot, active editable recovery overlay, supplied
reference APK and current rebuilt APK are committed in this repository. **The active
candidate contains 1,244 recovered Java method bodies across 605 classes.** Remaining
application code builds from preserved editable smali; native libraries and opaque
assets remain binary dependencies. The method count is not a parity percentage.

**Whole-app 1:1 Android behaviour and complete original Java/Kotlin source have not
been established.** This is an independent reconstruction of the supplied MacroDroid
5.67.8 APK, not an authenticated publisher source release.

## Current accepted source — 13 October 2026

The combined DayTrigger numeric and dictionary-entry lookup checkpoint passed all
sixteen configured hosted source acceptance gates in run **38365018305**, against
source selection commit `daf58639000f449a55ac1985746925cd2a1816e8`. Its independent
closing verifier also passed. The same signed APK was reproduced separately in the
local restored source environment before publication.

| Check | Verified result |
| --- | --- |
| Registered recovered Java bodies / target classes | 1,244 / 605 |
| Original instructions, recovered JVM, signed rebuilt DEX | 195,151 cases; zero mismatches and unsupported executions |
| Python application tests | 357 passed |
| Compiled Java UI deliberate faults | All 101 rejected; exact positive restoration passed |
| Numeric and lookup DEX controls | Two executed D8 mutants and two provenance rejections per target; positive restoration passed |
| Configured source gates / fresh closing reports | 16 / 24 |
| Complete source input inventory | 81,304 files, rehashed before and after acceptance |
| Signed source-edit experiment | Passed; the edited source reached the signed rebuilt APK |
| Prepared job controls / publication controls | 155 / 14 passed in their respective hosted jobs |
| Android execution of this exact new APK | Not established by the source acceptance job |

The complete, unmodified 242,139,181-byte CI ZIP is stored in ordinary Git parts
under [the accepted checkpoint](docs/verification/lookup-hosted-daf5863/). All 6,115
member identities are retained, with readable selected reports and immutable APK
parts. [The literal closing verification](docs/verification/lookup-hosted-daf5863/selected/verification.json)
keeps its original `active_promoted: false` field: that report predates this
publication and is not rewritten to simulate a later observation.

The new application recovery is `DayTrigger.p0(Dictionary,String)`: first matching
dictionary entry using case-insensitive comparison, preserving entry identity and
original iteration behaviour. Its 371 target cases are part of the aggregate above.
A report-writer correction retains explicit JSON nulls; the shared Gson settings,
application methods and strict closing comparisons were not weakened to obtain a pass.
The previous rejected report remains historical evidence.

## Exact current identities

| Input or output | Identity |
| --- | --- |
| Current signed hybrid APK | 94,683,170 bytes; SHA-256 `bb527f25da36b55fe91a166043e297158213a7458bf3f901e2199adfc21668a2` |
| Full source snapshot | 81,304 files; canonical SHA-256 `5df3f861db4fd2f372edbad1d4ff6fc3df701ed70adf4737024baffd722dab2c` |
| Full source manifest file | 14,505,034 bytes; SHA-256 `223c0f13a6075e036b5878cb523297ba985e37308f1e2213dd034a17c71e3598` |
| Supplied reference APK | 95,725,918 bytes; SHA-256 `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800` |
| Preserved baseline APK | SHA-256 `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096` |

## Restore, build and verify

Use Java 21 and Python 3.12 or newer. From the repository root:

```sh
python3 scripts/materialize_v9.py
cd workspace/MacroDroid_v9
python3 release_integrity.py verify
python3 build.py build --variant hybrid
python3 acceptance.py
```

The materializer verifies every committed archive part, restores the historical
v9 source/toolchain and applies `project/`. It preserves an existing destination;
choose a fresh `--destination` for another restoration. Use `--without-overlay`
only for the historical v9 snapshot. The original APK is a comparison input, not an
application build input. The selected original-instruction fixture is test-only.

Assemble the committed current APK without recompiling:

```sh
python3 scripts/assemble_artifact.py artifacts/current/manifest.json
```

Output: `workspace/artifacts/MacroDroid-5.67.8-current-hybrid.apk`. The historical
build output filename remains `dist/MacroDroid-5.67.8-v9-hybrid.apk`; use the exact
manifest and hash, not the `v9` filename, to identify a development checkpoint.
The multipart files are ordinary Git objects, not LFS pointers.

## Android evidence and limits

Earlier Android captures and ART probes retain their own APK identities and scopes.
They are not transferred to the new `bb527f25…` candidate by a source-test success.
The supplied original contains a third-party promotion and has exhibited the same
promotion-dialog Fragment crash as earlier rebuilt candidates; see
[provenance](docs/SUPPLIED_APK_PROVENANCE.md) and
[the preserved fresh rerun](docs/verification/editor-session-guard-fix/FRESH_RERUN.md).

The earlier [post-onboarding editor comparison](docs/verification/editor-session-guard-fix/)
has ten exact full-frame and hierarchy pairs, independently replayed after fixing
stale-evidence guards. It does not prove crash-free onboarding or macro execution.
Later trigger/settings captures retain their exact failed pixel comparisons and
observed switch states; a checked settings switch is not proof of a permission API
result, scheduled alarm delivery or an executed macro.

Remaining functional acceptance includes configuring and saving macros, reopening
and editing them, real trigger/action/constraint execution, scheduling and alarm
behaviour, process death, persistence, permissions, services, external integrations,
animations and multiple physical devices. Rebuilt APKs use a development test
signing identity, not the publisher's private key. Signature-sensitive integrations
and update identity may therefore differ.

## Repository layout

`project/` is the active source overlay. `vendor/v9/` preserves the original complete
source/toolchain ZIP bytes; `vendor/original/` preserves the supplied reference APK.
`artifacts/current/manifest.json` names the current immutable APK parts.
`docs/verification/` contains exact measured results, including failures.
`work-in-progress/` holds inactive recoveries and their historical evidence; it is
not automatically applied by the materializer. `tools/android/` contains pinned
runtime setup and capture tooling. The [reconstruction workflow](.github/workflows/reconstruction.yml)
separately reruns source reproduction and bounded Android captures after active
source changes. No unstarted or incomplete run is counted as a pass.
