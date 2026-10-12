#!/usr/bin/env python3
"""Prepare a guarded repository README update for the closed Android result."""
from pathlib import Path
from datetime import datetime, timezone
import difflib
import hashlib
import json
import shutil

ROOT = Path('/dev/shm/macrodroid-notification-readiness')
BEFORE = ROOT / 'checkpoints/03-repository-status-update/README.md'
ANALYSIS = ROOT / 'checkpoints/05-thirteen-screen-device-analysis/checkpoint.json'
OUT = ROOT / 'checkpoints/06-completed-readiness-status'


def identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    old = BEFORE.read_bytes()
    assert identity(old) == {'bytes': 17486, 'sha256': '3ae619d100d212572703ec51feae2e23fd70e35a8e301e361141e2cee63cc209'}
    assert identity(ANALYSIS.read_bytes())['sha256'] == '716e3cd70c54659f1b0b84a68a875d61d8c3b1b41e864eb36756938660612439'
    text = old.decode()
    start, end = text.index('## Latest trigger-navigation observations\n'), text.index('## Get the working source\n')
    section = '''## Latest trigger-navigation observations

The completed [thirteen-screen readiness observation](docs/verification/android-day-time-readiness-e1ade015/)
at commit `e1ade015` reached all thirteen screens with both fixed APKs. The
[independent replay](docs/verification/android-day-time-readiness-e1ade015/analysis/)
reproduced the complete recorded verdict and comparison: all thirteen UI
hierarchies and twelve full screenshot pairs are byte-identical, while the second
introduction screen has **26 different pixels**, all inside the observed page
indicator. The exact comparison therefore remains failed. Both runs reach the
same exact-alarm permission explanation after the Day/Time trigger tap; neither
run presses its OK button or confirms a trigger configuration.

Both bounded notification-readiness phases passed their actual raw command and
chronology checks before full-frame capture. Both runs also preserve the known
Fragment exception, replacement process and observed continuation, so a crash-free
run is not established. The replay verified all 3,258 raw artifact files, 252
prepared input roles, 50 accepted snapshot ledgers and 100 frame observations.
All 166 journey, six downloader and ten animation host tests passed in this job.
No pixel region was masked and no mismatch tolerance was applied.

The earlier [twelve-screen trigger-catalog comparison](docs/verification/android-trigger-category-6331410/)
completed both runs at animation scale zero with a five-pixel second-introduction
difference. The earlier [thirteen-screen Day/Time observation](docs/verification/android-day-time-trigger-e610d98/analysis/)
recorded five matching pairs before the original run failed at the
notification-result boundary with an absent main PID; only its candidate reached
all thirteen screens. These historical outcomes remain unchanged.

The [corrected notification-readiness guard](work-in-progress/notification-readiness/01-corrected-host-guard/)
preserves both initial counterexamples and their corrections. Its 21 focused
tests and exact historical replays pass. The
[separate readiness workflow](work-in-progress/notification-readiness-workflow/01-thirteen-screen/)
passed its 55 offline validation commands before the completed Android execution
above. Source acceptance, evidence completeness, process behavior and exact pixel
equality retain their separately recorded results.

'''
    new = (text[:start] + section + text[end:]).encode()
    assert new[:start] == old[:start]
    assert new.decode().split('## Get the working source\n', 1)[1] == text.split('## Get the working source\n', 1)[1]
    OUT.mkdir(parents=True, exist_ok=False)
    (OUT / 'README-before.md').write_bytes(old)
    (OUT / 'README.md').write_bytes(new)
    (OUT / 'README.patch').write_text(''.join(difflib.unified_diff(text.splitlines(True), new.decode().splitlines(True), fromfile='a/README.md', tofile='b/README.md')))
    shutil.copyfile(__file__, OUT / 'update-completed-readiness-status.py')
    files = [{'path': p.name, **identity(p.read_bytes()), 'mode': '100644'} for p in sorted(OUT.iterdir())]
    checkpoint = {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(), 'status': 'CLOSED_READINESS_README_UPDATE_PREPARED', 'repo_target': 'docs/verification/android-day-time-readiness-e1ade015/repository-status-update', 'active_files': [{'path': 'README.md', 'source': 'README.md', 'baseline': identity(old), 'candidate': identity(new), 'mode': '100644'}], 'facts_bound_to': {'analysis_checkpoint_sha256': identity(ANALYSIS.read_bytes())['sha256'], 'run_id': 38230072388, 'artifact_id': 11739145683}, 'files': files, 'file_count': len(files), 'payload_bytes': sum(r['bytes'] for r in files), 'app_source_modified': False, 'android_executed_here': False, 'full_runtime_1_to_1_established': False}
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity((OUT / 'checkpoint.json').read_bytes()), 'files': len(files), 'readme': identity(new)}, indent=2))


if __name__ == '__main__':
    main()
