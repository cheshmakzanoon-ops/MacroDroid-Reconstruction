#!/usr/bin/env python3
"""Record the reviewed 16-screen journey and independently compare the editor session.

This is an explicit test-plan adapter, not a change to either APK. It reuses the
current recorder and all its fail-closed evidence checks. No promotional link is
opened. Equality would apply to the supplied reference, not an official release.
"""
from __future__ import annotations
from contextlib import contextmanager
import argparse
import sys
import json
from pathlib import Path
import editor_journey as runner
from post_onboarding import SessionRecorder, compare_session

from supplied_reference_journey import load_plan



@contextmanager
def configured_plan():
    plan = load_plan()
    previous = runner.PLAN
    previous_recorder = runner.Recorder
    try:
        runner.PLAN = plan
        runner.Recorder = SessionRecorder
        yield plan
    finally:
        runner.PLAN = previous
        runner.Recorder = previous_recorder


def main():
    with configured_plan() as plan:
        status = runner.main()
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--output', type=Path, required=True)
        args, _ = parser.parse_known_args()
        report = json.loads((args.output / 'journey.json').read_text())
        result = compare_session(args.output, report, plan, sys.modules['android_compare'])
        (args.output / 'editor-session-comparison.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result, indent=2))
        # A narrower session result never overwrites the continuous startup result.
        return status


if __name__ == '__main__':
    raise SystemExit(main())
