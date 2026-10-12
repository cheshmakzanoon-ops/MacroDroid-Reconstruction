#!/usr/bin/env python3
"""Record or verify an exact release build/test-input snapshot.
A mismatch after intentional source editing is expected. This command checks delivery
integrity, not whether a user modification is correct. It never modifies source files.
"""
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def inputs():
    for directory in ['source','test-support','tests','signing','tools','reference']:
        for p in sorted((ROOT/directory).rglob('*')):
            if not p.is_file() or '__pycache__' in p.parts or (directory=='tools' and 'classes' in p.relative_to(ROOT).parts):continue
            if p.suffix in ['.pyc','.pyo']:continue
            yield p
    yield from sorted(ROOT.glob('*.py'))

def snapshot()->dict:
    entries={}
    for p in inputs():
        with p.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
        entries[p.relative_to(ROOT).as_posix()]={'size':p.stat().st_size,'sha256':digest}
    canonical=json.dumps(entries,sort_keys=True,separators=(',',':')).encode()
    return {'format':1,'files':len(entries),'snapshot_sha256':hashlib.sha256(canonical).hexdigest(),'entries':entries}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('command',choices=['record','verify']);ap.add_argument('--manifest',type=Path,default=ROOT/'reports/release-input-snapshot.json');a=ap.parse_args()
    current=snapshot()
    if a.command=='record':a.manifest.parent.mkdir(parents=True,exist_ok=True);a.manifest.write_text(json.dumps(current,indent=2));print(json.dumps({k:v for k,v in current.items() if k!='entries'},indent=2));return
    expected=json.loads(a.manifest.read_text());old=expected['entries'];new=current['entries']
    missing=sorted(old.keys()-new.keys());extra=sorted(new.keys()-old.keys());changed=sorted(k for k in old.keys()&new.keys() if old[k]!=new[k])
    report={'pass':not(missing or extra or changed),'files_checked':len(new),'snapshot_sha256':current['snapshot_sha256'],'missing':missing,'extra':extra,'changed':changed}
    print(json.dumps(report,indent=2));sys.exit(0 if report['pass'] else 2)
if __name__=='__main__':main()
