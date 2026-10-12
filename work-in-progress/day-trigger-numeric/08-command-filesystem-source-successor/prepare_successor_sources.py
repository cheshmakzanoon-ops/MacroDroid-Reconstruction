#!/usr/bin/env python3
"""Create private successor files from exact retained baselines; never edit them."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
OLD_SOURCE = Path('/workspace/scratch/4130730d15aa/day-trigger-integration/checkpoints/04-source-acceptance-integration')
OLD_TOOLS = ROOT / 'baseline-source'


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    old_manifest = OLD_SOURCE / 'checkpoint.json'
    assert identity(old_manifest)['sha256'] == 'c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f'
    manifest = json.loads(old_manifest.read_text())
    project = ROOT / 'source-successor' / 'project'
    project.mkdir(parents=True, exist_ok=False)
    for row in manifest['source_changes']:
        src = OLD_SOURCE / row['source']
        assert identity(src) == row['candidate'], row['path']
        dst = project / row['path']
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    target = project / 'day_numeric_dex_controls.py'
    old = target.read_text()
    assert identity(target) == {'bytes': 30381, 'sha256': '2d5c58fc15dc50d74aeaf85802e5d57a785937439f6692772801a621209211e2'}
    block = (ROOT / 'command_stream_recording.py').read_text()
    new = old.replace('import shutil\n', 'import shutil\nimport stat\n', 1)
    needle = '\ndef validate_dependencies(root: Path, registry: list[dict]) -> set[str]:\n'
    assert new.count(needle) == 1
    new = new.replace(needle, '\n' + block + '\n' + needle, 1)
    previous = """        started = datetime.now(timezone.utc).isoformat(); tick = time.monotonic(); code = None
        try:
            with stdout.open('xb') as out, stderr.open('xb') as err:
                code = subprocess.run(list(map(str, argv)), cwd=root, stdout=out, stderr=err, timeout=timeout).returncode
        finally:
            row = {'name': name, 'argv': list(map(str, argv)), 'started_utc': started,
                   'ended_utc': datetime.now(timezone.utc).isoformat(), 'duration_seconds': time.monotonic() - tick,
                   'timeout_seconds': timeout, 'returncode': code,
                   'stdout': {'path': stdout.relative_to(root).as_posix(), **identity(stdout)},
                   'stderr': {'path': stderr.relative_to(root).as_posix(), **identity(stderr)}}
            report['commands'].append(row); write_json(destination, report)
"""
    replacement = """        observation = CommandStreamEvidence(root, stdout, stderr); code = None
        try:
            with observation as streams:
                code = subprocess.run(list(map(str, argv)), cwd=root, stdout=streams.handles['stdout'],
                                      stderr=streams.handles['stderr'], timeout=timeout).returncode
        finally:
            row = {'name': name, 'argv': list(map(str, argv)), 'timeout_seconds': timeout, 'returncode': code}
            observation.add_to(row)
            report['commands'].append(row); write_json(destination, report)
"""
    assert new.count(previous) == 1
    new = new.replace(previous, replacement, 1)
    previous = """    report = {'schema': 1, 'passed': False, 'status': 'RUNNING', 'androidRuntime': False,
              'started_utc': datetime.now(timezone.utc).isoformat(), 'commands': [],
"""
    replacement = """    started = command_clock()
    report = {'schema': 2, 'passed': False, 'status': 'RUNNING', 'androidRuntime': False,
              'started_utc': started['utc'], 'started_unix_ns': started['unix_ns'],
              'started_monotonic_ns': started['monotonic_ns'], 'commands': [],
"""
    assert new.count(previous) == 1
    new = new.replace(previous, replacement, 1)
    previous = "report['finished_utc'] = datetime.now(timezone.utc).isoformat()"
    assert new.count(previous) == 1
    new = new.replace(previous, "finished = command_clock()\n        report.update(finished_utc=finished['utc'], finished_unix_ns=finished['unix_ns'],\n                      finished_monotonic_ns=finished['monotonic_ns'])", 1)
    target.write_text(new)
    tools = ROOT / 'source'
    shutil.copytree(OLD_TOOLS, tools)
    runner = tools / 'tools/day_numeric_acceptance/run_acceptance.py'
    text = runner.read_text().replace('import os\n', 'import os\nimport hashlib\nimport stat\n', 1)
    marker = '\ndef stop_owned_group(process):\n'
    assert text.count(marker) == 1
    text = text.replace(marker, '\n' + block + '\n' + marker, 1)
    start = text.index('def run_child(')
    end = text.index('\n\ndef main():', start)
    text = text[:start] + """def run_child(command, cwd, env, stdout, stderr, timeout):
    result = {'argv': list(command), 'cwd': str(cwd), 'timeout_seconds': timeout,
              'returncode': None, 'timed_out': False}
    observation = CommandStreamEvidence(stdout.parent, stdout, stderr)
    process = None
    try:
        with observation as streams:
            try:
                process = subprocess.Popen(command, cwd=cwd, env=env, stdout=streams.handles['stdout'],
                                           stderr=streams.handles['stderr'], start_new_session=True)
                result['owned_process_group'] = process.pid
                try:
                    result['returncode'] = process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    result['timed_out'] = True
                    stop_owned_group(process)
                    result['returncode'] = process.returncode
            finally:
                if process is not None:
                    stop_owned_group(process)
    except BaseException as error:
        result['error'] = repr(error)
        if process is not None:
            result['returncode'] = process.returncode
    finally:
        observation.add_to(result)
    return result
""" + text[end:]
    old = """    report = {'schema': 1, 'status': 'HOST_ACCEPTANCE_NOT_COMPLETED', 'passed': False,
              'started_utc': datetime.now(timezone.utc).isoformat(), 'active_promoted': False,
"""
    new = """    started = command_clock()
    report = {'schema': 2, 'status': 'HOST_ACCEPTANCE_NOT_COMPLETED', 'passed': False,
              'started_utc': started['utc'], 'started_unix_ns': started['unix_ns'],
              'started_monotonic_ns': started['monotonic_ns'], 'active_promoted': False,
"""
    assert text.count(old) == 1
    text = text.replace(old, new, 1)
    old = "report['finished_utc'] = datetime.now(timezone.utc).isoformat()"
    assert text.count(old) == 1
    text = text.replace(old, "finished = command_clock()\n        report.update(finished_utc=finished['utc'], finished_unix_ns=finished['unix_ns'],\n                      finished_monotonic_ns=finished['monotonic_ns'])", 1)
    runner.write_text(text)
    print(json.dumps({'source': str(target), 'source_identity': identity(target),
                      'runner': str(runner), 'runner_identity': identity(runner),
                      'old_18_unchanged': all(identity(project / row['path']) == row['candidate']
                          for row in manifest['source_changes'] if row['path'] != 'day_numeric_dex_controls.py')}))


if __name__ == '__main__':
    main()
