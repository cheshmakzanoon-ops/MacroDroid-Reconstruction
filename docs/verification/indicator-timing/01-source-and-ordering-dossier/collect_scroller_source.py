#!/usr/bin/env python3
"""Public source corroboration; does not bind the captured device's framework."""
from pathlib import Path
import base64
import datetime
import hashlib
import json
import time
import urllib.request

OUT = Path(__file__).resolve().parent / 'reports/04-public-scroller-source'
URL = 'https://android.googlesource.com/platform/frameworks/base/+/android-15.0.0_r1/core/java/android/widget/Scroller.java?format=TEXT'

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=False)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(URL, timeout=25) as response:
            assert response.status == 200 and response.geturl() == URL
            raw = response.read(2 * 1024 * 1024)
        data = base64.b64decode(raw, validate=True)
        assert data.startswith(b'/*\n') and b'package android.widget;' in data
        (OUT / 'Scroller.java.base64').write_bytes(raw)
        (OUT / 'Scroller.java').write_bytes(data)
        result = {'status': 'PUBLIC_SOURCE_RETRIEVED', 'url': URL, 'started_utc': started,
                  'elapsed_seconds': time.monotonic() - t0,
                  'raw_bytes': len(raw), 'raw_sha256': hashlib.sha256(raw).hexdigest(),
                  'source_bytes': len(data), 'source_sha256': hashlib.sha256(data).hexdigest(),
                  'actual_device_framework_bytes_verified': False}
    except Exception as exc:
        result = {'status': 'PUBLIC_SOURCE_RETRIEVAL_FAILED', 'url': URL,
                  'started_utc': started, 'elapsed_seconds': time.monotonic() - t0,
                  'error_type': type(exc).__name__, 'error_message': str(exc)}
    (OUT / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result['status'] == 'PUBLIC_SOURCE_RETRIEVED' else 1)
