#!/usr/bin/env python3
"""Freeze the reviewed-source-bound numeric tooling successor and complete controls."""
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'source'
DEST = ROOT / 'checkpoints/02-hosted-filesystem-tooling-successor'
DEST.mkdir(parents=True, exist_ok=False)
PUBLICATION = 'work-in-progress/day-trigger-numeric/09-hosted-filesystem-acceptance'
BUDGET = 64 * 1024 * 1024

def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')

def copy_file(path, target):
    assert path.is_file() and not path.is_symlink(), path
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, target)
    assert identity(path) == identity(target)

bindings = json.loads((ROOT / 'reports/07-final-tool-bindings-from-fetched-git/result.json').read_bytes())
full = json.loads((ROOT / 'reports/08-complete-tooling-discovery/result.json').read_bytes())
assert full['passed'] is True and full['returncode'] == 0 and full['tests'] == 92
assert full['source_unchanged'] is True and full['source_before'] == full['source_after'] == bindings['proposed_tool_files']
log = (ROOT / 'reports/08-complete-tooling-discovery/stderr.log').read_text()
assert len(re.findall(r'^test_\S+ \(.*\) \.\.\. ', log, re.M)) == 92 and '\nOK\n' in log
active = []
diff = []
for row, before in zip(bindings['proposed_tool_files'], bindings['active_repository_baselines']):
    assert row['path'] == before['path']
    name = row['path']
    assert identity(SOURCE / name) == {key: row[key] for key in ('bytes', 'sha256')}
    original = ROOT / 'baseline-source' / name
    assert identity(original) == {key: before[key] for key in ('bytes', 'sha256')}
    copy_file(SOURCE / name, DEST / 'source' / name)
    copy_file(original, DEST / 'prior-source' / name)
    active.append({'path': name, 'source': 'source/' + name,
                   'baseline': {key: before[key] for key in ('bytes', 'sha256')},
                   'candidate': {key: row[key] for key in ('bytes', 'sha256')},
                   'must_be_absent': False, 'mode': '100644'})
    diff.extend(difflib.unified_diff(original.read_text().splitlines(True), (SOURCE / name).read_text().splitlines(True),
                                    fromfile='prior/' + name, tofile='successor/' + name))
assert len(active) == 9
(DEST / 'tooling-derivation.patch').write_text(''.join(diff))
write(DEST / 'nine-path-bindings.json', active)

reports = ['04-verifier-controls-attempt-01', '05-verifier-adversarial-attempt-01',
           '06-final-tool-bindings', '07-final-tool-bindings-from-fetched-git', '08-complete-tooling-discovery']
for name in reports:
    for path in sorted((ROOT / 'reports' / name).rglob('*')):
        if path.is_file():
            copy_file(path, DEST / 'evidence' / name / path.relative_to(ROOT / 'reports' / name))
for name in ['06-final-tool-bindings.stdout.log', '06-final-tool-bindings.stderr.log',
             '07-final-tool-bindings.stdout.log', '07-final-tool-bindings.stderr.log']:
    copy_file(ROOT / 'reports' / name, DEST / 'evidence' / name)
for name in ['prepare_verifier_successor.py', 'verify_stream_recording.py', 'update_successor_tests.py',
             'run_tool_controls.py', 'finalize_tooling.py', 'finalize_tooling_02.py', 'freeze_tooling_successor.py']:
    copy_file(ROOT / name, DEST / 'authoring' / name)

fixture_index = []
for path in sorted((DEST / 'evidence').glob('*/control-evidence/*/observations.json')):
    value = json.loads(path.read_bytes())
    fixture_index.append({'test': value['test'], 'path': path.relative_to(DEST).as_posix(),
                          **identity(path), 'raw_inventory_entries': len(value['files']),
                          'metadata_scope': value['metadata_scope']})
assert len(fixture_index) == 128
write(DEST / 'retained-fixture-index.json', {'schema': 1, 'fixtures': fixture_index,
    'scope': '23 inherited focused fixtures +23 new owned fixtures +82 full-suite owned fixtures; pure controls use their exact source/log only'})
write(DEST / 'provenance.json', {
    'failed_hosted_run': {'commit': '5c402b43ce7851a49072e8a36e93c3d88b615f75', 'run': 38232050667,
        'job': 114753636437, 'artifact': 11739380591,
        'zip_sha256': 'b37c338cbfea7f6ce48e35c055e4b3ff1e501247526146a76dfdcf8a6141013e',
        'publication_commit': '029729b1c27b916c16eee6d36f3979681f79c7c8',
        'repo_path': 'docs/verification/day-numeric-hosted-run-5c402b4'},
    'source_successor': {'commit': bindings['source_commit'],
        'path': 'work-in-progress/day-trigger-numeric/08-command-filesystem-source-successor/checkpoint.json',
        **bindings['source_checkpoint']},
    'prior_tooling': {'commit': '5c402b43ce7851a49072e8a36e93c3d88b615f75',
        'path': 'work-in-progress/day-trigger-numeric/07-hosted-acceptance/checkpoint.json',
        'sha256': '994a29b51e3758cf9f3b32e5bd22a489009cfd45febb31f3d403572ffc1e9473'},
    'producer_cleanup_counterexample': {'commit': '0e5677a38a4d18f38fa14fc0736cc3502c6247ef',
        'path': 'docs/verification/day-numeric-hosted-review/05-producer-cleanup-error/checkpoint.json',
        'sha256': '157e4cc5ca0709a1c725091ac041fbee02b6edb91d21ddeff16323fae906730f'},
    'live_metadata_scope': 'Original live fstat/inode/ctime observed by the producer/verifier and retained in JSON. Copied/extracted inodes and ctimes are different and are never substituted.',
    'hosted_fixture_deltas_scope': 'The first failed hosted run retained the traceback but not its exact synthetic stat deltas. Separate actual local subprocess measurements are in the source08 capsule.'})

(DEST / 'README.md').write_text('''# Numeric hosted tooling successor

This nine-path proposal binds the unchanged 1,242-method application baseline to
the separately committed source08 numeric overlay at `811f979eda1b937917c18defef38455c49a59062`.
The source capsule changes only command-evidence instrumentation in one of its
nineteen files; its remaining eighteen files and all application semantics stay
byte-identical to source06. No full application build, Java/D8 stage or Android
execution occurred while preparing this tooling successor. The active app remains
unchanged, and a new hosted sixteen-gate result is still pending.

## Review index

- `nine-path-bindings.json` and `tooling-derivation.patch` bind all prior and proposed
  tool/workflow bytes. `source/` and `prior-source/` retain both complete versions.
- `source/tools/day_numeric_acceptance/README.md` documents the producer/verifier
  contract, exact source pins and full hosted acceptance scope.
- `evidence/08-complete-tooling-discovery/result.json` and its raw logs retain all
  **92 passing tooling tests**, executed in 3.888 seconds with all nine source files
  unchanged. Its `executed-source/` tree is byte-identical to this proposal.
- `evidence/07-final-tool-bindings-from-fetched-git/result.json` retains exact Git
  blob/mode verification, complete source-input derivation, unchanged preparation,
  identical producer ASTs, five Bash syntax checks and three CLI/import checks.
- `retained-fixture-index.json` locates all 128 owned fixture snapshots across the
  focused and complete checks, including every retained file and original stat.

## Recorded correction and limits

The original hosted 67-control failure is preserved unchanged in the published
raw artifact referenced by `provenance.json`. Its missing exact fixture stat values
are not invented here. The source08 capsule retains the separate measured
eight-child/sixteen-stream filesystem diagnosis, first thirteen producer controls,
exceptional-cleanup counterexample, corrected sixteen controls and complete future
81,298-file input manifest.

The independent verifier now checks exact integer Unix and monotonic clocks,
exclusive initial files, live final fstat/hash, one-inode/one-link ownership and
the complete bounded filesystem-witness sequence. It uses the first actual
bracket, with at most sixteen witnesses and a requested five-millisecond wait
between failed observations. It adds no timestamp tolerance. All 17 numeric
commands, JVM flags, paths and outcomes remain independently reconstructed.
Missing/reordered/borrowed witnesses, altered metadata/inodes, stale mtime, reversed
fine clocks, partial cleanup and extra witness selection are rejected. A Java
observation with an evidence error stops before the long acceptance child even
when that child observation returned zero.

The first successor focused batch passed 23 inherited envelope/process controls;
the second passed 25 new controls. The initial final-binding attempt then stopped
before any tool mutation because it assumed the publisher had materialized the
new capsule in the shared working tree. The publisher instead keeps its fetched
objects in a bare tmpfs repository. That exact failed read, script and source
identities remain under `evidence/06-final-tool-bindings`. The separate corrected
binding reads fixed Git blobs/tree entries directly, avoiding any application or
large source copy. It derives all expected input rows using the production pure
derivation function; it does not pretend that a full checkout/materialization or
the complete preparation command ran locally.

Live hosted verification and later artifact replay have different metadata
scopes. This verifier compares the original files while they exist; the artifact
preserves exact serialized observations and bytes. Extraction creates new inode
and ctime values. They must not be presented as the original hosted fstat.
The hosted test step now preserves raw fixture/stat observations outside the
application preparation/output scope so another early failure remains diagnosable.

All previous failures remain failures. A successful local tooling suite is not a
full sixteen-gate application result, APK promotion or complete runtime parity.
''')

files = []
for path in sorted(DEST.rglob('*')):
    assert not path.is_symlink(), path
    if path.is_file():
        files.append({'path': path.relative_to(DEST).as_posix(), **identity(path)})
pins = json.loads((SOURCE / 'tools/day_numeric_acceptance/pins.json').read_bytes())
allocated = sum(path.stat().st_blocks * 512 for path in ROOT.rglob('*') if path.is_file())
assert allocated + 2 * 1024 * 1024 < BUDGET, allocated
checkpoint = {'schema': 1, 'status': 'TOOLING_SUCCESSOR_REVIEW_READY_HOSTED_ACCEPTANCE_PENDING',
    'created_utc': datetime.now(timezone.utc).isoformat(), 'publication_path': PUBLICATION,
    'scope': 'Nine proposed tooling/workflow paths only; the new nineteen-file source capsule is already separately immutable',
    'active_application_modified': False, 'full_host_acceptance_executed': False,
    'signed_numeric_primary_packaging_verified': False, 'android_executed': False,
    'full_runtime_1_to_1_established': False, 'baseline_commit': pins['baseline_commit'],
    'source_overlay_commit': pins['overlay_commit'], 'source_overlay_checkpoint': pins['overlay_checkpoint'],
    'future_snapshot': pins['future_snapshot'], 'future_manifest': pins['future_manifest'],
    'local_verification': {'full_tool_tests': 92, 'seconds': full['unittest_seconds'],
        'focused_batches': [23, 25], 'retained_fixture_snapshots': 128, 'tool_sources_unchanged': True,
        'source_capsule_payloads_verified': 408, 'bash_syntax_checks': 5, 'cli_import_checks': 3},
    'active_files': active, 'runtime_manifest': identity(SOURCE / 'tools/day_numeric_acceptance/runtime-files.json'),
    'workflow': identity(SOURCE / '.github/workflows/day-numeric-wip-acceptance.yml'),
    'files': files, 'file_count': len(files), 'payload_bytes': sum(row['bytes'] for row in files),
    'owned_tmpfs_budget_bytes': BUDGET, 'owned_tmpfs_allocated_before_checkpoint': allocated}
write(DEST / 'checkpoint.json', checkpoint)
print(json.dumps({'checkpoint': str(DEST / 'checkpoint.json'), **identity(DEST / 'checkpoint.json'),
                  'files': len(files), 'payload_bytes': checkpoint['payload_bytes'],
                  'runtime_manifest': checkpoint['runtime_manifest'], 'workflow': checkpoint['workflow'],
                  'owned_tmpfs_allocated_before_checkpoint': allocated}, indent=2))
