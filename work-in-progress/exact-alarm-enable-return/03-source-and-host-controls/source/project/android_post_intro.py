#!/usr/bin/env python3
"""Capture and compare the first surface after one observed intro completion tap.

Only the final CONSTRAINTS page's observed Next button can be pressed. No
permission, dialog, or landing-screen control is activated. Unknown surfaces
are preserved as failed captures, never accepted as application home parity.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import sys
import time
from typing import Callable
import uuid
import xml.etree.ElementTree as ET
import zlib

from android_compare import (PACKAGE, CaptureError, artifact, color_metadata,
                             command_output, installed_digest, installed_path,
                             live_pids, png_pixels, resumed_components,
                             valid_live_interval, xml_state)
from android_intro import (MAX_PRECONDITION_AGE, NEXT_ID, compare_intro,
                           intro_foreground, next_target, page_title)

HOME_CLASS = PACKAGE + '.homescreen.NewHomeScreenActivity'
PERMISSION_PACKAGES = {'com.android.permissioncontroller', 'com.google.android.permissioncontroller'}
PARTIAL_STATUS = 'COLD_AND_INTRO_CAPTURES_RECORDED_POST_INTRO_INCOMPLETE'


def completion_target(data: bytes, width: int, height: int) -> tuple[int, int]:
    """The completed four-page capture observed this same Next id and label."""
    page_title(data, 4)
    coordinates = next_target(data, width, height)
    node = next(node for node in ET.fromstring(data).iter('node')
                if node.get('package') == PACKAGE and node.get('resource-id') == NEXT_ID)
    if node.get('class') != 'android.widget.ImageButton' or node.get('content-desc') != 'Next':
        raise CaptureError('Completion control differs from the observed intro ImageButton')
    return coordinates


def surface_state(data: bytes, foreground: str) -> tuple[dict, tuple]:
    """Recognize a source-supported landing activity or notification prompt.

    Recognition is a rejection gate only. Every attribute and complete image
    remains part of the comparison; an unknown surface is never acted upon.
    """
    components = resumed_components(foreground)
    if len(components) != 1:
        raise CaptureError('Post-intro foreground owner is missing or ambiguous')
    component = components[0]
    package, class_name = component.split('/', 1)
    if class_name.startswith('.'):
        class_name = package + class_name
    if package == PACKAGE and class_name == HOME_CLASS:
        state, owned = xml_state(data)
        return {'kind': 'app_landing_surface', 'component': component,
                'owner_package': package, 'owned_nodes': owned}, state
    allowed_permission_classes = {p + '.permission.ui.GrantPermissionsActivity' for p in PERMISSION_PACKAGES}
    if package not in PERMISSION_PACKAGES or class_name not in allowed_permission_classes:
        raise CaptureError('Unexpected foreground surface after intro completion')
    state, owned = xml_state(data, owner_package=package)
    nodes = [node for node in ET.fromstring(data).iter('node') if node.get('package') == package]
    def selected(identifier: str):
        return [node for node in nodes if node.get('resource-id') in
                {p + ':id/' + identifier for p in PERMISSION_PACKAGES}]
    messages = selected('permission_message')
    if len(messages) != 1 or ' '.join(messages[0].get('text', '').split()) != 'Allow MacroDroid to send you notifications?':
        raise CaptureError('Permission surface is not the expected MacroDroid notification request')
    for identifier in ['permission_allow_button', 'permission_deny_button']:
        matches = selected(identifier)
        if len(matches) != 1 or matches[0].get('enabled') != 'true' or matches[0].get('clickable') != 'true':
            raise CaptureError('Notification permission controls are missing or ambiguous')
    return {'kind': 'notification_permission_dialog', 'component': component,
            'owner_package': package, 'owned_nodes': owned,
            'message': messages[0].get('text', '')}, state


@dataclass(frozen=True)
class CaptureIO:
    output: Path
    ui_timeout: int
    shell: Callable
    device: Callable
    save: Callable
    checked: Callable
    evidence: Callable
    environment: Callable
    checkpoint: Callable


def capture_after_intro(run: dict, label: str, io: CaptureIO, *, clock=time) -> None:
    """Execute at most one tap, preserving all observations on failure."""
    post = {'status': 'RECORDING', 'completion_input_count': 0,
            'permission_actions_taken': 0, 'artifacts': {}}
    run['post_intro'] = post
    io.checkpoint()
    sequence = run.get('intro_sequence', {})
    pages = sequence.get('pages', [])
    if sequence.get('status') != 'INTRO_PAGES_RECORDED' or len(pages) != 4 or pages[-1].get('page') != 4:
        raise CaptureError('Completed four-page intro is required before the completion input')
    final_page = pages[-1]
    previous = artifact(io.output, final_page['artifacts']['hierarchy'])
    width, height, _ = png_pixels(artifact(io.output, final_page['artifacts']['screenshot']))
    completion_target(previous, width, height)
    anchor = artifact(io.output, final_page['artifacts']['pid_final']).decode('utf-8')
    name = label + '-post-intro'

    # Recheck the installed bytes before observing the final input precondition.
    installed = {}
    post['installed_apk_before_completion'] = installed
    found = io.shell(['pm', 'path', PACKAGE])
    installed['package_path'] = io.save(name + '-installed-path', found)
    path = installed_path(found.returncode, found.stdout, found.stderr)
    checksum = io.shell(['sha256sum', path])
    installed['checksum'] = io.save(name + '-installed-sha256', checksum)
    installed['sha256'] = installed_digest(checksum.returncode, checksum.stdout, checksum.stderr, path)
    if installed['sha256'] != run['apk_sha256']:
        raise CaptureError('Installed APK changed before intro completion')
    post['environment_before'] = io.environment()
    if post['environment_before'] != run['environment']:
        raise CaptureError('Device environment changed before intro completion')

    def hierarchy(suffix: str) -> bytes:
        remote = '/data/local/tmp/mdrecovery-' + uuid.uuid4().hex + '.xml'
        try:
            io.checked(name + suffix + '-ui-dump', io.shell(['uiautomator', 'dump', remote], timeout=io.ui_timeout))
            captured = io.device(['exec-out', 'cat', remote], binary=True)
            if captured.returncode:
                raise CaptureError('Post-intro UI hierarchy retrieval failed')
            return captured.stdout
        finally:
            io.save(name + suffix + '-ui-cleanup', io.shell(['rm', '-f', remote]))

    observed = clock.monotonic()
    before = {}
    post['precondition_artifacts'] = before
    fresh = hierarchy('-before')
    before['hierarchy'] = io.evidence(name + '-before-hierarchy.xml', fresh)
    if xml_state(fresh)[0] != xml_state(previous)[0]:
        raise CaptureError('CONSTRAINTS hierarchy changed before completion input')
    pid = io.shell(['pidof', PACKAGE])
    before['pid'] = io.checked(name + '-before-pid', pid)
    live_pids(anchor, pid.stdout)
    foreground = io.shell(['dumpsys', 'activity', 'activities'])
    before['foreground'] = io.checked(name + '-before-foreground', foreground)
    if not intro_foreground(foreground.stdout):
        raise CaptureError('Intro activity is not foreground before completion input')
    coordinates = completion_target(fresh, width, height)
    transition = {'from_page': 4, 'selector': NEXT_ID, 'coordinates': list(coordinates),
                  'precondition_hierarchy': before['hierarchy'],
                  'shell_argv': ['input', 'tap', *map(str, coordinates)]}
    post['completion_transition'] = transition
    transition['precondition_age_seconds'] = clock.monotonic() - observed
    if not 0 <= transition['precondition_age_seconds'] <= MAX_PRECONDITION_AGE:
        raise CaptureError('Completion input precondition expired')
    post['completion_input_count'] = 1
    io.checkpoint()
    tapped = io.shell(transition['shell_argv'])
    transition['command'] = io.save(name + '-completion-tap', tapped)
    if tapped.returncode or tapped.stdout.strip() or tapped.stderr.strip():
        raise CaptureError('Intro completion tap did not complete cleanly')
    io.checkpoint()
    clock.sleep(3)

    a = post['artifacts']
    first = io.shell(['pidof', PACKAGE])
    a['pid_first'] = io.checked(name + '-pid-first', first)
    sampled = clock.monotonic()
    live_pids(anchor, first.stdout)
    front = io.shell(['dumpsys', 'activity', 'activities'])
    a['foreground'] = io.checked(name + '-foreground', front)
    current = hierarchy('')
    a['hierarchy'] = io.evidence(name + '-hierarchy.xml', current)
    picture = io.device(['exec-out', 'screencap', '-p'], binary=True)
    if picture.returncode:
        raise CaptureError('Post-intro screenshot retrieval failed')
    a['screenshot'] = io.evidence(name + '.png', picture.stdout)
    w, h, _ = png_pixels(picture.stdout)
    post['screen_size'] = [w, h]
    io.checkpoint()
    # Preserve the actual resulting XML/PNG before rejecting an unknown surface.
    surface, state = surface_state(current, front.stdout)
    if (w, h) != (width, height):
        raise CaptureError('Display dimensions changed after intro completion')
    after_ui = hierarchy('-after')
    a['hierarchy_after'] = io.evidence(name + '-after-hierarchy.xml', after_ui)
    after_front = io.shell(['dumpsys', 'activity', 'activities'])
    a['foreground_after'] = io.checked(name + '-foreground-after', after_front)
    surface_after, state_after = surface_state(after_ui, after_front.stdout)
    if surface_after != surface or state_after != state:
        raise CaptureError('Post-intro surface changed during screenshot collection')
    clock.sleep(max(0, 1 - (clock.monotonic() - sampled)))
    final = io.shell(['pidof', PACKAGE])
    a['pid_final'] = io.checked(name + '-pid-final', final)
    post['sample_interval_seconds'] = clock.monotonic() - sampled
    live_pids(anchor, first.stdout, final.stdout)
    post['environment_after'] = io.environment()
    if post['environment_after'] != run['environment']:
        raise CaptureError('Device environment changed after intro completion')
    post['surface'] = surface
    post['status'] = 'POST_INTRO_SURFACE_RECORDED'
    io.checkpoint()


def compare_post_intro(folder: Path) -> dict:
    result = {'scope': 'Exact first resulting surface after one observed intro completion tap per APK',
              'post_intro_surface_equal': False, 'android_runtime_executed': False,
              'complete_post_intro_captures_observed': False, 'full_runtime_1_to_1_established': False,
              'feature_parity_established': False, 'home_feature_parity_established': False,
              'animation_parity_established': False, 'permission_actions_taken': 0,
              'masks_used': False, 'ignored_app_attributes': [], 'status': 'REJECTED'}
    try:
        intro = compare_intro(folder)
        result['intro'] = intro
        result['android_runtime_executed'] = intro.get('android_runtime_executed') is True
        if intro.get('complete_intro_sequences_observed') is not True:
            raise CaptureError('Both complete intro sequences and their installed identities are required')
        report = json.loads((folder / 'result.json').read_text())
        if report.get('post_intro_requested') is not True or report.get('intro_pages_requested') is not True:
            raise CaptureError('Post-intro scope was not explicitly requested')
        if report.get('status') != 'CAPTURES_RECORDED_NOT_PARITY' or report.get('requested_capture_complete') is not True:
            raise CaptureError('Recorder did not complete the requested post-intro scope')
        collected, targets, surfaces = [], [], []
        for run in report['runs']:
            post = run['post_intro']
            if post.get('status') != 'POST_INTRO_SURFACE_RECORDED':
                raise CaptureError('Post-intro capture did not complete')
            if type(post.get('completion_input_count')) is not int or post['completion_input_count'] != 1:
                raise CaptureError('Exactly one intro completion input is required')
            if type(post.get('permission_actions_taken')) is not int or post['permission_actions_taken'] != 0:
                raise CaptureError('Permission interaction is outside this capture scope')
            installed = post['installed_apk_before_completion']
            for key in ['package_path', 'checksum']:
                if ((folder / installed[key]['stdout']['path']).resolve() ==
                        (folder / run['installed_apk'][key]['stdout']['path']).resolve()):
                    raise CaptureError('Completion reuses the initial installed-APK observation')
            path = installed_path(*command_output(folder, installed['package_path']))
            digest = installed_digest(*command_output(folder, installed['checksum']), path)
            if digest != run['apk_sha256'] or installed.get('sha256') != digest:
                raise CaptureError('Installed identity before completion differs from the input APK')
            if post['environment_before'] != run['environment'] or post['environment_after'] != run['environment']:
                raise CaptureError('Device environment changed during post-intro capture')
            page = run['intro_sequence']['pages'][-1]
            original_ui = artifact(folder, page['artifacts']['hierarchy'])
            width, height, _ = png_pixels(artifact(folder, page['artifacts']['screenshot']))
            anchor = artifact(folder, page['artifacts']['pid_final']).decode('utf-8')
            before = post['precondition_artifacts']
            if (folder / before['hierarchy']['path']).resolve() == (folder / page['artifacts']['hierarchy']['path']).resolve():
                raise CaptureError('Completion tap reused an old hierarchy file')
            fresh = artifact(folder, before['hierarchy'])
            if xml_state(fresh)[0] != xml_state(original_ui)[0]:
                raise CaptureError('CONSTRAINTS UI changed before completion input')
            live_pids(anchor, artifact(folder, before['pid']).decode('utf-8'))
            if not intro_foreground(artifact(folder, before['foreground']).decode('utf-8')):
                raise CaptureError('Intro was not foreground immediately before completion input')
            coordinates = list(completion_target(fresh, width, height))
            transition = post['completion_transition']
            age = transition.get('precondition_age_seconds')
            if type(age) not in (int, float) or not 0 <= age <= MAX_PRECONDITION_AGE:
                raise CaptureError('Completion input precondition age is invalid or expired')
            if transition.get('from_page') != 4 or transition.get('selector') != NEXT_ID or transition.get('coordinates') != coordinates:
                raise CaptureError('Completion input differs from the observed final intro button')
            if any(transition['precondition_hierarchy'].get(key) != before['hierarchy'][key] for key in ('path', 'bytes', 'sha256')):
                raise CaptureError('Completion input does not reference its observed hierarchy')
            if transition.get('shell_argv') != ['input', 'tap', *map(str, coordinates)]:
                raise CaptureError('Completion shell input differs from the observed target')
            code, stdout, stderr = command_output(folder, transition['command'])
            if type(code) is not int or code != 0 or stdout.strip() or stderr.strip():
                raise CaptureError('Completion input did not finish cleanly')
            a = post['artifacts']
            if (folder / a['hierarchy_after']['path']).resolve() == (folder / a['hierarchy']['path']).resolve():
                raise CaptureError('Surface stability reuses the initial hierarchy observation')
            if not valid_live_interval(post.get('sample_interval_seconds')):
                raise CaptureError('Post-intro process samples lack time separation')
            live_pids(anchor, artifact(folder, a['pid_first']).decode('utf-8'), artifact(folder, a['pid_final']).decode('utf-8'))
            surface, state = surface_state(artifact(folder, a['hierarchy']), artifact(folder, a['foreground']).decode('utf-8'))
            after_surface, after_state = surface_state(artifact(folder, a['hierarchy_after']), artifact(folder, a['foreground_after']).decode('utf-8'))
            if surface != post.get('surface') or after_surface != surface or after_state != state:
                raise CaptureError('Post-intro surface identity changed during capture')
            picture = artifact(folder, a['screenshot'])
            w, h, pixels = png_pixels(picture)
            if (w, h) != (width, height) or post.get('screen_size') != [w, h]:
                raise CaptureError('Post-intro screenshot dimensions differ from the recorded display')
            collected.append((state, w, h, pixels, color_metadata(picture)))
            targets.append(coordinates)
            surfaces.append(surface)
        left, right = collected
        changed = sum(left[3][i:i + 4] != right[3][i:i + 4] for i in range(0, len(left[3]), 4))
        result.update(complete_post_intro_captures_observed=True, surfaces=surfaces,
                      screen_size_equal=left[1:3] == right[1:3], hierarchy_equal=left[0] == right[0],
                      changed_pixels=changed, color_metadata_equal=left[4] == right[4],
                      surface_identity_equal=surfaces[0] == surfaces[1], completion_targets_equal=targets[0] == targets[1],
                      apk_sha256=[run['apk_sha256'] for run in report['runs']])
        result['post_intro_surface_equal'] = (intro.get('intro_sequence_equal') is True and
            result['screen_size_equal'] and result['hierarchy_equal'] and changed == 0 and
            result['color_metadata_equal'] and result['surface_identity_equal'] and result['completion_targets_equal'])
        result['status'] = 'EXACT_POST_INTRO_SURFACE_MATCH_ONLY' if result['post_intro_surface_equal'] else 'POST_INTRO_SURFACE_DIFFERENCE'
    except (OSError, KeyError, TypeError, ValueError, AttributeError, IndexError, OverflowError, zlib.error) as exc:
        result['reason'] = str(exc)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capture_directory', type=Path)
    args = parser.parse_args()
    result = compare_post_intro(args.capture_directory)
    (args.capture_directory / 'post-intro-comparison.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['post_intro_surface_equal'] else 2


if __name__ == '__main__':
    sys.exit(main())
