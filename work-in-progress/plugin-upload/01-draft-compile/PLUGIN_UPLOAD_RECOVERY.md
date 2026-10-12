# Plugin upload coroutine recovery

## Draft compile checkpoint

This separate private workstream contains a readable Java draft for
`com.arlosoft.macrodroid.plugins.k.invokeSuspend(Object)` and controlled host
boundary types. All 23 authored Java files compile with Java 21 targeting Java 8,
using the frozen 1,240-body plugin-lookup host classes as their classpath.
The draft is not yet registered for transplantation. Original/JVM comparisons,
instruction and branch coverage, a signed rebuilt APK, independent roundtrip and
deliberate-fault controls are still pending. No equivalence claim follows from this
compile check.

The original body is preserved in
`source/smali/classes3/52/k_5259e6b9bbdca2b7.smali`, SHA-256
`e1e358c48fd74e5bff3dae102917559cbc463795413aa0d329f3bede881609fe`.
It has 526 smali lines, 163 instructions, 13 conditional branches and six catch
declarations. The baseline is the frozen plugin-lookup checkpoint04, whose signed
proof is preserved separately and whose source, reports and artifact remain unchanged.

## Semantics to verify

The entry label selects initial invocation or one of two API resumptions. Label 1
casts five stored object fields, in order, outside the `Exception` handler. Label 2
casts the saved upload body and icon string outside that handler. These casts must
remain observable even though their values are unused. Initial-result checking is
also outside the handler; resumed-result checking is inside it. Invalid labels call
the original guard and retain its defensive return.

When a drawable is present, the body obtains a bitmap, compresses it as PNG with
quality 100 into a byte stream, and ignores the compression Boolean. The request-body
companion is captured before the media-type companion is checked. Parsing
`image/*` has a nested `IllegalArgumentException` handler that supplies a null media
type. Other `Exception` values reach the outer handler, while `Error` escapes.
The original byte-array null check, request-body arguments, `icon` multipart name,
continuation-field clearing order and label-1 write precede the icon upload.

The upload payload captures the current user ID, then the original name, developer,
description, package, download link, selected icon URL, website and `en` language.
A null returned icon uses the stored icon URL. The owner/API and hash are then read
again before all five object fields are cleared and label 2 is stored. Both API
suspension comparisons use object identity. A successful upload publishes a newly
constructed success payload to the sink captured before payload construction.

The error path reads an HTTP exception's status twice, first for 409 and then for
403. The first result has priority when both tests succeed. A denied upload sets the
captured owner's denial flag before reading its sink. The generic error publication
precedes the logger companion check and logger call. Failures in the handler itself
must escape. This body does not reset the lookup attempt counter.

## Host boundaries and shared-stub changes

The framework and API doubles expose arguments, call order, continuation state and
partial effects for the forthcoming differential cases. Bitmap compression is a
scripted byte-write boundary; it does not encode real Android pixels. No upload,
network request, scheduler, analytics endpoint or Android lifecycle is executed.
Only the selected compiled body can become an APK candidate; none of these doubles
or helper classes may enter the application.

The two shared-stub edits are narrow: `plugins.b` adds the original typed API and
user-provider fields, and `PluginControl` adds an optional continuation snapshot
callback used only when its existing lookup-continuation field is absent. Reset
clears that callback. The original lookup snapshot behavior stays intact. There
are no upload-specific changes to `u2f.P`, `e6d.r`, `hb9`, or the HTTP exception stub.

The private working directory currently holds only small draft files. Materializing
the full preserved source is deferred until the shared disk cleanup is complete.
The closed scene build cache was removed after its source, signed APK and complete
proof were confirmed durable; the separate cleanup receipt records exactly that
reproducible-cache removal.
