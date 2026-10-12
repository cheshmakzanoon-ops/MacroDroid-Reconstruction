#!/usr/bin/env python3
"""Offline source build: smali baseline + optional javac/D8 method reconstruction.
The original APK/DEX files are NOT build inputs. Test doubles never enter the APK.
"""
from __future__ import annotations
import argparse,hashlib,json,os,re,shutil,struct,subprocess,sys,tempfile,uuid,zipfile,zlib,time
import xml.etree.ElementTree as ET
from pathlib import Path
from constructor_owner import restore_from_preserved_source
ROOT=Path(__file__).resolve().parent
JAR=ROOT/'tools/lib/jadx-r2721.4574686-all.jar'
TOOLS=ROOT/'tools/classes'
WORK=ROOT/'build'
REPORTS=ROOT/'reports'
APKTOOL=ROOT/'tools/apktool_v3.0.3-26-0a1c54f7-SNAPSHOT.jar'

def remove_generated_directory(path:Path)->None:
    """Never continue a build or control with a partially removed staging tree."""
    if path.is_symlink():raise RuntimeError('Generated staging must not be a symbolic link: '+str(path))
    if not path.exists():return
    if not path.is_dir():raise RuntimeError('Generated staging must be a directory: '+str(path))
    retired=path.with_name(path.name+'-retired-'+uuid.uuid4().hex)
    if retired.exists():raise RuntimeError('Generated retirement path already exists: '+str(retired))
    path.rename(retired)
    shutil.rmtree(retired)
    if path.exists():raise RuntimeError('Generated staging reappeared during retirement: '+str(path))

def run(args:list[str|Path],log:str)->None:
    REPORTS.mkdir(exist_ok=True)
    with (REPORTS/log).open('w',encoding='utf-8') as f:
        f.write('COMMAND: '+json.dumps([str(x) for x in args])+'\n');f.flush()
        p=subprocess.run([str(x) for x in args],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
    if p.returncode:
        raise RuntimeError(f'Command failed ({p.returncode}); see reports/{log}\n'+(REPORTS/log).read_text(errors='replace')[-4000:])

def bootstrap()->None:
    if not shutil.which('java') or not shutil.which('javac'):raise RuntimeError('JDK 21 is required on PATH')
    WORK.mkdir(exist_ok=True);TOOLS.mkdir(parents=True,exist_ok=True)
    run(['javac','-cp',JAR,'-d',TOOLS,*sorted((ROOT/'tools/src').glob('*.java'))],'compile-build-tools.log')

def java(main:str,*args:str|Path,log:str='java.log',heap:str='1600m')->None:
    run(['java','-Xmx'+heap,'-cp',str(JAR)+os.pathsep+str(TOOLS),main,*args],log)

def aapt()->Path:
    system={'linux':'linux','darwin':'macosx','win32':'windows'}.get(sys.platform)
    if system is None:raise RuntimeError('Unsupported host platform')
    p=ROOT/'tools/prebuilt'/system/('aapt2.exe' if system=='windows' else 'aapt2')
    if system!='windows':p.chmod(0o755)
    return p

def index()->dict:
    return json.loads((ROOT/'source/class-index.json').read_text())

def resources()->Path:
    d=WORK/'resources';d.mkdir(exist_ok=True);s=ROOT/'source/android'
    # Apktool's generated public.xml enumerates ALL IDs, not original visibility.
    # Stable IDs are supplied separately; preserve original public/private visibility.
    stage=d/'res';remove_generated_directory(stage)
    shutil.copytree(s/'res',stage,copy_function=os.link if os.name!='nt' else shutil.copy2)
    pub=stage/'values/public.xml';tree=ET.parse(pub);el=tree.getroot()
    original_public=set(json.loads((s/'original-public-resources.json').read_text())['public_resources'])
    original_names={l.split(':',1)[1].split(' = ')[0] for l in (s/'stable-ids.txt').read_text().splitlines()}
    for child in list(el):
        name=child.get('type','')+'/'+child.get('name','')
        if child.tag=='public' and name in original_names and name not in original_public:el.remove(child)
    tmp=pub.with_suffix('.tmp');tree.write(tmp,encoding='utf-8',xml_declaration=True);tmp.replace(pub)
    run([aapt(),'compile','--dir',stage,'--no-crunch','-o',d/'compiled.zip'],'resource-compile.log')
    run([aapt(),'link','-o',d/'linked.apk','-I',ROOT/'tools/framework-res.apk',
         '--manifest',s/'AndroidManifest.xml','--stable-ids',s/'stable-ids.txt',
         '--min-sdk-version','23','--target-sdk-version','36','--version-code','896700008','--version-name','5.67.8',
         '--auto-add-overlay','--no-auto-version','--no-version-vectors','--no-version-transitions','--no-resource-deduping','--no-resource-removal',
         '-R',d/'compiled.zip'],'resource-link.log')
    run([aapt(),'dump','resources',d/'linked.apk'],'resource-linked-table.txt')
    from resource_pack import restore
    return restore(ROOT,d/'linked.apk',REPORTS/'resource-linked-table.txt')

def relocate_class(raw:bytes)->bytes:
    """Remove JADX's artificial default-package prefix in classfile symbolic names.
    Literal strings are excluded. Constant-pool indices and method code stay intact.
    """
    if raw[:4]!=b'\xca\xfe\xba\xbe':raise ValueError('Not a classfile')
    count=struct.unpack_from('>H',raw,8)[0];entries=[];strings=set();pos=10;i=1
    sizes={3:4,4:4,5:8,6:8,7:2,8:2,9:4,10:4,11:4,12:4,15:3,16:2,17:4,18:4,19:2,20:2}
    while i<count:
        tag=raw[pos];pos+=1
        if tag==1:
            n=struct.unpack_from('>H',raw,pos)[0];pos+=2;data=raw[pos:pos+n];pos+=n
        else:
            n=sizes[tag];data=raw[pos:pos+n];pos+=n
            if tag==8:strings.add(struct.unpack('>H',data)[0])
        entries.append((i,tag,data));i+=2 if tag in (5,6) else 1
    chunks=[raw[:10]]
    for i,tag,data in entries:
        if tag==1:
            if i not in strings:data=data.replace(b'Ldefpackage/',b'L')
            if i not in strings and data.startswith(b'defpackage/'):data=data[11:]
            chunks.extend((bytes([tag]),struct.pack('>H',len(data)),data))
        else:chunks.extend((bytes([tag]),data))
    return b''.join(chunks)+raw[pos:]

def compile_java()->Path:
    # Every compiler invocation writes to a never-reused generation. Publish only
    # after javac, D8 and disassembly complete; a failure retains the prior output.
    WORK.mkdir(parents=True,exist_ok=True)
    d=Path(tempfile.mkdtemp(prefix='java-stage-',dir=WORK))
    (d/'hostclasses').mkdir(parents=True)
    sources=sorted((ROOT/'source/java').rglob('*.java'))+sorted((ROOT/'test-support/java').rglob('*.java'))
    af=d/'sources.args';af.write_text(''.join('"'+str(p).replace('\\','/')+'"\n' for p in sources))
    run(['javac','--release','8','-g:none','-Xlint:-options','-d',d/'hostclasses','@'+str(af)],'javac-methods.log')
    emitted=[]
    for p in (d/'hostclasses/recovered').rglob('*.class'):
        dest=d/'relocated'/p.relative_to(d/'hostclasses');dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(relocate_class(p.read_bytes()));emitted.append(dest)
    # Only recovered/*.class is sent to D8. The android/com/defpackage host stubs are deliberately excluded.
    inputs=d/'inputs.jar'
    with zipfile.ZipFile(inputs,'w') as z:
        for p in sorted(emitted):z.write(p,str(p.relative_to(d/'relocated')))
    (d/'dex').mkdir()
    java('com.android.tools.r8.D8','--release','--no-desugaring','--min-api','23','--output',d/'dex',inputs,log='d8-methods.log')
    java('com.android.tools.smali.baksmali.Main','d','--api','23','--use-locals','-o',d/'smali',d/'dex/classes.dex',log='disassemble-java-methods.log')
    helper_hash=dex_integrity(d/'dex/classes.dex')
    if not (d/'smali').is_dir():raise RuntimeError('Compiled helper disassembly is missing')
    target=WORK/'java';remove_generated_directory(target)
    d.rename(target)
    (REPORTS/'java-staging.json').write_text(json.dumps({'compiled_generation':d.relative_to(ROOT).as_posix(),
        'published_directory':target.relative_to(ROOT).as_posix(),'published_after_all_compiler_commands':True,
        'helper_dex_sha256':helper_hash,
        'scope':'Fresh generated Java/D8 staging; not Android execution'},indent=2)+'\n')
    return target

METHOD=re.compile(r'^\.method [^\n]*\n.*?^\.end method',re.M|re.S)
ANNOT=re.compile(r'(?m)^\s*\.annotation .*?^\s*\.end annotation\n?',re.S)
def methods(text:str)->dict[str,str]:
    return {m[0].splitlines()[0].split()[-1]:m[0] for m in METHOD.finditer(text)}

def hybrid_source(javadir:Path)->Path:
    target=WORK/'hybrid-smali';remove_generated_directory(target)
    shutil.copytree(ROOT/'source/smali',target,copy_function=os.link if os.name!='nt' else shutil.copy2)
    registry=json.loads((ROOT/'source/java-method-map.json').read_text());idx=index();bytype={v['descriptor']:v for v in idx.values()};changes=[];constructor_proofs=[]
    for e in registry:
        original=bytype[e['target']];path=target/Path(original['path']).relative_to('source/smali')
        helperpath=javadir/'smali'/(e['helper'][1:-1]+'.smali')
        hm=methods(helperpath.read_text());oldtext=path.read_text();old=methods(oldtext)[e['method']]
        suffix=e['method'][e['method'].index('('):]
        expected=e.get('helper_descriptor',e['helper_method']+'('+ (e['target'] if e['instance'] else '')+suffix[1:])
        if expected not in hm:raise RuntimeError('Compiled method descriptor mismatch: '+expected)
        compiled,proofs=restore_from_preserved_source(e,hm[expected],old,idx,ROOT)
        constructor_proofs.extend({'target':e['target'],'method':e['method'],**proof} for proof in proofs)
        body=compiled.split('\n',1)[1].rsplit('.end method',1)[0]
        body=ANNOT.sub('',body)
        if 'Lrecovered/' in body or 'Ldefpackage/' in body:raise RuntimeError('Unexpected helper/stub reference in runtime body')
        anns=ANNOT.findall(old)
        replacement=old.splitlines()[0]+'\n'+''.join(anns)+body+'.end method'
        newtext=oldtext.replace(old,replacement,1)
        # Atomic replacement avoids changing the immutable baseline through a hard link.
        temp=path.with_suffix('.tmp');temp.write_text(newtext);temp.replace(path)
        changes.append({'class':e['target'],'method':e['method'],'source':e['java_source'],'source_partition':original['partition']})
    (REPORTS/'java-integration.json').write_text(json.dumps({'methods':len(changes),'classes':len(set(x['class'] for x in changes)),'changes':changes,'runtime_stub_classes_included':0,'constructor_owner_corrections':constructor_proofs},indent=2))
    return target

def write_aligned(z:zipfile.ZipFile,name:str,data:bytes,compression:int=zipfile.ZIP_STORED)->None:
    zi=zipfile.ZipInfo(name,(1980,1,1,0,0,0));zi.compress_type=compression;zi.external_attr=0o100644<<16
    alignment=(16384 if name.endswith('.so') else 4) if compression==zipfile.ZIP_STORED else 1
    offset=z.fp.tell()+30+len(name.encode('utf-8'))
    padding=(-offset)%alignment
    if padding:
        if padding<4:padding+=alignment
        zi.extra=struct.pack('<HH',0xd935,padding-4)+b'\0'*(padding-4)
    z.writestr(zi,data)

def dex_integrity(path:Path)->str:
    raw=path.read_bytes()
    if len(raw)<112 or raw[:8]!=b'dex\n035\0':raise ValueError('Invalid DEX header: '+str(path))
    if struct.unpack_from('<I',raw,32)[0]!=len(raw):raise ValueError('DEX length mismatch')
    if raw[12:32]!=hashlib.sha1(raw[32:]).digest():raise ValueError('DEX SHA1 mismatch')
    if struct.unpack_from('<I',raw,8)[0]!=(zlib.adler32(raw[12:])&0xffffffff):raise ValueError('DEX Adler32 mismatch')
    return hashlib.sha256(raw).hexdigest()

def partition_fingerprint(source:Path,compiler_sha256:str)->str:
    digest=hashlib.sha256(('smali-api23-j2-v1:'+compiler_sha256).encode())
    for path in sorted(source.rglob('*.smali')):
        name=path.relative_to(source).as_posix().encode()
        raw=path.read_bytes()
        digest.update(len(name).to_bytes(4,'big'));digest.update(name)
        digest.update(hashlib.sha256(raw).digest())
    return digest.hexdigest()

def assemble(variant:str,source:Path,resource_apk:Path)->Path:
    d=WORK/variant;d.mkdir(exist_ok=True)
    cache=WORK/'assembly-cache';cache.mkdir(exist_ok=True)
    compiler_sha256=hashlib.sha256(JAR.read_bytes()).hexdigest()
    entries=[]
    for part in json.loads((ROOT/'source/partitions.json').read_text()):
        started=time.monotonic();src=source/part['name']
        fingerprint=partition_fingerprint(src,compiler_sha256)
        cached=cache/(fingerprint+'.dex');metadata=cache/(fingerprint+'.json')
        valid=False
        if cached.is_file() and metadata.is_file():
            try:
                manifest=json.loads(metadata.read_text())
                valid=(manifest['source_fingerprint']==fingerprint and manifest['compiler_sha256']==compiler_sha256
                       and manifest['dex_sha256']==dex_integrity(cached))
            except (OSError,ValueError,KeyError,struct.error):valid=False
        if not valid:
            temporary=cache/(fingerprint+'.partial.dex')
            java('com.android.tools.smali.smali.Main','a','--api','23','-j','2','-o',temporary,src,log=variant+'-assemble-'+part['name']+'.log')
            dex_sha256=dex_integrity(temporary)
            temporary.replace(cached)
            manifest={'source_fingerprint':fingerprint,'compiler_sha256':compiler_sha256,'dex_sha256':dex_sha256}
            temp_metadata=metadata.with_suffix('.tmp');temp_metadata.write_text(json.dumps(manifest,indent=2));temp_metadata.replace(metadata)
        out=d/(part['name']+'.dex');shutil.copyfile(cached,out)
        entries.append({'partition':part['name'],'source_fingerprint':fingerprint,'dex_sha256':dex_integrity(out),
                        'origin':'verified_source_cache' if valid else 'assembled_from_smali','seconds':round(time.monotonic()-started,3)})
        (REPORTS/(variant+'-assembly-inputs.json')).write_text(json.dumps({'complete':False,'partitions':entries},indent=2))
        print(variant,part['name'],entries[-1]['origin'],flush=True)
    (REPORTS/(variant+'-assembly-inputs.json')).write_text(json.dumps({'complete':True,'partitions':entries},indent=2))
    return package_apk(variant,resource_apk)

def package_apk(variant:str,resource_apk:Path)->Path:
    d=WORK/variant
    dexfiles={p['apk_path']:d/(p['name']+'.dex') for p in json.loads((ROOT/'source/partitions.json').read_text())}
    compression=json.loads((ROOT/'source/zip-compression.json').read_text())
    unsigned=d/'unsigned.apk'
    with zipfile.ZipFile(ROOT/'source/payload.zip') as payload,zipfile.ZipFile(resource_apk) as res,zipfile.ZipFile(unsigned,'w',compresslevel=6) as dest:
        duplicate=set(payload.namelist())&set(res.namelist())
        if duplicate:raise RuntimeError('Conflicting payload/resource entries '+str(duplicate))
        names=sorted(set(payload.namelist())|set(res.namelist())|set(dexfiles))
        for n in names:
            data=dexfiles[n].read_bytes() if n in dexfiles else (res.read(n) if n in res.namelist() else payload.read(n))
            write_aligned(dest,n,data,compression.get(n,zipfile.ZIP_DEFLATED))
    key=ROOT/'signing/development.p12';key.parent.mkdir(exist_ok=True)
    if not key.exists():
        run(['keytool','-genkeypair','-keystore',key,'-storetype','PKCS12','-storepass','android','-keypass','android','-alias','reconstruction','-keyalg','RSA','-keysize','2048','-validity','3650','-dname','CN=MacroDroid Reconstruction Test Key, O=Local Development, C=CA'],'key-generation.log')
    dest=ROOT/'dist'/('MacroDroid-5.67.8-v9-'+variant+'.apk');dest.parent.mkdir(exist_ok=True)
    java('BuildSupport','sign',unsigned,dest,key,log=variant+'-sign.log')
    java('BuildSupport','verify',dest,log=variant+'-signature-verification.log')
    (REPORTS/(variant+'-build.json')).write_text(json.dumps({'variant':variant,'apk':str(dest.relative_to(ROOT)),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'original_apk_build_input':False,'original_dex_build_input':False,'source_dex_partitions':len(dexfiles)},indent=2))
    print(dest,flush=True);return dest

def verify(variant:str)->None:
    apk=ROOT/'dist'/('MacroDroid-5.67.8-v9-'+variant+'.apk')
    java('BuildSupport','verify',apk,log=variant+'-signature-verification.log')
    idx=index();expected=idx;seen={};changed=[];missing=[];extra=[];methodchanges=[];source_changes=[]
    out=WORK/('verify-'+variant);remove_generated_directory(out);out.mkdir()
    with zipfile.ZipFile(apk) as z:
        bad=z.testzip()
        if bad:raise RuntimeError('APK ZIP checksum failure '+bad)
        for p in json.loads((ROOT/'source/partitions.json').read_text()):
            dex=out/(p['name']+'.dex');dex.write_bytes(z.read(p['apk_path']))
            java('com.android.tools.smali.baksmali.Main','d','--api','23','--use-locals','-j','2','-o',out/p['name'],dex,log=variant+'-verify-'+p['name']+'.log')
            for f in (out/p['name']).rglob('*.smali'):
                text=f.read_text();type=next(l.rsplit(' ',1)[-1] for l in text.splitlines() if l.startswith('.class '));key=p['name']+':'+type;seen[key]=True
                if key not in expected:extra.append(key);continue
                raw=(ROOT/expected[key]['path']).read_bytes();orig=raw.decode('utf-8')
                if hashlib.sha256(raw).hexdigest()!=expected[key]['sha256']:source_changes.append(key)
                if orig!=text:
                    changed.append(type);om=methods(orig);nm=methods(text)
                    if set(om)!=set(nm):raise RuntimeError('Class method interface changed '+type)
                    for signature in om:
                        if om[signature]!=nm[signature]:methodchanges.append((type,signature))
                    # Fields, class hierarchy, interfaces and class annotations must be preserved.
                    if METHOD.sub('<METHOD>',orig)!=METHOD.sub('<METHOD>',text):raise RuntimeError('Non-method class metadata changed '+type)
        for t in expected:
            if t not in seen:missing.append(t)
        with zipfile.ZipFile(ROOT/'source/payload.zip') as payload:
            alteredpayload=[n for n in payload.namelist() if n not in z.namelist() or payload.read(n)!=z.read(n)]
        alignment=[]
        with apk.open('rb') as f:
            for info in z.infolist():
                if info.compress_type==0:
                    f.seek(info.header_offset+26);nl,el=struct.unpack('<HH',f.read(4));off=info.header_offset+30+nl+el
                    if off%(16384 if info.filename.endswith('.so') else 4):alignment.append(info.filename)
    registry=json.loads((ROOT/'source/java-method-map.json').read_text());allowed={(e['target'],e['method']) for e in registry} if variant=='hybrid' else set()
    unexpected=set(methodchanges)-allowed
    # Every currently registered migration changes its canonical body (debug stripped).
    # Reject a build that silently omits a registered replacement.
    omitted=allowed-set(methodchanges)
    report={'variant':variant,'apk_sha256':hashlib.sha256(apk.read_bytes()).hexdigest(),'baseline_source_hash_mismatches':source_changes,'classes_compared':len(seen),'methods_total':sum(v['methods'] for v in idx.values()),'changed_classes':changed,'changed_methods':methodchanges,'missing':missing,'extra':extra,'unexpected_changed_methods':sorted(unexpected),'omitted_registered_changes':sorted(omitted),'altered_opaque_payload':alteredpayload,'misaligned':alignment,'pass':not(missing or extra or unexpected or omitted or alteredpayload or alignment or source_changes)}
    (REPORTS/(variant+'-roundtrip.json')).write_text(json.dumps(report,indent=2))
    if not report['pass']:raise RuntimeError('Roundtrip failed; see report')
    print(json.dumps({k:v for k,v in report.items() if k not in ('changed_methods','changed_classes')},indent=2))

def main()->None:
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='command',required=True)
    for n in ('build','verify','package'):
        sp=sub.add_parser(n);sp.add_argument('--variant',choices=['baseline','hybrid'],default='baseline')
    sub.add_parser('compile-java');fp=sub.add_parser('find-class');fp.add_argument('query')
    a=ap.parse_args()
    if a.command=='find-class':
        for v in index().values():
            if a.query.lower() in v['descriptor'].lower():print(v['descriptor'],v['path'])
        return
    bootstrap()
    if a.command=='compile-java':compile_java()
    elif a.command=='verify':verify(a.variant)
    elif a.command=='package':package_apk(a.variant,WORK/'resources/restored.apk')
    else:
        src=ROOT/'source/smali'
        if a.variant=='hybrid':src=hybrid_source(compile_java())
        assemble(a.variant,src,resources())
if __name__=='__main__':
    try:main()
    except Exception as e:print('BUILD ERROR:',e,file=sys.stderr);sys.exit(1)
