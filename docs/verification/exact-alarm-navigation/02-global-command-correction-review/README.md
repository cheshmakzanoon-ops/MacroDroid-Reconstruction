# Corrected alarm14 global-command boundary

The exact second source attempt rejects the preserved whole-report extra-input
counterexample and still accepts the intended synthetic fourteen-screen journey.
This review is separate from the immutable first-attempt false acceptance in
the sibling `01-global-input-counterexample` directory, published at commit
`811f979eda1b937917c18defef38455c49a59062`.

The reviewer executed three complete comparisons against unchanged source:
the full positive fixture, the same report with one appended
`['shell', 'input tap 20 20']` record, and exact positive restoration. The added
command has distinct streams and finite times after every terminal capture.
The new comparison rejects it with the global mutation ownership error. The
restored complete comparison equals the positive object exactly. A separate
direct readiness-verifier control also rejects nonchronological placement.

The bounded source review covered only the two production deltas recorded in
`reviewed-delta.patch`: `exact_alarm_journey.py` and `editor_journey.py`. The
gate accounts for 26 planned inputs and six install/launch/removal mutations
in exact order, claims distinct resolved stream paths and physical inodes,
and classifies other commands through a canonical finite recorder grammar.
Ordinary allowlisted evidence commands are intentionally permitted. The new
comparator call and recorded uninstall role are restricted to schema6's exact
alarm plan. This read found no further concrete blocker in those deltas.

The two archives preserve all 98 reviewed source files and all 1,418 synthetic
artifact files, with each member's bytes and mode verified. The source inventory
was unchanged after the review. The fixture uses the observed explanation
dialog and an explicitly synthetic Settings destination. No Android device,
Settings input or subprocess was executed by this review. Full new and legacy
host suites and any actual device result remain separate work. This capsule
does not activate source or workflows or establish runtime parity.
