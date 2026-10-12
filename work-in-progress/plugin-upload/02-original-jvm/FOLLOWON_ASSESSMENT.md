# Follow-on method assessment

## Completed isolated recovery: plugin lookup coroutine

`com.arlosoft.macrodroid.plugins.j.invokeSuspend(Object)` has completed its isolated signed original/JVM/rebuilt proof: 3,053 plugin cases, all 198 original instructions and 34 conditional edges, all 37 UI fault controls and clean positive restoration. See `PLUGIN_RECOVERY.md` for the complete scope, source/APK identities and preserved diagnostics. The method retains the original user-not-allowed/known-package/attempt-limit guards, both suspension labels, continuation fields, typed lookup result publication, analytics ordering, repeated status-code reads, and narrow exception ranges. The original retry block repeatedly reads key index 0. This behavior is retained rather than repaired. No real API, credential, analytics endpoint or coroutine scheduler is contacted by host tests.

The full signed scene proof remains frozen in the separate scene-recovery directory. This follow-on isolation does not modify current, restored, or the frozen scene source/reports.

## Current recovery: plugin upload coroutine

The next ordinary application method is `com.arlosoft.macrodroid.plugins.k.invokeSuspend(Object)`, preserved in `source/smali/classes3/52/k_5259e6b9bbdca2b7.smali`. Its selected body has SHA-256 `e1e358c48fd74e5bff3dae102917559cbc463795413aa0d329f3bede881609fe`: 526 smali lines, 163 instructions, 13 conditional branches and six catch declarations. This method is now recovered in a separate private upload workstream. Its original/JVM comparison passes 2,356 upload cases with all 163 instructions and 26 conditional edges, while signed rebuilt proof and behavioral deliberate-fault execution remain pending. See `PLUGIN_UPLOAD_RECOVERY.md` for current scope and evidence.

The body handles optional icon conversion/upload, constructs the plugin upload payload, suspends at two API boundaries, and publishes success or the original duplicate/denied/connection-error result. Recovery must preserve the five continuation-object casts and their exception positions, ignored bitmap-compression return, nested media-type parsing catch, field-clearing order, current-owner reads, suspension identity, repeated HTTP status reads and error-handler side effects. Unlike the deferred Widget allocation, its constructor calls use the allocated classes directly. Controlled API and framework boundaries can exercise these semantics without contacting an endpoint. The upload workstream uses a new private working directory and leaves the frozen lookup proof unchanged.

## Deferred tooling gap: WidgetUpdateManager.m

The preserved original method allocates a subclass and directly invokes its superclass constructor:

```smali
new-instance v9, Lzhh;
invoke-direct {v9, v5, v6}, Lrff;-><init>(ILm73;)V
```

The allocation occurs in `source/smali/classes/67/WidgetUpdateManager_6791e8994482f6df.smali`, method `m(Landroid/content/Context;Ljava/util/List;Lo73;)Ljava/lang/Object;`. The preserved class in `source/smali/classes/c2/Lzhh_c22737dc2c4c675a.smali` extends `Lrff;` and declares **no constructor**. Its own `create` method uses the same superclass-constructor allocation pattern. `Lrff;` declares `<init>(ILm73;)V` in `source/smali/classes7/d2/Lrff_d2448d30d4685e58.smali`.

A normal Java expression `new zhh(2, null)` would require an invented compile-only subclass constructor and emit a reference to `Lzhh;-><init>(ILm73;)V`, which the preserved application does not declare. When this gap was first assessed, `validate_migration.py` intentionally did not resolve constructors by inheritance and `build.py` copied compiled bodies without a constructor-owner alias facility. A helper or stub constructor cannot be added to the APK under the current reconstruction rules.

This was a precise gap in the plain Java-body transplant pipeline. It is not a claim that the original allocation is invalid or that the method is unrecoverable. Addressing it would require a narrowly specified constructor-owner transformation, verified against the original allocation/hierarchy and tested independently, with an Android verification layer. A separate parent-owned workstream is addressing the gap with a narrowly pinned correction and an independent ART probe; its status and validation are reported there. No constructor-owner rewrite, reflection workaround, extra runtime helper, or baseline-smali change is introduced or validated by this plugin recovery.
