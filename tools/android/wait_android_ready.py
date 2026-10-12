#!/usr/bin/env python3
"""Wait a bounded time for this service launch to report a completed Android boot."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--timeout', type=float, default=900)
    args = parser.parse_args()
    if not 0 < args.timeout <= 3600:
        parser.error('--timeout must be in (0, 3600]')
    deadline = time.monotonic() + args.timeout
    next_update = 0.0
    status = {}
    while time.monotonic() < deadline:
        launch = read_json(args.evidence / 'emulator-launch.json')
        status = read_json(args.evidence / 'runtime-status.json')
        same_launch = bool(launch.get('started_utc')) and launch.get('started_utc') == status.get('started_utc')
        if same_launch:
            props = status.get('properties', {})
            if status.get('state') == 'ready' and props.get('sys.boot_completed') == '1':
                if 'arm64-v8a' not in props.get('ro.product.cpu.abilist', ''):
                    print('Boot completed but required ARM64 ABI is absent', file=sys.stderr)
                    return 1
                if props.get('ro.dalvik.vm.native.bridge') != 'libndk_translation.so':
                    print('Boot completed but expected native bridge is absent', file=sys.stderr)
                    return 1
                print(json.dumps(status, indent=2))
                return 0
            if status.get('state') in ['stopped', 'emulator_exited']:
                print(json.dumps(status, indent=2), file=sys.stderr)
                return 1
        if time.monotonic() >= next_update:
            print(json.dumps({'state': status.get('state', 'waiting_for_service'),
                              'updated_utc': status.get('updated_utc'),
                              'adb_error': status.get('adb_error', '')}), flush=True)
            next_update = time.monotonic() + 30
        time.sleep(min(2, max(0, deadline - time.monotonic())))
    print('Android did not report ready before the bounded deadline.', file=sys.stderr)
    print(json.dumps(status, indent=2), file=sys.stderr)
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
