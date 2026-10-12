# Isolated DayTrigger numeric source acceptance

This job evaluates the reviewed nineteen-file `DayTrigger.r0(DictionaryEntry)`
integration in a fresh hosted workspace. A successful result is a **WIP host
acceptance result**. The workflow does not promote or replace the active source or
APK, install either application, run Android, or establish full application parity.

## Immutable inputs

The job uses three sparse checkouts. The tooling checkout is the triggering commit;
the application baseline and the reviewed overlay have independent fixed commits.

| Role | Fixed identity |
| --- | --- |
| Application baseline | `dbcad968c5c3e8f084205393a6c0d2d06a203c71` |
| Reviewed overlay publication | `394234b0e74c9f1d660836c8f2a89901fe05ff9d` |
| Overlay capsule | `work-in-progress/day-trigger-numeric/06-source-integration/checkpoint.json` |
| Overlay checkpoint SHA-256 | `c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f` |
| Complete baseline input inventory | 81,291 files; snapshot `b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553` |
| Complete future input inventory | 81,298 files; snapshot `04b2867b722335f6b2b4910fc4ccba02e89bdbca52f80e1e9a9b9ac4b18fa1d4` |
| Future manifest bytes | 14,504,095 bytes; SHA-256 `25a60c227b5083b6e608b161ee403503b0232ad59368ba9603db5e6b8e00eb23` |

`pins.json` contains the complete nineteen copy roles, all twelve old-file hashes,
all seven absence requirements, the exact future manifest identity, the 91 compiled
Java fault selections, and the required result inventory. The future snapshot is
derived from every row of the exact baseline manifest. Missing baseline rows,
omitted overlay roles, extra changes, or a locally recorded substitute manifest
cannot define the expected result.

The workflow validates the SHA-256 of `runtime-files.json` before executing the
job tools. That manifest binds every top-level tool file. `prepare.py`,
`run_acceptance.py`, and `verify.py` each check it again. The source capsule's
complete 113-file inventory and its checkpoint are checked without editing them.

## Preparation and execution

`prepare.py` verifies both fixed Git commits and the original materializer, import
helper, vendor archive manifest, parent source workflow and unchanged release/test
drivers. It invokes the existing checksum-pinned v9 materializer in a fresh
destination. It then independently enumerates and hashes all 81,291 baseline
inputs before applying any change. All nineteen source payloads and old/absent
destinations are checked before the first atomic replacement. A second complete
scan must equal the independently derived 81,298-file inventory.

Historical `reports` and `dist` directories are moved into `prior-outputs`, with
unchanged file hashes recorded. The new acceptance reports directory initially
contains only the expected future input manifest; its `dist` directory is empty.
The input definition matches the existing release verifier: `source`,
`test-support`, `tests`, `signing`, `tools`, `reference` and root Python files,
excluding Python bytecode/cache paths and generated `tools/classes` paths. The
independent scan also rejects symlinks, special files and aliases between distinct
input paths.

`run_acceptance.py` records the actual Python and Java observations, exact child
command, resolved Python executable identity, stream hashes, start/end times and return code. It executes the unchanged
sixteen-gate acceptance sequence from the reviewed overlay, including the isolated
signed source-edit test and the final positive three-path run. The UI gate retains
its reviewed 5,400-second limit; each other gate retains 1,200 seconds. The outer
acceptance invocation is bounded to 6,600 seconds inside the 120-minute hosted job,
leaving time for setup and evidence upload. Its own process group is stopped at
completion or timeout so a descendant cannot continue mutating the disposable
workspace after the recorded invocation. A timeout or failure remains a failure.

## Required result

`verify.py` derives the full expected input inventory again, scans the actual final
source twice, checks all sixteen gate commands in order and their actual exit
codes, and verifies all 23 required fresh report hashes. Result paths must be
canonical, physically distinct and created/modified inside the recorded acceptance
interval. The Java-version and acceptance streams must use their exact distinct
filenames and fall within their own child invocation intervals. A prior report,
aliased log, skipped source-edit test or missing gate
prevents success.

The required numerical scope is 194,780 host cases over three paths, with 1,243
registered methods in 605 application classes. The original fixture contains
1,246 methods in 607 classes because three original field getters are test-only
dependencies and receive no recovery credit. The UI suite contributes 24,465 cases
over eleven registered methods. The job requires 308 actual Python test successes,
all 91 Java fault rejections with retained source/class hashes, complete positive
restoration, and two separate actual numeric D8/transplant fault rejections.

The numeric check replays all 1,291 raw observations and bit-derived expected
results; verifies all 32 original and 25 rebuilt instructions and both four-edge
inventories; reconstructs the exact 17-command D8/harness sequence, all input/output
arguments and all 34 distinct output streams; and binds the positive transplanted method to the actual signed APK's
instruction bytes. All 23 actual harness/oracle/host class files are retained with
their identities. The thirteen numeric Java faults remain part of the larger
91-control UI inventory. The two provenance rejections and byte-exact restoration
remain separate required checks. The command verifier binds the observed Java
executable and HotSpot library hashes to the exact JVM flag command and its raw
effective-flag output. Both provenance-test configurations must equal the positive
configuration with only their declared substitution. Recorded command arguments,
configuration names or stream files cannot substitute for those independently
reconstructed roles.

The unchanged baseline APK must reproduce its existing SHA-256. The new hybrid
APK's identity is measured from its actual bytes and must be bound by its code,
resource, host, numeric and source-edit reports. The workflow does not substitute
the previous hybrid artifact. The final status is
`ISOLATED_DAY_NUMERIC_ALL_16_HOST_GATES_VERIFIED` only when every required check
passes; `active_promoted` and full Android parity flags remain false.

## Evidence and local controls

The workflow always uploads the complete new `reports` and `dist` scope, the
preparation/execution/verification receipts, the complete old and future input
manifests, the exact nineteen overlay payloads, retained historical outputs,
runtime class evidence, host-control logs, and the exact job tools/workflow.
Temporary build caches and installed Java binaries are infrastructure; their
source/tool identities and actual runtime observations are recorded. Failed and
partial results are retained with their literal statuses.

Run the small policy controls with:

```sh
python3 -B -m unittest discover -s tools/day_numeric_acceptance -p 'test_*.py' -v
```

These controls use small synthetic report fixtures and actual bounded Python child
processes. They test inventory truncation, overlay omission, stale or physically
aliased artifacts, nonzero exits, skips, timeouts and source-preservation guards.
They do not claim that the full application build or 91 UI controls have executed.

The job inherits the pinned action versions and Java 21 setup from the reviewed
[source workflow](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/blob/dbcad968c5c3e8f084205393a6c0d2d06a203c71/.github/workflows/reconstruction.yml).
The explicit `ref`, `path`, `sparse-checkout`, cone mode and credential-persistence
inputs are defined in the pinned
[checkout action](https://github.com/actions/checkout/blob/11d5960a326750d5838078e36cf38b85af677262/action.yml).
No later action release or mutable application baseline is selected implicitly.
