#!/usr/bin/env python3
"""Independently recheck the exact prepared input boundary after host tests."""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time

WORKFLOW = Path('/dev/shm/macrodroid-notification-readiness/workflow-01')
SUITE = Path('/dev/shm/macrodroid-notification-readiness/workflow-01-validation')
OUTPUT = Path(__file__).resolve().parent / 'reports/post-suite-inputs'
RESULT_SHA256 = 'e7f4ece8436cc55c020a6cea94d57de15aaa7dbfff645586e3b3933d020092df'
SOURCE_ROWS = [
  {
    "path": ".github/workflows/editor-day-time-readiness.yml",
    "bytes": 11315,
    "sha256": "56808b331ec8995c5ebf82a5a55972dfa75c078233247543a5f526f2f0949930"
  },
  {
    "path": "build_workflow.py",
    "bytes": 8024,
    "sha256": "daeff59fc2b8b6f30c22dc2f833b88bae8704655a9bfedbb106a72f01f392a24"
  },
  {
    "path": "derivation.patch",
    "bytes": 39605,
    "sha256": "95c514474564687f571708c66c43b5ce7962fac49fd0c67483dfd34aab29a1f2"
  },
  {
    "path": "derive_workflow.py",
    "bytes": 18842,
    "sha256": "5e049f39656b4ddda2d15bf50b675b7a2b39533205c407199c963a64d4d3ff0c"
  },
  {
    "path": "freeze_readiness_workflow.py",
    "bytes": 10619,
    "sha256": "0d8c2520e74beacfeb5ffbb409ae6b39bc88d8a86c76121e009ed0b704a3db9b"
  },
  {
    "path": "parent-source-identities.json",
    "bytes": 3210,
    "sha256": "0395ab70faa29690105130e251dda4d6ed56c660b6929e693b958365c0c81245"
  },
  {
    "path": "prepare_trigger_journey.py",
    "bytes": 12585,
    "sha256": "7c9bcd22d8a14463766bb053e87d56167581052a9f91d7005e2cd85f7a002195"
  },
  {
    "path": "validate_workflow.py",
    "bytes": 21432,
    "sha256": "d3412bcecd6d902d7d74bb34600844c241cd13419ead520e04b1b0ff6cf12b04"
  },
  {
    "path": "verify_trigger_journey.py",
    "bytes": 7086,
    "sha256": "99f365ff58605f1f768ee9ac1715a1a47f280b4a06a18ad549bd71d03191486c"
  }
]

def identity(path):
    digest = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        while data := stream.read(1024 * 1024):
            size += len(data)
            digest.update(data)
    return {'bytes': size, 'sha256': digest.hexdigest()}

def source_inputs():
    result = []
    for row in SOURCE_ROWS:
        path = WORKFLOW / row['path']
        actual = identity(path)
        if path.is_symlink() or actual != {k: row[k] for k in ('bytes', 'sha256')}:
            raise ValueError('Reviewed workflow source changed: ' + row['path'])
        result.append({'path': row['path'], **actual})
    return result

def main():
    OUTPUT.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    result = {
        'status': 'INDEPENDENT_POST_SUITE_INPUT_RECHECK_RUNNING',
        'passed': False,
        'android_executed': False,
        'host_suites_rerun': False,
        'writes_scope': str(Path(__file__).resolve().parent),
        'started_utc': datetime.now(timezone.utc).isoformat(),
    }
    try:
        result['source_inputs_before'] = source_inputs()
        closed = SUITE / 'result.json'
        closed_identity = identity(closed)
        if closed_identity['sha256'] != RESULT_SHA256:
            raise ValueError('The closed parent offline result changed')
        parent_result = json.loads(closed.read_bytes())
        if (parent_result.get('passed') is not True
                or parent_result.get('status') != 'OFFLINE_DAY_TIME_READINESS_WORKFLOW_VALIDATED'
                or len(parent_result['commands']) != 55):
            raise ValueError('The exact closed 55-command parent run is required')
        root = SUITE / 'private-inputs'
        prepared = root / 'ci-day-time-readiness'
        input_path = prepared / 'input-preflight.json'
        input_before = identity(input_path)
        declared = json.loads(input_path.read_bytes())
        sys.dont_write_bytecode = True
        source = WORKFLOW / 'prepare_trigger_journey.py'
        spec = importlib.util.spec_from_file_location('independently_reviewed_preparation', source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if Path(module.__file__).resolve() != source:
            raise ValueError('The intended preparation source was not loaded')
        rows = module.verify_prepared_inputs(root.resolve(), prepared.resolve(), declared)
        if len(rows) != 252 or rows != declared['files']:
            raise ValueError('The full 252-role copied boundary differs')
        if (identity(input_path) != input_before or identity(closed) != closed_identity
                or source_inputs() != result['source_inputs_before']):
            raise ValueError('A source/report changed during the independent recheck')
        result.update(
            status='INDEPENDENT_POST_SUITE_252_ROLE_INPUT_RECHECK_PASSED',
            passed=True,
            executed_function='prepare_trigger_journey.verify_prepared_inputs',
            loaded_source={'path': str(source), **identity(source)},
            parent_closed_result={'path': str(closed), **closed_identity},
            prepared_report={'path': str(input_path), **input_before},
            independently_rechecked_roles=len(rows),
            copied_source_files_and_original_inputs_exact=True,
            source_and_parent_reports_unchanged=True,
            requested_report_schema=declared['requested_report_schema'],
            notification_readiness_policy_sha256=declared['notification_readiness_policy_sha256'],
            python_version=sys.version,
        )
        (OUTPUT / 'exact-252-roles.json').write_text(json.dumps(rows, indent=2) + '\n')
    except Exception as error:
        result.update(status='INDEPENDENT_POST_SUITE_INPUT_RECHECK_FAILED',
                      reason=type(error).__name__ + ': ' + str(error))
    result['seconds'] = time.monotonic() - started
    result['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (OUTPUT / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 2

if __name__ == '__main__':
    raise SystemExit(main())

