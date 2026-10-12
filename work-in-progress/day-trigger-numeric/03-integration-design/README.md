# Inactive DayTrigger integration design

The independently reviewed `DayTrigger.r0(DictionaryEntry)I` helper is approved for a small, isolated integration study. This checkpoint preserves the exact design before any integration compilation. It changes no active application, fixture, source registry or workflow.

The [proposal](proposal.json) pins all 19 proposed paths against the active 1,242-method input snapshot `b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`, published from application checkpoint `dbcad968c5c3e8f084205393a6c0d2d06a203c71`. Existing paths require exact baseline hashes; seven new paths must be absent. The six expressly unchanged inputs include the active `BytecodeOracle.java`, production build and constructor-owner code, the main test driver and existing Widget fault catalog/tests.

The preceding [independent review](../../../docs/verification/day-trigger-numeric/01-independent-review/README.md) verifies the original-APK extraction, 1,291 bit-precise numeric expectations, three recorded execution paths, 13 compiled Java faults, two actual D8/transplant faults and two provenance controls. Its checkpoint SHA256 is `30567165fc992e16e52ef0ba90636d13c17f7560b70c00b4fe1478cf00fbbf4f`. That evidence remains separate from pending integration results.

## Approved implementation boundaries

The helper adds one registered method. The three original field getters are test-fixture dependencies and earn no recovered-method credit. Expected integrated counts are 1,243 registered methods in 605 target classes, and 1,246 test-fixture methods in 607 classes. The UI partition grows to 11 recovered methods and adds the exact 1,291 numeric cases. Those counts must be computed and verified after integration.

The existing public final `VariableValue` fields, constructors, equality and observable encodings remain intact. Private transient aliases support the original getter instructions without adding serialized fields. A measured regression must compare existing canonical, Gson and event observations before and after the aliases.

All 78 existing UI fault controls remain. The 13 Day Java faults join the UI control runner; two actual rebuilt-DEX faults run as a separately reported stage with class/source/fixture identities, production relocation and transplant binding, independent-path checks and exact restoration. The existing 16-gate acceptance structure and its declared command budgets remain.

No full source copy, app build, signed release, Android execution, calendar behavior or application parity is claimed by this design. Later numbered checkpoints will preserve actual integration attempts and results without rewriting this initial plan.
