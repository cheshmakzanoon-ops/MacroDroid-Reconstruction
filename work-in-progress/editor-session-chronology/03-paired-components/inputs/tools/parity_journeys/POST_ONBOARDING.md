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

The proposed corrected session result has schema 3. It requires `session_observation`
start/finish monotonic timestamps recorded around every complete snapshot, including
fresh snapshots before input. The recorder saves those observations separately as
raw JSON before collecting any endpoint identity. A result capture must begin
after its input finishes; a fresh pre-input capture must follow the prior captured
surface and the preceding boundary/input. The measured capture-to-input interval
must stay within the existing 15-second freshness budget. Endpoint commands must
follow their own captured observation, occur in order, and report finite successful
non-timeout intervals. Home identity must finish before the first session input
acquisition, and final identity must occur after the last input/capture. Its resumed
component must equal the captured component; Android's equivalent abbreviated and
fully qualified component spellings are accepted.

A single published ledger of resolved paths and file identities covers both variants and every in-scope
snapshot, pre-input sample, input command stream and endpoint command stream.
Reusing another observation's file, including through a `./` or symbolic path
alias or hard link, is rejected. Equal bytes in distinct observation files remain valid. These
checks address reproduced false positives where final identity reused all home
identity outputs after its own eight files were deleted, and a later input reused
an earlier input's PID/foreground outputs after its own files were deleted.

Older schema 1 and schema 2 session results and their exact source remain historical evidence.
The corrected verifier refuses captures lacking the new absolute observation
intervals; it does not infer timestamps, rename old snapshots, or revise an old
comparison. A fresh Android run is required to establish this corrected gate.
No host result establishes Android parity.

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

## Follow-up after the published file identity ledger

This proposed timing follow-up is based on commit `47458097056fd023bad8b47b6464978b0d02e85c`. It retains `session_evidence.py`, its exact path-and-inode ledger, all twelve published ledger tests, the reproduction helper, and `SESSION_EVIDENCE.md` unchanged. The ledger is checked before chronology so a reused observation remains an explicit file-identity rejection. Equal bytes in distinct fresh files remain valid.

The comparator result advances to schema 3 because the additional capture/input chronology is mandatory. Generic journey capture schema 2 remains the outer container, with versioned `session_observation` records added by this session recorder. Older schema-2 device artifacts lack those records: preserve and replay them with their exact historical source, and record the stronger gate as pending a fresh device run. Do not invent missing capture times or replace historical reports.

The separate current ten-screen observed policy and the twelve-screen trigger proposal are unchanged by this session-only overlay. No animation setting, reference plan, app APK, selector, screenshot, XML or workflow is changed here.
