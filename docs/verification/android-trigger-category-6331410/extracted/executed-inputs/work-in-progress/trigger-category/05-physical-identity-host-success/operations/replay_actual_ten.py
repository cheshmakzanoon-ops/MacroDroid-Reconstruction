#!/usr/bin/env python3
"""Replay the untouched actual ten-screen archive under new capture guards."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import time
import zipfile


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--historic', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.repository, args.historic, args.output = [p.resolve() for p in (args.repository, args.historic, args.output)]
    args.output.mkdir(parents=True, exist_ok=False)
    result = {'status': 'VERIFYING_HISTORICAL_ARCHIVE', 'android_executed_during_replay': False,
              'historic_run_id': 38205737183, 'historical_result_remains_unchanged': True,
              'started_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'New source policy replay against original archived command/capture bytes only; no device execution'}
    start = time.monotonic()
    try:
        archive = args.historic / 'evidence.zip'
        result['archive'] = identity(archive)
        if result['archive'] != {'bytes': 15156144, 'sha256': 'f6760a909477b09e91cb9315c67c4c59146bbf454aecc50a72809d101749b2ca'}:
            raise RuntimeError('Actual ten-screen archive identity changed')
        extracted = args.historic / 'extracted'
        files = {}
        with zipfile.ZipFile(archive) as bundle:
            for item in bundle.infolist():
                if item.is_dir():
                    continue
                name = PurePosixPath(item.filename)
                if name.is_absolute() or '..' in name.parts or item.filename in files:
                    raise RuntimeError('Invalid or duplicate archived path')
                raw = bundle.read(item)
                path = extracted / name
                if path.is_symlink() or path.read_bytes() != raw:
                    raise RuntimeError('Historical extracted bytes changed: ' + item.filename)
                files[item.filename] = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        if len(files) != 2302:
            raise RuntimeError('Historical archive member count changed')
        (args.output / 'historical-files-before.json').write_text(json.dumps(files, indent=2) + '\n')
        source_files = {path.relative_to(args.repository).as_posix(): identity(path)
                        for directory in ('tools/parity_journeys', 'project')
                        for path in sorted((args.repository / directory).rglob('*'))
                        if path.is_file() and '__pycache__' not in path.parts and path.suffix not in ('.pyc', '.pyo')}
        (args.output / 'new-policy-source.json').write_text(json.dumps(source_files, indent=2) + '\n')
        sys.dont_write_bytecode = True
        sys.path[:0] = [str(args.repository / 'tools/parity_journeys'), str(args.repository / 'project')]
        import android_compare as proof
        import editor_journey as runner
        import favourite_info_journey as favourite
        folder = extracted / 'ci-editor/journey'
        report = json.loads((folder / 'journey.json').read_text())
        original_result = json.loads((folder / 'comparison.json').read_text())
        with favourite.configured_plan():
            result['plan_sha256'] = runner.fingerprint(runner.PLAN)
            actual = runner.compare(folder, report, proof)
        (args.output / 'new-policy-comparison.json').write_text(json.dumps(actual, indent=2) + '\n')
        result['new_result_equals_historical_result'] = actual == original_result
        result['pixel_vector'] = [row['changed_pixels'] for row in actual['screens']]
        if (actual != original_result or actual['status'] != 'JOURNEY_DIFFERENCE'
                or result['pixel_vector'] != [0, 26, 0, 0, 0, 0, 0, 0, 0, 0]):
            raise RuntimeError('New capture guards did not preserve the actual measured difference: ' + str(actual.get('reason')))
        after = {relative: identity(extracted / relative) for relative in files}
        if after != files or any(identity(args.repository / relative) != expected for relative, expected in source_files.items()):
            raise RuntimeError('Historical evidence or new policy source changed during replay')
        (args.output / 'historical-files-after.json').write_text(json.dumps(after, indent=2) + '\n')
        result.update(status='NEW_CHRONOLOGY_POLICY_PRESERVES_ACTUAL_TEN_SCREEN_DIFFERENCE', passed=True,
                      historical_members_verified=len(files), historical_bytes_unchanged=True, new_source_unchanged=True)
    except Exception as exc:
        result.update(status='NEW_CHRONOLOGY_POLICY_REPLAY_FAILED', passed=False,
                      error_type=type(exc).__name__, reason=str(exc))
    result['seconds'] = round(time.monotonic() - start, 6)
    result['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (args.output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
