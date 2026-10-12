"""Independent home-to-editor evidence, not a replacement for cold-start acceptance.

The declared scope starts at the observed home screen AFTER onboarding. A crash
before that boundary stays in the original report and cannot become a startup pass.
All full-frame pixels, UI attributes, input evidence and in-scope PIDs are checked.
"""
from __future__ import annotations
import json
import math
import re
import shlex
import time
import zlib
import xml.etree.ElementTree as ET
from pathlib import Path
import editor_journey as runner
from robust_capture import EvidenceRecorder

HOME_CLASS = runner.PACKAGE + '.homescreen.NewHomeScreenActivity'
END = 'editor-after-constraint-back'


def component(data: bytes, proof) -> str:
    values = proof.resumed_components(data.decode())
    if len(values) != 1:
        raise runner.JourneyError('Session evidence lacks one resumed component')
    package, activity = values[0].split('/', 1)
    return package + '/' + (package + activity if activity.startswith('.') else activity)


def claim_artifacts(folder, records, proof, seen, label=None):
    """A distinct semantic observation cannot reuse any earlier resolved file."""
    paths = [runner.artifact_path(folder, record, proof) for record in records]
    if len(set(paths)) != len(paths) or seen.intersection(paths):
        raise runner.JourneyError('Reused session artifact, including a resolved path alias')
    if label is not None and any(
            not path.relative_to(folder.resolve()).as_posix().startswith(label + '-') for path in paths):
        raise runner.JourneyError('Cross-run resolved session artifact')
    seen.update(paths)


def command_window(item):
    def finite(value):
        return type(value) in (int, float) and math.isfinite(value)
    start, finish, timeout = (item.get(key) for key in
                              ('started_monotonic', 'finished_monotonic', 'timeout_seconds'))
    if (not all(finite(value) for value in (start, finish, timeout))
            or start < 0 or not start <= finish or timeout <= 0 or finish - start > timeout
            or item.get('timed_out') is not False):
        raise runner.JourneyError('Invalid or timed-out session command timing')
    return start, finish


def observation_window(shot):
    observed = shot['session_observation']
    start, finish = observed.get('started_monotonic'), observed.get('finished_monotonic')
    interval = shot['sample_interval_seconds']
    if (observed.get('schema') != 1
            or any(type(value) not in (int, float) or not math.isfinite(value)
                   for value in (start, finish, interval))
            or start < 0 or finish <= start or interval <= 0 or finish - start < interval):
        raise runner.JourneyError('Invalid session capture observation interval')
    return start, finish


def home_foreground(data: bytes, proof) -> bool:
    components = proof.resumed_components(data.decode())
    expected = {runner.PACKAGE + '/' + HOME_CLASS,
                runner.PACKAGE + '/.homescreen.NewHomeScreenActivity'}
    return len(components) == 1 and components[0] in expected


class SessionRecorder(EvidenceRecorder):
    """Bind both endpoints of the independently declared editor session to the APK."""
    def snapshot(self, label, owner):
        started = time.monotonic()
        shot = super().snapshot(label, owner)
        shot['session_observation'] = {'schema': 1, 'started_monotonic': started,
                                       'finished_monotonic': time.monotonic()}
        self.save(label + '-session-observation.json', (json.dumps(shot, indent=2) + '\n').encode())
        if not any(label.endswith('-' + name) for name in ('home', END)):
            return shot
        context = {'environment': self.environment()}
        def command(name, args):
            item, out, err = self.shell(args)
            item = dict(item)
            item['stdout'] = self.save(label + '-identity-' + name + '.stdout', out)
            item['stderr'] = self.save(label + '-identity-' + name + '.stderr', err)
            context[name] = item
            runner.evidence_command(self.folder, item, self.proof)
            return out, err
        out, err = command('package_path', ['pm', 'path', runner.PACKAGE])
        path = self.proof.installed_path(0, out.decode(), err.decode())
        out, err = command('checksum', ['sha256sum', path])
        self.proof.installed_digest(0, out.decode(), err.decode(), path)
        out, _ = command('pid', ['pidof', runner.PACKAGE])
        self.proof.live_pids(self.proof.artifact(self.folder, shot['artifacts']['pid_final']).decode(), out.decode())
        out, _ = command('foreground', ['dumpsys', 'activity', 'activities'])
        if (not runner.resumed(out.decode(), owner)
                or component(out, self.proof) != component(
                    self.proof.artifact(self.folder, shot['artifacts']['foreground']), self.proof)):
            raise runner.JourneyError('Session endpoint lost its captured foreground component')
        shot['session_identity'] = context
        self.save(label + '-session-identity.json', (json.dumps(context, indent=2) + '\n').encode())
        return shot


def checked_identity(folder, run, shot, proof, seen=None):
    if seen is None:
        seen = set()
    identity = shot['session_identity']
    if identity['environment'] != run['environment']:
        raise runner.JourneyError('Session endpoint environment changed')
    capture_finish = observation_window(shot)[1]
    windows = []
    def read(name, argv):
        item = identity[name]
        if item['argv'] != ['shell', shlex.join(argv)]:
            raise runner.JourneyError('Session identity command differs')
        for record in (item['stdout'], item['stderr']):
            if not record['path'].startswith(run['label'] + '-'):
                raise runner.JourneyError('Cross-run identity evidence')
        claim_artifacts(folder, [item['stdout'], item['stderr']], proof, seen, run['label'])
        window = command_window(item)
        if window[0] < capture_finish:
            raise runner.JourneyError('Session endpoint command precedes its captured observation')
        if windows and windows[-1][1] > window[0]:
            raise runner.JourneyError('Session endpoint commands are out of order')
        windows.append(window)
        return runner.evidence_command(folder, item, proof)
    out, err = read('package_path', ['pm', 'path', runner.PACKAGE])
    path = proof.installed_path(0, out.decode(), err.decode())
    out, err = read('checksum', ['sha256sum', path])
    if proof.installed_digest(0, out.decode(), err.decode(), path) != run['apk_sha256']:
        raise runner.JourneyError('Session endpoint APK differs from the intended input')
    out, err = read('pid', ['pidof', runner.PACKAGE])
    if err.strip():
        raise runner.JourneyError('Session PID command had stderr')
    proof.live_pids(proof.artifact(folder, shot['artifacts']['pid_final']).decode(), out.decode())
    out, err = read('foreground', ['dumpsys', 'activity', 'activities'])
    if err.strip() or not runner.resumed(out.decode(), runner.PACKAGE):
        raise runner.JourneyError('Session endpoint is no longer foreground')
    if component(out, proof) != component(proof.artifact(folder, shot['artifacts']['foreground']), proof):
        raise runner.JourneyError('Session endpoint differs from its captured foreground component')
    if shot['name'] == 'home' and not home_foreground(out, proof):
        raise runner.JourneyError('Session did not start in the observed home activity')
    return windows[0][0], windows[-1][1]


def checked_transition(folder, run, prior, transition, step, anchor, prior_state, proof, seen, earliest):
    name, owner, required, action = step
    before = transition['before']
    if before['owner'] != prior['owner'] or any(
            not record['path'].startswith(run['label'] + '-') for record in before['artifacts'].values()):
        raise runner.JourneyError('Wrong transition owner or cross-run artifacts')
    claim_artifacts(folder, before['artifacts'].values(), proof, seen, run['label'])
    before_window = observation_window(before)
    if runner.validate_snapshot(folder, before, proof)[0] != prior_state[0]:
        raise runner.JourneyError('UI changed before the scoped input')
    proof.live_pids(anchor, proof.artifact(folder, before['artifacts']['pid_final']).decode())
    if runner.artifact_path(folder, before['artifacts']['hierarchy'], proof) == runner.artifact_path(
            folder, prior['artifacts']['hierarchy'], proof):
        raise runner.JourneyError('Reused input hierarchy')
    live = transition['preinput_artifacts']
    if set(live) != {'pid', 'foreground'} or any(
            not record['path'].startswith(run['label'] + '-') for record in live.values()):
        raise runner.JourneyError('Missing or cross-run immediate input evidence')
    claim_artifacts(folder, live.values(), proof, seen, run['label'])
    previous_paths = {runner.artifact_path(folder, record, proof) for shot in (prior, before)
                      for record in shot['artifacts'].values()}
    live_paths = {runner.artifact_path(folder, record, proof) for record in live.values()}
    if len(live_paths) != 2 or live_paths.intersection(previous_paths):
        raise runner.JourneyError('Reused immediate input artifacts')
    proof.live_pids(anchor, proof.artifact(folder, live['pid']).decode())
    if not runner.resumed(proof.artifact(folder, live['foreground']).decode(), prior['owner']):
        raise runner.JourneyError('Wrong foreground immediately before input')
    age = transition['precondition_age_seconds']
    if type(age) not in (int, float) or not 0 <= age <= runner.MAX_PRECONDITION_AGE:
        raise runner.JourneyError('Scoped input precondition expired')
    expected = ['input', 'keyevent', '4'] if action == 'BACK' else ['input', 'tap', *map(str, runner.target(
        proof.artifact(folder, before['artifacts']['hierarchy']), prior['owner'], action,
        prior_state[1], prior_state[2]))]
    if transition['to'] != name or transition['action'] != action or transition['command']['argv'] != ['shell', shlex.join(expected)]:
        raise runner.JourneyError('Scoped input command does not match its observed target')
    claim_artifacts(folder, [transition['command'][key] for key in ('stdout', 'stderr')], proof, seen)
    start, finish = command_window(transition['command'])
    if start - age < earliest:
        raise runner.JourneyError('Session input acquisition precedes the previous boundary or input')
    if (before_window[0] < max(earliest, observation_window(prior)[1])
            or not before_window[1] <= start
            or not 0 <= start - before_window[0] <= runner.MAX_PRECONDITION_AGE):
        raise runner.JourneyError('Session pre-input capture timing is stale or out of order')
    runner.evidence_command(folder, transition['command'], proof, clean=True)
    return finish


def compare_session(folder: Path, report: dict, plan: list, proof) -> dict:
    result = {'schema': 2, 'status': 'REJECTED', 'editor_session_equal': False,
              'evidence_policy': 'Distinct session observations with ordered captures, inputs and endpoints',
              'scope': 'Observed home through empty-editor catalog navigation, AFTER onboarding only',
              'scope_start': 'home', 'scope_end': END, 'startup_parity_established': False,
              'full_runtime_1_to_1_established': False, 'masks_used': False,
              'macros_saved': False, 'macros_executed': False, 'screens': []}
    try:
        names = [step[0] for step in plan]
        if names.count('home') != 1 or names[-1] != END or len(set(names)) != len(names):
            raise runner.JourneyError('Invalid session plan boundary')
        start = names.index('home')
        if (report['schema'] != runner.SCHEMA or report['status'] != 'RECORDED_NOT_PARITY'
                or report['plan_sha256'] != runner.fingerprint(plan) or report['plan'] != plan):
            raise runner.JourneyError('Report is not bound to the declared plan')
        runs = report['runs']
        if len(runs) != 2 or [run['label'] for run in runs] != ['original', 'candidate']:
            raise runner.JourneyError('Two ordered variants required')
        if runs[0]['apk_sha256'] != proof.ORIGINAL_SHA256 or not re.fullmatch('[0-9a-f]{64}', runs[1]['apk_sha256']) or runs[1]['apk_sha256'] == runs[0]['apk_sha256']:
            raise runner.JourneyError('Wrong reference or candidate identity')
        required = {'serial', 'display_size', 'display_density', *runner.PROPERTIES,
                    *(namespace + ':' + name for namespace, name in runner.SETTINGS)}
        env = runs[0]['environment']
        if (env != runs[1]['environment'] or set(env) != required or not env['serial']
                or env['ro.kernel.qemu'] != '1' or env['ro.build.version.sdk'] != '35'
                or 'arm64-v8a' not in env['ro.product.cpu.abilist'].split(',')):
            raise runner.JourneyError('Unsupported or unequal environments')
        states = []
        # Share resolved identities across both variants and every session role.
        # Equal bytes in distinct fresh files are valid; one file reused is not.
        seen = set()
        for run in runs:
            if run['status'] != 'COMPLETE' or run['environment_after'] != env:
                raise runner.JourneyError('Incomplete run or changed environment')
            if [s['name'] for s in run['screens']] != names or len(run['transitions']) != len(plan) - 1:
                raise runner.JourneyError('Incomplete or reordered capture sequence')
            initial_window = checked_identity(folder, run, run['screens'][start], proof, seen)
            final_window = checked_identity(folder, run, run['screens'][-1], proof, seen)
            home = run['screens'][start]
            if not home_foreground(proof.artifact(folder, home['artifacts']['foreground']), proof):
                raise runner.JourneyError('Home foreground is not the observed landing activity')
            anchor = proof.artifact(folder, home['artifacts']['pid_first']).decode()
            series = []
            previous_finish = initial_window[1]
            for index in range(start, len(plan)):
                shot, step = run['screens'][index], plan[index]
                if shot['owner'] != runner.PACKAGE or step[1] != runner.PACKAGE:
                    raise runner.JourneyError('Wrong editor screen owner')
                if any(not r['path'].startswith(run['label'] + '-') for r in shot['artifacts'].values()):
                    raise runner.JourneyError('Cross-run editor artifacts')
                claim_artifacts(folder, shot['artifacts'].values(), proof, seen, run['label'])
                state = runner.validate_snapshot(folder, shot, proof)
                capture_window = observation_window(shot)
                runner.select(runner.tree(proof.artifact(folder, shot['artifacts']['hierarchy']), shot['owner']), shot['owner'], step[2])
                proof.live_pids(anchor, proof.artifact(folder, shot['artifacts']['pid_final']).decode())
                if index > start:
                    previous_finish = checked_transition(
                        folder, run, run['screens'][index - 1], run['transitions'][index - 1],
                        step, anchor, series[-1], proof, seen, previous_finish)
                    if capture_window[0] < previous_finish:
                        raise runner.JourneyError('Session result capture began before its input finished')
                series.append(state)
            if final_window[0] < previous_finish:
                raise runner.JourneyError('Final session identity precedes the final input')
            states.append(series)
        for step, left, right in zip(plan[start:], *states):
            same_size = left[1:3] == right[1:3]
            changes = sum(left[3][i:i+4] != right[3][i:i+4] for i in range(0, len(left[3]), 4)) if same_size else None
            result['screens'].append({'name': step[0], 'equal': left == right, 'changed_pixels': changes,
                                      'hierarchy_equal': left[0] == right[0], 'same_size': same_size,
                                      'color_metadata_equal': left[4] == right[4]})
        result['editor_session_equal'] = all(s['equal'] for s in result['screens'])
        result['status'] = 'EXACT_POST_ONBOARDING_EDITOR_MATCH_ONLY' if result['editor_session_equal'] else 'EDITOR_SESSION_DIFFERENCE'
        result['apk_sha256'] = [r['apk_sha256'] for r in runs]
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError, ET.ParseError, zlib.error) as error:
        result['reason'] = str(error)
    return result


def main() -> int:
    """Read-only replay; never edit either the APKs or the original comparison."""
    import argparse
    import hashlib
    import sys
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--journey', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.source.resolve()))
    import android_compare as proof
    from supplied_reference_journey import load_plan
    raw = args.journey.read_bytes()
    result = compare_session(args.journey.parent, json.loads(raw), load_plan(), proof)
    result['journey_document_sha256'] = hashlib.sha256(raw).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(result, indent=2))
    return 0 if result['editor_session_equal'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
