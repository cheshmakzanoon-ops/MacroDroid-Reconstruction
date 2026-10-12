#!/usr/bin/env python3
"""Bind the prior all-scales-one failure without converting it to parity."""
from pathlib import Path
import json
import zipfile
import numpy as np
from PIL import Image
from review_later_run_variation import identity

BASE = Path('/workspace/scratch/4130730d15aa')
ROOT = Path(__file__).resolve().parent
RAW = BASE / 'tooling-validation/normal-animation-run-38212813248'
ZIP = RAW.with_suffix('.zip')
RECEIPT = BASE / 'tooling-validation/normal-animation-run-38212813248-extraction.json'
OUT = ROOT / 'reports/08-prior-normal-scale-failure-context'


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    before = [identity(Path(__file__).resolve()), identity(ROOT / 'review_later_run_variation.py'),
              identity(ZIP), identity(RECEIPT)]
    assert before[-2]['bytes'] == 28080813
    assert before[-2]['sha256'] == '93cfed4c5f5c17170a926bd79781807422698c22b26cf7afc60430b2a7183d92'
    receipt = json.loads(RECEIPT.read_text())
    assert receipt['run_id'] == 38212813248 and receipt['member_count'] == 952
    assert receipt['head_sha'] == '3edcddd86660ea10c8aff71b651b446f86412525'
    jp = RAW / 'journey/journey.json'
    before.append(identity(jp))
    d = json.loads(jp.read_text())
    assert d['status'] == 'RECORDED_NOT_PARITY'
    summaries = []
    with zipfile.ZipFile(ZIP) as z:
        assert len(z.namelist()) == len(set(z.namelist())) == 952
        assert jp.read_bytes() == z.read('journey/journey.json')
        for run in d['runs']:
            label = run['label']
            assert run['status'] == 'FAILED' and run['current_step'] == 'intro-2'
            assert len(run['screens']) == 1
            expected = ('84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800'
                        if label == 'original' else
                        '9108b5811757e20f079ab22f2d19e65135e4b863489e6c17a6a3f524bfc7c1e2')
            assert run['apk_sha256'] == expected
            for key in ('animator_duration_scale', 'window_animation_scale', 'transition_animation_scale'):
                assert run['environment']['global:' + key] == '1'
            rel = 'journey/' + label + '-intro-2-acquisition-1-settling.json'
            p = RAW / rel
            before.append(identity(p))
            assert p.read_bytes() == z.read(rel)
            ledger = json.loads(p.read_text())
            assert ledger['status'] == 'FAILED'
            (OUT / p.name).write_bytes(p.read_bytes())
            images = []
            xmls = []
            for attempt in ledger['attempts']:
                for kind in ('screenshot', 'hierarchy'):
                    row = attempt['artifacts'][kind]
                    fp = RAW / 'journey' / row['path']
                    actual = identity(fp)
                    assert actual['sha256'] == row['sha256'] and actual['bytes'] == row['bytes']
                    assert fp.read_bytes() == z.read('journey/' + row['path'])
                    before.append(actual)
                    if kind == 'screenshot':
                        im = np.asarray(Image.open(fp).convert('RGBA'))
                        assert im.shape == (1280,720,4)
                        images.append(im)
                    else:
                        xmls.append(fp.read_bytes())
            adjacent = []
            for i in range(1,len(images)):
                pos = np.argwhere(np.any(images[i-1] != images[i],axis=2))
                assert len(pos) > 0
                adjacent.append({'first_sample': i, 'second_sample': i+1,
                                 'entire_frame_compared': True, 'different_pixels': len(pos),
                                 'difference_bounds_inclusive': [int(pos[:,1].min()), int(pos[:,0].min()),
                                                                 int(pos[:,1].max()), int(pos[:,0].max())],
                                 'hierarchy_bytes_equal': xmls[i-1] == xmls[i]})
            summaries.append({'label': label, 'apk_sha256': expected, 'status': run['status'],
                              'reason': run['reason'], 'current_step':run['current_step'],
                              'completed_screen_count':1, 'environment':run['environment'],
                              'completed_failed_acquisition_samples':len(images),
                              'ledger_status':ledger['status'], 'ledger_reason':ledger.get('reason'),
                              'adjacent_full_frame_comparisons':adjacent})
    for row in before:
        assert identity(Path(row['path'])) == row
    result = {'status':'PRIOR_ALL_SCALES_ONE_FAILURE_CONTEXT_VERIFIED',
              'actual_run_id':38212813248, 'actual_candidate_is_older_9108':True,
              'candidate_is_not_combined_5f635e':True, 'runs':summaries,
              'new_android_execution':False, 'full_frame_settling_pass_claimed':False,
              'parity_claimed':False, 'indicator_crop_used_for_acceptance':False,
              'inputs_unchanged':len(before)}
    (OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'input-identities-before-after.json').write_text(json.dumps(before,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
