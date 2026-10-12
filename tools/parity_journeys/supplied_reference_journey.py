#!/usr/bin/env python3
"""Run the editor journey through the supplied APK's observed promotion dialog.

This is an explicit test-plan adapter, not a change to either APK. It reuses the
current recorder and all its fail-closed evidence checks. No promotional link is
opened. Equality would apply to the supplied reference, not an official release.
"""
from __future__ import annotations
from contextlib import contextmanager
import copy
import json
from pathlib import Path
import editor_journey as runner
from robust_capture import EvidenceRecorder

PLAN_PATH = Path(__file__).with_name('editor-plan.json')


def load_plan():
    plan = json.loads(PLAN_PATH.read_text())
    baseline = json.loads(json.dumps(runner.PLAN))
    if len(baseline) != 13 or baseline[5][0] != 'home' or baseline[5][3] != runner.DENY:
        raise runner.JourneyError('Base journey changed; review the reference adapter')
    expected = copy.deepcopy(baseline)
    expected.insert(5, ['reference-promotion', runner.PACKAGE, {'text': 'LITEAPKS'}, runner.DENY])
    expected[6][3] = {'text': 'CLOSE'}
    # The first + tap is consumed by the shared first-use tip (sflpi).
    expected.insert(8, ['trigger-favourites-tip', runner.PACKAGE,
                        {'text': 'Favourite Triggers'}, runner.TRIGGER])
    expected.insert(9, ['editor-after-favourites-tip', runner.PACKAGE, runner.TRIGGER,
                        {'resource-id': 'android:id/button1'}])
    if plan != expected:
        raise runner.JourneyError('Reference plan differs from the reviewed promotion/tip sequence')
    return plan


@contextmanager
def configured_plan():
    plan = load_plan()
    previous = runner.PLAN
    previous_recorder = runner.Recorder
    try:
        runner.PLAN = plan
        runner.Recorder = EvidenceRecorder
        yield plan
    finally:
        runner.PLAN = previous
        runner.Recorder = previous_recorder


def main():
    with configured_plan():
        return runner.main()


if __name__ == '__main__':
    raise SystemExit(main())
