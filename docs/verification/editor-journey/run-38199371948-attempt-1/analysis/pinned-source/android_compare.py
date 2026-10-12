#!/usr/bin/env python3
"""Compare two freshly recorded cold-launch captures, never whole-app parity.
Requires the same device/settings, two different APK hashes, live foreground app
processes, app-owned UI nodes, intact artifacts, and exact complete pixels/UI XML.
There are no ignored status bars, dynamic text masks, or inferred feature passes.
"""
from __future__ import annotations
import argparse,hashlib,json,math,re,struct,sys,zlib
import xml.etree.ElementTree as ET
from pathlib import Path
PACKAGE='com.arlosoft.macrodroid'
ORIGINAL_SHA256='84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'
PNG_MAGIC=b'\x89PNG\r\n\x1a\n'
MAX_PIXELS=16_000_000

class CaptureError(ValueError):pass

def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def png_pixels(data:bytes)->tuple[int,int,bytes]:
    """Strict bounded decoder for noninterlaced 8-bit RGB/RGBA screenshots."""
    if len(data)>128_000_000 or not data.startswith(PNG_MAGIC):raise CaptureError('Invalid PNG signature or file size')
    offset=8;header=None;compressed=bytearray();finished=False;seen_data=False;closed_data=False
    while offset<len(data):
        if offset+12>len(data):raise CaptureError('Truncated PNG chunk')
        size=struct.unpack_from('>I',data,offset)[0];kind=data[offset+4:offset+8];offset+=8
        if size>64_000_000 or offset+size+4>len(data):raise CaptureError('Invalid PNG chunk length')
        payload=data[offset:offset+size];crc=struct.unpack_from('>I',data,offset+size)[0];offset+=size+4
        if zlib.crc32(kind+payload)&0xffffffff!=crc:raise CaptureError('PNG CRC mismatch')
        if header is None and kind!=b'IHDR':raise CaptureError('PNG IHDR must be first')
        if kind==b'IHDR':
            if header is not None or size!=13:raise CaptureError('Duplicate or invalid PNG IHDR')
            w,h,depth,color,compression,filtering,interlace=struct.unpack('>IIBBBBB',payload)
            if not w or not h or w*h>MAX_PIXELS:raise CaptureError('PNG dimensions exceed safe bounds')
            if depth!=8 or color not in (2,6) or compression or filtering or interlace:raise CaptureError('Unsupported PNG screenshot format')
            header=(w,h,3 if color==2 else 4)
        elif kind==b'IDAT':
            if closed_data:raise CaptureError('Noncontiguous PNG data')
            seen_data=True;compressed.extend(payload)
        elif kind==b'IEND':
            if size or not seen_data or offset!=len(data):raise CaptureError('Invalid PNG ending')
            finished=True;break
        else:
            if seen_data:closed_data=True
            if kind in (b'acTL',b'fcTL',b'fdAT',b'tRNS'):raise CaptureError('Unsupported animated/transparency PNG metadata')
            # Unknown critical chunks must not silently change interpretation.
            if kind[0]&32==0 and kind!=b'PLTE':raise CaptureError('Unknown critical PNG chunk')
    if not finished or header is None:raise CaptureError('Incomplete PNG')
    w,h,bpp=header;stride=w*bpp;needed=h*(stride+1)
    stream=zlib.decompressobj()
    raw=stream.decompress(bytes(compressed),needed+1)
    if len(raw)!=needed or not stream.eof or stream.unconsumed_tail or stream.unused_data:raise CaptureError('PNG data length mismatch')
    rows=bytearray();previous=bytearray(stride);cursor=0
    for _ in range(h):
        filtering=raw[cursor];cursor+=1;row=bytearray(raw[cursor:cursor+stride]);cursor+=stride
        if filtering>4:raise CaptureError('Unsupported PNG row filter')
        for x in range(stride):
            left=row[x-bpp] if x>=bpp else 0;up=previous[x];upper_left=previous[x-bpp] if x>=bpp else 0
            if filtering==1:predictor=left
            elif filtering==2:predictor=up
            elif filtering==3:predictor=(left+up)//2
            elif filtering==4:
                p=left+up-upper_left;a=abs(p-left);b=abs(p-up);c=abs(p-upper_left)
                predictor=left if a<=b and a<=c else up if b<=c else upper_left
            else:predictor=0
            row[x]=(row[x]+predictor)&255
        if bpp==4:rows.extend(row)
        else:
            for x in range(0,stride,3):rows.extend(row[x:x+3]);rows.append(255)
        previous=row
    return w,h,bytes(rows)

def color_metadata(data:bytes)->tuple:
    """Call only after png_pixels validation; preserve color-space interpretation."""
    offset=8;values=[];seen=set()
    while offset<len(data):
        size=struct.unpack_from('>I',data,offset)[0];kind=data[offset+4:offset+8]
        if kind in (b'iCCP',b'gAMA',b'cHRM',b'sRGB',b'cICP',b'mDCV',b'cLLI'):
            if kind in seen:raise CaptureError('Duplicate PNG color metadata')
            seen.add(kind);values.append((kind,data[offset+8:offset+8+size]))
        offset+=size+12
    return tuple(sorted(values))

def xml_state(data:bytes)->tuple[tuple,int]:
    if len(data)>8_000_000:raise CaptureError('UI XML exceeds safe bound')
    text=data.decode('utf-8')
    if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():raise CaptureError('UI XML declarations not allowed')
    try:root=ET.fromstring(data)
    except ET.ParseError as exc:raise CaptureError('Invalid UI hierarchy XML') from exc
    if root.tag!='hierarchy':raise CaptureError('Unexpected UI XML root')
    nodes=list(root.iter())
    if len(nodes)>50_000:raise CaptureError('UI node limit exceeded')
    owned=sum(n.tag=='node' and n.get('package')==PACKAGE for n in nodes)
    if not owned:raise CaptureError('No target-app nodes in hierarchy')
    # Attribute ordering and formatting whitespace are irrelevant to an XML tree.
    # Values, child ordering, bounds, text, selection and every other attribute remain.
    def canonical(node,depth=0):
        if depth>100:raise CaptureError('UI XML depth exceeded')
        text=node.text if node.text and node.text.strip() else ''
        tail=node.tail if node.tail and node.tail.strip() else ''
        return node.tag,tuple(sorted(node.attrib.items())),text,tail,tuple(canonical(c,depth+1) for c in node)
    return canonical(root),owned

def live_pids(*samples:str)->tuple[str,...]:
    parsed=[]
    for sample in samples:
        values=sample.strip().split()
        if not values or any(not re.fullmatch(r'[1-9][0-9]*',x) for x in values):raise CaptureError('App process was not observed alive')
        parsed.append(tuple(sorted(set(values))))
    if len(parsed)<2 or any(x!=parsed[0] for x in parsed[1:]):raise CaptureError('App PID changed or lacks two live samples')
    return parsed[0]

def resumed_components(text:str)->tuple[str,...]:
    """An explicit top-resumed owner takes precedence over lower task records."""
    for field in ['topResumedActivity','mResumedActivity','ResumedActivity','mFocusedActivity']:
        lines=[line for line in text.splitlines() if re.match(r'^\s*'+field+r'\s*[:=]',line)]
        if not lines:continue
        components=[]
        for line in lines:
            matches=re.findall(r'(?<![A-Za-z0-9_.$])[A-Za-z0-9_.$]+/[A-Za-z0-9_.$]+',line)
            if len(matches)!=1:return ()
            components.append(matches[0])
        return tuple(components)
    return ()

def foreground_ok(text:str)->bool:
    components=resumed_components(text)
    return bool(components) and all(component.split('/',1)[0]==PACKAGE for component in components)

def valid_live_interval(value)->bool:
    return type(value) in (int,float) and math.isfinite(value) and value>=1

def install_ok(code:int,stdout:str,stderr:str='')->bool:
    """Require ADB's terminal success and reject explicit failure diagnostics."""
    lines=[line.strip() for line in stdout.splitlines() if line.strip()]
    if type(code) is not int or code!=0 or not lines or lines[-1]!='Success':return False
    return not any(re.search(r'\b(?:Failure|Error|Exception|failed)\b',line,re.I)
                   for line in stdout.splitlines()+stderr.splitlines())

def absence_ok(code:int,stdout:str,stderr:str)->bool:
    """Android's missing-package response is empty; transport errors are distinct."""
    return type(code) is int and code in (0,1) and not stdout.strip() and not stderr.strip()

def launch_ok(code:int,text:str)->bool:
    return type(code) is int and code==0 and any(line.strip()=='Status: ok' for line in text.splitlines()) and not any(line.lstrip().startswith(('Error:','Exception','Error type')) for line in text.splitlines())

def artifact(folder:Path,record:dict)->bytes:
    name=record.get('path','');p=Path(name)
    if p.is_absolute() or '..' in p.parts:raise CaptureError('Unsafe capture artifact path')
    path=folder/p
    if not path.resolve().is_relative_to(folder.resolve()) or not path.is_file():raise CaptureError('Capture artifact missing: '+name)
    data=path.read_bytes()
    if len(data)!=record.get('bytes') or sha(data)!=record.get('sha256'):raise CaptureError('Capture artifact was changed: '+name)
    return data

def command_output(folder:Path,record:dict)->tuple[int,str,str]:
    return record['returncode'],artifact(folder,record['stdout']).decode('utf-8'),artifact(folder,record['stderr']).decode('utf-8')

def installed_path(code:int,stdout:str,stderr:str)->str:
    lines=[line.strip() for line in stdout.splitlines() if line.strip()]
    if type(code) is not int or code!=0 or stderr.strip() or len(lines)!=1 or not lines[0].startswith('package:/data/app/'):
        raise CaptureError('Installed monolithic APK path was not observed')
    path=lines[0][len('package:'):]
    if not path.endswith('/base.apk') or '\x00' in path:raise CaptureError('Installed APK path is unexpected')
    return path

def installed_digest(code:int,stdout:str,stderr:str,path:str)->str:
    found=re.fullmatch(r'([0-9a-f]{64})\s+'+re.escape(path)+r'\s*',stdout)
    if type(code) is not int or code!=0 or stderr.strip() or not found:
        raise CaptureError('Installed APK checksum was not observed')
    return found[1]

def compare_capture(folder:Path)->dict:
    result={'scope':'Exact cold-launch capture comparison only','cold_launch_capture_equal':False,
            'full_runtime_1_to_1_established':False,'feature_parity_established':False,'android_runtime_executed':False,
            'installed_apk_identities_verified':False,'status':'REJECTED'}
    try:
        report=json.loads((folder/'result.json').read_text())
        schema=report.get('schema_version')
        if type(schema) is not int or schema not in (2,3):raise CaptureError('A schema-2 or schema-3 recorder run is required')
        cold_complete=report.get('status')=='CAPTURES_RECORDED_NOT_PARITY'
        if schema==3 and report.get('intro_pages_requested') is True and report.get('status')=='COLD_CAPTURES_RECORDED_INTRO_INCOMPLETE':cold_complete=True
        if not cold_complete:raise CaptureError('Recorder did not complete both cold captures')
        runs=report.get('runs',[])
        if len(runs)!=2 or [r.get('label') for r in runs]!=['original','candidate']:raise CaptureError('Missing unique original/candidate capture')
        if len({r.get('apk_sha256') for r in runs})!=2 or any(not re.fullmatch('[0-9a-f]{64}',r.get('apk_sha256','')) for r in runs):raise CaptureError('APKs are identical or identities invalid')
        if schema==3:
            pair=report.get('apk_preflight',[])
            if len(pair)!=2 or [entry.get('label') for entry in pair]!=['original','candidate']:raise CaptureError('Both APK preflight records are required')
            if runs[0]['apk_sha256']!=ORIGINAL_SHA256:raise CaptureError('Original APK identity differs from the supplied target')
            expected_metadata={'package':PACKAGE,'version_code':'896700008','version_name':'5.67.8','min_sdk':23,'target_sdk':36}
            for entry,run in zip(pair,runs):
                if entry.get('apk_sha256')!=run['apk_sha256'] or entry.get('metadata')!=expected_metadata or type(entry.get('bytes')) is not int or entry['bytes']<=0:
                    raise CaptureError('APK preflight identities or package metadata differ')
        if runs[0].get('environment')!=runs[1].get('environment') or not runs[0].get('environment'):raise CaptureError('Device/settings differ between captures')
        environment=runs[0]['environment']
        required={'serial','ro.product.cpu.abilist','ro.build.version.sdk','ro.build.fingerprint','ro.kernel.qemu','persist.sys.locale','persist.sys.timezone','display_size','display_density','font_scale'}
        if not required.issubset(environment) or any(not environment.get(k) for k in required-{'ro.kernel.qemu','persist.sys.timezone','persist.sys.locale'}):raise CaptureError('Incomplete device environment')
        if 'arm64-v8a' not in environment['ro.product.cpu.abilist'].split(','):raise CaptureError('ARM64 capture required')
        if len({r.get('component') for r in runs})!=1 or not re.fullmatch(re.escape(PACKAGE)+r'/[A-Za-z0-9_.$]+',runs[0].get('component','')):raise CaptureError('Different or invalid launch components')
        states=[]
        for run in runs:
            if run.get('status')!='APP_CAPTURE_RECORDED' or run.get('android_runtime_executed') is not True:raise CaptureError('An app capture was not completed')
            if not valid_live_interval(run.get('sample_interval_seconds')):raise CaptureError('Live PID samples lack a finite positive interval')
            if not absence_ok(*command_output(folder,run['after_uninstall'])):raise CaptureError('Package absence was not verified before installation')
            if not install_ok(*command_output(folder,run['install'])):raise CaptureError('APK installation did not succeed')
            if schema==3:
                installed=run['installed_apk']
                path=installed_path(*command_output(folder,installed['package_path']))
                observed=installed_digest(*command_output(folder,installed['checksum']),path)
                if observed!=run['apk_sha256'] or installed.get('sha256')!=observed:
                    raise CaptureError('Installed APK bytes differ from the prevalidated input')
            a=run['artifacts'];launch=artifact(folder,a['launch']).decode('utf-8');p0=artifact(folder,a['pid_first']).decode('utf-8');p1=artifact(folder,a['pid_second']).decode('utf-8')
            if not launch_ok(run.get('launch_exit'),launch):raise CaptureError('App start failed')
            live_pids(p0,p1,artifact(folder,a['pid_final']).decode('utf-8'))
            if not foreground_ok(artifact(folder,a['foreground']).decode('utf-8')):raise CaptureError('Target application is not foreground')
            state,owned=xml_state(artifact(folder,a['hierarchy']));picture=artifact(folder,a['screenshot']);w,h,pixels=png_pixels(picture)
            states.append((state,w,h,pixels,color_metadata(picture)));run['owned_nodes_verified']=owned
        result['android_runtime_executed']=True
        result['installed_apk_identities_verified']=schema==3
        a,b=states;same_size=a[1:3]==b[1:3]
        changed=sum(a[3][i:i+4]!=b[3][i:i+4] for i in range(0,len(a[3]),4)) if same_size else None
        result.update(hierarchy_equal=a[0]==b[0],screen_size_equal=same_size,changed_pixels=changed,color_metadata_equal=a[4]==b[4],
                      masks_used=False,ignored_app_attributes=[],apk_sha256=[r['apk_sha256'] for r in runs])
        result['cold_launch_capture_equal']=result['hierarchy_equal'] and same_size and changed==0 and result['color_metadata_equal']
        result['status']='EXACT_COLD_LAUNCH_MATCH_ONLY' if result['cold_launch_capture_equal'] else 'CAPTURE_DIFFERENCE'
    except (OSError,KeyError,TypeError,ValueError,AttributeError,IndexError,OverflowError,zlib.error) as exc:result['reason']=str(exc)
    return result

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('capture_directory',type=Path);args=ap.parse_args()
    report=compare_capture(args.capture_directory)
    (args.capture_directory/'cold-launch-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2));return 0 if report['cold_launch_capture_equal'] else 2
if __name__=='__main__':sys.exit(main())
