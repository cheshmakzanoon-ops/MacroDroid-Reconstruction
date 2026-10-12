# Exact AVD console response in both evidence stages

The first actual Widget method job, run **38206308421** at commit
`f050cfcfd70af4699f9145311b8628260c1ed17c`, remains failed with
`ART_WIDGET_EVIDENCE_INVALID`. Its complete unchanged evidence is preserved in
the separate `03-hosted-avd-failure` checkpoint. Both actual guest processes
returned zero with identical eight-case output and empty stderr. The final host
guard rejected the AVD console response's internal CRLF separator.

The corrected wrapper applies one exact raw-byte predicate at the initial AVD
check and at the independent final evidence check. It accepts exactly these two
complete responses:

| Response bytes | Meaning |
| --- | --- |
| `MacroDroid_API35_Disposable\nOK\n` | Existing complete LF fixture |
| `MacroDroid_API35_Disposable\r\nOK\r\n` | Actual 33-byte ADB console response |

No stripping or general line-separator normalization occurs in this predicate.
It requires the complete pinned name, exact `OK`, uniform LF or CRLF line endings,
and final line ending. The existing nonzero-exit, timeout, and stderr checks apply
before accepting the response. The evidence checker still binds the exact raw
bytes and their recorded hashes. All other environment comparisons, strict
LF-only guest case output, command arguments, timeouts, APK/DEX identities,
verification options, and owned cleanup retain their previous implementation.

## Measured host checks

`reports/validation-01/result.json` records all **31 Python tests passing**.
The existing 27 tests remain. Four added tests cover the exact captured CRLF
success through both stages, 25 malformed identity/protocol responses rejected
before guest mutation, 25 independently rehashed evidence faults rejected during
final verification, and nonzero/bool-exit/stderr failures. The raw recorded AVD
fixture is SHA-256
`8522ad4bd14867dd505fdecb0e0657c506a22c36d86c8a8634fdfda384bae977`.
Extra lines, blank lines, name substitutions, whitespace, absent/repeated `OK`,
CR-only/mixed/double-CR separators, missing final newline, Unicode/control
separators, NUL, BOM, invalid UTF-8 and empty output all fail. Evidence faults
retain their deliberately changed report/output files and rejection reason.
The clean baseline evidence is checked again after those faults.

The validator also replays all **60 actual recorded command responses** against
both wrappers. It checks command sequence and timeout identity, allowing only
local ADB and local push-source pathname rebinding. Real unchanged APK bytes are
hashed locally; the injected runner returns captured raw streams and executes
no ADB command. Both replay reports explicitly say `simulated-host-control` and
`android_runtime_executed: false`.

The unchanged original wrapper, SHA-256
`c16dcf9376b1ea4de42ca51c63caeeb2ab157a5f4b89fcd0eea505182302d983`,
reproduced exit **2** and the exact AVD evidence error. The corrected policy,
SHA-256 `4738616dd655fd74832b501b95390ae744c7c6050fbb3d16f17bf78300aec541`,
passed its separate replay with exit **0** and
`SIMULATED_WIDGET_CASES_PASSED`. That result does not relabel the historical job.
All **3,171** historical artifact paths and the failed report were verified
unchanged before and after validation. The report SHA-256 remains
`37ec2e3eb9b0bad36a81913b37cfb57176edfdd82744540cb258288db3375b81`.

## Scope and next gate

The APKs and one-class probe DEX retain their exact published identities. This
checkpoint changes the host AVD response policy and its controls. It adds no
Android execution. A fresh disposable Android job must run the corrected wrapper
and pass the complete final evidence guard before this method probe is accepted.
The eight-case scope remains limited to empty-list entry/restoration/type checks;
nonempty widget updates, rendering and full application parity remain outside it.
