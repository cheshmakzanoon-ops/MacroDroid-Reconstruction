#!/usr/bin/env python3
"""Freeze the closed incomplete DayTime13 replay without duplicating large inputs."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent
RESULT = BASE / 'daytime13-run-38221713675-analysis'
RAW = BASE / 'daytime13-run-38221713675-extracted'
OUT = BASE / 'checkpoints/06-daytime13-original-process-failure'


def identity(path):
    data = path.read_bytes()
    return {'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest()}


def link(source, name):
    assert source.is_file() and not source.is_symlink()
    expected = identity(source)
    target = OUT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    os.link(source, target)
    assert identity(target) == expected


def artifacts(value):
    if isinstance(value, dict):
        if set(value) == {'path','bytes','sha256'}:
            yield value
        for child in value.values():
            yield from artifacts(child)
    elif isinstance(value, list):
        for child in value:
            yield from artifacts(child)


def main():
    result = json.loads((RESULT / 'independent-daytime13-analysis.json').read_text())
    assert result['status'] == 'INCOMPLETE_DAYTIME13_REPLAYED_WITH_ORIGINAL_PROCESS_FAILURE'
    assert result['literal_evidence_valid'] is False and result['literal_comparison_status'] == 'REJECTED'
    assert result['original_recorded_screens'] == 5 and result['candidate_recorded_screens'] == 13
    assert result['five_available_rgba_pixel_vector'] == [0,0,0,0,0]
    assert (BASE / 'daytime13-replay-01.stderr.txt').read_bytes() == b''
    OUT.mkdir(parents=True, exist_ok=False)
    for source in sorted(RESULT.rglob('*')):
        if source.is_file():
            link(source, source.relative_to(RESULT))
    for name, source in {
        'freeze_daytime13_38221713675.py':Path(__file__).resolve(),
        'extract_artifact.py':BASE / 'extract_artifact.py',
        'replay.stdout.txt':BASE / 'daytime13-replay-01.stdout.txt',
        'replay.stderr.txt':BASE / 'daytime13-replay-01.stderr.txt',
        'original-extraction-receipt.json':BASE / 'daytime13-run-38221713675-extracted-extraction.json',
        'original-download-receipt.json':BASE / 'daytime13-run-38221713675.download.json',
    }.items():
        link(source, name)
    failure = json.loads((RESULT / 'original-process-failure-and-candidate-handoff.json').read_text())
    selected = {}
    for row in artifacts(failure):
        assert selected.setdefault(row['path'],row) == row
    boundary_path = RAW / 'journey/candidate-notification-boundary.json'
    boundary = json.loads(boundary_path.read_text())
    for row in artifacts(boundary):
        assert selected.setdefault(row['path'],row) == row
    for name, row in sorted(selected.items()):
        source = RAW / 'journey' / name
        assert identity(source) == {key:row[key] for key in ('bytes','sha256')}
        link(source, 'lifecycle/' + name)
    link(boundary_path, 'lifecycle/candidate-notification-boundary.json')
    pairs = json.loads((RESULT / 'five-available-full-frame-pairs-diagnostic-only.json').read_text())
    table = []
    for pair in pairs:
        old = pair['original']['artifacts']['screenshot']['path']
        new = pair['candidate']['artifacts']['screenshot']['path']
        table.append(f'| {pair["name"]} | 0 | Yes | [original](review-captures/{old}) / [candidate](review-captures/{new}) |')
    terminal = json.loads((RESULT / 'candidate-only-observed-exact-alarm-dialog.json').read_text())
    image = terminal['shot']['artifacts']['screenshot']['path']
    readme = '''# DayTime13: original process failure, incomplete comparison

The supplied original app stops during the promotion-screen capture after notification denial. It records five screens. The reconstruction records all thirteen declared screens and reaches an exact-alarm permission explanation. **The requested thirteen-screen comparison remains incomplete and rejected.**

This is [run 38221713675](https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/actions/runs/38221713675), job `114719291293`, at commit `e610d98812f3d26da732035e039a1250b8afe9f3`. The fixed original APK is SHA-256 `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`; the fixed reconstruction is SHA-256 `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`. These are the same two APK identities used for the earlier Zero12 comparison.

## Preserved actual failure

The exact hosted final verifier reports `DAY_TIME_TRIGGER_EVIDENCE_INCOMPLETE`, `evidence_valid=false`, with reason `ValueError: Configuration and complete journey are not in order`. The inner comparator reports `REJECTED`, with an empty accepted comparison list and reason `Incomplete run or changed environment`. The independent replay reproduces both objects, excluding only the new outer verifier timestamp. Its diagnostic checks do not replace either verdict.

The original's immediate pre-input PID is `3891`. The freshly verified notification-denial tap succeeds at 08:14:17.444 UTC. The next promotion acquisition calls `pidof com.arlosoft.macrodroid` at 08:14:19.475 UTC; it returns exit code 1 with empty stdout and stderr. The acquisition fails after approximately 0.063 seconds, before recording a full-frame attempt. It does not reach or exhaust the thirty-second frame-settling bound.

The original's pre-denial crash buffer is empty. The later crash-buffer command, retained before the candidate's notification denial, contains an actual main-thread fatal exception for original PID 3891 at 08:14:19.124 UTC: `IllegalStateException` from `Fragment.getResources`, reached through `com.zx.lbua80.onShow`. The exact original stack is classified using the unchanged pinned observer. This establishes the recorded original fatal and the subsequent absent-process observation. The original's restart or continuation is not observed by this run, and notification denial is not asserted to be the underlying cause.

The candidate also records a fatal exception at its notification boundary. Its existing strict handoff verifier checks the replacement PID, old-process absence, foreground component and freshly installed APK identity before continuation. Its raw boundary record is under [lifecycle](lifecycle/candidate-notification-boundary.json). The [failure and handoff report](original-process-failure-and-candidate-handoff.json) binds the exact commands, original failure ledger, later original crash buffer and candidate classification; the referenced raw outputs are preserved under `lifecycle/`. Neither app is described as crash-free.

## Five available pairs: diagnostic observations

The five full-screen pairs that exist in both runs are pixel-identical, with byte-identical hierarchy XML. This partial result does not substitute for the missing eight original screens.

| Available screen | Changed RGBA pixels | Exact XML bytes | Full unmodified screenshots |
| --- | ---: | --- | --- |
''' + '\n'.join(table) + '''

The [complete five-pair diagnostic](five-available-full-frame-pairs-diagnostic-only.json) records full PNG/XML identities and every measured pixel difference. The introduction indicator that differed by five pixels in the previous Zero12 run matches here. The older failure remains unchanged; these are separate actual runs, and the new equality does not establish the cause of the earlier difference.

## Candidate-only next surface

The last observed candidate surface is an app-owned `Permission Required` dialog over `AddTriggerActivity`. Its message states that MacroDroid needs permission to set exact alarms and asks for access on the next screen. The exact enabled buttons are `CANCEL` (`android:id/button2`) and `OK` (`android:id/button1`). The observed OK bounds are `[496,761][624,857]`, giving center `(560,809)` after a future fresh input guard.

The [terminal observation](candidate-only-observed-exact-alarm-dialog.json) preserves the literal XML node identities, component, raw artifacts and prior guarded Day/Time tap. [The full screenshot](review-captures/''' + image + ''') is unchanged. No input was made after this dialog. Exact-alarm permission was not granted and trigger configuration was not confirmed. There is no original counterpart to this screen in this run.

## Verification and preservation

The replay independently reconstructs all 224 input-copy roles from the exact pinned preparer. It verifies all 2,395 raw files before and after replay, all 717 recorded commands' referenced payloads, 37 capture ledgers, 1,927 unique referenced journey artifacts, and 35 accepted snapshot ledgers. Each accepted snapshot is rechecked with the original live-PID, stable-component, full PNG/XML equality and first-consecutive-pair requirements. The unchanged capture-event gate separately rejects the failed semantic/process acquisition, as required. No attempt is discarded, reclassified as a valid frame, or used to manufacture a complete original run.

The hosted guard logs contain 145 individual successes; the zero-animation helper has ten, and the downloader has six. The declared nineteen-command scale-zero configuration and all device command outputs are checked. The owned runtime cleanup succeeds while preserving the observation step's exit code 2. Complete source-origin hashes, host summaries, configuration data and replay logs accompany this report.

Artifact `11735470323` is exactly 38,451,864 bytes, SHA-256 `ad31af7b9fb237dbca1285a671a3e12fdcd9c3cd3754f55064055066043dffa4`. Its 2,395 unchanged members total 57,260,609 bytes. The parent publication preserves the complete original archive and extracted members. This capsule uses hardlinks for closed review payloads to avoid duplicate allocation; its content hashes are frozen and no linked file is edited afterward.

One emulator boot-log line contains ephemeral ADB public material. The raw ZIP and log remain unchanged. Only a separately labeled review-log copy omits that one value, with both hashes and the explicit transformation recorded. No raw value is repeated in this summary.

No APK, application source, workflow, historical result, runtime screenshot, or original archive is changed by this analysis. It establishes neither a complete thirteen-screen match nor full application 1:1 parity.
'''
    (OUT / 'README.md').write_text(readme)
    files = [{'path':path.relative_to(OUT).as_posix(), **identity(path)} for path in sorted(OUT.rglob('*')) if path.is_file()]
    checkpoint = {
        'schema':1, 'status':'FROZEN_INCOMPLETE_DAYTIME13_WITH_ORIGINAL_PROCESS_FAILURE',
        'created_utc':datetime.now(timezone.utc).isoformat(),
        'repo_target':'docs/verification/android-day-time-trigger-e610d98/analysis',
        'run_id':38221713675, 'head_sha':result['head_sha'], 'active_files':[],
        'raw_archive':result['archive'], 'original_raw_evidence_modified':False,
        'hardlinks_used_for_closed_review_files':True, 'files':files,
    }
    path = OUT / 'checkpoint.json'
    path.write_text(json.dumps(checkpoint,indent=2) + '\n')
    print(json.dumps({'checkpoint':str(path), **identity(path), 'files':len(files),
        'bytes_total':sum(row['bytes'] for row in files), 'repo_target':checkpoint['repo_target']},indent=2))


if __name__ == '__main__':
    main()
