# Editor journey precondition regressions

The independent editor-journey recorder and comparator now use evidence schema 2. This checkpoint contains host verification only. No Android device or application was executed for these checks, and the results establish no additional runtime parity.

## Findings and changes

The previous recorder started its 15-second freshness clock after the entire precondition snapshot had completed. UI dump, retrieval and screenshot latency therefore did not count toward the deadline. The recorder now starts the clock before acquisition, performs the UI and target checks, records a new PID and foreground observation immediately before input, and checks the full elapsed time before sending the tap or Back command. A changed PID, wrong foreground owner or expired precondition stops input.

The previous comparator compared raw hierarchy path strings. A synthetic report using `candidate-snap/h.xml` for the previous capture and `candidate-snap/./h.xml` for the purported fresh precondition referred to the same file and still passed. The retained source at commit `383c9ad798a4699b940152794c12f65f97c73493` reproduces that false positive. The fixed comparator validates artifact bytes and path confinement, then compares resolved file paths and rejects the reuse.

Schema 2 requires both immediate pre-input observations. Their files must be distinct from the previous capture and fresh snapshot files; their hashes, PID continuity and expected foreground owner are checked. Schema 1 reports retain their historical meaning and are rejected by this stricter comparator. Existing historical evidence is unchanged.

## Measured host results

[The actual test log](host-tests.log) records **23 passing tests in 6.124 seconds**: the 12 existing tests and 11 focused additions. The new tests cover missing or modified immediate evidence, stale-file reuse, a process restart, a foreground departure, capture delays, and the normalized path alias.

[The verification record](host-verification.json) binds both source-file hashes and the test-log hash. It also records an actual before/after replay of the path-alias report and five traces through the real snapshot and transition code using virtual ADB responses and a virtual clock:

| Synthetic case | Observation |
| --- | --- |
| Fresh snapshot | One tap recorded after new PID and foreground checks; precondition age 1.20 seconds |
| UI retrieval delayed 20 seconds | Expired at 20.45 seconds; zero input commands |
| Final foreground check delayed 20 seconds | Expired at 21.20 seconds; zero input commands |
| PID changed after snapshot | Rejected; zero input commands |
| Foreground changed after snapshot | Rejected; zero input commands |

These virtual traces exercise the recorder's acquisition order and rejection behavior. They do not substitute for a new device capture. The existing full screenshot and UI-attribute comparison scope, notification-denial selector, APK identity checks and independent journey plan are preserved.

Run the host checks from the repository root:

```sh
python -m unittest discover -s tools/parity_journeys -p 'test_*.py' -v
```
