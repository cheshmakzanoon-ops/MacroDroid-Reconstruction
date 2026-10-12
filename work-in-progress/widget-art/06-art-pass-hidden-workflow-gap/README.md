# Actual Widget ART success with a separate artifact input-copy gap

Run **38207925500**, job **114675450663**, commit
`c1a6d71d2e290d16ea3a047d036996f79005883a` completed successfully.
The actual `probe-result.json` is `ART_WIDGET_CASES_VERIFIED`. Both original and
candidate guest processes returned zero with identical eight-case stdout and
empty stderr. All 60 command identities and 120 raw streams pass an independent
recheck with the frozen, reviewed wrapper. Actual ADB CRLF output is preserved
and accepted by both exact AVD checks. Input and binary postchecks, read-only
guest files, and owned guest/service cleanup passed. No new Android commands
were executed during this local verification.

The independent complete-input-copy audit separately failed because the uploader
excluded `executed-inputs/.github/workflows/widget-method-probe.yml`. Its original
failed audit, traceback and executed verifier are retained unchanged. The exact
7,213-member downloaded ZIP also remains unchanged. No file was inserted into
its extraction to make that audit pass.

Supplemental provenance fetches the workflow at the exact published c1a6d71
commit: Git blob `5dc674dd2ce9572b5f61ae1e8ef794ef6ec81528`, 13,095 bytes,
SHA-256 `b694b68e29dcb815c4dded4aed48773999f1800d5fd489dacbca067926ac32c7`.
That exact source matches the workflow hash reported by the actual input
preflight. It is explicitly supplemental and is not represented as an archived
executed copy. The uploader's exact pinned action.yml is also preserved; its
`include-hidden-files` input defaults to false.

The next narrow workflow change enables hidden-file upload only within the
fresh owned `ci-widget-method/` output root, followed by a fresh actual run to
retain every input copy. The historical AVD-failed run remains failed; this
successful ART run keeps its separate artifact-copy limitation. Neither run
proves nonempty widget updates, rendering, or complete application runtime parity.
