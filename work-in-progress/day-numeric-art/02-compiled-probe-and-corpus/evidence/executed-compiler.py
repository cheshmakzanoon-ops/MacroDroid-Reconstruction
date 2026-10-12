#!/usr/bin/env python3
"""Compile only the neutral probe and independently verify its full input corpus."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import struct
import subprocess
import sys
import time
import traceback
import zlib

BASE = Path('/dev/shm/macrodroid-day-numeric-art')
CAP = BASE / 'source-draft-02'
OUT = BASE / 'compile-01'
JDK = Path('/workspace/scratch/4130730d15aa/tooling/jdk21')
JAR = Path('/workspace/scratch/4130730d15aa/current/MacroDroid_v9/tools/lib/jadx-r2721.4574686-all.jar')
OLD = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9')


def identity(path):
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), str(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    last = path.lstat()
    assert (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns) == (last.st_dev, last.st_ino, last.st_size, last.st_mtime_ns)
    return {'bytes': last.st_size, 'sha256': digest, 'mode': stat.S_IMODE(last.st_mode)}


def save(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def expected(row):
    bits = int(row['rawBitsHex'], 16)
    if row['kind'] == 'null-entry':
        return 'exception:java.lang.NullPointerException'
    if row['kind'] == 'integer':
        value = bits & 0xffffffff
        if value & 0x80000000:
            value -= 1 << 32
    elif row['kind'] == 'decimal':
        exponent = (bits >> 52) & 0x7ff
        fraction = bits & ((1 << 52) - 1)
        negative = bool(bits >> 63)
        if exponent == 0x7ff:
            value = 0 if fraction else -(1 << 31) if negative else (1 << 31) - 1
        else:
            significand = fraction | (1 << 52) if exponent else fraction
            shift = (exponent if exponent else 1) - 1023 - 52
            magnitude = significand << shift if shift >= 0 else significand >> -shift
            value = -magnitude if negative else magnitude
            value = min((1 << 31) - 1, max(-(1 << 31), value))
    else:
        value = 0
    return 'value:' + str(value)


def dex_metadata(path):
    data = path.read_bytes()
    assert data[:8] == b'dex\n035\0'
    assert struct.unpack_from('<II', data, 32) == (len(data), 112)
    assert struct.unpack_from('<I', data, 8)[0] == zlib.adler32(data[12:]) & 0xffffffff
    assert data[12:32] == hashlib.sha1(data[32:]).digest()
    strings, string_offset = struct.unpack_from('<II', data, 56)
    types, type_offset = struct.unpack_from('<II', data, 64)
    classes, class_offset = struct.unpack_from('<II', data, 96)
    assert classes == 1
    def descriptor(index):
        assert 0 <= index < types
        string_index = struct.unpack_from('<I', data, type_offset + index * 4)[0]
        assert 0 <= string_index < strings
        cursor = struct.unpack_from('<I', data, string_offset + string_index * 4)[0]
        for _ in range(5):
            byte = data[cursor]; cursor += 1
            if byte < 128:
                break
        else:
            raise ValueError('Invalid descriptor length')
        return data[cursor:data.index(b'\0', cursor)].decode('ascii')
    owner = descriptor(struct.unpack_from('<I', data, class_offset)[0])
    assert owner == 'Lrecovered/probe/DayNumericMethodProbe;'
    references = sorted(descriptor(i) for i in range(types))
    for name in references:
        base = name.lstrip('[')
        assert base in set('VZBSCIJFD') or base == owner or base.startswith('Ljava/') or base in ('Ldalvik/annotation/Signature;', 'Ldalvik/annotation/Throws;'), name
    return {'runtime_class_count': 1, 'runtime_class': owner, 'typed_references': references,
            'application_or_android_class_definitions': 0, 'direct_application_or_android_references': 0,
            'dex_header_and_internal_checksums_verified': True, **identity(path)}


def main():
    OUT.mkdir(exist_ok=False)
    shutil.copyfile(__file__, OUT / 'executed-compiler.py')
    temporary = OUT / 'temporary'; temporary.mkdir()
    env = {**os.environ, 'TMPDIR': str(temporary), 'PYTHONDONTWRITEBYTECODE': '1'}
    before = {}
    result = {'schema': 1, 'passed': False, 'started_utc': datetime.now(timezone.utc).isoformat(),
        'android_executed': False, 'application_build_executed': False, 'probe_runtime_executed': False,
        'inventory_only_jvm_execution': False, 'commands': []}
    def execute(label, argv, timeout):
        folder = OUT / 'commands' / label; folder.mkdir(parents=True, exist_ok=False)
        started = time.monotonic()
        row = {'label': label, 'argv': argv, 'cwd': str(OUT), 'timeout_seconds': timeout,
               'started_utc': datetime.now(timezone.utc).isoformat(), 'timed_out': False}
        with (folder / 'stdout.txt').open('wb') as out, (folder / 'stderr.txt').open('wb') as err:
            try:
                process = subprocess.run(argv, cwd=OUT, env=env, stdout=out, stderr=err, timeout=timeout)
                row['returncode'] = process.returncode
            except subprocess.TimeoutExpired:
                row.update(returncode=None, timed_out=True)
        row.update(seconds=time.monotonic() - started, finished_utc=datetime.now(timezone.utc).isoformat())
        row['stdout'] = identity(folder / 'stdout.txt'); row['stderr'] = identity(folder / 'stderr.txt')
        save('commands/' + label + '/command.json', row); result['commands'].append(row)
        assert row['returncode'] == 0 and row['timed_out'] is False, label
        return folder
    try:
        before[str(CAP / 'checkpoint.json')] = identity(CAP / 'checkpoint.json')
        assert before[str(CAP / 'checkpoint.json')]['sha256'] == '707afe796307be6044a5571cc39d4480ec032d2bf3d0ad87eb9a75118959deda'
        cp = json.loads((CAP / 'checkpoint.json').read_bytes())
        assert len(cp['files']) == 31
        for row in cp['files']:
            path = CAP / row['path']; before[str(path)] = identity(path)
            assert before[str(path)] == {k: row[k] for k in ('bytes', 'sha256', 'mode')}
        for path in (JDK / 'bin/java', JDK / 'bin/javac', JDK / 'release', JAR, OLD / 'reports/release-input-snapshot.json'):
            before[str(path)] = identity(path)
        snapshot = json.loads((OLD / 'reports/release-input-snapshot.json').read_bytes())
        entry = snapshot['entries']['tools/lib/jadx-r2721.4574686-all.jar']
        assert before[str(JAR)]['bytes'] == entry['size'] and before[str(JAR)]['sha256'] == entry['sha256']
        release = (JDK / 'release').read_bytes()
        (OUT / 'jdk-release.txt').write_bytes(release)
        assert re.search(rb'^JAVA_VERSION="21[.]', release, re.M)
        source = OUT / 'source/recovered/probe/DayNumericMethodProbe.java'
        source.parent.mkdir(parents=True)
        shutil.copyfile(CAP / 'source/recovered/probe/DayNumericMethodProbe.java', source)
        assert identity(source) == identity(CAP / 'source/recovered/probe/DayNumericMethodProbe.java')
        classes = OUT / 'classes'; classes.mkdir()
        dex = OUT / 'dex'; dex.mkdir()
        execute('java-version', [str(JDK / 'bin/java'), '-version'], 30)
        execute('javac-version', [str(JDK / 'bin/javac'), '-version'], 30)
        execute('neutral-probe-javac', [str(JDK / 'bin/javac'), '-J-Xmx512m', '-J-XX:ActiveProcessorCount=2',
            '--release', '8', '-encoding', 'UTF-8', '-g:none', '-d', str(classes), str(source)], 120)
        files = sorted(p.relative_to(classes).as_posix() for p in classes.rglob('*') if p.is_file())
        assert files == ['recovered/probe/DayNumericMethodProbe.class']
        output = execute('inventory-only-jvm', [str(JDK / 'bin/java'), '-Xmx512m', '-XX:ActiveProcessorCount=2',
            '-Xverify:all', '-cp', str(classes), 'recovered.probe.DayNumericMethodProbe', '--inventory'], 120)
        assert (output / 'stderr.txt').read_bytes() == b''
        lines = (output / 'stdout.txt').read_text().splitlines()
        assert lines[0] == 'DAY_NUMERIC_INPUTS_BEGIN\tcases=1291\tsha256=e083bc1996c5c7191bffe837fc0f30e254848a4754676ba0a8a119d23e8f6e79'
        assert lines[-1] == 'DAY_NUMERIC_INPUTS_END\tcases=1291\tandroid_executed=false' and len(lines) == 1293
        rows, values, counts = [], [], {}
        for line in lines[1:-1]:
            encoded, value = line.split('\t')
            row = json.loads(encoded)
            assert list(row) == (['case', 'kind', 'rawBitsHex', 'text'] if 'text' in row else ['case', 'kind', 'rawBitsHex'])
            assert re.fullmatch('[0-9a-f]{16}', row['rawBitsHex']) and expected(row) == value
            rows.append(row); values.append({'case': row['case'], 'expected': value})
            counts[row['kind']] = counts.get(row['kind'], 0) + 1
        assert len({row['case'] for row in rows}) == 1291
        encoded = json.dumps(rows, ensure_ascii=False, separators=(',', ':')).encode()
        assert hashlib.sha256(encoded).hexdigest() == 'e083bc1996c5c7191bffe837fc0f30e254848a4754676ba0a8a119d23e8f6e79'
        save('exact-input-corpus.json', rows); save('independent-python-expectations.json', values)
        save('input-corpus-review.json', {'cases': 1291, 'per_kind': counts, 'all_python_integer_only_expectations_match': True,
             'original_compact_inventory_sha256': hashlib.sha256(encoded).hexdigest(), 'android_executed': False})
        result['inventory_only_jvm_execution'] = True
        output = execute('neutral-probe-d8', [str(JDK / 'bin/java'), '-Xmx512m', '-XX:ActiveProcessorCount=2',
            '-cp', str(JAR), 'com.android.tools.r8.D8', '--release', '--no-desugaring', '--min-api', '23',
            '--output', str(dex), str(classes / files[0])], 120)
        assert (output / 'stdout.txt').read_bytes() == (output / 'stderr.txt').read_bytes() == b''
        assert sorted(p.name for p in dex.iterdir()) == ['classes.dex']
        metadata = dex_metadata(dex / 'classes.dex')
        save('probe-dex-metadata.json', metadata)
        result.update(passed=True, status='NEUTRAL_NUMERIC_PROBE_COMPILED_AND_1291_INPUTS_VERIFIED_NO_ANDROID',
            probe_compiled=True, corpus_cases=1291, probe_dex=metadata, retained_original_corpus=True,
            full_runtime_1_to_1_established=False)
    except Exception as error:
        result.update(status='NEUTRAL_NUMERIC_PROBE_PREPARATION_FAILED', reason=repr(error))
        save('exception.json', {'exception': repr(error), 'traceback': traceback.format_exc()})
    finally:
        after = {name: identity(Path(name)) for name in before}
        result['all_read_inputs_unchanged'] = before == after
        if before != after:
            result['passed'] = False
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save('inputs-before.json', before); save('inputs-after.json', after); save('result.json', result)
        print(json.dumps({k:v for k,v in result.items() if k not in ('commands', 'probe_dex')}, indent=2))
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
