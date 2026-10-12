#!/usr/bin/env python3
"""Check migrated invocation kinds and private/static accesses against original declarations.

This is a bounded static check, NOT the ART verifier. It does not prove Android API
availability, protected/package access, receiver dataflow or classloader behavior.
The separate validate_migration.py checks signatures and external-reference provenance.
"""
from __future__ import annotations
import functools,json,re,sys
from dataclasses import dataclass
from pathlib import Path
import build
from constructor_owner import restore_from_preserved_source

@dataclass(frozen=True)
class Declaration:
    parent: str | None
    interfaces: tuple[str,...]
    flags: frozenset[str]
    methods: dict[str,frozenset[str]]
    fields: dict[str,frozenset[str]]

def parse(text:str)->Declaration:
    header=re.search(r'^\.class\s+(.+)$',text,re.M)
    if not header:raise ValueError('Missing class declaration')
    parent=re.search(r'^\.super\s+(\S+)',text,re.M)
    methods={};fields={}
    for line in text.splitlines():
        if line.startswith('.method '):
            tokens=line.split();methods[tokens[-1]]=frozenset(tokens[1:-1])
        if line.startswith('.field '):
            tokens=line.split(' = ',1)[0].split();fields[tokens[-1]]=frozenset(tokens[1:-1])
    return Declaration(parent[1] if parent else None,tuple(re.findall(r'^\.implements\s+(\S+)',text,re.M)),frozenset(header[1].split()[:-1]),methods,fields)

def check_method(caller:str,opcode:str,owner:str,actual:str,member:str,flags:frozenset[str],owner_flags:frozenset[str])->list[str]:
    opcode=opcode.split('/')[0];errors=[]
    expected='invoke-static' if 'static' in flags else 'invoke-direct' if 'private' in flags or member.startswith('<init>(') else 'invoke-interface' if 'interface' in owner_flags else 'invoke-virtual'
    if opcode!=expected:errors.append('invocation kind: expected '+expected+', got '+opcode)
    if 'private' in flags and caller!=actual:errors.append('private method access from another class')
    return errors

def check_field(caller:str,opcode:str,actual:str,flags:frozenset[str])->list[str]:
    errors=[]
    if (opcode[0]=='s')!=('static' in flags):errors.append('field static/instance mismatch')
    if 'private' in flags and caller!=actual:errors.append('private field access from another class')
    return errors

def verify()->dict:
    by={};idx=build.index()
    for e in idx.values():by.setdefault(e['descriptor'],[]).append(e)
    @functools.lru_cache(None)
    def declaration(descriptor:str,domain:str):
        choices=[e for e in by.get(descriptor,[]) if (e['partition'].startswith('embedded_'))==(domain=='embedded')]
        if not choices:return None
        parsed=[parse((build.ROOT/e['path']).read_text()) for e in choices]
        if any(p!=parsed[0] for p in parsed[1:]):raise ValueError('Ambiguous declaration in source domain: '+descriptor)
        return parsed[0]
    def resolve(descriptor,member,kind,domain,seen=None):
        seen=set() if seen is None else seen
        if descriptor in seen:return None
        seen.add(descriptor);d=declaration(descriptor,domain)
        if d is None:return None
        table=d.methods if kind=='method' else d.fields
        if member in table:return descriptor,table[member]
        if member.startswith('<init>('):return None
        for parent in (d.parent,)+d.interfaces:
            if parent:
                found=resolve(parent,member,kind,domain,seen)
                if found:return found
        return None
    errors=[];constructor_proofs=[];counts={'invocations_seen':0,'fields_seen':0,'original_invocations_checked':0,'original_fields_checked':0,'external_or_unresolved':0}
    entries=json.loads((build.ROOT/'source/java-method-map.json').read_text())
    for e in entries:
        candidates=by[e['target']];domains={'embedded' if x['partition'].startswith('embedded_') else 'main' for x in candidates}
        if len(domains)!=1:raise ValueError('Migration target appears in multiple loader domains: '+e['target'])
        domain=domains.pop();helper=build.WORK/'java/smali'/(e['helper'][1:-1]+'.smali')
        if not helper.is_file():raise RuntimeError('Compile Java first: '+str(helper))
        suffix=e['method'][e['method'].index('('):]
        signature=e.get('helper_descriptor',e['helper_method']+'('+(e['target'] if e['instance'] else '')+suffix[1:])
        body=build.methods(helper.read_text())[signature]
        if e.get('constructor_owner_mappings') is not None:
            if len(candidates)!=1:raise ValueError('Constructor migration target is ambiguous: '+e['target'])
            old=build.methods((build.ROOT/candidates[0]['path']).read_text())[e['method']]
            body,corrections=restore_from_preserved_source(e,body,old,idx,build.ROOT)
            constructor_proofs.extend({'target':e['target'],'method':e['method'],**proof} for proof in corrections)
        for raw in body.splitlines():
            line=raw.strip();inv=re.match(r'(invoke-\S+) .*?, (L[^;]+;)->(\S+)',line);field=re.match(r'([is][gp]et\S*) .*?, (L[^;]+;)->(\S+)',line)
            if not inv and not field:continue
            opcode,owner,member=(inv or field).groups();kind='method' if inv else 'field';counts['invocations_seen' if inv else 'fields_seen']+=1
            found=resolve(owner,member,kind,domain)
            if found is None:counts['external_or_unresolved']+=1;continue
            actual,flags=found
            problems=check_method(e['target'],opcode,owner,actual,member,flags,declaration(owner,domain).flags) if inv else check_field(e['target'],opcode,actual,flags)
            counts['original_invocations_checked' if inv else 'original_fields_checked']+=1
            for problem in problems:errors.append({'caller':e['target']+'->'+e['method'],'line':line,'declaring_class':actual,'problem':problem})
    report={'pass':not errors,'registered_methods':len(entries),**counts,'errors':errors,'android_runtime_executed':False,'scope':__doc__.strip(),'constructor_owner_corrections':constructor_proofs}
    (build.REPORTS/'migration-linkage-check.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    result=verify();print(json.dumps(result,indent=2));sys.exit(0 if result['pass'] else 2)
