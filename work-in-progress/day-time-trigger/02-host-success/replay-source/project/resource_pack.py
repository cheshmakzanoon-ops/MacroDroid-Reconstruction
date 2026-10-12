#!/usr/bin/env python3
"""Restore original resource ZIP paths after AAPT2 recompilation.

Only global resource-table strings are replaced; resource IDs/string indices, styles,
package tables and all other string bytes are retained. Original APK is not needed.
"""
from __future__ import annotations
import json,re,struct,zipfile
from pathlib import Path

def file_values(text:str)->dict[str,str]:
    result={};rid=None
    for line in text.splitlines():
        m=re.match(r'    resource (0x[0-9a-f]+) (\S+)',line)
        if m:rid=m[1]
        m=re.match(r'      \(([^)]*)\) \(file\) (\S+)',line)
        if m:
            if rid is None:raise ValueError('File value without resource ID')
            key=rid+'|'+m[1]
            if key in result and result[key]!=m[2]:raise ValueError('Ambiguous file resource')
            result[key]=m[2]
    return result

def length8(data:bytes,pos:int)->tuple[int,int]:
    first=data[pos]
    return (((first&127)<<8)|data[pos+1],pos+2) if first&128 else (first,pos+1)

def length16(data:bytes,pos:int)->tuple[int,int]:
    first=struct.unpack_from('<H',data,pos)[0]
    return (((first&32767)<<16)|struct.unpack_from('<H',data,pos+2)[0],pos+4) if first&32768 else (first,pos+2)

def encode_length8(n:int)->bytes:
    if n<0 or n>32767:raise ValueError('UTF-8 resource string too long')
    return bytes([n]) if n<128 else bytes([128|(n>>8),n&255])

def encode_length16(n:int)->bytes:
    return struct.pack('<H',n) if n<32768 else struct.pack('<HH',32768|(n>>16),n&65535)

def replace_pool(pool:bytes,mapping:dict[str,str])->tuple[bytes,set[str]]:
    kind,header,size=struct.unpack_from('<HHI',pool)
    if kind!=1 or header<28 or size!=len(pool):raise ValueError('Invalid global string pool')
    count,stylecount,flags,start,stylestart=struct.unpack_from('<5I',pool,8)
    if start<header+4*(count+stylecount):raise ValueError('Overlapping string offsets')
    offsets=struct.unpack_from('<'+str(count)+'I',pool,header)
    chunks=[];new_offsets=[];changed=set();cursor=0
    for offset in offsets:
        pos=start+offset;begin=pos
        if flags&256:
            _,pos=length8(pool,pos);n,pos=length8(pool,pos);raw=pool[pos:pos+n];end=pos+n+1
            if pool[end-1]!=0:raise ValueError('Missing UTF-8 terminator')
            value=raw.decode('utf-8',errors='surrogatepass')
        else:
            n,pos=length16(pool,pos);raw=pool[pos:pos+2*n];end=pos+2*n+2
            if pool[end-2:end]!=b'\0\0':raise ValueError('Missing UTF-16 terminator')
            value=raw.decode('utf-16le',errors='surrogatepass')
        encoded=pool[begin:end]
        if value in mapping and mapping[value]!=value:
            new=mapping[value];raw=new.encode('utf-8' if flags&256 else 'utf-16le')
            chars=len(new.encode('utf-16le'))//2
            encoded=(encode_length8(chars)+encode_length8(len(raw))+raw+b'\0') if flags&256 else (encode_length16(chars)+raw+b'\0\0')
            changed.add(value)
        new_offsets.append(cursor);chunks.append(encoded);cursor+=len(encoded)
    blob=b''.join(chunks);blob+=b'\0'*((-len(blob))%4)
    prefix=bytearray(pool[:start]);struct.pack_into('<'+str(count)+'I',prefix,header,*new_offsets)
    tail=pool[stylestart:] if stylestart else b''
    newstyle=start+len(blob) if stylestart else 0
    struct.pack_into('<I',prefix,24,newstyle)
    if changed:struct.pack_into('<I',prefix,16,flags&~1) # Updated strings cannot claim sorted order.
    result=prefix+blob+tail;struct.pack_into('<I',result,4,len(result))
    return bytes(result),changed

def replace_table_paths(data:bytes,mapping:dict[str,str])->tuple[bytes,set[str]]:
    kind,header,size=struct.unpack_from('<HHI',data)
    if kind!=2 or size!=len(data):raise ValueError('Invalid resources.arsc')
    out=[data[:header]];pos=header;replaced=set();seen_pool=False
    while pos<len(data):
        t,h,n=struct.unpack_from('<HHI',data,pos)
        if n<h or pos+n>len(data):raise ValueError('Invalid resource chunk bounds')
        chunk=data[pos:pos+n]
        if t==1:
            if seen_pool:raise ValueError('Unexpected second global pool')
            chunk,replaced=replace_pool(chunk,mapping);seen_pool=True
        out.append(chunk);pos+=n
    result=bytearray(b''.join(out));struct.pack_into('<I',result,4,len(result))
    if not seen_pool:raise ValueError('No global resource string pool')
    return bytes(result),replaced

def restore(root:Path,linked:Path,table_dump:Path)->Path:
    old=json.loads((root/'source/android/original-resource-paths.json').read_text())['by_id_and_config']
    current=file_values(table_dump.read_text());mapping={};reverse={}
    for key,newpath in current.items():
        oldpath=old.get(key,newpath)
        if newpath in mapping and mapping[newpath]!=oldpath:raise ValueError('Conflicting resource path mapping')
        if oldpath in reverse and reverse[oldpath]!=newpath:raise ValueError('Many source paths map to one destination')
        mapping[newpath]=oldpath;reverse[oldpath]=newpath
    output=linked.with_name('restored.apk')
    with zipfile.ZipFile(linked) as src,zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
        data,changed=replace_table_paths(src.read('resources.arsc'),mapping)
        missing=set(mapping)-set(src.namelist())
        if missing:raise ValueError('Resource table references missing files: '+str(sorted(missing)[:5]))
        needed={a for a,b in mapping.items() if a!=b}
        if changed!=needed:raise ValueError('Not all resource strings were rewritten')
        written=set()
        for info in src.infolist():
            name=mapping.get(info.filename,info.filename)
            if name in written:raise ValueError('Duplicate output ZIP entry')
            written.add(name);raw=data if info.filename=='resources.arsc' else src.read(info.filename)
            info.filename=name;out.writestr(info,raw)
    (root/'reports/resource-path-restoration.json').write_text(json.dumps({'rewritten_paths':len(changed),'resource_file_mapping_count':len(mapping),'missing_original_id_config_keys':sorted(set(old)-set(current)),'original_apk_required':False},indent=2))
    return output
