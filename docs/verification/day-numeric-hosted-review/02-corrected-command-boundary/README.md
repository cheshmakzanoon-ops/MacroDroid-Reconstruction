# Corrected numeric command and stream boundary review

Nine selected synthetic controls passed against the immutable hosted package
`994a29b51e3758cf9f3b32e5bd22a489009cfd45febb31f3d403572ffc1e9473`.
The reviewed verifier is SHA-256
`e58525d32a71170f08520caf18c4d6cfc67b4bc87d7e18f692322dac4a886a39`.
No additional blocking finding was identified in the corrected command and
outer-stream boundary examined here.

The four argument substitutions preserved in the [earlier review](../01-command-argv-counterexamples/README.md)
now reject: a different D8 executable, a missing JVM exception flag, different
configuration/result paths, and a boolean argument. The positive seventeen-command
envelope retains thirty-four distinct streams. The selected controls also reject
a real hardlink alias, Java-version streams substituted for acceptance streams,
and a dot alias of an outer stream role; the exact outer-child positive case
passes. The exact earlier failure remains unchanged at commit
`01a36663c9455a1192fedd3d1cade2c090561e59`.

The actual [test output](test-output.log) records nine successes, zero failures,
zero errors and zero skips. The measured selected-test interval was 0.128315478
seconds. [result.json](result.json) lists each selected method and its retained
synthetic observation directory. All 155 package payload files and the exact
checkpoint were rehashed before and after the review without changes.

## Evidence and scope

`reviewed-source/` contains the nine exact proposed tool/workflow files. They are
review copies and are not activated by this documentation. `synthetic/` retains
the actual synthetic report envelopes, output bytes and original inode/timestamp
observations. Hardlinked negative-test files are preserved as separate inert byte
copies with their observed shared physical identity recorded in the manifest;
this publication does not recreate that alias.

The only test adaptation was a teardown wrapper which copied synthetic artifacts
before the normal cleanup. Production source and test methods were unchanged.
The executed reviewer is [review_numeric_corrected_boundary.py](review_numeric_corrected_boundary.py).
It imports only the frozen test and tool copies and runs the nine named controls.

This is a direct synthetic verifier-boundary review. It did not execute Java,
D8, a full acceptance build or Android. It does not establish a signed numeric
candidate or runtime parity. The separate hosted package still needs its actual
complete build and evidence check; this review does not relabel that pending work.
