# Independent neutral numeric ART probe review

The frozen Java source and its retained compilation/corpus evidence **pass this bounded independent review**. No semantic blocker was found. This is a source and stored-evidence result. The real application target, Android ART, the future runtime wrapper and its workflow were not executed or accepted by this review.

| Reviewed input | Exact SHA256 |
|---|---|
| Source-design checkpoint, 6,786 bytes | `707afe796307be6044a5571cc39d4480ec032d2bf3d0ad87eb9a75118959deda` |
| Compiled-probe checkpoint, 6,901 bytes | `e3c67ab9f469e39b637cba2efd0ca6bd1a0892e49cc6333638b0b6aab66fd5ad` |
| Neutral Java, 15,540 bytes | `ab5b1b1d01ab33f66cab22c1d5a5f7c09ffdf13b8e0e335cf22f86ba5fcc6c2b` |
| Single probe DEX, 14,108 bytes | `7cf6f31793b1f0546bf4927a63481a25662634b8a0ac2fa520a69900204ed3aa` |

The intended APK identities remain the original `84333011a4803b296ebe030564a549495de61b76c51263488aa46af594351800` and the numeric candidate `0762aad956193ef305afc47b4cbe68e6239c94f72732556e650d701b4a288afd`. This review does not substitute the combined lookup candidate or the older indicator candidate for either input.

## Actual independent work

`review.py` rehashed all 64 payloads in the two capsules, checked the exact source copy used for compilation, replayed the mechanical adaptation of the old typed case/expectation methods to the neutral `Object[]` representation, and verified all ten bound original-class fingerprints. The exact extracted original `r0` body has SHA256 `8383c90ebe3d35afa63d52cf92cd4c92b54ed4525ca0d8a31a29fe603f9eef21`.

The review parsed the existing inventory-only JVM stdout, retained corpus and prior independent Python expectations. Its own arithmetic calculation agrees for **all 1,291 inputs** and the compact input digest remains `e083bc1996c5c7191bffe837fc0f30e254848a4754676ba0a8a119d23e8f6e79`. Integer expectations use signed modulo 2^32. For a finite decimal, this review decodes the represented binary64 value into an exact rational, truncates that rational toward zero and clamps to the signed 32-bit endpoints. NaNs and infinities have explicit branches. This read-only calculation is distinct from executing the application or a new probe/test suite.

| Input kind | Cases |
|---|---:|
| Integer | 547 |
| Decimal | 734 |
| Null entry | 1 |
| Null contained value | 1 |
| String, including one null text field | 4 |
| Boolean | 2 |
| Dictionary | 1 |
| Nested entry | 1 |
| **Total** | **1,291** |

The five recorded compiler/version/inventory commands and their ten raw output streams match their receipts. Each returned zero within its recorded 30- or 120-second bound. The Java 8 compilation warning remains in the raw stderr. The existing JVM command used `--inventory` and `-Xverify:all`; that branch returns before application-class loading. No compiler, JVM, test suite, ART process, application build or Git operation was invoked by this reviewer.

I also independently parsed the DEX header, checksums, class definitions and type IDs. Its one definition is `Lrecovered/probe/DayNumericMethodProbe;`. The direct type references are primitives/arrays, Java classes, that probe and the two declared Dalvik metadata annotations. It defines and directly references no application or Android class. Application names are reflection strings; they are not substitute class definitions. The retained classfile is Java 8 major version 52. All reviewed source and evidence identities match again at closure. The read-only audit passed on its first executed attempt.

## Target semantics and real-object construction

The original public static `DayTrigger.r0(DictionaryEntry):int` calls `getVariable()` exactly once. An integer value uses the real `getIntValue():long` followed by `long-to-int`; a decimal uses the real `getDecimalValue():double` followed by `double-to-int`; every other contained type, including null, returns zero. A null entry fails at the initial virtual getter call. There is no target call to an alarm API.

The neutral source resolves that exact declared method, checks its declaring class, public/static modifiers and `int` return type, and invokes it through reflection. It never calls a recovered helper or includes a copy of the numeric implementation. All argument objects use the real constructors found on application classes. The selected original integer/decimal constructors store the supplied primitive fields and the final getters read those fields directly. The selected entry constructor stores the supplied contained object; the list fields accept the deliberately supplied null parent-list value. The string and entry constructors reject the null fields that the two exceptional heap-state cases need.

The probe checks that the target uses a non-bootstrap classloader and that all seven related application types use that same loader. This is a useful consistency check, but the later wrapper must still prove the exact probe-plus-one-APK classpath with no preceding or inherited app/stub input. Classloader identity alone is not a standalone byte-origin proof.

For each of the 547 direct integer and 734 direct decimal cases, a real getter readback must preserve the exact input long/double bits before the target is invoked. Any raw-bit alteration, including one affecting a NaN payload, fails the probe instead of silently changing that case. No Android behavior of that conversion/reflection path has yet been observed.

## Explicit unusual states and one documentation refinement

`null-value` first constructs a valid private entry, writes its `variable` field to null and verifies that the real outer getter returns null. `string-null` constructs a valid string object, writes its `textValue` field to null and reads that field back. These are the only two reflective field mutations, and they affect newly created disposable argument objects. They do not claim that the original constructors accept null or that the states are reachable through ordinary app UI.

The design README's statements that every integer/decimal getter and every contained identity is observed should be read more narrowly. The actual direct numeric cases have bit readbacks, and every non-null outer entry checks its contained-object identity. The `nested-entry` case creates a real integer value 91 inside a real nested entry but does not separately read that inner getter or inner reference. Those inner fields follow the exact reviewed constructors, and `r0` only sees the outer contained `DictionaryEntry` type before returning zero. This wording refinement is not a target-semantic blocker; the frozen source and original README remain unchanged.

## Exception/output boundary and pending runtime requirements

Only the declared `null-entry` case accepts the exact `java.lang.NullPointerException` class from the real reflected target. A normal result for that case fails. A different exception, a subclass or an unexpected exception in another case also fails. Target exceptions are unwrapped from `InvocationTargetException`; construction and other direct failures are not swallowed.

The null-entry message is preserved as either the literal null marker or every UTF-16 code unit in hexadecimal, including empty strings, control characters and surrogate units. That is lossless representation, not message normalization. Only this one VM-generated message is excluded from equality requirements; its raw form must remain in the eventual evidence.

The inventory branch accepts only the single `--inventory` argument and loads no app type. The runtime branch requires zero arguments, visits every input in fixed order, and prints a fixed begin line, one observation per case and an end line only after all 1,291 cases complete. It exposes no case-selection or retry mode. A partial run must remain a failure with its partial output preserved.

Root is separately authoring the bounded wrapper. Its later review must bind both APKs, this exact DEX and the actual guest binary/device, use separate original and candidate processes with verification enabled, enforce the full output/corpus contract, retain raw streams and both pre/post input identities, and clean only the owned guest directory. That wrapper/workflow and actual Android result remain pending. This review grants no runtime parity, recovered-method, alarm, UI or application-promotion credit.
