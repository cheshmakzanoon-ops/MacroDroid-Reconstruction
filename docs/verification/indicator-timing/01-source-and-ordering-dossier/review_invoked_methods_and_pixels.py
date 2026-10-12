#!/usr/bin/env python3
"""Close the correctly scoped class/method audit and compare every retained frame.

The earlier all-class assertion stays failed. This report explicitly distinguishes
the single registered q77.B change from the unchanged q77.t drawing dependency.
"""
from pathlib import Path
import hashlib
import importlib.util
import itertools
import json
import re
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'reports/01-exact-input-and-path-observations'
OUT = ROOT / 'reports/03-invoked-method-and-full-frame-review'
COLLECTOR = OLD / 'collector-at-execution.py'
assert hashlib.sha256(COLLECTOR.read_bytes()).hexdigest() == 'ec84ee7d904340236eaddfbb6bcf947c157fa0f2817ceb03630fe540a4c3df02'
spec = importlib.util.spec_from_file_location('closed_indicator_collector', COLLECTOR)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
c.OUT = OUT
METHOD = re.compile(r'^\.method [^\n]+\n.*?^\.end method$', re.M | re.S)


def methods(text):
    result = {}
    for match in METHOD.finditer(text):
        key = match.group(0).splitlines()[0].rsplit(' ', 1)[-1]
        assert key not in result
        result[key] = match.group(0)
    return result


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    before = [c.identity(Path(__file__).resolve()), c.identity(COLLECTOR)]
    old_cp = c.OLD / 'checkpoint.json'
    before.append(c.exact(old_cp, '8792b2936e0d2832361c98699b707ceb7982373cbb661048b549bedfcce174ab'))
    historical = json.loads(old_cp.read_text())
    for row in historical['files']:
        before.append(c.exact(c.OLD / row['path'], row['sha256'], row['bytes']))
    historical_paths = {r['path'][len('preserved-source/'):] for r in historical['files']
                        if r['path'].startswith('preserved-source/')}
    class_path = OLD / 'class-byte-results.json'
    before.append(c.identity(class_path))
    class_rows = json.loads(class_path.read_text())
    assert len(class_rows) == 52
    changed = []
    exact_classes = []
    q77 = None
    for row in class_rows:
        src = c.PROJECT / row['source']
        preserved = OLD / 'preserved-source' / row['source']
        actual = Path(row['output']['path'])
        before.extend([c.exact(src, row['sha256'], row['bytes']),
                       c.exact(preserved, row['sha256'], row['bytes']),
                       c.exact(actual, row['output']['sha256'], row['output']['bytes'])])
        equal = src.read_bytes() == actual.read_bytes()
        assert equal == row['complete_smali_bytes_equal']
        if row['source'] in historical_paths:
            assert equal, 'A historical eighteen-class member differs'
        if equal:
            exact_classes.append({'variant': row['variant'], 'descriptor': row['descriptor']})
            continue
        assert row['variant'] == 'candidate' and row['descriptor'] == 'Lq77;'
        a, b = src.read_text(), actual.read_text()
        am, bm = methods(a), methods(b)
        assert am.keys() == bm.keys()
        assert METHOD.sub('<METHOD>', a) == METHOD.sub('<METHOD>', b)
        delta = [k for k in am if am[k] != bm[k]]
        assert delta == ['B(Ljava/lang/String;Ljava/lang/String;Ljava/lang/StringBuilder;)Ljava/lang/String;']
        invoked = 't(FFFF)F'
        assert am[invoked] == bm[invoked]
        (OUT / 'q77-invoked-t-original-and-candidate-identical.smali').write_text(am[invoked] + '\n')
        q77 = {'descriptor': row['descriptor'], 'whole_class_equal': False,
               'changed_methods': delta, 'method_interface_equal': True,
               'non_method_metadata_equal': True, 'invoked_method': invoked,
               'invoked_method_complete_bytes_equal': True,
               'invoked_method_sha256': hashlib.sha256(am[invoked].encode()).hexdigest()}
        changed.append(q77)
    assert len(exact_classes) == 51 and len(changed) == 1 and q77 is not None
    reg = Path('/tmp/macrodroid-widget-plugin-combined-qmngc23u/MacroDroid_v9/source/java-method-map.json')
    before.append(c.identity(reg))
    expected = {'target': 'Lq77;', 'method': q77['changed_methods'][0],
                'helper': 'Lrecovered/strings/LegacyStrings;', 'helper_method': 'appendSuffix',
                'instance': False, 'java_source': 'source/java/recovered/strings/LegacyStrings.java'}
    registrations = [r for r in json.loads(reg.read_text()) if r['target'] == 'Lq77;']
    assert registrations == [expected]
    q77['existing_registered_change'] = expected
    for apk, sha, size in c.APKS.values():
        before.append(c.exact(apk, sha, size))
    before.append(c.exact(c.ARCHIVE, '1ea3ad6302d53c2fcc8341c03deec7ccd04d729facaf5658acb87e4aebc6f4b3', 42199893))
    jp = c.RAW / 'journey/journey.json'
    before.append(c.exact(jp, 'a6253dfea14353a2d8fe552e3772e4fe5e58a693e2339bafcce9f0d008a61409', 839255))
    journey = json.loads(jp.read_text())
    assert [r['apk_sha256'] for r in journey['runs']] == [c.APKS[k][1] for k in ('original', 'candidate')]
    names = ['intro-2-acquisition-1-frame-1', 'intro-2-acquisition-1-frame-2',
             'intro-3-before-acquisition-1-frame-1', 'intro-3-before-acquisition-1-frame-2']
    images, frame_rows, indicators = {}, [], []
    with zipfile.ZipFile(c.ARCHIVE) as z:
        assert len(z.namelist()) == len(set(z.namelist())) == 2944
        for label in c.APKS:
            for name in names:
                stem = label + '-' + name
                for ext in ('png', 'xml'):
                    member = 'journey/' + stem + '.' + ext
                    p = c.RAW / member
                    row = c.identity(p)
                    assert p.read_bytes() == z.read(member)
                    before.append(row)
                    frame_rows.append({**row, 'archive_member': member})
                images[stem] = np.asarray(Image.open(c.RAW / ('journey/' + stem + '.png')).convert('RGBA'))
            p = c.RAW / f'journey/{label}-intro-2-acquisition-1-frame-2.xml'
            nodes = [n for n in ET.fromstring(p.read_bytes()).iter('node')
                     if n.get('resource-id') == 'com.arlosoft.macrodroid:id/indicator']
            assert len(nodes) == 1
            indicators.append({'variant': label, 'attributes': dict(nodes[0].attrib)})
    pairs = []
    for left, right in itertools.combinations(sorted(images), 2):
        a, b = images[left], images[right]
        assert a.shape == b.shape == (1280, 720, 4)
        pos = np.argwhere(np.any(a != b, axis=2))
        pairs.append({'left': left, 'right': right, 'different_pixels': len(pos),
                      'entire_frame_compared': True,
                      'pixels': [{'x': int(x), 'y': int(y), 'left_rgba': a[y, x].tolist(),
                                  'right_rgba': b[y, x].tolist()} for y, x in pos]})
    within = [p for p in pairs if p['left'].split('-')[0] == p['right'].split('-')[0]]
    cross = [p for p in pairs if p not in within]
    assert len(within) == 12 and len(cross) == 16
    assert all(p['different_pixels'] == 0 for p in within)
    assert all(p['different_pixels'] == 5 for p in cross)
    representative = next(p for p in cross if p['left'] == 'candidate-intro-2-acquisition-1-frame-2'
                          and p['right'] == 'original-intro-2-acquisition-1-frame-2')
    pixels = [{'x': p['x'], 'y': p['y'], 'original_rgba': p['right_rgba'],
               'candidate_rgba': p['left_rgba']} for p in representative['pixels']]
    for row in before:
        assert c.identity(Path(row['path'])) == row, 'Input changed during review'
    c.save('input-identities-before-after.json', {'all_unchanged': True, 'inputs': before})
    c.save('whole-class-and-invoked-method-results.json', {
        'historical_classes': 18, 'historical_apk_comparisons_equal': 36,
        'all_selected_classes': 26, 'whole_class_comparisons_equal': 51,
        'whole_class_comparisons_total': 52, 'exact_classes': exact_classes,
        'explicit_non_equal_class': q77, 'initial_broad_class_gate_remains_failed': True})
    c.save('raw-frame-inputs.json', frame_rows)
    c.save('all28-exact-full-frame-pairs.json', pairs)
    c.save('five-pixel-observations.json', {'original_then_candidate': pixels})
    c.save('indicator-xml-observations.json', indicators)
    c.save('captured-environments.json', [{'variant': r['label'], 'before': r['environment'],
                                         'after': r['environment_after']} for r in journey['runs']])
    c.save('result.json', {'status': 'SCOPED_SOURCE_AND_RAW_FRAME_OBSERVATIONS_VERIFIED',
                          'historical_class_comparisons_equal': 36,
                          'selected_whole_class_comparisons_equal': 51,
                          'selected_whole_class_comparisons_total': 52,
                          'q77_t_complete_bytes_equal': True, 'q77_B_registered_change': True,
                          'raw_within_apk_pairs': 12, 'raw_within_apk_all_zero_pixels': True,
                          'raw_cross_apk_pairs': 16, 'raw_cross_apk_all_five_pixels': True,
                          'input_identity_observations_unchanged': len(before),
                          'new_android_execution': False, 'new_disassembly': False,
                          'app_source_or_apk_changed': False,
                          'mask_tolerance_or_cross_apk_frame_selection': False,
                          'cause_proven': False})
    print((OUT / 'result.json').read_text())


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        if OUT.is_dir():
            c.save('failure.json', {'type': type(exc).__name__, 'message': str(exc)})
        raise
