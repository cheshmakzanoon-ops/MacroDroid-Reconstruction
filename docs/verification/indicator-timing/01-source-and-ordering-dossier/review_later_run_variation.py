#!/usr/bin/env python3
"""Read five available paired screens from the later incomplete DayTime run."""
from pathlib import Path
import hashlib
import itertools
import json
import zipfile
import numpy as np
from PIL import Image

BASE = Path('/workspace/scratch/4130730d15aa')
ROOT = Path(__file__).resolve().parent
RAW = BASE / 'ci-run-analysis/daytime13-run-38221713675-extracted'
ZIP = BASE / 'ci-run-analysis/daytime13-run-38221713675.zip'
OLD = BASE / 'ci-run-analysis/zero12-run-38216299675-extracted/journey'
OUT = ROOT / 'reports/07-later-incomplete-run-five-screen-observations'


def identity(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return {'path': str(p), 'bytes': p.stat().st_size, 'sha256': h.hexdigest()}


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    before = [identity(Path(__file__).resolve()), identity(ZIP)]
    assert before[-1]['sha256'] == 'ad31af7b9fb237dbca1285a671a3e12fdcd9c3cd3754f55064055066043dffa4'
    jp = RAW / 'journey/journey.json'
    before.append(identity(jp))
    d = json.loads(jp.read_text())
    assert d['status'] == 'RECORDED_NOT_PARITY'
    a, b = d['runs']
    assert (a['label'], a['status'], len(a['screens'])) == ('original', 'FAILED', 5)
    assert (b['label'], b['status'], len(b['screens'])) == ('candidate', 'COMPLETE', 13)
    assert a['apk_sha256'] == '84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'
    assert b['apk_sha256'] == '5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182'
    for run in (a, b):
        for key in ('animator_duration_scale', 'window_animation_scale', 'transition_animation_scale'):
            assert run['environment']['global:' + key] == '0'
    pairs = []
    raw_inputs = []
    image_sets = {}
    with zipfile.ZipFile(ZIP) as z:
        assert jp.read_bytes() == z.read('journey/journey.json')
        for sa, sb in zip(a['screens'], b['screens']):
            assert sa['name'] == sb['name']
            imgs, xmls = [], []
            for run, screen in ((a, sa), (b, sb)):
                for kind in ('screenshot', 'hierarchy'):
                    row = screen['artifacts'][kind]
                    p = RAW / 'journey' / row['path']
                    actual = identity(p)
                    assert actual['bytes'] == row['bytes'] and actual['sha256'] == row['sha256']
                    assert p.read_bytes() == z.read('journey/' + row['path'])
                    before.append(actual)
                    raw_inputs.append({**actual, 'run': run['label'], 'screen': screen['name'], 'kind': kind})
                    if kind == 'screenshot':
                        arr = np.asarray(Image.open(p).convert('RGBA'))
                        assert arr.shape == (1280, 720, 4)
                        imgs.append(arr)
                        if screen['name'] == 'intro-2':
                            image_sets['later-' + run['label']] = arr
                    else:
                        xmls.append(p.read_bytes())
            count = int(np.count_nonzero(np.any(imgs[0] != imgs[1], axis=2)))
            assert count == 0 and xmls[0] == xmls[1]
            pairs.append({'screen': sa['name'], 'full_frame_different_pixels': count,
                          'xml_bytes_identical': True, 'entire_frame_compared': True})
    for label, expected in [('original', '9c5afe54308ce2bf5cf00fd5a95c24ad589f83ff590ecad3cb95cf6f94576322'),
                            ('candidate', '92a14136c68347341c9dd190adef81f5453a91190dc857585b04ce8a65e1e25e')]:
        p = OLD / f'{label}-intro-2-acquisition-1-frame-2.png'
        row = identity(p)
        assert row['sha256'] == expected
        before.append(row)
        image_sets['earlier-' + label] = np.asarray(Image.open(p).convert('RGBA'))
    cross_runs = []
    for left, right in itertools.combinations(sorted(image_sets), 2):
        ia, ib = image_sets[left], image_sets[right]
        pos = np.argwhere(np.any(ia != ib, axis=2))
        cross_runs.append({'left': left, 'right': right, 'entire_frame_compared': True,
                           'different_pixels': len(pos),
                           'pixels': [{'x': int(x), 'y': int(y), 'left_rgba': ia[y,x].tolist(),
                                       'right_rgba': ib[y,x].tolist()} for y, x in pos]})
    for row in before:
        assert identity(Path(row['path'])) == row
    result = {'status': 'LATER_INCOMPLETE_RUN_FIVE_SCREEN_OBSERVATIONS_VERIFIED',
              'original_status_unchanged': a['status'], 'candidate_status_unchanged': b['status'],
              'journey_status_unchanged': d['status'], 'journey_parity_claimed': False,
              'five_screen_pairs': pairs, 'intro2_cross_run_pairs': cross_runs,
              'new_android_execution': False, 'raw_archive_or_inputs_modified': False,
              'pixel_mask_tolerance_or_cross_frame_selection': False,
              'cause_proven': False, 'unchanged_input_observations': len(before)}
    (OUT / 'result.json').write_text(json.dumps(result,indent=2) + '\n')
    (OUT / 'input-identities-before-after.json').write_text(json.dumps(before,indent=2) + '\n')
    (OUT / 'raw-inputs.json').write_text(json.dumps(raw_inputs,indent=2) + '\n')
    print(json.dumps({'status':result['status'], 'paired_screens':pairs,
                      'cross_run_pixel_counts':[{k:p[k] for k in ('left','right','different_pixels')} for p in cross_runs],
                      'journey_parity_claimed':False},sort_keys=True))


if __name__ == '__main__':
    main()
