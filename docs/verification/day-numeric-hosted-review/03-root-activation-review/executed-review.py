#!/usr/bin/env python3
"""Bind the final root activation review without rerunning a build or mutating inputs."""
import hashlib
import json
import shutil
import stat
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

PACKAGE = Path('/dev/shm/day-numeric-hosted-01/checkpoints/01-hosted-wip-acceptance')
REVIEW = Path('/dev/shm/macrodroid-transfer-space-20261012/day-numeric-final-boundary-review/checkpoint.json')
OUT = Path('/dev/shm/macrodroid-day-numeric-root-review/checkpoints/01-activation-review')
PACKAGE_SHA = '994a29b51e3758cf9f3b32e5bd22a489009cfd45febb31f3d403572ffc1e9473'
REVIEW_SHA = '02e163b39a8e181a10679e6031f5d1aeeee469aa703bd2793e4b20691617ed09'


def identity(path):
    st = path.lstat()
    assert stat.S_ISREG(st.st_mode), str(path)
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def write(path, value):
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def main():
    started = datetime.now(timezone.utc).isoformat()
    assert identity(PACKAGE / 'checkpoint.json')['sha256'] == PACKAGE_SHA
    assert identity(REVIEW)['sha256'] == REVIEW_SHA
    manifest = json.loads((PACKAGE / 'checkpoint.json').read_bytes())
    names = [r['path'] for r in manifest['files']]
    assert len(names) == len(set(names)) == 155
    actual = []
    for row in manifest['files']:
        rel = PurePosixPath(row['path'])
        assert not rel.is_absolute() and '..' not in rel.parts and rel.as_posix() == row['path']
        path = PACKAGE / rel
        current = identity(path)
        assert current == {k: row[k] for k in ('bytes', 'sha256')}, row['path']
        mode = '100755' if path.stat().st_mode & 0o111 else '100644'
        assert mode == row['mode'], row['path']
        actual.append({'path': row['path'], **current, 'mode': mode})
    assert {p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob('*') if p.is_file()} == set(names) | {'checkpoint.json'}
    assert not any(p.is_symlink() for p in PACKAGE.rglob('*'))
    active = manifest['active_files']
    assert len(active) == 9 and len({r['path'] for r in active}) == 9
    for row in active:
        assert row['must_be_absent'] is True and row['baseline'] is None
        assert identity(PACKAGE / row['source']) == row['candidate']
        assert row['mode'] == '100644'
        assert row['path'] == '.github/workflows/day-numeric-wip-acceptance.yml' or row['path'].startswith('tools/day_numeric_acceptance/')
    toolroot = PACKAGE / 'source/tools/day_numeric_acceptance'
    runtime = json.loads((toolroot / 'runtime-files.json').read_bytes())
    assert len(runtime['files']) == 7
    for row in runtime['files']:
        assert identity(toolroot / row['path']) == {k: row[k] for k in ('bytes', 'sha256')}
    pins = json.loads((toolroot / 'pins.json').read_bytes())
    assert pins['baseline_commit'] == 'dbcad968c5c3e8f084205393a6c0d2d06a203c71'
    assert pins['overlay_commit'] == '394234b0e74c9f1d660836c8f2a89901fe05ff9d'
    assert pins['overlay_checkpoint']['sha256'] == 'c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f'
    assert len(pins['source_changes']) == 19
    assert sum(r['baseline'] is None for r in pins['source_changes']) == 7
    assert len(pins['gate_commands']) == 16 and len(pins['fresh_reports']) == 23
    workflow = (PACKAGE / 'source/.github/workflows/day-numeric-wip-acceptance.yml').read_text()
    assert identity(toolroot / 'runtime-files.json')['sha256'] in workflow
    assert pins['baseline_commit'] in workflow and pins['overlay_commit'] in workflow
    assert 'contents: read' in workflow and 'cancel-in-progress: false' in workflow
    assert workflow.count('persist-credentials: false') == 3
    assert 'if: always()' in workflow and 'include-hidden-files: true' in workflow
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(__file__, OUT / 'executed-review.py')
    review = {
        'schema': 1,
        'status': 'NINE_ADDITIVE_TOOLING_PATHS_CLEARED_FOR_HOSTED_EXECUTION',
        'started_utc': started,
        'finished_utc': datetime.now(timezone.utc).isoformat(),
        'reviewed_package': {'checkpoint_sha256': PACKAGE_SHA, 'file_count': len(actual), 'payload_bytes': sum(r['bytes'] for r in actual)},
        'independent_corrected_boundary_review': {'checkpoint_sha256': REVIEW_SHA, 'scope': 'Nine selected synthetic controls; not application acceptance'},
        'clearance': active,
        'required_remote_checks': ['Every active path absent before publication', 'Expected remote head only, no force update', 'Fetch and byte/mode verify every published file'],
        'manual_source_review': ['Exact final workflow, inputs.py, prepare.py and runtime manifest read completely', 'Fixed baseline and fixed nineteen-file capsule used in separate sparse checkouts', 'Complete source inventory preflight and nineteen guarded source writes occur only inside a fresh hosted workspace', 'All historical reports and APKs retained outside the fresh acceptance scope', 'All sixteen gates execute with literal child outcomes and complete evidence upload', 'Final verifier command and stream corrections independently reviewed against the frozen package'],
        'execution_scope': {'full_host_acceptance_executed_here': False, 'android_executed_here': False, 'active_application_promotion_authorized_by_this_review': False, 'full_runtime_1_to_1_established': False},
        'files_checked': actual,
    }
    write(OUT / 'review.json', review)
    (OUT / 'README.md').write_text('# Numeric hosted workflow activation review\n\nThe final nine additive tooling and workflow paths in frozen package `994a29b51e3758cf9f3b32e5bd22a489009cfd45febb31f3d403572ffc1e9473` are cleared for publication and actual hosted acceptance. The root read the complete final workflow, inputs, preparation code and runtime manifest. All 155 package identities and modes were checked here. The publisher separately executed the nine selected correction controls preserved at checkpoint `02e163b39a8e181a10679e6031f5d1aeeee469aa703bd2793e4b20691617ed09`.\n\nThis review changes no application source or APK and runs no application build. It requires the publisher to verify the nine absence guards and fetched remote bytes. The future job must execute all sixteen gates before a separate review can promote the nineteen-file application overlay. Its Android behavior and full runtime parity remain unproved.\n')
    rows = [{'path': p.name, **identity(p), 'mode': '100644'} for p in sorted(OUT.iterdir())]
    checkpoint = {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(), 'status': review['status'], 'repo_target': 'docs/verification/day-numeric-hosted-review/03-root-activation-review', 'active_files': [], 'files': rows, 'file_count': len(rows), 'payload_bytes': sum(r['bytes'] for r in rows)}
    write(OUT / 'checkpoint.json', checkpoint)
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'), 'files': len(rows), 'package_files_checked': len(actual), 'clearance_paths': len(active)}, indent=2))


if __name__ == '__main__':
    main()
