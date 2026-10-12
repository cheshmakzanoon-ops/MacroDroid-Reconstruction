#!/usr/bin/env python3
"""Independently inspect the closed two-stage DayTrigger host design."""
from __future__ import annotations
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import tarfile
import traceback

SOURCE = Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/06-combined-host-workflow-design')
OUTPUT = Path('/dev/shm/macrodroid-combined-host-design-review')
EXPECTED = {'bytes': 9298, 'sha256': '3da7b4fa3707c301256c8dd7236c18f7680d2fb5bd72595d353e8a01b223830f'}
EVIDENCE = SOURCE / 'evidence/reports/22-combined-host-design-source'
SNAPSHOTS = [
    Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/reports/release-input-snapshot.json'),
    Path('/dev/shm/day-numeric-hosted-02/checkpoints/01-command-filesystem-source-successor/evidence/future-input-snapshot.json.gz'),
    Path('/dev/shm/macrodroid-day-lookup-integration/checkpoints/05-lookup-recorder-successor/future-input-snapshot.json.gz')]


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def identity(path):
    require(stat.S_ISREG(path.lstat().st_mode), 'Non-regular input: ' + str(path))
    with path.open('rb') as stream:
        value = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': value}


def save(name, value):
    path = OUTPUT / name
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def scan(checkpoint):
    rows = []
    for row in checkpoint['files']:
        path = SOURCE / row['path']
        require(path.resolve().is_relative_to(SOURCE), 'Escaping design path')
        got = identity(path)
        require(got == {key: row[key] for key in ('bytes', 'sha256')}
                and stat.S_IMODE(path.stat().st_mode) == row['mode'], 'Design payload changed: ' + row['path'])
        rows.append({'path': row['path'], 'mode': row['mode'], **got})
    require(len(rows) == 35, 'Design payload count differs')
    require(sorted(p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob('*') if p.is_file())
            == sorted(['checkpoint.json'] + [row['path'] for row in rows]), 'Unlisted design file')
    return rows


def review(result):
    require(identity(SOURCE / 'checkpoint.json') == EXPECTED, 'Design checkpoint changed')
    checkpoint = json.loads((SOURCE / 'checkpoint.json').read_text())
    before = scan(checkpoint)
    save('design-files-before.json', before)
    reads = json.loads((EVIDENCE / 'read-input-identities.json').read_text())
    before_reads = {name: identity(Path(name)) for name in reads}
    require(before_reads == reads and len(reads) == 125, 'A bound read input changed')
    save('bound-read-inputs-before.json', before_reads)
    archived = []
    with tarfile.open(SOURCE / 'evidence.tar.gz', 'r:gz') as archive:
        for member in archive.getmembers():
            name = PurePosixPath(member.name)
            require(member.isfile() and not name.is_absolute() and '..' not in name.parts
                    and name.as_posix() == member.name, 'Noncanonical evidence archive member')
            raw = archive.extractfile(member).read()
            target = SOURCE / 'evidence' / member.name
            require(identity(target) == digest(raw), 'Archived evidence differs from its retained raw file')
            archived.append({'path': member.name, **digest(raw)})
    require(len(archived) == len({row['path'] for row in archived}) == 19, 'Evidence archive roles differ')
    save('archive-members-independently-verified.json', archived)
    contract = json.loads((EVIDENCE / 'two-stage-source-contract.json').read_text())
    require(contract['baseline_commit'] == 'dbcad968c5c3e8f084205393a6c0d2d06a203c71'
            and contract['numeric_commit'] == '811f979eda1b937917c18defef38455c49a59062',
            'Fixed baseline or numeric commit changed')
    snapshots = []
    for path, expected in zip(SNAPSHOTS, contract['complete_snapshots']):
        raw = gzip.decompress(path.read_bytes()) if path.suffix == '.gz' else path.read_bytes()
        require(digest(raw) == expected['manifest'], 'Manifest bytes changed')
        snapshot = json.loads(raw)
        require(snapshot['files'] == len(snapshot['entries']) == expected['files']
                and snapshot['snapshot_sha256'] == expected['snapshot_sha256'], 'Manifest count or declared snapshot differs')
        snapshots.append(snapshot)
    require([item['files'] for item in snapshots] == [81291, 81298, 81304], 'Source boundary counts differ')
    actual_stages = []
    for index, name in enumerate(('numeric_stage_changes', 'lookup_stage_changes')):
        entries = dict(snapshots[index]['entries'])
        changes = contract[name]
        require(len(changes) == len({row['path'] for row in changes}) == (19 if index == 0 else 21),
                'Source stage roles differ')
        # Check every before state before mutating even this private in-memory map.
        for row in changes:
            old = row['baseline']
            if old is None:
                require(row['must_be_absent_if_new'] is True and row['path'] not in entries, 'New path is not absent')
            else:
                require(row['must_be_absent_if_new'] is False
                        and entries.get(row['path']) == {'size': old['bytes'], 'sha256': old['sha256']},
                        'Stage before hash differs: ' + row['path'])
        for row in changes:
            entries[row['path']] = {'size': row['candidate']['bytes'], 'sha256': row['candidate']['sha256']}
        require(entries == snapshots[index + 1]['entries'], 'Complete transformed entry map differs')
        actual_stages.append({'stage': name, 'changed_paths': len(changes), 'input_files_before': snapshots[index]['files'],
                              'input_files_after': len(entries), 'exact_complete_next_entry_map': True})
    numeric = {row['path'] for row in contract['numeric_stage_changes']}
    lookup = {row['path'] for row in contract['lookup_stage_changes']}
    require(len(numeric | lookup) == 25 and len(numeric - lookup) == 4,
            'Combined source union or numeric-only count differs')
    require({row['path'] for row in contract['numeric_only_paths']} == numeric - lookup, 'Numeric-only pins incomplete')
    require({row['path'] for row in contract['union']} == numeric | lookup, 'Combined union declaration incomplete')
    actual_new = set(snapshots[-1]['entries']) - set(snapshots[0]['entries'])
    require(len(actual_new) == contract['union_new_inputs'] == 13, 'New input count differs')
    expected_payloads = {row['path']: row['candidate'] for row in contract['lookup_stage_changes']}
    resolutions = contract['lookup_payload_resolutions']
    require(len(resolutions) == len({row['path'] for row in resolutions}) == 21, 'Lookup resolver roles differ')
    for row in resolutions:
        require(identity(Path(row['payload'])) == row['identity'] == expected_payloads[row['path']],
                'Final lookup payload differs from its declared stage candidate')
    save('independently-derived-source-boundaries.json', {'stages': actual_stages, 'union': sorted(numeric | lookup),
         'numeric_only': sorted(numeric - lookup), 'new_inputs': sorted(actual_new),
         'physical_application_tree_materialized': False})
    counts = json.loads((EVIDENCE / 'source-derived-counts.json').read_text())
    require(counts['all_cases'] == sum(counts['suite_cases'].values()) == 194780 + 371 == 195151,
            'Positive case arithmetic differs')
    require(counts['registered_methods'] == 1244 and counts['uncredited_dependencies'] == 5
            and counts['fixture_methods'] == 1249 and counts['target_classes'] == 605
            and counts['fixture_classes'] == 607 and counts['python_tests'] == 308 + 49 == 357,
            'Source-derived fixture/test partition differs')
    commands = json.loads((EVIDENCE / 'proposed-command-and-report-contract.json').read_text())
    require(len(commands['gate_order']) == commands['gate_count'] == 16
            and len(commands['fresh_reports']) == len(set(commands['fresh_reports'])) == 24,
            'Acceptance gate or fresh-report role count differs')
    require(len(commands['numeric_commands']) == 17 and len(commands['lookup_commands']) == 19
            and commands['method_command_count'] == 36 and commands['method_stream_count'] == 72,
            'Method command counts differ')
    for name in ('numeric_commands', 'lookup_commands'):
        rows = commands[name]
        require(len({(row['directory'], row['name']) for row in rows}) == len(rows), 'Duplicate method command role')
        require(all(row['timeout_seconds'] == 120 and type(row['expected_returncode']) is int
                    and row['expected_returncode'] in (0, 1, 3) for row in rows), 'Method exit/timeout contract differs')
    require(commands['all_actual_commands_pending'] is True and commands['symbolic_paths_are_design_only'] is True,
            'Design commands are mislabeled as actual execution')
    after = scan(checkpoint)
    after_reads = {name: identity(Path(name)) for name in reads}
    require(after == before and after_reads == before_reads and identity(SOURCE / 'checkpoint.json') == EXPECTED,
            'Reviewed inputs changed')
    save('design-files-after.json', after)
    save('bound-read-inputs-after.json', after_reads)
    result.update(status='BOUNDED_COMBINED_HOST_DESIGN_REVIEW_PASSED', passed=True, payloads_rehashed=35,
                  bound_reads_rehashed=125, raw_archive_members_verified=19,
                  complete_source_entry_maps_derived=[81291, 81298, 81304], source_union_paths=25,
                  new_input_paths=13, numeric_only_paths=4, required_gates=16, required_fresh_reports=24,
                  numeric_command_roles=17, lookup_command_roles=19, all_reviewed_inputs_unchanged=True,
                  source_derived_expected_cases=195151, source_derived_expected_project_tests=357,
                  new_fixture_dex_decode_by_this_review=False, new_application_or_tooling_tests=False,
                  physical_application_tree_materialized=False, android_executed=False,
                  new_parity_or_signed_acceptance_claim=False)


def main():
    OUTPUT.mkdir(exist_ok=False)
    shutil.copyfile(Path(__file__), OUTPUT / 'executed-review.py')
    result = {'status': 'BOUNDED_COMBINED_HOST_DESIGN_REVIEW_INCOMPLETE', 'passed': False,
              'started_utc': datetime.now(timezone.utc).isoformat(), 'reviewed_checkpoint': EXPECTED}
    try:
        review(result)
    except Exception as error:
        result.update(status='BOUNDED_COMBINED_HOST_DESIGN_REVIEW_FAILED', error=type(error).__name__ + ': ' + str(error))
        (OUTPUT / 'failure.traceback.txt').write_text(traceback.format_exc())
    result['finished_utc'] = datetime.now(timezone.utc).isoformat()
    save('review-result.json', result)
    (OUTPUT / 'README.md').write_text('# Independent combined host design review\n\n'
        'The review checks the exact frozen design and its 125 bound local inputs. It independently derives both '
        'complete in-memory source transformations with every stage before state checked first; verifies the 25-path '
        'union, four numeric-only pins, 13 new inputs and all 21 final lookup payload resolutions; and checks the '
        '16-gate, 24-report and 17+19-command inventories. It retains its literal result and full failure traceback '
        'if any check stops. The 19-member evidence archive is compared against the already retained raw copies.\n\n'
        'These are design and source-inventory checks. No whole application is materialized, no Java/DEX or project '
        'test suite runs, and no signed-APK or Android result is claimed. The actual 195,151 cases and 357 project '
        'tests remain future CI requirements. The design\'s fixture decode and prior method outcomes retain their '
        'existing source-bound evidence; this review does not present them as new execution.\n')
    files = [{'path': p.relative_to(OUTPUT).as_posix(), 'mode': '100644', **identity(p)}
             for p in sorted(OUTPUT.iterdir()) if p.is_file()]
    save('checkpoint.json', {'schema': 1, 'status': result['status'], 'repo_target':
         'docs/verification/day-trigger-combined/design-review', 'files': files, 'file_count': len(files),
         'payload_bytes': sum(row['bytes'] for row in files), 'active_files': []})
    print(json.dumps({'output': str(OUTPUT), 'checkpoint': identity(OUTPUT / 'checkpoint.json'),
                      'files': len(files), 'payload_bytes': sum(row['bytes'] for row in files),
                      'status': result['status'], 'passed': result['passed'], 'error': result.get('error')}))
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
