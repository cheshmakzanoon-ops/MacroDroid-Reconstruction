# Widget oracle and existing-method regression: inactive checkpoint05

The strict constructor-owner oracle is extended with the original Widget method's three-register AND_INT operation. Exactly one opcode case was added; the explicit method/child/parent/descriptor/occurrence guards remain intact. This checkpoint also refines the draft Widget helper to preserve the original referenced method owners and exception-message/StringBuilder order. No active registry or candidate APK is changed here.

## Actual closed measurements

* All 4,546 independent bitwise conformance cases passed, covering all 32-by-32 single-bit pairs, signed boundary patterns, both destination aliases, and the continuation high-bit mask. Expected values use independent per-bit arithmetic and fixed truth-table results.
* All 16 constructor boundary cases were rerun with this exact oracle and passed.
* All three existing primitive/numeric conformance suites passed.
* All 188,791 existing original/JVM/signed-rebuilt cases passed across all 1,240 registered methods, with zero failures or unsupported executions. The five suite method-key lists exactly partition the registry.
* The launcher verified the actual loaded strict-oracle class location. Every existing application suite had zero parent-constructor adapter rules and zero adapter calls. All baseline compiled class hashes were rechecked unchanged after execution.

The previous launcher failed after the local-variable UI numeric conformance because it assumed every suite exposed a static oracle field. Checkpoint03 preserves that failure. This follow-up permits exactly that already-existing local numeric fixture while retaining mandatory inspection for all five application suites. The complete corrected run is preserved in reports/existing-oracle-regression-05, including all commands, source copies, exact copied DEX hashes, baseline class inventories and cleanup receipt. Each copied rebuilt DEX was verified byte-for-byte against the pinned signed9108 APK before execution. This is not a new APK build or a full acceptance run.

## Independent Android prerequisite

The hosted run38200503458 separately verified the original Lzhh allocation through the original public Lrff constructor on recorded API35 ART under -Xverify:all. Its single-class1436-byte probe had no compile stubs on its runtime classpath; the exact original APK and probe were device-hashed, set read-only and cleaned up. The root independently reran the frozen verifier and verified all24 command stdout/stderr hash pairs. The reference receipt is reports/oracle-conformance-05/art-reference-recheck.json; complete raw Android evidence is preserved separately by that hosted-run checkpoint. This narrow allocation result is not a Widget behavior proof.

## Source scope

The draft helper now calls Iterable.iterator, rx6.d and Throwable.getMessage through explicit static types, and reads each exception message before allocating StringBuilder with the original prefix constructor. The method's original dead casts, literal saved index, state write order and exception ranges remain explicit. The full Widget body and its own malformed-null-receiver host-message boundary are tested in separate Widget04 studies. The unchanged old helper source and failed intermediate studies remain preserved at their original hashes.
