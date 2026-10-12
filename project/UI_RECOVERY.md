# UI, scene-state, selection and touch-blocking recovery

Six existing method bodies in this family are compiled from readable Java. The full
registry has 1,238 bodies across 602 classes; 1,119 are prior constant/no-op bodies.
This is not a complete Java/Kotlin application or Android runtime equivalence.

| Original method | Recovered helper | Scope |
|---|---|---|
| `DragLinearLayout.onTouchEvent(MotionEvent)` | `InteractionMethods.touch` | Pointer/event dispatch and original drag-state cleanup |
| `PlaySoundAction.Z(String)` | `SelectionMethods.isSoundToken` | Fixed/localized/generic bracket-token recognition |
| `IncomingSMSTrigger.isValid()` | `SelectionMethods.validSms` | Original contact/group option validation and cached result behavior |
| `SceneTextConfig$a.createFromParcel(Parcel)` | `SceneStateMethods.read` | Original constructor argument/read sequence |
| `SceneTextConfig.writeToParcel(Parcel,int)` | `SceneStateMethods.write` | Original field/write sequence and Parcelable flags |
| `BlockTouchesAction.invokeAction(TriggerContextInfo)` | `BlockTouchesMethods.invoke` | Trigger restrictions, block/unblock/toggle selection, original service calls and typed Intent payloads |

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

`UiParityTests` compares original selected instructions, recovered Java on the JVM
and rebuilt DEX instructions whose bytes are checked against the signed APK. The
suite has 11,353 cases: 1,271 sound-token; 2,065 SMS-validation; 1,494 drag; 945
scene-read; 3,158 scene-write; and 2,420 touch-blocking cases. Its 9,543 independently
specified result/state expectations supplement the three-path comparisons. All
563 represented original instructions in these six methods were visited. The
new touch-blocking method visited all 162 original instructions and both outcomes
of its 15 conditional branches (30/30 edges); the suite requires that coverage.
This remains bounded evidence rather than exhaustive path/input coverage.

The complete `test.py --three-way` run passes 181,668 cases across all 1,238
registered method bodies, with zero failed cases or unsupported executions and an
exact, non-overlapping method-key partition across the five suites. All nine rebuilt
DEX partitions were matched byte-for-byte to the signed APK. The independent hybrid
round-trip verifier compared 71,267 classes and 349,972 methods, with no missing or
extra classes, unregistered body changes, changed baseline source, altered opaque
payload, or alignment failures. See `reports/java-all-path-parity.json` and
`reports/hybrid-roundtrip.json`.

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

Twelve temporary host defects must be rejected by named cases. The five existing
controls move the drag cast, accept only boolean integer 1, substitute italic for
bold during writing, swallow SMS provider Error, and reject generic sound tokens.
Seven touch-blocking controls recompute the toggle state after stopping, omit the
option reread, reuse an earlier trigger, substitute height for width, alter the
hidden-color sentinel, narrow the handler to RuntimeException, and widen it to
swallow Error. Each control must fail its named case with zero unsupported
executions. The correct positive suite runs again afterward, and hashes verify
that recovered source, the original fixture and the signed APK remain unchanged.
No faulty APK is distributed. The current run passes all twelve controls and the
11,353-case positive restoration, with zero unsupported executions. The seven new
controls detect 34, 31, 926, 420, 159, 9 and 41 affected cases respectively; see
`reports/ui-negative-controls.json`.

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
