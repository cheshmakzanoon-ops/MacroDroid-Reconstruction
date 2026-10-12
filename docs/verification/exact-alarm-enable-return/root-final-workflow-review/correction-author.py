#!/usr/bin/env python3
"""Keep the failed audit and bind the already indexed candidate's actual parent."""
from pathlib import Path
import difflib
import hashlib
import json

root=Path('/dev/shm/macrodroid-settings-final-root-review')
old=(root/'review-01/executed-reviewer.py').read_text()
new=old.replace("OUT = ROOT / 'review-01'", "OUT = ROOT / 'review-02'",1)
before="r['commit']==PARENT and r['exit_code']==0 and r['timeout_seconds']==30"
after="r['commit']==('48ddc442c61e383c4368606cb31984f15d03bb1f' if r['path'].startswith('work-in-progress/day-trigger-numeric/10-hosted-accepted-artifact/') else PARENT) and r['exit_code']==0 and r['timeout_seconds']==30"
assert new.count(before)==1
new=new.replace(before,after,1)
marker="    copy(Path(__file__), 'executed-reviewer.py')\n"
retention="""    copy(Path(__file__), 'executed-reviewer.py')
    for prior in sorted((ROOT/'review-01').rglob('*')):
        if prior.is_file(): copy(prior, 'retained-root-review-attempt-01/'+prior.relative_to(ROOT/'review-01').as_posix())
    copy(ROOT/'correct_review_parent_binding.py', 'correction-author.py')
    copy(ROOT/'review-parent-correction.patch', 'review-parent-correction.patch')
    copy(ROOT/'review-parent-correction.json', 'review-parent-correction.json')
"""
assert new.count(marker)==1
new=new.replace(marker,retention,1)
with (root/'audit_settings_02.py').open('x') as f: f.write(new)
with (root/'review-parent-correction.patch').open('x') as f:
    f.write(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='failed-review-01/executed-reviewer.py',tofile='review-02/executed-reviewer.py')))
result={'scope':'Root evidence-reader correction only; no source/workflow/test or raw evidence change',
        'prior_failure':'The root reviewer incorrectly assumed all immutable read references used fc825ede. The closed index and reader use the earlier 48ddc442 publication for the candidate manifest and its 12 parts.',
        'observed_git_read_counts':{'fc825ede39a40249e33c8ba75b93128a98bd5e3c':189,'48ddc442c61e383c4368606cb31984f15d03bb1f':13},
        'correction':'Require the exact 48ddc442 revision only for the fixed candidate publication prefix; retain fc825ede for every other role. All byte, mode, source, execution and result checks remain unchanged.',
        'old_author_sha256':hashlib.sha256(old.encode()).hexdigest(),'new_author_sha256':hashlib.sha256(new.encode()).hexdigest(),
        'retained_prior_capsule_sha256':hashlib.sha256((root/'review-01/checkpoint.json').read_bytes()).hexdigest(),
        'android_executed':False,'host_suite_executed':False,'production_source_changed':False}
with (root/'review-parent-correction.json').open('x') as f: f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
