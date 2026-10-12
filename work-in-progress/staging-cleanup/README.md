# Inactive generated-staging cleanup checkpoint

[01-fresh-generations/checkpoint.json](01-fresh-generations/checkpoint.json) preserves
the exact proposed cleanup code, six focused regression tests, input pin and local
diagnostics while full acceptance is running. The checkpoint SHA-256 is
`285525e151a78a0f9fd8d51536432b8ee8a5061ea9ec89e66e8403afeae9a126`.
This directory is inactive: it is not applied by the materializer and does not
change the active source or the running hosted checkpoint `95077fcb`.

The change creates a never-reused Java generation, then completes compilation,
DEX generation, disassembly and DEX validation before replacing the previous
published generation. Ten generated-directory reset sites retire the previous
directory by an atomic rename before strict removal. Cleanup errors propagate.
The source input snapshot contains 81,212 files, canonical SHA-256
`f83e1b06145a67238a722fe088c35525de359f1b20c72c06d7931c3dcc825d85`.

All six focused host tests passed. The local diagnostic also records that a
previous hybrid staging directory could subsequently be removed successfully in
0.899 seconds. That observation does not identify the underlying cause of the
earlier retained/reintroduced directory metadata, or prove the complete reuse
problem fixed. Full acceptance was still running when this checkpoint was frozen.
The exact earlier failure remains in
[scene-runtime-local-failure](../../docs/verification/scene-runtime-local-failure/).

No application method body changes in this proposal. The same 1,239-body scene APK
is expected; its reproducibility and acceptance require a completed measured run.
