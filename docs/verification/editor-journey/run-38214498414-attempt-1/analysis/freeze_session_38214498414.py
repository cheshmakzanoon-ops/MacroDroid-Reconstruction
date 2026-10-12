#!/usr/bin/env python3
"""Preserve the verified editor scope and its raw, still-failed startup context."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil

BASE = Path(__file__).resolve().parent
RESULT = BASE / 'session-run-38214498414-analysis-03'
RAW = BASE / 'session-run-38214498414-extracted'
OUT = BASE / 'checkpoints/02-dbcad-session-actual'


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    report = json.loads((RESULT / 'independent-session-analysis.json').read_text())
    assert report['status'] == 'INDEPENDENT_SCHEMA4_POST_ONBOARDING_MATCH_STARTUP_REMAINS_REJECTED'
    assert report['scoped_session_result']['editor_session_equal'] is True
    assert report['continuous_startup_result']['status'] == 'REJECTED'
    assert len(report['startup_java_crashes']) == 2
    assert [row['changed_rgba_pixels'] for row in report['complete_unmasked_image_pairs']] == [0,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    OUT.mkdir(parents=True, exist_ok=False)
    copies = {p.relative_to(RESULT).as_posix(): p for p in RESULT.rglob('*') if p.is_file()}
    copies.update({
        'freeze_session_38214498414.py': Path(__file__).resolve(),
        'extract_artifact.py': BASE / 'extract_artifact.py',
        'extraction-receipt.json': BASE / 'session-run-38214498414-extracted-extraction.json',
        'replay.stdout.log': BASE / 'session-38214498414-replay-03.stdout.log',
        'github-jobs-observed-20261012T070947.json': BASE / 'github-jobs-observed-20261012T070947.json',
    })
    for label in ('session-source-binding-failure-01', 'session-configuration-label-failure-02'):
        for path in (BASE / label).rglob('*'):
            if path.is_file():
                copies['preserved-analysis-attempts/' + label + '/' + path.relative_to(BASE / label).as_posix()] = path
    for path in (RAW / 'ci-editor/device').iterdir():
        assert path.is_file()
        copies['raw-device/' + path.name] = path
    for name in ('runtime-status.json', 'runtime-properties.json'):
        copies['raw-device/' + name] = RAW / 'ci-editor/environment' / name
    copies['service.log'] = RAW / 'ci-editor/service.log'
    for relative, source in copies.items():
        assert not source.is_symlink()
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert identity(source) == identity(target)
    table = []
    for row in report['complete_unmasked_image_pairs']:
        left = row['original']['screenshot']['path']
        right = row['candidate']['screenshot']['path']
        table.append('| ' + row['name'] + ' | ' + str(row['changed_rgba_pixels']) +
                     ' | Exact | [original](review-captures/' + left + ') / [candidate](review-captures/' + right + ') |')
    (OUT / 'README.md').write_text('''# Independent schema 4 editor-session result at dbcad968

The ten-screen **post-onboarding editor scope passes** the exact activated schema 4 verifier. Its complete PNG pixels, XML state, dimensions, color metadata, and paired foreground activities match from the observed home screen through the final editor return. This is a narrow continuation result. **Continuous startup remains rejected**, and the raw logs preserve a Java crash and process restart for each APK before that boundary. The independently measured TRIGGERS intro image also differs at ten pixels.

This analysis belongs to [run 38214498414](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38214498414), exact source commit `dbcad968c5c3e8f084205393a6c0d2d06a203c71`. It compares original APK `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800` and combined candidate `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182` under the actual declared sixteen-step plan.

## Complete recorded stills

The table is a diagnosis of every actual recorded image pair. Each comparison uses all 720 × 1280 RGBA pixels. No crop, mask, tolerance or cross-APK frame selection is used. Every one of the sixteen hierarchy files also matches byte-for-byte. The ten rows starting at `home` are the independently verified session scope; earlier rows do not gain a startup acceptance claim from their image measurements.

| Actual surface | Changed RGBA pixels | XML | Complete PNGs |
| --- | ---: | --- | --- |
''' + '\n'.join(table) + '''

The ten scoped PNG files are themselves byte-identical between variants. The sole nonzero diagnostic image is `intro-2`, with exclusive difference bounds `[317,1186,338,1197)`. This separate run's ten-pixel measurement does not replace the 35-pixel result in reconstruction run 38214498395 or any earlier preserved failure.

All 32 complete PNGs, 32 hierarchies, and their actual foreground/PID samples are available in [review-captures](review-captures/). Their exact original member names and SHA256 identities remain in the [derived analysis](independent-session-analysis.json) and [complete member inventory](all-2096-member-identities.json). The immutable [original ZIP](../evidence.zip) retains every capture, pre-input sample, command stream, rejected XML-acquisition attempt, report and source artifact from the job.

## What the successful scoped replay checks

The literal schema 4 comparison and the standalone recorded replay both reproduce exactly. The result is `EXACT_POST_ONBOARDING_EDITOR_MATCH_ONLY`, with 294 distinct semantic observation files and zero reuse. The retained path/inode ledger is accompanied by explicit capture/input/endpoint ordering, bounded pre-input freshness, APK identity checks at both home and final editor boundaries, stable in-scope PIDs, and matching normalized foreground component identities for each original/candidate screen. The final observed component is exactly `com.arlosoft.macrodroid.editscreen.EditMacroActivity`.

The home component is `com.arlosoft.macrodroid.homescreen.NewHomeScreenActivity`. Trigger, action and constraint catalogs respectively use `com.arlosoft.macrodroid.selectableitemlist.AddTriggerActivity`, `AddActionActivity` and `AddConstraintActivity`; each return and the Favourite Triggers information dialog are in `EditMacroActivity`. Both variants show the same recorded components. The precise package-qualified identities are retained in the result.

The verifier source `post_onboarding.py` has SHA256 `6e155f43a2a7f7cdd2364911191f2b88b0085db915da2adefb8b2f918a1dbd80`. The analysis checked 43 exact Git-authored source/workflow bindings before importing the small copied source tree. It preserved the external session ledger unchanged. Eighteen generated CI bytecode files remain untouched archive evidence and were not executed. The local extraction creates fresh filesystem inodes; the replay independently checks distinct local artifact identities and exactly reproduces the hosted ledger result, rather than claiming the original remote inode numbers were preserved by ZIP extraction.

The complete journey JSON has SHA256 `9b3bf79cb55b0c10f6d40485e9e8f8a5964b2c20fba5e4d4bab99079a272d391`. All 1,816 unique artifact references reachable through that report were verified. Both complete literal outcomes are retained: [scoped session replay](literal-session-replay.json) and [continuous startup rejection](literal-continuous-startup-replay.json). No original report was overwritten.

## Startup crash and restart remain explicit failures

The continuous comparison rejects with `App PID changed or lacks two live samples`, and the recorded startup exit code is 2. The original starts under PID 4078 and resumes the observed home under PID 4997; the candidate changes from PID 6551 to PID 7207. Both raw logs show `java.lang.IllegalStateException` in the app-owned `Fragment LB`, reporting that it is not attached to an Activity, with `android.app.Fragment.getResources` followed by `com.zx.lbua80.onShow` in the stack. Their actual fragment object identifiers and all raw stack text remain intact.

Read the [original crash](original-actual-java-crash.txt), [candidate crash](candidate-actual-java-crash.txt), [original process events](original-actual-process-events.txt), [candidate process events](candidate-actual-process-events.txt), and [complete lifecycle log](lifecycle.log). The observed crash times are 06:54:38.387 UTC and 06:56:51.791 UTC on 2026-10-12. These are crashes, not a benign handoff or a crash-free pass. The ten-screen scope begins at the fresh observed home boundary after the restart, and all in-scope captures and guarded inputs retain their respective home PID.

## Device configuration, evidence integrity, and limits

The separate session device configuration succeeds as `CAPTURE_DEVICE_CONFIGURED`. Its recorded primary radio is WCDMA at computed level 4 after 15.12 seconds of stability. All 40 command records and 80 raw output hashes are checked. Its complete original report/streams and environment properties are retained under [raw-device](raw-device/). Both capture environments declare API 35, the same 720 × 1280 display at density 320, animation scales zero, and SystemUI clock demo mode at 12:00. These are still-capture conditions; animation timing and motion are untested.

The immutable artifact is 11,628,251 bytes, SHA256 `b671aa04ef05ed5bf064bd16dd92b7046819da69578ec362b7d3ea86bfb17ff5`, artifact ID `11731381967`. Every one of its 2,096 members was checked against the GitHub-bound manifest, ZIP bytes and local extracted bytes before and after analysis. The full archive remains at the existing published path; it was not downloaded again or rewritten. The actual host logs record 148 verifier controls in 31.689 seconds and six downloader controls in 0.101 seconds; these existing outcomes were checked without rerunning those suites.

The [analysis source](analyze_session_38214498414.py), exact [source pins](source-commit-pins.json), complete inventories, [actual successful log](replay.stdout.log), extractor, and freezer are preserved. Two earlier analysis attempts are retained in [preserved-analysis-attempts](preserved-analysis-attempts/): one rejected generated bytecode as an absent Git source path before import; the next completed both literal replays but used the wrong expected device-success label in a reporting assertion. The final correction uses the existing `CAPTURE_DEVICE_CONFIGURED` label and changes no runtime guard, screenshot or raw report. Their sources, tracebacks, literal intermediate replay outputs and inventories remain available.

No macro was saved or executed. Trigger/action/constraint behavior beyond the observed catalog navigation, notification/startup correctness, animation parity, crash-free operation and full runtime 1:1 are not established. This independent replay executed no new Android command and changed no active app, workflow, capture policy or raw evidence.
''')
    private = re.compile(rb'^-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----\r?$|^adb\.pubkey=.*$|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}', re.M)
    files, findings = [], []
    for path in sorted(OUT.rglob('*')):
        if path.is_file():
            assert not path.is_symlink()
            if private.search(path.read_bytes()):
                findings.append(path.relative_to(OUT).as_posix())
            files.append({'path': path.relative_to(OUT).as_posix(), **identity(path)})
    assert findings == []
    checkpoint = {'schema': 1, 'status': 'FROZEN_ACTUAL_SCHEMA4_SESSION_MATCH_STARTUP_REJECTED',
                  'created_utc': datetime.now(timezone.utc).isoformat(),
                  'repo_target': 'docs/verification/editor-journey/run-38214498414-attempt-1/analysis',
                  'run_id': 38214498414, 'head_sha': report['head_sha'],
                  'active_files': [], 'key_scan_findings': findings, 'files': files}
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
                      'files': len(files), 'bytes_total': sum(row['bytes'] for row in files),
                      'repo_target': checkpoint['repo_target']}, indent=2))


if __name__ == '__main__':
    main()
