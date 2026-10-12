#!/usr/bin/env python3
"""Bounded local timing check of exact-byte PNG decoding; no device actions."""
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'project'), str(ROOT / 'tools/parity_journeys')]
import android_compare as proof
import observed_journey as observed

data = (ROOT / 'tools/parity_journeys/fixtures/favourite-triggers-api35.png').read_bytes()
assert hashlib.sha256(data).hexdigest() == 'a825ecda49d1d7e04e65a84d1579f47219d52eb6ffba66519401e4177b5f2689'
started = time.perf_counter()
direct = proof.png_pixels(data)
direct_seconds = time.perf_counter() - started
observed._decoded_png.cache_clear()
started = time.perf_counter()
for _ in range(11):
    assert observed.png_pixels(data, proof) == direct
cached_seconds = time.perf_counter() - started
info = observed._decoded_png.cache_info()
assert info.misses == 1 and info.hits == 10 and info.maxsize == 4
result = {'status': 'EXACT_BYTE_DECODE_CACHE_CHECKED', 'android_executed': False,
          'png_sha256': hashlib.sha256(data).hexdigest(), 'png_bytes': len(data),
          'image_size': list(direct[:2]), 'rgba_sha256': hashlib.sha256(direct[2]).hexdigest(),
          'one_uncached_decode_seconds': direct_seconds,
          'eleven_exact_same_byte_decodes_with_cache_seconds': cached_seconds,
          'cache_hits': info.hits, 'cache_misses': info.misses, 'max_entries': info.maxsize,
          'all_decoded_pixels_equal': True, 'artifact_checks_and_device_observations_cached': False,
          'device_freshness_budgets_changed': False, 'actual_hosted_capture_status': 'PENDING'}
(ROOT / 'reports/decode-cache-check.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
