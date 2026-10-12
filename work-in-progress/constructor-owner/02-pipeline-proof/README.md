# Constructor owner restoration: reviewed pipeline checkpoint

This checkpoint adds a narrowly guarded mechanism for a preserved DEX instruction that allocates `Lzhh;` but invokes the public direct-superclass constructor `Lrff;-><init>(ILm73;)V`. It changes only the owner reference after proving the exact original method, target class declaration, class hashes, loader domain, concrete child/direct parent relationship, constructor descriptor, allocation register and occurrence count. It adds no application constructor and changes no allocated type.

`integration/merge-manifest.json` specifies the six proposed active paths and their expected parent hashes. No migration registry entry or application method is added by this integration. All 1,239 existing unmapped helper bodies were byte-unchanged through the new wrapper, and their actual static and linkage verifiers passed with zero corrections. The three integration points use the same validation wrapper.

## Evidence

- `reports/05-reviewed-pipeline-tests.log`: all 31 host regressions passed, including target declaration identity, raw source hashes, duplicate descriptors, main/embedded loader domains, source containment, unchanged methods, and matching behavior across all three integration gates. The independent review found a missing target `.class` declaration check; this checkpoint includes that check and its regression test.
- `reports/probe-03/result.json`: all seven original extraction, Java compilation, host execution, D8, transformation and smali roundtrip commands passed using the final reviewed wrapper. All three extracted original classes matched preserved source bytes.
- `reports/probe-03/constructor-probe.dex`: 1,436 bytes, SHA-256 `85f53ad51a1a85fd2161bd485db9f12556f737b0745f6e26ffdff31a927d5281`. It contains one helper class and no compile-only host stubs. Its transformed smali roundtrip is byte-identical.
- `reports/existing-02/result.json`: the reviewed integration leaves all 1,239 existing helpers unchanged and passes their original static/linkage verification.

The Android ART probe remains pending. Host execution and DEX assembly do not establish Android verifier acceptance. The WidgetUpdateManager translation remains unregistered and unproved; this checkpoint neither activates it nor claims whole-application parity. The CI probe will use this exact standalone DEX alongside the unchanged original APK, outside the installed application.

Earlier failed and successful attempts remain under `reports/`; checkpoint 01 is retained separately without alteration.
