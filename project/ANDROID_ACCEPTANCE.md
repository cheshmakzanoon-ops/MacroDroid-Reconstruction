# Android acceptance gates and measured scope

The source/build and host-test results do not satisfy these gates. The first hosted
device run completed installation and cold captures for both APKs but reported a
75-pixel status-icon difference. See [RUNTIME_CAPTURE.md](RUNTIME_CAPTURE.md) for the
actual evidence, subsequent configuration failure, and four-page capture contract.
Use a disposable ARM64 Android environment with no real account data.
Test the user-supplied original, the v9 baseline, and the v9 hybrid under identical device,
locale, permission, storage and network conditions. Preserve installation failures rather
than treating them as skipped successes. Do not bypass identity, purchase or integrity
requirements to make a result look equivalent.

| Gate | Required evidence | Current state |
|---|---|---|
| Installation/package verification | Installer output and package identity for each APK/API | Both APKs installed in the first hosted API 35 run; schema-3 installed-file hashing awaits its device run |
| Cold launch and application initialization | Activity launch output, process/crash logs and first-screen capture | Both captured in the first hosted run; exact comparison failed on 75 system-icon pixels |
| First-run UI and consent | Matching prompts, navigation, displayed strings and permission choices | Not executed |
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

The original local probe returned BLOCKED because ADB was absent. Later hosted
execution installed and launched both APKs and preserved the measured comparison.
The current recorder adds installed-file hashing, stricter foreground/install
validation, fresh input preconditions, and four optional intro pages. These additions
have synthetic regression coverage and require their own hosted device result.

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
is restricted to the observed application PID. The first hosted recorder executed
this cold path; newly added schema-3 command and intro paths need fresh device evidence.

The comparator rejects stale schemas, identical APKs, changed environments, missing
or changed evidence, dead/restarted PIDs, wrong foreground packages and incomplete
app UI. It compares every decoded pixel, PNG color metadata and all UI XML attribute
values/child ordering. No screen regions or dynamic text are masked. A clock/status-bar
change can therefore produce a difference; that difference must be investigated, not
automatically hidden. Synthetic comparator tests are not Android evidence. Even an
exact capture match leaves every feature gate in the table above open.

For the v9 methods, separately test multiple fingers and drag interruption, scene
state save/restore with nested Parcelables and process recreation, sound selection
locales, denied contacts permissions and SMS contact/group configuration. Host tests
substitute MotionEvent, widgets, Parcel and provider boundaries and cannot certify
those behaviors on Android.
