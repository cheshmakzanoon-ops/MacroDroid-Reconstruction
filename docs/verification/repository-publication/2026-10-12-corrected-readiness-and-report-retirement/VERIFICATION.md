# Publication verification and bounded checkpoint audit

Fetched commit d2c0932d7a91a2de967cd34bc3d3a2314ec6c577 was checked against all 178 staged paths: 141 unique Git blobs and 5,423,547 bytes. Git modes, lengths, SHA-1 blob identities and SHA-256 values matched. Every staged file also matched the fetched bytes. The verifier made no source-worktree or index changes.

The separate bounded audit found 113 workspace manifests at */checkpoints/*/checkpoint.json. Each had a byte-identical published Git blob in that fetched commit. This check establishes manifest presence; it does not repeat all archived payload checks. Each original publication retains its own payload verification. New tmpfs readiness capsules are covered by the 178-path commit verification.

The executable verifier, executable audit source, actual receipts and before-publication guard are included. Local worktree/index alignment remains pending while the main filesystem has limited free space; all described deliverables are already on remote main. No active application, APK or device-workflow path changed.
