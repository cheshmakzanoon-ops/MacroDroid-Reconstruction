"""Build a narrow current-candidate README update while retaining historical observations."""
import hashlib

def replacement(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)

def update_readme(old):
    text = old.decode('utf-8')
    old_observations = text.split('## Latest trigger-navigation observations\n',1)[1].split('## Get the working source\n',1)[0]
    text = replacement(text, 'contains 1,242 recovered Java method bodies across 605 classes',
                       'contains 1,243 recovered Java method bodies across 605 classes')
    lead = '''The current numeric source and signed candidate passed all 16 configured hosted
acceptance gates: 194,780 three-path cases, 308 project Python tests, 91 compiled
Java UI fault controls, two actual numeric DEX fault controls, exact positive
restoration and the signed source-edit experiment. The job also passed 92 tooling
host controls. Its UI group ran 24,465 cases. The
[complete numeric artifact](docs/verification/day-numeric-hosted-run-3d91187/) and
[independent streamed review](docs/verification/day-numeric-hosted-run-3d91187/analysis/)
preserve the exact result, all 23 fresh reports, and the full 81,298-input snapshot
`f8fc1cadac8213468e42ac99a2cd5d807827dcdeee25166b8025620ff39a6545`.
The [nineteen-file source checkpoint](work-in-progress/day-trigger-numeric/08-command-filesystem-source-successor/)
is the exact overlay used by that job. **Android behavior for this new `0762aad9…`
APK has not yet been observed.** The existing device observations below belong
to their explicitly recorded earlier APKs.

'''
    text = replacement(text, 'The current source checkpoint is described in\n', lead + 'The previous 1,242-body source checkpoint is described in\n')
    text = replacement(text,
        '94,683,119 bytes, SHA-256\n`5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`.',
        '94,683,136 bytes, SHA-256\n`0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd`.')
    current = '''The active 1,243-body numeric candidate passed all 16 configured acceptance
gates in hosted run `38238858564`, job `114776169911`. Its 194,780 cases include
24,465 UI cases; all 308 project Python tests and 92 tooling host tests passed.
All 91 compiled Java UI faults and both actual numeric DEX faults were detected,
and the exact positive result and signed source-edit probe passed. The complete
3,308-member artifact, all 23 fresh reports and the separate review are retained
in [the numeric host evidence](docs/verification/day-numeric-hosted-run-3d91187/).
This is host/source/APK evidence; its Android probe remains unexecuted.

'''
    text = replacement(text, 'The active 1,242-body combined source passed all 16 configured acceptance gates:',
                       current + 'The previous 1,242-body combined source passed all 16 configured acceptance gates:')
    text = replacement(text, '[the current combined evidence]', '[the previous combined evidence]')
    text = replacement(text, 'new combined APK beyond the separately recorded device scopes linked above.',
                       'later candidates beyond their separately recorded device scopes.')
    marker = '| Check | Measured result | Evidence |\n| --- | --- | --- |\n'
    rows = '''| Current numeric host/source/APK proof | All 16 configured gates; 194,780 three-path cases across 1,243 bodies; 308 project Python and 92 tooling tests; 91 Java UI faults, two actual numeric DEX faults and exact restoration | [Complete numeric artifact and independent review](docs/verification/day-numeric-hosted-run-3d91187/) |
| Current numeric Android behavior | Not yet observed for the `0762aad9…` candidate; earlier APK results remain separately recorded | [Pinned current candidate](artifacts/current/manifest.json) |
'''
    text = replacement(text, marker, marker + rows)
    text = replacement(text, '| Active combined host/artifact proof |', '| Previous 1,242-body combined host/artifact proof |')
    text = replacement(text, '| Current hosted source reproduction |', '| Previous 1,242-body hosted source reproduction |')
    text = replacement(text, '| Current cold launch, intro and constructor probe |', '| Previous `5f635e16…` cold launch, intro and constructor probe |')
    text = replacement(text, '| Current scoped post-home editor session |', '| Previous `5f635e16…` scoped post-home editor session |')
    text = replacement(text, '| `artifacts/current/` | Current rebuilt APK in 12 checksum-pinned ordinary Git parts. |',
                       '| `artifacts/current/` | Current candidate manifest references 12 checksum-pinned ordinary Git parts; historical parts remain preserved. |')
    text = replacement(text, '| `docs/verification/source-ci-dbcad968/` | Exact complete ZIP and independently verified 16-gate hosted source reproduction for the active 1,242-body candidate. |',
        '| `docs/verification/day-numeric-hosted-run-3d91187/` | Complete numeric 16-gate host artifact, exact signed `0762aad9…` APK input and independent review for the active 1,243-body candidate. |\n'
        '| `docs/verification/source-ci-dbcad968/` | Exact complete ZIP and independently verified 16-gate hosted source reproduction for the previous 1,242-body candidate. |')
    new_observations = text.split('## Latest trigger-navigation observations\n',1)[1].split('## Get the working source\n',1)[0]
    assert new_observations == old_observations
    return text.encode(), {'latest_trigger_navigation_section_unchanged':True,
                          'section_sha256':hashlib.sha256(old_observations.encode()).hexdigest(),
                          'new_candidate_android_observed':False}
