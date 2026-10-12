# Combined plugin upload and Widget source recovery

## Source and behavior

`PluginUploadMethods.upload` supplies the body of `plugins.k.invokeSuspend(Object)`.
It preserves the optional icon path, the ignored PNG compression return value,
captured request companion, original default-argument mask, icon fallback, both
suspension labels and identity checks, saved-field casts/clearing, repeated HTTP
status reads, success/error publication order and the original Exception boundaries.
Controlled host dependencies perform no network request or real coroutine scheduling.

`WidgetUpdateMethods.update` supplies `WidgetUpdateManager.m(Context,List,o73)`.
It preserves high-bit continuation reuse/clearing, labels 0/1/2, original saved-field
casts including otherwise unused reads, the unchanged saved index, ordered state
writes and identity-based suspension handling. It retains the original Exception-only
catch. Logger and exception-message failures still escape, and the caught message
is read before the StringBuilder is allocated. The Java helper uses explicit original
owners where required; no helper or host-stub class is shipped in the APK.

The one declared constructor-owner mapping translates the compiled `zhh` child
constructor reference back to the original direct-parent `rff` owner. Allocation
type and original constructors remain unchanged. Build, static and linkage checks
share the existing source/domain/descriptor/occurrence guards. This is the first
active mapping in this registry; earlier published methods had zero.

## Independent completed evidence

The isolated upload proof passed 191,147 cases over 1,241 methods and three paths,
all 54 UI faults and exact 20,832-case restoration, full code verification and
resource/native payload checks. Its signed APK is
`e4643b554429743703bed5c1aa5e3541dbfc0705d9fd87c353bd968f348baf80`.
The original upload method visited all 163 instructions and 26 conditional edges.

The isolated Widget signed proof passed all five planned gates, 191,133 cases over
1,241 methods and three paths, and all 265 Python tests. Its signed APK is
`b79b0010285733e4ed27d50590786e5e87f943ad6d15aeeef445d2b2c750f82f`.
The Widget cases cover all 194 original instructions and 20 conditional edges.
The earlier independent study rejected 24 actual compiled method faults plus two
class-origin controls. These finite host studies are not Android feature execution.

The original constructor-only ART probe succeeded with `-Xverify:all` on the
pinned API 35 emulator. The separate original/isolated-Widget method probe also
passed all eight cases in hosted run 38209599059: each guest exited zero, with
379 bytes of identical stdout and empty stderr. All 7,214 artifact members,
including the exact hidden workflow, and all 19 executed input copies were
independently verified. See [the complete ART proof](../work-in-progress/widget-art/08-hosted-complete-proof/).
These cases cover empty/resumed lists, invalid labels, saved-field casts and a
null list; they do not render a Widget or cover nonempty lists, services,
scheduling, complete lifecycle behavior, or this new combined APK.

## Host exception policy and execution budgets

A full Widget UI run exposed one mismatch caused by the default HotSpot fast-throw
optimization omitting the message at a warmed reflection call site. The unchanged
901-file classpath/fixture/APK experiment passed all 20,818 cases when that omission
was disabled. No literal-null message normalization was added. Injected exceptions,
external lookalike messages and explicit null observations remain checked.

The UI positive, deliberate-fault and restoration commands all use and verify
`-XX:-OmitStackTraceInFastThrow` and `-XX:+ShowCodeDetailsInExceptionMessages`.
The report binds the actual Java executable, HotSpot library and effective values.
Six adversarial runtime-policy tests and eight mutation-catalog tests accompany it.
Constructor and AND_INT interpreter extensions retain their separate conformance
fixtures and strict, explicit host-only constructor adapter.

The actual 54-fault upload gate took 1,962.871 seconds on this host. The combined
78-fault suite therefore has a recorded 5,400-second outer budget; every actual UI
execution, including the last clean rerun, is independently limited to 300 seconds.
Other acceptance gates retain their 1,200-second budget. The proposed source CI job
allows 120 minutes and preserves every report, nested mutant artifact and final APK.
Changing a time budget does not change any required outcome or comparison rule.

## Completed combined host and artifact proof

The independent source preparation verified all 81,245 baseline inputs before
and after copying, applied only the frozen reviewed changes, and freshly extracted
the original fixture for 1,242 methods across 605 classes. The resulting 81,291
inputs retained the same pin before and after all 16 configured acceptance gates:

`b8eccfa12bc6bf0111616b2b5e812c921ca95568e019b769582041d8c852b553`

The complete run passed 193,489 cases on all three paths, including 23,174 UI cases
across ten methods, 15,326 independent UI expectations, 273 Python tests and all
78 deliberate UI faults. The signed source-edit experiment and final complete
positive run both passed. The wrapper independently checked all 16 gate logs,
22 fresh report hashes, every retained mutant source/class pair, and both final
signed APK identities. The closed [result](../work-in-progress/combined-recovery/05-full-acceptance/result.json) and
[complete report manifest](../work-in-progress/combined-recovery/05-full-acceptance/complete-reports-manifest.json) preserve
the actual outcomes; the configured acceptance subprocess took 4,800.347 seconds.

The 94,683,119-byte combined APK SHA256 is
`5f635e165479895cabc4608a0a82452b99a62bf9f9b03cb09b1ac5e3a45e5182`.
Its separate Android measurements and clean hosted reproduction remain pending.
The isolated Widget and upload reports retain their own source/APK identities.

The reference APK, original selected fixture, historical reference Java and host
stubs remain separate from application build inputs. Most application logic is
preserved editable smali. Native libraries and opaque assets remain original binary
dependencies. This work does not recover the publisher's signing identity or claim
whole-application 1:1 behavior.
