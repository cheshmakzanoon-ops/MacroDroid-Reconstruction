"""Bounded, read-only lifecycle observations before notification result capture.

These observations are not screenshots or continuity evidence. The existing
full-frame and recorded-crash handoff checks remain independently required.
"""
from __future__ import annotations

import copy
import json
import re
import shlex
import time

import editor_journey as runner
import observed_journey as observed

REPORT_SCHEMA = 5
PLAN_SHA256 = '42ece5a06a280186ddf9796a4524975d478263e545260674e2b1b4cf718d46fb'
REFERENCE_KEY = 'pre_capture_readiness'
POLICY_KEY = 'notification_readiness_policy'
POLICY = {
    'schema': 1,
    'plan_sha256': PLAN_SHA256,
    'after': 'notification-request',
    'before': 'reference-promotion',
    'action': runner.DENY,
    'max_observations': 16,
    'max_seconds': 10,
    'post_input_wait_seconds': 2,
    'observation_gap_seconds': 0.25,
    'minimum_ready_observations': 2,
    'minimum_ready_span_seconds': 1.05,
    'ready_component': observed.HOME,
    'other_allowed_component': observed.PERMISSION_ACTIVITY,
    'commands': [['pidof', runner.PACKAGE], ['dumpsys', 'activity', 'activities'], ['pidof', runner.PACKAGE]],
    'first_eligible_contiguous_sequence': True,
    'frames_or_continuity_credit': False,
    'app_restart_performed': False,
}
EPSILON = 0.001
COMMAND_FIELDS = {'argv', 'returncode', 'timed_out', 'started_utc', 'started_monotonic',
                  'finished_monotonic', 'timeout_seconds', 'stdout', 'stderr'}


def require_plan():
    import day_time_journey
    day_time_journey.require_plan()
    if runner.fingerprint(runner.PLAN) != PLAN_SHA256:
        raise runner.JourneyError('Notification readiness requires the exact thirteen-screen plan')


def contains_evidence(value):
    if isinstance(value, dict):
        return (REFERENCE_KEY in value or POLICY_KEY in value
                or any(contains_evidence(item) for item in value.values()))
    return isinstance(value, list) and any(contains_evidence(item) for item in value)


def _field_count(value, name):
    if isinstance(value, dict):
        return int(name in value) + sum(_field_count(item, name) for item in value.values())
    return sum(_field_count(item, name) for item in value) if isinstance(value, list) else 0


def require_policy(report):
    require_plan()
    if (type(report.get('schema')) is not int or report['schema'] != REPORT_SCHEMA
            or runner.fingerprint(report.get(POLICY_KEY)) != runner.fingerprint(POLICY)):
        raise runner.JourneyError('Missing or altered notification readiness policy')


def _command(folder, record, args, proof):
    if (set(record) != COMMAND_FIELDS or record['argv'] != ['shell', shlex.join(args)]
            or record['timed_out'] is not False or type(record['returncode']) is not int
            or not isinstance(record['started_utc'], str) or not record['started_utc']):
        raise runner.JourneyError('Invalid notification readiness command')
    start, finish, timeout = (record[key] for key in
                              ('started_monotonic', 'finished_monotonic', 'timeout_seconds'))
    if (not all(observed.finite(item) for item in (start, finish, timeout))
            or start > finish or not 0 < timeout <= POLICY['max_seconds']):
        raise runner.JourneyError('Invalid notification readiness command timing')
    return proof.artifact(folder, record['stdout']), proof.artifact(folder, record['stderr'])


def _pid(folder, record, proof):
    out, err = _command(folder, record, POLICY['commands'][0], proof)
    if record['returncode'] == 1 and out == b'' and err == b'':
        return None
    if record['returncode'] != 0 or err != b'' or re.fullmatch(rb'[1-9][0-9]*\n?', out) is None:
        raise runner.JourneyError('Unreviewed notification readiness PID result')
    return out.strip().decode('ascii')


def _foreground(folder, record, proof):
    out, err = _command(folder, record, POLICY['commands'][1], proof)
    if record['returncode'] != 0 or err != b'':
        raise runner.JourneyError('Notification readiness foreground command failed')
    front = observed.component(out, proof)
    if front not in (observed.HOME, observed.PERMISSION_ACTIVITY):
        raise runner.JourneyError('Unreviewed notification readiness foreground component')
    return front


def derive_observation(folder, commands, proof):
    if not commands:
        raise runner.JourneyError('Notification readiness observation has no command')
    first = _pid(folder, commands[0], proof)
    if first is None:
        if len(commands) != 1:
            raise runner.JourneyError('Absent PID observation contains additional commands')
        return {'state': 'MAIN_PID_ABSENT', 'pid_first': None, 'pid_final': None, 'component': None}
    if len(commands) != 3:
        raise runner.JourneyError('Present PID observation needs exactly three commands')
    front = _foreground(folder, commands[1], proof)
    last = _pid(folder, commands[2], proof)
    if last is None:
        state = 'MAIN_PID_ABSENT_AFTER_FOREGROUND'
    elif first != last:
        state = 'MAIN_PID_CHANGED'
    elif front != observed.HOME:
        state = 'PERMISSION_STILL_FOREGROUND'
    else:
        state = 'HOME_WITH_SAME_PID'
    return {'state': state, 'pid_first': first, 'pid_final': last, 'component': front}


def _sequence(rows):
    """Return the first eligible sequence; every non-ready sample resets it."""
    anchor = None
    pid = None
    for index, row in enumerate(rows):
        state = row['observation']
        if state['state'] != 'HOME_WITH_SAME_PID':
            anchor, pid = None, None
            continue
        if anchor is None or pid != state['pid_final']:
            anchor, pid = index, state['pid_final']
        if (index - anchor + 1 >= POLICY['minimum_ready_observations']
                and row['finished_monotonic'] - rows[anchor]['started_monotonic']
                >= POLICY['minimum_ready_span_seconds']):
            return [anchor, index], pid
    return None, None


def _boundary(folder, run, transition, prior, proof):
    require_plan()
    if (run.get('label') not in ('original', 'candidate')
            or transition.get('to') != POLICY['before'] or transition.get('action') != runner.DENY
            or prior.get('name') != POLICY['after'] or prior.get('owner') != runner.PERMISSION):
        raise runner.JourneyError('Notification readiness is outside the reviewed denial boundary')
    if observed.component(proof.artifact(folder, transition['preinput_artifacts']['foreground']), proof) != observed.PERMISSION_ACTIVITY:
        raise runner.JourneyError('Readiness input did not start from the observed permission component')
    return observed.one_pid(proof.artifact(folder, transition['preinput_artifacts']['pid']), proof)


def observe(recorder, run, transition, prior):
    old_pid = _boundary(recorder.folder, run, transition, prior, recorder.proof)
    if REFERENCE_KEY in transition:
        raise runner.JourneyError('Notification readiness was already attempted')
    start = time.monotonic()
    label = run['label'] + '-notification-readiness'
    phase = {'schema': 1, 'status': 'INCOMPLETE', 'label': label, 'policy': copy.deepcopy(POLICY),
             'old_pid': old_pid, 'started_monotonic': start, 'observations': [], 'gaps': []}
    deadline = start + POLICY['max_seconds']

    def execute(row, args):
        count = len(recorder.log)
        try:
            return recorder.shell(args)[0]
        finally:
            row['commands'].extend(copy.deepcopy(recorder.log[count:]))

    try:
        if start + EPSILON < transition['command']['finished_monotonic'] + POLICY['post_input_wait_seconds']:
            raise runner.JourneyError('Readiness began before the fixed post-input wait finished')
        with observed.command_budget(recorder, POLICY['max_seconds']):
            recorder.deadline = min(recorder.deadline, deadline)
            for index in range(POLICY['max_observations']):
                if time.monotonic() >= deadline:
                    raise runner.JourneyError('Notification readiness deadline expired')
                row = {'index': index, 'started_monotonic': time.monotonic(), 'commands': []}
                phase['observations'].append(row)
                try:
                    first = execute(row, POLICY['commands'][0])
                    if _pid(recorder.folder, first, recorder.proof) is not None:
                        front = execute(row, POLICY['commands'][1])
                        _foreground(recorder.folder, front, recorder.proof)
                        execute(row, POLICY['commands'][2])
                    row['observation'] = derive_observation(recorder.folder, row['commands'], recorder.proof)
                finally:
                    row['finished_monotonic'] = time.monotonic()
                if time.monotonic() > deadline:
                    raise runner.JourneyError('Notification readiness deadline expired')
                sequence, pid = _sequence(phase['observations'])
                if sequence is not None:
                    phase.update(status='READY', accepted_sequence=sequence, ready_pid=pid)
                    break
                if index + 1 == POLICY['max_observations']:
                    raise runner.JourneyError('Notification readiness observation limit exhausted')
                if time.monotonic() + POLICY['observation_gap_seconds'] > deadline:
                    raise runner.JourneyError('Insufficient notification readiness time for the next fixed gap')
                gap = {'after_index': index, 'requested_seconds': POLICY['observation_gap_seconds'],
                       'started_monotonic': time.monotonic()}
                phase['gaps'].append(gap)
                try:
                    time.sleep(gap['requested_seconds'])
                finally:
                    gap['finished_monotonic'] = time.monotonic()
    except Exception as error:
        phase.update(status='FAILED', error_type=type(error).__name__, reason=str(error))
        raise
    finally:
        phase['finished_monotonic'] = time.monotonic()
        phase['seconds'] = phase['finished_monotonic'] - start
        transition[REFERENCE_KEY] = recorder.save(label + '.json', (json.dumps(phase, indent=2) + '\n').encode())
    return phase


def verify_phase(folder, phase, proof):
    """Replay a successful phase, without claiming it as app parity evidence."""
    if (set(phase) != {'schema', 'status', 'label', 'policy', 'old_pid', 'started_monotonic',
                      'observations', 'gaps', 'accepted_sequence', 'ready_pid', 'finished_monotonic', 'seconds'}
            or phase.get('schema') != 1 or phase.get('status') != 'READY'
            or runner.fingerprint(phase.get('policy')) != runner.fingerprint(POLICY)):
        raise runner.JourneyError('Incomplete or altered notification readiness phase')
    start, finish = phase['started_monotonic'], phase['finished_monotonic']
    if (not all(observed.finite(value) for value in (start, finish, phase['seconds']))
            or not 0 <= finish - start <= POLICY['max_seconds']
            or abs(finish - start - phase['seconds']) > EPSILON):
        raise runner.JourneyError('Notification readiness exceeded its time bound')
    rows, gaps = phase['observations'], phase['gaps']
    if not 2 <= len(rows) <= POLICY['max_observations'] or len(gaps) != len(rows) - 1:
        raise runner.JourneyError('Invalid notification readiness observation or gap count')
    previous = start
    commands = []
    for index, row in enumerate(rows):
        first, last = row['started_monotonic'], row['finished_monotonic']
        if (set(row) != {'index', 'started_monotonic', 'finished_monotonic', 'commands', 'observation'}
                or type(row['index']) is not int or row['index'] != index
                or not all(observed.finite(value) for value in (first, last))
                or not previous <= first <= last <= finish):
            raise runner.JourneyError('Notification readiness observations are out of order')
        state = derive_observation(folder, row['commands'], proof)
        if row['observation'] != state:
            raise runner.JourneyError('Notification readiness state differs from its raw commands')
        command_finish = first
        for command in row['commands']:
            command_start, end = command['started_monotonic'], command['finished_monotonic']
            if (not command_finish <= command_start <= end <= last
                    or command_start + command['timeout_seconds'] > start + POLICY['max_seconds'] + EPSILON):
                raise runner.JourneyError('Notification readiness command is out of order or beyond its deadline')
            command_finish = end
            commands.append(command)
        previous = last
        if index < len(gaps):
            gap = gaps[index]
            gap_start, gap_finish = gap['started_monotonic'], gap['finished_monotonic']
            if (gap['after_index'] != index or gap['requested_seconds'] != POLICY['observation_gap_seconds']
                    or not all(observed.finite(value) for value in (gap_start, gap_finish))
                    or not last <= gap_start <= gap_finish <= finish
                    or gap_finish - gap_start + EPSILON < POLICY['observation_gap_seconds']):
                raise runner.JourneyError('Invalid notification readiness fixed gap')
            previous = gap_finish
    sequence, pid = _sequence(rows)
    if (sequence is None or sequence[-1] != len(rows) - 1 or phase.get('accepted_sequence') != sequence
            or phase.get('ready_pid') != pid):
        raise runner.JourneyError('Notification readiness did not accept the first eligible contiguous sequence')
    return commands


def _artifact_references(value):
    if isinstance(value, dict):
        if {'path', 'bytes', 'sha256'} <= set(value):
            yield value
        else:
            for item in value.values():
                yield from _artifact_references(item)
    elif isinstance(value, list):
        for item in value:
            yield from _artifact_references(item)


def _identity(folder, item, proof):
    path = runner.artifact_path(folder, item, proof)
    metadata = path.stat()
    return path, (metadata.st_dev, metadata.st_ino)


def verify_report(folder, report, proof):
    require_policy(report)
    if _field_count(report, REFERENCE_KEY) != 2 or _field_count(report, POLICY_KEY) != 1:
        raise runner.JourneyError('Missing or misplaced notification readiness evidence')
    ledger = report['commands']
    fingerprints = {}
    global_owners = {}
    for index, command in enumerate(ledger):
        fingerprints.setdefault(runner.fingerprint(command), []).append(index)
        for stream in ('stdout', 'stderr'):
            for identity in _identity(folder, command[stream], proof):
                global_owners.setdefault(identity, []).append((index, stream))
    foreign = set()
    for key, value in report.items():
        if key != 'commands':
            for item in _artifact_references(value):
                foreign.update(_identity(folder, item, proof))
    for reference in report['capture_events']:
        for item in _artifact_references(json.loads(proof.artifact(folder, reference))):
            foreign.update(_identity(folder, item, proof))
    for run in report['runs']:
        for transition in run['transitions']:
            if 'process_handoff' in transition:
                for item in _artifact_references(json.loads(proof.artifact(folder, transition['process_handoff']))):
                    foreign.update(_identity(folder, item, proof))
    used = set()
    outcomes = []
    for run in report['runs']:
        bound = [index for index, transition in enumerate(run['transitions']) if REFERENCE_KEY in transition]
        if bound != [4]:
            raise runner.JourneyError('Exactly one notification readiness proof is required at the denial boundary')
        transition = run['transitions'][4]
        prior, shot = run['screens'][4:6]
        old_pid = _boundary(folder, run, transition, prior, proof)
        reference = transition[REFERENCE_KEY]
        if reference['path'] != run['label'] + '-notification-readiness.json':
            raise runner.JourneyError('Cross-run notification readiness proof')
        phase = json.loads(proof.artifact(folder, reference))
        if phase['label'] != run['label'] + '-notification-readiness' or phase['old_pid'] != old_pid:
            raise runner.JourneyError('Notification readiness process or run binding differs')
        commands = verify_phase(folder, phase, proof)
        result_start = json.loads(proof.artifact(folder, shot['settling']))['started_monotonic']
        if (phase['started_monotonic'] + EPSILON < transition['command']['finished_monotonic'] + POLICY['post_input_wait_seconds']
                or phase['finished_monotonic'] > result_start
                or phase['ready_pid'] != observed.one_pid(proof.artifact(folder, shot['artifacts']['pid_first']), proof)):
            raise runner.JourneyError('Notification readiness is not between its input and resulting full-frame acquisition')
        indices = []
        for command in commands:
            positions = fingerprints.get(runner.fingerprint(command), [])
            if len(positions) != 1:
                raise runner.JourneyError('Notification readiness command is not unique in the global ledger')
            index = positions[0]
            indices.append(index)
            for stream in ('stdout', 'stderr'):
                for identity in _identity(folder, command[stream], proof):
                    if identity in foreign or identity in used or global_owners[identity] != [(index, stream)]:
                        raise runner.JourneyError('Notification readiness reused a command artifact from another evidence role')
                    used.add(identity)
        if indices != list(range(indices[0], indices[-1] + 1)):
            raise runner.JourneyError('Unplanned command inside notification readiness')
        phase_start, phase_end = phase['started_monotonic'], phase['finished_monotonic']
        for index, command in enumerate(ledger):
            if index in indices:
                continue
            begin, end = command['started_monotonic'], command['finished_monotonic']
            if begin < phase_end and end > phase_start:
                raise runner.JourneyError('Foreign command overlaps notification readiness')
        outcomes.append({'label': run['label'], 'observations': len(phase['observations']),
                         'states': [row['observation']['state'] for row in phase['observations']],
                         'old_pid': old_pid, 'ready_pid': phase['ready_pid'],
                         'accepted_sequence': phase['accepted_sequence'],
                         'lifecycle_observations_only': True})
    return outcomes
