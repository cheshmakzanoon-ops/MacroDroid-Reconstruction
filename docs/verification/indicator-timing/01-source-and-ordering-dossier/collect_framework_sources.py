#!/usr/bin/env python3
"""Retain public Android 15 source for a scheduling hypothesis, not device proof."""
from pathlib import Path
import base64
import concurrent.futures
import datetime
import hashlib
import json
import time
import urllib.request

OUT = Path(__file__).resolve().parent / 'reports/02-public-framework-sources'
NAMES = ('ValueAnimator.java', 'AnimationHandler.java')
ROOT = 'https://android.googlesource.com/platform/frameworks/base/+/android-15.0.0_r1/core/java/android/animation/'


def fetch(name):
    url = ROOT + name + '?format=TEXT'
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(url, timeout=25) as response:
            if response.status != 200 or response.geturl() != url:
                raise AssertionError('Unexpected source URL/status')
            raw = response.read(2 * 1024 * 1024)
        decoded = base64.b64decode(raw, validate=True)
        if not decoded.startswith(b'/*\n') or b'package android.animation;' not in decoded:
            raise AssertionError('Unexpected source payload')
        if name == 'ValueAnimator.java':
            assert hashlib.sha256(raw).hexdigest() == 'd2ad9517ded9574e0c0b278b82ed490afcbc0b239e149db7303be018e2f20dd1'
        (OUT / (name + '.base64')).write_bytes(raw)
        (OUT / name).write_bytes(decoded)
        return {'name': name, 'url': url, 'started_utc': started,
                'elapsed_seconds': time.monotonic() - t0, 'status': 'SOURCE_RETRIEVED',
                'response_bytes': len(raw), 'response_sha256': hashlib.sha256(raw).hexdigest(),
                'decoded_bytes': len(decoded), 'decoded_sha256': hashlib.sha256(decoded).hexdigest(),
                'actual_device_framework_bytes_verified': False}
    except Exception as exc:
        return {'name': name, 'url': url, 'started_utc': started,
                'elapsed_seconds': time.monotonic() - t0, 'status': 'SOURCE_RETRIEVAL_FAILED',
                'error_type': type(exc).__name__, 'error_message': str(exc)}


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=False)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(fetch, NAMES))
    report = {'scope': 'Android 15 public tag only; captured emulator framework identity is different and unverified',
              'sources': rows}
    (OUT / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, sort_keys=True))
    raise SystemExit(0 if all(r['status'] == 'SOURCE_RETRIEVED' for r in rows) else 1)
