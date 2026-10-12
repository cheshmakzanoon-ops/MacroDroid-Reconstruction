# Independent post-onboarding editor scope

`editor_journey.py` still checks the entire continuous-process sequence from cold
launch. Its `comparison.json` and exit status are never replaced with a narrower
result. The supplied reference has a measured promotion-dialog crash during
onboarding; see `docs/verification/editor-journey/FIRST_USE_AND_CRASH.md`.

The separate `editor_session_journey.py` entry point also records a separate editor session, starting
at the observed **home activity after onboarding** and ending after returning from
the constraint catalog. Its results go to `editor-session-comparison.json`.
It does not certify cold launch, notification handling, absence of the observed
crash, macro saving/execution, services, scheduling, or whole-app equivalence.

The two endpoints each re-read the installed APK path and SHA-256, environment,
PID, and foreground owner. An old capture with no endpoint identities is rejected;
identity evidence is never invented or inferred from the intended APK filename.
The start must be the actual NewHomeScreenActivity, not just any activity in the
application's package. All screens and transitions inside the declared session
require one continuous process, fresh non-reused pre-input artifacts, correct
foreground, successful input commands, and exactly the observed target coordinates.

Every full-frame pixel, color metadata item and hierarchy attribute is compared.
There are no crops, masks, fuzzy pixel thresholds, or ignored status bars. Screen
records are not sliced or rewritten to fool the cold-start verifier. Shared crashes
before the session remain separately recorded; a crash or restart inside the
editor session invalidates it. The entry point retains the original overall exit status. The separate
`editor-session.yml` job records that status, then gates only its explicitly named
post-onboarding scope through an independent read-only replay. The existing
ten-screen observation workflow and original reference adapter are not replaced.

Replay a completed capture with the matching source checkpoint:

```sh
python3 tools/parity_journeys/post_onboarding.py \
  --source project \
  --journey /path/to/extracted/ci-editor/journey/journey.json \
  --output /path/to/new-editor-session-replay.json
```

The command refuses to overwrite an existing output. It does not execute ADB,
install an APK, press any controls, or modify an original report. Host tests use
explicit synthetic evidence and do not themselves establish Android execution.
