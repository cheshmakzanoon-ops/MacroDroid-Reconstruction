#!/usr/bin/env python3
"""Recover side-effect-free constant/no-op methods into editable Java.
Only exact, narrowly recognized instruction forms are accepted. Constructors,
exception handlers, class initialization, branches and field access are excluded.
"""
from __future__ import annotations
import hashlib,json,re,struct
from pathlib import Path
import build
METHOD=build.METHOD

def descriptor_types(s:str)->list[str]:
    result=[];i=0
    while i<len(s):
        start=i
        while s[i]=='[':i+=1
        if s[i]=='L':i=s.index(';',i)+1
        else:i+=1
        result.append(s[start:i])
    return result

def bridge_type(t:str)->tuple[str,str]:
    values={'Z':'boolean','B':'byte','S':'short','C':'char','I':'int','J':'long','F':'float','D':'double','V':'void'}
    if t in values:return values[t],t
    if t=='Ljava/lang/String;':return 'String',t
    return 'Object','Ljava/lang/Object;'

def java_string(value:str)->str:
    result='"'
    for c in value:
        n=ord(c)
        if c=='"':result+='\\"'
        elif c=='\\':result+='\\\\'
        elif n<32 or n==127:result+='\\'+format(n,'03o')
        elif n>126:
            for i in range(0,len(c.encode('utf-16be','surrogatepass')),2):result+='\\u'+c.encode('utf-16be','surrogatepass')[i:i+2].hex()
        else:result+=c
    return result+'"'

def constant(block:str):
    header=block.splitlines()[0];sig=header.split()[-1];ret=sig.rsplit(')',1)[1]
    if sig.startswith(('<init>','<clinit>')) or ' abstract ' in header or ' native ' in header or '.catch' in block:return None
    body=build.ANNOT.sub('',block)
    lines=[x.strip() for x in body.splitlines() if x.strip() and not x.strip().startswith(('.','#',':'))]
    if lines==['return-void']:return {'kind':'void','java':'','value':None,'return':ret}
    if len(lines)!=2:return None
    first,last=lines
    m=re.fullmatch(r'(const(?:/[\w]+)?|const-wide(?:/[\w]+)?) ([vp]\d+), (-?0x[0-9a-f]+)(?:\s+#.*)?',first)
    if m:
        reg,value=m[2],int(m[3],16)
        if last=='return-void' and ret=='V':return {'kind':'void','java':'','value':None,'return':ret}
        if last not in ('return '+reg,'return-wide '+reg,'return-object '+reg):return None
        if ret=='Z' and value in (0,1):return {'kind':'integer','java':'true' if value else 'false','value':value,'return':ret}
        if ret=='I' and -(1<<31)<=value<(1<<32):
            if value>=1<<31:value-=1<<32
            return {'kind':'integer','java':str(value),'value':value,'return':ret}
        if ret=='J' and -(1<<63)<=value<(1<<64):
            if value>=1<<63:value-=1<<64
            return {'kind':'long','java':str(value)+'L','value':value,'return':ret}
        if ret=='D' and value==0:return {'kind':'double','java':'0.0d','value':0.0,'return':ret}
        if (ret.startswith('L') or ret.startswith('[')) and value==0 and last=='return-object '+reg:return {'kind':'null','java':'null','value':None,'return':ret}
        return None
    m=re.fullmatch(r'const-string(?:/jumbo)? ([vp]\d+), ("(?:[^"\\]|\\.)*")(?:\s+#.*)?',first)
    if m and ret=='Ljava/lang/String;' and last=='return-object '+m[1]:
        try:value=json.loads(m[2].replace("\\'", "'"))
        except json.JSONDecodeError:return None
        return {'kind':'string','java':java_string(value),'value':value,'return':ret}
    return None

def generate()->dict:
    root=build.ROOT
    registry=json.loads((root/'source/java-method-map.json').read_text())
    registry=[e for e in registry if e.get('proof_family')!='constant']
    used={(e['target'],e['method']) for e in registry};groups={};added=[]
    for item in build.index().values():
        desc=item['descriptor']
        if not desc.startswith('Lcom/arlosoft/macrodroid/'):continue
        text=(root/item['path']).read_text()
        for match in METHOD.finditer(text):
            block=match[0];head=block.splitlines()[0];sig=head.split()[-1]
            if (desc,sig) in used:continue
            c=constant(block)
            if c is None:continue
            instance=' static ' not in head
            params=descriptor_types(sig.split('(',1)[1].split(')',1)[0])
            params=([desc] if instance else [])+params
            bridges=[bridge_type(t) for t in params];rt,rd=bridge_type(c['return'])
            short=re.sub(r'[^A-Za-z0-9_$]','_',desc.split('/')[-1][:-1]).replace('$','_')
            cls=short+'_'+hashlib.sha256(desc.encode()).hexdigest()[:8]
            method=re.sub(r'[^A-Za-z0-9_$]','_',sig.split('(')[0])+'_'+hashlib.sha256(sig.encode()).hexdigest()[:8]
            path='source/java/recovered/constants/'+cls+'.java';helper='Lrecovered/constants/'+cls+';'
            helperdesc=method+'('+''.join(d for _,d in bridges)+')'+rd
            stmt='return;' if c['kind']=='void' else 'return '+c['java']+';'
            source='    /** Original: '+sig.replace('*/','* /')+' */\n    public static '+rt+' '+method+'('+', '.join(t+' a'+str(i) for i,(t,_) in enumerate(bridges))+') { '+stmt+' }\n'
            groups.setdefault((cls,path),[]).append(source)
            entry={'target':desc,'method':sig,'helper':helper,'helper_method':method,'helper_descriptor':helperdesc,'instance':instance,'java_source':path,'proof_family':'constant','original_method_sha256':hashlib.sha256(block.encode()).hexdigest(),'expected':{k:v for k,v in c.items() if k!='java'}}
            registry.append(entry);added.append(entry)
    out=root/'source/java/recovered/constants';out.mkdir(parents=True,exist_ok=True)
    for (cls,path),lines in groups.items():
        (root/path).write_text('package recovered.constants;\n/** Recovered constant/no-op methods. Object bridge parameters are unused and never alter the target API. */\npublic final class '+cls+' {\n    private '+cls+'() {}\n'+''.join(lines)+'}\n')
    (root/'source/java-method-map.json').write_text(json.dumps(registry,indent=2,ensure_ascii=True))
    summary={'new_constant_or_noop_methods':len(added),'classes':len(groups),'total_java_methods':len(registry),'scope':'Exact constant/no-op forms only; not complex business logic or Android execution.'}
    (root/'reports/v5-constant-migration.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2));return summary
if __name__=='__main__':generate()
