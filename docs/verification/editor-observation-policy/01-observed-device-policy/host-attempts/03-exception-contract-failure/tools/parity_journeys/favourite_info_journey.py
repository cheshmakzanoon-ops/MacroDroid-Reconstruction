#!/usr/bin/env python3
"""Observe the supplied APK's Favourite Triggers dialog, tap OK once, then stop.

The earlier 13/14-step plans remain unchanged. This opt-in ten-screen plan records
the actual first app surface after OK; it does not assume a trigger catalog or
issue another input. A matched continuation may include a recorded shared crash.
"""
from __future__ import annotations

from contextlib import contextmanager
import copy
import json
import re

import editor_journey as runner
import observed_journey as observed
import supplied_reference_journey as reference

REFERENCE_PLAN_SHA256 = '69bae4f2af8e2f14c407808dbcdea91cdca009af2ae390e13b5c7fbf035a3065'
EDITOR = runner.PACKAGE + '/' + runner.PACKAGE + '.editscreen.EditMacroActivity'
TITLE = {'resource-id': runner.PACKAGE + ':id/alertTitle', 'text': 'Favourite Triggers'}
OK = {'resource-id': 'android:id/button1', 'text': 'OK'}
# The parsed UIAutomator message contains two actual newline characters.
MESSAGE = ('You can now long press on the + button to display quick tiles for your favourite items.\n\n'
           'The set of quick tiles displayed can be edited and tailored to your needs using the wrench icon.')


def expected_plan():
    baseline = json.loads(reference.PLAN_PATH.read_text())
    if runner.fingerprint(baseline) != REFERENCE_PLAN_SHA256:
        raise runner.JourneyError('Reviewed reference plan changed; review the information-dialog adapter')
    return copy.deepcopy(baseline[:8]) + [
        ['favourite-triggers-info', runner.PACKAGE, TITLE, runner.TRIGGER],
        ['after-favourite-info', runner.PACKAGE, None, OK],
    ]


def require_plan():
    if runner.fingerprint(runner.PLAN) != runner.fingerprint(expected_plan()):
        raise runner.JourneyError('Information-dialog plan differs from the reviewed single-OK sequence')


@contextmanager
def configured_plan():
    with reference.configured_plan():
        previous = runner.PLAN
        try:
            runner.PLAN = expected_plan()
            yield runner.PLAN
        finally:
            runner.PLAN = previous


def dialog_identity(folder, shot, proof):
    require_plan()
    if shot['owner'] != runner.PACKAGE:
        raise runner.JourneyError('Information dialog has an unexpected owner')
    for key in ['foreground', 'foreground_final']:
        if observed.component(proof.artifact(folder, shot['artifacts'][key]), proof) != EDITOR:
            raise runner.JourneyError('Information dialog is not on EditMacroActivity')
    data = proof.artifact(folder, shot['artifacts']['hierarchy'])
    root = runner.tree(data, runner.PACKAGE)
    title = runner.select(root, runner.PACKAGE, TITLE)
    message = runner.select(root, runner.PACKAGE, {'resource-id': 'android:id/message'})
    # Select by ID alone first so a duplicate button with different text fails.
    button = runner.select(root, runner.PACKAGE, {'resource-id': 'android:id/button1'})
    if (title.get('class') != 'android.widget.TextView' or title.get('enabled') != 'true'
            or message.get('class') != 'android.widget.TextView' or message.get('enabled') != 'true'
            or message.get('text') != MESSAGE or button.get('text') != 'OK'
            or button.get('class') != 'android.widget.Button' or button.get('clickable') != 'true'
            or button.get('enabled') != 'true'):
        raise runner.JourneyError('Observed Favourite Triggers title, message or unique OK button changed')
    width, height, _ = proof.png_pixels(proof.artifact(folder, shot['artifacts']['screenshot']))
    return runner.target(data, runner.PACKAGE, OK, width, height)


def terminal_surface(folder, shot, proof):
    require_plan()
    if shot.get('name') != 'after-favourite-info' or shot['owner'] != runner.PACKAGE:
        raise runner.JourneyError('Unexpected terminal app capture')
    component = observed.component(proof.artifact(folder, shot['artifacts']['foreground_final']), proof)
    if component.split('/', 1)[0] != runner.PACKAGE:
        raise runner.JourneyError('Terminal surface belongs to another package')
    return {'name': shot['name'], 'owner': runner.PACKAGE, 'component': component,
            'surface_after_one_observed_ok': True, 'subsequent_inputs': 0}


def checked_installed(folder, records, run, proof):
    if list(records) != ['installed_path', 'installed_checksum'] or not re.fullmatch('[0-9a-f]{64}', run['apk_sha256']):
        raise runner.JourneyError('Incomplete installed-APK guard before OK')
    out = observed.checked_command(folder, records['installed_path'], ['pm', 'path', runner.PACKAGE], proof)
    path = proof.installed_path(0, out.decode(), '')
    old_out, old_err = runner.evidence_command(folder, run['installed_path'], proof)
    if path != proof.installed_path(0, old_out.decode(), old_err.decode()):
        raise runner.JourneyError('Installed APK path changed before OK')
    digest = observed.checked_command(folder, records['installed_checksum'], ['sha256sum', path], proof)
    if proof.installed_digest(0, digest.decode(), '', path) != run['apk_sha256']:
        raise runner.JourneyError('Installed APK identity changed before OK')


def installed_guard(recorder, run):
    if run is None:
        raise runner.JourneyError('Missing exact run identity before OK')
    records = {}
    records['installed_path'], out, err = recorder.shell(['pm', 'path', runner.PACKAGE])
    path = recorder.proof.installed_path(records['installed_path']['returncode'], out.decode(), err.decode())
    records['installed_checksum'] = recorder.shell(['sha256sum', path])[0]
    checked_installed(recorder.folder, records, run, recorder.proof)
    return records


def verify_installed_guard(folder, transition, run, proof):
    require_plan()
    if transition['to'] != 'after-favourite-info' or transition['action'] != OK:
        raise runner.JourneyError('Installed-APK OK guard has the wrong boundary')
    records = transition['pre_ok_installed_identity']
    checked_installed(folder, records, run, proof)
    start = transition['observation_started_monotonic']
    finish = json.loads(proof.artifact(folder, transition['before']['settling']))['started_monotonic']
    used = {runner.artifact_path(folder, item, proof)
            for command in [run['installed_path'], run['installed_checksum'],
                            *transition['preinput_commands'].values(), transition['command']]
            for item in [command['stdout'], command['stderr']]}
    for command in records.values():
        if not start <= command['started_monotonic'] <= command['finished_monotonic'] <= finish:
            raise runner.JourneyError('Installed-APK OK guard is stale or unordered')
        start = command['finished_monotonic']
        paths = {runner.artifact_path(folder, command[key], proof) for key in ['stdout', 'stderr']}
        if len(paths) != 2 or used & paths:
            raise runner.JourneyError('Installed-APK OK guard reused earlier command output')
        used |= paths


def main():
    with configured_plan():
        return runner.main()


if __name__ == '__main__':
    raise SystemExit(main())
