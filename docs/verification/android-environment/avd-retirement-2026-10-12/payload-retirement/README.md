# Generated AVD payload retirement after exact reappearance

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
