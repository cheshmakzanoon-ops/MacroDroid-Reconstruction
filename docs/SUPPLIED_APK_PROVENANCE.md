# Supplied APK identity and observed promotion

The reconstruction and differential tests target the exact user-supplied Android APK, not an independently authenticated publisher release.

Reference SHA-256: `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`.
Reference size: 95,725,918 bytes. Package: `com.arlosoft.macrodroid`.

## Measured finding

On fresh installation, after the four introduction pages and denial of the Android notification permission, both the supplied original and the then-current rebuilt candidate displayed a dialog headed **LITEAPKS**. The dialog contains **CLOSE** and **DOWNLOAD** controls and text promoting modified applications. This was observed in actual Android screenshots and UI hierarchy captures, not inferred from an app-store description.

The exact evidence is committed in:

- `docs/verification/editor-journey/run-38198783416-attempt-1/evidence.zip`
- ZIP members `ci-editor/journey/original-home.xml` and `candidate-home.xml`, with matching screenshots.
- Artifact SHA-256: `abf947195917bb8f090cee7ae2eff250963c8d0ddd5d5663d7b76103a850c46e`.

The test label `home` in that failed run describes the expected destination, not the actual screen reached. Both runs were correctly rejected as incomplete. They are not successful home/editor parity results.

## Test behavior and limits

The reviewed reference-specific journey now records the promotion as its own state and targets only its observed **CLOSE** button. It does not open the download link, change either APK, grant permissions, use an account, save a macro or execute a macro. The original remains checksum-pinned. Existing fresh-input, process, foreground, artifact-hash, full-image and full-hierarchy checks remain in force.

A match against this supplied reference must not be advertised as proven equivalence to an official MacroDroid publisher build. Establishing that separate claim requires an independently authenticated publisher reference and new measurements. This finding alone is not a malware determination or an attribution of the dialog to the publisher.

The 14-state reviewed plan is `tools/parity_journeys/editor-plan.json`; its adapter is `supplied_reference_journey.py`. Host regression tests use the exact archived Android capture rather than a fabricated approximation of the dialog.
