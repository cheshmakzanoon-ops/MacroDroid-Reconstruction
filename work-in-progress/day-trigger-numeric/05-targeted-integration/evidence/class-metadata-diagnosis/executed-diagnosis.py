#!/usr/bin/env python3
"""Prove the reviewed/integrated helper differs only in external inner-class flags."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import time

BASE = Path(__file__).resolve().parent
OUT = BASE / 'reports/03-helper-metadata-diagnosis'
OLD = BASE.parent / 'day-trigger-numeric-recovery/reports/original-java-01/hostclasses/recovered/ui/DayTriggerValueMethods.class'
NEW = BASE / 'reports/02-targeted-numeric-attempt-01/hostclasses/recovered/ui/DayTriggerValueMethods.class'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inspect(data):
    assert data[:4] == b'\xca\xfe\xba\xbe'
    u2 = lambda p: struct.unpack_from('>H', data, p)[0]
    u4 = lambda p: struct.unpack_from('>I', data, p)[0]
    count, offset, index, strings = u2(8), 10, 1, {}
    sizes = {3: 4, 4: 4, 5: 8, 6: 8, 7: 2, 8: 2, 9: 4, 10: 4, 11: 4, 12: 4, 15: 3, 16: 2, 17: 4, 18: 4, 19: 2, 20: 2}
    while index < count:
        tag = data[offset]; offset += 1
        if tag == 1:
            length = u2(offset); offset += 2; strings[index] = data[offset:offset + length].decode(); offset += length
        else:
            offset += sizes[tag]
        index += 2 if tag in (5, 6) else 1
    pool_end = offset
    offset += 6
    offset += 2 + 2 * u2(offset)
    members = {}
    for kind in ('field', 'method'):
        number = u2(offset); offset += 2
        for _ in range(number):
            start = offset; name, descriptor, attributes = strings[u2(offset + 2)], strings[u2(offset + 4)], u2(offset + 6); offset += 8
            for _ in range(attributes):
                length = u4(offset + 2); offset += 6 + length
            members[kind + ':' + name + descriptor] = sha(data[start:offset])
    count = u2(offset); offset += 2; flags = []
    for _ in range(count):
        name, length = strings[u2(offset)], u4(offset + 2); start = offset + 6
        if name == 'InnerClasses':
            for index in range(u2(start)):
                at = start + 2 + index * 8
                flags.append({'name': strings[u2(at + 4)], 'offset': at + 6, 'flags': u2(at + 6)})
        offset = start + length
    assert offset == len(data)
    return {'constant_pool_sha256': sha(data[10:pool_end]), 'members': members, 'inner_classes': flags}


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    (OUT / 'executed-diagnosis.py').write_bytes(Path(__file__).read_bytes())
    old, new = OLD.read_bytes(), NEW.read_bytes()
    assert sha(old) == 'f527fe58f65ff1a079c920d711e25e1bdfb13421fcea7557c3ad653cab401441'
    assert sha(new) == '2f8b2d3769749301442dae35aca9fda5314eb1f17d59ea6310bd50be62596211'
    a, b = inspect(old), inspect(new)
    assert a['constant_pool_sha256'] == b['constant_pool_sha256'] and a['members'] == b['members']
    assert len(a['inner_classes']) == len(b['inner_classes']) == 3
    changed = bytearray(old)
    for x, y in zip(a['inner_classes'], b['inner_classes']):
        assert x['name'] == y['name'] and x['offset'] == y['offset']
        assert x['flags'] == 0x19 and y['flags'] == 0x09
        struct.pack_into('>H', changed, x['offset'], y['flags'])
    assert bytes(changed) == new
    commands = []
    for name, path in [('reviewed', OLD), ('integrated', NEW)]:
        at = datetime.now(timezone.utc).isoformat(); tick = time.monotonic()
        command = [str(BASE.parent / 'tooling/jdk21/bin/javap'), '-v', '-p', str(path)]
        done = subprocess.run(command, capture_output=True, timeout=30)
        for stream, data in [('stdout', done.stdout), ('stderr', done.stderr)]:
            (OUT / (name + '.' + stream + '.log')).write_bytes(data)
        commands.append({'argv': command, 'started_utc': at, 'finished_utc': datetime.now(timezone.utc).isoformat(),
                         'duration_seconds': time.monotonic() - tick, 'timeout_seconds': 30, 'returncode': done.returncode,
                         'stdout_sha256': sha(done.stdout), 'stderr_sha256': sha(done.stderr)})
        assert done.returncode == 0
    result = {'schema': 1, 'status': 'EXACT_THREE_INNERCLASS_FINAL_FLAGS_DIFFERENCE', 'passed': True,
              'reviewed_sha256': sha(old), 'integrated_sha256': sha(new), 'class_bytes': len(new),
              'constant_pool_byte_identity': True, 'all_fields_methods_attributes_byte_identity': True,
              'complete_difference_accounted_for': True, 'reviewed': a, 'integrated': b,
              'changed_byte_offsets': [i for i, (x, y) in enumerate(zip(old, new)) if x != y], 'commands': commands,
              'reason': 'The existing active DictionaryEntry/IntegerValue/DecimalValue host classes are non-final; the standalone study used final classes. The integrated helper retains the active host contract. Both compiled method structures and all their attributes are identical.'}
    (OUT / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('reviewed', 'integrated', 'commands')}, indent=2))


if __name__ == '__main__':
    main()
