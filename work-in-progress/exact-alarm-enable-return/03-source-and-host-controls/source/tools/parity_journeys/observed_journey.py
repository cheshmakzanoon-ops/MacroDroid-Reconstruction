"""Opt-in evidence for one observed PID boundary and consecutive full frames.

This module never chooses a frame using another APK's capture, edits a screenshot,
or changes the existing reference plan. Legacy reports retain their original
process-continuity rule. All observations below are from a disposable emulator.
"""
from __future__ import annotations

from contextlib import contextmanager
import copy
from functools import lru_cache
import json
import math
import re
import shlex
import time
import xml.etree.ElementTree as ET

import editor_journey as runner

REPORT_SCHEMA = 3
HOME = runner.PACKAGE + '/' + runner.PACKAGE + '.homescreen.NewHomeScreenActivity'
PERMISSION_ACTIVITY = runner.PERMISSION + '/com.android.permissioncontroller.permission.ui.GrantPermissionsActivity'
POLICY = {
    'schema': 1,
    'handoff_after': 'notification-request',
    'handoff_to': 'reference-promotion',
    'handoff_action': runner.DENY,
    'handoff_component': HOME,
    'handoff_timeout_seconds': 30,
    'settling_max_attempts': 6,
    'settling_timeout_seconds': 30,
    'consecutive_identical_full_frames': 2,
    'png_and_xml_bytes_must_match': True,
    'cross_apk_frame_selection': False,
}


@lru_cache(maxsize=4)
def _decoded_png(decoder, data):
    # Pure decoding only: every caller still reads/hash-checks each artifact.
    # Both the complete bytes and decoder identity are part of the cache key.
    return decoder(data)


def png_pixels(data, proof):
    return _decoded_png(proof.png_pixels, data)


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def exact_alarm_plan():
    return runner.fingerprint(runner.PLAN) == '4133e9410db84ac5636ece780b67331bf139afaa2de6b5c110c5ef5679fda85c'


def exact_alarm_enable_return_plan():
    return runner.fingerprint(runner.PLAN) == 'ca597b23d9c2d11ebce1ed3953d609189476d7179635f2a4c4068df0795f2211'


def readiness_adapter(schema=None):
    if schema == 7 or (schema is None and exact_alarm_enable_return_plan()):
        import exact_alarm_enable_return_readiness as adapter
    elif schema == 6 or (schema is None and exact_alarm_plan()):
        import exact_alarm_readiness as adapter
    else:
        import notification_readiness as adapter
    return adapter


def information_adapter():
    if len(runner.PLAN) == 10:
        import favourite_info_journey as adapter
    elif len(runner.PLAN) == 12:
        import trigger_category_journey as adapter
    elif len(runner.PLAN) == 13:
        import day_time_journey as adapter
    elif exact_alarm_enable_return_plan():
        import exact_alarm_enable_return as adapter
    elif exact_alarm_plan():
        import exact_alarm_journey as adapter
    else:
        raise runner.JourneyError('No reviewed information adapter for this plan')
    return adapter


def require_plan():
    if (len(runner.PLAN) not in (10, 12, 13, 14, 16)
            or list(runner.PLAN[4]) != ['notification-request', runner.PERMISSION, runner.DENY, runner.NEXT]
            or list(runner.PLAN[5]) != ['reference-promotion', runner.PACKAGE, {'text': 'LITEAPKS'}, runner.DENY]
            or list(runner.PLAN[6]) != ['home', runner.PACKAGE,
                                       {'resource-id': runner.PACKAGE + ':id/navigation_home'}, {'text': 'CLOSE'}]):
        raise runner.JourneyError('Observed policy requires the unchanged reviewed reference adapter')
    if len(runner.PLAN) in (10, 12, 13) or exact_alarm_plan() or exact_alarm_enable_return_plan():
        information_adapter().require_plan()
    elif runner.fingerprint(runner.PLAN) != '69bae4f2af8e2f14c407808dbcdea91cdca009af2ae390e13b5c7fbf035a3065':
        raise runner.JourneyError('Historical fourteen-screen plan differs from its reviewed complete identity')


def required_surface(folder, shot, required, proof):
    """Only an exact reviewed adapter may declare its final unassumed surface."""
    if len(runner.PLAN) in (12, 13) or exact_alarm_plan() or exact_alarm_enable_return_plan():
        return information_adapter().required_surface(folder, shot, required, proof)
    if len(runner.PLAN) == 10:
        import favourite_info_journey as favourite
        favourite.require_plan()
        if shot['name'] == 'favourite-triggers-info':
            favourite.dialog_identity(folder, shot, proof)
        if shot['name'] == 'after-favourite-info':
            if required is not None:
                raise runner.JourneyError('Terminal surface unexpectedly has an assumed selector')
            return favourite.terminal_surface(folder, shot, proof)
    if required is None:
        raise runner.JourneyError('Only the reviewed terminal capture may omit a selector')
    runner.select(runner.tree(proof.artifact(folder, shot['artifacts']['hierarchy']), shot['owner']),
                  shot['owner'], required)
    return None


def report_policy(report):
    import exact_alarm_enable_return
    if exact_alarm_enable_return_plan() and report.get('schema') != exact_alarm_enable_return.REPORT_SCHEMA:
        raise runner.JourneyError('Exact-alarm enable/return requires schema7 and both declared policies')
    if report.get('schema') != exact_alarm_enable_return.REPORT_SCHEMA and exact_alarm_enable_return.contains_evidence(report):
        raise runner.JourneyError('Exact-alarm enable/return evidence cannot use another schema')
    import exact_alarm_journey
    if exact_alarm_plan() and report.get('schema') != exact_alarm_journey.REPORT_SCHEMA:
        raise runner.JourneyError('Exact-alarm navigation requires schema6 and both declared policies')
    if report.get('schema') != exact_alarm_journey.REPORT_SCHEMA and exact_alarm_journey.contains_evidence(report):
        raise runner.JourneyError('Exact-alarm navigation evidence cannot use an older schema')
    notification_readiness = readiness_adapter(report.get('schema'))
    readiness = report.get('schema') == notification_readiness.REPORT_SCHEMA
    if readiness:
        notification_readiness.require_policy(report)
    elif notification_readiness.contains_evidence(report):
        raise runner.JourneyError('Notification readiness evidence cannot use an older schema')
    if report.get('schema') == runner.SCHEMA:
        if 'capture_policy' in report or 'capture_events' in report:
            raise runner.JourneyError('Observed evidence cannot use the legacy schema')
        return None
    if type(report.get('schema')) is not int or report['schema'] not in (REPORT_SCHEMA, notification_readiness.REPORT_SCHEMA):
        raise runner.JourneyError('Unknown journey evidence schema')
    require_plan()
    if runner.fingerprint(report.get('capture_policy')) != runner.fingerprint(POLICY):
        raise runner.JourneyError('Unknown or altered observed capture policy')
    return POLICY


@contextmanager
def command_budget(recorder, seconds):
    previous = getattr(recorder, 'deadline', None)
    deadline = time.monotonic() + seconds
    recorder.deadline = min(previous, deadline) if previous is not None else deadline
    try:
        yield
    finally:
        recorder.deadline = previous


def capture(recorder, label, owner):
    with command_budget(recorder, POLICY['settling_timeout_seconds']):
        return recorder.snapshot(label, owner)


def one_pid(data, proof):
    text = data.decode()
    values = proof.live_pids(text, text)
    if len(values) != 1:
        raise runner.JourneyError('Exactly one live main app PID is required')
    return values[0]


def component(data, proof):
    values = proof.resumed_components(data.decode())
    if len(values) != 1:
        raise runner.JourneyError('Exactly one resumed component is required')
    package, name = values[0].split('/', 1)
    return package + '/' + (package + name if name.startswith('.') else name)


def observation(folder, shot, proof):
    state = runner.validate_snapshot(folder, shot, proof)
    artifacts = shot['artifacts']
    if set(artifacts) != {'pid_first', 'pid_final', 'foreground', 'foreground_final', 'hierarchy', 'screenshot'}:
        raise runner.JourneyError('Incomplete observed snapshot artifacts')
    first = proof.artifact(folder, artifacts['pid_first'])
    last = proof.artifact(folder, artifacts['pid_final'])
    pid = one_pid(first, proof)
    if one_pid(last, proof) != pid:
        raise runner.JourneyError('PID changed within a full-frame observation')
    front = component(proof.artifact(folder, artifacts['foreground']), proof)
    if component(proof.artifact(folder, artifacts['foreground_final']), proof) != front:
        raise runner.JourneyError('Component changed within a full-frame observation')
    timing = shot['observation']
    start, finish = timing['started_monotonic'], timing['finished_monotonic']
    if (not finite(start) or not finite(finish) or finish < start
            or abs(finish - start - shot['sample_interval_seconds']) > 0.001):
        raise runner.JourneyError('Invalid full-frame observation timing')
    paths = [runner.artifact_path(folder, item, proof) for item in artifacts.values()]
    if len(set(paths)) != len(paths):
        raise runner.JourneyError('Observation artifacts reuse a path')
    return state, pid, front


def identical_bytes(folder, a, b, proof):
    return all(proof.artifact(folder, a['artifacts'][key]) == proof.artifact(folder, b['artifacts'][key])
               for key in ['hierarchy', 'screenshot'])


def settle(recorder, label, owner, acquire):
    """Accept the first consecutive identical pair; retain every earlier attempt."""
    started = time.monotonic()
    evidence = {'schema': 1, 'status': 'INCOMPLETE', 'label': label, 'owner': owner,
                'started_monotonic': started, 'attempts': [],
                'max_attempts': POLICY['settling_max_attempts'],
                'max_seconds': POLICY['settling_timeout_seconds']}
    previous_identity = None
    frame_label = None
    try:
        for attempt in range(1, POLICY['settling_max_attempts'] + 1):
            if time.monotonic() >= recorder.deadline:
                raise runner.JourneyError('Full-frame acquisition deadline expired')
            frame_label = label + '-frame-' + str(attempt)
            shot = acquire(frame_label, owner)
            evidence['attempts'].append(shot)
            _, pid, front = observation(recorder.folder, shot, recorder.proof)
            identity = (pid, front)
            if previous_identity is not None and identity != previous_identity:
                raise runner.JourneyError('Process or component changed while waiting for full-frame stability')
            previous_identity = identity
            if len(evidence['attempts']) > 1 and identical_bytes(
                    recorder.folder, evidence['attempts'][-2], shot, recorder.proof):
                if time.monotonic() > recorder.deadline:
                    raise runner.JourneyError('Full-frame acquisition deadline expired')
                evidence['status'] = 'CONSECUTIVE_FULL_FRAMES_IDENTICAL'
                evidence['accepted_pair'] = [attempt - 2, attempt - 1]
                result = copy.deepcopy(shot)
                break
        else:
            raise runner.JourneyError('No consecutive identical full frames within six attempts')
    except Exception as error:
        evidence.update(status='FAILED', error_type=type(error).__name__, reason=str(error))
        # The base recorder saves its raw snapshot before validating XML/PID/UI.
        # This binds a rejected partial observation even when acquire raised.
        if frame_label:
            path = recorder.folder / (frame_label + '-snapshot.json')
            if path.is_file():
                data = path.read_bytes()
                evidence['last_raw_snapshot'] = recorder.save(frame_label + '-retained-snapshot.json', data)
        raise
    finally:
        evidence['finished_monotonic'] = time.monotonic()
        evidence['seconds'] = evidence['finished_monotonic'] - started
        record = recorder.save(label + '-settling.json', json.dumps(evidence, indent=2).encode())
        recorder.capture_events.append(record)
    result['settling'] = record
    return result


def stable_snapshot(folder, shot, proof, label):
    record = shot['settling']
    if not record['path'].startswith(label + '-'):
        raise runner.JourneyError('Cross-run settling evidence')
    evidence = json.loads(proof.artifact(folder, record))
    attempts = evidence['attempts']
    if (evidence.get('schema') != 1 or evidence.get('status') != 'CONSECUTIVE_FULL_FRAMES_IDENTICAL'
            or evidence['max_attempts'] != POLICY['settling_max_attempts']
            or evidence['max_seconds'] != POLICY['settling_timeout_seconds']
            or not 2 <= len(attempts) <= POLICY['settling_max_attempts']
            or evidence['accepted_pair'] != [len(attempts) - 2, len(attempts) - 1]):
        raise runner.JourneyError('Incomplete or altered full-frame stability proof')
    start, finish = evidence['started_monotonic'], evidence['finished_monotonic']
    if (not finite(start) or not finite(finish) or not 0 <= finish - start <= POLICY['settling_timeout_seconds']
            or not finite(evidence['seconds']) or abs(finish - start - evidence['seconds']) > 0.001):
        raise runner.JourneyError('Full-frame stability exceeded its time bound')
    used = set()
    identity = None
    previous_finish = start
    state = None
    for index, attempt in enumerate(attempts):
        state, pid, front = observation(folder, attempt, proof)
        timing = attempt['observation']
        if not previous_finish <= timing['started_monotonic'] <= timing['finished_monotonic'] <= finish:
            raise runner.JourneyError('Full-frame observation order is invalid')
        previous_finish = timing['finished_monotonic']
        paths = {runner.artifact_path(folder, item, proof) for item in attempt['artifacts'].values()}
        if any(not item['path'].startswith(label + '-') for item in attempt['artifacts'].values()) or used & paths:
            raise runner.JourneyError('Full-frame acquisition reused an earlier artifact')
        used |= paths
        if identity is not None and identity != (pid, front):
            raise runner.JourneyError('PID or component changed between consecutive observations')
        identity = (pid, front)
        if index:
            same = identical_bytes(folder, attempts[index - 1], attempt, proof)
            if same != (index == len(attempts) - 1):
                raise runner.JourneyError('Recorder did not accept the first consecutive identical full frames')
    selected = {key: value for key, value in shot.items() if key not in {'settling', 'name'}}
    if selected != attempts[-1] or evidence['owner'] != shot['owner']:
        raise runner.JourneyError('Selected snapshot differs from its final full-frame observation')
    return state


def input_identity(folder, previous, before, action, name, proof, label):
    if stable_snapshot(folder, previous, proof, label) != stable_snapshot(folder, before, proof, label):
        raise runner.JourneyError('Full frame changed before input')
    prior_front = component(proof.artifact(folder, previous['artifacts']['foreground_final']), proof)
    before_front = component(proof.artifact(folder, before['artifacts']['foreground_final']), proof)
    if prior_front != before_front:
        raise runner.JourneyError('Resumed component changed before input')
    data = proof.artifact(folder, before['artifacts']['hierarchy'])
    root = runner.tree(data, before['owner'])
    if action == runner.DENY:
        if name != 'reference-promotion' or previous.get('name') != 'notification-request' or prior_front != PERMISSION_ACTIVITY:
            raise runner.JourneyError('Notification denial is outside its observed boundary')
        node = runner.select(root, runner.PERMISSION, runner.DENY)
        if node.get('class') != 'android.widget.Button' or node.get('enabled') != 'true' or node.get('clickable') != 'true':
            raise runner.JourneyError('Observed notification denial button changed')
    if action == {'text': 'CLOSE'}:
        if name != 'home' or previous.get('name') != 'reference-promotion' or prior_front != HOME:
            raise runner.JourneyError('CLOSE is outside the observed promotion surface')
        title = runner.select(root, runner.PACKAGE, {'text': 'LITEAPKS'})
        button = runner.select(root, runner.PACKAGE, {'text': 'CLOSE'})
        if (title.get('class') != 'android.widget.TextView' or title.get('enabled') != 'true'
                or button.get('class') != 'android.widget.Button'
                or button.get('enabled') != 'true' or button.get('clickable') != 'true'):
            raise runner.JourneyError('Observed promotion title or CLOSE button changed')
    if name == 'after-favourite-info':
        favourite = information_adapter()
        favourite.require_plan()
        if action != favourite.OK or previous.get('name') != 'favourite-triggers-info':
            raise runner.JourneyError('Favourite information input is outside its observed boundary')
        favourite.dialog_identity(folder, before, proof)
    if len(runner.PLAN) in (12, 13) or exact_alarm_plan() or exact_alarm_enable_return_plan():
        information_adapter().input_identity(folder, previous, before, action, name, proof)
    return prior_front


def boundary_diagnostics(recorder):
    # Never clear a buffer. A separate verifier binds any new, known fatal block.
    return {key: recorder.shell(args, 10)[0] for key, args in [
        ('processes', ['dumpsys', 'activity', 'processes', runner.PACKAGE]),
        ('crash', ['logcat', '-d', '-b', 'crash', '-v', 'threadtime']),
    ]}


FRAGMENT_FATAL_STACK = [
    'at android.app.Fragment.getResources(Fragment.java:785)',
    'at com.zx.lbua80.onShow(Unknown Source:22)',
    'at android.app.Dialog$ListenersHandler.handleMessage(Dialog.java:1500)',
    'at android.os.Handler.dispatchMessage(Handler.java:107)',
    'at android.os.Looper.loopOnce(Looper.java:232)',
    'at android.os.Looper.loop(Looper.java:317)',
    'at android.app.ActivityThread.main(ActivityThread.java:8705)',
    'at java.lang.reflect.Method.invoke(Native Method)',
    'at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:580)',
    'at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:886)',
]


def crash_observation(folder, before, after, old_pid, proof):
    """Classify only the observed LB fatal stack; retain all literal log bytes.

    This is not a claim that notification denial caused the crash. An empty or
    unavailable Java crash buffer cannot establish that a run was crash-free.
    """
    records = [before['crash'], after['crash']]
    data = []
    for record in records:
        out, err = (proof.artifact(folder, record[key]) for key in ['stdout', 'stderr'])
        if record['returncode'] != 0 or err.strip():
            return {'classification': {'status': 'CRASH_DIAGNOSTIC_UNAVAILABLE'}, 'new_fatal_blocks': []}
        data.append(out.decode())
    pattern = re.compile(r'^(\d\d-\d\d \d\d:\d\d:\d\d\.\d{3})\s+([1-9]\d*)\s+([1-9]\d*)\s+[EF]\s+AndroidRuntime: ?(.*)$')
    blocks = []
    for line in data[1].splitlines(keepends=True):
        match = pattern.fullmatch(line.rstrip('\r\n'))
        if not match or match[2] != old_pid:
            continue
        payload = match[4]
        if payload.startswith('FATAL EXCEPTION:'):
            blocks.append({'header': line, 'lines': [], 'payloads': [], 'thread': match[3]})
        if blocks:
            blocks[-1]['lines'].append(line)
            blocks[-1]['payloads'].append(payload)
    events = []
    for block in blocks:
        if block['header'] in data[0]:
            continue
        payloads = block['payloads']
        if (block['thread'] != old_pid or len(payloads) != 13 or payloads[0] != 'FATAL EXCEPTION: main'
                or payloads[1] != 'Process: ' + runner.PACKAGE + ', PID: ' + old_pid
                or not re.fullmatch(r'java\.lang\.IllegalStateException: Fragment LB\{[0-9a-f]+\} not attached to Activity', payloads[2])
                or [value.strip() for value in payloads[3:]] != FRAGMENT_FATAL_STACK):
            raise runner.JourneyError('Unreviewed new fatal exception at the notification boundary; raw log retained')
        events.append({'literal_header': block['header'], 'literal_exception': payloads[2],
                       'literal_block': ''.join(block['lines'])})
    if not events:
        classification = {'status': 'NO_NEW_JAVA_FATAL_EXCEPTION_OBSERVED'}
    else:
        classification = {'status': 'NEW_OBSERVED_FRAGMENT_FATAL_EXCEPTION', 'count': len(events),
                          'exception_type': 'java.lang.IllegalStateException',
                          'message_pattern': 'Fragment LB{hex instance} not attached to Activity',
                          'stack': FRAGMENT_FATAL_STACK}
    return {'classification': classification, 'new_fatal_blocks': events}


def outcome(old, new, crash):
    known_fatal = crash['classification']['status'] == 'NEW_OBSERVED_FRAGMENT_FATAL_EXCEPTION'
    return {'pid_replaced': old != new, 'old_pid_absent_in_both_lists': old != new,
            'component': HOME, 'installed_apk_identity_verified': True,
            'cause': 'RECORDED_JAVA_FATAL_EXCEPTION' if known_fatal else 'UNDETERMINED',
            'crash_observation': crash['classification']}


def parse_processes(data):
    lines = data.decode().splitlines()
    if not lines or lines[0].split() != ['PID', 'NAME']:
        raise runner.JourneyError('Unexpected complete process-list header')
    values = {}
    for line in lines[1:]:
        match = re.fullmatch(r'\s*([1-9][0-9]*)\s+(\S.*?)\s*', line)
        if not match or match[1] in values:
            raise runner.JourneyError('Malformed or duplicate process-list row')
        values[match[1]] = match[2]
    if '1' not in values or len(values) < 2:
        raise runner.JourneyError('Incomplete all-process listing')
    return values


def check_processes(data, old, new):
    values = parse_processes(data)
    if [pid for pid, name in values.items() if name == runner.PACKAGE] != [new]:
        raise runner.JourneyError('Expected single main app process is absent or ambiguous')
    if (old not in values) != (old != new):
        raise runner.JourneyError('Old PID remains present after a claimed replacement')


def checked_command(folder, record, args, proof):
    if record['argv'] != ['shell', shlex.join(args)]:
        raise runner.JourneyError('Observed device command differs from the required command')
    out, err = runner.evidence_command(folder, record, proof)
    if err.strip() or record.get('timed_out') is not False:
        raise runner.JourneyError('Observed device command failed or timed out')
    start, finish = record['started_monotonic'], record['finished_monotonic']
    if not finite(start) or not finite(finish) or finish < start:
        raise runner.JourneyError('Invalid observed command timing')
    return out


def verify_preinput(folder, transition, proof):
    start = transition['observation_started_monotonic']
    input_start = transition['command']['started_monotonic']
    age = transition['precondition_age_seconds']
    before = json.loads(proof.artifact(folder, transition['before']['settling']))
    if (not finite(start) or not finite(input_start) or not 0 <= input_start - start <= runner.MAX_PRECONDITION_AGE
            or abs(input_start - start - age) > 0.05
            or transition['command'].get('timed_out') is not False
            or not start <= before['started_monotonic'] <= before['finished_monotonic'] <= input_start):
        raise runner.JourneyError('Recorded input freshness does not include its full acquisition')
    commands = transition['preinput_commands']
    if list(commands) != ['pid', 'foreground']:
        raise runner.JourneyError('Incomplete immediate pre-input command records')
    previous = before['finished_monotonic']
    used = {runner.artifact_path(folder, item, proof) for item in transition['before']['artifacts'].values()}
    used |= {runner.artifact_path(folder, item, proof) for item in transition['preinput_artifacts'].values()}
    for key, args in [('pid', ['pidof', runner.PACKAGE]), ('foreground', ['dumpsys', 'activity', 'activities'])]:
        command = commands[key]
        out = checked_command(folder, command, args, proof)
        if (out != proof.artifact(folder, transition['preinput_artifacts'][key])
                or not previous <= command['started_monotonic'] <= command['finished_monotonic'] <= input_start):
            raise runner.JourneyError('Immediate pre-input bytes or timing are inconsistent')
        paths = {runner.artifact_path(folder, command[stream], proof) for stream in ['stdout', 'stderr']}
        if len(paths) != 2 or used & paths:
            raise runner.JourneyError('Immediate pre-input command reused earlier artifacts')
        used |= paths
        previous = command['finished_monotonic']


def handoff_outcome(folder, record, run, transition, prior, shot, proof):
    """Validate actual bytes before authorizing a new phase's PID anchor."""
    if (transition.get('to') != 'reference-promotion' or transition.get('action') != runner.DENY
            or prior.get('name') != 'notification-request' or shot.get('name') != 'reference-promotion'):
        raise runner.JourneyError('Process boundary is outside notification denial')
    if type(record.get('schema')) is not int or record['schema'] != 1 or record.get('status') != 'OBSERVED_NOTIFICATION_BOUNDARY':
        raise runner.JourneyError('Incomplete notification-boundary observation')
    old = one_pid(proof.artifact(folder, transition['preinput_artifacts']['pid']), proof)
    new = one_pid(proof.artifact(folder, shot['artifacts']['pid_first']), proof)
    if component(proof.artifact(folder, shot['artifacts']['foreground_final']), proof) != HOME:
        raise runner.JourneyError('Unexpected post-denial resumed component')
    commands = record['commands']
    keys = ['pid_first', 'process_list_first', 'installed_path', 'installed_checksum', 'foreground',
            'process_list_final', 'pid_final']
    if list(commands) != keys:
        raise runner.JourneyError('Incomplete or reordered notification-boundary commands')
    path_data = checked_command(folder, commands['installed_path'], ['pm', 'path', runner.PACKAGE], proof)
    path = proof.installed_path(0, path_data.decode(), '')
    old_out, old_err = runner.evidence_command(folder, run['installed_path'], proof)
    if path != proof.installed_path(0, old_out.decode(), old_err.decode()):
        raise runner.JourneyError('Installed APK path changed across notification denial')
    digest = checked_command(folder, commands['installed_checksum'], ['sha256sum', path], proof)
    if proof.installed_digest(0, digest.decode(), '', path) != run['apk_sha256']:
        raise runner.JourneyError('Fresh post-denial installed APK identity differs')
    for key in ['pid_first', 'pid_final']:
        if one_pid(checked_command(folder, commands[key], ['pidof', runner.PACKAGE], proof), proof) != new:
            raise runner.JourneyError('PID changed during the notification-boundary checks')
    for key in ['process_list_first', 'process_list_final']:
        check_processes(checked_command(folder, commands[key], ['ps', '-A', '-o', 'PID,NAME'], proof), old, new)
    front = checked_command(folder, commands['foreground'], ['dumpsys', 'activity', 'activities'], proof)
    if component(front, proof) != HOME:
        raise runner.JourneyError('Unexpected component during notification-boundary checks')
    start, finish = record['started_monotonic'], record['finished_monotonic']
    if (not finite(start) or not finite(finish) or not 0 <= finish - start <= POLICY['handoff_timeout_seconds']
            or transition['command']['finished_monotonic'] > shot['observation']['started_monotonic']
            or shot['observation']['finished_monotonic'] > start):
        raise runner.JourneyError('Stale or unordered notification-boundary evidence')
    previous = start
    all_paths = set()
    stale = {runner.artifact_path(folder, item, proof)
             for snapshot in [prior, transition['before'], shot] for item in snapshot['artifacts'].values()}
    stale |= {runner.artifact_path(folder, item, proof) for item in transition['preinput_artifacts'].values()}
    for command in [run['installed_path'], run['installed_checksum'], transition['command'],
                    *transition['preinput_commands'].values(), *transition['pre_denial_diagnostics'].values()]:
        stale |= {runner.artifact_path(folder, command[stream], proof) for stream in ['stdout', 'stderr']}
    for key in keys:
        command = commands[key]
        if not previous <= command['started_monotonic'] <= command['finished_monotonic'] <= finish:
            raise runner.JourneyError('Boundary command order is not fresh')
        previous = command['finished_monotonic']
        paths = {runner.artifact_path(folder, command[stream], proof) for stream in ['stdout', 'stderr']}
        if len(paths) != 2 or all_paths & paths or stale & paths:
            raise runner.JourneyError('Boundary command reused an earlier artifact')
        if any(not command[stream]['path'].startswith('command-') for stream in ['stdout', 'stderr']):
            raise runner.JourneyError('Unexpected boundary command artifact identity')
        all_paths |= paths
    before_event = json.loads(proof.artifact(folder, transition['before']['settling']))
    verify_diagnostics(folder, transition['pre_denial_diagnostics'], proof,
                       transition['observation_started_monotonic'], before_event['started_monotonic'])
    verify_diagnostics(folder, record['after_diagnostics'], proof, previous, finish)
    crash = crash_observation(folder, transition['pre_denial_diagnostics'], record['after_diagnostics'], old, proof)
    expected = outcome(old, new, crash)
    if (record['old_pid'] != old or record['new_pid'] != new
            or runner.fingerprint(record['outcome']) != runner.fingerprint(expected)
            or runner.fingerprint(record['crash_observation']) != runner.fingerprint(crash)):
        raise runner.JourneyError('Reported process/crash outcome differs from observed command bytes')
    return expected


def verify_diagnostics(folder, diagnostics, proof, earliest, latest):
    if set(diagnostics) != {'processes', 'crash'}:
        raise runner.JourneyError('Missing raw process/crash diagnostics')
    for key, args in [('processes', ['dumpsys', 'activity', 'processes', runner.PACKAGE]),
                      ('crash', ['logcat', '-d', '-b', 'crash', '-v', 'threadtime'])]:
        record = diagnostics[key]
        if record['argv'] != ['shell', shlex.join(args)] or type(record['returncode']) is not int:
            raise runner.JourneyError('Invalid diagnostic command')
        start, finish = record['started_monotonic'], record['finished_monotonic']
        if not finite(start) or not finite(finish) or not earliest <= start <= finish <= latest or record.get('timed_out') is not False:
            raise runner.JourneyError('Raw diagnostic timing is outside the observed boundary')
        earliest = finish
        for stream in ['stdout', 'stderr']:
            proof.artifact(folder, record[stream])


def observe_handoff(recorder, run, transition, prior, shot):
    started = time.monotonic()
    record = {'schema': 1, 'status': 'INCOMPLETE', 'started_monotonic': started, 'commands': {}}
    try:
        with command_budget(recorder, POLICY['handoff_timeout_seconds']):
            for key, args in [
                ('pid_first', ['pidof', runner.PACKAGE]),
                ('process_list_first', ['ps', '-A', '-o', 'PID,NAME']),
                ('installed_path', ['pm', 'path', runner.PACKAGE]),
            ]:
                record['commands'][key], out, err = recorder.shell(args)
            path_record = record['commands']['installed_path']
            out, err = runner.evidence_command(recorder.folder, path_record, recorder.proof)
            installed = recorder.proof.installed_path(path_record['returncode'], out.decode(), err.decode())
            for key, args in [
                ('installed_checksum', ['sha256sum', installed]),
                ('foreground', ['dumpsys', 'activity', 'activities']),
                ('process_list_final', ['ps', '-A', '-o', 'PID,NAME']),
                ('pid_final', ['pidof', runner.PACKAGE]),
            ]:
                record['commands'][key] = recorder.shell(args)[0]
            record['after_diagnostics'] = boundary_diagnostics(recorder)
            old = one_pid(recorder.proof.artifact(recorder.folder, transition['preinput_artifacts']['pid']), recorder.proof)
            new = one_pid(recorder.proof.artifact(recorder.folder, shot['artifacts']['pid_first']), recorder.proof)
            crash = crash_observation(recorder.folder, transition['pre_denial_diagnostics'],
                                      record['after_diagnostics'], old, recorder.proof)
            record.update(old_pid=old, new_pid=new, status='OBSERVED_NOTIFICATION_BOUNDARY',
                          finished_monotonic=time.monotonic(),
                          outcome=outcome(old, new, crash), crash_observation=crash)
            handoff_outcome(recorder.folder, record, run, transition, prior, shot, recorder.proof)
    except Exception as error:
        record.update(status='FAILED', reason=str(error), error_type=type(error).__name__)
        raise
    finally:
        record['finished_monotonic'] = time.monotonic()
        transition['process_handoff'] = recorder.save(run['label'] + '-notification-boundary.json',
                                                      json.dumps(record, indent=2).encode())


def verified_handoff(folder, run, transition, prior, shot, proof):
    artifact = transition['process_handoff']
    if artifact['path'] != run['label'] + '-notification-boundary.json':
        raise runner.JourneyError('Cross-run process-boundary artifact')
    return handoff_outcome(folder, json.loads(proof.artifact(folder, artifact)), run, transition, prior, shot, proof)


def capture_events(folder, report, proof):
    """Bind successful ledgers and rejected XML acquisitions retained by the adapter."""
    entries = report['capture_events']
    paths = set()
    for entry in entries:
        path = runner.artifact_path(folder, entry, proof)
        if path in paths:
            raise runner.JourneyError('Duplicate acquisition ledger')
        paths.add(path)
        event = json.loads(proof.artifact(folder, entry))
        if event['status'] == 'FAILED':
            if event.get('error_type') != 'ParseError':
                raise runner.JourneyError('Completed journey contains a rejected semantic/process acquisition')
            raw = json.loads(proof.artifact(folder, event['last_raw_snapshot']))
            try:
                runner.validate_snapshot(folder, raw, proof)
            except ET.ParseError:
                pass
            else:
                raise runner.JourneyError('Retry was not caused by an actual XML parser failure')
        elif event['status'] != 'CONSECUTIVE_FULL_FRAMES_IDENTICAL':
            raise runner.JourneyError('Incomplete acquisition ledger')
    for run in report['runs']:
        shots = run['screens'] + [transition['before'] for transition in run['transitions']]
        for shot in shots:
            if runner.artifact_path(folder, shot['settling'], proof) not in paths:
                raise runner.JourneyError('Accepted observation is missing from the acquisition ledger')
    import capture_chronology
    capture_chronology.verify(folder, report, proof)
