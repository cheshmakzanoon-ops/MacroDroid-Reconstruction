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
from pathlib import Path

PACKAGE = 'com.arlosoft.macrodroid'
PERMISSION = 'com.google.android.permissioncontroller'
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

class Recorder:
    def __init__(self, folder, serial, proof):
        self.folder, self.serial, self.proof = folder, serial, proof
        self.adb = shutil.which('adb')
        if not self.adb:
            raise JourneyError('ADB unavailable')
        self.count = 0
        self.log = []
    def save(self, name, data):
        (self.folder / name).write_bytes(data)
        return {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    def cmd(self, args, timeout=120):
        self.count += 1
        name = f'command-{self.count:05}'
        p = subprocess.run([self.adb, '-s', self.serial, *args], capture_output=True, timeout=timeout)
        item = {'argv': args, 'returncode': p.returncode,
                'stdout': self.save(name + '.stdout', p.stdout),
                'stderr': self.save(name + '.stderr', p.stderr)}
        self.log.append(item)
        return item, p.stdout, p.stderr
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
        a['pid_final'] = self.save(label + '-pid-final.txt', self.ok(['pidof', PACKAGE]))
        result = {'owner': owner, 'artifacts': a, 'sample_interval_seconds': time.monotonic() - started}
        # Persist even an unexpected screen as diagnostic evidence before validation.
        self.save(label + '-snapshot.json', json.dumps(result, indent=2).encode())
        validate_snapshot(self.folder, result, self.proof)
        return result

def validate_snapshot(folder, shot, proof):
    a = shot['artifacts']
    if shot['owner'] not in (PACKAGE, PERMISSION) or not proof.valid_live_interval(shot['sample_interval_seconds']):
        raise JourneyError('Invalid snapshot owner or live interval')
    proof.live_pids(proof.artifact(folder, a['pid_first']).decode(), proof.artifact(folder, a['pid_final']).decode())
    if not resumed(proof.artifact(folder, a['foreground']).decode(), shot['owner']):
        raise JourneyError('Expected activity is not resumed')
    data = proof.artifact(folder, a['hierarchy'])
    root = tree(data, shot['owner'])
    png = proof.artifact(folder, a['screenshot'])
    width, height, pixels = proof.png_pixels(png)
    return canonical(root), width, height, pixels, proof.color_metadata(png)

def compare(folder, report, proof):
    result = {'status': 'REJECTED', 'journey_equal': False, 'full_runtime_1_to_1_established': False,
              'scope': 'Fresh install, notification denial, home and empty-editor catalog navigation only',
              'screens': [], 'masks_used': False, 'android_runtime_executed': False, 'macros_executed': False, 'macros_saved': False}
    try:
        if report.get('schema') != 1 or report.get('plan_sha256') != fingerprint(PLAN) or report.get('status') != 'RECORDED_NOT_PARITY':
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
            anchor = proof.artifact(folder, run['screens'][0]['artifacts']['pid_first']).decode()
            for index, (screen, step) in enumerate(zip(run['screens'], PLAN)):
                name, owner, required, action = step
                if screen.get('name') != name or screen['owner'] != owner:
                    raise JourneyError('Screen order/owner mismatch')
                if any(not item['path'].startswith(run['label'] + '-') for item in screen['artifacts'].values()):
                    raise JourneyError('Cross-run snapshot artifact reuse')
                state = validate_snapshot(folder, screen, proof)
                select(tree(proof.artifact(folder, screen['artifacts']['hierarchy']), owner), owner, required)
                proof.live_pids(anchor, proof.artifact(folder, screen['artifacts']['pid_final']).decode())
                if index:
                    transition = run['transitions'][index - 1]
                    before = transition['before']
                    if any(not item['path'].startswith(run['label'] + '-') for item in before['artifacts'].values()):
                        raise JourneyError('Cross-run input artifact reuse')
                    prior = run['screens'][index - 1]
                    if before['owner'] != prior['owner'] or validate_snapshot(folder, before, proof)[0] != collected[-1][0]:
                        raise JourneyError('UI changed immediately before input')
                    if before['artifacts']['hierarchy']['path'] == prior['artifacts']['hierarchy']['path']:
                        raise JourneyError('Reused stale input precondition')
                    proof.live_pids(anchor, proof.artifact(folder, before['artifacts']['pid_final']).decode())
                    age = transition['precondition_age_seconds']
                    if type(age) not in (int, float) or not 0 <= age <= 15:
                        raise JourneyError('Expired input precondition')
                    expected = ['input', 'keyevent', '4'] if action == 'BACK' else ['input', 'tap', *map(str, target(
                        proof.artifact(folder, before['artifacts']['hierarchy']), before['owner'], action, collected[-1][1], collected[-1][2]))]
                    if transition.get('to') != name or transition.get('action') != action or transition['command']['argv'] != ['shell', shlex.join(expected)]:
                        raise JourneyError('Input command differs from observed plan')
                    evidence_command(folder, transition['command'], proof, clean=True)
                collected.append(state)
            states.append(collected)
        result['android_runtime_executed'] = True
        for step, a, b in zip(PLAN, *states):
            same_size = a[1:3] == b[1:3]
            changed = sum(a[3][i:i+4] != b[3][i:i+4] for i in range(0, len(a[3]), 4)) if same_size else None
            result['screens'].append({'name': step[0], 'hierarchy_equal': a[0] == b[0], 'same_size': same_size,
                                      'changed_pixels': changed, 'color_metadata_equal': a[4] == b[4],
                                      'equal': a == b})
        result['journey_equal'] = all(s['equal'] for s in result['screens'])
        result['status'] = 'EXACT_EDITOR_JOURNEY_MATCH_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'
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
    args = ap.parse_args()
    sys.path.insert(0, str(args.source.resolve()))
    import android_compare as proof
    from android_acceptance import prevalidate_pair
    args.output.mkdir(parents=True, exist_ok=False)
    report = {'schema': 1, 'plan_sha256': fingerprint(PLAN), 'plan': PLAN, 'runs': [], 'status': 'INCOMPLETE'}
    def save():
        (args.output / 'journey.json').write_text(json.dumps(report, indent=2) + '\n')
    save()
    try:
        if not args.accept_package_data_removal:
            raise JourneyError('Explicit package data removal acceptance required')
        pair = prevalidate_pair(args.original.resolve(), args.candidate.resolve())
        recorder = Recorder(args.output, args.serial, proof)
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
                        before = recorder.snapshot(entry['label'] + '-' + name + '-before', previous['owner'])
                        proof.live_pids(proof.artifact(args.output, previous['artifacts']['pid_final']).decode(),
                                        proof.artifact(args.output, before['artifacts']['pid_final']).decode())
                        fresh = time.monotonic()
                        prior_state = validate_snapshot(args.output, previous, proof)
                        if validate_snapshot(args.output, before, proof)[0] != prior_state[0]:
                            raise JourneyError('UI changed before action')
                        argv = ['input', 'keyevent', '4'] if action == 'BACK' else ['input', 'tap', *map(str, target(
                            proof.artifact(args.output, before['artifacts']['hierarchy']), previous['owner'], action, prior_state[1], prior_state[2]))]
                        age = time.monotonic() - fresh
                        if age > 15:
                            raise JourneyError('Input precondition expired')
                        cmd, out, err = recorder.shell(argv)
                        run['transitions'].append({'to': name, 'action': action, 'before': before, 'precondition_age_seconds': age, 'command': cmd})
                        if cmd['returncode'] or out.strip() or err.strip():
                            raise JourneyError('Input did not complete cleanly')
                        time.sleep(2)
                    shot = recorder.snapshot(entry['label'] + '-' + name, owner)
                    shot['name'] = name
                    run['screens'].append(shot)
                    select(tree(proof.artifact(args.output, shot['artifacts']['hierarchy']), owner), owner, required)
                    save()
                run['environment_after'] = recorder.environment()
                run['status'] = 'COMPLETE'
            except (ValueError, OSError, subprocess.SubprocessError) as exc:
                run['reason'] = str(exc)
                run['status'] = 'FAILED'
            report['commands'] = recorder.log
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
