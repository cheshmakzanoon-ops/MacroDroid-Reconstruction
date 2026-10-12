#!/usr/bin/env python3
"""Compile the same pinned Java inputs twice and verify fresh, identical DEX.

Run with JDK 21 on PATH. This diagnostic replaces generated build/java contents
in the explicitly selected reconstruction directory; it never edits app source.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import time
import traceback


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    spec = importlib.util.spec_from_file_location('reconstruction_build', source / 'build.py')
    if spec is None or spec.loader is None:
        raise RuntimeError('Could not load the selected reconstruction build script')
    build = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build)
    report = {
        'scope': 'Consecutive Java staging cleanup and compilation',
        'build_script_sha256': hashlib.sha256((source / 'build.py').read_bytes()).hexdigest(),
        'pass': False, 'invocations': [],
    }
    try:
        build.bootstrap()
        for number in (1, 2):
            started = time.monotonic()
            directory = build.compile_java()
            dex = directory / 'dex/classes.dex'
            record = {'invocation': number,
                      'seconds': round(time.monotonic() - started, 3),
                      'dex_sha256': hashlib.sha256(dex.read_bytes()).hexdigest()}
            report['invocations'].append(record)
            print(json.dumps(record), flush=True)
        report['pass'] = len({r['dex_sha256'] for r in report['invocations']}) == 1
        return 0 if report['pass'] else 2
    except Exception as exc:
        report['error'] = f'{type(exc).__name__}: {exc}'
        report['traceback'] = traceback.format_exc()
        return 2
    finally:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
