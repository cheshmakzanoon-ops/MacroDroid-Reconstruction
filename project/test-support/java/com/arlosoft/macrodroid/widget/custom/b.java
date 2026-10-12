package com.arlosoft.macrodroid.widget.custom;

import defpackage.WidgetControl;
import defpackage.o73;

/** Host-only continuation storage; resumes are driven explicitly by test cases. */
public class b extends o73 {
    public int label, I$0, I$1, I$2;
    public Object L$0, L$1, L$2, L$3, L$4, L$5, L$6, L$7, result;
    public WidgetUpdateManager this$0;
    public o73 completion;
    public b(WidgetUpdateManager owner, o73 completion) {
        this.this$0 = owner; this.completion = completion;
        WidgetControl.name(this, "continuation" + WidgetControl.continuations.size());
        WidgetControl.continuations.add(this); WidgetControl.current = this;
        WidgetControl.hit("continuation.new:" + WidgetControl.id(this) + ":" + WidgetControl.id(owner) + ":" + WidgetControl.id(completion));
    }
}
