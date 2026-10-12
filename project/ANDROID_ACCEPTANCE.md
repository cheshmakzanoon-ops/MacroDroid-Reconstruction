# Android acceptance gates and measured scope

Hosted run `38194498356` at source commit `95077fcb1d3c86f3b1c91026619642d99198f149`
verified the actual installed original/candidate APK hashes, completed both cold launches,
and measured exact full-image/XML equality on all four English intro pages and three
observed Next transitions. Its strict reports are `EXACT_COLD_LAUNCH_MATCH_ONLY` and
`EXACT_FOUR_PAGE_INTRO_MATCH_ONLY`. All four PNG/XML pairs are byte-identical, with zero
changed decoded pixels on each page. See the [preserved successful device evidence][android-success]
and [RUNTIME_CAPTURE.md](RUNTIME_CAPTURE.md) for the tested APK identities, declared device
settings, independent checks and capture contract. These results belong to that exact
APK pair; later candidates require their own device run.

The earlier [75-pixel status-icon comparison failure][signal-failure] and
[pre-install configuration failure][configuration-failure] remain preserved. Source/build
and synthetic host-test results are separate evidence and do not satisfy unexecuted
Android gates. The newly added post-intro surface capture and standalone ART constructor
probe remain pending.
Use a disposable ARM64 Android environment with no real account data.
Test the user-supplied original, the v9 baseline, and the v9 hybrid under identical device,
locale, permission, storage and network conditions. Preserve installation failures rather
than treating them as skipped successes. Do not bypass identity, purchase or integrity
requirements to make a result look equivalent.

| Gate | Required evidence | Current state |
|---|---|---|
| Installation/package verification | Installer output and package identity for each APK/API | Original and the tested hybrid installed on API 35; schema-3 device-side hashes matched both exact local inputs before launch. Other APK/API combinations remain untested |
| Cold launch and application initialization | Activity launch output, live process/foreground evidence and first-screen capture | Exact complete cold capture passed for the `95077fcb` APK pair under the declared device settings; broader initialization behavior remains untested |
| Four English intro page stills | Four complete PNG/XML pairs and three fresh observed Next transitions | Exact match passed for `MACRODROID`, `TRIGGERS`, `ACTIONS` and `CONSTRAINTS`; zero changed pixels per page |
| First surface after intro completion | One fresh validated completion tap per APK, installed identity and full resulting PNG/XML comparison | New `--post-intro` scope pending; no permission choice or app-dialog dismissal is requested |
| Consent and permission choices | Matching prompts, chosen responses and resulting app behavior | Not executed by the measured cold/four-page scenario |
| Standalone constructor allocation on ART | Exact pinned probe/original classpath identities, enabled verification, VM output and cleanup | New independent `Lzhh;`/`Lrff;` allocation probe pending; not a Widget behavior gate |
| Macro creation/edit/delete | UI recordings and exported synthetic macro definitions | Not executed |
| Text manipulation in actual macros | Real expression/magic-text evaluation, text output and failure behavior, not host doubles | Not executed |
| Trigger/action/constraint engine | Representative supported triggers, constraints and actions with timestamped outputs | Not executed |
| Persistence/import/export | Clean restart/reboot and round-trip synthetic data comparisons | Not executed |
| Notifications/accessibility/background operation | Real permission flows and service behavior, including cancellation/restart | Not executed |
| Widgets/shortcuts/helper integration | Real launcher/helper interactions and signature-permission results | Not executed |
| Locale/device/API variation | Repeated cases across relevant API levels, screen sizes and locales | Not executed |
| Native code compatibility | Real ARM64 library loading, device logs and crash evidence | Not executed |
| Account/server/payment/integrity dependencies | Authorized test account/server results without bypasses | Not executed |
| Performance/optimization | Startup, macro latency, memory and profile-installation behavior | Not executed |

## Controlled text tests

Include empty input, null/invalid configuration where reachable, lower/uppercase with
Turkish and non-Latin text, UTF-16 boundary truncation, the three removed direction marks,
substring start/end bounds, valid/invalid regex, missing regex capture groups, literal vs
regex removal, replacement group references, escaped newlines and absent/present newline
flags. Exercise preview text as well as execution. The split-array implementation is now Java-compiled and host-tested, but still requires
real Android macro integration tests. The macro expression evaluator and magic-text
expansion remain original smali and are controlled doubles in host tests.

## Evidence rules

Record APK SHA-256, certificate fingerprint, API/ABI/locale and clean-state procedure for
each run. Screenshot resemblance alone is not functional equivalence. Do not infer a pass
from lack of a visible crash, and do not treat host mocks as real Android behavior. Flag
certificate-bound differences separately; a new development signing identity is an actual
known difference, not a cosmetic packaging change. Repeat observed failures in the
original before attributing them to reconstruction.

## Recorder status

The original local probe returned BLOCKED because ADB was absent. Hosted run
`38194498356` later exercised schema-3 installed-file hashing, strict successful installs,
foreground/process validation, fresh Next-input preconditions and all four intro pages.
Those measured gates passed for the exact original and candidate hashes recorded in
[RUNTIME_CAPTURE.md](RUNTIME_CAPTURE.md) and the [device recorder result][recorder-success].

The current extension requests `--intro-pages --post-intro`, rechecks the installed APK
and fresh `CONSTRAINTS` hierarchy, and taps the observed final `button_next` control once.
It captures the first resulting notification-permission or app landing surface without
choosing a permission or dismissing an app dialog. Its strict comparator uses the full
pixels/XML and requires the previous intro match. This additional scope is Android-pending.

The separate repository helper `tools/android/android_constructor_probe.py` uses a pinned
1,436-byte DEX and the unchanged original APK to test one constructor allocation with
`-Xverify:all`. The [frozen Java/D8 proof][constructor-proof] is established on the host;
the actual ART invocation remains pending. An ART failure still permits both app captures
and all three comparisons, and a later capture failure preserves the independent ART
result. Neither this probe nor the intro captures establishes Widget or home-feature parity.

## Core method Android scenarios — not executed

Use synthetic macros to compare the original, baseline and hybrid for AND/OR gates,
all-disabled constraints, force/category behavior, debugging suppression, wait-until
trigger continuation, logging exclusions and constraint evaluation order. Test
first-match macro-name selection, self references, GUID/name fallback and missing
references. Check light equality and crossing decisions with controlled sensor inputs,
and replay permitted synthetic weather responses for threshold, code-group and
previous/current-state transitions. These scenarios require the real app boundaries,
not the host test doubles. Keep app state, permissions and observations comparable;
record nondeterminism and certificate/service differences rather than bypassing them.


## Additional v7 acceptance — NOT EXECUTED

Compare System/Secure/Global settings reads and permission-denied/default paths on actual Android. Check Wi-Fi and hotspot constraints around API 27/29, location prompts, SSID aliases and disabled/disconnected states. Compare solar constraints before/equal/after event times, timezone changes, polar dates, persistence and nested macro gating. Host stubs and the deterministic test clock do not satisfy any of these device gates. No permission or integrity-check bypass should be used to conceal a discrepancy.


## Cold-launch recorder and comparison

The recorder now validates both APK ZIPs, the exact original SHA-256 and the expected
package/version/minimum/target SDK before uninstalling anything. It checks distinct
APK identities and never selects a device implicitly. The explicit data-removal flag
acknowledges that the known target package will be removed between runs.

On an already isolated disposable ARM64 environment with ADB on PATH:

```sh
python android_acceptance.py --serial DISPOSABLE_SERIAL --original /path/to/original.apk --candidate dist/MacroDroid-5.67.8-v9-hybrid.apk --accept-package-data-removal --output reports/device-capture
python android_compare.py reports/device-capture
```

A physical device additionally requires `--allow-physical-device`. These commands
are optional and are not executed by offline acceptance. They do not grant
permissions, click consent, log in, alter licensing, or enable cloud billing.

The recorder requires an explicit successful activity start, matching nonempty PID
samples before/after collection, foreground target activity, target-owned UI nodes,
and a CRC-valid screenshot. Screenshots, hierarchy and logs are locally hashed.
Installed-only or background-only states cannot become a capture pass. Log collection
is restricted to the observed application PID. The `95077fcb` hosted recorder successfully
executed the schema-3 cold and four-page paths. A new candidate identity or the newly
requested post-intro scope still requires fresh device evidence.

The comparator rejects stale schemas, identical APKs, changed environments, missing
or changed evidence, dead/restarted PIDs, wrong foreground packages and incomplete
app UI. It compares every decoded pixel, PNG color metadata and all UI XML attribute
values/child ordering. No screen regions or dynamic text are masked. A clock/status-bar
change can therefore produce a difference; that difference must be investigated, not
automatically hidden. Synthetic comparator tests are not Android evidence. The measured
exact still captures leave the remaining feature, permission-choice, animation and
device-variation gates in the table above open.

For the v9 methods, separately test multiple fingers and drag interruption, scene
state save/restore with nested Parcelables and process recreation, sound selection
locales, denied contacts permissions and SMS contact/group configuration. Host tests
substitute MotionEvent, widgets, Parcel and provider boundaries and cannot certify
those behaviors on Android.

[android-success]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/blob/0c5913324bcf60bacdb46554d80b3eda684dd79d/docs/verification/android-ci-95077fc/README.md
[recorder-success]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/blob/0c5913324bcf60bacdb46554d80b3eda684dd79d/docs/verification/android-ci-95077fc/capture/result.json
[signal-failure]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/0c5913324bcf60bacdb46554d80b3eda684dd79d/docs/verification/android-ci-ba52fd6
[configuration-failure]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/0c5913324bcf60bacdb46554d80b3eda684dd79d/docs/verification/android-ci-bebf448
[constructor-proof]: https://github.com/cheshmakzanoon-ops/MacroDroid-Reconstruction/tree/c7abf086ebffbc70cb3143f909a7f48648de22bc/work-in-progress/constructor-owner/02-pipeline-proof
