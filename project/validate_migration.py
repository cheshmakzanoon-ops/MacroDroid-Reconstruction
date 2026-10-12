#!/usr/bin/env python3
"""Validate constant-body equivalence, bridge ABI widths and all migrated member references.
This is static evidence. It does not assert Android lifecycle or device behavior.
"""
from __future__ import annotations
import functools,hashlib,json,re
from pathlib import Path
import build
from migrate_constants import constant,descriptor_types,bridge_type

METHOD_REF=re.compile(r'(L[^\s,;]+;)->([^\s(]+\([^\s)]*\)[^\s,]+)')
FIELD_REF=re.compile(r'(L[^\s,;]+;)->([^\s:(]+:[^\s,]+)')

def verify()->dict:
    idx=build.index();by={v['descriptor']:v for v in idx.values()};registry=json.loads((build.ROOT/'source/java-method-map.json').read_text())
    d=build.WORK/'java/smali';errors=[];proofs=[];calls=set();fields=set();external_original=set();external_fields=set()
    @functools.lru_cache(None)
    def original(desc:str)->str:return (build.ROOT/by[desc]['path']).read_text()
    @functools.lru_cache(None)
    def helper(path:str)->dict:return build.methods((d/(path[1:-1]+'.smali')).read_text())
    @functools.lru_cache(None)
    def declarations(desc:str):
        if desc not in by:return None
        text=original(desc);parent=re.search(r'^\.super (\S+)',text,re.M);interfaces=re.findall(r'^\.implements (\S+)',text,re.M)
        ms=build.methods(text);fs={l.split(' = ')[0].split()[-1] for l in text.splitlines() if l.startswith('.field ')}
        return ms,fs,([parent[1]] if parent else [])+interfaces
    def resolves(desc:str,signature:str,kind:str,visited=None):
        visited=set() if visited is None else visited
        if desc in visited:return False
        visited.add(desc);definition=declarations(desc)
        if definition is None:return None
        ms,fs,parents=definition
        if signature in (ms if kind=='method' else fs):return True
        if kind=='method' and signature.startswith('<init>'):return False
        unknown=False
        for p in parents:
            result=resolves(p,signature,kind,visited)
            if result is True:return True
            if result is None:unknown=True
        return None if unknown else False
    for e in registry:
        old=build.methods(original(e['target']))[e['method']]
        external_original.update(METHOD_REF.findall(old));external_fields.update(FIELD_REF.findall(old))
    for e in registry:
        old=build.methods(original(e['target']))[e['method']]
        suffix=e['method'][e['method'].index('('):]
        hs=e.get('helper_descriptor',e['helper_method']+'('+(e['target'] if e['instance'] else '')+suffix[1:])
        new=helper(e['helper'])[hs]
        expected_params=([e['target']] if e['instance'] else [])+descriptor_types(suffix[1:].split(')')[0])
        helper_params=descriptor_types(hs.split('(',1)[1].split(')')[0])
        widths=lambda ts:[2 if t in ('J','D') else 1 for t in ts]
        if widths(expected_params)!=widths(helper_params):errors.append({'target':e['target'],'method':e['method'],'reason':'Argument-register ABI mismatch'})
        if e.get('proof_family')=='constant':
            oc=constant(old);nc=constant(new)
            if oc is None or nc is None or (oc['kind'],oc['value'])!=(nc['kind'],nc['value']):errors.append({'target':e['target'],'method':e['method'],'reason':'Constant-body proof failed'})
            if hashlib.sha256(old.encode()).hexdigest()!=e['original_method_sha256']:errors.append({'target':e['target'],'method':e['method'],'reason':'Original constant body changed'})
            proofs.append({'target':e['target'],'method':e['method'],'value_equal':oc is not None and nc is not None and (oc['kind'],oc['value'])==(nc['kind'],nc['value'])})
        elif expected_params!=helper_params:errors.append({'target':e['target'],'method':e['method'],'reason':'Unexpected reference bridge in nonconstant body'})
        body=new.split('\n',1)[1]
        if 'Lrecovered/' in body or 'Ldefpackage/' in body:errors.append({'target':e['target'],'method':e['method'],'reason':'Compile-only reference leaked'})
        calls.update(METHOD_REF.findall(body));fields.update(FIELD_REF.findall(body))
    resolved=0;external=[]
    for kind,refs,permitted in [('method',calls,external_original),('field',fields,external_fields)]:
        for owner,sig in sorted(refs):
            answer=resolves(owner,sig,kind)
            if answer is True:resolved+=1
            elif answer is False:errors.append({'kind':kind,'owner':owner,'member':sig,'reason':'Missing member in preserved application/library source'})
            elif (owner,sig) not in permitted:external.append({'kind':kind,'owner':owner,'member':sig})
    # Any previously unseen external API needs review, not an automatic device-compatibility claim.
    errors.extend({'reason':'New external API reference requires review',**v} for v in external)
    report={'pass':not errors,'methods_registered':len(registry),'constant_methods_proven':len(proofs),'member_references_checked':len(calls)+len(fields),'app_members_resolved':resolved,'new_external_refs':external,'errors':errors,'android_executed':False}
    (build.REPORTS/'migration-static-proof.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
    if errors:raise RuntimeError('Migration validation failed; see report')
    return report
if __name__=='__main__':verify()
