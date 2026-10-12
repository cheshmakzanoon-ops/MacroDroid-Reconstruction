#!/usr/bin/env python3
"""Freeze the closed host-contract regression without activating its source."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE / 'reports/01-host-contract'
OUT = BASE / 'checkpoints/02-host-contract-regression'


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    result = json.loads((SOURCE / 'result.json').read_text())
    assert result['passed'] is True and result['encoding_files_byte_equal'] is True
    commands = json.loads((SOURCE / 'commands.json').read_text())
    assert len(commands) == result['commands'] == 9
    seen = set()
    for command in commands:
        for stream in ('stdout', 'stderr'):
            row = command[stream]
            assert row['path'] not in seen
            seen.add(row['path'])
            assert identity(SOURCE / row['path']) == {k: row[k] for k in ('bytes', 'sha256')}
    assert (SOURCE / 'baseline/contract.json').read_bytes() == (SOURCE / 'candidate/contract.json').read_bytes()
    OUT.mkdir(parents=True, exist_ok=False)
    for source in sorted(SOURCE.rglob('*')):
        if source.is_file():
            target = OUT / 'evidence' / source.relative_to(SOURCE)
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(source, target)
    for name, source in {'freeze_host_contract.py': Path(__file__),
                         'overlay-preparation.json': BASE / 'overlay-01/preparation.json',
                         'prepare_overlay.py': BASE / 'overlay-01/prepare_overlay.py'}.items():
        (OUT / name).write_bytes(source.read_bytes())
    (OUT / 'README.md').write_text('''# DayTrigger integration: existing VariableValue contracts

The isolated getter aliases pass the measured host-contract regression. The baseline and candidate produce byte-identical complete encoding reports, SHA256 `b5d5f4f17925397e9f2c7523907599af43ee20f5bfe7c499db4b6d0b578b1a2d`.

This follow-up implements only the host-field portion of the [approved 19-path design](../03-integration-design/README.md). The active repository remains unchanged. It does not claim completion of numeric-method integration or a new APK.

The original host source is `5953b3925539d215d3f32546d97280ed4403feeb5907909236ced0c5267831a1`; the isolated candidate is `f8804d5188c8d7c7594e9372cf94aace7336a04b038078664275befae1b532e9`. Both exact sources and their actual compiled classes are retained under [evidence](evidence/result.json). The new `variable`, `intValue` and `decimalValue` aliases are private, final and transient. Existing public final fields, constructors and entry identity equality remain.

## Executed checks

The closed run lasted from 08:05:27.990926 to 08:05:47.448674 UTC on 2026-10-12. Nine bounded commands compile the three unchanged legacy/core/UI test encoders and one integration probe, compile four separate field-container variants, and execute each with `-Xverify:all`. The [command ledger](evidence/commands.json) retains every argument, time, return code and exact stdout/stderr hash.

The baseline and candidate each encode 28 values through five existing encoding routes: `ParityTests.canon`, `CoreParityTests.canon`, `UiParityTests.canonical`, default Gson and Gson with null serialization. A containing `s0` record adds the 141st encoding observation. Cases include nested entries/dictionaries, nulls, strings, booleans, signed integer limits, negative zero, subnormal values, infinities and distinct NaN payloads. Existing Gson rejections of non-finite values retain their actual class/message and compare unchanged.

The existing event-bus recorder executes with the same variable record and entry. Its complete trace is retained and equal. Nine explicit public-field/constructor/identity conditions pass; public fields and constructor descriptors also compare exactly. The candidate separately passes 21 alias modifier, reference identity and raw numeric-bit checks. These checks establish host-boundary compatibility, not Android variable construction, parceling or runtime behavior.

Two measured negative controls show that the regression detects the relevant errors. Removing `transient` changes the complete serialization result. Changing only `intValue` to `v + 1` retains the legacy encoding but fails the alias-value assertion. Both faulty sources and actual compiled classes/logs remain preserved.

All 912 existing read-only classpath files and the unchanged encoder sources were rehashed after execution. No active source, original APK, test fixture or build cache was modified. The numeric registry/fixture/case/control integration is still pending at this checkpoint.
''')
    files = [{'path': p.relative_to(OUT).as_posix(), **identity(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
    manifest = {'schema': 1, 'status': 'FROZEN_DAY_HOST_CONTRACT_REGRESSION_PASSED',
                'created_utc': datetime.now(timezone.utc).isoformat(),
                'repo_target': 'work-in-progress/day-trigger-numeric/04-host-contract-regression',
                'active_files': [], 'files': files}
    (OUT / 'checkpoint.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
                      'files': len(files), 'bytes_total': sum(r['bytes'] for r in files),
                      'repo_target': manifest['repo_target']}, indent=2))


if __name__ == '__main__':
    main()
