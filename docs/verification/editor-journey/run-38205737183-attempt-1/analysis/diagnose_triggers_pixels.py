#!/usr/bin/env python3
"""Measure complete recorded frames and retain every changed RGBA coordinate."""
from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET
from collections import Counter

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
FOLDER = ROOT / 'extracted/ci-editor/journey'


def artifact(entry):
    path = FOLDER / entry['path']
    assert path.resolve().is_relative_to(FOLDER.resolve())
    data = path.read_bytes()
    assert len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256']
    return data


def rgba(entry):
    artifact(entry)
    result = np.asarray(Image.open(FOLDER / entry['path']).convert('RGBA'))
    assert result.shape == (1280, 720, 4)
    return result


def pixels_changed(a, b):
    return int(np.any(a != b, axis=2).sum())


def main():
    report = json.loads((FOLDER / 'journey.json').read_text())
    selected = {run['label']: run['screens'][1] for run in report['runs']}
    assert all(shot['name'] == 'intro-2' for shot in selected.values())
    images = {label: rgba(shot['artifacts']['screenshot']) for label, shot in selected.items()}
    a, b = images['original'], images['candidate']
    yy, xx = np.where(np.any(a != b, axis=2))
    coordinates = [{'x':int(x), 'y':int(y), 'original_rgba':a[y,x].tolist(),
                    'candidate_rgba':b[y,x].tolist(),
                    'candidate_minus_original':(b[y,x].astype(int)-a[y,x].astype(int)).tolist()}
                   for y,x in zip(yy,xx)]
    distributions = Counter((tuple(row['original_rgba']), tuple(row['candidate_rgba'])) for row in coordinates)
    frames = []
    events = []
    for entry in report['capture_events']:
        event = json.loads(artifact(entry))
        events.append({'path':entry['path'], 'label':event['label'], 'status':event['status'],
                       'attempts':len(event['attempts']), 'accepted_pair':event.get('accepted_pair'),
                       'seconds':event['seconds']})
        for index, shot in enumerate(event['attempts']):
            hierarchy = artifact(shot['artifacts']['hierarchy'])
            tree = ET.fromstring(hierarchy)
            if not any(node.get('text') == 'TRIGGERS' and node.get('resource-id') == 'com.arlosoft.macrodroid:id/titleText'
                       for node in tree.iter('node')):
                continue
            label = event['label'].split('-',1)[0]
            assert label in images
            image = rgba(shot['artifacts']['screenshot'])
            frames.append({'label':label, 'event':entry, 'event_label':event['label'], 'attempt_index':index,
                           'selected_by_event':index in event['accepted_pair'],
                           'observation':shot['observation'], 'artifacts':shot['artifacts'],
                           'complete_png_bytes_equal_to_selected':shot['artifacts']['screenshot']['sha256'] == selected[label]['artifacts']['screenshot']['sha256'],
                           'complete_xml_bytes_equal_to_selected':shot['artifacts']['hierarchy']['sha256'] == selected[label]['artifacts']['hierarchy']['sha256'],
                           'full_rgba_pixels_different_from_same_apk_selected':pixels_changed(image,images[label]),
                           'full_rgba_pixels_different_from_other_apk_selected':pixels_changed(image,images['candidate' if label=='original' else 'original']),
                           'rgba_at_every_cross_apk_difference': [image[row['y'],row['x']].tolist() for row in coordinates]})
    assert len(coordinates) == 26 and len(frames) == 8
    assert len(events) == 38 and all(event['attempts'] == 2 and event['accepted_pair'] == [0,1] for event in events)
    assert all(frame['full_rgba_pixels_different_from_same_apk_selected'] == 0 for frame in frames)
    temporal = {}
    for label in images:
        same = [frame for frame in frames if frame['label'] == label]
        temporal[label] = {'frames':len(same), 'event_labels':sorted({frame['event_label'] for frame in same}),
                           'first_observation_start':min(frame['observation']['started_monotonic'] for frame in same),
                           'last_observation_finish':max(frame['observation']['finished_monotonic'] for frame in same),
                           'all_full_png_and_xml_bytes_identical':all(frame['complete_png_bytes_equal_to_selected'] and frame['complete_xml_bytes_equal_to_selected'] for frame in same),
                           'observed_temporal_changed_pixels':0}
        temporal[label]['observed_interval_seconds'] = temporal[label]['last_observation_finish'] - temporal[label]['first_observation_start']
    result = {'schema':1, 'run_id':38205737183, 'head_sha':'5a95831d897a6fc2b6e59a0ef4088badf63c92da',
              'scope':'Full-frame RGBA and XML observations; diagnostic coordinates only, no masking or acceptance changes',
              'selected_frames':selected, 'changed_rgba_pixels':26,
              'difference_bounds_exclusive':[int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1],
              'maximum_absolute_channel_delta':np.abs(a.astype(int)-b.astype(int)).max(axis=(0,1)).tolist(),
              'all_alpha_channels_equal':bool(np.array_equal(a[:,:,3],b[:,:,3])),
              'coordinates':coordinates,
              'color_distribution':[{'original_rgba':list(old),'candidate_rgba':list(new),'pixels':count}
                                    for (old,new),count in sorted(distributions.items())],
              'all_stabilization_events':events, 'all_triggers_stabilization_frames':frames,
              'temporal_observations':temporal,
              'selected_or_rejected_triggers_frame_omitted':False,
              'within_this_run_each_apk_full_triggers_frames_are_identical':True,
              'same_26_cross_apk_differences_in_every_triggers_frame':True,
              'cross_run_determinism_established':False, 'cause_established':False,
              'active_capture_or_comparison_guard_changed':False}
    path = ROOT / 'triggers-pixel-diagnosis.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ['changed_rgba_pixels','difference_bounds_exclusive','maximum_absolute_channel_delta',
                                                'all_alpha_channels_equal','color_distribution','coordinates','temporal_observations']},indent=2))


if __name__ == '__main__':
    main()
