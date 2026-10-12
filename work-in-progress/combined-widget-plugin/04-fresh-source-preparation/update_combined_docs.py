#!/usr/bin/env python3
"""Describe the combined candidate without treating inherited evidence as current."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from prepare_merge_overlay import identity, replace_once, require, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preparation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    preparation = json.loads(args.preparation.read_text())
    require(preparation["passed"] is True, "Source preparation did not pass")
    root = Path(preparation["private_project"])
    pin = preparation["candidate_inputs"]["snapshot_sha256"]
    args.output.mkdir(parents=True, exist_ok=False)
    changes = []

    def save(relative, text):
        path = root / relative
        previous = identity(path) if path.exists() else None
        path.write_text(text)
        changes.append({"path": relative, "before": previous, "after": identity(path), "build_input": False})

    text = (root / "README.md").read_text()
    text = replace_once(text, "1,237 selected method bodies across 602 classes", "1,242 selected method bodies across 605 classes", "current registry count")
    text = replace_once(text, "## Extract and build", """## Current candidate and evidence

This private combined candidate adds plugin upload and Widget update bodies to the
published 1,240-method source. Its fresh original-method fixture and complete source
copy are verified; full combined acceptance and the separate Android method/journey
measurements are pending. The isolated methods have their own passing signed proofs.
See `RECONSTRUCTION_STATUS.md` and `COMBINED_RECOVERY.md` for exact boundaries and
the distinction between current, inherited and still-pending evidence.

## Extract and build""", "source-copy scope")
    text = replace_once(text,
                        "The new drag-event, sound/SMS validation and scene-state methods are under\n`source/java/recovered/ui/`; dispatcher helpers remain under `source/java/recovered/engine/`.",
                        "Touch events, selection validation, scene state/dispatch, plugin lookup/upload and\nWidget update bodies are under `source/java/recovered/ui/`; dispatcher helpers remain\nunder `source/java/recovered/engine/`.", "current helper families")
    text = replace_once(text,
                        "The final `QUALITY_REPORT.md` distinguishes measured\nresults from unresolved gates. Historical reports are not current acceptance.",
                        "`RECONSTRUCTION_STATUS.md` distinguishes current measured results from unresolved\ngates. `QUALITY_REPORT.md` and older reports retain their historical scope.", "current status authority")
    save("README.md", text)
    ui = (root / "UI_RECOVERY.md").read_text()
    ui = replace_once(ui, "# UI, scene-state, selection, touch-blocking, scene-dispatch and plugin recovery",
                      "# UI, scene, plugin and Widget recovery", "UI title")
    ui = replace_once(ui,
                      "Eight existing method bodies in this family are compiled from readable Java. The full\nregistry has 1,240 bodies across 603 classes; 1,119 are prior constant/no-op bodies.",
                      "Ten existing method bodies in this family are registered for compilation from readable\nJava. The combined registry has 1,242 bodies across 605 classes; 1,119 are prior\nconstant/no-op bodies. Combined acceptance is still pending for this source copy.", "combined UI counts")
    anchor = "`source/ui-methods.json` pins the exact descriptors and original method hashes."
    addition = """| `plugins.k.invokeSuspend(Object)` | `PluginUploadMethods.upload` | Optional icon preparation/upload, plugin upload, two suspension states and original result/error publication |
| `WidgetUpdateManager.m(Context,List,o73)` | `WidgetUpdateMethods.update` | Continuation reuse, original list iteration and saved-state protocol, two suspension boundaries and narrow exception handling |

"""
    ui = replace_once(ui, anchor, addition + anchor, "two new method rows")
    ui = replace_once(ui, "## Executed host comparisons", """## Combined candidate evidence

The two methods contribute 2,356 plugin-upload cases and 2,342 Widget cases. Their
isolated signed candidates passed all three execution paths, complete code and
resource comparisons, and unchanged-input checks. The upload proof rejected all
54 then-configured UI faults and passed its clean 20,832-case rerun. The independent
Widget mutation study rejected all 24 compiled faults and both class-origin controls.
The Widget signed five-gate proof passed 191,133 total cases and 265 Python tests.
These are separate source/APK identities, not an executed combined result.

The combined source prepares 23,174 UI cases, 15,326 independent expected-result
checks, and all 78 actual Java fault controls. It retains multi-edit occurrence
counts, every required case label, the same original instruction coverage, actual
mutant source/classes, and exact full positive restoration. The complete run has
not executed yet. `COMBINED_RECOVERY.md` describes both methods and the host runtime
policy; the original message normalizer remains unchanged.

## Inherited eight-method host comparisons

The rest of this measured-host section records the published 1,240-method baseline,
whose complete hosted acceptance passed before these two bodies were combined.
Its counts and artifact identities are historical; they do not certify this candidate.
""", "inherited UI evidence heading")
    save("UI_RECOVERY.md", ui)
    save("COMBINED_RECOVERY.md", """# Combined plugin upload and Widget source recovery

## Source and behavior

`PluginUploadMethods.upload` supplies the body of `plugins.k.invokeSuspend(Object)`.
It preserves the optional icon path, the ignored PNG compression return value,
captured request companion, original default-argument mask, icon fallback, both
suspension labels and identity checks, saved-field casts/clearing, repeated HTTP
status reads, success/error publication order and the original Exception boundaries.
Controlled host dependencies perform no network request or real coroutine scheduling.

`WidgetUpdateMethods.update` supplies `WidgetUpdateManager.m(Context,List,o73)`.
It preserves high-bit continuation reuse/clearing, labels 0/1/2, original saved-field
casts including otherwise unused reads, the unchanged saved index, ordered state
writes and identity-based suspension handling. It retains the original Exception-only
catch. Logger and exception-message failures still escape, and the caught message
is read before the StringBuilder is allocated. The Java helper uses explicit original
owners where required; no helper or host-stub class is shipped in the APK.

The one declared constructor-owner mapping translates the compiled `zhh` child
constructor reference back to the original direct-parent `rff` owner. Allocation
type and original constructors remain unchanged. Build, static and linkage checks
share the existing source/domain/descriptor/occurrence guards. This is the first
active mapping proposed for the published registry; earlier methods had zero.

## Independent completed evidence

The isolated upload proof passed 191,147 cases over 1,241 methods and three paths,
all 54 UI faults and exact 20,832-case restoration, full code verification and
resource/native payload checks. Its signed APK is
`e4643b554429743703bed5c1aa5e3541dbfc0705d9fd87c353bd968f348baf80`.
The original upload method visited all 163 instructions and 26 conditional edges.

The isolated Widget signed proof passed all five planned gates, 191,133 cases over
1,241 methods and three paths, and all 265 Python tests. Its signed APK is
`b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f`.
The Widget cases cover all 194 original instructions and 20 conditional edges.
The earlier independent study rejected 24 actual compiled method faults plus two
class-origin controls. These finite host studies are not Android feature execution.

The original constructor-only ART probe already succeeded with `-Xverify:all` on
the pinned API 35 emulator. It executed the original allocation only. The separate
eight-case actual Widget method wrapper has its own pending device run against
the exact original and isolated Widget APK; it does not render a Widget or cover
nonempty lists, services, scheduling or real device lifecycle behavior.

## Host exception policy and execution budgets

A full Widget UI run exposed one mismatch caused by the default HotSpot fast-throw
optimization omitting the message at a warmed reflection call site. The unchanged
901-file classpath/fixture/APK experiment passed all 20,818 cases when that omission
was disabled. No literal-null message normalization was added. Injected exceptions,
external lookalike messages and explicit null observations remain checked.

The UI positive, deliberate-fault and restoration commands all use and verify
`-XX:-OmitStackTraceInFastThrow` and `-XX:+ShowCodeDetailsInExceptionMessages`.
The report binds the actual Java executable, HotSpot library and effective values.
Six adversarial runtime-policy tests and eight mutation-catalog tests accompany it.
Constructor and AND_INT interpreter extensions retain their separate conformance
fixtures and strict, explicit host-only constructor adapter.

The actual 54-fault upload gate took 1,962.871 seconds on this host. The combined
78-fault suite therefore has a recorded 5,400-second outer budget; every actual UI
execution, including the last clean rerun, is independently limited to 300 seconds.
Other acceptance gates retain their 1,200-second budget. The proposed source CI job
allows 120 minutes and preserves every report, nested mutant artifact and final APK.
Changing a time budget does not change any required outcome or comparison rule.

## Combined proof still required

The new copy verifies all 81,245 baseline input files before/after independent
copying, overlays only the frozen reviewed sources, and extracts a fresh complete
original fixture for exactly 1,242 methods across 605 classes. Both prior isolated
fixtures remain historical. The expected combined inventory is 193,489 cases,
23,174 UI cases across ten methods, 15,326 independent UI expectations, 273 Python
tests and all 78 deliberate UI faults. Full configured acceptance, including the
signed source-edit experiment and final complete positive run, remains pending.

The reference APK, original selected fixture, historical reference Java and host
stubs remain separate from application build inputs. Most application logic is
preserved editable smali. Native libraries and opaque assets remain original binary
dependencies. This work does not recover the publisher's signing identity or claim
whole-application 1:1 behavior.
""")
    save("RECONSTRUCTION_STATUS.md", f"""# Current reconstruction progress

This source copy is the **private combined candidate: 1,242 registered Java method
bodies across 605 classes**, including ten UI-family methods. The full combined
acceptance run is pending. The currently published APK remains the separately
verified 1,240-method candidate until a coherent new source/APK promotion.

The comparison target is the supplied MacroDroid 5.67.8 APK, package
`com.arlosoft.macrodroid`, version code `896700008`. Most application code still
builds from preserved smali; native libraries and opaque assets remain binary
dependencies. Method counts do not measure the percentage of application parity.

## Evidence by exact scope

| Scope | Completed measurement | Remaining requirement |
| --- | --- | --- |
| Published 1,240-method source | Two hosted runs passed all 16 gates, 188,791 three-path cases, 259 Python tests, all 37 UI faults and clean restoration | Those reports retain their original source/APK identity |
| Isolated plugin upload | Signed build, full code/resources, 191,147 three-path cases and all 54 UI faults passed | Actual plugin/network behavior on Android |
| Isolated Widget | Five planned signed/host/integrity gates, 191,133 three-path cases and 265 Python tests passed; prior 24 compiled faults rejected | Separate actual Android method probe and Widget feature behavior |
| Combined source copy | All 81,245 baseline inputs independently copied and verified; fresh 1,242-method original fixture; exact source delta pinned | Full 16-gate combined acceptance and all 78 actual UI faults |
| Original constructor ART probe | Exact original allocation succeeded on the pinned API 35 emulator with verification enabled | This does not execute the Widget method |
| Editor journey | Actual original and candidate captures, installed hashes and lifecycle/crash records retained | Strict full comparison rejected PID changes and one observed intro-frame difference; updated bounded policy has its own device run |

The current source input pin covers {preparation['candidate_inputs']['files']:,} files:

`{pin}`

The combined build is expected to execute 193,489 cases across all 1,242 methods
and three paths, including 23,174 UI cases and 15,326 independent UI expectations.
All 78 deliberate UI faults, 273 Python tests, the signed source-edit experiment
and final positive run remain required. Expected counts are not reported as passes.

## Reproduction

The repository materializer verifies the committed multipart source/toolchain
archives and applies only the active `project/` overlay. Historical
`work-in-progress/` checkpoints are never applied automatically. From a fresh
materialized source tree with Python 3.11+ and JDK 21:

```sh
python3 release_integrity.py verify
python3 acceptance.py
```

`acceptance.py` records each subprocess, budget, exit code and evidence hash. UI
fault execution receives the measured 5,400-second suite budget and individual
300-second execution limits. All other gate budgets remain 1,200 seconds. A failed
gate stops acceptance and retains its evidence. The Android availability probe is
not an Android feature test.

## Limits and next measurements

Both observed APKs encountered the same supplied promotion-listener exception
after notification denial. The saved raw stack reports a Fragment not attached to
Activity in `com.zx.lbua80.onShow`. Matching stack evidence does not make this
crash-free behavior. The new opt-in journey policy preserves raw crash logs and
verifies an installed-identity/process boundary before subsequent observations.
It uses full consecutive byte-identical PNG and XML captures, without cropping,
masking, cross-APK frame selection or pixel tolerance.

The app uses the openly distributed development signing identity, not the
publisher's. Complete high-level Java/Kotlin and native source recovery, the
publisher's signing identity and full application runtime equivalence remain
unestablished. Real macro execution, permissions/services, persistence/reboot,
widgets, integrations, locales/devices/API versions and performance each require
their own observed evidence. See `COMBINED_RECOVERY.md`, `UI_RECOVERY.md` and the
immutable verification checkpoints for method and test details.
""")
    write_json(args.output / "changes.json", {"status": "COMBINED_PREPARATION_SCOPE_DOCUMENTED", "changes": changes,
                                              "application_inputs_changed": False, "combined_acceptance_claimed": False})
    for row in changes:
        path = args.output / row["path"]; path.write_bytes((root / row["path"]).read_bytes())
    print(json.dumps({"status": "COMBINED_PREPARATION_SCOPE_DOCUMENTED", "files": len(changes)}, indent=2))


if __name__ == "__main__":
    main()
