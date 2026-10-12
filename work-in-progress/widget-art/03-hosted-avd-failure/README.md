# Actual Widget Android job: preserved evidence-validator failure

Run **38206308421**, job **114670448046**, commit
`f050cfcfd70af4699f9145311b8628260c1ed17c` remains **failed**.
Its original `probe-result.json` remains `ART_WIDGET_EVIDENCE_INVALID`.
The exact downloaded GitHub artifact ZIP and every member binding are preserved.

Both real `app_process64 -Xverify:all` processes returned zero, emitted the same
379-byte eight-case stdout, and produced empty stderr. The 60 recorded device
commands returned zero without timeout. Input identities, device binary hashes,
read-only modes, environment checks and owned guest/service cleanup were retained.
This evidence is limited to eight empty-list/continuation/type-check cases. It
does not establish nonempty widget updates, rendering, or complete runtime parity.

The final host evidence check failed because the AVD console returned exactly
`MacroDroid_API35_Disposable\r\nOK\r\n`. The execution-time check split lines and
accepted that exact name and `OK`. The final evidence check compared a stripped
string with an internal LF-only separator, so its internal CR remained unequal.
The observed bytes were not rewritten. The original wrapper SHA-256 remains
`c16dcf9376b1ea4de42ca51c63caeeb2ab157a5f4b89fcd0eea505182302d983`.

A separate new parser policy and host replay must not relabel this job as passed.
A fresh Android run is required after review and publication of the correction.
