# Fresh Widget ART run with the corrected AVD evidence policy

This proposal updates only `.github/workflows/widget-method-probe.yml`. The
existing workflow SHA-256 is
`43cf0363c9382083bdeed97f33fd71cfe2905eada2f34dd9e5698900ce226149`;
the proposed SHA-256 is
`b694b68e29dcb815c4dded4aed48773999f1800d5fd489dacbca067926ac32c7`.
The exact patch is included in this checkpoint.

The workflow selects the reviewed eight-file
`work-in-progress/widget-art/04-avd-parser-fix` package and binds its checkpoint
SHA-256 `3f1126ec9ee00af1f8b2ca3bcbdb36cbfee1545b229a5cb29705d7bfee3e35dc`.
Its trigger path, wrapper/test/DEX/provenance paths, expected package file count,
and displayed host-test count follow that package. All other workflow bytes are
unchanged, including the exact original and inactive b79 APK manifests, action
and downloader/bootstrap/service pins, guest verifier/classpath/timeouts,
disposable AVD startup, owned STOP cleanup, and complete failure artifact upload.

The same unchanged 7,580-byte probe DEX and the same original/b79 APK bytes will
be used. The new wrapper only corrects the exact LF/CRLF AVD response comparison.
The historical run **38206308421** stays failed. A successful host replay is
explicitly simulated; it cannot replace a fresh completed Android run.

## Measured validation

`reports/validation-01/result.json` records **21 bounded commands** with every
expected result: five Bash syntax checks; a successful preflight binding all
19 execution inputs; nine deliberately changed/missing/unsafe input scenarios
rejected; four isolated owned-service cleanup simulations with exact exit-code
and receipt checks; six current downloader tests; and all 31 corrected wrapper
tests. The simulated ADB evidence and intentionally changed evidence reports are
preserved with raw output. This validation executed no Android commands.

`baseline-inputs.json` binds all 20 selected files, including the original target
workflow, reference editor workflow, existing pinned downloader/runtime/manifests,
and exact proposed wrapper package. Their hashes were rechecked after validation
and before freeze. The publisher must verify the original target workflow hash
before applying the patch. The captured CRLF fixture is an exact byte artifact
and should use `-text` in Git attributes.

After root review, the sole publisher can commit the frozen package and this
workflow change. Its scoped push trigger starts a new independent disposable
Android job. The result must retain its own run/commit/artifact identity and pass
both exact eight-case observations, all before/after input and binary bindings,
clean diagnostics, and owned cleanup. Any failure remains preserved separately.
