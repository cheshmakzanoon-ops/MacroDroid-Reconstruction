#!/usr/bin/env python3
"""One focused offline queued-entry-point control; does not execute probe code."""
import hashlib
import json
from pathlib import Path
import shlex
import unittest
import yaml

ROOT=Path('/dev/shm/day-numeric-art-workflow-01')
OBSERVATIONS=[]


def require_queued_wrapper(source):
    manifest=json.loads((source/'tools/day_numeric_art/runtime-files.json').read_bytes())
    matches=[row for row in manifest['source_roles']
             if row['source_checkpoint_path']=='source/android_day_numeric_method_probe.py']
    if len(matches)!=1:
        raise ValueError('One exact pinned executable wrapper role is required')
    role=matches[0]
    expected='$GITHUB_WORKSPACE/'+role['path']
    path=source/role['path']
    if path.is_symlink() or not path.is_file() or (path.stat().st_size,hashlib.sha256(path.read_bytes()).hexdigest())!=(role['bytes'],role['sha256']):
        raise ValueError('The pinned executable wrapper bytes differ')
    workflow=source/'.github/workflows/day-numeric-method-probe.yml'
    doc=yaml.load(workflow.read_text(),Loader=yaml.BaseLoader)
    steps=doc['jobs']['day-numeric-method-probe']['steps']
    runtime=[step['run'] for step in steps if step['name']=='Run the neutral probe once per exact APK with verification enabled']
    if len(runtime)!=1:
        raise ValueError('One exact queued runtime step is required')
    marker='python3 parent-inputs/tools/android/runtime_job.py '
    tail='2>&1 | tee ci-day-numeric-art/runtime-job.log'
    text=runtime[0]
    if text.count(marker)!=1 or text.count(tail)!=1:
        raise ValueError('One exact queued command framing is required')
    command=marker+text.split(marker,1)[1].split(tail,1)[0]
    argv=shlex.split(command.replace('\\\n',' '),comments=False,posix=True)
    if argv.count('--')!=1:
        raise ValueError('One queued child command boundary is required')
    child=argv[argv.index('--')+1:]
    if len(child)<2 or child[0]!='python3' or child[1]!=expected:
        actual=child[1] if len(child)>1 else None
        raise ValueError('Queued Python script differs from the pinned executable wrapper role: '+str(actual))
    return {'workflow_sha256':hashlib.sha256(workflow.read_bytes()).hexdigest(),
            'queued_script':child[1],'pinned_role':role['path'],'wrapper_sha256':role['sha256'],
            'queued_child_argv':child,'application_code_executed':False,'android_executed':False}


class QueuedWrapperRoleControl(unittest.TestCase):
    def test_queued_wrapper_matches_exact_manifest_role(self):
        current=ROOT/'source-02'
        original=ROOT/'source-01'
        first=require_queued_wrapper(current)
        OBSERVATIONS.append({'label':'corrected-workflow-positive','accepted':True,**first})
        with self.assertRaisesRegex(ValueError,'Queued Python script differs from the pinned executable wrapper role') as observed:
            require_queued_wrapper(original)
        OBSERVATIONS.append({'label':'retained-old-spelling','rejected':True,'reason':str(observed.exception),
            'workflow_sha256':hashlib.sha256((original/'.github/workflows/day-numeric-method-probe.yml').read_bytes()).hexdigest()})
        restored=require_queued_wrapper(current)
        self.assertEqual(first,restored)
        OBSERVATIONS.append({'label':'corrected-workflow-restored','accepted':True,**restored})


if __name__=='__main__':
    unittest.main(verbosity=2)
