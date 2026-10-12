#!/usr/bin/env python3
"""Prepare a separate twelve-screen observation proposal from actual UI fixtures."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


def identity(path):
    return {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def replace(text, old, new, label):
    if text.count(old) != 1:
        raise RuntimeError('Unexpected source anchor: ' + label)
    return text.replace(old, new)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--captures', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.repository, args.captures, args.output = [p.resolve() for p in (args.repository, args.captures, args.output)]
    args.output.mkdir(parents=True, exist_ok=False)
    target = args.output / 'repository'
    baseline = {}
    for directory in ['tools/parity_journeys', 'project']:
        for path in sorted((args.repository / directory).rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts or path.suffix in {'.pyc', '.pyo'}:
                continue
            # The complete journey tooling plus its exact pure-Python comparator dependencies.
            if directory == 'project' and path.parent != args.repository / 'project':
                continue
            if directory == 'project' and path.suffix != '.py':
                continue
            relative = path.relative_to(args.repository)
            expected = identity(path)
            destination = target / relative; destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
            if identity(path) != expected or identity(destination) != expected:
                raise RuntimeError('Baseline changed while copying')
            baseline[relative.as_posix()] = expected
    # Existing external host tests read these complete archives relative to the
    # repository root. Preserve their byte-pinned evidence dependencies too.
    for relative, digest in {
        'docs/verification/editor-journey/run-38198783416-attempt-1/evidence.zip':
            'abf947195917bb8f090cee7ae2eff250963c8d0ddd5d5663d7b76103a850c46e',
        'docs/verification/editor-journey/run-38202401351-attempt-1/evidence.zip':
            'fa2eca5f893ae181b91aa7a7bf5df8320620bbc8da21b87eacffb1de0c3bc7ee',
    }.items():
        source = args.repository / relative
        expected = identity(source)
        if expected['sha256'] != digest:
            raise RuntimeError('Existing host evidence dependency changed: ' + relative)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        if identity(source) != expected or identity(destination) != expected:
            raise RuntimeError('Evidence dependency changed while copying: ' + relative)
        baseline[relative] = expected
    folder = target / 'tools/parity_journeys'
    path = folder / 'favourite_info_journey.py'; text = path.read_text()
    text = replace(text,
                   'def dialog_identity(folder, shot, proof):\n    require_plan()\n',
                   'def dialog_identity(folder, shot, proof):\n    require_plan()\n    return _dialog_identity(folder, shot, proof)\n\n\ndef _dialog_identity(folder, shot, proof):\n',
                   'reuse unchanged dialog checks after independent plan validation')
    text = replace(text,
                   'def verify_installed_guard(folder, transition, run, proof):\n    require_plan()\n',
                   'def verify_installed_guard(folder, transition, run, proof):\n    require_plan()\n    return _verify_installed_guard(folder, transition, run, proof)\n\n\ndef _verify_installed_guard(folder, transition, run, proof):\n',
                   'reuse unchanged installed identity checks after independent plan validation')
    path.write_text(text)
    path = folder / 'observed_journey.py'; text = path.read_text()
    text = replace(text, 'def require_plan():\n', '''def information_adapter():
    if len(runner.PLAN) == 10:
        import favourite_info_journey as adapter
    elif len(runner.PLAN) == 12:
        import trigger_category_journey as adapter
    else:
        raise runner.JourneyError('No reviewed information adapter for this plan')
    return adapter


def require_plan():
''', 'explicit adapter dispatch')
    text = replace(text, 'len(runner.PLAN) not in (10, 14)', 'len(runner.PLAN) not in (10, 12, 14)', 'known plan lengths only')
    text = replace(text,
                   '    if len(runner.PLAN) == 10:\n        import favourite_info_journey as favourite\n        favourite.require_plan()\n\n\ndef required_surface',
                   '    if len(runner.PLAN) in (10, 12):\n        information_adapter().require_plan()\n\n\ndef required_surface',
                   'require the exact full plan for both explicit adapters')
    text = replace(text,
                   '    """Only the separate ten-step plan may end with an unassumed app surface."""\n',
                   '    """Only an exact reviewed adapter may declare its final unassumed surface."""\n'
                   '    if len(runner.PLAN) == 12:\n'
                   '        return information_adapter().required_surface(folder, shot, required, proof)\n',
                   'twelve-screen terminal dispatcher')
    text = replace(text,
                   "    if name == 'after-favourite-info':\n        import favourite_info_journey as favourite\n",
                   "    if name == 'after-favourite-info':\n        favourite = information_adapter()\n", 'unchanged OK identity through reviewed adapter')
    text = replace(text, '    return prior_front\n\n\ndef boundary_diagnostics',
                   '    if len(runner.PLAN) == 12:\n'
                   '        information_adapter().input_identity(folder, previous, before, action, name, proof)\n'
                   '    return prior_front\n\n\ndef boundary_diagnostics', 'observed editor/category pre-input checks')
    path.write_text(text)
    path = folder / 'editor_journey.py'; text = path.read_text()
    text = replace(text,
                   "        if name == 'after-favourite-info':\n            import favourite_info_journey as favourite\n",
                   "        if name == 'after-favourite-info':\n            favourite = observed_journey.information_adapter()\n", 'record installed OK identity')
    text = replace(text,
                   "                        if name == 'after-favourite-info':\n                            import favourite_info_journey as favourite\n",
                   "                        if name == 'after-favourite-info':\n                            favourite = observed_journey.information_adapter()\n", 'replay installed OK identity')
    text = replace(text,
                   "            result['status'] = 'EXACT_OBSERVED_DIALOG_JOURNEY_MATCH_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'\n",
                   "            result['status'] = 'EXACT_OBSERVED_DIALOG_JOURNEY_MATCH_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'\n"
                   "            if len(PLAN) == 12:\n"
                   "                result['scope'] = 'Observed first-use dialog, trigger catalog and one Date/Time category tap; the resulting app surface only'\n"
                   "                result['catalog_navigation_established'] = True\n"
                   "                result['trigger_selected'] = False\n"
                   "                result['status'] = 'EXACT_TRIGGER_CATEGORY_OBSERVATION_ONLY' if result['journey_equal'] else 'JOURNEY_DIFFERENCE'\n", 'bounded terminal scope metadata')
    path.write_text(text)
    inputs = Path(__file__).resolve().parent / 'inputs'
    for path in sorted(inputs.rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts:
            destination = folder / path.relative_to(inputs); destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
    expected = {
        'original-trigger-catalog-acquisition-1': ('3245d595f8bb661282aa228c7012169daa768fe3d874eb8f949bc5e022680bbc', 'c1e40ac122d1a0393d685c6f3018c9569b5cd731f803760d96ee75abc9a05048'),
        'candidate-trigger-catalog-acquisition-1': ('3245d595f8bb661282aa228c7012169daa768fe3d874eb8f949bc5e022680bbc', '8e77f9a5c01e2eacb1d96205cf6ffca8a372ab3ab6fc4af2e815add992aec051'),
        'original-editor-after-favourites-tip-acquisition-1': ('b679312fb987cebf3d8ff1423937e00e02ee283612d74b3027937336d9377275', 'aa1ad3841c96b4fecd1f828d77a79240330541b5784ecec43c617a194fcc7840'),
    }
    evidence = []
    for stem, hashes in expected.items():
        for suffix in ['.xml', '.png', '-foreground.txt']:
            path = args.captures / (stem + suffix)
            if suffix in ['.xml', '.png'] and identity(path)['sha256'] != hashes[['.xml', '.png'].index(suffix)]:
                raise RuntimeError('Actual observation changed: ' + path.name)
            destination = folder / 'fixtures/trigger-category' / path.name
            destination.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(path, destination)
            if identity(path) != identity(destination):
                raise RuntimeError('Copied observation differs')
            evidence.append({'path': destination.relative_to(target).as_posix(), **identity(destination)})
    changed = []
    for path in sorted(folder.rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts:
            relative = path.relative_to(target).as_posix(); actual = identity(path)
            if baseline.get(relative) != actual:
                changed.append({'path': relative, 'before': baseline.get(relative), 'after': actual})
    for relative, expected in baseline.items():
        if identity(args.repository / relative) != expected:
            raise RuntimeError('Active source changed while preparing: ' + relative)
    result = {'status': 'INACTIVE_TWELVE_SCREEN_SOURCE_PREPARED_TESTS_PENDING', 'active_source_changed': False,
              'active_apk_changed': False, 'android_executed': False, 'tests_executed': False,
              'baseline': baseline, 'changes': changed, 'observed_fixtures': evidence}
    (args.output / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'changed_paths': len(changed), 'repository': str(target)}, indent=2))


if __name__ == '__main__':
    main()
