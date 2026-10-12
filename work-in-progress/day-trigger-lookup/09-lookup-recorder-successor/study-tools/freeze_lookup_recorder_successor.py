#!/usr/bin/env python3
"""Freeze the two-path command-evidence correction and its exact future inputs."""
from pathlib import Path
from datetime import datetime, timezone
import gzip
import hashlib
import json
import shutil
import tarfile

ROOT = Path(__file__).resolve().parent
PARENT = ROOT / 'checkpoints/04-numeric-filesystem-merge'
STAGE = ROOT / 'stage-04'
SOURCE = ROOT / 'reports/19-lookup-recorder-source-successor'
TESTS = ROOT / 'reports/20-lookup-recorder-focused-controls'
TARGET = ROOT / 'checkpoints/05-lookup-recorder-successor'


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest, 'mode': path.stat().st_mode & 0o777}


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def copy(path, name):
    target = TARGET / name; target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target); assert identity(target) == identity(path)


def main():
    assert not TARGET.exists(); TARGET.mkdir(parents=True)
    assert identity(PARENT / 'checkpoint.json')['sha256'] == '56aa7bfc05286d9fc474d24e6afc33fbd3a664e9dc731f70912df1a9e375b350'
    proof = json.loads((STAGE / 'source-derivation.json').read_text())
    assert len(proof['edited_paths']) == 2
    tests = json.loads((TESTS / 'result.json').read_text())
    assert tests['passed'] is True and tests['tests_run'] == 57 and tests['failures'] == tests['errors'] == tests['skipped'] == 0
    assert tests['test_module_counts'] == {'test_day_numeric.DayNumericCatalogTests': 8, 'test_day_lookup': 49}
    changes = proof['edited_paths']
    for row in changes:
        assert identity(STAGE / 'project' / row['path']) == row['after']
        assert identity(PARENT / 'project' / row['path']) == row['baseline']
        copy(STAGE / 'project' / row['path'], 'project/' + row['path'])
    copy(STAGE / 'project/day_numeric_dex_controls.py', 'unchanged-provider/day_numeric_dex_controls.py')
    assert identity(STAGE / 'project/day_numeric_dex_controls.py')['sha256'] == '2608a9a0a9d5b44627595fcbb696f2ec3f70213eb6af88a7282ec818d53e92f4'
    parent_manifest = json.loads((PARENT / 'merge-manifest.json').read_text())
    complete = json.loads((PARENT / 'merge-manifest.json').read_text())
    for row in complete['changes']:
        replacement = next((value for value in changes if value['path'] == row['path']), None)
        if replacement is not None:
            assert row['after'] == replacement['baseline']
            row['lookup08_candidate'] = row['after']; row['after'] = replacement['after']
            row['payload_source'] = 'this-capsule/project/' + row['path']
        else:
            row['payload_source'] = 'lookup08-56aa7bfc/project/' + row['path']
        assert identity(STAGE / 'project' / row['path']) == row['after']
    complete.update(recorder_successor_edited_paths=2, total_future_overlay_paths=21,
                    lookup08_checkpoint_sha256=identity(PARENT / 'checkpoint.json')['sha256'])
    save(TARGET / 'complete-future-overlay-manifest.json', complete)
    for source, name in [(STAGE / 'source-derivation.json', 'source-derivation.json'),
                         (SOURCE / 'day_lookup_dex_controls.py.patch', 'day_lookup_dex_controls.py.patch'),
                         (SOURCE / 'test_day_lookup.py.patch', 'test_day_lookup.py.patch')]:
        copy(source, name)
    old_bytes = gzip.decompress((PARENT / 'future-input-snapshot.json.gz').read_bytes())
    old = json.loads(old_bytes)
    assert old['snapshot_sha256'] == '1c4782766c3a2d309a9228262435e46e420455f839093654bfe6e7e5c47277d0'
    assert hashlib.sha256(old_bytes).hexdigest() == '96dc48fd99daa8cec999516f7d5701a0283bd125f706e7c0b03490183c4ab35a'
    assert old['snapshot_sha256'] == hashlib.sha256(json.dumps(old['entries'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    future = json.loads(old_bytes)
    for row in changes:
        assert future['entries'][row['path']] == {'size': row['baseline']['bytes'], 'sha256': row['baseline']['sha256']}
        future['entries'][row['path']] = {'size': row['after']['bytes'], 'sha256': row['after']['sha256']}
    assert future['files'] == len(future['entries']) == 81304
    assert all(future['entries'][key] == value for key, value in old['entries'].items()
               if key not in {row['path'] for row in changes})
    future['snapshot_sha256'] = hashlib.sha256(json.dumps(future['entries'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    raw = json.dumps(future, indent=2).encode()
    (TARGET / 'future-input-snapshot.json.gz').write_bytes(gzip.compress(raw, mtime=0))
    future_binding = {'scope': 'Complete derived future manifest; no full tree was materialized or rehashed.',
                      'parent_checkpoint_sha256': identity(PARENT / 'checkpoint.json')['sha256'],
                      'baseline_manifest_bytes': len(old_bytes), 'baseline_manifest_sha256': hashlib.sha256(old_bytes).hexdigest(),
                      'changed_existing_entries': 2, 'new_entries': 0, 'unchanged_entries': 81302,
                      'future_snapshot': {key: future[key] for key in ('files', 'snapshot_sha256')},
                      'future_manifest': {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()},
                      'compressed_manifest': identity(TARGET / 'future-input-snapshot.json.gz')}
    save(TARGET / 'future-manifest-derivation.json', future_binding)
    observations = []
    for path in sorted((TESTS / 'recorder-cases').glob('*/observation.json')):
        observed = json.loads(path.read_text()); report = observed['acceptance_report']
        assert report['passed'] is False and report['status'] == 'LOOKUP_DEX_CONTROL_FAILED'
        assert len(report['commands']) == 1
        row = report['commands'][0]
        assert row['recording_finalized']['monotonic_ns'] <= report['finished_monotonic_ns']
        observations.append({'test': path.parent.name, 'observation': identity(path), 'report_status': report['status'],
                             'recorded_commands': 1, 'returncode': row['returncode'], 'error_type': row['error_type'],
                             'timed_out': row['timed_out'], 'stream_context_entered': row['stream_context_entered'],
                             'context_finished': 'finished' in row['stream_evidence'],
                             'cleanup_errors': row['stream_evidence'].get('cleanup_errors', []),
                             'injected_context_handles_closed': observed['context_handles_closed']})
    assert len(observations) == 16
    assert len(list((TESTS / 'recorder-cases').glob('*/child-reaped.json'))) == 2
    save(TARGET / 'recorder-case-summary.json', observations)
    for name in ['prepare_lookup_recorder_successor.py', 'lookup_recorder_tests.py.txt',
                 'run_lookup_recorder_controls.py', 'freeze_lookup_recorder_successor.py']:
        copy(ROOT / name, 'study-tools/' + name)
    evidence = []
    for folder in [SOURCE, TESTS]:
        for path in sorted(folder.rglob('*')):
            if path.is_file():
                assert not path.is_symlink()
                evidence.append((path, 'reports/' + folder.name + '/' + path.relative_to(folder).as_posix()))
    rows = [{'path': name, **identity(path)} for path, name in evidence]
    save(TARGET / 'evidence-files.json', rows)
    archive = TARGET / 'evidence.tar.gz'
    with tarfile.open(archive, 'w:gz', dereference=True) as tar:
        for path, name in evidence:
            tar.add(path, arcname=name, recursive=False)
    with tarfile.open(archive) as tar:
        members = tar.getmembers(); assert len(members) == len(rows)
        for member, row in zip(members, rows):
            assert member.isfile() and member.name == row['path'] and member.size == row['bytes'] and member.mode & 0o777 == row['mode']
            assert hashlib.sha256(tar.extractfile(member).read()).hexdigest() == row['sha256']
    for folder in [SOURCE, TESTS]:
        for path in sorted(folder.rglob('*')):
            if path.is_file() and path.name in {'result.json', 'unittest.log', 'observation.json', 'child-reaped.json',
                                                'day-lookup-dex-controls.json', 'loaded-runner-identities.json'}:
                copy(path, 'review/' + folder.name + '/' + path.relative_to(folder).as_posix())
    (TARGET / 'MEASURED_COUNT_CORRECTION.md').write_text('''# Planned versus measured focused-test count

The executed driver's scope string said nine numeric catalog/dependency guards. The actual class contains **eight** tests. The closed result, log and executed driver are retained unchanged. The measured counts are **49 lookup tests** (33 prior controls plus 16 new recorder controls) and **eight numeric catalog/dependency tests**, totaling **57**, with zero failures, errors or skips. No test was omitted to reconcile the label, and no additional run is claimed.
''')
    doc = f'''# Lookup recorder: explicit shared schema-2 evidence and retained failure rows

This inactive successor changes exactly **two paths** from frozen Lookup08 checkpoint `56aa7bfc05286d9fc474d24e6afc33fbd3a664e9dc731f70912df1a9e375b350`: day_lookup_dex_controls.py and tests/test_day_lookup.py. It repairs the two measured recorder limitations while preserving the exact application proof and command inputs. **All 57 focused tests passed** in {tests['seconds']:.6f} seconds. Every recorder exercise still produces a deliberately failed acceptance report; this is not a signed or full-project acceptance result.

## Source changes and provider contract

The lookup source is 35,479 bytes, SHA-256 `0b72325dbdaf60525f07a7b72708b9096d1e585ef5e1601332ceaac9aa67c8c9`. The old `aaf53f9c105727c7b68f7e78b5bed0d0b89ff7772452fc6aaf51315cb73bd208` source and its real accepted-hardlink/missing-row evidence remain untouched in Lookup08. The updated 49-test lookup module is 32,426 bytes, SHA-256 `b819d42007f3345023420b5cfac4c4463309eed7c62b5bc654fdbc2ce1413972`.

The nested production recorder directly uses **numeric.CommandStreamEvidence** and **numeric.command_clock**. Their exact 40,949-byte provider file remains SHA-256 `2608a9a0a9d5b44627595fcbb696f2ec3f70213eb6af88a7282ec818d53e92f4`; no shared implementation was copied, modified or weakened. Outer lookup evidence now explicitly declares schema 2, command stream schema 2, and the provider's fully qualified name. The ordinary Java/DEX harness reports retain their prior schema and exact validation rules.

The shared context records exclusive regular single-link files, descriptor/path identity through closure, hashes, integer wall and monotonic clocks, and actual bounded before/after filesystem witnesses. An additional hardlink changes ownership and is rejected. The lookup wrapper finalizes and saves one failed command row after open, child, flush and close errors instead of losing the row when cleanup raises.

Each row adds the actual expected exit code, observed error type/repr and an observed TimeoutExpired flag. A separate recording_finalized clock records the wrapper's actual finalization. Pre-existing-output failures preserve the prior RuntimeError and never enter the shared stream context; their stream_context_entered flag is false and no context-finish timestamp is invented. This distinction is visible in the retained rows and must remain visible to future evidence validation.

The complete application try body and handlers are AST-identical. Every other top-level lookup definition is unchanged. All application run-call ASTs and the subprocess argv/cwd/timeout arguments are exact; the only subprocess redirection change is to the shared context's real handles. All application expectations, Java/D8 commands, nonzero expectations, coverage gates, source checks, signed-primary comparison and positive restoration remain intact. The shared numeric file and all other 23 small source-subset files are byte-identical to Lookup08. The old 33 lookup tests are an exact source prefix; 16 recording controls were appended.

## What actually executed

The focused test run measured **49 lookup tests and eight numeric catalog/dependency tests**, or 57. The original planned scope string's nine-test numeric count was wrong; MEASURED_COUNT_CORRECTION.md explains it without changing the closed driver/result. No Java, D8, APK, application method or Android process ran in this study. All loaded modules, original sources and copied test inputs were checked unchanged after execution.

Sixteen tests enter the actual production run_controls function. A private hook at its first application-input boundary obtains and checks the live nested recorder's code identity. Real bounded Python children cover empty and nonempty output, expected and unexpected exit 7, timeout, missing executable, inode replacement and an extra hardlink. Explicit controlled I/O failures cover the second stream open, flush, close, both flush and close, and timeout combined with both cleanup failures. The fault factory still constructs the exact original numeric context class; only the designated test file-operation handle fails. Injected exception object identity, primary-error priority and closure of every captured handle are checked.

Both actual timeout cases independently confirm the owned child has exited and been reaped. All 16 attempts retain exactly one finalized command row. In all 16 production reports, passed is false and status is LOOKUP_DEX_CONTROL_FAILED. Successful recorder calls stop with an explicit boundary sentinel; no application-input validation or signed-proof gate is bypassed into success. These tests earn zero application-case or instruction credit.

The real additional-hardlink case is now rejected with an ownership error. The replaced-inode case retains its failed command row. Partial stream receipts and cleanup errors remain present on failures; they are never upgraded to complete passing evidence. Report-file write/storage failure itself was not fault-injected here, and no durability claim beyond the successfully retained files is made.

## Exact future integration

The total future application overlay remains **21 paths**; this successor changes only two of them. complete-future-overlay-manifest.json binds those two payloads here and the other 19 unchanged payloads to Lookup08. The complete future manifest changes two existing entries, preserves the other 81,302 rows and remains **81,304 files**. Its new snapshot SHA-256 is `{future['snapshot_sha256']}`; the decompressed JSON is {len(raw):,} bytes, SHA-256 `{hashlib.sha256(raw).hexdigest()}`. This is a guarded complete-inventory derivation, not a freshly materialized full checkout.

The inherited 371-input original/JVM/micro-D8 proof and compiled semantic fault results remain bound to unchanged helper, harness and fixture sources. No new application case total is claimed. The future 1,244-body/605-class source still requires a fresh full build, actual signed-primary binding for both ordinary DayTrigger methods, all 101 Java faults, both numeric and lookup D8/provenance/restoration gates and all 16 acceptance commands. Those gates remain pending.

The full evidence archive preserves every source and command attempt, including deliberately failed acceptance reports, raw stdout/stderr, clocks, inode/link observations, witness files, injected I/O traces and closed source manifests. It stores independent byte copies of intentional hardlinks; the raw study retains the original physical links and their exact observed metadata.
'''
    (TARGET / 'CHECKPOINT_SCOPE.md').write_text(doc)
    assert all(identity(path) == {key: row[key] for key in ('bytes', 'sha256', 'mode')}
               for (path, _), row in zip(evidence, rows))
    files = [{'path': path.relative_to(TARGET).as_posix(), **identity(path)}
             for path in sorted(TARGET.rglob('*')) if path.is_file()]
    checkpoint = {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
                  'status': 'INACTIVE_TWO_PATH_LOOKUP_RECORDER_SUCCESSOR_FOCUSED_CONTROLS_PASSED',
                  'repo_target': 'work-in-progress/day-trigger-lookup/09-lookup-recorder-successor',
                  'parent_checkpoint_sha256': identity(PARENT / 'checkpoint.json')['sha256'],
                  'source_path_count': 2, 'complete_future_overlay_path_count': 21,
                  'future_manifest': future_binding['future_manifest'], 'future_snapshot': future_binding['future_snapshot'],
                  'focused_tests': 57, 'actual_production_recorder_controls': 16,
                  'production_acceptance_reports_passed': 0, 'application_executions': 0,
                  'active_source_changed': False, 'full_build_or_signing': False, 'new_apk': False,
                  'evidence_file_count': len(rows), 'evidence_archive': identity(archive), 'files': files}
    save(TARGET / 'checkpoint.json', checkpoint)
    print(json.dumps({'checkpoint': str(TARGET / 'checkpoint.json'), **identity(TARGET / 'checkpoint.json'),
                      'direct_files': len(files), 'evidence_files': len(rows), 'evidence_archive': identity(archive),
                      'future_snapshot': future_binding['future_snapshot']}, indent=2))
    assert sum(path.stat().st_size for path in ROOT.rglob('*') if path.is_file()) <= 256 * 1024 * 1024


if __name__ == '__main__':
    main()
