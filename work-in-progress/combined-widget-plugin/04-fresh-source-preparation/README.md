# Fresh combined source prepared; full acceptance pending

All 81,245 active baseline input files were independently copied and checked
against the published pin before and after copying. No input was hardlinked and
no generated cache was copied. The frozen combined source overlay was verified
and applied, then the original-method fixture was freshly extracted from the
unchanged supplied APK for exactly 1,242 methods across 605 classes. Its actual
hash, byte size and inventory are bound in fixture provenance.

The 81,291-file candidate input pin is
`b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`.
Every input was independently rehashed again before this freeze. All exact
delta inputs and the compressed complete input manifest are included.

Review of the previous control runner identified an unbounded final positive
UI child. This follow-up explicitly logs that command and limits it to the same
300 seconds as every fault execution. The actual 54-control plugin gate took
1,962.871 seconds, so the combined 78-control acceptance budget is 5,400 seconds;
other gate budgets remain 1,200 seconds. Raw measured evidence and exact patches
are retained. The staged source workflow allows 120 minutes and preserves every
report and nested mutant artifact. It must only activate with the verified
combined candidate, not as a standalone current-source workflow change.

The expected combined run covers 193,489 cases, ten UI methods / 23,174 UI cases,
15,326 independent UI expectations, 273 Python tests and 78 actual UI fault
controls. Those full combined gates have not executed in this checkpoint.
The active source/APK remain unchanged. No Android or whole-app parity is claimed.
