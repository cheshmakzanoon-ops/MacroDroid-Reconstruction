# Exact normal-animation failure evidence

Run 38212813248 checked out commit 3edcddd86660ea10c8aff71b651b446f86412525 and
used the original and prior 9108 candidate. The recorder accepted intro-1 for both
APKs, then failed to acquire matching consecutive TRIGGERS frames at animation
scale 1. No complete ten-screen comparison passed. This run predates promotion of
the combined 5f635e candidate; it is not a result for that new candidate.

The unchanged downloaded ZIP is preserved in four parts. `manifest.json` pins the
28,080,813-byte archive and its GitHub run/job/artifact identity. Reconstruct it
with `scripts/assemble_artifact.py` from the repository root. Every one of its
952 original regular members is also preserved under `extracted/` and bound by
the exact `extraction-receipt.json`. No raw artifact was rewritten or relabeled.
Derived visual analysis is separate from these complete original bytes.
