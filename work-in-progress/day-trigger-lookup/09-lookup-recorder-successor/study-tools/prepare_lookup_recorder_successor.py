#!/usr/bin/env python3
"""Prepare the approved two-path recorder successor without altering its freeze."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import difflib
import hashlib
import json
import shutil
import traceback

ROOT = Path(__file__).resolve().parent
PARENT = ROOT / 'checkpoints/04-numeric-filesystem-merge'
STAGE = ROOT / 'stage-04'
OUT = ROOT / 'reports/19-lookup-recorder-source-successor'

RECORDER = '''    def run(folder, name, argv, expected=0, timeout=120):
        stdout, stderr = folder / (name + '.stdout.log'), folder / (name + '.stderr.log')
        observation = numeric.CommandStreamEvidence(root, stdout, stderr)
        code = None; failure = None
        try:
            folder.mkdir(parents=True, exist_ok=True)
            require(not stdout.exists() and not stderr.exists(), 'Lookup command output already exists')
            with observation as streams:
                code = subprocess.run(list(map(str, argv)), cwd=root, stdout=streams.handles['stdout'],
                                      stderr=streams.handles['stderr'], timeout=timeout).returncode
            require(code == expected, 'Lookup command failed: ' + name)
        except BaseException as error:
            failure = error
            raise
        finally:
            row = {'name': name, 'argv': list(map(str, argv)), 'timeout_seconds': timeout,
                   'expected_returncode': expected, 'returncode': code,
                   'timed_out': isinstance(failure, subprocess.TimeoutExpired),
                   'error_type': None if failure is None else type(failure).__module__ + '.' + type(failure).__qualname__,
                   'error': None if failure is None else repr(failure)}
            observation.add_to(row)
            # This is the observed wrapper finalization clock, not a fabricated
            # stream-context exit. Precondition failures never enter that context.
            row['recording_finalized'] = numeric.command_clock()
            row['stream_context_entered'] = 'invocation_started' in observation.value
            report['commands'].append(row); write_json(destination, report)
        return row'''


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'mode': path.stat().st_mode & 0o777}


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copy2(__file__, OUT / 'executed-driver.py')
    result = {'status': 'RUNNING', 'passed': False, 'started_utc': datetime.now(timezone.utc).isoformat()}
    save(OUT / 'result.json', result)
    try:
        assert not STAGE.exists()
        assert identity(PARENT / 'checkpoint.json')['sha256'] == '56aa7bfc05286d9fc474d24e6afc33fbd3a664e9dc731f70912df1a9e375b350'
        cp = json.loads((PARENT / 'checkpoint.json').read_text())
        for row in cp['files']:
            if not (row['path'].startswith('project/') or row['path'].startswith('unchanged-numeric-support/')):
                continue
            src = PARENT / row['path']
            assert identity(src) == {key: row[key] for key in ('bytes', 'sha256', 'mode')}
            relative = row['path'].split('/', 1)[1]
            target = STAGE / 'project' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
        target = STAGE / 'project/day_lookup_dex_controls.py'
        before = target.read_text()
        assert identity(target)['sha256'] == 'aaf53f9c105727c7b68f7e78b5bed0d0b89ff7772452fc6aaf51315cb73bd208'
        old_tree = ast.parse(before)
        outer = next(n for n in old_tree.body if isinstance(n, ast.FunctionDef) and n.name == 'run_controls')
        nested = next(n for n in outer.body if isinstance(n, ast.FunctionDef) and n.name == 'run')
        lines = before.splitlines(True)
        old_recorder = ''.join(lines[nested.lineno - 1:nested.end_lineno]).rstrip('\n')
        assert before.count(old_recorder) == 1
        after = before.replace(old_recorder, RECORDER)
        pairs = [
            ("    report = {'schema': 1, 'passed': False, 'status': 'RUNNING', 'androidRuntime': False,\n              'started_utc': datetime.now(timezone.utc).isoformat(), 'commands': [],",
             "    started = numeric.command_clock()\n    report = {'schema': 2, 'passed': False, 'status': 'RUNNING', 'androidRuntime': False,\n              'command_stream_evidence_schema': 2,\n              'command_stream_evidence_provider': 'day_numeric_dex_controls.CommandStreamEvidence',\n              'started_utc': started['utc'], 'started_unix_ns': started['unix_ns'],\n              'started_monotonic_ns': started['monotonic_ns'], 'commands': [],"),
            ("        report['finished_utc'] = datetime.now(timezone.utc).isoformat(); write_json(destination, report)",
             "        finished = numeric.command_clock()\n        report.update(finished_utc=finished['utc'], finished_unix_ns=finished['unix_ns'],\n                      finished_monotonic_ns=finished['monotonic_ns'])\n        write_json(destination, report)"),
        ]
        for old, new in pairs:
            assert after.count(old) == 1
            after = after.replace(old, new)
        target.write_text(after)
        test = STAGE / 'project/tests/test_day_lookup.py'
        old_test = test.read_text()
        end = "if __name__ == '__main__': unittest.main()\n"
        assert old_test.endswith(end)
        addition = (ROOT / 'lookup_recorder_tests.py.txt').read_text()
        test.write_text(old_test[:-len(end)] + addition + '\n\n' + end)
        dump = lambda node: ast.dump(node, include_attributes=False)
        new_tree = ast.parse(after)
        new_outer = next(n for n in new_tree.body if isinstance(n, ast.FunctionDef) and n.name == 'run_controls')
        assert [dump(n) for n in old_tree.body if n is not outer] == [dump(n) for n in new_tree.body if n is not new_outer]
        old_app = next(n for n in outer.body if isinstance(n, ast.Try))
        new_app = next(n for n in new_outer.body if isinstance(n, ast.Try))
        assert [dump(n) for n in old_app.body] == [dump(n) for n in new_app.body]
        assert [dump(n) for n in old_app.handlers] == [dump(n) for n in new_app.handlers]
        calls = lambda node: [dump(n) for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'run']
        assert calls(old_app) == calls(new_app)
        subprocess_call = lambda node: next(n for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                                           and isinstance(n.func.value, ast.Name) and n.func.value.id == 'subprocess' and n.func.attr == 'run')
        old_call, new_call = subprocess_call(nested), subprocess_call(new_outer)
        assert [dump(n) for n in old_call.args] == [dump(n) for n in new_call.args]
        assert [dump(n) for n in old_call.keywords if n.arg not in {'stdout', 'stderr'}] == [dump(n) for n in new_call.keywords if n.arg not in {'stdout', 'stderr'}]
        assert test.read_text().startswith(old_test[:-len(end)])
        assert identity(STAGE / 'project/day_numeric_dex_controls.py')['sha256'] == '2608a9a0a9d5b44627595fcbb696f2ec3f70213eb6af88a7282ec818d53e92f4'
        changes = []
        for name in ['day_lookup_dex_controls.py', 'tests/test_day_lookup.py']:
            old = PARENT / 'project' / name; fresh = STAGE / 'project' / name
            ast.parse(fresh.read_text())
            changes.append({'path': name, 'baseline': identity(old), 'after': identity(fresh)})
            (OUT / (Path(name).name + '.patch')).write_text(''.join(difflib.unified_diff(old.read_text().splitlines(True), fresh.read_text().splitlines(True),
                fromfile='lookup08/' + name, tofile='recorder-successor/' + name)))
        for row in cp['files']:
            if row['path'].startswith(('project/', 'unchanged-numeric-support/')):
                name = row['path'].split('/', 1)[1]
                if name not in {item['path'] for item in changes}:
                    assert identity(STAGE / 'project' / name) == identity(PARENT / row['path'])
        proof = {'all_other_top_level_lookup_definitions_exact_ast': True,
                 'complete_application_try_body_exact_ast': True, 'application_exception_handlers_exact_ast': True,
                 'all_application_run_calls_exact_ast': True, 'run_call_count': len(calls(old_app)),
                 'subprocess_argv_cwd_timeout_exact_ast': True, 'only_output_handle_selection_changes_to_shared_context': True,
                 'old_thirty_three_lookup_tests_exact_source_prefix': True, 'other_twenty_three_source_files_exact': True,
                 'shared_numeric_recorder_source_unchanged': True, 'edited_paths': changes}
        save(STAGE / 'source-derivation.json', proof)
        save(OUT / 'source-derivation.json', proof)
        for name in ['day_lookup_dex_controls.py', 'tests/test_day_lookup.py']:
            fresh = STAGE / 'project' / name
            dest = OUT / 'executed-source' / name
            dest.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(fresh, dest)
        result.update(status='TWO_PATH_RECORDER_SUCCESSOR_AUTHORED_NOT_EXECUTED', passed=True, proof=proof,
                      production_acceptance_passed=False, application_executions=0)
    except BaseException as error:
        result.update(status='SOURCE_SUCCESSOR_PREPARATION_FAILED_PRESERVED', error=repr(error))
        (OUT / 'failure.traceback.txt').write_text(traceback.format_exc())
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat(); save(OUT / 'result.json', result)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
