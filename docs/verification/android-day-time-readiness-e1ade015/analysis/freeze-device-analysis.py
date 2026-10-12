#!/usr/bin/env python3
"""Freeze the closed literal thirteen-screen replay and exact raw evidence links."""
import hashlib
import json
import os
import shutil
import stat
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('/dev/shm/macrodroid-notification-readiness')
ANALYSIS = BASE / 'device-run-38230072388-analysis-01'
RAW_ROOT = Path('/dev/shm/macrodroid-transfer-space-20261012/readiness-run-38230072388')
OUT = BASE / 'checkpoints/05-thirteen-screen-device-analysis'
REMOTE = 'docs/verification/android-day-time-readiness-e1ade015'


def identity(path):
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    after = path.lstat()
    assert (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    return {'bytes': after.st_size, 'sha256': digest}


def write(path, value):
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def main():
    result = json.loads((ANALYSIS / 'independent-readiness-analysis.json').read_bytes())
    assert result['status'] == 'EXACT_READINESS_DEVICE_ARTIFACT_REPLAYED' and result['analysis_passed'] is True
    assert result['raw_archive_and_all_files_unchanged'] is True and result['fixed_apks_unchanged'] is True
    assert result['journey_equal'] is False and result['literal_evidence_valid'] is True
    assert result['head_sha'] == 'e1ade015f938339479216a1a91518e556902fce8'
    assert result['run_id'] == 38230072388 and result['artifact_id'] == 11739145683
    assert result['diagnostic_rgba_pixel_vector'] == [0, 26] + [0] * 11
    assert result['full_runtime_1_to_1_established'] is False and result['crash_free_run_established'] is False
    before = json.loads((ANALYSIS / 'raw-file-identities-before.json').read_bytes())
    assert before == json.loads((ANALYSIS / 'raw-file-identities-after.json').read_bytes()) and len(before) == 3258
    raw = RAW_ROOT / 'extracted'
    assert {p.relative_to(raw).as_posix() for p in raw.rglob('*') if p.is_file()} == set(before)
    for name, expected in before.items():
        assert identity(raw / name) == expected, name
    archive = RAW_ROOT / 'readiness-run-38230072388.zip'
    assert identity(archive) == result['raw_archive']
    assert identity(ANALYSIS / 'executed-replay-script.py')['sha256'] == '84bee2f7254d47bd049d3a273f1f401981a42b6af22670fa47fc3ed20131d2fe'
    pairs = json.loads((ANALYSIS / 'all-available-full-frame-pairs-diagnostic-only.json').read_bytes())
    assert len(pairs) == 13 and all(x['xml_bytes_equal'] for x in pairs)
    assert all(x['png_bytes_equal'] for i, x in enumerate(pairs) if i != 1)
    assert pairs[1]['bounds_exclusive'] == [313, 1184, 352, 1200]
    assert sum(x['changed_rgba_pixels'] for x in pairs) == 26
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(__file__, OUT / 'freeze-device-analysis.py')
    preserved = []
    for path in sorted(ANALYSIS.rglob('*')):
        assert not path.is_symlink()
        if not path.is_file():
            continue
        name = path.relative_to(ANALYSIS).as_posix()
        target = OUT / 'analysis' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.stat().st_dev == OUT.stat().st_dev:
            os.link(path, target)
        else:
            shutil.copy2(path, target)
        assert identity(target) == identity(path)
        preserved.append(name)
    assert len(preserved) == 175
    external = {
        'schema': 1,
        'run_url': 'https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38230072388',
        'head_sha': result['head_sha'],
        'artifact_id': result['artifact_id'],
        'zip': {'repository_path': REMOTE + '/readiness-run-38230072388.zip', **identity(archive)},
        'raw': {'repository_path': REMOTE + '/extracted', 'files': len(before), 'payload_bytes': sum(x['bytes'] for x in before.values()), 'inventory_path': 'analysis/raw-file-identities-before.json', 'inventory_identity': identity(ANALYSIS / 'raw-file-identities-before.json')},
        'extraction_receipt': {'repository_path': REMOTE + '/extracted-extraction.json', **identity(RAW_ROOT / 'extracted-extraction.json')},
        'workflow_checkpoint': {'repository_path': 'work-in-progress/notification-readiness-workflow/01-thirteen-screen/checkpoint.json', 'sha256': '3ca1103f0e247cb827be1d654ce082989658a54cfb8b6b7c4f2c655fd553c50b'},
        'raw_reverified_at_freeze': True,
        'analysis_file_count': len(preserved),
        'publication_state': 'Publisher must publish and fetch-verify the external raw roles; this file does not claim they are already remote',
    }
    write(OUT / 'external-evidence.json', external)
    readme = '''# Day/Time trigger: completed thirteen-screen readiness observation

Run **38230072388**, artifact **11739145683**, executed the exact workflow at `e1ade015f938339479216a1a91518e556902fce8`. Both APKs completed **13 screens and 12 inputs**. The literal outcome is **DAY_TIME_READINESS_THIRTEEN_SCREEN_DIFFERENCE**, with valid evidence and `journey_equal: false`.

The independent replay reproduced the complete recorded comparison object and complete workflow verdict, excluding only the replay's new verification timestamp. It re-established all 252 prepared input roles, verified all 3,258 raw files against the single artifact ZIP, and found all raw bytes and both compared APKs unchanged afterwards. The replay executed no Android input. Its own successful completion verifies the recorded difference; it does not convert the device result into parity.

## Full-frame outcome

The changed-pixel vector is `[0, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`. Every pair is 720 by 1280 pixels and all 13 hierarchy XML files are byte-identical between APKs. The twelve other screen PNGs are also byte-identical. The 26 different RGBA pixels occur on `intro-2`, inside exclusive bounds `[313, 1184, 352, 1200]`, at the page indicator. The diagnostic includes every changed coordinate and both raw colors; no region was masked and no tolerance was applied. The cause of this variation remains unproved.

The replay independently checked 50 accepted snapshot ledgers, 50 capture ledgers, 100 recorded frame observations, 2,744 uniquely referenced journey artifacts and all 1,021 recorded commands. All 166 journey, 10 animation and 6 downloader host tests have individually successful raw log entries. The nineteen zero-scale configuration commands and owned runtime cleanup also verify.

## Readiness and process outcome

Both bounded readiness phases contain four consecutive `HOME_WITH_SAME_PID` observations and accept the first eligible sequence `[0, 3]`. The original records PID `4049` before the notification boundary and ready PID `5474`; the candidate records `7262` and `8331`. Their complete phase durations are approximately 1.102 and 1.221 seconds. Actual raw command endpoints, global order, exclusive stream roles and subsequent full-frame binding were checked. Readiness observations receive no frame or process-continuity credit.

Both runs record the known `java.lang.IllegalStateException` with the Fragment LB not-attached message and then continue in the replacement process. The exact crash signatures and handoff observations remain in the literal comparison. This is not a crash-free run, and the notification action is not established as the cause of that exception.

## Observed terminal and next bounded step

Both terminal observations show the exact same **Permission Required** dialog explaining exact-alarm access, over `AddTriggerActivity`. The full PNG is 97,172 bytes, SHA-256 `3d7c58b3e7c1c8e84964ab504ab69c00b970ee6e493904ec5d03b9b41d26a7c7`; the XML is 6,678 bytes, SHA-256 `d9e3f0fcb4139e4cfbaa6fe4b856159157136e82775cad4c45746abeef10d076`. The root viewed the full original terminal PNG, and both terminal bytes are preserved.

The observed `android:id/button1` control says **OK**, is enabled and clickable, and has bounds `[496,761][624,857]`, with center `(560,809)`. A future explicitly defined journey may validate that whole dialog, tap this one control, and record the resulting surface. This run contains no such tap, no exact-alarm permission grant, no confirmed trigger configuration, and no saved or executed macro. Full runtime 1:1 remains false.

## Preservation

`analysis/` preserves all 175 files produced by the exact executed replay, including complete comparison objects, all full paired screen images, raw reference inventories, terminal XML nodes, source-module identities and the literal result. `external-evidence.json` binds the complete original ZIP and raw extraction retained by the publisher. Only the existing ephemeral public ADB value is omitted in a clearly marked review copy of the boot log; the raw artifact bytes are unchanged. Historical twelve-screen and earlier thirteen-screen failures retain their original outcomes.
'''
    (OUT / 'README.md').write_text(readme)
    rows = []
    for path in sorted(OUT.rglob('*')):
        if path.is_file():
            rows.append({'path': path.relative_to(OUT).as_posix(), **identity(path), 'mode': '100755' if path.stat().st_mode & 0o111 else '100644'})
    checkpoint = {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(), 'status': 'EXACT_COMPLETED_THIRTEEN_SCREEN_DIFFERENCE_REPLAYED', 'repo_target': REMOTE + '/analysis', 'active_files': [], 'android_executed_by_analysis': False, 'device_evidence_valid': True, 'journey_equal': False, 'full_runtime_1_to_1_established': False, 'files': rows, 'file_count': len(rows), 'payload_bytes': sum(r['bytes'] for r in rows), 'raw_zip_identity': identity(archive), 'run_id': result['run_id'], 'artifact_id': result['artifact_id'], 'head_sha': result['head_sha']}
    write(OUT / 'checkpoint.json', checkpoint)
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'), 'files': len(rows), 'payload_bytes': checkpoint['payload_bytes']}, indent=2))


if __name__ == '__main__':
    main()
