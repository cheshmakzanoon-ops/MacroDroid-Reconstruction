#!/usr/bin/env python3
"""Freeze the bounded guarded merge and separate actual recorder diagnostics."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import gzip
import hashlib
import json
import shutil
import tarfile

ROOT = Path(__file__).resolve().parent
STAGE = ROOT / 'stage-03'
TARGET = ROOT / 'checkpoints/04-numeric-filesystem-merge'
MERGE = ROOT / 'reports/16-numeric-successor-merge'
TESTS = ROOT / 'reports/17-merged-focused-guards'
RECORDER = ROOT / 'reports/18-actual-lookup-recorder'


def identity(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest, 'mode': path.stat().st_mode & 0o777}


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def copy(path, name):
    target = TARGET / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)
    assert identity(target) == identity(path)


def main():
    assert not TARGET.exists()
    TARGET.mkdir(parents=True)
    manifest = json.loads((STAGE / 'merge-manifest.json').read_text())
    changes = manifest['changes']
    assert len(changes) == len({row['path'] for row in changes}) == 21
    for row in changes:
        source = STAGE / 'project' / row['path']
        assert identity(source) == row['after']
        if row['baseline'] is not None:
            assert identity(Path(row['baseline_source'])) == row['baseline']
        if source.suffix == '.py':
            ast.parse(source.read_text())
        copy(source, 'project/' + row['path'])
    for name, expected in json.loads((MERGE / 'merged-source-identities.json').read_text()).items():
        assert identity(STAGE / 'project' / name) == expected
        if name not in {row['path'] for row in changes}:
            copy(STAGE / 'project' / name, 'unchanged-numeric-support/' + name)
    merge = json.loads((MERGE / 'result.json').read_text())
    tests = json.loads((TESTS / 'result.json').read_text())
    recorder = json.loads((RECORDER / 'result.json').read_text())
    assert merge['passed'] is True and merge['edited_or_new_paths'] == 21 and merge['merge_guard_controls'] == 8
    assert tests['passed'] is True and tests['tests_run'] == 76 and tests['failures'] == tests['errors'] == tests['skipped'] == 0
    assert recorder['exercise_completed'] is True and recorder['cases_observed'] == 8 and recorder['production_acceptance_reports_passed'] == 0
    assert recorder['application_executions'] == recorder['method_or_instruction_coverage_credit'] == 0
    future = json.loads(gzip.decompress((MERGE / 'future-input-snapshot.json.gz').read_bytes()))
    assert future['files'] == len(future['entries']) == 81304
    assert future['snapshot_sha256'] == hashlib.sha256(json.dumps(future['entries'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert {key: future[key] for key in ('files', 'snapshot_sha256')} == merge['future_snapshot']
    for row in changes:
        assert future['entries'][row['path']] == {'size': row['after']['bytes'], 'sha256': row['after']['sha256']}
    for source, name in [
        (STAGE / 'merge-manifest.json', 'merge-manifest.json'),
        (MERGE / 'future-input-snapshot.json.gz', 'future-input-snapshot.json.gz'),
        (MERGE / 'future-manifest-derivation.json', 'future-manifest-derivation.json'),
        (MERGE / 'three-way-ast-and-text-proof.json', 'three-way-ast-and-text-proof.json'),
        (MERGE / 'numeric08-to-merged.patch', 'numeric08-to-merged.patch'),
        (MERGE / 'lookup07-to-merged.patch', 'lookup07-to-merged.patch'),
        (RECORDER / 'bound-production-recorder.txt', 'bound-production-recorder.txt'),
    ]:
        copy(source, name)
    for name in ['merge_numeric_successor.py', 'run_merged_focused_guards.py',
                 'exercise_lookup_production_recorder.py', 'freeze_numeric_lookup_merge.py']:
        copy(ROOT / name, 'study-tools/' + name)
    rows = []
    evidence = []
    for folder in [MERGE, TESTS, RECORDER]:
        for path in sorted(folder.rglob('*')):
            if path.is_file():
                assert not path.is_symlink()
                name = 'reports/' + folder.name + '/' + path.relative_to(folder).as_posix()
                rows.append({'path': name, **identity(path)})
                evidence.append((path, name))
    save(TARGET / 'evidence-files.json', rows)
    archive = TARGET / 'evidence.tar.gz'
    # Store each file's bytes independently. The recorder's deliberate extra
    # hardlink remains physically untouched in the raw study; its observed inode
    # and two-link metadata are separately retained in the exact observations.
    with tarfile.open(archive, 'w:gz', dereference=True) as tar:
        for path, name in evidence:
            tar.add(path, arcname=name, recursive=False)
    with tarfile.open(archive) as tar:
        members = tar.getmembers()
        assert len(members) == len(rows)
        for member, row in zip(members, rows):
            assert member.isfile() and member.name == row['path'] and member.size == row['bytes']
            assert member.mode & 0o777 == row['mode']
            assert hashlib.sha256(tar.extractfile(member).read()).hexdigest() == row['sha256']
    for folder in [MERGE, TESTS, RECORDER]:
        for path in sorted(folder.rglob('*')):
            if path.is_file() and (path.name in {'result.json', 'observation.json', 'production-code-binding.json',
                                                'merge-guard-controls.json', 'unittest.log', 'failure.traceback.txt'}
                                   or path.name == 'day-lookup-dex-controls.json'):
                copy(path, 'review/' + folder.name + '/' + path.relative_to(folder).as_posix())
    scope = '''# Lookup dependency integration with the numeric filesystem recorder

The approved **21-path lookup overlay is merged in an isolated source subset** with the frozen numeric command-recorder successor. Eight source/inventory guard controls and all 76 focused numeric, lookup and existing Widget catalog tests passed. A separate exercise reached the lookup runner's actual nested recorder and exposed two concrete evidence limitations; every resulting production acceptance report remains failed. This capsule contains no complete APK build, signed candidate, Android execution or active-source promotion.

## Exact source ancestry and merge

| Input | Frozen checkpoint SHA-256 | Role |
| --- | --- | --- |
| Numeric19 | `c59d9624844864de085723167ed67af017ed6e0ef17e06ba0206a33649e92b2f` | Common source ancestor |
| Lookup07 | `d40df7530d090b6717d99e5011f1a0e5c0774297576ecc88047737301812a292` | Complete 21-path lookup overlay and bounded original/JVM/micro-D8 proof |
| Numeric08 | `d9ddd3e0f692c66e2cd47870ff3cf95bfa0a2b1cd50fc2fd55a3c09e66df9bcf` | Frozen numeric filesystem-recorder successor |

The merged day_numeric_dex_controls.py is 40,949 bytes, SHA-256 `2608a9a0a9d5b44627595fcbb696f2ec3f70213eb6af88a7282ec818d53e92f4`. It applies precisely the prior lookup dependency-hash and declaration/validator splices to the exact 39,491-byte numeric successor, SHA-256 `10bd78a41dcc9f16e0a301229e7b714189fd3bf7e497c5b35c49c7ccbcfd9e7c`.

The complete source outside those two splices is byte-identical to Numeric08. Full top-level AST and text comparisons additionally prove that command_clock, command_file_stat, CommandStreamEvidence and all of run_controls retain their exact source. Every child command, argv, timeout, file operation and recorder exception boundary is preserved. The five dependency AST nodes match Lookup07 exactly. All other 20 lookup files and all other 18 numeric-successor files retain their frozen bytes. The four unchanged numeric supporting files are provided under unchanged-numeric-support; they add no edited path to the approved 21-path scope.

The eight merge guards reject altered ancestor bytes, a substituted recorder clock, loosened duplicate-consumer validation, a rehashed wrong baseline module row, a rehashed pre-existing allegedly new path, and a widened source domain. These are source/inventory controls with no application-execution credit.

The focused run passed 35 numeric, 33 lookup and eight existing Widget catalog tests, with zero failures, errors or skips. It bound the actual loaded numeric and lookup modules to their exact copied sources. All executed copies and their original input sources were rehashed unchanged after the run. Numeric selection tests execute the real bounded Java selector; this is not an all-suite application parity rerun.

## Complete future input inventory

The verified Numeric08 manifest contains 81,298 entries. This derivation changes exactly 15 existing rows, requires six new lookup paths to be absent, and retains all other 81,283 rows exactly. The resulting complete future inventory has **81,304 files**, snapshot SHA-256 `1c4782766c3a2d309a9228262435e46e420455f839093654bfe6e7e5c47277d0`. Its decompressed JSON is 14,505,034 bytes, SHA-256 `96dc48fd99daa8cec999516f7d5701a0283bd125f706e7c0b03490183c4ab35a`.

This is a guarded derivation from a verified complete inventory, not a claim that a full tree was materialized and freshly hashed. A future full preparation must still materialize the exact inputs and reproduce this snapshot. No active manifest or registry has been changed here. The three-entry DayTrigger registry preserves requiresScheduleExactAlarm, r0 and p0 exactly as recorded in Lookup07. The 1,244-body/605-class source inventory and projected 195,151 all-suite case total remain distinct from measured fresh execution.

## Actual lookup-recorder exercise

The lookup DEX runner has its own nested recorder. It imports numeric code for dependency validation, numeric target/helper identity and signed numeric-body preservation; it does **not** call Numeric08's command-recording block. Its own source remains the exact Lookup07 bytes, SHA-256 `aaf53f9c105727c7b68f7e78b5bed0d0b89ff7772452fc6aaf51315cb73bd208`.

A private test hook replaces only target_entry at the first application-input boundary. The actual run_controls function first creates its normal failed-by-default report and live nested run closure. The hook verifies the caller and closure code objects, invokes one bounded real Python child through that unchanged closure, then stops with an explicit sentinel where the recorder returns. Rejected/nonzero/timeout cases retain their actual exceptions instead. No application validation was bypassed into a passing result: all eight reports are literally LOOKUP_DEX_CONTROL_FAILED with passed=false, and no original/JVM/DEX application case, instruction, or signed proof is credited.

The eight observations cover empty output; exact nonempty stdout and stderr; expected exit 7; unexpected exit 7; a bounded timeout with independently confirmed child reaping; pre-existing stdout rejected before invocation; a replaced stdout inode rejected; and an additional hardlink to the original stdout inode. The latter is accepted by this narrower recorder and is retained as a missing single-link guard. The replacement rejection occurs before appending its final command row, so the failed overall report and this independent diagnostic carry that attempt's raw files and exception. Neither limitation was repaired or normalized in this capsule.

The actual lookup contract is exclusive xb creation, final same-device/inode checks, exact stream size/hash, integer monotonic duration and a bounded subprocess. It does not supply Numeric08's filesystem timestamp witnesses, regular-single-link postcondition or per-stream lifecycle receipts. A timeout records a null return code and preserves TimeoutExpired, but timeout type and reaped PID are present only in the independent diagnostic. A follow-up must decide and explicitly review the required lookup evidence contract before relying on the full acceptance runner. No implicit transfer of numeric verifier semantics is claimed.

## Retained proof and remaining work

Lookup07 remains unchanged and is durably published at commit `867791e6ad0f7ffb14d9cea4a7f1d8fbea7e0477`. Its exact 371-input original/JVM/micro-D8 results, ten compiled Java faults, two compiled DEX faults, provenance controls, old-fixture byte restoration and historical failed attempts remain separate inherited evidence. The application helper, Java harness, fixtures and all other lookup source files are unchanged by this merge; those observations were not re-executed or added to new case totals here.

Full signed-primary p0 matching, all 101 Java UI faults, all four acceptance-level DEX faults, the complete application suites and all sixteen full acceptance commands remain pending for these future inputs. The production-recorder exercise does not satisfy any of those gates. No new APK is present in this capsule.

The exact complete evidence archive preserves all three closed attempts, executed source copies, focused logs, guard reports, raw subprocess output and deliberately failed acceptance reports. Archive copies preserve bytes and modes; the raw study's intentional two-link file retains its physical state, which is bound in its observation JSON. Earlier capsules and active source were never modified.
'''
    (TARGET / 'CHECKPOINT_SCOPE.md').write_text(scope)
    save(TARGET / 'verified-results.json', {
        'merge': merge, 'focused_guards': tests,
        'recorder_diagnostic': {key: value for key, value in recorder.items() if key != 'cases'},
        'future_input_manifest_materialized_as_full_tree': False,
        'inherited_lookup_proof_checkpoint_sha256': 'd40df7530d090b6717d99e5011f1a0e5c0774297576ecc88047737301812a292',
        'full_signed_lookup_acceptance_pending': True,
        'numeric_witness_semantics_implicitly_applied_to_lookup': False})
    assert all(identity(path) == {key: row[key] for key in ['bytes', 'sha256', 'mode']}
               for (path, _), row in zip(evidence, rows))
    files = [{'path': path.relative_to(TARGET).as_posix(), **identity(path)}
             for path in sorted(TARGET.rglob('*')) if path.is_file()]
    checkpoint = {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'INACTIVE_DEPENDENCY_MERGE_GUARDS_PASSED_WITH_LOOKUP_RECORDER_LIMITATIONS',
        'repo_target': 'work-in-progress/day-trigger-lookup/08-numeric-filesystem-merge',
        'source_path_count': 21, 'unchanged_numeric_support_files': 4,
        'active_source_changed': False, 'full_build_or_signing': False, 'new_apk': False,
        'parent_checkpoint_sha256': 'd40df7530d090b6717d99e5011f1a0e5c0774297576ecc88047737301812a292',
        'numeric_successor_checkpoint_sha256': 'd9ddd3e0f692c66e2cd47870ff3cf95bfa0a2b1cd50fc2fd55a3c09e66df9bcf',
        'merged_numeric_module': merge['merged_numeric_module'], 'future_manifest': merge['future_manifest'],
        'future_snapshot': merge['future_snapshot'], 'focused_tests': 76, 'merge_guard_controls': 8,
        'actual_recorder_observations': 8, 'production_acceptance_reports_passed': 0,
        'evidence_file_count': len(rows), 'evidence_archive': identity(archive), 'files': files}
    save(TARGET / 'checkpoint.json', checkpoint)
    print(json.dumps({'checkpoint': str(TARGET / 'checkpoint.json'), **identity(TARGET / 'checkpoint.json'),
                      'direct_files': len(files), 'evidence_files': len(rows), 'archive': identity(archive),
                      'future_snapshot': merge['future_snapshot']}, indent=2))
    assert sum(path.stat().st_size for path in ROOT.rglob('*') if path.is_file()) <= 256 * 1024 * 1024


if __name__ == '__main__':
    main()
