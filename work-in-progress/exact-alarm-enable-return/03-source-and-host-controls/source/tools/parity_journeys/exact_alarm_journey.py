#!/usr/bin/env python3
"""One observed exact-alarm OK tap followed by a Settings observation only."""
from __future__ import annotations

from contextlib import contextmanager
import copy
import hashlib
import json
from pathlib import Path
import re
import shlex

import day_time_journey as day
import editor_journey as runner
import observed_journey as observed

REPORT_SCHEMA = 6
THIRTEEN_PLAN_SHA256 = '42ece5a06a280186ddf9796a4524975d478263e545260674e2b1b4cf718d46fb'
PLAN_SHA256 = '4133e9410db84ac5636ece780b67331bf139afaa2de6b5c110c5ef5679fda85c'
CONTRACT_SHA256 = 'e7401a3b2864b15b683efd644ebd10d6793a04b76fe83a3a4e9feb2752ada668'
PANEL_SHA256 = 'f1702bd247b1f68e54edc1d94ba928eab7a3d50cceeda8f4f9c39a8c6d272aa7'
CONTRACT_PATH = Path(__file__).with_name('fixtures') / 'exact-alarm/dialog-contract.json'
OK = day.OK
SETTINGS = 'com.android.settings'
DIALOG = 'after-day-time-trigger'
TERMINAL = 'after-exact-alarm-ok'
POLICY_KEY = 'exact_alarm_navigation_policy'
POLICY = {
    'schema': 1,
    'plan_sha256': PLAN_SHA256,
    'dialog_contract_sha256': CONTRACT_SHA256,
    'canonical_dialog_panel_sha256': PANEL_SHA256,
    'from': DIALOG,
    'from_component': day.CATALOG,
    'action': OK,
    'observed_center': [560, 809],
    'full_image_size': [720, 1280],
    'to': TERMINAL,
    'terminal_owner': SETTINGS,
    'terminal_component_class_assumed': False,
    'terminal_xml_acquisition_numbers': [1, 2, 3],
    'terminal_full_frame_numbers': [1, 2, 3, 4, 5, 6],
    'main_app_pid_continuity_required': True,
    'new_inputs': 1,
    'settings_inputs': 0,
    'permission_granted': False,
    'trigger_configuration_confirmed': False,
    'global_command_contract': {
        'schema': 1,
        'planned_inputs_per_run': 13,
        'setup_mutations_per_run': ['uninstall', 'install', 'launch'],
        'state_changing_commands_must_match_declared_roles_in_order': True,
        'other_commands_use_exact_recorder_evidence_grammar': True,
        'shell_argv_must_be_canonical': True,
        'command_stream_paths_and_inodes_are_unique': True,
    },
}


def expected_plan():
    prefix = day.expected_plan()
    if runner.fingerprint(prefix) != THIRTEEN_PLAN_SHA256:
        raise runner.JourneyError('Reviewed thirteen-screen prefix changed')
    result = copy.deepcopy(prefix)
    result[-1][2] = copy.deepcopy(OK)
    result.append([TERMINAL, SETTINGS, None, copy.deepcopy(OK)])
    if runner.fingerprint(result) != PLAN_SHA256:
        raise runner.JourneyError('Exact-alarm sequence differs from its complete reviewed identity')
    return result


def is_configured():
    return runner.fingerprint(runner.PLAN) == PLAN_SHA256


def require_plan():
    if not is_configured() or runner.fingerprint(runner.PLAN) != runner.fingerprint(expected_plan()):
        raise runner.JourneyError('Exact-alarm navigation requires the exact new fourteen-screen plan')


@contextmanager
def configured_plan():
    with day.configured_plan():
        previous = runner.PLAN
        try:
            runner.PLAN = expected_plan()
            yield runner.PLAN
        finally:
            runner.PLAN = previous


@contextmanager
def _prefix_plan():
    """Delegate unchanged prefix semantics from an already validated new plan."""
    require_plan()
    previous = runner.PLAN
    try:
        runner.PLAN = day.expected_plan()
        yield
    finally:
        runner.PLAN = previous


def _field_count(value, name):
    if isinstance(value, dict):
        return int(name in value) + sum(_field_count(item, name) for item in value.values())
    return sum(_field_count(item, name) for item in value) if isinstance(value, list) else 0


def contains_evidence(value):
    return _field_count(value, POLICY_KEY) != 0


def require_navigation_policy(report):
    require_plan()
    if (type(report.get('schema')) is not int or report['schema'] != REPORT_SCHEMA
            or report.get('plan_sha256') != PLAN_SHA256
            or runner.fingerprint(report.get('plan')) != PLAN_SHA256
            or runner.fingerprint(report.get(POLICY_KEY)) != runner.fingerprint(POLICY)
            or _field_count(report, POLICY_KEY) != 1):
        raise runner.JourneyError('Missing, altered or misplaced exact-alarm navigation policy or plan')


def _contract():
    data = CONTRACT_PATH.read_bytes()
    if hashlib.sha256(data).hexdigest() != CONTRACT_SHA256:
        raise runner.JourneyError('Observed exact-alarm dialog contract changed')
    value = json.loads(data)
    if value['canonical_panel_sha256'] != PANEL_SHA256:
        raise runner.JourneyError('Observed exact-alarm dialog panel identity changed')
    return value


def dialog_identity(folder, shot, proof):
    # This interface is the existing favourite-dialog adapter contract.
    with _prefix_plan():
        return day.dialog_identity(folder, shot, proof)


def installed_guard(recorder, run):
    with _prefix_plan():
        return day.installed_guard(recorder, run)


def verify_installed_guard(folder, transition, run, proof):
    with _prefix_plan():
        return day.verify_installed_guard(folder, transition, run, proof)


def alarm_dialog_identity(folder, shot, proof):
    require_plan()
    value = _contract()
    day.exact_component(folder, shot, value['component'], proof)
    data = proof.artifact(folder, shot['artifacts']['hierarchy'])
    root = runner.tree(data, runner.PACKAGE)
    if root.attrib != value['hierarchy_attributes'] or any(
            node.get('package') != runner.PACKAGE for node in root.iter('node')):
        raise runner.JourneyError('Exact-alarm dialog hierarchy ownership or attributes changed')
    nodes = {}
    for role in ('positive', 'cancel', 'title', 'message'):
        expected = value[role]
        node = runner.select(root, runner.PACKAGE, {'resource-id': expected['resource-id']})
        if node.attrib != expected:
            raise runner.JourneyError('Observed exact-alarm dialog ' + role + ' changed')
        nodes[role] = node
    panel = runner.select(root, runner.PACKAGE, {'resource-id': runner.PACKAGE + ':id/parentPanel'})
    if runner.fingerprint(runner.canonical(panel)) != PANEL_SHA256:
        raise runner.JourneyError('Observed exact-alarm dialog panel changed')
    parents = {child: parent for parent in root.iter() for child in parent}
    chain = [nodes['positive']]
    while chain[-1] in parents and parents[chain[-1]] is not root:
        chain.append(parents[chain[-1]])
    if ([node.attrib for node in chain] != value['positive_ancestor_chain']
            or parents.get(chain[-1]) is not root):
        raise runner.JourneyError('Observed exact-alarm positive-button ancestor chain changed')
    width, height, _ = observed.png_pixels(proof.artifact(folder, shot['artifacts']['screenshot']), proof)
    if [width, height] != value['image_size']:
        raise runner.JourneyError('Observed exact-alarm dialog full-frame size changed')
    containing = (0, 0, width, height)
    for node in reversed(chain):
        match = re.fullmatch(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', node.get('bounds', ''))
        if match is None:
            raise runner.JourneyError('Observed exact-alarm ancestor bounds are invalid')
        left, top, right, bottom = map(int, match.groups())
        if not (containing[0] <= left < right <= containing[2]
                and containing[1] <= top < bottom <= containing[3]):
            raise runner.JourneyError('Observed exact-alarm ancestor bounds are inconsistent')
        containing = (left, top, right, bottom)
    center = runner.target(data, runner.PACKAGE, OK, width, height)
    if center != value['observed_center']:
        raise runner.JourneyError('Observed exact-alarm positive-button center changed')
    return center


def validate_settings_snapshot(folder, shot, proof):
    """Allow the foreign owner only in this plan's six terminal artifact roles."""
    require_plan()
    suffixes = {'pid_first': '-pid-first.txt', 'foreground': '-foreground.txt',
                'hierarchy': '.xml', 'screenshot': '.png',
                'foreground_final': '-foreground-final.txt', 'pid_final': '-pid-final.txt'}
    if (shot.get('owner') != SETTINGS or shot.get('name', TERMINAL) != TERMINAL
            or 'observation' not in shot or set(shot['artifacts']) != set(suffixes)):
        raise runner.JourneyError('Settings observation is outside its exact terminal boundary')
    stems = set()
    for role, suffix in suffixes.items():
        path = shot['artifacts'][role]['path']
        if not isinstance(path, str) or not path.endswith(suffix):
            raise runner.JourneyError('Settings terminal artifact role changed')
        stem = path[:-len(suffix)]
        if re.fullmatch(r'(original|candidate)-after-exact-alarm-ok-acquisition-[1-3]-frame-[1-6]', stem) is None:
            raise runner.JourneyError('Settings terminal artifact label changed')
        stems.add(stem)
    if len(stems) != 1:
        raise runner.JourneyError('Settings terminal artifacts combine different observations')
    first = observed.component(proof.artifact(folder, shot['artifacts']['foreground']), proof)
    last = observed.component(proof.artifact(folder, shot['artifacts']['foreground_final']), proof)
    if first != last or last.split('/', 1)[0] != SETTINGS:
        raise runner.JourneyError('Settings terminal component is not stable')
    root = runner.tree(proof.artifact(folder, shot['artifacts']['hierarchy']), SETTINGS)
    if any(node.get('package') != SETTINGS for node in root.iter('node')):
        raise runner.JourneyError('Settings terminal hierarchy contains another owner')
    width, height, _ = observed.png_pixels(proof.artifact(folder, shot['artifacts']['screenshot']), proof)
    if [width, height] != POLICY['full_image_size']:
        raise runner.JourneyError('Settings terminal full-frame size changed')
    return last


def _command_kind(argv, installed_paths):
    """Classify only literal commands issued by the reviewed recorder source."""
    if type(argv) is not list or not argv or any(type(item) is not str or not item for item in argv):
        raise runner.JourneyError('Unknown exact-alarm global command arguments')
    if argv == ['uninstall', runner.PACKAGE]:
        return 'uninstall'
    if len(argv) == 3 and argv[:2] == ['install', '--no-streaming'] and Path(argv[2]).is_absolute():
        return 'install'
    capture_path = r'/data/local/tmp/md-journey-[0-9a-f]{32}\.xml'
    if argv == ['exec-out', 'screencap', '-p']:
        return 'evidence'
    if len(argv) == 3 and argv[:2] == ['exec-out', 'cat'] and re.fullmatch(capture_path, argv[2]):
        return 'evidence'
    if len(argv) != 2 or argv[0] != 'shell':
        raise runner.JourneyError('Unreviewed exact-alarm global command')
    parts = shlex.split(argv[1])
    if shlex.join(parts) != argv[1]:
        raise runner.JourneyError('Noncanonical exact-alarm shell command')
    if (len(parts) == 4 and parts[:2] == ['input', 'tap']
            and all(re.fullmatch(r'0|[1-9][0-9]*', value) for value in parts[2:])):
        return 'input'
    if parts == ['am', 'start', '-W', '-n', runner.PACKAGE + '/.intro.IntroActivity']:
        return 'launch'
    reads = [
        ['pidof', runner.PACKAGE], ['dumpsys', 'activity', 'activities'],
        ['dumpsys', 'activity', 'processes', runner.PACKAGE],
        ['logcat', '-d', '-b', 'crash', '-v', 'threadtime'], ['ps', '-A', '-o', 'PID,NAME'],
        ['pm', 'path', runner.PACKAGE], ['wm', 'size'], ['wm', 'density'],
        ['cmd', 'package', 'resolve-activity', '--brief', '-a', 'android.intent.action.MAIN',
         '-c', 'android.intent.category.LAUNCHER', '-p', runner.PACKAGE],
        *[['getprop', name] for name in runner.PROPERTIES],
        *[['settings', 'get', namespace, name] for namespace, name in runner.SETTINGS],
    ]
    if parts in reads:
        return 'evidence'
    if len(parts) == 2 and parts[0] == 'sha256sum' and parts[1] in installed_paths:
        return 'evidence'
    if (len(parts) == 3 and parts[:2] in (['uiautomator', 'dump'], ['rm', '-f'])
            and re.fullmatch(capture_path, parts[2])):
        return 'evidence'
    raise runner.JourneyError('Unreviewed exact-alarm global shell command')


def verify_global_commands(folder, report, proof):
    """Bind every device mutation to its planned run role, including the final tap."""
    require_navigation_policy(report)
    runs, ledger = report['runs'], report['commands']
    if [run.get('label') for run in runs] != ['original', 'candidate']:
        raise runner.JourneyError('Exact-alarm command roles require both ordered runs')
    installed_paths = [proof.installed_path(run['installed_path']['returncode'],
                        proof.artifact(folder, run['installed_path']['stdout']).decode(),
                        proof.artifact(folder, run['installed_path']['stderr']).decode()) for run in runs]
    positions, used_paths, used_inodes, mutations = {}, set(), set(), []
    previous_finish = None
    for index, command in enumerate(ledger):
        start, finish = command['started_monotonic'], command['finished_monotonic']
        if (not observed.finite(start) or not observed.finite(finish) or start > finish
                or previous_finish is not None and start < previous_finish
                or command.get('timed_out') is not False or type(command.get('returncode')) is not int):
            raise runner.JourneyError('Invalid exact-alarm global command completion or chronology')
        previous_finish = finish
        for role in ('stdout', 'stderr'):
            path = runner.artifact_path(folder, command[role], proof)
            info = path.stat(); inode = (info.st_dev, info.st_ino)
            if path in used_paths or inode in used_inodes:
                raise runner.JourneyError('Exact-alarm global command reused a stream path or inode')
            used_paths.add(path); used_inodes.add(inode)
        identity = runner.fingerprint(command)
        if identity in positions:
            raise runner.JourneyError('Exact-alarm global command record is not unique')
        positions[identity] = index
        kind = _command_kind(command.get('argv'), installed_paths)
        if kind != 'evidence':
            mutations.append((kind, identity))
    expected = []
    previous_terminal_finish = None
    for run, installed in zip(runs, installed_paths):
        setup = {
            'uninstall': ['uninstall', runner.PACKAGE],
            'absence': ['shell', shlex.join(['pm', 'path', runner.PACKAGE])],
            'install': run['install']['argv'],
            'installed_path': ['shell', shlex.join(['pm', 'path', runner.PACKAGE])],
            'installed_checksum': ['shell', shlex.join(['sha256sum', installed])],
            'launch': ['shell', shlex.join(['am', 'start', '-W', '-n', runner.PACKAGE + '/.intro.IntroActivity'])],
        }
        indices = []
        for role, argv in setup.items():
            command = run[role]; identity = runner.fingerprint(command)
            if command['argv'] != argv or identity not in positions:
                raise runner.JourneyError('Exact-alarm setup command is not bound to its unique global role')
            indices.append(positions[identity])
        if indices != sorted(set(indices)):
            raise runner.JourneyError('Exact-alarm setup command roles are out of order')
        if _command_kind(run['install']['argv'], installed_paths) != 'install':
            raise runner.JourneyError('Exact-alarm install command changed')
        if previous_terminal_finish is not None and run['uninstall']['started_monotonic'] < previous_terminal_finish:
            raise runner.JourneyError('Next exact-alarm run started before the prior terminal capture finished')
        if len(run['transitions']) != POLICY['global_command_contract']['planned_inputs_per_run']:
            raise runner.JourneyError('Exact-alarm global input count differs from its plan')
        expected.extend((role, runner.fingerprint(run[role])) for role in ('uninstall', 'install', 'launch'))
        expected.extend(('input', runner.fingerprint(transition['command'])) for transition in run['transitions'])
        terminal = run['screens'][-1]
        if terminal.get('name') != TERMINAL or terminal.get('owner') != SETTINGS:
            raise runner.JourneyError('Exact-alarm global command role has no Settings terminal')
        previous_terminal_finish = json.loads(proof.artifact(folder, terminal['settling']))['finished_monotonic']
    if mutations != expected:
        raise runner.JourneyError('Unbound, missing or reordered exact-alarm global input or setup mutation')
    return {'commands': len(ledger), 'unique_command_streams': len(used_paths),
            'planned_inputs': sum(len(run['transitions']) for run in runs),
            'setup_mutations': 6, 'unbound_mutations': 0, 'settings_inputs': 0}


def terminal_surface(folder, shot, proof):
    if shot.get('name') != TERMINAL:
        raise runner.JourneyError('Missing exact-alarm terminal observation name')
    component = validate_settings_snapshot(folder, shot, proof)
    return {'name': TERMINAL, 'owner': SETTINGS, 'component': component,
            'exact_alarm_explanation_ok_tapped': True, 'settings_navigation_observed': True,
            'settings_inputs': 0, 'permission_granted': False,
            'trigger_type_tapped': True, 'trigger_configuration_confirmed': False}


def required_surface(folder, shot, required, proof):
    require_plan()
    if shot['name'] == DIALOG:
        if required != OK:
            raise runner.JourneyError('Exact-alarm explanation requires the observed OK selector')
        alarm_dialog_identity(folder, shot, proof)
        return None
    if shot['name'] == TERMINAL:
        if required is not None:
            raise runner.JourneyError('Settings terminal observation has an assumed selector')
        return terminal_surface(folder, shot, proof)
    with _prefix_plan():
        return day.required_surface(folder, shot, required, proof)


def input_identity(folder, previous, before, action, name, proof):
    require_plan()
    if name == TERMINAL:
        if previous.get('name') != DIALOG or action != OK:
            raise runner.JourneyError('Exact-alarm OK tap is outside its observed explanation boundary')
        alarm_dialog_identity(folder, before, proof)
        return
    with _prefix_plan():
        day.input_identity(folder, previous, before, action, name, proof)


def main():
    with configured_plan():
        return runner.main()


if __name__ == '__main__':
    raise SystemExit(main())
