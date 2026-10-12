#!/usr/bin/env python3
"""Freeze the one-file evidence-instrumentation successor without a source build."""
import ast
import copy
from datetime import datetime, timezone
import difflib
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
OLD = Path('/workspace/scratch/4130730d15aa/day-trigger-integration/checkpoints/04-source-acceptance-integration')
BASE = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')
PROJECT = ROOT / 'source-successor/project'
DEST = ROOT / 'checkpoints/01-command-filesystem-source-successor'
sys.path.insert(0, str(ROOT / 'baseline-source/tools/day_numeric_acceptance'))
import inputs


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def copy_tree(src, dst):
    dst.mkdir(parents=True, exist_ok=False)
    for path in sorted(src.rglob('*')):
        assert not path.is_symlink(), str(path)
        if path.is_file():
            target = dst / path.relative_to(src)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
            assert inputs.identity(path) == inputs.identity(target)


def body_review(old, new):
    a, b = ast.parse(old), ast.parse(new)
    names = {'command_clock', 'command_file_stat', 'CommandStreamEvidence'}
    def outside(tree):
        return ast.Module(body=[node for node in tree.body
            if not (isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in names | {'run_controls'})
            and not (isinstance(node, ast.Import) and [v.name for v in node.names] == ['stat'])], type_ignores=[])
    assert ast.dump(outside(a), include_attributes=False) == ast.dump(outside(b), include_attributes=False)
    arun = next(n for n in a.body if isinstance(n, ast.FunctionDef) and n.name == 'run_controls')
    brun = next(n for n in b.body if isinstance(n, ast.FunctionDef) and n.name == 'run_controls')
    achild = next(n for n in arun.body if isinstance(n, ast.FunctionDef) and n.name == 'run')
    bchild = next(n for n in brun.body if isinstance(n, ast.FunctionDef) and n.name == 'run')
    assert ast.dump(achild.args) == ast.dump(bchild.args)
    def invocation(node):
        calls = [n for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                 and isinstance(n.func.value, ast.Name) and n.func.value.id == 'subprocess' and n.func.attr == 'run']
        assert len(calls) == 1
        value = copy.deepcopy(calls[0])
        streams = {kw.arg: ast.unparse(kw.value) for kw in value.keywords if kw.arg in ('stdout', 'stderr')}
        value.keywords = [kw for kw in value.keywords if kw.arg not in ('stdout', 'stderr')]
        return ast.dump(value, include_attributes=False), streams
    acall, _ = invocation(achild)
    bcall, streams = invocation(bchild)
    assert acall == bcall
    assert streams == {'stdout': "streams.handles['stdout']", 'stderr': "streams.handles['stderr']"}
    class ClockOnly(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            if node.name == 'run':
                return ast.FunctionDef(name='run', args=node.args, body=[ast.Pass()], decorator_list=[], returns=None, type_comment=None)
            return self.generic_visit(node)
        def visit_Assign(self, node):
            if len(node.targets) == 1:
                target = ast.unparse(node.targets[0])
                if target in ('started', 'finished') and ast.unparse(node.value) == 'command_clock()':
                    return None
                if target == "report['finished_utc']":
                    return None
                if target == 'report' and isinstance(node.value, ast.Dict):
                    pairs = [(k, v) for k, v in zip(node.value.keys, node.value.values)
                             if not isinstance(k, ast.Constant) or k.value not in
                             {'schema', 'started_utc', 'started_unix_ns', 'started_monotonic_ns'}]
                    node.value.keys, node.value.values = map(list, zip(*pairs))
            return self.generic_visit(node)
        def visit_Expr(self, node):
            if (isinstance(node.value, ast.Call) and ast.unparse(node.value.func) == 'report.update'
                    and {k.arg for k in node.value.keywords} == {'finished_utc', 'finished_unix_ns', 'finished_monotonic_ns'}):
                return None
            return self.generic_visit(node)
    normalize = lambda node: ast.dump(ClockOnly().visit(copy.deepcopy(node)), include_attributes=False)
    assert normalize(arun) == normalize(brun), 'Unexpected non-recording change in run_controls'
    return {'all_top_level_non_recording_nodes_exact_ast': True,
            'run_controls_after_only_clock_report_and_nested_runner_normalization_exact_ast': True,
            'nested_runner_signature_unchanged': True,
            'actual_subprocess_run_argv_cwd_timeout_exact_ast': True,
            'stdout_stderr_still_passed_as_open_file_descriptors': streams}


def main():
    DEST.mkdir(parents=True, exist_ok=False)
    old_checkpoint = inputs.read_json(OLD / 'checkpoint.json')
    assert inputs.identity(OLD / 'checkpoint.json')['sha256'] == 'c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f'
    pins = inputs.read_json(ROOT / 'baseline-source/tools/day_numeric_acceptance/pins.json')
    before = inputs.identity(BASE / 'reports/release-input-snapshot.json')
    assert before == {k: pins['baseline_manifest'][k] for k in ('bytes', 'sha256')}
    baseline = inputs.validate_snapshot(inputs.read_json(BASE / 'reports/release-input-snapshot.json'))
    old_future = inputs.derive(baseline, old_checkpoint['source_changes'])
    assert {k: old_future[k] for k in ('files', 'snapshot_sha256')} == pins['future_snapshot']
    assert inputs.byte_identity(inputs.encoded(old_future)) == pins['future_manifest']
    changes = copy.deepcopy(old_checkpoint['source_changes'])
    retained, changed = [], []
    for row in changes:
        current = inputs.identity(PROJECT / row['path'])
        prior = inputs.identity(OLD / row['source'])
        assert prior == row['candidate']
        item = {'path': row['path'], 'prior': prior, 'successor': current}
        if current != prior:
            changed.append(item)
            assert row['path'] == 'day_numeric_dex_controls.py'
            row['candidate'] = current
        else:
            retained.append(item)
    assert len(changed) == 1 and len(retained) == 18 and len(changes) == 19
    future = inputs.derive(baseline, changes)
    assert future['files'] == old_future['files'] == 81298
    assert [name for name in future['entries'] if future['entries'][name] != old_future['entries'][name]] == ['day_numeric_dex_controls.py']
    raw = inputs.encoded(future)
    compressed = gzip.compress(raw, mtime=0)
    (DEST / 'evidence').mkdir()
    (DEST / 'evidence/future-input-snapshot.json.gz').write_bytes(compressed)
    assert gzip.decompress(compressed) == raw
    old_text = (OLD / 'project/day_numeric_dex_controls.py').read_text()
    new_text = (PROJECT / 'day_numeric_dex_controls.py').read_text()
    review = body_review(old_text, new_text)
    (DEST / 'evidence/source-derivation.patch').write_text(''.join(difflib.unified_diff(old_text.splitlines(keepends=True), new_text.splitlines(keepends=True),
        fromfile='source06/project/day_numeric_dex_controls.py', tofile='successor/project/day_numeric_dex_controls.py')))
    copy_tree(PROJECT, DEST / 'project')
    copy_tree(ROOT / 'reports/01-unchanged-guard-diagnosis', DEST / 'evidence/unchanged-guard-diagnosis')
    copy_tree(ROOT / 'baseline-source', DEST / 'evidence/exact-failed-job-source')
    copy_tree(ROOT / 'reports/02-producer-controls-attempt-01', DEST / 'evidence/producer-controls-attempt-01')
    copy_tree(ROOT / 'reports/03-producer-controls-attempt-02', DEST / 'evidence/producer-controls-attempt-02')
    for name in ('diagnose_timestamps.py', 'prepare_successor_sources.py', 'test_source_stream_recording.py',
                 'command_stream_recording.py', 'freeze_source_successor.py'):
        shutil.copyfile(ROOT / name, DEST / name)
    shutil.copyfile(ROOT / 'reports/03-producer-controls-attempt-02/executed-source/run_acceptance.py',
                    DEST / 'evidence/producer-controls-attempt-02/executed-wrapper.py')
    source_proof = inputs.read_json(DEST / 'evidence/producer-controls-attempt-02/result.json')
    assert source_proof['passed'] is True and source_proof['tests_run'] == 16 and source_proof['errors'] == source_proof['failures'] == []
    assert source_proof['source_before'] == source_proof['source_after']
    assert source_proof['source_after'][str(PROJECT / 'day_numeric_dex_controls.py')] == changed[0]['successor']
    empty = [r for r in source_proof['actual_process_records'] if 'eight_real_empty' in r['test']]
    assert len(empty) == 8
    equal_ticks = sum(len({v['initial_stat']['ctime_ns'] for v in r['row']['stream_evidence']['streams'].values()}) == 1 for r in empty)
    binding = {'schema': 1, 'status': 'ONE_RECORDING_FILE_CHANGED_18_SOURCE_FILES_EXACT',
        'active_promoted': False, 'application_build_executed': False, 'java_or_d8_executed_in_this_successor': False,
        'android_runtime_executed': False, 'full_runtime_1_to_1_established': False,
        'prior_source_commit': '394234b0e74c9f1d660836c8f2a89901fe05ff9d',
        'prior_checkpoint': inputs.identity(OLD / 'checkpoint.json'), 'baseline_manifest': before,
        'old_future_snapshot': pins['future_snapshot'], 'future_snapshot': {k: future[k] for k in ('files', 'snapshot_sha256')},
        'future_manifest': inputs.byte_identity(raw),
        'full_future_manifest_container': {'path': 'evidence/future-input-snapshot.json.gz', **inputs.byte_identity(compressed),
                                          'decompressed_identity': inputs.byte_identity(raw), 'complete_entries': 81298},
        'changed_source': changed, 'retained_18_source_files': retained, 'body_review': review,
        'focused_source_controls': 16, 'actual_empty_subprocesses': 8, 'pairs_with_equal_initial_filesystem_ticks': equal_ticks,
        'expected_method_class_counts_unchanged_from_source06': {'registered_methods': 1243, 'target_classes': 605,
                                                              'fixture_methods': 1246, 'fixture_classes': 607},
        'full_16_host_gates': 'PENDING; this source successor has not been built',
        'metadata_scope': 'Producer controls observed live fstat; copied/archived files do not preserve original inode or ctime. Recorded raw observations are retained unchanged.'}
    write(DEST / 'evidence/source-binding.json', binding)
    write(DEST / 'provenance.json', {
        'prior_source': {'commit': '394234b0e74c9f1d660836c8f2a89901fe05ff9d', 'path': 'work-in-progress/day-trigger-numeric/06-source-integration/checkpoint.json',
                         'sha256': 'c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f'},
        'failed_hosted_run': {'run': 38232050667, 'job': 114753636437, 'commit': '5c402b43ce7851a49072e8a36e93c3d88b615f75',
            'artifact': 11739380591, 'zip_sha256': 'b37c338cbfea7f6ce48e35c055e4b3ff1e501247526146a76dfdcf8a6141013e',
            'published_at': '029729b1c27b916c16eee6d36f3979681f79c7c8', 'repo_path': 'docs/verification/day-numeric-hosted-run-5c402b4'},
        'cleanup_counterexample': {'commit': '0e5677a38a4d18f38fa14fc0736cc3502c6247ef',
            'path': 'docs/verification/day-numeric-hosted-review/05-producer-cleanup-error/checkpoint.json',
            'sha256': '157e4cc5ca0709a1c725091ac041fbee02b6edb91d21ddeff16323fae906730f'},
        'primary_references': ['https://cdn.kernel.org/doc/html/latest/filesystems/multigrain-ts.html',
            'https://cdn.kernel.org/doc/html/latest/core-api/timekeeping.html', 'https://docs.python.org/3.12/library/datetime.html']})
    (DEST / 'README.md').write_text('''# Numeric command filesystem evidence successor

This inactive source capsule changes only `day_numeric_dex_controls.py` from the previously frozen nineteen-file overlay. The other eighteen source files, every Java body, the original fixture, helper/D8 identities, command arguments, 120-second subprocess timeout, and application acceptance expectations remain unchanged. The complete future input manifest has 81,298 entries and is retained in a lossless gzip container; `evidence/source-binding.json` pins both its compressed and decompressed bytes.

## Actual failure and diagnosis

Hosted run 38232050667 failed before materialization or application build: 67 tooling tests ran, with 64 successes, two errors and one dependent failure. The exact twelve-member raw artifact is preserved at `docs/verification/day-numeric-hosted-run-5c402b4/`. That log did not retain the failing fixtures' exact stat values, so this capsule does not invent hosted nanosecond deltas.

The unchanged-source diagnosis separately ran 32 synthetic numeric fixtures and 32 wrapper fixtures successfully on local tmpfs. Eight actual empty Python subprocesses then produced sixteen streams whose mtime/ctime were earlier than their recorded precise wall-clock start, despite exclusive creation after that start. All exact observations and original source are retained. The kernel documentation explains that inode times can use coarse clock values; Python datetime records microseconds, and conversion through a floating-point timestamp introduces an additional precision loss. These are distinct limitations.

## Exact producer contract

Each command records integer Unix and monotonic nanoseconds. ISO text is derived from that same Unix value using integer seconds and microseconds. Before opening stdout/stderr it exclusively creates an empty filesystem witness in the same directory. Each stream is opened with `xb`; the producer records its open-operation clocks, initial empty fstat/hash, final fstat/hash, and closure clocks. The file must retain one regular inode and one link.

After both streams close, the producer creates and retains filesystem witnesses until the actual timestamp of one brackets all recorded initial/final stream timestamps. A coarse filesystem clock may need to advance after a fine write timestamp, so this is a bounded observation sequence: at most sixteen separate empty witnesses, with a requested five-millisecond wait between failed observations (at most fifteen waits). It uses the first actual bracket, never changes timestamps, never discards unsuccessful witnesses, and never adds a timestamp tolerance. If no bracket is observed, the command evidence fails. The real subprocess timeout remains exactly the existing caller-supplied timeout.

The first producer attempt passed thirteen controls but an independent review found an exceptional-I/O cleanup gap. Its exact source/results and the published counterexample remain preserved. The corrected attempt passed sixteen controls: both producer copies share an identical helper AST; actual empty/nonempty/nonzero subprocess outputs are retained; preexisting files/symlinks, borrowed witnesses, inode/link substitution and an actual stale mtime are rejected. Additional injected flush-plus-close errors demonstrate cleanup of the other owned stream, retention of the original exception, and a recorded finish. These are host producer/evidence controls, with no Java, D8, application build, or Android execution.

## Verification scope

The successor independent hosted verifier will compare recorded metadata against the live files, enforce both integer-clock orderings, exact argv/path/hash/physical ownership, complete witness ordering, and the first actual bracket. It is still being prepared separately; the full sixteen application gates remain pending. Archived fstat values describe the host observations at capture time. Extraction does not preserve original inode or ctime, and an archive replay must not treat extraction metadata as the hosted filesystem observation.

Primary documentation: [Linux multigrain timestamps](https://cdn.kernel.org/doc/html/latest/filesystems/multigrain-ts.html), [Linux timekeeping accessors](https://cdn.kernel.org/doc/html/latest/core-api/timekeeping.html), and [Python datetime](https://docs.python.org/3.12/library/datetime.html).
''')
    files = []
    for path in sorted(DEST.rglob('*')):
        assert not path.is_symlink()
        if path.is_file():
            files.append({'path': path.relative_to(DEST).as_posix(), **inputs.identity(path)})
    checkpoint = {'schema': 1, 'status': 'INACTIVE_NUMERIC_COMMAND_FILESYSTEM_EVIDENCE_SUCCESSOR',
                  'created_utc': datetime.now(timezone.utc).isoformat(),
                  'repo_target': 'work-in-progress/day-trigger-numeric/08-command-filesystem-source-successor',
                  'active_files': [], 'source_changes': changes, 'future_snapshot': binding['future_snapshot'],
                  'future_manifest': binding['future_manifest'], 'files': files}
    write(DEST / 'checkpoint.json', checkpoint)
    print(json.dumps({'checkpoint': str(DEST / 'checkpoint.json'), **inputs.identity(DEST / 'checkpoint.json'),
                      'files': len(files), 'payload_bytes': sum(v['bytes'] for v in files),
                      'future_snapshot': binding['future_snapshot'], 'future_manifest': binding['future_manifest']}))


if __name__ == '__main__':
    main()
