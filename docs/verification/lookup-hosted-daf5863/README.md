# Accepted 1,244-method numeric + lookup source

Hosted run **38365018305** executed the exact selected source at commit
`daf58639000f449a55ac1985746925cd2a1816e8` on 13 October 2026. All sixteen application
gates and the independent final live-host verification passed. The unchanged
closing report is [selected/verification.json](selected/verification.json).

## Actual measured result

195,151 original-instruction/JVM/signed-rebuilt-DEX cases covered all 1,244 registered
methods across 605 target classes with no mismatches or unsupported executions.
357 Python tests passed. All 101 compiled Java UI deliberate-fault controls were
rejected, with exact positive restoration. The numeric and lookup control suites
each executed two actual D8 mutants and rejected two provenance substitutions.
All 24 fresh reports, literal gate commands and closed logs were verified. The
source-edit experiment reached the signed APK and the final input scan matched
all 81,304 files. The lookup target alone has 371 cases.

The resulting 94,683,170-byte APK has SHA-256
`bb527f25da36b55fe91a166043e297158213a7458bf3f901e2199adfc21668a2`.
An independent local build reproduced this exact hash and passed bytecode/resource
verification, all 357 Python tests and the complete 195,151-case three-path suite.
The original local virtual-environment interpreter caused two readiness controls
to fail; switching to the available fast system interpreter made the unchanged
tests pass. Neither the failed local run nor the previous rejected hosted report
was relabelled as successful.

## Complete preservation and publication

`raw/manifest.json` assembles the exact **242,139,181-byte** GitHub artifact ZIP,
SHA-256 `216576a3ca0122fae6b60c004c5ec4735202632a0fd9bd226b61b4aadbd3455f`.
Every one of its **6,115 members** is inventoried in `inventory.json`; no report,
control failure, command stream, source selection or signed output was edited
inside that archive. `candidate/manifest.json` assembles the separately preserved
current APK. Both are ordinary Git multipart files.

Staging run **38370958866** first passed 14 publisher controls, then independently
validated the complete artifact and uploaded exact Git objects without moving any
branch. Before this publication, local inspection matched every source/part hash
and Git blob identity against that staging receipt; the inventory's only added
metadata was the matching GitHub artifact API object. Source files, the complete
input manifest, current APK pointer and all evidence are published together.

```sh
python3 scripts/assemble_artifact.py docs/verification/lookup-hosted-daf5863/raw/manifest.json
python3 scripts/assemble_artifact.py docs/verification/lookup-hosted-daf5863/candidate/manifest.json
```

The closing report was made before promotion and retains `active_promoted: false`.
Its inode/ctime fields are actual historical live-host observations, not claims
about extracted files. No downloaded script was executed by the archive publisher.

## Limits

This checkpoint establishes the declared source/host/artifact checks. It does not
establish complete original Java/Kotlin source, an original publisher signing key,
new Android captures, alarm delivery, macro saving/execution or whole-app 1:1 parity.
Inactive recovery studies remain separate; they do not increase the active count.
