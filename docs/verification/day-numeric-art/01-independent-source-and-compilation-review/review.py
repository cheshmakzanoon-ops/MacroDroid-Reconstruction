#!/usr/bin/env python3
"""Read-only review of already-compiled neutral probe and retained case output."""
import collections
import datetime
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import stat
import struct
import sys
import traceback
import zlib

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'attempt-01'
DESIGN = Path('/dev/shm/macrodroid-day-numeric-art/source-draft-02')
COMPILED = Path('/dev/shm/macrodroid-day-numeric-art/checkpoints/02-compiled-probe-and-corpus')
PINS = [(DESIGN, '707afe796307be6044a5571cc39d4480ec032d2bf3d0ad87eb9a75118959deda'),
        (COMPILED, 'e3c67ab9f469e39b637cba2efd0ca6bd1a0892e49cc6333638b0b6aab66fd5ad')]


def identity(path):
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode)
    raw = path.read_bytes()
    after = path.lstat()
    assert (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) == (
        after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'mode':stat.S_IMODE(after.st_mode)}


def load(path):
    return json.loads(path.read_bytes())


def save(name,value):
    with (OUT/name).open('x') as f:
        json.dump(value,f,indent=2);f.write('\n')


def block(text,anchor):
    start = text.index(anchor)
    opening = text.index('{',start)
    depth = 0
    for i in range(opening,len(text)):
        if text[i] == '{':depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:return text[start:i+1]
    raise ValueError(anchor)


def expected(row):
    """Third read-only arithmetic implementation, using exact rational truncation.

    Float decoding obtains the represented binary64 value. Fraction.from_float
    then expresses every finite value exactly, so no decimal parse or rounded
    intermediate multiplication participates in the integer expectation.
    """
    bits = int(row['rawBitsHex'],16)
    kind = row['kind']
    if kind == 'null-entry':return 'exception:java.lang.NullPointerException'
    if kind == 'integer':
        low = bits % (1 << 32)
        value = low if low < (1 << 31) else low - (1 << 32)
    elif kind == 'decimal':
        number = struct.unpack('>d',bits.to_bytes(8,'big'))[0]
        if math.isnan(number):value=0
        elif math.isinf(number):value=-(1 << 31) if number < 0 else (1 << 31)-1
        else:
            value = int(Fraction.from_float(number))
            value = max(-(1 << 31),min((1 << 31)-1,value))
    else:value=0
    return 'value:' + str(value)


def dex_metadata(raw):
    assert raw[:8] == b'dex\n035\0'
    assert struct.unpack_from('<III',raw,32) == (len(raw),112,0x12345678)
    assert struct.unpack_from('<I',raw,8)[0] == zlib.adler32(raw[12:]) & 0xffffffff
    assert raw[12:32] == hashlib.sha1(raw[32:]).digest()
    ns,so,nt,to = struct.unpack_from('<IIII',raw,56)
    nc,co = struct.unpack_from('<II',raw,96)
    assert nc == 1
    def descriptor(i):
        assert 0 <= i < nt
        si = struct.unpack_from('<I',raw,to+i*4)[0]
        assert 0 <= si < ns
        cursor = struct.unpack_from('<I',raw,so+si*4)[0]
        length = 0
        for part in range(5):
            value = raw[cursor];cursor += 1
            length |= (value & 127) << (part*7)
            if value < 128:break
        else:raise ValueError('DEX string length')
        text = raw[cursor:raw.index(b'\0',cursor)].decode('ascii')
        assert len(text) == length
        return text
    types = sorted(descriptor(i) for i in range(nt))
    owner = descriptor(struct.unpack_from('<I',raw,co)[0])
    assert owner == 'Lrecovered/probe/DayNumericMethodProbe;'
    for value in types:
        simple=value.lstrip('[')
        assert simple in 'VZBSCIJFD' or simple == owner or simple.startswith('Ljava/') or simple in (
            'Ldalvik/annotation/Signature;','Ldalvik/annotation/Throws;'),value
    return {'class_count':nc,'class':owner,'types':types,'internal_checksums_exact':True,
            'application_or_android_class_definitions':0,'direct_application_or_android_types':0}


def main():
    bindings=[]
    before={}
    for root,expected_cp in PINS:
        cp_id=identity(root/'checkpoint.json');assert cp_id['sha256']==expected_cp
        cp=load(root/'checkpoint.json')
        rows=cp['files'];assert len({r['path'] for r in rows})==len(rows)
        current=[]
        for row in rows:
            rel=Path(row['path']);assert not rel.is_absolute() and '..' not in rel.parts
            p=root/rel;got=identity(p);assert got=={k:row[k] for k in ('bytes','sha256','mode')},str(p)
            before[str(p)]=got;current.append({'path':row['path'],**got})
        before[str(root/'checkpoint.json')]=cp_id
        bindings.append({'capsule':str(root),'checkpoint':cp_id,'payloads':current})
    assert [len(r['payloads']) for r in bindings]==[31,33]
    save('capsule-bindings.json',bindings)
    source_rel='source/recovered/probe/DayNumericMethodProbe.java'
    source=(DESIGN/source_rel).read_text()
    assert source==(COMPILED/'evidence'/source_rel).read_text()
    assert identity(DESIGN/source_rel)['sha256']=='ab5b1b1d01ab33f66cab22c1d5a5f7c09ffdf13b8e0e335cf22f86ba5fcc6c2b'
    host=(DESIGN/'inputs/DayTriggerParityCases.java').read_text()
    adapted_expected=block(host,'    static Integer expected(Input input)').replace(
        'expected(Input input)','expected(Object[] input)').replace('input.kind()','kind(input)').replace('input.bits()','bits(input)')
    assert adapted_expected==block(source,'    static Integer expected(Object[] input)')
    adapted_cases=block(host,'    static List<Input> cases()').replace('List<Input>','List<Object[]>')
    adapted_cases,count=re.subn(r'new Input\((.+)\)\);',r'new Object[]{\1});',adapted_cases)
    assert count==19
    old='        require(out.stream().map(Input::name).distinct().count() == out.size(), "Duplicate case identifiers");'
    new='        Set<String> names = new HashSet<String>();\n        for (Object[] input : out) require(names.add(name(input)), "Duplicate case identifiers");'
    assert adapted_cases.count(old)==1
    adapted_cases=adapted_cases.replace(old,new).replace('INPUT_INVENTORY_SHA256','INVENTORY_SHA256')
    assert adapted_cases==block(source,'    static List<Object[]> cases()')
    method=re.search(r'(?ms)^\.method public static r0\([^\n]*\n.*?^\.end method$',(
        DESIGN/'inputs/original-smali/DayTrigger_74d1108db13471a8.smali').read_text()).group(0)
    assert hashlib.sha256(method.encode()).hexdigest()=='8383c90ebe3d35afa63d52cf92cd4c92b54ed4525ca0d8a31a29fe603f9eef21'
    assert method.count('->getVariable()')==1 and method.count('long-to-int')==method.count('double-to-int')==1
    (OUT/'reviewed-original-r0.smali').write_text(method)
    parent_rows=load(DESIGN/'baseline-source-rows.json')
    for row in parent_rows:
        got=identity(DESIGN/'inputs/original-smali'/Path(row['path']).name)
        assert got['bytes']==row['size'] and got['sha256']==row['sha256']
    save('source-mechanism-review.json',{
        'source':identity(DESIGN/source_rel),'exact_original_method_sha256':hashlib.sha256(method.encode()).hexdigest(),
        'original_class_fingerprints_exact':10,'cases_and_expectations_exact_mechanical_host_adaptation':True,
        'constructor_sites_use_reflection_on_actual_app_types':True,
        'no_recovered_target_body_substituted':True,
        'target_method':'public static int DayTrigger.r0(DictionaryEntry)',
        'zero_argument_runtime_branch':True,
        'only_exception_class_allowed':'java.lang.NullPointerException',
        'exception_case_only':'null-entry','message':'Complete UTF-16 code units retained; no equality requirement for this one VM-generated message.',
        'declared_mutated_fields':[{'case':'null-value','class':'VariableValue$DictionaryEntry','field':'variable'},
                                  {'case':'string-null','class':'VariableValue$StringValue','field':'textValue'}],
        'getter_readback_scope':'547 integer and 734 decimal direct target-value cases; nested inner integer not separately read back.',
        'identity_readback_scope':'Every outer non-null entry. The nested inner reference follows exact reviewed constructor stores without an extra readback.',
        'wrapper_and_runtime_review_pending':True})

    protocol=load(DESIGN/'protocol.json')
    assert protocol['constructor_invalid_states_injected_into_disposable_objects']==['null-value','string-null']
    result=load(COMPILED/'evidence/result.json')
    assert result['passed'] is True and result['probe_runtime_executed'] is False and result['android_executed'] is False
    assert len(result['commands'])==5
    labels=['java-version','javac-version','neutral-probe-javac','inventory-only-jvm','neutral-probe-d8']
    assert [r['label'] for r in result['commands']]==labels
    for row in result['commands']:
        folder=COMPILED/'evidence/commands'/row['label']
        assert load(folder/'command.json')==row
        assert type(row['returncode']) is int and row['returncode']==0 and row['timed_out'] is False
        assert row['timeout_seconds']==(30 if row['label'].endswith('version') else 120)
        for stream in ('stdout','stderr'):
            assert identity(folder/(stream+'.txt'))==row[stream]
    inventory_argv=result['commands'][3]['argv']
    assert inventory_argv[-2:]==['recovered.probe.DayNumericMethodProbe','--inventory'] and '-Xverify:all' in inventory_argv
    assert result['commands'][2]['argv'][-1].endswith('/source/recovered/probe/DayNumericMethodProbe.java')
    assert result['commands'][4]['argv'][-1].endswith('/classes/recovered/probe/DayNumericMethodProbe.class')
    save('inspected-five-commands.json',{'commands':result['commands'],'new_commands_executed_by_this_review':0})

    rows=load(COMPILED/'evidence/exact-input-corpus.json')
    previous=load(COMPILED/'evidence/independent-python-expectations.json')
    raw=(COMPILED/'evidence/commands/inventory-only-jvm/stdout.txt').read_text()
    lines=raw.splitlines();assert len(lines)==1293
    assert lines[0]=='DAY_NUMERIC_INPUTS_BEGIN\tcases=1291\tsha256='+protocol['input_inventory_sha256']
    assert lines[-1]=='DAY_NUMERIC_INPUTS_END\tcases=1291\tandroid_executed=false'
    compact=json.dumps(rows,ensure_ascii=False,separators=(',',':')).encode()
    assert hashlib.sha256(compact).hexdigest()==protocol['input_inventory_sha256']
    assert len(rows)==len(previous)==1291 and len({r['case'] for r in rows})==1291
    reviewed=[]
    for i,row in enumerate(rows):
        encoded,actual=lines[i+1].split('\t')
        assert json.loads(encoded)==row
        wanted=expected(row)
        assert actual==wanted==previous[i]['expected'] and previous[i]['case']==row['case']
        reviewed.append({'case':row['case'],'kind':row['kind'],'rawBitsHex':row['rawBitsHex'],'expected':wanted})
    counts=dict(collections.Counter(r['kind'] for r in rows))
    assert counts=={'integer':547,'decimal':734,'null-entry':1,'null-value':1,'string':4,'boolean':2,'dictionary':1,'nested-entry':1}
    save('independent-rational-expectations.json',reviewed)
    save('corpus-review.json',{'cases':1291,'per_kind':counts,'compact_inventory_sha256':hashlib.sha256(compact).hexdigest(),
         'all_java_and_existing_python_expectations_agree':True,'review_arithmetic':'Finite binary64 decoded to an exact Fraction before truncation and saturation; integers use signed modulo 2^32.',
         'real_target_or_probe_execution_by_this_review':False})

    dex=COMPILED/'evidence/dex/classes.dex';assert identity(dex)['bytes']==14108
    assert identity(dex)['sha256']=='7cf6f31793b1f0546bf4927a63481a25662634b8a0ac2fa520a69900204ed3aa'
    metadata=dex_metadata(dex.read_bytes())
    assert metadata['types']==load(COMPILED/'evidence/probe-dex-metadata.json')['typed_references']
    class_data=(COMPILED/'evidence/classes/recovered/probe/DayNumericMethodProbe.class').read_bytes()
    assert class_data[:4]==b'\xca\xfe\xba\xbe' and struct.unpack_from('>H',class_data,6)[0]==52
    metadata.update(dex_identity=identity(dex),classfile_major_version=52)
    save('independent-dex-review.json',metadata)
    after={name:identity(Path(name)) for name in before}
    assert after==before
    save('all-read-inputs-before.json',before);save('all-read-inputs-after.json',after)
    return {'status':'INDEPENDENT_NEUTRAL_NUMERIC_SOURCE_AND_COMPILATION_REVIEW_PASSED',
       'capsules_verified':2,'payloads_verified':64,'source_sha256':identity(DESIGN/source_rel)['sha256'],
       'dex_sha256':identity(dex)['sha256'],'dex_bytes':14108,'class_definitions':1,
       'cases_verified':1291,'java_expectations_and_two_python_analyses_agree':True,
       'original_method_body_hash_verified':True,'source_semantic_blockers':[],
       'documentation_scope_refinement':'Getter-bit and contained-identity readbacks cover direct numeric inputs and outer entries; nested inner state is constructor-bound, not separately observed.',
       'new_suites_executed':0,'new_compilation_executed':False,'android_executed':False,
       'actual_target_executed':False,'probe_runtime_executed':False,'application_build_executed':False,
       'wrapper_or_workflow_reviewed':False,'all_read_inputs_unchanged':True,'new_runtime_parity_credit':0}


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=False)
    execution={'argv':sys.argv,'python':sys.executable,'source':identity(Path(__file__).resolve()),
               'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'scope':'Read-only capsule, source, stored command and stored inventory analysis. No compiler, JVM, ART, suite or Git invocation.'}
    try:
        result=main();code=0
    except BaseException as error:
        result={'status':'INDEPENDENT_REVIEW_ATTEMPT_FAILED','error_type':type(error).__name__,
                'error':str(error),'traceback':traceback.format_exc(),'source_modified':False}
        traceback.print_exc();code=1
    execution.update(returncode=code,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    save('execution.json',execution);save('result.json',result)
    print(json.dumps(result,indent=2))
    raise SystemExit(code)
