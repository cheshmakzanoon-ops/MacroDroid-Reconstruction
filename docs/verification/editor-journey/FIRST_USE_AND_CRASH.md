# First-use editor blocker and observed shared crash

Source inspected: `5024b1b46056de6a6e76a61883b469521a89ea44`.
Measured run: 38202401351 (candidate `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`).

The preserved `run-38202401351-attempt-1/evidence.zip` is 6,517,530 bytes;
SHA-256 `fa2eca5f893ae181b91aa7a7bf5df8320620bbc8da21b87eacffb1de0c3bc7ee`.
Its `ci-editor/journey/journey.json` records both variants reaching nine screens,
then rejecting the expected Add Trigger title. Both actual last hierarchies instead
show **Favourite Triggers**, a first-use informational dialog, with an OK button
at resource `android:id/button1`. The original XML SHA-256 is
`af7f2d14b631c0762a065a831f8247d9ca194f7fd755d0d30f2e2ba63d5b85b2`.

The original `EditMacroActivity.Z1(Lht5;)Z` instructions in the checksum-pinned v9
source archive use the shared preference `sflpi` (default true), show the tip,
set it false and return true. The reviewed plan now records that tip, acknowledges
its observed OK button, records the editor again, then taps the observed trigger
button a second time. It neither skips a visible dialog nor pretends it was a
catalog. No macro is saved or executed and no permission is granted.

## Shared crash now directly observed, not inferred from PID alone

The exact archive member `ci-editor/lifecycle.log` records these two fatal events:

| Variant | Initial PID | UTC event time, 2026-10-12 | Restarted PID |
| --- | ---: | --- | ---: |
| Supplied original | 3947 | 04:11:08.873 | 5039 |
| Candidate | 5811 | 04:12:40.576 | 6498 |

Both report `java.lang.IllegalStateException: Fragment LB{...} not attached to Activity`,
then `android.app.Fragment.getResources(Fragment.java:785)` and
`com.zx.lbua80.onShow(Unknown Source:22)`. Raw fragment identities differ and are
retained in the log. The process-death and new-process events follow in both runs.
This is evidence of a crash in both supplied inputs, not proof of a candidate-only
regression. It does not authenticate an official publisher build or attribute the
third-party promotion to the publisher.

The original strict continuous-process journey remains failed. Neither its PID
checks nor its full-image/full-hierarchy checks are relaxed by the first-use fix.
Any later editor-only comparison must explicitly start after onboarding and retain
this separate failure; it cannot establish uninterrupted startup or whole-app parity.
