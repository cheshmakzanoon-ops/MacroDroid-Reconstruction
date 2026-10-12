# Widget update recovery in progress

The candidate method is `WidgetUpdateManager.m(Context, List, o73): Object`, pinned to original method SHA-256 `a1dd490bbfd6837fa72e6bf8ae4c75736612989fcba050fe2f0582aa03640e34`. Its class was independently extracted from the original APK and matched to the preserved source in the constructor-owner checkpoint.

The Java file is an inactive first translation. It has not yet passed compilation, differential cases, instruction coverage, deliberate fault controls, an application DEX round trip, or Android execution. It must not replace active application code until the required checks pass.

The translation preserves continuation reuse and high-bit clearing, both suspension labels, the otherwise unused casts on restored continuation fields, clearing of continuation slots, iterator ordering, the per-widget exception boundary, logging outside that boundary, and the original unchanged saved index. It contains no new runtime helper calls.

The original method allocates `Lzhh;` and invokes its public direct-parent `Lrff;-><init>(ILm73;)V`. A separately reviewed, explicit constructor-owner mapping is required after Java compilation. The compatibility prototype has passed standalone D8 round trips; Android verification remains a separate required result. Compile-only constructors are excluded from the application.

Next work is to compile this translation against isolated host-only boundaries and compare actual original instructions, Java execution, and rebuilt DEX with complete instruction/conditional-edge coverage and injected-failure controls.
