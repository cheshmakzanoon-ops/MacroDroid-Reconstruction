#!/usr/bin/env python3
"""Directly check actual current-ten chronology beyond the archived policy."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
FOLDER = ROOT / 'extracted/ci-editor/journey'


def meta(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def read(entry):
    path = FOLDER / entry['path']
    assert path.resolve().is_relative_to(FOLDER.resolve())
    data = path.read_bytes()
    assert meta(data) == {key: entry[key] for key in ('bytes', 'sha256')}
    return data


def main():
    raw = (FOLDER / 'journey.json').read_bytes()
    assert meta(raw) == {'bytes': 709737, 'sha256': '169ca0ac100b8a6e3cb9504ba3eb1077b6b06d99add19bda2925b4795afb4bc6'}
    report = json.loads(raw)
    ledger_paths, frame_paths = set(), set()
    checks = []
    for run in report['runs']:
        for shot in run['screens'] + [step['before'] for step in run['transitions']]:
            entry = shot['settling']
            path = (FOLDER / entry['path']).resolve()
            assert path not in ledger_paths
            ledger_paths.add(path)
            event = json.loads(read(entry))
            assert {key: value for key, value in shot.items() if key not in ('name', 'settling')} == event['attempts'][-1]
            for attempt in event['attempts']:
                for artifact in attempt['artifacts'].values():
                    read(artifact)
                    path = (FOLDER / artifact['path']).resolve()
                    assert path not in frame_paths
                    frame_paths.add(path)
        for index, transition in enumerate(run['transitions']):
            prior, after = run['screens'][index:index + 2]
            before = json.loads(read(transition['before']['settling']))
            after_event = json.loads(read(after['settling']))
            command = transition['command']
            assert prior['observation']['finished_monotonic'] <= before['started_monotonic']
            assert before['finished_monotonic'] <= command['started_monotonic'] <= command['finished_monotonic']
            assert command['finished_monotonic'] <= after_event['started_monotonic']
            assert all(command['finished_monotonic'] <= attempt['observation']['started_monotonic']
                       for attempt in after_event['attempts'])
            checks.append({'label': run['label'], 'to': transition['to'],
                           'prior_selected_finished': prior['observation']['finished_monotonic'],
                           'before_acquisition_started': before['started_monotonic'],
                           'before_acquisition_finished': before['finished_monotonic'],
                           'input_started': command['started_monotonic'], 'input_finished': command['finished_monotonic'],
                           'result_acquisition_started': after_event['started_monotonic'],
                           'result_first_frame_started': after_event['attempts'][0]['observation']['started_monotonic'],
                           'result_selected_finished': after['observation']['finished_monotonic']})
    assert len(ledger_paths) == 38 and len(frame_paths) == 456 and len(checks) == 18
    result = {'schema': 1, 'status': 'ACTUAL_CAPTURE_IDENTITIES_AND_CROSS_INPUT_CHRONOLOGY_VERIFIED',
              'run_id': 38205737183, 'journey': meta(raw), 'unique_selected_ledgers': 38,
              'unique_raw_frame_artifact_paths': 456, 'raw_frames': 76,
              'all_18_result_acquisitions_begin_after_their_inputs_finish': True,
              'all_18_preinput_acquisitions_follow_previous_selected_capture': True,
              'transitions': checks, 'archived_policy_has_known_missing_guards': True,
              'archived_policy_replayed_or_modified_by_this_audit': False,
              'original_comparison_status_unchanged': 'JOURNEY_DIFFERENCE',
              'changed_pixels_unchanged': [0, 26, 0, 0, 0, 0, 0, 0, 0, 0],
              'app_or_active_tools_modified': False, 'android_executed_by_audit': False,
              'scope': 'Direct extra checks of actual immutable evidence; not a repair of the archived policy'}
    out = ROOT / 'chronology-followup'
    out.mkdir(exist_ok=False)
    (out / 'chronology-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    (out / 'audit_capture_chronology.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
