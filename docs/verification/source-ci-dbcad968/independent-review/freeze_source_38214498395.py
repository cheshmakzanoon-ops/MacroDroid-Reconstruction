#!/usr/bin/env python3
"""Freeze the compact independent source-CI review without reopening its ZIP."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

BASE = Path(__file__).resolve().parent
RESULT = BASE / 'source-run-38214498395-independent-review'
OUT = BASE / 'checkpoints/04-dbcad-source-independent-review'


def identity(path):
    raw = path.read_bytes()
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def main():
    report = json.loads((RESULT / 'independent-source-review.json').read_text())
    assert report['status'] == 'HOSTED_SOURCE_JOB_ALL_16_GATES_AND_EXACT_CANDIDATE_VERIFIED'
    OUT.mkdir(parents=True,exist_ok=False)
    copies = {p.relative_to(RESULT).as_posix():p for p in RESULT.rglob('*') if p.is_file()}
    copies.update({'freeze_source_38214498395.py':Path(__file__).resolve(),
                   'review.stdout.log':BASE/'source-38214498395-review.stdout.log',
                   'github-final-dbcad-source-and-zero12.json':BASE/'github-final-dbcad-source-and-zero12.json'})
    for relative,source in copies.items():
        assert not source.is_symlink()
        target = OUT / relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target)
        assert identity(source)==identity(target)
    latest=json.loads((OUT/'compact-evidence/reports/acceptance-latest.json').read_text())
    table=[]
    for gate in latest['commands']:
        table.append(f'| {gate["label"]} | 0 | {gate["seconds"]:.3f} | {gate["timeout_seconds"]} | [actual log](compact-evidence/{gate["log"]}) |')
    (OUT/'README.md').write_text('''# Independent review of the dbcad source-build job

The exact hosted source artifact passes this closed evidence review. **All sixteen configured host gates passed, and the freshly built hybrid APK has the exact committed candidate identity.** This is a source-build and bounded host-verification result. The separate Android job at the same workflow run retains its intro pixel failure.

Source job `114695960566` belongs to [run 38214498395](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38214498395), commit `dbcad968c5c3e8f084205393a6c0d2d06a203c71`. Its acceptance starts at 06:51:46.140289 UTC and finishes at 07:13:55.222515 UTC on 2026-10-12. The latest result is byte-identical to its uniquely dated result file. The independent review checks all sixteen corresponding log SHA256 values and actual exit codes, plus all twenty-two fresh report bindings.

## Actual gate results

| Gate | Exit code | Seconds | Timeout budget | Evidence |
| --- | ---: | ---: | ---: | --- |
'''+ '\n'.join(table)+'''

The larger UI control budget is confined to that one gate. Its actual completion took 725.704 seconds, below its 5,400-second limit. All other gate limits remain 1,200 seconds. The signed-source-edit experiment was actually run; it was not skipped.

## Source and APK identities

The complete input manifest has 81,291 entries and snapshot SHA256 `b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`. This review recomputed the canonical ordered-entry digest and compared the entire 14,502,990-byte manifest with the exact `project/reports/release-input-snapshot.json` Git blob at the tested commit. The bytes match. The host result reports that the before/after build inputs are unchanged. This review does not claim an additional remote source-filesystem rehash; it checks the complete preserved inventory and its immutable source binding.

The archive's APK members were read and SHA256-hashed as streams, without extracting another APK copy:

| APK | Bytes | SHA256 |
| --- | ---: | --- |
| Fresh baseline | 94,677,674 | `aa8ad3013ad211c8a39d083943b0a671d75e0bbbedccc924ea0093c590c9a096` |
| Fresh hybrid | 94,683,119 | `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182` |

Both identities match the acceptance result and their actual build reports. The hybrid also matches the exact committed candidate manifest. The hosted candidate-versus-fresh-build comparison step succeeded independently of this replay.

## Host semantics and retained controls

The recorded three-path result contains 193,489 cases, 1,242 covered/expected methods, zero failed cases and zero unsupported executions. Its suites contain 95,262 legacy, 34,753 core, 30,684 environment, 9,616 engine and 23,174 UI cases. The result verifies the exact method-key partition and binds the rebuilt DEX comparison to the same hybrid APK and fixture identity.

All 78 UI mutation controls report the required rejection with zero unsupported executions. This review checks the SHA256 of every retained mutant Java source and compiled class against its individual report, confirms that each mutant class differs from its positive class, and checks the source/fixture/APK preservation fields. The complete restored UI result object equals the complete positive baseline object, including its cases and coverage, with all 23,174 UI cases passing. The [78 individual checks](all-78-retained-mutant-checks.json) and [original control report](compact-evidence/reports/ui-negative-controls.json) retain those bindings.

The actual Python regression log contains 273 individual successes and a matching `Ran 273 tests in 6.611s` summary. The exact Git-bound `test.py` invokes that suite as part of the positive host commands. The copied acceptance runner, test runner, release-integrity code and workflow explain the actual orchestration. The Java staging receipt is retained with the compact proof; no new compiler invocation or broader test suite was performed by this review.

## Complete archive preservation and scope

The original source artifact is 188,134,390 bytes, SHA256 `da5668cb030718c72a557179b3d38e33769531d497ec5e16d0a45ea2c8f53d88`, artifact ID `11731218792`. All 1,136 archive members, totaling 450,752,098 uncompressed bytes, were independently streamed and checked, with CRC and SHA256 metadata in the [complete inventory](all-1136-member-identities.json). The archive also retains historical reports; this review selects the actual dated acceptance result and its fresh bindings rather than mistaking older evidence for the current run.

Only compact current reports and gate logs were copied into this review. The two APK members, large resource tables and full duplicate report tree were not expanded. The immutable original container is preserved by the repository publisher under the parent evidence directory. After successful verification, this reviewer closed all ZIP readers and required no further source-archive reads, allowing the separately authorized disk-aware publication and retirement procedure.

The source job's availability probe reports `BLOCKED` and `android_runtime_executed=false`; that probe is not an Android acceptance test. The parallel Android job has its own actual evidence and failure. No full runtime 1:1, complete high-level Java/Kotlin source, animation parity or general feature parity is inferred from these host results.

The [independent result](independent-source-review.json), [actual review log](review.stdout.log), exact [source pins](source-commit-pins.json), [twenty-two fresh-report checks](all-22-fresh-evidence-checks.json), reviewer and freezer preserve this closed review. The raw ZIP and application inputs were not modified.
''')
    files=[{'path':p.relative_to(OUT).as_posix(),**identity(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
    checkpoint={'schema':1,'status':'FROZEN_INDEPENDENT_SOURCE_CI_ALL16_REVIEW',
                'created_utc':datetime.now(timezone.utc).isoformat(),
                'repo_target':'docs/verification/source-ci-dbcad968/independent-review',
                'run_id':38214498395,'source_job_id':114695960566,'active_files':[],'files':files}
    (OUT/'checkpoint.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
    print(json.dumps({'checkpoint':str(OUT/'checkpoint.json'),**identity(OUT/'checkpoint.json'),
                      'files':len(files),'bytes_total':sum(r['bytes'] for r in files),
                      'repo_target':checkpoint['repo_target']},indent=2))


if __name__=='__main__':
    main()
