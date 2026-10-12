# Widget D8 and linkage prerequisites: inactive checkpoint

The fresh private study copied and hash-checked all 81,245 published active inputs,
with no hardlinks or generated caches. It added the frozen Widget helper and host
boundaries, the reviewed original/JVM case harness and strict oracle, two explicit
constructor/numeric conformance fixtures, and exactly one migration registry entry.
The resulting candidate has 1,241 Java bodies across 604 classes and 9 UI methods.

All six preparation commands passed: extractor bootstrap, fresh full original
fixture extraction, candidate input recording, actual javac/D8/disassembly, static
migration validation, and linkage validation. The 81,264 candidate input files have
canonical SHA-256 `a729f01fc4b0dc136c980501c144b43769332c324f8c6f63438107d605291691`.
The full original-method fixture is test-only and is never an APK build input.

The actual D8 body uses `new-instance Lzhh;` and a non-range direct constructor
call. The guarded pipeline restores exactly one owner reference from `Lzhh;` to
the original `Lrff;-><init>(ILm73;)V`. Static validation checks 633 distinct member
references and resolves 427 application members, with no new external references
or errors. Both verifiers produce the identical source-bound correction record;
no allocated type changes and no constructor is added. The narrow guard needed no
range-call extension. Exact D8 output, input JAR, disassembly and logs are retained.

This checkpoint does not activate the method and does not contain a newly built
application APK. The five-command signed/code/resource/three-path/input-integrity
study is separate ongoing work. Method-only deliberate-fault controls, the earlier
two-path Widget study and the independently verified ART allocation probe each
retain their distinct scopes. No whole-application 1:1 result is asserted.
