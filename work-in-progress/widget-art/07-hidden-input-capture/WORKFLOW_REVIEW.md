# Preserve the bound workflow in the Widget ART artifact

The proposal adds exactly one input to the existing, pinned `actions/upload-artifact` step:

```yaml
          path: ci-widget-method/
          include-hidden-files: true
```

The baseline workflow is SHA-256 `b694b68e29dcb815c4dded4aed48773999f1800d5fd489dacbca067926ac32c7`; the proposed workflow is `f0d210cc3f877f407a33df84e7e15b3e5a9179288ffb640e3aabf9eb499fffba`. Every executable step, input pin, APK identity, probe byte, timeout, verifier option, action version, artifact root, and cleanup command remains byte-identical. The checked-out workflow already copies itself to the owned output root during the nineteen-input preflight.

## Observed result and separate archive omission

Actual run `38207925500` at commit `c1a6d71d2e290d16ea3a047d036996f79005883a` passed the independent eight-case Widget ART comparison. Both guest processes returned zero, produced the exact expected 379-byte stdout, and produced empty stderr. The frozen wrapper's independent local verification accepted all sixty recorded commands and all 120 bound raw output files. This local recheck performs no new Android execution.

The separate complete-input artifact audit failed because the downloaded ZIP omitted `executed-inputs/.github/workflows/widget-method-probe.yml`. The other eighteen declared input copies were present. The exact uploader implementation pinned by this workflow declares `include-hidden-files` with default `false`; the retained official action definition and Git blob identity are bound in this checkpoint. The exact missing workflow was separately fetched from the published commit, matched its declared SHA-256 and Git blob identity, and was retained as supplemental provenance outside the original ZIP and extraction.

ART06 preserves the actual successful probe, the failed completeness audit, and this supplemental binding separately. No historical status, report, extraction, or ZIP is rewritten. Its frozen checkpoint SHA-256 is `6f12e96586f845000f0fe5cbb2f95c8e65e83de6c46113bdf92031ff75a423e4`.

## Scope of the uploader input

The changed input applies only to the fresh, owned `ci-widget-method/` directory. The preflight creates that directory with `mkdir`, which refuses an existing root. Checkout credentials are not persisted, and the repository's `.git` directory is outside the upload root. SDK state and ADB private keys remain in the separate runner tooling directory.

The validation result contains the complete path, byte-size, and SHA-256 inventory of all 7,213 files in the actual downloaded artifact. It matches every observed path to the reviewed output producers: the nineteen selected input copies, the exact probe report and raw streams, the packaged host-control output paths, nine emulator/service files, eight explicitly selected public toolchain metadata files, and fifteen top-level logs. The known omitted workflow is the sole expected hidden path. There are zero unexpected paths, zero credential-shaped paths, and zero unexpected hidden paths in this observed tree. This is an inventory of the prior observed output plus its one known missing input, not an assertion that a future output tree has already been inspected.

## Measured validation and next actual run

`reports/validation-01/result.json` records a successful targeted validation completed at `2026-10-12T05:36:40.737644+00:00`. It checks the exact one-line diff, the unchanged executable YAML steps, the pinned official uploader input definition, all observed archive file hashes, and the owned output scope. It also executes the unchanged real offline preflight with a sixty-second bound: all nineteen input copies are created, including the exact proposed workflow under `.github`.

The unchanged earlier ART05 validation retains its twenty-one commands, including all thirty-one packaged wrapper tests, six downloader tests, input rejection cases, and owned-service cleanup controls. That frozen checkpoint is `670bb7a33921547e74460669d940da8cb4f223d17366e28eab7430ac7276c501`. Those commands are referenced with their exact evidence; they are not represented as rerun in this upload-only checkpoint.

No uploader or Android execution has occurred for this proposal at freeze time. After publication, a fresh actual workflow run must independently bind the complete downloaded ZIP, all nineteen captured input copies including the workflow, both real ART observations, the sixty raw command records, and owned cleanup. The eight bounded cases do not establish UI rendering, nonempty widget updates, service behavior, or full application 1:1 parity.
