# Exact archive publication layout

The immutable checkpoint and all nine source, inventory, and document files retain their exact bytes. The checkpoint's `offline-evidence.tar.gz` is preserved without recompression as thirteen ordered parts of at most 8 MiB under `offline-evidence/`. Its complete size is 102,744,757 bytes and SHA-256 is `b62e9914e41608a8efe6030e3bba93bc3e8d40fa94739c678ead965d1f710885`.

From the repository root, verify all parts and the complete original stream:

```sh
python3 scripts/assemble_artifact.py work-in-progress/animation-diagnostic/02-initial-workflow-controls/offline-evidence/manifest.json --verify-only
```

To materialize the original archive, replace `--verify-only` with `--output /path/to/offline-evidence.tar.gz`. The archive's 1,383 regular files were individually checked against `offline-evidence-manifest.json`. Complete command metadata/streams and compact original reports are additionally visible under `review-evidence/`. One deliberately tested symlink remains inert metadata only; no link is recreated.

This is the initial inactive Normal02 proposal. Its measured offline commands remain preserved alongside the subsequently identified physical-alias and mutable-inventory gaps. The successful old controls do not establish that the proposal's preflight or capture guard is complete. The separate row-omission review is preserved under `docs/verification/normal-animation-preflight-review/01-row-omission/`; no Android or active workflow change was made by this publication.
