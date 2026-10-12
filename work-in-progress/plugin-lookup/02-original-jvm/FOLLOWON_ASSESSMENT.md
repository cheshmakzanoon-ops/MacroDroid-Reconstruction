# Follow-on method assessment

## Selected recovery: plugin lookup coroutine

`com.arlosoft.macrodroid.plugins.j.invokeSuspend(Object)` is being recovered in this separate isolation from the frozen 1,239-body scene candidate. The method retains the original user-not-allowed/known-package/attempt-limit guards, both suspension labels, continuation fields, typed lookup result publication, analytics ordering, repeated status-code reads, and narrow exception ranges. The original retry block repeatedly reads key index 0. This behavior is retained rather than repaired. No real API, credential, analytics endpoint or coroutine scheduler is contacted by host tests.

The full signed scene proof remains frozen in the separate scene-recovery directory. This follow-on isolation does not modify current, restored, or the frozen scene source/reports.

## Deferred tooling gap: WidgetUpdateManager.m

The preserved original method allocates a subclass and directly invokes its superclass constructor:

```smali
new-instance v9, Lzhh;
invoke-direct {v9, v5, v6}, Lrff;-><init>(ILm73;)V
```

The allocation occurs in `source/smali/classes/67/WidgetUpdateManager_6791e8994482f6df.smali`, method `m(Landroid/content/Context;Ljava/util/List;Lo73;)Ljava/lang/Object;`. The preserved class in `source/smali/classes/c2/Lzhh_c22737dc2c4c675a.smali` extends `Lrff;` and declares **no constructor**. Its own `create` method uses the same superclass-constructor allocation pattern. `Lrff;` declares `<init>(ILm73;)V` in `source/smali/classes7/d2/Lrff_d2448d30d4685e58.smali`.

A normal Java expression `new zhh(2, null)` would require an invented compile-only subclass constructor and emit a reference to `Lzhh;-><init>(ILm73;)V`, which the preserved application does not declare. The existing `validate_migration.py` intentionally does not resolve constructors by inheritance. The existing `build.py` transplant copies the compiled method body without a constructor-owner alias facility. A helper or stub constructor cannot be added to the APK under the current reconstruction rules.

This is a precise gap in the present Java-body transplant pipeline. It is not a claim that the original allocation is invalid or that the method is unrecoverable. Addressing it would require a narrowly specified constructor-owner transformation, verified against the original allocation/hierarchy and tested independently, with an Android verification layer. No such rewrite, reflection workaround, extra runtime helper, or baseline-smali change is introduced in this plugin recovery.
