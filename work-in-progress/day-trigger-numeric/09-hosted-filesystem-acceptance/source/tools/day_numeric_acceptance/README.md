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
| Reviewed overlay publication | `811f979eda1b937917c18defef38455c49a59062` |
| Overlay capsule | `work-in-progress/day-trigger-numeric/08-command-filesystem-source-successor/checkpoint.json` |
| Overlay checkpoint SHA-256 | `d9ddd3e0f692c66e2cd47870ff3cf95bfa0a2b1cd50fc2fd55a3c09e66df9bcf` |
| Complete baseline input inventory | 81,291 files; snapshot `b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553` |
| Complete future input inventory | 81,298 files; snapshot `f8fc1cadac8213468e42ac99a2cd5d807827dcdeee25166b8025620ff39a6545` |
| Future manifest bytes | 14,504,095 bytes; SHA-256 `896f3eb29dc832eb245fee8dcb70b0e8c8935c9635bf1ccc54c09987b26c91c6` |

`pins.json` contains the complete nineteen copy roles, all twelve old-file hashes,
all seven absence requirements, the exact future manifest identity, the 91 compiled
Java fault selections, and the required result inventory. The future snapshot is
derived from every row of the exact baseline manifest. Missing baseline rows,
omitted overlay roles, extra changes, or a locally recorded substitute manifest
cannot define the expected result.

The workflow validates the SHA-256 of `runtime-files.json` before executing the
job tools. That manifest binds every top-level tool file. `prepare.py`,
`run_acceptance.py`, and `verify.py` each check it again. The source capsule's
complete 408-file inventory and its checkpoint are checked without editing them.
This source successor changes only command-evidence instrumentation in
`day_numeric_dex_controls.py`; the other eighteen overlay files remain byte-identical
to the earlier source capsule. Its complete old/new input binding, semantic AST
comparison, first producer attempt, exceptional-cleanup counterexample, and
corrected sixteen-control evidence remain in that immutable capsule.

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
command, resolved Python executable identity, stream hashes, integer Unix and
monotonic operation clocks, filesystem witnesses, and return code. A zero-exit
Java observation with a recording/cleanup error stops before the acceptance child.
The wrapper executes the unchanged
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
filenames and complete exclusive-creation receipts, with separately ordered
integer command clocks and the actual filesystem bracket described below. A prior report,
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

## Exact command file creation and clocks

Hosted run [38232050667](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38232050667)
failed in the 67 tooling controls before materialization or an application build.
The [unchanged raw artifact](../../docs/verification/day-numeric-hosted-run-5c402b4/)
retains 64 successes, two errors and one dependent failure. It did not record those
fixtures' exact stat deltas. The separate unchanged-source diagnosis retained eight
actual empty subprocesses whose sixteen streams had inode timestamps before a
precise clock sampled immediately before exclusive creation. This is a coarse
filesystem-clock issue. Floating-point conversion of an epoch timestamp and ISO
microsecond truncation were distinct additional precision problems; the successor
uses integer conversions throughout.

For each Java-version, acceptance, and numeric D8/harness command, the producer:

1. Records exact integer Unix and monotonic nanoseconds; ISO is derived from the
   same Unix value, with no floating-point epoch conversion.
2. Exclusively creates and closes one empty witness in the stream directory.
3. Opens stdout and stderr using `xb`, recording the operation clocks, initial
   empty fstat/hash, and later final fstat/hash and closure clocks for each file.
4. Preserves every exclusive after-witness observation until the first actual
   filesystem clock brackets both streams' initial and final mtime/ctime values.
   There are at most sixteen observations, with a requested five-millisecond wait
   between failed observations: at most fifteen waits. A missing bracket fails.

The observer never changes a timestamp or adds a tolerance. Repeated observations
allow a coarse filesystem clock to advance past a recently written fine timestamp.
The 120-second numeric subprocess limit, 15-second Java-observation limit and
6,600-second outer acceptance limit stay unchanged. Exception paths attempt every
owned descriptor's cleanup, retain cleanup errors and preserve an original child
exception; they never turn that evidence into success.

The independent verifier reconstructs all roles and exact argv, checks the live
files against recorded final fstat/hash, enforces one regular inode and one link,
and checks the ordered exclusive-open, invocation, closure and witness clocks.
Both Unix and monotonic clocks must move forward. All unsuccessful witnesses must
precede the first successful one; missing, reordered, borrowed or later selected
witnesses reject. The literal sixteen-observation and five-millisecond policy is
fixed. Empty files with unchanged creation/final metadata are valid, including
observed equal filesystem ticks.

**Live verification and archive replay have different metadata scopes.** The
hosted verifier compares original inode/ctime and bytes while those files still
exist. The artifact retains the exact serialized original observations and bytes.
Extraction creates other inodes and ctimes, so a later replay must verify its raw
byte identities and recorded observations without treating extraction metadata as
the hosted stat. This tooling does not silently substitute extracted metadata or
claim that a post-extraction live-stat check occurred on the runner.

The clock interpretation follows the primary [Linux multigrain timestamp
documentation](https://cdn.kernel.org/doc/html/latest/filesystems/multigrain-ts.html),
[Linux timekeeping accessors](https://cdn.kernel.org/doc/html/latest/core-api/timekeeping.html),
and [Python datetime precision](https://docs.python.org/3.12/library/datetime.html).

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
The hosted test step also retains each owned fixture's raw files, recorded
creation receipts, and original stat inventory under `hosted-tool-control-evidence`.
Intentional symlink faults are retained as inert descriptions. This output is
separate from preparation and cannot populate the fresh application result scope.
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
The successor adds witness ownership/order, actual replaced inodes and stale
mtime, live-stat mismatch, both fine-clock reversals, exact integer precision,
partial cleanup and zero-exit fail-fast controls. Actual small empty subprocesses
check the complete live creation receipt; synthetic command rows explicitly have
synthetic contents and do not execute Java.
They do not claim that the full application build or 91 UI controls have executed.

The job inherits the pinned action versions and Java 21 setup from the reviewed
[source workflow](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/blob/dbcad968c5c3e8f084205393a6c0d2d06a203c71/.github/workflows/reconstruction.yml).
The explicit `ref`, `path`, `sparse-checkout`, cone mode and credential-persistence
inputs are defined in the pinned
[checkout action](https://github.com/actions/checkout/blob/11d5960a326750d5838078e36cf38b85af677262/action.yml).
No later action release or mutable application baseline is selected implicitly.
