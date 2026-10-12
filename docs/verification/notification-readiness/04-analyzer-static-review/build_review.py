#!/usr/bin/env python3
"""Preserve a bounded static review; execute no reviewed program or Android action."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path('/dev/shm/readiness-analyzer-review-01')
TARGET = Path('/dev/shm/macrodroid-notification-readiness')
POLICY = TARGET / 'workflow-01-validation/private-inputs/ci-day-time-readiness/reviewed-source/tools/parity_journeys'


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def save(path, value):
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def main():
    output = ROOT / 'capsule'
    output.mkdir()
    started = datetime.now(timezone.utc).isoformat()
    checkpoint = TARGET / 'checkpoints/02-thirteen-screen-readiness-workflow/checkpoint.json'
    assert identity(checkpoint)['sha256'] == '3ca1103f0e247cb827be1d654ce082989658a54cfb8b6b7c4f2c655fd553c50b'
    frozen = json.loads(checkpoint.read_text())
    assert len(frozen['files']) == 13
    frozen_check = []
    for row in frozen['files']:
        actual = identity(checkpoint.parent / row['path'])
        assert actual == {key: row[key] for key in ('bytes', 'sha256')}
        frozen_check.append({'path': row['path'], **actual})
    paths = [TARGET / 'analyze_device_run.py', TARGET / 'workflow-01/prepare_trigger_journey.py',
             TARGET / 'workflow-01/verify_trigger_journey.py',
             TARGET / 'workflow-01/.github/workflows/editor-day-time-readiness.yml', checkpoint,
             *[POLICY / name for name in ('day_time_journey.py', 'notification_readiness.py',
                                         'observed_journey.py', 'capture_chronology.py', 'editor_journey.py')]]
    before = {str(path): identity(path) for path in paths}
    assert before[str(paths[0])]['sha256'] == '84bee2f7254d47bd049d3a273f1f401981a42b6af22670fa47fc3ed20131d2fe'
    for path in paths:
        target = output / 'source' / path.name
        target.parent.mkdir(exist_ok=True)
        shutil.copyfile(path, target)
        assert identity(target) == before[str(path)]
    report = {
        'schema': 1,
        'status': 'STATIC_REVIEW_COMPLETE_NO_CONFIRMED_ACTUAL_ARTIFACT_BLOCKER',
        'scope': 'Static source compatibility only; no actual failed-run artifact was opened or downloaded',
        'requested_run_id': 38230072388,
        'started_utc': started,
        'analyzer_sha256': before[str(paths[0])]['sha256'],
        'workflow_capsule_sha256': identity(checkpoint)['sha256'],
        'reviewed_source_files': before,
        'frozen_workflow_payloads_checked': frozen_check,
        'compatible_boundaries': [
            {'analyzer_lines': [120, 124], 'finding': 'The workflow and both helper hashes match all three exact frozen capsule payloads.'},
            {'analyzer_lines': [155, 184], 'finding': 'Executed-input paths are reconstructed at the root; the complete independently expected 252 source/copy roles are checked before copied project code is used.'},
            {'analyzer_lines': [163, 189], 'finding': 'The sole verifier-written day-time-readiness-verification.json is copied privately. Its literal result is compared with raw evidence, excluding only the new verification timestamp.'},
            {'analyzer_lines': [201, 205], 'finding': 'Policy and full comparison run within the exact thirteen-screen configured_plan context. Standalone raw verify_phase does not require configured_plan.'},
            {'analyzer_lines': [338, 376], 'finding': 'Independent analysis success is separate from literal evidence_valid, journey_equal and the failed runtime statuses; no crash-free or full-parity claim is set.'},
            {'analyzer_lines': [266, 296], 'finding': 'Available original/candidate full RGBA frames are compared without tolerance; partial pairs are explicitly diagnostic-only and terminal raw captures remain available.'},
        ],
        'conditional_failed_run_edge': {
            'status': 'STATICALLY_IDENTIFIED_NOT_CONFIRMED_IN_ACTUAL_RUN',
            'condition': 'A legitimate failed run has no accepted screen, and capture_events reaches capture_chronology.verify without an earlier JourneyError.',
            'analyzer_location': 'analyze_device_run.py:248-252',
            'producer_locations': ['editor_journey.py:521-572', 'capture_chronology.py:53-58'],
            'finding': 'The analyzer catches only JourneyError for the completion-only capture-event gate. The chronology checker directly indexes run["screens"][0], so a zero-screen failed run raises IndexError into the outer rejection handler instead of becoming a recorded failed diagnostic gate.',
            'impact': 'This can terminate independent partial-run analysis; it does not create an application-parity false pass.',
            'smallest_followup_if_actual_artifact_hits_condition': 'Record the non-completion exception class/message in the diagnostic event-gate receipt for failed runs, preserving the literal failed comparator and all raw inputs. Do not relax the comparator or claim chronology passed.',
            'actual_screen_counts_inspected': False,
        },
        'reviewed_programs_executed': False,
        'test_suites_run': False,
        'android_actions': [],
        'artifact_downloads': 0,
        'reviewed_files_changed': False,
    }
    after = {str(path): identity(path) for path in paths}
    assert after == before
    report['source_hashes_unchanged_after_review'] = True
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    save(output / 'review.json', report)
    shutil.copyfile(Path(__file__), output / 'build_review.py')
    files = [{'path': path.relative_to(output).as_posix(), **identity(path)}
             for path in sorted(output.rglob('*')) if path.is_file()]
    assert sum(row['bytes'] for row in files) < 16 * 1024 * 1024
    save(output / 'checkpoint.json', {'schema': 1, 'status': 'FROZEN_STATIC_REVIEW',
                                     'files': files, 'file_count': len(files),
                                     'publication_path': 'docs/verification/notification-readiness/device-analyzer-static-review-01',
                                     'active_files': [], 'android_executed': False})
    print(json.dumps({'path': str(output / 'checkpoint.json'), **identity(output / 'checkpoint.json'),
                      'file_count': len(files), 'payload_bytes': sum(row['bytes'] for row in files)}, indent=2))


if __name__ == '__main__':
    main()
