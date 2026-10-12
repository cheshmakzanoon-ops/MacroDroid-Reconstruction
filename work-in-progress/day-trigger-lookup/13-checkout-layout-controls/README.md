# Combined hosted tooling: checkout scope correction

This inactive successor corrects one authored tooling test. Actual hosted run
38245093369 at59df961 executed153 tests in3.961 seconds:152 passed and exactly one
failed. The failed assertion counted every file beneath the checkout root and
expected nine; the real checkout contained56. The runtime verifier had already
accepted the seven exact runtime siblings before that unrelated whole-root count
failed. Physical source preparation and all sixteen application gates were
skipped. The later missing preparation report is a consequence of that skip.
The original job result is preserved as a failure; no APK or app parity passed.

## Exact change

Only three of the nine job paths change: test_day_trigger_acceptance.py, its
runtime-files.json byte/hash row, and the workflow's manifest hash literal. The
production inputs.py, prepare.py, run_acceptance.py, verify.py, pins.json and
README.md remain byte-for-byte identical to4447 and the actual archived runtime.
No recorder, cleanup, command argv, timeout, source-stage verification, numeric or
lookup proof, application count, or acceptance semantics is altered.

The corrected test derives the nine declared paths from the exact seven runtime
rows, manifest and workflow, requires the literal nine-path set, and validates
those regular files within the checkout. The unchanged production runtime
verifier still requires the exact complete sibling inventory. Unrelated root
documentation or Git-style metadata is outside that explicitly owned job scope;
it is preserved, not removed, masked or included in app parity.

Two new named controls copy the actual nine source files into a private checkout
with unrelated root documentation and inert Git-style metadata. That fixture is
accepted unchanged. Adding an undeclared runtime sibling is rejected by the
unchanged production runtime inventory guard. The corrected full corpus is155
distinct tests: all prior153 test identities remain, only the faulty body changed,
and two additional controls were added; the other152 test bodies are AST-exact.

## Actual closed local attempts

01 stopped before any test because the collector unnecessarily required the
immutable read-only parent's hardlinked payload to have one link. Its traceback
and exact wrapper remain. The collector now permits immutable source aliases
while requiring every newly copied executed file to have a single link. It never
mutates the parent source.

02 executes the old four workflow tests against a real56-file private layout:
nine exact old source files plus47 explicitly synthetic unrelated files. The
original9-versus56 assertion alone fails exactly, and the whole layout is retained
unchanged. This reproduces the count assumption, not the original host's unknown
metadata file contents, and is not a successful original tooling gate.

03 executes the six corrected workflow/layout tests successfully. 04 executes
the entire155-test corrected corpus successfully, including the inherited92
numeric controls and all lookup controls. Both execute in the same kind of
populated56-file private layout and verify all source and metadata bytes before
and after. Focused repeated tests are not added again to the155 distinct count.

The complete local attempts, fixtures, command streams and source snapshots are
in the exact evidence archive. The actual hosted ZIP is reused from the sole
publisher download, identified in review/preservation.json; all4355 extracted
files were rehashed unchanged. Its failure log, verifier result, source report,
job observations and raw inventory are included as review copies. The complete
raw ZIP remains a separate durable publication under
docs/verification/day-trigger-hosted-run-59df961.

This capsule proposes a fresh hosted rerun after independent review and exact
three-path publication. It does not change the active application, register a
method, build/sign an APK, execute Android, or establish full-host app acceptance.
