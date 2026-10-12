#!/usr/bin/env python3
"""Prepare a guarded README update for the already preserved device outcomes."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import shutil


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repository, output = args.repository.resolve(), args.output.resolve()
    source = repository / 'README.md'
    before_id = identity(source)
    before = source.read_text()
    anchor = '## Get the working source\n'
    if before.count(anchor) != 1 or '## Latest trigger-navigation observations' in before:
        raise ValueError('The expected README boundary changed')
    addition = '''## Latest trigger-navigation observations

The [twelve-screen trigger-catalog comparison](docs/verification/android-trigger-category-6331410/)
completed both runs with the exact active APK and reference APK at animation
scale zero. All UI hierarchy pairs and eleven complete screenshot pairs match;
the second introduction screen retains a five-pixel difference. That run remains
a failed exact comparison.

The [thirteen-screen Day/Time observation](docs/verification/android-day-time-trigger-e610d98/analysis/)
then recorded five matching paired screens before the original run failed at the
notification-result boundary with an absent main PID. The candidate completed
all thirteen screens and reached an exact-alarm permission explanation. That
candidate-only terminal observation does not establish a paired match or a
configured trigger.

The [corrected notification-readiness guard](work-in-progress/notification-readiness/01-corrected-host-guard/)
preserves both initial counterexamples and their corrections. Its 21 focused
tests pass, and its exact historical replays preserve both device outcomes above.
The [separate thirteen-screen readiness workflow](work-in-progress/notification-readiness-workflow/01-thirteen-screen/)
also passed all 166 packaged journey tests, six downloader tests, ten animation
tests, and 55 actual offline commands with their required outcomes. It adds a
bounded read-only process/foreground phase before the existing full-frame
capture. Its fresh Android result must be assessed separately; no historical
difference, crash, or incomplete run is converted into a pass.

'''
    after = before.replace(anchor, addition + anchor, 1)
    output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(source, output / 'README-before.md')
    (output / 'README.md').write_text(after)
    shutil.copyfile(Path(__file__), output / Path(__file__).name)
    (output / 'README.patch').write_text(''.join(difflib.unified_diff(
        before.splitlines(True), after.splitlines(True), fromfile='a/README.md', tofile='b/README.md')))
    if identity(source) != before_id:
        raise ValueError('README changed during guarded preparation')
    files = [{'path': path.name, **identity(path)} for path in sorted(output.iterdir()) if path.is_file()]
    manifest = {'status': 'DOCUMENTATION_UPDATE_PREPARED', 'created_utc': datetime.now(timezone.utc).isoformat(),
                'active_changes': False, 'android_executed_here': False,
                'target': 'README.md', 'expected_before': before_id, 'expected_after': identity(output / 'README.md'),
                'facts_bound_to': {
                    'zero_scale_twelve_checkpoint_sha256': 'e918ea97a3f2c217997559430182195d022b1211a31d68aea04b90e1574d3676',
                    'day_time_thirteen_checkpoint_sha256': '7b3fd99fed8b5871446ab443c4f373e04b5d882d12ffdda09d1d229a48532787',
                    'corrected_guard_checkpoint_sha256': 'b9d069a653b3ecc483f8e6579ccfb13e5a70450c00015f9a3a31c5277c9a84b3',
                    'workflow_checkpoint_sha256': '3ca1103f0e247cb827be1d654ce082989658a54cfb8b6b7c4f2c655fd553c50b'},
                'files': files}
    path = output / 'checkpoint.json'
    path.write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(path), **identity(path), 'expected_before': before_id,
                      'expected_after': identity(output / 'README.md')}, indent=2))


if __name__ == '__main__':
    main()
