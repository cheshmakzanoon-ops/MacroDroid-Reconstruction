#!/usr/bin/env python3
"""Strict source/resource parity checks. Does not use the original APK."""
from __future__ import annotations
import argparse,hashlib,json,re,struct,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
import build

def xml_attr_mapping(path:Path):
    def canonical(e):
        children=[canonical(c) for c in e]
        # Only enum/flag declarations under attr are unordered. No layout/list ordering is ignored.
        if e.tag=='attr' and all(c.tag in ('enum','flag') for c in e):children.sort(key=repr)
        return e.tag,tuple(sorted(e.attrib.items())),(e.text or '').strip(),tuple(children)
    return canonical(ET.parse(path).getroot())

def source_files(root:Path):
    return {str(p.relative_to(root)).replace('\\','/'):p for p in root.rglob('*')
            if p.is_file() and (p==root/'AndroidManifest.xml' or p.is_relative_to(root/'res'))}

def verify(variant:str)->dict:
    root=build.ROOT;apk=root/'dist'/f'MacroDroid-5.67.8-v9-{variant}.apk'
    output=root/'build'/f'resource-verify-{variant}'
    build.run(['java','-Xmx1200m','-jar',build.APKTOOL,'d','-s','--no-assets','-f','-o',output,apk],variant+'-decode-resources.log')
    a=source_files(root/'source/android');b=source_files(output)
    changed=[n for n in sorted(a.keys()&b.keys()) if a[n].read_bytes()!=b[n].read_bytes()]
    equivalent=[];bad=[]
    for name in changed:
        if name=='res/values/attrs.xml' and xml_attr_mapping(a[name])==xml_attr_mapping(b[name]):equivalent.append(name)
        else:bad.append(name)
    build.run([build.aapt(),'dump','resources',apk],variant+'-resource-table.txt')
    table=(root/'reports'/(variant+'-resource-table.txt')).read_text()
    actual={name:rid for rid,name in re.findall(r'^    resource (0x[0-9a-f]+) ([^\s]+)',table,re.M)}
    expected={line.split(':',1)[1].split(' = ')[0]:line.split(' = ')[1].strip()
              for line in (root/'source/android/stable-ids.txt').read_text().splitlines()}
    original_public=set(json.loads((root/'source/android/original-public-resources.json').read_text())['public_resources'])
    actual_public=set(re.findall(r'^    resource 0x[0-9a-f]+ (\S+) PUBLIC',table,re.M))
    errors=[name for name in expected.keys()&actual.keys() if expected[name]!=actual[name]]
    compression=json.loads((root/'source/zip-compression.json').read_text());native=[]
    with zipfile.ZipFile(apk) as z:
        def signature(n):return n=='META-INF/MANIFEST.MF' or (n.startswith('META-INF/') and n.upper().endswith(('.RSA','.DSA','.EC','.SF')))
        actual_entries={n for n in z.namelist() if not signature(n)}
        compression_changes=[n for n in actual_entries&compression.keys() if z.getinfo(n).compress_type!=compression[n]]
        with zipfile.ZipFile(root/'source/payload.zip') as opaque:
            for n in sorted(z.namelist()):
                if not n.endswith('.so'):continue
                data=z.read(n)
                if data[:6]!=b'\x7fELF\x02\x01':raise RuntimeError('Unexpected native ELF format: '+n)
                machine=struct.unpack_from('<H',data,18)[0];phoff=struct.unpack_from('<Q',data,32)[0]
                size,count=struct.unpack_from('<HH',data,54);loads=[]
                for i in range(count):
                    start=phoff+i*size
                    if struct.unpack_from('<I',data,start)[0]!=1:continue
                    offset,address=struct.unpack_from('<QQ',data,start+8);align=struct.unpack_from('<Q',data,start+48)[0]
                    loads.append({'offset':offset,'virtual_address':address,'alignment':align,'compatible_16k':align>=16384 and (offset-address)%16384==0})
                native.append({'path':n,'sha256':hashlib.sha256(data).hexdigest(),'original_bytes_preserved':opaque.read(n)==data,'machine':machine,'load_segments':loads,'pass':machine==183 and bool(loads) and all(x['compatible_16k'] for x in loads)})
    result={'variant':variant,'apk_sha256':hashlib.sha256(apk.read_bytes()).hexdigest(),'files_expected':len(a),'files_actual':len(b),'byte_identical':len(a)-len(changed),
        'equivalent_enum_order_only':equivalent,'changed_files':bad,'missing_files':sorted(a.keys()-b.keys()),'extra_files':sorted(b.keys()-a.keys()),
        'resource_ids_expected':len(expected),'resource_ids_actual':len(actual),'changed_resource_ids':sorted(errors),
        'missing_resource_names':sorted(expected.keys()-actual.keys()),'extra_resource_names':sorted(actual.keys()-expected.keys()),
        'missing_apk_entries':sorted(compression.keys()-actual_entries),'extra_apk_entries':sorted(actual_entries-compression.keys()),
        'changed_zip_compression_methods':compression_changes,'native_libraries':native,'public_resources_expected':len(original_public),'public_resources_actual':len(actual_public),'public_resource_visibility_changes':sorted(original_public^actual_public)}
    result['pass']=not any(result[k] for k in ('changed_files','missing_files','extra_files','changed_resource_ids','missing_resource_names','extra_resource_names','missing_apk_entries','extra_apk_entries','changed_zip_compression_methods','public_resource_visibility_changes')) and all(n['pass'] and n['original_bytes_preserved'] for n in native)
    (root/'reports'/f'{variant}-resource-parity.json').write_text(json.dumps(result,indent=2))
    if not result['pass']:raise RuntimeError('Resource/packaging parity failed; see report')
    print(f'{variant}: {len(a)} resources, {len(expected)} IDs, {len(native)} native libraries verified')
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--variant',choices=['baseline','hybrid'],default='baseline')
    build.bootstrap();verify(parser.parse_args().variant)
