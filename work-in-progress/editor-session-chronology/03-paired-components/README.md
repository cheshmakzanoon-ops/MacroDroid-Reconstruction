# Paired foreground component correction

This is a frozen inactive follow-up to session chronology checkpoint 02. It proposes only the same three files: `post_onboarding.py`, `test_post_onboarding.py`, and `POST_ONBOARDING.md`. The external 4745809 path-and-inode ledger, its twelve tests, shared observed-capture policy, reference plan, workflows, and all app/APK inputs remain unchanged. Neither this checkpoint nor its earlier session02 baseline has been activated by this study.

## Exact false pass retained

The session02 verifier correctly required an endpoint foreground record to match its own capture, but omitted the paired foreground component from its comparison. The preserved synthetic reproduction first sets both final captures and endpoints to the **actually observed EditMacroActivity**, and verifies a passing positive. It then changes only the candidate final capture foreground and its separate endpoint foreground to `.DifferentFinalActivity`. All 294 semantic observation files remain distinct; timestamps, PIDs, installed APK identities, all ten full screenshots and all ten hierarchies stay valid and unchanged. Session02 incorrectly returns `EXACT_POST_ONBOARDING_EDITOR_MATCH_ONLY` again.

The complete before/after reports, literal old results, 584-file deterministic synthetic artifact ZIP and member hash manifest are retained under `reports/01-frozen02-false-positive/`. A separate read-only replay verifies every archive member, exactly reproduces both old results, and shows that this correction accepts the positive and rejects the mutation. This is a host test of recorded evidence; it is not an Android observation or an attestation of an untrusted recorder.

## Narrow correction

Every paired scoped screenshot now compares normalized foreground components in addition to unchanged full RGBA pixels, dimensions, color metadata and full hierarchy. Each result row exposes the original and candidate component strings and `foreground_component_equal`; a component difference makes that row unequal even when pixels/XML match. Abbreviated and fully qualified spellings of the same Android component normalize equally.

The final `editor-after-constraint-back` endpoint additionally requires `com.arlosoft.macrodroid.editscreen.EditMacroActivity`. This is bound to the exact final capture and separate endpoint command in **both variants of preserved run 38206460588**, with the observed enabled/clickable `edit_macro_addTriggerButton` selector. `reports/03-observed-final-component/` retains those four foreground records and two complete hierarchies byte-for-byte, their original archive-member/hash identities, exact resumed lines, and the pinned original journey/ZIP metadata. No component was inferred solely from a screen label or matching image.

The result advances to schema 4. Endpoint-to-own-capture matching, command/capture/input chronology, exact installed identity, process continuity, raw file uniqueness, input guards and the external physical-file ledger are retained. The comparison covers observed activity identities at scoped capture boundaries; it does **not** establish complete activity lifecycle equivalence, startup parity, absence of crashes, animation parity, macro execution, or whole-app 1:1.

## Measured host checks

All **42 focused tests pass in 19.340 seconds**: thirty session tests and all twelve unchanged external ledger tests. Four new methods reject a jointly changed candidate final capture/endpoint, reject the same wrong final class in both variants, detect activity differences at every intermediate paired screen with equal full pixels/XML, and accept equivalent component spelling. The final positive fixture now uses the actually observed editor class. The complete integration suite with the independently corrected Trigger05 overlay is pending a separate immutable follow-up; this checkpoint does not claim that unexecuted result.

The schema-4 Android gate remains **pending a fresh capture**. Historical artifacts and previous schema results are unchanged. The prior startup crashes and 26-pixel TRIGGERS failure remain failures. No screenshot is cropped, masked, rewritten or compared with tolerance.

## Review and integration

`inputs/` contains the thirty exact session02 baseline files; `proposed_files/` contains only the three replacements. Both an incremental patch from session02 and a cumulative patch from external 4745809 are provided. `validation-result.json` binds each old/new hash and actual test count. Check the declared baseline hashes and preserve concurrent changes before any later active integration. `checkpoint.json` deliberately has no automatic active-file mutations.
