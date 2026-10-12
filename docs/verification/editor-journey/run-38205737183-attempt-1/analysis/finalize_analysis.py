#!/usr/bin/env python3
"""Freeze additive, unchanged runtime evidence and its derived offline analysis."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'analysis'


def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    assert not (OUT / 'checkpoint.json').exists()
    for name in ['analyze_preserved_run.py', 'analysis-run.log', 'diagnose_triggers_pixels.py',
                 'triggers-pixel-diagnosis.json', 'triggers-pixel-diagnosis.log',
                 'compare_historical_triggers.py', 'cross-run-analysis.log', 'workflow-job.log',
                 'finalize_analysis.py']:
        shutil.copyfile(ROOT / name, OUT / name)
    proof = json.loads((OUT / 'independent-analysis.json').read_text())
    pixels = json.loads((OUT / 'triggers-pixel-diagnosis.json').read_text())
    historical = json.loads((OUT / 'cross-run-triggers/cross-run-analysis.json').read_text())
    assert proof['exact_pinned_comparator_replay_matches'] is True
    assert proof['actual_comparison']['status'] == 'JOURNEY_DIFFERENCE'
    assert pixels['changed_rgba_pixels'] == 26
    assert historical['older_original_full_png_equals_current_candidate_full_png'] is True
    readme = '''# Ten observed screens: exact replay preserves the TRIGGERS failure

Run [38205737183](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38205737183), source commit `5a95831d897a6fc2b6e59a0ef4088badf63c92da`, completed both ten-screen recordings. The exact pinned comparator reports **`JOURNEY_DIFFERENCE`**. The TRIGGERS page differs in **26 full-frame RGBA pixels**; the other nine full screenshots and all ten complete XML hierarchies match. Both apps also record the known fatal exception and continue in a replacement process. This is neither a crash-free result nor full runtime 1:1 parity.

This directory is additive analysis of the unchanged [raw artifact manifest](../manifest.json), [journey](../journey.json), [actual comparator result](../comparison.json), and [complete ZIP](../evidence.zip). The evidence bot archived them at `95c424943d26ac920ab83e15d2e011808cd34dc3`. The 15,156,144-byte ZIP has SHA256 `f6760a909477b09e91cb9315c67c4c59146bbf454aecc50a72809d101749b2ca`. All **2,302 members**, all **2,106 recursively referenced artifact paths**, and **2,552 references** were independently verified. No original archive member was changed.

## Actual devices, identities and scope

The original installed APK hash is `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`; the candidate installed APK hash is `9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2`. Fresh `pm path` and device `sha256sum` observations bind each initial installation, each post-denial process boundary, and each final OK input. The captured environment before and after both runs is unchanged.

The disposable device is `emulator-5560`, API35, 720×1280, density320, x86_64 with arm64-v8a translation. Its recorded build fingerprint is `google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.043/12960925:userdebug/dev-keys`. [Device configuration](device/capture-device.json) records the stable primary cellular signal/level, SystemUI demo clock `1200`, and all three animation scales set to `0`. These are declared still-capture controls. Animation timing and motion parity were not tested. Battery, actual device wall clock, APKs, app resources and screenshots were not modified by that helper.

The hosted [journey test log](host-tests.log) contains **81 successful host tests in24.423 seconds**; [download tests](download-tests.log) contain **6 successes in0.006 seconds**. The actual Android job then failed its comparison. Host success is not an Android visual pass.

| Captured screen | Changed full-frame RGBA pixels | Complete XML | Result |
|---|---:|---|---|
| Intro: MACRODROID | 0 | Exact | Exact still |
| Intro: TRIGGERS | 26 | Exact | Difference |
| Intro: ACTIONS | 0 | Exact | Exact still |
| Intro: CONSTRAINTS | 0 | Exact | Exact still |
| Notification request | 0 | Exact | Exact still |
| LITEAPKS promotion dialog | 0 | Exact | Exact still |
| Home | 0 | Exact | Exact still |
| Empty editor | 0 | Exact | Exact still |
| Favourite Triggers information dialog | 0 | Exact | Exact still |
| Actual first surface after one OK | 0 | Exact | Exact still |

Both final surfaces are `com.arlosoft.macrodroid/com.arlosoft.macrodroid.editscreen.EditMacroActivity`. Each app executed exactly nine observed taps. The last tap used the unique enabled/clickable `android:id/button1` with text `OK`, after exact `Favourite Triggers` title/message validation and a fresh installed-APK guard. Its observed center was `(560,828)`. No further input followed, and this run does not establish catalog navigation, macro saving, or macro execution. The [independent report](independent-analysis.json) includes the exact selectors, literal message, input commands, foreground components, both sampled PIDs, and guarded timings.

## The 26 pixels survive the declared frame-stability policy

All **38 acquisitions accepted their first two consecutive byte-identical complete PNG/XML observations**. Thus **76 raw frame observations** were retained, with zero rejected intermediate frames in this actual run. Every accepted still and every fresh pre-input still was independently revalidated. All18 inputs also retained immediate fresh PID/component samples and the full15-second acquisition-to-input budget. [All evidence ledgers and review copies](captures/) preserve each frame, full XML, first/final foreground and PID output, command streams, and process-boundary observations.

For TRIGGERS specifically, the capture pair and the before-next-input pair provide **four byte-identical complete PNG/XML frames per APK**. The original observations span **11.553359332 seconds**, and candidate observations span **9.661739439 seconds**. Every original/candidate combination retains the same26 differing coordinates. No temporal pixel change was observed within either APK's four frames.

The difference bounding box is `[313,1184,352,1200)` in the full720×1280 image, around the first two page-indicator dots. Three first-dot pixels are `(314,1184)`, `(317,1186)`, `(313,1199)`; the remaining23 lie on the second-dot edge. The maximum absolute RGBA channel difference is `[28,73,73,0]`. All alpha values at changed coordinates are255. The original and candidate full screenshots remain available directly:

- [Original TRIGGERS](captures/original-intro-2-acquisition-1-frame-2.png), [complete XML](captures/original-intro-2-acquisition-1-frame-2.xml).
- [Candidate TRIGGERS](captures/candidate-intro-2-acquisition-1-frame-2.png), [complete XML](captures/candidate-intro-2-acquisition-1-frame-2.xml).

| Original RGBA | Candidate RGBA | Pixels |
|---|---|---:|
| `[200,109,109,255]` | `[172,36,36,255]` | 3 |
| `[220,163,163,255]` | `[232,194,194,255]` | 2 |
| `[221,165,165,255]` | `[232,195,195,255]` | 4 |
| `[231,191,191,255]` | `[239,212,212,255]` | 3 |
| `[243,222,222,255]` | `[247,233,233,255]` | 6 |
| `[254,251,251,255]` | `[254,253,253,255]` | 8 |

[Pixel diagnosis](triggers-pixel-diagnosis.json) records every changed coordinate/color, every TRIGGERS acquisition and exact observation interval. It does not crop, mask, normalize, choose cross-APK frames, or introduce a tolerance. The full-frame comparison remains failed.

## Cross-run evidence limits a deterministic-source explanation

[The historical analysis](cross-run-triggers/cross-run-analysis.json) verifies six immutable ZIP identities and12 complete TRIGGERS frames, their report-bound hashes, all66 full-frame pair comparisons, full XML, and the recorded environment fields. Each original uses the same original APK hash. Candidate95077 uses the older `be1138a5…` APK; every later candidate uses the exact same `9108b581…` APK as this run.

The full PNG SHA256 groups are:

- **A:** `6e98d2ba0e7d3bd76b15f3e9f6de6ab698f763caa6d89f43672d00a75067a845`
- **B:** `d3dd1a3b8560b47569be67cac2bc98c37ec4f453dd520af6f48224c53d94c65b`
- **C:** `92a14136c68347341c9dd190adef81f5453a91190dc857585b04ce8a65e1e25e`
- **D:** `fd6305f1bd200eb2728d1c7fc76d011dc6b14232b6cc64744f35ed5ddf032458`
- **E:** `cd9bc602e2789878903e92b8edd3a282c9813fd8452ebb09719dc30de20c8676`

| Actual preserved run | Original PNG group | Candidate PNG group | Full TRIGGERS differences in that run |
|---|---|---|---:|
| 38194498356 /95077 four-page capture | B | B | 0 |
| 38200503458 /3a2e6ea reconstruction | A | C | 34 |
| 38202401393 /cada56 reconstruction | A | B | 26 |
| 38202401351 /cada56 nine-screen editor | A | B | 26 |
| 38204928419 /external736da sixteen-screen editor | D | E | 589 |
| 38205737183 /current ten-screen policy | A | B | 26 |

The earlier original PNG is byte-identical to the current candidate PNG, while the unchanged original APK also produced groupA later. The same later candidate APK produced both groupsB andC. The current pair recurs exactly in two earlier archives. These facts rule out assuming that each APK always produces one unique TRIGGERS rendering. They do not identify a rendering/application cause or establish universal nondeterminism. External16 also has status-bar differences; its unchanged589-pixel full result remains in its own evidence.

All environment fields recorded by the current editor recorder match across these six runs after explicitly mapping the older recorder's setting-key names. The mapping is diagnostic metadata only. Different recorder scopes, unrecorded state, renderer state and timing are not treated as a controlled identical experiment. All prior pass/failure labels remain unchanged. Further diagnostic animation runs, if performed, must be separately declared and archived.

## Fatal exception and bounded post-crash continuation

Both raw logs retain a main-thread `java.lang.IllegalStateException: Fragment LB{instance} not attached to Activity` with the same ten stack frames. The literal instance identifiers differ and are retained. The full [lifecycle log](lifecycle.log), raw before/after crash buffers, and [original](captures/original-notification-boundary.json)/[candidate](captures/candidate-notification-boundary.json) boundary records remain unchanged.

| App | Initial PID | Replacement PID | Literal fragment instance | Recorded replacement hosting |
|---|---:|---:|---|---|
| Original | 3934 | 5382 | `LB{693f793}` | top-activity /NewHomeScreenActivity |
| Candidate | 6767 | 7813 | `LB{edd232}` | top-activity /NewHomeScreenActivity |

Each guarded boundary verifies the old PID's absence from both process lists, one new live app PID, the expected resumed home component, a fresh installed-APK SHA, and stable PID/component observations through subsequent captures/inputs. The independently replayed classifier reports the observed new Java fatal block. Its `process_handoff_cause_established` field is not evidence that tapping denial caused the exception or that complete process lifecycles are equivalent. Device/host wall-clock synchronization is not established. No buffers were cleared, no raw fatal block was removed, and no crash-free or benign-crash claim is made.

## Reproduce the unchanged failure

[analyze_preserved_run.py](analyze_preserved_run.py) checks the exact ZIP/manifest and each raw member before importing seven hash-pinned verifier dependencies. It invokes the original comparator without monkeypatching its guards, requires the entire replayed result to equal the archived result, independently decodes all ten pairs with Pillow/NumPy, and checks all raw reference bindings. From a checkout, use fresh temporary output directories:

```sh
python docs/verification/editor-journey/run-38205737183-attempt-1/analysis/analyze_preserved_run.py \
  --archive docs/verification/editor-journey/run-38205737183-attempt-1/evidence.zip \
  --manifest docs/verification/editor-journey/run-38205737183-attempt-1/manifest.json \
  --extracted /tmp/editor-38205737183-raw \
  --output /tmp/editor-38205737183-replay \
  --android-compare docs/verification/editor-journey/run-38205737183-attempt-1/analysis/pinned-source/android_compare.py
```

The [successful replay log](analysis-run.log) records zero exit status in the freeze receipt. The [historical comparison script](compare_historical_triggers.py) accepts `--repo` and a fresh `--output`; its source ZIP pins prevent accidental comparison against updated captures. The original detailed coordinate script/log/report are also preserved exactly. Every additive file is bound by [checkpoint.json](checkpoint.json); complete source/device evidence remains in the unchanged parent ZIP.
'''
    (OUT / 'README.md').write_text(readme)
    # Scan only for actual key/token syntax; preserve all reviewed raw evidence.
    patterns = [re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
                re.compile(rb'\b(?:ghp_|github_pat_)[A-Za-z0-9_]{30,}\b')]
    scanned = 0
    for path in OUT.rglob('*'):
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert not path.is_symlink()
        assert not any(pattern.search(data) for pattern in patterns), str(path)
        scanned += 1
    receipt = {'schema': 1, 'frozen_utc': datetime.now(timezone.utc).isoformat(), 'run_id': 38205737183,
               'analysis_exit_code': 0, 'historical_analysis_exit_code': 0,
               'analysis_guard_replay_exact': True, 'raw_members_unchanged': 2302,
               'raw_review_copy_files': 712, 'actual_private_key_or_token_syntax_scan_files': scanned,
               'actual_private_key_or_token_syntax_matches': 0,
               'new_device_actions': False, 'app_or_active_policy_modified': False,
               'source_archive': {'path': '../evidence.zip', 'bytes': 15156144,
                                  'sha256': 'f6760a909477b09e91cb9315c67c4c59146bbf454aecc50a72809d101749b2ca'}}
    (OUT / 'freeze-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    files = [{'path': str(path.relative_to(OUT)), **meta(path.read_bytes()), 'mode': '100644'}
             for path in sorted(OUT.rglob('*')) if path.is_file()]
    checkpoint = {'schema': 1, 'status': 'FROZEN_FAILED_TEN_SCREEN_RUNTIME_EVIDENCE',
                  'repository_destination': 'docs/verification/editor-journey/run-38205737183-attempt-1/analysis',
                  'active_files': [], 'run_id': 38205737183,
                  'source_commit': '5a95831d897a6fc2b6e59a0ef4088badf63c92da',
                  'archive_commit': '95c424943d26ac920ab83e15d2e011808cd34dc3',
                  'actual_comparison_status': 'JOURNEY_DIFFERENCE',
                  'full_runtime_1_to_1_established': False, 'files': files}
    p = OUT / 'checkpoint.json'
    p.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(p), **meta(p.read_bytes()), 'files': len(files),
                      'total_file_bytes': sum(entry['bytes'] for entry in files),
                      'analysis': meta((OUT / 'independent-analysis.json').read_bytes()),
                      'readme': meta((OUT / 'README.md').read_bytes())}, indent=2))


if __name__ == '__main__':
    main()
