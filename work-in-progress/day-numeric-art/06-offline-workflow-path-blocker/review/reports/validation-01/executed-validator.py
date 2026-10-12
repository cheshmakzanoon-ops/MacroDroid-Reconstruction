#!/usr/bin/env python3
"""Execute only new offline workflow boundaries; retain prior wrapper tests as prior evidence."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import time
import traceback
import yaml

ROOT = Path('/dev/shm/day-numeric-art-workflow-01')
SOURCE = ROOT / 'source-01'
PARENT = ROOT / 'inputs/parent'
OUT = ROOT / 'reports/validation-01'
PACKAGE = 'tools/day_numeric_art'
WORKFLOW = '.github/workflows/day-numeric-method-probe.yml'
SCHEMA = Path('/dev/shm/macrodroid-day-numeric-art-schema-02/checkpoints/01-literal-schema-successor-and-review')
OLD_HOST = Path('/dev/shm/macrodroid-day-numeric-art/checkpoints/04-wrapper-host-controls')
SIMULATED = Path('/dev/shm/macrodroid-day-numeric-art-schema-02/reports/focused-01/host-evidence/test_literal_integer_schema_is_required_for_provenance_and_result_replay/result')


def utc():
    return datetime.now(timezone.utc).isoformat()


def identity(path):
    a = path.lstat()
    if not stat.S_ISREG(a.st_mode):
        raise ValueError('Regular evidence/input required: ' + str(path))
    with path.open('rb') as stream:
        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    b = path.lstat()
    if (a.st_dev, a.st_ino, a.st_size, a.st_mtime_ns, a.st_ctime_ns, a.st_mode) != (
            b.st_dev, b.st_ino, b.st_size, b.st_mtime_ns, b.st_ctime_ns, b.st_mode):
        raise ValueError('Input changed while hashing')
    return {'bytes': b.st_size, 'sha256': sha, 'mode': '100755' if b.st_mode & 0o111 else '100644'}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def before_files(folder):
    return {str(path): identity(path) for path in folder.rglob('*') if path.is_file()}


def replace_bytes(path, data):
    path.unlink()
    with path.open('xb') as stream:
        stream.write(data)
    path.chmod(0o644)


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    (OUT / 'temporary').mkdir()
    shutil.copyfile(__file__, OUT / 'executed-validator.py')
    before = before_files(SOURCE) | before_files(PARENT)
    report = {'started_utc': utc(), 'passed': False, 'commands': [], 'checks': [],
        'android_executed': False, 'application_build_executed': False,
        'full_42_wrapper_suite_executed': False,
        'scope': 'New workflow/input boundaries and simulated owned cleanup only; no Android or application build.'}
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(OUT / 'temporary')}
    started = time.monotonic()

    def execute(label, argv, *, cwd=SOURCE, extra=None, timeout=120):
        if time.monotonic() - started > 600:
            raise ValueError('The fixed 600-second offline validation budget expired')
        folder = OUT / 'commands' / label
        folder.mkdir(parents=True, exist_ok=False)
        row = {'label': label, 'argv': [str(item) for item in argv], 'cwd': str(cwd),
               'timeout_seconds': timeout, 'started_utc': utc(), 'timed_out': False}
        clock = time.monotonic()
        with (folder / 'stdout.txt').open('xb') as out, (folder / 'stderr.txt').open('xb') as err:
            try:
                proc = subprocess.run(row['argv'], cwd=cwd, env={**env, **(extra or {})},
                    stdout=out, stderr=err, timeout=timeout)
                row['returncode'] = proc.returncode
            except subprocess.TimeoutExpired:
                row.update(returncode=None, timed_out=True)
        row.update(finished_utc=utc(), seconds=time.monotonic()-clock,
                   stdout=identity(folder/'stdout.txt'), stderr=identity(folder/'stderr.txt'))
        save(folder / 'command.json', row)
        report['commands'].append(row)
        print(json.dumps({key:row[key] for key in ('label','returncode','timed_out','seconds')}), flush=True)
        if row['timed_out']:
            raise ValueError('A bounded offline command timed out: ' + label)
        return row

    def preflight(label, current=SOURCE, parent=PARENT, phase='inputs', result_path=None, target=None):
        target = target or OUT / 'observations' / label
        argv = [sys.executable, '-B', current / PACKAGE / 'preflight.py', '--current', current,
                '--parent', parent, '--output', target, '--phase', phase]
        if result_path is not None:
            argv += ['--probe-result', result_path]
        row = execute(label, argv, cwd=current)
        value = json.loads((target / 'result.json').read_bytes()) if (target/'result.json').is_file() else None
        return row, value

    try:
        doc = yaml.load((SOURCE / WORKFLOW).read_text(), Loader=yaml.BaseLoader)
        job = doc['jobs']['day-numeric-method-probe']
        steps = job['steps']
        if (job['timeout-minutes'] != '60' or job['runs-on'] != 'ubuntu-24.04'
                or doc['permissions'] != {'contents':'read'}
                or doc['concurrency']['cancel-in-progress'] != 'false'):
            raise ValueError('Inherited bounded job policy changed')
        if (steps[0]['with']['persist-credentials'] != 'false'
                or steps[1]['with']['ref'] != 'fc825ede39a40249e33c8ba75b93128a98bd5e3c'
                or steps[1]['with']['persist-credentials'] != 'false'):
            raise ValueError('Fixed independent checkout policy differs')
        if steps[-1]['if'] != 'always()' or steps[-1]['with']['include-hidden-files'] != 'true' or steps[-2]['if'] != 'always()':
            raise ValueError('Raw partial evidence or final verification is not unconditional')
        source_binding = json.loads((ROOT / 'reports/source-binding-01/result.json').read_bytes())
        if not source_binding['passed'] or identity(SOURCE / WORKFLOW) != source_binding['workflow']:
            raise ValueError('Generated exact workflow differs from source binding')
        manifest = json.loads((SOURCE / PACKAGE / 'runtime-files.json').read_bytes())
        all_paths = [row['path'] for row in manifest['source_roles']] + [row['path'] for row in manifest['parent_roles']]
        if len(all_paths) != 43:
            raise ValueError('Literal complete role inventory differs')
        run_steps = [step for step in steps if 'run' in step]
        snippets = []
        for number, step in enumerate(run_steps, 1):
            script = OUT / f'step-{number:02}.sh'
            script.write_text(step['run'])
            if execute(f'bash-syntax-{number:02}', ['bash','-n',script], timeout=20)['returncode']:
                raise ValueError('Generated shell syntax failed')
            lines = step['run'].splitlines()
            for index, line in enumerate(lines):
                if "<<'PY'" in line:
                    end = next(pos for pos in range(index+1,len(lines)) if lines[pos] == 'PY')
                    text = '\n'.join(lines[index+1:end])+'\n'
                    ast.parse(text)
                    path = OUT / f'python-snippet-{len(snippets)+1:02}.py'
                    path.write_text(text)
                    snippets.append({'step':step['name'],'path':path.name,**identity(path)})
        for path in (SOURCE / PACKAGE).rglob('*.py'):
            ast.parse(path.read_text(), filename=str(path))
        report['python_snippets_parsed'] = snippets
        report['shell_steps_checked'] = len(run_steps)
        tests = ast.parse((SOURCE/PACKAGE/'test_android_day_numeric_method_probe.py').read_text())
        named = [node.name for node in ast.walk(tests) if isinstance(node,ast.FunctionDef) and node.name.startswith('test_')]
        if len(named) != 42 or len(set(named)) != 42:
            raise ValueError('The full hosted wrapper suite is not exactly 42 named tests')
        save(OUT/'hosted-test-inventory.json', {'count':42,'names':sorted(named),'executed_locally':False})
        for label,path in [('preflight-help',SOURCE/PACKAGE/'preflight.py'),
                           ('probe-help',SOURCE/PACKAGE/'android_day_numeric_method_probe.py')]:
            if execute(label,[sys.executable,'-B',path,'--help'],timeout=20)['returncode']:
                raise ValueError('Final CLI import/help failed')
        first, value = preflight('literal-complete-inputs')
        if first['returncode'] != 0 or value['passed'] is not True or value['roles_verified'] != 43 or len(value['entry_points']) != 3:
            raise ValueError('Literal complete input preflight failed')
        second, actual = preflight('actual-original-and-candidate-preflight',phase='apks')
        if second['returncode'] != 0 or actual['passed'] is not True:
            raise ValueError('Actual fixed APK preflight failed')
        for label,name in [('original','vendor/original/manifest.json'),
                           ('candidate','work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/manifest.json')]:
            row = execute('verify-parts-'+label,[sys.executable,'-B',PARENT/'scripts/assemble_artifact.py',PARENT/name,'--verify-only'])
            if row['returncode']:
                raise ValueError('Existing parent assembler did not verify exact logical bytes')
        cases = [
            ('missing-source','source','missing','tools/day_numeric_art/fixtures/observed-avd-name-crlf.stdout.txt','inputs','Executable package'),
            ('changed-source','source','append','tools/day_numeric_art/android_day_numeric_method_probe.py','inputs','Pinned source or part changed'),
            ('extra-source','source','extra','tools/day_numeric_art/unexpected.py','inputs','Executable package'),
            ('changed-runtime-manifest','source','append','tools/day_numeric_art/runtime-files.json','inputs','Exact runtime input manifest changed'),
            ('missing-runtime','parent','missing','tools/android/wait_android_ready.py','inputs','FileNotFoundError'),
            ('changed-runtime','parent','append','tools/android/bootstrap_android_runtime.py','inputs','Pinned source or part changed'),
            ('missing-original-part','parent','missing','vendor/original/original.0001.part','inputs','FileNotFoundError'),
            ('substituted-original-part','parent','substitute','vendor/original/original.0001.part','inputs','Pinned source or part changed'),
            ('truncated-candidate-part','parent','truncate','work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/parts/part-0012.bin','inputs','Pinned source or part changed'),
            ('symlink-original-part','parent','symlink','vendor/original/original.0001.part','inputs','Symlinked input'),
            ('wrong-candidate-apk','parent','wrong-apk','workspace/artifacts/MacroDroid-5.67.8-day-numeric-0762aad9.apk','apks','Fixed actual APK identity differs'),
        ]
        for label,surface,change,name,phase,reason in cases:
            case = OUT/'input-controls'/label
            shutil.copytree(SOURCE,case/'current',copy_function=os.link)
            shutil.copytree(PARENT,case/'parent',copy_function=os.link)
            path = case/('current' if surface=='source' else 'parent')/name
            if change=='missing': path.unlink()
            elif change=='append': replace_bytes(path,path.read_bytes()+b'\n# bounded offline identity fault\n')
            elif change=='extra': path.write_bytes(b'# unexpected local input\n')
            elif change=='truncate': replace_bytes(path,b'\0')
            elif change=='substitute':
                path.unlink();os.link(case/'parent/vendor/original/original.0002.part',path)
            elif change=='symlink':
                path.unlink();path.symlink_to(PARENT/name)
            elif change=='wrong-apk':
                path.unlink();os.link(case/'parent/workspace/artifacts/MacroDroid-5.67.8-original.apk',path)
            row,value=preflight(label,case/'current',case/'parent',phase)
            if row['returncode']!=2 or value is None or value['passed'] is not False or reason not in value['reason']:
                raise ValueError('Expected bounded input rejection did not occur: '+label)
            report['checks'].append({'label':label,'rejected':True,'reason':value['reason']})
        existing = OUT/'observations/literal-complete-inputs'
        existing_before = before_files(existing)
        row,_=preflight('existing-output',target=existing)
        if row['returncode']!=1 or before_files(existing)!=existing_before:
            raise ValueError('Existing preflight evidence was reused or changed')
        report['checks'].append({'label':'existing-output','rejected':True,'prior_evidence_unchanged':True})
        row,value=preflight('missing-runtime-result',phase='final')
        if row['returncode']!=2 or 'actual bounded probe result is required' not in value['reason']:
            raise ValueError('Missing final raw runtime result was not rejected')
        report['checks'].append({'label':'missing-runtime-result','rejected':True,'reason':value['reason']})
        simulated_before=before_files(SIMULATED)
        row,value=preflight('simulated-runtime-result',phase='final',result_path=SIMULATED)
        if row['returncode']!=2 or value['passed'] is not False:
            raise ValueError('Simulated host report was accepted as actual Android evidence')
        if before_files(SIMULATED)!=simulated_before:
            raise ValueError('Borrowed focused simulated evidence changed')
        report['checks'].append({'label':'simulated-runtime-result','rejected':True,'reason':value['reason']})
        runtime = next(step['run'] for step in steps if step['name'].startswith('Run the neutral probe once'))
        if ('--timeout 900' not in runtime or '--timeout 720' not in runtime or '--timeout 120' not in runtime
                or '--acceleration on' not in runtime or ' install ' in runtime):
            raise ValueError('Bounded neutral runtime invocation differs')
        start=runtime.index('cleanup_numeric_runtime() {')
        stop=runtime.index("trap 'exit 143' TERM")+len("trap 'exit 143' TERM")
        cleanup=runtime[start:stop]
        parent_doc=yaml.load((PARENT/'.github/workflows/widget-method-probe.yml').read_text(),Loader=yaml.BaseLoader)
        parent_runtime=next(step['run'] for step in parent_doc['jobs']['widget-method-probe']['steps'] if step['name'].startswith('Run both exact APKs'))
        parent_cleanup=parent_runtime[parent_runtime.index('cleanup_widget_runtime() {'):parent_runtime.index("trap 'exit 143' TERM")+len("trap 'exit 143' TERM")]
        expected_cleanup=parent_cleanup.replace('ci-widget-method','ci-day-numeric-art').replace('macrodroid-widget-tooling','macrodroid-numeric-art-tooling').replace('widget_','numeric_')
        if cleanup!=expected_cleanup:
            raise ValueError('Owned cleanup differs beyond explicit role renaming')
        save(OUT/'cleanup-derivation.json', {'unchanged_beyond_role_renaming':True,
            'parent_sha256':hashlib.sha256(parent_cleanup.encode()).hexdigest(),
            'final_sha256':hashlib.sha256(cleanup.encode()).hexdigest()})
        for label,step_status,service_status in [('clean',0,0),('failed-probe',7,0),('failed-service',0,5)]:
            case=OUT/'cleanup-controls'/label
            queue=case/'ci-day-numeric-art/environment/queue';queue.mkdir(parents=True)
            adb=case/'tooling/macrodroid-numeric-art-tooling/android/platform-tools/adb';adb.parent.mkdir(parents=True)
            adb.write_text('#!/bin/sh\nprintf "SIMULATED OFFLINE DIAGNOSTIC ONLY\\n"\nexit 0\n');adb.chmod(0o755)
            script=OUT/('cleanup-'+label+'.sh')
            script.write_text('set -euo pipefail\n'+"bash -c 'for ((n=0;n<200;n++)); do if test -e ci-day-numeric-art/environment/queue/STOP; then exit \"$1\"; fi; sleep 0.01; done; exit 99' _ "+str(service_status)+' &\n'+
                'numeric_service_pid=$!\n'+cleanup+'\nexit '+str(step_status)+'\n')
            row=execute('owned-cleanup-'+label,['bash',script],cwd=case,extra={'RUNNER_TEMP':str(case/'tooling')},timeout=10)
            result=json.loads((case/'ci-day-numeric-art/runtime-cleanup.json').read_bytes())
            if row['returncode']!=(step_status or (1 if service_status else 0)) or result['service_cleanup_confirmed'] is not (service_status==0):
                raise ValueError('Owned service cleanup exit/result differs')
            report['checks'].append({'label':'owned-cleanup-'+label,'passed':True,'actual_exit':row['returncode']})
        for label,folder,sha in [('old-41',OLD_HOST,'14bd536aa8af2e8458d8c3b1d45de6c770e55ce4e7f0f5e152a70bc6ed79e0bb'),
                                ('focused-schema',SCHEMA,'4d2bc4d8c9c5350b9572d5fa0b384438faf0a7b550156486da1e6701cc5eee1a')]:
            if identity(folder/'checkpoint.json')['sha256']!=sha:
                raise ValueError('Reused host source checkpoint changed')
            target=OUT/'reused-host-evidence'/label;target.mkdir(parents=True)
            shutil.copyfile(folder/'checkpoint.json',target/'checkpoint.json')
        report['prior_host_evidence']={'prior_41_passed_on_old_source':True,'focused_one_passed_on_successor':True,
            'old_41_reexecuted_locally':False,'full_42_reexecuted_locally':False,'hosted_full_suite_required':42}
        after={path:identity(Path(path)) for path in before}
        save(OUT/'inputs-before.json',before);save(OUT/'inputs-after.json',after)
        if after!=before:
            raise ValueError('Original source, parent parts or APK inputs changed')
        report.update(passed=True,status='OFFLINE_NEUTRAL_NUMERIC_ART_WORKFLOW_VALIDATED',
                      all_read_input_bytes_and_modes_unchanged=True,protected_inputs=len(before),
                      original_and_candidate_apks_validated_read_only=True,
                      complete_source_roles=9,complete_parent_roles=34)
    except Exception as error:
        report.update(status='OFFLINE_NEUTRAL_NUMERIC_ART_WORKFLOW_FAILED',reason=repr(error))
        save(OUT/'exception.json',{'error':repr(error),'traceback':traceback.format_exc()})
    finally:
        report.update(finished_utc=utc(),seconds=time.monotonic()-started)
        save(OUT/'result.json',report)
        print(json.dumps({k:v for k,v in report.items() if k not in ('commands','checks','python_snippets_parsed')},indent=2),flush=True)
    return 0 if report['passed'] else 2


if __name__=='__main__':
    raise SystemExit(main())
