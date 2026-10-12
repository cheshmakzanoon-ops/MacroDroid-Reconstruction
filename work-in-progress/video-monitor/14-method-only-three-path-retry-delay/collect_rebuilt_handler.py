#!/usr/bin/env python3
"""Inventory the exact rebuilt handler without executing any app instruction."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import traceback

HERE = Path(__file__).resolve().parent
DEX_SHA = '9a8770cfc8c438a08d6ebf87983767af878b01de39a93562e7bf9122c3c921b5'
SOURCE_SHA = '06d86e88dd685e53382ec6b9773a8ca9a26e6862336ddc57f5319ce7beb821e2'
CLASS_SHA = '3b9fb8b04763ec8724ffb9f808165f44bd7a29ed82bfa81a21db8a2e7a5b4333'
JAR_SHA = '354b10af74c09f5d2ab139def4231f0906dc6cc75738b1057e5a8263a412848e'


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    output = HERE / 'reports/rebuilt-handler-inventory-14'
    output.mkdir(parents=True, exist_ok=False)
    report = {'status': 'COLLECTING', 'started_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Read-only rebuilt DEX instruction/handler metadata. The unchanged old collector uses historical original-instructions.json and Original stdout labels; this wrapper explicitly identifies the input as the rebuilt fixture.',
        'input_kind': 'rebuilt-one-target-dex', 'app_method_executions': 0,
        'coverage_credit': 0, 'coverage_exemption_implemented': False, 'commands': []}
    try:
        pins = [(HERE / 'checkpoints/12-method-only-three-path/evidence/run/pipeline-output/rebuilt-video-monitor.dex', 'inputs/rebuilt-video-monitor.dex', DEX_SHA),
            (HERE / 'reports/handler-dataflow-04/VideoHandlerInventory.java', 'inputs/VideoHandlerInventory.java', SOURCE_SHA),
            (HERE / 'reports/handler-dataflow-04/toolclasses/VideoHandlerInventory.class', 'toolclasses/VideoHandlerInventory.class', CLASS_SHA)]
        report['inputs'] = []
        for source, relative, digest in pins:
            if source.is_symlink() or sha(source) != digest:
                raise RuntimeError('Pinned collector/input identity differs')
            target = output / relative; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            if sha(target) != digest:
                raise RuntimeError('Input copy differs')
            report['inputs'].append({'source': str(source), 'path': relative, 'bytes': target.stat().st_size, 'sha256': digest})
        jar = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/tools/lib/jadx-r2721.4574686-all.jar')
        if sha(jar) != JAR_SHA:
            raise RuntimeError('Bound dexlib tool identity differs')
        jdk = HERE.parent / 'tooling/jdk21'
        command = [str(jdk / 'bin/java'), '-Xmx256m', '-cp', str(jar) + os.pathsep + str(output / 'toolclasses'),
            'VideoHandlerInventory', str(output / 'inputs/rebuilt-video-monitor.dex'), str(output)]
        env = {key: value for key, value in os.environ.items() if key not in ('JAVA_TOOL_OPTIONS', 'JDK_JAVA_OPTIONS', '_JAVA_OPTIONS', 'CLASSPATH')}
        started = time.monotonic()
        out, err = output / 'inspect-rebuilt.stdout.txt', output / 'inspect-rebuilt.stderr.txt'
        with out.open('xb') as stdout, err.open('xb') as stderr:
            completed = subprocess.run(command, cwd=output, env=env, stdout=stdout, stderr=stderr, timeout=180)
        report['commands'].append({'argv': command, 'returncode': completed.returncode, 'timeout_seconds': 180,
            'seconds': round(time.monotonic()-started, 6), 'stdout_sha256': sha(out), 'stderr_sha256': sha(err)})
        if completed.returncode != 0:
            raise RuntimeError('Metadata collector failed')
        inventory = json.loads((output / 'original-instructions.json').read_text())
        report['instruction_rows'] = len(inventory['instructions'])
        report['exception_regions'] = len(inventory['exceptionRegions'])
        report['unvisited_handler_rows'] = [row for row in inventory['instructions'] if row['offset'] in (235, 236)]
        report['regions_targeting_handler'] = [row for row in inventory['exceptionRegions'] if any(h['offset'] == 235 for h in row['handlers'])]
        if report['instruction_rows'] != 290 or report['unvisited_handler_rows'] != [
                {'offset': 235, 'opcode': 'MOVE_EXCEPTION', 'units': 1, 'A': 0},
                {'offset': 236, 'opcode': 'GOTO_16', 'units': 2, 'target': 522}]:
            raise RuntimeError('Unexpected exact rebuilt handler metadata')
        if report['regions_targeting_handler'] != [{'start': 132, 'end': 163, 'handlers': [{'type': 'Ljava/lang/Exception;', 'offset': 235}]}]:
            raise RuntimeError('Unexpected rebuilt protected range')
        report['inputs_unchanged'] = all(sha(output / row['path']) == row['sha256'] and sha(Path(row['source'])) == row['sha256'] for row in report['inputs'])
        report['tool_unchanged'] = sha(jar) == JAR_SHA
        if not report['inputs_unchanged'] or not report['tool_unchanged']:
            raise RuntimeError('Metadata input changed during inspection')
        report['status'] = 'EXACT_REBUILT_HANDLER_METADATA_COLLECTED'
    except Exception as error:
        report['status'] = 'REBUILT_METADATA_COLLECTION_FAILED'; report['error'] = type(error).__name__ + ': ' + str(error)
        (output / 'failure-traceback.txt').write_text(traceback.format_exc())
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        report['files'] = [{'path': path.relative_to(output).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)} for path in sorted(output.rglob('*')) if path.is_file()]
        (output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
