#!/usr/bin/env python3
"""Freeze the exact dbcad ART/capture replay and its preserved derivation."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil

BASE = Path(__file__).resolve().parent
OUT = BASE / 'checkpoints/01-dbcad-reconstruction-actual'


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    report = json.loads((BASE / 'android-run-38214498395/independent-analysis.json').read_text())
    assert report['status'] == 'ART_VERIFIED_COLD_EXACT_INTRO_DIFFERENCE'
    assert report['all_three_exact_comparator_replays_match'] is True
    assert [r['changed_rgba_pixels'] for r in report['full_unmasked_pairs']] == [0, 35, 0, 0, 0]
    assert report['constructor_probe_independent_verify_result'] is True
    OUT.mkdir(parents=True, exist_ok=False)
    copies = {
        'analysis/freeze_android_38214498395.py': Path(__file__).resolve(),
        'analysis/extract_artifact.py': BASE / 'extract_artifact.py',
        'analysis/prepare_android_replay.py': BASE / 'prepare_android_replay.py',
        'analysis/android-replay-derivation.patch': BASE / 'android-replay-derivation.patch',
        'analysis/android-replay-parent.json': BASE / 'android-replay-parent.json',
        'analysis/replay.stdout.log': BASE / 'android-38214498395.stdout.log',
        'analysis/github-jobs-observed-20261012T070947.json': BASE / 'github-jobs-observed-20261012T070947.json',
    }
    for path in sorted((BASE / 'android-run-38214498395').iterdir()):
        assert path.is_file()
        copies['analysis/' + path.name] = path
    for relative, sha in report['source_verifier_pins'].items():
        source = BASE.parent / 'MacroDroid-Reconstruction' / relative
        assert identity(source)['sha256'] == sha
        copies['analysis/replay-source/' + relative] = source
    for relative, source in copies.items():
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert identity(source) == identity(target)
    (OUT / 'README.md').write_text('''# Measured Android reconstruction result at dbcad968

The constructor allocation probe passed on Android ART, and the complete cold-launch image and hierarchy match exactly. The four-page intro gate failed: the TRIGGERS screen differs at 35 pixels. All other recorded images match. The post-intro gate also remains failed because it retains the unequal intro prerequisite, even though its own notification image and hierarchy are identical.

This evidence belongs to [run 38214498395](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38214498395), exact commit `dbcad968c5c3e8f084205393a6c0d2d06a203c71`. It compares the supplied original APK `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800` with the 94,683,119-byte combined candidate `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`. Actual installed package digests are bound in the recorder evidence and independently rechecked by the exact comparison source.

## Full-frame measurements

All comparisons use the complete 720 × 1280 RGBA image. No crop, mask, tolerance, changed XML attribute or cross-APK frame selection was introduced.

| Recorded surface | Changed RGBA pixels | Hierarchy | Result |
| --- | ---: | --- | --- |
| MACRODROID / cold launch | 0 | Exact | Cold scope passes |
| TRIGGERS | 35 | Exact | Intro scope fails |
| ACTIONS | 0 | Exact | This image pair is exact |
| CONSTRAINTS | 0 | Exact | This image pair is exact |
| First notification-permission surface | 0 | Exact | This image pair is exact; its overall gate retains the failed intro prerequisite |

Every differing TRIGGERS pixel lies within exclusive bounds `[313,1184,352,1200)`, in the previously observed page-indicator area. The [derived analysis](analysis/independent-analysis.json) preserves every actual differing coordinate and both raw RGBA values. This is diagnosis only. The cause is not established by this run, and the measured failure is retained.

The complete pairs are available directly: [cold original](extracted/capture/original.png) and [candidate](extracted/capture/candidate.png); [TRIGGERS original](extracted/capture/original-intro-2.png) and [candidate](extracted/capture/candidate-intro-2.png); [ACTIONS original](extracted/capture/original-intro-3.png) and [candidate](extracted/capture/candidate-intro-3.png); [CONSTRAINTS original](extracted/capture/original-intro-4.png) and [candidate](extracted/capture/candidate-intro-4.png); [notification original](extracted/capture/original-post-intro.png) and [candidate](extracted/capture/candidate-post-intro.png). Every corresponding original XML and command output remains under `extracted/capture/`.

The observed notification surface belongs to `com.google.android.permissioncontroller/com.android.permissioncontroller.permission.ui.GrantPermissionsActivity`. Both show the same MacroDroid notification request. This recorder performs no permission action after that one intro-completion tap. The [cold](extracted/capture/cold-launch-comparison.json), [intro](extracted/capture/intro-comparison.json) and [post-intro](extracted/capture/post-intro-comparison.json) reports remain unchanged, including the latter's failed overall status.

## Independent constructor allocation result

The [actual ART probe report](extracted/constructor-probe/probe-result.json) has status `ART_CONSTRUCTOR_ALLOCATION_VERIFIED`. Its 1,436-byte standalone probe DEX has SHA256 `85f53ad51a1a85fd2161bd485db9f12556f737b0745f6e26ffdff31a927d5281`. The command used `dalvikvm64 -Xverify:all`, the original APK on the classpath, verified device input hashes and read-only file modes. Its bounded command exited 0 and printed exactly `CONSTRUCTOR_ALLOCATION_OK class=zhh arity=2`, with empty stderr. The temporary input directory was removed successfully.

The independently pinned helper's `verify_result` accepted all 24 command records and their 48 output artifacts. No compile-only stubs were on the ART classpath. This separate probe neither installed nor modified an app APK. It proves this narrow constructor allocation on this runtime; it does not establish Widget behavior or general feature parity.

## Runtime and reproducibility

The disposable API 35 device is `emulator-5560`, with Android fingerprint `google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.043/12960925:userdebug/dev-keys`. Its observed ABI list includes `x86_64,arm64-v8a`, and its native bridge is `libndk_translation.so`. Both capture environments contain the same complete display, locale, network and presentation settings. The recorded animation scales are all zero; SystemUI demo clock is 12:00. These are declared still-capture conditions. Animation parity remains untested.

The exact 1,021,235-byte Android artifact has SHA256 `46b33e5b3d22aba73644da191f60c9639fe7d600e003c1f5ce1ee471d31e7372` and artifact ID `11731291550`. All 426 original files are retained under `extracted/`, with the immutable ZIP payload, [manifest](manifest.json) and [extraction receipt](extraction-receipt.json). The separate 1,299-byte host-test artifact has SHA256 `bbf978617fcc7a8e0760813d54fc5d492dc44be4132eca9b0807f5f34ffcdb50`. Its actual log records 33 successful tests in 5.452 seconds, and the replay checks all individual test outcomes against that summary.

The [independent replay](analysis/analyze_android_38214498395.py) verified every archive member, 136 unique recorder artifacts, all 48 constructor output files, all six runtime report hash bindings, the literal original ready-state JSON retained in boot stdout, and all three exact comparison objects. It decoded all five image pairs independently. The source pins, copied exact verifier files, retained derivation from the previous reviewed analyzer, and [actual stdout](analysis/replay.stdout.log) are included. The replay performed no new Android action and changed no raw source, screenshot, hierarchy or report.

The overall runtime status remains `REQUESTED_RUNTIME_SCOPES_INCOMPLETE_OR_DIFFERENT`, with the intro and post-intro prerequisite failures preserved. Full runtime 1:1, animation parity, and feature parity are not established. The editor/session jobs at the same source commit have separate scopes and evidence; their outcomes do not alter this result.
''')
    findings = []
    private = re.compile(rb'^-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----\r?$|^adb\.pubkey=.*$|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}', re.M)
    files = []
    for path in sorted(OUT.rglob('*')):
        if path.is_file():
            assert not path.is_symlink()
            if private.search(path.read_bytes()):
                findings.append(path.relative_to(OUT).as_posix())
            files.append({'path': path.relative_to(OUT).as_posix(), **identity(path)})
    assert findings == []
    checkpoint = {'schema': 1, 'status': 'FROZEN_ACTUAL_ANDROID_REPLAY_ART_PASS_INTRO_FAILURE',
                  'created_utc': datetime.now(timezone.utc).isoformat(),
                  'repo_target': 'docs/verification/android-ci-dbcad968',
                  'run_id': 38214498395, 'head_sha': report['commit'],
                  'active_files': [], 'key_scan_findings': findings, 'files': files}
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
                      'files': len(files), 'bytes_total': sum(row['bytes'] for row in files),
                      'repo_target': checkpoint['repo_target']}, indent=2))


if __name__ == '__main__':
    main()
