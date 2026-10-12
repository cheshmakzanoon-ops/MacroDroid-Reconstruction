#!/usr/bin/env python3
"""Validate the small hosted package without checkout, source materialization or build."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

import yaml

ROOT = Path('/dev/shm/day-numeric-hosted-01')
REPO = Path('/workspace/scratch/4130730d15aa/MacroDroid-Reconstruction')
TOOLS = ROOT / 'source/tools/day_numeric_acceptance'
sys.path.insert(0, str(TOOLS))
import inputs
import verify


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    args = parser.parse_args()
    inputs.require(args.name in ('workflow-validation-01', 'workflow-validation-02'), 'Unexpected output scope')
    output = ROOT / 'reports' / args.name
    output.mkdir()
    (output / 'tmp').mkdir()
    source_rows = []
    for path in sorted((ROOT / 'source').rglob('*')):
        if path.is_file():
            name = path.relative_to(ROOT / 'source').as_posix()
            target = output / 'executed-source' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
            source_rows.append({'path': name, **inputs.identity(path)})
    report = {'schema': 1, 'passed': False, 'started_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Small local hosted-workflow/CLI/input verification; no network checkout, materialization, compilation or APK copy',
              'commands': [], 'source_files': source_rows, 'full_host_acceptance_executed': False, 'android_executed': False}
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', TMPDIR=str(output / 'tmp'))
    def run(label, argv, cwd=ROOT, wanted=0):
        start = time.time_ns()
        with (output / (label + '.stdout.log')).open('xb') as stdout, (output / (label + '.stderr.log')).open('xb') as stderr:
            done = subprocess.run(argv, cwd=cwd, env=env, stdout=stdout, stderr=stderr, timeout=30)
        row = {'label': label, 'argv': argv, 'cwd': str(cwd), 'started_unix_ns': start,
               'ended_unix_ns': time.time_ns(), 'returncode': done.returncode, 'expected_returncode': wanted,
               'timeout_seconds': 30, 'stdout': inputs.identity(output / (label + '.stdout.log')),
               'stderr': inputs.identity(output / (label + '.stderr.log'))}
        report['commands'].append(row)
        inputs.require(done.returncode == wanted, 'Offline command had another result: ' + label)
    try:
        pins, before, future, capsule = inputs.contract(REPO, REPO)
        report['exact_real_input_contract'] = {'baseline': {key: before[key] for key in ('files', 'snapshot_sha256')},
                                              'future': {key: future[key] for key in ('files', 'snapshot_sha256')},
                                              'future_manifest': inputs.byte_identity(inputs.encoded(future)),
                                              'source_checkpoint': inputs.identity(capsule / 'checkpoint.json'),
                                              'source_capsule_files_verified': 113, 'source_changes': pins['source_changes']}
        raw = inputs.regular(ROOT / 'source', '.github/workflows/day-numeric-wip-acceptance.yml').read_bytes()
        workflow = yaml.load(raw, Loader=yaml.BaseLoader)
        inputs.require(workflow['permissions'] == {'contents': 'read'} and workflow['concurrency']['cancel-in-progress'] == 'false',
                       'Workflow authority or concurrency changed')
        inputs.require(set(workflow['on']) == {'push', 'pull_request', 'workflow_dispatch'}, 'Unexpected workflow trigger')
        paths = ['tools/day_numeric_acceptance/**', '.github/workflows/day-numeric-wip-acceptance.yml']
        inputs.require(workflow['on']['push'] == {'branches': ['main'], 'paths': paths}
                       and workflow['on']['pull_request'] == {'paths': paths}, 'Workflow became a broader automatic trigger')
        job = workflow['jobs']['isolated-numeric-source']
        inputs.require(set(workflow['jobs']) == {'isolated-numeric-source'} and job['runs-on'] == 'ubuntu-24.04'
                       and job['timeout-minutes'] == '120', 'Hosted platform or job bound changed')
        steps = job['steps']
        inputs.require(len(steps) == 10, 'Hosted step inventory differs')
        checkouts = steps[:3]
        bindings = [
            ('${{ github.sha }}', 'job-source', ['tools/day_numeric_acceptance', '.github/workflows']),
            (pins['baseline_commit'], 'baseline-repository', ['project', 'vendor/v9', 'scripts', '.github/workflows']),
            (pins['overlay_commit'], 'overlay-repository', [pins['overlay_capsule_path']])]
        for step, (commit, path, sparse) in zip(checkouts, bindings):
            options = step['with']
            inputs.require(step['uses'] == 'actions/checkout@11d5960a326750d5838078e36cf38b85af677262'
                           and options == {'ref': commit, 'path': path, 'fetch-depth': '1', 'persist-credentials': 'false',
                                           'sparse-checkout-cone-mode': 'true', 'sparse-checkout': '\n'.join(sparse) + '\n'},
                           'Immutable sparse checkout role differs')
        setup = steps[3]
        inputs.require(setup['uses'] == 'actions/setup-java@cf277c60eb25467037889841efdb72551f06f6c3'
                       and setup['with'] == {'distribution': 'temurin', 'java-version': '21'}, 'Parent Java action changed')
        upload = steps[-1]
        expected_upload = ['hosted-proof/', '!hosted-proof/tmp/', 'numeric-workspace/MacroDroid_v9/reports/',
                           'numeric-workspace/MacroDroid_v9/dist/*.apk', 'hosted-tool-host-tests.log',
                           'hosted-tool-source-verification.json', 'job-source/tools/day_numeric_acceptance/',
                           'job-source/.github/workflows/day-numeric-wip-acceptance.yml']
        inputs.require(upload['if'] == 'always()' and upload['uses'] == 'actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02'
                       and upload['with']['include-hidden-files'] == 'true' and upload['with']['if-no-files-found'] == 'error'
                       and upload['with']['retention-days'] == '30'
                       and upload['with']['path'].splitlines() == expected_upload, 'Full literal evidence upload differs')
        inputs.require(steps[-2]['if'] == "always() && steps.tool-inputs.outcome == 'success'", 'Failure verification guard differs')
        digest = workflow['env']['DAY_NUMERIC_RUNTIME_MANIFEST_SHA256']
        report['runtime_source'] = inputs.verify_runtime_manifest(digest)
        report['workflow'] = inputs.byte_identity(raw)
        report['sparse_checkout_roles'] = bindings
        for index, step in enumerate(steps):
            if 'run' in step:
                script = output / ('step-' + str(index) + '.sh')
                script.write_text(step['run'])
                run('bash-syntax-' + str(index), ['bash', '-n', str(script)])
        for name in ('prepare.py', 'run_acceptance.py', 'verify.py'):
            run('cli-' + name, ['python3', '-B', str(TOOLS / name), '--help'])
        # Exercise the exact inline fingerprint block in a small tooling-only layout.
        layout = output / 'fingerprint-layout'
        shutil.copytree(TOOLS, layout / 'job-source/tools/day_numeric_acceptance')
        env['DAY_NUMERIC_RUNTIME_MANIFEST_SHA256'] = digest
        fingerprint = output / 'fingerprint.sh'
        fingerprint.write_text(steps[4]['run'])
        run('actual-inline-tool-fingerprint', ['bash', str(fingerprint)], layout)
        value = inputs.read_json(layout / 'hosted-tool-source-verification.json')
        inputs.require(value.get('passed') is True and value['manifest_sha256'] == digest
                       and value['files'] == report['runtime_source']['files'], 'Inline fingerprint result differs')
        target = layout / 'job-source/tools/day_numeric_acceptance/verify.py'
        original = target.read_bytes()
        target.write_bytes(original + b'\n# SYNTHETIC WRONG TOOL BYTES\n')
        run('changed-tool-rejected', ['bash', str(fingerprint)], layout, 1)
        target.write_bytes(original)
        env['DAY_NUMERIC_RUNTIME_MANIFEST_SHA256'] = '0' * 64
        run('wrong-manifest-pin-rejected', ['bash', str(fingerprint)], layout, 1)
        env['DAY_NUMERIC_RUNTIME_MANIFEST_SHA256'] = digest
        run('exact-tool-fingerprint-restored', ['bash', str(fingerprint)], layout)
        # Recheck the preserved valid engine format with this final verifier.
        prior = ROOT / 'reports/report-compatibility-01'
        values = {p.name: inputs.read_json(p) for p in (prior / 'synthetic-rebound-reports').glob('*.json')}
        class Reports:
            def json(self, name):
                return values[name.removeprefix('reports/')]
        verify.verify_registry_and_partition(prior / 'candidate-inputs', pins,
                                             values['java-all-path-parity.json']['apkSha256'], values, Reports())
        report['engine_report_schema_compatibility'] = {'passed': True, 'scope': 'Same preserved report-format fixture with declared synthetic future counts only'}
        inputs.require(all(inputs.identity(ROOT / 'source' / row['path']) == {k: row[k] for k in ('bytes', 'sha256')}
                           for row in source_rows), 'Validated tooling changed during offline checks')
        inputs.require(inputs.identity(capsule / 'checkpoint.json') == report['exact_real_input_contract']['source_checkpoint'],
                       'Frozen application source checkpoint changed')
        actual_proposals = []
        for row in source_rows:
            inputs.require(not (REPO / row['path']).exists() and not (REPO / row['path']).is_symlink(), 'New hosted path already exists in shared repo')
            actual_proposals.append({'path': row['path'], 'baseline': None, 'must_be_absent': True, 'candidate': {k: row[k] for k in ('bytes', 'sha256')}})
        report.update(passed=True, status='SPARSE_HOSTED_WORKFLOW_AND_FROZEN_INPUTS_VERIFIED_OFFLINE',
                      completed_commands=len(report['commands']), active_proposals=actual_proposals,
                      source_and_tool_bytes_unchanged=True, full_source_or_apk_copies_created=0)
    except Exception as error:
        report['error'] = repr(error)
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        inputs.write_json(output / 'result.json', report)
    print(json.dumps({key: report.get(key) for key in ('passed', 'status', 'completed_commands', 'error')}, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
