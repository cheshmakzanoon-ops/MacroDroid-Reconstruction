#!/usr/bin/env python3
"""Prepare publication docs for the exact closed combined source/APK proof."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import difflib
import json
from pathlib import Path

from prepare_merge_overlay import identity, replace_once, require, write_json

EVIDENCE = '../work-in-progress/combined-recovery/05-full-acceptance'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--proof', type=Path, required=True)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    proof = json.loads(args.proof.read_text())
    require(proof['passed'] is True and proof['status'] == 'COMBINED_ALL_16_ACCEPTANCE_GATES_PASSED',
            'Closed acceptance required before current-evidence prose')
    root, output = Path(proof['project']), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    pin = json.loads((root / 'reports/release-input-snapshot.json').read_text())
    changes = []

    def save(name, text, original):
        require(name.removeprefix('project/') not in pin['entries'], 'Documentation unexpectedly is a pinned build input')
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        before = identity(original)
        old = original.read_text()
        path.write_text(text)
        require(identity(original) == before, 'Documentation source changed')
        changes.append({'path': name, 'source': str(original), 'before': before,
                        'after': identity(path), 'build_input': False})
        patch = output / 'patches' / (name.replace('/', '_') + '.patch')
        patch.parent.mkdir(parents=True, exist_ok=True)
        patch.write_text(''.join(difflib.unified_diff(old.splitlines(True), text.splitlines(True),
                        fromfile='a/' + name, tofile='b/' + name)))

    readme = (root / 'README.md').read_text()
    readme = replace_once(readme, '''This private combined candidate adds plugin upload and Widget update bodies to the
published 1,240-method source. Its fresh original-method fixture and complete source
copy are verified; full combined acceptance and the separate Android method/journey
measurements are pending. The isolated methods have their own passing signed proofs.
See `RECONSTRUCTION_STATUS.md` and `COMBINED_RECOVERY.md` for exact boundaries and
the distinction between current, inherited and still-pending evidence.''', f'''This combined candidate adds plugin upload and Widget update bodies to the prior
1,240-method source. Its complete configured acceptance passed on 12 October 2026:
all 16 gates, 193,489 three-path cases across 1,242 methods, 273 Python tests, all 78
UI faults with exact positive restoration, and the signed source-edit experiment.
The [closed proof]({EVIDENCE}/result.json) binds the exact source and signed APK.
Android observations for this new combined APK remain pending. See
`RECONSTRUCTION_STATUS.md` and `COMBINED_RECOVERY.md` for measured scopes.''', 'current project readme')
    readme = replace_once(readme, '''The historical local environment lacked ADB/emulator execution. A later hosted run
installed and cold-launched both APKs with complete captures; exact comparison
reported 75 differing pixels in Android's signal-strength icon. Actual macro execution,
permissions, accessibility, background work, persistence/reboot, native loading and
performance have not been verified by that capture.
The host interpreter is not ART, and host test doubles are not Android services.''', '''The historical Android runs retain their exact source/APK identities. The prior
9108 candidate's ten-screen observation completed and retained a 26-pixel indicator
difference on the second intro page; all ten XML pairs matched. Both APKs also
encountered the supplied promotion-listener exception. The isolated Widget APK
passed a separate eight-case ART method probe. Those results do not execute this
new combined APK or establish full macro, service, persistence or device behavior.
The host interpreter and controlled dependencies have their own explicit scope.''', 'current runtime evidence')
    save('project/README.md', readme, root / 'README.md')

    ui = (root / 'UI_RECOVERY.md').read_text()
    ui = replace_once(ui, 'constant/no-op bodies. Combined acceptance is still pending for this source copy.',
                      'constant/no-op bodies. All 16 configured acceptance gates passed for this source copy.', 'UI current scope')
    ui = replace_once(ui, '''The combined source prepares 23,174 UI cases, 15,326 independent expected-result
checks, and all 78 actual Java fault controls. It retains multi-edit occurrence
counts, every required case label, the same original instruction coverage, actual
mutant source/classes, and exact full positive restoration. The complete run has
not executed yet. `COMBINED_RECOVERY.md` describes both methods and the host runtime
policy; the original message normalizer remains unchanged.''', f'''The combined source passed 23,174 UI cases, 15,326 independent expected-result
checks, and all 78 actual Java fault controls. Every required case rejected its
intended defect, with zero unsupported executions and unchanged original coverage;
the final clean UI run restored the complete positive baseline exactly. The actual
78-control gate took 2,661.218 seconds. All retained mutant sources/classes and
the [fresh control report]({EVIDENCE}/reviewable/ui-negative-controls.json) are
bound in the closed proof. `COMBINED_RECOVERY.md` describes both methods and the
host runtime policy; the original message normalizer remains unchanged.''', 'UI completed proof')
    save('project/UI_RECOVERY.md', ui, root / 'UI_RECOVERY.md')

    combined = (root / 'COMBINED_RECOVERY.md').read_text()
    combined = replace_once(combined, 'This is the first\nactive mapping proposed for the published registry; earlier methods had zero.',
                            'This is the first\nactive mapping in this registry; earlier published methods had zero.', 'mapping status')
    combined = replace_once(combined, '''The original constructor-only ART probe already succeeded with `-Xverify:all` on
the pinned API 35 emulator. It executed the original allocation only. The separate
eight-case actual Widget method wrapper has its own pending device run against
the exact original and isolated Widget APK; it does not render a Widget or cover
nonempty lists, services, scheduling or real device lifecycle behavior.''', '''The original constructor-only ART probe succeeded with `-Xverify:all` on the
pinned API 35 emulator. The separate original/isolated-Widget method probe also
passed all eight cases in hosted run 38209599059: each guest exited zero, with
379 bytes of identical stdout and empty stderr. All 7,214 artifact members,
including the exact hidden workflow, and all 19 executed input copies were
independently verified. See [the complete ART proof](../work-in-progress/widget-art/08-hosted-complete-proof/).
These cases cover empty/resumed lists, invalid labels, saved-field casts and a
null list; they do not render a Widget or cover nonempty lists, services,
scheduling, complete lifecycle behavior, or this new combined APK.''', 'actual Widget ART proof')
    combined = replace_once(combined, '## Combined proof still required', '## Completed combined host and artifact proof', 'combined proof heading')
    combined = replace_once(combined, '''The new copy verifies all 81,245 baseline input files before/after independent
copying, overlays only the frozen reviewed sources, and extracts a fresh complete
original fixture for exactly 1,242 methods across 605 classes. Both prior isolated
fixtures remain historical. The expected combined inventory is 193,489 cases,
23,174 UI cases across ten methods, 15,326 independent UI expectations, 273 Python
tests and all 78 deliberate UI faults. Full configured acceptance, including the
signed source-edit experiment and final complete positive run, remains pending.''', f'''The independent source preparation verified all 81,245 baseline inputs before
and after copying, applied only the frozen reviewed changes, and freshly extracted
the original fixture for 1,242 methods across 605 classes. The resulting 81,291
inputs retained the same pin before and after all 16 configured acceptance gates:

`{proof['source_input_snapshot_sha256']}`

The complete run passed 193,489 cases on all three paths, including 23,174 UI cases
across ten methods, 15,326 independent UI expectations, 273 Python tests and all
78 deliberate UI faults. The signed source-edit experiment and final complete
positive run both passed. The wrapper independently checked all 16 gate logs,
22 fresh report hashes, every retained mutant source/class pair, and both final
signed APK identities. The closed [result]({EVIDENCE}/result.json) and
[complete report manifest]({EVIDENCE}/complete-reports-manifest.json) preserve
the actual outcomes; the configured acceptance subprocess took 4,800.347 seconds.

The 94,683,119-byte combined APK SHA256 is
`{proof['apks']['hybrid']['sha256']}`.
Its separate Android measurements and clean hosted reproduction remain pending.
The isolated Widget and upload reports retain their own source/APK identities.''', 'combined completed measurement')
    save('project/COMBINED_RECOVERY.md', combined, root / 'COMBINED_RECOVERY.md')

    status = f'''# Current reconstruction progress

The current combined source compiles **1,242 registered Java method bodies across
605 classes**, including ten UI-family methods. It adds plugin upload and Widget
update to the prior 1,240-method candidate. **All 16 configured host acceptance
gates passed** for this exact source and APK on 12 October 2026. Whole-application
1:1 Android behavior remains unestablished.

The comparison target is the supplied MacroDroid 5.67.8 APK, package
`com.arlosoft.macrodroid`, version code `896700008`. Most executable logic still
builds from preserved editable smali; native libraries and opaque assets remain
original binaries. The number of recovered Java methods is not a parity percentage.

## Current source and signed artifact

| Identity | Exact value |
| --- | --- |
| Source input files | 81,291; rehashed before/after acceptance and freezing |
| Input snapshot SHA256 | `{proof['source_input_snapshot_sha256']}` |
| Registered bodies / classes | 1,242 / 605 |
| Fresh original-method fixture SHA256 | `bfc27193f5fcd067e374ba2715e52e9eac067ea78c752189dba8c0ab0c7bb27e` |
| Signed combined APK bytes | 94,683,119 |
| Signed combined APK SHA256 | `{proof['apks']['hybrid']['sha256']}` |
| Preserved baseline SHA256 | `{proof['apks']['baseline']['sha256']}` |

The [complete acceptance report]({EVIDENCE}/reviewable/acceptance-latest.json)
records all commands, limits, exits and evidence hashes. The
[independent closing check]({EVIDENCE}/result.json) verifies the source boundaries,
16 gate logs, 22 fresh reports, 78 retained mutant source/class pairs and exact
signed APKs. All 551 closed reports and the signed candidate bytes are preserved
in the [immutable checkpoint]({EVIDENCE}/).

## Evidence by exact scope

| Scope | Completed measurement | Remaining requirement |
| --- | --- | --- |
| Current combined host/artifact acceptance | All 16 gates; 193,489 original/JVM/rebuilt cases over all 1,242 methods; zero mismatches and unsupported executions; 273 Python tests | Clean hosted reproduction and Android execution of this exact new APK |
| Current combined UI controls | 23,174 cases / ten methods; 15,326 independent expectations; all 78 compiled faults detected; exact positive restoration | Real UI feature, lifecycle and integration behavior |
| Signed source-edit experiment | Fresh controlled source edit reached the signed APK; complete final positive run passed | This proves the editable build path within its measured scope |
| Prior 1,240-method hosted source | Two complete hosted 16-gate successes; 188,791 cases and 259 Python tests each | Historical source/APK identities remain separate |
| Isolated plugin upload | 191,147 three-path cases; all 163 original instructions and 26 conditional edges; 54 UI faults and exact restoration | Actual plugin/network behavior on Android |
| Isolated Widget source | 191,133 three-path cases; all 194 original instructions and 20 conditional edges; 265 Python tests; prior 24 compiled faults rejected | Real nonempty Widget rendering, scheduling and service behavior |
| Original/isolated Widget ART probe | Eight cases per APK under verification; identical stdout, zero exits, complete 7,214-member hosted archive | This limited probe does not execute the combined APK or a nonempty Widget |
| Prior 9108 ten-screen Android observation | Both runs complete; all ten XML pairs match; changed pixels `[0,26,0,0,0,0,0,0,0,0]` | The second-page indicator difference and broader Android scope remain unresolved |

The original/isolated Widget Android record is
[run 38209599059](../work-in-progress/widget-art/08-hosted-complete-proof/).
The prior ten-screen observation is
[run 38205737183](../docs/verification/editor-journey/run-38205737183-attempt-1/).
Neither result is relabelled as a measurement of the new combined APK.

## Reproduction

The repository materializer verifies the committed multipart source/toolchain
archives and applies the active `project/` overlay. Historical `work-in-progress/`
checkpoints are not applied automatically. From a fresh materialized source tree
with Python 3.11+ and JDK 21:

```sh
python3 release_integrity.py verify
python3 acceptance.py
```

The UI fault suite has a measured 5,400-second outer budget and each individual
UI execution is limited to 300 seconds. Other acceptance gates retain 1,200-second
budgets. The source CI job allows 120 minutes. A failure stops acceptance and
retains raw evidence; no comparison threshold is relaxed by these time budgets.

## Android differences and further work

The prior original and 9108 candidate both encountered the supplied promotion
listener's Fragment-not-attached exception after notification denial. That shared
stack does not establish a crash-free or identical complete lifecycle. The
bounded continuation policy preserves raw crash records and checks installed
identity, process boundaries and fresh observations before each further input.

The ten-screen scale-zero run retained a stable 26-pixel indicator difference on
the second intro page. The original APK itself produced both observed indicator
renderings across preserved runs. The cause remains unestablished. A separately
pinned scale-one diagnostic compares the same original and 9108 APKs using the
unchanged full-PNG/XML rule; its result must remain distinct from this source proof.
No crop, mask, pixel tolerance or cross-APK frame selection is used to claim a match.

The shared capture guard now has a reviewed correction for stale chronology and
physical file reuse; the scoped session verifier also checks capture/input timing
and paired foreground activity components. Their fresh Android results must be
measured with the exact activated verifier, while historical reports remain intact.

Complete high-level Java/Kotlin recovery, native source, the publisher's signing
identity and full runtime equivalence remain unestablished. Macro execution,
permissions/services, persistence and reboot, widgets, integrations, locales,
devices/API versions and performance require their own observed evidence.
See `COMBINED_RECOVERY.md` and `UI_RECOVERY.md` for the current recovered bodies.
'''
    save('project/RECONSTRUCTION_STATUS.md', status, root / 'RECONSTRUCTION_STATUS.md')

    top_source = args.repository.resolve() / 'README.md'
    top = top_source.read_text()
    top = replace_once(top, 'contains 1,240 recovered Java method bodies across 603 classes',
                       'contains 1,242 recovered Java method bodies across 605 classes', 'repository registry count')
    start = top.index('The current source checkpoint is described in\n')
    end = top.index('\n## Get the working source', start)
    top = top[:start] + '''The current source checkpoint is described in
[RECONSTRUCTION_STATUS.md](project/RECONSTRUCTION_STATUS.md). The combined plugin
upload and Widget candidate passed all 16 configured host acceptance gates,
193,489 three-path cases, 273 Python tests, all 78 UI fault controls with exact
positive restoration, and the signed source-edit experiment. Its exact source,
signed APK and every closed report are retained in the
[complete combined proof](work-in-progress/combined-recovery/05-full-acceptance/).
Clean hosted reproduction and Android measurements for this new APK have their
own pending scopes. The [verification workflow](.github/workflows/reconstruction.yml)
records those actual outcomes separately; previous hosted/device results retain
their original source and APK identities.
''' + top[end:]
    top = replace_once(top, '94,683,497 bytes, SHA-256\n`9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`.',
                       '94,683,119 bytes, SHA-256\n`5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`.', 'repository APK')
    start = top.index('The active 1,240-body plugin/runtime checkpoint passed five clean integration\n')
    end = top.index('\nThe previous combined 1,239-body', start)
    top = top[:start] + '''The active 1,242-body combined source passed all 16 configured acceptance gates:
signed baseline/hybrid builds, complete code and resource verification, the full
three-path host suite, all fault families, the signed source-edit experiment,
final positive restoration and unchanged source-input checks. It ran 193,489
cases with zero mismatches or unsupported executions and passed 273 Python tests.
The ten-method UI group passed 23,174 cases with 15,326 independent expectations;
all 78 deliberate UI faults were detected and the full positive baseline restored.
All 551 closed reports and the exact signed artifact are preserved in
[the current combined evidence](work-in-progress/combined-recovery/05-full-acceptance/).

The prior 1,240-body source separately passed two complete hosted acceptance runs,
38200503458 and 38202401393, with 188,791 cases and 259 Python tests each. Its
9108 candidate also has a complete ten-screen Android observation with a remaining
26-pixel intro indicator difference. The isolated Widget candidate passed a
separate eight-case ART probe. These historical measurements do not certify the
new combined APK's unobserved Android behavior.
''' + top[end:]
    top = replace_once(top, '| Active combined host/artifact proof | All five planned checks; 188,791 three-path cases across 1,240 bodies; 259 Python tests; exact signed candidate reproduced | [Complete combined evidence](docs/verification/plugin-runtime-integration/) |',
                       '| Active combined host/artifact proof | All 16 configured gates; 193,489 three-path cases across 1,242 bodies; 273 Python tests; all 78 UI faults and exact restoration | [Complete combined evidence](work-in-progress/combined-recovery/05-full-acceptance/) |', 'current evidence table row')
    top = replace_once(top, '## Measured Android cold launch and four intro stills',
                       '## Historical Android cold launch and four intro stills', 'historical Android heading')
    top = replace_once(top, '[The latest hosted Android evidence](docs/verification/android-ci-95077fc/)',
                       '[The preserved 1,239-body hosted Android evidence](docs/verification/android-ci-95077fc/)', 'historical Android label')
    save('README.md', top, top_source)
    add = output / 'finalize_combined_docs.py'
    add.write_bytes(Path(__file__).read_bytes())
    write_json(output / 'changes.json', {'status': 'COMPLETED_COMBINED_PROOF_DOCUMENTED_FOR_COHERENT_PROMOTION',
        'created_utc': datetime.now(timezone.utc).isoformat(), 'proof': {'path': str(args.proof), **identity(args.proof)},
        'changes': changes, 'application_build_inputs_changed': False, 'active_source_changed': False,
        'activation_condition': 'Promote only with the exact closed combined source/APK after the old-candidate normal-animation diagnostic checks out its reviewed commit.'})
    files = [{'path': path.relative_to(output).as_posix(), **identity(path)}
             for path in sorted(output.rglob('*')) if path.is_file()]
    write_json(output / 'checkpoint.json', {'status': 'CURRENT_COMBINED_DOCUMENTATION_PREPARED',
        'source_input_snapshot_sha256': proof['source_input_snapshot_sha256'], 'apk': proof['apks']['hybrid'],
        'active_changes': False, 'files': files})
    print(json.dumps({'checkpoint': str(output / 'checkpoint.json'), **identity(output / 'checkpoint.json'),
                      'files': len(files), 'documents': len(changes)}, indent=2))


if __name__ == '__main__':
    main()
