# Inactive constructor-owner prototype

[Checkpoint 01](01-dex-proof/checkpoint.json) preserves all 35 source, test,
original-extraction and generated-proof files byte for byte. The standalone
prototype passed 20 host regressions and an actual Java/D8/DEX roundtrip probe.
Android execution remains pending, and this prototype is not part of the active
application pipeline.

The bounded transformation checks a pinned original method, a concrete subclass
that declares no constructor, a directly accessible public parent constructor,
and the exact allocation receiver. Only numeric constants may occur in the
permitted gap. It requires exact occurrence counts and changes only the
constructor owner. Review fixes cover physical-register aliases, indented
constructor declarations and unsupported constant opcodes.

[The frozen README](01-dex-proof/README.md) describes the original/D8 comparison.
[The actual probe result](01-dex-proof/reports/probe-01/result.json) binds the
standalone probe DEX to SHA-256
`85f53ad51a1a85fd2161bd485db9f12556f737b0745f6e26ffdff31a927d5281`.
The first failed host test and subsequent corrected results are retained.
Checkpoint SHA-256:
`ca7ccf81463758ed7c342aade853138e080178c5e9f85f92eab4495ed2446766`.

## 02: Reviewed pipeline integration and repeated D8 proof

[Checkpoint 02](02-pipeline-proof/checkpoint.json) preserves all 102 listed files,
including the six-path proposed integration with baseline hashes, the shared
method-hash/domain/target-declaration guard, 31 passing host regressions, and the
actual D8 probe's seven successful commands. All prior prototype failures and
subsequent proofs remain in the immutable checkpoint. Its SHA-256 is
`98d73cb9f3c73731e2a376bfdb446704674b2019e996a59483263f0d37b31e9a`.

The standalone probe still produces the exact 1,436-byte DEX with SHA-256
`85f53ad51a1a85fd2161bd485db9f12556f737b0745f6e26ffdff31a927d5281`.
A check of the 1,239 actual existing mapped methods found no unintended changes
and no constructor corrections; existing static and linkage checks passed.
The integration remains proposed and inactive, and Android execution is pending.
No registry or active application change is included in this preservation commit.

[The integration merge manifest](02-pipeline-proof/integration/merge-manifest.json)
pins its six paths and their baselines for a later deliberate merge. The original
APK and source-input identities remain explicit in the checkpoint.
