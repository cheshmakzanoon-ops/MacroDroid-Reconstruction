#!/usr/bin/env python3
"""Preserve the prepared independent replay tool before its first device artifact."""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    home = Path(__file__).resolve().parent
    source = home / 'analyze_device_run.py'
    before = identity(source)
    ast.parse(source.read_text())
    output = home / 'checkpoints/04-prepared-device-replay-tool'
    output.mkdir(parents=True, exist_ok=False)
    for path in (source, Path(__file__)):
        shutil.copyfile(path, output / path.name)
    (output / 'syntax-check.json').write_text(json.dumps({
        'source': before, 'ast_parse_passed': True, 'artifact_replay_executed': False,
        'checked_utc': datetime.now(timezone.utc).isoformat()}, indent=2) + '\n')
    (output / 'README.md').write_text(
        '# Prepared independent readiness artifact replay\n\n'
        'This tool is prepared for the exact workflow 56808b33, activated at '
        'e1ade015f938339479216a1a91518e556902fce8. Its Python syntax has been parsed. '
        'It has not yet replayed the new Android artifact, and this checkpoint does '
        'not claim a device or analysis result.\n\n'
        'The caller supplies the actual run and artifact IDs, complete downloaded ZIP '
        'hash, raw extraction, exact reference/candidate APK paths, and a fresh output '
        'directory. The tool rehashes every ZIP member and raw file; reconstructs all '
        '252 prepared roles; replays both complete recorded comparison objects; checks '
        'raw readiness, full-frame captures and hosted test logs; and records full RGBA '
        'pixel counts for every available pair. It runs no Android command. Raw evidence '
        'and APK hashes are checked after the private replay. A failed or incomplete '
        'device result remains a failed or incomplete result even when its independent '
        'analysis reproduces it exactly.\n')
    if identity(source) != before:
        raise ValueError('Replay source changed during checkpoint creation')
    files = [{'path': path.name, **identity(path)} for path in sorted(output.iterdir()) if path.is_file()]
    value = {'status': 'REPLAY_TOOL_PREPARED_NOT_EXECUTED',
             'created_utc': datetime.now(timezone.utc).isoformat(), 'active_changes': False,
             'android_executed': False, 'artifact_replay_executed': False,
             'repo_target': 'work-in-progress/notification-readiness-analysis/01-replay-tool', 'files': files}
    target = output / 'checkpoint.json'
    target.write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(target), **identity(target), 'files': len(files)}, indent=2))


if __name__ == '__main__':
    main()
