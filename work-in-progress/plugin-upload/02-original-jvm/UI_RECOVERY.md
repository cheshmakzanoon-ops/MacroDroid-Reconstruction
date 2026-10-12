# UI and plugin method recovery

Nine existing method bodies in this family are compiled from readable Java. The full
registry has 1,241 bodies across 604 classes; 1,119 are prior constant/no-op bodies.
This is not a complete Java/Kotlin application or Android runtime equivalence.

| Original method | Recovered helper | Scope |
|---|---|---|
| `DragLinearLayout.onTouchEvent(MotionEvent)` | `InteractionMethods.touch` | Pointer/event dispatch and original drag-state cleanup |
| `PlaySoundAction.Z(String)` | `SelectionMethods.isSoundToken` | Fixed/localized/generic bracket-token recognition |
| `IncomingSMSTrigger.isValid()` | `SelectionMethods.validSms` | Original contact/group option validation and cached result behavior |
| `SceneTextConfig$a.createFromParcel(Parcel)` | `SceneStateMethods.read` | Original constructor argument/read sequence |
| `SceneTextConfig.writeToParcel(Parcel,int)` | `SceneStateMethods.write` | Original field/write sequence and Parcelable flags |
| `BlockTouchesAction.invokeAction(TriggerContextInfo)` | `BlockTouchesMethods.invoke` | Trigger restrictions, block/unblock/toggle selection, original service calls and typed Intent payloads |
| `CustomSceneAction.W(int,TriggerContextInfo,boolean,Stack,ResumeMacroInfo)` | `CustomSceneMethods.display` | Overlay/dialog/full-screen selection, existing-scene dispatch, original permission-warning fallthrough and ordered payloads/events |
| `plugins.j.invokeSuspend(Object)` | `PluginLookupMethods.lookup` | Lookup gates, suspension/resumption state, original repeated-key retry behavior, analytics and result/error publication |
| `plugins.k.invokeSuspend(Object)` | `PluginUploadMethods.upload` | Optional icon processing, saved-field casts, two upload suspension points, ordered payloads and original error publication |

`source/ui-methods.json` pins the exact descriptors and original method hashes.
Only the registered bodies replace existing implementations. Class structure,
fields, constructors, dependencies and unregistered methods remain preserved smali.
The original APK and selected original DEX fixture are not build inputs. The fixture
was re-extracted from the exact original upload for comparisons.

## Preserved behavior

Drag motion casts the float coordinate to an integer BEFORE subtracting the integer
anchor. Reordering those operations changes fractional values and extreme values.
The original explicit animator/view casts, transition handling, active-pointer
release behavior and partial cleanup before exceptions remain. The actual animation,
movement and view-lifecycle methods are original dependencies, not reimplemented here.

The sound-token method checks the fixed stop token first, then a localized resource
inside its narrow Exception handler, then accepts any string enclosed in brackets.
Its handler does not catch Error. The SMS validator normalizes a negative option
without changing its stored field, retains the legacy contact sentinel, and only
updates lastValidCheck in the single-group provider path. Context lookup and group
ID casting occur outside the provider handler. That handler catches Exception, not
Throwable. The uploaded method does not close its returned Cursor; no silent behavior
fix was introduced during reconstruction.

Touch blocking was recovered directly from the original 474-line smali method,
including the instructions that the reference decompiler could not reconstruct.
Option 0 blocks, option 1 unblocks, and option 2 toggles using the service state
observed before `stopService`. Other option values take the unblock path. The
option field is read again after `stopService`, so a dependency changing the option
can affect that later decision. Device-unlocked and screen-on restrictions run
before any service is stopped. The original repeated trigger lookups, explicit
null checks, casts, companion reads and context lookups retain their order.

Color resolution still occurs before choosing the service and before replacing a
hidden area's color with the original `-1` sentinel. Accessibility blocking sends
only `blocking_color` and the original action string. The overlay service receives
`x`, `y`, `width`, `height`, then `blocking_color`, with the four dimensions kept as
float values. The accessibility Intent construction/configuration/start region
catches `Exception` and logs the same caught object with the original message.
Its earlier context/null checks and color resolution remain outside that handler;
`Error` propagates. The overlay and unblock paths retain their unguarded calls.
Service return values are ignored exactly as in the uploaded implementation.

Custom scene dispatch retains the separate accessibility and regular overlay paths,
plus dialog/full-screen activity selection. Its background/overlay-permission warning
continues into display selection. Existing scene activities are reused only when they
are neither finishing nor destroyed, with the original short-circuit order and
Runnable discriminator. New activities receive the original extras and flags, and
the clear-by-exact-name event is posted before launch. Only accessibility overlay
Intent construction/start has the original narrow Exception handler. Repeated
macro, scene, context and identifier reads and all companion/null checks remain in
their original order. See `SCENE_RECOVERY.md` for the complete scope and evidence.

Plugin lookup preserves the denied/known-package/attempt-limit gates, both suspension
labels, continuation-field write/read order and identity-based suspension detection.
The original retry loop keeps selecting key index 0. Repeated HTTP status reads,
restored retry flags, analytics order, captured owners/sinks and later field reads
remain distinct. Only the original `Exception` regions catch failures; Error and
handler failures escape. Counter reset follows successful result publication.
See `PLUGIN_RECOVERY.md` for the literal retry behavior and detailed proof scope.

Plugin upload preserves the saved-field casts outside its handler, initial versus
resumed result checks, optional icon conversion, ignored compression Boolean and
nested media-type parsing handler. Request companion capture, exact request defaults,
all five continuation-field clears, payload argument order and both suspension
identity checks retain their positions. HTTP status is read twice; denied-state
mutation precedes publication, and generic error publication precedes logging.
Only the original Exception regions catch failures. Returned API values, thrown
exceptions and resumed failure wrappers remain distinct. See `PLUGIN_UPLOAD_RECOVERY.md`.


Scene state retains its 21-field read/write protocol in this order:

```
text, textColor, textColorVariable, textSize, isBold, isItalic,
textAlignment, enableSelection, htmlFormatting, visibilityVariable,
enabledVariable, maxLinesEnabled, maxLines, autoSizeText, fontFamily,
enableAutoRefresh, padding, buttonClickConfig, closeSceneOnPress,
variableToUpdate, variableUpdateValue
```

Read booleans accept every nonzero integer. Writes emit canonical 0/1 and forward
the caller's flags to each nested Parcelable. Class-loader calls and casts remain
in their original order. The original constructor and nested Parcelable behavior
are not reconstructed by these two methods.

## Executed host comparisons

`UiParityTests` compares original selected instructions with recovered Java on the
JVM and also supports a rebuilt DEX path whose bytes must match the signed APK.
The current upload candidate passes the original/JVM path; its signed path is pending.
The suite has 20,832 cases: 1,271 sound-token; 2,065 SMS-validation; 1,494 drag; 945
scene-read; 3,158 scene-write; 2,420 touch-blocking; 4,070 scene-dispatch;
3,053 plugin-lookup; and 2,356 plugin-upload cases. Its 15,128 independently
specified result/state expectations supplement the differential comparisons. All
1,329 represented original instructions in these nine methods were visited. The
new touch-blocking method visited all 162 original instructions and both outcomes
of its 15 conditional branches (30/30 edges); the suite requires that coverage.
Scene dispatch visits all 405 original instructions and all 40 conditional edges,
and the suite requires that coverage as well. Eight explicitly identified cases
inject a returning `j68.h0` boundary to exercise the defensive `throw null` instructions;
they do not claim that the original null-guard implementation returns.
Plugin lookup visits all 198 original instructions and all 34 conditional edges,
also enforced as a hard gate. Upload visits all 163 original instructions and all 26
conditional edges, with the same hard coverage requirement. Lookup and upload each
have one explicit case substituting a returning invalid-label guard to exercise an
original defensive return; normal invalid labels must throw.
This remains bounded evidence rather than exhaustive path/input coverage.

The complete five-suite original/JVM host acceptance run for this upload candidate
passes 191,147 cases across exactly all 1,241 bodies, with zero failed cases or
unsupported executions and an exact, non-overlapping method-key partition. All 161
Python tests pass in this isolation. Its signed rebuild, three-path comparison and
independent APK roundtrip are pending. The preceding frozen lookup checkpoint passed 188,791 three-path cases
across 1,240 bodies, matched all nine rebuilt DEX partitions to its signed APK and
independently compared 71,267 classes and 349,972 methods without structural or opaque
payload changes outside the registered bodies. That historical result is described
in `PLUGIN_RECOVERY.md`; it does not establish signed acceptance of the added upload
body. Current evidence and pending gates are detailed in `PLUGIN_UPLOAD_RECOVERY.md`.

Touch-blocking cases compare ordered calls, typed Intent tokens and float bits,
argument identities, repeated dependency reads, partial effects before failures,
service flags and caught-exception identity. They cover every option branch,
changing trigger responses, nullable collaborators, extreme/NaN/zero/subnormal
float payloads, color inputs, ignored service return values and option/configuration
changes during calls. Failure injection visits every observed boundary in selected
representative paths, including a checked IOException to verify the complete
Exception handler and an AssertionError to verify that the handler stays narrow.

The fake Parcel records typed tokens and ordered calls, NOT Android Parcel binary
format. MotionEvent, view state, resource lookup, constructors, contacts and provider
results are controlled host boundaries. Context, Intent, service state and the
color resolver are also test doubles; they do not start Android services, display
an overlay, intercept touches or implement Android Intent marshalling. Values,
selected identities, exception types, call order and partial mutations compare.
Rendering, actual contacts/permissions, process recreation, native code, app
lifecycle and Android framework implementations are not tested by this suite.

The bounded test interpreter initially lacked float-to-int support. That failed
run is preserved in `reports/development-v9/ui-missing-float-to-int.json`. The new
opcode implementation is checked by `UiOracleConformance`: 6,270 cases including
21 fixed expected vectors, generated raw floating-point values, saturation,
NaN/zero, subnormal values and integer-subtraction overflow. This is not ART.

Fifty-four temporary host defects must be rejected by named cases. The five existing
controls move the drag cast, accept only boolean integer 1, substitute italic for
bold during writing, swallow SMS provider Error, and reject generic sound tokens.
Seven touch-blocking controls recompute the toggle state after stopping, omit the
option reread, reuse an earlier trigger, substitute height for width, alter the
hidden-color sentinel, narrow the handler to RuntimeException, and widen it to
swallow Error. Each control must fail its named case with zero unsupported
executions. The correct positive suite runs again afterward, and hashes verify
that recovered source, the original fixture and the signed APK remain unchanged.
Ten scene controls stop after the permission warning, change the accessibility
description key, alter the dialog Runnable discriminator, reuse a destroyed
activity, launch before posting the clear event, substitute the macro identifier
for the item identifier, omit the description reread after context lookup, narrow
the catch to RuntimeException, swallow Error, and hard-code the activity description
key. Fifteen plugin controls alter the denied gate, attempt threshold, false precheck,
precheck/API labels, repeated key selection, repeated HTTP status reads, counter-reset
order, checked-exception catch, Error escape, restored error index, retained retry flag,
owner capture, analytics index and suspension identity. Each is required to reject a
specific named case. Seventeen upload controls remove a saved cast, obey the ignored
compression Boolean, change the nested handler, re-read the request companion,
change request defaults, alter both labels, omit a saved-field clear, remove icon
fallback, collapse status reads, delay denied-state mutation, move sink capture,
narrow/widen the catch, move logging and replace both identity checks with equality.
All 17 new defect sources have unique anchors and compile. Behavioral execution of
all 54 controls and the final clean 20,832-case three-path restoration are pending.
The preceding lookup candidate's 37-control and 18,476-case restoration results are
preserved in its separate frozen proof. Source, fixture and signed APK hashes must
remain unchanged throughout the new control run; all full reports/logs will be retained.
No faulty APK is distributed.

VM-generated null/cast message wording is excluded from equality because it depends
on the interpreter/JVM/ART implementation. Exception class, ordering and partial
effects still compare. This exclusion does not apply to injected boundary exceptions:
their exact identities and messages, including injected NullPointerException messages,
are checked. The original uninitialized-property message is checked separately.

## Report and runner boundaries

`test.py --three-way` requires all five suites, fresh reports, exact executed-method
key coverage with no overlaps, and DEX bytes that match the signed APK. Counts alone
cannot conceal untested or duplicate registered replacements. Malformed/negative
counts cannot be used to cancel failures. The new suite cannot be omitted while
retaining an overall pass.

`android_acceptance.py` and `android_compare.py` address a separate issue in the old
smoke recorder: installation or `Status: ok` alone no longer proves a live app capture.
The gates and comparison logic have synthetic unit tests. Android execution is a
separate acceptance layer; consult `ANDROID_ACCEPTANCE.md` and the current device
reports for that evidence. These host suites do not establish full runtime 1-to-1
application equivalence.
