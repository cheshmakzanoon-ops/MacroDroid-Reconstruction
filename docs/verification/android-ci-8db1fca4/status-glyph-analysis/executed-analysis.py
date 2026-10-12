#!/usr/bin/env python3
"""Read original captured pixels and test exact glyph translation; never edit images."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import gzip
import hashlib
import json
import stat
from PIL import Image, __version__ as pillow_version

ROOT=Path('/dev/shm/macrodroid-active-numeric-status-glyph-review')
OUT=ROOT/'analysis-01'
RAW=Path('/dev/shm/macrodroid-transfer-space-20261012/active-numeric-android-run-38247941263')
CAPTURE=RAW/'extracted/capture'
PAIRS=[('MACRODROID','original.png','candidate.png'),('TRIGGERS','original-intro-2.png','candidate-intro-2.png'),
       ('ACTIONS','original-intro-3.png','candidate-intro-3.png'),('CONSTRAINTS','original-intro-4.png','candidate-intro-4.png'),
       ('notification-permission','original-post-intro.png','candidate-post-intro.png')]
ROI=(580,0,644,48)

def digest(raw):return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def identity(path):return dict(path=str(path),**digest(path.read_bytes()),mode=stat.S_IMODE(path.stat().st_mode))
def save(name,obj):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:f.write(json.dumps(obj,indent=2)+'\n')
def bounds(points):
    if not points:return None
    return [min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points),max(p[1] for p in points)]

def main():
    OUT.mkdir(parents=True,exist_ok=False)
    with (OUT/'executed-analysis.py').open('xb') as f:f.write(Path(__file__).read_bytes())
    started=datetime.now(timezone.utc).isoformat()
    archive=digest((RAW/'artifact.zip').read_bytes())
    assert archive==dict(bytes=1017412,sha256='1fb4a6375b9eb6b416c963f1d3e6d49733c9e5884d0081887bff96bec30fea04')
    paths=[CAPTURE/name for _,a,b in PAIRS for name in (a,b)]
    before=[identity(p) for p in paths];save('inputs-before.json',before)
    rows=[];literal=[]
    for label,aname,bname in PAIRS:
        loaded=[]
        for name in (aname,bname):
            with Image.open(CAPTURE/name) as image:
                assert image.size==(720,1280)
                loaded.append(image.convert('RGBA').tobytes())
        a,b=loaded; width,height=720,1280
        all_changed=[i for i,(x,y) in enumerate(zip(memoryview(a).cast('I'),memoryview(b).cast('I'))) if x!=y]
        pixels=[];backgrounds=[];foreground=[]
        for raw in (a,b):
            pixel={(x,y):raw[(y*width+x)*4:(y*width+x)*4+4].hex() for y in range(ROI[1],ROI[3]) for x in range(ROI[0],ROI[2])}
            background=Counter(pixel.values()).most_common(1)[0][0]
            fg={(x,y,c) for (x,y),c in pixel.items() if c!=background}
            pixels.append(pixel);backgrounds.append(background);foreground.append(fg)
        matches=[]
        if backgrounds[0]==backgrounds[1] and foreground[0] and len(foreground[0])==len(foreground[1]):
            for dx in range(-16,17):
                for dy in range(-8,9):
                    if {(x+dx,y+dy,c) for x,y,c in foreground[0]}==foreground[1]:matches.append(dict(dx=dx,dy=dy))
        regional=[i for i in all_changed if ROI[0]<=i%width<ROI[2] and ROI[1]<=i//width<ROI[3]]
        remainder=[i for i in all_changed if i not in set(regional)]
        rows.append(dict(screen=label,full_changed_pixels=len(all_changed),status_region_changed_pixels=len(regional),
            remaining_full_frame_changed_pixels=len(remainder),
            full_change_bounds_inclusive=bounds([(i%width,i//width) for i in all_changed]),
            status_change_bounds_inclusive=bounds([(i%width,i//width) for i in regional]),
            remaining_change_bounds_inclusive=bounds([(i%width,i//width) for i in remainder]),
            status_background_rgba_hex=backgrounds,original_foreground_pixels=len(foreground[0]),candidate_foreground_pixels=len(foreground[1]),
            original_foreground_bounds_inclusive=bounds(foreground[0]),candidate_foreground_bounds_inclusive=bounds(foreground[1]),
            exact_rgba_translation_matches=matches))
        literal.append(dict(screen=label,region_xyxy_exclusive=list(ROI),original_pixels=sorted((x,y,c) for (x,y),c in pixels[0].items()),
                            candidate_pixels=sorted((x,y,c) for (x,y),c in pixels[1].items())))
    raw=json.dumps(literal,separators=(',',':')).encode()+b'\n'
    packed=gzip.compress(raw,mtime=0)
    with (OUT/'complete-status-region-rgba.json.gz').open('xb') as f:f.write(packed)
    after=[identity(p) for p in paths];assert after==before;save('inputs-after.json',after)
    result=dict(status='CLOSED_READ_ONLY_STATUS_GLYPH_TRANSLATION_ANALYSIS',started_utc=started,
        finished_utc=datetime.now(timezone.utc).isoformat(),input_archive=archive,pillow_version=pillow_version,
        original_capture_run=38247941263,android_job=114806467130,android_job_conclusion='failure',
        diagnostic_region_xyxy_exclusive=list(ROI),full_frame_gate_recomputed=True,
        region_used_as_mask=False,images_modified=False,image_files_created=False,android_reexecuted=False,
        causal_claim_established=False,full_runtime_1_to_1_established=False,all_input_images_unchanged=True,
        complete_region_records=dict(compressed=digest(packed),uncompressed=digest(raw)),screens=rows)
    save('result.json',result)
    with (OUT/'README.md').open('x') as f:
        f.write('# Status-bar pixel difference in the active numeric Android run\n\nThis read-only addendum preserves the ten original screenshot identities and computes whole-frame pixel differences again. It then compares every RGBA pixel in a fixed diagnostic status-bar region and tests whether its entire foreground is exactly related by an integer translation. It does not crop, edit, regenerate, interpolate or mask either screenshot. All region pixels are retained losslessly for review.\n\nThe result records the measured translation candidates, foreground counts and remaining full-frame differences for each of the five screens. This is a spatial description of the recorded pixels. It identifies neither the status glyph\'s system cause nor an application cause. The original Android comparison remains a failure, and this addendum grants no parity credit. The indicator diagnostic runs separately with its own deliberately fixed earlier candidate.\n')
    files=[]
    for p in sorted(OUT.rglob('*')):
        if p.is_file():files.append(dict(path=p.relative_to(OUT).as_posix(),**digest(p.read_bytes()),mode='100644'))
    save('checkpoint.json',dict(schema=1,status=result['status'],repo_target='docs/verification/android-ci-8db1fca4/status-glyph-analysis',
        active_files=[],android_executed=False,full_runtime_1_to_1_established=False,files=files,
        frozen_payload_count=len(files),frozen_payload_bytes=sum(r['bytes'] for r in files)))
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),**digest((OUT/'checkpoint.json').read_bytes()),screens=rows),indent=2))

if __name__=='__main__':main()
