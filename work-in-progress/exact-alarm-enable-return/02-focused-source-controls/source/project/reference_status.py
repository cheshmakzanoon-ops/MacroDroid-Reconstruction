#!/usr/bin/env python3
"""Inventory historical JADX failures with exact registered replacement signatures.
A matching helper supersedes one method only. It does not make the containing Java
reference file a compilable class or establish runtime equivalence.
"""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PRIMITIVES=dict(zip('VZBCSIJFD',['void','boolean','byte','char','short','int','long','float','double']))

def type_name(text:str,index:int=0)->tuple[str,int]:
    start=index
    while index<len(text) and text[index]=='[':index+=1
    dimensions=index-start
    if index>=len(text):raise ValueError('Truncated type descriptor')
    if text[index]=='L':
        end=text.index(';',index);name=text[index+1:end].replace('/','.').replace('$','.');index=end+1
    else:name=PRIMITIVES[text[index]];index+=1
    return name+'[]'*dimensions,index

def signature(entry:dict)->str:
    method=entry['method'];name,desc=method.split('(',1);args=[];i=0
    while desc[i]!=')':value,i=type_name(desc,i);args.append(value)
    result,end=type_name(desc,i+1)
    if end!=len(desc):raise ValueError('Trailing method descriptor')
    owner=entry['target'][1:-1].replace('/','.').replace('$','.')
    return owner+'.'+name+'('+', '.join(args)+'):'+result

def inventory()->dict:
    registry=json.loads((ROOT/'source/java-method-map.json').read_text());registered={signature(e):e for e in registry}
    rows=[];files=sorted((ROOT/'reference/java').rglob('*.java'))
    for path in files:
        for line,text in enumerate(path.read_text(errors='strict').splitlines(),1):
            for match in re.finditer(r'Method not decompiled: ([^"\n]+)',text):
                marker=match[1];entry=registered.get(marker)
                rows.append({'reference':path.relative_to(ROOT).as_posix(),'line':line,'marker':marker,
                             'registered_replacement':None if entry is None else {'target':entry['target'],'method':entry['method'],'java_source':entry['java_source'],'helper':entry['helper']}})
    return {'reference_java_files':len(files),'failed_decompilation_markers':len(rows),
            'markers_with_registered_replacements':sum(x['registered_replacement'] is not None for x in rows),
            'markers_without_registered_replacements':sum(x['registered_replacement'] is None for x in rows),
            'reference_tree_is_compilable_application':False,'android_runtime_executed':False,
            'scope':'Exact-signature metadata inventory; compilation and behavior have separate checks','markers':rows}

def main():
    result=inventory();(ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports/reference-failures-status-v9.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='markers'},indent=2))
if __name__=='__main__':main()
