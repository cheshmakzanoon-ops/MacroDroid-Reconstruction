#!/usr/bin/env python3
"""Verify an observed four-page MacroDroid intro sequence on both APKs.

The recorder taps only the app's observed, enabled Next button three times.
Every complete screenshot and UI hierarchy is compared, including system UI.
Synthetic unit fixtures exercise rejection rules and never prove device behavior.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
import zlib

from android_compare import (PACKAGE, CaptureError, artifact, color_metadata,
                             compare_capture, live_pids, png_pixels, resumed_components,
                             valid_live_interval, xml_state)

PAGE_COUNT = 4
NEXT_ID = PACKAGE + ':id/button_next'
MAX_PRECONDITION_AGE = 10
EXPECTED_TITLES = ('MACRODROID', 'TRIGGERS', 'ACTIONS', 'CONSTRAINTS')


def intro_foreground(text: str) -> bool:
    components = resumed_components(text)
    expected = {PACKAGE + '/.intro.IntroActivity', PACKAGE + '/' + PACKAGE + '.intro.IntroActivity'}
    return bool(components) and all(component in expected for component in components)


def page_identity(data: bytes) -> tuple[tuple[str, str], ...]:
    """Require changing app text to establish page progression; never mask XML."""
    xml_state(data)
    items = tuple((node.get('resource-id', ''), node.get('text', ''))
                  for node in ET.fromstring(data).iter('node')
                  if node.get('package') == PACKAGE and node.get('text', '').strip())
    if not items:
        raise CaptureError('Intro page has no observed app text')
    return items


def page_title(data: bytes, page: int) -> str:
    """Anchors come from the preserved intro layouts and default English strings."""
    xml_state(data)
    titles = [node.get('text', '') for node in ET.fromstring(data).iter('node')
              if node.get('package') == PACKAGE and node.get('resource-id') == PACKAGE + ':id/titleText']
    if titles != [EXPECTED_TITLES[page - 1]]:
        raise CaptureError('Observed title does not identify the expected English intro page')
    return titles[0]


def next_target(data: bytes, width: int, height: int) -> tuple[int, int]:
    xml_state(data)
    matches = [node for node in ET.fromstring(data).iter('node')
               if node.get('package') == PACKAGE and node.get('resource-id') == NEXT_ID]
    if len(matches) != 1:
        raise CaptureError('Intro Next selector is missing or ambiguous')
    node = matches[0]
    if node.get('enabled') != 'true' or node.get('clickable') != 'true':
        raise CaptureError('Intro Next button is not enabled and clickable')
    bounds = re.fullmatch(r'\[([0-9]+),([0-9]+)\]\[([0-9]+),([0-9]+)\]', node.get('bounds', ''))
    if bounds is None:
        raise CaptureError('Intro Next button bounds are invalid')
    left, top, right, bottom = map(int, bounds.groups())
    if not 0 <= left < right <= width or not 0 <= top < bottom <= height:
        raise CaptureError('Intro Next button is outside the captured screen')
    return (left + right) // 2, (top + bottom) // 2


def compare_intro(folder: Path) -> dict:
    result = {'scope': 'Exact four English intro page stills and three observed Next transitions only',
              'intro_sequence_equal': False, 'full_runtime_1_to_1_established': False,
              'feature_parity_established': False, 'android_runtime_executed': False,
              'complete_intro_sequences_observed': False,
              'animation_parity_established': False,
              'status': 'REJECTED', 'pages': [], 'masks_used': False,
              'ignored_app_attributes': []}
    try:
        cold = compare_capture(folder)
        result['cold_launch'] = cold
        result['android_runtime_executed'] = cold.get('android_runtime_executed') is True
        if cold.get('android_runtime_executed') is not True:
            raise CaptureError('Both original and candidate cold-launch captures are required')
        report = json.loads((folder / 'result.json').read_text())
        if report.get('schema_version') != 3 or cold.get('installed_apk_identities_verified') is not True:
            raise CaptureError('Intro sequence requires schema-3 installed-APK identity evidence')
        if report.get('intro_pages_requested') is not True:
            raise CaptureError('Recorder did not request the intro sequence')
        if report.get('status') != 'CAPTURES_RECORDED_NOT_PARITY' or report.get('requested_capture_complete') is not True:
            raise CaptureError('Recorder did not complete the requested intro capture')
        states = []
        transition_targets = []
        for run in report['runs']:
            sequence = run.get('intro_sequence', {})
            pages, transitions = sequence.get('pages', []), sequence.get('transitions', [])
            if sequence.get('status') != 'INTRO_PAGES_RECORDED' or len(pages) != PAGE_COUNT or len(transitions) != PAGE_COUNT - 1:
                raise CaptureError('All four intro pages and three transitions must be recorded')
            if any(pages[0].get('artifacts', {}).get(key) != run['artifacts'][key]
                   for key in ['pid_first', 'pid_final', 'foreground', 'hierarchy', 'screenshot']):
                raise CaptureError('First intro page does not reference the actual cold-launch capture')
            anchor = artifact(folder, run['artifacts']['pid_final']).decode('utf-8')
            collected, identities, targets = [], [], []
            for index, page in enumerate(pages, 1):
                if page.get('page') != index:
                    raise CaptureError('Intro page ordering is invalid')
                if not valid_live_interval(page.get('sample_interval_seconds')):
                    raise CaptureError('Intro page lacks two separated live process samples')
                a = page['artifacts']
                live_pids(anchor, artifact(folder, a['pid_first']).decode('utf-8'),
                          artifact(folder, a['pid_final']).decode('utf-8'))
                if not intro_foreground(artifact(folder, a['foreground']).decode('utf-8')):
                    raise CaptureError('Intro activity is not foreground for every page')
                hierarchy = artifact(folder, a['hierarchy'])
                state, owned = xml_state(hierarchy)
                identity = page_identity(hierarchy)
                if identity in identities:
                    raise CaptureError('Intro sequence repeats a page instead of progressing')
                identities.append(identity)
                page_title(hierarchy, index)
                picture = artifact(folder, a['screenshot'])
                width, height, pixels = png_pixels(picture)
                collected.append((state, width, height, pixels, color_metadata(picture), owned))
                if index < PAGE_COUNT:
                    transition = transitions[index - 1]
                    before = transition['precondition_artifacts']
                    fresh = artifact(folder, before['hierarchy'])
                    if (folder / before['hierarchy']['path']).resolve() == (folder / a['hierarchy']['path']).resolve():
                        raise CaptureError('Intro tap reused an old UI capture instead of a fresh precondition')
                    if xml_state(fresh)[0] != state:
                        raise CaptureError('Intro UI changed between capture and input')
                    live_pids(anchor, artifact(folder, before['pid']).decode('utf-8'))
                    if not intro_foreground(artifact(folder, before['foreground']).decode('utf-8')):
                        raise CaptureError('Intro was not foreground immediately before input')
                    age = transition.get('precondition_age_seconds')
                    if type(age) not in (int, float) or not 0 <= age <= MAX_PRECONDITION_AGE:
                        raise CaptureError('Intro input precondition age is invalid or expired')
                    coordinates = list(next_target(fresh, width, height))
                    if (transition.get('from_page'), transition.get('to_page')) != (index, index + 1):
                        raise CaptureError('Intro transition ordering is invalid')
                    if transition.get('selector') != NEXT_ID or transition.get('coordinates') != coordinates:
                        raise CaptureError('Intro input does not match the observed Next button')
                    recorded = transition['precondition_hierarchy']
                    if any(recorded.get(key) != before['hierarchy'][key] for key in ('path', 'bytes', 'sha256')) or transition.get('shell_argv') != ['input', 'tap', *map(str, coordinates)]:
                        raise CaptureError('Intro input lacks the exact recorded UI precondition')
                    command = transition['command']
                    stdout = artifact(folder, command['stdout']).decode('utf-8')
                    stderr = artifact(folder, command['stderr']).decode('utf-8')
                    if type(command.get('returncode')) is not int or command['returncode'] != 0 or stdout.strip() or stderr.strip():
                        raise CaptureError('Intro tap command did not complete cleanly')
                    targets.append(coordinates)
            states.append(collected)
            transition_targets.append(targets)
        result['android_runtime_executed'] = True
        result['complete_intro_sequences_observed'] = True
        result['transitions_equal'] = transition_targets[0] == transition_targets[1]
        for index, (original, candidate) in enumerate(zip(*states), 1):
            same_size = original[1:3] == candidate[1:3]
            changed = sum(original[3][offset:offset + 4] != candidate[3][offset:offset + 4]
                          for offset in range(0, len(original[3]), 4)) if same_size else None
            page = {'page': index, 'title': EXPECTED_TITLES[index - 1], 'hierarchy_equal': original[0] == candidate[0],
                    'screen_size_equal': same_size, 'changed_pixels': changed,
                    'color_metadata_equal': original[4] == candidate[4],
                    'owned_nodes': [original[5], candidate[5]]}
            page['equal'] = page['hierarchy_equal'] and same_size and changed == 0 and page['color_metadata_equal']
            result['pages'].append(page)
        result['apk_sha256'] = [run['apk_sha256'] for run in report['runs']]
        result['intro_sequence_equal'] = cold['cold_launch_capture_equal'] and result['transitions_equal'] and all(page['equal'] for page in result['pages'])
        result['status'] = 'EXACT_FOUR_PAGE_INTRO_MATCH_ONLY' if result['intro_sequence_equal'] else 'INTRO_DIFFERENCE'
    except (OSError, KeyError, TypeError, ValueError, AttributeError, IndexError, OverflowError, zlib.error) as exc:
        result['reason'] = str(exc)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capture_directory', type=Path)
    args = parser.parse_args()
    result = compare_intro(args.capture_directory)
    (args.capture_directory / 'intro-comparison.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['intro_sequence_equal'] else 2


if __name__ == '__main__':
    sys.exit(main())
