#!/usr/bin/env python3
"""Write complete, closed, independently checked source/toolchain ZIPs atomically.
No build caches or output APKs are included. Each member's decompressed bytes are
compared with the local input before the .partial archive becomes a final .zip.
"""
from __future__ import annotations
import argparse,hashlib,json,os,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def entries():
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(ROOT)
        if rel.parts[0] in ['build','dist','.git'] or '__pycache__' in rel.parts or p.suffix in ['.pyc','.pyo']:continue
        if rel.parts[:2]==('tools','classes'):continue
        if p.is_symlink():raise RuntimeError('Symlink not allowed in release: '+str(rel))
        group='Toolchain' if rel.parts[0]=='tools' and rel.parts[1]!='src' else 'Source'
        yield group,p,rel

def write_archive(path:Path,items):
    partial=path.with_suffix(path.suffix+'.partial');expected={};total=0
    with zipfile.ZipFile(partial,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        for p,rel in items:
            name='MacroDroid_v9/'+rel.as_posix();info=zipfile.ZipInfo(name,(1980,1,1,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(0o100755 if os.access(p,os.X_OK) else 0o100644)<<16
            digest=hashlib.sha256();size=0
            with p.open('rb') as src,z.open(info,'w',force_zip64=True) as dest:
                while data:=src.read(1024*1024):digest.update(data);dest.write(data);size+=len(data)
            expected[name]={'size':size,'sha256':digest.hexdigest()};total+=size
    # Re-open only after the central directory has been written and closed.
    with zipfile.ZipFile(partial) as z:
        if len(z.namelist())!=len(set(z.namelist())) or set(z.namelist())!=set(expected):raise RuntimeError('Archive entry set mismatch')
        for name,record in expected.items():
            with z.open(name) as src:actual=hashlib.file_digest(src,'sha256').hexdigest()
            if actual!=record['sha256'] or z.getinfo(name).file_size!=record['size']:raise RuntimeError('Archive member integrity mismatch: '+name)
            # ZipExtFile also checks CRC upon complete reading.
    partial.replace(path)
    with path.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
    return {'archive':path.name,'bytes':path.stat().st_size,'sha256':digest,'entries':len(expected),'uncompressed_bytes':total,'closed_central_directory':True,'all_members_crc_and_sha256_checked':True}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args()
    destination=a.output_dir.resolve()
    if destination==ROOT or destination.is_relative_to(ROOT):raise RuntimeError('Place release archives outside the project to avoid recursion.')
    destination.mkdir(parents=True,exist_ok=True);groups={'Source':[],'Toolchain':[]}
    for g,p,r in entries():groups[g].append((p,r))
    reports=[]
    for group,items in groups.items():
        print('Writing',group,len(items),'files',flush=True)
        report=write_archive(destination/('MacroDroid_v9_'+group+'.zip'),items);reports.append(report);print(json.dumps(report),flush=True)
    (destination/'archive-validation.json').write_text(json.dumps({'pass':True,'archives':reports},indent=2))
if __name__=='__main__':main()
