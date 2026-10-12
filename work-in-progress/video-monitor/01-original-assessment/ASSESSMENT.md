# Next exact method recovery after the 1,242-body baseline

The fresh registry contains **1,242** exact method-body replacements. Scanning the
reference tree finds 42 decompiler-failure markers: 21 map to registered bodies
and 21 remain. These are reference markers, not an application-wide parity metric.
The inventory was generated against the verified combined source and independently
read the selected methods from the original uploaded APK. Active inputs were
only read; all output is in this separate assessment folder.

## Selected next method: video recording storage and growth monitor

`Lcom/arlosoft/macrodroid/action/services/a;->invokeSuspend(Ljava/lang/Object;)Ljava/lang/Object;`

The original APK method has **262 instructions**, **534 code units**, **25
registers**, and **46 conditional IF edges**. It has no switch instruction and six
Exception-handler regions. The edge count follows the current host UI coverage
gate: two edges per IF; exception-handler transfers and unconditional jumps are
listed separately and are not counted as conditional edges. Counts are metadata,
not visited coverage. Original bytecode extraction produced a one-method,
4,552-byte test-only DEX, SHA-256
`940aee4861d9bd52951ccc835e91a917bb56748b4eaad5deb8a0fa1c7d2c3254`.

Original method body SHA-256:
`4c1233b2c46c08ba5713e1194d626e29a4bd07c6891190d08ff86afd6380c376`.
Its enclosing source class is
`source/smali/classes/0d/a_0dfe0f87312c8ea9.smali`, SHA-256
`05149221b78ddab67933f4aa8aba10330787889c9a3749d6d7296eaeb6cd6d4d`.
The extracted `.smali` review copy includes a final newline, so its file hash is
separately recorded from the exact build-method matcher hash.

### Coroutine entry and exit cases

| Entry | Original required behavior | Proposed controlled cases |
| --- | --- | --- |
| Label 0 | Check resumed result outside catches, write label 1, call 5,000ms delay, return the captured marker by identity or continue | Normal/failure result; synchronous, suspended, null and unrelated delay returns; delay Exception/Error; callback mutation of recording flag/owner |
| Label 1 | Check resumed result outside catches and enter monitor loop | Active/inactive recording, result failures, unchanged saved slots until a later yield |
| Label 2 | Cast saved L$1 to File and then L$0 to qnc before the Exception catch; check result inside that catch; success returns captured Unit | Both dead casts independently malformed and both malformed for order; injected Exception enters outer-error log plus repeat delay; Error escapes; exact Unit identity |
| Label 3 | Check resumed result outside catches and enter monitor loop directly | Resume success/failure, null owner, inactive recording, saved-slot preservation |
| Other labels | Call the exact invalid-resume guard; original defensive return is null if that external guard returns | Negative, positive and high-bit labels; exact thrown message/type; one explicitly injected returning-guard case |
| Loop continuation | Check companion nonnull, then volatile recording flag; repeat yields clear both saved slots, write label 3, call 3,000ms delay | Synchronous sequences ending in suspension/recording=false, repeated resumes and two-or-more iterations, exact state before every external call |
| Stop dispatch | Read zp4.a even though its value is discarded, then at9.a; construct d31 with current owner and null completion; clear slots/write label 2 before dt9.e0 | Synchronous/suspended/null/unrelated results; exact dispatcher/callback/owner/continuation identity; constructor/dispatch Exception or Error |

### Storage, file and state boundaries

The method chooses the current video file's parent, then falls back to the
current owner's external Movies directory if the file or its parent is null.
Every repeated read of `self.this$0`, `owner.t`, owner IDs and counters must remain
at its original point. Controlled File subclasses can independently implement
`getParentFile`, `exists` and `length` without touching the host filesystem.

Available-space reporting updates `x` when its old value is nonpositive or the
new space is strictly below `x - 104857600` (100 MiB). Storage below 134217728
bytes (128 MiB) requests a stop. Cases cover values just below/at/above each
threshold, negative and large signed long values, and exact integer-division log
text. No saturating arithmetic or threshold rounding is proposed.

File-size handling preserves the distinct missing-file size zero and nonnull
ParcelFileDescriptor sentinel -1. A nonnegative measured size is logged. A
positive previous size with nonpositive growth increments `w`, including Java's
32-bit wraparound, and checks a freshly read counter against three. Positive
growth resets the captured owner's `w`. A nonpositive previous size leaves that
counter untouched. The current owner's `v` is written after these checks and
logs. Planned cases include growth/stall/regression, zero/negative sizes,
counter values around two/three and both integer extremes, absent/present file
and descriptor, and owner/file/ID/counter changes at each observable boundary.

### Exceptions and ordering

The initial result checks, label-2 dead casts, companion null check, repeat delay
and outer error logger lie outside the main Exception handling region. File
exists/length failures have an inner Exception handler that logs with its
captured owner and falls back to zero. Failure in that inner logger is handled by
the outer Exception handler. The outer handler calls `Throwable.getMessage`
before concatenation and reads the owner again before logging. Its own failures
escape. Errors escape both Exception-only catches. Tests will inject the same
exception objects at every controlled call, compare exact identity/message,
trace and partial state, and distinguish VM-generated cast/null messages only if
an actual original/JVM difference requires a narrowly documented exclusion.

### Required host dependencies and proof

New host boundaries are BaseVideoRecordingService, its companion and continuation
class; Context.getExternalFilesDir, Environment.DIRECTORY_MOVIES and
ParcelFileDescriptor; the sz6 delay, dt9 dispatcher and d31 callback; and the
at9/zp4 dispatcher holders plus their declared types. Existing coroutine/result,
logging and string helpers can gain inactive-by-default VideoControl hooks.
All host boundaries remain excluded from the APK. The original creates d31 and
invokes d31's own constructor; this body needs no constructor-owner rewrite.

The original opcode-name scan found a current interpreter path for every opcode
in this method. This does not replace differential execution, full instruction
and IF-edge coverage, or meaningful opcode conformance if a real semantic gap
appears. Planned deliberate compiled faults target delay values/state order,
continuation labels/dead casts, threshold inequalities, repeated owner/file
reads, stall-counter arithmetic, Exception-vs-Error catches/logger placement,
Unit/suspension identity, file sentinel behavior, callback capture and loop exit.
A complete original/JVM proof and clean restoration precede any signed build.
A full build cache waits for root's combined acceptance and disk coordination.

## All remaining original methods

The following exact original-DEX counts supersede the preliminary text-line
counts in `remaining-method-metadata.json`. Data payload text is not counted as
individual DEX instructions. For example, R.styleable has 42 DEX instructions,
while its initial smali text scan counted 111 instruction-like lines. An explicit
SceneSlider decompiler alias resolves to `SliderValueText-cf5BqRc`; no source
method was missing. Any listed opcode gap is a static name scan of the current
oracle, not an executed failure or license to approximate the operation.

| Original method | Instructions | Conditional IF edges | Opcode names lacking a current handler |
| --- | ---: | ---: | --- |
| `action.services.a.invokeSuspend` | 262 | 46 | None found by scan |
| `DonateActivity.i1` | 108 | 18 | None found by scan |
| `R$styleable.<clinit>` | 42 | 0 | SPUT_OBJECT |
| `common.SelectableItem.checkAllPermissions` | 593 | 96 | None found by scan |
| `action.FloatingButtonConfigureAction.X` | 853 | 44 | DIV_FLOAT |
| `action.GetCalendarEventsAction.m0` | 1266 | 74 | MUL_INT, MUL_INT_LIT16, MUL_INT_LIT8 |
| `action.NotificationInteractionAction.handleItemSelected` | 594 | 102 | None found by scan |
| `action.UIInteractionAction.secondaryItemConfirmed` | 2042 | 366 | None found by scan |
| `action.k.invokeSuspend` | 228 | 18 | None found by scan |
| `action.services.FileOperationV21Service.f` | 1087 | 208 | None found by scan |
| `action.services.UIInteractionAccessibilityService.onStartCommand` | 1665 | 178 | ADD_FLOAT, ADD_FLOAT_2ADDR, DIV_FLOAT, DIV_FLOAT_2ADDR, DOUBLE_TO_FLOAT, FLOAT_TO_DOUBLE, LONG_TO_FLOAT, MUL_FLOAT, MUL_FLOAT_2ADDR, SUB_FLOAT, SUB_FLOAT_2ADDR |
| `action.services.k.invokeSuspend` | 466 | 94 | SPUT_BOOLEAN, SPUT_OBJECT |
| `constraint.NotificationPresentConstraint.secondaryItemConfirmed` | 526 | 30 | None found by scan |
| `scene.components.SceneSlider.Composable_sW7UJKQ$lambda$3` | 553 | 38 | ADD_FLOAT, ADD_FLOAT_2ADDR, DIV_FLOAT_2ADDR, MUL_FLOAT, MUL_FLOAT_2ADDR, MUL_INT_2ADDR, OR_INT, SUB_FLOAT, SUB_FLOAT_2ADDR, USHR_LONG, XOR_LONG |
| `scene.components.SceneSlider.SliderValueText-cf5BqRc` | 493 | 54 | OR_INT, SHL_INT_LIT8, USHR_LONG, XOR_LONG, XOR_LONG_2ADDR |
| `triggers.NotificationTrigger.secondaryItemConfirmed` | 571 | 34 | None found by scan |
| `triggers.VariableTrigger.z0` | 712 | 76 | None found by scan |
| `upgrade.ProDeviceCheckWorker.a` | 291 | 32 | None found by scan |
| `upgrade.billing.e.k` | 174 | 22 | None found by scan |
| `upgrade.billing.e.l` | 200 | 18 | None found by scan |
| `i4e.invoke` | 219 | 18 | USHR_LONG, XOR_LONG_2ADDR |

The smaller selection-dialog Compose lambda is 219 instructions/18 IF edges,
but needs USHR_LONG and XOR_LONG_2ADDR conformance plus many Compose boundaries.
Video monitoring provides a substantial ordinary app state machine with directly
bounded external effects. Billing and device-pro entitlement methods retain their
original behavior and are deferred for this recovery chunk.

## Input and outcome binding

Original APK SHA-256:
`84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800`.
Fresh registry SHA-256:
`73a37f1ac4148c03a1dc0df9810e899ebb8ff7bcc6f1df7c1672fd525d66a20e`.
`reports/original-inventory-01/result.json` records both successful bounded Java
commands, exact inputs and original fixture. The complete metadata contains
method/field/type references, opcode frequencies, each IF-edge offset and each
Exception-region boundary. There is no app execution, registration, rebuilt
comparison, Android execution or full-runtime parity claim in this checkpoint.
