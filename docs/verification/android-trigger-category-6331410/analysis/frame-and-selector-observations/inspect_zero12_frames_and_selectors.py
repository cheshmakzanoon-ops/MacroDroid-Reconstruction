#!/usr/bin/env python3
"""Describe complete recorded frames and actual category rows; take no input."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image

BASE=Path(__file__).resolve().parent
RAW=BASE/'zero12-run-38216299675-extracted/journey'
ANALYSIS=BASE/'zero12-run-38216299675-analysis'
OUT=ANALYSIS/'frame-and-selector-observations'
PACKAGE='com.arlosoft.macrodroid'


def identity(path):
    raw=path.read_bytes()
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def verified(row):
    path=RAW/row['path']
    assert path.resolve().is_relative_to(RAW.resolve()) and not path.is_symlink()
    assert identity(path)=={k:row[k] for k in ('bytes','sha256')}
    return path


def put(name,value):
    (OUT/name).write_text(json.dumps(value,indent=2)+'\n')


def main():
    OUT.mkdir(parents=True,exist_ok=False)
    closed=json.loads((ANALYSIS/'independent-zero12-analysis.json').read_text())
    assert closed['literal_verifier_reproduced_except_replay_timestamp'] and closed['evidence_valid']
    report=json.loads((RAW/'journey.json').read_text())
    ledgers=[]
    physical=set()
    triggers={'original':[],'candidate':[]}
    for event in report['capture_events']:
        ledger=json.loads(verified(event).read_text())
        assert ledger['status']=='CONSECUTIVE_FULL_FRAMES_IDENTICAL'
        assert ledger['accepted_pair']==[0,1] and len(ledger['attempts'])==2
        frame_records=[]
        for attempt in ledger['attempts']:
            for row in attempt['artifacts'].values():
                path=verified(row);st=path.stat()
                token=(st.st_dev,st.st_ino)
                assert token not in physical
                physical.add(token)
            picture=attempt['artifacts']['screenshot'];xml=attempt['artifacts']['hierarchy']
            tree=ET.fromstring(verified(xml).read_bytes())
            is_triggers=any(n.get('resource-id')==PACKAGE+':id/titleText' and n.get('text')=='TRIGGERS'
                            for n in tree.iter('node'))
            frame_records.append({'screenshot':picture,'hierarchy':xml,'observation':attempt['observation']})
            if is_triggers:
                label='original' if event['path'].startswith('original-') else 'candidate'
                triggers[label].append({'ledger':event['path'],**frame_records[-1]})
        assert frame_records[0]['screenshot']['sha256']==frame_records[1]['screenshot']['sha256']
        assert frame_records[0]['hierarchy']['sha256']==frame_records[1]['hierarchy']['sha256']
        ledgers.append({'path':event['path'],'seconds':ledger['seconds'],'max_seconds':ledger['max_seconds'],
                        'accepted_pair':ledger['accepted_pair'],'all_full_png_and_xml_bytes_equal':True,
                        'first_start':frame_records[0]['observation']['started_monotonic'],
                        'last_finish':frame_records[-1]['observation']['finished_monotonic']})
    assert len(ledgers)==46 and len(physical)==552
    assert [len(triggers[k]) for k in ('original','candidate')]==[4,4]
    arrays={label:[np.asarray(Image.open(verified(row['screenshot'])).convert('RGBA')) for row in frames]
            for label,frames in triggers.items()}
    all_pairs=[]
    for left_label,right_label in [('original','original'),('candidate','candidate'),('original','candidate')]:
        for i,left in enumerate(arrays[left_label]):
            for j,right in enumerate(arrays[right_label]):
                if left_label==right_label and j<=i:continue
                yy,xx=np.where(np.any(left!=right,axis=2))
                all_pairs.append({'left_label':left_label,'left_index':i,'right_label':right_label,'right_index':j,
                                  'changed_rgba_pixels':len(xx),
                                  'bounds_exclusive':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)] if len(xx) else None})
    same=[p for p in all_pairs if p['left_label']==p['right_label']]
    cross=[p for p in all_pairs if p['left_label']!=p['right_label']]
    assert len(same)==12 and len(cross)==16
    assert all(p['changed_rgba_pixels']==0 for p in same)
    assert all(p['changed_rgba_pixels']==5 for p in cross)
    rows_by_variant={}
    for run in report['runs']:
        shot=run['screens'][-1]
        assert shot['name']=='after-trigger-date-category'
        tree=ET.fromstring(verified(shot['artifacts']['hierarchy']).read_bytes())
        parents={child:parent for parent in tree.iter() for child in parent}
        rows=[]
        for node in tree.iter('node'):
            if node.get('resource-id')!=PACKAGE+':id/select_item_name':continue
            ancestor=parents.get(node)
            while ancestor is not None and ancestor.get('clickable')!='true':ancestor=parents.get(ancestor)
            assert ancestor is not None and ancestor.get('resource-id')==PACKAGE+':id/select_item_row_frame'
            rows.append({'text':node.get('text'),'text_node':dict(node.attrib),'clickable_row':dict(ancestor.attrib)})
        assert len(rows)==7
        day=[row for row in rows if row['text']=='Day/Time']
        assert len(day)==1 and day[0]['clickable_row']['enabled']=='true'
        assert day[0]['clickable_row']['bounds']=='[14,574][354,678]'
        rows_by_variant[run['label']]={'screenshot':shot['artifacts']['screenshot'],'hierarchy':shot['artifacts']['hierarchy'],
                                      'foreground':shot['artifacts']['foreground'],'rows':rows}
    assert rows_by_variant['original']['rows']==rows_by_variant['candidate']['rows']
    put('all46-stabilization-ledgers.json',ledgers)
    put('all28-within-and-cross-trigger-frame-pairs.json',{'frames':triggers,'comparisons':all_pairs})
    put('observed-date-time-category-rows.json',rows_by_variant)
    result={'schema':1,'status':'RECORDED_ZERO12_STILL_FRAMES_AND_OBSERVED_SELECTORS_VERIFIED',
            'observed_utc':datetime.now(timezone.utc).isoformat(),'run_id':38216299675,
            'all_complete_ledgers_accept_first_two_identical_full_frames':46,
            'distinct_physical_observation_artifacts':552,
            'retained_trigger_frames_per_variant':4,
            'within_variant_trigger_frame_comparisons':12,'within_variant_changed_pixels':[p['changed_rgba_pixels'] for p in same],
            'cross_variant_trigger_frame_comparisons':16,'cross_variant_changed_pixels':[p['changed_rgba_pixels'] for p in cross],
            'date_time_visible_row_texts':[r['text'] for r in rows_by_variant['original']['rows']],
            'day_time_unique_enabled_clickable_row_bounds':'[14,574][354,678]',
            'possible_row_center_if_future_fresh_guards_pass':[184,626],
            'any_day_time_row_input_executed':False,'any_raw_capture_modified':False,
            'pixel_masks_tolerance_or_cross_apk_frame_selection':False,
            'animation_or_full_runtime_parity_established':False}
    put('result.json',result)
    (OUT/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
