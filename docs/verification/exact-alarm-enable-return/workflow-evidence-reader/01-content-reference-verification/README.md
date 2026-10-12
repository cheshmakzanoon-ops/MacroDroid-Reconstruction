# Settings workflow evidence-reference verification

The corrected read-only reader verified the complete frozen Settings workflow evidence. The original workflow and its four executable payloads remain unchanged at checkpoint `5f64e5e87270fd1f2e5203bdc54559c50c4920102451f9761c58c2f269b72cfa`. This follow-up records a separate reader defect and its correction; it adds no application, workflow, image-comparison, or Android change.

## Retained first attempt

At 12:35:13–12:35:22 UTC on 2026-10-12, the first reader returned `FROZEN_SETTINGS_EVIDENCE_VERIFICATION_FAILED` with `ValueError: Referenced exact logical bytes differ`. Its source, full result and diagnosis are retained under `retained-failure/`.

The reader cached two different content roles under the same `(commit, path)` key. The source03 archive-layout manifest was first read as a 1,549-byte Git blob. The same immutable manifest path later identified the 13,014,001-byte logical archive assembled from its two parts. Reusing the manifest's digest for that second role incorrectly rejected the reference. The preserved diagnosis identifies the exact commit, paths, sizes and SHA-256 values.

## Narrow correction and actual result

`corrected-reader/derivation.patch` makes the content-reference kind part of each cache key and removes that tag only when forming the Git read. The exact size, SHA-256, Git-object, mode, inventory and archive checks are unchanged. No retained bytes or source workflow were adjusted to satisfy the reader.

The corrected invocation completed at 12:37:37 UTC with `COMPLETE_FROZEN_SETTINGS_EVIDENCE_VERIFIED`. Its full receipt preserves every fetched Git read. It checked:

- All 602 frozen workflow/evidence payloads.
- All 16,454 indexed paths: 16,452 regular paths and two symlinks retained as inert evidence.
- 7,114,730,719 logical regular bytes, including repeated case-tree references without duplicate APK copies.
- 173 distinct immutable Git-blob references.
- Three complete multipart logical containers, streamed from fetched Git objects and rehashed: the original APK, the fixed numeric candidate APK, and the source03 evidence archive.

No APK file was materialized by this reader. `bindings/final-frozen-payload-rehash.json` separately rechecks all 602 original payloads, their modes and complete membership after the reader attempts. All remain exact.

## Scope of the workflow result

The source capsule's earlier offline validation remains the actual 74-command pass, with 317 complete input-copy roles and 402 protected inputs unchanged. The closed 259 source controls were reused rather than rerun locally; the future hosted workflow retains the full suite. Archive, inventory, policy, APK and cleanup faults remain in that original capsule.

This follow-up is evidence-reference validation only. It does not run the host suite, application build, emulator or Settings journey, and does not establish runtime parity or activate a workflow. Recorded closure filesystem metadata remains closure metadata; the reader does not reinterpret it as the original command's filesystem timestamps.

## Files

- `bindings/source-workflow-checkpoint.json` binds the immutable 602-file source capsule.
- `bindings/final-frozen-payload-rehash.json` records the final exact-source check.
- `retained-failure/` preserves the first actual failure and its source.
- `corrected-reader/` preserves the four-line correction, final source and actual successful receipt.
- `result.json` keeps offline workflow and reader scopes separate.
