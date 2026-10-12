# Hosted Android capture: cada56c

Run [38202401393](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38202401393) used source commit `cada56c8a11ff5cbd892ec6d0beaeab60b3e644d`. Its Android job failed the requested capture comparison. Independent replay preserves the exact failed result while validating the successful cold-launch and standalone ART evidence.

| Measured scope | Actual result |
| --- | --- |
| Cold launch / first intro page | Exact full 720 × 1280 RGBA pixels and XML; installed APK identities verified |
| Four intro pages and three Next transitions | Complete capture; transitions agree; TRIGGERS differs by 26 pixels, the other pages by zero; strict intro gate fails |
| Post-intro notification surface | Raw PNG and XML pairs agree exactly; the aggregate post-intro gate retains its failed intro prerequisite |
| Standalone constructor allocation on ART | Passed pinned DEX/device checks, `-Xverify:all`, exact stdout marker and cleanup verification |
| Tooling host tests | 33 individual successes in 0.729 seconds |

The original installed APK is `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`; the candidate is the unchanged active 1,240-body build `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`. The ART allocation probe is a separate prerequisite, not Widget application behavior or whole-app parity. The successful source-build job is preserved separately in [source-ci-cada56c](../source-ci-cada56c/README.md).

## Exact evidence and replay

All 428 raw artifact files are copied unchanged. The exact 1,022,164-byte GitHub artifact ZIP has SHA-256 `552cfb1df46eb0fb324fde6468c9edee53611db2983ee7a60dc85179ccdf4891`; `manifest.json` and `extraction-receipt.json` bind its parts and every extracted member. The raw sanitizer's recorded omissions remain part of the original evidence; publisher scanning found no private-key or token patterns.

[Independent analysis](analysis/independent-analysis.json) records all three comparator replays, 136 capture and 48 constructor artifact paths, all six runtime-report bindings, image hashes and changed-pixel bounds. The exact ready-status JSON was recovered from captured readiness stdout and verified against its recorded hash; the final live status file correctly records the subsequent stopped state.

The replay uses four exact verifier-source hashes and full images without masks. Its executable source is [analyze_android_38202401393.py](analysis/analyze_android_38202401393.py). Five new transport tests print between their unittest headers and success markers; [the parser note](analysis/parser-format-note.json) retains the initial inline-only counting assumption and the narrow correction requiring 33 distinct headers, 33 success markers and the exact successful suite summary. No CI evidence or comparator result was changed by that adjustment.

```bash
python3 scripts/assemble_artifact.py docs/verification/android-ci-cada56c/manifest.json --verify-only
```

These measurements cover the recorded stills, transitions, controlled device state and standalone allocation probe. They do not establish runtime equality for the whole application, other device states, animations, permissions or Widget behavior.
