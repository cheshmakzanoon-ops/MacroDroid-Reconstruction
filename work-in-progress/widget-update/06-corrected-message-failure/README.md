# Corrected Widget inventory: one-message host failure preserved

The metadata correction changes only the two omitted count/provenance inputs.
All 259 Python tests now pass. The hybrid build, complete code round trip and
resource comparison pass again with the identical signed APK (`b79b0010…`).
That APK is retained in the adjacent `06-initial-signed-failure/apk/` multipart
artifact; this checkpoint does not create another APK copy or promote it.

The actual three-way UI run executes 20,818 cases across nine methods and finds
exactly one mismatch, `widget-saved-cast:1:3:false`. All Widget instructions and
conditional edges are visited, with zero unsupported executions or independent
expected-result failures. The original and rebuilt DEX paths produce a literal
null exception-message log; the direct Java path produces the helpful JVM null
receiver text already handled by the narrowly scoped normalizer. Their remaining
observations are identical. The complete failed JSON is retained unchanged.

The default JDK fast-throw optimization is a candidate explanation, to be tested
in a separate unchanged-classpath experiment. This checkpoint does not expand
message normalization, assert a passing three-way result, or claim Android parity.
All 81,264 corrected input files were rehashed before freezing. The 32 exact
delta inputs, complete input manifest, corrected scripts, every closed report,
all command logs, and metadata-correction history are preserved with hashes.
