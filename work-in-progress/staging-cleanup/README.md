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

## 02: Subsequent local acceptance failed during hybrid verification

[Checkpoint 02](02-local-verification-failure/checkpoint.json) preserves all 12
closed logs, reports and diagnostics from the failed local run. Input integrity,
baseline build, hybrid build and baseline code verification passed. The next
gate, hybrid code verification, failed after trying to read the vanished generated
path `build/verify-hybrid/classes/.rsync-tmp/aja.smali`. The eleven remaining gates
were not executed; this run did not pass full host acceptance or execute Android.

The contemporaneous diagnostic observed `rsync` and `sync_share.sh` process names,
and the temporary directory had already disappeared. Those observations do not
conclusively establish the synchronization mechanism. The next planned check is
to repeat the unchanged frozen inputs in a private temporary checkout.

[The exact acceptance result](02-local-verification-failure/reports/acceptance-20261012T022105883695Z/result.json)
and [diagnostic](02-local-verification-failure/reports/verification-staging-diagnostic.json)
retain the actual failure. The second checkpoint SHA-256 is
`d122aecf218768d08fd715189868c4c81be607cc78ac2fb6a414444108429ff4`.
