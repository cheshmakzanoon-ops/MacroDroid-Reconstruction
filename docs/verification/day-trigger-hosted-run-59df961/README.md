# Combined DayTrigger tooling run: pre-application failure

The single original artifact from run `38245093369`, job `114796870050`, at commit `59df96186fefb2bf883031c09562af08b48bde16` is preserved unchanged as [artifact.zip](artifact.zip). It is 4,960,179 bytes with SHA-256 `cc5afbb6833350ec9693b361ee63dae961587a30e90c35e57850c835e4b7f833`.

The tooling host-control step failed. Physical source preparation and all sixteen application acceptance gates were skipped; the final verifier reported failure and artifact upload succeeded. This run supplies no new application build or Android result. Its exact [host-control log](extracted/hosted-tool-host-tests.log), [final verification](extracted/hosted-proof/verification.json) and [job step metadata](github-jobs.json) remain the primary observations.

All 4,355 original ZIP members, totaling 21,756,616 bytes, are also directly available under [extracted/](extracted/). Every extracted file was compared against its size/SHA-256 inventory and the original ZIP member again at freezing. [extraction-receipt.json](extraction-receipt.json) records their identities. No raw member was edited, and the recorded key-pattern scan found no matches.

The successful numeric-only source run and its signed APK retain their separate proof. Diagnosis or corrections for this failed combined tooling run must be published as additive successors; this immutable failure remains unchanged.
