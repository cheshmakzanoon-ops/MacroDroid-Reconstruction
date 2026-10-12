# Session-wide evidence identity checks

The review at `docs/verification/editor-session-review/01-read-only-guard-gaps/` reproduced two stale-evidence weaknesses in the first post-onboarding comparator: reusing the entire starting endpoint at the end and reusing an earlier immediate input pair at a later input, including resolved dot aliases. That historical source and its reports remain unchanged in the review archive.

`session_evidence.py` now registers every in-scope screenshot, hierarchy, PID sample, foreground observation, input precondition and input command output, plus all four endpoint command groups at both ends. One ledger covers both APK variants. Every binding is checked for confinement, existence, length and SHA-256 before its resolved path and filesystem identity are registered. A second observation cannot reuse that path or inode, including dot aliases, symlinks, hard links, or cross-variant aliases. Equal bytes in genuinely different files remain valid; stable PID values and empty stderr files are not incorrectly required to have different hashes.

The comparator's output schema is now 2 and includes `evidence_identity_check`. The existing capture schema remains 2, so original raw device records can be reviewed without rewriting their evidence. The ledger registers observation roles, not duplicate summary references or the raw command journal. It does not provide cryptographic attestation of an untrusted recorder or detect arbitrary forged replacement files. Trusted capture provenance and the preserved original artifact remain essential.

Twelve additional tests cover the published cases and broader file-alias/reuse failures. Run the whole parity-tool suite with:

```sh
python3 -m unittest discover -s tools/parity_journeys -p 'test_*.py' -v
```

The four-case historical-versus-corrected reproduction is also executable:

```sh
python3 tools/parity_journeys/recheck_guard_regressions.py \
  --historical-source docs/verification/editor-session-review/01-read-only-guard-gaps/inputs/tools/parity_journeys/post_onboarding.py \
  --output /tmp/new-guard-recheck.json
```

The supplied historical source must match its pinned Git blob before import. No Android device is operated by that reproduction. Its temporary synthetic files are reconstructed by the committed fixtures. Original runtime reports, startup failures and APK bytes are not changed by this correction.
