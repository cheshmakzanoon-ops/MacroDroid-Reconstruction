# Real Widget ART comparison with all captured inputs preserved

Actual run **38209599059**, job **114680586735**, commit
`dbbb89cf4ca65edd3d2c2b96151dadf41aaec514` completed successfully. Its original
report is `ART_WIDGET_CASES_VERIFIED`. Independent read-only verification finished
at **2026-10-12T05:53:03.213053+00:00** and accepted the complete downloaded evidence.

The unchanged original APK and inactive Widget candidate each passed these eight
real ART cases using the actual APK classes and a one-class reflection probe:

| Case | Required observation |
| --- | --- |
| Fresh empty call | Real Unit singleton identity |
| Reused label zero | Reuse completes the empty operation |
| Resumed label two | Saved empty iterator completes |
| Invalid label | Exact exception class and message |
| Label-two dead cast L$7 | ClassCastException from malformed saved state |
| Label-two dead cast L$4 | ClassCastException from malformed saved state |
| Label-two dead cast L$1 | ClassCastException from malformed saved state |
| Null list | Expected exception type |

Both guest commands returned zero with identical 379-byte stdout
(`5fefb35053ba679c1f0aecdac3c93094023d348310537ba2b2b11653cce9efd7`)
and empty stderr. Original execution took 2.264 seconds and candidate execution
took 1.935 seconds. Both used the same bound `app_process64`, `-Xverify:all`,
explicit probe-plus-one-APK classpath, a 120-second guest timeout and 150-second
host timeout. The observed device environment, executable hashes, APK/probe
hashes before and after, exact CRLF AVD checks, and owned guest/service cleanup
are retained. No Android command was issued by the independent local audit.

The exact GitHub ZIP is **4,780,068 bytes**, SHA-256
`ad8b7f1e9e6ecc34c2b32199da0c7d777298a9a2cf8a89a464eff5779d2d1cc5`.
Every one of its **7,214 file members** is hash-bound and checked against the
fresh extraction. All nineteen executed input copies are inside this original
ZIP, including `.github/workflows/widget-method-probe.yml` with the reviewed
`f0d210cc3f877f407a33df84e7e15b3e5a9179288ffb640e3aabf9eb499fffba` hash.
The full output path set equals the previously reviewed owned output set plus
that exact hidden workflow; there are no additional paths. All sixty command
records and 120 raw streams pass the unchanged reviewed ART04 verifier.
The actual job also passed all thirty-one packaged wrapper tests and all six
downloader tests. Selected raw files are directly readable here, and the exact
ZIP preserves the entire host-control and environment evidence without rewriting.

The original APK is SHA-256
`84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`;
the candidate is
`b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f`;
the unchanged probe DEX is
`79bd3b46e71253b17ec75099cce3611df1735b8f74e8bdcb61c61e5a37ae1a07`.

The earlier AVD-policy-failed job remains failed. The earlier successful ART06
run retains its separate failed archived-workflow audit. Their frozen manifests
and original ZIP hashes are rechecked here, and no historical report or archive
has been patched or relabelled. This new proof applies only to the eight bounded
real method cases. It does not establish nonempty widget updates, rendering,
Android service behavior, or complete application runtime 1:1 parity.
