#!/usr/bin/env python3
"""Check narrow structural facts; never change or supply original coverage credit."""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import traceback


HERE = Path(__file__).resolve().parent
FIXTURE_SHA = '940aee4861d9bd52951ccc835e91a917bb56748b4eaad5deb8a0fa1c7d2c3254'
INVENTORY_SHA = '2d368ab110348b3934f217d084d0b66df4d61a0ef3ddb41d3e804ec876efcfda'
COLLECTION_SHA = '2815ca1b9c3268b90850508734f90695911f502c31e035756abc51c396dd5c18'
RELEASE_SHA = 'ebbd70bf00bab6d39addf51969c5ff244030b86b29de400b9fb10612ebd3ceec'
JRT_HASHES = {
    'StringBuilder': '14c9ab4b30fdb96f62b74b2cd6a53c3a790a221981f59a1d349b0dc09ecc592e',
    'AbstractStringBuilder': 'f1ccca2afbe6d7d0ba5a1f19b7095b555796701dfafd5c529366350f7c9c94e4',
    'StringUTF16': 'e03e9a012b6c29de2130ef49badab77d421f5272e1c72224838545e1091488b5',
    'Object': '10cc90d16479279e1d6ee258fdaea4c5640ac6125acb5a7100a7b0a20237a9f2'}
JAVAP_HASHES = {
    'StringBuilder': '9dd80fb96b823d0ce9bf2e55382dff5f16d218142c1c9bff4de6c2f024c586a1',
    'AbstractStringBuilder': '6c4ee77294902e331277a8a8918d08e9f33d2d2913cb8aae221dc9a540ceb50d',
    'StringUTF16': 'ea0800a4ed57f2739594c9e838f508631a46770c5cb1a422f029a027a37aaab1',
    'Object': '55ac3db4d20f4ae417cc9c2b9ecdaaef3a3b2576d810deed6e5860327b3b5cf1'}
OWNER = 'Lcom/arlosoft/macrodroid/action/services/BaseVideoRecordingService;'
COROUTINE = 'Lcom/arlosoft/macrodroid/action/services/a;'
REGION_OFFSETS = [122, 124, 126, 129, 132, 134, 137, 140, 142, 144, 146, 147, 149, 150, 152, 154, 156]
KNOWN_OPS = set('ADD_INT_LIT8 CHECK_CAST CMP_LONG CONST_4 CONST_STRING CONST_WIDE_16 CONST_WIDE_32 DIV_LONG DIV_LONG_2ADDR GOTO GOTO_16 IF_EQ IF_EQZ IF_GEZ IF_GTZ IF_LEZ IF_LT IF_LTZ IF_NE IF_NEZ IGET IGET_OBJECT IGET_WIDE INT_TO_LONG INVOKE_DIRECT INVOKE_STATIC INVOKE_STATIC_RANGE INVOKE_VIRTUAL IPUT IPUT_OBJECT IPUT_WIDE MOVE MOVE_EXCEPTION MOVE_FROM16 MOVE_OBJECT MOVE_OBJECT_FROM16 MOVE_RESULT MOVE_RESULT_OBJECT MOVE_RESULT_WIDE MOVE_WIDE MOVE_WIDE_FROM16 MUL_LONG NEW_INSTANCE RETURN_OBJECT SGET_BOOLEAN SGET_OBJECT SUB_LONG'.split())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_instruction(by, offset, **fields):
    require(all(by[offset].get(key) == value for key, value in fields.items()),
            'Instruction operands changed at ' + str(offset))


def writes(instruction):
    """Destination registers for only the original opcodes preceding/inside this region."""
    op = instruction['opcode']
    if op.startswith(('INVOKE_', 'IPUT', 'IF_', 'GOTO', 'RETURN')):
        return set()
    require('A' in instruction, 'Unexpected register writer')
    wide = op.startswith('CONST_WIDE') or op in {'IGET_WIDE', 'MOVE_RESULT_WIDE', 'SUB_LONG', 'DIV_LONG'}
    return {instruction['A'], instruction['A'] + 1} if wide else {instruction['A']}


def structural_facts(inventory):
    instructions = inventory['instructions']
    require(len(instructions) == 262 and sum(i['units'] for i in instructions) == 534, 'Unexpected method size')
    by = {i['offset']: i for i in instructions}
    require(len(by) == len(instructions), 'Duplicate offset')
    offset = 0
    normal = {}
    for instruction in instructions:
        require(instruction['offset'] == offset and instruction['opcode'] in KNOWN_OPS, 'Unknown or noncontiguous instruction')
        op = instruction['opcode']
        next_offset = offset + instruction['units']
        if op.startswith('GOTO'):
            targets = [instruction['target']]
        elif op.startswith('IF_'):
            targets = [next_offset, instruction['target']]
        elif op == 'RETURN_OBJECT':
            targets = []
        else:
            targets = [next_offset]
        require(all(target in by for target in targets), 'Invalid normal target')
        normal[offset] = set(targets)
        offset = next_offset
    region = {'start': 122, 'end': 159, 'handlers': [{'type': 'Ljava/lang/Exception;', 'offset': 232}]}
    require(region in inventory['exceptionRegions'], 'Exact Exception-only protected interval changed')
    require([i['offset'] for i in instructions if 122 <= i['offset'] < 159] == REGION_OFFSETS, 'Protected instruction set changed')
    sources = [(r['start'], r['end'], h['type']) for r in inventory['exceptionRegions']
               for h in r['handlers'] if h['offset'] in (232, 233, 235)]
    require(sources == [(122, 159, 'Ljava/lang/Exception;')], 'Additional handler entry')
    normal_predecessors = {node: sorted(source for source, targets in normal.items() if node in targets) for node in by}
    require([normal_predecessors[n] for n in (232, 233, 235)] == [[], [232], [233]], 'Ordinary entry into handler chain')
    exact_instruction(by, 232, opcode='MOVE_EXCEPTION', A=0)
    exact_instruction(by, 233, opcode='MOVE_FROM16', A=21, B=10)
    exact_instruction(by, 235, opcode='GOTO_16', target=495)

    # Deliberately conservative: every protected instruction gets its declared exception edge.
    # This graph considers all 262 instructions reachable and does not exempt any handler.
    edges = {node: set(targets) for node, targets in normal.items()}
    for protected in inventory['exceptionRegions']:
        for node in by:
            if protected['start'] <= node < protected['end']:
                for handler in protected['handlers']:
                    require(handler['offset'] in by, 'Invalid exception target')
                    edges[node].add(handler['offset'])
    reachable = {0}
    todo = [0]
    while todo:
        for target in edges[todo.pop()]:
            if target not in reachable:
                reachable.add(target)
                todo.append(target)
    predecessors = {node: {source for source, targets in edges.items() if node in targets} for node in by}
    dominators = {node: {0} if node == 0 else set(reachable) for node in reachable}
    changed = True
    while changed:
        changed = False
        for node in sorted(reachable - {0}):
            value = {node} | set.intersection(*(dominators[p] for p in predecessors[node] if p in reachable))
            if value != dominators[node]:
                dominators[node] = value
                changed = True
    exact_instruction(by, 112, opcode='IGET_OBJECT', A=14, B=1, reference=COROUTINE + '->this$0:' + OWNER)
    exact_instruction(by, 116, opcode='INVOKE_VIRTUAL', invokeRegisters=[14, 0], reference=OWNER + '->c(Ljava/io/File;)J')
    exact_instruction(by, 119, opcode='MOVE_RESULT_WIDE', A=12)
    require({112, 116, 119, 120}.issubset(dominators[122]), 'Successful receiver call does not dominate protected entry')
    require(normal_predecessors[122] == [120], 'Extra protected entry')
    require(all(14 not in writes(i) for i in instructions if 114 <= i['offset'] < 159), 'Captured v14 overwritten')
    exact_instruction(by, 122, opcode='IGET_WIDE', A=5, B=14, reference=OWNER + '->x:J')
    exact_instruction(by, 150, opcode='IPUT_WIDE', A=12, B=14, reference=OWNER + '->x:J')
    for constant_offset in (126, 129):
        exact_instruction(by, constant_offset, opcode='CONST_WIDE_32', A=19, literal=1048576)
    require({126, 129}.issubset(dominators[152]), 'Constant divisor does not dominate division')
    require(all(not ({19, 20} & writes(i)) for i in instructions if 132 <= i['offset'] <= 152), 'Divisor overwritten')
    exact_instruction(by, 152, opcode='DIV_LONG', A=5, B=12, C=19)
    exact_instruction(by, 154, opcode='NEW_INSTANCE', A=0, reference='Ljava/lang/StringBuilder;')
    exact_instruction(by, 156, opcode='INVOKE_DIRECT', invokeRegisters=[0], reference='Ljava/lang/StringBuilder;-><init>()V')
    require(normal_predecessors[156] == [154], 'Constructor does not directly use fresh allocation')
    require([i['offset'] for i in instructions if 122 <= i['offset'] < 159 and i['opcode'].startswith('INVOKE_')] == [156], 'Additional protected call')
    return {'protected_region': region, 'protected_instruction_count': len(REGION_OFFSETS),
            'protected_instructions': [by[n] for n in REGION_OFFSETS],
            'conservative_graph_reachable_instructions': len(reachable),
            'selected_normal_predecessors': {str(n): normal_predecessors[n] for n in (122, 150, 152, 154, 156, 232, 233, 235)},
            'selected_dominators': {str(n): sorted(dominators[n]) for n in (122, 152, 156)},
            'captured_owner_register': 14, 'owner_defined_at': 112, 'successful_nonnull_receiver_call_at': 116,
            'owner_reloads_within_protected_region': [], 'constant_divisor': 1048576,
            'handler_has_no_normal_entry': True, 'handler_chain': [232, 233, 235], 'handler_destination': 495}


def javap_member(text, heading):
    lines = text.splitlines()
    indexes = [i for i, line in enumerate(lines) if line == '  ' + heading]
    require(len(indexes) == 1, 'Expected one pinned classfile member: ' + heading)
    start = indexes[0]
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith('  ') and not lines[i].startswith('    ') and lines[i].strip()), len(lines))
    return '\n'.join(lines[start:end]).rstrip()


def constructor_facts(texts):
    require(set(texts) == set(JAVAP_HASHES), 'Incomplete pinned constructor class set')
    for name, digest in JAVAP_HASHES.items():
        require(hashlib.sha256(texts[name].encode()).hexdigest() == digest,
                'Complete pinned constructor disassembly changed: ' + name)
    sb = javap_member(texts['StringBuilder'], 'public java.lang.StringBuilder();')
    abstract = javap_member(texts['AbstractStringBuilder'], 'java.lang.AbstractStringBuilder(int);')
    utf16 = javap_member(texts['StringUTF16'], 'public static byte[] newBytesFor(int);')
    length = javap_member(texts['StringUTF16'], 'public static int newBytesLength(int);')
    obj = javap_member(texts['Object'], 'public java.lang.Object();')
    require(re.search(r'1: bipush\s+16\n', sb) is not None, 'Default constructor capacity differs')
    require('java/lang/AbstractStringBuilder."<init>":(I)V' in sb, 'Default constructor target differs')
    require('java/lang/Object."<init>":()V' in abstract and 'newarray       byte' in abstract
            and 'java/lang/StringUTF16.newBytesFor:(I)[B' in abstract, 'Builder allocation branches differ')
    require('newBytesLength:(I)I' in utf16 and 'newarray       byte' in utf16, 'UTF16 allocation path differs')
    require('1: ifge          12' in length and '// int 1073741823' in length
            and '15: if_icmplt     55' in length and '56: iconst_1' in length and '57: ishl' in length,
            'Capacity checks differ')
    require(re.findall(r'^\s+\d+:.*$', obj, flags=re.MULTILINE) == ['       0: return'], 'Object constructor has additional code')
    return {'default_capacity': 16, 'compact_array_length': 16, 'utf16_array_length': 32,
            'utf16_limit': 1073741823, 'negative_array_guard_reachable_for_16': False,
            'size_limit_guard_reachable_for_16': False,
            'actual_jrt_members': {'StringBuilder()': sb, 'AbstractStringBuilder(int)': abstract,
                                   'StringUTF16.newBytesFor(int)': utf16, 'StringUTF16.newBytesLength(int)': length,
                                   'Object()': obj}}


def synthetic_controls(inventory, texts):
    result = []
    def test(label, change, constructor=False):
        data = copy.deepcopy(texts if constructor else inventory)
        change(data)
        try:
            (constructor_facts if constructor else structural_facts)(data)
        except ValueError as error:
            result.append({'label': label, 'rejected': True, 'reason': str(error),
                           'scope': 'Synthetic structural-proof input only; not an app method execution'})
        else:
            raise RuntimeError('Unsound structural control accepted: ' + label)
    def at(data, offset):
        return next(i for i in data['instructions'] if i['offset'] == offset)
    test('last-divisor-becomes-zero', lambda d: at(d, 129).__setitem__('literal', 0))
    test('wide-write-clobbers-owner', lambda d: at(d, 120).__setitem__('A', 14))
    test('branch-bypasses-receiver-call', lambda d: at(d, 99).__setitem__('target', 150))
    test('normal-entry-into-handler', lambda d: at(d, 231).__setitem__('target', 232))
    test('different-field-receiver', lambda d: at(d, 150).__setitem__('B', 1))
    test('different-constructor-arity', lambda d: at(d, 156).__setitem__('reference', 'Ljava/lang/StringBuilder;-><init>(I)V'))
    test('extended-protected-range', lambda d: d['exceptionRegions'][2].__setitem__('end', 163))
    test('catch-Throwable-instead-of-Exception', lambda d: d['exceptionRegions'][2]['handlers'][0].__setitem__('type', 'Ljava/lang/Throwable;'))
    test('additional-protected-constructor-call', lambda d: at(d, 134).update({
        'opcode': 'INVOKE_DIRECT', 'invokeRegisters': [0], 'reference': 'Ljava/lang/StringBuilder;-><init>()V'}))
    test('negative-default-capacity', lambda d: d.__setitem__('StringBuilder', d['StringBuilder'].replace('bipush        16', 'bipush        -1')), True)
    test('additional-constructor-throw-preserves-old-substrings', lambda d: d.__setitem__('StringBuilder',
        d['StringBuilder'].replace('       6: return\n',
            '       6: new           #999 // class java/lang/RuntimeException\n'
            '       9: dup\n      10: invokespecial #1000 // Method java/lang/RuntimeException."<init>":()V\n'
            '      13: athrow\n      14: return\n', 1)), True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    report = {'status': 'CHECKING', 'started_utc': datetime.now(timezone.utc).isoformat(),
              'app_method_executed': False, 'android_executed': False, 'original_coverage_credit_added': 0,
              'coverage_exemption_implemented': False, 'original_coverage_gate_remains_failed': True,
              'scope': 'Narrow mechanical facts and pinned synchronous host constructor argument for independent review; no runtime or complete-coverage claim.'}
    try:
        evidence = args.evidence.resolve()
        require(sha(evidence / 'result.json') == COLLECTION_SHA, 'Independently pinned collector manifest changed')
        collected = json.loads((evidence / 'result.json').read_text())
        require(collected['status'] == 'DATAFLOW_INPUTS_COLLECTED', 'Incomplete data-flow collection')
        require(collected['original_fixture']['sha256'] == FIXTURE_SHA, 'Original fixture binding differs')
        for item in collected['files']:
            path = evidence / item['path']
            require(not path.is_symlink() and path.stat().st_size == item['bytes'] and sha(path) == item['sha256'], 'Collected evidence differs: ' + item['path'])
        require(sha(evidence / 'original-instructions.json') == INVENTORY_SHA, 'Pinned original operands differ')
        require(sha(evidence / 'host-sources/release') == RELEASE_SHA, 'Pinned installed runtime release changed')
        for name, digest in JRT_HASHES.items():
            require(sha(evidence / 'jrt-classfiles' / (name + '.class')) == digest,
                    'Independently pinned actual JRT class bytes changed: ' + name)
        report['collection_result_sha256'] = sha(evidence / 'result.json')
        report['independent_digest_bindings'] = {'collection': COLLECTION_SHA, 'release': RELEASE_SHA,
            'actual_jrt_classfiles': JRT_HASHES, 'complete_javap_outputs': JAVAP_HASHES,
            'scope': 'Fixed reviewed evidence identities, independently specified by this verifier. A future runtime gate must also bind the runtime actually used; this is no such gate.'}
        report['every_collected_file_hash_verified'] = len(collected['files'])
        inventory = json.loads((evidence / 'original-instructions.json').read_text())
        texts = {name: (evidence / ('javap-' + name + '.stdout.txt')).read_text()
                 for name in ('StringBuilder', 'AbstractStringBuilder', 'StringUTF16', 'Object')}
        report['structural_facts'] = structural_facts(inventory)
        report['installed_host_constructor_facts'] = constructor_facts(texts)
        report['synthetic_fact_guard_controls'] = synthetic_controls(inventory, texts)
        report['primary_android_source_scope'] = 'AOSP android-15.0.0_r1 source corroborates capacity16 and positive array lengths; the hosted Google APIs boot library was not extracted or matched byte-for-byte.'
        report['unmodified_original_coverage'] = {'visited': 259, 'instructions': 262,
            'unvisited': [232, 233, 235], 'conditional_edges_visited': 46, 'conditional_edges': 46}
        shutil.copyfile(Path(__file__), args.output / 'executed-verifier.py')
        report['status'] = 'STRUCTURAL_FACTS_VERIFIED_SYNCHRONOUS_HOST_ARGUMENT_FOR_REVIEW'
    except Exception as error:
        report['status'] = 'STRUCTURAL_FACT_REVIEW_FAILED'
        report['error'] = type(error).__name__ + ': ' + str(error)
        (args.output / 'failure-traceback.txt').write_text(traceback.format_exc())
        raise
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (args.output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({key: value for key, value in report.items() if key not in ('structural_facts', 'installed_host_constructor_facts')}, indent=2))


if __name__ == '__main__':
    main()
