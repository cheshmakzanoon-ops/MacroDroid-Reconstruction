#!/usr/bin/env python3
"""Bind the final nine-role source and exact parent to a separate inactive workflow."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import stat

ROOT = Path('/dev/shm/day-numeric-art-workflow-01')
CAPSULE = Path('/dev/shm/macrodroid-day-numeric-art-schema-02/checkpoints/01-literal-schema-successor-and-review')
EXPECTED = '4d2bc4d8c9c5350b9572d5fa0b384438faf0a7b550156486da1e6701cc5eee1a'


def identity(path):
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError('Regular source required')
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'mode': '100755' if info.st_mode & 0o111 else '100644'}


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)
    path.chmod(0o644)


def json_bytes(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def main():
    output = ROOT / 'reports/source-binding-01'
    output.mkdir(parents=True, exist_ok=False)
    destination = ROOT / 'source-01'
    destination.mkdir(exist_ok=False)
    report = {'started_utc': datetime.now(timezone.utc).isoformat(), 'passed': False,
              'android_executed': False, 'application_build_executed': False,
              'host_controls_rerun': False, 'copies': []}
    before = identity(CAPSULE / 'checkpoint.json')
    try:
        if before['sha256'] != EXPECTED:
            raise ValueError('Final source checkpoint differs')
        checkpoint = json.loads((CAPSULE / 'checkpoint.json').read_bytes())
        if len(checkpoint['source_files']) != 9 or checkpoint['final_named_host_test_count'] != 42:
            raise ValueError('Closed nine-role 42-control source is required')
        source_roles = []
        for row in checkpoint['source_files']:
            path = CAPSULE / row['path']
            actual = identity(path)
            if actual != {'bytes': row['bytes'], 'sha256': row['sha256'],
                          'mode': '100755' if row['mode'] & 0o111 else '100644'}:
                raise ValueError('Frozen source role changed')
            relative = 'tools/day_numeric_art/' + row['path'].removeprefix('source/')
            save(destination / relative, path.read_bytes())
            if identity(destination / relative) != actual:
                raise ValueError('Exact source copy differs')
            source_roles.append({'path': relative, **actual, 'retain_copy': True,
                                 'source_checkpoint_path': row['path']})
            report['copies'].append({'origin': str(path), 'path': relative, **actual})
        parents = json.loads((ROOT / 'reports/parent-inputs-01/result.json').read_bytes())
        if not parents['passed'] or len(parents['rows']) != 34:
            raise ValueError('Exact parent inventory is incomplete')
        parent_roles = []
        for row in parents['rows']:
            parent_roles.append({key: row[key] for key in ('path','bytes','sha256','mode','git_blob_sha1')}
                                | {'retain_copy': row['role'] != 'apk-part-not-copied'})
        manifest = {
            'schema': 1, 'parent_commit': parents['commit'],
            'source_checkpoint': {'repo_path': checkpoint['repo_target'] + '/checkpoint.json',
                                  **before},
            'scope': 'Neutral DayTrigger r0 ART probe only; 1291 cases per exact APK, separate app_process64 processes, no installation, UI, macro configuration or alarms.',
            'source_roles': source_roles, 'parent_roles': parent_roles,
            'expected_host_controls': 42,
            'limits': {'job_minutes': 60, 'runtime_service_seconds': 3600,
                'readiness_seconds': 900, 'queued_probe_seconds': 720,
                'app_process_seconds_each': 120, 'host_controls_seconds': 240,
                'cleanup_logcat_seconds': 30, 'owned_service_wait_seconds': 60},
            'host_evidence_scope': {'prior_41_source_tests_reused': True,
                'successor_one_focused_test_reused': True, 'full_42_locally_rerun': False,
                'hosted_workflow_runs_all_42': True},
        }
        manifest_data = json_bytes(manifest)
        manifest_sha = hashlib.sha256(manifest_data).hexdigest()
        save(destination / 'tools/day_numeric_art/runtime-files.json', manifest_data)
        template = (ROOT / 'preflight.template.py').read_text()
        if template.count('__MANIFEST_SHA256__') != 1:
            raise ValueError('Preflight manifest placeholder count differs')
        preflight = template.replace('__MANIFEST_SHA256__', manifest_sha).encode()
        save(destination / 'tools/day_numeric_art/preflight.py', preflight)
        spec = importlib.util.spec_from_file_location('numeric_workflow_author', ROOT / 'derive_workflow.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        workflow = module.make_workflow(hashlib.sha256(preflight).hexdigest(), manifest_sha).encode()
        save(destination / '.github/workflows/day-numeric-method-probe.yml', workflow)
        save(ROOT / 'inputs/source-schema-checkpoint.json', (CAPSULE / 'checkpoint.json').read_bytes())
        save(ROOT / 'inputs/source-bindings.json', (CAPSULE / 'source-bindings.json').read_bytes())
        save(ROOT / 'inputs/source-ast-derivation.json', (CAPSULE / 'ast-derivation.json').read_bytes())
        if identity(CAPSULE / 'checkpoint.json') != before:
            raise ValueError('Source checkpoint changed during binding')
        for row in checkpoint['source_files']:
            if identity(CAPSULE / row['path'])['sha256'] != row['sha256']:
                raise ValueError('Original source changed during binding')
        report.update(passed=True, status='EXACT_NINE_SOURCE_AND_TWELVE_WORKFLOW_PAYLOADS_BOUND',
                      source_checkpoint=before, source_roles=9, parent_roles=34,
                      runtime_manifest=identity(destination / 'tools/day_numeric_art/runtime-files.json'),
                      preflight=identity(destination / 'tools/day_numeric_art/preflight.py'),
                      workflow=identity(destination / '.github/workflows/day-numeric-method-probe.yml'))
    except Exception as error:
        report.update(status='NUMERIC_SOURCE_WORKFLOW_BINDING_FAILED', reason=repr(error))
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(output / 'result.json', json_bytes(report))
        print(json.dumps({k:v for k,v in report.items() if k != 'copies'}, indent=2))
    if not report['passed']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
