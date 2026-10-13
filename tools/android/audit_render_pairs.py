#!/usr/bin/env python3
"""Audit complete, unmasked Android screenshot pairs for deterministic drift.

This is a diagnostic, *not* an app-parity verifier. It reports every differing
pixel, its bounding rectangle, row/column coverage, and the most common exact
RGBA changes. It does not crop, normalize away, recolor, or mask differences.
The existing strict PNG decoder validates dimensions, filters, CRC and metadata.

Example:
  python3 tools/android/audit_render_pairs.py --pair intro-2 orig.png rebuilt.png \
      --pair permission orig-perm.png rebuilt-perm.png --output report.json
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'project'))
from android_compare import CaptureError, color_metadata, png_pixels

MAX_PAIRS = 32
MAX_FILE = 128_000_000


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pixels_as_rgba(pixels: bytes, width: int, height: int) -> bytes:
    count = width * height
    if not count or len(pixels) not in (3 * count, 4 * count):
        raise ValueError('Unexpected strict decoder pixel layout')
    if len(pixels) == 4 * count:
        return pixels
    rgba = bytearray(4 * count)
    for src in range(0, len(pixels), 3):
        dst = (src // 3) * 4
        rgba[dst:dst + 4] = pixels[src:src + 3] + b'\xff'
    return bytes(rgba)


def checked_bytes(path: Path) -> bytes:
    if not path.is_file() or path.stat().st_size > MAX_FILE:
        raise ValueError('Screenshot missing or beyond the bounded PNG allowance')
    return path.read_bytes()


def audit_pair(label: str, original: Path, candidate: Path) -> dict:
    if not re.fullmatch(r'[a-z0-9][a-z0-9_.-]{0,63}', label):
        raise ValueError('Pair label must be a compact literal identifier')
    if original.resolve() == candidate.resolve() or original.stat().st_ino == candidate.stat().st_ino and original.stat().st_dev == candidate.stat().st_dev:
        raise ValueError('Two independent screenshot files are required')
    a, b = checked_bytes(original), checked_bytes(candidate)
    aw, ah, ap = png_pixels(a)
    bw, bh, bp = png_pixels(b)
    result = {
        'label': label, 'scope': 'Entire decoded image; no masks or tolerances',
        'original': {'filename': original.name, 'bytes': len(a), 'sha256': sha256(a), 'width': aw, 'height': ah},
        'candidate': {'filename': candidate.name, 'bytes': len(b), 'sha256': sha256(b), 'width': bw, 'height': bh},
        'identical_png_bytes': a == b,
        'identical_png_color_metadata': color_metadata(a) == color_metadata(b),
        'masks_used': False, 'pixel_tolerance': 0,
        'whole_app_parity_established': False,
    }
    if (aw, ah) != (bw, bh):
        result.update(status='DIMENSION_MISMATCH', exact_pixels_equal=False,
                      changed_pixels=None, changed_bbox_xyxy=None, rows_with_changes=None,
                      columns_with_changes=None, largest_row_change_counts=[], common_rgba_changes=[])
        return result

    first, second = pixels_as_rgba(ap, aw, ah), pixels_as_rgba(bp, bw, bh)
    changed = 0
    min_x, min_y, max_x, max_y = aw, ah, -1, -1
    rows = [0] * ah
    cols = [0] * aw
    changes: Counter[tuple[tuple[int, ...], tuple[int, ...]]] = Counter()
    for i in range(aw * ah):
        j = i * 4
        before, after = first[j:j + 4], second[j:j + 4]
        if before == after:
            continue
        x, y = i % aw, i // aw
        changed += 1
        rows[y] += 1
        cols[x] += 1
        min_x, min_y = min(min_x, x), min(min_y, y)
        max_x, max_y = max(max_x, x), max(max_y, y)
        changes[(tuple(before), tuple(after))] += 1
    result.update(
        status='EXACT_PIXELS' if changed == 0 else 'PIXEL_DIFFERENCE',
        exact_pixels_equal=(changed == 0),
        changed_pixels=changed,
        changed_bbox_xyxy=[min_x, min_y, max_x, max_y] if changed else None,
        rows_with_changes=sum(v > 0 for v in rows),
        columns_with_changes=sum(v > 0 for v in cols),
        largest_row_change_counts=[{'y': i, 'changed_pixels': n} for i, n in sorted(
            enumerate(rows), key=lambda p: (-p[1], p[0])) if n][:12],
        common_rgba_changes=[{'original_rgba': list(colors[0]), 'candidate_rgba': list(colors[1]),
                              'count': count} for colors, count in sorted(changes.items(),
                              key=lambda v: (-v[1], v[0]))[:12]],
    )
    return result


def make_report(pairs: list[list[str]]) -> dict:
    if not pairs or len(pairs) > MAX_PAIRS:
        raise ValueError('Expected between one and 32 unique screenshot pairs')
    if len({p[0] for p in pairs}) != len(pairs):
        raise ValueError('Duplicate pair labels are forbidden')
    checked = [audit_pair(label, Path(first), Path(second)) for label, first, second in pairs]
    return {
        'schema': 1,
        'status': 'DIAGNOSTIC_ONLY',
        'mask_or_tolerance_based_parity': False,
        'pair_count': len(checked),
        'all_pixels_equal': all(row['exact_pixels_equal'] for row in checked),
        'whole_app_parity_established': False,
        'pairs': checked,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pair', nargs=3, metavar=('LABEL', 'ORIGINAL', 'CANDIDATE'),
                        action='append', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = make_report(args.pair)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if any(args.output.resolve() == Path(path).resolve() for p in args.pair for path in p[1:]):
            raise ValueError('The report may not overwrite a screenshot')
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    except (OSError, ValueError, CaptureError) as exc:
        parser.exit(2, f'Invalid diagnostic evidence: {exc}\n')
    print(json.dumps({'status': report['status'], 'all_pixels_equal': report['all_pixels_equal'],
                      'changed_pixels': {p['label']: p['changed_pixels'] for p in report['pairs']}}, indent=2))
    # Producing a DIFFERENCE report is a successful diagnostic, *not* an acceptance pass.
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
