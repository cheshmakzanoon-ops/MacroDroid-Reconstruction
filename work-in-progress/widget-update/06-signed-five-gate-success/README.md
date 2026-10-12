# Widget signed candidate: five planned gates passed

The private Widget candidate passes the signed hybrid build, complete code
round trip, resource comparison, three-path host tests and final source integrity
check. All 191,133 cases across 1,241 registered methods and all three execution
paths pass; all 265 Python tests pass. The UI group executes 20,818 cases across
nine methods, including all 194 instructions and 20 conditional edges of Widget
`m`, with no mismatches, unsupported executions or independent-result failures.

The earlier metadata omission and one-message HotSpot failure remain preserved
in their original numbered checkpoints. This run uses the explicitly verified
host exception policy; the application method and its message normalizer have
not been changed to hide those failures. The signed APK is the same 94,683,439
byte `b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f`
artifact already retained in `06-initial-signed-failure/apk/manifest.json`.

All 81,266 final input files were independently rehashed before freezing. This
capsule contains every delta input, all five command logs, the actual compiled
helper and signed Widget smali, fresh reviewable results, and every closed report
including the complete input manifest. Join the ordered parts in
`complete-reports-manifest.json` to recover the exact verified report archive.

These five gates are separate from the complete configured acceptance suite and
the actual Android Widget method probe, which remain pending for this isolated
checkpoint. It does not promote the active source or APK, and it does not claim
complete high-level source recovery or whole-application 1:1 parity.
