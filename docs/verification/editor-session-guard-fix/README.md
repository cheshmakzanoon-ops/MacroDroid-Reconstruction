# Reviewed post-onboarding editor match and guard correction

## Actual Android result

The **Post-onboarding editor session** job in run **38206460588**, source `934c6543dce0897975f52457717b3a70bd27ce00`, completed successfully. Both APKs reached all 16 recorded surfaces. The independently declared scope begins at the observed home activity after onboarding and covers **ten screen pairs and nine in-scope inputs per variant** through the empty editor and trigger/action/constraint catalogs.

Every complete 720 x 1280 paired image in that scope has **zero unequal pixels**. The full PNG bytes and full UI hierarchy XML bytes also match. No crop, mask, ignored status bar, resized image or pixel tolerance was used. A separate Pillow/NumPy decode confirmed those ten raw frame comparisons. This is one measured API 35 emulator configuration, not a whole-app or multi-device claim.

Exact raw evidence is already committed at `../editor-journey/run-38206460588-attempt-1/`. The original artifact ZIP is **11,576,977 bytes**, SHA-256 `d22377dacd276c2c8ab2d52bfa639a912d1871c90757ebefc71af16d106cdff6`, with 2,034 members. Its recorded `journey.json` SHA-256 is `023461ca583b6586f317ab64cec34f8e25ad04af3a30a3fb05b429b20957c9e0`.

The supplied reference APK is `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`; candidate APK is `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`. The separate continuous-startup comparison remains **REJECTED** because the process changes during the shared promotion-dialog crash. That failure is not overridden by an editor-session result.

## Reviewed guard gaps corrected

The subsequent read-only review at `../editor-session-review/01-read-only-guard-gaps/` showed that the first comparator could accept reuse of an endpoint identity or a prior immediate-input pair. The same three synthetic false positives were reproduced against the exact historical comparator. Correction commit **`47458097056fd023bad8b47b6464978b0d02e85c`** introduces a single session-wide evidence ledger and rejects all three, including resolved dot aliases. Additional controls cover symlinks, hard links, cross-run files, earlier snapshot/PID reuse, and input output reuse.

**All 105 local parity-tool tests passed**, including 12 new evidence-ledger tests. The exact historical-versus-corrected results are readable in [regressions.json](regressions.json); the wrong-APK-digest control remains rejected in both versions. This synthetic reproduction does not operate Android.

The corrected source then performed a **read-only replay of the unchanged real device artifact**. It still reports `EXACT_POST_ONBOARDING_EDITOR_MATCH_ONLY`, with **294 distinct observation files and zero reuse**, and all ten image/hierarchy pairs equal. [runtime-replay.json](runtime-replay.json) is the exact completed output. The corrected comparator's output schema is 2; original device reports remain untouched. This replay is not described as a newly executed device run. New CI runs retain their own independent results.

## Preserved local evidence and reproduction

The six-member `local-control-evidence.zip` retains the exact 105-test log, 12-test log, compact four-case reproduction, corrected runtime replay, independent image recheck, and execution receipt. It also records that an earlier combined tool call completed the tests but timed out during its following replay; that interrupted replay was not counted as passing. The subsequent completed replay exited zero.

```sh
python3 scripts/assemble_artifact.py docs/verification/editor-session-guard-fix/manifest.json
python3 -m unittest discover -s tools/parity_journeys -p 'test_*.py' -v
python3 tools/parity_journeys/post_onboarding.py --source project \
  --journey /path/to/extracted/ci-editor/journey/journey.json \
  --output /path/to/new-guard-replay.json
```

The exact ZIP is 6,839 bytes, SHA-256 `680d8e75a556c1dab136587e9cce2a3b3d1b3c70eeb5751419eb3e6dfe6a1959`, published in four ordinary Git parts. Every part's returned Git blob SHA matched the verified local bytes before publication. The manifest identifies every ZIP member, size and hash. Reproduction tools are checked in under `tools/parity_journeys/`.

The guards verify recorded file identities and byte integrity; they are not cryptographic attestation of an untrusted recorder. No macro was saved or executed. Scheduling, services, persistence, integrations, animation, broader UI coverage and uninterrupted startup remain separate work. No application source, APK or publisher signing identity is changed or recovered by this verification work.
