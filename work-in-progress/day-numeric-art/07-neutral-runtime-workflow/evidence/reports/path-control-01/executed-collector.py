#!/usr/bin/env python3
"""Retain one actual static unittest, its three observations and unchanged-source identities."""
from datetime import datetime,timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import unittest

ROOT=Path('/dev/shm/day-numeric-art-workflow-01')


def identity(path):
    raw=path.read_bytes()
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
            'mode':'100755' if path.stat().st_mode&0o111 else '100644'}


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as stream:stream.write(json.dumps(value,indent=2)+'\n')


def child(source,output):
    spec=importlib.util.spec_from_file_location('queued_wrapper_control',source)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    suite=unittest.defaultTestLoader.loadTestsFromModule(module)
    result=unittest.TextTestRunner(verbosity=2,stream=sys.stderr).run(suite)
    value={'passed':result.wasSuccessful(),'tests_run':result.testsRun,
           'observations':module.OBSERVATIONS,'scope':'Static queued Python path to pinned source identity only.',
           'probe_code_executed':False,'android_executed':False,'application_build_executed':False}
    save(output,value)
    return 0 if result.wasSuccessful() and result.testsRun==1 else 2


def main():
    out=ROOT/'reports/path-control-01';out.mkdir(parents=True,exist_ok=False)
    shutil.copyfile(__file__,out/'executed-collector.py')
    shutil.copyfile(ROOT/'check_queued_wrapper.py',out/'executed-control.py')
    paths=[]
    for folder in [ROOT/'source-01',ROOT/'source-02',ROOT/'checkpoints/01-offline-validated-runtime-path-blocker']:
        paths.extend(path for path in folder.rglob('*') if path.is_file())
    before={str(path):identity(path) for path in paths}
    result={'started_utc':datetime.now(timezone.utc).isoformat(),'passed':False,
            'android_executed':False,'application_build_executed':False,
            'prior_30_commands_rerun':False,'full_42_controls_rerun':False}
    argv=[sys.executable,'-B',str(out/'executed-collector.py'),'--child',str(out/'executed-control.py'),str(out/'observations.json')]
    command={'argv':argv,'cwd':str(out),'timeout_seconds':60,'started_utc':datetime.now(timezone.utc).isoformat(),'timed_out':False}
    clock=time.monotonic()
    with (out/'stdout.txt').open('xb') as stdout,(out/'stderr.txt').open('xb') as stderr:
        try:
            process=subprocess.run(argv,cwd=out,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},stdout=stdout,stderr=stderr,timeout=60)
            command['returncode']=process.returncode
        except subprocess.TimeoutExpired:
            command.update(returncode=None,timed_out=True)
    command.update(finished_utc=datetime.now(timezone.utc).isoformat(),seconds=time.monotonic()-clock,
                   stdout=identity(out/'stdout.txt'),stderr=identity(out/'stderr.txt'))
    save(out/'command.json',command)
    after={str(path):identity(path) for path in paths}
    save(out/'inputs-before.json',before);save(out/'inputs-after.json',after)
    if command['returncode']==0 and not command['timed_out']:
        actual=json.loads((out/'observations.json').read_bytes())
        if actual['passed'] is True and actual['tests_run']==1 and len(actual['observations'])==3 and before==after:
            result.update(passed=True,status='FOCUSED_QUEUED_WRAPPER_ROLE_CONTROL_PASSED',
                          actual_tests_run=1,old_spelling_rejected=True,positive_and_restore_passed=True,
                          unchanged_source_and_frozen_payloads=len(before))
    if not result['passed']:result['status']='FOCUSED_QUEUED_WRAPPER_ROLE_CONTROL_FAILED'
    result['finished_utc']=datetime.now(timezone.utc).isoformat();save(out/'result.json',result)
    print(json.dumps(result,indent=2))
    return 0 if result['passed'] else 2


if __name__=='__main__':
    if len(sys.argv)==4 and sys.argv[1]=='--child':raise SystemExit(child(Path(sys.argv[2]),Path(sys.argv[3])))
    raise SystemExit(main())
