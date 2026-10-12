#!/usr/bin/env python3
"""Exercise the actual production nested lookup recorder, then stop explicitly.

The sole test hook replaces target_entry at the first application-input boundary.
It retrieves the live nested run closure from its real run_controls caller, runs
one bounded Python child, then raises a sentinel. No application inputs, Java,
DEX, APK, signing, method coverage, or successful acceptance are involved.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / 'stage-03/project'
BASE = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
OUT = ROOT / 'reports/18-actual-lookup-recorder'
LOOKUP_SHA = 'aaf53f9c105727c7b68f7e78b5bed0d0b89ff7772452fc6aaf51315cb73bd208'
NUMERIC_SHA = '2608a9a0a9d5b44627595fcbb696f2ec3f70213eb6af88a7282ec818d53e92f4'


class StopBeforeApplicationProof(RuntimeError):
    pass


def require(value, message):
    if not value:
        raise RuntimeError(message)


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest, 'mode': path.stat().st_mode & 0o777}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def describe(path):
    if not path.exists():
        return None
    st = path.stat()
    return {'path': str(path), **identity(path), 'device': st.st_dev, 'inode': st.st_ino,
            'links': st.st_nlink, 'mtime_ns': st.st_mtime_ns, 'ctime_ns': st.st_ctime_ns,
            'is_symlink': path.is_symlink()}


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copy2(__file__, OUT / 'executed-driver.py')
    report = {'status': 'RUNNING', 'exercise_completed': False,
              'started_utc': datetime.now(timezone.utc).isoformat(), 'cases': [],
              'scope': __doc__, 'androidRuntime': False, 'application_executions': 0,
              'method_or_instruction_coverage_credit': 0, 'full_signed_acceptance_executed': False}
    save(OUT / 'result.json', report)
    try:
        os.environ['TMPDIR'] = str(OUT)
        import tempfile
        tempfile.tempdir = str(OUT)
        sys.path[:0] = [str(PROJECT), str(BASE)]
        import day_lookup_dex_controls as lookup
        import day_numeric_dex_controls as numeric
        require(Path(lookup.__file__).resolve() == PROJECT / 'day_lookup_dex_controls.py', 'Wrong lookup implementation loaded')
        require(Path(numeric.__file__).resolve() == PROJECT / 'day_numeric_dex_controls.py', 'Wrong numeric implementation loaded')
        require(identity(Path(lookup.__file__))['sha256'] == LOOKUP_SHA, 'Lookup source changed')
        require(identity(Path(numeric.__file__))['sha256'] == NUMERIC_SHA, 'Merged numeric source changed')
        pins = {str(path): identity(path) for path in (PROJECT.rglob('*')) if path.is_file()}
        for name in ['build.py', 'constructor_owner.py', 'ui_runtime_policy.py']:
            pins[str(BASE / name)] = identity(BASE / name)
        save(OUT / 'source-inputs.json', pins)
        text = Path(lookup.__file__).read_text()
        outer_ast = next(node for node in ast.parse(text).body if isinstance(node, ast.FunctionDef) and node.name == 'run_controls')
        nested_ast = next(node for node in outer_ast.body if isinstance(node, ast.FunctionDef) and node.name == 'run')
        nested_source = ast.get_source_segment(text, nested_ast)
        nested_codes = [node for node in lookup.run_controls.__code__.co_consts if hasattr(node, 'co_name') and node.co_name == 'run']
        require(len(nested_codes) == 1, 'Production recorder code object is not unique')
        nested_code = nested_codes[0]
        (OUT / 'bound-production-recorder.txt').write_text(nested_source + '\n')
        binding = {'source': str(Path(lookup.__file__).resolve()), 'source_identity': identity(Path(lookup.__file__)),
                   'nested_function': 'run_controls.<locals>.run', 'source_sha256': hashlib.sha256(nested_source.encode()).hexdigest(),
                   'bytecode_sha256': hashlib.sha256(nested_code.co_code).hexdigest(),
                   'actual_outer_code_identity_checked': True, 'actual_nested_code_identity_checked': True,
                   'production_source_modified': False, 'numeric_recorder_invoked': False}
        save(OUT / 'production-code-binding.json', binding)
        original_entry = lookup.target_entry
        cases = [
            ('empty-zero', 'pass', 0, 5, 'sentinel'),
            ('nonempty-both-streams', 'import sys; print("bounded stdout", flush=True); print("bounded stderr", file=sys.stderr, flush=True)', 0, 5, 'sentinel'),
            ('expected-exit-seven', 'import sys; print("intentional seven", file=sys.stderr, flush=True); sys.exit(7)', 7, 5, 'sentinel'),
            ('unexpected-exit-seven', 'import sys; print("unexpected seven", file=sys.stderr, flush=True); sys.exit(7)', 0, 5, 'unexpected-exit'),
            ('bounded-timeout', 'from pathlib import Path; import os,time; Path("child.pid").write_text(str(os.getpid())); print("before bounded timeout", flush=True); time.sleep(10)', 0, 0.4, 'timeout'),
            ('preexisting-stdout', 'from pathlib import Path; Path("would-have-run").write_text("incorrect")', 0, 5, 'preexisting'),
            ('child-replaces-stdout-path', 'from pathlib import Path; import os,sys; p=Path(sys.argv[1]); q=p.with_name("replacement.txt"); q.write_bytes(b"replacement contents\\n"); os.replace(q,p)', 0, 5, 'replacement'),
            ('child-adds-stdout-hardlink', 'from pathlib import Path; import os,sys; p=Path(sys.argv[1]); os.link(p,p.with_name("extra-hardlink.txt")); print("same inode with extra link", flush=True)', 0, 5, 'hardlink-accepted'),
        ]
        for name, code, expected, timeout, outcome in cases:
            folder = OUT / name; folder.mkdir()
            cmdfolder = folder / 'command-output'; cmdfolder.mkdir()
            stdout, stderr = cmdfolder / 'actual.stdout.log', cmdfolder / 'actual.stderr.log'
            (folder / 'child-source.py').write_text(code + '\n')
            if outcome == 'preexisting':
                stdout.write_bytes(b'preexisting owned control payload\n')
            before = {'stdout': describe(stdout), 'stderr': describe(stderr)}
            save(folder / 'before-command-files.json', before)
            argv = [sys.executable, '-B', str(folder / 'child-source.py'), str(stdout)]
            record = {'name': name, 'expected_outcome': outcome, 'argv': argv, 'expected_child_exit': expected,
                      'timeout_seconds': timeout, 'hook_calls': 0, 'live_recorder_entered': False,
                      'started_monotonic_ns': time.monotonic_ns(), 'planned_source': identity(folder / 'child-source.py')}

            def boundary_hook(argument):
                record['hook_calls'] += 1
                require(argument == folder.resolve(), 'Unexpected application-boundary argument')
                caller = sys._getframe(1)
                require(caller.f_code is lookup.run_controls.__code__, 'Hook was not reached from the actual outer runner')
                run = caller.f_locals['run']
                require(run.__code__ is nested_code and run.__globals__ is lookup.__dict__, 'Recorder was copied or substituted')
                record['live_recorder_entered'] = True
                run(cmdfolder, 'actual', argv, expected=expected, timeout=timeout)
                record['live_recorder_returned'] = True
                raise StopBeforeApplicationProof('Bounded recorder probe stopped before every application input and signed-proof gate')

            lookup.target_entry = boundary_hook
            caught = None
            try:
                lookup.run_controls(folder, [])
            except BaseException as error:
                caught = error
                record['caught_type'] = type(error).__name__
                record['caught_error'] = str(error)
                (folder / 'actual.traceback.txt').write_text(traceback.format_exc())
            finally:
                lookup.target_entry = original_entry
                record['finished_monotonic_ns'] = time.monotonic_ns()
                record['after_files'] = {'stdout': describe(stdout), 'stderr': describe(stderr),
                                         'extra_hardlink': describe(cmdfolder / 'extra-hardlink.txt')}
                save(folder / 'observation.json', record)
            require(record['hook_calls'] == 1 and record['live_recorder_entered'], 'Actual production recorder not reached exactly once')
            require(caught is not None, 'Probe improperly returned acceptance success')
            acceptance_path = folder / 'reports/day-lookup-dex-controls.json'
            acceptance = json.loads(acceptance_path.read_text())
            require(acceptance['passed'] is False and acceptance['status'] == 'LOOKUP_DEX_CONTROL_FAILED', 'Diagnostic acceptance was not explicitly failed')
            require('positive_signed_apk_instruction_match' not in acceptance, 'Diagnostic claimed signed proof')
            record['acceptance_report'] = {'path': str(acceptance_path), **identity(acceptance_path),
                                           'passed': False, 'status': acceptance['status'], 'commands_recorded': len(acceptance['commands'])}
            if outcome in ('sentinel', 'hardlink-accepted'):
                require(isinstance(caught, StopBeforeApplicationProof) and record.get('live_recorder_returned'), 'Wrong sentinel outcome')
                require(len(acceptance['commands']) == 1 and acceptance['commands'][0]['returncode'] == expected, 'Command result not retained')
            elif outcome == 'unexpected-exit':
                require(type(caught) is RuntimeError and str(caught) == 'Lookup command failed: actual', 'Wrong exit-code rejection')
                require(len(acceptance['commands']) == 1 and acceptance['commands'][0]['returncode'] == 7, 'Nonzero exit report missing')
            elif outcome == 'timeout':
                require(isinstance(caught, subprocess.TimeoutExpired), 'Timeout was not preserved')
                require(len(acceptance['commands']) == 1 and acceptance['commands'][0]['returncode'] is None, 'Timeout command report missing')
                pid = int((folder / 'child.pid').read_text())
                try:
                    os.kill(pid, 0)
                except ProcessLookupError:
                    record['timed_out_child_reaped'] = True
                else:
                    raise RuntimeError('Timed-out owned child remains present')
                record['owned_child_pid'] = pid
            elif outcome == 'preexisting':
                require(type(caught) is RuntimeError and str(caught) == 'Lookup command output already exists', 'Wrong existing-output rejection')
                require(describe(stdout) == before['stdout'] and not stderr.exists() and not (folder / 'would-have-run').exists(), 'Existing-output control was mutated or invoked')
                require(acceptance['commands'] == [], 'Uninvoked child received command credit')
            elif outcome == 'replacement':
                require(type(caught) is RuntimeError and str(caught) == 'Lookup command output path no longer names its exclusively created stream', 'Wrong path-replacement rejection')
                require(acceptance['commands'] == [], 'Replacement behavior changed; inspect raw command evidence')
                record['missing_final_command_row_after_ownership_rejection'] = True
            if outcome == 'hardlink-accepted':
                require(stdout.stat().st_nlink == 2 and (cmdfolder / 'extra-hardlink.txt').stat().st_ino == stdout.stat().st_ino,
                        'Additional hardlink was not actually created')
                record['additional_hardlink_not_rejected_by_production_recorder'] = True
            for row in acceptance['commands']:
                require(row['name'] == 'actual' and row['argv'] == argv and row['timeout_seconds'] == timeout, 'Recorded command changed')
                require(type(row['started_monotonic_ns']) is int and type(row['finished_monotonic_ns']) is int and
                        row['started_monotonic_ns'] <= row['finished_monotonic_ns'] and
                        row['duration_nanoseconds'] == row['finished_monotonic_ns'] - row['started_monotonic_ns'], 'Command duration is not exact monotonic arithmetic')
                for role, path in [('stdout', stdout), ('stderr', stderr)]:
                    observed = row[role]; actual = describe(path)
                    require({'bytes': observed['bytes'], 'sha256': observed['sha256']} ==
                            {key: actual[key] for key in ('bytes', 'sha256')}, 'Command output hash differs')
                    require(observed['exclusive_stream_witness'] == {key: actual[key] for key in ('device', 'inode')}, 'Actual stream identity differs')
            if name == 'empty-zero':
                require(stdout.read_bytes() == b'' and stderr.read_bytes() == b'', 'Empty-child output differs')
            elif name == 'nonempty-both-streams':
                require(stdout.read_bytes() == b'bounded stdout\n' and stderr.read_bytes() == b'bounded stderr\n', 'Nonempty child bytes differ')
            save(folder / 'observation.json', record)
            report['cases'].append(record)
            save(OUT / 'result.json', report)
        require(all(identity(Path(path)) == pin for path, pin in pins.items()), 'Application/source inputs changed during recorder study')
        report.update(status='ACTUAL_LOOKUP_RECORDER_EXERCISE_COMPLETE_ACCEPTANCE_REMAINS_FAILED', exercise_completed=True,
                      cases_observed=len(cases), production_acceptance_reports_passed=0, source_inputs_unchanged=True,
                      app_input_validation_executed=False, numeric_filesystem_witness_contract_inherited=False,
                      actual_narrow_contract='Exclusive xb creation; same device/inode after the child; exact file size/hash; integer monotonic duration; bounded subprocess; no same-filesystem timestamp witnesses, regular-single-link postcondition or per-stream I/O lifecycle receipts.',
                      concrete_limitations=[
                          'An additional hardlink to the exclusively created stdout inode is accepted. The production recorder does not enforce single-link ownership.',
                          'Replacing stdout with a different inode is rejected, but the finally block raises before appending the final command row; only the failed overall report, raw files and this independent diagnostic retain that attempt.',
                          'A timeout preserves the TimeoutExpired exception and a command row with returncode null; timeout type/reaped PID are not fields in that production command row. The independent diagnostic records both.'
                      ])
    except BaseException as error:
        report.update(status='RECORDER_EXERCISE_UNEXPECTED_FAILURE_PRESERVED', error=repr(error))
        (OUT / 'failure.traceback.txt').write_text(traceback.format_exc())
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(OUT / 'result.json', report)
        print(json.dumps({key: value for key, value in report.items() if key != 'cases'}, indent=2))
        require(sum(path.stat().st_size for path in ROOT.rglob('*') if path.is_file()) <= 256 * 1024 * 1024,
                'Owned initial workspace budget exceeded')


if __name__ == '__main__':
    main()
