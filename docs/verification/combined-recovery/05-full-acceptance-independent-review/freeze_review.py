"""Freeze only the completed independent coherence review and its source."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
STUDY = ROOT / '01-closed-capsule'
OUT = ROOT / 'checkpoints/01-independent-full-acceptance-review'


def meta(path):
    return {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    result = json.loads((STUDY / 'review-result.json').read_bytes())
    assert result['passed'] is True and result['status'] == 'INDEPENDENT_COMBINED05_COHERENCE_REVIEW_PASSED'
    assert (result['capsule_files_verified'], result['archive_members_verified'], result['fresh_report_hashes_verified'],
            result['gate_logs_verified'], result['retained_mutant_source_class_pairs_verified']) == (125, 551, 22, 16, 78)
    assert result['current_baseline_input_files_rehashed'] == 81245 and result['closed_candidate_input_files_rehashed'] == 81291
    OUT.mkdir(parents=True, exist_ok=False)
    for source in sorted(STUDY.iterdir()):
        assert source.is_file()
        shutil.copyfile(source, OUT / source.name)
        assert meta(source) == meta(OUT / source.name)
    for name in ('review_closed_combined.py', '01-review-driver.log', 'freeze_review.py'):
        shutil.copyfile(ROOT / name, OUT / name)
        assert meta(ROOT / name) == meta(OUT / name)
    (OUT / 'README.md').write_text('''# Independent review of combined05 full acceptance

The closed combined source/APK capsule passed an independent read-only coherence review. The reviewed capsule is `work-in-progress/combined-recovery/05-full-acceptance/checkpoint.json`, SHA-256 `e4cd0b6af4cf95d7131138b3ad3dab8a070042cea077a80cf83c322168457063`; its prepared source is bound to reviewed checkpoint04 `da0a1a8944e24f2d559083ac7232634be257756a5073ea1755eb5006761191e6`.

**Verdict: approved as scoped closed host, source and APK evidence.** This review ran no build, test suite, APK or Android command and changed no active source, artifact or generated cache. Android acceptance for this particular combined APK remains pending. The prior normal-animation diagnostic uses its separately reviewed 9108 candidate and is not evidence for this new APK.

## Independently checked evidence

| Evidence | Actual verification |
| --- | --- |
| Combined capsule | All 125 declared files, with exact complete path inventory, lengths and SHA-256 hashes |
| Reviewed preparation | All 90 declared checkpoint04 files and the identical archived full input manifest |
| Complete reports archive | All 551 unique regular members, paths, lengths and hashes, streamed without extraction |
| Acceptance outputs | All 22 fresh-report hashes and all sixteen ordered gate logs, each bound to both the readable copy and archive |
| UI negative controls | All 78 retained Java source/class pairs and actual required failed-case labels, with zero unsupported executions and unchanged original method, case and instruction inventories |
| Positive restoration | Complete parsed positive UI report equals the original positive baseline object |
| Python result | All 273 individual success lines and the final 273-test success summary, 17.639 seconds |
| Three-path host result | 193,489 cases over all 1,242 registered bodies, three paths, zero failed or unsupported executions |
| Candidate APK | All twelve ordered part SHA-256 and Git blob SHA1 identities, streamed into the exact aggregate digest; both closed dist APKs also rehashed |

The candidate is exactly **94,683,119 bytes**, SHA-256 `5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`. Its source input pin is `b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`. No APK payload, report archive, private signing material, or large source tree is duplicated in this review capsule; their immutable paths and hashes are bound by the review results.

## Complete source coherence

The full current baseline input inventory was independently enumerated and rehashed: **81,245 files / 819,399,298 bytes**, canonical pin `19ea47f8563262c255b1d11632bfc404eb68819f332ececdf68d0a686643c183`. The closed candidate was independently enumerated and rehashed: **81,291 files / 819,562,916 bytes**, canonical pin `b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`. Missing or extra pinned-source inputs would reject the review; these are full inventories, not samples.

The exact source delta is **46 additions, 17 changes and zero removals**, totaling 63 files. Every changed file equals its reviewed checkpoint04 source and its candidate manifest entry, while every old/absent file matches the current and repository baseline. Replacing only those 63 entries in the full baseline manifest reconstructs the complete candidate manifest and canonical pin exactly. The 1,240 old registered entries remain unchanged; the only appended bodies are the reviewed plugin-upload `k.invokeSuspend` and Widget update method, yielding 1,242 bodies in 605 classes and ten UI methods.

## Scope and reproduction

`review_closed_combined.py` is the exact independent reviewer source and `01-review-driver.log` is its actual output. The eight JSON receipts preserve complete per-member, fresh-report, gate, mutant, APK-part and delta checks along with full source-rehash timings and the final verdict. It was executed from 06:34:07.691305 to 06:36:58.681825 UTC on 2026-10-12. Its input capsules and project locations remain explicitly bound; replay requires those unchanged source and evidence inputs.

This review confirms evidence coherence and the measured finite host result. It does not establish complete Java/Kotlin recovery, startup or lifecycle parity, animation parity, native behavior, absence of crashes, or whole-application 1:1. The retained historical runtime failures and 26-pixel TRIGGERS difference are unchanged. Existing raw evidence is not normalized or relabeled.
''')
    files = [{'path': path.relative_to(OUT).as_posix(), **meta(path)}
             for path in sorted(OUT.rglob('*')) if path.is_file()]
    checkpoint = {'schema': 1, 'status': 'FROZEN_INDEPENDENT_COMBINED05_COHERENCE_REVIEW_PASSED',
                  'publication_path': 'docs/verification/combined-recovery/05-full-acceptance-independent-review',
                  'active_files': [], 'reviewed_capsule_sha256': result['combined_checkpoint_sha256'],
                  'files': files, 'file_count': len(files), 'total_bytes': sum(row['bytes'] for row in files),
                  'passed': True, 'build_executed': False, 'tests_reexecuted': False, 'android_executed': False}
    (OUT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), **meta(OUT / 'checkpoint.json'),
                      'file_count': len(files), 'total_bytes': checkpoint['total_bytes']}, indent=2))


if __name__ == '__main__':
    main()
