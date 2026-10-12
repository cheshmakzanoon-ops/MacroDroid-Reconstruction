# Exact Settings03 archive layout

The original source checkpoint `6a4ea8e2794a5459bcb699bb314c9b9b14fe538f45b8e06a9c2aee66a5d08051` and all 180 non-archive payloads are preserved byte-for-byte at `../`. Its original `evidence.tar.gz` is represented by two exact binary parts because a single base64 transport request would exceed the connector request bound. The archive was neither recompressed nor edited.

The logical archive is **13,014,001 bytes**, SHA-256 **51749196bbc80e9ac82beb4821cb15253c7d94122b628f7ecfd624cc398d6755**, mode **0644**. `manifest.json` binds both canonical repository part paths, their byte counts, SHA-256 values and Git blob identities. `archive-members-verification.json` records all **353** exact member byte/mode checks against the original inventory.

From the repository root, reconstruct the logical file before validating the complete original 181-file capsule:

```sh
python3 scripts/assemble_artifact.py work-in-progress/exact-alarm-enable-return/03-source-and-host-controls/archive-layout/manifest.json --output work-in-progress/exact-alarm-enable-return/03-source-and-host-controls/evidence.tar.gz
chmod 0644 work-in-progress/exact-alarm-enable-return/03-source-and-host-controls/evidence.tar.gz
```

Then recheck the whole archive digest, the unchanged original `checkpoint.json`, all 181 declared payload byte/mode identities, and the 353 archived member identities. An absent archive is not a complete capsule; the parts are its published transport representation.

The existing fetched assembler was actually invoked with `--verify-only` against both exact parts in an owned repository layout. That check created no assembled duplicate. Its source and actual stdout/stderr are retained here. This publication activates no source, APK, device input, or workflow.
