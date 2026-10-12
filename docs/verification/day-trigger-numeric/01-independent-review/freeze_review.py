#!/usr/bin/env python3
"""Freeze the closed independent DayTrigger review as an additive evidence capsule."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE / 'reports/01-closed-capsules'
OUT = BASE / 'checkpoints/01-independent-numeric-review'


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    report = json.loads((SOURCE / 'result.json').read_text())
    assert report['status'] == 'INDEPENDENT_DAY_NUMERIC_CAPSULE_REVIEW_PASSED' and report['passed']
    OUT.mkdir(parents=True, exist_ok=False)
    selected = {p.relative_to(SOURCE).as_posix(): p for p in SOURCE.rglob('*') if p.is_file()}
    selected.update({'review.stdout.log': BASE / 'review-01.stdout.log', 'freeze_review.py': Path(__file__).resolve()})
    for relative, source in selected.items():
        assert source.is_file() and not source.is_symlink()
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        os.link(source, target)
        assert identity(source) == identity(target)
    controls = json.loads((SOURCE / 'all-17-compiled-and-provenance-controls.json').read_text())
    table = '\n'.join(f'| {r["name"]} | {r["kind"]} | {r.get("mismatch_count", "Rejected before report")} |'
                      for r in controls)
    (OUT / 'README.md').write_text('''# Independent review: DayTrigger numeric value recovery

**The two frozen numeric-method studies pass this independent evidence and arithmetic review. No blocking error was found in the recovered body, original getter scope, or production method transplant.** The method remains an inactive proposal at the time of review. No APK was built or modified, and no Android or ART execution was performed by this review.

The reviewed method is `DayTrigger.r0(VariableValue.DictionaryEntry)I`. Its narrow behavior is to read the entry's contained value, narrow a stored integer or decimal to an integer, and return zero for other contained types. A null entry raises a null-pointer exception; a non-null entry containing null returns zero. This is not a review of calendar selection, alarms, time zones, scheduling, persistence, or Android lifecycle behavior.

## Immutable proof bindings

| Frozen study | Checkpoint SHA256 | Source files checked | Archive members checked |
| --- | --- | ---: | ---: |
| [Original/JVM study](../../../../work-in-progress/day-trigger-numeric/01-original-java-proof/checkpoint.json) | `6c78e9a5498e516f4a2b6f939055151fa2ab1d5585e12b77a4c991534593da0e` | 19 | 47 |
| [Three-path and compiled controls](../../../../work-in-progress/day-trigger-numeric/02-three-path-and-compiled-controls/checkpoint.json) | `d93f08507afce1b6eebe1e3ae64338f86eb04ca01e26118bdd97f98f5d6af631` | 20 | 174 |

Every source identity and every archive member was independently checked against its frozen manifest. The second capsule embeds the exact first checkpoint. The recorded seven original-study commands and 41 three-path/control commands have distinct preserved output paths, matching hashes, completed return codes, bounded timeouts and ordered timestamps. Both positive reports are restored byte for byte. The original capsules and their archives are unchanged.

The closed independent review ran on 2026-10-12 from 07:46:34.839393 to 07:46:51.111837 UTC. Its [result](result.json), [executed reviewer](executed-review.py), [actual log](review.stdout.log), complete source/member inventories and command ledgers accompany this README.

## Independent numeric expectations

The reviewer recomputed every expected value from the recorded raw input bits using Python integer operations. For integer values it keeps the low 32 bits and interprets the sign bit. For binary64 decimals it decomposes the sign, exponent and significand, removes fractional bits by shifting, and explicitly handles NaN, infinities and the signed 32-bit range. It uses neither the recovered Java casts nor the study's BigDecimal calculation.

These expectations follow the [Java Language Specification, section 5.1.3](https://docs.oracle.com/javase/specs/jls/se21/html/jls-5.html#jls-5.1.3): integer narrowing keeps the low destination-width bits; floating-point narrowing truncates toward zero, maps NaN to zero, and saturates values outside the destination range. The arithmetic reviewer is separate from the original-instruction and rebuilt-instruction interpreter, whose cast implementations necessarily follow Java conversion behavior.

All 1,291 recorded cases agree across the original instructions, compiled Java helper and rebuilt instructions:

| Input category | Cases |
| --- | ---: |
| Integer boundaries, bit patterns and seeded values | 547 |
| Decimal boundaries, neighboring values, special IEEE-754 patterns and seeded bits | 734 |
| Null entry | 1 |
| Contained null | 1 |
| Strings | 4 |
| Booleans | 2 |
| Dictionary | 1 |
| Nested dictionary entry | 1 |

The [1,291 individual checks](all-1291-integer-only-expectation-checks.json) retain each input's raw bits and independently computed result. The two studies have the exact same ordered case identities and original/Java outcomes. The comparison of the null-entry case is deliberately limited to the required `NullPointerException` class; raw exception messages remain in the original reports. All other outcomes compare the complete observed record. No message equality or broader exception equivalence is inferred for the null-entry case.

## Direct original-APK extraction and getter scope

The original APK is SHA256 `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`. The reviewer freshly compiles only the small, frozen `ExtractDayFixture.java`; the resulting class is byte-identical to the archived extractor class. Running it with `-Xverify:all` directly against that pinned APK reproduces both the fixture and its method inventory byte for byte. The fixture is 7,528 bytes, SHA256 `26ff2b80887ee3c7ca8ebe55b94f458f388f2f3ce2b0542510304f3272015840`. The [two actual command records](independent-command-ledger.json), exact class, output DEX and [inventory](direct-original-apk-check/original-method-inventory.json) are retained.

All four original methods come from `classes3.dex`: the primary method plus `DictionaryEntry.getVariable()`, `IntegerValue.getIntValue()` and `DecimalValue.getDecimalValue()`. The interpreter executes those original getter instructions against small host field containers. The host constructors and unselected methods are test support; Android constructors, parceling and other variable behavior are outside the study.

The complete original path executes 32 instructions: 25 in the recovered target and seven in the three dependencies. The rebuilt path executes 25 instructions: 18 in the recovered target plus the same seven original getter instructions. Both paths execute all four conditional edges. The direct original inventory exactly matches the recorded required offsets, with no excluded instructions or exception regions.

## Production transplant and actual faults

The reviewer imports the frozen, hash-checked production `build.py` and `constructor_owner.py`, which match the active project byte for byte. It recomputes class relocation, the sole-class compiler-input JAR binding, constructor-owner analysis, annotation handling and exact target-method replacement for the positive helper and both actual rebuilt-bytecode faults. Each replacement preserves all 33 other original methods and every part of the class outside the replaced method. No constructor correction is needed. The D8 commands use the production release/no-desugaring/minimum-API-23 arguments; no host stub enters any of the three compiler-input JARs. Both helper and target DEX headers, signatures, checksums and SHA256 identities are independently checked.

The positive target DEX remains SHA256 `867e137f65908d8360f307cdd0f23b3f910e5606d6b5916f876e85186b813b47`. The [three reconstructed transplant checks](all-three-production-transplant-checks.json) retain every binding.

All actual faults and provenance controls reproduce their recorded rejection. For each Java fault, the reviewer checks the exact unique source replacement, changed compiled-class identity, complete ordered case inventory, named failing case, and unchanged original/rebuilt outcomes. For each rebuilt-DEX fault, the original and Java outcomes remain unchanged. None relies on an unsupported instruction.

| Control | Mechanism | Mismatching cases or rejection |
| --- | --- | ---: |
''' + table + '''

The [17 individual control checks](all-17-compiled-and-provenance-controls.json) and complete original result retain the precise scopes and identities. This review rechecks the closed control evidence; it does not claim a second execution of all 41 recorded commands.

## Integration boundary

The frozen study uses `BytecodeOracle.java` SHA256 `38f60a2ce6f30da923b2fd6a0c1824ba668e7ca8e63a2da72032dcd0b2953a80`, while the active project uses `d91ddcd8ec3d67d41d69b8252835e747c2cad2c6d5ea898323794ceec30e6b56`. The entire [source difference](frozen-to-active-oracle.patch) was reviewed. The active additions provide constructor-owner validation/adapters and `AND_INT`; none of those opcode paths occurs in the selected original methods or recovered numeric helper. This is not an instruction to replace the active oracle. Integration should retain it and run the combined registered-method checks after adding the new method and its scoped fixtures/cases.

The active registry had no entry for this target method at review time. This independent receipt approves the closed one-method host/interpreter proof, subject to normal integration validation. It establishes neither Android numeric execution nor Day/Time scheduling, full application parity, or a new production release. All selected source, original APK, toolchain, JDK and archive hashes were unchanged at closure.
''')
    files = [{'path': p.relative_to(OUT).as_posix(), **identity(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
    manifest = {'schema': 1, 'status': 'FROZEN_INDEPENDENT_DAY_NUMERIC_REVIEW',
                'created_utc': datetime.now(timezone.utc).isoformat(),
                'repo_target': 'docs/verification/day-trigger-numeric/01-independent-review',
                'active_files': [], 'files': files}
    (OUT / 'checkpoint.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **identity(OUT / 'checkpoint.json'),
                      'files': len(files), 'bytes_total': sum(r['bytes'] for r in files),
                      'repo_target': manifest['repo_target']}, indent=2))


if __name__ == '__main__':
    main()
