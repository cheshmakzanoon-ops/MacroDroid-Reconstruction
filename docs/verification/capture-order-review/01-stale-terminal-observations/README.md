# Read-only review: pre-input captures accepted as terminal observations

The inactive twelve-screen Trigger02 study and its unchanged existing ten-screen policy both accepted a synthetic terminal capture recorded before the final input. The exact 81-file input capsule and its checkpoint are copied under `inputs/`, matching durable commit `c1a6d71d2e290d16ea3a047d036996f79005883a` at `work-in-progress/trigger-category/02-reviewed-host-success/`.

For each sequence, the reproduction first requires a passing clean synthetic baseline. It then removes both genuine terminal acquisition ledgers and their two full observation sets: 26 files across original/candidate. It removes those two ledger references from `capture_events` and substitutes each preceding still for the terminal shot, changing only the declared screen name. The matching terminal PNG/XML therefore comes entirely from before the final input. The two false positives are:

| Sequence | Reused original/candidate observation ends | Original/candidate final input starts | Incorrect accepted scope |
| --- | --- | --- | --- |
| Twelve screens | 1056.6 / 2056.6 | 1059.4 / 2059.4 | `EXACT_TRIGGER_CATEGORY_OBSERVATION_ONLY`, surface after Date/Time tap |
| Ten screens | 1045.8 / 2045.8 | 1048.9 / 2048.9 | `EXACT_OBSERVED_DIALOG_JOURNEY_MATCH_ONLY`, surface after OK |

The shared guard validates each acquisition's internal timing and requires its ledger to exist, but permits one accepted ledger to be used by multiple screen records. It also omits a check that the next acquisition starts after its corresponding input command finishes. The successful reproduction proves this missing relationship without changing timestamps, hashes, input arguments, prior screens, APK declarations or process guards.

Two additional controls change only the candidate final input to `input tap 1 1`; both correctly return `REJECTED` with the recorded target-command error. The scripts, complete pre-mutation and mutated report documents, removed-file inventories, final verdicts and the complete artifact set actually presented to each mutated comparator are preserved. The intentionally removed terminal file bytes are not in that final artifact set; their hashes remain in the removed-file inventories and the pinned fixture code reproduces their contents. `synthetic-comparator-inputs.zip` holds all remaining artifact files with an independently verified member inventory.

## Actual ten-screen run remains a measured difference

A separate read-only audit of the unchanged 15,156,144-byte run38205737183 ZIP verified all38 accepted acquisition ledgers were distinct, all456 observation artifact paths were distinct, and all18 actual next captures started after their input commands finished. The actual chronology therefore does not exhibit this synthetic stale-terminal defect. `actual-ten-chronology.json` records every input-to-capture interval and the exact ZIP/journey hashes. It does not rerun Android or replace the existing `JOURNEY_DIFFERENCE` verdict, including the26 TRIGGERS pixels.

No active source or workflow was modified, and neither reproduction executed Android. The Trigger02 study remains inactive. The proposed correction should reject reuse of accepted capture identities and bind each resulting capture to the completed input before it, then replay the unchanged actual ten-screen evidence. Historical failed and passing source/runtime reports must remain intact.

The executed scripts retain explicit historical study paths. The complete pinned source and report inputs are included for an isolated replay; use a fresh output directory and preserve these frozen originals.
