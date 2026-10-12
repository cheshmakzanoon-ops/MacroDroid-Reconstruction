# Constructor owner compatibility prototype

This inactive checkpoint addresses one verified original allocation pattern: `new-instance Lzhh;` followed by the public direct-parent `Lrff;-><init>(ILm73;)V`. It does not modify the active application or claim Android execution.

Twenty host regressions pass. An independent extraction from the SHA-pinned original APK matches the preserved WidgetUpdateManager, zhh, and rff classes byte for byte. The standalone Java helper passes a host allocation check, actual D8 compilation, a guarded one-owner correction, and an exact smali-to-DEX-to-smali round trip. The final 1,436-byte DEX contains one helper class and no compile-only stubs. Its SHA-256 is `85f53ad51a1a85fd2161bd485db9f12556f737b0745f6e26ffdff31a927d5281`.

The correction checks the pinned original method, unchanged allocated type, concrete direct superclass, absence of child constructors, public parent constructor, exact occurrence counts, and physical register aliases. It rejects unsupported control flow and intervening instructions. No runtime constructors are synthesized. The first failed host-test attempt and subsequent corrected runs are retained.

Next required proof: execute the standalone helper on Android against the unchanged original APK classes. This checkpoint has not yet been integrated into the application build, migration verifier, or linkage verifier.
