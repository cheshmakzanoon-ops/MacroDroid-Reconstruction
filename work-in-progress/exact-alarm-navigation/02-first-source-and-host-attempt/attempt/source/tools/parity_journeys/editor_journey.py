#!/usr/bin/env python3
"""Fresh-install, notification-denial and editor-navigation differential capture.
No macro is saved or executed, no permission is granted, no account is used.
Full screenshots and every UI attribute are compared without masks.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shlex
import shutil
import subprocess
import sys
import time
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

PACKAGE = 'com.arlosoft.macrodroid'
PERMISSION = 'com.google.android.permissioncontroller'
SCHEMA = 2
MAX_PRECONDITION_AGE = 15
NEXT = {'resource-id': PACKAGE + ':id/button_next'}
# The Google permission-controller APK retains the AOSP resource namespace.
DENY = {'resource-id': 'com.android.permissioncontroller:id/permission_deny_button'}
TRIGGER = {'resource-id': PACKAGE + ':id/edit_macro_addTriggerButton'}
ACTION = {'resource-id': PACKAGE + ':id/edit_macro_addActionButton'}
CONSTRAINT = {'resource-id': PACKAGE + ':id/edit_macro_addConstraintButton'}
PLAN = [
    ('intro-1', PACKAGE, {'text': 'MACRODROID'}, None),
    ('intro-2', PACKAGE, {'text': 'TRIGGERS'}, NEXT),
    ('intro-3', PACKAGE, {'text': 'ACTIONS'}, NEXT),
    ('intro-4', PACKAGE, {'text': 'CONSTRAINTS'}, NEXT),
    ('notification-request', PERMISSION, DENY, NEXT),
    ('home', PACKAGE, {'resource-id': PACKAGE + ':id/navigation_home'}, DENY),
    ('empty-editor', PACKAGE, TRIGGER, {'text': 'Add Macro'}),
    ('trigger-catalog', PACKAGE, {'text': 'Add Trigger'}, TRIGGER),
    ('editor-after-trigger-back', PACKAGE, ACTION, 'BACK'),
    ('action-catalog', PACKAGE, {'text': 'Add Action'}, ACTION),
    ('editor-after-action-back', PACKAGE, CONSTRAINT, 'BACK'),
    ('constraint-catalog', PACKAGE, {'text': 'Add constraint'}, CONSTRAINT),
    ('editor-after-constraint-back', PACKAGE, TRIGGER, 'BACK'),
]
PROPERTIES = ['ro.build.fingerprint', 'ro.build.version.sdk', 'ro.product.cpu.abilist',
              'ro.kernel.qemu', 'persist.sys.locale', 'persist.sys.timezone']
SETTINGS = [('system', 'font_scale'), ('global', 'animator_duration_scale'),
            ('global', 'window_animation_scale'), ('global', 'transition_animation_scale'),
            ('global', 'airplane_mode_on'), ('global', 'wifi_on'), ('global', 'mobile_data'),
            ('global', 'sysui_demo_allowed'), ('global', 'sysui_tuner_demo_on')]

class JourneyError(ValueError):
    pass

def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def tree(data, owner):
    if len(data) > 8_000_000 or b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():
        raise JourneyError('Unsafe UI XML')
    root = ET.fromstring(data)
    if root.tag != 'hierarchy' or len(list(root.iter())) > 50_000:
        raise JourneyError('Invalid UI hierarchy')
    if not any(n.get('package') == owner for n in root.iter('node')):
        raise JourneyError('Expected screen owner is absent')
    return root

def canonical(root, depth=0):
    if depth > 100:
        raise JourneyError('Excessive UI depth')
    return (root.tag, tuple(sorted(root.attrib.items())), root.text if root.text and root.text.strip() else '',
            root.tail if root.tail and root.tail.strip() else '', tuple(canonical(n, depth + 1) for n in root))

def select(root, owner, selector):
    if not isinstance(selector, dict) or not selector or set(selector) - {'resource-id', 'text', 'content-desc'}:
        raise JourneyError('Invalid selector')
    nodes = [n for n in root.iter('node') if n.get('package') == owner
             and all(n.get(k) == v for k, v in selector.items())]
    if len(nodes) != 1:
        raise JourneyError('Missing or ambiguous selector: ' + str(selector))
    return nodes[0]

def target(data, owner, selector, width, height):
    root = tree(data, owner)
    node = select(root, owner, selector)
    parents = {child: parent for parent in root.iter() for child in parent}
    while node.get('clickable') != 'true':
        if node.get('enabled') != 'true' or node not in parents:
            raise JourneyError('Selector is disabled or has no clickable ancestor')
        node = parents[node]
        if node.get('package') != owner:
            raise JourneyError('Clickable ancestor belongs to another package')
    if node.get('enabled') != 'true':
        raise JourneyError('Click target is disabled')
    bounds = re.fullmatch(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', node.get('bounds', ''))
    if not bounds:
        raise JourneyError('Invalid click bounds')
    l, t, r, b = map(int, bounds.groups())
    if not (0 <= l < r <= width and 0 <= t < b <= height):
        raise JourneyError('Click target is outside the screen')
    return [(l + r) // 2, (t + b) // 2]

def resumed(text, owner):
    from android_compare import resumed_components
    components = resumed_components(text)
    return bool(components) and all(c.split('/', 1)[0] == owner for c in components)


def evidence_command(folder, record, proof, clean=False, codes=(0,)):
    if type(record.get('returncode')) is not int or record['returncode'] not in codes:
        raise JourneyError('Recorded command failed')
    out = proof.artifact(folder, record['stdout'])
    err = proof.artifact(folder, record['stderr'])
    if clean and (out.strip() or err.strip()):
        raise JourneyError('Input command did not complete cleanly')
    return out, err

def artifact_path(folder, record, proof):
    # Validate the bytes and confinement before comparing normalized identities.
    proof.artifact(folder, record)
    return (folder / record['path']).resolve()

class Recorder:
    def __init__(self, folder, serial, proof):
        self.folder, self.serial, self.proof = folder, serial, proof
        self.adb = shutil.which('adb')
        if not self.adb:
            raise JourneyError('ADB unavailable')
        self.count = 0
        self.log = []
        self.capture_policy = None
        self.capture_events = []
        self.deadline = None
    def save(self, name, data):
        (self.folder / name).write_bytes(data)
        return {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    def cmd(self, args, timeout=120):
        if self.deadline is not None:
            timeout = min(timeout, self.deadline - time.monotonic())
            if timeout <= 0:
                raise JourneyError('Observed command deadline expired before execution')
        self.count += 1
        name = f'command-{self.count:05}'
        started = time.monotonic()
        started_utc = datetime.now(timezone.utc).isoformat()
        timed_out = False
        try:
            p = subprocess.run([self.adb, '-s', self.serial, *args], capture_output=True, timeout=timeout)
            code, out, err = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as error:
            code, out, err = None, error.stdout or b'', error.stderr or b''
            timed_out = True
        item = {'argv': args, 'returncode': code, 'timed_out': timed_out,
                'started_utc': started_utc, 'started_monotonic': started,
                'finished_monotonic': time.monotonic(), 'timeout_seconds': timeout,
                'stdout': self.save(name + '.stdout', out),
                'stderr': self.save(name + '.stderr', err)}
        self.log.append(item)
        if timed_out:
            raise JourneyError('Device command timed out; partial output retained')
        return item, out, err
    def shell(self, args, timeout=120):
        return self.cmd(['shell', shlex.join(args)], timeout)
    def ok(self, args):
        item, out, err = self.shell(args)
        if item['returncode']:
            raise JourneyError('Device command failed: ' + str(args))
        return out
    def environment(self):
        result = {'serial': self.serial}
        for p in PROPERTIES:
            result[p] = self.ok(['getprop', p]).decode().strip()
        for namespace, name in SETTINGS:
            result[namespace + ':' + name] = self.ok(['settings', 'get', namespace, name]).decode().strip()
        for name in ['size', 'density']:
            result['display_' + name] = self.ok(['wm', name]).decode().strip()
        return result
    def snapshot(self, label, owner):
        if getattr(self, 'capture_policy', None) is not None:
            import observed_journey
            return observed_journey.settle(self, label, owner, self._snapshot_once)
        return self._snapshot_once(label, owner)
    def _snapshot_once(self, label, owner):
        started = time.monotonic()
        a = {}
        a['pid_first'] = self.save(label + '-pid-first.txt', self.ok(['pidof', PACKAGE]))
        a['foreground'] = self.save(label + '-foreground.txt', self.ok(['dumpsys', 'activity', 'activities']))
        remote = '/data/local/tmp/md-journey-' + uuid.uuid4().hex + '.xml'
        try:
            self.ok(['uiautomator', 'dump', remote])
            item, data, err = self.cmd(['exec-out', 'cat', remote])
            if item['returncode']:
                raise JourneyError('UI dump retrieval failed')
            a['hierarchy'] = self.save(label + '.xml', data)
        finally:
            self.shell(['rm', '-f', remote])
        item, png, err = self.cmd(['exec-out', 'screencap', '-p'])
        if item['returncode']:
            raise JourneyError('Screenshot failed')
        a['screenshot'] = self.save(label + '.png', png)
        time.sleep(max(0, 1.05 - (time.monotonic() - started)))
        if getattr(self, 'capture_policy', None) is not None:
            a['foreground_final'] = self.save(label + '-foreground-final.txt', self.ok(['dumpsys', 'activity', 'activities']))
        a['pid_final'] = self.save(label + '-pid-final.txt', self.ok(['pidof', PACKAGE]))
        finished = time.monotonic()
        result = {'owner': owner, 'artifacts': a, 'sample_interval_seconds': finished - started}
        if getattr(self, 'capture_policy', None) is not None:
            result['observation'] = {'started_monotonic': started, 'finished_monotonic': finished}
        # Persist even an unexpected screen as diagnostic evidence before validation.
        self.save(label + '-snapshot.json', json.dumps(result, indent=2).encode())
        validate_snapshot(self.folder, result, self.proof)
        return result

def validate_snapshot(folder, shot, proof):
    a = shot['artifacts']
    if shot['owner'] not in (PACKAGE, PERMISSION):
        import exact_alarm_journey
        if not exact_alarm_journey.is_configured() or shot['owner'] != exact_alarm_journey.SETTINGS:
            raise JourneyError('Invalid snapshot owner or live interval')
        exact_alarm_journey.validate_settings_snapshot(folder, shot, proof)
    if not proof.valid_live_interval(shot['sample_interval_seconds']):
        raise JourneyError('Invalid snapshot owner or live interval')
    proof.live_pids(proof.artifact(folder, a['pid_first']).decode(), proof.artifact(folder, a['pid_final']).decode())
    if not resumed(proof.artifact(folder, a['foreground']).decode(), shot['owner']):
        raise JourneyError('Expected activity is not resumed')
    data = proof.artifact(folder, a['hierarchy'])
    root = tree(data, shot['owner'])
    png = proof.artifact(folder, a['screenshot'])
    if 'observation' in shot:
        import observed_journey
        width, height, pixels = observed_journey.png_pixels(png, proof)
    else:
        width, height, pixels = proof.png_pixels(png)
    return canonical(root), width, height, pixels, proof.color_metadata(png)

def capture_transition(recorder, previous, label, name, action, proof, run=None):
    if getattr(recorder, 'capture_policy', None) is not None:
        import observed_journey
        with observed_journey.command_budget(recorder, MAX_PRECONDITION_AGE):
            return _capture_transition(recorder, previous, label, name, action, proof, run)
    return _capture_transition(recorder, previous, label, name, action, proof, run)

def _capture_transition(recorder, previous, label, name, action, proof, run=None):
    # Acquisition can be slow: the freshness budget includes the entire snapshot.
    started = time.monotonic()
    policy = getattr(recorder, 'capture_policy', None)
    diagnostics = None
    installed_guard = None
    if policy is not None:
        import observed_journey
        if action == DENY:
            diagnostics = observed_journey.boundary_diagnostics(recorder)
        if name == 'after-favourite-info':
            favourite = observed_journey.information_adapter()
            favourite.require_plan()
            installed_guard = favourite.installed_guard(recorder, run)
    before = recorder.snapshot(label + '-before', previous['owner'])
    proof.live_pids(proof.artifact(recorder.folder, previous['artifacts']['pid_final']).decode(),
                    proof.artifact(recorder.folder, before['artifacts']['pid_final']).decode())
    prior_state = validate_snapshot(recorder.folder, previous, proof)
    if validate_snapshot(recorder.folder, before, proof)[0] != prior_state[0]:
        raise JourneyError('UI changed before action')
    if artifact_path(recorder.folder, before['artifacts']['hierarchy'], proof) == artifact_path(
            recorder.folder, previous['artifacts']['hierarchy'], proof):
        raise JourneyError('Reused stale input precondition')
    expected_component = None
    if policy is not None:
        expected_component = observed_journey.input_identity(
            recorder.folder, previous, before, action, name, proof, label.split('-', 1)[0])
    argv = ['input', 'keyevent', '4'] if action == 'BACK' else ['input', 'tap', *map(str, target(
        proof.artifact(recorder.folder, before['artifacts']['hierarchy']), previous['owner'], action,
        prior_state[1], prior_state[2]))]
    # These observations occur after the dump, retrieval, screenshot and UI checks.
    live = {}
    live_commands = {}
    for key, args in [('pid', ['pidof', PACKAGE]), ('foreground', ['dumpsys', 'activity', 'activities'])]:
        item, out, err = recorder.shell(args)
        live[key] = recorder.save(label + '-preinput-' + key + '.txt', out)
        if policy is not None:
            live_commands[key] = item
        if type(item['returncode']) is not int or item['returncode'] != 0 or err.strip():
            raise JourneyError('Immediate input ' + key + ' check failed')
        if key == 'pid':
            proof.live_pids(proof.artifact(recorder.folder, before['artifacts']['pid_final']).decode(), out.decode())
        elif not resumed(out.decode(), previous['owner']):
            raise JourneyError('Expected activity left the foreground before input')
        elif expected_component is not None and observed_journey.component(out, proof) != expected_component:
            raise JourneyError('Expected component left the foreground before input')
    age = time.monotonic() - started
    if not 0 <= age <= MAX_PRECONDITION_AGE:
        raise JourneyError('Input precondition expired')
    cmd, out, err = recorder.shell(argv)
    transition = {'to': name, 'action': action, 'before': before, 'preinput_artifacts': live,
                  'precondition_age_seconds': age, 'command': cmd}
    if policy is not None:
        transition['observation_started_monotonic'] = started
        transition['preinput_commands'] = live_commands
        if diagnostics is not None:
            transition['pre_denial_diagnostics'] = diagnostics
        if installed_guard is not None:
            transition['pre_ok_installed_identity'] = installed_guard
    if cmd['returncode'] or out.strip() or err.strip():
        raise JourneyError('Input did not complete cleanly')
    return transition

def compare(folder, report, proof):
    result = {'status': 'REJECTED', 'journey_equal': False, 'full_runtime_1_to_1_established': False,
              'scope': 'Fresh install, notification denial, home and empty-editor catalog navigation only',
              'screens': [], 'masks_used': False, 'android_runtime_executed': False, 'macros_executed': False, 'macros_saved': False}
    try:
        import observed_journey
        policy = observed_journey.report_policy(report)
        if report.get('plan_sha256') != fingerprint(PLAN) or report.get('status') != 'RECORDED_NOT_PARITY':
            raise JourneyError('Unexpected journey schema or plan')
        runs = report['runs']
        if len(runs) != 2 or [r['label'] for r in runs] != ['original', 'candidate']:
            raise JourneyError('Two correctly ordered runs required')
        if runs[0]['apk_sha256'] != proof.ORIGINAL_SHA256 or runs[1]['apk_sha256'] == runs[0]['apk_sha256']:
            raise JourneyError('Invalid original/candidate identities')
        if runs[0]['environment'] != runs[1]['environment']:
            raise JourneyError('Device environments differ')
        env = runs[0]['environment']
        required_env = {'serial', 'display_size', 'display_density', *PROPERTIES,
                        *(namespace + ':' + name for namespace, name in SETTINGS)}
        if set(env) != required_env or env['ro.kernel.qemu'] != '1' or not env['serial'] or env['ro.build.version.sdk'] != '35' or 'arm64-v8a' not in env['ro.product.cpu.abilist'].split(','):
            raise JourneyError('Incomplete or unsupported device evidence')
        if not re.fullmatch('[0-9a-f]{64}', runs[1]['apk_sha256']):
            raise JourneyError('Invalid candidate checksum')
        states = []
        handoffs = []
        terminal_surfaces = []
        for run in runs:
            if run['status'] != 'COMPLETE' or run['environment'] != run['environment_after']:
                raise JourneyError('Incomplete run or changed environment')
            out, err = evidence_command(folder, run['absence'], proof, codes=(0, 1))
            if not proof.absence_ok(run['absence']['returncode'], out.decode(), err.decode()):
                raise JourneyError('Fresh package state was not verified')
            out, err = evidence_command(folder, run['install'], proof)
            if not proof.install_ok(0, out.decode(), err.decode()):
                raise JourneyError('Install did not succeed')
            out, err = evidence_command(folder, run['installed_path'], proof)
            apk_path = proof.installed_path(0, out.decode(), err.decode())
            out, err = evidence_command(folder, run['installed_checksum'], proof)
            if proof.installed_digest(0, out.decode(), err.decode(), apk_path) != run['apk_sha256']:
                raise JourneyError('Installed APK identity differs')
            out, err = evidence_command(folder, run['launch'], proof)
            if not proof.launch_ok(0, out.decode()):
                raise JourneyError('No successful launch')
            if len(run['screens']) != len(PLAN) or len(run['transitions']) != len(PLAN) - 1:
                raise JourneyError('Wrong number of screens or transitions')
            collected = []
            run_handoff = None
            anchor = proof.artifact(folder, run['screens'][0]['artifacts']['pid_first']).decode()
            for index, (screen, step) in enumerate(zip(run['screens'], PLAN)):
                name, owner, required, action = step
                if screen.get('name') != name or screen['owner'] != owner:
                    raise JourneyError('Screen order/owner mismatch')
                if any(not item['path'].startswith(run['label'] + '-') for item in screen['artifacts'].values()):
                    raise JourneyError('Cross-run snapshot artifact reuse')
                state = (observed_journey.stable_snapshot(folder, screen, proof, run['label'])
                         if policy is not None else validate_snapshot(folder, screen, proof))
                if policy is not None:
                    terminal = observed_journey.required_surface(folder, screen, required, proof)
                    if terminal is not None:
                        terminal_surfaces.append(terminal)
                else:
                    select(tree(proof.artifact(folder, screen['artifacts']['hierarchy']), owner), owner, required)
                if index:
                    transition = run['transitions'][index - 1]
                    before = transition['before']
                    if any(not item['path'].startswith(run['label'] + '-') for item in before['artifacts'].values()):
                        raise JourneyError('Cross-run input artifact reuse')
                    prior = run['screens'][index - 1]
                    if before['owner'] != prior['owner'] or validate_snapshot(folder, before, proof)[0] != collected[-1][0]:
                        raise JourneyError('UI changed immediately before input')
                    if artifact_path(folder, before['artifacts']['hierarchy'], proof) == artifact_path(
                            folder, prior['artifacts']['hierarchy'], proof):
                        raise JourneyError('Reused stale input precondition')
                    expected_component = None
                    if policy is not None:
                        expected_component = observed_journey.input_identity(
                            folder, prior, before, action, name, proof, run['label'])
                    proof.live_pids(anchor, proof.artifact(folder, before['artifacts']['pid_final']).decode())
                    live = transition['preinput_artifacts']
                    if set(live) != {'pid', 'foreground'} or any(
                            not item['path'].startswith(run['label'] + '-') for item in live.values()):
                        raise JourneyError('Incomplete or cross-run immediate input evidence')
                    observed_paths = {artifact_path(folder, item, proof) for shot in (prior, before)
                                      for item in shot['artifacts'].values()}
                    live_paths = {artifact_path(folder, item, proof) for item in live.values()}
                    if len(live_paths) != 2 or observed_paths.intersection(live_paths):
                        raise JourneyError('Reused stale immediate input evidence')
                    proof.live_pids(anchor, proof.artifact(folder, live['pid']).decode())
                    if not resumed(proof.artifact(folder, live['foreground']).decode(), prior['owner']):
                        raise JourneyError('Expected activity was not foreground immediately before input')
                    if expected_component is not None and observed_journey.component(
                            proof.artifact(folder, live['foreground']), proof) != expected_component:
                        raise JourneyError('Expected component was not foreground immediately before input')
                    age = transition['precondition_age_seconds']
                    if type(age) not in (int, float) or not 0 <= age <= MAX_PRECONDITION_AGE:
                        raise JourneyError('Expired input precondition')
                    expected = ['input', 'keyevent', '4'] if action == 'BACK' else ['input', 'tap', *map(str, target(
                        proof.artifact(folder, before['artifacts']['hierarchy']), before['owner'], action, collected[-1][1], collected[-1][2]))]
                    if transition.get('to') != name or transition.get('action') != action or transition['command']['argv'] != ['shell', shlex.join(expected)]:
                        raise JourneyError('Input command differs from observed plan')
                    evidence_command(folder, transition['command'], proof, clean=True)
                    if policy is not None:
                        observed_journey.verify_preinput(folder, transition, proof)
                        if name == 'reference-promotion':
                            run_handoff = observed_journey.verified_handoff(folder, run, transition, prior, screen, proof)
                            anchor = proof.artifact(folder, screen['artifacts']['pid_first']).decode()
                        elif 'process_handoff' in transition or 'pre_denial_diagnostics' in transition:
                            raise JourneyError('Unplanned process-boundary evidence')
                        if name == 'after-favourite-info':
                            favourite = observed_journey.information_adapter()
                            favourite.verify_installed_guard(folder, transition, run, proof)
                        elif 'pre_ok_installed_identity' in transition:
                            raise JourneyError('Unplanned information-dialog installed-APK guard')
                proof.live_pids(anchor, proof.artifact(folder, screen['artifacts']['pid_final']).decode())
                collected.append(state)
            states.append(collected)
            if policy is not None:
                if run_handoff is None:
                    raise JourneyError('Missing observed notification boundary')
                handoffs.append(run_handoff)
        if policy is not None:
            observed_journey.capture_events(folder, report, proof)
            notification_readiness = observed_journey.readiness_adapter(report['schema'])
            if report['schema'] == notification_readiness.REPORT_SCHEMA:
                result['notification_readiness_observations'] = notification_readiness.verify_report(folder, report, proof)
                result['notification_readiness_policy'] = notification_readiness.POLICY
                if observed_journey.exact_alarm_plan():
                    import exact_alarm_journey
                    result[exact_alarm_journey.POLICY_KEY] = exact_alarm_journey.POLICY
            result['capture_policy'] = policy
            result['process_handoff_outcomes'] = handoffs
            result['process_handoff_outcomes_equal'] = handoffs[0] == handoffs[1]
            result['process_handoff_cause_established'] = all(
                item['cause'] == 'RECORDED_JAVA_FATAL_EXCEPTION' for item in handoffs)
            result['crash_free_run_established'] = False
            result['crash_literal_messages_compared_for_equality'] = False
            result['post_crash_continuation_observed_in_both'] = all(
                item['pid_replaced'] and item['cause'] == 'RECORDED_JAVA_FATAL_EXCEPTION' for item in handoffs)
        result['android_runtime_executed'] = True
        for step, a, b in zip(PLAN, *states):
            same_size = a[1:3] == b[1:3]
            changed = sum(a[3][i:i+4] != b[3][i:i+4] for i in range(0, len(a[3]), 4)) if same_size else None
            result['screens'].append({'name': step[0], 'hierarchy_equal': a[0] == b[0], 'same_size': same_size,
                                      'changed_pixels': changed, 'color_metadata_equal': a[4] == b[4],
                                      'equal': a == b})
        result['journey_equal'] = all(s['equal'] for s in result['screens']) and (not handoffs or handoffs[0] == handoffs[1])
        result['status'] = 'EXACT_EDITOR_JOURNEY_MATCH_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'
        if terminal_surfaces:
            if len(terminal_surfaces) != 2:
                raise JourneyError('Missing paired terminal surface identity')
            result['terminal_surfaces'] = terminal_surfaces
            result['terminal_surface_identities_equal'] = terminal_surfaces[0] == terminal_surfaces[1]
            result['journey_equal'] &= result['terminal_surface_identities_equal']
            result['scope'] = 'Nine observed intro, notification, promotion, home/editor and information-dialog stills; one OK tap and its first app surface only'
            result['catalog_navigation_established'] = False
            result['status'] = 'EXACT_OBSERVED_DIALOG_JOURNEY_MATCH_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'
            if len(PLAN) == 12:
                result['scope'] = 'Observed first-use dialog, trigger catalog and one Date/Time category tap; the resulting app surface only'
                result['catalog_navigation_established'] = True
                result['trigger_selected'] = False
                result['status'] = 'EXACT_TRIGGER_CATEGORY_OBSERVATION_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'
            elif len(PLAN) == 13:
                result['scope'] = 'Observed first-use dialog, trigger catalog, Date/Time category and one Day/Time trigger-type tap; the resulting app surface only'
                result['catalog_navigation_established'] = True
                result['trigger_type_tapped'] = True
                result['trigger_configuration_confirmed'] = False
                result['status'] = 'EXACT_DAY_TIME_TRIGGER_OBSERVATION_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'
            elif observed_journey.exact_alarm_plan():
                result['scope'] = 'Observed Day/Time exact-alarm explanation, one observed OK tap and the resulting Settings surface only'
                result['catalog_navigation_established'] = True
                result['trigger_type_tapped'] = True
                result['exact_alarm_explanation_ok_tapped'] = True
                result['settings_navigation_observed'] = True
                result['settings_inputs'] = 0
                result['permission_granted'] = False
                result['trigger_configuration_confirmed'] = False
                result['status'] = 'EXACT_ALARM_SETTINGS_OBSERVATION_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'
        if result['journey_equal'] and result.get('post_crash_continuation_observed_in_both'):
            result['status'] = 'MATCHED_POST_CRASH_CONTINUATION_ONLY'
        result['apk_sha256'] = [r['apk_sha256'] for r in runs]
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError, ET.ParseError) as exc:
        result['reason'] = str(exc)
    return result

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--original', type=Path, required=True)
    ap.add_argument('--candidate', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--serial', required=True)
    ap.add_argument('--accept-package-data-removal', action='store_true')
    ap.add_argument('--observe-denial-handoff', action='store_true')
    ap.add_argument('--settle-full-frames', action='store_true')
    ap.add_argument('--observe-notification-readiness', action='store_true')
    args = ap.parse_args()
    import observed_journey
    if observed_journey.exact_alarm_plan() and not args.observe_notification_readiness:
        ap.error('Exact-alarm navigation requires --observe-notification-readiness')
    if args.observe_denial_handoff != args.settle_full_frames:
        ap.error('The observed policy requires both --observe-denial-handoff and --settle-full-frames')
    if args.observe_notification_readiness and not args.observe_denial_handoff:
        ap.error('Notification readiness requires the existing denial handoff and full-frame policy')
    if any(step[2] is None for step in PLAN) and not args.observe_denial_handoff:
        ap.error('The information-dialog adapter requires --observe-denial-handoff and --settle-full-frames')
    sys.path.insert(0, str(args.source.resolve()))
    import android_compare as proof
    from android_acceptance import prevalidate_pair
    args.output.mkdir(parents=True, exist_ok=False)
    report = {'schema': SCHEMA, 'plan_sha256': fingerprint(PLAN), 'plan': PLAN, 'runs': [], 'status': 'INCOMPLETE'}
    if args.observe_denial_handoff:
        import observed_journey
        report.update(schema=observed_journey.REPORT_SCHEMA, capture_policy=observed_journey.POLICY, capture_events=[])
    if args.observe_notification_readiness:
        notification_readiness = observed_journey.readiness_adapter()
        notification_readiness.require_plan()
        report.update(schema=notification_readiness.REPORT_SCHEMA,
                      notification_readiness_policy=notification_readiness.POLICY)
        if observed_journey.exact_alarm_plan():
            import exact_alarm_journey
            report[exact_alarm_journey.POLICY_KEY] = exact_alarm_journey.POLICY
    def save():
        (args.output / 'journey.json').write_text(json.dumps(report, indent=2) + '\n')
    save()
    try:
        if not args.accept_package_data_removal:
            raise JourneyError('Explicit package data removal acceptance required')
        pair = prevalidate_pair(args.original.resolve(), args.candidate.resolve())
        recorder = Recorder(args.output, args.serial, proof)
        if args.observe_denial_handoff:
            observed_journey.require_plan()
            recorder.capture_policy = observed_journey.POLICY
        props = recorder.environment()
        if props['ro.build.version.sdk'] != '35' or props['ro.kernel.qemu'] != '1' or 'arm64-v8a' not in props['ro.product.cpu.abilist'].split(','):
            raise JourneyError('Only an explicitly selected ARM64-capable emulator is allowed')
        for entry in pair:
            run = {'label': entry['label'], 'apk_sha256': entry['apk_sha256'], 'screens': [], 'transitions': [], 'status': 'INCOMPLETE'}
            report['runs'].append(run)
            try:
                run['environment'] = recorder.environment()
                if hashlib.sha256(Path(entry['path']).read_bytes()).hexdigest() != entry['apk_sha256']:
                    raise JourneyError('APK changed since preflight')
                recorder.cmd(['uninstall', PACKAGE])
                run['absence'], out, err = recorder.shell(['pm', 'path', PACKAGE])
                if not proof.absence_ok(run['absence']['returncode'], out.decode(), err.decode()):
                    raise JourneyError('Package removal failed')
                run['install'], out, err = recorder.cmd(['install', '--no-streaming', entry['path']], 600)
                if not proof.install_ok(run['install']['returncode'], out.decode(), err.decode()):
                    raise JourneyError('APK installation failed')
                run['installed_path'], out, err = recorder.shell(['pm', 'path', PACKAGE])
                installed = proof.installed_path(run['installed_path']['returncode'], out.decode(), err.decode())
                run['installed_checksum'], out, err = recorder.shell(['sha256sum', installed])
                if proof.installed_digest(run['installed_checksum']['returncode'], out.decode(), err.decode(), installed) != entry['apk_sha256']:
                    raise JourneyError('Installed APK checksum differs')
                resolved = recorder.ok(['cmd', 'package', 'resolve-activity', '--brief', '-a', 'android.intent.action.MAIN', '-c', 'android.intent.category.LAUNCHER', '-p', PACKAGE]).decode()
                components = re.findall(re.escape(PACKAGE) + r'/[A-Za-z0-9_.$]+', resolved)
                if len(components) != 1:
                    raise JourneyError('Ambiguous launcher')
                run['launch'], out, err = recorder.shell(['am', 'start', '-W', '-n', components[0]], 180)
                if not proof.launch_ok(run['launch']['returncode'], out.decode()):
                    raise JourneyError('Launch failed')
                time.sleep(4)
                for index, (name, owner, required, action) in enumerate(PLAN):
                    run['current_step'] = name
                    if action:
                        previous = run['screens'][-1]
                        run['transitions'].append(capture_transition(
                            recorder, previous, entry['label'] + '-' + name, name, action, proof, run))
                        time.sleep(2)
                        if args.observe_notification_readiness and name == 'reference-promotion':
                            notification_readiness.observe(recorder, run, run['transitions'][-1], previous)
                    shot = (observed_journey.capture(recorder, entry['label'] + '-' + name, owner)
                            if args.observe_denial_handoff else recorder.snapshot(entry['label'] + '-' + name, owner))
                    shot['name'] = name
                    run['screens'].append(shot)
                    if args.observe_denial_handoff:
                        observed_journey.required_surface(args.output, shot, required, proof)
                    else:
                        select(tree(proof.artifact(args.output, shot['artifacts']['hierarchy']), owner), owner, required)
                    if args.observe_denial_handoff and name == 'reference-promotion':
                        observed_journey.observe_handoff(recorder, run, run['transitions'][-1], run['screens'][-2], shot)
                    save()
                run['environment_after'] = recorder.environment()
                run['status'] = 'COMPLETE'
            except (ValueError, OSError, subprocess.SubprocessError) as exc:
                run['reason'] = str(exc)
                run['status'] = 'FAILED'
            report['commands'] = recorder.log
            if args.observe_denial_handoff:
                report['capture_events'] = recorder.capture_events
            save()
        report['status'] = 'RECORDED_NOT_PARITY'
    except (ValueError, OSError, RuntimeError, subprocess.SubprocessError) as exc:
        report['reason'] = str(exc)
    finally:
        save()
    result = compare(args.output, report, proof)
    (args.output / 'comparison.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['journey_equal'] else 2

if __name__ == '__main__':
    raise SystemExit(main())
