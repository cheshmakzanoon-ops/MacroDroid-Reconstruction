#!/usr/bin/env python3
"""Read-only archive, full-pixel and full-XML analysis of active numeric Android CI."""
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import stat
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile
from PIL import Image

BASE = Path('/dev/shm/macrodroid-transfer-space-20261012/active-numeric-android-run-38247941263')
RAW = BASE / 'extracted'
OUT = Path('/dev/shm/macrodroid-active-numeric-android-review/attempt-01')


def identity(path):
    a = path.lstat(); assert stat.S_ISREG(a.st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    b = path.lstat()
    assert (a.st_dev, a.st_ino, a.st_size, a.st_mtime_ns, a.st_ctime_ns) == (b.st_dev, b.st_ino, b.st_size, b.st_mtime_ns, b.st_ctime_ns)
    return {'bytes': b.st_size, 'sha256': digest, 'mode': stat.S_IMODE(b.st_mode)}


def save(name, value):
    path = OUT / name; path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def tree(element):
    return [element.tag, sorted(element.attrib.items()), element.text, element.tail, [tree(child) for child in element]]


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(__file__, OUT / 'executed-reviewer.py')
    before = {str(BASE / 'artifact.zip'): identity(BASE / 'artifact.zip'),
              str(BASE / 'extracted-extraction.json'): identity(BASE / 'extracted-extraction.json')}
    receipt = json.loads((BASE / 'extracted-extraction.json').read_bytes())
    assert receipt['head_sha'] == '8db1fca4f03532ee2e5a8791fde7ea18126c237f'
    assert receipt['artifact_id'] == 11746694777 and receipt['member_count'] == 424
    assert {k: before[str(BASE / 'artifact.zip')][k] for k in ('bytes', 'sha256')} == {
        'bytes': 1017412, 'sha256': '1fb4a6375b9eb6b416c963f1d3e6d49733c9e5884d0081887bff96bec30fea04'}
    rows = {row['path']: row for row in receipt['files']}
    assert len(rows) == 424
    with zipfile.ZipFile(BASE / 'artifact.zip') as archive:
        names = archive.namelist(); assert len(names) == len(set(names)) == 424 and set(names) == set(rows)
        for name in names:
            data = archive.read(name); row = rows[name]
            assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
            path = RAW / name; value = identity(path); before[str(path)] = value
            assert {k: value[k] for k in ('bytes', 'sha256')} == {k: row[k] for k in ('bytes', 'sha256')}
    capture = json.loads((RAW / 'capture/result.json').read_bytes())
    intro = json.loads((RAW / 'capture/intro-comparison.json').read_bytes())
    post = json.loads((RAW / 'capture/post-intro-comparison.json').read_bytes())
    runtime = json.loads((RAW / 'runtime-run.json').read_bytes())
    constructor = json.loads((RAW / 'constructor-probe/probe-result.json').read_bytes())
    assert [run['apk_sha256'] for run in capture['runs']] == [
        '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800',
        '0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd']
    assert capture['requested_capture_complete'] is True and capture['full_parity_established'] is False
    assert [row['exit_code'] for row in runtime['commands']] == [0, 0, 0, 0, 2, 2, 2]
    commands = []
    for scope, folder, records in [('runtime-driver', RAW, runtime['commands']),
                                   ('constructor', RAW / 'constructor-probe', constructor['commands'])]:
        for row in records:
            for channel in ('stdout', 'stderr'):
                expected = row[channel]; observed = identity(folder / expected['path'])
                assert {k: observed[k] for k in ('bytes', 'sha256')} == {k: expected[k] for k in ('bytes', 'sha256')}
            commands.append({'scope': scope, **row})
    call = constructor['art_command']
    assert call in constructor['commands'] and call['returncode'] == 0 and call['timed_out'] is False
    assert (RAW / 'constructor-probe' / call['stdout']['path']).read_bytes() == (constructor['expected_stdout'] + '\n').encode()
    assert (RAW / 'constructor-probe' / call['stderr']['path']).read_bytes() == b''
    assert constructor['verification_mode'] == '-Xverify:all' and constructor['cleanup_complete'] is True
    assert constructor['full_runtime_1_to_1_established'] is False and constructor['constructor_allocation_on_art_verified'] is True
    pairs, coordinate_sets = [], []
    for index, suffix in enumerate(['', '-intro-2', '-intro-3', '-intro-4', '-post-intro']):
        name = 'intro-1' if not suffix else suffix[1:]
        left_path, right_path = [RAW / 'capture' / (variant + suffix + '.png') for variant in ('original', 'candidate')]
        with Image.open(left_path) as source:
            left = source.convert('RGBA'); left.load()
        with Image.open(right_path) as source:
            right = source.convert('RGBA'); right.load()
        assert left.size == right.size == (720, 1280)
        a, b = left.tobytes(), right.tobytes()
        coordinates = [i // 4 for i in range(0, len(a), 4) if a[i:i + 4] != b[i:i + 4]]
        coordinate_sets.append(set(coordinates))
        expected = intro['pages'][index]['changed_pixels'] if index < 4 else post['changed_pixels']
        assert len(coordinates) == expected
        records = b''.join(struct.pack('>I', pos) + a[pos * 4:pos * 4 + 4] + b[pos * 4:pos * 4 + 4] for pos in coordinates)
        diff = OUT / 'full-pixel-differences' / (name + '.rgba12.gz'); diff.parent.mkdir(exist_ok=True)
        with diff.open('xb') as stream:
            stream.write(gzip.compress(records, mtime=0))
        assert gzip.decompress(diff.read_bytes()) == records and len(records) == len(coordinates) * 12
        lx, rx = [RAW / 'capture' / (variant + suffix + '-hierarchy.xml') for variant in ('original', 'candidate')]
        xml_equal = tree(ET.fromstring(lx.read_bytes())) == tree(ET.fromstring(rx.read_bytes()))
        record = {'name': name, 'pixels': len(coordinates), 'full_canonical_xml_equal': xml_equal,
            'raw_xml_bytes_equal': lx.read_bytes() == rx.read_bytes(),
            'difference_bounds': [min(pos % 720 for pos in coordinates), min(pos // 720 for pos in coordinates),
                                  max(pos % 720 for pos in coordinates) + 1, max(pos // 720 for pos in coordinates) + 1],
            'all_difference_records': {'path': str(diff.relative_to(OUT)), **identity(diff)},
            'expanded_records_sha256': hashlib.sha256(records).hexdigest(),
            'expanded_record_bytes': len(records), 'masks_used': False,
            'original_png': identity(left_path), 'candidate_png': identity(right_path),
            'original_xml': identity(lx), 'candidate_xml': identity(rx)}
        pairs.append(record)
    common = set.intersection(*coordinate_sets)
    extra = coordinate_sets[1] - common
    assert [len(x) for x in coordinate_sets] == [578, 612, 578, 578, 578] and len(common) == 578 and len(extra) == 34
    save('full-pixel-and-xml-review.json', {'pairs': pairs,
        'common_difference_coordinates_across_all_five': len(common),
        'common_bounds': [min(i % 720 for i in common), min(i // 720 for i in common), max(i % 720 for i in common) + 1, max(i // 720 for i in common) + 1],
        'triggers_additional_coordinates': [{'x': i % 720, 'y': i // 720} for i in sorted(extra)],
        'diagnostic_only_no_mask_or_exclusion': True, 'runtime_cause_established': False})
    save('raw-command-bindings.json', commands)
    save('runtime-stage-outcomes.json', {'stages': [{'label': row['label'], 'exit_code': row['exit_code'], 'timed_out': row['timed_out']} for row in runtime['commands']],
        'constructor_original_only': True, 'constructor_status': constructor['status'],
        'ui_runtime_status': runtime['status'], 'all_requested_runtime_checks_passed': False})
    for name in ['runtime-run.json', 'capture/result.json', 'capture/cold-launch-comparison.json', 'capture/intro-comparison.json',
                 'capture/post-intro-comparison.json', 'constructor-probe/probe-result.json']:
        target = OUT / 'retained-reports' / name; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(RAW / name, target)
    after = {name: identity(Path(name)) for name in before}; assert after == before
    save('inputs-before.json', before); save('inputs-after.json', after)
    result = {'status': 'CLOSED_LITERAL_ANDROID_FAILURE_WITH_INDEPENDENT_FULL_PIXEL_XML_ANALYSIS',
        'run_id': 38247941263, 'head_sha': receipt['head_sha'], 'artifact_id': receipt['artifact_id'],
        'raw_archive_members_rehashed': 424, 'full_pairs_analyzed': 5,
        'pixel_counts': [row['pixels'] for row in pairs], 'all_full_xml_equal': all(row['full_canonical_xml_equal'] for row in pairs),
        'constructor_original_allocation_passed': True, 'capture_complete': True,
        'runtime_gate_passed': False, 'full_runtime_1_to_1_established': False,
        'android_executed_during_this_review': False, 'new_suite_executed': False,
        'recorder_or_production_verifier_reexecuted': False, 'all_read_inputs_unchanged': True}
    save('result.json', result)
    save('reviewer-runtime.json', {'python': sys.version, 'python_executable': sys.executable, 'pillow': Image.__version__})
    (OUT / 'README.md').write_text('''# Active numeric build: literal Android result and independent pixel review

The Android job for active commit 8db1fca4 and candidate 0762aad9 completed capture but **failed all three exact image-comparison gates**. The separate constructor allocation probe on the original APK passed with verification enabled and owned cleanup complete. These outcomes remain separate; this review changes no gate status.

The actual four intro pages and the first notification-permission surface have pixel differences of **578, 612, 578, 578 and 578**, respectively. Independent full-RGBA decoding reproduces all five counts. The same 578 changed coordinates occur in rectangle [596,10,632,38] on every screen. TRIGGERS has 34 additional changed indicator coordinates. Every changed coordinate and both RGBA values are retained losslessly in the five 12-byte-record files. All pixels remain part of the failed comparisons. This spatial decomposition is a diagnostic observation, not a mask, cause assignment or revised success rule.

The exact full XML result is recorded in `full-pixel-and-xml-review.json` and `result.json`, alongside raw XML byte equality. Both APKs reached the same notification-permission surface; no permission choice was taken. The runtime driver retained four zero exits for readiness, configuration, original-only constructor allocation and capture, then three comparison exits of 2. Its complete requested-runtime gate is false.

This independent read-only analysis rehashed all 424 original ZIP members and their extracted bytes, reconciled the raw driver and constructor streams, and decoded all five pixel/XML pairs. It did not rerun the recorder, production verifier, tests or Android, and extracted filesystem metadata does not stand in for the original live metadata. All raw archive/extracted inputs remained unchanged. The complete raw artifact is published separately under `docs/verification/android-ci-8db1fca4/`.
''')
    files = [{'path': p.relative_to(OUT).as_posix(), **identity(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
    save('checkpoint.json', {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'repo_target': 'docs/verification/android-ci-8db1fca4/root-analysis', 'status': result['status'],
        'active_files': [], 'android_executed': False, 'new_suite_executed': False,
        'full_runtime_1_to_1_established': False, 'files': files})
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
                      'payload_count': len(files), 'payload_bytes': sum(row['bytes'] for row in files), 'result': result}))


if __name__ == '__main__':
    main()
