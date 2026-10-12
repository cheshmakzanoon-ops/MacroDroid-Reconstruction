"""Freeze existing AVD reappearance and payload retirement records; no device writes."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
REAPPEARED = HERE.parent / 'avd-reappearance-2026-10-12'


def meta(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def freeze(folder, path, status):
    files = [{'path': p.relative_to(folder).as_posix(), **meta(p)}
             for p in sorted(folder.rglob('*')) if p.is_file() and p.name != 'checkpoint.json']
    value = {'schema': 1, 'status': status, 'publication_path': path, 'active_files': [],
             'files': files, 'file_count': len(files), 'total_bytes': sum(row['bytes'] for row in files),
             'new_android_execution_performed': False, 'point_in_time_observations_only': True}
    target = folder / 'checkpoint.json'
    with target.open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'checkpoint': str(target), **meta(target), 'file_count': len(files),
                      'total_bytes': value['total_bytes']}))


def main():
    assert not (HERE / 'checkpoint.json').exists() and not (REAPPEARED / 'checkpoint.json').exists()
    observed = json.loads((REAPPEARED / 'reappearance.json').read_bytes())
    assert observed['target_exists'] and observed['regular_file_inventory_matches_prior_retired_payloads']
    assert observed['observed_file_count'] == 23 and observed['deletion_or_write_performed'] is False
    receipt = json.loads((HERE / 'receipt.json').read_bytes())
    followup = json.loads((HERE / 'followup-and-repeat-guard.json').read_bytes())
    assert meta(HERE / 'receipt.json')['sha256'] == '848d2b8049cf4719e18d7e82a349f62ec03e6b056466f0073ae8c6df54dc1d34'
    assert meta(REAPPEARED / 'reappearance.json')['sha256'] == receipt['prior_reappearance_report_sha256']
    assert receipt['status'] == 'FIVE_GENERATED_AVD_PAYLOADS_RETIRED_TO_EMPTY_PLACEHOLDERS'
    assert receipt['retained_avd_regular_files'] == 18 and receipt['protected_control_files'] == 22
    assert meta(HERE / 'retained-controls-before.json') == meta(HERE / 'retained-controls-after.json')
    assert followup['receipt_sha256_before'] == followup['receipt_sha256_after'] == meta(HERE / 'receipt.json')['sha256']
    assert followup['repeat_invocation_exit_code'] == 1 and followup['actual_retirement_repeated'] is False
    assert meta(HERE / 'executed-source/retire_payloads.py')['sha256'] == followup['executed_retirement_source_sha256']
    assert meta(HERE / 'retire_payloads.py')['sha256'] == followup['future_driver_sha256']
    originals = {row['path']: row for row in observed['files'] if 'sha256' in row}
    assert len(originals) == 23 and len(receipt['replaced']) == 5
    empty = hashlib.sha256(b'').hexdigest()
    for row in receipt['replaced']:
        assert all(row['original'][key] == originals[row['path']][key] for key in ('bytes', 'sha256'))
        assert row['after']['bytes'] == row['after']['allocated_bytes'] == 0
        assert row['after']['sha256'] == empty
    for row in followup['later_payload_observations']:
        assert row['bytes'] == row['allocated_bytes'] == 0 and row['sha256'] == empty
    (REAPPEARED / 'README.md').write_text('''# Point-in-time AVD reappearance

The original closed disposable AVD removal succeeded at its recorded observation. A later read-only inventory at **2026-10-12 06:01:01.373677 UTC** found the same path present again, with all **23 regular files matching the previously retired sizes and SHA-256 hashes**. It occupied 921,440,256 allocated bytes at this later observation; free space was 250,372,096 bytes. Sparse allocation can differ even when file content matches.

`reappearance.json` preserves all thirty directory/file entries, the original inventory hash, the exact path and sibling-name observation, and physical `/proc/self` PID 94272 separately from namespace PID 5. This probe did not delete or write the AVD. It shows that the earlier absence was not persistent; it does not alter the earlier successful point-in-time receipt or infer an unobserved exact restoration time.

The original removal and its explicit process-visibility correction are retained in the parent evidence directory and were published in commit `dfa130a90a271ad591dcdb86ec34ac4b6de8ddfb`. The authorized subsequent payload-only retirement is recorded separately under `../payload-retirement/`. No installation binaries, APKs, source, or capture evidence is contained in or changed by this follow-up.
''')
    (HERE / 'README.md').write_text('''# Generated AVD payload retirement after exact reappearance

After the separate read-only reappearance inventory found the retired disposable AVD files restored, root authorized a bounded fallback: atomically replace only the five previously inventoried and hash-matching **large generated disk payloads** with empty files while retaining their paths and modes. No installed SDK/JDK, pinned installer, source, APK, report, service, permission, or namespace setting was changed.

## Actual observed operation

The retirement ran from **2026-10-12 06:07:25.622479 to 06:07:54.690775 UTC** and completed successfully. Both process guards enumerate physical `/proc` entries and record the physical reader PID separately from its namespace PID. No emulator or QEMU executable was observed. Other-process cwd/fd/exe visibility may be denied; the bounded guard also binds the already preserved runtime stop and framework watchdog evidence. It does not claim unrestricted process visibility or modify permissions.

Every one of the 23 original regular AVD files was checked against the recorded content inventory before the operation. Exactly these five payloads were replaced:

| Generated payload | Original logical bytes |
| --- | ---: |
| `cache.img` | 69,206,016 |
| `encryptionkey.img` | 18,874,368 |
| `encryptionkey.img.qcow2` | 2,097,152 |
| `userdata-qemu.img` | 6,356,992 |
| `userdata-qemu.img.qcow2` | 822,345,728 |

All five replacement files have zero length, zero allocated blocks and the empty-file SHA-256. The 18 remaining AVD files, including small configuration, log, pstore and modem metadata, initrd and smaller cache overlay, retain their recorded hashes. All 22 retained outside controls—including pinned installers, usable JDK/SDK executables, APK/source and earlier evidence—match their before-operation hashes. Raw before/after inventories, exact process guards and the receipt are preserved.

Free space changed from 1,211,613,184 to 2,027,208,704 bytes during the operation. The observed increase is 815,595,520 bytes; other work was running, so it is not asserted to equal the sum of payload allocation. A separate observation at **06:10:03.680119 UTC** confirms the same five zero-byte/zero-block placeholders and 2,021,642,240 free bytes. These are point-in-time observations, not a guarantee against later workspace restoration. The disposable AVD must be recreated from the retained pinned inputs before any future boot; its retired disk payloads are not usable runtime state.

## Exact executed source and repeat guard follow-up

`executed-source/retire_payloads.py` is the exact driver that performed the successful retirement, bound by SHA-256 in `followup-and-repeat-guard.json`. After execution, review found that its refusal to overwrite an existing receipt was inside a `try/finally` that could itself rewrite that receipt on an accidental repeat invocation. The separately retained current `retire_payloads.py` moves that guard before the receipt-writing block. The original executed source and actual receipt remain unchanged.

A bounded repeat-invocation rejection control of the corrected future driver exits 1 before any retirement action, with the receipt hash unchanged before and after. Both stdout/stderr are preserved. The real retirement was not repeated. This small driver correction is distinguished explicitly from the code that performed the recorded operation.

`freeze_followups.py` verifies and freezes the already written reappearance and retirement evidence. It performs no device, payload or installed-tool mutation. The earlier removal, visibility limitation and later reappearance remain separate historical evidence; none is rewritten as persistent absence or a new Android acceptance result.
''')
    prefix = 'docs/verification/android-environment/avd-retirement-2026-10-12/'
    freeze(REAPPEARED, prefix + 'reappearance', 'FROZEN_EXACT_AVD_REAPPEARANCE_OBSERVATION')
    freeze(HERE, prefix + 'payload-retirement', 'FROZEN_GENERATED_AVD_PAYLOAD_RETIREMENT_RECEIPT')


if __name__ == '__main__':
    main()
