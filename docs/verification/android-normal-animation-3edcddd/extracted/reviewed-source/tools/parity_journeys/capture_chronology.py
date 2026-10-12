"""Bind unique observed captures and raw command evidence to their input order."""
from __future__ import annotations

import json

import editor_journey as runner
import observed_journey as observed


def verify(folder, report, proof):
    """Strengthen existing schema-three evidence without changing image equality.

    Each accepted ledger serves one observation. Every frame/command artifact
    has one acquisition role across the complete two-run report. A result's
    entire stabilization acquisition starts after its triggering input ends.
    """
    events = {runner.artifact_path(folder, item, proof): json.loads(proof.artifact(folder, item))
              for item in report['capture_events']}
    accepted = set()
    used = set()
    used_inodes = set()

    def claim(item):
        path = runner.artifact_path(folder, item, proof)
        metadata = path.stat()
        physical_identity = (metadata.st_dev, metadata.st_ino)
        if path in used or physical_identity in used_inodes:
            raise runner.JourneyError('Observed journey reused an artifact from another acquisition role')
        used.add(path)
        used_inodes.add(physical_identity)

    def command(record):
        for stream in ('stdout', 'stderr'):
            claim(record[stream])

    def capture(shot):
        path = runner.artifact_path(folder, shot['settling'], proof)
        if path not in events:
            raise runner.JourneyError('Accepted observation is missing from the acquisition ledger')
        if path in accepted:
            raise runner.JourneyError('Accepted acquisition ledger reused by another observation')
        accepted.add(path)
        event = events[path]
        if event['status'] != 'CONSECUTIVE_FULL_FRAMES_IDENTICAL':
            raise runner.JourneyError('Accepted observation references a failed acquisition')
        for frame in event['attempts']:
            for item in frame['artifacts'].values():
                claim(item)
        return event['started_monotonic'], event['finished_monotonic']

    for entry in report['capture_events']:
        claim(entry)
    for run in report['runs']:
        for key in ('absence', 'install', 'installed_path', 'installed_checksum', 'launch'):
            command(run[key])
        observed.checked_command(folder, run['launch'],
            ['am', 'start', '-W', '-n', runner.PACKAGE + '/.intro.IntroActivity'], proof)
        first_start, previous_finish = capture(run['screens'][0])
        if run['launch']['finished_monotonic'] > first_start:
            raise runner.JourneyError('Initial full-frame acquisition precedes the completed launch')
        for transition, shot in zip(run['transitions'], run['screens'][1:]):
            before_start, before_finish = capture(transition['before'])
            start = transition['observation_started_monotonic']
            input_start = transition['command']['started_monotonic']
            input_finish = transition['command']['finished_monotonic']
            if (not all(observed.finite(value) for value in (start, input_start, input_finish))
                    or not previous_finish <= start <= before_start <= before_finish <= input_start <= input_finish):
                raise runner.JourneyError('Input acquisition or command is out of chronological order')
            for item in transition['preinput_artifacts'].values():
                claim(item)
            for record in transition['preinput_commands'].values():
                command(record)
            command(transition['command'])
            for key in ('pre_ok_installed_identity', 'pre_denial_diagnostics'):
                for record in transition.get(key, {}).values():
                    command(record)
            result_start, result_finish = capture(shot)
            if input_finish > result_start:
                raise runner.JourneyError('Result acquisition started before its input completed')
            previous_finish = result_finish
            if 'process_handoff' in transition:
                claim(transition['process_handoff'])
                handoff = json.loads(proof.artifact(folder, transition['process_handoff']))
                for record in handoff['commands'].values():
                    command(record)
                for record in handoff['after_diagnostics'].values():
                    command(record)
                if result_finish > handoff['started_monotonic']:
                    raise runner.JourneyError('Notification checks precede the completed result acquisition')
                previous_finish = handoff['finished_monotonic']
    successful = {path for path, event in events.items() if event['status'] == 'CONSECUTIVE_FULL_FRAMES_IDENTICAL'}
    if accepted != successful:
        raise runner.JourneyError('Unbound successful acquisition remains in the capture ledger')
