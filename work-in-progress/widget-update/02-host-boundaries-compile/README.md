# Widget update recovery in progress

The candidate is `WidgetUpdateManager.m(Context, List, o73): Object`, pinned to original method SHA-256 `a1dd490bbfd6837fa72e6bf8ae4c75736612989fcba050fe2f0582aa03640e34`. The original class was extracted independently from the supplied APK and matched to preserved source in the constructor-owner checkpoint.

The translation and its host boundaries now compile with the existing recovered source and controlled dependencies: 802 Java input files, Java 8 bytecode target, JDK 21, exit code 0. The exact command, all input hashes, complete compiler log and generated host-class archive are preserved in `reports/02-host-*`. The 18 authored overlay paths are separately identified in the compile manifest. No active application source was changed by this study and no Widget method is registered.

The new host boundaries observe continuation slots, object identities, provider reads, manager/renderer/factory creation, both suspending calls, logging, injected failures and dependency mutations. They do not implement Android widgets, rendering, scheduling or services. Compilation alone does not establish behavioral equality. Original-instruction/JVM/rebuilt differential cases, instruction and branch coverage, deliberate fault controls and application DEX integration remain pending.

The original allocates `Lzhh;` and calls `Lrff;-><init>(ILm73;)V`. The independently reviewed constructor-owner pipeline restores only that pinned owner after Java compilation, preserving the allocated type and adding no runtime constructor. The host stub's child constructor is compile-only. The bounded interpreter must validate an explicit method-scoped adapter before using host reflection for this original instruction; its Android legality is checked independently by the pending ART probe.

The translation retains continuation reuse and high-bit clearing, both suspension labels, otherwise unused casts on restored fields, clearing of continuation slots, iterator ordering, the per-widget Exception boundary, logging outside that boundary, and the original unchanged saved index. These are implementation aims awaiting differential proof, not runtime claims.
