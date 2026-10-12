#!/usr/bin/env python3
"""Materialize a fixed baseline; physically verify Numeric19 and then Lookup21 separately."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

import inputs


def inventory(root):
    rows = []
    for path in sorted(root.rglob('*')):
        inputs.require(not path.is_symlink(), 'Symlink in prior output tree: ' + str(path))
        if path.is_file():
            rows.append({'path': path.relative_to(root).as_posix(), **inputs.identity(path)})
    return rows


def retain_prior_outputs(project, output):
    """Move historical reports/dist aside; acceptance starts with an empty output scope."""
    records = []
    prior = output / 'prior-outputs'
    prior.mkdir()
    for name in ('reports', 'dist'):
        source = project / name
        inputs.require(not source.is_symlink(), 'Historical output directory is a symlink')
        before = inventory(source) if source.exists() else []
        if source.exists():
            inputs.require(source.is_dir(), 'Historical output is not a directory')
            source.rename(prior / name)
            inputs.require(inventory(prior / name) == before, 'Historical output retention differs')
        source.mkdir(exist_ok=False)
        records.append({'scope': name, 'files': before, 'retained_directory': 'prior-outputs/' + name})
    return records


def apply_source_stages(project, output, pins, before, future, context):
    """Physically scan the complete tree before and after each exact source stage."""
    def scan(label, expected):
        actual = inputs.scan_inputs(project)
        inputs.compare_inputs(actual, expected)
        path = output / 'inputs' / (label + '-complete-inputs.json')
        with path.open('xb') as stream:
            stream.write(inputs.encoded(actual))
        inputs.require(inputs.identity(path) == inputs.byte_identity(inputs.encoded(expected)), 'Saved complete scan differs: ' + label)
    scan('baseline', before)
    inputs.apply_changes(project, context['numeric_root'], pins['source_changes'])
    scan('numeric', context['numeric_snapshot'])
    inputs.apply_changes(project, output / 'inputs/lookup-overlay', pins['lookup_source_changes'])
    scan('combined', future)
    return inputs.prepared_stage_records(pins, context)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-repository', type=Path, required=True)
    parser.add_argument('--overlay-repository', type=Path, required=True)
    parser.add_argument('--lookup-repository', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--expected-job-commit', required=True)
    parser.add_argument('--runtime-manifest-sha256', required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    baseline, overlay, lookup = args.baseline_repository.resolve(), args.overlay_repository.resolve(), args.lookup_repository.resolve()
    job = Path(__file__).resolve().parents[2]
    inputs.require(not any(output.is_relative_to(path) for path in (baseline, overlay, lookup, job)),
                   'Generated proof must be outside all checkouts')
    output.mkdir(parents=True, exist_ok=False)
    report = {'schema': 1, 'status': 'PREPARATION_FAILED', 'passed': False,
              'started_utc': datetime.now(timezone.utc).isoformat(), 'active_promoted': False,
              'android_runtime_executed': False, 'full_runtime_1_to_1_established': False}
    try:
        report['runtime_source'] = inputs.verify_runtime_manifest(args.runtime_manifest_sha256)
        report['job_checkout'] = inputs.verify_git_commit(job, args.expected_job_commit)
        report['github_context'] = {key: os.environ.get(key) for key in
                                    ('GITHUB_REPOSITORY', 'GITHUB_SHA', 'GITHUB_RUN_ID', 'GITHUB_RUN_ATTEMPT', 'GITHUB_JOB', 'GITHUB_WORKFLOW', 'RUNNER_OS', 'RUNNER_ARCH')}
        pins, before, future, context = inputs.contract(baseline, overlay, lookup)
        capsule = context['numeric_root']
        report['baseline_checkout'] = inputs.verify_git_commit(baseline, pins['baseline_commit'])
        report['overlay_checkout'] = inputs.verify_git_commit(overlay, pins['overlay_commit'])
        report['lookup_checkout'] = inputs.verify_git_commit(lookup, pins['lookup_commit'])
        for row in pins['baseline_repository_files']:
            inputs.checked_identity(baseline, row['path'], {k: row[k] for k in ('bytes', 'sha256')})
        destination = args.destination.resolve()
        inputs.require(not destination.exists() and not destination.is_symlink(), 'WIP materialization destination must be fresh')
        inputs.require(not any(destination.is_relative_to(path) or output.is_relative_to(path)
                               for path in (baseline, overlay, lookup, job)), 'Generated outputs must be outside all checkouts')
        inputs.require(not (destination.is_relative_to(output) or output.is_relative_to(destination)), 'Output and project workspaces overlap')
        retained = output / 'inputs'
        retained.mkdir()
        inputs.write_json(retained / 'source-changes.json', pins['source_changes'])
        inputs.write_json(retained / 'lookup-source-changes.json', pins['lookup_source_changes'])
        # Retain exact checkpoint bytes, not a reserialized substitute.
        shutil.copyfile(capsule / 'checkpoint.json', retained / 'source-checkpoint.json')
        for role in ('merge', 'successor'):
            shutil.copyfile(context['lookup_roots'][role] / 'checkpoint.json', retained / ('lookup-' + role + '-checkpoint.json'))
        shutil.copyfile(baseline / pins['baseline_manifest']['path'], retained / 'baseline-input-snapshot.json')
        shutil.copyfile(inputs.HERE / 'pins.json', retained / 'pins.json')
        for row in pins['source_changes']:
            target = retained / 'overlay' / row['source']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(capsule / row['source'], target)
            inputs.require(inputs.identity(target) == row['candidate'], 'Retained overlay identity differs')
        for row in context['lookup_payloads']:
            target = retained / 'lookup-overlay/project' / row['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(row['source'], target)
            inputs.require(inputs.identity(target) == row['identity'], 'Retained lookup payload differs')
        for row in pins['baseline_repository_files']:
            target = retained / 'baseline-tools' / row['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(baseline / row['path'], target)
        command = [sys.executable, '-B', str(baseline / 'scripts/materialize_v9.py'), '--destination', str(destination)]
        env = os.environ.copy()
        (output / 'tmp').mkdir()
        env.update(PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(output / 'tmp'))
        start = time.time_ns()
        with (output / 'materialize.stdout.log').open('xb') as stdout, (output / 'materialize.stderr.log').open('xb') as stderr:
            child = subprocess.run(command, cwd=baseline, env=env, stdout=stdout, stderr=stderr,
                                   timeout=pins['materialize_timeout_seconds'])
        report['materialize'] = {'argv': command, 'returncode': child.returncode,
                                 'started_unix_ns': start, 'ended_unix_ns': time.time_ns(),
                                 'timeout_seconds': pins['materialize_timeout_seconds'],
                                 'stdout': inputs.identity(output / 'materialize.stdout.log'),
                                 'stderr': inputs.identity(output / 'materialize.stderr.log')}
        inputs.require(child.returncode == 0, 'Pinned baseline materialization failed')
        project = destination / 'MacroDroid_v9'
        report['source_stages'] = apply_source_stages(project, output, pins, before, future, context)
        report['prior_outputs'] = retain_prior_outputs(project, output)
        manifest = project / 'reports/release-input-snapshot.json'
        with manifest.open('xb') as stream:
            stream.write(inputs.encoded(future))
        inputs.require(inputs.identity(manifest) == pins['future_manifest'], 'Written future manifest differs')
        shutil.copyfile(manifest, retained / 'future-input-snapshot.json')
        report['project'] = str(project.resolve())
        report['output'] = str(output)
        report['before_acceptance_reports'] = inventory(project / 'reports')
        report['before_acceptance_dist'] = inventory(project / 'dist')
        inputs.require(report['before_acceptance_reports'] == [{'path': 'release-input-snapshot.json', **pins['future_manifest']}]
                       and report['before_acceptance_dist'] == [], 'Historical evidence survived in the acceptance output scope')
        report.update(status='EXACT_NUMERIC19_THEN_LOOKUP21_WIP_PREPARED', passed=True,
                      complete_baseline_files_checked=before['files'], complete_numeric_files_checked=context['numeric_snapshot']['files'],
                      complete_future_files_checked=future['files'], numeric_source_changes_applied=19,
                      lookup_source_changes_applied=21, distinct_final_source_paths=25, new_files=13)
        inputs.verify_prepared_boundaries(pins, report, output, context)
        return 0
    except Exception as error:
        report.update(passed=False, status='PREPARATION_FAILED', error=repr(error))
        print('PREPARATION FAILED:', error, file=sys.stderr)
        return 2
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        inputs.write_json(output / 'preparation.json', report)
        print(report['status'], flush=True)


if __name__ == '__main__':
    sys.exit(main())
