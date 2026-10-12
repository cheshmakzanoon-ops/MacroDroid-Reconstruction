#!/usr/bin/env python3
"""A labeled source-derived witness; this is not original Android execution."""
from pathlib import Path
import copy
import hashlib
import json
import re
import struct

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'reports/01-exact-input-and-path-observations/disassembled/original/classes'
OUT = ROOT / 'reports/06-source-derived-ordering-witness'
METHOD = re.compile(r'^\.method [^\n]+\n.*?^\.end method$', re.M | re.S)
TARGETS = {
    'agency/tango/materialintroscreen/widgets/InkPageIndicator.smali':
        ['b(IFI)V', 'c(I)V', 'f()V', 'g()V', 'setSelectedPage(I)V', 'onDraw(Landroid/graphics/Canvas;)V'],
    'androidx/viewpager/widget/ViewPager.smali':
        ['setCurrentItem(I)V', 'u(IIZZ)V', 't(IIZZ)V', 'computeScroll()V', 'i()Lx5h;', 'n(I)Z', 'k(IFI)V'],
    'iz7.smali': ['onAnimationStart(Landroid/animation/Animator;)V', 'onAnimationEnd(Landroid/animation/Animator;)V'],
    'kz7.smali': ['onAnimationUpdate(Landroid/animation/ValueAnimator;)V'],
    'lz7.smali': ['onAnimationStart(Landroid/animation/Animator;)V', 'onAnimationEnd(Landroid/animation/Animator;)V'],
    'oz7.smali': ['b(F)V'],
    'x82.smali': ['onAnimationUpdate(Landroid/animation/ValueAnimator;)V'],
    'v6.smali': ['onAnimationEnd(Landroid/animation/Animator;)V'],
    'lt1.smali': ['run()V'],
}


def f32(v):
    return struct.unpack('>f', struct.pack('>f', v))[0]


def bits(v):
    return '0x' + struct.pack('>f', v).hex()


def scrolled(state, position, fraction):
    """Transcribed arithmetic/branches of original b(IFI), independently labeled."""
    if not state['D']:
        return
    previous = state['v'] if state['E'] else state['u']
    if previous != position:
        fraction = f32(f32(1) - fraction)
        if fraction == f32(1):
            position = min(previous, position)
    if state['z'] is not None and position < len(state['z']):
        state['z'][position] = fraction
        state['post_invalidations'] += 1


def retreat_finished(state):
    """f() plus following E=false store in the actual iz7 discriminator-0 arm."""
    state['z'] = [f32(0)] * (state['t'] - 1)
    state['C'] = [f32(0)] * state['t']
    state['A'] = state['B'] = f32(-1)
    state['x'] = True
    state['E'] = False


def snapshot(state):
    return {**copy.deepcopy(state), 'z_float_bits': [bits(v) for v in state['z']]}


def witness(last_x, reset_after_terminal=False):
    state = {'D': True, 'E': True, 'u': 1, 'v': 0, 't': 4,
             'z': [f32(0)] * 3, 'C': [f32(0)] * 4,
             'A': f32(-1), 'B': f32(-1), 'x': True, 'post_invalidations': 0}
    trace = []
    if not reset_after_terminal:
        retreat_finished(state)
        trace.append({'event': 'retreat completion before final pager callbacks', 'state': snapshot(state)})
    fraction = f32(f32(last_x) / f32(720))
    scrolled(state, 0, fraction)
    trace.append({'event': 'pager old-page callback', 'position': 0,
                  'fraction': fraction, 'fraction_bits': bits(fraction), 'state': snapshot(state)})
    scrolled(state, 1, f32(0))
    trace.append({'event': 'pager exact terminal callback', 'position': 1,
                  'fraction': 0.0, 'state': snapshot(state)})
    if reset_after_terminal:
        retreat_finished(state)
        trace.append({'event': 'retreat completion after final pager callbacks', 'state': snapshot(state)})
    return {'last_nonterminal_scroll_x_assumption': last_x,
            'client_width_assumption': 720, 'margin_assumption': 0,
            'reset_after_terminal': reset_after_terminal, 'trace': trace,
            'final_joining_fraction': state['z'][0], 'final_joining_fraction_bits': bits(state['z'][0]),
            'old_page_draw_branch': ('two facing cubic/arc lobes' if 0 < state['z'][0] <= 0.5
                                     else 'plain old-page circle'),
            'selected_page_slot_final_zero': state['z'][1] == 0}


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    inputs, excerpts = [], []
    for rel, targets in TARGETS.items():
        path = SOURCE / rel
        raw = path.read_bytes()
        inputs.append({'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
        all_methods = {m.group(0).splitlines()[0].rsplit(' ', 1)[-1]: m.group(0)
                       for m in METHOD.finditer(raw.decode())}
        for target in targets:
            body = all_methods[target]
            excerpts.append({'class_path': rel, 'method': target,
                             'sha256': hashlib.sha256(body.encode()).hexdigest(), 'complete_text': body})
    rows = [witness(718), witness(719), witness(718, True), witness(719, True)]
    assert rows[0]['final_joining_fraction'] != rows[1]['final_joining_fraction']
    assert all(r['final_joining_fraction'] > 0 for r in rows[:2])
    assert all(r['final_joining_fraction'] == 0 for r in rows[2:])
    assert all(r['selected_page_slot_final_zero'] for r in rows)
    for row in inputs:
        raw = Path(row['path']).read_bytes()
        assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
    result = {'status': 'SOURCE_DERIVED_ORDERING_WITNESS_RECORDED',
              'original_or_candidate_method_executed': False, 'new_android_execution': False,
              'positive_parity_cases_added': 0, 'actual_callback_order_observed': False,
              'actual_718_or_719_scroll_samples_observed': False,
              'scope': 'Four explicit float32 model traces; no prediction of an exact pixel count',
              'source_methods': len(excerpts), 'source_classes': len(inputs),
              'traces': rows, 'sources_unchanged': True}
    (OUT / 'source-excerpts.json').write_text(json.dumps(excerpts, indent=2) + '\n')
    (OUT / 'source-identities.json').write_text(json.dumps(inputs, indent=2) + '\n')
    (OUT / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'traces'}, sort_keys=True))


if __name__ == '__main__':
    main()
